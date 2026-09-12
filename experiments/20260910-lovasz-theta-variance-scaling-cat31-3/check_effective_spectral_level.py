"""Exam 3, stage 2: the "effective spectral level" reformulation the user derived (2026-09-12)
from stage 1's tail_tightness data -- independently re-verified below before being trusted
(audit-verification-gate.md: the user's own "VERIFIED" is this session's "INFERRED" until an
independent computation confirms it).

Derivation (re-checked, not assumed): since gamma_l = l(N+1-l)/(q(N-q)) (already the swap-walk
gap formula used throughout points 15-21), the q(N-q) factor cancels in t_r := R_r/(D_r/gamma_r):

    1/t_r = [ sum_{l>=r} l(N+1-l)*E_l ] / [ r(N+1-r) * sum_{l>=r} E_l ]

i.e. 1/t_r is the tail's E_l-weighted average of l(N+1-l), normalized to 1 at the boundary value
r(N+1-r). Defining the "effective spectral level" l_eff via l_eff(N+1-l_eff) = r(N+1-r)/t_r
(the SAME quadratic, solved for the smaller root near r rather than the mirror root near N+1-r)
turns the abstract tightness ratio into a single number with a direct physical reading: "the
tail behaves, on average, as if its mass sat at level l_eff instead of exactly at level r".

At r=4, using the already-verified aggregate tail_tightness_4 from metrics/tail_concentration_
ratio.json (point 22): l_eff grows from 4.00 to 4.72 (n=23 -> 47) over N=10..22.

CORRECTED (2026-09-12, before this point was first merged -- caught by the user in the same
session): the naive fallback target "l_eff=O(N)" is nearly vacuous, and the growth-rate
diagnostic below (dividing delta:=l_eff-r by log(N)/sqrt(N)/N) does NOT discriminate between
growth classes on 7 points where delta starts at exactly 0 -- any subsequent positive delta
trivially makes each normalized ratio "increase from zero", which is an artifact of the
starting point, not evidence of a specific asymptotic rate. The diagnostic below is kept for
transparency (raw numbers, not an asymptotic-rate claim) but should NOT be read as showing
delta grows faster than any particular reference rate.

The REAL target, independently re-derived: since t_4 = 4(N-3)/(l_eff*(N+1-l_eff)), if
l_eff=o(N) at ANY rate (even l_eff~log log N), then N+1-l_eff~N and t_4 ~ 4/l_eff -> 0; if
l_eff~cN, t_4 -> 0 even faster (~1/N). So uniform constant-factor tail control (t_4>=c>0 for
fixed r=4) requires l_eff=O(1) -- a genuine finite limit, not just sub-linear growth. This is a
strictly stronger and more useful target than the initially-proposed O(N). Whether l_eff(N)
actually converges (Scenario A) or diverges even slowly (Scenario B, forcing a move to r=r(N))
is NOT resolved by 7 points spanning N=10..22 -- too short a range to distinguish a finite limit
from log log N, log N, or another slowly-diverging function.
"""

from __future__ import annotations

import json
from math import log, sqrt
from pathlib import Path

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"


def l_eff(r: int, big_n: int, t_r: float) -> float | None:
    """Solve l(N+1-l) = r(N+1-r)/t_r for the root near r (not the mirror root near N+1-r)."""
    if t_r is None or t_r <= 0:
        return None
    target = r * (big_n - r + 1) / t_r
    np1 = big_n + 1
    disc = np1 * np1 - 4 * target
    if disc < 0:
        return None
    return (np1 - sqrt(disc)) / 2


def growth_rate_fit(ns: list[int], deltas: list[float]) -> dict:
    """Raw diagnostic ratios for how (l_eff - r) compares to log(N)/sqrt(N)/N -- NOT a rate test.
    CORRECTED (2026-09-12, user-caught before merge): with delta=0 at the smallest N, every
    ratio trivially "increases from zero" once delta turns positive, regardless of the true
    growth class -- this does NOT discriminate 'bounded' from 'slowly diverging'. Kept only as
    raw transparency data (see decision.md point 23), not as evidence for any specific rate."""
    out = []
    for n, delta in zip(ns, deltas):
        out.append(
            {
                "big_n": n,
                "delta_l_eff": delta,
                "delta_over_log_n": delta / log(n) if n > 1 and delta is not None else None,
                "delta_over_sqrt_n": delta / sqrt(n) if delta is not None else None,
                "delta_over_n": delta / n if delta is not None else None,
            }
        )
    return {"points": out}


if __name__ == "__main__":
    tail_data = json.load(open(METRICS / "tail_concentration_ratio.json", encoding="utf-8"))
    agg = {a["n"]: a for a in tail_data["aggregate"]}

    ladder = json.load(open(METRICS / "l4_ladder_bound_analytic.json", encoding="utf-8"))
    big_n_by_n = {int(n_str): rows[0]["N"] for n_str, rows in ladder["per_layer"].items()}

    results = {}
    for r in [1, 2, 3, 4]:
        rows = []
        for n in sorted(agg):
            big_n = big_n_by_n[n]
            t_r = agg[n][f"tail_tightness_{r}"]
            leff = l_eff(r, big_n, t_r)
            delta = (leff - r) if leff is not None else None
            rows.append({"n": n, "N": big_n, "t_r": t_r, "l_eff": leff, "delta": delta})
            if leff is None:
                print(f"r={r} n={n:3d} N={big_n:3d} t_r={t_r:.4f} l_eff=None (no real root)")
            else:
                print(
                    f"r={r} n={n:3d} N={big_n:3d} t_r={t_r:.4f} l_eff={leff:.3f} delta={delta:.3f}"
                )
        results[r] = rows

    print("\n=== Growth-rate diagnostics for r=4 (delta = l_eff - 4) ===")
    r4_rows = [row for row in results[4] if row["delta"] is not None]
    fit = growth_rate_fit([row["N"] for row in r4_rows], [row["delta"] for row in r4_rows])
    for pt in fit["points"]:
        print(
            f"  N={pt['big_n']:3d}  delta={pt['delta_l_eff']:.3f}  "
            f"delta/log(N)={pt['delta_over_log_n']:.4f}  "
            f"delta/sqrt(N)={pt['delta_over_sqrt_n']:.4f}  delta/N={pt['delta_over_n']:.5f}"
        )

    METRICS.mkdir(exist_ok=True)
    with open(METRICS / "effective_spectral_level.json", "w", encoding="utf-8") as f:
        json.dump({"per_r": results, "r4_growth_fit": fit}, f, indent=2)
