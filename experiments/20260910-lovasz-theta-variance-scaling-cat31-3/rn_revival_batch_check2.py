"""Cheaper batch-consistency check: regenerate OLD batch alone (cheap: 80-200
reps) and compare its n*R_n against Point 95's own already-recorded NEW-only
values (800/600/160 reps at n=509/1021/2039 respectively, decision.md Point
95's own raw result). Both are point estimates from disjoint, independent
seed regions -- a real disagreement here would flag a batch effect."""

import importlib.util
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
paired_bootstrap_ci = fc.paired_bootstrap_ci
RNG_SEED_BASE = fc.RNG_SEED_BASE

TARGET_N = [509, 1021, 2039]
OLD_REPS = {509: 200, 1021: 150, 2039: 80}
# Point 95's own already-recorded NEW-only results (decision.md, this session's own context)
POINT95_NEW = {
    509: {"reps": 800, "n_times_r_n": 0.6528, "ci": [0.1265833825783941, 1.0653909194964377]},
    1021: {"reps": 600, "n_times_r_n": 0.7209, "ci": [0.16893421475999654, 1.1454824811728463]},
    2039: {"reps": 160, "n_times_r_n": 0.8104, "ci": [-0.32103852522421533, 1.5931703911586168]},
}

for n in TARGET_N:
    t0 = time.time()
    x_old, q_old = sample_x_and_q(n, OLD_REPS[n], RNG_SEED_BASE)
    dec_old = compute_decomposition(x_old, q_old, n)
    ci_old = paired_bootstrap_ci(x_old, q_old, n, 2000, 12345)
    se_old = (ci_old["n_times_r_n_ci95"][1] - ci_old["n_times_r_n_ci95"][0]) / (2 * 1.96)

    new = POINT95_NEW[n]
    se_new = (new["ci"][1] - new["ci"][0]) / (2 * 1.96)
    diff = new["n_times_r_n"] - dec_old["n_times_r_n_hat"]
    se_diff = np.sqrt(se_old**2 + se_new**2)
    z = diff / se_diff if se_diff > 0 else float("nan")

    print(
        f"n={n:5d} (elapsed {time.time() - t0:.1f}s): "
        f"OLD(reps={OLD_REPS[n]}) n*R_n={dec_old['n_times_r_n_hat']:.4f} "
        f"CI={ci_old['n_times_r_n_ci95']}  "
        f"NEW(reps={new['reps']}) n*R_n={new['n_times_r_n']:.4f} CI={new['ci']}  "
        f"z(new-old)={z:.3f}"
    )
