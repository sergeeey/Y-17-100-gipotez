"""Reviewer-flagged P2 (2026-09-12): derive_lambda_k_from_first_principles.py's own MATCH
claims were not pytest-wrapped, so an edit could silently reintroduce a symbolic regression
without failing commit-test-gate's pytest-scoped check. This closes that gap."""

from __future__ import annotations

import importlib.util
from pathlib import Path

EXPERIMENT_DIR = Path(__file__).resolve().parent.parent


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_lambda_k_matches_hypothesis_for_k_1_2_3_4():
    """Point 27 (k=1,2,3) + point 28 (k=4): lambda_k derived from first principles (symbolic,
    via the trace identity on ||Z_A||^2) must exactly match the falling-factorial closed form
    (q)_k(N-q)_k/(N)_{2k} for general symbolic N,q -- not a numeric coincidence at spot-checked
    values. k=4 additionally exercises the self-adjoint cross-term computation for E_3(Y_A)
    (region-based classification of triples by |A intersect triple|), the first level where
    E_{k-1} could not reuse an explicit y_ab/z_abc-style basis directly."""
    mod = _load_module(
        "h_cat31_3_lambda_k_under_test",
        EXPERIMENT_DIR / "derive_lambda_k_from_first_principles.py",
    )
    import sympy as sp

    for k, derive_fn in [
        (1, mod.derive_lambda_1),
        (2, mod.derive_lambda_2),
        (3, mod.derive_lambda_3),
        (4, mod.derive_lambda_4),
    ]:
        derived = derive_fn()
        hypothesis = mod.lambda_hypothesis(k)
        assert sp.simplify(derived - hypothesis) == 0, (
            f"lambda_{k} mismatch: {derived} != {hypothesis}"
        )
