# Grammaire de présentation des schémas Sp3ctra

**Statut : application autorisée aux blocs désignés par l’utilisateur — 8 septembre 2026.**

Ce document décrit le style observé dans les références CIS disponibles. Le 8 septembre 2026, l’utilisateur a demandé explicitement d’appliquer sa charte aux parties acquisition et alimentation précédemment modifiées, montrées dans ses captures. Cette demande autorise leur réorganisation selon ce guide et l’emploi de symboles KiCad ou de dérivés locaux compatibles. Les cas insuffisamment documentés restent ouverts ; cette application ne transforme pas les hypothèses contextuelles en règles universelles. Aucune modification de schéma de production n’avait été effectuée pendant la phase d’étude.

## 1. Portée et qualité des preuves

### Corpus effectivement utilisé

Les identifiants ci-dessous désignent des **versions d'une même famille de conception**, pas trois projets indépendants. La répétition d'un même bloc entre deux sauvegardes ne vaut pas deux preuves indépendantes. L'attribution personnelle de chaque détail reste à confirmer par l'utilisateur ; l'auteur d'un commit ne prouve pas l'auteur de chaque choix graphique.

| ID | Source relative à la racine du workspace | Contenu et statut |
|---|---|---|
| V3 | `Sp3ctra_CIS_Hardware/CIS/Electronique/Sp3ctra_CIS_electronics_v3/CIS.kicad_sch` | Cartouche CIS, rév. **2.2.0**, 2023-05-04 ; dossier nommé v3. 176 composants hors symboles d'alimentation. Historique Git avec Zhonx comme auteur. Référence ancienne candidate. |
| V4_AUTO | `Sp3ctra_CIS_Hardware/CIS/Electronique/Sp3ctra_CIS_electronics_v4/_autosave-CIS.kicad_sch` | Cartouche 4.0.0, 2026-02-11 ; fichier daté du 2 avril 2026 sur disque. 236 composants. Référence de géométrie récente antérieure aux interventions de cette session ; une sauvegarde de travail n'est pas un schéma validé électriquement. |
| V4_REF | `Corrections_Schema_2026-09-08/avant/CIS.kicad_sch` | Cartouche 4.0.0, 267 composants. Identique octet par octet à `.history/CIS.kicad_sch` du projet v4. Snapshot antérieur aux corrections acquisition/alimentation de cette session, mais comportant déjà une revue récente. Sert à confirmer la persistance des motifs, pas à attribuer automatiquement les ajouts récents à l'utilisateur. |
| CAPTURE | Captures fournies par l'utilisateur | Preuve explicite de la disposition souhaitée : passifs associés à leur actif, connexions visibles dans le bloc, cadres fonctionnels. Les distances ne sont pas mesurées en pixels pour en déduire une grille. |

V4_AUTO et V4_REF partagent 502 UUID d'instances ; 460 ont conservé à la fois position, rotation et identifiant de symbole. V3 et V4_REF ne partagent que 25 UUID d'instances, aucun avec position et identifiant de symbole simultanément inchangés. La géométrie a donc réellement évolué entre V3 et V4, tout en restant dans la même famille de produit.

**Exclusions :**

- Le fichier `USB-ETH/USB-ETH/USB-ETH.kicad_sch` et les 14 schémas mécaniques LA…LG des v3/v4 sont vides : aucune preuve de style.
- `USB-GIGABIT_Rev_C.kicad_sch` porte le cartouche **Olimex Ltd** : référence tierce, exclue des inférences personnelles.
- Les feuilles `ES_Daisy_Patch_Rev4_*` du dossier ADAC contiennent des bibliothèques `ADAC-eagle-import` : origine importée, attribution personnelle non établie. Ne pas les utiliser pour inventer des règles d'AOP/DAC.
- Les dossiers ReverseAppleTouchBar et leurs doublons ne sont pas attribués à l'utilisateur ; exclus en attente d'identification des parties personnelles.
- Le schéma CubeMX est un export STM32, insuffisant pour attribuer ses placements au style personnel.
- Le `CIS.kicad_sch` de production actuel et les propositions/réorganisations générées par l'assistant ne sont **pas** des références d'apprentissage. Ne pas prendre les nouveaux grands blocs V5 comme précédents graphiques.

### Méthode et traçabilité

Lecture des S-expressions avec `sexpdata`, lecture des symboles incorporés, positions/orientations/propriétés, fils, junctions, textes, cadres et labels ; export XML de la connectivité et PDF par **KiCad CLI 10.0.1**, depuis des copies temporaires. Inspection visuelle des pages et de neuf extraits fonctionnels. Les exports ne réécrivent pas les originaux.

Les mesures brutes, coordonnées des broches et nets exportés sont dans [RD/style](RD/style). Voir [synthèse](RD/style/synthese-mesures.json), [manifest avec SHA-256](RD/style/corpus.json), [script de mesure](RD/style/analyser_style.py), et [atlas visuel de référence](RD/style/Atlas-style-reference.pdf). Les CSV `*-symboles.csv` permettent de retrouver un composant ; les JSON `*-mesures.json` contiennent aussi les champs visibles et leurs décalages.

Les couleurs des exports dépendent du thème KiCad utilisé. Le thème clair des PDF d'étude n'est pas une proposition de remplacement du thème sombre des captures ; aucune règle personnelle de couleur n'est déduite de cette différence.

**Confiance** signifie confiance dans une inférence applicable au corpus : élevée = plusieurs motifs concordants ou instruction explicite ; moyenne = contexte limité/variantes ; faible = exemple isolé. Aucune confiance élevée dans ce corpus ne prouve l'universalité du style sur d'autres projets.

**Fréquence** : systématique = sans contre-exemple dans le périmètre indiqué ; fréquente = dominante avec variantes ; contextuelle = déclenchée par un rôle électrique ; exceptionnelle = cas isolé/écart. Les prescriptions nouvelles proposées pour résoudre un écart sont signalées comme telles.

## 2. Invariants imposés par l'utilisateur

Ces règles sont normatives, issues de la demande, et non déduites d'une fréquence.

1. Priorité : **intégrité électrique → style personnel → compréhension fonctionnelle → lisibilité → compacité**.
2. Regrouper les passifs autour de l'actif dont ils dépendent. Déterminer cette dépendance par la connectivité et la fonction, pas seulement par la distance actuelle ou le numéro de référence.
3. Avant toute application, faire valider ce guide et les ambiguïtés. La création du guide n'autorise pas une modification de production.
4. Une réorganisation graphique conserve composants, références, valeurs, unités, broches, nets et topologie. Toute proposition électrique est présentée séparément avant exécution.
5. Une convention personnelle problématique doit être signalée avec une alternative ; ne pas la remplacer silencieusement par une préférence générique.

Confiance **élevée**, application **systématique**, source : instruction utilisateur actuelle et captures.

## 3. Unités et mesures utilisables

