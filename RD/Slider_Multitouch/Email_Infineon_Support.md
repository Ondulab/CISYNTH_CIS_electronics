# Support Technique Infineon - Procédure Officielle

**Date:** 09/12/2025  
**Dernière mise à jour:** 09/12/2025 18:19  
**Statut:** ⏳ EN ATTENTE DE SOUMISSION

---

## 🎯 PROCÉDURE OFFICIELLE INFINEON (RECOMMANDÉE)

### ✅ Canal Prioritaire: myCases Portal

**Infineon recommande officiellement d'utiliser le portail myCases pour le support technique.**

**Avantages:**
- ✅ Canal direct avec les ingénieurs applications Infineon
- ✅ Suivi de ticket avec numéro de référence
- ✅ Historique des échanges conservé
- ✅ Possibilité de joindre des fichiers (PDFs, schémas)
- ✅ Confidentialité assurée (pas public)
- ✅ Réponse généralement sous 2-5 jours ouvrés
- ✅ Meilleur pour demandes techniques complexes

---

## 📋 ÉTAPE 1: Inscription myInfineon (OBLIGATOIRE)

### 1.1 Créer un Compte myInfineon

**URL:** https://www.infineon.com/

**Procédure:**
1. Cliquer sur **"Register for myInfineon"** (coin supérieur droit)
2. Remplir le formulaire d'inscription:
   - ✅ **Utiliser votre email CORPORATE** (avantages supplémentaires)
   - Nom, prénom, société
   - Pays, téléphone
3. Accepter les conditions d'utilisation
4. Valider l'inscription
5. **Vérifier votre email** pour activer le compte
6. Se connecter avec vos identifiants

**⚠️ Important:** L'utilisation d'un email corporate (société) donne accès à des avantages supplémentaires et un support prioritaire.

### 1.2 Vérifier l'Accès au Portail

Une fois inscrit:
1. Cliquer sur **"Login to myInfineon"**
2. Entrer vos identifiants
3. Vérifier que vous avez accès au menu **"My Cases"**

---

## 📋 ÉTAPE 2: Créer un Case sur myCases Portal

### 2.1 Accéder au Portail

**URL directe:** https://mycases.infineon.com

**Ou via le site:**
1. Se connecter à myInfineon
2. Cliquer sur le lien **"My Cases"**
3. Vous serez redirigé vers le Customer Portal

### 2.2 Créer un Nouveau Case

**Dans le portail myCases:**

1. Cliquer sur **"Create New Case"** ou **"New Support Request"**

2. **Sélectionner la catégorie:**
   ```
   Product Family: Touch Sensing / Capacitive Touch
   Product Line: PSoC Automotive Multitouch
   Product: CYAT61658-56LWA41
   Application: Automotive
   ```

3. **Remplir les informations:**
   - **Subject:** Technical Support Request - 1D Slider Design with CYAT61658-56LWA41
   - **Priority:** Normal (ou High si urgent)
   - **Description:** Copier le message ci-dessous (section "Message pour myCases")

4. **Joindre les fichiers:**
   - [ ] PDF avec schémas système
   - [ ] PDF stack-up PCB 4 couches
   - [ ] Croquis slider avec dimensions
   - [ ] Diagramme environnement (châssis, carte mère)
   - [ ] Proposition technique (optionnel)

5. **Soumettre le case**

6. **Noter le numéro de case** (ex: CASE-12345) pour suivi

### 2.3 Timeline Attendue

```
Jour 0:  Soumission du case
Jour 1-2: Accusé de réception automatique
Jour 2-5: Première réponse d'un ingénieur Infineon
Jour 7:  Relance si pas de réponse
Jour 10: Escalade via hotline si nécessaire
```

---

## 📧 MESSAGE POUR myCases PORTAL

**Copier-coller ce message dans le champ "Description" du case:**

---

## 📧 Version Anglaise (RECOMMANDÉE)

