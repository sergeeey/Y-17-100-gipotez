"""run.py — H-B1-1a: r-statistic of Riemann zeta zeros vs GUE (lab positive control).

PIPELINE (pure functions, no I/O, no verdicts):   r_stat, mean_r, synthetic_gue/goe, poisson_levels,
                                                    local_unfold, mean_r_pure_python
EXPERIMENT (I/O, controls, verdicts):             cmd_controls, cmd_run, cmd_stress

Every number this script produces is written to metrics/*.json — nothing lives only in stdout.

Usage:
    python run.py controls [--seed 0]   # Step 3/4: GUE (+), GOE (discriminating), Poisson (-)
    python run.py run                   # Step 6 + 4a + no-collapse; no PASS over failed controls
    python run.py stress                # Step 7
Constants: Atas, Bogomolny, Giraud, Roux, PRL 110, 084101 (2013), arXiv:1212.5611.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
import time
from itertools import pairwise
from pathlib import Path

import numpy as np
import requests

HERE = Path(__file__).resolve().parent
DATA = HERE / "data" / "zeros1.txt"
METRICS = HERE / "metrics"
URL = "https://www-users.cse.umn.edu/~odlyzko/zeta_tables/zeros1"

R_POISSON = 2 * math.log(2) - 1  # 0.386294
R_GOE = 4 - 2 * math.sqrt(3)  # 0.535898 (3x3 surmise)
R_GUE = 2 * math.sqrt(3) / math.pi - 0.5  # 0.602660 (3x3 surmise) — PRIMARY TARGET
TOL = 0.01  # kill tolerance == MCID
EXPECTED_COUNT = 100_000
FIRST_ZERO = 14.134725  # gamma_1 to 6 dp — guards against HTML-as-data


# ───────────────────────────── PIPELINE ─────────────────────────────
def r_stat(levels: np.ndarray) -> np.ndarray:
    """r_n = min(s_n, s_{n+1}) / max(s_n, s_{n+1}). Raises on non-positive spacing (ICE: abort)."""
    s = np.diff(np.asarray(levels, dtype=float))
    if s.size < 2:
        raise ValueError("need >= 3 levels")
    if np.any(s <= 0):
        bad = int(np.argmax(s <= 0))
        raise ValueError(
            f"non-positive spacing at index {bad}: data corrupted/misordered — aborting"
        )
    return np.minimum(s[:-1], s[1:]) / np.maximum(s[:-1], s[1:])


def mean_r(levels: np.ndarray) -> float:
    return float(r_stat(levels).mean())


def mean_r_pure_python(levels) -> float:
    """Independent implementation (alternative tool) — plain loops, no numpy."""
    lv = [float(x) for x in levels]
    s = [b - a for a, b in pairwise(lv)]
    if any(x <= 0 for x in s):
        raise ValueError("non-positive spacing")
    rs = [min(a, b) / max(a, b) for a, b in pairwise(s)]
    return sum(rs) / len(rs)


def local_unfold(levels: np.ndarray, window: int = 501) -> np.ndarray:
    """Convention flip: divide spacings by a sliding-window mean; return unfolded levels."""
    s = np.diff(levels)
    kernel = np.ones(window) / window
    local_mean = np.convolve(s, kernel, mode="same")
    return np.concatenate([[0.0], np.cumsum(s / local_mean)])


def synthetic_bulk_eigs(n: int, matrices: int, rng: np.random.Generator, beta: int) -> np.ndarray:
    """Central 50% eigenvalues of `matrices` random matrices of size n (beta=1 GOE, beta=2 GUE)."""
    out = []
    for _ in range(matrices):
        if beta == 2:
            a = rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))
            h = (a + a.conj().T) / 2
        else:
            a = rng.standard_normal((n, n))
            h = (a + a.T) / math.sqrt(2)
        ev = np.linalg.eigvalsh(h)
        out.append(ev[n // 4 : 3 * n // 4])  # bulk only — edges have different statistics
    return np.array(out)


def ensemble_mean_r(bulks: np.ndarray) -> tuple[float, float]:
    rs = np.concatenate([r_stat(b) for b in bulks])
    return float(rs.mean()), float(rs.std(ddof=1) / math.sqrt(rs.size))


def poisson_levels(n: int, rng: np.random.Generator) -> np.ndarray:
    return np.cumsum(rng.exponential(1.0, n))


def shuffled_spacings(levels: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Keep P(s), destroy spacing correlations."""
    s = np.diff(levels)
    return np.concatenate([[0.0], np.cumsum(rng.permutation(s))])


