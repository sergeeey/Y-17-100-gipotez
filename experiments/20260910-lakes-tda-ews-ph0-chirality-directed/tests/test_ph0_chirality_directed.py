import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from run import (
    b3_1,
    chirality_excess,
    merge_tree_bars,
    merge_tree_bars_full,
    surrogate_crossing_generic,
    surrogate_null_curve_generic,
    trend_slope_series,
)


def test_monotone_increasing_gives_single_L_bar():
    """min at t=0, max at t=n-1: min precedes max -> L. Hand-verified: only
    one bar possible (no interior extrema), (b_idx=0, d_idx=4)."""
    w = np.array([0.0, 1.0, 2.0, 3.0, 4.0])
    bars = merge_tree_bars(w)
    assert len(bars) == 1
    b_idx, d_idx, b_val, d_val = bars[0]
    assert b_idx == 0 and d_idx == 4
    assert b_val == 0.0 and d_val == 4.0
    assert chirality_excess(w) == -1.0  # all L


def test_monotone_decreasing_gives_single_N_bar():
    """max at t=0, min at t=n-1: min AFTER max -> N."""
    w = np.array([4.0, 3.0, 2.0, 1.0, 0.0])
    bars = merge_tree_bars(w)
    assert len(bars) == 1
    b_idx, d_idx, _b_val, _d_val = bars[0]
    assert b_idx == 4 and d_idx == 0
    assert chirality_excess(w) == 1.0  # all N


def test_hand_verified_w_shape_zero_three_one_four():
    """w = [0,3,1,4]. Recursive global-min/max-first pairing (Baryshnikov
    2022 Sec 2.2.1): among all 4 points {0,3,1,4}, global min is t=0 (val 0),
    global max is t=3 (val 4) -- paired FIRST as the outermost "stem" bar,
    min BEFORE max -> L. That leaves the interior run [t=1, t=2] (val 3, val
    1): min t=2 AFTER max t=1 -> N. Total: 1 L, 1 N -> chirality_excess = 0."""
    w = np.array([0.0, 3.0, 1.0, 4.0])
    bars = merge_tree_bars(w)
    assert len(bars) == 2
    first = bars[0]
    assert first[0] == 0 and first[1] == 3  # min at t=0, max at t=3 -> L-type pairing (outermost)
    second = bars[1]
    assert second[0] == 2 and second[1] == 1  # min at t=2, max at t=1 -> N-type pairing (interior)
    assert chirality_excess(w) == 0.0


def test_time_reversal_flips_chirality_sign_for_asymmetric_case():
    """Reversing a genuinely asymmetric (not palindromic) series must not
    leave chirality_excess unchanged in general -- this is the whole point
    of the statistic (Mechanism Claim Gate: distinguishes what H1-VR
    cannot). Uses the monotone case where the flip is exact and provable."""
    w = np.array([0.0, 1.0, 2.0, 3.0, 4.0])
    w_rev = w[::-1].copy()
    assert chirality_excess(w) == -1.0
    assert chirality_excess(w_rev) == 1.0
    assert chirality_excess(w) != chirality_excess(w_rev)


def test_merge_tree_bars_full_accounts_for_every_point_exactly():
    """Exact accounting, no floor division: every extremum point is either
    consumed by exactly one bar (2 points per bar) or explicitly reported as
    unmatched (merge_tree_bars_full) -- none may be silently dropped.

    Caught this session (independent reviewer pass, not self-caught): the
    original version of this test compared `len(bars)` to
    `total_points // 2`, which passes even when a point is silently lost
    (floor division absorbs the -1). A 7-point counter-example
    (test_reviewer_counter_example_odd_extrema_includes_global_min below)
    demonstrated the earlier `merge_tree_bars` implementation dropped the
    window's GLOBAL MINIMUM specifically -- with floor division this test
    would still have reported success on that exact input."""
    rng = np.random.default_rng(123)
    w = rng.normal(size=25)
    bars, unmatched = merge_tree_bars_full(w)
    n_interior_extrema = sum(
        1
        for i in range(1, len(w) - 1)
        if (w[i] - w[i - 1] != 0)
        and (w[i + 1] - w[i] != 0)
        and ((w[i] - w[i - 1] > 0) != (w[i + 1] - w[i] > 0))
    )
    total_points = n_interior_extrema + 2
    assert len(bars) * 2 + len(unmatched) == total_points  # exact, no rounding
    # NOTE: an earlier version of this assertion claimed "at most one leftover
    # point" -- WRONG, verified directly this session: a larger sequence
    # recurses into MULTIPLE independent sub-runs (unlike the reviewer's
    # single-branch 7-point counter-example below), and each odd-sized
    # sub-run can leave its OWN unmatched point (this fixture, seed 123,
    # n=25, produces unmatched == [3, 10, 24] -- three, not one). The real
    # invariant is that no point is EVER double-counted or fabricated:
    assert len(set(unmatched)) == len(unmatched)  # no unmatched index repeats
    assert set(unmatched).issubset(set(range(len(w))))  # every unmatched index is a real point


