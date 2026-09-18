"""Locate the SMALLEST feasible below-threshold configuration, and an above-threshold one.

claim.md/controls.md speak of a "(d,s) pair" below/above the Eq. (15) threshold. The
primary source does NOT make `n` a function of `(d,s)`: `n = dim V_perp - 1 = d^2-1-dim V`,
and `dim V` is a property of the sampled state (bounded by `s(s+1)r^2/2`). So the
below/above-threshold status must be MEASURED per configuration, which is what this does.
It also reports the rank `r`, which claim.md's `(d,s)` shorthand omits entirely.

Run:  python threshold_scan.py
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pcc_core as pc

OUT = Path(__file__).parent / "metrics" / "threshold_scan.json"


def probe(kind: str, dims: tuple, n_rep: int, rng: np.random.Generator) -> dict:
    rows = []
    for _ in range(n_rep):
        model = (
            pc.sample_bipartite_quasipure(*dims, rng)
            if kind == "bipartite"
            else pc.sample_generic_quasipure(*dims, rng)
        )
        if model is None:
            continue
        ana = pc.analyse(model)
        rows.append(
            {
                "d": ana.d,
                "s": ana.s,
                "r": ana.rank,
                "dim_V": ana.dim_v,
                "n": ana.n,
                "rhs_eq15": ana.rhs,
                "below_threshold": bool(ana.below_threshold),
                "pcc_holds": bool(ana.pcc_holds),
                "pcc_violation": ana.pcc_violation,
                "n_lt_d_minus_1": bool(ana.n < ana.d - 1),
                "qfim_min_eig": float(np.min(np.linalg.eigvalsh(ana.qfim))),
            }
        )
    if not rows:
        return {"kind": kind, "dims": list(dims), "samples": 0, "note": "sampler failed"}
    return {
        "kind": kind,
        "dims": list(dims),
        "samples": len(rows),
        "d": rows[0]["d"],
        "s": rows[0]["s"],
        "r": rows[0]["r"],
        "dim_V_values": sorted({r_["dim_V"] for r_ in rows}),
        "n_values": sorted({r_["n"] for r_ in rows}),
        "rhs_eq15": rows[0]["rhs_eq15"],
        "all_below_threshold": all(r_["below_threshold"] for r_ in rows),
        "all_above_threshold": all(not r_["below_threshold"] for r_ in rows),
        "all_pcc_hold": all(r_["pcc_holds"] for r_ in rows),
        "max_pcc_violation": max(r_["pcc_violation"] for r_ in rows),
        "any_n_lt_d_minus_1": any(r_["n_lt_d_minus_1"] for r_ in rows),
        "min_qfim_eig": min(r_["qfim_min_eig"] for r_ in rows),
    }


def main() -> None:
    rng = np.random.default_rng(56_20260918)
    configs = [
        ("bipartite", (2, 2, 2)),  # d=4  -- smallest Eq.(16) multiparameter case
        ("bipartite", (3, 2, 2)),  # d=6
        ("bipartite", (2, 3, 2)),  # d=6
        ("bipartite", (4, 2, 2)),  # d=8  -- the paper's own two-qubit+ancilla size
        ("bipartite", (3, 2, 3)),  # d=6, s=3
        ("bipartite", (5, 2, 2)),  # d=10 -- candidate above-threshold
        ("bipartite", (6, 2, 2)),  # d=12
        ("generic", (3, 2, 2)),  # d=3 -- smallest generic quasi-pure case at all
        ("generic", (4, 2, 2)),
        ("generic", (5, 2, 3)),
        ("generic", (6, 2, 4)),  # candidate n < d-1 counterexample regime
        ("generic", (7, 2, 4)),
        ("generic", (8, 2, 2)),  # candidate above-threshold
        ("generic", (9, 2, 2)),
        ("generic", (10, 2, 2)),
    ]
    out = [probe(k, dims, 6, rng) for k, dims in configs]
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")
    hdr = f"{'kind':10s} {'d':>3s} {'s':>2s} {'r':>2s} {'dimV':>8s} {'n':>8s} {'rhs':>6s}  status"
    print(hdr)
    for row in out:
        if row.get("samples", 0) == 0:
            print(f"{row['kind']:10s} {row['dims']}  SAMPLER FAILED")
            continue
        status = (
            "BELOW"
            if row["all_below_threshold"]
            else ("ABOVE" if row["all_above_threshold"] else "MIXED")
        )
        flag = "  n<d-1!" if row["any_n_lt_d_minus_1"] else ""
        print(
            f"{row['kind']:10s} {row['d']:3d} {row['s']:2d} {row['r']:2d} "
            f"{row['dim_V_values']!s:>8s} {row['n_values']!s:>8s} "
            f"{row['rhs_eq15']:6.1f}  {status}{flag} pcc={row['all_pcc_hold']}"
        )


if __name__ == "__main__":
    main()