# ───────────────────────────── EXPERIMENT ─────────────────────────────
def _write(name: str, payload: dict) -> None:
    METRICS.mkdir(exist_ok=True)
    payload["_written"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    (METRICS / name).write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"→ metrics/{name}")


def in_band(x: float) -> bool:
    return abs(x - R_GUE) < TOL


def load_zeros() -> tuple[np.ndarray, str]:
    if not DATA.exists():
        DATA.parent.mkdir(exist_ok=True)
        resp = requests.get(URL, timeout=120)
        resp.raise_for_status()
        DATA.write_text(resp.text, encoding="utf-8")
    raw = DATA.read_text(encoding="utf-8")
    sha = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    zeros = np.array([float(x) for x in raw.split()])
    # A4 — artifact identity (Gate 1)
    if zeros.size != EXPECTED_COUNT:
        raise RuntimeError(
            f"BLOCKED-INFRASTRUCTURE: expected {EXPECTED_COUNT} zeros, got {zeros.size}"
        )
    if abs(zeros[0] - FIRST_ZERO) > 1e-5:
        raise RuntimeError(f"BLOCKED-INFRASTRUCTURE: first zero {zeros[0]} != {FIRST_ZERO}")
    if np.any(np.diff(zeros) <= 0):
        raise RuntimeError("BLOCKED-INFRASTRUCTURE: zeros not strictly increasing")
    return zeros, sha


def cmd_controls(seed: int) -> dict:
    rng = np.random.default_rng(seed)
    n, m = 400, 500  # 500 matrices x 200 bulk eigenvalues ~ 1e5 ratios, comparable to the data
    gue = synthetic_bulk_eigs(n, m, rng, beta=2)
    goe = synthetic_bulk_eigs(n, m, rng, beta=1)
    poi = poisson_levels(EXPECTED_COUNT, rng)
    gue_r, gue_se = ensemble_mean_r(gue)
    goe_r, goe_se = ensemble_mean_r(goe)
    poi_r = mean_r(poi)
    shuf_gue_r = float(np.mean([mean_r(shuffled_spacings(b, rng)) for b in gue]))

    positive_pass = in_band(gue_r)
    negative_pass = not in_band(poi_r)  # the kill criterion MUST fire on Poisson
    goe_separated = abs(goe_r - gue_r) > TOL  # metric can tell beta=1 from beta=2
    out = {
        "seed": seed,
        "matrix_size": n,
        "matrices": m,
        "positive_control_gue": {
            "mean_r": gue_r,
            "se": gue_se,
            "target_surmise": R_GUE,
            "result": "PASS" if positive_pass else "FAIL",
        },
        "discriminating_control_goe": {
            "mean_r": goe_r,
            "se": goe_se,
            "surmise": R_GOE,
            "separated_from_gue": goe_separated,
            "result": "PASS" if goe_separated else "FAIL",
        },
        "negative_control_poisson": {
            "mean_r": poi_r,
            "analytic": R_POISSON,
            "kill_criterion_fired": negative_pass,
            "result": "PASS" if negative_pass else "FAIL",
        },
        "shuffled_gue_spacings": {
            "mean_r": shuf_gue_r,
            "note": "P(s) kept, correlations destroyed",
        },
        "floor_ceiling": {
            "floor_poisson": R_POISSON,
            "ceiling_surmise": R_GUE,
            "ceiling_empirical_gue": gue_r,
            "pass_band": [R_GUE - TOL, R_GUE + TOL],
            "criterion_valid": not in_band(R_POISSON),
            "task_feasible": in_band(gue_r),
            "headroom": R_GUE - R_POISSON,
        },
        "all_controls_pass": positive_pass and negative_pass and goe_separated,
    }
    _write("controls.json", out)
    return out


