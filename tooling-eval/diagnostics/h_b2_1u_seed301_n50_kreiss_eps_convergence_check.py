"""Diagnostic kept for provenance (referenced from H-B2-1u's run.py CONVERGENCE CAVEAT
comment): follow-up to the mandatory reviewer's P1 finding that k_estimate was pinned to the
smallest sampled eps (0.02) for 20/20 matrices with no plateau. Extends the scan on the
worst-case matrix (seed=301, N_DIM=50) two more octaves down, using a finer/narrower grid than
production, to check whether the ratio is converging or still climbing.

Run from the project root:
python tooling-eval/diagnostics/h_b2_1u_seed301_n50_kreiss_eps_convergence_check.py
"""

import importlib.util
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent.parent

_M_DIR = ROOT / "experiments" / "20260907-chernoff-neuralode-nd-multiseed-multin"
_SPEC_M = importlib.util.spec_from_file_location("h_b2_1u_conv_multin", _M_DIR / "run.py")
multin = importlib.util.module_from_spec(_SPEC_M)
_SPEC_M.loader.exec_module(multin)

_R_DIR = ROOT / "experiments" / "20260907-chernoff-neuralode-nd-pseudospectral-abscissa"
_SPEC_R = importlib.util.spec_from_file_location("h_b2_1u_conv_alpha", _R_DIR / "run.py")
alpha_mod = importlib.util.module_from_spec(_SPEC_R)
_SPEC_R.loader.exec_module(alpha_mod)

a = multin.build_matrix_with_seed_and_n(50, 301)
spectral_abscissa = float(np.max(np.linalg.eigvals(a).real))
print("spectral_abscissa:", spectral_abscissa)

# Finer, narrower grid than production KREISS_GRID_KWARGS -- window +8 (not +30), n_re=1200,
# giving step ~8/1199~=0.00667, still coarser than eps=0.001 and 0.002 (documented in the
# result: even these numbers should not be read as fully converged).
for eps in (0.02, 0.01, 0.005, 0.002, 0.001):
    alpha_eps = alpha_mod.pseudospectral_abscissa(
        a,
        eps=eps,
        re_min=spectral_abscissa,
        re_max=spectral_abscissa + 8.0,
        im_max=6.0,
        n_re=1200,
        n_im=400,
    )
    ratio = (alpha_eps - spectral_abscissa) / eps
    print(f"eps={eps:7.4f}  alpha_eps={alpha_eps:10.5f}  ratio={ratio:10.4f}")
