"""Run with KiCad's Python, from the workspace. Placement study, not a routed board."""
import argparse,os,json,re,subprocess,xml.etree.ElementTree as ET
from pathlib import Path
import pcbnew as p
base=Path(__file__).resolve().parent; elec=base.parent
parser=argparse.ArgumentParser();parser.add_argument('--geometry');parser.add_argument('--output');parser.add_argument('--name',default='CIS_Integration_V4');args=parser.parse_args()
here=Path(args.output).resolve() if args.output else base;here.mkdir(parents=True,exist_ok=True);project=args.name
m=elec.parents[1]/'Meca/Sp3ctra_CIS_mechanics_v4/Integration_V4'
g=json.loads((Path(args.geometry) if args.geometry else m/'geometry.json').read_text()); subprocess.run(['/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli','sch','export','netlist','--format','kicadxml','-o',str(here/'source_netlist.xml'),str(elec/'CIS.kicad_sch')],check=True); root=ET.parse(here/'source_netlist.xml')
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
library_paths={lib:elec/(lib+'.pretty') for lib in ['DISP','Library']}
if any('pin1_silk_shift_mm' in q for q in g['connectors'].values()):
 library_paths['DISP']=here/'DISP.pretty';library_paths['DISP'].mkdir(exist_ok=True)
for ref,pos in g['connectors'].items():
 c=root.find('.//components/comp[@ref="%s"]'%ref); lib,name=c.findtext('footprint').split(':')
 f=p.FootprintLoad(str(elec/(lib+'.pretty')),name);assert f
 if 'pin1_silk_shift_mm' in pos:
  dx,dy=pos['pin1_silk_shift_mm']
  for item in f.GraphicalItems():
   if isinstance(item,p.PCB_SHAPE) and item.GetLayer()==p.F_SilkS and item.GetShape()==p.SHAPE_T_CIRCLE:
    item.Move(p.VECTOR2I(p.FromMM(dx),p.FromMM(-dy)))
 if library_paths[lib]!=elec/(lib+'.pretty'):
  raw=(elec/(lib+'.pretty')/(name+'.kicad_mod')).read_text()
  if 'pin1_silk_shift_mm' in pos:
   match=re.search(r'\(fp_circle \(center ([^ ]+) ([^)]+)\) \(end ([^ ]+) ([^)]+)\)',raw)
   assert match and 'F.SilkS' in raw[match.end():match.end()+100]
   cx,cy,ex,ey=map(float,match.groups());dx,dy=pos['pin1_silk_shift_mm']
   replacement='(fp_circle (center %s %s) (end %s %s)'%(cx+dx,cy-dy,ex+dx,ey-dy)
   raw=raw[:match.start()]+replacement+raw[match.end():]
  (library_paths[lib]/(name+'.kicad_mod')).write_text(raw)
 f.SetReference(ref);f.SetValue(c.findtext('value'));f.SetFPID(p.LIB_ID(lib,name))
 sheet_uuid=re.search(r'\(uuid \"([^\"]+)\"\)',(elec/'CIS.kicad_sch').read_text()).group(1)
 f.SetPath(p.KIID_PATH('/'+sheet_uuid+'/'+c.findtext('tstamps')))
 f.SetOrientationDegrees(pos['angle']);f.SetPosition(vec(pos['center']));f.SetLocked(True)
 for pad in f.Pads():
  net=padnets.get((ref,pad.GetNumber()))
  if net:pad.SetNet(net)
 model=p.FP_3DMODEL();model.m_Filename="${KIPRJMOD}/"+os.path.relpath(base/"models",here)+"/"+ref+"_envelope.step";f.Models().push_back(model)
 b.Add(f)
 f.Reference().SetTextSize(p.VECTOR2I(p.FromMM(.8),p.FromMM(.8)))
 f.Reference().SetPosition(vec(pos.get('reference_position',[pos['center'][0],pos['center'][1]+(3 if ref!='J2' else 5)])))

 out[ref]=dict(center_local=pos['center'],angle=pos['angle'],layer=f.GetLayerName(),pads=[dict(number=z.GetNumber(),net=z.GetNetname(),xy_mm=list(p.ToMM(z.GetPosition())),size_mm=list(p.ToMM(z.GetSize())),drill_mm=list(p.ToMM(z.GetDrillSize()))) for z in f.Pads()])
