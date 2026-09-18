"""No-Collapse Tests (controls.md, Perelman-audit stability checklist).

Four tests are run here; the remaining three are produced by other scripts and
merely referenced:

  * negative control / adversarial input -> check_prefix_consistency.py
  * alternative tool (PEPit)             -> substrate_check.py

Each test re-runs the SAME prefix-consistent search procedure under a legal
perturbation and asks whether the VERDICT survives, not whether the number is
identical.  A result that only exists for one horizon split, one seed, one
training-set size or one objective is an artefact.

Run (after pep_prefix_search.py):  python no_collapse_tests.py
"""

from __future__ import annotations

import json
import time
import warnings
from pathlib import Path

import numpy as np
from optimizer import PepCache, optimize_prefix_consistent
from pep_core import constant_schedule, silver_prefix, zldc_anytime_schedule

warnings.filterwarnings("ignore")

OUT = Path(__file__).parent / "metrics"
PASS_RATIO = 1.0 / 1.05


def run_case(
    name: str,
    n_train: list[int],
    n_test: list[int],
    objective: str,
    seed: int,
    maxiter: int = 20,
    n_starts: int = 2,
) -> dict:
    # WHY this budget: each case is a full prefix-consistent search (one exact SDP per
    # horizon per function evaluation).  The question a no-collapse test asks is whether
    # the VERDICT survives a legal perturbation, not whether the optimum is refined --
    # and a smaller budget can only make a PASS harder, never easier, so it cannot
    # manufacture the FAIL these cases are checking for stability.
    cache = PepCache(objective)
    k = max(n_train + n_test)
    zl = np.array(zldc_anytime_schedule(k))
    base = {n: float(cache.value(zl[:n]).value) for n in sorted(set(n_train + n_test))}

    rng = np.random.default_rng(seed)
    starts = [
        zl,
        np.array(silver_prefix(k)),
        np.array(constant_schedule(k, 1.5)),
        np.clip(zl * rng.uniform(0.6, 1.6, size=k), 0.05, 50.0),
        np.clip(zl * rng.uniform(0.4, 2.2, size=k), 0.05, 50.0),
    ][:n_starts]

    t0 = time.time()
    best = optimize_prefix_consistent(
        n_train, {n: base[n] for n in n_train}, cache, starts,
        betas=(40.0, 150.0), maxiter=maxiter
    )
    master = np.array(best["master"])
    ratios = {n: float(cache.value(master[:n]).value / base[n]) for n in base}
    train_r = {n: ratios[n] for n in n_train}
    test_r = {n: ratios[n] for n in n_test}
    verdict = (
        "PASS"
        if all(r <= PASS_RATIO for r in train_r.values())
        and all(r <= PASS_RATIO for r in test_r.values())
        else "FAIL"
    )
    return {
        "name": name,
        "objective": objective,
        "N_train": n_train,
        "N_test": n_test,
        "seed": seed,
        "ratios": {str(n): round(v, 5) for n, v in ratios.items()},
        "worst_train_ratio": max(train_r.values()),
        "worst_test_ratio": max(test_r.values()),
        "VERDICT": verdict,
        "master_schedule": [round(float(v), 6) for v in master],
        "seconds": round(time.time() - t0, 1),
    }


def main() -> None:
    cases = [
        # 1. Data swap: a completely different (disjoint-ish) horizon split.
        run_case("data_swap", [3, 7, 13, 17, 21], [4, 9, 14, 19, 23], "R", seed=11),
        # 2. Noise injection: PEP is deterministic worst-case optimisation, so the
        #    legal analogue is perturbing the optimiser's starting point.
        run_case(
            "noise_injection_seed_a", [4, 8, 12, 16, 20, 24], [5, 7, 11, 15, 19, 23], "R", 101
        ),
        run_case(
            "noise_injection_seed_b", [4, 8, 12, 16, 20, 24], [5, 7, 11, 15, 19, 23], "R", 202
        ),
        # 3. Scale variation: much smaller and much larger training sets.
        run_case("scale_small_train", [6, 16], [4, 8, 12, 20, 24], "R", seed=31),
        run_case(
            "scale_large_train",
            [4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24],
            [5, 9, 13, 17, 21, 23],
            "R",
            seed=41,
            maxiter=15,
        ),
        # 4. Convention flip: squared gradient norm G_n instead of function value R_n
        #    (different rate class per Tsai et al. Theorem 1.2).
        run_case("convention_flip_Gn", [4, 8, 12, 16, 20], [6, 10, 14, 18], "G", seed=51),
    ]
    report = {
        "pass_ratio_threshold": PASS_RATIO,
        "cases": cases,
        "summary": {c["name"]: c["VERDICT"] for c in cases},
    }
    (OUT / "no_collapse_tests.json").write_text(json.dumps(report, indent=2))
    for c in cases:
        print(
            f"{c['name']:<24} {c['VERDICT']:<5} "
            f"worst_train={c['worst_train_ratio']:.4f} worst_test={c['worst_test_ratio']:.4f} "
            f"({c['seconds']}s)"
        )


if __name__ == "__main__":
    main()
