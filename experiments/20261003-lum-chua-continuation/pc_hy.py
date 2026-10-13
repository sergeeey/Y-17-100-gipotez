"""C2 positive control: Huan-Yang/Llibre-Ponce system, 3 cycles, compare to published Y_k."""
import numpy as np, json
from pwl import *
zR,zL = hy_zones()
for n in (3000,6000,12000):
    r = count_cycles(zR,zL,n=n,dmin=1e-6,dmax=200.0)
    print("n=",n,"count",r["n_sign_changes"],"amb",r["ambiguous_gaps"],"suspect",r["noise_suspect"],flush=True)
roots = r["roots"]
for x in roots: print(x)
ys = sorted([x["y0"] for x in roots]+[x["y1"] for x in roots])
pub = sorted(HY_Y)
print("published", pub)
# match: each published Y should be in either y0 or y1 set
allv = np.array([x["y0"] for x in roots]+[x["y1"] for x in roots])
for Y in pub:
    print(Y, "closest", allv[np.argmin(abs(allv-Y))], "err", np.min(abs(allv-Y)))
