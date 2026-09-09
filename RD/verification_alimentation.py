"""Verify actual KiCad XML connectivity, power-domain separation and retained acquisition nets."""
from pathlib import Path
import argparse,xml.etree.ElementTree as E,collections,json

def read(path):
 root=E.parse(path);parts={c.get('ref'):c for c in root.findall('.//components/comp')};pins={};groups={}
 for net in root.findall('.//nets/net'):
  name=net.get('name');ps=frozenset((p.get('ref'),p.get('pin')) for p in net.findall('node'));groups[name]=ps
  for p in ps:pins[p]=name
 return parts,pins,groups

def verify(path,before=None):
 c,n,g=read(path);checks=[]
 def ok(cond,msg):
  assert cond,msg
  checks.append(msg)
 def same(*ps):
  pp=[(r,str(p)) for r,p in ps];ok(len({n[x] for x in pp})==1,'Connected: '+str(pp))
 def apart(*ps):
  pp=[(r,str(p)) for r,p in ps];ok(len({n[x] for x in pp})==len(pp),'Separated: '+str(pp))
 def value(ref,v):ok(c[ref].findtext('value')==v,ref+'='+v)
 # All independent power rails must remain independent, including ground.
 apart(('J4',4),('Q4',3),('Q4',2),('U30',6),('U1',11),('U2',8),('U14','A6'),('U7',1),('U22',1),('U14','A1'))
 same(('J4',4),('J4',5),('F1',1));same(('F1',2),('Q4',3),('D3',1));same(('J4',7),('J4',8),('D3',2),('U14','A1'))
 same(('Q4',2),('D4',1),('C155',1),('U30',5));same(('Q4',1),('D4',2),('C155',2),('R130',1));same(('R130',2),('U14','A1'))
 same(('U30',6),('U1',7),('D5',1),('R136',1));same(('U30',3),('U1',1),('R136',2),('R137',1));value('R135','2.67k')
 same(('U30',1),('D6',1));same(('U1',1),('D7',1));same(('D6',2),('D7',2),('U14','A1'));value('R131','19.6k');value('R132','10k');value('R136','22k');value('R137','12.7k')
 same(('U30',1),('R131',2),('R132',1));same(('U30',2),('R133',2),('R134',1));same(('U30',9),('R135',1));same(('U30',7),('C157',1))
 for r in ['R132','R134','R135','R137']:same((r,2),('U14','A1'))
 same(('U1',8),('L1',1),('C131',1));same(('U1',20),('C131',2));same(('U1',10),('L1',2),('C159',1));same(('U1',19),('C159',2))
 same(('U1',11),('U1',12),('U1',13),('J2',22),('J3',13),('U7',8),('U22',9),('U22',10),('U22',7),('R17',1))
 same(('U1',14),('R17',2),('R18',1));same(('R18',2),('U1',17),('U1',9),('U14','A1'));value('R17','100k');value('R18','31.6k')
 same(('U1',15),('R140',1),('C162',1));same(('R140',2),('C161',1));same(('C161',2),('C162',2),('U14','A1'))
 same(('U1',6),('R138',1));same(('U1',5),('R139',2));same(('R138',2),('R139',1),('U14','A1'));same(('U1',2),('U1',18),('C160',1))
 same(('U2',3),('U2',2),('U1',11));same(('U2',5),('L8',1),('C19',2));same(('U2',6),('C19',1));same(('L8',2),('U14','A6'),('R76',1));same(('U2',8),('R76',2),('R77',1));value('R76','31.3k');value('R77','10k')
 same(('U22',1),('U22',2),('U4',12),('U4',16),('L2',2),('L3',1),('R153',1));same(('U22',3),('R153',2),('R154',1));value('R153','41.2k');value('R154','10k')
 same(('U22',4),('U22',6),('U22',11),('R154',2),('U14','A1'));same(('U22',8),('C177',1))
 same(('U7',1),('U7',2),('J3',6),('J3',9),('U3',19),('U3',41),('U3',43),('U18',20));apart(('U7',1),('U1',11),('U14','A6'))
 # Stable reference, default-off selection, all three local feedback loops and transistor sense paths.
 value('R142','35.7k');value('R143','10k')
 same(('U29',2),('R142',1),('R146',2),('R149',2),('R152',2));same(('R142',2),('R143',1),('C165',1),('U26',1),('U27',1),('U28',1))
 for i,(timer,cath,gate,sense,pull,fb,bias,cp) in enumerate([('R17',15,37,39,38,145,146,166),('T17',14,40,42,41,148,149,169),('T16',16,43,45,44,151,152,172)]):
  q='Q'+str(i+1);op='U'+str(23+i);sw='U'+str(26+i)
  same((q,3),('J3',cath));same((q,2),('R'+str(sense),1),('R'+str(fb),2));same((op,4),('R'+str(fb),1),('R'+str(bias),1),('C'+str(cp),2));same((op,1),('R'+str(gate),1),('C'+str(cp),1));same((q,1),('R'+str(gate),2));same((op,3),(sw,4));same((sw,6),('R'+str(pull),1))
  same((sw,2),(sw,3),(op,2),('R'+str(sense),2),('R'+str(pull),2),('U14','A1'));same((sw,5),('U14','A6'));same((op,5),('U1',11));value('R'+str(sense),'4.99');value('R'+str(fb),'1k');value('R'+str(bias),'1M')
  ok(c['R'+str(sense)].find("fields/field[@name='Tolerance']").text=='0.1%','Precision Rsense')
 # All capacitors must connect between distinct nets. This catches accidental wire crossings through bypass grounds.
 for ref,part in c.items():
  if ref.startswith('C') and (ref,'1') in n and (ref,'2') in n:ok(n[ref,'1']!=n[ref,'2'],'No short across '+ref)
 if before:
  bc,bn,bg=read(before)
  for r,sw in [('R37','U26'),('R40','U27'),('R43','U28')]:ok(n[sw,'6']==bn[r,'1'],'Original RGB timer preserved: '+sw)
  changed={'U1','U2','D3','F1','Q1','Q2','Q3','R37','R38','R39','R40','R41','R42','R43','R44','R45','R17','R18','R76','R77','C19','C20','C131','L1','C2','C4','C1','C3','C7','C25','C29','C37','C26','C30'}
  kept={p for p in bn if p[0] not in changed};ok(kept<=set(n),'All preserved pins present')
  for name,ps in bg.items():
   ps=ps & kept
   if ps and name not in ['+4.5V','+15V','Net-(C54-Pad1)','Net-(C58-Pad1)']:ok(len({n[p] for p in ps})==1,'No split: '+name)
  for name,ps in g.items():
   ps=ps & kept
   if ps and name!='GND':ok(len({bn[p] for p in ps})==1,'No merge: '+name)
   elif ps:ok({bn[p] for p in ps}<={'GND','Net-(C58-Pad1)'},'Only intentional RJ45 return grounded')
 return checks
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('netlist');p.add_argument('--before');a=p.parse_args();r=verify(a.netlist,a.before);print(f'{len(r)} power/connectivity checks passed.')
