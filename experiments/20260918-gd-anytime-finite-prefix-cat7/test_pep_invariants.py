"""Regression tests locking in the invariants the verdict rests on.

These are cheap (all at small horizons) and are the things that, if they silently
broke, would make every downstream number wrong without any visible error:

* the PEP reproduces the known closed form for constant stepsizes;
* the analytic gradient matches finite differences;
* the reconstructed silver / ZLDC schedules have the algebraic properties their own
  source paper proves for them, including primitivity -- with a control that the
  primitivity test can actually fail;
* the ZLDC schedule is prefix-monotone, which is the entire reason it is a legitimate
  *anytime* comparator.

Run:  python -m pytest test_pep_invariants.py -q
"""

from __future__ import annotations

import math

import numpy as np
import pytest
from pep_core import (
    RHO,
    GDPep,
    constant_schedule,
    silver_schedule,
    zldc_anytime_schedule,
    zldc_concat_endpoints,
)


@pytest.mark.parametrize(("n", "h"), [(1, 1.0), (3, 1.0), (5, 0.5), (8, 0.75)])
def test_constant_stepsize_closed_form(n: int, h: float) -> None:
    """Drori-Teboulle / Taylor et al.: R_N = 1 / (4 N h + 2) for h <= 1."""
    got = GDPep(n, "R").solve(np.array(constant_schedule(n, h))).value
    assert got == pytest.approx(1.0 / (4 * n * h + 2.0), rel=1e-6)


def test_analytic_gradient_matches_finite_difference() -> None:
    rng = np.random.default_rng(0)
    h = rng.uniform(0.4, 2.0, size=5)
    pep = GDPep(5, "R")
    res = pep.solve(h, want_grad=True)
    eps = 1e-3
    fd = np.array(
        [
            (pep.solve(h + eps * np.eye(5)[k]).value - pep.solve(h - eps * np.eye(5)[k]).value)
            / (2 * eps)
            for k in range(5)
        ]
    )
    assert np.max(np.abs(res.grad - fd)) / np.max(np.abs(fd)) < 1e-3


@pytest.mark.parametrize("order", [1, 2, 3, 4, 5])
def test_silver_schedule_algebra(order: int) -> None:
    s = silver_schedule(order)
    assert len(s) == 2**order - 1
    assert sum(s) == pytest.approx(RHO**order - 1.0, rel=1e-12)
    assert all(v > 0 for v in s)


def test_zldc_is_prefix_monotone() -> None:
    """The anytime property: one infinite schedule, every shorter one a literal prefix."""
    long = zldc_anytime_schedule(120)
    for m in (1, 3, 9, 27, 64, 100):
        assert np.allclose(zldc_anytime_schedule(m), long[:m], rtol=0, atol=1e-12)
    assert all(v > 0 for v in long)


def test_zldc_exponent_matches_paper() -> None:
    # The papers write "~ O(n^{-1.119})", truncating 1.1195452... to three decimals,
    # so the tolerance has to admit truncation rather than rounding.
    assert 2 * math.log2(RHO) / (1 + math.log2(RHO)) == pytest.approx(1.1195, abs=1e-4)


@pytest.mark.parametrize("order", [2, 3, 4])
def test_silver_is_primitive(order: int) -> None:
    s = silver_schedule(order)
    lhs = GDPep(len(s), "R").solve_primitivity(np.array(s))
    assert lhs <= 0.5 + 1e-6


def test_zldc_concatenation_endpoints_are_primitive() -> None:
    sched = zldc_anytime_schedule(30)
    for t in zldc_concat_endpoints(30)[:6]:
        lhs = GDPep(t, "R").solve_primitivity(np.array(sched[:t]))
        assert lhs <= 0.5 + 1e-6, f"length {t} not primitive"


def test_primitivity_test_can_fail() -> None:
    """Control: a test that accepts everything proves nothing."""
    bad = [*silver_schedule(3)[:-1], 9.0]
    assert GDPep(len(bad), "R").solve_primitivity(np.array(bad)) > 0.5 + 1e-6


def test_prefix_slicing_is_the_only_coupling() -> None:
    """A prefix-consistent evaluation must depend only on the first n entries."""
    master = np.array(zldc_anytime_schedule(12))
    tail_changed = master.copy()
    tail_changed[8:] = 0.77
    for n in (4, 6, 8):
        a = GDPep(n, "R").solve(master[:n]).value
        b = GDPep(n, "R").solve(tail_changed[:n]).value
        assert a == pytest.approx(b, rel=1e-9)
