# Implantation nominale — photos écran du 10 septembre 2026

Ouvrir [CIS_Montage_Photos.kicad_pro](CIS_Montage_Photos.kicad_pro). Le PCB comporte J1 Display, J2 Touch et J4 Ethernet, avec leurs réseaux issus du schéma V4. Les trois positions sont verrouillées. `MECH1` est une référence mécanique hors nomenclature et hors fichier de placement : elle affiche l'écran et les nappes pliées dans la vue 3D KiCad.

[Assemblage et hypothèses mécaniques](../../../../Meca/Sp3ctra_CIS_mechanics_v4/Integration_V4/Photos_2026-09-10/README.md) · [Implantation SVG](implantation.svg) · [STEP complet issu de KiCad](CIS_Montage_Photos.step) · [Contrôles](verification.json).

## Positions sur F.Cu

| Référence | X KiCad (mm) | Y KiCad (mm) | Rotation |
|---|---:|---:|---:|
| J1 Display | 91,293363 | 56,680000 | 0° |
| J2 Touch | 75,150637 | 58,524500 | 270° |
| J4 Ethernet | 58,826500 | 59,000000 | 270° |

Ces valeurs sont nominales : les scans ne permettent pas une précision au micromètre. Les pads et leurs réseaux sont conservés. La copie locale `DISP.pretty` déplace uniquement le repère sérigraphié de broche 1 de J1 vers l'intérieur du PCB. La numérotation électrique et les pads restent ceux de la bibliothèque V4.

Le contour de cette variante suppose un **PCB relevé de 1,6 mm dans l'assemblage**, une encoche de 3 mm recentrée à X local 35 mm et approfondie jusqu'à Y local 7,8 mm, ainsi qu'une fenêtre sous le connecteur CIS. Le STEP reprend ce contour et les deux trous de positionnement RJ45. La hauteur d'assemblage est décrite dans le dossier mécanique ; elle ne modifie pas l'épaisseur KiCad du PCB, qui reste de 1 mm.

## État de validation

- Concordance FreeCAD/KiCad des positions, rotations, faces, réseaux, contour et modèles 3D vérifiée après enregistrement et export.
- 76 affectations de pads vérifiées contre la netlist.
- **0 violation de placement J1/J2** dans le DRC de cette variante.
- **6 violations restantes, toutes sur J4** : 2 erreurs de distance cuivre/bord, 2 erreurs de distance aux trous, 2 avertissements de sérigraphie. Elles proviennent de l'empreinte Ethernet V4 héritée. Elles ne sont ni masquées ni acquittées dans le projet.
- Carte non routée, **34 éléments non connectés**.
- **J2 reste le mockup AA07-S022VA1** de la bibliothèque V4 : son empreinte et son accouplement ne peuvent pas être déclarés exacts sans le plan JAE MB-0215 ou un relevé fiable. Les petites enveloppes STEP des embases restent provisoires.
- Le rayon neutre des plis de 0,2 mm, le recalage transversal Display de −0,25 mm et les faibles jeux mécaniques exigent une validation sur l'écran réel. La variante est destinée à la revue de montage, pas à la fabrication.

Le projet principal `CIS.kicad_pcb` n'est pas remplacé par cette carte partiellement implantée. Le projet d'intégration du 9 septembre et la précédente proposition issue des scans sont conservés pour comparaison.

## Régénération

Depuis la racine du dépôt électronique, après les trois scripts mécaniques indiqués dans le README lié :

```sh
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 Integration_Mecanique/build_board.py --geometry ../../Meca/Sp3ctra_CIS_mechanics_v4/Integration_V4/Photos_2026-09-10/geometry.json --output Integration_Mecanique/Montage_Photos --name CIS_Montage_Photos
/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli pcb drc --format json -o Integration_Mecanique/Montage_Photos/drc.json Integration_Mecanique/Montage_Photos/CIS_Montage_Photos.kicad_pcb
/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli pcb export step --board-only --user-origin 50x68mm --force -o /tmp/photos_board.step Integration_Mecanique/Montage_Photos/CIS_Montage_Photos.kicad_pcb
/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli pcb export step --user-origin 50x68mm --force -o Integration_Mecanique/Montage_Photos/CIS_Montage_Photos.step Integration_Mecanique/Montage_Photos/CIS_Montage_Photos.kicad_pcb
/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli pcb export svg --layers F.Cu,F.Silkscreen,Edge.Cuts,Dwgs.User --mode-single --exclude-drawing-sheet --page-size-mode 2 -o Integration_Mecanique/Montage_Photos/implantation.svg Integration_Mecanique/Montage_Photos/CIS_Montage_Photos.kicad_pcb
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 Integration_Mecanique/verify_photos.py
```

Exécuter les commandes KiCad successivement. La génération recharge les connecteurs depuis la netlist du schéma présent ; une modification de ce schéma peut donc changer les résultats. Le contrôle géométrique final s'exécute ensuite avec le Python FreeCAD et `Integration_V4/verify_photos.py` dans le dépôt mécanique.
