# Placement issu des scans — variante NON VALIDÉE

Cette variante reporte les positions calculées depuis les longueurs développées des nappes, dans une hypothèse de PCB relevé de 1,6 mm et d'encoche déplacée/élargie. **Elle présente des interférences mécaniques et des chevauchements de plages J2/J4 ; elle n'est pas une implantation finalisée.**

Centres en coordonnées locales de la pièce PCB FreeCAD :

- J1 Display : (37,0876 ; 11,5700) mm, 0° ;
- J2 Touch : (18,4621 ; 9,4755) mm, 270°.

Les empreintes sont sur F.Cu. Les nets et identifiants proviennent du schéma V4 courant. Les modèles d'embase de l'étude précédente restent des enveloppes et l'empreinte tactile est toujours un MOCKUP. Les offsets sont nominaux, avec une incertitude de relevé estimée à ±0,5 mm sur les centres.

DRC : 47 violations dont 12 `shorting_items`, 12 `solder_mask_bridge`, 4 `clearance` et un recouvrement de courtyards. Il faut résoudre le montage des nappes et l'interférence avec les queues de soudure du RJ45 avant de retenir une implantation. Le fichier `../CIS_Integration_V4.kicad_pcb` n'est pas modifié.

Voir le [relevé et les hypothèses mécaniques](../../../../Meca/Sp3ctra_CIS_mechanics_v4/Integration_V4/RELEVE_SCANS.md) et le fichier `TouchBar_Scans_Proposition.FCStd` associé.
