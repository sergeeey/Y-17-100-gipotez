# ruff: noqa
"""POST-HOC (not pre-registered): do the structural baselines separate poison from MATCHED benign insertions?

Reads metrics/s4_raw.json relative to this file (no absolute paths). Output is recorded in
audit/posthoc_benign_output.txt. Exploratory only; not part of the S4 verdict.
"""

import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parents[1]  # experiment directory
import sys  # noqa: E402

sys.path.insert(0, str(HERE))
import rstat_lib as L  # noqa: E402

raw = json.load(open(HERE / "metrics" / "s4_raw.json", encoding="utf-8"))
SIGNS = {"r": 1, "n_components": -1, "lambda2": 1, "modularity": -1, "centroid_cos": 1}
for c, arms in raw.items():
    print("==", c)
    for rate in (0.005, 0.01, 0.05, 0.2):
        row = {}
        for det, sg in SIGNS.items():
            pb = np.array(arms[f"P_bridge@{rate}"][det]) * sg
            bb = np.array(arms[f"B_bridge@{rate}"][det]) * sg
            cl = np.array(arms["clean"][det]) * sg
            row[det] = (
                round(L.auroc(pb, cl), 2),
                round(L.auroc(bb, cl), 2),
                round(L.auroc(pb, bb), 2),
            )
        print(
            f" rate={rate:5}  (AUC poison-vs-clean, benign-bridge-vs-clean, poison-vs-benign):", row
        )
