# Slider Tactile - Spécifications Électrodes
Généré le: 2025-12-09 15:02:40

## Configuration Globale
- Dimensions PCB: 217.0mm × 8.0mm
- Épaisseur: 1.0mm (4 couches FR4)
- Marges PCB: 0.5mm

## Électrodes TX (Layer 1 - Top)
- Nombre: 2 bandes parallèles
- Largeur: 3.0mm chacune
- Longueur: 216.0mm
- Gap entre TX1 et TX2: 1.0mm
- Positions Y:
  - TX1: 0.5mm → 3.5mm
  - TX2: 4.5mm → 7.5mm

## Électrodes RX (Layer 2 - Inner 1)
- Nombre: 41 segments
- Largeur: 4.0mm
- Hauteur: 7.0mm
- Pitch (centre à centre): 5.0mm
- Marge gauche: 6.0mm
- Position Y: 0.5mm → 7.5mm

### Positions RX (extrait):

| RX# | Centre X (mm) | Left X (mm) | Right X (mm) |
|-----|---------------|-------------|---------------|
|  0  |    8.0        |   6.0       |   10.0        |
|  1  |   13.0        |  11.0       |   15.0        |
|  2  |   18.0        |  16.0       |   20.0        |
| 19  |  103.0        | 101.0       |  105.0        |
| 20  |  108.0        | 106.0       |  110.0        |
| 21  |  113.0        | 111.0       |  115.0        |
| 38  |  198.0        | 196.0       |  200.0        |
| 39  |  203.0        | 201.0       |  205.0        |
| 40  |  208.0        | 206.0       |  210.0        |

... (41 électrodes au total)

## Vérifications Dimensionnelles
- Longueur utilisée par RX: 216.0mm
- Longueur PCB disponible: 217.0mm
- Marge restante: 1.0mm ✓

## Plan GND Shield (Layer 3 - Inner 2)
- Type: Hachuré 60-70%
- Via stitching: Grille 7mm × 7mm
- Diamètre via: 0.6mm (drill 0.3mm)

## Layer 4 (Bottom)
- Plan GND continu
- Zone composants (CYAT61658-56LWA41)
- Routage signaux numériques

## Fichiers Générés
1. `Slider_TX_Electrodes.kicad_mod` - Électrodes TX (Layer 1)
2. `Slider_RX_Electrodes.kicad_mod` - Électrodes RX (Layer 2)
3. `Slider_GND_Shield.kicad_mod` - Plan GND + via stitching (Layer 3)
4. `Slider_Specifications.md` - Ce fichier

## Utilisation dans KiCad
1. Copier les fichiers .kicad_mod dans votre bibliothèque de footprints
2. Ajouter la bibliothèque dans KiCad (Preferences > Manage Footprint Libraries)
3. Placer les footprints sur le PCB:
   - Slider_TX_Electrodes sur Layer F.Cu (Top)
   - Slider_RX_Electrodes sur Layer In1.Cu (Inner 1)
   - Slider_GND_Shield sur Layer In2.Cu (Inner 2)

## Notes Importantes
- Les électrodes TX et RX doivent être alignées précisément
- Vérifier le DRC après placement
- Les vias de connexion RX doivent traverser vers Layer 4 (Bottom)
- Respecter les clearances autour des électrodes actives

## Prochaines Étapes
1. Importer dans KiCad
2. Placer le CYAT61658-56LWA41 sur Layer 4
3. Router les connexions RX vers le contrôleur
4. Ajouter les composants passifs
5. Compléter le routage I²C/SPI/Power
6. Vérifier DRC et contraintes de fabrication
