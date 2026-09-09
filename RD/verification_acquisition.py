#!/usr/bin/env python3
"""Vérifie la netliste KiCad XML de la correction acquisition du 08/09/2026.

Usage: python3 RD/verification_acquisition.py schema.xml [--before avant.xml]
Ne remplace ni ERC, ni simulation, ni validation du timing sur prototype.
"""
import argparse
import xml.etree.ElementTree as ET


def read(path):
    root = ET.parse(path).getroot()
    items = root.findall('./components/comp')
    comps = {c.get('ref'): c for c in items}
    assert len(comps) == len(items), 'Références dupliquées'
    nets = {}
    groups = {}
    for net in root.findall('./nets/net'):
        name = net.get('name')
        pins = {(n.get('ref'), n.get('pin')) for n in net}
        groups[name] = pins
        for pin in pins:
            assert pin not in nets, f'Broche sur plusieurs nets : {pin}'
            nets[pin] = name
    return comps, nets, groups


def verify(path, before=None):
    c, n, g = read(path)
    checks = []

    def check(condition, description):
        assert condition, description
        checks.append(description)

    def same(*pins):
        return len({n[p] for p in pins}) == 1

    def dnp(ref):
        return c[ref].find("property[@name='dnp']") is not None

    def resistor_between(ref, a, b):
        return {n[(ref, '1')], n[(ref, '2')]} == {n[a], n[b]}

    check(same(('U7', '1'), ('U7', '2'), ('U3', '19'), ('U3', '41'),
               ('U3', '43'), ('J3', '6'), ('J3', '9'), ('U18', '20'),
               ('U19', '5'), ('U20', '1'), ('U21', '5'), ('U17', '8'),
               ('R82', '1')), 'Rail ACQ commun et SENSE local')
    check(n[('U7', '1')] != n[('U14', 'A6')], 'ACQ distinct du 3V3 permanent')
    check(c['U7'].findtext('value') == 'ADP7104ARDZ-3.3' and
          'U8' not in c and 'U15' not in c, 'Un seul régulateur acquisition 500 mA')
    check(same(('U7', '3'), ('U7', '6'), ('U7', '9'), ('U18', '10'),
               ('U19', '3'), ('U20', '2'), ('U21', '3'), ('U17', '4'),
               ('U3', '3'), ('U3', '12'), ('U3', '15'), ('U3', '18'),
               ('U3', '26'), ('U3', '29'), ('U3', '42'), ('U3', '44'),
               ('U3', '57'), ('J3', '2'), ('U14', 'A1')), 'Masse commune, EPAD compris')
    check(same(('U7', '5'), ('U14', 'D10'), ('R75', '1')),
          'Commande alimentation PJ14 et rappel bas')
    check(same(('U7', '7'), ('U19', '2'), ('U21', '1'), ('U14', 'P6')) and
          same(('U18', '1'), ('U19', '4')) and
          same(('U18', '19'), ('U21', '4')) and
          not same(('U18', '1'), ('U18', '19')), 'OE séparés : PG et PG/RUN')
    check(same(('U14', 'N6'), ('U21', '2'), ('R112', '1')) and
          n[('R112', '2')] == n[('U3', '3')], 'PJ0 RUN_EN avec rappel 10k bas')
    check(c['U19'].findtext('value') == 'SN74LVC1G14DBV' and
          c['U21'].findtext('value') == 'SN74LVC1G132DBV',
          'Schmitt sur les commandes lentes PG/RUN')

    # Broches indépendamment vérifiées sur le brochage 244 / schéma STM32.
    for source, ip in [(('R65', '1'), '2'), (('U14', 'C3'), '4'),
                       (('U14', 'E5'), '6'), (('U14', 'D2'), '8'),
                       (('R67', '2'), '11'), (('U14', 'E16'), '13'),
                       (('R57', '2'), '15')]:
        check(same(source, ('U18', ip)), f'Commande source {source} vers U18.{ip}')
    for op, series, receiver in [('16', 'R92', ('U3', '32')),
                                 ('14', 'R93', ('U3', '31')),
                                 ('12', 'R94', ('U3', '30')),
                                 ('9', 'R95', ('J3', '10')),
                                 ('7', 'R96', ('J3', '8')),
                                 ('5', 'R97', ('U3', '45'))]:
        check(resistor_between(series, ('U18', op), receiver),
              f'Sortie U18.{op} via {series} vers {receiver}')
    check(same(('U18', '17'), ('U3', '3')) and
          len(g[n[('U18', '3')]]) == 1, 'Voie buffer inutilisée définie')
    check(resistor_between('R84', ('U3', '47'), ('R64', '1')) and
          same(('R64', '2'), ('U14', 'R3')), 'PIXCLK direct GPIO3 -> R84 -> R64 -> PA6')
    check(not dnp('R84') and all(dnp(r) for r in
          ['R88', 'C141', 'U17', 'R114', 'R115', 'R116', 'R117', 'R118', 'R119']),
          'Un seul chemin PIXCLK peuplé par défaut')
    for pin, ref in [('7', 'R115'), ('2', 'R116'), ('6', 'R117'),
                     ('3', 'R118'), ('5', 'R119')]:
        check(resistor_between(ref, ('U17', pin), ('R64', '1')),
              f'Tap DS1100L broche {pin} via {ref}')
    check(resistor_between('R121', ('R91', '2'), ('U3', '28')) and
          resistor_between('R120', ('R91', '2'), ('J3', '12')),
          'Branches MCLK indépendantes vers WHEC et VSP')
    check(same(('R87', '1'), ('U7', '1')) and
          same(('R85', '2'), ('U3', '3')) and
          same(('R87', '2'), ('R85', '1'), ('C142', '1')) and
          resistor_between('R125', ('R85', '1'), ('U3', '27')),
          'RCLK_N = diviseur ACQ/2 via strap sélectionnable')
    check(resistor_between('R122', ('U20', '4'), ('U3', '28')) and
          resistor_between('R123', ('U20', '3'), ('U3', '27')) and
          all(dnp(r) for r in ['U20', 'R122', 'R123', 'R124']),
          'Option LVDS désactivée, polarités Y/Z correctes')
    for vp, ref, mp in [('40', 'R62', 'R13'), ('39', 'R66', 'D14'),
                        ('38', 'R63', 'A9'), ('37', 'R68', 'E14'),
                        ('36', 'R69', 'B13'), ('35', 'R58', 'A4'),
                        ('34', 'R60', 'A2'), ('33', 'R61', 'B3')]:
        check(resistor_between(ref, ('U3', vp), ('U14', mp)), f'DCMI D{40-int(vp)} inchangé')
    check(same(('TP13', '1'), ('U14', 'R3')) and
          same(('TP14', '1'), ('U14', 'R13')) and
          same(('TP15', '1'), ('U14', 'B3')), 'Mesures PCLK/D0/D7 côté récepteur')
    check(all(dnp(r) for r in ['R126', 'R127', 'R128', 'R129', 'J5']),
          'Framing MCU/externe optionnel DNP')
    check(resistor_between('R126', ('U14', 'B5'), ('U14', 'U3')) and
          resistor_between('R127', ('U14', 'N5'), ('U14', 'A3')),
          'PB6/PA0 vers HSYNC/VSYNC')
    check(all(dnp(r) for r in ['C16', 'C59', 'R86']) and
          same(('U3', '10'), ('U3', '11')), 'Référence et voie 4 : montage conservateur')
    for ref in ['C46', 'C51', 'C53']:
        check(c[ref].find("fields/field[@name='Diélectrique']").text == 'C0G', ref+' C0G')
    # V5: sense resistors replace the old voltage-driven LED ballast resistors.
    for ref in ['R39', 'R42', 'R45']:
        check(c[ref].findtext('value') == '4.99' and
              '0805' in c[ref].findtext('footprint'), ref+' LED : resistance de mesure 4.99 ohm')
        check(c[ref].find("fields/field[@name='Tolerance']").text == '0.1%', ref+' precision 0.1%')

    if before:
        bc, bn, bg = read(before)
        retained = (set(bc) & set(c)) - {'U7', 'R85', 'R87', 'C142'}
        oldpins = {p for p in bn if p[0] in retained}
        check(oldpins <= set(n), 'Aucune broche anciennement connectée perdue')
        allowed_splits = {'+3.3V', '/CIS_CP', '/CIS_RS', '/CIS_SP', '/CIS_XLSYNC',
                          '/SPI4_MOSI', '/SPI4_NSS', '/SPI4_SCK'}
        for name, pins in bg.items():
            pins = {p for p in pins if p[0] in retained}
            if pins and name not in allowed_splits:
                check(len({n[p] for p in pins}) == 1, 'Pas de rupture : '+name)
        for name, pins in g.items():
            pins = {p for p in pins if p in oldpins}
            if pins and name not in {'+3.3VACQ', '/+3.3VACQ', 'GND'}:
                check(len({bn[p] for p in pins}) == 1, 'Pas de fusion : '+name)
    return checks


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('netlist')
    parser.add_argument('--before')
    args = parser.parse_args()
    checks = verify(args.netlist, args.before)
    print(f'{len(checks)} contrôles de connectivité / population réussis.')
