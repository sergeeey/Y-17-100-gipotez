"""Numerical search for limit cycles in discontinuous (Filippov) 2-zone planar
piecewise-linear systems, following the Lienard-normal-form reduction verified
in full from Carmona-Fernandez-Sanchez-Novaes (2019, IME/Unicamp RP-2019-03),
generalized to independent a_L != a_R (the structural difference between the
PROVEN continuous Lum-Chua case, a_L=a_R, and the open discontinuous case).

WHY numerical ODE integration instead of the paper's closed-form Inverse
Integrating Factor V(x,y): the OCR'd text of that formula was ambiguous
(garbled brackets/exponents) and reconstructing it by guesswork risks silently
validating against a wrong formula (Substrate Gate 2a: don't build on an
untrusted source when a clean, independently-verifiable alternative exists).
Direct numerical integration of the half-return map is slower but has no
transcription risk and is independently checkable against the known theorem.

System (each zone a linear focus, Lienard form):
    x<0:  xdot = T_L*x - y,  ydot = D_L*x - a_L
    x>0:  xdot = T_R*x - y,  ydot = D_R*x - a_R

Zone requires T^2 < 4D (focus, not node/saddle) for a well-defined half-return.
T_L*T_R < 0 is a known necessary condition (Green's theorem) for any periodic
orbit at all -- used here as the negative control.
"""

import sys
import time

import numpy as np
from scipy.integrate import solve_ivp


def half_return(T: float, D: float, a: float, y0: float, t_max: float = 60.0):
    """First return to x=0 of the forward trajectory starting at (0, y0).

    Returns the y-coordinate at first return, or None if no return within
    t_max (trajectory escaped -- not a focus, or t_max too small).

    Uses solve_ivp's own `y_events` (interpolated at the event via its dense
    output under the hood) -- no second re-integration needed, and no forced
    `max_step` (adaptive RK45 step is both faster and, via dense interpolation
    at the root, at least as accurate as a fixed tiny step for locating x=0).
    """

    def rhs(t, state):
        x, y = state
        return [T * x - y, D * x - a]

    def event_x_zero(t, state):
        return state[0]

    event_x_zero.terminal = False
    event_x_zero.direction = 0

    sol = solve_ivp(
        rhs,
        [0.0, t_max],
        [0.0, y0],
        events=event_x_zero,
        rtol=1e-9,
        atol=1e-11,
    )
    te = sol.t_events[0]
    ye = sol.y_events[0]
    mask = te > 1e-9
    if not np.any(mask):
        return None
    idx = np.argmax(mask)  # first True
    return float(ye[idx, 1])


def composed_map(y0: float, TL: float, DL: float, aL: float, TR: float, DR: float, aR: float):
    """G(y0) = (R-zone half-return of L-zone half-return of y0) - y0.

    A root of G is a periodic orbit through (0, y0). y0 > 0 enters the L-zone
    (x<0); the resulting y1 < 0 enters the R-zone (x>0); a closed orbit
    requires landing back exactly at y0.
    """
    y1 = half_return(TL, DL, aL, y0)
    if y1 is None or y1 >= 0:
        return None
    y0p = half_return(TR, DR, aR, y1)
    if y0p is None or y0p <= 0:
        return None
    return y0p - y0


def count_sign_changes(TL, DL, aL, TR, DR, aR, y_grid):
    """Count sign changes of G over y_grid (>0). Each sign change brackets at
    least one root generically; returns (count, list of (y_lo,y_hi) brackets,
    list of None-gaps encountered)."""
    vals = []
    for y0 in y_grid:
        vals.append(composed_map(y0, TL, DL, aL, TR, DR, aR))
    brackets = []
    for i in range(len(vals) - 1):
        a, b = vals[i], vals[i + 1]
        if a is None or b is None:
            continue
        if a == 0.0:
            brackets.append((y_grid[i], y_grid[i]))
        elif a * b < 0:
            brackets.append((y_grid[i], y_grid[i + 1]))
    return len(brackets), brackets, vals


def refine_root(TL, DL, aL, TR, DR, aR, y_lo, y_hi, tol=1e-10, max_iter=100):
    """Bisection refine (robust; composed_map is not guaranteed smooth near
    None-gaps, so avoid Brent's method which assumes continuity)."""
    f_lo = composed_map(y_lo, TL, DL, aL, TR, DR, aR)
    f_hi = composed_map(y_hi, TL, DL, aL, TR, DR, aR)
    if f_lo is None or f_hi is None or f_lo * f_hi > 0:
        return None
    for _ in range(max_iter):
        y_mid = 0.5 * (y_lo + y_hi)
        f_mid = composed_map(y_mid, TL, DL, aL, TR, DR, aR)
        if f_mid is None:
            return None
        if abs(f_mid) < tol or (y_hi - y_lo) < tol:
            return y_mid
        if f_lo * f_mid < 0:
            y_hi, f_hi = y_mid, f_mid
        else:
            y_lo, f_lo = y_mid, f_mid
    return 0.5 * (y_lo + y_hi)


