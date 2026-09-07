"""verify_local_vs_global.py -- FL Step 8a response to the skeptic's sharpest concern (H-B2-1r):
does the GLOBAL grid search (re in [0.5, 60], im in [-15,15], 100x100) sometimes land on a
pseudospectral component belonging to a DIFFERENT (negative) eigenvalue cluster, rather than the
one containing the dominant eigenvalue (always +0.5 for this matrix family) -- undetectably,
since such a hit would look like a plausible positive number, not an impossible one like the
original 0.0 bug?

Verification: run a LOCAL search tightly centered on the known dominant eigenvalue (re in
[0.5, 10.5], im in [-5,5], 100x100 -- the same safe floor as the already-fixed global search
(re_min = spectral_abscissa = 0.5), but with re_max pulled way down (10.5, generous vs. the
observed global values, which topped out well under that) and im_max shrunk from 15 to 5 --
buying much finer LOCAL resolution in both directions within a box that is mathematically
guaranteed to exclude every OTHER eigenvalue's own eps-disk (the closest negative eigenvalue is
always exactly -1, whose disk only reaches re=-1+eps=0.0, strictly below this box's floor of 0.5
for every N_DIM in this family) -- so any hit found here provably belongs to the dominant
eigenvalue's own pseudospectral component, not a coalesced cluster from the negative side.

Does NOT recompute M1 (the expensive step -- reuses M1 already stored in metrics/run.json's
per_seed data). Only recomputes alpha_eps with the local, finer search, for the SAME matrices.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

HERE = Path(__file__).resolve().parent

_SPEC = importlib.util.spec_from_file_location("chernoff_1r_run", HERE / "run.py")
pseudo = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(pseudo)

with open(HERE / "metrics" / "run.json", encoding="utf-8") as f:
    existing = json.load(f)


def local_search(a: np.ndarray) -> float:
    return pseudo.pseudospectral_abscissa(
        a, eps=pseudo.EPS, re_min=0.5, re_max=10.5, im_max=5.0, n_re=100, n_im=100
    )


def main() -> dict:
    comparison = {}
    for n_dim_str, slice_data in existing["per_n_slice"].items():
        n_dim = int(n_dim_str)
        local_alphas = []
        global_alphas = []
        m1s = []
        for seed_str, seed_data in slice_data["per_seed"].items():
            seed = int(seed_str)
            a = pseudo.multin.build_matrix_with_seed_and_n(n_dim, seed)
            local_alpha = local_search(a)
            local_alphas.append(local_alpha)
            global_alphas.append(seed_data["alpha_eps"])
            m1s.append(seed_data["m1"])

        rho_local, p_local = spearmanr(local_alphas, m1s)
        rho_global = slice_data["spearman_rho"]
        p_global = slice_data["spearman_p"]
        max_abs_diff = float(np.max(np.abs(np.array(local_alphas) - np.array(global_alphas))))
        n_below_universal_bound = sum(1 for v in local_alphas if v < 0.5 + pseudo.EPS - 1e-6)

        comparison[n_dim_str] = {
            "n_dim": n_dim,
            "rho_global": float(rho_global),
            "p_global": float(p_global),
            "rho_local": float(rho_local),
            "p_local": float(p_local),
            "rho_diff": float(rho_local - rho_global),
            "max_abs_alpha_diff_local_vs_global": max_abs_diff,
            "n_local_below_universal_bound_1p5": n_below_universal_bound,
            "local_alpha_min": float(min(local_alphas)),
            "local_alpha_max": float(max(local_alphas)),
        }

    (HERE / "metrics" / "local_vs_global_verification.json").write_text(
        json.dumps(comparison, indent=2), encoding="utf-8"
    )
    print(json.dumps(comparison, indent=2))
    return comparison


if __name__ == "__main__":
    main()
