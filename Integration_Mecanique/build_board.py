"""Run with KiCad's Python, from the workspace. Placement study, not a routed board."""
import json,re,subprocess,xml.etree.ElementTree as ET
from pathlib import Path
import pcbnew as p
here=Path(__file__).resolve().parent; elec=here.parent
m=elec.parents[1]/'Meca/Sp3ctra_CIS_mechanics_v4/Integration_V4'
g=json.loads((m/'geometry.json').read_text()); subprocess.run(['/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli','sch','export','netlist','--format','kicadxml','-o',str(here/'source_netlist.xml'),str(elec/'CIS.kicad_sch')],check=True); root=ET.parse(here/'source_netlist.xml')
b=p.BOARD(); b.GetDesignSettings().SetBoardThickness(p.FromMM(1))
def vec(pt):return p.VECTOR2I(p.FromMM(50+pt[0]),p.FromMM(68-pt[1]))
for e in g['edges']:
 s=p.PCB_SHAPE(); s.SetLayer(p.Edge_Cuts);s.SetWidth(p.FromMM(.05))
 if e['type']=='line':s.SetShape(p.SHAPE_T_SEGMENT);s.SetStart(vec(e['points'][0]));s.SetEnd(vec(e['points'][2]))
 else:s.SetShape(p.SHAPE_T_ARC);s.SetArcGeometry(*[vec(x) for x in e['points']])
 b.Add(s)
netmap={}; padnets={}
for net in root.findall('.//nets/net'):
 nodes=[n for n in net.findall('node') if n.get('ref') in g['connectors']]
 if not nodes:continue
 n=p.NETINFO_ITEM(b,net.get('name'));b.Add(n);netmap[net.get('name')]=n
 for node in nodes:padnets[(node.get('ref'),node.get('pin'))]=n
out={}
for ref,pos in g['connectors'].items():
 c=root.find('.//components/comp[@ref="%s"]'%ref); lib,name=c.findtext('footprint').split(':')
 f=p.FootprintLoad(str(elec/(lib+'.pretty')),name);assert f
 f.SetReference(ref);f.SetValue(c.findtext('value'));f.SetFPID(p.LIB_ID(lib,name))
 sheet_uuid=re.search(r'\(uuid \"([^\"]+)\"\)',(elec/'CIS.kicad_sch').read_text()).group(1)
 f.SetPath(p.KIID_PATH('/'+sheet_uuid+'/'+c.findtext('tstamps')))
 f.SetOrientationDegrees(pos['angle']);f.SetPosition(vec(pos['center']));f.SetLocked(True)
 for pad in f.Pads():
  net=padnets.get((ref,pad.GetNumber()))
  if net:pad.SetNet(net)
 model=p.FP_3DMODEL();model.m_Filename="${KIPRJMOD}/models/"+ref+"_envelope.step";f.Models().push_back(model)
 b.Add(f)
 f.Reference().SetTextSize(p.VECTOR2I(p.FromMM(.8),p.FromMM(.8)))
 f.Reference().SetPosition(vec([pos['center'][0],pos['center'][1]+(3 if ref!='J2' else 5)]))
 out[ref]=dict(center_local=pos['center'],angle=pos['angle'],layer=f.GetLayerName(),pads=[dict(number=z.GetNumber(),net=z.GetNetname(),xy_mm=list(p.ToMM(z.GetPosition())),size_mm=list(p.ToMM(z.GetSize())),drill_mm=list(p.ToMM(z.GetDrillSize()))) for z in f.Pads()])
# Retain the user's two placement rectangles on a documentation layer.
for ref in ['J1','J2']:
 x0,y0,x1,y1=g['connectors'][ref]['bounds']; s=p.PCB_SHAPE();s.SetShape(p.SHAPE_T_RECT);s.SetStart(vec([x0,y0]));s.SetEnd(vec([x1,y1]));s.SetWidth(p.FromMM(.1));s.SetLayer(p.Dwgs_User);b.Add(s)
def note(s,xy,size=.9):
 t=p.PCB_TEXT(b);t.SetText(s);t.SetLayer(p.Dwgs_User);t.SetPosition(vec(xy));t.SetTextSize(p.VECTOR2I(p.FromMM(size),p.FromMM(size)));t.SetTextThickness(p.FromMM(.12));b.Add(t)
note('INTEGRATION MECANIQUE V4 - NON ROUTE - NON FABRICABLE',[120,24],1.4)
note('F.Cu : connecteurs / B.Cu : arrivee nappes depuis ecran',[125,21])
note('J2 : MOCKUP a remplacer par plan JAE MB-0215',[62,-4])
note('J4 : plages blindage hors contour 18 mm ; SH absent de l empreinte V4',[82,-7])
note('Encoche commune / plis MIPI et retour tactile 180 deg',[61,28])
# Reserve the insertion corridor on both faces, without altering the user's outline.
z=p.ZONE(b);z.SetIsRuleArea(True);z.SetDoNotAllowTracks(True);z.SetDoNotAllowVias(True);z.SetDoNotAllowZoneFills(True);z.SetDoNotAllowPads(True);z.SetDoNotAllowFootprints(True)
layers=p.LSET();layers.AddLayer(p.F_Cu);layers.AddLayer(p.B_Cu);z.SetLayerSet(layers)
poly=z.Outline();poly.NewOutline()
for q in [[33.6,8.2],[37.4,8.2],[37.4,18.5],[33.6,18.5]]:
 v=vec(q);poly.Append(v.x,v.y)
b.Add(z)
p.SaveBoard(str(here/'CIS_Integration_V4.kicad_pcb'),b)
(here/'placements.json').write_text(json.dumps(out,indent=2))
(here/'fp-lib-table').write_text('(fp_lib_table (version 7)\n'+''.join('(lib (name "'+lib+'")(type "KiCad")(uri "${KIPRJMOD}/../'+lib+'.pretty")(options "")(descr ""))\n' for lib in ['DISP','Library'])+')\n')
# Independent mechanical project with matching 1 mm board thickness.
(here/'CIS_Integration_V4.kicad_pro').write_text(json.dumps({'meta':{'filename':'CIS_Integration_V4.kicad_pro','version':1},'board':{'design_settings':{'rules':{'min_copper_edge_clearance':.2,'min_clearance':.15}}},'net_settings':{'classes':[{'name':'Default','clearance':.15}]}},indent=2))
print('Saved',len(b.GetDrawings()),'drawings and',len(b.GetFootprints()),'footprints')
