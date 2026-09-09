# Corrections du schéma d’acquisition — 8 septembre 2026

Les corrections autorisées sont appliquées au **schéma**, révision 4.0.1. Elles visent à rendre le prototype WHEC LC3R216N-8008 → VSP5610 → STM32H747 exploitable et réglable. Elles ne constituent pas une qualification de l’interface DCMI sur tout le domaine PVT.

Le PCB, le fichier CubeMX et le firmware n’ont pas été modifiés. Dans `.kicad_pro`, la seule différence observée concerne la métadonnée `used_designators`, désormais vide ; les réglages électriques sont conservés. À la demande de l’utilisateur, tous les circuits sont réintégrés dans **CIS.kicad_sch**, sur une seule feuille A0. Les deux feuilles hiérarchiques ont été supprimées et les étiquettes globales remplacées par des étiquettes locales sans renvoi de navigation. Les 359 réseaux électriques, valeurs, empreintes et états DNP sont identiques à la version corrigée avant cette réorganisation. La bibliothèque `Acquisition_Options.kicad_sym` et l’empreinte locale `Library:ADP7104_RD-8-4` accompagnent les nouveaux composants.

## Modifications appliquées

| Élément | Modification et raison |
|---|---|
| U7/U8/U15 | Remplacement des trois ADP7142 par **U7 ADP7104ARDZ-3.3, 500 mA**, avec retour SENSE à VOUT. WHEC VDD, VSP VDD/LVDD/DVDD_IO et logique d’acquisition alimentés par le même net `+3.3VACQ`. Supprime l’écart de séquencement entre trois régulateurs indépendants. |
| Alimentation | C143/C144 = 100 µF/16 V X5R 1210 à l’entrée, C145 = 100 nF ; C146 = 10 µF et C147 = 100 nF en sortie. R89 = 1 kΩ pour décharge passive. Les réservoirs WHEC C136/C137 de 47 µF sont conservés. |
| Masses | GNDA et GND deviennent un seul net GND ; R72 supprimée. Le futur PCB doit réaliser un plan continu, avec placement séparant les retours LED, numériques et analogiques. Aucun plan cuivre n’a été changé dans cette intervention. |
| R82 | Pull-up SEN déplacé du 3,3 V permanent vers `+3.3VACQ`. |
| U18 | **SN74LVC244APW**, alimenté par ACQ : sept commandes MCU traversent un buffer à entrées tolérantes et protection Ioff lorsque VCC = 0. Rappels côté MCU et côté récepteurs ajoutés. SDO reste une entrée directe du MCU. |
| U19/U21 | **SN74LVC1G14DBV** et **SN74LVC1G132DBV**, entrées Schmitt. Groupe 1 de U18 : MCLK/SPI autorisés par PG. Groupe 2 : SI/CNT/XLSYNC autorisés seulement par PG **et** `ACQ_RUN_EN`. |
| GPIO de contrôle | PJ0/bille N6 : `ACQ_RUN_EN`, rappel bas R112 = 10 kΩ. PJ1/bille P6 : lecture de `ACQ_PGOOD`. PJ14/bille D10 conserve `PW_ADC_EN`. |
| XLSYNC | Protection contre la contention au démarrage : U3.45 est une **sortie par défaut** ; U18.5 reste haute impédance tant que RUN_EN = 0. Cette autorisation doit rester basse jusqu’à configuration du VSP en synchronisation externe. |
| MCLK | Sortie tamponnée divisée en branches WHEC et VSP avec résistances série propres. R120 = 22 Ω vers WHEC ; R121 = 22 Ω vers RCLKP. |
| RCLKN | R87/R85 = 1 kΩ/1 kΩ, C142 = 1 nF C0G, liaison de polarisation R125 = 0 Ω. Constante de temps idéale du pont : 0,5 µs. Option différentielle U20 **SN65LVDS1DBV**, DNP, avec terminaison 100 Ω DNP. |
| PIXCLK | R84 = 0 Ω et R64 = 33 Ω conservées en chemin direct GPIO3 → PA6. R88 et C141 restent DNP. Ajout U17 **DS1100LZ-20**, DNP, et cinq sélections de retard nominal 4/8/12/16/20 ns. Aucun condensateur de retard n’est imposé. |
| Synchronisation DCMI | Options DNP PB6/TIM4_CH1 → HSYNC et PA0/TIM2_CH1 → VSYNC, ou sources externes sur J5. Pull-downs HS/VS conservés. TIM4 est aussi utilisé pour LED_R : configuration coordonnée nécessaire. |
| Analogique | C46/C51/C53 = 100 pF **C0G**. C59 = 1 µF passée DNP pour réduire la charge VREF. R86 passée DNP : voie 4 court-circuitée/découplée, sans charge supplémentaire sur VREF. C16 reste DNP. |
| LED | R39/R42/R45 = **56/33/30 Ω**, 1 %, boîtier 1206, puissance 0,25 W. Réduit le risque de dépasser 60 mA crête ; la limite doit encore être mesurée. |
| Mesures | TP1…TP15 et J5 DNP. TP13/14/15 sont raccordés à PIXCLK/D0/D7 **après les résistances série, côté STM32**. |
| Symboles et notes | Types électriques du VSP corrigés selon sa fonction, y compris les broches multiplexées. Anciennes annotations affirmant une garantie LVCK/registre/timing retirées, descriptions des composants corrigées. |

