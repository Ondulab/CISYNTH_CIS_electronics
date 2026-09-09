# Alimentation CIS — révision 5.0.0-dev, 8 septembre 2026

Le schéma `CIS.kicad_sch` a été repris sur **une feuille A0**, à partir de la version 4.0.1 aplatie et déjà corrigée pour l’acquisition. Les nouveaux blocs ont leurs cadres, un chemin de puissance de gauche à droite, les condensateurs raccordés près des circuits et les réseaux de réglage regroupés. Le fichier PCB n’a pas été modifié. Cette révision constitue un schéma de prototype à router et à qualifier, pas une validation de fabrication.

## Architecture retenue

`RJ45 → F1 / TVS → MOSFET antipolarité → eFuse → buck-boost 5 V`

Le 5 V alimente le connecteur J2, l’anode commune des LED, le convertisseur numérique 3,3 V, l’ADP7104 d’acquisition et le nouveau LDO OLED 4,096 V.

| Fonction | Réalisation | Réglage / intérêt |
|---|---|---|
| Injection | J4 : 4 et 5 positifs ; 7 et 8 à GND | Injection passive 100BASE-TX, polarité imposée ; ce n’est pas une interface PoE IEEE |
| Protection | F1 conservé, D3 SMBJ13CA, Q4 AO3401A, D4 8,2 V | Le pont DF01S disparaît. Drain de Q4 côté câble, source côté charge ; protection de VGS |
| Courant et démarrage | U30 TPS259470ARPWR | R135=2,67 kΩ : environ 1,25 A ; DVDT=3,3 nF ; OVLO nominal 14,4 V ; UVLO nominal 3,552/3,226 V |
| Conversion principale | U1 TPS552892RYQR | 4,997 V par 100 kΩ / 31,6 kΩ ; 400 kHz, PWM forcé ; L1=4,7 µH XAL7070-472MEC |
| Numérique | U2 TPS62933FDRLR | 3,304 V par 31,3 kΩ / 10 kΩ ; 1,2 MHz, PWM forcé ; L8=2,2 µH XAL5030-222MEC |
| Acquisition | U7 ADP7104ARDZ-3.3 conservé | Un seul rail +3.3VACQ pour WHEC, VSP et logique associée ; 500 mA maximum pour l’ensemble |
| OLED | U22 TPS7A91DSKR | 4,096 V par 41,2 kΩ / 10 kΩ, résistances 0,1 % |
| LED | U23…U28, Q1…Q3, U29 | Trois boucles linéaires indépendantes, commandes timer existantes, environ 54,62 mA par couleur |

Le TPS552892 offre plus de marge en tension que le TPS63070 pour cette réalisation acceptant le 12 V. Cette marge concerne le convertisseur : **l’ensemble de la carte reste prévu pour une injection 5 V ou 12 V ±5 %**. Les protections d’entrée ne constituent pas une autorisation d’injecter 24 V ou 48 V. D3 a une tension de maintien de 13 V ; la coordination des transitoires doit être vérifiée avec le câble réel.

`AUXOFF` de U30 maintient l’entrée EN de U1 basse pendant la rampe d’entrée. Le pont R136/R137 donne un seuil de démarrage U1 nominal proche de 3,36 V après cette rampe, et un seuil d’arrêt proche de 3,22 V en tenant compte du courant d’hystérésis interne de 5 µA. L’eFuse bloque aussi le courant inverse ; le MOSFET placé en amont évite d’exposer l’eFuse à une inversion négative importante alors que ses condensateurs de sortie sont encore chargés. R136/R137=22 kΩ/12,7 kΩ limitent le déplacement du seuil dû à ce courant. R131/R132=19,6 kΩ/10 kΩ règlent l’UVLO de l’eFuse. D6 et D7, zeners 5,1 V, limitent la tension des nœuds EN lors des surtensions ; elles ne règlent pas les seuils UVLO. La limitation dans l’instrument ne remplace pas la protection du câble **au niveau de l’injecteur**.

## TPS65632 et OLED

Le nouveau domaine `+4V1_OLED` dessert **AVIN (16), PVIN (12), l’entrée de L2 et l’entrée de L3**, ainsi que leurs condensateurs existants. Le bus 5 V ne leur est plus relié. L4 conserve son raccordement à GND. Les sorties d’écran et les commandes de programmation existantes sont conservées.

La valeur nominale de 4,096 V laisse une marge sous la limite de fonctionnement de 4,5 V du TPS65632. Même une estimation statique conservatrice avec précision LDO ±1 % et résistances ±0,1 % reste sous environ 4,145 V. Cela ne remplace pas une mesure des dépassements au démarrage et lors des changements d’image. CIN et COUT du TPS7A91 doivent chacun dépasser **10 µF effectifs**, polarisation et température comprises ; les empreintes portent 47 µF pour fournir cette marge. À 500 mA, le LDO dissipe environ 0,45 W ; à 1 A, environ 0,90 W. Le courant total OLED et sa dissipation restent à mesurer.

