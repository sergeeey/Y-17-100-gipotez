# ruff: noqa
"""POST-HOC (not pre-registered): do the structural baselines separate poison from MATCHED benign insertions?"""

import json
import sys

sys.path.insert(
    0,
    r"E:\Проверка Гипотез\работаю над проверкой гипотез\Y-17 100 gipotez\experiments\20261014-syn-h1-rstat-memory-graph",
)
import numpy as np
import rstat_lib as L

raw = json.load(
    open(
        r"E:\Проверка Гипотез\работаю над проверкой гипотез\Y-17 100 gipotez\experiments\20261014-syn-h1-rstat-memory-graph\metrics\s4_raw.json",
        encoding="utf-8",
    )
)
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
