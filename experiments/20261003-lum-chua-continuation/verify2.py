"""Independent verification of the two 2-cycle points found in the Lienard+beta family (aL,beta)."""
import json, numpy as np
from pwl import *
from continuation import BASE, build
from verify import verify_cycle
for aL, beta in [(-2.625, 3.0), (-2.25, 2.5)]:
    p = dict(BASE, aL=aL, beta=beta)
    zR, zL = build(p)
    r = count_cycles(zR, zL, n=12000, dmin=1e-6, dmax=600.0)
    print("aL,beta", aL, beta, "n_sign_changes", r["n_sign_changes"], "amb", r["ambiguous_gaps"], flush=True)
    for x in r["roots"]:
        v = verify_cycle(zR.A, zR.b, zL.A, zL.b, x["y0"], x["tR"], x["tL"])
        print("  y0=%.12f y1=%.12f res=%.2e dG=%.4g | A: y0=%.12f resA=%.1e | B closure=%s transversal=%s first_return=%s" % (
            x["y0"], x["y1"], x["res"], x["dG"], v["y0"], v["resA"], v["simB_closure"], v["transversal"], v["first_return"]), flush=True)
