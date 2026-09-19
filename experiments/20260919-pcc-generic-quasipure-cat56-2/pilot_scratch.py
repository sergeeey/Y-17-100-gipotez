# ruff: noqa  (throw-away pilot, see claim.md registration note)
import sys

import h2_core as h
import numpy as np

rng = np.random.default_rng(2)
r = int(sys.argv[1])
for k in range(int(sys.argv[2]), int(sys.argv[3])):
    d = r + k
    best = None
    for s in range(2, 40):
        res = h.sample_sequential(k, r, s, rng)
        if res is None:
            break
        bl, nl = res
        q = np.ones(r) / r
        if h.qfim_rank(bl, q) < s:
            break
        rk = h.ranks(bl)
        vperp = d * d - rk["dim_v"]
        best = (s, rk["M"]["dim"], rk["W"]["dim"], vperp)
        if vperp < d:
            print(
                "  FIRES d=%d r=%d s=%d dimM=%d dimW=%d vperp=%d"
                % (d, r, s, rk["M"]["dim"], rk["W"]["dim"], vperp)
            )
    print(
        f"d={d} r={r} k={k} s*={best[0]} M={best[1]}/{2 * r * k} W={best[2]}/{k * k - 1} Vperp={best[3]} (need <{d}) r2+s+1={r * r + best[0] + 1}",
        flush=True,
    )
