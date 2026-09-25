# ruff: noqa
"""Thin driver: calls the blind implementer's r=3 library UNCHANGED for (41,5,14) and controls. Parameters and printing only."""
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "independent_r3"))

import numpy as np  # noqa: E402
from cx_modp import build_tower, pipeline  # noqa: E402

D, R, S = 41, 5, 14
results = {}
t0 = time.time()


def brief(out):
    keys = ("sld_ok", "pcc_ok", "det_qfim_nonzero", "qfim_rank", "dim_V", "dim_Vperp")
    return {k: out.get(k) for k in keys if k in out}


# plumbing sanity: the r=3 case whose answer is already known (22)
Bs, dims = build_tower(23, 3, 12, 998244353, 1)
o = pipeline(23, 3, 12, 998244353, Bs)
print("SANITY d=23 r=3 s=12:", brief(o), flush=True)
results["sanity_d23"] = o

for p in (998244353, 1000000007):
    for seed in (1, 2):
        Bs, dims = build_tower(D, R, S, p, seed)
        print(f"=== EXACT d={D} r={R} s={S} p={p} seed={seed} (t={time.time()-t0:.0f}s)")
        print("   stage dims:", dims, flush=True)
        o = pipeline(D, R, S, p, Bs, field_check=(p % 4 == 3))
        print("   ", brief(o), flush=True)
        o["stage_dims"] = dims
        results[f"d{D}_p{p}_seed{seed}"] = o

p, seed = 998244353, 1
Bs, dims = build_tower(D, R, S, p, seed)
Bc = [B.copy() for B in Bs]
Bc[4][0, 0, 0] = (Bc[4][0, 0, 0] + 1) % p
o = pipeline(D, R, S, p, Bc, compute_V=False)
print("N1 corrupt B_5:", brief(o), "fail pairs:", str(o.get("pcc_fail_pairs"))[:120], flush=True)
results["N1"] = o
Bd = [B.copy() for B in Bs]
Bd[S - 1] = Bd[S - 2].copy()
o = pipeline(D, R, S, p, Bd)
print("N2 B_14 := B_13:", brief(o), flush=True)
results["N2"] = o
Bs14, dims14 = build_tower(D, R, S + 1, p, seed)
o = pipeline(D, R, S + 1, p, Bs14)
print("N3 s=15 stage dims tail:", dims14[-3:], brief(o), flush=True)
o["stage_dims"] = dims14
results["N3"] = o

Path(HERE / "r5_results.json").write_text(json.dumps(results, indent=1, default=str), encoding="utf-8")
print(f"done in {time.time()-t0:.0f}s")
