#!/usr/bin/env python3
"""
Script pour corriger le schéma converti en supprimant la section lib_symbols
KiCad régénérera automatiquement cette section à partir des bibliothèques standard
"""

import re
import sys
from pathlib import Path

def remove_lib_symbols_section(content):
    """
    Supprime la section lib_symbols du schéma
    KiCad la régénérera automatiquement
    """
    # Pattern pour trouver la section lib_symbols complète
    # Elle commence par (lib_symbols et se termine par le ) correspondant
    
    # Trouver le début de lib_symbols
    start_pattern = r'\(lib_symbols\s*\n'
    start_match = re.search(start_pattern, content)
    
    if not start_match:
        print("Aucune section lib_symbols trouvée")
        return content
    
    start_pos = start_match.start()
    
    # Compter les parenthèses pour trouver la fin de la section
    depth = 0
    in_lib_symbols = False
    end_pos = start_pos
    
    for i in range(start_pos, len(content)):
        char = content[i]
        if char == '(':
            depth += 1
            in_lib_symbols = True
        elif char == ')':
            depth -= 1
            if in_lib_symbols and depth == 0:
                end_pos = i + 1
                break
    
    # Supprimer la section lib_symbols
    before = content[:start_pos]
    after = content[end_pos:]
    
    # Ajouter une section lib_symbols vide
    # KiCad la remplira automatiquement
    new_content = before + "\t(lib_symbols\n\t)\n" + after
    
    return new_content

def process_schema(input_file, output_file):
    """Traite le fichier schéma"""
    
    print(f"Lecture du schéma: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Suppression de la section lib_symbols...")
    new_content = remove_lib_symbols_section(content)
    
    print(f"Écriture du schéma corrigé: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("\n✓ Correction terminée!")
    print(f"\nLe schéma corrigé a été créé: {output_file}")
    print("\nKiCad régénérera automatiquement la section lib_symbols")
    print("à partir des bibliothèques standard lors de l'ouverture.")

def main():
    input_file = Path("CIS_kicad_standard.kicad_sch")
    output_file = Path("CIS_kicad_standard_fixed.kicad_sch")
    
    if not input_file.exists():
        print(f"Erreur: Le fichier {input_file} n'existe pas!")
        sys.exit(1)
    
    if output_file.exists():
        response = input(f"Le fichier {output_file} existe déjà. Écraser? (o/N): ")
        if response.lower() != 'o':
            print("Correction annulée.")
            sys.exit(0)
    
    process_schema(input_file, output_file)

if __name__ == "__main__":
    main()
