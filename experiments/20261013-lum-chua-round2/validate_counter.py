"""Calibrate float64 noise vs mpmath, then run all controls through count_cycles2 (and the round-1 counter for contrast)."""

import json
import sys
import time

import numpy as np

import pwl_r1
from controls_def import all_controls
from lc2_core import calibrate, count_cycles2, y_grid

out = {}
ctr = all_controls()

# ---- 1. noise calibration on three systems (log-spaced starts across 1e-6..1e5)
cal = {}
for name in ["HY_paper_eq2", "FPTT21_paper_eq3", "GRS_paper_eq4"]:
    zR, zL = ctr[name]
    ys = y_grid(zR, 60, 1e-4, 1e5)
    t0 = time.time()
    e, m = calibrate(zR, zL, ys)
    cal[name] = dict(max_rel_err=e, n=m, sec=round(time.time() - t0, 1))
    print("calib", name, cal[name], flush=True)
out["calibration"] = cal
noise_rel = max(
    1e-14, 10 * max(v["max_rel_err"] for v in cal.values() if np.isfinite(v["max_rel_err"]))
)
out["noise_rel_used"] = noise_rel
print("noise_rel used", noise_rel, flush=True)

# ---- 2. controls
res = {}
for name, (zR, zL) in ctr.items():
    t0 = time.time()
    r = count_cycles2(zR, zL, n=8000, dmax=1e6, noise_rel=noise_rel)
    old = pwl_r1.count_cycles(zR, zL, n=6000, dmax=200.0)
    short = dict(
        count=r["count"],
        n_roots_total=r["n_roots_total"],
        degenerate=r["degenerate"],
        flat_share=round(r["flat_share"], 4),
        rejected=r["rejected_float_sign_changes"],
        hidden_pairs=len(r["hidden_pairs"]),
        n_near_tangent=r["n_near_tangent"],
        kappa=r["kappa"],
        ambiguous_gaps=r["ambiguous_gaps"],
        n_valid=r["n_valid"],
        old_counter=dict(sign_changes=old["n_sign_changes"], noise_suspect=old["noise_suspect"]),
        roots=[
            dict(y0=x["y0"], y1=x["y1"], mult=x["multiplier"], crossing=x["crossing"], tag=x["tag"])
            for x in r["roots"]
        ],
        sec=round(time.time() - t0, 1),
    )
    res[name] = short
    print(name, {k: v for k, v in short.items() if k != "roots"}, flush=True)
    for x in short["roots"]:
        print("    root", x, flush=True)
out["controls"] = res
json.dump(out, open("validate_counter.json", "w"), indent=1, default=float)
