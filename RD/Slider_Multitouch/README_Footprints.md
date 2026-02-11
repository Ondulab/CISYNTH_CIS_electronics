# Guide d'Utilisation - Footprints Slider Tactile CYAT61658

**Date:** 09/12/2025  
**Version:** 1.0  
**Projet:** Zone de Touch Slider 1D Multitouch 217mm × 8mm

---

## 📋 Vue d'Ensemble

Ce dossier contient tous les fichiers nécessaires pour créer un slider capacitif multitouch 1D utilisant le contrôleur Infineon CYAT61658-56LWA41.

### Fichiers Générés

```
R_D/Slider_Multitouch/
├── generate_slider_electrodes.py          # Script de génération
├── generated_footprints/
│   ├── Slider_TX_Electrodes.kicad_mod    # Électrodes TX (Layer 1)
│   ├── Slider_RX_Electrodes.kicad_mod    # Électrodes RX (Layer 2)
│   ├── Slider_GND_Shield.kicad_mod       # Plan GND (Layer 3)
│   └── Slider_Specifications.md          # Spécifications détaillées
├── Proposition_Technique_CYAT61658.md    # Documentation technique complète
├── BOM_Preliminaire.md                   # Liste des composants
└── README_Footprints.md                  # Ce fichier
```

---

## 🎯 Spécifications Rapides

| Paramètre | Valeur |
|-----------|--------|
| **Dimensions PCB** | 217mm × 8mm |
| **Épaisseur** | 1.0mm (4 couches FR4) |
| **Électrodes TX** | 2 bandes × 3mm × 216mm |
| **Électrodes RX** | 41 segments × 4mm × 7mm |
| **Pitch RX** | 5.0mm (centre à centre) |
| **Pattern** | Manhattan-3 (MH3) |
| **Contrôleur** | CYAT61658-56LWA41 (QFN-56) |

---

## 🚀 Guide d'Installation KiCad

### Étape 1: Préparer la Bibliothèque

**Option A: Bibliothèque Projet (Recommandé)**

```bash
# Dans votre projet KiCad
mkdir -p footprints/Slider_Touch.pretty
cp generated_footprints/*.kicad_mod footprints/Slider_Touch.pretty/
```

**Option B: Bibliothèque Globale**

```bash
# Copier dans bibliothèque KiCad globale
cp generated_footprints/*.kicad_mod ~/Documents/KiCad/7.0/footprints/Slider_Touch.pretty/
```

### Étape 2: Ajouter la Bibliothèque dans KiCad

1. Ouvrir KiCad PCB Editor
2. Menu: **Preferences** → **Manage Footprint Libraries**
3. Onglet **Project Specific Libraries** (ou Global)
4. Cliquer **Add Library** (icône dossier)
5. Naviguer vers `footprints/Slider_Touch.pretty`
6. Cliquer **OK**

### Étape 3: Configuration PCB 4 Couches

**Dans KiCad PCB Editor:**

1. Menu: **File** → **Board Setup**
2. Section **Board Stackup**
3. Configurer:

```
┌─────────────────────────────────────────┐
│ F.SilkS (Silkscreen)                    │
│ F.Mask (Solder Mask)                    │
├─────────────────────────────────────────┤
│ F.Cu (Layer 1 - Top)        35µm Cu     │ ← TX Electrodes
├─────────────────────────────────────────┤
│ Prepreg                     0.2mm       │
├─────────────────────────────────────────┤
│ In1.Cu (Layer 2 - Inner 1)  35µm Cu     │ ← RX Electrodes
├─────────────────────────────────────────┤
│ Core FR4                    0.4mm       │
├─────────────────────────────────────────┤
│ In2.Cu (Layer 3 - Inner 2)  35µm Cu     │ ← GND Shield
├─────────────────────────────────────────┤
│ Prepreg                     0.2mm       │
├─────────────────────────────────────────┤
│ B.Cu (Layer 4 - Bottom)     35µm Cu     │ ← Components + GND
├─────────────────────────────────────────┤
│ B.Mask (Solder Mask)                    │
│ B.SilkS (Silkscreen)                    │
└─────────────────────────────────────────┘
Total: ~1.0mm
```

### Étape 4: Placer les Footprints

**4.1 Créer le PCB**

```
Dimensions: 217mm × 8mm
Origine: (0, 0) au coin supérieur gauche
```

**4.2 Placer les Électrodes TX**

1. Menu: **Add** → **Footprint**
2. Chercher: `Slider_TX_Electrodes`
3. Placer à l'origine (0, 0)
4. Vérifier layer: **F.Cu (Top)**

**4.3 Placer les Électrodes RX**

