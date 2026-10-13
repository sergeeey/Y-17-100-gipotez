"""Independent second computation for the FPTT21 / GRS roots found by the new counter (exact rational parameters):
 (1) mpmath 40-digit exact-rational G sign flips at y0*(1 +- 1e-6) around each root;
 (2) round-1 verify.py: expm+fsolve Newton in (tR,tL,y0) and DOP853 piecewise simulation closure + transversality."""
import json
import mpmath as mp
import numpy as np
from fractions import Fraction as Fr
from controls_def import FPTT21, GRS, zones
from lc2_core import MPZone, count_cycles2, mp_G
import verify_r1 as V

def mpz(A, b):
    c = lambda x: mp.mpf(Fr(x).numerator) / mp.mpf(Fr(x).denominator)
    return MPZone([[c(x) for x in r] for r in A], [c(x) for x in b])

out = {}
for name, d in [("FPTT21", FPTT21), ("GRS", GRS)]:
    zR, zL = zones(d)
    mR, mL = mpz(d["AR"], d["bR"]), mpz(d["AL"], d["bL"])
    r = count_cycles2(zR, zL, n=8000, dmax=1e6, noise_rel=2e-14)
    AR = np.array([[float(x) for x in rr] for rr in d["AR"]]); AL = np.array([[float(x) for x in rr] for rr in d["AL"]])
    bR = np.array([float(x) for x in d["bR"]]); bL = np.array([float(x) for x in d["bL"]])
    rows = []
    for q in r["roots"]:
        y = q["y0"]
        gm = mp_G(mR, mL, zR, zL, y * (1 - 1e-6)); gp = mp_G(mR, mL, zR, zL, y * (1 + 1e-6))
        v = V.verify_cycle(AR, bR, AL, bL, y, q["tR"], q["tL"])
        rows.append(dict(y0=y, mp_G_left=mp.nstr(gm, 6), mp_G_right=mp.nstr(gp, 6), mp_sign_flip=bool(gm * gp < 0),
                         newton_y0=v["y0"], newton_res=v["resA"], transversal=v["transversal"], first_return=v["first_return"],
                         simB_closure=v["simB_closure"], trans=v["trans"]))
        print(name, rows[-1], flush=True)
    out[name] = dict(count=r["count"], rows=rows)
json.dump(out, open("verify_fptt.json", "w"), indent=1, default=str)
