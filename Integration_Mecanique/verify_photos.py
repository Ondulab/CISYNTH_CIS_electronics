"""Verify the saved nominal board against the mechanical coordinates and netlist."""
import json,xml.etree.ElementTree as ET
from pathlib import Path
import pcbnew as p
base=Path(__file__).resolve().parent;out=base/'Montage_Photos';mech=base.parent.parents[1]/'Meca/Sp3ctra_CIS_mechanics_v4/Integration_V4/Photos_2026-09-10'
g=json.loads((mech/'geometry.json').read_text());b=p.LoadBoard(str(out/'CIS_Montage_Photos.kicad_pcb'));refs={f.GetReference():f for f in b.GetFootprints()};netlist=ET.parse(out/'source_netlist.xml')
expected={}
for net in netlist.findall('.//nets/net'):
 for node in net.findall('node'):
  if node.get('ref') in g['connectors']:expected[(node.get('ref'),node.get('pin'))]=net.get('name')
report=dict(board_thickness_mm=p.ToMM(b.GetDesignSettings().GetBoardThickness()),connectors={})
assert abs(report['board_thickness_mm']-1)<1e-8
for ref,pose in g['connectors'].items():
 f=refs[ref];x,y=p.ToMM(f.GetPosition());expectedx=50+pose['center'][0];expectedy=68-pose['center'][1]
 assert abs(x-expectedx)<.000001 and abs(y-expectedy)<.000001,ref
 assert abs((f.GetOrientationDegrees()-pose['angle']+180)%360-180)<.000001
 assert f.IsLocked() and f.GetLayer()==p.F_Cu
 for pad in f.Pads():
  if (ref,pad.GetNumber()) in expected:assert pad.GetNetname()==expected[(ref,pad.GetNumber())],(ref,pad.GetNumber())
 report['connectors'][ref]=dict(kicad_xy_mm=[x,y],pcb_local_xy_mm=pose['center'],angle_deg=pose['angle'],layer=f.GetLayerName(),locked=f.IsLocked(),pads=len(list(f.Pads())),netlist_assignments_checked=sum(1 for pad in f.Pads() if (ref,pad.GetNumber()) in expected))
models=[]
for ref,f in refs.items():
 for model in f.Models():
  path=Path(model.m_Filename.replace('${KIPRJMOD}',str(out)));assert path.is_file(),path
  models.append(dict(ref=ref,path=str(path.relative_to(out) if path.is_relative_to(out) else path)))
report['model_files_present']=models
mechanical=refs['MECH1'];assert mechanical.GetAttributes() & p.FP_EXCLUDE_FROM_BOM;assert mechanical.GetAttributes() & p.FP_EXCLUDE_FROM_POS_FILES
r=json.loads((out/'drc.json').read_text());report['drc_violations']=len(r['violations']);report['drc_unconnected_items']=len(r['unconnected_items']);report['drc_types']={t:sum(v['type']==t for v in r['violations']) for t in sorted(set(v['type'] for v in r['violations']))}
assert len(r['violations'])==6
for v in r['violations']:assert any('J4' in i['description'] for i in v['items']),v
report['J1_J2_placement_violations']=0
report['fabrication_status']='Not fabrication-ready: J2 is a mockup; J4 has four errors and two warnings; board is unrouted.'
(out/'verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
