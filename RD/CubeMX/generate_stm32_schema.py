#!/usr/bin/env python3
"""
Générateur de schéma KiCad pour STM32H747XIHx
Génère automatiquement un schéma avec toutes les étiquettes de pins configurées
"""

import uuid

# Configuration des pins du STM32H747XIHx depuis CubeMX
# Format: (Pin_Number, Pin_Name, Function, Label)
PIN_CONFIG = [
    ("R13", "PH9", "DCMI_D0", ""),
    ("D14", "PA10", "DCMI_D1", ""),
    ("A9", "PG10", "DCMI_D2", ""),
    ("E14", "PC9", "DCMI_D3", ""),
    ("B13", "PC11", "DCMI_D4", ""),
    ("A4", "PI4", "DCMI_D5", ""),
    ("A2", "PI6", "DCMI_D6", ""),
    ("B3", "PI7", "DCMI_D7", ""),
    ("U3", "PA4", "DCMI_HSYNC", ""),
    ("R3", "PA6", "DCMI_PIXCLK", ""),
    ("A3", "PI5", "DCMI_VSYNC", ""),
    ("B14", "PA14 (JTCK/SWCLK)", "DEBUG_JTCK-SWCLK", ""),
    ("C15", "PA13 (JTMS/SWDIO)", "DEBUG_JTMS-SWDIO", ""),
    ("L16", "DSI_CKP", "DSIHOST_CKP", ""),
    ("L17", "DSI_CKN", "DSIHOST_CKN", ""),
    ("M16", "DSI_D0P", "DSIHOST_D0P", ""),
    ("M17", "DSI_D0N", "DSIHOST_D0N", ""),
    ("K16", "DSI_D1P", "DSIHOST_D1P", ""),
    ("K17", "DSI_D1N", "DSIHOST_D1N", ""),
    ("R5", "PA7", "ETH_CRS_DV", ""),
    ("M2", "PC1", "ETH_MDC", ""),
    ("N3", "PA2", "ETH_MDIO", ""),
    ("N4", "PA1", "ETH_REF_CLK", ""),
    ("T4", "PC4", "ETH_RXD0", ""),
    ("U4", "PC5", "ETH_RXD1", ""),
    ("D9", "PG13", "ETH_TXD0", ""),
    ("D8", "PG14", "ETH_TXD1", ""),
    ("B9", "PG11", "ETH_TX_EN", ""),
    ("M4", "PC3", "FMC_SDCKE0", ""),
    ("M3", "PC2", "FMC_SDNE0", ""),
    ("H14", "PG4", "FMC_BA0", ""),
    ("G14", "PG5", "FMC_BA1", ""),
    ("G4", "PF0", "FMC_A0", ""),
    ("G3", "PF1", "FMC_A1", ""),
    ("G1", "PF2", "FMC_A2", ""),
    ("H4", "PF3", "FMC_A3", ""),
    ("J5", "PF4", "FMC_A4", ""),
    ("J4", "PF5", "FMC_A5", ""),
    ("R7", "PF12", "FMC_A6", ""),
    ("P7", "PF13", "FMC_A7", ""),
    ("P8", "PF14", "FMC_A8", ""),
    ("R9", "PF15", "FMC_A9", ""),
    ("T8", "PG0", "FMC_A10", ""),
    ("U8", "PG1", "FMC_A11", ""),
    ("F15", "PG8", "FMC_SDCLK", ""),
    ("D6", "PG15", "FMC_SDNCAS", ""),
    ("T7", "PF11", "FMC_SDNRAS", ""),
    ("L2", "PC0", "FMC_SDNWE", ""),
    ("P16", "PD14", "FMC_D0", ""),
    ("P15", "PD15", "FMC_D1", ""),
    ("D13", "PD0", "FMC_D2", ""),
    ("E12", "PD1", "FMC_D3", ""),
    ("U9", "PE7", "FMC_D4", ""),
    ("T9", "PE8", "FMC_D5", ""),
    ("P9", "PE9", "FMC_D6", ""),
    ("N9", "PE10", "FMC_D7", ""),
    ("P10", "PE11", "FMC_D8", ""),
    ("R10", "PE12", "FMC_D9", ""),
    ("T10", "PE13", "FMC_D10", ""),
    ("U10", "PE14", "FMC_D11", ""),
    ("R11", "PE15", "FMC_D12", ""),
    ("U16", "PD8", "FMC_D13", ""),
    ("T17", "PD9", "FMC_D14", ""),
    ("T16", "PD10", "FMC_D15", ""),
    ("C4", "PE0", "FMC_NBL0", ""),
    ("B4", "PE1", "FMC_NBL1", ""),
    ("P3", "PH4", "I2C2_SCL", ""),
    ("P4", "PH5", "I2C2_SDA", ""),
    ("E15", "PA8", "I2C3_SCL", ""),
    ("T13", "PH8", "I2C3_SDA", ""),
    ("K4", "PF8", "QUADSPI_BK1_IO0", ""),
    ("L4", "PF9", "QUADSPI_BK1_IO1", ""),
    ("K3", "PF7", "QUADSPI_BK1_IO2", ""),
    ("K2", "PF6", "QUADSPI_BK1_IO3", ""),
    ("P11", "PB10", "QUADSPI_BK1_NCS", ""),
    ("L3", "PF10", "QUADSPI_CLK", ""),
    ("J2", "PH0-OSC_IN (PH0)", "RCC_OSC_IN", ""),
    ("J1", "PH1-OSC_OUT (PH1)", "RCC_OSC_OUT", ""),
    ("A10", "PG9", "SPI1_MISO", ""),
    ("A5", "PB5", "SPI1_MOSI", ""),
    ("C6", "PB3 (JTDO/TRACESWO)", "SPI1_SCK", ""),
    ("U15", "PB14", "SPI2_MISO", ""),
    ("T15", "PB15", "SPI2_MOSI", ""),
    ("B12", "PD3", "SPI2_SCK", ""),
    ("D4", "PB9", "SPI2_NSS", "MEMS_CS"),
    ("D1", "PE5", "SPI4_MISO", ""),
    ("E5", "PE6", "SPI4_MOSI", ""),
    ("C3", "PE2", "SPI4_SCK", ""),
    ("D2", "PE4", "SPI4_NSS", ""),
    ("D15", "PA9", "TIM1_CH2", "CIS_CP"),
    ("F14", "PC6", "TIM3_CH1", "CIS_LED_B"),
    ("R17", "PD13", "TIM4_CH2", "CIS_LED_R"),
    ("R14", "PH12", "TIM5_CH3", "CIS_LED_G"),
    ("E13", "PC8", "TIM8_CH3", "CIS_SP"),
    ("C5", "PB7", "USART1_RX", ""),
    ("B5", "PB6", "USART1_TX", ""),
    ("A14", "PA15 (JTDI)", "GPIO_Input", "MEMS_FSYNC"),
    ("E16", "PA12", "GPIO_Output", "CIS_RS"),
    ("C2", "PC14-OSC32_IN (OSC32_IN)", "GPIO_Output", "ETH_RST"),
    ("G15", "PG6", "GPIO_Output", "EN_12V"),
    ("H16", "PG2", "GPIO_Output", "EN_5V"),
    ("N13", "PJ8", "GPIO_EXTI8", "MEMS_INT"),
]

