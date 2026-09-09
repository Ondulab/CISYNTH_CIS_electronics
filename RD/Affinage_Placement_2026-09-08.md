# Affinage du placement et des labels — 8 septembre 2026

La demande consiste à améliorer les règles graphiques à partir du bloc DISPLAY fourni, puis à les appliquer au schéma courant **5.0.0-dev**. Le travail part de la version V5 déjà présente dans le workspace et conserve ses modifications électriques.

La [charte du projet](../SCHEMATIC_STYLE_GUIDE.md) est complétée par la section 11 : largeur des départs selon le texte, colonnes communes, marge de 2,54 mm avant une broche ou une branche, déplacement rigide des cellules, références des résistances hors des fils et traitement particulier des rangées serrées. Les dimensions sont des règles graphiques du projet ; aucune longueur de piste PCB ni contrainte de timing n’est déduite du dessin.

## Application

- U7 : capacités d’entrée rapprochées ; rail de sortie compacté avec ses capacités, son pull-up PG et sa résistance de décharge. Le retour SENSE reste filaire et visible.
- U18 : séries et résistances de rappel rapprochées des faces du buffer ; colonnes de labels homogènes dimensionnées suivant le texte le plus large. L’espacement vertical réserve la place nécessaire aux masses et aux tirages.
- U19/U21 : rappels OE rapprochés et départs de labels après les jonctions, sans texte placé sur la référence des résistances.
- Résistances série des options et des boucles concernées : références au-dessus du corps ; exception décalée pour R115…R119, dont les lignes sont serrées, et R139 près d’une masse.
- OLED de la capture : C35/C133/C134 et C31/C135 espacées de **7,62 mm entre axes** ; référence, capacité et tension lisibles séparément. Les départs DSI et leurs marqueurs graphiques conservent leur disposition.

**59 composants physiques** ont un placement ou des champs repositionnés. Les symboles de masse/alimentation suivent les déplacements concernés. L’outil normalise 53 départs de labels ; le label PG local de U7 est également repositionné sur sa liaison existante. Les cadres et la feuille A0 unique sont conservés.

Les connexions internes partagées ne sont pas remplacées par des labels. Les petites différences de longueur entre fils ne constituent pas un appairage électrique.

## Vérifications

| Contrôle | Résultat |
|---|---|
| Composants physiques | 392, inventaire identique |
| Nets et noms explicites/automatiques | 389, strictement identiques |
| Terminaux de la netlist | 1 460, partitions identiques : aucune fusion ou séparation |
| Broches marquées non connectées | 43, ensemble identique |
| Valeurs, propriétés, UUID, empreintes, unités, DNP et définitions de symboles | Identiques |
| Chargement natif | Exports KiCad CLI 10.0.1 XML, PDF et ERC réussis |
| Contrôles d’intégrité graphique/électrique | 1 746 assertions réussies |
| Vérifications existantes | 270 contrôles alimentation et 53 contrôles acquisition réussis |
| ERC au même réglage de projet | Mêmes 60 erreurs ; aucun nouveau défaut de niveau erreur. Les avertissements hors grille passent de 1 077 à 1 071 |
| PCB, firmware et bibliothèques de symboles | Non modifiés |

Le projet n’est pas déclaré ERC propre. Les alertes préexistantes sont conservées et les nombres du tableau se rapportent aux exports du présent snapshot. L’ERC et les netlistes vérifient la connectivité ; les extraits PDF ont également été examinés visuellement. Aucun cycle d’ouverture/sauvegarde dans l’éditeur interactif n’est revendiqué.

## Livraison

Le dossier `Affinage_Placement_2026-09-08/` à la racine du workspace contient `Comparatif-placement.pdf`, `apres.pdf`, les netlistes et ERC avant/après, les résultats JSON, les sauvegardes et les scripts du snapshot. La source de production est comparée à son empreinte initiale avant installation pour éviter d’écraser une modification concurrente.

Si KiCad affiche encore l’ancienne vue, recharger le fichier depuis le disque sans enregistrer cette ancienne vue par-dessus le résultat.
