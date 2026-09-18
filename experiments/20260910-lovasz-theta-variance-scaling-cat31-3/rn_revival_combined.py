"""
H-CAT31-3 PARK revival plan for C1/C2/C3 (lambda_n / R_n scaling), executed
verbatim per Point 95's own named 4-step plan (decision.md Point 95, Revival
condition):
  1. Combine OLD (200/150/80-rep) and NEW (800/600/160-rep) draws via
     inverse-variance weighting at each n=509,1021,2039.
  2. Equalize rep counts across all three n (800 at all three, not tapering
     to 160 at n=2039).
  3. Reformulate as a 95% CI on the scaling exponent b in n*R_n ~ n^b, with a
     pre-registered stopping rule (stated below) to exclude b=1.
  4. Use a bootstrap-based (not normal-approximation) CI for n*R_n itself,
     since it sits near a boundary (0) and is visibly skewed.

Reuses check_first_chaos_decomposition_large_n.py's own sample_x_and_q /
compute_decomposition UNCHANGED (read-only import), per Unclaimed Work
Ownership convention -- same functions rn_tightened_reps.py (Point 95) used.

PRE-REGISTERED DECISION RULE (written before running):
  - LEAD (supports C1+C2, i.e. Var(X_n)=O(1/n)): 95% CI on b excludes 1 AND
    is close to / consistent with 0.
  - CONCERNING (supports C3, i.e. Var(X_n) does not decay as 1/n): CI on b
    excludes 0 and is close to / consistent with 1.
  - STILL INCONCLUSIVE: CI on b contains both 0 and 1.
Stopping rule: this IS the pre-registered stopping point (rep counts
equalized to 800 at all three n, matching Point 95's own named target) --
no further reps added regardless of the outcome without a NEW, separately
pre-registered follow-up.
"""

import importlib.util
import json
import time
from pathlib import Path

import numpy as np

EXP_DIR = Path(__file__).resolve().parent


def _load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


fc = _load_module("first_chaos_canonical", EXP_DIR / "check_first_chaos_decomposition_large_n.py")
sample_x_and_q = fc.sample_x_and_q
compute_decomposition = fc.compute_decomposition
RNG_SEED_BASE = fc.RNG_SEED_BASE  # 3331000, the OLD sweep's own seed base

NEW_SEED_BASE = RNG_SEED_BASE + 500000  # 3831000, Point 95's own "fresh, non-overlapping" base

TARGET_N = [509, 1021, 2039]
OLD_REPS = {509: 200, 1021: 150, 2039: 80}
ALREADY_NEW_REPS = {509: 800, 1021: 600, 2039: 160}  # Point 95's own already-run batch
TARGET_REPS = 800  # equalize to 800 at all three, per Point 95's own step 2

t_start = time.time()
pooled = {}
for n in TARGET_N:
    t0 = time.time()
    # OLD draws: seed_base=RNG_SEED_BASE, i in [0, OLD_REPS[n])
    x_old, q_old = sample_x_and_q(n, OLD_REPS[n], RNG_SEED_BASE)

    # NEW draws already run at Point 95: seed_base=NEW_SEED_BASE, i in [0, ALREADY_NEW_REPS[n])
    x_new1, q_new1 = sample_x_and_q(n, ALREADY_NEW_REPS[n], NEW_SEED_BASE)

    # EXTENSION to reach TARGET_REPS=800: i in [ALREADY_NEW_REPS[n], TARGET_REPS), same
    # seed_base=NEW_SEED_BASE -- fresh, non-overlapping with the already-run batch above
    # (sample_x_and_q's own seed formula is seed_base + n*100000 + i).
    n_extra = TARGET_REPS - ALREADY_NEW_REPS[n]
    if n_extra > 0:
        # sample_x_and_q always starts i at 0; to get i in [ALREADY_NEW_REPS[n], TARGET_REPS)
        # specifically, call it for TARGET_REPS total then slice off the already-covered head.
        x_new_full, q_new_full = sample_x_and_q(n, TARGET_REPS, NEW_SEED_BASE)
        x_ext, q_ext = x_new_full[ALREADY_NEW_REPS[n] :], q_new_full[ALREADY_NEW_REPS[n] :]
    else:
        x_ext, q_ext = np.array([]), np.array([])

    x_pooled = np.concatenate([x_old, x_new1, x_ext])
    q_pooled = np.concatenate([q_old, q_new1, q_ext])
    pooled[n] = (x_pooled, q_pooled)

    elapsed = time.time() - t0
    print(
        f"n={n}: pooled reps = {len(x_pooled)} (old {len(x_old)} + new1 {len(x_new1)} + "
        f"ext {len(x_ext)}), elapsed={elapsed:.1f}s",
        flush=True,
    )

print(f"\nTotal data-generation time: {time.time() - t_start:.1f}s")

out_raw = {n: {"x": pooled[n][0].tolist(), "q": pooled[n][1].tolist()} for n in TARGET_N}
(Path("metrics") / "rn_revival_pooled_raw.json").write_text(json.dumps(out_raw))
print("Raw pooled data written to metrics/rn_revival_pooled_raw.json")
