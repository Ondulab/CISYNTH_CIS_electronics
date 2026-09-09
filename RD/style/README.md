# Pièces de l'étude de style du 8 septembre 2026

Le document à valider est [SCHEMATIC_STYLE_GUIDE.md](../../SCHEMATIC_STYLE_GUIDE.md). Aucun schéma de production n'est modifié par cette étude.

- `corpus.json` : chemins des trois références et SHA-256. Les copies sous `/private/tmp` ont uniquement servi à isoler les exports de KiCad ; les sources durables sont celles du champ `source`.
- `V3.pdf`, `V4_AUTO.pdf`, `V4_REF.pdf` : exports des trois références, sur la page A2 existante. Les éléments déjà hors page ne figurent pas dans ces PDF ; ils restent présents dans les mesures de coordonnées et les netlists.
- `Atlas-style-reference.pdf` : neuf extraits vectoriels, sans déplacement de symbole ; source et fenêtre en mm indiquées en haut de chaque page. Ordre : V3 alimentations, CIS, MEMS ; V4_AUTO alimentations, ADC, Ethernet, MEMS, haut MCU, RAM.
- `*.png` : rendus des pages/extraits examinés.
- `V3.xml`, `V4_AUTO.xml`, `V4_REF.xml` : netlists exportées par KiCad. Elles documentent la topologie existante ; elles ne constituent pas une validation électrique de ces références historiques.
- `*-mesures.json` : symboles, broches, nets, champs visibles, fils, labels, cadres/textes, junctions, groupes représentatifs et croisements géométriques.
- `*-symboles.csv` : index lisible des composants, positions, unités et nets.
- `synthese-mesures.json` : compteurs descriptifs. L'unité des longueurs suffixées `_g` est **0,635 mm**. Les fréquences entre versions ne sont pas des observations indépendantes.
- `integrite-avant.json`, `verification-etude.json` : empreintes de 46 fichiers de référence/production et contrôle final : aucune variation pendant l'étude. Les modifications déjà présentes au début de la tâche ne sont pas annulées.

## Reproduction des mesures

`analyser_style.py` nécessite Python 3 et `sexpdata`. Exécuter depuis n'importe quel répertoire :

```sh
python3 /chemin/du/projet/RD/style/analyser_style.py
```

Le script retrouve la racine du workspace par son emplacement, vérifie que les sources correspondent au manifest, lit les netlists existantes et réécrit uniquement les JSON/CSV d'étude. Si une source a changé, il s'arrête pour éviter de mélanger une nouvelle géométrie avec une ancienne netlist.

Les exports initiaux ont utilisé `kicad-cli` 10.0.1, une commande à la fois par copie temporaire :

```sh
kicad-cli sch export netlist --format kicadxml -o /chemin/sortie/V3.xml /copie/temporaire/V3/CIS.kicad_sch
kicad-cli sch export pdf -o /chemin/sortie/V3.pdf /copie/temporaire/V3/CIS.kicad_sch
```

Même procédure pour V4_AUTO et V4_REF. Les symboles incorporés aux schémas permettent ces exports. Les extraits ont été produits avec PyMuPDF, en convertissant les coordonnées de fenêtre mm en points PDF par `72/25.4`, sans transformation des schémas sources.

## Limites de l'analyse automatisée

Le rôle électrique et l'attribution d'auteur ont été examinés séparément des statistiques. Le script n'infère pas une norme de dessin d'après une moyenne. Il n'est ni un moteur de placement, ni un audit ERC, ni un vérificateur complet de connectivité avant/après modification. Les croisements comptés sont les intersections strictement intérieures de segments H/V, hors jonctions en T et diagonales.

Les références n'ont aucun composant multi-unité. Une future réorganisation multi-unité nécessitera les contrôles supplémentaires prescrits dans le guide, sans supposer cette analyse suffisante. Aucun ERC n'a été lancé pendant cette étude documentaire ; aucun déplacement n'a été appliqué. Les exports CLI prouvent le chargement et le tracé des références, pas une nouvelle validation électrique ni une session d'édition GUI.
