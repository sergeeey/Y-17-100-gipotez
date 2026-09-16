"""Point 83's decisive test: measure the FULL ||x*||^2 / ||w*||^2 per row, not just one
coordinate (x_i/w_i at GEN_INDEX=1, as ppl_gate_pilot.py's canonical rows store).

Why: Point 83 (decision.md) found that the single-coordinate proxy m*E[x_i^2] cannot
distinguish (POL) (sup_n E||x*||^2 < infinity, slope a=0) from the same slow power-law growth
(a~0.04-0.05) already measured in three OTHER independent series in this project (Var(X_n),
J_n, K_n slopes). The single-coordinate estimator's SE is too wide (95% CI on the slope was
[-0.045, 0.062]) to resolve this. The full vector norm -- already computed by the same LP
solve, just not persisted -- is a materially tighter estimator of E||x*||^2 (each row's own
||x||^2 is itself an average over m coordinates, not a single one), and should cut the SE
enough to actually tell a=0 apart from a~0.04-0.05.

This script does NOT touch ppl_gate_pilot.json or its own pipeline -- it is a separate,
read-only-of-existing-code, write-only-to-its-own-output script, per this project's own
convention of not silently mutating an already skeptic-reviewed, decision-relevant artifact.
It reuses the exact same LP solver, sampling protocol, and seed scheme as ppl_gate_pilot.py's
one_case() (SEED_BASE=3351000, seed = SEED_BASE + n*100_000 + rep, GEN_INDEX=1) so that:
  (a) the computed x_i/w_i at GEN_INDEX should reproduce ppl_gate_pilot.json's existing rows
      EXACTLY (a free positive control, checked at the end of each n's block, not just assumed);
  (b) the new x_norm_sq/w_norm_sq values are paired with the exact same random draws already
      analyzed elsewhere in this project, not a fresh, uncomparable sample.

Output: metrics/pol_full_norm_check.json, written incrementally (after each n completes, and
flushed) so a crash does not lose completed n's -- same lesson this session already learned the
hard way with the n=2039 extension's silent background-capture failures.
"""

from __future__ import annotations

import importlib.util
import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
CODEX_DIR = HERE / "codex-20260914-susceptibility"
H_CAT31_1_DIR = HERE.parent / "20260909-lovasz-theta-random-circulant-graphs"
sys.path.insert(0, str(CODEX_DIR))

from test_convolution_repair import CertificateLP  # noqa: E402  (path set above)


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_h_cat31_1 = _load_module("pol_full_norm_dep_h_cat31_1", H_CAT31_1_DIR / "run.py")
sample_circulant_neighbors = _h_cat31_1.sample_circulant_neighbors  # canonical, unmodified


def flip_generator(c: np.ndarray, i: int) -> np.ndarray:
    """Character-for-character identical to ppl_gate_pilot.py's own flip_generator."""
    n = len(c)
    c2 = c.copy()
    c2[i] = 1.0 - c2[i]
    c2[n - i] = 1.0 - c2[n - i]
    return c2


GEN_INDEX = 1  # matches ppl_gate_pilot.py's GEN_INDEX, TEST_GENERATOR_INDEX elsewhere
SEED_BASE = 3351000  # matches ppl_gate_pilot.py's SEED_BASE -- same seeds, paired comparison
SIZES_REPS = ((127, 500), (509, 500), (1021, 500), (2039, 500))

# Free positive control: the existing canonical JSON's x_i/w_i at these same seeds, to confirm
# this script's LP solves reproduce the already-validated pipeline before trusting the new field.
EXISTING_JSON = HERE / "metrics" / "ppl_gate_pilot.json"


