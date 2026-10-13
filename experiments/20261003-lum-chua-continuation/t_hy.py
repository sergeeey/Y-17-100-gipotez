import time, numpy as np
from pwl import *
zR, zL = hy_zones()
print("zR w,tau", zR.w, zR.tau, "zL w,tau", zL.w, zL.tau, flush=True)
t=time.time()
res = count_cycles(zR, zL, n=6000, dmin=1e-6, dmax=200.0)
print("time", time.time()-t)
print(res["n_sign_changes"], res["ambiguous_gaps"], res["n_valid"], res["grid"])
for r in res["roots"]:
    print(r)
print("published Y:", HY_Y)