Les noms historiques `+7.6V` et `-4.5V` sont conservés pour ne pas modifier implicitement la configuration de l’écran. Ils ne sont pas une preuve des tensions réellement programmées : SELP2 à GND correspond à la sélection 7,7 V ; vérifier également la consigne OUTN envoyée par le firmware.

## Courant LED et extinction

Les anciennes résistances de ballast R39/R42/R45 deviennent des résistances de mesure **4,99 Ω, 0,1 %, 0805** dans les sources des NMOS. Chaque OPA320 mesure la tension de source et ajuste la grille. Le TS5A3159 sélectionne la consigne ou zéro selon le timer RGB ; les trois signaux MCU sont conservés.

U29 fournit 1,25 V. R142/R143 donnent 0,273523 V. La résistance de 1 MΩ vers la référence sur chaque entrée inverseuse crée un biais d’extinction d’environ 1,25 mV, supérieur à l’offset attendu de l’amplificateur. Elle évite que la consigne zéro corresponde à un petit courant lumineux résiduel. Avec la résistance de retour de 1 kΩ :

`I_LED = [VSET × (1 + 1k/1M) − 1,25 × 1k/1M] / 4,99 = 54,619 mA`

Les résistances de grille sont de 100 Ω ; la compensation locale est de 1 nF C0G entre sortie de l’amplificateur et entrée inverseuse. Les grilles et entrées de commande ont leurs rappels à zéro. Les dissipations des résistances de mesure sont proches de 15 mW à ce courant.

La marge de régulation dépend de `5 V − Vf_LED − environ 0,273 V`. **Le Vf maximal du CIS et le temps d’établissement optique doivent être mesurés**, notamment à froid. La précision DC du courant n’est pas une garantie d’absence de dépassement transitoire. Vérifier les trois plateaux, l’extinction, les fronts et le courant crête inférieur à 60 mA avant de valider les temps d’exposition. La compensation de départ doit être adaptée au NMOS et au routage réels si nécessaire.

## Câble de 10 m et source USB

L’enveloppe utilisée pour le premier dimensionnement est **3 W sur le bus 5 V** avec une injection minimale de 4,75 V, un rendement supposé de 90 % et une résistance totale de boucle de 1,2 Ω :

- Tension d’entrée calculée du convertisseur : environ 3,66 V.
- Courant dans le câble : environ 0,912 A.
- Pertes de câble et protections comprises dans les 1,2 Ω : environ 1 W.

Cette enveloppe inclut les conducteurs en parallèle, les deux contacts, la PTC, le MOSFET et l’eFuse. Un câble fin de 10 m n’est donc pas validé par son seul marquage « Ethernet ». À 10 m, avec deux conducteurs identiques par polarité, l’AWG28 cuivre présente déjà environ 2,13 Ω à température ambiante, hors contacts : il ne permet pas cette enveloppe 3 W sous 5 V. L’AWG24 est beaucoup plus plausible ; une mesure de la résistance du câble fini tranche.

Il faut une source dont le courant **encore disponible après la consommation de l’interface USB/Ethernet** couvre le besoin. La valeur 1,5 A citée sur le schéma est une hypothèse de source appropriée à la limitation 1,25 A, pas une autorisation de prélever 1,5 A sur n’importe quel port USB. Un port limité à 500 mA peut imposer un mode de puissance réduit ou une autre alimentation. L’injection 12 V réduit fortement le courant de câble à puissance utile identique.

## Bruit, stabilité et acquisition

L’acquisition garde son rail commun et ses protections d’IO, ses pulls, son activation PG/RUN, les straps d’horloge, l’option LVDS et les points de mesure. Les seules modifications électriques de cette zone sont son entrée désormais à 5 V et la commande des LED. Les contrôles de population ont été mis à jour pour les nouvelles résistances de mesure.

Le 3,3 V numérique passe en buck pour diminuer les pertes et l’échauffement. Le rail d’acquisition conserve le LDO ; il faut vérifier le bilan thermique de U7 à 5 V, jusqu’à environ 0,85 W pour 500 mA. C143/C144 doivent toujours fournir au moins **125 µF effectifs cumulés, désormais sous 5 V**. La valeur imprimée de 100 µF sur une MLCC ne suffit pas à satisfaire cette exigence : vérifier les courbes de polarisation des références achetées, et agrandir les boîtiers ou augmenter le réservoir si nécessaire.

