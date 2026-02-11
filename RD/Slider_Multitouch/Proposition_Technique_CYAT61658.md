# Proposition Technique - Slider Multitouch CYAT61658-56LWA41

**Date:** 09/12/2025  
**Projet:** Zone de Touch Slider 1D Multitouch  
**Contrôleur:** Infineon CYAT61658-56LWA41  
**Statut:** ✅ FAISABLE avec conditions

---

## 📋 Résumé Exécutif

Cette proposition technique valide la faisabilité d'un slider capacitif multitouch 1D utilisant le contrôleur Infineon CYAT61658-56LWA41 pour une zone de touch de **217mm × 8mm** avec overlay plastique de **2mm** d'épaisseur.

### Caractéristiques Principales
- **Dimensions:** 217mm (L) × 8mm (l)
- **Type:** Slider 1D (détection position X uniquement)
- **Détection simultanée:** Jusqu'à 8 doigts
- **Overlay:** Plastique 2mm d'épaisseur
- **PCB:** Double couche
- **Environnement:** Châssis aluminium + carte mère à 1mm

---

## 🎯 Spécifications Système

### 1. Contrôleur CYAT61658-56LWA41

#### Caractéristiques Clés
- **Package:** 56-lead QFN wettable flank (8×8×1mm)
- **Pins de sense:** 41 I/O configurables (TX/RX)
- **CPU:** 32-bit ARM Cortex à 48MHz
- **Capacité multitouch:** Jusqu'à 10 doigts simultanés
- **Refresh rate:** Jusqu'à 250Hz (configurable)
- **Communication:** I²C (100/400 kbps) ou SPI (jusqu'à 8 Mbps)
- **Température:** Grade-A: -40°C à 85°C | Grade-S: -40°C à 105°C

#### Fonctionnalités Avancées
- ✅ Auto armor technology (immunité EMI)
- ✅ Water rejection (dual sense)
- ✅ Wet-finger tracking
- ✅ Glove support (< 1mm thin, < 5mm thick)
- ✅ Large object rejection
- ✅ Look-for-touch low-power mode
- ✅ Field upgrades via bootloader

### 2. Performance Attendue

| Paramètre | Valeur | Unité |
|-----------|--------|-------|
| **Accuracy** | 0.5 | mm |
| **Jitter** | 0.5 | mm |
| **Refresh rate** | 60-250 | Hz |
| **Response time** | < 30 | ms |
| **Swipe speed** | Jusqu'à 1000 | mm/s |
| **Doigts simultanés** | 8 (10 max) | - |
| **Taille doigt min** | 4 | mm |
| **Power Active** | ~180 | mW |
| **Power Deep Sleep** | 11 | µW |

---

## 🔧 Architecture Technique

### 1. Configuration Électrodes

#### Disposition Recommandée
```
┌─────────────────────────────────────────────────────────────┐
│  TX1 ████████████████████████████████████████████████████   │ 3mm
│      ─────────────────────────────────────────────────────   │ 1mm gap
│  TX2 ████████████████████████████████████████████████████   │ 3mm
└─────────────────────────────────────────────────────────────┘
    ↑     ↑     ↑     ↑     ↑     ↑     ↑     ↑     ↑
   RX0   RX5   RX10  RX15  RX20  RX25  RX30  RX35  RX40
   
   217mm de long / 5mm pitch = 43-44 électrodes RX
```

#### Paramètres
- **Électrodes RX:** 41 segments (pitch 5mm)
- **Électrodes TX:** 2 bandes parallèles continues
- **Configuration:** 41 RX × 2 TX = 82 intersections
- **Pattern capteur:** Manhattan-3 (MH3) recommandé

### 2. Stack-up PCB 4 Couches (RECOMMANDÉ pour Shielding EMI Optimal)

**Configuration optimale pour isolation EMI carte mère:**

```
┌────────────────────────────────────────────────────────┐
│  Overlay Plastique (2mm)                               │
├────────────────────────────────────────────────────────┤
│  Layer 1 (Top - 35µm Cu):                              │
│  - TX électrodes (2 bandes 3mm)                        │
│  - GND fill hachuré 50% autour                         │
│  - Solder mask vert/noir                               │
├────────────────────────────────────────────────────────┤
│  Prepreg (~0.2mm)                                       │
├────────────────────────────────────────────────────────┤
│  Layer 2 (Inner 1 - 35µm Cu):                          │
│  - RX électrodes (41 segments)                         │
│  - GND fill hachuré 50% autour                         │
│  - Isolation 0.5mm entre RX adjacents                  │
├────────────────────────────────────────────────────────┤
│  Core FR4 (~0.4mm)                                      │
├────────────────────────────────────────────────────────┤
│  Layer 3 (Inner 2 - 35µm Cu):                          │
│  - Plan GND hachuré 60-70% (SHIELDING)                 │
│  - Via stitching vers Layer 4 (5-10mm)                 │
│  - Pas de routage signal                               │
├────────────────────────────────────────────────────────┤
│  Prepreg (~0.2mm)                                       │
├────────────────────────────────────────────────────────┤
│  Layer 4 (Bottom - 35µm Cu):                           │
│  - Plan GND continu (SHIELDING)                        │
│  - Zone composants (CYAT61658)                         │
│  - Routage signaux numériques                          │
│  - Via stitching vers Layer 3                          │
└────────────────────────────────────────────────────────┘
   Total épaisseur: ~1.0mm ✅
         ↓ 1mm gap
┌────────────────────────────────────────────────────────┐
│  Carte Mère (EMI bloqué par double plan GND L3+L4)    │
└────────────────────────────────────────────────────────┘
```

**Avantages configuration 4 couches:**
- ✅ **Shielding EMI optimal** avec double plan GND (L3 + L4)
- ✅ **Séparation TX/RX** sur couches différentes = moins de crosstalk
- ✅ **Impédance contrôlée** pour meilleure intégrité signal
- ✅ **Via stitching** crée une cage de Faraday
- ✅ **Isolation carte mère** maximale (critique à 1mm distance)

**Alternative 2 couches (budget limité):**

```
┌─────────────────────────────────────────────────────┐
│  Overlay Plastique (2mm)                            │
├─────────────────────────────────────────────────────┤
│  Layer 1 (Top): Électrodes TX (2 bandes)           │
│  - Largeur: 3mm chacune                             │
│  - Espacement: 1mm                                  │
│  - GND fill hachuré 50%                             │
├─────────────────────────────────────────────────────┤
│  Core FR4 (0.8-1.0mm)                               │
├─────────────────────────────────────────────────────┤
│  Layer 2 (Bottom): Électrodes RX + Plan de masse   │
│  - 41 segments perpendiculaires                     │
│  - Routage vers contrôleur                          │
│  - Plan de masse hachuré 50% pour shielding EMI    │
└─────────────────────────────────────────────────────┘
         ↓ 1mm gap
┌─────────────────────────────────────────────────────┐
│  Carte Mère (source EMI potentielle)                │
└─────────────────────────────────────────────────────┘
```

**Note:** Configuration 2 couches acceptable mais shielding EMI limité. 
Recommandation forte pour 4 couches vu proximité carte mère (1mm).

### 3. Pattern Capteur: Manhattan-3 (MH3)

**Pourquoi MH3?**
- ✅ Optimal pour overlay ≥ 1mm (vs SSD problématique < 1mm)
- ✅ Bon compromis signal disparity
- ✅ Design simplifié pour largeur réduite (8mm)
- ✅ Meilleure linéarité pour détection de position X
- ✅ Moins sensible aux variations d'épaisseur overlay

**Alternative:** Dual-Solid Diamond (DSD) si SNR insuffisant

---

## ⚡ Gestion EMI et Shielding

### 1. Problématiques Identifiées

| Source | Impact | Criticité |
|--------|--------|-----------|
| Carte mère à 1mm | Bruit haute fréquence | 🔴 HAUTE |
| Châssis aluminium | Couplage capacitif | 🔴 HAUTE |
| Alimentation switching | Ripple basse fréquence | 🟡 MOYENNE |
| Signaux numériques | Crosstalk | 🟡 MOYENNE |

### 2. Solutions de Mitigation

#### A. Shielding PCB Slider
```
Plan de masse continu sur Layer 2 (Bottom):
- Connexion au châssis alu via plusieurs points
- Via stitching entre layers (espacement 5mm max)
- Clearance 0.5mm minimum autour électrodes actives
```

#### B. Isolation Châssis Aluminium
- **Clearance:** Minimum 2-3mm entre électrodes actives et châssis
- **Guard trace:** Anneau de garde connecté à VDDA via résistance 1kΩ
- **Grounding:** Points de masse multiples pour drain EMI

#### C. Filtrage Alimentation
```
VDDA (3.0-4.7V):
  - Résistance série: 1.0Ω (5% tolérance)
  - Capacité découplage: 0.1µF (X7R) + 1µF (X5R)
  - Capacité bulk: 2.2µF (pour bruit basse fréquence)

VDDA_Q (RX analog):
  - Résistance série: 1.0Ω (5% tolérance)
  - Capacité découplage: 0.1µF (X7R) + 1µF (X5R)

VDDD (1.8V ou 3.0-5.5V):
  - Capacité découplage: 0.1µF (X7R)
  - Capacité bulk: 4.7µF (X5R)

VCCD (1.71-1.95V):
  - Capacité découplage: 0.1µF (X7R)

VCCTX (TX pump, si activé):
  - Capacité: 0.22µF (X7R)
```

#### D. Routage Critique
- **Traces RX/TX:** Courtes et directes, largeur 0.2mm minimum
- **Espacement:** 0.15mm minimum entre traces
- **Via:** Minimiser le nombre, diamètre 0.3mm
- **Ground stitching:** Via GND tous les 5mm le long des traces sensibles
- **Crosstalk:** Éviter parallélisme traces RX/TX > 5mm

---

## 📐 Spécifications PCB Détaillées

### 1. Paramètres Fabrication

#### Configuration 4 Couches (RECOMMANDÉE)

| Paramètre | Valeur | Notes |
|-----------|--------|-------|
| **Substrate** | FR4 standard | Épaisseur totale 1.0mm |
| **Nombre de couches** | 4 | L1: TX, L2: RX, L3: GND, L4: GND+Comp |
| **Stack-up détaillé** | Voir ci-dessous | Optimisé shielding EMI |
| **Finition surface** | ENIG (or) | Durabilité + conductivité |
| **Épaisseur cuivre** | 35µm (1oz) | Toutes couches |
| **Largeur trace min** | 0.15mm | 0.2mm recommandé |
| **Espacement min** | 0.15mm | Entre électrodes |
| **Diamètre via** | 0.3mm | Drill 0.2mm |
| **Via stitching** | 5-10mm | Entre L3 et L4 |
| **Solder mask** | Vert/Noir | Côté composants |
| **Silkscreen** | Blanc | Marquages |

**Stack-up 4 couches détaillé:**
- Layer 1 (Top): 35µm Cu + Solder mask
- Prepreg: 0.2mm (εr = 4.2)
- Layer 2 (Inner 1): 35µm Cu
- Core: 0.4mm FR4 (εr = 4.5)
- Layer 3 (Inner 2): 35µm Cu
- Prepreg: 0.2mm (εr = 4.2)
- Layer 4 (Bottom): 35µm Cu + Solder mask
- **Total: ~1.0mm**

#### Configuration 2 Couches (Alternative budget)

| Paramètre | Valeur | Notes |
|-----------|--------|-------|
| **Substrate** | FR4 standard | Épaisseur 0.8-1.0mm |
| **Nombre de couches** | 2 | Top: TX, Bottom: RX + GND |
| **Finition surface** | ENIG (or) | Durabilité + conductivité |
| **Épaisseur cuivre** | 35µm (1oz) | Standard |
| **Largeur trace min** | 0.15mm | 0.2mm recommandé |
| **Espacement min** | 0.15mm | Entre électrodes |
| **Diamètre via** | 0.3mm | Drill 0.2mm |
| **Solder mask** | Vert/Noir | Côté composants |
| **Silkscreen** | Blanc | Marquages |

### 2. Dimensions Électrodes

#### Configuration 4 Couches

**Électrodes TX (Layer 1 - Top):**
- Longueur: 217mm
- Largeur: 3mm chacune
- Espacement: 1mm
- Nombre: 2 bandes parallèles
- GND fill: Hachuré 50% autour

**Électrodes RX (Layer 2 - Inner 1):**
- Longueur: ~7mm (largeur utile)
- Largeur: 4mm
- Pitch: 5mm
- Nombre: 41 segments
- Isolation: 0.5mm entre RX adjacents
- GND fill: Hachuré 50% autour

**Plan GND Shield (Layer 3 - Inner 2):**
- Type: Plan hachuré 60-70%
- Via stitching: Tous les 5-10mm vers L4
- Fonction: Shielding EMI primaire

**Plan GND + Composants (Layer 4 - Bottom):**
- Type: Plan continu maximum
- Zone composants: CYAT61658 + passifs
- Via stitching: Connexion vers L3
- Fonction: Shielding EMI + routage

#### Configuration 2 Couches (Alternative)

**Électrodes TX (Layer Top):**
- Longueur: 217mm
- Largeur: 3mm chacune
- Espacement: 1mm
- Nombre: 2 bandes parallèles
- GND fill: Hachuré 50%

**Électrodes RX (Layer Bottom):**
- Longueur: ~7mm (largeur utile)
- Largeur: 4mm
- Pitch: 5mm
- Nombre: 41 segments
- Plan GND: Hachuré 50%

### 3. Placement Composants

#### Configuration 4 Couches

```
Position CYAT61658-56LWA41 (Layer 4):
- Centré sur la longueur du PCB
- Côté Bottom Layer 4
- Orientation: pins vers zone RX pour routage court
- Clearance: 2mm minimum du bord PCB
- Via vers Layer 2 (RX) pour connexions courtes

Composants passifs (Layer 4):
- Proximité immédiate du contrôleur (< 5mm)
- Condensateurs découplage au plus près des pins
- Résistances série VDDA/VDDA_Q côté alimentation
- Routage sur Layer 4 avec GND plan

Via Stitching (Layer 3 ↔ Layer 4):
- Grille régulière 5-10mm
- Sous zone active des électrodes
- Crée cage de Faraday pour shielding
```

**Pattern Via Stitching:**
```
Vue de dessus:

●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●
   TX1 ████████████████████
●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●
   ─────────────────────────
●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●
   TX2 ████████████████████
●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●

● = Via GND L3 ↔ L4 (espacement 5-10mm)
```

#### Configuration 2 Couches

```
Position CYAT61658-56LWA41:
- Centré sur la longueur du PCB
- Côté Bottom (opposé aux électrodes TX)
- Orientation: pins vers électrodes RX pour routage court
- Clearance: 2mm minimum du bord PCB

Composants passifs:
- Proximité immédiate du contrôleur (< 5mm)
- Condensateurs découplage au plus près des pins
- Résistances série VDDA/VDDA_Q côté alimentation
```

---

## 🔌 Schéma de Connexion

### 1. Alimentation

```
Source 3.3V ──┬── 1.0Ω ──┬── 0.1µF ──┬── VDDA (Pin 27)
              │          │           │
              │          └── 1µF ────┤
              │                      │
              ├── 1.0Ω ──┬── 0.1µF ──┼── VDDA_Q (Pin 32, TQFP uniquement)
              │          │           │
              │          └── 1µF ────┤
              │                      │
              └── 4.7µF ──┬── 0.1µF ─┴── VDDD (Pin 24)
                          │
                          └── 0.1µF ──── VCCD (Pin 23)

TX Pump (si activé):
VCCTX (Pin 28) ── 0.22µF ── GND
```

### 2. Communication I²C

```
Host MCU                    CYAT61658
────────                    ─────────
SDA ──┬── 2.2kΩ ── VDD      P0[1] (Pin 17)
      │
SCL ──┴── 2.2kΩ ── VDD      P0[0] (Pin 16)

INT ────────────────────    P1[3] (Pin 22) COMM_INT
```

**Alternative SPI:**
```
Host MCU                    CYAT61658
────────                    ─────────
SCLK ──────────────────     P0[0] (Pin 16)
MOSI ──────────────────     P0[1] (Pin 17)
MISO ──────────────────     P1[0] (Pin 19)
SS ────────────────────     P1[1] (Pin 20)
INT ───────────────────     P1[3] (Pin 22)
```

### 3. Reset et Debug

```
XRES (Pin 18) ──┬── 10kΩ ── VDDD
                │
                └── Bouton ── GND

Debug SWD:
SWDCLK ─────────────────    P1[0] (Pin 19)
SWDIO ──────────────────    P1[1] (Pin 20)
```

---

## ⚠️ Analyse de Risques

### Matrice de Risques

| # | Risque | Probabilité | Impact | Criticité | Mitigation |
|---|--------|-------------|---------|-----------|------------|
| 1 | EMI carte mère | 🔴 HAUTE | 🟡 Moyen | **HAUTE** | Shielding + plan masse + filtrage |
| 2 | Effet châssis alu | 🔴 HAUTE | 🔴 Élevé | **CRITIQUE** | Clearance 2-3mm + guard + grounding |
| 3 | Signal disparity 2mm | 🟡 MOYENNE | 🟡 Moyen | **MOYENNE** | Pattern MH3 + calibration firmware |
| 4 | Crosstalk 8mm largeur | 🟡 MOYENNE | 🟡 Moyen | **MOYENNE** | Routing soigné + guard traces |
| 5 | Fusion touches proches | 🟡 MOYENNE | 🟢 Faible | **FAIBLE** | Algorithme séparation + tuning |
| 6 | Water rejection | 🟢 FAIBLE | 🟢 Faible | **FAIBLE** | Dual-sense activé par défaut ✅ |
| 7 | Température extrême | 🟢 FAIBLE | 🟡 Moyen | **FAIBLE** | Grade-A qualifié -40°C à 85°C ✅ |

### Plans de Mitigation Détaillés

#### Risque #1: EMI Carte Mère
**Actions:**
1. Plan de masse continu sur Layer 2
2. Via stitching tous les 5mm
3. Filtrage alimentation renforcé (2.2µF au lieu de 1µF)
4. Film de cuivre adhésif entre PCB slider et carte mère (optionnel)
5. Tests EMI précoces sur prototype

#### Risque #2: Effet Châssis Aluminium
**Actions:**
1. Clearance minimum 2-3mm entre électrodes et châssis
2. Guard trace périmétrique connectée à VDDA via 1kΩ
3. Connexions masse multiples au châssis (4-6 points)
4. Tests avec châssis réel dès prototype 1
5. Ajustement mécanique si nécessaire

#### Risque #3: Signal Disparity
**Actions:**
1. Utilisation pattern MH3 (optimisé pour 2mm)
2. Calibration firmware extensive
3. Tests avec différentes épaisseurs (1.8-2.2mm)
4. Tuning avec TTHE (Touch Tuning Host Emulator)

---

## 📅 Planning et Jalons

### Phase 1: Design (3 semaines)

**Semaine 1-2: Schematic et Layout**
- [ ] Schematic CYAT61658 avec alimentation
- [ ] Placement composants optimisé
- [ ] Routage électrodes TX/RX
- [ ] Plan de masse et shielding
- [ ] Design Rule Check (DRC)

**Semaine 3: Validation**
- [ ] Revue design interne
- [ ] Validation Infineon (sous NDA, doc 001-50467)
- [ ] DFM check avec fabricant PCB
- [ ] Génération Gerbers et BOM

**Livrables:**
- Schematic PDF
- Layout PCB (KiCad/Altium)
- Gerbers + drill files
- BOM complète
- Document de design

### Phase 2: Prototype (4 semaines)

**Semaine 4-5: Fabrication**
- [ ] Commande PCB (5 pcs, délai 10-15 jours)
- [ ] Commande composants (Digikey/Mouser)
- [ ] Préparation stencil soudure

**Semaine 6: Assemblage**
- [ ] Assemblage PCB (manuel ou prestataire)
- [ ] Inspection visuelle et AOI
- [ ] Tests électriques de base
- [ ] Programmation firmware initial

**Semaine 7: Tests Initiaux**
- [ ] Test communication I²C/SPI
- [ ] Vérification alimentations
- [ ] Premier scan capacitif
- [ ] Détection touch basique

**Livrables:**
- 5 PCB assemblés
- Rapport d'assemblage
- Firmware v0.1
- Rapport tests initiaux

### Phase 3: Tuning et Validation (3 semaines)

**Semaine 8: Tuning**
- [ ] Installation TTHE (Touch Tuning Host Emulator)
- [ ] Calibration baseline
- [ ] Optimisation seuils détection
- [ ] Tuning multitouch (8 doigts)
- [ ] Tests swipe et gestures

**Semaine 9: Tests Environnementaux**
- [ ] Tests température (-40°C à 85°C)
- [ ] Tests humidité
- [ ] Tests water rejection
- [ ] Tests wet finger
- [ ] Tests avec gants (optionnel)

**Semaine 10: Validation EMI/EMC**
- [ ] Tests avec châssis aluminium
- [ ] Tests avec carte mère active
- [ ] Mesures EMI/EMC (pré-compliance)
- [ ] Optimisations si nécessaire

**Livrables:**
- Firmware v1.0 tuné
- Rapport de tuning TTHE
- Rapport tests environnementaux
- Rapport EMI/EMC
- Recommandations pour production

### Phase 4: Itération (si nécessaire, 2-3 semaines)

**Semaine 11-13: Corrections**
- [ ] Modifications design basées sur tests
- [ ] Prototype v2 si nécessaire
- [ ] Re-validation
- [ ] Documentation finale

---

## 💰 Budget Estimatif

### Prototype Phase 1 - Configuration 4 Couches (RECOMMANDÉE)

| Poste | Quantité | Prix Unitaire | Total | Notes |
|-------|----------|---------------|-------|-------|
| **PCB Fabrication 4L** | 5 pcs | 90€ | 450€ | Prototype 4 couches, délai 12-15j |
| **CYAT61658-56LWA41** | 5 pcs | 25€ | 125€ | Samples Infineon possibles |
| **Composants passifs** | 1 kit | 50€ | 50€ | Condensateurs, résistances |
| **Connecteurs** | 5 sets | 10€ | 50€ | I²C, alimentation |
| **Assemblage** | 5 pcs | 60€ | 300€ | Prestataire ou manuel |
| **Overlay plastique** | 5 pcs | 30€ | 150€ | Découpe sur mesure |
| **Frais divers** | - | - | 75€ | Shipping, imprévus |
| **TOTAL Phase 1 (4L)** | | | **1200€** | |

### Prototype Phase 1 - Configuration 2 Couches (Alternative Budget)

| Poste | Quantité | Prix Unitaire | Total | Notes |
|-------|----------|---------------|-------|-------|
| **PCB Fabrication 2L** | 5 pcs | 50€ | 250€ | Prototype 2 couches, délai 10j |
| **CYAT61658-56LWA41** | 5 pcs | 25€ | 125€ | Samples Infineon possibles |
| **Composants passifs** | 1 kit | 50€ | 50€ | Condensateurs, résistances |
| **Connecteurs** | 5 sets | 10€ | 50€ | I²C, alimentation |
| **Assemblage** | 5 pcs | 60€ | 300€ | Prestataire ou manuel |
| **Overlay plastique** | 5 pcs | 30€ | 150€ | Découpe sur mesure |
| **Frais divers** | - | - | 75€ | Shipping, imprévus |
| **TOTAL Phase 1 (2L)** | | | **1000€** | |

**Comparaison 2L vs 4L:**
- Surcoût 4 couches: +200€ (+20%)
- Avantage: Shielding EMI optimal (critique vu proximité carte mère)
- Recommandation: **4 couches fortement conseillé**

### Outils et Logiciels

| Outil | Coût | Notes |
|-------|------|-------|
| **TTHE** | Gratuit | Touch Tuning Host Emulator (Infineon) |
| **KiCad** | Gratuit | Design PCB |
| **Firmware SDK** | Gratuit | Sous NDA Infineon |
| **Analyseur logique** | 0-500€ | Si non disponible (I²C debug) |

### Coût Total Projet (3 itérations)

#### Configuration 4 Couches (RECOMMANDÉE)

| Phase | Coût |
|-------|------|
| Prototype 1 (4L) | 1200€ |
| Prototype 2 (ajustements 4L) | 950€ |
| Prototype 3 (validation finale 4L) | 750€ |
| Outils (si achat nécessaire) | 500€ |
| **TOTAL PROJET (4L)** | **3400€** |

#### Configuration 2 Couches (Alternative)

| Phase | Coût |
|-------|------|
| Prototype 1 (2L) | 1000€ |
| Prototype 2 (ajustements 2L) | 800€ |
| Prototype 3 (validation finale 2L) | 600€ |
| Outils (si achat nécessaire) | 500€ |
| **TOTAL PROJET (2L)** | **2900€** |

**Analyse Coût/Bénéfice:**
- Surcoût 4 couches: +500€ (+17% du projet total)
- Bénéfices 4 couches:
  - ✅ Shielding EMI optimal (critique à 1mm de la carte mère)
  - ✅ Réduction risque d'échec prototype
  - ✅ Moins d'itérations probables
  - ✅ Performance finale supérieure
- **Verdict:** Investissement justifié pour environnement EMI critique

---

## 📚 Documentation Requise

### Documents Infineon (sous NDA)

**À demander à automotive@infineon.com:**

1. **001-50467** - PSoC™ Automotive Multitouch touchscreen controller module design best practices
   - Guidelines FPC/PCB design
   - Recommandations shielding EMI
   - Exemples de layouts

2. **001-49389** - PSoC™ Automotive Multitouch touchscreen controller user interface performance definitions
   - Définitions paramètres performance
   - Méthodologies de test
   - Critères d'acceptation

3. **001-83948** - Touch Tuning Host Emulator user guide
   - Guide utilisation TTHE
   - Procédures de calibration
   - Optimisation paramètres

4. **Firmware SDK**
   - Code source firmware
   - API documentation
   - Exemples d'application

### Standards et Normes

- **ISO11452** - Component test methods for electrical disturbances in Road Vehicles
- **CISPR25** - Radio disturbance characteristics for automotive
- **J-STD-020D.1** - Moisture/Reflow Sensitivity Classification
- **IPC-2221** - Generic Standard on Printed Board Design

---

## 🔍 Checklist Pré-Design

### Validation Mécanique
- [ ] Dimensions finales confirmées (217mm × 8mm)
- [ ] Épaisseur overlay validée (2mm ± tolérance)
- [ ] Type de plastique sélectionné (PET recommandé)
- [ ] Méthode de fixation PCB/overlay définie
- [ ] Clearance châssis aluminium vérifiée (2-3mm)
- [ ] Points de montage PCB identifiés

### Validation Électrique
- [ ] Tension alimentation disponible (3.3V ou 5V)
- [ ] Interface communication choisie (I²C ou SPI)
- [ ] Pins disponibles sur carte mère identifiés
- [ ] Niveau logique compatible (1.8V ou 3.3V)
- [ ] Courant disponible vérifié (200mA max)

### Validation Environnementale
- [ ] Plage température opération définie
- [ ] Exposition eau/humidité évaluée
- [ ] Niveau EMI environnement estimé
- [ ] Contraintes mécaniques (vibrations) connues

### Validation Logicielle
- [ ] Host MCU identifié (STM32, ESP32, etc.)
- [ ] Ressources CPU disponibles (I²C/SPI driver)
- [ ] Framework logiciel existant
- [ ] Besoins en gestures définis

---

## 🎓 Recommandations Techniques

### 1. Choix du Plastique Overlay

**Recommandé: PET (Polyéthylène Téréphtalate)**
- ✅ Bonne constante diélectrique (εr ≈ 3.2)
- ✅ Flexible et résistant
- ✅ Coût modéré
- ✅ Facile à découper/former
- ⚠️ Sensible aux rayures (traitement anti-rayures recommandé)

**Alternative: Polycarbonate (PC)**
- ✅ Très résistant mécaniquement
- ✅ Bonne clarté optique
- ⚠️ Constante diélectrique plus élevée (εr ≈ 3.0)
- ⚠️ Plus coûteux

**À éviter: Verre**
- ❌ Trop rigide pour 8mm de large
- ❌ Risque de casse
- ✅ Mais excellentes propriétés électriques

### 2. Optimisation Performance

**Pour maximiser le SNR (Signal-to-Noise Ratio):**
1. Utiliser TX pump activé (effective 20V drive)
2. Optimiser nombre de TX pulses (8-16 recommandé)
3. Filtrage numérique agressif (IIR + FIR)
4. Baseline tracking automatique activé
5. Frequency hopping si EMI important

**Pour minimiser le jitter:**
1. Refresh rate stable (60Hz ou 120Hz)
2. Moyennage temporel (3-5 samples)
3. Filtrage prédictif (Kalman filter)
4. Compensation température activée

### 3. Gestion Multitouch 8 Doigts

**Limitations physiques:**
- Espacement minimum entre doigts: ~10mm
- Sur 217mm: 8 doigts = espacement moyen 27mm ✅
- Risque de fusion si doigts trop proches (< 8mm)

**Algorithmes recommandés:**
- Large finger tracking (évite split en 2 touches)
- Touch separation algorithm
- Palm rejection
- Edge compensation

### 4. Stratégie de Test

**Tests unitaires (chaque PCB):**
1. Continuité électrique
2. Court-circuits
3. Valeurs composants
4. Communication I²C/SPI
5. Scan capacitif baseline

**Tests fonctionnels:**
1. Détection 1 doigt (tous les points)
2. Détection 2-8 doigts simultanés
3. Swipe lent/rapide
4. Water rejection
5. Température extrêmes

**Tests EMC (pré-compliance):**
1. Émissions conduites
2. Émissions rayonnées
3. Immunité ESD
4. Immunité EFT/Burst
5. Immunité champs RF

---

## 📞 Contacts et Support

### Infineon Technologies
- **Email:** automotive@infineon.com
- **Objet:** "CYAT61658 Slider Design Support - NDA Request"
- **Demander:**
  - Accès documentation technique (NDA)
  - Samples CYAT61658-56LWA41
  - Support technique design review
  - Accès TTHE software

### Fabricants PCB Recommandés
- **JLCPCB** - Prototypes rapides, bon rapport qualité/prix
- **PCBWay** - Qualité supérieure, bon support technique
- **Eurocircuits** - Européen, excellent pour prototypes

### Distributeurs Composants
- **Digikey** - Stock important, livraison rapide
- **Mouser** - Alternative fiable
- **Farnell** - Présence européenne

---

## 📈 Critères de Succès

### Phase Prototype
- ✅ PCB assemblé sans défaut
- ✅ Communication I²C/SPI fonctionnelle
- ✅ Détection touch basique opérationnelle
- ✅ Pas de court-circuit ou surchauffe

### Phase Tuning
- ✅ Détection 8 doigts simultanés stable
- ✅ Accuracy < 1mm sur toute la longueur
- ✅ Jitter < 1mm
- ✅ Refresh rate ≥ 60Hz
- ✅ Pas de faux positifs

### Phase Validation
- ✅ Tests température -40°C à 85°C passés
- ✅ Water rejection fonctionnel
- ✅ EMI/EMC pré-compliance OK
- ✅ Intégration châssis + carte mère validée
- ✅ Durabilité mécanique confirmée

---

## 🚀 Prochaines Actions

### Immédiat (Semaine 1)
1. ✅ Valider cette proposition technique
2. [ ] Contacter Infineon pour NDA et samples
3. [ ] Confirmer dimensions mécaniques finales
4. [ ] Choisir type de plastique overlay
5. [ ] Sélectionner interface communication (I²C/SPI)

### Court Terme (Semaine 2-3)
1. [ ] Démarrer design schematic
2. [ ] Commander composants longue lead-time
3. [ ] Préparer environnement développement
4. [ ] Installer TTHE software
5. [ ] Définir protocole de test

### Moyen Terme (Semaine 4-8)
1. [ ] Finaliser layout PCB
2. [ ] Commander prototype 1
3. [ ] Développer firmware initial
4. [ ] Préparer banc de test
5. [ ] Planifier tests EMI

---

## 📝 Notes et Considérations

### Points d'Attention Critiques

1. **Châssis Aluminium**
   - Le couplage capacitif avec le châssis est le risque #1
   - Tests précoces avec châssis réel INDISPENSABLES
   - Prévoir ajustements mécaniques (clearance, grounding)

2. **Carte Mère à 1mm**
   - Distance très faible = couplage EMI fort
   - Shielding et filtrage CRITIQUES
   - Envisager film de cuivre adhésif si problèmes

3. **Largeur 8mm**
   - Limite physique pour multitouch 2D
   - Mode 1D uniquement (position X)
   - Acceptable pour slider linéaire

4. **Overlay 2mm**
   - Épaisseur acceptable avec pattern MH3
   - Calibration firmware essentielle
   - Tester avec tolérances ±0.2mm

### Optimisations Futures

**Si performance insuffisante:**
1. Augmenter largeur à 10-12mm (meilleur SNR)
2. Réduire overlay à 1.5mm (meilleur signal)
3. Ajouter layer de shielding (PCB 4 couches)
4. Utiliser pattern DSD au lieu de MH3

**Si coût trop élevé:**
1. Réduire nombre de prototypes
