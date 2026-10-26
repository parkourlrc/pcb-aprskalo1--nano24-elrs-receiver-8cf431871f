from pathlib import Path
import subprocess,json,csv,re,zipfile,os,shutil
import xml.etree.ElementTree as ET
root=Path(__file__).resolve().parents[1];out=root/'exports/pcb';fab=out/'manufacturing';fab.mkdir(parents=True,exist_ok=True)
cli=os.environ.get('KICAD_CLI') or shutil.which('kicad-cli') or 'C:/Program Files/KiCad/10.0/bin/kicad-cli.exe'
def run(*args):
 r=subprocess.run([cli,*map(str,args)],cwd=root,capture_output=True,text=True,encoding='utf-8',errors='replace')
 if r.returncode:raise RuntimeError(r.stdout+r.stderr)
run('sch','erc','--format','json','--exit-code-violations','-o','exports/ERC.json','ELRS-Receiver.kicad_sch')
run('sch','export','netlist','--format','kicadxml','-o','exports/ELRS-Receiver.net.xml','ELRS-Receiver.kicad_sch')
# KiCad records an absolute workstation path here; use a portable public filename.
netlist_path=root/'exports/ELRS-Receiver.net.xml'
netlist=ET.parse(netlist_path);netlist.find('./design/source').text='ELRS-Receiver.kicad_sch'
netlist.write(netlist_path,encoding='utf-8',xml_declaration=True)
run('sch','export','bom','--fields','Reference,Value,MPN,Manufacturer,LCSC,Footprint,QUANTITY,TuningNote','--labels','Designator,Value,MPN,Manufacturer,LCSC,Footprint,Quantity,TuningNote','--group-by','MPN,Value,Footprint','--ref-range-delimiter','','-o','exports/ELRS-Receiver-BOM.csv','ELRS-Receiver.kicad_sch')
run('pcb','drc','--schematic-parity','--format','json','--exit-code-violations','-o',out/'DRC.json','ELRS-Receiver.kicad_pcb')
run('pcb','export','gerbers','--layers','F.Cu,In1.Cu,In2.Cu,In3.Cu,In4.Cu,B.Cu,F.Mask,B.Mask,F.SilkS,B.SilkS,F.Paste,B.Paste,Edge.Cuts','--use-drill-file-origin','--subtract-soldermask','-o',str(fab)+'/', 'ELRS-Receiver.kicad_pcb')
run('pcb','export','drill','--format','excellon','--excellon-units','mm','--drill-origin','plot','--excellon-separate-th','-o',str(fab)+'/', 'ELRS-Receiver.kicad_pcb')
run('pcb','export','pos','--format','csv','--units','mm','--side','both','--smd-only','--exclude-dnp','--use-drill-file-origin','-o',out/'ELRS-Receiver-positions.csv','ELRS-Receiver.kicad_pcb')
run('sch','export','svg','-o','exports/schematic/', 'ELRS-Receiver.kicad_sch')
for side,layers in [('top','F.Cu,F.SilkS,Edge.Cuts'),('bottom','B.Cu,B.SilkS,Edge.Cuts'),('assembly-top','F.Fab,F.CrtYd,Edge.Cuts'),('assembly-bottom','B.Fab,B.CrtYd,Edge.Cuts')]:
 run('pcb','export','svg','--mode-single','--page-size-mode','2','--layers',layers,*(['--mirror'] if 'bottom' in side else []),'-o',out/f'PCB-{side}.svg','ELRS-Receiver.kicad_pcb')
for side in ['top','bottom']:
 run('pcb','render','--width','1800','--height','1600','--side',side,'--background','opaque','--quality','basic','-o',out/f'PCB-{side}.png','ELRS-Receiver.kicad_pcb')
run('pcb','render','--width','1500','--height','1300','--side','top','--perspective','--rotate','30,0,-20','--zoom','0.65','--background','opaque','--quality','basic','-o',out/'PCB-perspective.png','ELRS-Receiver.kicad_pcb')
with (out/'ELRS-Receiver-positions.csv').open(encoding='utf-8-sig',newline='') as f:positions=list(csv.DictReader(f))
assert len(positions)==41,len(positions)
with (root/'exports/ELRS-Receiver-BOM.csv').open(encoding='utf-8-sig',newline='') as f:bom=list(csv.DictReader(f))
assert sum(int(r['Quantity']) for r in bom)==41
with (out/'JLCPCB-CPL.csv').open('w',encoding='utf-8',newline='') as f:
 w=csv.writer(f);w.writerow(['Designator','Mid X','Mid Y','Layer','Rotation'])
 for r in positions:w.writerow([r['Ref'],r['PosX'],r['PosY'],'Top' if r['Side'].lower()=='top' else 'Bottom',r['Rot']])
with (out/'JLCPCB-BOM.csv').open('w',encoding='utf-8',newline='') as f:
 w=csv.writer(f);w.writerow(['Comment','Designator','Footprint','LCSC Part #'])
 for r in bom:w.writerow([r['Value'],r['Designator'],r['Footprint'].split(':')[-1],r['LCSC']])
for file in fab.glob('*.drl'):
 text=file.read_text();xs=[float(x) for x in re.findall(r'X(-?\d+(?:\.\d+)?)',text)];ys=[float(y) for y in re.findall(r'Y(-?\d+(?:\.\d+)?)',text)]
 assert not xs or 0<=min(xs)<=max(xs)<=13,file.name
 assert not ys or 0<=min(ys)<=max(ys)<=11.1,file.name
with zipfile.ZipFile(out/'nano24-Gerbers-PROTOTYPE.zip','w',compression=zipfile.ZIP_DEFLATED) as z:
 for f in sorted(fab.iterdir()):
  if f.is_file():z.write(f,f.name)
print('Exported six-layer fabrication review plots, both-side positions for 41 parts, BOM, assembly maps and previews.')
