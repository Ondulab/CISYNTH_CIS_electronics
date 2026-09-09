# U18 : symbole compact — 9 septembre 2026

Demande utilisateur : remplacer la représentation excessivement haute de U18 par une version compacte inspirée de la bibliothèque KiCad, et appliquer la modification.

Le symbole local `Schematic_Style:SN74LVC244APW` reprend désormais exactement les coordonnées des vingt broches, leurs longueurs et le rectangle du symbole installé `74xx:74HC244` de KiCad 10.0.1. Ce dernier sert uniquement de gabarit graphique : le composant reste le **SN74LVC244APW**, avec son empreinte TSSOP-20, sa datasheet TI, ses noms et types électriques de broches et ses commandes actives à zéro conservés. Ce n'est pas une substitution de technologie LVC par HC. La bibliothèque locale et le symbole incorporé au schéma ont été mis à jour ensemble.

Le corps passe de **20,32 × 119,38 mm** à **15,24 × 30,48 mm**, soit **74,5 % de hauteur en moins** pour le corps. Les unités sont celles du dessin schématique, sans rapport avec les dimensions du boîtier PCB. L'ordre vertical de la seconde banque suit maintenant le gabarit KiCad (17/15/13/11 à gauche, 3/5/7/9 à droite) ; les nets suivent les numéros de broches, sans permutation électrique.

Les sept résistances série restent directement sur les sorties. Les deux capacités restent au-dessus du circuit. Les treize résistances de tirage sont regroupées immédiatement en dessous, côté RAW à gauche et côté buffer à droite, reliées par des labels locaux explicites. R108 reste une résistance de tirage vers +3,3 V, représentée avec l'alimentation au-dessus. Aucun composant physique n'a été ajouté ou supprimé.

Validation :

- Les **389 réseaux et leurs ensembles exacts de 1 460 terminaux** sont identiques avant/après, noms inclus.
- Les **392 composants physiques**, références, UUID, valeurs, empreintes, attributs et types/noms de broches sont conservés ; les **43 terminaux non connectés** restent identiques.
- Aucun objet extérieur à la cellule U18 n'a été déplacé ; aucun autre symbole de bibliothèque n'a été modifié.
- Les broches du symbole local ont exactement la géométrie du gabarit KiCad et la bibliothèque locale correspond au cache du schéma.
- Exports XML, PDF et ERC réussis avec KiCad CLI 10.0.1 ; inspection visuelle de l'extrait final. Pas de test d'ouverture/enregistrement dans l'éditeur interactif.
- Aucune nouvelle erreur ni nouvelle catégorie de défaut ERC : **60 erreurs préexistantes conservées** ; avertissements de points hors grille 1 071 → 1 067, autres avertissements inchangés. Le résultat n'est pas un schéma exempt d'erreurs ERC.
- Une seule feuille A0, aucun label global/hiérarchique ajouté. PCB, fichier de projet et firmware inchangés.

Les sauvegardes avant intervention, exports, scripts et `verification.json` sont dans le dossier de workspace `Compactage_U18_2026-09-09`. `U18-comparatif.pdf` montre l'avant et l'après à la même échelle ; `U18-apres.pdf` est l'extrait compact.
