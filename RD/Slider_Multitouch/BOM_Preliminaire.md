# BOM Préliminaire - Slider Multitouch CYAT61658

**Date:** 09/12/2025  
**Version:** 1.0  
**Projet:** Slider 1D Multitouch 217mm × 8mm

---

## 🔌 Composants Principaux

### 1. Contrôleur Touch

| Référence | Description | Quantité | Fabricant | Part Number | Prix Unit. | Total | Distributeur |
|-----------|-------------|----------|-----------|-------------|------------|-------|--------------|
| U1 | Touch Controller 56-pin QFN | 1 | Infineon | CYAT61658-56LWA41 | 25€ | 25€ | Infineon/Digikey |

**Notes:**
- Demander samples gratuits à Infineon (automotive@infineon.com)
- Grade-A: -40°C à 85°C
- Package: 56-lead QFN wettable flank (8×8×1mm)

---

## ⚡ Alimentation et Découplage

### 2. Résistances Série Alimentation

| Référence | Description | Valeur | Tolérance | Puissance | Quantité | Part Number | Prix Unit. | Total |
|-----------|-------------|--------|-----------|-----------|----------|-------------|------------|-------|
| R1 | Résistance série VDDA | 1.0Ω | 5% | 1/4W | 1 | RC0805FR-071RL | 0.10€ | 0.10€ |
| R2 | Résistance série VDDA_Q | 1.0Ω | 5% | 1/4W | 1 | RC0805FR-071RL | 0.10€ | 0.10€ |

**Distributeur:** Digikey, Mouser  
**Package:** 0805 (2012 metric)

### 3. Condensateurs Découplage

| Référence | Description | Valeur | Tension | Diélectrique | Quantité | Part Number | Prix Unit. | Total |
|-----------|-------------|--------|---------|--------------|----------|-------------|------------|-------|
| C1 | Découplage VDDA | 0.1µF | 16V | X7R | 1 | CL21B104KBCNNNC | 0.10€ | 0.10€ |
| C2 | Découplage VDDA | 1.0µF | 16V | X5R | 1 | CL21B105KAFNNNE | 0.15€ | 0.15€ |
| C3 | Bulk VDDA | 2.2µF | 16V | X5R | 1 | CL21B225KAFNNNE | 0.20€ | 0.20€ |
| C4 | Découplage VDDA_Q | 0.1µF | 16V | X7R | 1 | CL21B104KBCNNNC | 0.10€ | 0.10€ |
| C5 | Découplage VDDA_Q | 1.0µF | 16V | X5R | 1 | CL21B105KAFNNNE | 0.15€ | 0.15€ |
| C6 | Bulk VDDA_Q | 2.2µF | 16V | X5R | 1 | CL21B225KAFNNNE | 0.20€ | 0.20€ |
| C7 | Découplage VDDD | 0.1µF | 16V | X7R | 1 | CL21B104KBCNNNC | 0.10€ | 0.10€ |
| C8 | Bulk VDDD | 4.7µF | 16V | X5R | 1 | CL21B475KAFNNNE | 0.25€ | 0.25€ |
| C9 | Découplage VCCD | 0.1µF | 16V | X7R | 1 | CL21B104KBCNNNC | 0.10€ | 0.10€ |
| C10 | TX Pump VCCTX | 0.22µF | 16V | X7R | 1 | CL21B224KAFNNNE | 0.15€ | 0.15€ |

**Fabricant:** Samsung (CL series) ou équivalent Murata, TDK  
**Distributeur:** Digikey, Mouser  
**Package:** 0805 (2012 metric)  
**Note:** Vérifier voltage coefficient à la tension d'utilisation

---

## 🔄 Communication I²C

### 4. Résistances Pull-up I²C

| Référence | Description | Valeur | Tolérance | Puissance | Quantité | Part Number | Prix Unit. | Total |
|-----------|-------------|--------|-----------|-----------|----------|-------------|------------|-------|
| R3 | Pull-up SDA | 2.2kΩ | 1% | 1/8W | 1 | RC0805FR-072K2L | 0.10€ | 0.10€ |
| R4 | Pull-up SCL | 2.2kΩ | 1% | 1/8W | 1 | RC0805FR-072K2L | 0.10€ | 0.10€ |