U1 reste en PWM forcé ; le strap R139 à GND désactive le dithering. Pour injecter une horloge externe sur BB_SYNC, retirer ce strap et respecter les niveaux/fréquences TI. La fréquence du buck numérique n’est pas synchronisée à celle de U1. Les battements résiduels et ceux de l’OLED doivent donc être recherchés dans les images ; le mode PWM évite principalement les paquets PFM variables.

La compensation U1 **10 kΩ / 100 nF / 100 pF** est une valeur de départ issue du modèle moyen TI, avec une capacité de bus effective de l’ordre de 150 à 450 µF. L’inductance minimale à 400 kHz est de 3 µH pour la boucle interne ; L1 reste à 3,76 µH avec sa tolérance −20 %. Le modèle résistif simplifié donne un ordre de grandeur de coupure de quelques kHz. Il ne représente ni l’impédance dynamique des régulateurs en aval, ni le câble, ni les limites de courant : **aucune simulation complète de stabilité ni mesure Bode n’a été effectuée**.

Au prototype : vérifier le démarrage à froid en 5 V avec le câble le plus résistif, les cycles arrêt/redémarrage, les appels LED/OLED, puis mesurer les marges de boucle U1 en buck, en boost et près de VIN=VOUT. Viser plus de 45° de marge de phase et 10 dB de gain. Vérifier aussi les transitions de limitation U30, pour détecter d’éventuels cycles de redémarrage.

Pour le PCB, conserver un plan GND continu, minimiser les boucles commutées et séparer physiquement les retours LED et numériques de la référence et des entrées analogiques. Raccorder les mesures LED en Kelvin. Comparer les trames noires et uniformes avec OLED éteint/allumé et différentes phases d’exposition. PG de U7 ne suffit pas, à lui seul, à garantir immédiatement la tension minimale WHEC : conserver une temporisation avant MCLK et la séquence d’initialisation VSP avant RUN_EN.

## Fichiers et contrôles

Les bibliothèques locales `Power_V5.kicad_sym` et `Power_V5.pretty` contiennent les nouveaux symboles et les trois empreintes TI absentes de la bibliothèque installée. Les broches ont été reprises des tableaux constructeurs ; les empreintes utilisent les land patterns RYQ0021A, RPW0010A et DSK0010A. Les ouvertures de pâte des formes composées et les vias thermiques devront être revus lors du travail PCB.

Le dossier `avant/` conserve les fichiers précédents et leurs empreintes SHA-256. Les exports finaux et les résultats de vérification accompagnent cette note : **951 contrôles alimentation/connectivité et 53 contrôles acquisition réussis**. Les 60 erreurs ERC identifiées avant intervention sont également présentes après intervention ; aucune nouvelle erreur ERC. Les vérifications portent sur les connexions et la population du schéma, pas sur le comportement électrique réel. L’ERC global reste affecté par les erreurs préexistantes du projet ; il ne faut pas confondre absence de nouvelle erreur avec un ERC global vierge.

## Sources constructeurs

- [TPS552892, brochage, boucle et application](https://www.ti.com/lit/ds/symlink/tps552892.pdf)
- [TPS25947, limitation, rampe, inversion et transitoires](https://www.ti.com/lit/ds/symlink/tps25947.pdf)
- [BZT52H, zeners de protection VGS et EN](https://assets.nexperia.com/documents/data-sheet/BZT52H_SER.pdf)
- [AO3401A, résistance à VGS=-2,5 V et limites](https://www.aosmd.com/sites/default/files/res/datasheets/AO3401A.pdf)
- [TPS62933, alimentation numérique](https://www.ti.com/lit/ds/symlink/tps62933.pdf)
- [TPS7A91, LDO OLED](https://www.ti.com/lit/ds/symlink/tps7a91.pdf)
- [TPS65632, domaine d’entrée OLED](https://www.ti.com/lit/ds/symlink/tps65632.pdf)
- [ADP7104, alimentation d’acquisition](https://www.analog.com/media/en/technical-documentation/data-sheets/ADP7104.pdf)
- [OPA320](https://www.ti.com/lit/ds/symlink/opa320.pdf), [TS5A3159](https://www.ti.com/lit/ds/symlink/ts5a3159.pdf), [REF33](https://www.ti.com/lit/ds/symlink/ref33.pdf), [DMN2056U](https://www.diodes.com/datasheet/download/DMN2056U.pdf)
- [Coilcraft XAL7070-472](https://www.coilcraft.com/en-us/products/power/shielded-inductors/molded-inductor/xal/xal7070/xal7070-472/), [XAL5030-222](https://www.coilcraft.com/en-us/products/power/shielded-inductors/molded-inductor/xal/xal50xx/xal5030-222/)
- WHEC LC3R216N-8008A : document local `RD/CIS/LC3R216N-8008A.pdf`.
