#!/usr/bin/env python3
"""
Script de génération des électrodes pour slider tactile CYAT61658
Génère les footprints KiCad pour les électrodes TX et RX

Configuration: 217mm × 8mm, 41 RX, 2 TX, Pattern Manhattan-3
PCB: 4 couches FR4 1.0mm
"""

import os
from datetime import datetime

# ============================================================================
# PARAMÈTRES DE CONFIGURATION
# ============================================================================

# Dimensions globales du slider
SLIDER_LENGTH = 217.0  # mm - Longueur totale
SLIDER_WIDTH = 8.0     # mm - Largeur totale
PCB_MARGIN = 0.5       # mm - Marge de sécurité bord PCB

# Électrodes RX (Layer 2 - Inner 1)
RX_COUNT = 41          # Nombre d'électrodes RX
RX_PITCH = 5.0         # mm - Espacement centre à centre
RX_WIDTH = 4.0         # mm - Largeur de chaque RX
RX_HEIGHT = 7.0        # mm - Hauteur (couvre TX1 + gap + TX2)
RX_MARGIN_X = 6.0      # mm - Marge gauche pour centrage

# Électrodes TX (Layer 1 - Top)
TX_COUNT = 2           # Nombre de bandes TX
TX_WIDTH = 3.0         # mm - Largeur de chaque bande TX
TX_GAP = 1.0           # mm - Gap entre TX1 et TX2
TX_LENGTH = SLIDER_LENGTH - (2 * PCB_MARGIN)  # mm

# Vias de connexion
VIA_DIAMETER = 0.6     # mm - Diamètre via (drill 0.3mm)
VIA_DRILL = 0.3        # mm - Diamètre perçage

# Layers KiCad
LAYER_TOP = "F.Cu"
LAYER_INNER1 = "In1.Cu"
LAYER_INNER2 = "In2.Cu"
LAYER_BOTTOM = "B.Cu"

# ============================================================================
# FONCTIONS DE GÉNÉRATION
# ============================================================================

def generate_kicad_header(name, description):
    """Génère l'en-tête d'un fichier footprint KiCad"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f'''(footprint "{name}" (version 20221018) (generator pcbnew)
  (layer "F.Cu")
  (descr "{description}")
  (tags "capacitive touch slider electrode")
  (attr board_only exclude_from_pos_files exclude_from_bom)
  (fp_text reference "REF**" (at 0 -1) (layer "F.SilkS")
    (effects (font (size 1 1) (thickness 0.15)))
    (tstamp {generate_uuid()})
  )
  (fp_text value "{name}" (at 0 1) (layer "F.Fab")
    (effects (font (size 1 1) (thickness 0.15)))
    (tstamp {generate_uuid()})
  )
  (fp_text user "Generated: {timestamp}" (at 0 2.5) (layer "Cmts.User")
    (effects (font (size 0.5 0.5) (thickness 0.1)))
    (tstamp {generate_uuid()})
  )
'''

def generate_uuid():
    """Génère un UUID simple pour KiCad"""
    import uuid
    return str(uuid.uuid4())

def generate_rectangle(x1, y1, x2, y2, layer, width=0.1):
    """Génère un rectangle KiCad (zone filled)"""
    uuid = generate_uuid()
    return f'''  (fp_poly
    (pts
      (xy {x1} {y1})
      (xy {x2} {y1})
      (xy {x2} {y2})
      (xy {x1} {y2})
    )
    (stroke (width {width}) (type solid))
    (fill solid)
    (layer "{layer}")
    (tstamp {uuid})
  )
'''

def generate_pad(number, x, y, width, height, layer, shape="rect"):
    """Génère un pad KiCad"""
    uuid = generate_uuid()
    layers = f'"{layer}"' if isinstance(layer, str) else ' '.join([f'"{l}"' for l in layer])
    return f'''  (pad "{number}" smd {shape} (at {x} {y}) (size {width} {height})
    (layers {layers})
    (tstamp {uuid})
  )
'''

def generate_via(x, y, number=""):
    """Génère un via de connexion"""
    uuid = generate_uuid()
    return f'''  (pad "{number}" thru_hole circle (at {x} {y}) (size {VIA_DIAMETER} {VIA_DIAMETER})
    (drill {VIA_DRILL})
    (layers "*.Cu" "*.Mask")
    (tstamp {uuid})
  )
'''

def generate_kicad_footer():
    """Génère le pied de page d'un fichier footprint KiCad"""
    return ")\n"

