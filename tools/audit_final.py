from pathlib import Path
import json,math,collections,xml.etree.ElementTree as ET
import wx
wx.Log.EnableLogging(False);wx.DisableAsserts()
import pcbnew as p
root=Path(__file__).resolve().parents[1];M=p.FromMM
V=lambda x,y:p.VECTOR2I(M(x),M(y))
b=p.LoadBoard(str(root/'ELRS-Receiver.kicad_pcb'));fps={f.GetReference():f for f in b.GetFootprints()}
assert len(fps)==47
parts=[f for f in fps.values() if not f.IsExcludedFromBOM()];assert len(parts)==41
edges=[d for d in b.GetDrawings() if isinstance(d,p.PCB_SHAPE) and d.GetLayer()==p.Edge_Cuts]
pts=[q for d in edges for q in [d.GetStart(),d.GetEnd()]]
size=[p.ToMM(max(q.x for q in pts)-min(q.x for q in pts)),p.ToMM(max(q.y for q in pts)-min(q.y for q in pts))]
assert size==[13.,11.1],size
assert b.GetCopperLayerCount()==6
keep=p.SHAPE_RECT(V(110.651,99.451),V(112.699,105.149))
counts=collections.Counter();length=0;vias=[];clockvias=[]
for t in b.GetTracks():
 if isinstance(t,p.PCB_VIA):
  vias.append(t)
  if t.GetNetname() in ['/XTAL_N','/XTAL_P','Net-(C1-Pad1)']:clockvias.append(t)
 else:
  counts[b.GetLayerName(t.GetLayer())]+=1;length+=p.ToMM(t.GetLength())
  assert t.GetLayer() not in [p.In1_Cu,p.In4_Cu]
 if p.SHAPE.Collide(t.GetEffectiveShape(t.GetLayer()),keep,0):
  assert t.GetNetname()=='/WIFI' and not isinstance(t,p.PCB_VIA)
 if t.GetNetname() in ['Net-(FL1-IN)','Net-(FL1-OUT)']:
  assert not isinstance(t,p.PCB_VIA) and t.GetLayer()==p.F_Cu
assert len(clockvias)==2
for r,f in fps.items():
 for q in f.Pads():
  if q.GetNumber() and p.SHAPE.Collide(q.GetEffectiveShape(f.GetLayer()),keep,0):assert r=='AE1',r
 name=f.GetFPID().GetUniStringLibItemName();folder='V04.pretty' if f.GetFPID().GetLibNickname()=='RX_V04' else 'Compact.pretty'
 assert (root/'libraries'/folder/f'{name}.kicad_mod').is_file()
 for model in f.Models():
  if model.m_Filename.startswith('${KIPRJMOD}/'):assert (root/model.m_Filename.replace('${KIPRJMOD}/','')).is_file()
for z in b.Zones():
 if z.GetIsRuleArea():continue
 assert not p.SHAPE.Collide(z.GetFilledPolysList(z.GetLayer()),keep,0),'Plane copper in antenna clearance'
ae=fps['AE1'];assert ae.IsExcludedFromBOM() and ae.IsExcludedFromPosFiles()
assert len(list(ae.Pads()))==1 and not len(ae.Models())
padrow=[]
for ref,x in [('TP1',101.25),('TP2',104.55),('TP3',107.85),('TP4',111.15)]:
 f=fps[ref];q=next(q for q in f.Pads() if q.GetProperty()==p.PAD_PROP_CASTELLATED)
 assert p.ToMM(q.GetPosition().x)==x and p.ToMM(q.GetPosition().y)==110.3
 assert p.ToMM(q.GetDrillSize().x)==.6
 assert f.IsExcludedFromBOM() and f.IsExcludedFromPosFiles();padrow.append(ref)
u1=fps['U1'];thermal=sum(t.GetNetname()=='GND' and abs(t.GetPosition().x-u1.GetPosition().x)<M(1.5) and abs(t.GetPosition().y-u1.GetPosition().y)<M(1.5) for t in vias);assert thermal>=9
d=json.loads((root/'exports/pcb/DRC.json').read_text());assert not d['violations'] and not d['unconnected_items'] and not d['schematic_parity']
erc=json.loads((root/'exports/ERC.json').read_text());assert not any(s.get('violations') for s in erc.get('sheets',[]))
xml=ET.parse(root/'exports/ELRS-Receiver.net.xml').getroot()
members=sorted([sorted([[q.attrib['ref'],q.attrib['pin']] for q in n.findall('node')]) for n in xml.findall('./nets/net')])
assert members==json.loads((root/'tools/expected-connectivity.json').read_text())
lookup={(q.attrib['ref'],q.attrib['pin']):n.attrib['name'] for n in xml.findall('./nets/net') for q in n.findall('node')}
mapping=json.loads((root/'firmware/receiver-hardware.json').read_text())
for key,pin,gpio,ref,target in [('serial_rx','27',20,'TP1','1'),('serial_tx','28',21,'TP2','1'),('radio_miso','10',5,'U3','16'),('radio_mosi','9',4,'U3','17'),('radio_sck','12',6,'U3','18'),('radio_nss','13',7,'U3','19'),('radio_rst','6',2,'U3','3'),('radio_busy','8',3,'U3','7'),('radio_dio1','5',1,'U3','8'),('led_rgb','14',8,'D1','4')]:
 assert mapping[key]==gpio and lookup['U1',pin]==lookup[ref,target]
data={'revision':'0.4','outline_mm':size,'bounding_rectangle_area_mm2':144.3,'area_reduction_from_v0_3_percent':20.71,'copper_layers':6,'nominal_thickness_mm':1.0,'purchased_components':41,'footprints':47,'top_components':sum(f.GetLayer()==p.F_Cu for f in parts),'bottom_components':sum(f.GetLayer()==p.B_Cu for f in parts),'track_segments_by_layer':dict(counts),'routed_length_mm':round(length,2),'via_count':len(vias),'C3_ground_vias_under_exposed_pad':thermal,'DRC_violations':0,'unconnected_items':0,'schematic_parity_issues':0,'ERC_violations':0,'antenna_all_layer_clear_region_mm':[2.05,5.7],'antenna_region_independent_copper_check':'AE1 and intended WiFi feed only; no plane fills, vias or foreign tracks/pads','antenna':'custom PCB meandered monopole; unmeasured tuning prototype','RF_feed_vias':0,'MCU_crystal_signal_vias':len(clockvias),'signals_on_near_surface_ground_planes':0,'cable_pad_order_front_left_to_right':padrow,'firmware_pin_mapping_checked':True,'circuit_change':'AE1 ceramic two-pin antenna replaced by one-feed PCB antenna; all other physical net memberships retained','not_verified':['antenna resonance, efficiency and matching','final fabricator stackup and RF impedance','castellated panel/process approval','physical prototype performance','final sourcing and assembler rotations']}
(root/'exports/verification.json').write_text(json.dumps(data,indent=2));print(json.dumps(data,indent=2))
