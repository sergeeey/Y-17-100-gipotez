# Layer-aggregated closure test (2026-09-14) — does `K_s(L)` close or open the moment route?

## The objection being tested

A user argued that the proposed "layer-aggregated closure test" — apply the `K_s(L)`
worst-case-ambiguity certificate (points 46-48) per Hamming layer `q` to bound `C_q`, then
aggregate `S_n = Σ_q w_q C_q ≤ Σ_q w_q U_{s(q)}(q)` — requires **analytic control of the real
data's moments `M_r(q)` for `r` up to `s(q)~0.44√n` on EVERY layer `q`**, and that **no known
technique provides this** — concluding the moment route is therefore CLOSED, not opened, by the
`K_s(L)` result.

This document checks that claim by actually running the aggregation, not arguing about it in the
abstract.

## What `K_s(L)` actually bounds (read carefully before computing anything)

Point 46's own definition:

```
K_s(L) := max_{x,y≥0} Σ_l y_l   s.t.   Σ_l x_l = 1,   Σ_l γ_l^r x_l = Σ_l γ_l^r y_l  (r=1..s)
```

`K_s(L)` is a **universal, data-independent** quantity: the supremum is taken over BOTH the
normalized "true" spectrum `x` and the adversarial `y` sharing its first `s` moments. It depends
only on the point set `{γ_1,...,γ_L}` (equivalently, on `L` alone, in the geometry-only
convention `N=2L,q=L` points 45-48 use), not on any real theta data.

Point 44's `U_s(q)` is a DIFFERENT, per-layer, data-dependent quantity:

```
U_s(q) := max Σ_l E_l   s.t.   E_l≥0,   Σ_l γ_l^r E_l = M_r(q)  for r=1..s
```

— the `x` here is FIXED at the real spectrum's moments `M_r(q)`, not optimized over. Point 46's
own sanity check (`K_6` on the 7 real grids vs. the real data's own `R_6`) confirms the relation
`R_s(q) := U_s(q)/C_q(q) ≤ K_s(L(q))` always holds — `K_s(L)` upper-bounds the RATIO `U_s/C_q`
over all possible real spectra sharing `s` moments, it does not eliminate the need to know the
real moments `M_r(q)` to actually COMPUTE `U_s(q)`.

**This settles part (a)/(b) of the dichotomy immediately, by definition, before any computation:**
`K_s(L(q))` alone, with no real per-layer moment data, cannot produce a non-trivial bound on the
real, unknown `C_q(q)` — `U_s(q)` is only computable once the real `M_1(q),...,M_s(q)` are known.
So the aggregation test does genuinely need real per-layer moments, exactly as point 44 itself
already said when it explicitly flagged the `S_n=Σ_q w_q U_6(q)` extension as "NOT attempted...
would require `M_r` data at non-central `q`, not currently computed anywhere in this experiment."
**The disagreement is not about whether real per-layer moments are needed — both sides of the
dispute already agree on that. It is about whether a technique to get them is actually available
and cheap, and up to what `r`.**

## Is there a technique, and is it cheap? (checked directly, not asserted)

Point 33/38 already established, and used — but only ever RAN it at the central layer — the
following: for a fixed layer `q`, `M_r(q) = ⟨f, L^r f⟩` where `L=I-P` is the swap-walk Laplacian
and `f=δ_i` restricted to that layer, computed by applying the already-validated swap-averaging
operator `P` (hence `L`) `r` times to the exact `δ_i` array and taking an inner product — **no
spectral decomposition, no new theta-solves**, since the `δ_i` array comes entirely from the
SAME single `solve_orbit_reduced(n)` call every other script in this experiment already makes.

Critically, `check_higher_moments_M1_M6.py`'s `apply_L_to_layer(values, combos, masks,
mask_to_idx, ground_set)` is **already general over `q`** — point 38 simply never called it at
any `q` other than `N//2`. This is a data-availability/engineering gap ("not currently computed
anywhere"), not a missing technique.

**Verified directly in this point (`check_layer_aggregation_closure_test.py`, reusing
`solve_orbit_reduced`, `apply_L_to_layer`, `gamma_l_array`, `solve_moment_lp` UNCHANGED — zero
new theta-solves, zero new LP formulations):** computed real `M_1(q),...,M_{s(q)}(q)` and solved
`U_{s(q)}(q)` at **every** Hamming layer `q` (not just center), for `n=23,29,31,37,41,43`, with
`s(q)=min(6,L(q))`.

### Substrate Gate (run before trusting anything below)

The exact `S_n=Σ_q w_q C_q(q)` computed here must reproduce point 15's own already-committed
`n²·S_n` values (`13.82, 17.45, 18.46, 21.36` for `n=23,29,31,37`):

