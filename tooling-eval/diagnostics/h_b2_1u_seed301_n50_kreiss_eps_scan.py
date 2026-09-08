"""Diagnostic kept for provenance (referenced from H-B2-1u's run.py bug/fix comment): the
script that resolved H-B2-1u's single apparent Kreiss upper-bound violation (seed=301,
N_DIM=50) by showing the true Kreiss-constant supremum lives in the small-eps regime for this
matrix family, which the experiment's first-draft EPS_VALUES=(0.5..3.0) never sampled.

Run from the project root: python tooling-eval/diagnostics/h_b2_1u_seed301_n50_kreiss_eps_scan.py
"""

import importlib.util
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent.parent

_M_DIR = ROOT / "experiments" / "20260907-chernoff-neuralode-nd-multiseed-multin"
_SPEC_M = importlib.util.spec_from_file_location("h_b2_1u_diag_multin", _M_DIR / "run.py")
multin = importlib.util.module_from_spec(_SPEC_M)
_SPEC_M.loader.exec_module(multin)

_R_DIR = ROOT / "experiments" / "20260907-chernoff-neuralode-nd-pseudospectral-abscissa"
_SPEC_R = importlib.util.spec_from_file_location("h_b2_1u_diag_alpha", _R_DIR / "run.py")
alpha_mod = importlib.util.module_from_spec(_SPEC_R)
_SPEC_R.loader.exec_module(alpha_mod)

a = multin.build_matrix_with_seed_and_n(50, 301)
spectral_abscissa = float(np.max(np.linalg.eigvals(a).real))
print("spectral_abscissa:", spectral_abscissa)
print("is upper triangular (max abs lower-tri entry):", np.max(np.abs(np.tril(a, k=-1))))

for eps in (0.02, 0.05, 0.1, 0.2, 0.3, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0, 8.0):
    alpha_eps = alpha_mod.pseudospectral_abscissa(
        a,
        eps=eps,
        re_min=spectral_abscissa - 1.0,
        re_max=spectral_abscissa + 30.0,
        im_max=10.0,
        n_re=180,
        n_im=100,
    )
    ratio = (alpha_eps - spectral_abscissa) / eps
    print(f"eps={eps:6.3f}  alpha_eps={alpha_eps:10.4f}  ratio(K-candidate)={ratio:10.4f}")