1. Menu: **Add** → **Footprint**
2. Chercher: `Slider_RX_Electrodes`
3. Placer à l'origine (0, 0)
4. **IMPORTANT:** Changer layer vers **In1.Cu (Inner 1)**
   - Sélectionner le footprint
   - Appuyer **E** (Edit)
   - Changer "Layer" → **In1.Cu**

**4.4 Placer le Plan GND Shield**

1. Menu: **Add** → **Footprint**
2. Chercher: `Slider_GND_Shield`
3. Placer à l'origine (0, 0)
4. **IMPORTANT:** Changer layer vers **In2.Cu (Inner 2)**

**4.5 Placer le CYAT61658**

1. Télécharger footprint QFN-56 (voir section Ressources)
2. Placer sur **B.Cu (Bottom)** au centre:
   - Position X: ~108mm (milieu du slider)
   - Position Y: ~4mm (centré verticalement)

---

## 🔌 Connexions et Routage

### Connexions RX vers CYAT61658

**Les 41 électrodes RX doivent être connectées aux pins du contrôleur:**

```
Mapping RX → CYAT61658 Pins (QFN-56):

RX[0]  → Pin 14 (XY00)    RX[21] → Pin 49 (XY21)
RX[1]  → Pin 13 (XY01)    RX[22] → Pin 47 (XY22)
RX[2]  → Pin 12 (XY02)    RX[23] → Pin 46 (XY23)
RX[3]  → Pin 11 (XY03)    RX[24] → Pin 45 (XY24)
RX[4]  → Pin 10 (XY04)    RX[25] → Pin 44 (XY25)
RX[5]  → Pin 9  (XY05)    RX[26] → Pin 43 (XY26)
RX[6]  → Pin 8  (XY06)    RX[27] → Pin 42 (XY27)
RX[7]  → Pin 7  (XY07)    RX[28] → Pin 41 (XY28)
RX[8]  → Pin 6  (XY08)    RX[29] → Pin 40 (XY29)
RX[9]  → Pin 5  (XY09)    RX[30] → Pin 39 (XY30)
RX[10] → Pin 4  (XY10)    RX[31] → Pin 38 (XY31)
RX[11] → Pin 3  (XY11)    RX[32] → Pin 37 (XY32)
RX[12] → Pin 2  (XY12)    RX[33] → Pin 36 (XY33)
RX[13] → Pin 1  (XY13)    RX[34] → Pin 35 (XY34)
RX[14] → Pin 56 (XY14)    RX[35] → Pin 34 (XY35)
RX[15] → Pin 55 (XY15)    RX[36] → Pin 33 (XY36)
RX[16] → Pin 54 (XY16)    RX[37] → Pin 32 (XY37)
RX[17] → Pin 53 (XY17)    RX[38] → Pin 31 (XY38)
RX[18] → Pin 52 (XY18)    RX[39] → Pin 30 (XY39)
RX[19] → Pin 51 (XY19)    RX[40] → Pin 29 (XY40)
RX[20] → Pin 50 (XY20)
```

**Méthode de routage:**
- Utiliser les vias déjà présents dans le footprint RX
- Router sur Layer 4 (Bottom) vers le contrôleur
- Largeur trace: 0.15-0.2mm
- Éviter parallélisme > 5mm entre traces RX

### Connexions TX vers CYAT61658

```
TX1 → Pin à configurer (ex: XY41 si disponible)
TX2 → Pin à configurer (ex: XY42 si disponible)
```

**Note:** Vérifier la configuration exacte dans la datasheet CYAT61658.

### Alimentation et Communication

**Voir schéma dans:** `Proposition_Technique_CYAT61658.md` section "Schéma de Connexion"

**Résumé:**
```
VDDA (Pin 27)   ← 3.3V via 1.0Ω + 0.1µF + 1µF
VDDD (Pin 24)   ← 3.3V via 4.7µF + 0.1µF
VCCD (Pin 23)   ← 0.1µF vers GND
VCCTX (Pin 28)  ← 0.22µF vers GND (si TX pump activé)

I²C:
P0[0] (Pin 16)  ← SCL (pull-up 2.2kΩ)
P0[1] (Pin 17)  ← SDA (pull-up 2.2kΩ)
P1[3] (Pin 22)  ← INT vers host

Reset:
XRES (Pin 18)   ← Pull-up 10kΩ vers VDDD
```

---

## ⚙️ Règles de Design (DRC)

### Clearances Minimales

```
Électrode TX ↔ Électrode TX:  1.0mm (gap)
Électrode RX ↔ Électrode RX:  1.0mm (gap)
Électrode ↔ Bord PCB:         0.5mm
Électrode ↔ Via:              0.3mm
Trace ↔ Trace:                0.15mm
Via ↔ Via:                    0.5mm
```