## Variantes de montage : ne pas mélanger les pilotes

Les croix DNP représentent des composants **non montés** ; la netliste KiCad conserve leurs connexions.

| Fonction | Montage initial | Variante de caractérisation |
|---|---|---|
| PIXCLK direct | R84 montée ; U17, R114…R119, R88, C141 DNP | Retirer R84. Monter U17 + R114 et **une seule** de R115/116/117/118/119. Garder R88 DNP. |
| Retards U17 | Aucune sortie sélectionnée | R115 = tap 1/4 ns (broche 7) ; R116 = tap 2/8 ns (2) ; R117 = tap 3/12 ns (6) ; R118 = tap 4/16 ns (3) ; R119 = tap 5/20 ns (5). Valeurs nominales uniquement. |
| RCLK CMOS/bias | R121 et R125 montées ; U20/R122/R123/R124 DNP | Pour LVDS, retirer R121 **et** R125 ; monter U20, R122/R123 = 0 Ω et R124 = 100 Ω. Polarisation R87/R85 isolée du récepteur. |
| Framing MCU | R126/R127 DNP initialement | Monter R126 = 33 Ω pour PB6 → PA4/HSYNC, R127 = 33 Ω pour PA0 → PI5/VSYNC. |
| Framing externe | J5/R128/R129 DNP | Monter J5 et R128/R129 = 33 Ω ; ne pas monter les straps MCU correspondants. Sources externes 3,3 V uniquement. |

GPIO2/R88 reste une réserve physique **non qualifiée** : ne pas la monter sur la base d’une écriture dans un champ réservé supposé.

## Séquence à respecter dans le futur firmware

1. Au reset MCU : PJ0/RUN_EN bas, PJ14/PW_ADC_EN bas ; DCMI et SDO en entrées sans pull-up. SEN haut côté MCU ; signaux capteur et horloges définis au repos.
2. Activer PW_ADC_EN, attendre PG lu sur PJ1 avec timeout. PG valide matériellement MCLK et SPI. Il ne garantit ni la fin du reset interne VSP ni le lock PLL.
3. Initialiser le VSP par SPI : respecter les délais constructeur accessibles, vérifier les lectures et l’état d’horloge. Sélectionner SDI en entrée : le buffer unidirectionnel ne permet pas le protocole SDI bidirectionnel à trois fils.
4. Configurer explicitement XLSYNC en entrée (`XLSYNC_SEL = 1`, adresse/masque à obtenir dans la map exacte du 5610). Définir SI/CNT/XLSYNC bas avant d’activer RUN_EN.
5. Activer RUN_EN puis démarrer les timers capteur et la capture correctement synchronisés. La validité des registres LVCK et de la calibration reste à établir ; aucune écriture déduite d’un registre réservé n’a été ajoutée.
6. Avant arrêt, reset logiciel VSP ou reconfiguration de XLSYNC : **RUN_EN = 0 d’abord**, puis arrêter les commandes, puis couper l’alimentation si nécessaire. Attendre la décharge réelle avant un redémarrage supposé équivalent à un power-cycle. Sur chute PG, abandonner la capture et reprendre l’initialisation complète.

