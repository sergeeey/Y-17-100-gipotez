"""verify_local_vs_global_wide.py -- follow-up to verify_local_vs_global.py: the first local
verification (re_max=10.5) CLIPPED at N_DIM=40,50 (local_alpha_max hit exactly 10.5, the window
boundary, while the global search found values up to 12.52 and 15.53 there). Re-run those two
slices only, with re_max=20.0 (comfortably above the global max of 15.53), same fine resolution.
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


def local_search_wide(a: np.ndarray) -> float:
    return pseudo.pseudospectral_abscissa(
        a, eps=pseudo.EPS, re_min=0.5, re_max=20.0, im_max=5.0, n_re=150, n_im=100
    )


def main() -> dict:
    comparison = {}
    for n_dim in (40, 50):
        slice_data = existing["per_n_slice"][str(n_dim)]
        local_alphas = []
        m1s = []
        for seed_str, seed_data in slice_data["per_seed"].items():
            seed = int(seed_str)
            a = pseudo.multin.build_matrix_with_seed_and_n(n_dim, seed)
            local_alphas.append(local_search_wide(a))
            m1s.append(seed_data["m1"])

        rho_local, p_local = spearmanr(local_alphas, m1s)
        comparison[str(n_dim)] = {
            "n_dim": n_dim,
            "rho_global": float(slice_data["spearman_rho"]),
            "p_global": float(slice_data["spearman_p"]),
            "rho_local_wide": float(rho_local),
            "p_local_wide": float(p_local),
            "local_alpha_min": float(min(local_alphas)),
            "local_alpha_max": float(max(local_alphas)),
            "hit_window_boundary_20": any(v >= 19.9 for v in local_alphas),
        }

    (HERE / "metrics" / "local_vs_global_verification_wide.json").write_text(
        json.dumps(comparison, indent=2), encoding="utf-8"
    )
    print(json.dumps(comparison, indent=2))
    return comparison


if __name__ == "__main__":
    main()