# ============================================================================
# GÉNÉRATION ÉLECTRODES TX
# ============================================================================

def generate_tx_electrodes():
    """Génère le footprint pour les 2 électrodes TX (Layer 1 - Top)"""
    
    output = generate_kicad_header(
        "Slider_TX_Electrodes",
        f"Slider TX electrodes - 2 bands {TX_WIDTH}mm × {TX_LENGTH}mm"
    )
    
    # TX1 - Bande supérieure
    tx1_y_start = PCB_MARGIN
    tx1_y_end = PCB_MARGIN + TX_WIDTH
    tx1_x_start = PCB_MARGIN
    tx1_x_end = PCB_MARGIN + TX_LENGTH
    
    output += f"  # TX1 - Upper band\n"
    output += generate_rectangle(
        tx1_x_start, tx1_y_start,
        tx1_x_end, tx1_y_end,
        LAYER_TOP
    )
    
    # TX2 - Bande inférieure
    tx2_y_start = PCB_MARGIN + TX_WIDTH + TX_GAP
    tx2_y_end = tx2_y_start + TX_WIDTH
    tx2_x_start = PCB_MARGIN
    tx2_x_end = PCB_MARGIN + TX_LENGTH
    
    output += f"  # TX2 - Lower band\n"
    output += generate_rectangle(
        tx2_x_start, tx2_y_start,
        tx2_x_end, tx2_y_end,
        LAYER_TOP
    )
    
    # Pads de connexion pour TX1 et TX2
    output += f"  # Connection pads\n"
    output += generate_pad("TX1", tx1_x_start + 2, (tx1_y_start + tx1_y_end) / 2, 
                          2, TX_WIDTH, LAYER_TOP)
    output += generate_pad("TX2", tx2_x_start + 2, (tx2_y_start + tx2_y_end) / 2, 
                          2, TX_WIDTH, LAYER_TOP)
    
    output += generate_kicad_footer()
    return output

# ============================================================================
# GÉNÉRATION ÉLECTRODES RX
# ============================================================================

def generate_rx_electrodes():
    """Génère le footprint pour les 41 électrodes RX (Layer 2 - Inner 1)"""
    
    output = generate_kicad_header(
        "Slider_RX_Electrodes",
        f"Slider RX electrodes - {RX_COUNT} segments {RX_WIDTH}mm × {RX_HEIGHT}mm, pitch {RX_PITCH}mm"
    )
    
    # Calcul des positions
    rx_y_start = PCB_MARGIN
    rx_y_end = PCB_MARGIN + RX_HEIGHT
    
    output += f"  # RX Electrodes - {RX_COUNT} segments\n"
    
    for i in range(RX_COUNT):
        # Position X du centre de l'électrode RX[i]
        rx_center_x = RX_MARGIN_X + (i * RX_PITCH) + (RX_WIDTH / 2)
        rx_x_start = rx_center_x - (RX_WIDTH / 2)
        rx_x_end = rx_center_x + (RX_WIDTH / 2)
        
        # Génération du rectangle pour RX[i]
        output += f"  # RX[{i}] at X={rx_center_x:.1f}mm\n"
        output += generate_rectangle(
            rx_x_start, rx_y_start,
            rx_x_end, rx_y_end,
            LAYER_INNER1
        )
        
        # Pad de connexion au centre de chaque RX
        output += generate_pad(
            f"RX{i}", 
            rx_center_x, 
            (rx_y_start + rx_y_end) / 2,
            RX_WIDTH * 0.8,  # Pad légèrement plus petit que l'électrode
            RX_HEIGHT * 0.8,
            LAYER_INNER1
        )
        
        # Via de connexion vers Layer 4 (en haut de l'électrode)
        via_x = rx_center_x
        via_y = rx_y_start + 1.0  # 1mm du bord supérieur
        output += generate_via(via_x, via_y, f"RX{i}")
    
    output += generate_kicad_footer()
    return output

