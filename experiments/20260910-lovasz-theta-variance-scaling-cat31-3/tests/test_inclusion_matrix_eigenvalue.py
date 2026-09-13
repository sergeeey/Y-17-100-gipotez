"""Point 29: pytest wrapper for verify_inclusion_matrix_eigenvalue.py's exact-Fraction check
that the inclusion-product matrix M^(k) (M^(k)_{S,T}=C(|S cap T|,k)) has eigenvalue
C(N-2k,q-k) on the level-k Johnson eigenspace V_k, verified via ALREADY-REVIEWED Z_A/y_ab/
z_abc constructions (points 25-28) as independent eigenvector witnesses -- not new code
written to match the claim."""

from __future__ import annotations

import importlib.util
from pathlib import Path

EXPERIMENT_DIR = Path(__file__).resolve().parent.parent


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_inclusion_matrix_eigenvalue_matches_binomial_n_minus_2k_q_minus_k():
    mod = _load_module(
        "h_cat31_3_inclusion_matrix_eigenvalue_under_test",
        EXPERIMENT_DIR / "verify_inclusion_matrix_eigenvalue.py",
    )
    for N, q, k in [(8, 4, 1), (8, 4, 2), (8, 4, 3), (9, 5, 1), (9, 5, 2), (9, 5, 3), (10, 4, 2)]:
        assert mod.build_and_check(N, q, k), f"eigenvalue mismatch at N={N}, q={q}, k={k}"