```
Subject: Technical Support Request - 1D Slider Design with CYAT61658-56LWA41

Dear Infineon Automotive Touch Team,

I am an electronics engineer currently developing a 1D multitouch capacitive 
slider for an automotive application using your CYAT61658-56LWA41 controller.

Before finalizing the PCB design, I need your expertise to validate several 
critical technical choices.

═══════════════════════════════════════════════════════════════════════════
PROJECT SPECIFICATIONS
═══════════════════════════════════════════════════════════════════════════

• Application: Linear 1D multitouch slider
• Dimensions: 217mm (length) × 8mm (width)
• Detection: 8-10 simultaneous fingers
• Overlay: PET plastic 2mm thickness
• PCB: 4-layer FR4, 1.0mm total thickness
• Environment:
  - Temperature: -40°C to 85°C (Grade-A)
  - Aluminum chassis surrounding the slider
  - Motherboard 1mm below (potential EMI source)

═══════════════════════════════════════════════════════════════════════════
CRITICAL QUESTIONS - SENSOR PATTERN
═══════════════════════════════════════════════════════════════════════════

Q1. Which electrode pattern do you recommend for a 1D slider of this geometry?
    Options considered:
    □ Manhattan-3 (MH3)
    □ Dual-Solid Diamond (DSD)
    □ Single-Solid Diamond (SSD)
    □ Linear pattern specific for sliders?
    □ Other pattern optimized for narrow width (8mm)?

Q2. For a 1D slider, how many TX electrodes are recommended?
    □ Single continuous TX?
    □ 2 parallel TX (as in my current calculations)?
    □ 3 TX (CYAT61658 maximum)?
    
Q3. Optimal RX configuration:
    • Recommended number of RX electrodes for 217mm?
      (My current calculation: 41 RX)
    • Recommended RX pitch? (My current calculation: 5.0mm)
    • Optimal RX width? (My current calculation: 4.0mm)

Q4. With a 2mm overlay, which pattern ensures the best SNR?
    • Acceptable signal disparity?
    • Need for firmware compensation?

═══════════════════════════════════════════════════════════════════════════
CRITICAL QUESTIONS - 4-LAYER PCB
═══════════════════════════════════════════════════════════════════════════

Q5. Is my 4-layer stack-up optimal for this use case?
    
    Layer 1 (Top):     TX electrodes + 50% hatched GND fill
    Prepreg:           0.2mm
    Layer 2 (Inner 1): RX electrodes + 50% hatched GND fill
    Core:              0.4mm FR4
    Layer 3 (Inner 2): 60-70% hatched GND plane (EMI shielding)
    Prepreg:           0.2mm
    Layer 4 (Bottom):  Continuous GND plane + components
    Total:             ~1.0mm
    
    Specific points:
    • Via stitching Layer 3 ↔ Layer 4: maximum recommended spacing?
      (My current calculation: 7mm × 7mm)
    • Optimal GND fill percentage on Layer 3 for EMI shielding?
    • Does this configuration provide sufficient protection against EMI 
      from motherboard located 1mm below the PCB?

Q6. Recommended clearance between active electrodes and aluminum chassis?
    (My current estimate: 2-3mm)

═══════════════════════════════════════════════════════════════════════════
QUESTIONS - DOCUMENTATION & SUPPORT
═══════════════════════════════════════════════════════════════════════════

Q7. Do you have reference designs or examples of 1D sliders?
    • PCB files (KiCad/Altium) available under NDA?
    • DXF templates for electrodes?
    • Validated reference Gerbers?

Q8. Available documentation:
    □ Design guidelines specific to sliders (vs touchscreens)?
    □ Application notes for 4-layer rigid PCB?
    □ TX/RX electrode routing guide?
    □ EMI/EMC recommendations for automotive environment?

Q9. Tools and support:
    • Touch Tuning Host Emulator (TTHE): download link?
    • Firmware SDK: access procedure?
    • Possibility of design review before manufacturing?
    • Technical support during tuning phase?

Q10. Samples:
    • Possibility to obtain CYAT61658-56LWA41 samples?
    • Quantity and delivery time?

═══════════════════════════════════════════════════════════════════════════
QUESTIONS - TECHNICAL SPECIFICATIONS
═══════════════════════════════════════════════════════════════════════════

Q11. Optimal configuration for 8-10 finger multitouch:
    • Recommended refresh rate?
    • Optimal number of TX pulses?
    • Maximum TX frequency to minimize EMI?

Q12. TX Pump:
    • Do you recommend enabling the TX pump for 2mm overlay?
    • VCCTX configuration with 3.3V VDDA?

Q13. Overlay validation:
    • Recommended overlay materials (PET, PC, glass)?
    • Maximum supported thickness with recommended pattern?
    • Impact of dielectric constant (εr) on performance?

═══════════════════════════════════════════════════════════════════════════
ADDITIONAL INFORMATION
═══════════════════════════════════════════════════════════════════════════

Documents I have already reviewed:
✓ CYAT6165X Datasheet (002-19012 Rev. *J)
✓ Module Design Best Practices (001-50467) - partially

I am ready to sign an NDA if necessary to access additional documents and 
reference designs.

Project timeline:
• PCB Design: January-February 2025
• Prototype 1: March 2025
• Validation: April-May 2025

R&D budget allocated for prototypes and testing.

═══════════════════════════════════════════════════════════════════════════

I remain at your disposal for any additional information or clarification 
about the project.

Looking forward to your response,

Best regards,

[YOUR NAME]
[YOUR COMPANY]
[YOUR EMAIL]
[YOUR PHONE]
```