# ============================================================================
# GÉNÉRATION PLAN GND LAYER 3
# ============================================================================

def generate_gnd_shield():
    """Génère le footprint pour le plan GND shield (Layer 3 - Inner 2)"""
    
    output = generate_kicad_header(
        "Slider_GND_Shield",
        f"GND shield plane with via stitching - Layer 3"
    )
    
    # Plan GND hachuré (représenté par une zone)
    output += f"  # GND Shield plane (hatched 60-70%)\n"
    output += generate_rectangle(
        PCB_MARGIN, PCB_MARGIN,
        SLIDER_LENGTH - PCB_MARGIN, SLIDER_WIDTH - PCB_MARGIN,
        LAYER_INNER2
    )
    
    # Via stitching - grille 7mm × 7mm
    via_spacing_x = 7.0  # mm
    via_spacing_y = 7.0  # mm
    
    output += f"  # Via stitching grid (7mm × 7mm)\n"
    
    x = RX_MARGIN_X
    via_count = 0
    while x < (SLIDER_LENGTH - RX_MARGIN_X):
        y = PCB_MARGIN + 1.0
        while y < (SLIDER_WIDTH - PCB_MARGIN - 1.0):
            output += generate_via(x, y, f"GND{via_count}")
            via_count += 1
            y += via_spacing_y
        x += via_spacing_x
    
    output += f"  # Total via stitching: {via_count}\n"
    output += generate_kicad_footer()
    return output

# ============================================================================
# GÉNÉRATION DOCUMENTATION
# ============================================================================

def generate_documentation():
    """Génère un fichier de documentation avec les spécifications"""
    
    doc = f"""# Slider Tactile - Spécifications Électrodes
Généré le: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Configuration Globale
- Dimensions PCB: {SLIDER_LENGTH}mm × {SLIDER_WIDTH}mm
- Épaisseur: 1.0mm (4 couches FR4)
- Marges PCB: {PCB_MARGIN}mm

## Électrodes TX (Layer 1 - Top)
- Nombre: {TX_COUNT} bandes parallèles
- Largeur: {TX_WIDTH}mm chacune
- Longueur: {TX_LENGTH}mm
- Gap entre TX1 et TX2: {TX_GAP}mm
- Positions Y:
  - TX1: {PCB_MARGIN}mm → {PCB_MARGIN + TX_WIDTH}mm
  - TX2: {PCB_MARGIN + TX_WIDTH + TX_GAP}mm → {PCB_MARGIN + 2*TX_WIDTH + TX_GAP}mm

## Électrodes RX (Layer 2 - Inner 1)
- Nombre: {RX_COUNT} segments
- Largeur: {RX_WIDTH}mm
- Hauteur: {RX_HEIGHT}mm
- Pitch (centre à centre): {RX_PITCH}mm
- Marge gauche: {RX_MARGIN_X}mm
- Position Y: {PCB_MARGIN}mm → {PCB_MARGIN + RX_HEIGHT}mm

### Positions RX (extrait):
"""
    
    # Tableau des positions RX
    doc += "\n| RX# | Centre X (mm) | Left X (mm) | Right X (mm) |\n"
    doc += "|-----|---------------|-------------|---------------|\n"
    
    for i in [0, 1, 2, 19, 20, 21, 38, 39, 40]:  # Échantillon
        rx_center_x = RX_MARGIN_X + (i * RX_PITCH) + (RX_WIDTH / 2)
        rx_left = rx_center_x - (RX_WIDTH / 2)
        rx_right = rx_center_x + (RX_WIDTH / 2)
        doc += f"| {i:2d}  | {rx_center_x:6.1f}        | {rx_left:5.1f}       | {rx_right:6.1f}        |\n"
    
    doc += f"\n... (41 électrodes au total)\n"
    
    # Calculs de vérification
    total_rx_length = RX_MARGIN_X + (RX_COUNT - 1) * RX_PITCH + RX_WIDTH + RX_MARGIN_X
    doc += f"""
## Vérifications Dimensionnelles
- Longueur utilisée par RX: {total_rx_length:.1f}mm
- Longueur PCB disponible: {SLIDER_LENGTH}mm
- Marge restante: {SLIDER_LENGTH - total_rx_length:.1f}mm ✓

## Plan GND Shield (Layer 3 - Inner 2)
- Type: Hachuré 60-70%
- Via stitching: Grille 7mm × 7mm
- Diamètre via: {VIA_DIAMETER}mm (drill {VIA_DRILL}mm)

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
"""
    
    return doc

