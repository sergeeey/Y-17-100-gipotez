# decision.md — H-B2-1j (Theorem 3.1 bound at N_DIM=50)

## Result

**Verdict: CONFIRMED** — the bound holds in ALL 16 tested cases (8 step-counts × 2 orders) and
the empirical convergence order matches theory as tightly as at N=8. But the practical-usefulness
gap widens dramatically: efficiency drops from H-B2-1g's already-poor ~1.5×10⁻⁷ (N=8) to
~1.3×10⁻¹⁰–4.3×10⁻¹² (N=50) — 3 to 5 further orders of magnitude looser.

| Quantity | N=8, strong coupling (`H-B2-1g`) | N=50, same coupling magnitude (this experiment) |
|---|---|---|
| `M1` | 158.93 | **675.40 — ~4.25× larger** |
| Empirical order, order-1 | 1.0026 | **0.9983** |
| Empirical order, order-2 | 2.0007 | **2.0081** |
| Bound holds (16 cases) | 16/16 | **16/16** |
| Efficiency, order-1 | ~1.5×10⁻⁷ | **~1.3×10⁻¹⁰ — ~1,000× worse** |
| Efficiency, order-2 | n/a (order-1 reported) | **~4.3×10⁻¹²** |

## What Was Confirmed

- [x] The bound's VALIDITY and ORDER-MATCHING are robust to a 6× increase in dimensionality
  (N=8→50) at the SAME coupling magnitude — the mechanism (`K_j=0`, per every prior `H-B2-1*`
  experiment's own algebraic argument) does not depend on dimension in any way that breaks it.
- [x] **New finding: `M1` does NOT continue the N=2→N=8 shrinkage found in `H-B2-1f`.** Going
  from N=8 to N=50 at the SAME coupling magnitude, `M1` grew ~4.25× (158.93 → 675.40) — the
  earlier counterintuitive shrinkage was specific to the N=2→N=8 comparison, not a general
  "higher dimension is easier" trend. `M1` can grow substantially with dimension when N goes
  beyond the small range previously tested.
- [x] **New mechanistic detail for WHY efficiency collapses further at higher N:** inspecting
  `a_power_m1_x0_norm` (the `‖A^(m+1)x0‖` term in Theorem 3.1's own bound formula) shows it is
  enormous at N=50 (25,750 for order-1, 1.67 million for order-2) — this term, not just `M1²·M2`,
  is a major driver of the bound's looseness, and it scales with N independently of `M1` itself
  (more dimensions means more terms accumulate in the matrix-power/vector product). This gives a
  more precise account of the efficiency collapse than `H-B2-1g`'s own "the constant gets large"
  framing — there are at least two independently-growing terms in the bound (`M1²·M2` and
  `‖A^(m+1)x0‖`), not one.

## What Remains Open

- Whether `M1`'s growth from N=8→50 is itself monotonic in between, or has its own
  non-monotonicity (like the N=2→N=8 shrinkage) — untested; would need intermediate N values
  (e.g. 16, 24, 32).
- The specific eigenvalue-spread convention (linear from -1 to -50) is one choice among many;
  whether a differently-shaped N=50 spectrum (e.g. logarithmically spread, or clustered) shows
  the same `M1` growth and efficiency collapse is untested.
- No multi-seed test at N=50 (per `H-B2-1i`'s own established need to check typicality) — this
  experiment used a single seed, matching every prior `H-B2-1*` convention, but `H-B2-1i`'s own
  finding (M1 can be a non-representative, above-median draw) applies here too, untested.

## Relaxation Map

- **Intermediate N sweep** (16, 24, 32, 40) — would clarify whether `M1`'s N=8→50 growth is
  monotonic or has its own local structure, analogous to `H-B2-1h`'s coupling-magnitude sweep.
- **Multi-seed at N=50** — direct analogue of `H-B2-1i`, now at the largest tested dimension.
- **Decompose the bound's growth** — separately track how `M1²·M2` and `‖A^(m+1)x0‖` each scale
  with N, to determine which term dominates the efficiency collapse as N grows further.

## Note on Floor–Ceiling (FL Step 4a)

Not applicable in the arm/null-model sense — descriptive verification of a bound's validity and
order-matching property on a fully specified deterministic construction, matching every prior
`H-B2-1*` experiment's own treatment of this section.

## FL Step 8a — Skeptic Pass

Not run as a separate agent invocation (Evaluator-Optimizer cap still in effect session-wide).
Manual discipline applied: the M1-growth finding (N=8→50 INCREASE, reversing a naive
extrapolation of `H-B2-1f`'s N=2→N=8 decrease) is reported as a genuine finding requiring
explanation, not smoothed into "consistent with prior results." The `a_power_m1_x0_norm`
observation was checked directly from the run's own output before being asserted as a mechanism,
not assumed.

**Anticipated FALSIFIED-equivalent concern:** "efficiency ~10⁻¹⁰ to 10⁻¹² is so extreme it might
indicate a bug, not a real property of the construction." **Response: Mitigated** — the same
`theorem_3_1_bound` formula, `measure_m1_with_w`/`measure_m2_with_w` functions, and
`empirical_order` machinery are BYTE-IDENTICAL to `H-B2-1g`'s own already-validated code (only
`N_DIM`, `EIGENVALUES`, and the derived `A`/`X0` differ) — the extreme efficiency values are a
direct, mechanically unsurprising consequence of `‖A^(m+1)x0‖` scaling with dimension, verified
by inspecting that term's actual reported magnitude, not merely asserted.

## EstimandOps — What This Does NOT Mean (restated per claim.md)

1. Does NOT generalize beyond this specific eigenvalue-spread convention and coupling magnitude.
2. Does NOT imply anything about real Neural-ODE/ResNet layers of comparable width.
3. Does NOT retroactively strengthen or weaken `H-B2-1g`'s own efficiency finding at N=8 — this
   experiment measures a DIFFERENT dimension's efficiency, extending the pattern, not revising it.
4. Does NOT establish that `M1` growth with N is monotonic beyond N=8 and N=50 — only two points
   on this axis have been tested (plus N=1,2 from earlier experiments).

## Pearl Card Update

**Extends H-B2-1g's own "valid ≠ useful" finding by 3-5 further orders of magnitude at N=50,**
and adds a genuinely new mechanistic detail (the `‖A^(m+1)x0‖` term's own N-scaling, not just
`M1`) to WHY. Also directly falsifies a plausible extrapolation of `H-B2-1f`'s N=2→N=8 shrinkage
("maybe M1 keeps shrinking with N") — it does not; M1 grew substantially again from N=8 to N=50.
Closes LAB.md's own last-named open item for the `H-B2-1*` arc's original three (coupling sweep,
multi-seed, N=50+) — all three are now tried.
