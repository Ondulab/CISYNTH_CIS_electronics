# Schéma KiCad STM32H747XIHx - Sp3ctra

## 📋 Vue d'ensemble

Ce document décrit le schéma KiCad généré automatiquement pour le microcontrôleur **STM32H747XIHx** du projet Sp3ctra.

### Fichiers générés
- `Sp3ctra_STM32.kicad_sch` - Schéma KiCad principal
- `generate_stm32_schema.py` - Script de génération automatique

## 🔧 Configuration du STM32H747XIHx

### Caractéristiques
- **MCU**: STM32H747XIHx (Dual Core Cortex-M7 + Cortex-M4)
- **Package**: TFBGA-265 (14x14mm, pitch 0.8mm)
- **Mémoire**: 2048KB Flash, 1024KB RAM
- **Fréquence**: Jusqu'à 480 MHz
- **Pins configurés**: 102 pins

## 📊 Périphériques configurés

### 🎥 DCMI (Digital Camera Interface)
Interface 8 bits pour capteur d'image CIS

| Signal | Pin | Description |
|--------|-----|-------------|
| DCMI_D0 | PH9 (R13) | Data bit 0 |
| DCMI_D1 | PA10 (D14) | Data bit 1 |
| DCMI_D2 | PG10 (A9) | Data bit 2 |
| DCMI_D3 | PC9 (E14) | Data bit 3 |
| DCMI_D4 | PC11 (B13) | Data bit 4 |
| DCMI_D5 | PI4 (A4) | Data bit 5 |
| DCMI_D6 | PI6 (A2) | Data bit 6 |
| DCMI_D7 | PI7 (B3) | Data bit 7 |
| DCMI_HSYNC | PA4 (U3) | Horizontal sync |
| DCMI_PIXCLK | PA6 (R3) | Pixel clock |
| DCMI_VSYNC | PI5 (A3) | Vertical sync |

### 🌐 ETH (Ethernet RMII)
Interface Ethernet RMII pour communication réseau

| Signal | Pin | Description |
|--------|-----|-------------|
| ETH_CRS_DV | PA7 (R5) | Carrier sense/data valid |
| ETH_MDC | PC1 (M2) | Management data clock |
| ETH_MDIO | PA2 (N3) | Management data I/O |
| ETH_REF_CLK | PA1 (N4) | Reference clock (50MHz) |
| ETH_RXD0 | PC4 (T4) | Receive data bit 0 |
| ETH_RXD1 | PC5 (U4) | Receive data bit 1 |
| ETH_TXD0 | PG13 (D9) | Transmit data bit 0 |
| ETH_TXD1 | PG14 (D8) | Transmit data bit 1 |
| ETH_TX_EN | PG11 (B9) | Transmit enable |

**Label personnalisé:**
- ETH_RST (PC14/C2) - Reset Ethernet PHY

### 💾 FMC (Flexible Memory Controller)
Interface SDRAM 16 bits, 12 adresses

**Signaux de contrôle:**
| Signal | Pin | Description |
|--------|-----|-------------|
| FMC_SDCKE0 | PC3 (M4) | Clock enable |
| FMC_SDNE0 | PC2 (M3) | Chip enable |
| FMC_SDCLK | PG8 (F15) | Clock |
| FMC_SDNCAS | PG15 (D6) | Column address strobe |
| FMC_SDNRAS | PF11 (T7) | Row address strobe |
| FMC_SDNWE | PC0 (L2) | Write enable |
| FMC_NBL0 | PE0 (C4) | Byte mask 0 |
| FMC_NBL1 | PE1 (B4) | Byte mask 1 |

**Bus d'adresses (12 bits):**
- FMC_A0 à FMC_A11 : PF0-PF5, PF12-PF15, PG0-PG1

**Bank address:**
- FMC_BA0 (PG4/H14), FMC_BA1 (PG5/G14)

**Bus de données (16 bits):**
- FMC_D0 à FMC_D15 : PD14-PD15, PD0-PD1, PD8-PD10, PE7-PE15

### 🔌 I2C
Deux interfaces I2C configurées

**I2C2:**
- I2C2_SCL : PH4 (P3)
- I2C2_SDA : PH5 (P4)

**I2C3:**
- I2C3_SCL : PA8 (E15)
- I2C3_SDA : PH8 (T13)

### 🔲 QUADSPI
Interface Quad-SPI pour mémoire Flash externe

| Signal | Pin | Description |
|--------|-----|-------------|
| QUADSPI_BK1_IO0 | PF8 (K4) | Data 0 |
| QUADSPI_BK1_IO1 | PF9 (L4) | Data 1 |
| QUADSPI_BK1_IO2 | PF7 (K3) | Data 2 |
| QUADSPI_BK1_IO3 | PF6 (K2) | Data 3 |
| QUADSPI_BK1_NCS | PB10 (P11) | Chip select |
| QUADSPI_CLK | PF10 (L3) | Clock |

### 🔄 SPI
Trois interfaces SPI configurées

**SPI1** (Full-Duplex Master):
- SPI1_MISO : PG9 (A10)
- SPI1_MOSI : PB5 (A5)
- SPI1_SCK : PB3 (C6)

**SPI2** (Full-Duplex Master avec NSS):
- SPI2_MISO : PB14 (U15)
- SPI2_MOSI : PB15 (T15)
- SPI2_SCK : PD3 (B12)
- SPI2_NSS : PB9 (D4) → **Label: MEMS_CS**