def generate_kicad_label(label_name, x, y, uuid_str):
    """Génère une étiquette KiCad"""
    return f'''	(label "{label_name}"
		(at {x} {y} 0)
		(effects
			(font
				(size 1.27 1.27)
			)
			(justify left bottom)
		)
		(uuid "{uuid_str}")
	)'''

def generate_kicad_wire(x1, y1, x2, y2, uuid_str):
    """Génère un fil KiCad"""
    return f'''	(wire
		(pts
			(xy {x1} {y1}) (xy {x2} {y2})
		)
		(stroke
			(width 0)
			(type default)
		)
		(uuid "{uuid_str}")
	)'''

def generate_kicad_schema():
    """Génère le schéma KiCad complet"""
    
    schema_uuid = str(uuid.uuid4())
    
    # En-tête du schéma
    content = f'''(kicad_sch
	(version 20231120)
	(generator "eeschema")
	(generator_version "8.0")
	(uuid "{schema_uuid}")
	(paper "A2")
	(title_block
		(title "Sp3ctra - STM32H747XIHx Schematic")
		(date "2026-02-11")
		(rev "1.0")
		(company "CISYNTH")
		(comment 1 "Configuration: Sp3ctra")
	)
	(lib_symbols
		(symbol "MCU_ST_STM32H7:STM32H747XIHx"
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "U"
				(at 0 2.54 0)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "Value" "STM32H747XIHx"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "Footprint" "Package_BGA:TFBGA-265_14x14mm_Layout17x17_P0.8mm"
				(at 0 -2.54 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Datasheet" "https://www.st.com/resource/en/datasheet/stm32h747xi.pdf"
				(at 0 -5.08 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Description" "STM32H747XIHx Dual Core MCU"
				(at 0 -7.62 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(symbol "STM32H747XIHx_0_1"
				(rectangle
					(start -40.64 150.0)
					(end 40.64 -150.0)
					(stroke
						(width 0.254)
						(type default)
					)
					(fill
						(type background)
					)
				)
			)
			(symbol "STM32H747XIHx_1_1"
'''
    
    # Ajout des pins
    y_pos = 145.0
    pin_spacing = 2.54
    
    for pin_num, pin_name, function, label in PIN_CONFIG:
        pin_uuid = str(uuid.uuid4())
        content += f'''				(pin bidirectional line
					(at -45.72 {y_pos:.2f} 0)
					(length 5.08)
					(name "{pin_name}"
						(effects
							(font
								(size 1.016 1.016)
							)
						)
					)
					(number "{pin_num}"
						(effects
							(font
								(size 1.016 1.016)
							)
						)
					)
					(alternate "{function}" bidirectional line)
				)
'''
        y_pos -= pin_spacing
    
    content += '''			)
		)
	)
'''
    
    # Ajout du composant principal
    comp_uuid = str(uuid.uuid4())
    content += f'''	(symbol
		(lib_id "MCU_ST_STM32H7:STM32H747XIHx")
		(at 100.0 0 0)
		(unit 1)
		(exclude_from_sim no)
		(in_bom yes)
		(on_board yes)
		(dnp no)
		(uuid "{comp_uuid}")
		(property "Reference" "U1"
			(at 100.0 152.54 0)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Value" "STM32H747XIHx"
			(at 100.0 -152.54 0)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Footprint" "Package_BGA:TFBGA-265_14x14mm_Layout17x17_P0.8mm"
			(at 100.0 -155.08 0)
			(effects
				(font
					(size 1.27 1.27)
				)
				(hide yes)
			)
		)
'''
    
    # Ajout des références de pins
    for pin_num, pin_name, function, label in PIN_CONFIG:
        pin_inst_uuid = str(uuid.uuid4())
        content += f'''		(pin "{pin_num}"
			(uuid "{pin_inst_uuid}")
		)
'''
    
    content += '''		(instances
			(project "Sp3ctra_STM32"
				(path "/a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d"
					(reference "U1")
					(unit 1)
				)
			)
		)
	)
'''
    
    # Ajout des fils et étiquettes
    y_pos = 145.0
    for pin_num, pin_name, function, label in PIN_CONFIG:
        # Position du fil
        wire_start_x = 140.64  # Sortie du symbole
        wire_start_y = y_pos
        wire_end_x = 160.0
        wire_end_y = y_pos
        
        # Génération UUID
        wire_uuid = str(uuid.uuid4())
        label_uuid = str(uuid.uuid4())
        
        # Ajout du fil
        content += generate_kicad_wire(wire_start_x, wire_start_y, wire_end_x, wire_end_y, wire_uuid) + '\n'
        
        # Ajout de l'étiquette (fonction ou label personnalisé)
        label_text = label if label else function
        content += generate_kicad_label(label_text, wire_end_x + 2.54, wire_end_y, label_uuid) + '\n'
        
        y_pos -= pin_spacing
    
    # Fermeture du fichier
    content += ')\n'
    
    return content

if __name__ == "__main__":
    schema_content = generate_kicad_schema()
    output_file = "Sp3ctra_STM32.kicad_sch"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(schema_content)
    print(f"Schéma généré: {output_file}")
