#!/usr/bin/env python3
"""Validate archived settings and export measurements. Does not run LTspice."""
from pathlib import Path
import csv, re
ROOT = Path(__file__).resolve().parents[1]
CASES = [('P08_baseline50_recovered','P08_schematic','4.99u','100n',299.451540021),('P08_duty30','P08_duty30','2.99u','100n',213.97343711),('P08_duty60','P08_duty60','5.99u','100n',374.414215074),('P08_loss_model','P08_loss_model','4.99u','100n',293.362307576),('P08_mosfet_model','P08_mosfet_model','4.99u','100n',295.164190811),('P08_mosfet_check','P08_mosfet_check','4.99u','50n',295.102534534)]
rows=[]
for asc_name,record,pulse,step,expected in CASES:
    asc=(ROOT/'ltspice'/f'{asc_name}.asc').read_text()
    net=(ROOT/'results/netlists'/f'{record}.net').read_text()
    log=(ROOT/'results/logs'/f'{record}.log').read_text()
    for text in [asc,net]:
        assert f'PULSE(0 10 0 10n 10n {pulse} 10u)' in text, asc_name
        assert f'.tran 0 400m 0 {step} startup' in text, asc_name
    assert 'ALY HANY RAKHA' in asc.upper()
    # Compare expressions, not just the existence of measurement names.
    a=set(re.findall(r'\.meas[^\n\\]+',asc))
    n=set(re.findall(r'\.meas[^\n\\]+',net))
    assert a==n, (asc_name, a^n)
    if step=='50n': assert '.options plotwinsize=0' in asc and '.options plotwinsize=0' in net
    measurements={}
    for line in log.splitlines():
        m=re.match(r'([a-zA-Z0-9_]+):.*=\s*([-+0-9.eE]+)(?:\s|$)',line)
        if m:
            measurements[m[1].lower()]=float(m[2])
            rows.append([asc_name,m[1].lower(),m[2]])
    assert abs(measurements['vout_avg']-expected)<1e-7
    if 'efficiency_total_pct' in measurements:
        calc=100*measurements['pout']/(measurements['pin']+measurements['pgate'])
        assert abs(calc-measurements['efficiency_total_pct'])<1e-6
    print(f'{asc_name}: settings match saved netlist; Vout={measurements["vout_avg"]:.6f} V')
with (ROOT/'results/measurements.csv').open('w',newline='') as f:
    writer=csv.writer(f); writer.writerow(['case','measurement','value']); writer.writerows(rows)
print(f'PASS: {len(CASES)} cases; exported {len(rows)} recorded measurements.')
