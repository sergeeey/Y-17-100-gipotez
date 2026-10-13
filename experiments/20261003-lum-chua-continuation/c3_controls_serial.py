"""C3 negative controls, SERIAL (replaces Pool version controls.py).  Seeded draws."""

import time, json, numpy as np
from pwl import *


def one(TL, DL, aL, TR, DR, aR):
    zR = lienard_zone(TR, DR, aR)
    zL = lienard_zone(TL, DL, aL)
    r = count_cycles(zR, zL, n=2500, dmin=1e-5, dmax=300.0)
    return r["n_sign_changes"], r["ambiguous_gaps"]


rng = np.random.default_rng(11)


def draw(sign_ok):
    TL = -rng.uniform(0.05, 2.5)
    TR = rng.uniform(0.05, 2.5)
    if not sign_ok:
        TR = -TR
    DL = TL**2 / 4 + rng.uniform(0.02, 4)
    DR = TR**2 / 4 + rng.uniform(0.02, 4)
    a = rng.uniform(-6, 6)
    return (TL, DL, a, TR, DR, a)


t = time.time()
cc = []
amb = 0
for i in range(200):
    n, a = one(*draw(True))
    cc.append(n)
    amb += a
    if i % 50 == 49:
        print("cont", i + 1, np.bincount(cc), time.time() - t, flush=True)
cs = []
for i in range(100):
    n, a = one(*draw(False))
    cs.append(n)
print("continuous hist", np.bincount(cc).tolist(), "max", max(cc), "ambig", amb)
print("same-sign hist", np.bincount(cs).tolist(), "max", max(cs))
print("time", time.time() - t)
json.dump(
    dict(cont=np.bincount(cc).tolist(), same=np.bincount(cs).tolist()),
    open("c3_controls_serial.json", "w"),
)
