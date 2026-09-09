# Éclairage CIS : disposition et option DAC — 9 septembre 2026

## Modifications appliquées

Le canal bleu sauvegardé par l’utilisateur dans le schéma est le gabarit de référence, conforme à sa capture. Les canaux rouge et vert reprennent exactement ses placements relatifs, orientations, champs visibles, connexions et labels, par translations respectives de −373,38 et −186,69 mm. Les références, valeurs et affectations électriques propres à chaque couleur sont conservées.

La chaîne se lit commutateur → OPA320 → résistance de grille → NMOS, sur une même ligne. Le drain sort verticalement vers le CIS ; la résistance de mesure descend vers GND. Le feedback passe sous l’OPA320, avec la résistance de 1 kΩ à droite, la capacité de compensation verticale au nœud de sortie avant la résistance de grille, et la résistance de biais de 1 MΩ à gauche. Les capacités de découplage surplombent leurs circuits.

U28 emploie une modification locale du symbole (`lib_name TS5A3159DCKR_1`), distincte du seul identifiant `lib_id`. Les canaux rouge et vert utilisent maintenant cette même variante incorporée. Les broches 2 et 5 sont déplacées graphiquement mais gardent leurs numéros et types électriques. Le canal bleu, toutes les bibliothèques incorporées et les fichiers de bibliothèques sont conservés. Une mise à jour aveugle depuis une ancienne bibliothèque pourrait rétablir l’ancienne géométrie : conserver cette variante utilisateur lors d’une consolidation ultérieure.

Contrôles effectués :

- 392 composants physiques et leurs propriétés électriques conservés.
- 389 réseaux, noms et ensembles exacts de 1 460 terminaux identiques avant/après.
- 43 terminaux avec marqueur non-connecté identiques.
- 24 composants physiques repositionnés ; aucun objet hors des cellules rouge/verte modifié.
- Aucun nouveau label global ou hiérarchique ; une feuille A0 conservée.
- Exports XML, PDF et ERC avec KiCad CLI, inspection visuelle du résultat ; pas de test d’enregistrement dans l’éditeur interactif.
- Aucune nouvelle erreur ERC : 61 erreurs préexistantes conservées. Aucun nouvel avertissement d’une autre catégorie que les points hors grille. Les avertissements de points hors grille passent de 1 073 à 1 091 (+18), le motif utilisateur étant sur un pas de base 25 mil et le contrôle de connexions du projet réglé sur 50 mil. Aucune règle ERC n’a été assouplie.
- PCB, fichier de projet, firmware et configuration CubeMX non modifiés.

Les sauvegardes et preuves sont dans le dossier workspace `Disposition_LED_2026-09-09`, notamment `Canaux-LED.pdf` et `verification.json`.

## Option consigne fixe / DAC — proposée, non câblée

Le DAC ne remplace pas le régulateur de courant. Il peut remplacer sa consigne fixe ; les trois ensembles OPA320/NMOS/shunt et les commutateurs d’exposition restent utilisés.

Proposition de sélection au nœud LED_ISET :

- Entrée FIXE : sortie du pont R142/R143 alimenté par REF3312, environ 0,2735 V.
- Entrée DAC : sortie atténuée et filtrée d’un canal DAC, avec un plafond de courant dimensionné matériellement, tolérances de VREF+ et des résistances comprises.
- Commun : LED_ISET vers les entrées NO des trois TS5A3159. C165 peut servir au filtrage commun, à condition de recalculer la réponse et la charge de chaque source.
- Un sélecteur trois plots exclusif, ou deux straps 0 Ω mutuellement exclusifs, assure le choix. Jamais de liaison directe entre les deux sources.

Le REF3312 doit rester disponible en mode DAC pour le biais d’extinction via R146/R149/R152. Le DAC ne doit pas attaquer directement les LED ni recevoir directement 1 µF sur sa sortie. Le diviseur et le filtre doivent tenir compte de l’impédance du DAC ; la plage basse du buffer DAC, ses offsets et le comportement au reset devront être dimensionnés. Les timers restent responsables de l’exposition. Mettre à jour la consigne hors exposition et attendre l’établissement du filtre. Un DAC commun règle le courant de crête des trois couleurs ensemble ; les durées d’exposition restent indépendantes.

## Réaffectation proposée — non appliquée

Observation de la netlist courante :

| Broche | Bille STM32H747XIHx | État actuel | Proposition |
|---|---|---|---|
| PA4 | U3 | DCMI_HSYNC | DAC1_OUT1, mode analogique |
| PH8 | T13 | Non connectée, marqueur NC | DCMI_HSYNC, AF13 |
| PA5 | T3 | SPI1_SCK | Conserver |
| PB3 | C6 | SWO | Conserver |
| PG11 | B9 | ETH_TX_EN | Conserver |

PH8 fournit bien DCMI_HSYNC en AF13 selon le tableau des fonctions alternatives du STM32H747. Ce choix libère PA4 sans toucher à SPI1, SWO ou Ethernet. Il implique le déplacement réel du net HSYNC sur le schéma/PCB ; sélectionner une fonction alternative en firmware ne déplace pas un fil existant.

Le futur firmware V5 devra activer GPIOH et configurer PH8 en AF13 DCMI ; PA4 en mode analogique pour DAC1_OUT1, sans pull-up/pull-down. La configuration CubeMX devra refléter ce choix. L’affectation PH8 est libre dans le schéma examiné ; le routage PCB et le firmware V5 final ne sont pas qualifiés par cette étude.

Source primaire : [ST, STM32H747xI/G, DS12930, brochage, fonctions alternatives et DAC](https://www.st.com/resource/en/datasheet/stm32h747xi.pdf). Le sélecteur, les résistances DAC et la réaffectation restent des propositions, conformément à la portée annoncée pour cette intervention.
