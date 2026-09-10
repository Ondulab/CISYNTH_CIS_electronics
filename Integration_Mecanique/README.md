> **Version du 10 septembre :** [Montage_Photos](Montage_Photos/README.md) contient les positions synchronisées et l’écran avec ses nappes dans la vue 3D KiCad. Le document ci-dessous concerne la première maquette.

# Base de placement mécanique V4

Ouvrir **CIS_Integration_V4.kicad_pro** puis le PCB associé. Carte de 256 × 18 × 1 mm, contour exact de FreeCAD, avec J1 écran, J2 tactile et J4 Ethernet sur F.Cu. Les centres J1/J2 proviennent des deux esquisses utilisateur. J4 ouvre vers X négatif, à l'extrémité où arrivent les nappes. Les trois empreintes sont verrouillées pour conserver le repérage.

Le projet est une étude d'implantation : seuls ces trois connecteurs sont présents. Les nets et les identifiants des symboles proviennent du schéma actuel `../CIS.kicad_sch`. La carte ne comporte aucun routage. L'ancien PCB routé `../CIS.kicad_pcb` reste intact. Les bibliothèques d'empreintes sont référencées relativement au projet ; les trois enveloppes STEP locales apparaissent dans le visualiseur 3D.

`placements.json` donne les coordonnées de chaque plage et son net. `source_netlist.xml` conserve l'instantané de la source. Les cadres des esquisses et les annotations se trouvent sur Dwgs.User. Une zone d'exclusion cuivre/empreintes sur les deux faces protège l'encoche commune.

Points ouverts avant routage/fabrication :

- J2 est l'empreinte **AA07-S022VA1-Mockup** existante, expressément provisoire ; remplacer par le dessin JAE MB-0215.
- J4 conserve l'empreinte V4 : plages de blindage hors contour et absence de plage numérotée SH. Les fixations débordent malgré un corps de connecteur plus étroit. La revue ne corrige pas silencieusement ce contour.
- L'orientation du contact 1 et les dimensions physiques des nappes restent à confirmer sur les pièces.
- Les enveloppes 3D sont simplifiées ; le modèle tactile et les parties mâles ne sont pas des modèles fabricant.
- DRC : 6 alertes restantes liées à J4 (2 isolation perçage, 2 cuivre/bord, 2 sérigraphie/bord), plus 34 éléments non connectés ; consulter `drc.json`. L'isolation nominale cuivre est provisoirement réglée à 0,15 mm pour le pas 0,35 mm de J1, isolation au bord 0,20 mm. Aucun procédé de fabrication n'est validé.

Détails mécaniques, hypothèses et contrôles : [rapport FreeCAD](../../../Meca/Sp3ctra_CIS_mechanics_v4/Integration_V4/README.md).

Régénérer avec le Python inclus dans KiCad :

```sh
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 build_board.py
```

Le script relit le contour JSON du dépôt mécanique et réexporte la netlist du schéma courant. Il recrée la carte d'étude ; il ne faut pas le relancer sur un routage ajouté manuellement sans sauvegarde préalable.