On note **g = 0,635 mm = 25 mil**. Le pas de 1,27 mm vaut **2g**. Il s'agit du plus gros pas commun constaté sur presque toutes les coordonnées de placement et de fils ; le réglage de grille de l'interface KiCad n'a pas été observé directement.

Les coordonnées KiCad ont x vers la droite, y vers le bas. Pour un CI, l'ancre d'instance peut être très décentrée par rapport au corps : aligner les corps ou les broches utiles, pas aveuglément les ancres. Les distances entre petits passifs citées ci-dessous sont entre ancres/axes ; elles ne représentent pas un espace libre entre textes.

| Mesure | V3 | V4_AUTO | V4_REF |
|---|---:|---:|---:|
| Coordonnées x/y d'ancres sur g, symboles d'alimentation inclus | 720/720 | 1031/1032 | 1163/1164 |
| Coordonnées x/y des extrémités de fils sur g | 1152/1152 | 2575/2576 | 2715/2716 |
| Segments horizontaux / verticaux / diagonaux | 209 / 74 / 5 | 537 / 107 / 0 | 560 / 119 / 0 |
| Longueur médiane d'un **segment**, pas d'une liaison entière | 10g | 12g | 12g |
| Quartiles 25–75 % des segments | 4–20g | 10–28g | 8–27g |
| Labels locaux / globaux / hiérarchiques | 146 / 0 / 0 | 267 / 0 / 0 | 270 / 0 / 0 |
| Références R avec valeur à l'ancre du corps | 40/50 | 69/69 | 73/87 |
| Condensateurs avec référence au-dessus de l'ancre | 75/86 | 127/130 | 139/142 |

Les grandes longueurs incluent les lignes de bus et les sorties étiquetées du MCU. Ne pas transformer une médiane en longueur universelle de fil. L'unique coordonnée hors g des V4 est l'abscisse **288,296 mm** du symbole `#PWR0162`, avec une extrémité de fil correspondante ; ce n'est pas une preuve d'emploi volontaire d'une grille fine.

### Gabarits dimensionnels proposés à la validation

| Usage | Valeur observée / point de départ | Preuves et limites |
|---|---|---|
| Rangée de capacités compactes | **10 à 11g** entre axes | V4 C1/C3/C7 : 10g ; C44/C47 et C60/C63 : 11g ; rangées MCU : 11g. V3 C5/C31 : 14g. Élargir si les champs l'exigent. |
| Capacités de sortie du bloc MAIN POWER | **21g** entre axes | V4 C25/C29/C37 et C26/C30/C38 : même pas de 13,335 mm. Gabarit propre à ces deux étages, pas aux découplages en général. |
| Colonne de deux résistances de feedback | **12g** entre centres | V3 R7/R8 et R9/R6 ; V4_AUTO R17/R18. Les broches se rencontrent au nœud médian dans ces symboles. |
| Rangée de pull-up Ethernet | **8g** entre axes | V4 R10/R13/R14/R15/R16 : x=48,895…69,215 mm. |
| Trois voies analogiques au connecteur CIS | **5g** entre lignes | V4 R33/R34/R35 : y=24,765 / 27,940 / 31,115 mm. Ne pas appliquer ce pas aux broches d'un autre symbole. |
| Trois commandes LED identiques | **22g** entre cellules | V4 Q1/Q2/Q3 : x=252,730 / 266,700 / 280,670 mm ; même y=106,680 mm. |
| Découplages MCU en deux rangées | **26g** entre axes des rangées principales | V4 y=28,575 et 45,085 mm. Organisation en rangées, pas un condensateur déplacé au hasard sur chaque broche. |
| Fil court courant | **4g = 2,54 mm** | 85 segments V3, 75 V4_AUTO, 81 V4_REF. Point de départ pour une extension ; les symboles d'alimentation peuvent aussi toucher directement une broche. |
| Séparation de cadres voisins | **4 à 6g en V4 ; 8g fréquent en V3** | V4 125,095→128,270 : 5g ; RAM/ETH 250,825→254 : 5g ; FLASH/PROG 414,020→416,560 : 4g. V3 157,480→162,560 : 8g. Pas de marge uniforme commune à toutes les versions. |
| Typographie V4 courante | **1,0 mm** ; titres **1,524 mm** | 610 champs visibles V4_AUTO, 673 V4_REF à 1 mm. Titres fonctionnels à 1,524 mm. Les tailles de texte ne sont pas à forcer sur g. |

Ces nombres servent à construire le bon **motif**, puis à contrôler ses collisions. Ils n'autorisent ni à déplacer un point électrique sur une broche voisine, ni à écraser les annotations pour respecter un pas.

## 4. Règles fortes proposées

### F1 — L'actif et son réseau local forment une cellule fonctionnelle

**Règle.** Identifier d'abord le CI/transistor, ses alimentations, son réseau de réglage et ses entrées/sorties. Placer les passifs associés autour des faces portant les broches concernées, avec des fils explicites à l'intérieur de cette cellule. Les composants d'une même fonction se déplacent avec leurs fils, junctions et annotations ; ne pas créer un bloc de passifs déporté sans rattachement visuel.

**Observations.** V3 : cinq étages POWER autour de U1/U3/U9/U4/U5 ; MEMS U8/U10 et PHY U14. V4 : U1/U2, U7/U8, U11/U12, U5 ; capture de l'alimentation expressément choisie par l'utilisateur. Les banques de découplage MCU sont un cas de regroupement collectif, traité en C4.

**Confiance élevée ; fréquente dans les sources, obligatoire par instruction utilisateur.**

### F2 — L'orientation d'un passif exprime son rôle, pas sa catégorie seule

**Règle.** Une résistance insérée dans un chemin horizontal suit ce chemin ; un pull-up/pull-down ou un diviseur est normalement vertical. Une capacité en dérivation est normalement verticale, plaques horizontales, et descend vers la masse. Conserver une autre orientation lorsque la topologie locale le justifie.

**Observations.** V4 R4…R9/R33…R35 horizontales en série ; R10/R13…R16 verticales vers le rail ; R17/R18 verticales en feedback ; C1/C3/C7 et C46/C51/C53 en dérivation. V3 montre les mêmes familles de motifs. Contre-exemple instructif : R37/R40/R43 sont des résistances **série de grille**, mais verticales car la commande arrive d'en haut dans les cellules LED.

**Confiance élevée ; contextuelle.** Ne pas imposer l'angle 0° : les symboles C à 0° et 180° produisent ici le même axe graphique, avec des numéros de broche inversés.

### F3 — Le schéma est une mosaïque de fonctions nommées

**Règle.** Délimiter les fonctions principales par un cadre fin en tirets, sans remplissage. Placer le titre court en capitales en haut à gauche, normalement justifié gauche/bas sur la limite supérieure. Aligner les limites des blocs voisins lorsque leurs dimensions le permettent. Une fonction peut contenir plusieurs cellules sans sous-cadre pour chacune.