Cette séquence est une exigence d’intégration ; elle n’est pas implémentée dans le firmware existant.

## Calculs et limites restantes

**Alimentation.** Un seul rail supprime le suivi inter-régulateurs à garantir ; il ne supprime pas les chutes locales ni les injections par signaux externes. Dimensionner le cuivre, l’inrush et la thermique. À 4,5 → 3,3 V et 500 mA, la dissipation idéale de U7 est 0,60 W. La marge de courant doit inclure capteur, VSP, buffers et option DS1100L. Les entrées Ioff protègent les commandes MCU lorsque ACQ = 0 ; elles ne certifient pas le comportement pendant toute rampe intermédiaire ou lorsque le MCU lui-même n’est plus alimenté.

**Capacités.** Les 200 µF d’entrée sont nominaux : choisir des références dont les courbes DC-bias/température/tolérance assurent au moins 125 µF effectifs à 4,5 V, et confronter CIN à la capacité de sortie totale réellement montée. La recommandation WHEC de réservoir 100 µF ne doit pas être considérée satisfaite par la simple somme nominale de MLCC. C136/C137 et les 10 µF locaux nécessitent cette vérification BOM. COUT local U7 doit conserver au moins 5 µF effectifs comme objectif de conception. L’empreinte SOIC8 EP locale est basée sur le boîtier ADI RD-8-4 ; cuivre thermique, stencil et vias restent à valider avec le futur PCB.

**RCLK.** Le pont 1 kΩ/1 kΩ suit plus rapidement l’alimentation que l’ancien 10 kΩ/10 kΩ + 100 nF. Ni ce calcul ni l’option LVDS ne prouvent le mode commun admissible du VSP5610 au reset. La topologie par défaut et l’alternative doivent être vérifiées auprès de TI et sur prototype.

**DCMI.** À 48 MHz, T = 20,833 ns ; il manque toujours les bornes min/max du délai données/LVCK exporté du VSP5610. Les 12 ns du VSP5640 sont **typiques**, pas un maximum. Le DS1100L-20 spécifie une période minimale de 8 ns et une impulsion minimale de 4 ns ; ses tolérances de retard sont ±3 ns sur 0…70 °C, ±4 ns sur le domaine industriel. Il offre des points d’essai, pas une fermeture automatique du budget setup/hold. Conserver les exigences DCMI data de 3 ns setup et 1 ns hold, sans remplacer les bornes manquantes par une valeur typique.

**WHEC.** Mesurer CLK/SI aux broches du connecteur : VIH ≥ 2,4 V, VIL ≤ 0,5 V, duty CLK 48…52 %, SI setup/hold ≥ 60 ns. Le buffer et les séries modifient les délais et niveaux réels. La fiche WHEC étant préliminaire, la charge d’entrée et l’ambiguïté CNT restent à confirmer.

**LED.** Avec VLED = 4,725 V (hypothèse +5 %), Vf de référence 2,0/3,2/3,3 V, résistances à −1 % et VDS = 0 : I ≈ 49,2/46,7/48,0 mA. Ces Vf ne sont pas des bornes démontrées pour tout le domaine. Vérifier les trois crêtes ≤ 60 mA à froid/chaud ; le PWM ne corrige pas un dépassement du courant pulsé. Une limitation active sera nécessaire si les marges mesurées sont insuffisantes.

## Validation effectuée et essais restant à faire

Export KiCad 10.0.1 de la feuille unique en PDF et XML, vérification des références uniques, du brochage des nouveaux circuits, des rails, des commandes isolées, des variantes DNP et des huit bits DCMI. Le script `RD/verification_acquisition.py` compare aussi les connexions des composants conservés à la netliste avant modification : seules les séparations de commandes et fusions d’alimentation/masse prévues sont autorisées. Le dossier de livraison contient les résultats, rapports ERC bruts, empreintes SHA-256 et nomenclature des options.

**L’ERC complet n’est pas propre** : les signalements préexistants du projet restent à traiter. La comparaison par type et UUID vérifie l’absence de nouveaux signalements hors grille ; une diminution du nombre d’alertes n’est pas une certification électrique.

