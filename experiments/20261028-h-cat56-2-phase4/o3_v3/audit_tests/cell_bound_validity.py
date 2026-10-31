"""Cell-level validity test of the certified bounds B_up (numerical, NOT a certificate).

For each cell [th_lo, th_hi, ph_lo, ph_hi] in metrics/interval_top1000.json (the 1000 tightest
certified cells; most, but not all, lie near the pole theta ~ pi: 784 of 1000 have th_lo > 3.0),
sample an n x n grid over the closed cell and compute
M(x) = lambda_max(N(x)^T H N(x)) (sup of y^H R y over unit y in ker Phi_x).
A certified bound is valid only if M(x) <= B_up for every x in the cell. A sampled violation
M(x) > B_up is a counterexample to that cell's certificate.

Usage: python -I cell_bound_validity.py <n_grid> <out.json>
"""

import json
import sys

import numpy as np

import os  # noqa: E402

sys.path.insert(
    0, os.path.dirname(os.path.abspath(__file__))
)  # -I drops the script dir from sys.path
from dense_sup_grid import INST, RPATH, S, kernel_basis, real_form, sa  # noqa: E402

As = sa.load_A(INST)
H = real_form(np.load(RPATH)["R"])

TOP = r"E:\Проверка Гипотез\работаю над проверкой гипотез\Y-17 100 gipotez\experiments\20261028-h-cat56-2-phase4\metrics\interval_top1000.json"


def cell_grid_sup(th_lo, th_hi, ph_lo, ph_hi, n):
    best = -1.0
    arg = None
    for t in np.linspace(th_lo, th_hi, n):
        for p in np.linspace(ph_lo, ph_hi, n):
            x = np.array([np.cos(t / 2), np.sin(t / 2) * np.exp(1j * p)])
            N, _ = kernel_basis(sa.phi_rows(As, S, x))
            K = N.T @ H @ N
            lam = float(np.linalg.eigvalsh(0.5 * (K + K.T))[-1])
            if lam > best:
                best, arg = lam, (float(t), float(p))
    return best, arg


def main():
    n = int(sys.argv[1])
    out = sys.argv[2]
    with open(TOP, encoding="utf-8") as fh:
        rows = json.load(fh)["rows"]
    records = []
    violations = []
    worst_ratio = (0.0, None)
    for k, r in enumerate(rows):
        th_lo, th_hi, ph_lo, ph_hi = r["cell"]
        b_up = float(r["B_up"])
        sup, arg = cell_grid_sup(th_lo, th_hi, ph_lo, ph_hi, n)
        ratio = sup / b_up
        rec = {
            "row": k,
            "cell": r["cell"],
            "B_up": b_up,
            "grid_sup": sup,
            "ratio": ratio,
            "arg": arg,
        }
        records.append(rec)
        if sup > b_up:
            violations.append(rec)
        if ratio > worst_ratio[0]:
            worst_ratio = (ratio, k)
    summary = {
        "cells_tested": len(rows),
        "grid_per_axis": n,
        "violations_sampled_M_gt_Bup": len(violations),
        "worst_ratio_sup_over_Bup": worst_ratio[0],
        "worst_row": worst_ratio[1],
        "max_grid_sup": max(r["grid_sup"] for r in records),
        "max_B_up": max(r["B_up"] for r in records),
        "violations": violations[:20],
    }
    with open(out, "w", encoding="utf-8") as fh:
        json.dump({"summary": summary, "records": records}, fh, indent=1)
    print(json.dumps({k: v for k, v in summary.items() if k != "violations"}, indent=1))


if __name__ == "__main__":
    main()
