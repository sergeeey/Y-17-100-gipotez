"""ADVERSARIAL PREFIX CHECK (controls.md negative control) -- the control this
whole experiment exists to add.

The per-horizon optima found by the positive control are the ALREADY-PUBLISHED
Das Gupta setting.  If their first k entries happened to coincide across horizons,
the per-horizon result would secretly already be an anytime schedule, and this
experiment's prefix constraint would be testing nothing new.  Expected outcome:
the prefixes differ.  Coincidence is escalated, not absorbed.

Two independent probes of the same question:

A. NUMERIC -- pairwise comparison of the first k stepsizes.
B. FUNCTIONAL -- take the n=50 optimum, truncate to length n', and evaluate
   R_{n'} on it.  If the prefixes really coincided, this truncation would be
   optimal at n' too.  This probe cannot be fooled by cosmetic reparametrisation
   and does not reuse probe A's arithmetic.

Run (after pep_unconstrained_baseline.py):  python check_prefix_consistency.py
"""

from __future__ import annotations

import json
import warnings
from pathlib import Path

import numpy as np
from pep_core import GDPep

warnings.filterwarnings("ignore")

HERE = Path(__file__).parent
OUT = HERE / "metrics"
K_PREFIX = 10
COINCIDE_TOL = 1e-3  # relative; anything below this counts as "the same prefix"


# Cheaper self-contained horizons, used when the pre-registered positive control at
# n in {10,...,50} has not finished.  The control's question -- do per-horizon optima
# share a prefix? -- does not depend on the horizons being large, only on their being
# several and distinct.
FALLBACK_HORIZONS = [6, 10, 14, 18]


def compute_own_optima() -> dict:
    """Per-horizon optima computed here, so this control never depends on another run."""
    from optimizer import PepCache, optimize_per_horizon
    from pep_core import constant_schedule, silver_prefix, zldc_anytime_schedule

    cache = PepCache("R")
    out = {}
    for n in FALLBACK_HORIZONS:
        starts = [
            np.array(zldc_anytime_schedule(n)),
            np.array(silver_prefix(n)),
            np.array(constant_schedule(n, 1.5)),
        ]
        best = optimize_per_horizon(n, cache, starts, maxiter=120)
        out[str(n)] = {"value": best["value"], "schedule": best["schedule"]}
        print(f"  own optimum n={n}: R_n={best['value']:.6e}", flush=True)
    return {"per_horizon_optimum": out, "source": "computed in check_prefix_consistency.py"}


def main() -> None:
    pc = OUT / "positive_control.json"
    if pc.exists():
        src = json.loads(pc.read_text())
        src.setdefault("source", "pep_unconstrained_baseline.py")
    else:
        print("positive_control.json absent -- computing own per-horizon optima", flush=True)
        src = compute_own_optima()
    opts = {int(k): np.array(v["schedule"]) for k, v in src["per_horizon_optimum"].items()}
    horizons = sorted(opts)

    # -- probe A: numeric pairwise prefix comparison -------------------------
    pairs = []
    for a in range(len(horizons)):
        for b in range(a + 1, len(horizons)):
            na, nb = horizons[a], horizons[b]
            k = min(K_PREFIX, na, nb)
            pa, pb = opts[na][:k], opts[nb][:k]
            rel = float(np.max(np.abs(pa - pb) / np.maximum(np.abs(pa), 1e-12)))
            pairs.append(
                {
                    "n_a": na,
                    "n_b": nb,
                    "k": k,
                    "max_rel_diff": rel,
                    "max_abs_diff": float(np.max(np.abs(pa - pb))),
                    "coincide": bool(rel < COINCIDE_TOL),
                }
            )

    # -- probe B: functional truncation test ---------------------------------
    n_max = horizons[-1]
    functional = []
    for n in horizons[:-1]:
        trunc = opts[n_max][:n]
        val_trunc = float(GDPep(n, "R").solve(trunc).value)
        val_opt = float(src["per_horizon_optimum"][str(n)]["value"])
        functional.append(
            {
                "n": n,
                "R_n_of_truncated_n50_optimum": val_trunc,
                "R_n_of_own_optimum": val_opt,
                "excess_ratio": val_trunc / val_opt,
            }
        )

    any_coincide = any(p["coincide"] for p in pairs)
    functional_coincide = all(f["excess_ratio"] < 1.0 + COINCIDE_TOL for f in functional)

    report = {
        "optima_source": src.get("source", "unknown"),
        "k_prefix": K_PREFIX,
        "coincidence_tolerance_relative": COINCIDE_TOL,
        "probe_A_pairwise_numeric": pairs,
        "probe_B_functional_truncation": functional,
        "first_k_of_each_optimum": {
            str(n): [round(float(v), 5) for v in opts[n][: min(K_PREFIX, n)]] for n in horizons
        },
        "any_pair_coincides": bool(any_coincide),
        "functional_prefixes_equivalent": bool(functional_coincide),
        # PASS == "prefixes differ", i.e. per-horizon is NOT secretly anytime,
        # which is the expected and non-surprising outcome.
        "RESULT": "FAIL_ESCALATE" if (any_coincide or functional_coincide) else "PASS",
    }
    (OUT / "prefix_consistency_check.json").write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
