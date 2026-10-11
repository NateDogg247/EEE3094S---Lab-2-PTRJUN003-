"""Create enlarged report views from an unchanged native KiCad SVG export.

Usage: python export_report_panels.py path/to/Kitticopter_3OpAmp_Controller.svg
First export that SVG with kicad-cli sch export svg --exclude-drawing-sheet.
Inkscape is used for vector PDF and PNG conversion when installed.
"""
from pathlib import Path
import argparse
import copy
import shutil
import subprocess
import xml.etree.ElementTree as ET

NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)

def export(svg_path, project_root):
    raw = ET.parse(svg_path).getroot()
    folder = project_root / 'report/figures'
    hardware = project_root / 'hardware/kicad'
    def crop(path, box):
        root = copy.deepcopy(raw)
        x, y, w, h = box
        root.set('viewBox', f'{x} {y} {w} {h}')
        root.set('width', f'{w}mm')
        root.set('height', f'{h}mm')
        ET.ElementTree(root).write(path, encoding='utf-8', xml_declaration=True)
    crop(folder/'kicad_bias.svg', (22,113,72,72))
    crop(hardware/'Kitticopter_3OpAmp_preview.svg', (0,20,297.0022,180))
    combined = ET.Element(f'{{{NS}}}svg', {'viewBox':'0 0 112 145', 'width':'112mm', 'height':'145mm'})
    # Each panel is a crop of the same export. V1 and V2 connect the panels.
    for i, (x,y,w,h) in enumerate([(0,39,97,46),(99,39,79,46),(178,39,112,46)]):
        child = copy.deepcopy(raw)
        for key, value in {'viewBox':f'{x} {y} {w} {h}', 'x':'0', 'y':str(i*49), 'width':str(w), 'height':str(h)}.items():
            child.set(key,value)
        combined.append(child)
    ET.ElementTree(combined).write(folder/'kicad_signal_stages.svg', encoding='utf-8', xml_declaration=True)
    inkscape = shutil.which('inkscape')
    if inkscape:
        for stem in ['kicad_bias','kicad_signal_stages']:
            subprocess.run([inkscape,str(folder/(stem+'.svg')),'--export-type=pdf',
                            '--export-filename='+str(folder/(stem+'.pdf'))], check=True)
        preview = hardware/'Kitticopter_3OpAmp_preview.svg'
        subprocess.run([inkscape,str(preview),'--export-type=png','--export-width=4200',
                        '--export-filename='+str(hardware/'Kitticopter_3OpAmp_preview.png')],check=True)
        subprocess.run([inkscape,str(preview),'--export-type=pdf',
                        '--export-filename='+str(folder/'kicad_controller.pdf')],check=True)
    else:
        print('SVG views exported; use Inkscape to convert them to PDF/PNG.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('native_svg', type=Path)
    parser.add_argument('--project-root',type=Path,default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    export(args.native_svg,args.project_root)