| Mesure prototype | Accès | Conditions / critère |
|---|---|---|
| Rail, PG, EN, RUN | TP1/2/3/4 ; R112 ; U3.19/.41/.43 et J3.6/.9 | Démarrage lent/rapide, reset MCU, arrêt et redémarrage court, chute de la source. Observer les écarts réels entre broches, l’inrush et la décharge. Aucun pilotage XLSYNC avant sélection entrée. |
| MCLK/RCLK | TP7 CLK WHEC, TP8 RCLKP, TP9 RCLKN ; TP12 GND | MCLK 7,5…8,5 MHz, températures dans le domaine commun des composants, tolérances d’alimentation. Mesurer duty, amplitude, mode commun et comportement au reset. |
| SI/XLSYNC | TP10/11 ; CLK TP7 | Vérifier les 60 ns au connecteur, l’absence de contention à l’allumage et après reset VSP, ainsi que la phase par rapport au plateau analogique. |
| PCLK/données | TP5 LVCK brut, TP6 avant R64, **TP13 PCLK reçu**, TP14 D0, TP15 D7 ; autres bits sur pads MCU des séries R66/R63/R68/R69/R58/R60 | Sondes faible capacité avec ressort de masse, toutes les données mesurées face au même front reçu. Balayer les taps un à un ; exiger setup ≥ 3 ns, hold ≥ 1 ns plus marge de mesure/jitter. Comparer aussi bit à bit des motifs vérifiés. |
| Référence / signaux analogiques | J3 VREF, AIN1/2/3, AINGND1/2/3 ; ne pas charger REF_AIN par défaut | Noir/blanc, LED par LED, températures et gains. Vérifier stabilité VREF, bruit et établissement avant SHD ; réévaluer C59 et la ferrite sur ces mesures. |
| Framing | J5 ou pads R126…R129, PA4/PI5 | Vérifier setup/hold sync de 2/1 ns, frontières d’octets et reprise après arrêt/overrun. Éviter un câble de debug branché à PCLK pendant qualification. |
| LED et thermique | Chute aux bornes R39/42/45 ; U7 | Mesure de courant crête corrigée de la tolérance R, VLED extrêmes, froid/chaud, charge maximale. Vérifier ≤ 60 mA et températures composants. |

Les essais PCB/firmware ci-dessus sont un plan pour l’intégration ultérieure ; aucun résultat de prototype n’est revendiqué.

## Sources primaires

- [TI VSP5610, SBES021](https://www.ti.com/lit/gpn/VSP5610) : limites électriques, p.15 note 2 (voies inutilisées), p.16 (XLSYNC par défaut sortie et SDI), interface série. La map complète et les timings CMOS LVCK/GPIO manquent dans la version publique.
- [WHEC LC3R216N-8008A, copie constructeur locale](CIS/LC3R216N-8008A.pdf) : p.6–9 courant LED, entrées et réservoir. Document préliminaire.
- [ADI ADP7104](https://www.analog.com/media/en/technical-documentation/data-sheets/ADP7104.pdf) : pin configuration, caractéristiques, PG, sélection des condensateurs et thermique ; [boîtier RD-8-4](https://www.analog.com/media/en/package-pcb-resources/package/pkg_pdf/soic_edrd/rd-8-4.pdf).
- [TI SN74LVC244A](https://www.ti.com/lit/ds/symlink/sn74lvc244a.pdf), [SN74LVC1G14](https://www.ti.com/lit/ds/symlink/sn74lvc1g14.pdf), [SN74LVC1G132](https://www.ti.com/lit/ds/symlink/sn74lvc1g132.pdf) : brochage, Ioff, seuils et comportement des entrées.
- [ADI DS1100L](https://www.analog.com/media/en/technical-documentation/data-sheets/ds1100l.pdf) : pin assignment et caractéristiques AC. [TI SN65LVDS1](https://www.ti.com/lit/ds/symlink/sn65lvds1.pdf) : brochage DBV et sortie différentielle.
- [ST STM32H747xI](https://www.st.com/resource/en/datasheet/stm32h747xi.pdf) : brochage/AF et caractéristiques DCMI, table 104 de la révision 3 utilisée dans l’audit.
- VSP5640 : copie constructeur locale dans `RD/Etude CIS ADC/VSP5640 datasheet.pdf`, p.80/95/112. Utilisée uniquement comme **extrapolation identifiée**, jamais pour qualifier un registre réservé du VSP5610.