**Note:** Vérifier si pull-ups déjà présents sur carte mère  
**Package:** 0805 (2012 metric)

---

## 🔌 Reset et Debug

### 5. Résistance Pull-up XRES

| Référence | Description | Valeur | Tolérance | Puissance | Quantité | Part Number | Prix Unit. | Total |
|-----------|-------------|--------|-----------|-----------|----------|-------------|------------|-------|
| R5 | Pull-up XRES | 10kΩ | 5% | 1/8W | 1 | RC0805FR-0710KL | 0.10€ | 0.10€ |

**Package:** 0805 (2012 metric)

### 6. Bouton Reset (Optionnel)

| Référence | Description | Type | Quantité | Part Number | Prix Unit. | Total |
|-----------|-------------|------|----------|-------------|------------|-------|
| SW1 | Bouton tactile reset | SPST NO | 1 | PTS645SM43SMTR92 | 0.50€ | 0.50€ |

**Fabricant:** C&K  
**Package:** SMD tactile switch

---

## 🔗 Connecteurs

### 7. Connecteur Alimentation

| Référence | Description | Pins | Pitch | Quantité | Part Number | Prix Unit. | Total |
|-----------|-------------|------|-------|----------|-------------|------------|-------|
| J1 | Connecteur alimentation | 2 | 2.54mm | 1 | 22-28-4020 | 0.50€ | 0.50€ |

**Type:** Header 1×2 ou JST  
**Tension:** 3.3V ou 5V

### 8. Connecteur I²C/SPI

| Référence | Description | Pins | Pitch | Quantité | Part Number | Prix Unit. | Total |
|-----------|-------------|------|-------|----------|-------------|------------|-------|
| J2 | Connecteur communication | 6 | 2.54mm | 1 | 22-28-4060 | 0.80€ | 0.80€ |

**Pins:** GND, VCC, SDA/MOSI, SCL/SCLK, INT, MISO/SS  
**Alternative:** Connecteur JST-SH 1mm pitch

### 9. Connecteur Debug SWD (Optionnel)

| Référence | Description | Pins | Pitch | Quantité | Part Number | Prix Unit. | Total |
|-----------|-------------|------|-------|----------|-------------|------------|-------|
| J3 | Connecteur SWD | 4 | 2.54mm | 1 | 22-28-4040 | 0.60€ | 0.60€ |

**Pins:** GND, VCC, SWDCLK, SWDIO  
**Alternative:** Tag-Connect TC2030

---

## 🛡️ Protection et Shielding

### 10. Composants Protection (Optionnel)

| Référence | Description | Type | Quantité | Part Number | Prix Unit. | Total |
|-----------|-------------|------|----------|-------------|------------|-------|
| D1 | Diode protection alimentation | Schottky | 1 | BAT54C | 0.20€ | 0.20€ |
| TVS1 | Protection ESD I²C | TVS Array | 1 | PRTR5V0U2X | 0.30€ | 0.30€ |

**Note:** Évaluer nécessité selon environnement

---

## 📋 PCB et Mécanique

### 11. PCB

| Description | Spécification | Quantité | Prix Unit. | Total |
|-------------|---------------|----------|------------|-------|
| PCB 2 couches | 217mm × 8mm, FR4 0.8-1.0mm, ENIG | 5 | 50€ | 250€ |

**Fabricant:** JLCPCB, PCBWay, Eurocircuits  
**Délai:** 10-15 jours  
**Finition:** ENIG (or) pour durabilité

### 12. Overlay Plastique

| Description | Matériau | Épaisseur | Quantité | Prix Unit. | Total |
|-------------|----------|-----------|----------|------------|-------|
| Overlay transparent | PET ou PC | 2mm ± 0.2mm | 5 | 30€ | 150€ |

**Dimensions:** 217mm × 8mm  
**Traitement:** Anti-rayures recommandé  
**Découpe:** Laser ou CNC

### 13. Adhésif Double-Face

| Description | Type | Quantité | Prix Unit. | Total |
|-------------|------|----------|------------|-------|
| Adhésif PCB/Overlay | 3M 468MP ou équivalent | 1 rouleau | 15€ | 15€ |

**Épaisseur:** 0.13mm  
**Température:** -40°C à 150°C

---

## 🔧 Assemblage

