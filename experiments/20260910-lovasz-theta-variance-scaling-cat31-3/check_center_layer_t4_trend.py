"""Exam 3, stage 3: a cheap empirical check ruling out one specific concern before attempting an
analytic proof of l_eff(N) boundedness -- does the aggregate tail_tightness_4 decline (point 22,
23) come from mixing across q-layers with different Lmax=min(q,N-q), or does it show up even at
a SINGLE q where Lmax is held at "half the available range" throughout?

No new computation -- reads the already-verified per-layer tail_tightness_4 values from
metrics/tail_concentration_ratio.json and isolates the CENTER layer (q closest to N/2, where
Lmax=min(q,N-q) is maximal for that N) at each n.
"""

from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"

if __name__ == "__main__":
    d = json.load(open(METRICS / "tail_concentration_ratio.json", encoding="utf-8"))
    rows_out = []
    for n_str, rows in d["per_layer"].items():
        n = int(n_str)
        big_n = rows[0]["N"]
        center = min(rows, key=lambda r: abs(r["q"] - big_n / 2))
        q = center["q"]
        lmax = min(q, big_n - q)
        t4 = center["tail_tightness_4"]
        rows_out.append({"n": n, "N": big_n, "center_q": q, "Lmax": lmax, "t4_center": t4})
        print(f"n={n:3d}  N={big_n:3d}  center_q={q:2d}  Lmax={lmax:2d}  t4_center={t4:.4f}")

    METRICS.mkdir(exist_ok=True)
    with open(METRICS / "center_layer_t4_trend.json", "w", encoding="utf-8") as f:
        json.dump({"rows": rows_out}, f, indent=2)