def test_reviewer_counter_example_odd_extrema_includes_global_min():
    """w = [2, 8, 0, 9, 1, 7, 3] -- all 7 points are extrema (odd count),
    hand-constructed by an independently-invoked reviewer agent (FL Step 8a)
    to falsify the earlier `merge_tree_bars` implementation, which paired
    the two INDEX-ADJACENT points with smallest value-difference first,
    working inward -- and silently dropped the window's GLOBAL MINIMUM
    (value 0.0 at index 2) whenever the total extrema count was odd
    (measured on the real Lower Zurich data: ~55%, 45/82, of rolling
    windows). Confirmed by the reviewer both by hand-tracing and by running
    the live code.

    The fix (this file, `_recursive_pairing`): re-implemented per
    Baryshnikov 2022 Sec 2.2.1 -- find the GLOBAL min/max of the current
    point set, pair them first (the outermost "stem"), remove both, recurse
    on each remaining contiguous run. Hand-traced result: global min
    (idx=2, val=0.0) pairs with global max (idx=3, val=9.0) as the very
    FIRST bar. Remaining runs [0,1] and [4,5,6] recurse independently;
    [4,5,6] has 3 points (odd) and leaves index 6 (val=3.0) unmatched --
    an explicit, visible leftover, never silently dropped, and never the
    global minimum this counter-example was built to protect."""
    w = np.array([2.0, 8.0, 0.0, 9.0, 1.0, 7.0, 3.0])
    bars, unmatched = merge_tree_bars_full(w)

    global_min_idx = int(np.argmin(w))
    assert global_min_idx == 2
    assert any(b_idx == global_min_idx or d_idx == global_min_idx for b_idx, d_idx, _, _ in bars), (
        "global minimum must appear in some bar, not be silently dropped"
    )

    # exact accounting: 7 points total, 3 bars (6 points) + 1 unmatched = 7
    assert len(bars) == 3
    assert unmatched == [6]

    # the global min/max pair is extracted FIRST, as the outermost stem
    assert bars[0] == (2, 3, 0.0, 9.0)


def test_v1_surrogate_crossing_fires_on_a_series_with_a_real_moderate_trend():
    """Sanity/positive control for the generic V1 calibration helper.

    WHY noise_sd=6, not a cleaner-looking small-noise trend (found this
    session, not assumed): a first attempt used noise_sd=0.3 (very clean
    linear trend) and FAILED -- diagnosis showed phi (lag-1 autocorrelation
    of x) came out at 0.99, because a strong deterministic trend is itself
    highly autocorrelated. `ar1_surrogate` matches that phi, producing
    near-unit-root surrogates that themselves wander with spurious apparent
    trends (a well-known phenomenon in AR(1)-null testing, not a bug) --
    the null curve's 95th percentile reached tau~1.0, impossible for the
    real series to exceed. noise_sd=6 keeps phi in a moderate range (~0.5)
    where the AR(1) null is a meaningful comparison, confirmed via a
    parameter sweep (diag_v1_trend2.py) before picking this value -- not
    tuned to force a pass on an otherwise-broken implementation."""
    rng = np.random.default_rng(1)
    n = 80
    x = np.linspace(0, 20, n) + rng.normal(0, 6.0, n)
    window = 30
    tau = b3_1.expanding_kendall_tau(trend_slope_series(x, window))
    null_curve = surrogate_null_curve_generic(x, window, trend_slope_series, reps=30, seed=99)
    crossing = surrogate_crossing_generic(tau, null_curve)
    assert crossing is not None