---

## 📧 Version Française

```
Objet: Demande de Support Technique - Design Slider 1D avec CYAT61658-56LWA41

Bonjour,

Je suis ingénieur électronique et je développe actuellement un slider capacitif 1D 
multitouch pour une application automobile, utilisant votre contrôleur 
CYAT61658-56LWA41.

Avant de finaliser le design PCB, j'aurais besoin de votre expertise pour valider 
certains choix techniques critiques.

═══════════════════════════════════════════════════════════════════════════
SPÉCIFICATIONS DU PROJET
═══════════════════════════════════════════════════════════════════════════

• Application: Slider linéaire 1D multitouch
• Dimensions: 217mm (longueur) × 8mm (largeur)
• Détection: 8-10 doigts simultanés
• Overlay: Plastique PET 2mm d'épaisseur
• PCB: 4 couches FR4, 1.0mm
• Environnement:
  - Température: -40°C à 85°C (Grade-A)
  - Châssis aluminium entourant le slider
  - Carte mère à 1mm en-dessous (source EMI potentielle)

═══════════════════════════════════════════════════════════════════════════
QUESTIONS CRITIQUES - PATTERN CAPTEUR
═══════════════════════════════════════════════════════════════════════════

Q1. Quel pattern d'électrodes recommandez-vous pour un slider 1D de cette géométrie?
    Options envisagées:
    □ Manhattan-3 (MH3)
    □ Dual-Solid Diamond (DSD)
    □ Single-Solid Diamond (SSD)
    □ Pattern linéaire spécifique pour sliders?
    □ Autre pattern optimisé pour largeur réduite (8mm)?

Q2. Pour un slider 1D, combien d'électrodes TX sont recommandées?
    □ 1 TX unique continue?
    □ 2 TX parallèles (comme dans mes calculs actuels)?
    □ 3 TX maximum du CYAT61658?
    
Q3. Configuration RX optimale:
    • Nombre d'électrodes RX recommandé pour 217mm?
      (Mon calcul actuel: 41 RX)
    • Pitch RX recommandé? (Mon calcul actuel: 5.0mm)
    • Largeur RX optimale? (Mon calcul actuel: 4.0mm)

Q4. Avec un overlay de 2mm, quel pattern assure le meilleur SNR?
    • Signal disparity acceptable?
    • Nécessité de compensation firmware?

═══════════════════════════════════════════════════════════════════════════
QUESTIONS CRITIQUES - PCB 4 COUCHES
═══════════════════════════════════════════════════════════════════════════

Q5. Mon stack-up 4 couches est-il optimal pour ce cas d'usage?
    
    Layer 1 (Top):     TX électrodes + GND fill hachuré 50%
    Prepreg:           0.2mm
    Layer 2 (Inner 1): RX électrodes + GND fill hachuré 50%
    Core:              0.4mm FR4
    Layer 3 (Inner 2): Plan GND hachuré 60-70% (shielding EMI)
    Prepreg:           0.2mm
    Layer 4 (Bottom):  Plan GND continu + composants
    Total:             ~1.0mm
    
    Points spécifiques:
    • Via stitching Layer 3 ↔ Layer 4: espacement maximum recommandé?
      (Mon calcul actuel: 7mm × 7mm)
    • Pourcentage de GND fill sur Layer 3 optimal pour shielding EMI?
    • Cette configuration protège-t-elle suffisamment contre EMI de la 
      carte mère située à 1mm sous le PCB?

Q6. Clearance recommandée entre électrodes actives et châssis aluminium?
    (Mon estimation actuelle: 2-3mm)

═══════════════════════════════════════════════════════════════════════════
QUESTIONS - DOCUMENTATION & SUPPORT
═══════════════════════════════════════════════════════════════════════════

Q7. Disposez-vous de reference designs ou exemples de sliders 1D?
    • Fichiers PCB (KiCad/Altium) disponibles sous NDA?
    • Templates DXF pour électrodes?
    • Gerbers de référence validés?

Q8. Documentation disponible:
    □ Design guidelines spécifiques aux sliders (vs touchscreens)?
    □ Application notes pour PCB rigide 4 couches?
    □ Guide de routage électrodes TX/RX?
    □ Recommandations EMI/EMC pour environnement automotive?

Q9. Outils et support:
    • Touch Tuning Host Emulator (TTHE): lien de téléchargement?
    • Firmware SDK: procédure d'accès?
    • Possibilité d'une revue de design avant fabrication?
    • Support technique durant la phase de tuning?

Q10. Samples:
    • Possibilité d'obtenir des échantillons CYAT61658-56LWA41?
    • Quantité et délai de livraison?

═══════════════════════════════════════════════════════════════════════════
QUESTIONS - SPÉCIFICATIONS TECHNIQUES
═══════════════════════════════════════════════════════════════════════════

Q11. Configuration optimale pour multitouch 8-10 doigts:
    • Refresh rate recommandé?
    • Nombre de TX pulses optimal?
    • Fréquence TX maximale pour minimiser EMI?

Q12. TX Pump:
    • Recommandez-vous d'activer le TX pump pour overlay 2mm?
    • VCCTX configuration avec 3.3V VDDA?

Q13. Validation overlay:
    • Matériaux overlay recommandés (PET, PC, verre)?
    • Épaisseur maximale supportée avec pattern recommandé?
    • Impact de la constante diélectrique (εr) sur les performances?

═══════════════════════════════════════════════════════════════════════════
INFORMATIONS COMPLÉMENTAIRES
═══════════════════════════════════════════════════════════════════════════

Documents que j'ai déjà consultés:
✓ Datasheet CYAT6165X (002-19012 Rev. *J)
✓ Module Design Best Practices (001-50467) - partiellement

Je suis prêt à signer un NDA si nécessaire pour accéder aux documents et 
reference designs supplémentaires.

Planning projet:
• Design PCB: Janvier-Février 2025
• Prototype 1: Mars 2025
• Validation: Avril-Mai 2025

Budget R&D alloué pour prototypes et tests.

═══════════════════════════════════════════════════════════════════════════

Je reste à votre disposition pour toute information complémentaire ou 
clarification sur le projet.

Dans l'attente de votre retour,

Cordialement,

[VOTRE NOM]
[VOTRE SOCIÉTÉ]
[VOTRE EMAIL]
[VOTRE TÉLÉPHONE]
```