### 14. Stencil Soudure

| Description | Type | Quantité | Prix Unit. | Total |
|-------------|------|----------|------------|-------|
| Stencil PCB | Acier inox, épaisseur 0.12mm | 1 | 25€ | 25€ |

**Note:** Nécessaire pour assemblage manuel ou semi-automatique

### 15. Pâte à Souder

| Description | Type | Quantité | Prix Unit. | Total |
|-------------|------|----------|------------|-------|
| Pâte à souder | SAC305 (sans plomb) | 1 seringue | 20€ | 20€ |

**Température fusion:** 217-220°C  
**Stockage:** Réfrigérateur (2-8°C)

---

## 💰 Résumé des Coûts

### Par PCB (Prototype)

| Catégorie | Coût |
|-----------|------|
| **Composants électroniques** | ~30€ |
| **PCB (unitaire)** | 50€ |
| **Overlay plastique** | 30€ |
| **Adhésif et divers** | 5€ |
| **Assemblage (si prestataire)** | 60€ |
| **TOTAL par unité** | **~175€** |

### Lot de 5 PCB (Prototype)

| Catégorie | Coût Total |
|-----------|------------|
| **Composants électroniques** | 150€ |
| **PCB (5 pcs)** | 250€ |
| **Overlay plastique (5 pcs)** | 150€ |
| **Adhésif et consommables** | 75€ |
| **Stencil et outils** | 45€ |
| **Assemblage (5 pcs)** | 300€ |
| **Frais de port** | 30€ |
| **TOTAL 5 prototypes** | **~1000€** |

---

## 📦 Commandes Recommandées

### Priorité 1 - Longue Lead Time

1. **CYAT61658-56LWA41** (Infineon)
   - Demander samples ou commander via Digikey
   - Lead time: 4-8 semaines si pas en stock

2. **PCB Fabrication**
   - Commander dès validation du design
   - Lead time: 10-15 jours

### Priorité 2 - Standard

3. **Composants passifs** (Digikey/Mouser)
   - Commander en kit complet
   - Lead time: 2-5 jours

4. **Overlay plastique**
   - Commander après validation dimensions finales
   - Lead time: 1-2 semaines (découpe sur mesure)

### Priorité 3 - Optionnel

5. **Connecteurs et accessoires**
   - Commander selon besoins spécifiques
   - Lead time: 2-5 jours

---

## 📝 Notes d'Approvisionnement

### Alternatives Composants

**Condensateurs:**
- Samsung CL series (recommandé, bon rapport qualité/prix)
- Murata GRM series (premium, meilleure stabilité)
- TDK C series (alternative fiable)

**Résistances:**
- Yageo RC series (standard)
- Vishay CRCW series (alternative)
- Panasonic ERJ series (haute précision)

### Quantités Recommandées

Pour 5 prototypes, commander:
- **Composants passifs:** +50% (pertes assemblage)
- **Contrôleur:** +1 unité (backup)
- **PCB:** 5 pcs (minimum fabricant)
- **Overlay:** 5-10 pcs (tests mécaniques)

### Stockage

- **Composants SMD:** Dry cabinet ou sachets anti-humidité
- **Pâte à souder:** Réfrigérateur 2-8°C
- **PCB:** Emballage anti-statique
- **Overlay plastique:** Protéger des rayures

---

## 🔄 Mise à Jour BOM

| Version | Date | Modifications |
|---------|------|---------------|
| 1.0 | 09/12/2025 | Création initiale |

**Prochaine révision:** Après validation design schematic

---

## 📞 Contacts Fournisseurs

### Distributeurs Électronique
- **Digikey:** www.digikey.fr | +33 (0)1 76 54 00 00
- **Mouser:** www.mouser.fr | +33 (0)1 30 15 80 10
- **Farnell:** fr.farnell.com | +33 (0)1 47 30 00 00

### Fabricants PCB
- **JLCPCB:** jlcpcb.com | support@jlcpcb.com
- **PCBWay:** www.pcbway.com | support@pcbway.com
- **Eurocircuits:** www.eurocircuits.com

### Infineon
- **Email:** automotive@infineon.com
- **Samples:** Demander via formulaire en ligne

---

**Note:** Prix indicatifs basés sur quantités prototype. Prix unitaires dégressifs en production.