### Dimensions Traces

```
Signaux RX/TX:     0.15-0.2mm
Alimentation:      0.3-0.5mm
GND:               Plan continu
```

### Vias

```
Diamètre pad:      0.6mm
Diamètre drill:    0.3mm
Via stitching:     Espacement 5-10mm
```

---

## 🔍 Vérifications Avant Fabrication

### Checklist Design

- [ ] **Alignement électrodes**
  - [ ] TX et RX parfaitement alignées (origine 0,0)
  - [ ] Pas de décalage entre layers
  
- [ ] **Layers corrects**
  - [ ] TX sur F.Cu (Layer 1)
  - [ ] RX sur In1.Cu (Layer 2)
  - [ ] GND Shield sur In2.Cu (Layer 3)
  - [ ] Composants sur B.Cu (Layer 4)

- [ ] **Connexions**
  - [ ] Toutes les 41 RX connectées au contrôleur
  - [ ] TX1 et TX2 connectées
  - [ ] Alimentation complète
  - [ ] I²C/SPI routé

- [ ] **DRC Clean**
  - [ ] Pas d'erreurs clearance
  - [ ] Pas de traces non connectées
  - [ ] Pas de vias orphelins

- [ ] **Fabrication**
  - [ ] Stack-up 4 couches configuré
  - [ ] Épaisseur totale = 1.0mm
  - [ ] Finition ENIG spécifiée
  - [ ] Solder mask sur F et B uniquement

---

## 📦 Export pour Fabrication

### Gerbers à Générer

```bash
# Dans KiCad PCB Editor
File → Fabrication Outputs → Gerbers

Layers à inclure:
✓ F.Cu (Top copper)
✓ In1.Cu (Inner 1 copper)
✓ In2.Cu (Inner 2 copper)
✓ B.Cu (Bottom copper)
✓ F.Mask (Top solder mask)
✓ B.Mask (Bottom solder mask)
✓ F.SilkS (Top silkscreen)
✓ B.SilkS (Bottom silkscreen)
✓ Edge.Cuts (Board outline)

Drill files:
✓ PTH (Plated Through Holes)
✓ NPTH (Non-Plated Through Holes)
```

### Fichiers Fabrication

```
Gerbers/
├── Slider_Touch-F_Cu.gbr
├── Slider_Touch-In1_Cu.gbr
├── Slider_Touch-In2_Cu.gbr
├── Slider_Touch-B_Cu.gbr
├── Slider_Touch-F_Mask.gbr
├── Slider_Touch-B_Mask.gbr
├── Slider_Touch-F_SilkS.gbr
├── Slider_Touch-B_SilkS.gbr
├── Slider_Touch-Edge_Cuts.gbr
├── Slider_Touch-PTH.drl
└── Slider_Touch-NPTH.drl
```

### Notes Fabricant

**À inclure dans les instructions:**

```
PCB Specifications:
- Dimensions: 217mm × 8mm
- Layers: 4 (FR4)
- Thickness: 1.0mm ±0.1mm
- Copper: 35µm (1oz) all layers
- Surface finish: ENIG (gold)
- Solder mask: Green/Black (both sides)
- Silkscreen: White
- Min trace: 0.15mm
- Min spacing: 0.15mm
- Min drill: 0.3mm

Stack-up:
Layer 1 (F.Cu):    35µm Cu
Prepreg:           0.2mm
Layer 2 (In1.Cu):  35µm Cu
Core:              0.4mm FR4
Layer 3 (In2.Cu):  35µm Cu
Prepreg:           0.2mm
Layer 4 (B.Cu):    35µm Cu
Total:             ~1.0mm

Special notes:
- Capacitive touch sensor - handle with care
- No solder mask on touch electrodes (F.Cu)
- Precise layer alignment critical
```

---

## 🛠️ Modification du Script

### Paramètres Configurables

Si vous devez modifier les dimensions, éditez `generate_slider_electrodes.py`:

```python
# Ligne 15-30 du script
SLIDER_LENGTH = 217.0  # Modifier longueur
SLIDER_WIDTH = 8.0     # Modifier largeur
RX_COUNT = 41          # Modifier nombre RX
RX_PITCH = 5.0         # Modifier espacement RX
TX_WIDTH = 3.0         # Modifier largeur TX
TX_GAP = 1.0           # Modifier gap entre TX
```

**Puis régénérer:**

```bash
cd R_D/Slider_Multitouch
python3 generate_slider_electrodes.py
```

---

## 📚 Ressources Complémentaires

### Documentation Projet

1. **Proposition_Technique_CYAT61658.md**
   - Spécifications complètes
   - Analyse de risques
   - Budget et planning