---

## 📋 CANAUX ALTERNATIFS (Si problème avec myCases)

### Option 2: Infineon Developer Community (Forum Public)

**URL:** https://community.infineon.com/

**Quand l'utiliser:**
- Questions générales sur les produits
- Partage d'expérience avec la communauté
- Recherche de solutions déjà documentées
- Complément au case myCases

**⚠️ Attention:** 
- Public (visible par tous)
- Moins adapté pour détails techniques confidentiels
- Peut référencer votre case number pour suivi détaillé

### Option 3: Email Direct (Dernier Recours)

**Email principal:**
```
automotive@infineon.com
```

**Quand l'utiliser:**
- Problème d'accès à myCases
- Urgence absolue
- Complément à un case existant

**⚠️ Moins recommandé:** Pas de suivi structuré, pas de numéro de case

## 📎 PIÈCES JOINTES À PRÉPARER

### Fichiers à Créer AVANT de Soumettre le Case

**PDF 1: Schémas Système (obligatoire)**
```
Contenu:
- Schéma bloc du système complet
- Diagramme environnement (châssis alu, carte mère, distances)
- Croquis slider avec dimensions annotées (217mm × 8mm)
- Positionnement relatif des composants
```

**PDF 2: Stack-up PCB (obligatoire)**
```
Contenu:
- Configuration 4 couches détaillée
- Épaisseurs de chaque layer
- Matériaux (FR4, prepreg)
- Via stitching pattern
- Copie du diagramme de la proposition technique
```

