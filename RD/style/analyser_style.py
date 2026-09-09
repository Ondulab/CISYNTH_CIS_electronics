"""Mesures descriptives, en lecture seule. Python + sexpdata ; XML exportés par KiCad.

Les fréquences décrivent des instances, pas des preuves indépendantes d'auteur.
Les propriétés graphiques ne sont pas arrondies ni réécrites dans les sources.
"""
from pathlib import Path
import collections as co
import csv
import hashlib
import json
import math
import xml.etree.ElementTree as ET
import sexpdata

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[5]
G = 0.635  # grille de mesure, 25 mil ; pas une instruction de déplacement


def tag(x):
    return str(x[0]) if isinstance(x, list) and x else ''


def one(x, k, default=None):
    return next((z for z in x if tag(z) == k), default)


def many(x, k):
    return [z for z in x if tag(z) == k]


def val(x, k, default=''):
    z = one(x, k)
    return z[1] if z is not None and len(z) > 1 else default


def at(x):
    return list(one(x, 'at', ['at', 0, 0, 0])[1:])


def percentile(values, f):
    a = sorted(values)
    return a[round((len(a) - 1) * f)] if a else None


def on_grid(x, pitch):
    return abs(x / pitch - round(x / pitch)) < 1e-5


def visible(p):
    eff = one(p, 'effects', [])
    return not (sexpdata.Symbol('hide') in eff or val(eff, 'hide') == sexpdata.Symbol('yes')
                or val(p, 'hide') == sexpdata.Symbol('yes'))


