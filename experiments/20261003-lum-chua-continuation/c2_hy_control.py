"""C2: HY / Llibre-Ponce 3-cycle positive control. Serial."""
import numpy as np, json, time
from pwl import *
t=time.time()
zR, zL = hy_zones()
res = {}
for n,dmax in ((3000,200.0),(8000,200.0),(8000,2000.0)):
    r = count_cycles(zR, zL, n=n, dmin=1e-7, dmax=dmax)
    ys1 = sorted([x["y1"] for x in r["roots"]], reverse=True)
    ys0 = sorted([x["y0"] for x in r["roots"]], reverse=True)
    print(f"n={n} dmax={dmax}: sign_changes={r['n_sign_changes']} ambiguous={r['ambiguous_gaps']} suspect={r['noise_suspect']}")
    print("  y1 (L-entry) :", ys1)
    print("  y0 (R-entry) :", ys0)
    print("  published Y  :", HY_Y)
    err = [min(abs(a-b) for a in ys1) for b in HY_Y]
    print("  |Y_pub - nearest y1| =", err)
    print("  roots:", [(x['res'], x['dG']) for x in r['roots']])
    res[f"{n}_{dmax}"] = dict(n=r['n_sign_changes'], y1=ys1, err=err)
json.dump(res, open("c2_hy_control.json","w"), indent=1)
print("time", time.time()-t)