**Observations.** V3 POWER, CIS CONNECTOR, ETHERNET, QSPI FLASH, MEMS ; V4 CIS ADC, MAIN POWER, DISPLAY, ETHERNET, RAM, MCU. La zone DISPLAY V4 est en L autour de MAIN POWER : tous les blocs ne sont donc pas des rectangles isolés. V3 emploie des segments de polyligne ; V4 mêle rectangles et polylignes, avec le même aspect.

**Confiance élevée ; fréquente.** La demande actuelle ajoute explicitement que les fonctions hors cadre devront être réintégrées lors de l'application validée.

### F4 — Conserver la grille électrique et les alignements par broche

**Règle.** Utiliser g comme grille de base déduite, avec des pas de 2g lorsque compatibles. Faire partir les fils exactement des extrémités de broches. Aligner les composants répétés par axes ou par broches de même rôle. Ne pas arrondir les coordonnées de champs de texte à la grille électrique.

**Observations.** Tableau de grille ci-dessus ; rangées de capacités, résistances d'Ethernet, cellules LED, étages LDO. La capture illustre des rails horizontaux communs et des retours verticaux.

**Confiance élevée ; quasi systématique pour les points électriques des références.** Toute remise sur grille doit être accompagnée du contrôle des connexions ; ne pas « corriger » seulement un symbole isolé.

### F5 — Utiliser le fil pour raconter une cellule, les labels pour relier les fonctions

**Règle.** Garder visibles par des fils les filtres, le feedback, les commandes locales et les liaisons rapprochées constituant un chemin fonctionnel. Utiliser des labels pour les liaisons éloignées avec le MCU et entre fonctions. Un label identique ne remplace pas automatiquement une liaison locale utile à comprendre.

**Observations.** Feedback filaire V3 U1/U5 et V4 U1/U2 ; PHY→transformateur→RJ45 V4 U5/TR1/J4 entièrement câblé ; signaux CIS_ADC, FMC, SPI et commandes LED par labels entre cellules distantes. Les rails emploient leurs symboles d'alimentation et des segments communs locaux.

**Confiance élevée ; contextuelle.** Les trois références sont sur une feuille ; voir P5 avant toute conclusion sur les labels globaux/hiérarchiques.

### F6 — Répéter une cellule en conservant sa grammaire

**Règle.** Pour des voies identiques, répéter orientation, ordre des composants et alignement des points homologues. Choisir une rangée si chaque cellule est haute et étroite ; empiler des étages si chacun se lit horizontalement. Adapter uniquement les dimensions nécessaires aux champs existants.

**Observations.** V3 trois commandes LED dans CIS CONNECTOR et boutons SW1…SW3 ; V4 Q1/Q2/Q3 en rangée, trois voies R33…R35 empilées, U7/U8 l'un sous l'autre, MAIN POWER U1/U2 alignés en x. Les références ne suivent pas toujours l'ordre spatial : ne jamais les renuméroter pour créer cet ordre.

**Confiance élevée ; fréquente.**

## 5. Préférences proposées

### P1 — Chemins locaux de gauche à droite ; alimentation des cellules de haut en bas

**Règle.** Pour un étage d'alimentation à entrée/sortie latérales, entrée et capacités d'entrée à gauche, actif au milieu, sortie et charge capacitive à droite. Placer le symbole du rail au-dessus et la masse au-dessous lorsque les broches s'y prêtent. Ce n'est pas une direction universelle imposée à la page.

**Preuves.** Cinq étages POWER V3, U1/U2 et U7/U8 V4 ; PHY→TR1→J4. Les masses GND à 0° représentent 95/127 en V3, 125/170 V4_AUTO et 146/191 V4_REF. Les autres orientations sont réelles, pas négligeables.

**Confiance élevée ; fréquente.** Exceptions : connecteur CIS à droite, MCU/mémoire bidirectionnels, masses latérales directement à une broche, pont d'entrée sous RJ45.

### P2 — Écriture des résistances intégrée au corps

**Règle.** Avec les symboles rectangulaires personnels adaptés, centrer la valeur dans le corps et orienter le texte dans le sens du corps. Déporter la référence à côté ; pour une résistance verticale, un décalage latéral de **3 à 4g** est récurrent. Pour une résistance horizontale serrée dans une rangée, placer la référence au-dessus et décalée latéralement pour libérer le chemin.

**Preuves.** Valeur centrée : 40/50 R en V3, 69/69 V4_AUTO, 73/87 V4_REF. V4_AUTO R17 : valeur à l'ancre, référence +4g en x ; R33 : référence +8g en x, −2g en y. Certains ajouts V4_REF ont des champs latéraux standards : ne pas les promouvoir en nouveau style sans confirmation.

**Confiance élevée pour V4_AUTO ; fréquente sur l'ensemble.** Ne pas forcer une valeur longue dans un symbole trop petit ni changer de symbole/broches sans validation. Vérifier le rendu : l'angle brut d'un champ est combiné avec celui de l'instance dans KiCad.

### P3 — Capacités lisibles avec leur tension nominale

**Règle.** Pour les rangées compactes, référence au-dessus des plaques ; capacité en dessous ; tension nominale sur la ligne suivante lorsqu'elle existe. Déporter les textes à gauche ou à droite pour laisser le fil vertical lisible et éviter les voisins. Préserver les informations existantes, y compris les champs personnalisés.

**Preuves.** V4_AUTO C1 : référence y−3g, capacité y+3g, tension y+6g. Ce placement vertical se retrouve sur de nombreuses rangées. Références au-dessus : 127/130 V4_AUTO, 139/142 V4_REF ; V3 75/86, avec aussi des champs latéraux. La tension est présente sur 86/86 C V3, 127/130 V4_AUTO, 131/142 V4_REF.

**Confiance élevée ; fréquente.** Ne pas fabriquer une tension absente : sa détermination est un choix de composant, pas une mise en page. En V3 la valeur utile est souvent `Field5` ou `Field4`, pas `Value` qui peut contenir un identifiant interne.

### P4 — Densité régulière à l'intérieur, respiration entre fonctions

**Règle.** Réutiliser le pas propre à chaque motif plutôt qu'une distance unique pour tous les composants. Densifier les petites rangées identiques ; laisser plus de largeur aux sorties de puissance, textes et symboles complexes. Déplacer ou agrandir le cadre si les annotations débordent.

**Preuves.** Pas de 8g pour les tirages PHY, 10–11g pour les petits C, 21g pour les C de sortie MAIN POWER, 22g pour les cellules LED. V3 laisse davantage d'espace entre étages et cadres que V4. Les grands corps MCU ne doivent pas être pris comme mesure de densité de toute la page.

**Confiance élevée pour ces motifs ; contextuelle.** Aucune marge intérieure minimale unique n'est démontrée. Une marge supplémentaire autour d'un texte est un ajustement de lisibilité à faire contrôler visuellement, pas une règle personnelle quantifiée ici.