# Retain the user's two placement rectangles on a documentation layer.
for ref in ['J1','J2']:
 x0,y0,x1,y1=g['connectors'][ref]['bounds']; s=p.PCB_SHAPE();s.SetShape(p.SHAPE_T_RECT);s.SetStart(vec([x0,y0]));s.SetEnd(vec([x1,y1]));s.SetWidth(p.FromMM(.1));s.SetLayer(p.Dwgs_User);b.Add(s)
def note(s,xy,size=.9):
 t=p.PCB_TEXT(b);t.SetText(s);t.SetLayer(p.Dwgs_User);t.SetPosition(vec(xy));t.SetTextSize(p.VECTOR2I(p.FromMM(size),p.FromMM(size)));t.SetTextThickness(p.FromMM(.12));b.Add(t)
note(g.get('board_note',('PROPOSITION SCANS - INTERFERENCES A RESOUDRE' if args.geometry else 'INTEGRATION MECANIQUE V4 - NON ROUTE - NON FABRICABLE')),[120,24],1.4)
if args.geometry:note('PCB propose : Z bas '+str(g['placement'][2])+' mm ; contour modifie ; non adopte',[95,31])
note('F.Cu : connecteurs / B.Cu : arrivee nappes depuis ecran',[125,21])
note('J2 : MOCKUP a remplacer par plan JAE MB-0215',[62,-4])
note('J4 : plages blindage hors contour 18 mm ; SH absent de l empreinte V4',[82,-7])
note('Encoche commune / plis MIPI et retour tactile 180 deg',[61,28])
# Reserve the insertion corridor on both faces, without altering the user's outline.
z=p.ZONE(b);z.SetIsRuleArea(True);z.SetDoNotAllowTracks(True);z.SetDoNotAllowVias(True);z.SetDoNotAllowZoneFills(True);z.SetDoNotAllowPads(True);z.SetDoNotAllowFootprints(True)
layers=p.LSET();layers.AddLayer(p.F_Cu);layers.AddLayer(p.B_Cu);z.SetLayerSet(layers)
poly=z.Outline();poly.NewOutline()
notch=g.get('notch',{'center_x':35.5,'width':3,'bottom_y':8.5});margin=g.get('notch_keepout_margin_mm',.4);left=notch['center_x']-notch['width']/2-margin;right=notch['center_x']+notch['width']/2+margin;bottom=notch['bottom_y']-.3
for q in [[left,bottom],[right,bottom],[right,18.5],[left,18.5]]:
 v=vec(q);poly.Append(v.x,v.y)
b.Add(z)
if g.get('mechanical_step_model'):
 library_paths['Montage3D']=here/'Montage3D.pretty';library_paths['Montage3D'].mkdir(exist_ok=True)
 model_path='${KIPRJMOD}/'+g['mechanical_step_model']
 library_paths['Montage3D'].joinpath('TouchBar_folded.kicad_mod').write_text('(footprint "TouchBar_folded" (version 20241229) (generator "pcbnew") (layer "F.Cu")\n (attr board_only exclude_from_pos_files exclude_from_bom)\n (model "'+model_path+'" (offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))\n)\n')
 mechanical=p.FootprintLoad(str(library_paths['Montage3D']),'TouchBar_folded');mechanical.SetFPID(p.LIB_ID('Montage3D','TouchBar_folded'))
 mechanical.SetReference('MECH1');mechanical.SetValue('TouchBar - montage nominal')
 mechanical.SetPosition(vec([0,0]));mechanical.SetLocked(True)
 mechanical.Reference().SetVisible(False);mechanical.Value().SetVisible(False);b.Add(mechanical)
p.SaveBoard(str(here/(project+'.kicad_pcb')),b)
(here/'placements.json').write_text(json.dumps(out,indent=2))
(here/'fp-lib-table').write_text('(fp_lib_table (version 7)\n'+''.join('(lib (name "'+lib+'")(type "KiCad")(uri "${KIPRJMOD}/'+os.path.relpath(library_paths[lib],here)+'")(options "")(descr ""))\n' for lib in library_paths)+')\n')
# Independent mechanical project with matching 1 mm board thickness.
(here/(project+'.kicad_pro')).write_text(json.dumps({'meta':{'filename':project+'.kicad_pro','version':1},'board':{'design_settings':{'rules':{'min_copper_edge_clearance':.2,'min_clearance':.15}}},'net_settings':{'classes':[{'name':'Default','clearance':.15}]}},indent=2))
print('Saved',len(b.GetDrawings()),'drawings and',len(b.GetFootprints()),'footprints')
