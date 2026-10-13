"""Homotopy from the known 1-cycle continuous Lienard example (round-1 control) to the HY 3-cycle system,
in (A_R, e_R, A_L, e_L) coordinates (line x=0, z'=A(z-e)).  Tracks #sign changes of G and located transitions."""
import numpy as np, json
from pwl import *
from search import P0, zones, evaluate

def zone_to_p(z):
    return z.A.ravel(), z.ze
zR0 = lienard_zone(0.5, 1.0, 0.5); zL0 = lienard_zone(-2.0, 5.0, 0.5)
pB = np.concatenate([zR0.A.ravel(), zL0.A.ravel(), zR0.ze, zL0.ze])
print("base 1-cycle ctrl count:", evaluate(pB, with_score=False))
print("HY count:", evaluate(P0, with_score=False))
rows = []
prev = None
for s in np.linspace(0, 1, 401):
    p = (1 - s) * pB + s * P0
    try:
        zR, zL = zones(p)
        r = count_cycles(zR, zL, n=3000, dmin=1e-6, dmax=300.0)
        good = [x for x in r["roots"] if abs(x["res"]) < 1e-8 * (1 + abs(x["y0"]))]
        n = len(good); sus = r["noise_suspect"]; spur = r["n_sign_changes"] - n
    except Exception as e:
        n = -1; sus = 0; spur = 0
    rows.append((float(s), n, spur, sus))
    if n != prev:
        print(f"s={s:.4f} n={n} spurious={spur} suspect={sus}", flush=True)
        prev = n
json.dump(rows, open("homotopy.json", "w"))
print("max n along path:", max(r[1] for r in rows))