### P5 — Labels locaux sur une feuille, sans faisceaux interblocs artificiels

**Règle.** Sur une feuille comparable au CIS, conserver les labels locaux existants et des départs alignés sur les broches. Les labels horizontaux dominent ; utiliser les verticaux dans les cellules alimentées/commandées verticalement. Ne pas convertir leur portée pour obtenir une forme graphique particulière.

**Preuves.** 146, 267 et 270 labels, tous locaux. V4_REF : 262/270 horizontaux ; V4_AUTO : 261/267. Les commandes LED constituent un exemple de labels verticaux. Les symboles d'alimentation ne sont pas comptés comme labels locaux.

**Confiance élevée pour l'observation ; moyenne pour la préférence personnelle, contextuelle aux feuilles uniques.** Il n'y a pas de preuve suffisante pour choisir entre label global et hiérarchique dans un projet multifeuille.

### P6 — Style typographique récent, sans normalisation arbitraire des champs

**Règle.** Sur le CIS v4, prendre 1 mm comme taille courante des champs et labels, 1,524 mm pour les titres. Garder les désignations fonctionnelles courtes en capitales. Ne pas convertir les écritures d'unités, noms de nets ou noms de champs pendant une réorganisation.

**Preuves.** V3 : champs courants 1,27 mm, labels 0,9906 mm ; V4_AUTO : champs visibles 1 mm, 258 labels à 1 mm et 9 à 1,27 mm ; V4_REF : champs visibles et labels à 1 mm. Titres principaux conservés à 1,524 mm.

**Confiance élevée ; contextuelle à la génération du schéma.** Le choix 1 mm pour une future réorganisation de V3 reste à valider ; ne pas effacer sa typographie ancienne automatiquement.

## 6. Grammaire dépendante du contexte électrique

### C1 — Régulateur : rail horizontal et réglages sous la sortie

**Déclencheur.** Convertisseur/LDO avec entrée à gauche et sortie à droite.

**Production graphique.** Rangée d'entrée → broche VIN → actif → élément de puissance éventuel → rail de sortie avec capacités en dérivation. Installer le diviseur dans une colonne à droite du CI, branche haute vers VOUT, branche basse vers GND, point médian relié explicitement à FB. Les condensateurs de bootstrap appartiennent à la boucle BST/SW et non à la rangée de découplage à la masse. Le composant NR/BPASS/SS reste du côté de sa broche, en branche locale.

**Preuves.** V3 U1/R7/R8/C24 et U5/R9/R6 ; V4 U1/R17/R18, C19 entre BST et le réseau SW ; U2/C20 sur NR ; V3 U3/C58 et U9/C59. U7/U8 V4 montrent le retour SENSE directement vers leur sortie. Voir atlas pages 1, 4, 5.

**Confiance élevée ; contextuelle.** Le boost V3 U1 place L1 et D2 au-dessus du CI selon sa topologie : ne pas recopier mécaniquement le dessin d'un buck. Les liens de cet exemple décrivent la disposition historique et ne certifient pas son dimensionnement électrique.

### C2 — Petit CI : découplage rassemblé au-dessus ou en haut à gauche

**Déclencheur.** Petit circuit numérique, MEMS, traducteur de niveaux, régulateur auxiliaire.

**Production graphique.** Rangée compacte de capacités, rail horizontal commun au-dessus des C, retour individuel vers GND ; raccorder cette rangée aux broches d'alimentation du CI. Garder les passifs propres à une autre broche près de celle-ci, même à droite ou sous le CI.

**Preuves.** V3 MEMS U8/C60/C62/C66 ; V4 U11/C75/C77/C79 et U12/C76/C78 ; U6/C10/C11. V4 U11 a aussi son propre condensateur à droite : tout le passif ne va donc pas dans la rangée haute.

**Confiance élevée ; fréquente dans ce contexte.** Pas courant 10–11g ; ne pas fixer un ordre universel par capacité décroissante : certaines rangées le suivent, d'autres non.

### C3 — ADC/CIS : conserver les trois voies et séparer analogique, commandes et alimentation

**Déclencheur.** Chaîne du capteur CIS et du VSP5610.

**Production graphique.** Garder côte à côte le bloc ADC et son connecteur de capteur, sans imposer que le connecteur soit à gauche. Au connecteur, représenter les trois lignes analogiques parallèles avec résistances série alignées et capacités de dérivation regroupées sous les lignes. Relier par leurs labels les arrivées analogiques sur l'ADC. Maintenir les condensateurs de référence/échantillonnage autour des broches analogiques concernées, les sorties DCMI et commandes numériques sur la face numérique. Placer les LDO dédiés comme petites cellules complètes dans le même bloc fonctionnel.

**Preuves.** V4 J3 à x=278,130 mm, R33/R34/R35 à x=236,855 mm, C46/C51/C53 à y=36,195 mm, ADC U3 à gauche. Les lignes du connecteur se lisent électriquement de droite à gauche ; les arrivées de labels sur U3 sont à gauche et les données numériques sortent à droite. V3 possède déjà trois voies et un réseau de capacités autour du connecteur CIS, mais pas le même ADC externe. U7/U8 sont empilés, ancre x=203,835 mm, Δy=35g.

**Confiance élevée pour le CIS V4 ; moyenne pour la généralisation, contextuelle.** Ne pas confondre les C sur REFP/REFN/REF_AIN/échantillonnage avec un filtre passe-bas à GND ; conserver leur topologie exacte. Aucun ordre « connecteur→AOP→filtre actif→ADC » universel n'est démontré.

### C4 — Gros MCU : banques de découplage par domaine et sorties à labels

**Déclencheur.** Grand symbole MCU regroupant les broches sur une seule unité.

**Production graphique.** Conserver le grand corps dans son bloc MCU ; découplage en banques au-dessus, subdivisé suivant les domaines existants et raccordé aux broches correspondantes. Faire descendre les fils de ces banques sur les broches d'alimentation hautes. Placer reset, boot, références et quartz près de leur groupe de broches. Utiliser des départs de signaux parallèles vers des labels, sans tirer tous les bus jusqu'aux périphériques éloignés.

**Preuves.** V3 U2 et ses banques hautes ; V4 U14, deux rangées principales de C à y=28,575/45,085 mm, groupes dédiés à proximité. V4 R54/C105 près de NRST, R55 sur BOOT0, C96/C102/C106 près de VREF+, quartz du côté des broches d'oscillateur. Les GPIO occupent des colonnes de départs répétées.

**Confiance élevée ; contextuelle.** Ce regroupement collectif est compatible avec F1. Il ne signifie pas qu'un condensateur peut être raccordé à n'importe quel domaine. Le placement sur le schéma ne remplace pas le placement PCB près des broches.

### C5 — Mémoire : suivre les banques de broches existantes

**Déclencheur.** SDRAM ou mémoire série.

