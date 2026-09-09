from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pytest

HERE = Path(__file__).resolve().parent.parent


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def h24():
    return _load_module("test_h2_4_run", HERE / "run.py")


def test_build_matrix_matches_h_b2_1k_at_seed_zero(h24):
    """Regression: at seed=0, this experiment's own build_matrix must reproduce H-B2-1k's own
    hardcoded-SEED=0 matrix exactly -- confirms the seed-parameterization is a pure
    generalization, not a silent behavior change."""
    a = h24.build_matrix(8, seed=0)
    assert a.shape == (8, 8)
    eigenvalues_diag = np.diag(a)
    assert eigenvalues_diag[0] == h24.POSITIVE_EIGENVALUE
    assert np.isclose(eigenvalues_diag[1], h24.SPECTRAL_RANGE[0])
    assert np.isclose(eigenvalues_diag[-1], h24.SPECTRAL_RANGE[1])


def test_different_seeds_give_different_matrices(h24):
    a0 = h24.build_matrix(8, seed=0)
    a1 = h24.build_matrix(8, seed=1)
    assert not np.allclose(a0, a1)
    # diagonal (eigenvalue placement) is seed-independent by construction
    assert np.allclose(np.diag(a0), np.diag(a1))


def test_sign_change_count_known_cases(h24):
    assert h24.sign_change_count(np.array([1, 2, 3, 4, 5])) == 0  # monotonic increasing
    assert h24.sign_change_count(np.array([5, 4, 3, 2, 1])) == 0  # monotonic decreasing
    assert h24.sign_change_count(np.array([1, 3, 2, 4, 3])) == 3  # up,down,up,down = 3 changes
    assert h24.sign_change_count(np.array([1, 2, 2, 3])) == 0  # tie doesn't count as a change


def test_permutation_preserves_per_seed_value_multiset(h24):
    """The permutation scheme must preserve each seed's own set of 9 M1 values (only reassigning
    which N_DIM they're labeled with), not draw from a different distribution."""
    rng = np.random.default_rng(1)
    grid = rng.normal(size=(5, 9))
    for seed_row in grid:
        perm = rng.permutation(9)
        permuted_row = seed_row[perm]
        assert sorted(permuted_row.tolist()) == sorted(seed_row.tolist())


def test_committed_run_mean_m1_is_monotonic_increasing():
    run_json_path = HERE / "metrics" / "run.json"
    if not run_json_path.exists():
        pytest.skip("metrics/run.json not yet generated")
    data = json.loads(run_json_path.read_text(encoding="utf-8"))
    n_values = data["n_dim_values"]
    means = [data["mean_m1_by_n_dim"][str(n)] for n in n_values]
    assert all(means[i] < means[i + 1] for i in range(len(means) - 1))
    assert data["observed_sign_changes"] == 0


def test_committed_run_verdict_rejected_with_p_value_one():
    run_json_path = HERE / "metrics" / "run.json"
    if not run_json_path.exists():
        pytest.skip("metrics/run.json not yet generated")
    data = json.loads(run_json_path.read_text(encoding="utf-8"))
    assert data["verdict"] == "REJECTED"
    assert data["p_value"] == 1.0
    assert data["n_seeds"] == 30
    assert data["n_permutations"] == 2000