def cmd_run(seed: int) -> dict:
    ctrl_path = METRICS / "controls.json"
    if not ctrl_path.exists():
        raise RuntimeError("run controls first (Step 3/4 before Step 6)")
    ctrl = json.loads(ctrl_path.read_text(encoding="utf-8"))
    rng = np.random.default_rng(seed)
    zeros, sha = load_zeros()

    r_all = mean_r(zeros)
    r_first, r_last = mean_r(zeros[: EXPECTED_COUNT // 2]), mean_r(zeros[EXPECTED_COUNT // 2 :])
    r_unfolded = mean_r(local_unfold(zeros))
    mean_s = float(np.diff(zeros).mean())
    r_noisy = mean_r(np.sort(zeros + rng.normal(0, 0.1 * mean_s, zeros.size)))
    r_scaled = (mean_r(zeros * 0.1), mean_r(zeros * 10.0))
    r_pure = mean_r_pure_python(zeros)
    r_shuffled = mean_r(shuffled_spacings(zeros, rng))
    se = float(r_stat(zeros).std(ddof=1) / math.sqrt(zeros.size - 2))

    efficiency = (r_all - R_POISSON) / (R_GUE - R_POISSON)
    passed = in_band(r_all)
    verdict = "PASS" if passed else "KILLED"
    if not ctrl["all_controls_pass"]:
        verdict = "CONTROLS_FAILED"  # STPA mitigation: never PASS over failed controls

    no_collapse = {
        "data_swap_halves": {
            "first_50k": r_first,
            "last_50k": r_last,
            "result": "PASS" if in_band(r_first) and in_band(r_last) else "FAIL",
        },
        "noise_injection_10pct": {
            "mean_r": r_noisy,
            "result": "PASS" if r_noisy > 0.5 else "FAIL",
        },
        "scale_x0.1_x10": {
            "values": r_scaled,
            "result": "PASS" if max(abs(v - r_all) for v in r_scaled) < 1e-12 else "FAIL",
        },
        "convention_flip_local_unfold": {
            "mean_r": r_unfolded,
            "delta": r_unfolded - r_all,
            "result": "PASS" if abs(r_unfolded - r_all) < 0.002 else "FAIL",
        },
        "negative_control": {
            "see": "controls.json",
            "result": ctrl["negative_control_poisson"]["result"],
        },
        "adversarial_shuffled_spacings": {
            "mean_r_zeta_shuffled": r_shuffled,
            "mean_r_gue_shuffled": ctrl["shuffled_gue_spacings"]["mean_r"],
            "note": "reported, not gated — tests P(s) equality independent of correlations",
            "result": "REPORTED",
        },
        "alternative_tool_pure_python": {
            "mean_r": r_pure,
            "result": "PASS" if abs(r_pure - r_all) < 1e-12 else "FAIL",
        },
    }
    out = {
        "data": {
            "url": URL,
            "sha256": sha,
            "count": int(zeros.size),
            "first_zero": float(zeros[0]),
        },
        "r_mean": r_all,
        "se": se,
        "target_surmise": R_GUE,
        "delta_to_surmise": r_all - R_GUE,
        "delta_to_empirical_gue": r_all - ctrl["positive_control_gue"]["mean_r"],
        "tolerance": TOL,
        "efficiency": efficiency,
        # WHY: added after skeptic Step 8a (2026-09-06) — efficiency outside [0, 1] was silently
        # absorbed into PASS. Not a claim change: verdict untouched; this only names the anomaly.
        "ceiling_check": (
            "CEILING_MISSPECIFIED: efficiency > 1 — observed exceeds the privileged answer; "
            "the ceiling's population (N->inf GUE) != measured population (finite height)"
            if efficiency > 1
            else "FLOOR_MISSPECIFIED: efficiency < 0"
            if efficiency < 0
            else "OK"
        ),
        "verdict": verdict,
        "no_collapse": no_collapse,
    }
    _write("run.json", out)
    return out


def cmd_stress() -> dict:
    zeros, _ = load_zeros()
    # 1 — low-height regime: first 1000 zeros only (reported; no PASS threshold claimed in claim.md)
    r_1000 = mean_r(zeros[:1000])
    # 2 — injected duplicate zero must abort, not silently bias
    corrupted = zeros.copy()
    corrupted[500] = corrupted[499]
    try:
        mean_r(corrupted)
        dup = {"result": "FAIL", "note": "duplicate zero was NOT rejected"}
    except ValueError as e:
        dup = {"result": "PASS", "note": str(e)}
    # 3 — parser robustness: CRLF + trailing blank lines must give identical array
    raw = DATA.read_text(encoding="utf-8")
    mangled = raw.replace("\n", "\r\n") + "\r\n\r\n   \r\n"
    z2 = np.array([float(x) for x in mangled.split()])
    parse = {"result": "PASS" if z2.size == zeros.size and np.allclose(z2, zeros) else "FAIL"}
    out = {
        "case1_first_1000_zeros": {
            "mean_r": r_1000,
            "delta_to_surmise": r_1000 - R_GUE,
            "result": "REPORTED",
        },
        "case2_duplicate_zero_aborts": dup,
        "case3_crlf_parse": parse,
    }
    _write("stress.json", out)
    return out


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("cmd", choices=["controls", "run", "stress"])
    p.add_argument("--seed", type=int, default=0)
    a = p.parse_args(argv)
    res = {
        "controls": lambda: cmd_controls(a.seed),
        "run": lambda: cmd_run(a.seed),
        "stress": cmd_stress,
    }[a.cmd]()
    print(json.dumps(res, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
