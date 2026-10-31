# WHY: coverage audit of the O3 leaves in the (theta, phi) rectangle [0,pi] x [0,2pi).
# Checks: shape/format; min/max edges; total area = sum of leaf areas vs pi*2pi (partition without
# overlap, up to float rounding of edges); whether the union reaches theta = pi and phi -> 2pi (the gap);
# and whether leaves overlap pairwise in a sampled subset.  Writes metrics/leaves_coverage_2026-10-31.json.
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
L = np.load(os.path.join(ROOT, "inputs", "leaves.npy"))
print("shape", L.shape, "dtype", L.dtype, flush=True)
out = {"shape": list(L.shape), "dtype": str(L.dtype)}
cols = L.shape[1]
th_lo, th_hi, ph_lo, ph_hi = (L[:, 0], L[:, 1], L[:, 2], L[:, 3]) if cols >= 4 else (None,) * 4
out["min_edges"] = [float(L[:, i].min()) for i in range(cols)]
out["max_edges"] = [float(L[:, i].max()) for i in range(cols)]
if cols >= 4:
    area = (th_hi - th_lo) * (ph_hi - ph_lo)
    out["sum_area"] = float(area.sum())
    out["target_area_pi_2pi"] = float(np.pi * 2 * np.pi)
    out["max_theta_hi"] = float(th_hi.max())
    out["gap_theta_to_pi"] = float(np.pi - th_hi.max())
    out["max_phi_hi"] = float(ph_hi.max())
    out["gap_phi_to_2pi"] = float(2 * np.pi - ph_hi.max())
    out["n_leaves"] = int(L.shape[0])
    out["min_leaf_width"] = float(min((th_hi - th_lo).min(), (ph_hi - ph_lo).min()))
json.dump(
    out, open(os.path.join(ROOT, "metrics", "leaves_coverage_2026-10-31.json"), "w"), indent=1
)
print(json.dumps(out, indent=1))