**Production graphique.** Labels courts sur les départs individuels ; découplage aux zones d'alimentation du symbole. Pour la SDRAM dont les broches d'alimentation sont dispersées, garder des petits groupes de C sur les côtés plutôt que d'imposer une unique rangée haute.

**Preuves.** V4 U9 : C71/C74 en haut à gauche, C69/C70/C72/C73 le long des VDDQ gauches, C82/C83 à droite. V3 mémoire série U7 et V4 U10/U13 : petits groupes locaux. Les noms FMC ne sont pas ordonnés numériquement le long du symbole.

**Confiance moyenne ; contextuelle.** Ne pas trier visuellement les signaux au prix d'une permutation de broches, ni interpréter l'ordre existant comme un choix universel pour les bus.

### C6 — Tirage versus résistance série : deux motifs différents

**Déclencheur.** Strap/pull-up/pull-down ou adaptation série d'une interface.

**Production graphique.** Les tirages de plusieurs lignes forment une rangée verticale raccordée à un rail commun, avec une descente vers chaque ligne. Une résistance série sur une liaison horizontale reste dans la ligne. Un pull-down isolé peut être latéral si la broche est latérale et le retour de masse court.

**Preuves.** V4 U5 : R10/R13/R14/R15/R16 à y=335,915 mm, pas de 8g ; R4…R9 en série sur les arrivées ; R11 descend vers GND sur ETH_RST. V3 Ethernet U14 possède le même motif de straps. V4 R55 BOOT0 et R70 sur une entrée MCU montrent des résistances vers masse horizontales.

**Confiance élevée ; contextuelle.** « Toutes les résistances de masse sont verticales » serait une règle fausse.

### C7 — MOSFET de commande : cellule verticale répétée

**Déclencheur.** Commande LED par commutation côté masse telle que dessinée dans les références.

**Production graphique.** MOSFET au centre, charge/drain au-dessus, source vers la masse au-dessous. Résistance de grille du côté de l'arrivée de commande, pull-down de grille dans sa branche vers GND. Répéter les trois cellules sans déplacer les seuls passifs dans un bloc séparé.

**Preuves.** V3 trois cellules dans CIS CONNECTOR ; V4 Q1/Q2/Q3 : résistance de charge au-dessus, R37/R40/R43 au-dessus à gauche, R38/R41/R44 sous le nœud de grille. Pas de cellule 22g en V4.

**Confiance élevée ; contextuelle.** Ce motif décrit la commande historique. Pour un futur asservissement à AOP, conserver l'association actif/passifs mais ne pas prétendre disposer déjà d'un style personnel démontré de boucle de courant.

### C8 — Ethernet : chaîne filaire et branches de protection attachées à l'interface

**Déclencheur.** PHY, magnétiques et RJ45.

**Production graphique.** PHY à gauche, magnétiques au milieu, RJ45 à droite ; lignes différentielles principalement horizontales. Terminaisons/rails au-dessus ou sous leurs nœuds ; protections en dérivation sous les lignes ; extraction d'alimentation sous le connecteur. Les connexions locales restent filaires.

**Preuves.** V3 U14→J2 à magnétiques intégrés ; V4 U5→TR1→J4. V4 D1/D2 sous les paires, D3/F1 sous J4, C49/C52/C54/C58 et résistances de terminaison organisés en branches basses. Voir atlas page 6.

**Confiance élevée pour Ethernet ; contextuelle.** Cela n'établit pas la disposition préférée d'une protection USB, d'une entrée analogique protégée ou d'une interface haute tension.

### C9 — Connecteurs : position déterminée par la fonction

**Déclencheur.** Connecteur lié à un sous-ensemble.

**Production graphique.** Placer le connecteur du côté qui permet de lire son interface et ses composants associés, en conservant son brochage. Les connecteurs CIS/Ethernet/display sont souvent à droite de leur électronique ; un connecteur de programmation constitue une petite cellule près du MCU. Un connecteur horizontal de capteur peut rester au-dessus de ses trois voies.

**Preuves.** V3 connecteur CIS horizontal en haut de son bloc et OLED vertical à gauche de la page ; V4 J3 à droite de CIS ADC, J1/J2 à droite des cellules DISPLAY ; RJ45 à droite en V3/V4 ; PROG CONNECTOR près du MCU dans les deux versions.

**Confiance élevée pour la diversité observée ; contextuelle.** Ni « tous les connecteurs à gauche », ni « tous à droite » n'est justifié.

### C10 — Croisements : orthogonalité récente, jonctions explicites, croisements admis

**Déclencheur.** Plusieurs lignes parallèles et branches de tirage/découplage.

**Production graphique.** Partir horizontalement/verticalement, changer de direction à angle droit. Garder les branches en colonnes. Distinguer explicitement la dérivation électrique par sa junction du croisement sans connexion. Ne pas ajouter un point à un croisement pour rendre le dessin « plus net ».

**Preuves.** 644/644 segments orthogonaux V4_AUTO, 679/679 V4_REF ; V3 283/288. Les croisements strictement intérieurs à un segment H et un segment V sont nombreux : 53 V3, 80 V4_AUTO, 84 V4_REF, sans junction à ces intersections. Ce comptage exclut les T, les extrémités et les diagonales ; ce n'est pas un audit d'isolation des nets. Les rangées de straps PHY et les réseaux ADC montrent les croisements conservés pour rester compacts.

**Confiance élevée ; fréquente pour l'orthogonalité, contextuelle pour les croisements.** Aucun seuil personnel « zéro croisement » ou nombre maximal de coudes par liaison n'est établi.

### C11 — Références de CI : nom commercial et référence dégagent le corps

**Déclencheur.** Présentation des champs d'un CI.

**Production graphique.** Sur les cellules d'alimentation et analogiques comparables, nom commercial au-dessus, référence généralement sous le corps ou en bas à droite. Conserver les variantes des grands CI et de la mémoire. Ajuster les champs selon le corps réel, pas selon l'origine arbitraire de l'instance.

**Preuves.** V3 U1/U3/U9/U4/U5 ; V4 U1/U2/U3/U7/U8/U5 suivent largement ce motif. V4 U9 a les deux champs au-dessus ; U14 et U13 les ont en bas ; U6 change de disposition entre AUTO et REF.

**Confiance moyenne ; contextuelle.** Aucune règle systématique unique de position des références de tous les CI ne doit être inscrite.

## 7. Contradictions et exceptions identifiées