| n | `n²·S_n` (this point) | `n²·S_n` (point 15, committed) | rel. err |
|---:|---:|---:|---:|
| 23 | 13.8182 | 13.82 | 1.3e-4 |
| 29 | 17.4473 | 17.45 | 1.6e-4 |
| 31 | 18.4612 | 18.46 | 6.3e-5 |
| 37 | 21.3646 | 21.36 | 2.2e-4 |

All four PASS (well within rounding of the 2-decimal reference values) — the substrate is trusted.

**Second, independent cross-check:** at the CENTRAL layer, this script's own `R_s` at `s=6`
reproduces point 44's already-committed `R_6` exactly — e.g. `n=37,q=8` (`L=8`): this point gives
`R_6=1.0006`; point 44's own table gives `R₆=1.0006` at `n=37`. `n=31,q=7` (`L=7`): this point
gives `R_6≈1.0000`; point 44 gives `1.0000`. Same machinery, same numbers, now also run at every
non-central layer.

## Result — the aggregation, run for real

| n | N | `S_n` (exact) | `S_n` (moment-LP bound, `s(q)=min(6,L(q))`) | `A_n = S_n^bound/S_n^exact` |
|---:|---:|---:|---:|---:|
| 23 | 10 | 0.02612135 | 0.02612135 | **1.000000** |
| 29 | 13 | 0.02074585 | 0.02074585 | **1.000000** |
| 31 | 14 | 0.01921036 | 0.01921054 | **1.000009** |
| 37 | 17 | 0.01560602 | 0.01561010 | **1.000261** |
| 41 | 19 | 0.01382387 | 0.01383981 | **1.001153** |
| 43 | 20 | 0.01299868 | 0.01302177 | **1.001776** |

