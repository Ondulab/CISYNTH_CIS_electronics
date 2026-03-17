# Document de Référence : Interfaçage STM32H747 ↔ VSP5610RSHR ↔ CIS LC3R216N-8008

**Version :** 2.5  
**Date :** 16/03/2026
**Auteur :** R&D Sp3ctra  
**MCU :** STM32H747XIHx  
**ADC/AFE :** VSP5610RSHR (Texas Instruments)  
**CIS :** LC3R216N-8008A (600 DPI, 3 canaux, 5184 pixels)

---

## Table des Matières

1. [Architecture Système](#1-architecture-système)
2. [Qui Pilote Quoi ?](#2-qui-pilote-quoi-)
3. [Interfaçage STM32 ↔ CIS LC3R216N-8008](#3-interfaçage-stm32--cis-lc3r216n-8008)
4. [Interfaçage STM32 ↔ ADC VSP5610](#4-interfaçage-stm32--adc-vsp5610)
5. [Interfaçage ADC VSP5610 ↔ CIS LC3R216N-8008](#5-interfaçage-adc-vsp5610--cis-lc3r216n-8008)
6. [Circuit de Pilotage LEDs (BSS138PW)](#6-circuit-de-pilotage-leds-bss138pw)
7. [Composants à Ajouter autour du VSP5610](#7-composants-à-ajouter-autour-du-vsp5610)
8. [Configuration des Timers STM32](#8-configuration-des-timers-stm32)
9. [Résistances Série sur les Signaux de Contrôle CIS](#9-résistances-série-sur-les-signaux-de-contrôle-cis)
10. [Notes de Routage PCB](#10-notes-de-routage-pcb)
11. [Configuration VSP5610 via SPI](#11-configuration-vsp5610-via-spi)
12. [Séquence Temporelle Complète](#12-séquence-temporelle-complète)
13. [BOM Complète des Composants Additionnels](#13-bom-complète-des-composants-additionnels)
14. [Signaux Manquants / Nets à Créer](#14-signaux-manquants--nets-à-créer)
15. [Réception des Données DCMI et Organisation Mémoire](#15-réception-des-données-dcmi-et-organisation-mémoire)
16. [Analyse de la Connexion Analogique CIS ↔ VSP5610 (CISVREF & Filtres)](#16-analyse-de-la-connexion-analogique-cis--vsp5610-cisvref--filtres)
17. [Hardware — Filtrage & Routage des Signaux Numériques (Horloges + Bus DCMI)](#17-hardware--filtrage--routage-des-signaux-numériques-horloges--bus-dcmi)

---

## 1. Architecture Système

```
┌───────────────────────────────────────────────────────────────────────────────────┐
│                                  STM32H747XIHx                                    │
│                                                                                   │
│  TIM1_CH2 (PA9) ──[22Ω]──┬──────────────────────────────────► CIS CLK (pin 12)    │
│  [CIS_CP, 8 MHz]         │                                                        │
│                          └─────────────────────────────────► VSP5610 RCLKP        │
│                                                                  (pin 28)         │
│  TIM8_CH3 (PC8) ──[33Ω]─────────────────────────────────────► CIS SI (pin 10)     │
│  [CIS_SP]                                                                         │
│                                                                                   │
│  TIM8_CH4 (PI2) ──[33Ω]─────────────────────────────────────► VSP5610 XLSYNC      │
│  [VSP_XLSYNC]                                                    (pin 45)         │
│                                                                                   │
│  SPI4 ───────────────────────────────────────────────────────► VSP5610 SPI        │
│  PE2/PE4/PE5/PE6                                                                  │
│                                                                                   │
│  DCMI D[7:0] ◄───────────────────────────────────────────────  VSP5610 D[7:0]     │
│  PH9/PA10/PG10/PC9/PC11/PI4/PI6/PI7                                               │
│                                                                                   │
│  DCMI_PIXCLK (PA6) ◄──[33Ω]─────────────────────────────────  VSP5610 GPIO2       │
│                                                       (pin 25, LVCK 48 MHz)       │
│  DCMI_HSYNC (PA4) ────[10kΩ]──► GND                                               │
│  DCMI_VSYNC (PI5) ────[10kΩ]──► GND                                               │
│                                                                                   │
│  TIM3_CH1 (PC6)  [CIS_LED_B] ──► Circuit LED Bleue  ──► CIS LEDb (pin 16)         │
│  TIM4_CH2 (PD13) [CIS_LED_R] ──► Circuit LED Rouge  ──► CIS LEDr (pin 15)         │
│  TIM5_CH3 (PH12) [CIS_LED_G] ──► Circuit LED Verte  ──► CIS LEDg (pin 14)         │
└───────────────────────────────────────────────────────────────────────────────────┘
          │                   │  ▲  ▲         │                         │
          │                   │  │  │         │ CLK (8MHz) + SI         │ LEDs
          │                   │  │  │         │                         │
          ▼                   │  │  │         ▼                         ▼
┌──────────────────────┐      │  │  │  ┌───────────────────────────────────────────────┐
│  VSP5610RSHR         │      │  │  │  │  CIS LC3R216N-8008A                           │
│                      │      │  │  │  │                                               │
│  RCLKP (pin 28) ◄────┼──────┼──┼──┼──┼─ CIS_CP (8 MHz, partagé avec CLK CIS)         │
│                      │      │  │  │  │                                               │
│  AIN1 ◄──────────────┼──────┼──┼──┼──┼─ SIG1 (pin 5)  [pixels 1-1728]                │
│  AIN2 ◄──────────────┼──────┼──┼──┼──┼─ SIG2 (pin 3)  [pixels 1729-3456]             │
│  AIN3 ◄──────────────┼──────┼──┼──┼──┼─ SIG3 (pin 1)  [pixels 3457-5184]             │
│  AINGND1/2/3 ◄───────┼──────┼──┼──┼──┼─ VREF (pin 7)  [~800 mV, ref vidéo]           │
│                      │      │  │  │  │                                               │
│  XLSYNC (pin 45) ◄───┼──────┘  │  │  │  CLK (pin 12) ◄── CIS_CP (8 MHz)              │
│                      │         │  │  │  SI  (pin 10) ◄── CIS_SP (pulse 125 ns)       │
│  D[7:0] ─────────────┼─────────┘  │  └───────────────────────────────────────────────┘
│  GPIO2 (LVCK) ───────┼────────────┘
└──────────────────────┘                   
```

---

## 2. Qui Pilote Quoi ?

### Le STM32 pilote directement le CIS ✅

Le **CIS LC3R216N-8008A** est un capteur CMOS linéaire simple (≠ CCD). Il ne nécessite que **2 signaux de contrôle** :

| Signal CIS       | Description                   | Source                    |
|------------------|-------------------------------|---------------------------|
| **CLK** (pin 12) | Horloge 8 MHz (continue)      | TIM1_CH2 (PA9) → `CIS_CP` |
| **SI** (pin 10)  | Start Impulse (1 pulse/ligne) | TIM8_CH3 (PC8) → `CIS_SP` |
| **CNT** (pin 8)  | Sélection résolution          | Câblé à VDD → 600 DPI     |

> ⚠️ **Important** : Le générateur de timing (TG) du VSP5610 est conçu pour des **capteurs CCD** (signaux XP1-4, XRS, XCP, XCLR, XSH1-4). Ces signaux complexes **ne sont PAS utilisés** pour ce CIS CMOS. Le STM32 pilote directement CLK et SI.

### Le STM32 pilote les LEDs du CIS ✅

La datasheet LC3R216N-8008A indique que les LEDs intégrées **n'ont pas de résistance interne**. Le VSP5610 n'a aucune sortie LED. Le STM32 pilote donc les 3 LEDs via des **transistors N-MOSFET BSS138PW** (un par couleur).

En mode couleur, les LEDs s'allument **séquentiellement** (une seule à la fois) :
- **Séquence** : Bleu → Rouge → Vert → Bleu...
- **Durée par couleur** : ~228 µs par ligne (1824 cycles CLK à 8 MHz)

### Le VSP5610 est piloté par le STM32 via SPI ✅

- **Configuration** : SPI4 (PE2/PE4/PE5/PE6) → registres VSP5610
- **Données** : VSP5610 convertit les signaux analogiques CIS et transmet en CMOS 8-bit vers DCMI
- **Synchronisation** : XLSYNC (depuis STM32) déclenche la lecture de chaque ligne

---

## 3. Interfaçage STM32 ↔ CIS LC3R216N-8008

### 3.1 Signaux de Contrôle

| Net STM32 | Pin STM32  | Timer    | → | Pin CIS      | Fonction             |
|-----------|------------|----------|---|--------------|----------------------|
| `CIS_CP`  | PA9        | TIM1_CH2 | → | Pin 12 (CLK) | Horloge 8 MHz        |
| `CIS_SP`  | PC8        | TIM8_CH3 | → | Pin 10 (SI)  | Start Impulse        |
| —         | VDD (3.3V) | —        | → | Pin 8 (CNT)  | Câblé haut = 600 DPI |

> **Note sur CNT** : Si la sélection de résolution doit être dynamique, connecter CNT à un GPIO. Câblé à VDD fixe = toujours 600 DPI.

### 3.2 Alimentation du CIS

| Pin CIS    | Signal | Connexion                                                                                          |
|------------|--------|----------------------------------------------------------------------------------------------------|
| Pin 6      | VDD    | 3.3V + condensateurs bypass (100 nF + 10 µF)                                                       |
| Pin 9      | VDD    | 3.3V + condensateurs bypass (100 nF + 10 µF)                                                       |
| Pin 2      | GND    | Masse analogique (AGND)                                                                            |
| Pin 4      | GND    | Masse analogique (AGND)                                                                            |
| Pin 11     | GND    | Masse analogique (AGND)                                                                            |
| Pin 13     | VLED   | **4.5V** (voir §6 — résistances dimensionnées pour BSS138PW à 4.5V) + [100 nF] + [10 µF] → **GND** |
| Pin 17, 18 | NC     | Non connecté                                                                                       |

> ℹ️ **VLED = 4.5V** : Les LEDs verte (VF≈3.3V) et bleue (VF≈3.4V) nécessitent une tension supérieure à 3.3V. Un rail à 4.5V offre un headroom suffisant avec les résistances de limitation dimensionnées à cet effet (§6.2). Un rail à 5V est également utilisable — voir §6.2 pour les deux jeux de valeurs.

> ⚠️ **Découplage VLED sur GND (numérique), pas GNDA** : Le courant des LEDs (60 mA pulsé par MOSFET) est numérique. Le retour de courant passe par GND (source des BSS138PW). Connecter les condensateurs de découplage à GNDA injecterait ces courants impulsifs dans le plan analogique et contaminerait les signaux SIG1/2/3.

### 3.3 Sorties Analogiques du CIS vers VSP5610

| Pin CIS | Signal | Description                                   |
|---------|--------|-----------------------------------------------|
| Pin 5   | SIG1   | Sortie analogique bloc 1 (pixels 1 à 1728)    |
| Pin 3   | SIG2   | Sortie analogique bloc 2 (pixels 1729 à 3456) |
| Pin 1   | SIG3   | Sortie analogique bloc 3 (pixels 3457 à 5184) |
| Pin 7   | VREF   | Référence vidéo ~800 mV (niveau noir)         |

---

## 4. Interfaçage STM32 ↔ ADC VSP5610

### 4.1 Bus de Données DCMI (STM32 ← VSP5610)

| Net STM32     | Pin STM32 | ← | Pin VSP5610         | Fonction             |
|---------------|-----------|---|---------------------|----------------------|
| `DCMI_D0`     | PH9       | ← | Pin 40 (TA+/D0)     | Data bit 0 (LSB)     |
| `DCMI_D1`     | PA10      | ← | Pin 39 (TA-/D1)     | Data bit 1           |
| `DCMI_D2`     | PG10      | ← | Pin 38 (TB+/D2)     | Data bit 2           |
| `DCMI_D3`     | PC9       | ← | Pin 37 (TB-/D3)     | Data bit 3           |
| `DCMI_D4`     | PC11      | ← | Pin 36 (TC+/D4)     | Data bit 4           |
| `DCMI_D5`     | PI4       | ← | Pin 35 (TC-/D5)     | Data bit 5           |
| `DCMI_D6`     | PI6       | ← | Pin 34 (TCLK+/D6)   | Data bit 6           |
| `DCMI_D7`     | PI7       | ← | Pin 33 (TCLK-/D7)   | Data bit 7 (MSB)     |
| `DCMI_PIXCLK` | PA6       | ← | Pin 25 (GPIO2/LVCK) | Pixel clock (48 MHz) |

> ⚠️ **PIXCLK via GPIO2 (LVCK)** : En mode CMOS 8-bit (`OUTPUT_MODE = 0x00`), les pins 34 et 33 servent exclusivement de **D6 et D7** (données). La pixel clock de sortie est fournie par **GPIO2 (pin 25)** configuré en mode **LVCK** (Line Valid Clock). LVCK = MCLK × 6 = 48 MHz pour 3 canaux en 8-bit. Le registre GPIO2 doit être configuré avec `GPIO2_SEL = LVCK`.

### 4.2 HSYNC et VSYNC (capture continue)

| Net STM32    | Pin STM32 | Connexion PCB | Justification                       |
|--------------|-----------|---------------|-------------------------------------|
| `DCMI_HSYNC` | PA4       | [10 kΩ] → GND | Toujours inactif = capture continue |
| `DCMI_VSYNC` | PI5       | [10 kΩ] → GND | Toujours inactif = capture continue |

Configuration DCMI correspondante :
```c
DCMI_HSPolarity = DCMI_HSPolarity_High;  // Actif haut
DCMI_VSPolarity = DCMI_VSPolarity_High;  // Actif haut
// Signal câblé à GND → jamais actif → capture continue
```

### 4.3 SPI de Configuration (STM32 → VSP5610)

| Net STM32   | Pin STM32 | → | Pin VSP5610        | Fonction                |
|-------------|-----------|---|--------------------|-------------------------|
| `SPI4_SCK`  | PE2       | → | Pin 32 (SCLK)      | Horloge SPI             |
| `SPI4_MOSI` | PE6       | → | Pin 31 (SDI)       | Données vers VSP5610    |
| `SPI4_NSS`  | PE4       | → | Pin 30 (SEN)       | Chip Select (actif bas) |
| `SPI4_MISO` | PE5       | ← | Pin 46 (SDO/GPIO1) | Lecture retour          |

> **Protocole SPI VSP5610** : Format 30-bit (10 bits adresse + 20 bits données). Fréquence max SCLK : 10 MHz. SDO sur pin 46 nécessite `GPIO1_SDO_SEL = 3` dans le registre GPIO.

### 4.4 Horloge Maître et Synchronisation Ligne

| Net STM32        | Pin STM32      | → | Pin VSP5610     | Fonction                |
|------------------|----------------|---|-----------------|-------------------------|
| `CIS_CP` (8 MHz) | PA9 (TIM1_CH2) | → | Pin 28 (RCLKP)  | MCLK maître             |
| —                | GND            | → | Pin 27 (RCLKN)  | GND (mode single-ended) |
| `VSP_XLSYNC`     | PI2 (TIM8_CH4) | → | Pin 45 (XLSYNC) | Sync début de ligne     |

> ⚠️ **Deux signaux distincts nécessaires** :
> - `CIS_SP` → CIS SI : pulse courte **~125 ns** (1 cycle CLK) — TIM8_CH3 (PC8)
> - `VSP_XLSYNC` → VSP5610 pin 45 : pulse minimum **≥ 375 ns** (≥ 3 cycles MCLK) — TIM8_CH4 (PI2)
>
> Les deux signaux sont sur le **même timer TIM8**, garantissant une synchronisation hardware parfaite. CH3 génère SI (1 cycle), CH4 génère XLSYNC (≥ 3 cycles). Pas besoin d'intervention logicielle.
>
> **Note** : PA12 (`CIS_RS`) est libéré et peut être connecté à CIS CNT (pin 8) pour une sélection dynamique 300/600 DPI, ou laissé NC si CNT reste câblé à VDD.

---

## 5. Interfaçage ADC VSP5610 ↔ CIS LC3R216N-8008

### 5.1 Entrées Analogiques (CIS → VSP5610)

| Pin CIS | Signal CIS              | → | Pin VSP5610      | Valeur typique      |
|---------|-------------------------|---|------------------|---------------------|
| Pin 5   | SIG1 (pixels 1-1728)    | → | Pin 4 (AIN1)     | 800 mV à 1.1 V      |
| Pin 7   | VREF (niveau noir)      | → | Pin 5 (AINGND1)  | ~800 mV             |
| Pin 3   | SIG2 (pixels 1729-3456) | → | Pin 6 (AIN2)     | 800 mV à 1.1 V      |
| Pin 7   | VREF                    | → | Pin 7 (AINGND2)  | ~800 mV             |
| Pin 1   | SIG3 (pixels 3457-5184) | → | Pin 8 (AIN3)     | 800 mV à 1.1 V      |
| Pin 7   | VREF                    | → | Pin 9 (AINGND3)  | ~800 mV             |
| —       | 100 nF → AGND           | → | Pin 10 (AIN4)    | **→ 100 nF → AGND** |
| —       | 100 nF → AGND           | → | Pin 11 (AINGND4) | **→ 100 nF → AGND** |

> **Amplitude signal CIS** : Le signal vidéo varie de VREF (~800 mV) + ΔV (~300 mV) = ~1.1 V en pleine lumière. La tension de sortie augmente avec la lumière (mode non-inversi).

> ⚠️ **AIN4 / AINGND4 (pins 10, 11) — Ne pas laisser flottant** : Un pin d'entrée analogique flottant capte les perturbations de l'environnement (harmoniques 8/16/24 MHz) et peut contaminer les canaux actifs via le plan de masse interne commun du VSP5610 (crosstalk spécifié à ±3 LSB). La datasheet VSP5610 (note (2) tableau PIN ASSIGNMENTS) autorise : *"they can be opened or decoupled to GND with a decoupling capacitor"*. **Recommandation : condensateur 100 nF vers AGND** (préférable à laisser en l'air). Désactiver le canal 4 via le registre `AIN_CH_SEL = 0b0111` (canaux 1, 2, 3 actifs uniquement). La masse est **VSS = AGND** (masse analogique, pins 3, 12, 15, 18).

### 5.2 Configuration Analogique Recommandée du VSP5610

| Paramètre              | Valeur                     | Justification                         |
|------------------------|----------------------------|---------------------------------------|
| `AIN_CH_SEL`           | 3 canaux actifs (AIN1/2/3) | CIS 3 sorties analogiques             |
| `AINx_SH_CDS`          | Mode SH (Sample & Hold)    | CIS CMOS, pas CDS (réservé CCD)       |
| `AINx_POL`             | Positif                    | Signal CIS monte au-dessus de VREF    |
| `AINx_CLP_SEL`         | 3 (référence externe)      | AINGND = VREF CIS = ~800 mV           |
| `APG_x` (gain analog.) | ~3.0 V/V                   | 300 mV × 3 = ~900 mV → pleine échelle |
| `OUTPUT_MODE`          | 0x00 (CMOS 8-bit)          | Compatibilité DCMI STM32              |

### 5.3 Signaux TG du VSP5610 Non Connectés

Les sorties Timing Generator du VSP5610 sont inutilisées (conçues pour CCD) :

| Pin VSP5610    | Signal              | État   |
|----------------|---------------------|--------|
| 20 (XSH1)      | Shift gate 1        | **NC** |
| 21 (XSH2)      | Shift gate 2        | **NC** |
| 22 (XSH3)      | Shift gate 3        | **NC** |
| 23 (XSH4)      | Shift gate 4        | **NC** |
| 47 (XST/GPIO3) | Storage pulse       | **NC** |
| 48 (XCLR)      | Clear gate          | **NC** |
| 49 (XP1)       | Fast transfer clock | **NC** |
| 50 (XP2)       | Fast transfer clock | **NC** |
| 51 (XP3)       | Fast transfer clock | **NC** |
| 52 (XP4)       | Fast transfer clock | **NC** |
| 53 (X1L)       | Transfer clock      | **NC** |
| 54 (X2L)       | Transfer clock      | **NC** |
| 55 (XCP)       | Clamp gate          | **NC** |
| 56 (XRS)       | Reset gate          | **NC** |
| 24 (GPIO0)     | GPIO                | **NC** |

---

## 6. Circuit de Pilotage LEDs (BSS138PW)

> **Mis à jour v2.5 — 16/03/2026**  
> Transistor remplacé par **BSS138PW** (SOT-363), VLED porté à **4.5V**. Résistances de limitation recalculées avec la formule complète intégrant le Rds(on) du MOSFET.

### 6.1 Schéma par LED

```
         4.5V (VLED — pin 13 CIS)
              │
              ▼
    ┌─────────────────────┐
    │    CIS LC3R216N     │
    │  Anode LED commune  │
    │  (pin 13 VLED)      │
    │                     │
    │  LEDr cathode ──────┼──── pin 15 ──► R_LED_R ──┐
    │  LEDg cathode ──────┼──── pin 14 ──► R_LED_G ──┤
    │  LEDb cathode ──────┼──── pin 16 ──► R_LED_B ──┘
    └─────────────────────┘                          │
                                                     ▼ Drain
                                               [BSS138PW] × 3
                                                     │ Source
                                                    GND
                                                     │ Gate
                                               [R_GATE 100Ω]
                                                     │
                                        STM32 PWM (3.3V)
                                             PC6 / PD13 / PH12
```

### 6.2 Calcul des Résistances de Limitation

**Courant nominal LED : IF = 60 mA** — autorisé à tout duty cycle de 10% à 100% (Figure 3 datasheet CIS, courbe plate).  
En mode RGB (duty ≤ 33% par couleur), la contrainte thermique est largement respectée.

**Tension VLED : 4.5V**

**Formule (intègre la chute Vds du MOSFET via Rds_on) :**

```
IF = (VLED − VF) / (R + Rds_on)

BSS138PW @ Vgs = 3.3V (GPIO STM32) : Rds_on ≈ 2.5 Ω typ (< 3.5 Ω max @ Vgs=2.5V)
```

| LED   | VF_typ @ 60mA | VF_min @ 60mA | VF_max @ 60mA | **R_E24** | IF_VFtyp | IF_VFmin | IF_VFmax | P_moy (33% duty) |
|-------|---------------|---------------|---------------|-----------|----------|----------|----------|------------------|
| Rouge | 2.15 V        | 2.00 V        | 2.30 V        | **36 Ω**  | 61 mA    | 65 mA ⚠️  | 57 mA    | ~44 mW           |
| Verte | 3.30 V        | 3.20 V        | 3.50 V        | **18 Ω**  | 59 mA    | 63 mA ⚠️  | 49 mA    | ~21 mW           |
| Bleue | 3.40 V        | 3.30 V        | 3.50 V        | **16 Ω**  | 60 mA    | 65 mA ⚠️  | 54 mA    | ~19 mW           |

> ⚠️ **IF_VFmin légèrement au-dessus de 60 mA** : les cas VF_min correspondent à des lots de process extrêmes. À 33% duty cycle en mode RGB, le courant thermique moyen reste ≈ 20 mA par LED — les dépassements ponctuels sont sans conséquence.

> 💡 **Vert et bleu partagent une valeur différente** (18Ω vs 16Ω) pour équilibrer la contribution lumineuse entre les canaux. La calibration firmware (paramètres Tred/Tgrn/Tblu) finalise l'équilibre blanc sur référence (§6.4).

> ℹ️ **Package 0603 1/10W suffisant** : puissance moyenne thermique 19–44 mW (33% duty), bien en dessous du rating 100 mW.

### 6.3 Résistance de Gate (BSS138PW)

Le BSS138PW (SOT-363) est un N-MOSFET logique-level avec Vgs(th) = 0.8–1.5 V. Il commute pleinement avec Vgs = 3.3 V (GPIO STM32).

```
STM32 GPIO (3.3V) ──[100Ω]──► Gate BSS138PW
                               Drain ──► Résistance + LED cathode
                               Source ──► GND
```

| Paramètre BSS138PW | Valeur                          |
|--------------------|---------------------------------|
| Vgs(th)            | 0.8 V min / 1.5 V max           |
| Rds(on) @ Vgs=2.5V | 3.5 Ω max (typ ~2 Ω)            |
| Rds(on) @ Vgs=3.3V | ~2.5 Ω (meilleur que spec 2.5V) |
| Id max             | 220 mA                          |
| Ciss               | ~20–50 pF                       |
| Package            | SOT-363 (SC-88), 6 pins         |

La résistance de gate de **100 Ω** limite le pic de courant de charge de Ciss au basculement, sans impacter la commutation aux fréquences PWM utilisées (< 10 kHz).

> **Pas de pull-down nécessaire** si le GPIO est configuré en push-pull (état bas = Vgs = 0 V → MOSFET bloqué).

### 6.4 Séquence Couleur et Calibration (Mode RGB)

```
Ligne N :
│◄─── 228 µs ───►│◄─── 228 µs ───►│◄─── 228 µs ───►│
│    LED Bleu     │   LED Rouge     │   LED Vert      │ → Ligne N+1
│  CIS_LED_B = 1  │  CIS_LED_R = 1  │  CIS_LED_G = 1  │
│  Capture CIS    │  Capture CIS    │  Capture CIS    │

Total par ligne RGB : 684 µs
```

---

## 7. Composants à Ajouter autour du VSP5610

### 7.1 Composants Obligatoires (selon datasheet VSP5610)

| Réf.   | Composant    | Valeur         | Connexion            | Justification                |
|--------|--------------|----------------|----------------------|------------------------------|
| R_ISET | Résistance   | **10 kΩ ±1%**  | Pin 14 (ISET) → AGND | Courant de référence interne |
| C_REFP | Condensateur | **100 nF X7R** | Pin 16 (REFP) → AGND | Filtrage référence interne + |
| C_REFN | Condensateur | **100 nF X7R** | Pin 17 (REFN) → AGND | Filtrage référence interne − |

> ⚠️ **AVDD_LDO (pin 2)** : Sortie du LDO interne 1.8 V. La datasheet indique explicitement **"Non Connection, Open"**. **Ne rien connecter sur ce pin** — ni condensateur, ni charge. Certains LDO internes sont instables avec une capacité externe (risque d'oscillation). Laisser en **NC**.

### 7.2 Découplage des Alimentations et Séparation des Rails

#### Domaines d'alimentation du VSP5610

Le VSP5610 possède **3 domaines d'alimentation distincts** qui doivent être séparés sur le PCB :

| Pin              | Domaine                                       | Rail      | Source recommandée     | Justification                                                    |
|------------------|-----------------------------------------------|-----------|------------------------|------------------------------------------------------------------|
| **19 (VDD)**     | Cœur analogique (ADC, Sample-Hold, REFP/REFN) | **3.3VA** | LDO faible bruit dédié | Le bruit sur ce rail dégrade directement la résolution ADC       |
| **41 (LVDD)**    | Drivers de sortie LVDS                        | **3.3VD** | Rail numérique STM32   | Transmetteur LVDS inactif en mode CMOS 8-bit — exigence relâchée |
| **43 (DVDD_IO)** | I/O numériques (D[7:0], SPI, GPIO, LVCK)      | **3.3VD** | Rail numérique STM32   | Niveaux logiques 3.3V compatibles STM32H747                      |

> ⚠️ **Ne pas alimenter VDD (pin 19) depuis le rail 3.3V du STM32** : le STM32 consomme > 200 mA avec des commutations qui génèrent du ripple. Un LDO analogique dédié est obligatoire.

#### Régulateur 3.3VA recommandé : **ADP7142AUJZ-3.3** (Analog Devices)

| Paramètre         | Valeur                               | Requis                                   | Verdict                      |
|-------------------|--------------------------------------|------------------------------------------|------------------------------|
| Tension d'entrée  | 2.3V – 5.5V                          | Alimentation depuis 5V                   | ✅                            |
| Tension de sortie | 3.3V fixe                            | 3.3V                                     | ✅                            |
| Courant max       | **200 mA**                           | VSP5610 ~50 mA + CIS VDD ~50 mA ≈ 100 mA | ✅ Marge × 2                  |
| Bruit de sortie   | **~9 µVrms** (10 Hz–100 kHz)         | < 30 µVrms                               | ✅ Excellent                  |
| PSRR              | **~70 dB @ 1 kHz, ~60 dB @ 100 kHz** | > 60 dB                                  | ✅                            |
| Dropout           | ~200 mV @ 200 mA                     | —                                        | ✅ (5V → 3.3V, 1.7V de marge) |
| Package           | SOT-23-5 (AUJZ)                      | Compact                                  | ✅                            |

```
Architecture d'alimentation 3.3VA :

5V_MAIN ──[1µF X5R]─── [ADP7142AUJZ-3.3] ──[1µF X5R]──► 3.3VA
              │                                  │
             AGND                               AGND
                                                 │
                                 ├──► VSP5610 VDD (pin 19) ──[100nF]──[10µF]── AGND
                                 └──► CIS VDD (pins 6, 9) ──[100nF]──[10µF]── AGND
```

> **Note condensateur de sortie ADP7142** : Stable avec céramique X5R/X7R. Valeur recommandée = 1 µF en sortie directe du LDO (datasheet ADP7142), puis condensateurs locaux 100 nF + 10 µF plus proches des charges.

#### Condensateurs de découplage locaux

| Réf.        | Valeur     | Connexion      | Pin VSP5610 | Rail      |
|-------------|------------|----------------|-------------|-----------|
| C_VDD_100n  | 100 nF X7R | VDD → VSS      | Pin 19      | **3.3VA** |
| C_VDD_10u   | 10 µF X5R  | VDD → VSS      | Pin 19      | **3.3VA** |
| C_DVDD_100n | 100 nF X7R | DVDD_IO → DVSS | Pin 43      | **3.3VD** |
| C_DVDD_10u  | 10 µF X5R  | DVDD_IO → DVSS | Pin 43      | **3.3VD** |
| C_LVDD_100n | 100 nF X7R | LVDD → LVSS    | Pin 41      | **3.3VD** |
| C_LVDD_10u  | 10 µF X5R  | LVDD → LVSS    | Pin 41      | **3.3VD** |

> **Placement** : Condensateurs 100 nF **aussi proches que possible** du pin d'alimentation (< 1 mm). Condensateurs 10 µF à maximum 5 mm.

### 7.3 Connexions des Masses et Pins Divers

| Pin VSP5610         | Signal                             | Connexion                                                                                                                        |
|---------------------|------------------------------------|----------------------------------------------------------------------------------------------------------------------------------|
| 1 (TEST)            | Test interne                       | → DGND (masse numérique)                                                                                                         |
| 3, 12, 15, 18 (VSS) | Masse analogique                   | → AGND (étoile sous le chip)                                                                                                     |
| 26, 29, 44 (DVSS)   | Masse numérique                    | → DGND                                                                                                                           |
| 42 (LVSS)           | Masse LVDS                         | → DGND                                                                                                                           |
| 57 (EPAD)           | Pad thermique exposé               | → AGND (plan de cuivre + vias thermiques)                                                                                        |
| 13 (REF_AIN)        | Référence DAC interne (par défaut) | **Référence interne** (mode 0, défaut = 1.5 V) + **100 nF → AGND** (bonne pratique, non prescrit explicitement par la datasheet) |

### 7.4 Pull-down HSYNC/VSYNC

| Réf.    | Valeur | Connexion              |
|---------|--------|------------------------|
| R_HSYNC | 10 kΩ  | DCMI_HSYNC (PA4) → GND |
| R_VSYNC | 10 kΩ  | DCMI_VSYNC (PI5) → GND |

### 7.5 Diagramme de Connexion VSP5610 (57 pins)

```
                            VSP5610RSHR (57 pins QFN)
                       ┌──────────────────────────────┐
          DGND ◄───────┤ 1  TEST              XRS  56 ├───────► NC
            NC ◄───────┤ 2  AVDD_LDO          XCP  55 ├───────► NC
          AGND ◄───────┤ 3  VSS               X2L  54 ├───────► NC
      CIS_SIG1 ───────►┤ 4  AIN1              X1L  53 ├───────► NC
      CIS_VREF ───────►┤ 5  AINGND1           XP4  52 ├───────► NC
      CIS_SIG2 ───────►┤ 6  AIN2              XP3  51 ├───────► NC
      CIS_VREF ───────►┤ 7  AINGND2           XP2  50 ├───────► NC
      CIS_SIG3 ───────►┤ 8  AIN3              XP1  49 ├───────► NC
      CIS_VREF ───────►┤ 9  AINGND3          XCLR  48 ├───────► NC
   100n→AGND  ◄───────┤10  AIN4        XST/GPIO3  47 ├───────► NC
   100n→AGND  ◄───────┤11  AINGND4      SDO/GPIO1 46 ├───────► SPI4_MISO (PE5)
          AGND ◄───────┤12  VSS           XLSYNC   45 ├◄────── VSP_XLSYNC (PI2)
100n→AGND(BP) ◄───────┤13  REF_AIN        DVSS    44 ├───────► DGND
    10k→AGND   ◄───────┤14  ISET          DVDD_IO  43 ├───────► 3.3V + découplage
          AGND ◄───────┤15  VSS            LVSS    42 ├───────► DGND
   100n→AGND   ◄───────┤16  REFP           LVDD    41 ├───────► 3.3V + découplage
   100n→AGND   ◄───────┤17  REFN          TA+/D0   40 ├───────► DCMI_D0 (PH9)
          AGND ◄───────┤18  VSS           TA-/D1   39 ├───────► DCMI_D1 (PA10)
  3.3V+découp. ◄───────┤19  VDD           TB+/D2   38 ├───────► DCMI_D2 (PG10)
            NC ◄───────┤20  XSH1          TB-/D3   37 ├───────► DCMI_D3 (PC9)
            NC ◄───────┤21  XSH2          TC+/D4   36 ├───────► DCMI_D4 (PC11)
            NC ◄───────┤22  XSH3          TC-/D5   35 ├───────► DCMI_D5 (PI4)
            NC ◄───────┤23  XSH4         TCLK+/D6  34 ├───────► DCMI_D6 (PI6)
            NC ◄───────┤24  GPIO0        TCLK-/D7  33 ├───────► DCMI_D7 (PI7)
DCMI_PIXCLK(PA6)◄──────┤25  GPIO2/LVCK.      SCLK  32 ├◄────── SPI4_SCK (PE2)
          DGND ◄───────┤26  DVSS             SDI   31 ├◄────── SPI4_MOSI (PE6)
           GND ◄───────┤27  RCLKN            SEN   30 ├◄────── SPI4_NSS (PE4)
 CIS_CP(8MHz)  ───────►┤28  RCLKP           DVSS   29 ├───────► DGND
                       └──────────────────────────────┘
                               EPAD (57) → AGND
```

---

## 8. Configuration des Timers STM32

### 8.1 TIM1 — Génération CLK 8 MHz (CIS_CP) ✅ Optimal

TIM1 est sur le bus **APB2** (jusqu'à 240 MHz), c'est le meilleur choix pour la clock maître.

**Paramètres** (clock TIM = 240 MHz) :

```c
// TIM1 → CIS_CP → 8 MHz, 50% duty cycle
// Timer clock APB2 = 240 MHz
TIM1->PSC = 0;       // Pas de prescaler
TIM1->ARR = 29;      // 240 MHz / 30 = 8.000 MHz
TIM1->CCR2 = 14;     // 50% duty = ARR/2 = 14 → 15/30 = 50%
// Mode: PWM Generation CH2 (PA9)
// TRGO: Update Event → cadence les timers esclaves (TIM3/4/5/8)
```

> Si clock APB2 = 200 MHz : `ARR = 24`, `CCR2 = 12` → 8.0 MHz, 50% duty.

**Rôle du TRGO** : TIM1 Update Event → ITR0 → source clock pour TIM3, TIM4, TIM5, TIM8. Ces timers esclaves **comptent les pixels** plutôt que le temps.

### 8.2 TIM8 — Génération SI + XLSYNC (CIS_SP + VSP_XLSYNC) ✅ Optimal

TIM8 est sur APB2, synchrone avec TIM1. En **External Clock Mode 1 (ITR0)**, il compte les impulsions CLK. Il utilise **deux canaux** sur le même timer pour garantir une synchronisation hardware parfaite entre SI et XLSYNC :

```c
// TIM8 → CIS_SP (CH3) + VSP_XLSYNC (CH4)
// Source clock: ITR0 (TIM1 TRGO = chaque cycle CLK 8 MHz)
TIM8->PSC = 0;
TIM8->ARR = 1819;    // 1820 clocks = 1728 pixels + 92 dummy = 1 ligne complète
TIM8->CCR3 = 1;      // CH3: Pulse SI = 1 clock de large (125 ns)
TIM8->CCR4 = 3;      // CH4: Pulse XLSYNC = 3 clocks de large (375 ns min)
// Mode: External Clock Mode 1, source ITR0
// PWM Generation CH3 (PC8) → CIS_SP
// PWM Generation CH4 (PI2) → VSP_XLSYNC
```

**Chronogramme** :
```
CLK:     _│‾│_│‾│_│‾│_  ...  _│‾│_   (8 MHz, continu)
          1   2   3           1820  → ARR atteint → reset → nouveau SI

SI:      ‾‾‾‾│_____________...____________│‾‾‾‾│___ ...
              1 cycle=125ns    1819 cycles          nouveau pulse
```

### 8.3 TIM3 — LED Bleue (CIS_LED_B)

```c
// TIM3 → CIS_LED_B → contrôle exposition LED bleue
// Source: ITR0 (TIM1), compte les pixels
TIM3->PSC = 0;
TIM3->ARR = 1823;    // 1824 clocks = durée d'une phase couleur (228 µs × 8 MHz)
TIM3->CCR1 = expo_B; // Durée ON de la LED bleue (contrôle exposition)
// PWM Generation CH1 (PC6) → CIS_LED_B
```

### 8.4 TIM4 — LED Rouge (CIS_LED_R)

```c
// TIM4 → CIS_LED_R → contrôle exposition LED rouge
TIM4->PSC = 0;
TIM4->ARR = 1823;
TIM4->CCR2 = expo_R;
// PWM Generation CH2 (PD13) → CIS_LED_R
```

### 8.5 TIM5 — LED Verte (CIS_LED_G)

```c
// TIM5 → CIS_LED_G → contrôle exposition LED verte
// TIM5 est 32 bits → peut compter de très longues périodes si nécessaire
TIM5->PSC = 0;
TIM5->ARR = 1823;
TIM5->CCR3 = expo_G;
// PWM Generation CH3 (PH12) → CIS_LED_G
```

### 8.6 Récapitulatif Architecture Timer

```
                 TIM1 (APB2, Maître)
                 ┌─────────────────────┐
                 │  ARR=29, CCR2=14    │
                 │  → CIS_CP (PA9)     │
                 │  TRGO: Update       │
                 └─────────┬───────────┘
                           │ ITR0 (compte chaque cycle CLK)
          ┌────────────────┼────────────────┬─────────────────┐
          ▼                ▼                ▼                 ▼
    TIM8 (Esclave)   TIM3 (Esclave)   TIM4 (Esclave)   TIM5 (Esclave)
    ARR=1819         ARR=1823         ARR=1823         ARR=1823
    CCR3=1, CCR4=3   CCR1=expo_B      CCR2=expo_R      CCR3=expo_G
    → CIS_SP (PC8)   → LED_B (PC6)   → LED_R (PD13)  → LED_G (PH12)
    → XLSYNC (PI2)
```

---

## 9. Résistances Série sur les Signaux de Contrôle CIS

### 9.1 Pourquoi des Résistances Série ?

Le STM32H747 produit des fronts de commutation très rapides (~2-4 ns). À 8 MHz, ces fronts raides génèrent :
- **EMI** : Harmoniques > 100 MHz pouvant perturber les signaux analogiques SIG1-3 (~300 mV d'amplitude)
- **Ringing** : Oscillations sur les traces PCB > 2 cm
- **Crosstalk** : Couplage dans les traces adjacentes

### 9.2 Valeurs Recommandées

| Signal                 | De             | Vers                    | R série  | Effet                               |
|------------------------|----------------|-------------------------|----------|-------------------------------------|
| `CIS_CP` (8 MHz)       | PA9 (TIM1_CH2) | Nœud branché            | **22 Ω** | Amortit sans dégrader le duty 50%   |
| `CIS_SP`               | PC8 (TIM8_CH3) | CIS SI (pin 10)         | **33 Ω** | Pulse court, fronts moins critiques |
| `VSP_XLSYNC`           | PI2 (TIM8_CH4) | VSP5610 pin 45          | **33 Ω** | Protection en sortie                |
| SPI4 (SCLK, MOSI, NSS) | PE2, PE6, PE4  | VSP5610 pins 32, 31, 30 | **33 Ω** | Standard SPI                        |

### 9.3 Calcul de Validation pour CIS_CP

```
R_série = 22 Ω
C_charge = CIS_CLK + VSP5610_RCLKP ≈ 5 pF + 5 pF = 10 pF

τ = R × C = 22 × 10e-12 = 220 ps
tr (10-90%) = 2.2 × τ = 484 ps

Demi-période CLK = 62.5 ns
tr/T = 484 ps / 62.5 ns = 0.77% → Aucun impact sur le duty cycle
```

### 9.4 Placement PCB des Résistances Série

```
STM32 PA9 ──►[22Ω]──┬──►[nœud]──[~2cm]──► CIS CLK (pin 12)
                     │
                     └──►[nœud]──[~2cm]──► VSP5610 RCLKP (pin 28)
```

> Les résistances série doivent être placées **au plus près du GPIO du STM32** (< 5 mm), pas au niveau de la charge.

---

## 10. Notes de Routage PCB

### 10.1 Séparation des Masses (Star Ground)

```
AGND (analogique) ──┐
                     ├──► Point étoile sous VSP5610 (EPAD)
DGND (numérique) ───┘
```

- Plan AGND sous le VSP5610 et les traces analogiques SIG1-3
- Plan DGND sous les parties numériques (DCMI, SPI)
- **Un seul point de connexion** entre AGND et DGND (idéalement sous l'EPAD VSP5610)

### 10.2 Traces Critiques

| Trace                        | Priorité   | Recommandation                                                         |
|------------------------------|------------|------------------------------------------------------------------------|
| SIG1, SIG2, SIG3 (CIS → AIN) | ⚠️ CRITIQUE | Courtes (< 20 mm), blindées par plans AGND, loin des traces numériques |
| VREF CIS → AINGND1/2/3       | ⚠️ CRITIQUE | Même plan de masse, pas de vias si possible                            |
| CIS_CP (8 MHz)               | IMPORTANT  | Longueurs équilibrées vers CIS et VSP5610                              |
| DCMI_PIXCLK                  | IMPORTANT  | Trace courte, plan de masse sous la trace                              |
| DCMI D[7:0]                  | STANDARD   | Longueurs quasi-égales (±5 mm)                                         |

### 10.3 EPAD (Pin 57 VSP5610)

- Souder sur plan de cuivre AGND
- **4 à 9 vias thermiques** (via drill 0.3 mm) sous l'EPAD vers plan intérieur ou arrière
- Dissipe ~200-300 mW à pleine vitesse

### 10.4 Découplage des Alimentations

Placement conseillé des condensateurs de découplage :

```
[100nF] → le plus proche possible du pin VSP5610 (face composant, < 1mm)
[10µF]  → à moins de 5mm du pin
```

---

## 11. Configuration VSP5610 via SPI

### 11.1 Protocole SPI VSP5610

Format de trame : **30 bits** (10 bits adresse + 20 bits données)

```
SEN ‾‾‾‾│_________________________│‾‾‾‾  (actif bas)
SCLK    _│‾│_│‾│_ ... _│‾│_│‾│_
SDI     [A9...A0][D19...D0]
```

### 11.2 Registres Clés à Configurer

```c
// Exemple de séquence d'initialisation VSP5610 (pseudo-code)

// 1. Mode de sortie CMOS 8-bit
VSP5610_WriteReg(0x00, 0x00000);  // OUTPUT_MODE = CMOS 8-bit

// 2. Activer 3 canaux analogiques
VSP5610_WriteReg(0x01, 0x00007);  // AIN_CH_SEL = AIN1+AIN2+AIN3

// 3. Configurer mode Sample & Hold (pas CDS)
VSP5610_WriteReg(0x02, 0x00000);  // AINx_SH_CDS = SH mode

// 4. Polarité positive (signal CIS monte au-dessus de VREF)
VSP5610_WriteReg(0x03, 0x00007);  // AINx_POL = positif

// 5. Référence externe (AINGND = VREF CIS)
VSP5610_WriteReg(0x04, 0x3FFFF);  // AINx_CLP_SEL = externe

// 6. Gain analogique ~3.0 V/V (ajuster selon signal réel)
VSP5610_WriteReg(0x05, 0x18C63);  // APG_x ≈ 3.0 V/V

// 7. Activer SDO sur pin 46 (GPIO1)
VSP5610_WriteReg(0x20, 0x00003);  // GPIO1_SDO_SEL = 3

// 8. XLSYNC externe (mode déclenché par STM32)
VSP5610_WriteReg(0x10, 0x00001);  // XLSYNC_SEL = externe

// 9. GPIO2 = LVCK (pixel clock de sortie → DCMI_PIXCLK)
VSP5610_WriteReg(0x21, 0x00002);  // GPIO2_SEL = LVCK (48 MHz pour 3ch 8-bit)
```

> **Note** : Les adresses de registres sont données à titre indicatif. Se référer à la datasheet VSP5610 Tableau 2 "Register Map" pour les adresses exactes et le formatage des champs.

---

## 12. Séquence Temporelle Complète

### 12.1 Acquisition d'une Ligne RGB

```
Temps 0                  228µs                456µs                684µs
│                          │                    │                    │
▼                          ▼                    ▼                    ▼
┌──────────────────────────┬────────────────────┬────────────────────┐
│   Phase BLEU             │   Phase ROUGE      │   Phase VERT       │
│   CIS_LED_B = ON         │   CIS_LED_R = ON   │   CIS_LED_G = ON   │
│                          │                    │                    │
│  ┌─ SI pulse (125ns)     │  ┌─ SI pulse       │  ┌─ SI pulse       │
│  │  XLSYNC (≥375ns)      │  │  XLSYNC         │  │  XLSYNC         │
│  │                       │  │                 │  │                 │
│  │  ┌─ DCMI capture ───► │  │  ┌─ DCMI ─────► │  │  ┌─ DCMI ─────► │
│  │  │  1728 pixels       │  │  │  1728 pix.   │  │  │  1728 pix.   │
│  └──┘                    │  └──┘              │  └──┘              │
└──────────────────────────┴────────────────────┴────────────────────┘
```

### 12.2 Séquence de Démarrage Logicielle

```
1. Initialiser SPI4 (STM32)
2. Écrire registres VSP5610 via SPI (OUTPUT_MODE, gains, canaux...)
3. Démarrer TIM1 (génère CIS_CP = MCLK)
   → Le CIS reçoit immédiatement CLK (sortie continue)
4. TIM3/4/5 démarrent en esclaves (comptent les pixels)
5. TIM8 démarre en esclave (génère SI automatique)
6. Séquence couleur :
   a. Activer CIS_LED_B (TIM3)
   b. Attendre ~92 clocks (dummy pixels CIS)
   c. Déclencher DCMI capture (DCMI_CaptureCmd)
   d. XLSYNC pulsé automatiquement par TIM8_CH4 (PI2) ≥ 375 ns
   e. Attendre interruption DMA (transfert terminé)
   f. Traiter les données (démux 3 blocs × 1728 pixels)
   g. Répéter pour LED_R, LED_G
7. Renvoyer ligne RGB vers USB/stockage
```

---

## 13. BOM Complète des Composants Additionnels

### 13.1 Composants autour du VSP5610

| Qté | Réf.          | Description            | Valeur     | Package | Tension | Note              |
|-----|---------------|------------------------|------------|---------|---------|-------------------|
| 1   | R_ISET        | Résistance précision   | 10 kΩ ±1%  | 0402    | —       | ISET pin 14       |
| 2   | C_REF         | Condensateur céramique | 100 nF X7R | 0402    | 10V     | REFP/REFN         |
| 3   | C_SUPPLY_100n | Condensateur céramique | 100 nF X7R | 0402    | 10V     | VDD/DVDD/LVDD     |
| 3   | C_SUPPLY_10u  | Condensateur céramique | 10 µF X5R  | 0805    | 10V     | VDD/DVDD/LVDD     |
| 2   | R_SYNC        | Résistance pull-down   | 10 kΩ      | 0402    | —       | HSYNC/VSYNC → GND |

> ⚠️ **AVDD_LDO (pin 2) = NC** : Aucun condensateur ni composant sur cette broche (datasheet : "Non Connection, Open").

### 13.2 Circuit LEDs CIS (× 3 couleurs)

| Qté | Réf.    | Description                   | Valeur         | Package  | Note                              |
|-----|---------|-------------------------------|----------------|----------|-----------------------------------|
| 3   | Q_LED   | MOSFET N-canal logic-level    | **BSS138PW**   | SOT-363  | Rds_on ≈ 2.5Ω @ Vgs=3.3V          |
| 3   | R_GATE  | Résistance de gate            | 100 Ω          | 0402     | Limitation di/dt                  |
| 1   | R_LED_R | Résistance limitation courant | **36 Ω** 1/10W | **0603** | Rouge — IF_typ=61mA @ VLED=4.5V   |
| 1   | R_LED_G | Résistance limitation courant | **18 Ω** 1/10W | **0603** | Verte — IF_typ=59mA @ VLED=4.5V   |
| 1   | R_LED_B | Résistance limitation courant | **16 Ω** 1/10W | **0603** | Bleue — IF_typ=60mA @ VLED=4.5V ¹ |

> ¹ **R_LED_B = 16 Ω** (valeur E24) : VF_bleu plus élevée que VF_vert (3.4V vs 3.3V) → résistance plus petite pour équilibrer le courant typique. IF_VFmin = 65mA sur lots de process extrêmes, acceptable en mode pulsé 33% duty (courant thermique moyen ≈ 21mA).

### 13.3 Résistances Série Signaux de Contrôle

| Qté | Réf.      | Description          | Valeur | Package | Signal             |
|-----|-----------|----------------------|--------|---------|--------------------|
| 1   | R_CIS_CLK | Résistance série     | 22 Ω   | 0402    | CIS_CP (8 MHz)     |
| 1   | R_CIS_SI  | Résistance série     | 33 Ω   | 0402    | CIS_SP (SI)        |
| 1   | R_XLSYNC  | Résistance série     | 33 Ω   | 0402    | VSP_XLSYNC         |
| 4   | R_SPI     | Résistance série SPI | 33 Ω   | 0402    | SCLK/MOSI/NSS/MISO |

### 13.4 Total BOM Additionnelle

| Catégorie     | Nombre de références | Nombre de composants |
|---------------|----------------------|----------------------|
| Résistances   | 7 types              | 12                   |
| Condensateurs | 3 types              | 8                    |
| MOSFET        | 1 type               | 3                    |
| **Total**     | **11 types**         | **23 composants**    |

---

## 14. Signaux Manquants / Nets à Créer

### 14.1 Nets à Renommer/Créer

| Net actuel | Nouveau net    | Pin STM32 | Destination    | Action                   |
|------------|----------------|-----------|----------------|--------------------------|
| —          | `VSP_XLSYNC`   | PI2       | VSP5610 pin 45 | Nouveau net (TIM8_CH4)   |
| —          | `VSP_PIXCLK`   | PA6 (←)   | VSP5610 pin 25 | GPIO2/LVCK → DCMI_PIXCLK |
| —          | `VSP_SPI_SCK`  | PE2       | VSP5610 pin 32 | Alias de SPI4_SCK        |
| —          | `VSP_SPI_MOSI` | PE6       | VSP5610 pin 31 | Alias de SPI4_MOSI       |
| —          | `VSP_SPI_NSS`  | PE4       | VSP5610 pin 30 | Alias de SPI4_NSS        |
| —          | `VSP_SPI_MISO` | PE5       | VSP5610 pin 46 | Alias de SPI4_MISO       |

> **Note** : Le net `CIS_RS` (PA12) était prévu pour la sélection de résolution (RS = Resolution Select, 300/600 DPI). Puisque XLSYNC est maintenant sur TIM8_CH4 (PI2), PA12 est libéré. Il peut être reconnecté à CIS CNT (pin 8) pour un contrôle dynamique de résolution, ou laissé NC si CNT reste câblé à VDD (600 DPI fixe).

### 14.2 Récapitulatif Complet des Nets CIS

| Net           | Pin STM32       | Vers                          | Fonction             |
|---------------|-----------------|-------------------------------|----------------------|
| `CIS_CP`      | PA9 (TIM1_CH2)  | CIS CLK + VSP5610 RCLKP       | Horloge maître 8 MHz |
| `CIS_SP`      | PC8 (TIM8_CH3)  | CIS SI                        | Start Impulse        |
| `CIS_LED_R`   | PD13 (TIM4_CH2) | Gate BSS138PW → LED rouge CIS | Contrôle LED rouge   |
| `CIS_LED_G`   | PH12 (TIM5_CH3) | Gate BSS138PW → LED verte CIS | Contrôle LED verte   |
| `CIS_LED_B`   | PC6 (TIM3_CH1)  | Gate BSS138PW → LED bleue CIS | Contrôle LED bleue   |
| `DCMI_D0`     | PH9             | VSP5610 D0 (pin 40)           | Données bit 0        |
| `DCMI_D1`     | PA10            | VSP5610 D1 (pin 39)           | Données bit 1        |
| `DCMI_D2`     | PG10            | VSP5610 D2 (pin 38)           | Données bit 2        |
| `DCMI_D3`     | PC9             | VSP5610 D3 (pin 37)           | Données bit 3        |
| `DCMI_D4`     | PC11            | VSP5610 D4 (pin 36)           | Données bit 4        |
| `DCMI_D5`     | PI4             | VSP5610 D5 (pin 35)           | Données bit 5        |
| `DCMI_D6`     | PI6             | VSP5610 D6 (pin 34)           | Données bit 6        |
| `DCMI_D7`     | PI7             | VSP5610 D7 (pin 33)           | Données bit 7        |
| `DCMI_PIXCLK` | PA6             | VSP5610 GPIO2/LVCK (pin 25)   | Pixel clock 48 MHz   |
| `DCMI_HSYNC`  | PA4             | [10kΩ] → GND                  | Forcé inactif        |
| `DCMI_VSYNC`  | PI5             | [10kΩ] → GND                  | Forcé inactif        |
| `VSP_XLSYNC`  | PI2 (TIM8_CH4)  | VSP5610 pin 45                | Sync ligne           |

---

## 15. Réception des Données DCMI et Organisation Mémoire

### 15.1 Sortie Numérique du VSP5610

Le VSP5610 en mode **CMOS 8-bit** (`OUTPUT_MODE = 0x00`) avec 3 canaux actifs sort les données sur **D[7:0]** (pins 33-40) cadencées par **LVCK** (GPIO2, pin 25).

L'ADC interne est **16 bits**. Chaque échantillon est découpé en 2 octets (**MSB puis LSB**) envoyés sur 2 cycles LVCK consécutifs. Les 3 canaux sont **multiplexés temporellement** :

```
MCLK (8 MHz)  ──┐     ┌─────┐     ┌─────┐     ┌─────┐
                └─────┘     └─────┘     └─────┘     └─────┘

LVCK (48 MHz) ─┐ ┌┐ ┌┐ ┌┐ ┌┐ ┌┐ ┌┐ ┌┐ ┌┐ ┌┐ ┌┐ ┌┐ ┌┐
               └─┘└─┘└─┘└─┘└─┘└─┘└─┘└─┘└─┘└─┘└─┘└─┘└─┘

D[7:0]         │C1 │C1 │C2 │C2 │C3 │C3 │C1 │C1 │C2 │C2 │C3 │C3 │
               │MSB│LSB│MSB│LSB│MSB│LSB│MSB│LSB│MSB│LSB│MSB│LSB│
               ├──── Pixel 0 ──────────────┤├──── Pixel 1 ────────┤
               ◄── 6 cycles LVCK = 1 MCLK ─►
```

**Pourquoi LVCK = 48 MHz ?** → 3 canaux × 2 bytes × 8 MHz = 48 MB/s

### 15.2 Mécanisme d'Accumulation du DCMI

Le DCMI possède un registre interne **DCMI_DR de 32 bits**. Il accumule **4 octets** reçus sur D[7:0] avant de déclencher un transfert DMA :

```
Cycle LVCK:  │  1   │  2   │  3   │  4   │ → DMA Request !
             │      │      │      │      │
D[7:0]:      │ B0   │ B1   │ B2   │ B3   │
             │CH1_M │CH1_L │CH2_M │CH2_L │

DCMI_DR:     [  B3  |  B2  |  B1  |  B0  ]
              31-24   23-16  15-8    7-0

→ DMA transfère ce mot 32-bit vers la RAM
```

Puis les 4 octets suivants :

```
Cycle LVCK:  │  5   │  6   │  7   │  8   │ → DMA Request !
D[7:0]:      │CH3_M │CH3_L │CH1_M │CH1_L │

DCMI_DR:     [CH1_L | CH1_M | CH3_L | CH3_M]
              31-24   23-16   15-8    7-0
```

> ⚠️ **Little-endian** : En mémoire ARM Cortex-M7, l'octet de poids faible (bits 7-0) est stocké à l'adresse la plus basse. Cela signifie que l'ordre en mémoire correspond à l'ordre temporel de réception.

### 15.3 Configuration DCMI

```c
// Configuration DCMI pour réception VSP5610
DCMI_InitTypeDef dcmi;

dcmi.DCMI_CaptureMode    = DCMI_CaptureMode_SnapShot;    // Capture à la demande
dcmi.DCMI_SynchroMode    = DCMI_SynchroMode_Hardware;     // Sync matérielle
dcmi.DCMI_PCKPolarity    = DCMI_PCKPolarity_Rising;       // Capture sur front ↑ LVCK
dcmi.DCMI_VSPolarity     = DCMI_VSPolarity_High;          // VSYNC=GND → jamais actif
dcmi.DCMI_HSPolarity     = DCMI_HSPolarity_High;          // HSYNC=GND → jamais actif
dcmi.DCMI_CaptureRate    = DCMI_CaptureRate_All_Frame;    // Chaque front
dcmi.DCMI_ExtendedDataMode = DCMI_ExtendedDataMode_8b;    // Bus 8-bit

DCMI_Init(&dcmi);
```

### 15.4 Configuration DMA

```c
#define PIXELS_PER_BLOCK    1728                              // Pixels par bloc CIS
#define BYTES_PER_LINE      (PIXELS_PER_BLOCK * 3 * 2)       // 1728 × 3ch × 2B = 10 368
#define DMA_WORDS_PER_LINE  (BYTES_PER_LINE / 4)             // 10 368 / 4 = 2 592

// Buffer DMA aligné 32-bit
__attribute__((aligned(4))) uint32_t dma_buffer[DMA_WORDS_PER_LINE];

// Configuration DMA2 Stream1 Channel1 (canal DCMI sur STM32H7)
DMA_InitTypeDef dma;

dma.DMA_Channel              = DMA_Channel_1;
dma.DMA_PeripheralBaseAddr   = (uint32_t)&DCMI->DR;
dma.DMA_Memory0BaseAddr      = (uint32_t)dma_buffer;
dma.DMA_DIR                  = DMA_DIR_PeripheralToMemory;
dma.DMA_BufferSize           = DMA_WORDS_PER_LINE;           // 2592 mots
dma.DMA_PeripheralInc        = DMA_PeripheralInc_Disable;
dma.DMA_MemoryInc            = DMA_MemoryInc_Enable;
dma.DMA_PeripheralDataSize   = DMA_PeripheralDataSize_Word;  // 32-bit depuis DCMI_DR
dma.DMA_MemoryDataSize       = DMA_MemoryDataSize_Word;      // 32-bit vers RAM
dma.DMA_Mode                 = DMA_Mode_Normal;              // PAS circulaire
dma.DMA_Priority             = DMA_Priority_High;
dma.DMA_FIFOMode             = DMA_FIFOMode_Enable;
dma.DMA_FIFOThreshold        = DMA_FIFOThreshold_Full;
dma.DMA_MemoryBurst          = DMA_MemoryBurst_INC4;
dma.DMA_PeripheralBurst      = DMA_PeripheralBurst_Single;

DMA_Init(DMA2_Stream1, &dma);
DMA_ITConfig(DMA2_Stream1, DMA_IT_TC, ENABLE);  // Interruption Transfer Complete
```

### 15.5 Organisation des Données en Mémoire

Le buffer DMA contient les octets dans l'ordre temporel de réception. La structure est un motif de **6 octets** qui se répète **1728 fois** :

```
Adresse  │ Contenu           │ Signification
─────────┼───────────────────┼──────────────────────────
0x0000   │ CH1_Pixel0_MSB    │ Canal 1 (SIG1), pixel 0, octet haut (bits 15-8)
0x0001   │ CH1_Pixel0_LSB    │ Canal 1 (SIG1), pixel 0, octet bas  (bits 7-0)
0x0002   │ CH2_Pixel0_MSB    │ Canal 2 (SIG2), pixel 0, octet haut
0x0003   │ CH2_Pixel0_LSB    │ Canal 2 (SIG2), pixel 0, octet bas
0x0004   │ CH3_Pixel0_MSB    │ Canal 3 (SIG3), pixel 0, octet haut
0x0005   │ CH3_Pixel0_LSB    │ Canal 3 (SIG3), pixel 0, octet bas
─────────┼───────────────────┼──────────────────────────
0x0006   │ CH1_Pixel1_MSB    │ Canal 1, pixel 1
0x0007   │ CH1_Pixel1_LSB    │
0x0008   │ CH2_Pixel1_MSB    │ Canal 2, pixel 1
0x0009   │ CH2_Pixel1_LSB    │
0x000A   │ CH3_Pixel1_MSB    │ Canal 3, pixel 1
0x000B   │ CH3_Pixel1_LSB    │
─────────┼───────────────────┼──────────────────────────
...      │ ...               │ ... (×1728 groupes)
─────────┼───────────────────┼──────────────────────────
0x287E   │ CH3_Pixel1727_MSB │ Canal 3, dernier pixel
0x287F   │ CH3_Pixel1727_LSB │ Fin du buffer (10 368 octets)
```

> **Note** : Les 3 canaux transmettent des **groupes de pixels différents** du CIS :
> - CH1 (SIG1) = pixels physiques **1 à 1728** sur la ligne CIS
> - CH2 (SIG2) = pixels physiques **1729 à 3456**
> - CH3 (SIG3) = pixels physiques **3457 à 5184**
>
> Pour reconstituer une ligne complète de 5184 pixels, il faut **concaténer** ch1 + ch2 + ch3.

### 15.6 Post-Traitement : Démultiplexage en 3 Canaux

```c
uint16_t ch1[PIXELS_PER_BLOCK];  // SIG1 : pixels 1-1728
uint16_t ch2[PIXELS_PER_BLOCK];  // SIG2 : pixels 1729-3456
uint16_t ch3[PIXELS_PER_BLOCK];  // SIG3 : pixels 3457-5184

void Demux_Line(uint8_t* buffer)
{
    for (int i = 0; i < PIXELS_PER_BLOCK; i++)
    {
        int offset = i * 6;  // 6 bytes par groupe de 3 canaux
        ch1[i] = ((uint16_t)buffer[offset + 0] << 8) | buffer[offset + 1];
        ch2[i] = ((uint16_t)buffer[offset + 2] << 8) | buffer[offset + 3];
        ch3[i] = ((uint16_t)buffer[offset + 4] << 8) | buffer[offset + 5];
    }
}

// Reconstitution ligne complète 5184 pixels (optionnel)
uint16_t line_full[5184];
memcpy(&line_full[0],    ch1, 1728 * sizeof(uint16_t));
memcpy(&line_full[1728], ch2, 1728 * sizeof(uint16_t));
memcpy(&line_full[3456], ch3, 1728 * sizeof(uint16_t));
```

### 15.7 Séquence Complète de Capture d'une Ligne (Mode Couleur)

```
 CPU                    TIM8                 VSP5610              DCMI/DMA           RAM
  │                      │                     │                    │                 │
  ├── Armer DMA ─────────────────────────────────────────────────►  │                 │
  ├── Activer DCMI ──────────────────────────────────────────────►  │                 │
  ├── Allumer LED_B ──►  │                     │                    │                 │
  │                      │                     │                    │                 │
  │                ┌──SI (CH3, 125ns)─────────►│                    │                 │
  │                └──XLSYNC (CH4, 375ns)─────►│                    │                 │
  │                      │                     │                    │                 │
  │                      │                ┌─── D[7:0] + LVCK ──────►│                 │
  │                      │                │    48 MHz, 10368 bytes  │── DMA ─────────►│
  │                      │                │    pendant 216 µs       │  2592 × 32-bit  │
  │                      │                └─────────────────────────│                 │
  │                      │                     │              IRQ TC│                 │
  │◄── IRQ DMA TC ───────────────────────────────────────────────── │                 │
  │                      │                     │                    │                 │
  ├── Éteindre LED_B     │                     │                    │                 │
  ├── Démux ch1/ch2/ch3 ───────────────────────────────────────────────────────────►  │
  │                      │                     │                    │                 │
  ├── Répéter avec LED_R puis LED_G            │                    │                 │
  │                      │                     │                    │                 │
  ├── Ligne RGB complète (3 × 10368 = 31104 bytes)                                    │
```

### 15.8 Chiffres Clés

| Paramètre                   | Valeur                       |
|-----------------------------|------------------------------|
| PIXCLK (LVCK)               | 48 MHz                       |
| Largeur bus données         | 8 bits                       |
| Bytes par ligne (1 couleur) | 10 368 (1728 pix × 3ch × 2B) |
| Mots DMA par ligne          | 2 592 (10 368 / 4)           |
| Durée capture (1 couleur)   | 216 µs (10 368 / 48 MHz)     |
| Durée ligne RGB complète    | 684 µs (3 × 228 µs)          |
| Lignes RGB / seconde        | ~1 462                       |
| Débit données DCMI          | 48 MB/s (< 54 MHz max DCMI)  |
| RAM par ligne RGB           | 31 104 bytes (3 × 10 368)    |

---

## 16. Analyse de la Connexion Analogique CIS ↔ VSP5610 (CISVREF & Filtres)

> **Ajout v2.2 — 13/03/2026**  
> Cette section détaille la partie intégration hardware de l'interface analogique : niveaux de tension, rôle de CISVREF, filtres anti-repliement sur les voies SIG, et circuit de filtrage recommandé sur VREF.

---

### 16.1 Cartographie des Niveaux de Tension Analogiques

D'après la datasheet LC3R216N-8008A (§4 Image Data Output Characteristics) :

| Signal CIS | Pin CIS | Niveau typique     | Plage (spec) | Destination VSP5610                        |
|------------|---------|--------------------|--------------|--------------------------------------------|
| **VREF**   | 7       | **800 mV**         | 600–1000 mV  | AINGND1 / AINGND2 / AINGND3 (pins 5, 7, 9) |
| **SIG1**   | 5       | VREF → VREF+300 mV | 650–1100 mV  | AIN1 (pin 4)                               |
| **SIG2**   | 3       | VREF → VREF+300 mV | 650–1100 mV  | AIN2 (pin 6)                               |
| **SIG3**   | 1       | VREF → VREF+300 mV | 650–1100 mV  | AIN3 (pin 8)                               |

```
Signal CIS (SIGx) — vue temporelle (1 pixel)

 ~1100 mV ┤ ▄▄▄▄ ← Vpmax blanc = VREF + 300 mV typ
          │ ████
  ~950 mV ┤ ████ ← Vdmax noir = VREF + 150 mV max
          │
   ~800 mV┼──────── ← VREF (niveau noir = référence) ← AINGND1/2/3
          │
  ~650 mV ┤         ← Vdmin noir = VREF − 150 mV min
          │
      0 V ┤         ← GND (⚠️ NE PAS connecter à AINGNDx)

Excursion utile : 0 → +300 mV au-dessus de VREF
```

> ⚠️ **Note critique CIS datasheet (§4.1)** :  
> *"Vref is the reference voltage for video signals. **Do not use GND instead of Vref.**"*  
> Le GND et VREF sont **deux tensions distinctes** (~800 mV d'écart). Connecter GND à AINGNDx décalerait le zéro de mesure et saturerait l'ADC.

---

### 16.2 Pourquoi Connecter VREF à AINGNDx (et non GND)

La datasheet VSP5610 (§SH Mode, AINx_CLP_SEL = 3) décrit le mode **"not clamped, external reference"** pour les capteurs CMOS :

> *"To use an external reference, it can be input to AINGNDx with sensor signals connected to AINx."*

Le circuit interne du VSP5610 en mode SH effectue une **mesure différentielle** :

```
Signal effectif mesuré = AINx − AINGNDx
                       = SIGx − VREF
                       = 0 mV (noir) → +300 mV (blanc)
```

**Avantages de cette architecture :**

| Avantage                                        | Explication                                               |
|-------------------------------------------------|-----------------------------------------------------------|
| ✅ Offset DC soustrait automatiquement           | Les ~800 mV communs à SIGx et VREF s'annulent             |
| ✅ Pas de condensateur de couplage AC nécessaire | Signal DC transmis directement                            |
| ✅ Rejection du bruit en mode commun             | Bruit sur VREF → mode commun → partiellement annulé       |
| ✅ Plein accord avec la plage d'entrée VSP5610   | 0–300 mV × gain 3 = 0–900 mV → dans la pleine échelle 1 V |

**Configuration registres VSP5610 correspondante :**

| Registre       | Valeur | Signification                                     |
|----------------|--------|---------------------------------------------------|
| `AINx_SH_CDS`  | **1**  | Mode SH (Sample & Hold) → capteur CMOS            |
| `AINx_CLP_SEL` | **3**  | Not clamped, external reference via AINGNDx       |
| `SH_REFx_EN`   | **0**  | Désactivé — on utilise AINGNDx, pas V_CLP interne |
| `AINx_POL`     | **1**  | Polarité positive (signal monte avec la lumière)  |

---

### 16.3 Filtre Anti-Repliement sur SIG1 / SIG2 / SIG3

#### ⚠️ Important — Condensateur AC série vs Condensateur shunt de filtrage

La datasheet VSP5610 (§Input Clamp, Not-Clamped Mode) précise :

> *"If the sensor signal is directly connected to the AFE, this mode should be configured **without an ac-coupling capacitor** at the input port."*

La note (1) sous la Figure 5 confirme :
> *"Under some conditions, the sensor signal can be directly input to the AFE **without requiring an external capacitor**."*

Il existe donc **deux types de condensateurs distincts** à ne pas confondre :

| Type                                | Placement                           | Fonction                         | Nécessaire ici ?                                                                                   |
|-------------------------------------|-------------------------------------|----------------------------------|----------------------------------------------------------------------------------------------------|
| **C AC série** (couplage)           | En **série** entre CIS SIGx et AINx | Bloquer l'offset DC CCD (~2V)    | ❌ **NON** — l'offset ~800 mV est dans la plage d'entrée ET AINGNDx = VREF gère l'offset nativement |
| **C shunt de filtrage** (passe-bas) | Entre AINx et **AGND**              | Filtrer les harmoniques HF (EMI) | ✅ **OUI** — filtre anti-repliement uniquement                                                      |

```
❌ À NE PAS FAIRE (couplage AC série, inutile ici) :
   CIS SIGx ──[C_AC 100nF]──[R]──► AINx   ← FAUX pour CIS CMOS dans plage DC

✅ À FAIRE (filtre passe-bas shunt) :
   CIS SIGx ──[R_F = 33Ω]──┬──► AINx     ← Connexion DC directe
                             │
                           [C_F = 100pF]  ← Shunt vers AGND (filtre EMI uniquement)
                             │
                            AGND
```

#### Contraintes temporelles (datasheet CIS §6)

| Paramètre                        | Valeur                         | Source                             |
|----------------------------------|--------------------------------|------------------------------------|
| Fréquence pixel (f_PIX)          | **8 MHz**                      | CIS CLK = 8 MHz                    |
| Ts — stabilisation signal CIS    | **20 à 40 ns** après front CLK | CIS datasheet §6                   |
| Capacité d'entrée VSP5610 (C_in) | **5 pF**                       | VSP5610 Electrical Characteristics |
| Période d'un pixel (1/f_PIX)     | **125 ns**                     | —                                  |
| Fenêtre disponible pour SH       | 125 ns − 40 ns = **85 ns**     | Après Ts min                       |

#### Circuit de filtre recommandé (par voie SIGx → AINx)

```
CIS SIGx ──[R_F = 33 Ω]──┬──────────────────────────► VSP5610 AINx (pin 4/6/8)
  (pin 1/3/5)             │         (connexion DC directe — pas de C en série)
                        [C_F = 100 pF X7R]
                        (shunt EMI)
                          │
                         AGND
```

#### Validation du filtre

```
C_totale = C_F + C_in_VSP5610 = 100 pF + 5 pF = 105 pF

Fréquence de coupure :
  fc = 1 / (2π × 33 × 105×10⁻¹²) ≈ 46 MHz

Constante de temps d'établissement :
  τ = 33Ω × 105pF = 3.5 ns
  Établissement à 99.9% (7τ) = 24 ns

Validation du timing :
  24 ns ≪ 85 ns (fenêtre disponible) ✅
```

**Effet du filtre :**
- ✅ Atténue les harmoniques > 46 MHz (EMI des CLK numériques)
- ✅ Amortit les pics de courant du circuit SH interne du VSP5610
- ✅ N'impacte pas le signal utile (46 MHz ≫ 4 MHz bande utile)
- ✅ Temps d'établissement bien inférieur à la fenêtre de sampling
- ✅ Connexion DC directe préservée — le signal CIS traverse sans décalage DC

> **Option alternative (filtrage plus fort) :** R = 100 Ω, C = 100 pF → fc = 15 MHz, 7τ = 70 ns ≈ limite acceptable. À réserver si des perturbations EMI subsistent sur les premières mesures prototype.

---

### 16.4 Circuit de Filtrage sur CISVREF — Architecture Recommandée

#### Problèmes potentiels sur VREF

1. **Couplage horloge 8 MHz** : le CIS partage le substrat avec ses switchs d'horloge → possible injection de parasites à 8 MHz et harmoniques sur la sortie VREF
2. **Distribution sur 3 pins AINGND** : VREF alimente simultanément AINGND1, 2 et 3 → la résistance de source de VREF doit rester faible
3. **Bruit basse fréquence** : ripple depuis le rail VDD du CIS (datasheet recommande 100 µF de filtrage BF sur VDD)

#### Option A — Filtrage standard (premier prototype)

```
                         ┌──[C_VREF_HF = 100 nF X7R 0402]── AGND
                         │
CIS VREF (pin 7) ────────┼──[C_VREF_BF = 1 µF X5R 0402]──── AGND
                         │
                         ├──[R_AGND1 = 33 Ω 0402]── AINGND1 (pin 5) ──[C_A1 = 100 nF]── AGND
                         ├──[R_AGND2 = 33 Ω 0402]── AINGND2 (pin 7) ──[C_A2 = 100 nF]── AGND
                         └──[R_AGND3 = 33 Ω 0402]── AINGND3 (pin 9) ──[C_A3 = 100 nF]── AGND
```

#### Option B — Filtrage renforcé avec ferrite (si couplage CLK détecté sur prototype)

```
              Ferrite 0402
              600 Ω @ 100 MHz
              (ex: BLM18PG601SN1D)
                    │
CIS VREF ──────[FB]─┼──[100 nF X7R]── AGND
    (pin 7)         │──[1 µF X5R]──── AGND
                    │
                    ├──[33 Ω]── AINGND1 ──[100 nF]── AGND
                    ├──[33 Ω]── AINGND2 ──[100 nF]── AGND
                    └──[33 Ω]── AINGND3 ──[100 nF]── AGND
```

> 💡 **Recommandation d'implémentation** : Prévoir l'emplacement 0402 de la ferrite en option de montage (non peuplée par défaut). Cela permet de l'ajouter sans révision PCB si des problèmes EMI sont constatés au prototype.

#### Rôle des résistances série 33 Ω sur chaque AINGND

En mode `AINx_CLP_SEL = 3` (not clamped), la résistance de clamp interne R_CLP = 500 Ω du VSP5610 est **inactive**. Les 33 Ω en série :
- Protègent la source VREF des courants de commutation des switchs SH internes
- Permettent au condensateur local de 100 nF d'agir comme réservoir de charge (impédance ≈ 0.2 Ω à 8 MHz)

```
Calcul de l'impédance à 8 MHz :
  Z(C_100nF à 8 MHz) = 1/(2π × 8×10⁶ × 100×10⁻⁹) ≈ 0.2 Ω
  → Le condensateur local fournit le courant de commutation, pas la source VREF ✅
```

---

### 16.5 Schéma Fonctionnel Complet — Partie Analogique

```
CIS LC3R216N-8008A                                   VSP5610RSHR
                    
Pin 5 (SIG1) ──[33Ω]──┬──────────────────────────► AIN1 (pin 4)
                       │
                     [100pF]                     (AINx_CLP_SEL = 3)
                       │                         (AINx_SH_CDS  = 1)
                      AGND                        (AINx_POL     = 1)
                                                  (APG_x ≈ 3.0 V/V)
Pin 3 (SIG2) ──[33Ω]──┬──────────────────────────► AIN2 (pin 6)
                       │
                     [100pF]
                       │
                      AGND

Pin 1 (SIG3) ──[33Ω]──┬──────────────────────────► AIN3 (pin 8)
                       │
                     [100pF]
                       │
                      AGND

                       ┌──[100nF X7R]── AGND  (bypass HF)
                       ├──[1µF X5R]──── AGND  (bypass BF)
Pin 7 (VREF) ──[FB?]──┤
    ~800 mV            ├──[33Ω]──────────────────► AINGND1 (pin 5) ──[100nF]── AGND
                       ├──[33Ω]──────────────────► AINGND2 (pin 7) ──[100nF]── AGND
                       └──[33Ω]──────────────────► AINGND3 (pin 9) ──[100nF]── AGND

[FB?] = Ferrite optionnelle (option de montage 0402)
```

---

### 16.6 Calcul du Gain APG Requis

```
Signal utile CIS : 0 → Vpmax = 300 mV typ (au-dessus de VREF)
Pleine échelle VSP5610 @ APG gain 1 V/V : 1 V_pp

Gain requis pour utiliser 90% de la pleine échelle :
  APG = (0.9 × 1 V) / 0.300 V = 3.0 V/V

Calcul du code registre APG_x :
  APG(V/V) = (Code + 0.5) × 3/63
  → Code = (APG × 63/3) − 0.5 = (3.0 × 21) − 0.5 = 62.5 → Code = 62 ou 63

  Code 62 → APG = (62.5 × 3/63) ≈ 2.976 V/V → signal ADC = 0.893 V (89%)
  Code 63 → APG = (63.5 × 3/63) ≈ 3.024 V/V → signal ADC = 0.907 V (91%) ✅
```

> **Note** : Le gain réel dépend de Vpmax mesuré sur le prototype. À ajuster via le registre `APG_x` et complété si besoin par `DPG_x` (gain digital × 1.0 à × 2.0).

---

### 16.7 Condensateur de Couplage AC — Nécessaire ou Non ?

**Réponse : NON (connexion directe DC recommandée)**

| Critère         | Valeur                     | Verdict                       |
|-----------------|----------------------------|-------------------------------|
| VREF nominal    | 800 mV                     | Dans [0, VDD=3.3V] ✅          |
| VREF plage spec | 600–1000 mV                | Dans [0, VDD=3.3V] ✅          |
| SIGx max        | ~1100 mV                   | Dans [0, VDD=3.3V] ✅          |
| Mode VSP5610    | AINx_CLP_SEL = 3 (ext ref) | Gère l'offset DC nativement ✅ |

**Cas où un couplage AC serait nécessaire :** si VREF mesuré sur le prototype sort de la plage [600 mV, 1000 mV]. Dans ce cas, utiliser le mode **AINx_CLP_SEL = 2** avec la référence interne V_RINT = 1.1V et ajouter un condensateur de couplage AC sur chaque AINx.

---

### 16.8 BOM Supplémentaire — Filtrage Analogique

| Qté | Réf.      | Description                 | Valeur           | Package | Note                            |
|-----|-----------|-----------------------------|------------------|---------|---------------------------------|
| 3   | R_AINx    | Résistance série SIG        | **33 Ω** 1%      | 0402    | Filtre anti-repliement SIG1/2/3 |
| 3   | C_AINx    | Condensateur filtre         | **100 pF X7R**   | 0402    | Filtre anti-repliement SIG1/2/3 |
| 3   | R_AGNDx   | Résistance série AINGND     | **33 Ω** 1%      | 0402    | Isolation switchs SH            |
| 3   | C_AGNDx   | Réservoir de charge local   | **100 nF X7R**   | 0402    | Découplage AINGND1/2/3          |
| 1   | C_VREF_HF | Bypass HF sur VREF          | **100 nF X7R**   | 0402    | Filtrage HF CISVREF             |
| 1   | C_VREF_BF | Bypass BF sur VREF          | **1 µF X5R**     | 0402    | Filtrage BF CISVREF             |
| 1   | FB_VREF   | Ferrite (option de montage) | **600 Ω@100MHz** | 0402    | BLM18PG601SN1D ou équiv.        |

**Total supplémentaire : 15 composants** (13 peuplés + 1 ferrite en option)

---

### 16.9 Recommandations Routage PCB — Spécifique Analogique

| Règle                                                         | Détail                                                    |
|---------------------------------------------------------------|-----------------------------------------------------------|
| **Traces SIG1/2/3 < 20 mm**                                   | Minimise le couplage capacitif avec les pistes numériques |
| **Plan AGND continu** sous SIG1/2/3 et VREF                   | Retour de courant le plus court possible                  |
| **Condensateurs C_AINx au plus près du VSP5610**              | < 1 mm des pins AIN1/2/3 (côté composant)                 |
| **C_VREF_HF au plus près du connecteur CIS**                  | Filtrage à la source (pin 7 CIS)                          |
| **Pas de via sur les traces SIG et VREF**                     | Inductance parasite nulle                                 |
| **SIG perpendiculaires aux pistes CLK numériques**            | Minimise le couplage inductif                             |
| **Résistances R_AGNDx entre le nœud VREF et les pins AINGND** | Placement préférentiel côté VSP5610                       |

---

### 16.10 Récapitulatif des Points d'Attention — Décisions à Valider sur Prototype

| Question                              | Action recommandée                                                              |
|---------------------------------------|---------------------------------------------------------------------------------|
| Valeur réelle de VREF (600–1000 mV ?) | Mesurer à l'oscilloscope sur le premier prototype avant validation PCB série    |
| Niveau réel de Vpmax (200–400 mV ?)   | Ajuster le code APG_x pour maximiser la dynamique ADC                           |
| Bruit HF visible sur VREF ?           | Peupler la ferrite FB_VREF si harmoniques à 8/16/24 MHz visibles                |
| Condensateur C_F = 100 pF suffisant ? | Peut être porté à 220 pF si des artéfacts EMI subsistent (7τ = 54 ns < 85 ns ✅) |
| Condensateur AC nécessaire sur AINx ? | Seulement si VREF hors plage [600–1000 mV] — sinon connexion DC directe         |

---

---

## 17. Hardware — Filtrage & Routage des Signaux Numériques (Horloges + Bus DCMI)

> **Ajout v2.4 — 14/03/2026**  
> Cette section détaille les règles de filtrage passif et de routage PCB pour les trois groupes de signaux numériques critiques : l'horloge partagée CIS_CP/RCLKP, les signaux de synchronisation ligne, et le bus DCMI 48 MHz.

---

### 17.1 Groupe 1 : CIS_CP / RCLKP — L'horloge 8 MHz partagée

#### Architecture du nœud de branchement

C'est le signal le plus critique car il est **branché sur deux charges** (CIS + VSP5610) depuis un seul GPIO STM32.

```
PA9 (TIM1_CH2)
      │
     [R_S = 22 Ω]    ← résistance série, placée < 5 mm du GPIO STM32
      │
      ●─────────────────────────────[trace ~X cm]──► CIS CLK (pin 12)
      │
      └─────────────────────────────[trace ~Y cm]──► VSP5610 RCLKP (pin 28)
```

**Règle fondamentale : la résistance série est côté source (GPIO STM32), pas côté charge.**

Si la résistance est placée au niveau du CIS ou du VSP5610, elle ne sert plus de terminaison source — elle crée juste une chute de tension. La placer au plus près du GPIO amortit le front **avant** qu'il ne se propage sur la trace.

#### Calcul de validation à 8 MHz

```
R_série = 22 Ω
C_charge = C_CIS_CLK (~5 pF) + C_RCLKP (~5 pF) + C_parasites trace (~2 pF) ≈ 12 pF

τ = 22 × 12×10⁻¹² = 264 ps
Temps de montée (10→90%) = 2.2 × τ = 581 ps

Demi-période à 8 MHz = 62.5 ns
t_r / T_demi = 581 ps / 62.5 ns = 0.93% → aucun impact sur le duty cycle ✅

Longueur d'onde à 8 MHz dans FR4 (v_prop ≈ 15 cm/ns) :
  λ = 15 cm/ns × (1/8 MHz) = 1875 mm = 187 cm
  Risque de réflexion si trace > λ/10 = 18.7 cm
  → Pas de problème pour des traces < 10 cm ✅
```

#### Règles de routage CIS_CP / RCLKP

| Règle                                         | Détail                                                                                  |
|-----------------------------------------------|-----------------------------------------------------------------------------------------|
| **Résistance série au plus proche du GPIO**   | < 5 mm de PA9, côté pad sortie                                                          |
| **Nœud T le plus court possible**             | Le stub vers le CIS et le stub vers VSP5610 partent du même pad (ou à 1-2 mm d'écart)   |
| **Plan de masse continu sous toute la trace** | Impédance de référence constante, pas de discontinuité                                  |
| **Pas de via si possible**                    | Chaque via ajoute ~0.5-1 nH d'inductance (acceptable à 8 MHz mais à éviter inutilement) |
| **Largeur trace**                             | 0.15 mm minimum (courant < 5 mA, résistance DC négligeable)                             |
| **Longueurs des deux stubs équilibrées**      | Si CIS à 30 mm et VSP5610 à 35 mm, acceptable. Éviter un rapport > 3:1.                 |

---

### 17.2 Groupe 2 : XLSYNC (PI2) et SI (PC8) — Synchronisation ligne

Ces signaux sont **moins critiques** que CIS_CP car leur fréquence effective est ~4.4 kHz (une impulsion par ligne). La contrainte est la **durée minimale d'impulsion**, pas la fréquence.

```
PI2 (TIM8_CH4) ──[33 Ω]──► VSP5610 XLSYNC (pin 45)    impulsion ≥ 375 ns
PC8 (TIM8_CH3) ──[33 Ω]──► CIS SI (pin 10)             impulsion = 125 ns
```

#### Règles de routage XLSYNC / SI

| Règle                                        | Détail                                                                                      |
|----------------------------------------------|---------------------------------------------------------------------------------------------|
| **33 Ω série standard**                      | Protège le GPIO, amortit le ringing sans contrainte de timing                               |
| **Traces courtes < 50 mm**                   | Largement suffisant ; ces signaux sont peu sensibles aux réflexions                         |
| **Plan de masse sous la trace**              | Bonne pratique systématique                                                                 |
| **Éloigner des traces analogiques SIG1/2/3** | Ces traces commutent au moment exact de l'échantillonnage ADC → espacement minimum **3 mm** |

---

### 17.3 Groupe 3 : Bus DCMI — Le cas critique à 48 MHz

C'est le groupe le plus exigeant. Le DCMI véhicule **9 signaux** à 48 MHz (D[7:0] + PIXCLK). À cette fréquence, les règles de signal intégrité s'appliquent pleinement.

#### Topologie et terminaisons

Les sorties CMOS du VSP5610 en mode 8-bit (pins 33-40) et LVCK (pin 25) sont des **drivers CMOS 3.3V** avec une impédance de sortie faible (~10-20 Ω typique). Le STM32 présente ~5 pF d'entrée par pin DCMI.

```
VSP5610 D[7:0] (pins 33-40) ──[R_S = 33 Ω]──► STM32 DCMI D[7:0]
VSP5610 GPIO2  (pin 25)     ──[R_S = 33 Ω]──► STM32 PA6 (DCMI_PIXCLK)
```

#### Calcul de validation à 48 MHz

```
R_source_VSP5610 ≈ 15 Ω (driver CMOS interne)
R_série = 33 Ω
R_total_source = 15 + 33 = 48 Ω ≈ Z_0 (50 Ω) → terminaison source quasi-adaptée ✅

C_charge_STM32 = 5 pF
τ = 48 × 5×10⁻¹² = 240 ps
t_r = 2.2 × 240 ps = 528 ps

Demi-période à 48 MHz = 10.4 ns
t_r / T_demi = 528 ps / 10.4 ns = 5.1% → acceptable ✅

Longueur critique (λ/10 à 48 MHz dans FR4) :
  λ = 15 cm/ns × (1/48 MHz) = 312 mm
  λ/10 = 31 mm ← ⚠️ Seuil de signal intégrité

→ Si les traces DCMI dépassent 31 mm, les effets de ligne de transmission commencent.
→ Objectif : maintenir toutes les traces DCMI < 30 mm si possible, < 50 mm maximum absolu.
```

#### Règles d'égalisation de longueur (length matching)

Le DCMI échantillonne D[7:0] sur le front montant de PIXCLK. Un skew excessif entre PIXCLK et une donnée peut provoquer une capture incorrecte.

```
Propagation dans FR4 : ~6.7 ps/mm

Setup time DCMI STM32H7 : ~2 ns (typique)
→ Skew maximum admissible PIXCLK ↔ D[x] : ≈ ±2 ns = ±300 mm

→ Le skew de longueur n'est PAS la contrainte limitante sur un PCB compact ✅
  (les longueurs seront bien inférieures à 300 mm)
```

Maintenir le skew entre les bits D[0]-D[7] eux-mêmes **≤ 5 mm** reste une bonne pratique de conception (pas bloquant fonctionnellement à 48 MHz).

#### Règles de routage du bus DCMI

```
             VSP5610 (QFN-56)
             ┌──────────────┐
  pin 40 ────┤ D0   ←      │──[33Ω]──────────────────────────► PH9
  pin 39 ────┤ D1   ←      │──[33Ω]──────────────────────────► PA10
  pin 38 ────┤ D2   ←      │──[33Ω]──────────────────────────► PG10
  pin 37 ────┤ D3   ←      │──[33Ω]──────────────────────────► PC9
  pin 36 ────┤ D4   ←      │──[33Ω]──────────────────────────► PC11
  pin 35 ────┤ D5   ←      │──[33Ω]──────────────────────────► PI4
  pin 34 ────┤ D6   ←      │──[33Ω]──────────────────────────► PI6
  pin 33 ────┤ D7   ←      │──[33Ω]──────────────────────────► PI7
             │              │
  pin 25 ────┤ LVCK →       │──[33Ω]──────────────────────────► PA6 (PIXCLK)
             └──────────────┘

  Placement des résistances 33 Ω :
  ┌ pad VSP5610 ┐ ← 0 à 2 mm → [33Ω] ← 0 à 50 mm de trace → ┌ pad STM32 ┐
  Les résistances sont côté VSP5610 (source), pas côté STM32 (charge).
```

| Règle                             | Valeur                                  | Justification                                                          |
|-----------------------------------|-----------------------------------------|------------------------------------------------------------------------|
| **Longueur max des traces**       | < 50 mm (idéal < 30 mm)                 | Seuil λ/10 à 48 MHz = 31 mm                                            |
| **Résistances 33 Ω côté VSP5610** | < 5 mm du pad de sortie                 | Source = VSP5610, terminaison côté source                              |
| **Espacement inter-traces D[x]**  | ≥ 3× la largeur de trace (règle 3W)     | Anti-crosstalk entre bits adjacents                                    |
| **Plan de masse continu**         | Sous toutes les traces DCMI             | Impédance ~50 Ω contrôlée                                              |
| **Via minimum**                   | ≤ 2 vias par trace                      | Chaque via = ~0.5-1 nH → 150-300 mΩ @ 48 MHz                           |
| **PIXCLK isolé des Data**         | Trace GND de garde ou espacement ≥ 5 mm | Évite le couplage horloge → données (jitter)                           |
| **Skew D[0]..D[7] entre eux**     | ≤ 5 mm idéal                            | Bonne pratique (pas bloquant à 48 MHz)                                 |
| **PIXCLK vs Data**                | PIXCLK ≤ Data en longueur               | Le front d'horloge doit arriver avant ou en même temps que les données |

---

### 17.4 Synthèse des règles par priorité

#### 🔴 Critique (non-négociable)

1. **Plan de masse continu** sous tous les signaux numériques rapides — pas de coupure, pas de fente sous les traces DCMI
2. **Résistances 33 Ω côté VSP5610** pour le bus DCMI (< 5 mm du pad)
3. **Résistance 22 Ω côté STM32** pour CIS_CP/RCLKP (< 5 mm du GPIO PA9)
4. **RCLKN connecté à GND** — ne jamais laisser flottant

#### 🟡 Important (fortement recommandé)

5. **Traces DCMI < 50 mm** — idéalement < 30 mm
6. **Espacement 3W** entre les traces D[0]-D[7]
7. **PIXCLK séparé des données** par une trace de garde GND ou ≥ 5 mm d'espace
8. **Maximum 2 vias** par trace DCMI
9. **Éloigner XLSYNC/SI des traces analogiques SIG1/2/3** — ≥ 3 mm d'espacement

#### 🟢 Bonne pratique

10. **Skew inter-données ≤ 5 mm** sur le bus D[7:0]
11. **Longueurs stubs CIS/VSP5610 équilibrées** pour CIS_CP (rapport de longueur < 3:1)
12. **Condensateurs de découplage 100 nF < 1 mm** des pins DVDD_IO du VSP5610

---

### 17.5 Récapitulatif des composants passifs de filtrage / terminaison

| Signal                   | Résistance   | Côté placement              | Condensateur additionnel |
|--------------------------|--------------|-----------------------------|--------------------------|
| CIS_CP → RCLKP + CIS CLK | **22 Ω**     | STM32 PA9 (source)          | Non                      |
| SI → CIS pin 10          | **33 Ω**     | STM32 PC8 (source)          | Non                      |
| XLSYNC → VSP5610 pin 45  | **33 Ω**     | STM32 PI2 (source)          | Non                      |
| D[7:0] → STM32           | **33 Ω × 8** | VSP5610 pins 33-40 (source) | Non                      |
| PIXCLK → PA6             | **33 Ω**     | VSP5610 pin 25 (source)     | Non                      |
| RCLKN pin 27             | —            | — (connexion GND directe)   | Non                      |

---

## Références

| Document                            | Source                                             |
|-------------------------------------|----------------------------------------------------|
| LC3R216N-8008A Datasheet            | RD/CIS/LC3R216N-8008A.pdf                          |
| VSP5610RSHR Datasheet               | RD/Etude CIS ADC/vsp5610.pdf                       |
| AN5020 - Introduction to DCMI STM32 | RD/Etude CIS ADC/an5020-...                        |
| Guide Interfaçage VSP5610 DCMI      | RD/Etude CIS ADC/Guide_Interfacage_VSP5610_DCMI.md |
| STM32H747 CubeMX Config             | RD/CubeMX/Sp3ctra.txt                              |
| Driving-AD922x-with-DCMI            | RD/Etude CIS ADC/Driving-AD922x-with-DCMI/         |