| ID | Constat précis | Interprétation et traitement proposé |
|---|---|---|
| E1 | Entrée→sortie à droite dans POWER et Ethernet ; capteur J3 à droite de l'ADC ; voies analogiques arrivant par labels à gauche de U3. | Le rôle des faces/broches et l'organisation du bloc dominent une direction globale. Appliquer P1/C3/C9 selon le contexte. Confiance élevée, contextuel. |
| E2 | Masse sous la plupart des C, mais latérale sur MCU, ADC, mémoire et LDO ; quelques masses orientées vers le haut. | Préférence descendante, exceptions pour connexion courte à une face du symbole. Ne pas tourner un grand CI pour éliminer ces exceptions. Confiance élevée, contextuel. |
| E3 | C regroupés en rangées en haut du MCU, mais répartis sur les côtés de la SDRAM. | Dépend de la répartition des broches d'alimentation. Les banques du MCU sont collectives ; la SDRAM conserve des groupes par zone. Confiance élevée, contextuel. |
| E4 | V3 emploie champs de 1,27 mm et davantage d'espace entre cadres ; V4 passe à 1 mm et resserre les cadres. | Évolution de densité, pas un motif électrique prouvé. Proposer V4 comme cible pour V5, à valider explicitement. Confiance moyenne sur l'intention, fréquent par génération. |
| E5 | Valeurs R centrées dans V4_AUTO ; plusieurs R ajoutées de V4_REF ont des champs extérieurs. | Possible effet de bibliothèque/revue récente, pas de changement de goût démontré. La proposition conserve le motif intérieur, soutenu par V3, AUTO et la capture. Confiance moyenne sur la cause. |
| E6 | V3 contient cinq fils diagonaux : quatre dans Ethernet et un sur le retour ADJ de U5 ; aucun en V4. | Écart ancien/local, pas règle à reproduire. Proposer les coudes orthogonaux récents ; ne pas réécrire un croisement sans vérification de net. Confiance élevée sur le constat, exceptionnel. |
| E7 | Position des champs U variable : régulateurs, RAM, MCU, flash et TXS0108 ne sont pas identiques. | Plusieurs gabarits selon le symbole. Garder C11 contextuel ; validation nécessaire avant uniformisation. Confiance élevée, contextuel. |
| E8 | V4_AUTO contient U15/U16 et C associés hors largeur A2 (x>600 mm) ; quelques labels flottants et cadres imparfaits. V3 porte une annotation géante de conflit EXTI. | Éléments de travail/inachèvement possibles, pas preuves d'une préférence. La demande explicite actuelle exclut le maintien des fonctions hors cadre. Ne pas apprendre la grande annotation comme taille de texte courante. Confiance élevée sur le constat, faible sur l'intention, exceptionnel. |
| E9 | Certaines limites de blocs sont partagées ou en L ; une limite de DISPLAY est légèrement oblique. | Le découpage fonctionnel est fort, la perfection géométrique ne l'est pas partout. Proposer d'aligner les limites lors de l'application validée ; conserver la possibilité d'un bloc en L. Confiance moyenne, exceptionnel pour l'oblique. |
| E10 | Beaucoup de croisements de fils malgré une forte préférence pour les lignes orthogonales. | La compacité de faisceaux locaux est acceptée. Ne pas imposer une absence de croisements en déportant les passifs ou en multipliant les labels. Confiance élevée, contextuel. |

Les petites valeurs inscrites dans les résistances et les champs serrés peuvent perdre en lisibilité sur un export pleine page. Proposition séparée : agrandir localement un motif ou produire des extraits pour la revue, plutôt que déplacer systématiquement ses valeurs à l'extérieur. Les marges de cadres de 4–6g nécessitent aussi un contrôle visuel des titres. **Ces alternatives ne sont pas appliquées sans validation du style.**

## 8. Points non démontrés — ne pas compléter par des habitudes génériques

| Sujet demandé | Ce que le corpus permet réellement |
|---|---|
| AOP, différentiels, unités A/B/C et unité d'alimentation séparée | Aucun composant multi-unité dans les trois références retenues ; aucun ensemble suffisant d'AOP discrets. Style non établi. Besoin d'exemples personnels comportant plusieurs boucles/voies pour choisir placement du feedback et des unités. |
| DAC et référence de tension autonome | Pas de chaîne DAC autonome représentative. V3 U5 produit un rail de référence et V4 a des broches de référence découplées, mais cela ne démontre pas un gabarit général DAC/référence. |
| Filtres analogiques actifs | Réseaux passifs RC et ferrites observés ; aucune série suffisante de filtres actifs pour inférer Sallen-Key, MFB, différentiel ou ordre spatial de leurs boucles. |
| Chaîne d'acquisition analogique générale | CIS à trois voies documenté ; généralisation à capteur→préampli→filtre→ADC non démontrée. |
| Hiérarchie et labels globaux | Références personnelles candidates toutes sur une feuille. Absence de labels hiérarchiques ne signifie pas refus de la hiérarchie. |
| Protections hors Ethernet | Motif Ethernet démontré. Protection analogique, USB, alimentation réversible et driver LED à courant asservi non établis stylistiquement par ce corpus. |
| Espacement universel, densité cible, maximum de coudes | Pas de seuil unique démontré. Employer les gabarits par contexte et le contrôle visuel. |
| Préférence interprojets | Une seule famille CIS exploitable confirmée par l'inventaire actuel. Compléter/valider la provenance de nouveaux projets avant d'affirmer une grammaire personnelle universelle. |

Pour ces cas, après validation générale, proposer un petit exemple graphique à faire valider ou conserver le motif existant. Ne pas présenter une convention KiCad courante comme une convention personnelle apprise.

## 9. Procédure d'application après validation

### Avant tout déplacement

1. Identifier précisément la feuille et la révision visées. Prendre un snapshot du schéma, du projet et des bibliothèques ; enregistrer leurs empreintes SHA-256. Respecter les fichiers déjà modifiés par l'utilisateur.
2. Exporter la netlist avec KiCad depuis l'état de départ. Enregistrer l'inventaire composants, UUID, références, unités, identifiants de symboles, valeurs, champs de tension, empreintes, attributs DNP/BOM/PCB et paramètres de broches. Garder les labels et symboles d'alimentation avec leur portée.
3. Exécuter l'ERC de départ lorsque possible ; conserver les diagnostics comme référence. Une erreur préexistante n'est pas une autorisation de la corriger pendant une tâche graphique.
4. Construire les groupes **par rôle électrique** : actif + entrée + sortie + réglage/feedback + découplage + commandes/protections. Un condensateur voisin n'appartient pas nécessairement au même domaine. Choisir les règles F/P/C applicables et signaler les cas encore non définis.
5. Séparer le plan graphique de toute proposition électrique. Ne pas changer silencieusement de symbole de bibliothèque pour obtenir un dessin plus conforme : une variante peut modifier broches, unités ou types électriques.

### Pendant les déplacements

1. Installer les fonctions, puis les actifs, puis les passifs associés ; appliquer les motifs contextuels et les pas mesurés.
2. Router les connexions locales et disposer leurs junctions ; conserver les labels et leur portée. Respecter l'ordre des voies et les noms existants.
3. Placer champs et titres en dernier, en vérifiant le rendu réel des rotations. Dimensionner les cadres d'après l'ensemble des symboles **et textes**, pas seulement leurs ancres.
4. Vérifier que chaque fonction désignée est dans son cadre et dans la page imprimable, sans empiéter sur le cartouche. Préserver le découpage en L si utile et validé.

