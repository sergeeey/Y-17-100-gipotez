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
def h():
    return _load_module("test_h_cat31_2_run", HERE / "run.py")


def test_pairs_match_report_verbatim(h):
    """Regression: the 3 (prime, composite) pairs must match
    reports/2026-09-09-breakthrough-routes.md exactly -- these were pre-registered BEFORE this
    experiment's data existed, and must not silently drift."""
    assert h.PAIRS == [(127, 129), (251, 255), (509, 511)]


def test_all_composite_partners_are_actually_composite_and_primes_are_prime(h):
    def is_prime(k: int) -> bool:
        if k < 2:
            return False
        for d in range(2, int(k**0.5) + 1):
            if k % d == 0:
                return False
        return True

    for prime_n, composite_n in h.PAIRS:
        assert is_prime(prime_n), f"{prime_n} expected prime"
        assert not is_prime(composite_n), f"{composite_n} expected composite"


def test_complement_neighbors_flips_all_nonzero_offsets(h):
    c = np.array([0.0, 1.0, 0.0, 1.0, 0.0])
    c_bar = h.complement_neighbors(c)
    assert c_bar[0] == 0.0
    assert np.array_equal(c_bar[1:], 1.0 - c[1:])


def test_complement_of_complement_is_original(h):
    rng = np.random.default_rng(7)
    n = 21
    c = h.sample_circulant_neighbors(n, 0.5, seed=7)
    c_bar = h.complement_neighbors(c)
    c_bar_bar = h.complement_neighbors(c_bar)
    assert np.array_equal(c, c_bar_bar)
    del rng


def test_top_decile_contribution_concentrated_case(h):
    """A single dominant value should contribute close to 100% of the total."""
    x = np.array([0.0] * 99 + [5.0])
    frac = h.top_decile_contribution(x)
    assert frac > 0.9


def test_top_decile_contribution_uniform_case(h):
    """If all |x| are equal, the top decile (10% of points) should contribute close to 10% of
    the total sum of cosh(x)-1 (exactly 10% up to the ceil-rounding of n_top)."""
    x = np.full(100, 0.3)
    frac = h.top_decile_contribution(x)
    assert abs(frac - 0.10) < 1e-9


def test_positive_control_holds_on_a_handful_of_small_graphs(h):
    for n in (7, 11, 15, 21):
        c = h.sample_circulant_neighbors(n, 0.5, seed=1000 + n)
        theta = h.theta_via_lp(c)
        c_bar = h.complement_neighbors(c)
        theta_bar = h.theta_via_lp(c_bar)
        assert abs(theta * theta_bar / n - 1.0) < 1e-6


def test_bootstrap_ci_is_well_formed(h):
    rng = np.random.default_rng(42)
    x = rng.normal(0, 0.2, size=200)
    lo, hi = h.bootstrap_ci_top_decile(x, n_resamples=200, seed=1)
    assert 0.0 <= lo <= hi <= 1.0


def test_committed_run_json_positive_control_passed():
    """The actual committed run must have passed its own pre-registered positive control --
    a failure here would mean the run.json on disk is stale or the control regressed."""
    run_json_path = HERE / "metrics" / "run.json"
    if not run_json_path.exists():
        pytest.skip("metrics/run.json not yet generated")
    data = json.loads(run_json_path.read_text(encoding="utf-8"))
    assert data["positive_control"]["passed"] is True
    assert data["positive_control"]["max_violation_of_theta_times_thetabar_over_n"] < 1e-6


def test_committed_run_json_verdict_is_one_of_the_pre_registered_outcomes():
    run_json_path = HERE / "metrics" / "run.json"
    if not run_json_path.exists():
        pytest.skip("metrics/run.json not yet generated")
    data = json.loads(run_json_path.read_text(encoding="utf-8"))
    assert data["verdict"] in ("LEAD", "CRITERION_INVALID", "REJECTED")
    assert len(data["pairs"]) == 3
