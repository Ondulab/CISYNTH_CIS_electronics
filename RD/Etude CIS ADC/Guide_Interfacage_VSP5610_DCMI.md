# Guide d'Interfaçage VSP5610 avec DCMI STM32

## Table des Matières
1. [Introduction](#introduction)
2. [Analyse du Projet AD922x avec DCMI](#analyse-du-projet-ad922x-avec-dcmi)
3. [Principe de l'AD9226](#principe-de-lad9226)
4. [Adaptation au VSP5610](#adaptation-au-vsp5610)
5. [Rôle de HSYNC et VSYNC](#rôle-de-hsync-et-vsync)
6. [Empaquetage des Données dans le DCMI](#empaquetage-des-données-dans-le-dcmi)
7. [Options de Configuration HSYNC](#options-de-configuration-hsync)
8. [Modes de Capture DCMI](#modes-de-capture-dcmi)
9. [Configuration Recommandée](#configuration-recommandée)
10. [Code d'Implémentation](#code-dimplémentation)

---

## Introduction

Ce document récapitule l'étude de faisabilité pour interfacer le **VSP5610** (AFE pour CIS) avec le périphérique **DCMI** (Digital Camera Interface) d'un STM32, en s'inspirant du projet open-source **Driving-AD922x-with-DCMI**.

### Paramètres du Système Cible
| Paramètre | Valeur |
|-----------|--------|
| CIS | 600 DPI |
| Fréquence MCLK | 8 MHz |
| Nombre de canaux | 3 (RGB) |
| Flux par canal | 8 Msps |
| **Flux total** | **24 Msps** (8 Msps × 3) |
| Résolution ADC | 16 bits |

---

## Analyse du Projet AD922x avec DCMI

### Concept du Projet
Le projet **Driving-AD922x-with-DCMI** démontre qu'il est possible d'utiliser le DCMI (normalement conçu pour des caméras) pour capturer des données d'un ADC haute vitesse comme l'AD9226.

### L'Astuce Principale
**HSYNC et VSYNC sont forcés à GND (masse)**, ce qui fait que le DCMI capture **en continu** toutes les données présentes sur le bus.

```
Configuration dans le projet AD922x :

DCMI_InitStructure.DCMI_VSPolarity = DCMI_VSPolarity_High;  // VSYNC actif haut
DCMI_InitStructure.DCMI_HSPolarity = DCMI_HSPolarity_High;  // HSYNC actif haut

// Câblage : HSYNC et VSYNC → GND
// Résultat : Ces signaux sont toujours "inactifs" → capture continue
```

---

## Principe de l'AD9226

### Caractéristiques Clés
| Paramètre | Valeur |
|-----------|--------|
| Résolution | 12 bits |
| Taux d'échantillonnage max | 65 MSPS |
| Interface de sortie | Parallèle 12 bits (D0-D11) |
| Horloge | Externe, fournie par l'utilisateur |
| Latence pipeline | 7 cycles d'horloge |

### Timing de l'AD9226
```
CLK     ────┐   ┌───┐   ┌───┐   ┌───┐   ┌───┐
            │   │   │   │   │   │   │   │   │
            └───┘   └───┘   └───┘   └───┘   └───┘
            ↑                               
            │ Échantillonne sur front montant
            │
D[11:0]     ├─── Données valides sur front descendant ───►

TOD (Output Delay) = 3.5 à 7 ns après front descendant CLK
```

### Schéma de Connexion AD9226 ↔ DCMI
```
                 STM32F4 (DCMI)                    AD9226
                 ──────────────                    ──────
                 
    MCO1 (PA8) ─────────────────────────────────► CLK
    
    DCMI_PIXCLK ◄───────────────────────────────── CLK (même signal)
    
    DCMI_D0-D11 ◄──────────────────────────────── D0-D11
    
    DCMI_HSYNC  ◄────── GND ◄─────────────────── Forcé bas
    DCMI_VSYNC  ◄────── GND ◄─────────────────── Forcé bas
```

---

## Adaptation au VSP5610

### Différences Clés AD9226 vs VSP5610

| Aspect | AD9226 | VSP5610 |
|--------|--------|---------|
| Largeur données | 12 bits natif | 8 bits (16 bits en 2×8) |
| Horloge données | Externe (CLK) | Interne (CK0, dérivée de MCLK) |
| Contrôle acquisition | Continu | XLSYNC déclenche ligne |
| Multiplexage | Non (1 canal) | Oui (jusqu'à 4 canaux) |
| Format sortie | Parallèle simple | MSB puis LSB par pixel |

### Schéma de Connexion VSP5610 ↔ DCMI
```
                 STM32 (DCMI)                     VSP5610
                 ────────────                     ───────
                 
    GPIO (PWM) ─────────────────────────────────► MCLK (RCLKP)
    
    GPIO (Output) ──────────────────────────────► XLSYNC
    
    DCMI_PIXCLK (PA6) ◄─────────────────────────── CK0
    
    DCMI_D[7:0] ◄───────────────────────────────── D[7:0]
    
    DCMI_HSYNC (PA4) ◄────── GND ────────────────── Forcé bas
    DCMI_VSYNC (PB7) ◄────── GND ────────────────── Forcé bas
```

---

## Rôle de HSYNC et VSYNC

### Sémantique dans le DCMI
- **HSYNC** (Horizontal Sync) : Synchronisation de **ligne** → blanking entre pixels
- **VSYNC** (Vertical Sync) : Synchronisation de **frame** → blanking entre images

### Comportement selon Polarité et Niveau

| Signal | Polarité Config | Niveau Physique | Effet |
|--------|-----------------|-----------------|-------|
| HSYNC | High | HIGH | Pause capture |
| HSYNC | High | LOW | Capture active |
| VSYNC | High | HIGH | Pause capture |
| VSYNC | High | LOW | Capture active |

### Pourquoi GND fonctionne
```
Configuration :
  DCMI_HSPolarity = High (actif sur niveau haut)
  DCMI_VSPolarity = High (actif sur niveau haut)

Câblage :
  HSYNC → GND (niveau bas permanent)
  VSYNC → GND (niveau bas permanent)

Résultat :
  → Les signaux ne sont JAMAIS "actifs"
  → Le DCMI capture EN CONTINU
```

---

## Empaquetage des Données dans le DCMI

### Mode 8 bits : Accumulation Automatique

Le DCMI accumule les bytes reçus dans un registre 32 bits avant de déclencher le DMA :

```
Cycle PIXCLK:    │  1  │  2  │  3  │  4  │
                 │     │     │     │     │
D[7:0] entrant:  │ B0  │ B1  │ B2  │ B3  │
                 
                          ▼
                          
DCMI_DR (32b):   │  B3   │  B2   │  B1   │  B0  │
                 │31-24  │23-16  │15-8   │7-0   │
                 └───────────────────────────────┘
                 
Après 4 cycles → DMA Request → Transfert vers RAM
```

### Ordre des Bytes en Mémoire
```
Attention : L'ordre est inversé !

Réception :     B0 → B1 → B2 → B3
En mémoire :    Addr+0: B0, Addr+1: B1, Addr+2: B2, Addr+3: B3

Mais dans le mot 32-bit lu par le CPU :
  uint32_t data = *(uint32_t*)addr;
  data = 0xB3B2B1B0  (B3 en MSB, B0 en LSB)
```

### Données VSP5610 en Mémoire

Pour 3 canaux, format MSB-LSB par pixel :
```
VSP5610 envoie :
Cycle:  1    2    3    4    5    6    7    8    9   10   11   12
Data:  CH1  CH1  CH2  CH2  CH3  CH3  CH1  CH1  CH2  CH2  CH3  CH3
       MSB  LSB  MSB  LSB  MSB  LSB  MSB  LSB  MSB  LSB  MSB  LSB
       ├─Pix0─┤  ├─Pix1─┤  ├─Pix2─┤  ├─Pix3─┤  ├─Pix4─┤  ├─Pix5─┤

En mémoire (buffer DMA) :
Addr    Contenu
0x00    CH1_P0_MSB
0x01    CH1_P0_LSB
0x02    CH2_P1_MSB
0x03    CH2_P1_LSB
0x04    CH3_P2_MSB
0x05    CH3_P2_LSB
...
```

---

## Options de Configuration HSYNC

### Option 1 : SANS HSYNC (Recommandé) ✅

**Câblage simple :**
```
DCMI_HSYNC → GND (via résistance pull-down ou trace PCB)
DCMI_VSYNC → GND (idem)
```

**Avantages :**
- Simplicité matérielle maximale
- Pas de synchronisation complexe
- Fiabilité accrue

**Inconvénients :**
- Démultiplexage et reconstitution en logiciel

### Option 2 : AVEC HSYNC (Plus complexe)

**Cas d'utilisation :** Si on veut que le DCMI structure automatiquement les lignes.

**Implémentation possible :**
```
Option A - Câblage interne (Timer) :
  TIM1 génère XLSYNC
  TIM1 trigger → TIM2
  TIM2 compte cycles CK0
  TIM2 génère pulse → DCMI_HSYNC

Option B - Piste externe :
  STM32_GPIO ──┬──► VSP5610_XLSYNC
               │
               └──► STM32_DCMI_HSYNC
```

**Non recommandé** pour la complexité ajoutée sans bénéfice significatif.

---

## Modes de Capture DCMI

### Mode Continuous
```c
DCMI_InitStructure.DCMI_CaptureMode = DCMI_CaptureMode_Continuous;
```

**Comportement :**
```
Données:    ├──L1──┤├──L2──┤├──L3──┤├──L4──┤├──L5──┤
            
DMA Buffer: │────────── Circulaire ──────────│
            │ L1 │ L2 │ L3 │ L4 │ L5 │ L1...│
                                       ↑ Écrasement
```

**Avantages :** Simple, capture continue
**Inconvénients :** Risque de perte de données si CPU lent

### Mode Snapshot (Recommandé pour CIS) ✅
```c
DCMI_InitStructure.DCMI_CaptureMode = DCMI_CaptureMode_SnapShot;
```

**Comportement :**
```
    CPU         DCMI           VSP5610
     │           │               │
     │──Capture──►│               │
     │──XLSYNC────┼───────────────►│
     │           │◄──── Données ──│
     │           │──DMA─►Buffer   │
     │◄─IRQ TC───│               │
     │──Process──│               │
     │           │               │
     │──Capture──►│ (ligne suivante)
```

**Avantages :**
- Contrôle précis ligne par ligne
- Pas de risque de perte de données
- Synchronisation avec XLSYNC

---

## Configuration Recommandée

### Récapitulatif des Choix

| Aspect | Recommandation | Justification |
|--------|----------------|---------------|
| HSYNC | → GND | Simplicité, fiabilité |
| VSYNC | → GND | Idem |
| Mode Capture | Snapshot | Contrôle ligne par ligne |
| Mode DMA | Normal (non circulaire) | Évite écrasement |
| Largeur données | 8 bits | Compatible VSP5610 |

### Câblage Final
```
                 STM32H7                         VSP5610
                 ───────                         ───────
                 
    TIM PWM ─────────────────────────────────► MCLK (8 MHz)
    
    GPIO Out ────────────────────────────────► XLSYNC
    
    DCMI_PIXCLK (PA6) ◄──────────────────────── CK0
    
    DCMI_D0 (PC6)  ◄─────────────────────────── D0
    DCMI_D1 (PC7)  ◄─────────────────────────── D1
    DCMI_D2 (PE0)  ◄─────────────────────────── D2
    DCMI_D3 (PE1)  ◄─────────────────────────── D3
    DCMI_D4 (PE4)  ◄─────────────────────────── D4
    DCMI_D5 (PD3)  ◄─────────────────────────── D5
    DCMI_D6 (PE5)  ◄─────────────────────────── D6
    DCMI_D7 (PE6)  ◄─────────────────────────── D7
    
    DCMI_HSYNC (PA4) ────── [10kΩ] ───► GND
    DCMI_VSYNC (PB7) ────── [10kΩ] ───► GND
```

---

## Code d'Implémentation

### Constantes et Définitions
```c
// Configuration CIS
#define CIS_PIXELS_PER_LINE     7200    // Ajuster selon votre capteur
#define NUM_CHANNELS            3       // R, G, B
#define BYTES_PER_PIXEL         2       // 16 bits = 2 bytes (MSB + LSB)

// Calculs dérivés
#define BYTES_PER_LINE          (CIS_PIXELS_PER_LINE * NUM_CHANNELS * BYTES_PER_PIXEL)
#define DMA_BUFFER_SIZE_WORDS   (BYTES_PER_LINE / 4)

// Buffer DMA (aligné sur 4 bytes)
__attribute__((aligned(4))) uint32_t dma_buffer[DMA_BUFFER_SIZE_WORDS];

// Flag de synchronisation
volatile uint8_t line_ready_flag = 0;
```

### Configuration DCMI
```c
void DCMI_Config(void)
{
    DCMI_InitTypeDef DCMI_InitStructure;
    
    // Activer horloge DCMI
    RCC_AHB2PeriphClockCmd(RCC_AHB2Periph_DCMI, ENABLE);
    
    // Configuration DCMI
    DCMI_InitStructure.DCMI_CaptureMode = DCMI_CaptureMode_SnapShot;
    DCMI_InitStructure.DCMI_SynchroMode = DCMI_SynchroMode_Hardware;
    DCMI_InitStructure.DCMI_PCKPolarity = DCMI_PCKPolarity_Rising;  // Selon timing VSP5610
    DCMI_InitStructure.DCMI_VSPolarity = DCMI_VSPolarity_High;      // VSYNC=GND → jamais actif
    DCMI_InitStructure.DCMI_HSPolarity = DCMI_HSPolarity_High;      // HSYNC=GND → jamais actif
    DCMI_InitStructure.DCMI_CaptureRate = DCMI_CaptureRate_All_Frame;
    DCMI_InitStructure.DCMI_ExtendedDataMode = DCMI_ExtendedDataMode_8b;
    
    DCMI_Init(&DCMI_InitStructure);
}
```

### Configuration DMA
```c
void DMA_Config(void)
{
    DMA_InitTypeDef DMA_InitStructure;
    NVIC_InitTypeDef NVIC_InitStructure;
    
    // Activer horloge DMA2
    RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_DMA2, ENABLE);
    
    // Désactiver DMA pour configuration
    DMA_Cmd(DMA2_Stream1, DISABLE);
    while (DMA_GetCmdStatus(DMA2_Stream1) != DISABLE) {}
    
    // Configuration DMA
    DMA_InitStructure.DMA_Channel = DMA_Channel_1;
    DMA_InitStructure.DMA_PeripheralBaseAddr = (uint32_t)&DCMI->DR;
    DMA_InitStructure.DMA_Memory0BaseAddr = (uint32_t)dma_buffer;
    DMA_InitStructure.DMA_DIR = DMA_DIR_PeripheralToMemory;
    DMA_InitStructure.DMA_BufferSize = DMA_BUFFER_SIZE_WORDS;
    DMA_InitStructure.DMA_PeripheralInc = DMA_PeripheralInc_Disable;
    DMA_InitStructure.DMA_MemoryInc = DMA_MemoryInc_Enable;
    DMA_InitStructure.DMA_PeripheralDataSize = DMA_PeripheralDataSize_Word;
    DMA_InitStructure.DMA_MemoryDataSize = DMA_MemoryDataSize_Word;
    DMA_InitStructure.DMA_Mode = DMA_Mode_Normal;  // Pas circulaire !
    DMA_InitStructure.DMA_Priority = DMA_Priority_High;
    DMA_InitStructure.DMA_FIFOMode = DMA_FIFOMode_Enable;
    DMA_InitStructure.DMA_FIFOThreshold = DMA_FIFOThreshold_Full;
    DMA_InitStructure.DMA_MemoryBurst = DMA_MemoryBurst_INC4;
    DMA_InitStructure.DMA_PeripheralBurst = DMA_PeripheralBurst_Single;
    
    DMA_Init(DMA2_Stream1, &DMA_InitStructure);
    
    // Activer interruption Transfer Complete
    DMA_ITConfig(DMA2_Stream1, DMA_IT_TC, ENABLE);
    
    // Configuration NVIC
    NVIC_InitStructure.NVIC_IRQChannel = DMA2_Stream1_IRQn;
    NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 0;
    NVIC_InitStructure.NVIC_IRQChannelSubPriority = 0;
    NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;
    NVIC_Init(&NVIC_InitStructure);
}
```

### Capture d'une Ligne
```c
void Capture_Line(void)
{
    // 1. Réarmer le DMA
    DMA_Cmd(DMA2_Stream1, DISABLE);
    while (DMA_GetCmdStatus(DMA2_Stream1) != DISABLE) {}
    DMA_SetCurrDataCounter(DMA2_Stream1, DMA_BUFFER_SIZE_WORDS);
    DMA_Cmd(DMA2_Stream1, ENABLE);
    
    // 2. Activer la capture DCMI
    DCMI_Cmd(ENABLE);
    DCMI_CaptureCmd(ENABLE);
    
    // 3. Déclencher XLSYNC (pulse)
    GPIO_SetBits(GPIOX, XLSYNC_PIN);
    for (volatile int i = 0; i < 10; i++) {}  // Petit délai
    GPIO_ResetBits(GPIOX, XLSYNC_PIN);
    
    // 4. Attendre interruption DMA
    // (géré dans DMA2_Stream1_IRQHandler)
}
```

### Gestionnaire d'Interruption DMA
```c
void DMA2_Stream1_IRQHandler(void)
{
    if (DMA_GetITStatus(DMA2_Stream1, DMA_IT_TCIF1))
    {
        DMA_ClearITPendingBit(DMA2_Stream1, DMA_IT_TCIF1);
        
        // Désactiver capture
        DCMI_CaptureCmd(DISABLE);
        DCMI_Cmd(DISABLE);
        DMA_Cmd(DMA2_Stream1, DISABLE);
        
        // Signaler que la ligne est prête
        line_ready_flag = 1;
    }
}
```

### Post-Traitement : Reconstitution des Pixels
```c
void Process_Line_Data(uint8_t* buffer, uint16_t* ch1, uint16_t* ch2, uint16_t* ch3)
{
    // Le VSP5610 envoie : CH1_MSB, CH1_LSB, CH2_MSB, CH2_LSB, CH3_MSB, CH3_LSB, ...
    // 6 bytes par groupe de 3 pixels (un par canal)
    
    for (int i = 0; i < CIS_PIXELS_PER_LINE; i++)
    {
        int offset = i * 6;  // 6 bytes par groupe
        
        // Reconstitution des pixels 16-bit
        ch1[i] = ((uint16_t)buffer[offset + 0] << 8) | buffer[offset + 1];
        ch2[i] = ((uint16_t)buffer[offset + 2] << 8) | buffer[offset + 3];
        ch3[i] = ((uint16_t)buffer[offset + 4] << 8) | buffer[offset + 5];
    }
}
```

### Boucle Principale
```c
int main(void)
{
    // Initialisation système
    SystemInit();
    
    // Configuration périphériques
    GPIO_Config();      // GPIOs pour DCMI et contrôle
    TIM_Config();       // Timer pour MCLK
    DCMI_Config();
    DMA_Config();
    VSP5610_SPI_Init(); // Configuration SPI pour registres VSP5610
    
    // Configurer VSP5610 via SPI
    VSP5610_Configure();
    
    // Démarrer MCLK
    TIM_Cmd(TIMx, ENABLE);
    
    // Buffers pour données traitées
    uint16_t channel1[CIS_PIXELS_PER_LINE];
    uint16_t channel2[CIS_PIXELS_PER_LINE];
    uint16_t channel3[CIS_PIXELS_PER_LINE];
    
    while (1)
    {
        // Capturer une ligne
        line_ready_flag = 0;
        Capture_Line();
        
        // Attendre fin de capture
        while (!line_ready_flag) {}
        
        // Traiter les données
        Process_Line_Data((uint8_t*)dma_buffer, channel1, channel2, channel3);
        
        // Utiliser les données...
        // (envoi USB, stockage, traitement image, etc.)
    }
}
```

---

## Résumé Final

### Points Clés

| Élément | Configuration |
|---------|---------------|
| **HSYNC/VSYNC** | → GND (capture continue) |
| **Mode DCMI** | Snapshot (à la demande) |
| **Largeur données** | 8 bits |
| **Mode DMA** | Normal (non circulaire) |
| **Synchronisation** | XLSYNC déclenche ligne |
| **Post-traitement** | Reconstitution 16-bit + démux 3 canaux |

### Flux de Données
```
1. CPU déclenche capture (DCMI_CaptureCmd)
2. CPU pulse XLSYNC
3. VSP5610 lit ligne CIS et transmet via D[7:0]
4. DCMI empaquète 4 bytes → 32 bits → DMA
5. DMA transfère vers buffer RAM
6. Interruption DMA quand buffer complet
7. CPU reconstitue pixels 16-bit et sépare canaux
8. Répéter pour ligne suivante
```

### Avantages de cette Approche
- ✅ Simplicité matérielle (HSYNC/VSYNC à GND)
- ✅ Contrôle précis ligne par ligne
- ✅ Pas de perte de données
- ✅ Compatible avec la bande passante du DCMI (54 MHz max)
- ✅ Post-traitement logiciel flexible

---

## Références

1. **AN5020** - Introduction to DCMI for STM32 MCUs (STMicroelectronics)
2. **VSP5610** - Datasheet (Texas Instruments)
3. **AD9226** - Datasheet (Analog Devices)
4. **Driving-AD922x-with-DCMI** - Projet GitHub de référence