def inspect(name, path):
    d = sexpdata.loads(path.read_text())
    libs = {x[1]: x for x in many(one(d, 'lib_symbols'), 'symbol')}
    pin_nets = {}
    xml = OUT / f'{name}.xml'
    if xml.exists():
        for net in ET.parse(xml).findall('./nets/net'):
            for n in net.findall('node'):
                pin_nets[n.get('ref'), n.get('pin')] = net.get('name')
    symbols = []
    for x in many(d, 'symbol'):
        p = {z[1]: z for z in many(x, 'property')}
        ref = p.get('Reference', ['', '', ''])[2]
        pos = at(x)
        angle = pos[2] if len(pos) > 2 else 0
        fields = []
        for k, v in p.items():
            if visible(v):
                a = at(v)
                eff = one(v, 'effects', [])
                fields.append(dict(name=k, text=v[2], at=a,
                                   offset=[round(a[0]-pos[0], 5), round(a[1]-pos[1], 5)],
                                   size=one(one(eff, 'font', []), 'size', [])[1:],
                                   justify=one(eff, 'justify', [])[1:]))
        unit = val(x, 'unit', 1)
        lib = libs.get(val(x, 'lib_id'), [])
        pins = []
        for sub in many(lib, 'symbol'):
            suffix = sub[1].rsplit('_', 2)
            if len(suffix) < 3 or suffix[-2] not in ('0', str(unit)):
                continue
            for pin in many(sub, 'pin'):
                px, py, *_ = at(pin)
                # KiCad symbol local axes: x right, y up. Mirror then rotate.
                mirror = str(val(x, 'mirror'))
                if mirror == 'x':
                    py = -py
                if mirror == 'y':
                    px = -px
                a = math.radians(angle)
                xy = [round(pos[0]+px*math.cos(a)-py*math.sin(a), 5),
                      round(pos[1]-px*math.sin(a)-py*math.cos(a), 5)]
                num = str(val(pin, 'number'))
                pins.append(dict(number=num, name=val(pin, 'name'), at=xy,
                                 net=pin_nets.get((ref, num))))
        symbols.append(dict(ref=ref, value=p.get('Value', ['', '', ''])[2],
                            lib_id=val(x, 'lib_id'), uuid=val(x, 'uuid'), unit=unit,
                            at=pos, mirror=str(val(x, 'mirror')), fields=fields, pins=pins))
    wires = []
    for w in many(d, 'wire'):
        pts = [p[1:] for p in one(w, 'pts')[1:]]
        for a, b in zip(pts, pts[1:]):
            dx, dy = b[0]-a[0], b[1]-a[1]
            orient = 'H' if abs(dy)<1e-6 else ('V' if abs(dx)<1e-6 else 'diagonal')
            wires.append(dict(a=a, b=b, orientation=orient, length_g=round(math.hypot(dx, dy)/G, 5)))
    labels = []
    for k in ('label', 'global_label', 'hierarchical_label'):
        for x in many(d, k):
            labels.append(dict(kind=k, name=x[1], at=at(x),
                               size=one(one(one(x, 'effects', []), 'font', []), 'size', [])[1:]))
    drawings = []
    for x in d[1:]:
        if tag(x) in ('polyline', 'rectangle', 'text', 'text_box'):
            drawings.append(sexpdata.dumps(x))
    real = [s for s in symbols if not s['ref'].startswith('#')]
    groups = {k:[s for s in real if s['ref'].startswith(k)] for k in ('R','C','U','J','D','Q','L')}
    coords = [s['at'][i] for s in symbols for i in (0,1)]
    endpoints = [p[i] for w in wires for p in (w['a'], w['b']) for i in (0,1)]
    lengths = [w['length_g'] for w in wires]
    by_ref = {s['ref']: s for s in symbols}
    junction_xy = {tuple(at(x)[:2]) for x in many(d, 'junction')}
    crossings = {}
    for h in (w for w in wires if w['orientation'] == 'H'):
        x1, x2 = sorted([h['a'][0], h['b'][0]])
        y = h['a'][1]
        for v in (w for w in wires if w['orientation'] == 'V'):
            y1, y2 = sorted([v['a'][1], v['b'][1]])
            x = v['a'][0]
            if x1+1e-5 < x < x2-1e-5 and y1+1e-5 < y < y2-1e-5:
                crossings[x,y] = (x,y) in junction_xy
    def layout_group(refs):
        selected = [by_ref[r] for r in refs if r in by_ref]
        return {'refs': [s['ref'] for s in selected],
                'at_mm': [s['at'] for s in selected],
                'successive_delta_g': [[round((b['at'][i]-a['at'][i])/G, 5) for i in (0,1)]
                                      for a,b in zip(selected,selected[1:])]}
    group_refs = ([['U1','U3','U9','U4','U5'], ['R7','R8'], ['R9','R6'],
                   ['C5','C31'], ['C19','C51'], ['C90','C35']] if name == 'V3' else
                  [['U1','U2'], ['U7','U8'], ['C1','C3','C7'], ['C2','C4'],
                   ['C25','C29','C37'], ['C26','C30','C38'], ['R17','R18'],
                   ['C44','C47'], ['C60','C63'], ['C46','C51','C53'],
                   ['R33','R34','R35'], ['R10','R13','R14','R15','R16'],
                   ['Q1','Q2','Q3'], ['C85','C87','C89','C93','C97','C103','C107'],
                   ['C76','C78'], ['C77','C79']])
    summary = dict(symbol_instances=len(symbols), nonpower_instances=len(real),
                   refs=len(set(s['ref'] for s in real)),
                   counts={k:len(v) for k,v in groups.items()},
                   angles={k:dict(co.Counter(s['at'][2] for s in v)) for k,v in groups.items()},
                   multiunits={r:sorted(s['unit'] for s in real if s['ref']==r)
                               for r,c in co.Counter(s['ref'] for s in real).items() if c>1},
                   grid_absolute_coordinates={str(g):{'symbols':sum(on_grid(v,g) for v in coords),
                                                     'symbol_total':len(coords),
                                                     'wire_endpoints':sum(on_grid(v,g) for v in endpoints),
                                                     'wire_total':len(endpoints)} for g in (1.27,.635,.3175,.254,.127)},
                   wire_orientations=dict(co.Counter(w['orientation'] for w in wires)),
                   wire_lengths_g={'p25':percentile(lengths,.25),'p50':percentile(lengths,.5),
                                   'p75':percentile(lengths,.75),'p90':percentile(lengths,.9),
                                   'max':max(lengths,default=0),
                                   'common':co.Counter(lengths).most_common(12)},
                   label_kinds=dict(co.Counter(l['kind'] for l in labels)),
                   label_angles=dict(co.Counter(l['at'][2] for l in labels)),
                   field_sizes=co.Counter(str(f['size']) for s in real for f in s['fields']).most_common(),
                   ground_angles=dict(co.Counter(s['at'][2] for s in symbols if s['value']=='GND')),
                   power_angles=dict(co.Counter(s['at'][2] for s in symbols if s['ref'].startswith('#PWR') and s['value']!='GND')))
    summary['measurement_grid_mm'] = G
    summary['resistor_value_at_anchor'] = sum(any(f['name'] in ('Value','Field4') and f['offset']==[0,0]
                                                 for f in s['fields']) for s in groups['R'])
    summary['capacitor_reference_above_anchor'] = sum(any(f['name']=='Reference' and f['at'][1]<s['at'][1]
                                                         for f in s['fields']) for s in groups['C'])
    summary['strict_interior_HV_crossings'] = {'total':len(crossings),'with_junction':sum(crossings.values()),
                                             'definition':'Croisements strictement intérieurs aux deux segments, hors T et diagonales.'}
    data=dict(source=str(path.relative_to(ROOT)), sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
              summary=summary, symbols=symbols,wires=wires,labels=labels,
              junctions=[at(x) for x in many(d,'junction')],drawings=drawings,
              measured_groups=[layout_group(refs) for refs in group_refs],
              crossings=[{'at':list(xy),'junction':j} for xy,j in crossings.items()])
    (OUT/f'{name}-mesures.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    with (OUT/f'{name}-symboles.csv').open('w') as f:
        writer=csv.writer(f);writer.writerow(['reference','unit','value','lib_id','x_mm','y_mm','angle','mirror','pins_nets'])
        for s in symbols:
            writer.writerow([s['ref'],s['unit'],s['value'],s['lib_id'],*s['at'],s['mirror'],
                             '; '.join(f"{p['number']}:{p['net']}" for p in s['pins'])])
    return summary


if __name__ == '__main__':
    manifest=json.loads((OUT/'corpus.json').read_text())
    for name, meta in manifest.items():
        source = ROOT / meta['source']
        if hashlib.sha256(source.read_bytes()).hexdigest() != meta['sha256']:
            raise RuntimeError(f'{name}: source modifiée depuis les exports KiCad ; créer un nouveau corpus cohérent avant de mesurer.')
    result={name:inspect(name, ROOT / meta['source']) for name,meta in manifest.items()}
    (OUT/'synthese-mesures.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(result,indent=2,ensure_ascii=False))