def one_case(n: int, seed: int) -> dict:
    lp = CertificateLP(n)
    m = lp.m
    assert m == (n - 1) // 2

    c = sample_circulant_neighbors(n, 0.5, seed)
    c_flip = flip_generator(c, GEN_INDEX)

    if c[GEN_INDEX] < 0.5:
        branch = "A"
        c_g0, c_g1 = c, c_flip
    else:
        branch = "B"
        c_g0, c_g1 = c_flip, c

    bits_g0 = c_g0[1 : m + 1].astype(int)
    bits_g1 = c_g1[1 : m + 1].astype(int)
    assert bits_g0[GEN_INDEX - 1] == 0
    assert bits_g1[GEN_INDEX - 1] == 1

    g0 = lp.solve(bits_g0)
    comp = lp.solve(1 - bits_g1)  # complement(G1), same construction as ppl_gate_pilot.py

    x_vec = np.asarray(g0["x"], dtype=float)
    w_vec = np.asarray(comp["x"], dtype=float)

    x_i = float(x_vec[GEN_INDEX])
    w_i = float(w_vec[GEN_INDEX])

    return {
        "n": n,
        "seed": seed,
        "branch": branch,
        "x_i": x_i,  # for the positive-control cross-check against existing JSON
        "w_i": w_i,
        "x_norm_sq": float(np.sum(x_vec**2)),  # ||x*||^2, the decisive new field
        "w_norm_sq": float(np.sum(w_vec**2)),  # ||w*||^2
        "x_dim": int(x_vec.shape[0]),
        "w_dim": int(w_vec.shape[0]),
    }


def positive_control(n: int, rows: list[dict]) -> dict:
    """Cross-check x_i/w_i against the existing canonical JSON's rows for the same (n, seed) --
    a free confirmation this script's LP solves reproduce the already-validated pipeline, not a
    new/different one, before the new x_norm_sq/w_norm_sq fields are trusted for anything.
    """
    if not EXISTING_JSON.exists():
        return {"checked": False, "note": "existing ppl_gate_pilot.json not found"}
    with open(EXISTING_JSON, encoding="utf-8") as f:
        existing = json.load(f)
    existing_rows = {r["seed"]: r for r in existing["rows_by_n"].get(str(n), [])}
    max_x_diff = 0.0
    max_w_diff = 0.0
    n_matched = 0
    for row in rows:
        ex = existing_rows.get(row["seed"])
        if ex is None:
            continue
        n_matched += 1
        max_x_diff = max(max_x_diff, abs(row["x_i"] - ex["x_i"]))
        max_w_diff = max(max_w_diff, abs(row["w_i"] - ex["w_i"]))
    return {
        "checked": True,
        "n_matched": n_matched,
        "n_rows": len(rows),
        "max_abs_diff_x_i": max_x_diff,
        "max_abs_diff_w_i": max_w_diff,
        "passed": n_matched > 0 and max_x_diff < 1e-6 and max_w_diff < 1e-6,
    }


def main() -> None:
    t_start = time.time()
    out_path = HERE / "metrics" / "pol_full_norm_check.json"
    results: dict = {"sizes_reps": {str(n): r for n, r in SIZES_REPS}, "by_n": {}}

    for n, reps in SIZES_REPS:
        t_n_start = time.time()
        rows = []
        for rep in range(reps):
            seed = SEED_BASE + n * 100_000 + rep
            rows.append(one_case(n, seed))
            if (rep + 1) % 25 == 0 or rep == reps - 1:
                elapsed = time.time() - t_n_start
                print(
                    f"n={n} rep={rep + 1}/{reps} elapsed={elapsed:.1f}s "
                    f"({elapsed / (rep + 1):.2f}s/rep)",
                    flush=True,
                )

        pc = positive_control(n, rows)
        x_norm = np.array([r["x_norm_sq"] for r in rows])
        w_norm = np.array([r["w_norm_sq"] for r in rows])

        results["by_n"][str(n)] = {
            "n": n,
            "reps": reps,
            "positive_control_vs_existing_json": pc,
            "mean_x_norm_sq": float(x_norm.mean()),
            "se_x_norm_sq": float(x_norm.std(ddof=1) / np.sqrt(len(x_norm))),
            "mean_w_norm_sq": float(w_norm.mean()),
            "se_w_norm_sq": float(w_norm.std(ddof=1) / np.sqrt(len(w_norm))),
            "rows": rows,
        }

        with open(out_path, "w", encoding="utf-8", newline="\n") as f:
            json.dump(results, f, indent=2)
        se_x = x_norm.std(ddof=1) / np.sqrt(len(x_norm))
        print(
            f"n={n} DONE: mean||x*||^2={x_norm.mean():.4f} SE={se_x:.4f}  "
            f"positive_control_passed={pc.get('passed')}  -- written to {out_path}",
            flush=True,
        )

    results["elapsed_seconds"] = time.time() - t_start
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(results, f, indent=2)
    print(f"ALL DONE in {results['elapsed_seconds']:.1f}s", flush=True)


if __name__ == "__main__":
    main()