**SPI4** (Full-Duplex Master avec NSS):
- SPI4_MISO : PE5 (D1)
- SPI4_MOSI : PE6 (E5)
- SPI4_SCK : PE2 (C3)
- SPI4_NSS : PE4 (D2)

### ⏱️ TIM (Timers)
Sorties PWM pour contrôle CIS et LEDs

| Timer | Canal | Pin | Label |
|-------|-------|-----|-------|
| TIM1_CH2 | PA9 (D15) | CIS_CP | Clock CIS |
| TIM3_CH1 | PC6 (F14) | CIS_LED_B | LED Bleue |
| TIM4_CH2 | PD13 (R17) | CIS_LED_R | LED Rouge |
| TIM5_CH3 | PH12 (R14) | CIS_LED_G | LED Verte |
| TIM8_CH3 | PC8 (E13) | CIS_SP | Signal CIS |

### 📡 USART1
Interface série asynchrone

- USART1_RX : PB7 (C5)
- USART1_TX : PB6 (B5)

### 🔌 GPIO
Signaux généraux

| Signal | Pin | Label | Description |
|--------|-----|-------|-------------|
| PA15 (A14) | GPIO_Input | MEMS_FSYNC | MEMS Frame Sync |
| PA12 (E16) | GPIO_Output | CIS_RS | CIS Reset |
| PC14 (C2) | GPIO_Output | ETH_RST | Ethernet Reset |
| PG6 (G15) | GPIO_Output | EN_12V | Enable 12V |
| PG2 (H16) | GPIO_Output | EN_5V | Enable 5V |
| PJ8 (N13) | GPIO_EXTI8 | MEMS_INT | MEMS Interrupt |

### 🪲 DEBUG
Interface de débogage Serial Wire Debug (SWD)

- DEBUG_JTCK-SWCLK : PA14 (B14)
- DEBUG_JTMS-SWDIO : PA13 (C15)

### 🎛️ RCC (Clock)
Oscillateur principal

- RCC_OSC_IN : PH0 (J2)
- RCC_OSC_OUT : PH1 (J1)

### 📺 DSIHOST (Display Serial Interface)
Interface MIPI DSI pour écran

| Signal | Pin | Description |
|--------|-----|-------------|
| DSIHOST_CKP | DSI_CKP (L16) | Clock positive |
| DSIHOST_CKN | DSI_CKN (L17) | Clock negative |
| DSIHOST_D0P | DSI_D0P (M16) | Data lane 0 positive |
| DSIHOST_D0N | DSI_D0N (M17) | Data lane 0 negative |
| DSIHOST_D1P | DSI_D1P (K16) | Data lane 1 positive |
| DSIHOST_D1N | DSI_D1N (K17) | Data lane 1 negative |

## 🛠️ Utilisation

### Ouvrir le schéma dans KiCad

```bash
# Ouvrir avec KiCad 8.0 ou supérieur
kicad Sp3ctra_STM32.kicad_sch
```

### Régénérer le schéma

Si vous devez modifier la configuration :

1. Éditez le fichier `generate_stm32_schema.py`
2. Modifiez le tableau `PIN_CONFIG`
3. Exécutez le script :

```bash
python3 generate_stm32_schema.py
```

## 📝 Notes importantes

### Format du package
- **TFBGA-265** : 17x17 balls, pitch 0.8mm
- Nomenclature BGA : Lettres (A-U) + Nombres (1-17)
- Exemple : R13 = Rangée R, Colonne 13

### Alimentation
⚠️ Les pins d'alimentation (VDD, VSS, VDDA, VSSA, etc.) ne sont pas inclus dans ce schéma.
Ils doivent être ajoutés manuellement selon les recommandations ST:
- Découplage par condensateurs sur chaque paire VDD/VSS
- Filtrage analogique pour VDDA/VSSA
- Régulation appropriée pour VDDLDO, VCAP, etc.

### Horloge système
- Oscillateur externe : HSE 25MHz typique
- RCC_OSC_IN/OUT : Quartz + condensateurs de charge

### Reset
- Pin NRST : Pull-up + bouton reset
- Circuit RC pour power-on reset

## 🎯 Signaux spécifiques CIS

Les signaux suivants sont spécifiques au capteur d'image linéaire (CIS):

| Signal | Description | Utilisation |
|--------|-------------|-------------|
| CIS_CP | Clock Pulse | Horloge principale du capteur |
| CIS_SP | Start Pulse | Signal de démarrage de ligne |
| CIS_RS | Reset Signal | Reset du capteur |
| CIS_LED_R | LED Rouge | Éclairage rouge |
| CIS_LED_G | LED Verte | Éclairage vert |
| CIS_LED_B | LED Bleue | Éclairage bleu |

## 📚 Références

- [STM32H747XI Datasheet](https://www.st.com/resource/en/datasheet/stm32h747xi.pdf)
- [STM32H7 Reference Manual](https://www.st.com/resource/en/reference_manual/rm0399-stm32h745755-and-stm32h747757-advanced-armbased-32bit-mcus-stmicroelectronics.pdf)
- Configuration CubeMX : `RD/CubeMX/Sp3ctra.ioc`

## 🔄 Historique

- **2026-02-11** : Génération initiale du schéma
  - 102 pins configurés
  - Tous les périphériques principaux inclus
  - Labels personnalisés ajoutés

## 📧 Contact

Projet CISYNTH - Sp3ctra CIS Electronics

---

*Schéma généré automatiquement par `generate_stm32_schema.py`*