def run_case(label, TL, DL, aL, TR, DR, aR, y_max=20.0, n_grid=400):
    t0 = time.time()
    y_grid = np.linspace(1e-3, y_max, n_grid)
    n_sign_changes, brackets, _ = count_sign_changes(TL, DL, aL, TR, DR, aR, y_grid)
    roots = []
    for lo, hi in brackets:
        r = refine_root(TL, DL, aL, TR, DR, aR, lo, hi)
        if r is not None:
            roots.append(r)
    dt = time.time() - t0
    print(f"[{label}] TL={TL} DL={DL} aL={aL} TR={TR} DR={DR} aR={aR}", flush=True)
    print(f"    focus check: TL^2<4DL = {TL**2 < 4 * DL}, TR^2<4DR = {TR**2 < 4 * DR}", flush=True)
    print(
        f"    sign changes on grid (0,{y_max}]: {n_sign_changes}  roots: {[round(r, 6) for r in roots]}"
        f"  ({dt:.2f}s)",
        flush=True,
    )
    return n_sign_changes, roots


if __name__ == "__main__":
    sys.stdout.reconfigure(line_buffering=True)
    print(
        "=== Positive control: continuous case (a_L = a_R), known theorem says <=1 cycle ===",
        flush=True,
    )
    # Freire et al. 1998 / Carmona et al. 2019 proved AT MOST ONE limit cycle
    # when a_L = a_R (continuous matching). TL*TR<0 required for any cycle.
    # WHY these specific params, not the first guess: a --calibrate-positive-control
    # scan (35 configs) found these are an actual CYCLE-BEARING example (y*=2.887683)
    # -- the first two guesses tried here earlier both gave 0 cycles, which is
    # consistent with "at most 1" but vacuously so (doesn't exercise the n=1 code
    # path at all). Real positive control needs a case where the answer is nonzero.
    run_case(
        "continuous a_L=a_R=0.5 (has 1 cycle)",
        TL=-2.0,
        DL=5.0,
        aL=0.5,
        TR=0.5,
        DR=1.0,
        aR=0.5,
        n_grid=40,
    )
    run_case(
        "continuous a_L=a_R=2.0 (no cycle, still <=1 OK)",
        TL=-0.5,
        DL=2.0,
        aL=2.5,
        TR=0.8,
        DR=1.5,
        aR=2.5,
        n_grid=40,
    )

    print(flush=True)
    print("=== Negative control: T_L*T_R > 0, Green's theorem says 0 cycles ===", flush=True)
    run_case("same-sign traces", TL=0.3, DL=1.0, aL=1.0, TR=0.4, DR=1.0, aR=1.3, n_grid=40)

    if "--controls-only" in sys.argv:
        print(flush=True)
        print("=== --controls-only: skipping main search ===", flush=True)
        sys.exit(0)

    if "--calibrate-positive-control" in sys.argv:
        print(flush=True)
        print(
            "=== Calibration scan: find ANY continuous (a_L=a_R) config with a cycle ===",
            flush=True,
        )
        combos = [
            (-0.3, 1.0, 0.3, 1.0),
            (-1.0, 2.0, 1.0, 2.0),
            (-2.0, 5.0, 0.5, 1.0),
            (-0.5, 1.0, 2.0, 5.0),
            (-1.5, 1.0, 1.5, 1.0),
        ]
        found_any = False
        for TL, DL, TR, DR in combos:
            for a in (0.5, 1.0, 2.0, 4.0, 8.0, -1.0, -4.0):
                n, roots = run_case(
                    f"calib TL={TL} DL={DL} TR={TR} DR={DR} a={a}",
                    TL,
                    DL,
                    a,
                    TR,
                    DR,
                    a,
                    y_max=10.0,
                    n_grid=25,
                )
                if n > 0:
                    found_any = True
        print(f"=== calibration done, found_any_cycle={found_any} ===", flush=True)
        sys.exit(0)

    print(flush=True)
    print("=== Main search: discontinuous case, a_L != a_R, scan for >3 cycles ===", flush=True)
    rng = np.random.default_rng(20261003)
    best = (0, None)
    n_trials = 40
    for i in range(n_trials):
        TL = -rng.uniform(0.05, 2.0)
        TR = rng.uniform(0.05, 2.0)
        DL = (TL**2) / 4 + rng.uniform(0.05, 3.0)
        DR = (TR**2) / 4 + rng.uniform(0.05, 3.0)
        aL = rng.uniform(-5.0, 5.0)
        aR = rng.uniform(-5.0, 5.0)
        try:
            n, roots = run_case(f"trial {i}", TL, DL, aL, TR, DR, aR, y_max=15.0, n_grid=60)
        except Exception as e:  # noqa: BLE001 -- exploratory search, log and continue
            print(f"[trial {i}] FAILED: {e}", flush=True)
            continue
        if n > best[0]:
            best = (n, (TL, DL, aL, TR, DR, aR))
    print(flush=True)
    print(f"=== Best found over {n_trials} random trials: {best[0]} sign changes ===", flush=True)
    print(f"    params: {best[1]}", flush=True)
