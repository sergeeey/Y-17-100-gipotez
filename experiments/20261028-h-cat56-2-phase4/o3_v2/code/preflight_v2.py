"""Preflight for O3 v2: positive control, negative tests of the kernel certificate, comparison with v1.

Writes metrics/preflight_v2.json. Exit code 0 only if every check holds:
  - all test cells are CERTIFIED with slack > 0 (positive control);
  - every negative test is REJECTED by kernel_certificate (or by an exception in building the projector);
  - B_up of the 200 closest cells equals the stored v1 value (same formulas, certified path).
Negative tests change the kernel basis AFTER the exact projector (not the float starting vectors).
"""

import json
import os
import sys

os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

import numpy as np  # noqa: E402
from flint import arb, arb_mat  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
O3 = os.path.normpath(os.path.join(HERE, ".."))
PHASE4 = os.path.normpath(os.path.join(O3, ".."))
sys.path.insert(0, HERE)
import interval_cells_v2 as ivl  # noqa: E402

LEAVES = os.path.join(O3, "inputs", "leaves.npy")
TOP = os.path.join(PHASE4, "metrics", "interval_top1000.json")
OUT = os.path.join(O3, "metrics", "preflight_v2.json")


def _matrix(rows, cols, fn):
    return arb_mat(rows, cols, [fn(i, j) for i in range(rows) for j in range(cols)])


def _variant_z(Z0, fn):
    return _matrix(40, 4, lambda i, k: fn(i, k, Z0[i, k]))


def main():
    rows_top = sorted(json.load(open(TOP, encoding="utf-8"))["rows"], key=lambda r: r["slack"])
    leaves = np.load(LEAVES, mmap_mode="r")
    rng = np.random.default_rng(7)
    rand_idx = sorted(rng.choice(len(leaves), size=100, replace=False).tolist())

    test_cells = [(r["cell"], r["B_up"]) for r in rows_top[:200]]
    test_cells += [(leaves[i].tolist(), None) for i in rand_idx]

    report = {
        "R_hermitian_exact": ivl.R_HERMITIAN_EXACT,
        "final_gap_positive": bool(ivl.final_gap > 0),
        "final_gap": float(ivl.final_gap),
        "s_target": float(ivl.s_target_f),
        "positive_control": {},
        "negative_tests": {},
    }

    certified = 0
    slack_ok = 0
    cert_fail = []
    max_diff_v1 = 0.0
    min_slack = None
    for k, (cell, v1_bup) in enumerate(test_cells):
        r = ivl.cell_bound([float(x) for x in cell])
        if r["status"] != "OK":
            cert_fail.append(
                {"idx": k, "cell": cell, "status": r["status"], "reasons": r.get("reasons")}
            )
            continue
        certified += 1
        if ivl.s_target - r["B_up"] > 0:
            slack_ok += 1
        sl = float(ivl.s_target - r["B_up"])
        min_slack = sl if min_slack is None else min(min_slack, sl)
        if v1_bup is not None:
            max_diff_v1 = max(max_diff_v1, abs(float(r["B_up"]) - float(v1_bup)))
    report["positive_control"] = {
        "cells": len(test_cells),
        "certified": certified,
        "slack_positive": slack_ok,
        "cert_fail_sample": cert_fail[:20],
        "min_slack": min_slack,
        "max_abs_diff_B_up_vs_v1_top200": max_diff_v1,
    }

    # Negative tests on the cell with the smallest stored slack (kernel and lambda_K must not be certified)
    cell0 = [float(x) for x in rows_top[0]["cell"]]
    b = ivl.build_cell(cell0)
    Phi0, G, P, Z0 = b["Phi0"], b["G"], b["P"], b["Z0"]
    neg = report["negative_tests"]

    def record(name, fails, extra=None):
        neg[name] = {"rejected": bool(fails), "reasons": fails}
        if extra:
            neg[name].update(extra)

    # N0: genuine data must pass (control for the negatives)
    record("N0_genuine_control", ivl.kernel_certificate(Phi0, G, P, Z0))

    # N1: one kernel column replaced by a unit vector (not in ker Phi0)
    Z_n1 = _variant_z(
        Z0, lambda i, k, v: arb(1) if (i == 0 and k == 0) else (arb(0) if k == 0 else v)
    )
    record("N1_column_not_in_kernel", ivl.kernel_certificate(Phi0, G, P, Z_n1))

    # N2: two identical columns (dependent basis)
    Z_n2 = _variant_z(Z0, lambda i, k, v: Z0[i, 0] if k == 1 else v)
    record("N2_dependent_columns", ivl.kernel_certificate(Phi0, G, P, Z_n2))

    # N3: basis scaled by 2 (not orthonormal; lambda_K computed from it would be off by a factor 4)
    Z_n3 = _variant_z(Z0, lambda i, k, v: 2 * v)
    record("N3_not_orthonormal_scaled", ivl.kernel_certificate(Phi0, G, P, Z_n3))

    # N4: rank-deficient Phi0 (row 35 := row 34). G singular -> certificate (a) must fail
    Phi_n4 = _matrix(36, 40, lambda i, j: Phi0[34, j] if i == 35 else Phi0[i, j])
    G_n4 = Phi_n4 * Phi_n4.transpose()
    det_lo = float(G_n4.det().lower())
    try:
        Pinv_n4 = Phi_n4.transpose() * G_n4.inv()
        P_n4 = ivl.I40 - Pinv_n4 * Phi_n4
        fails4 = ivl.kernel_certificate(Phi_n4, G_n4, P_n4, Z0)
        record("N4_rank_deficient_Phi0", fails4, {"det_lower": det_lo})
    except Exception as exc:  # singular inverse: the pipeline must refuse, not certify
        record(
            "N4_rank_deficient_Phi0",
            [f"exception while building projector: {type(exc).__name__}: {exc}"],
            {"det_lower": det_lo},
        )

    # N5: zero column (rank drop of the basis)
    Z_n5 = _variant_z(Z0, lambda i, k, v: arb(0) if k == 2 else v)
    record("N5_zero_column", ivl.kernel_certificate(Phi0, G, P, Z_n5))

    neg_ok = (
        all(v["rejected"] for key, v in neg.items() if key != "N0_genuine_control")
        and not neg["N0_genuine_control"]["rejected"]
    )
    report["negatives_all_rejected_and_control_passes"] = bool(neg_ok)
    # WHY: v2 uses the exact (arb) Hermitian part of R, v1 the float one: B_up may differ at ~1e-16 level only
    pos_ok = certified == len(test_cells) and slack_ok == len(test_cells) and max_diff_v1 <= 1e-12
    report["positive_control_all_pass"] = bool(pos_ok)
    report["verdict"] = (
        "PREFLIGHT_OK" if (pos_ok and neg_ok and report["final_gap_positive"]) else "PREFLIGHT_FAIL"
    )

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=1, default=float)
    print(json.dumps(report, indent=1, default=float))
    sys.exit(0 if report["verdict"] == "PREFLIGHT_OK" else 1)


if __name__ == "__main__":
    main()