# ============================================================================
# FONCTION PRINCIPALE
# ============================================================================

def main():
    """Fonction principale - génère tous les fichiers"""
    
    print("=" * 70)
    print("Générateur d'Électrodes pour Slider Tactile CYAT61658")
    print("=" * 70)
    print()
    
    # Créer le répertoire de sortie
    output_dir = "generated_footprints"
    os.makedirs(output_dir, exist_ok=True)
    print(f"Répertoire de sortie: {output_dir}/")
    print()
    
    # Générer les footprints TX
    print("Génération des électrodes TX...")
    tx_content = generate_tx_electrodes()
    tx_file = os.path.join(output_dir, "Slider_TX_Electrodes.kicad_mod")
    with open(tx_file, 'w') as f:
        f.write(tx_content)
    print(f"  ✓ {tx_file}")
    
    # Générer les footprints RX
    print("Génération des électrodes RX...")
    rx_content = generate_rx_electrodes()
    rx_file = os.path.join(output_dir, "Slider_RX_Electrodes.kicad_mod")
    with open(rx_file, 'w') as f:
        f.write(rx_content)
    print(f"  ✓ {rx_file}")
    
    # Générer le plan GND shield
    print("Génération du plan GND shield...")
    gnd_content = generate_gnd_shield()
    gnd_file = os.path.join(output_dir, "Slider_GND_Shield.kicad_mod")
    with open(gnd_file, 'w') as f:
        f.write(gnd_content)
    print(f"  ✓ {gnd_file}")
    
    # Générer la documentation
    print("Génération de la documentation...")
    doc_content = generate_documentation()
    doc_file = os.path.join(output_dir, "Slider_Specifications.md")
    with open(doc_file, 'w') as f:
        f.write(doc_content)
    print(f"  ✓ {doc_file}")
    
    print()
    print("=" * 70)
    print("Génération terminée avec succès!")
    print("=" * 70)
    print()
    print("Résumé:")
    print(f"  - {TX_COUNT} électrodes TX ({TX_WIDTH}mm × {TX_LENGTH}mm)")
    print(f"  - {RX_COUNT} électrodes RX ({RX_WIDTH}mm × {RX_HEIGHT}mm, pitch {RX_PITCH}mm)")
    print(f"  - Plan GND shield avec via stitching")
    print(f"  - Documentation complète")
    print()
    print("Prochaines étapes:")
    print("  1. Vérifier les fichiers générés dans", output_dir + "/")
    print("  2. Importer les footprints dans KiCad")
    print("  3. Placer sur le PCB et vérifier l'alignement")
    print()

if __name__ == "__main__":
    main()