2. **BOM_Preliminaire.md**
   - Liste des composants
   - Références fournisseurs

3. **Slider_Specifications.md** (généré)
   - Positions exactes des électrodes
   - Vérifications dimensionnelles

### Footprints Externes Nécessaires

**CYAT61658-56LWA41 (QFN-56):**

- **SnapEDA:** https://www.snapeda.com/
  - Chercher "CYAT61658" ou "QFN-56-8x8-0.5"
  - Télécharger format KiCad

- **Component Search Engine:** https://componentsearchengine.com/
  - Chercher "CYAT61658"

- **KiCad Library:** Package_DFN_QFN
  - `QFN-56-1EP_8x8mm_P0.5mm_EP4.5x5.2mm`

### Documentation Infineon (Sous NDA)

**À demander à:** automotive@infineon.com

1. **001-50467** - Module Design Best Practices
2. **001-49389** - Performance Definitions
3. **001-83948** - Touch Tuning Host Emulator Guide
4. **Firmware SDK** - Code source et API

---

## ⚠️ Points d'Attention Critiques

### 1. Alignement des Layers

**CRITIQUE:** Les électrodes TX (Layer 1) et RX (Layer 2) doivent être parfaitement alignées.

**Vérification:**
- Placer tous les footprints à l'origine (0, 0)
- Utiliser la vue 3D pour vérifier l'alignement
- Vérifier que les intersections TX/RX sont correctes

### 2. Clearance Châssis Aluminium

**Le slider sera monté dans un châssis aluminium:**
- Maintenir 2-3mm de clearance entre électrodes et châssis
- Prévoir points de connexion GND au châssis
- Tester avec châssis réel dès prototype 1

### 3. EMI Carte Mère

**La carte mère sera à 1mm sous le PCB slider:**
- Le plan GND Layer 3 est CRITIQUE pour le shielding
- Via stitching Layer 3 ↔ Layer 4 obligatoire
- Tester avec carte mère active

### 4. Overlay Plastique

**Un overlay plastique de 2mm sera collé sur le PCB:**
- Pas de solder mask sur les électrodes TX (Layer 1)
- Surface doit être plane et propre
- Tester adhésion overlay sur ENIG

---

## 🐛 Dépannage

### Problème: Footprints non visibles dans KiCad

**Solution:**
1. Vérifier que la bibliothèque est bien ajoutée
2. Menu: Preferences → Manage Footprint Libraries
3. Vérifier le chemin vers `Slider_Touch.pretty`
4. Redémarrer KiCad

### Problème: Électrodes sur mauvais layer

**Solution:**
1. Sélectionner le footprint
2. Appuyer **E** (Edit Properties)
3. Changer "Layer" vers le layer correct:
   - TX → F.Cu
   - RX → In1.Cu
   - GND → In2.Cu

### Problème: DRC erreurs clearance

**Solution:**
1. Vérifier Board Setup → Design Rules
2. Ajuster clearances si nécessaire:
   - Copper to copper: 0.15mm
   - Hole to hole: 0.5mm
3. Vérifier que les électrodes ne se chevauchent pas

### Problème: Via stitching manquants

**Solution:**
- Les vias sont inclus dans le footprint `Slider_GND_Shield`
- Vérifier que le footprint est bien placé
- Si besoin, ajouter manuellement des vias GND

---

## 📞 Support

### Questions Techniques

**Infineon Support:**
- Email: automotive@infineon.com
- Forum: community.infineon.com

**KiCad Support:**
- Forum: forum.kicad.info
- Discord: discord.gg/kicad

### Bugs Script Python

**Reporter sur:**
- GitHub du projet (si disponible)
- Email projet

---

## 📝 Changelog

### Version 1.0 (2025-12-09)
- ✅ Génération initiale des footprints
- ✅ 41 électrodes RX, pitch 5mm
- ✅ 2 électrodes TX, largeur 3mm
- ✅ Plan GND shield avec via stitching
- ✅ Documentation complète

---

## ✅ Prochaines Étapes

1. **Immédiat:**
   - [ ] Importer footprints dans KiCad
   - [ ] Créer nouveau projet PCB
   - [ ] Configurer stack-up 4 couches

2. **Court terme:**
   - [ ] Télécharger footprint CYAT61658
   - [ ] Placer tous les composants
   - [ ] Router connexions RX

3. **Moyen terme:**
   - [ ] Compléter routage alimentation/I²C
   - [ ] Vérifier DRC
   - [ ] Générer Gerbers

4. **Avant fabrication:**
   - [ ] Contacter Infineon pour validation design
   - [ ] Commander overlay plastique
   - [ ] Préparer banc de test

---

**Bonne chance avec votre projet de slider tactile! 🚀**