### Vérification obligatoire de l'intégrité

1. Ouvrir/charger le résultat avec KiCad et refaire l'export XML et PDF. Le succès du parsing Python seul ne prouve pas l'ouvrabilité ni la bonne édition dans KiCad. Contrôler aussi l'ouverture dans l'éditeur lorsque disponible ; si seul le CLI a été utilisé, le dire explicitement.
2. Comparer les nets comme **ensembles de terminaux** `(chemin hiérarchique, référence, numéro de broche)`, avec inventaire des composants. Comparer la partition complète, les broches isolées et les marqueurs non-connectés ; pas seulement le nombre de nets, ni les codes numériques d'export. Les noms automatiques peuvent changer lors d'un export ; les noms explicites et leurs portées doivent rester identiques.
3. Comparer séparément les unités et leur affectation au composant, les symboles, valeurs, champs, numéros et types de broches, attributs et alimentations. Traiter les broches superposées/cachées et les symboles d'alimentation globaux ; ne pas se limiter aux connexions visibles sur le PDF.
4. Vérifier les junctions, contacts fil/broche, jonctions en T, croisements, labels effectivement ancrés aux fils et nouveaux contacts accidentels. Un déplacement de label peut joindre des nets même lorsque le dessin paraît cohérent.
5. Exécuter l'ERC final si disponible et comparer les diagnostics sémantiquement, en tenant compte du déplacement des coordonnées. Investiguer toute différence nouvelle. Un ERC inchangé ou sans erreur n'est **pas** une preuve suffisante d'identité de connectivité.
6. Contrôler visuellement la page complète et des extraits : croisements, ordre des voies, orientations, textes dans les résistances, condensateurs, cadres, bord de page. Les comparaisons de netlist et l'inspection graphique sont complémentaires.
7. Livrer le schéma, les exports de revue et le résultat des comparaisons. Si une vérification n'a pas été possible, indiquer précisément laquelle ; ne pas déclarer la réorganisation validée électriquement sur la seule apparence.

## 10. Application autorisée et questions restant ouvertes

La proposition est d'adopter **F1–F6**, **P1–P6 avec leurs limites**, et **C1–C11 uniquement dans leurs contextes observés**, avec **g=25 mil** et les gabarits dimensionnels ci-dessus. Les cas de la section 8 restent volontairement ouverts.

Questions de généralisation à d’autres schémas :

- Les sources CIS retenues représentent-elles bien le style personnel à reproduire ? Quels autres projets/feuilles personnels peuvent établir les cas encore absents ?
- Pour V5, retenir la densité et la typographie V4 (1 mm), les valeurs R dans le corps et les rangées C à 10–11g ?
- Confirmer que les exceptions liées aux broches sont souhaitées : masses latérales, découplage SDRAM distribué, connecteurs parfois à droite, MCU regroupé sur une seule unité.
- Confirmer que les écarts de travail hors cadre, limites obliques et annotation géante ne sont pas des conventions à reproduire.

**Autorisation utilisateur : demande explicite du 8 septembre 2026 d’appliquer la charte aux zones des captures.** L’application utilise F1–F6, les préférences observées et les contextes pertinents, sans modifier le circuit. Voir [le compte rendu d’application](RD/Application_Charte_2026-09-08.md). Les points de la section 8 restent ouverts.


## 11. Affinage à partir du bloc DISPLAY fourni — application autorisée

**Demande utilisateur :** améliorer les règles de placement, de longueurs des fils et de labels à partir de l’extrait DISPLAY, puis appliquer les modifications proposées. Cette autorisation couvre la présente réorganisation graphique ; aucune modification de topologie ni nouvelle demande d’approbation n’est nécessaire pour ces placements.

L’extrait montre U6/TXS0108, J1, U10/Flash, U4/TPS65632 et J2. Les conventions retenues sont : départs de signaux parallèles et étiquetés sur leur fil, capacités associées au CI, connexions locales orthogonales, résistances de tirage verticales et résistances série dans le chemin du signal. Les collisions visibles autour de C133/C134/C135 sont des écarts à corriger, pas des précédents à reproduire.

Les dimensions ci-dessous sont des **prescriptions graphiques pour ce projet**, autorisées par cette demande. Elles ne sont ni des distances déduites des pixels de la capture, ni des contraintes constructeur.

### L1 — Longueur d’un départ étiqueté dictée par le texte

- Conserver la grille électrique **g = 0,635 mm**. Garder un fil court de 4g lorsqu’il sert simplement à raccorder une broche à un élément voisin.
- Pour un départ terminal portant un label, réserver au moins **la largeur rendue du texte + 4g**, avec un point de départ de **12g = 7,62 mm**. Arrondir la longueur au g supérieur. Cette réserve dégage le texte du numéro de broche, de la branche ou du passif voisin.
- Mesurer la largeur dans le rendu KiCad à la taille retenue, ou prendre une enveloppe conservatrice. Un nombre fixe de caractères ne suffit pas : `M`, `I` et `_` n’ont pas la même largeur. La présente application utilise les étendues de texte de l’export PDF KiCad.
- La règle concerne seulement une **queue de fil libre portant un label**. Ne pas raccourcir une liaison entre deux composants, une branche de feedback ou un bus partagé sur la base de cette longueur.
- Ne jamais déplacer le bout du fil sur une autre broche, un croisement ou un fil voisin. Comparer les partitions de netlist après modification.

### L2 — Labels lisibles sur le fil et colonnes alignées

- Départ vers la gauche : label au bout gauche, lecture normale, texte au-dessus du fil et vers la broche. Départ vers la droite : texte au-dessus du fil, aligné par sa fin sur le bout droit.
- Dans une banque de signaux homogènes, choisir une **colonne commune selon le nom le plus large** et la position de la première branche. Ne pas créer un escalier d’extrémités parce que les noms ont des longueurs différentes.
- Dégager aussi les champs voisins : une masse de la rangée précédente peut imposer un fil plus long. La compacité ne prime pas sur la séparation des textes.
- Un label placé à une sortie de porte avec pull-up reçoit un court départ explicite après la jonction. Le texte ne se superpose pas à la référence du pull-up.
- Les noms, portées et polarités sont conservés. Une seule feuille ; aucun label global ou hiérarchique de navigation n’est ajouté.
- Les marqueurs graphiques associés à une paire différentielle se déplacent avec la paire, ou la paire conserve sa disposition. Ne pas laisser des marqueurs isolés après raccourcissement des fils. Les départs DSI du bloc de référence sont conservés dans cette application.

### L3 — Passifs proches, sans déformer les symboles