**PDF 3: Application Finale (recommandé)**
```
Contenu:
- Photo ou rendu 3D de l'application
- Contexte d'utilisation
- Contraintes mécaniques
- Environnement EMI
```

**PDF 4: Proposition Technique (optionnel)**
```
Contenu:
- Votre document Proposition_Technique_CYAT61658.md en PDF
- Calculs et justifications
- Analyse de risques
```

### Checklist Avant Soumission

- [ ] Compte myInfineon créé et validé
- [ ] Email corporate utilisé pour l'inscription
- [ ] Accès au portail myCases vérifié
- [ ] PDF schémas système créé
- [ ] PDF stack-up PCB créé
- [ ] PDF application finale créé (optionnel)
- [ ] Message copié et adapté avec vos coordonnées
- [ ] Toutes les informations [YOUR NAME], [YOUR COMPANY] complétées

## 🔄 SUIVI DU CASE

### Après Soumission

**Vous recevrez:**
1. Email de confirmation avec numéro de case
2. Lien pour suivre l'évolution du case
3. Notifications par email à chaque mise à jour

**Suivi actif:**
- Connectez-vous régulièrement à myCases pour vérifier les réponses
- Répondez rapidement aux questions des ingénieurs
- Fournissez les informations complémentaires demandées

### Timeline de Relance

```
Jour 0:  ✅ Case soumis sur myCases
Jour 2:  ⏳ Attente première réponse
Jour 5:  ⏳ Attente réponse détaillée
Jour 7:  ⚠️ Relance via le case si pas de réponse
Jour 10: 🔴 Escalade via hotline: https://www.infineon.com/support/service-center
Jour 15: 🔴 Contact commercial Infineon local
```

### Contacts Escalade

**Si pas de réponse après 10 jours:**

1. **Hotline Support Center**
   - URL: https://www.infineon.com/support/service-center
   - Mentionner votre case number
   - Demander escalade

2. **Forum Community** (parallèle)
   - URL: https://community.infineon.com/
   - Poster question publique
   - Référencer le case number

3. **Distributeur Infineon**
   - Digikey: https://www.digikey.com/
   - Mouser: https://www.mouser.com/
   - Demander contact ingénieur applications

4. **Commercial Infineon Local**
   - Rechercher bureau Infineon dans votre pays
   - Contact via LinkedIn: "Infineon Touch Sensing"

---

## 🎯 Après Réception de la Réponse

### Scénario A: Réponse Positive avec Reference Design
```
✅ Télécharger tous les documents
✅ Signer NDA si nécessaire
✅ Étudier le reference design
✅ Adapter à vos dimensions
✅ Demander design review
```

### Scénario B: Recommandations sans Reference Design
```
✅ Noter toutes les recommandations
✅ Réviser votre design en conséquence
✅ Créer nouveau prototype basé sur leurs specs
✅ Demander validation avant fabrication
```

### Scénario C: Pattern Différent Recommandé
```
⚠️ STOP le design actuel
✅ Comprendre le nouveau pattern
✅ Refaire les calculs
✅ Régénérer les footprints/zones
✅ Revalider le budget et planning
```

### Scénario D: Pas de Réponse ou Réponse Négative
```
Plan B:
1. Contacter distributeur Infineon
2. Chercher intégrateur système partenaire Infineon
3. Envisager prototype simplifié 2 couches
4. Considérer alternative: Microchip, Azoteq, etc.
```

---

## ⚠️ Points Critiques à Clarifier

**AVANT de continuer le design, vous DEVEZ obtenir:**

1. ✅ **Pattern validé** pour slider 1D 8mm de large
2. ✅ **Nombre de TX** optimal (1, 2 ou 3?)
3. ✅ **Pitch RX** recommandé
4. ✅ **Via stitching** espacement max pour EMI
5. ✅ **Reference design** si disponible

**Sans ces informations, le risque d'échec est ÉLEVÉ!**

---

## 📝 Notes

- **Langue:** Anglais recommandé (équipe internationale)
- **Ton:** Professionnel mais direct
- **Détails:** Suffisamment précis pour montrer votre sérieux
- **NDA:** Mentionner votre disponibilité à signer
- **Budget:** Mentionner que vous avez un budget R&D
- **Volume:** Si production série prévue, le mentionner

---

**Date de création:** 09/12/2025  
**Dernière mise à jour:** 09/12/2025  
**Statut:** ⏳ EN ATTENTE D'ENVOI
