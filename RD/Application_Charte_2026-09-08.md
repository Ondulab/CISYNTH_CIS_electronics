# Application de la charte — 8 septembre 2026

La réorganisation demandée est appliquée aux blocs acquisition, horloges, options de mesure, alimentation d’entrée, buck-boost, OLED et éclairage des captures, ainsi qu’à leur cellule MAIN POWER. **181 composants physiques sur 392** sont réorganisés. Les autres instances physiques sont conservées à l’identique, y compris la position de leurs broches. Le PCB n’est pas modifié.

## Présentation

- Passifs rattachés à leur actif ; découplage à l’entrée, sorties à droite, contre-réaction et compensation localisées.
- Résistances rectangulaires avec valeur dans le corps ; champs des condensateurs séparant référence, capacité et tension.
- Fils orthogonaux, labels ancrés, cadres fonctionnels pointillés et cellules compactées. Les trois voies LED emploient le même gabarit.
- Grille de connexion du projet passée de 50 à **25 mil (0,635 mm)**, conformément au guide. Aucun diagnostic ERC n’a été désactivé. Tous les terminaux réorganisés sont sur cette grille.

## Bibliothèques

Les symboles officiels de la bibliothèque KiCad installée sont utilisés directement pour **U2 TPS62933F, U22 TPS7A91, Q4 AO3401A, Q1–Q3 DMN2056U, U19 SN74LVC1G14DBV et U20 SN65LVDS1DBV** : huit instances, six types. Les passifs, connecteurs et points de mesure conservent également leurs bibliothèques KiCad usuelles.

La bibliothèque projet **Schematic_Style.kicad_sym**, déclarée dans `sym-lib-table`, fournit neuf représentations adaptées : TPS552892RYQR, TPS259470ARPWR, ADP7104ARDZ-3.3, DS1100LZ-20, SN74LVC1G132DBV, REF3312AIDBZR, SN74LVC244APW, OPA320AIDBVR et TS5A3159DCKR. Les symboles locaux reprennent les numéros et fonctions des broches du schéma de départ et permettent le regroupement des passifs. Le TS5A3159 est dérivé du symbole officiel : ses deux unités graphiques sont réunies dans l’unité 1 déjà utilisée par le projet, sans changement d’affectation physique. L’OPA320 est présenté en triangle avec son alimentation dans la même unité. Les empreintes et références commerciales existantes sont conservées, même lorsque le symbole officiel propose une autre empreinte par défaut.

L’adoption des symboles officiels modifie certains noms et types ERC de broches, notamment les broches superposées du TPS7A91. Ces écarts de métadonnées sont détaillés dans `bibliotheques.json` et `verification.json` du dossier de livraison. Les numéros de broches et les connexions physiques sont identiques.

**Deux noms automatiques changent** à cause des noms de broches de U20 : `Net-(U20-Y/P)` devient `Net-(U20-Y)` et `Net-(U20-Z/N)` devient `Net-(U20-Z)`. Les ensembles de terminaux de ces nets ne changent pas. Tous les noms de nets explicites sont conservés ; le rail local `/+3.3VACQ` reste local.

## Vérification

| Contrôle | Résultat |
|---|---|
| Nets et terminaux avant/après | 389 nets, 1 460 terminaux ; partitions strictement identiques |
| Connexions créées/supprimées | Aucune ; aucun net fusionné ou scindé |
| Composants, propriétés, valeurs, empreintes, UUID, unités, DNP | Conservés pour les 392 composants physiques |
| Broches marquées non connectées | Même ensemble de 43 terminaux, y compris les broches cachées |
| Labels et jonctions | Labels nouveaux ancrés ; segments découpés aux contacts ; jonctions aux embranchements ; connectivité contrôlée par netlist |
| Contrôles de conservation | 3 272 assertions réussies |
| Vérifications alimentation/acquisition existantes | 270 + 53 contrôles réussis |
| Chargement par KiCad 10.0.1 | Exports XML et PDF, et ERC réussis |
| ERC à grille identique de 25 mil | Mêmes 60 erreurs ; avertissements 79 → 69 |
| PCB | SHA-256 identique à la sauvegarde |

Les 60 erreurs ERC préexistantes comprennent 56 broches non connectées, trois conflits entre types de broches et une alimentation non pilotée. L’ensemble sémantique des erreurs est identique. Les avertissements de points hors grille passent de 12 à 2 ; les autres catégories restent à 56 avertissements entre broches, neuf divergences de symbole et deux problèmes de liaison d’empreinte. Cette réorganisation n’est pas une validation matérielle de l’alimentation ou du bruit image.

Le fichier reste un schéma KiCad natif avec symboles en cache et bibliothèque locale éditable. La lecture par le moteur KiCad est vérifiée ; une ouverture interactive et un cycle de sauvegarde dans l’éditeur n’ont pas été exécutés, car une vue du projet était déjà ouverte.

## Livraison et traçabilité

Le dossier `Application_Charte_2026-09-08/` à la racine du workspace contient :

- `Extraits-charte.pdf` : une page par bloc réorganisé ; `apres.pdf` : schéma complet ; `Vue-ensemble.png` : aperçu.
- `avant/` : sauvegarde des fichiers avant intervention ; `sha256-avant.json` : leurs empreintes.
- `avant.xml`, `apres.xml`, rapports ERC avant/après et `verification.json` : preuves de contrôle.
- `bibliotheques.json`, `placement.json`, `cadres.json` : correspondances et géométrie.
- `scripts/` : reconstruction et vérification utilisées pour cette application. Ces scripts visent ce snapshot précis, pas un réorganisateur universel ; le générateur nécessite les bibliothèques KiCad locales, Python et sexpdata.

La source de production a été comparée à ses empreintes initiales avant installation afin d’éviter d’écraser une modification concurrente. Les fichiers de verrouillage et autosauvegardes KiCad restent intacts.

**Dans KiCad déjà ouvert : recharger le schéma depuis le disque sans enregistrer l’ancienne vue**, pour ne pas écraser la nouvelle disposition.