- Rapprocher les séries et tirages de la face du CI qu’ils desservent. Déplacer chaque composant avec ses champs, ses symboles d’alimentation/masse et ses fils associés.
- Conserver une translation rigide des broches d’un symbole : on peut supprimer un espace vide entre cellules, pas étirer un symbole ou déplacer une broche indépendamment.
- Garder visibles les rails locaux et les retours SENSE/FB. Les labels relient les fonctions distantes ; ils ne remplacent pas ces connexions de compréhension.
- Dans une banque de sorties à pull-downs, réserver la hauteur nécessaire au corps de la résistance, à la masse et à ses textes. Le maintien du pas de 12,7 mm de U18, retenu le 8 septembre, est remplacé par la règle de compacité du §12 à la demande de l’utilisateur le 9 septembre.
- Ne pas déduire la marge entre deux composants uniquement de leurs ancres. Les valeurs, références, tensions et jonctions font partie de leur enveloppe visuelle.

### L4 — Champs des résistances et condensateurs

- Résistance série isolée : valeur dans le corps, référence centrée **4g = 2,54 mm au-dessus**. La référence ne doit pas être imprimée dans le fil de sortie.
- Rangée serrée de séries, notamment R115…R119 : référence déportée latéralement de **8 à 10g**, et de **2g = 1,27 mm vers le haut**. Ne pas placer la référence exactement dans le corps de la résistance de la ligne précédente.
- Si un symbole de masse ou un autre texte occupe l’emplacement au-dessus, utiliser un emplacement au-dessous et latéral, comme pour R139. L’exception doit rester cohérente avec le chemin du signal.
- Capacités en dérivation : référence au-dessus des plaques, valeur en dessous et tension sur la ligne suivante. Les textes restent horizontaux à la lecture, indépendamment de l’orientation 0°/180° du symbole.
- Pour les capacités OLED concernées, employer **12g = 7,62 mm entre axes**, plutôt que les 8g qui causaient les collisions. Cette valeur est une correction locale, pas un remplacement universel des autres pas du corpus.
- Une tension nominale existante ne doit pas être supprimée pour gagner de la place ; élargir la cellule ou repositionner le champ. Aucun champ électrique n’est renommé ni aucune valeur changée.

### L5 — Vérification de l’application

Contrôler les exports à la fois à l’échelle du bloc et en détail : labels près des numéros de broches, masses des lignes voisines, références des séries, tensions des capacités et croix DNP. Le contrôle visuel complète l’ERC et la comparaison exacte des nets. Un fil schématique plus court **ne signifie pas** une piste PCB plus courte ni une amélioration du timing électrique.

Application : voir [RD/Affinage_Placement_2026-09-08.md](RD/Affinage_Placement_2026-09-08.md). La feuille reste A0 ; les bibliothèques de symboles, les valeurs, les références commerciales et le PCB sont conservés.


## 12. Symboles compacts — correction autorisée du 9 septembre 2026

Le corps très étiré de U18 n’est pas une référence de style à reproduire. Privilégier les dimensions et le pas de broches du symbole KiCad approprié. Lorsqu’un dérivé local est nécessaire pour conserver l’identité exacte du composant, documenter son gabarit et conserver brochage, types électriques, références, empreinte et attributs. Le seul nom ressemblant d’un composant ne suffit pas à établir sa compatibilité.

Ne pas agrandir systématiquement un CI pour placer un tirage et une masse entre chaque voie. Pour un buffer dense tel que U18, conserver les séries directement dans les sorties et regrouper les tirages dans des banques compactes immédiatement adjacentes, reliées par des labels locaux. Distinguer les côtés entrée/sortie et les tirages haut/bas. Cette disposition est une exception explicite à la préférence des connexions locales entièrement filaires ; elle ne justifie pas de déporter les passifs dans une autre fonction ou feuille.

Cette demande autorise la modification graphique du symbole U18 et de sa bibliothèque locale, avec contrôle des connexions par numéro de broche. Lorsqu’on reprend un gabarit de bibliothèque, vérifier aussi l’ordre vertical des broches : l’ordre visuel peut changer sans que les signaux changent de broche. La copie en bibliothèque et celle incorporée au schéma doivent rester identiques.

Application : [RD/Compactage_U18_2026-09-09.md](RD/Compactage_U18_2026-09-09.md).


## 13. Boucles LED : disposition utilisateur du 9 septembre 2026

**Source primaire de style :** capture utilisateur et canal bleu U28/U25/Q3 sauvegardé dans le schéma. Cette disposition remplace les propositions antérieures de placement des trois canaux LED. Son application aux canaux rouge et vert est explicitement demandée ; elle n’autorise pas, à elle seule, la réaffectation d’une broche MCU ou l’ajout d’une consigne DAC.

- Aligner horizontalement la sortie du commutateur et l’entrée non-inverseuse de l’OPA320. Aligner la sortie de l’AOP, la résistance série de grille et la grille du NMOS.
- Garder le symbole AOP triangulaire et le commutateur compact choisi par l’utilisateur. Avant de reproduire le motif, résoudre le symbole effectivement employé, y compris `lib_name` s’il désigne une variante incorporée distincte du `lib_id` de bibliothèque. Copier les positions des seuls composants sans les bonnes extrémités de broches peut rompre les alimentations.
- Placer le découplage du commutateur au-dessus à gauche et celui de l’AOP au-dessus à droite, avec leurs rails et retours locaux visibles.
- Faire partir le drain verticalement vers le haut, avec son label vertical. La résistance de mesure descend depuis la source vers la masse ; le rappel de grille descend vers sa propre masse.
- Fermer la boucle de mesure sous l’AOP : résistance de retour 1 kΩ à droite, compensation verticale entre sortie d’AOP avant résistance de grille et nœud inverseur, biais 1 MΩ arrivant de la gauche. Conserver tous les points de jonction électriques.
- Placer les labels de consigne, commande et biais sur des départs courts à gauche. Conserver les propriétés de lecture de la capture : valeurs résistives intégrées, références des séries au-dessus, référence du biais au-dessous, annotations des capacités empilées avec leur tension.
- Reproduire les cellules homologues par translation du motif complet, sans recopier les noms de nets propres à une autre couleur. Préserver composants, UUID, valeurs, numéros et types des broches. Ne pas déplacer le canal utilisateur servant de modèle.
- Conserver la géométrie voulue et distinguer grille de dessin, coordonnées effectives des symboles et grille ERC : le motif utilise des multiples de 25 mil alors que le contrôle de connexions du projet est réglé sur 50 mil. Signaler les avertissements supplémentaires ; ne pas déplacer indépendamment une extrémité de broche ni désactiver une règle pour faire disparaître le diagnostic.

Le motif est démontré pour ces boucles de courant LED. Il ne constitue pas une règle universelle de placement pour les amplificateurs ou filtres analogiques.

Application et proposition DAC : [RD/Disposition_LED_et_option_DAC_2026-09-09.md](RD/Disposition_LED_et_option_DAC_2026-09-09.md).
