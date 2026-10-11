#!/usr/bin/env python3
"""Check the KiCad-exported connectivity and nominal ideal-op-amp DC model.

Run: python3 verify_netlist.py [path/to/controller.net]
Requires only the Python standard library. These are design checks, not
measurements of the assembled board and not a substitute for KiCad ERC.
"""
from pathlib import Path
import sys, json, math, xml.etree.ElementTree as ET

path=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('Kitticopter_3OpAmp_Controller.net')
root=ET.parse(path).getroot()
actual={n.attrib['name'].lstrip('/'): {x.attrib['ref']+'.'+x.attrib['pin'] for x in n.findall('node')} for n in root.findall('./nets/net')}
expected={
    '+15V':{'J2.1','U1.7','U2.7','U3.7'},
    '-15V':{'J2.3','R13.2','U1.4','U2.4','U3.4'},
    'GND':{'J1.5','J2.2','R11.1','R2.2','R6.2','R8.2'},
    'DAC-0':{'J1.2','J1.4','R3.1'}, 'DAC-1':{'J1.1','R1.1'},
    'ADC-1':{'J1.3','R10.2','U3.6'}, 'BIAS':{'P1.2','R9.1'},
    'BIAS_A':{'P1.1','R11.2','R12.1'}, 'BIAS_B':{'P1.3','R12.2','R13.1'},
    'V1':{'R4.2','U1.6','U2.3'}, 'V2':{'R5.2','R7.1','U2.6'},
    'Net-(U1-+)':{'R1.2','R2.1','U1.3'},
    'Net-(U1--)':{'R3.2','R4.1','U1.2'},
    'Net-(U2--)':{'R5.1','R6.1','U2.2'},
    'Net-(U3-+)':{'R7.2','R8.1','U3.3'},
    'Net-(U3--)':{'R10.1','R9.2','U3.2'},
}
for net,nodes in expected.items():
    if actual.get(net)!=nodes: raise AssertionError(f'{net}: {actual.get(net)} != {nodes}')
unused=set()
for i in range(1,4):
    for p in (1,5,8): unused.add(f'U{i}.{p}')
extra={k:v for k,v in actual.items() if k not in expected}
if any(len(v)!=1 for v in extra.values()) or set().union(*extra.values())!=unused:
    raise AssertionError(f'Unexpected unconnected pins: {extra}')
values={x.attrib['ref']:x.findtext('value') for x in root.findall('./components/comp')}
def resistance(ref):
    v=values[ref].lower()
    return float(v[:-1])*1000 if v.endswith('k') else float(v)
r={i:resistance('R'+str(i)) for i in range(1,14)}
rp=resistance('P1')
def solve(a,b):
    m=[list(row)+[rhs] for row,rhs in zip(a,b)]
    for i in range(len(m)):
        pivot=max(range(i,len(m)),key=lambda j:abs(m[j][i]))
        m[i],m[pivot]=m[pivot],m[i]
        scale=m[i][i]; m[i]=[v/scale for v in m[i]]
        for j in range(len(m)):
            if j!=i:
                s=m[j][i]; m[j]=[u-s*v for u,v in zip(m[j],m[i])]
    return [row[-1] for row in m]
def bias(w):
    parallel=rp*r[12]/(rp+r[12])
    total=r[11]+parallel+r[13]
    va=-15*r[11]/total; vb=-15*(r[11]+parallel)/total
    vth=va+w*(vb-va)
    # With the -15 V source shorted, inject 1 A into W to obtain Rth.
    ga=1/(rp*w); gb=1/(rp*(1-w)); g12=1/r[12]
    matrix=[[1/r[11]+g12+ga,-g12,-ga],[-g12,1/r[13]+g12+gb,-gb],[-ga,-gb,ga+gb]]
    rth=solve(matrix,[0,0,1])[2]
    ratio=r[10]/(r[9]+rth)
    return vth,rth,ratio,-ratio*vth
lo,hi=1e-9,1-1e-9
for _ in range(70):
    mid=(lo+hi)/2
    if bias(mid)[3]<2.5: lo=mid
    else: hi=mid
w=(lo+hi)/2; vth,rth,ratio,hover=bias(w)
g2=1+r[5]/r[6]; g3=(1+ratio)*r[8]/(r[7]+r[8])
af=r[4]/r[3]; ar=(1+af)*r[2]/(r[1]+r[2]); kp=af*g2*g3
assert math.isclose(af,ar,rel_tol=1e-12)
assert math.isclose(kp,0.014321913,abs_tol=1e-9)
assert math.isclose(hover,2.5,abs_tol=1e-10)
print(json.dumps({'status':'PASS','connected_nets':len(expected),'intentional_unused_pins':sorted(unused),'components':len(values),'nominal_ideal_DC':{'P1_fraction_from_pin_1':w,'bias_open_circuit_V':vth,'bias_thevenin_ohm':rth,'U2_gain':g2,'U3_incremental_gain':g3,'Kp_V_per_V':kp,'zero_error_command_V':hover},'scope':'KiCad XML netlist topology and ideal nominal DC; no hardware measurements or ERC'},indent=2))
