# decision.md — H-B2-1j (Theorem 3.1 bound at N_DIM=50)

## CORRECTION ADDENDUM (2026-09-07, FL Step 8a skeptic pass — second real one this session)

**The M1-growth finding is DOWNGRADED from "genuine reversal of H-B2-1f's shrinkage" to
"uninterpretable due to a confound this experiment itself contains."** Original text kept below
unedited (Hindsight Distortion Gap discipline); this dated correction sits on top. Found by the
same context-asymmetric `Agent(skeptic)` invocation pattern used on `H-B2-1l` immediately before
this one, in the same `/loop` continuation.

**What the skeptic found, given only `claim.md` + `run.py` (plus permission to read `H-B2-1g`'s
own source directly to check the transcription, which it did):**

1. **[Confirmed — the fatal one]** This experiment's own eigenvalue construction
   (`[0.5] + linspace(-1, -50, 49)`) changes BOTH `N_DIM` (8→50) AND the spectral range
   (`max|λ|` 8→50) simultaneously, relative to `H-B2-1g`. Per claim.md's own "Scope Decision —
   Explicit" section, this was claimed as "only `N_DIM` changes... per the Minimal Relaxation
   Rule" — **that claim is false as written**. The coupling block also grew from 8×8 to 50×50 at
   the same per-entry amplitude, which itself increases its expected operator norm by roughly
   √(50/8)≈2.5×. **At least three things changed at once**, not one. The M1 growth
   (158.93→675.40) cannot be attributed to dimension specifically — it is confounded with
   spectral range and coupling-block size. **Directly ironic:** the very same session later
   built `H-B2-1k` specifically because it recognized this exact confound and deliberately fixed
   it (holding spectral range fixed while varying N) — but never went back to flag that `H-B2-1j`
   itself, one experiment earlier, has the confound `H-B2-1k`'s own claim.md explicitly names as
   something to avoid. That gap sat unnoticed until this skeptic pass.
2. **[Confirmed, minor]** `empirical_order`'s single global log-log slope can mask local
   variation. Checked directly against the committed `per_n` data (not left as speculation):
   local pairwise orders for order-1 are 0.9923 (n=50→100) rising monotonically to 0.9999
   (n=3200→6400); for order-2, 2.0307 falling to 2.0006. A small, real, monotonic trend — the
   coarsest step is measurably (though not dramatically, <3.1% off theoretical) less clean than
   the asymptotic tail. The reported global estimates (0.9983, 2.0081) are a reasonable summary,
   not a misleading one, but the claim "matches theory AS TIGHTLY as at N=8" slightly overstates
   it: `H-B2-1g`'s N=8 system (max|λ|=8) doesn't carry this same coarse-step artifact because it
   isn't as stiff. This is a real, if small, side effect of the confound in point 1 — a stiffer
   system takes longer to reach the asymptotic convergence regime.
3. **[Accepted, reframing]** "Bound holds 16/16" is a much weaker claim than it sounds at
   efficiency ~1e-10 to 1e-12 — the bound is so loose it is a near-certain pass by construction
   for any well-behaved linear system, not a meaningful stress test of the theorem. This was
   already partially reflected in the original text's own "efficiency drops... 3 to 5 further
   orders of magnitude looser" framing, but the skeptic's sharper point stands: CONFIRMED here
   mostly certifies "the formula was computed without a sign/power error," not "the mechanism
   was meaningfully stress-tested."

**What survives:** the bound's formal VALIDITY (holds in 16/16 cases, byte-identical formula
to `H-B2-1g`'s own validated code) and the qualitative fact that convergence order is close to
theoretical (with the small coarse-step caveat above) — these are not confounded, they hold
regardless of what else changed in the construction. **What does NOT survive:** the "M1 does NOT
continue the N=2→N=8 shrinkage" finding as an isolated dimensionality effect, and the "matches
theory as tightly as N=8" framing (real but overstated).

**Corrected honest statement:** *At N=50 (with spectral range and coupling-block size ALSO
changed, not isolated), the Theorem 3.1 bound remains formally valid and the empirical order
remains close to theoretical (with a small, verified, stiffness-related coarse-step deviation).
The observed M1 growth (158.93→675.40) is NOT attributable to dimension alone — this experiment
does not isolate that variable, despite claiming to. `H-B2-1k`'s later, properly-isolated N-sweep
(fixed spectral range) is the experiment that actually answers "does M1 grow with dimension
specifically," and its own finding (non-monotonic M1(N)) supersedes this one's confounded
comparison.*

**Response Matrix disposition:** Confirmed (1, fatal to the M1-attribution claim), Confirmed (2,
minor, verified with real numbers not left as speculation), Accepted (3, reframing). Bound
validity and order-matching are NOT killed by any of the three.

**Process note:** this is the SECOND genuine skeptic pass of the session (after `H-B2-1l`,
run minutes earlier in the same `/loop` continuation) — both found real, previously-unnoticed
flaws. Neither was a false alarm or a stylistic nitpick.

---

## Result (ORIGINAL TEXT, superseded in part by the correction above — kept for the audit trail)

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