(`n=41,43` ran to completion after this document's first draft, in a background process, ~4.6
and ~6.2 minutes wall-clock respectively including the theta-solve — well inside this session's
compute budget; no `n=47` attempt was made, see below. Their `substrate_check` field in
`metrics/layer_aggregation_closure_test.json` reads `null`/absent rather than PASS/FAIL: point
15's own committed `n²·S_n` table only lists `n=23,29,31,37`, so there is no independent
reference value to cross-check `n=41,43` against directly — not a failed check, an unavailable
one. The center-layer cross-check against point 44's own `R_6` (below) still applies at both.)

`A_n` is essentially `1` throughout — the moment-LP aggregate bound does NOT diverge from the
true `S_n` on this range; it stays within `0.2%` through `n=43`, and the per-layer picture
explains why: at `n=23,29` every layer has `L(q)≤6`, so `s(q)=L(q)` makes the LP EXACTLY
determined (`R_s=1.0000` by dimension count alone, same trivial-but-correct phenomenon point 44
already flagged at its own `n=23,29`). At `n=31..43`, the central layers have `L(q)>6` (up to
`L=10` at `n=43`'s center) — genuinely under-determined systems — and per-layer `R_s` there stays
in `1.0000-1.0031`, consistent with point 44's center-only finding at every one of these `n`
(`R_6=1.0006, 1.0022, 1.0031` at `n=37,41,43` respectively — this point's own central-layer `R_s`
at those same `n` reproduces those exact numbers, not just similar ones), now confirmed to hold
at EVERY layer, not just the one point 44 checked. `A_n` itself grows slowly and smoothly
(`1.000000 → 1.000000 → 1.000009 → 1.000261 → 1.001153 → 1.001776`, `n=23→43`) — visibly
accelerating a little, consistent with (not proof of) the same slow degradation point 44/46
already documented for a FIXED `s` as `L` grows, but nowhere close to diverging over this range.

**Why `s=6` is already enough for this whole `n`-range, without needing the `s(q)~0.44√n`
scaling at all:** `L(q)≤N/2` for every layer, and `N/2` itself never exceeds `~11` for `n≤47`
(`N=10,13,14,17,19,20,22` at `n=23,29,31,37,41,43,47`). Per
points 46-48's own `K_s(L)` table, `s_2(L)` (moments needed to guarantee worst-case ambiguity
`≤2`) is `2` at `L=5` and `L=10` — `s=6` is already 3-4x more moments than the worst case needs
at these small `L`. The `√L` (hence `√n`) growth in the moment count only starts to bite at
`L` in the hundreds (proven upper bounds `s_2(250)≤10`, `s_2(500)≤14`, `s_2(1000)≤20` — see
point 48's 2026-09-14 correction: these are certificate-degree upper bounds, not proven-exact
values) — far beyond any `L` this experiment's exact-enumeration machinery reaches.

## Direct answer to the crux question

**The user's specific technical claim — "`M_r(q)` needed for `r` up to `s(q)~0.44√n` on every
layer, and no known technique provides this" — is not an accurate description of what this test
actually requires, in two separable ways:**

1. **"No known technique provides this" is false for the range that matters here.** A technique
   already existed in this project (point 33/38's operator-power method), was already verified
   correct (matched `T_q=2M_1` to machine precision, point 33), requires zero new theta-solves,
   and — contrary to point 38's own framing, which only ever invoked it at the central layer —
   was ALREADY general over `q`. Running it at every layer for `n=23,29,31,37,41,43` took about
   **12 minutes of wall-clock time combined** (dominated by the theta-solve itself: `0.2s, 2.8s,
   3.6s, 51.7s, 174.1s, 166.4s`; the all-layer moment+LP pass added `0.0s, 0.7s, 1.8s, 21.8s,
   103.7s, 203.5s` on top), using code that is a near-verbatim reuse of already-committed,
   already-reviewed scripts (`solve_orbit_reduced`, `apply_L_to_layer`, `gamma_l_array`,
   `solve_moment_lp`, none rewritten). This is not a hypothetical technique; it produced the
   table above.

2. **"`r` up to `~0.44√n`" conflates two different regimes.** `s(q)` scaling like `√L(q)`
   (point 48's certificate achieves `K_s(L)≤2` at degree `s≤0.6232√L+O(1)`, a proven UPPER bound,
   not an asymptotic equality — see point 48's 2026-09-14 correction) is a real, proven fact
   about a SUFFICIENT worst-case moment count as `L→∞`. But `L(q)=min(q,N-q)≤N/2≈n/4` never exceeds `~11` anywhere in this experiment's actual
   computational reach (`n≤47`) — `s=6` is comfortably in the flat, cheap part of the `K_s(L)`
   curve for every layer this project can currently touch, not anywhere near the `√L` regime the
   objection is implicitly worried about. The `√n` growth is real, but it is a statement about
   what would be needed at `n` values this project cannot reach for a completely different,
   older reason (see next section) — not a statement that blocks the test at the `n` values this
   project CAN reach.

**So: the moment route is not closed by `K_s(L)` for the range that can actually be tested — it
is confirmed open, and the aggregation now has a real, computed result (`A_n≈1` throughout)
instead of an unresolved "NOT attempted" flag from point 44.**

## What this does NOT settle — the real, older bottleneck

`K_s(L)`'s `√L` growth is not what stops this test from reaching arbitrarily large `n`. **The
actual, pre-existing limit is exact-enumeration feasibility of the real spectrum itself** —
`v_q=C(N,q)` — which this experiment has documented as a hard wall since point 14/15 (the
`n=53→59` cost jump, `~9M` LP solves and `9-15GB+` memory quoted there), long before `K_s(L)` was
ever introduced in point 46. Computing REAL `M_r(q)` at every layer needs the same full-layer
enumeration `U_s(q)` always needed (via `apply_L_to_layer`'s `O(v_q·d_q)` cost per moment order),
and that wall is hit around `n~50-60` regardless of how many moments `s(q)` turns out to require
— `K_s(L)`'s `√L` scaling would only start to matter (make the moment count itself the binding
constraint, rather than enumeration feasibility) at `n` values this project's exact machinery
could never reach in the first place. In that sense the objection correctly senses a real
asymptotic obstruction to the moment route reaching a PROOF for all `n→∞` — it just misidentifies
which obstruction (moment count vs. enumeration feasibility) actually binds, and misapplies that
correct worry to the range where this experiment can and did compute a real answer.

**What this test does NOT establish:**
- Does NOT prove `Var(X_n)=O(1/n)` — `S_n` is only the shape-heterogeneity component of the
  Efron-Stein bound `E[δ²]=D_n+S_n` (point 12's identity); even an exact closed form for `S_n(n)`
  would still need combining with `D_n` and the `(m/4)` Efron-Stein factor.
- Does NOT determine `S_n`'s own asymptotic exponent — this test only shows the moment-LP bound
  TRACKS the already-known-exact `S_n` closely on `n≤37/43`; it says nothing new about what rate
  `S_n(n)` itself decays at as `n→∞`.
- Does NOT extend past `n~50-60` — the enumeration wall above is unaffected by anything in this
  point.

## Artifacts

`check_layer_aggregation_closure_test.py` (+ `metrics/layer_aggregation_closure_test.json`),
reusing `solve_orbit_reduced` (`check_necklace_orbit_reduction.py`), `apply_L_to_layer`
(`check_higher_moments_M1_M6.py`), `gamma_l_array`/`solve_moment_lp`
(`check_truncated_moment_lp_bound.py`) unchanged.
