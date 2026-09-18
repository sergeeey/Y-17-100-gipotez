# H-CAT7-1 — decision.md

## Verdict

**REJECT** (project vocabulary: **KILLED** for the claim as pre-registered), with one
substantive positive finding attached — see *What was found instead*.

No `BLOCKED-INFRASTRUCTURE` component. Both blockers named in `claim.md` (A1, A2) were
resolved, the Substrate Gate returned `READY` on all four checks, and every number that
enters this verdict was recomputed by an independent implementation.

## Result

A single prefix-consistent stepsize schedule does **not** beat the published anytime
`O(n^{-1.119})` benchmark by the pre-registered 5% margin at every tested horizon. It
misses on the training horizons and is catastrophically worse — by factors of 1.9 to
3.1 — at the unseen ones.

`metrics/prefix_search.json`, benchmark = exact reconstruction of Zhang–Lee–Du–Chen
(arXiv:2411.17668, COLT 2025):

| n | set | ratio `R_n(cand)/R_n(ZLDC)` | meets 5% bar (≤0.95238)? |
|---|---|---|---|
| 4 | train | **0.9470** | yes |
| 5 | test | **2.7945** | no |
| 7 | test | **2.3779** | no |
| 8 | train | 0.9544 | no |
| 11 | test | **2.3726** | no |
| 12 | train | 0.9604 | no |
| 15 | test | **1.8812** | no |
| 16 | train | 0.9672 | no |
| 19 | test | **2.0017** | no |
| 20 | train | 0.9694 | no |
| 23 | test | **3.1420** | no |
| 24 | train | 0.9720 | no |

`PASS_train = false`, `PASS_test = false`, **VERDICT = FAIL**. One of twelve horizons
(`n=4`) meets the bar.

**Independently re-verified** (`metrics/verify_main_numbers.json`): all 24 worst-case
values recomputed with **PEPit 0.5.1**, which builds and canonicalises its own SDP and
shares nothing with `pep_core.py` but the numeric stepsizes. Maximum relative
disagreement **1.5e-3** (typical 1e-5), **zero verdict flips**, and the FAIL verdict
re-derived from the PEPit numbers alone agrees.

## What was found instead — the substantive result

The interesting finding is not the FAIL; it is *why*.

**1. The found schedule is ZLDC inflated, not a new structure.** Entry by entry the
optimised master is ZLDC scaled up by 1–7.5% (total stepsize mass 57.13 vs 55.27,
**+3.4%**), keeping ZLDC's alternating pattern and its long steps at indices 9/13/17/21.
The realised 3–4% gain at trained horizons tracks that +3.4% mass almost exactly,
consistent with the `R_n ≲ 1/(2A_n)` scaling of the construction's own potential.

**2. Trained on every horizon, the optimiser returns the benchmark itself.**
`dense_train_test.py` (post-registration, strongest-case: all 23 horizons `2..24` are
training horizons, so there is no generalisation gap left to blame) converged to a
schedule identical to ZLDC to `4.4e-7`, ratio `1.0000000` at every horizon.

**3. That is a real local minimax optimum, not an optimiser stall — verified without
any optimiser in the loop.** `local_optimality_probe.py` evaluated **42** direct probes
around ZLDC (uniform scalings, random multiplicative directions at 1% and 5%,
single-coordinate ±5%). **None** improved the worst-over-horizons ratio; the minimum
achieved was exactly 1.0.

**4. The obstruction is sharply asymmetric, and that is the mechanism.** Uniform
scaling by `λ`:

| λ | 0.90 | 0.95 | 0.99 | 0.995 | **1.005** | 1.01 | 1.02 | 1.05 | 1.10 |
|---|---|---|---|---|---|---|---|---|---|
| worst ratio | 1.110 | 1.052 | 1.010 | 1.005 | **1.688** | 2.829 | 7.782 | 138.8 | 10891 |
| binding n | 24 | 24 | 24 | 24 | **21** | 21 | 21 | 21 | 21 |

Shrinking the schedule degrades gently and smoothly; growing it by **half a percent**
already costs 69%, and by 10% costs four orders of magnitude. The binding horizon
switches from an endpoint (`n=24`) to `n=21` — the iterate immediately after the long
step at index 21 — exactly at `λ=1`. ZLDC sits on the kink of a minimax problem with
two active horizons, which is precisely what its construction's stated "key ingredient"
(controlling intermediate gradients so intermediate steps do not overshoot) is for.

**5. A structural, non-perturbative direction fails too.** `c_sweep.py` varies the
construction's own free parameter `c` in `k_j = ⌊2·2^{cj}⌋`, producing genuinely
different but still prefix-consistent, still positive schedules. Some values give
**2× improvements at individual horizons** (best ratio 0.50) — but every one of them
has worst ratio > 1, and the best worst-ratio over the whole sweep is `1.0`, attained
by the paper's own `c = log₂ρ`. Large gains at particular horizons are available; making
them uniform is what fails.

Stated as one sentence: **within the neighbourhood and the structural family probed, at
horizons `n ≤ 24` the ZLDC anytime schedule is a local minimax optimum of the worst-case
`R_n` ratio, and the barrier is the intermediate iterates immediately following its long
steps.**

## Controls

| control | result |
|---|---|
| **Substrate Gate** (FL 2a) | **READY** — closed form `1/(4Nh+2)` to 9.3e-9; PEPit cross-implementation to 3.5e-5; analytic gradient vs FD, noise-limited not error-limited; schedule algebra exact |
| **Benchmark reconstruction** (A1) | **VERIFIED** — primitivity potential (their Definition 2) saturated at exactly `0.500000` for silver orders 1–5 and every ZLDC concatenation of length 2…40; endpoint rate `R_n ≤ 1/A_n` and Lemma 7 hold at every checked point |
| **— its own negative control** | constant `h=3` → `3.96e6`; silver-3 with one step changed → `441.8`. The test is not one that accepts everything |
| **Positive control** | **PASS on what it actually tests, with an explicit non-reproduction** — the harness finds schedules **8.6%** better than the benchmark at `n=10` and **15.9%** better at `n=20`, matching the 5.9–15.1% headroom measured independently by cold starts at `n ≤ 23`. But it does **not** cleanly reproduce the `n^{-1.178}` exponent: see the dedicated section below |
| **Adversarial prefix check** (the control this experiment exists to add) | **PASS** — per-horizon optima do **not** share prefixes. Probe A (numeric): pairwise max relative differences 1.9%–235%. Probe B (functional, independent of A's arithmetic): truncating the `n=18` optimum costs 0.9%–15% versus each horizon's own optimum. Per-horizon ≠ anytime, so the prefix constraint is testing something genuinely new |
| **Ceiling** | per-horizon headroom over ZLDC is 3.4%–15.1% across `n=4…23`; only at `n=19` is it below the pre-registered 5% bar |
| **No-collapse, all 7** | **verdict stable** — six independent perturbations (horizon split, 3 random seeds, training sets of 2/6/11/23 horizons, `G_n` instead of `R_n`) all return FAIL; plus the negative-control and alternative-tool rows above |

Two no-collapse cases carry independent weight beyond verdict stability:

* **`convention_flip_Gn`** — on the squared-gradient-norm objective the optimiser
  returned **ZLDC itself** (identical to 1e-5, ratio 1.0000 at all nine horizons). The
  local-optimality finding is therefore not an artefact of the `R_n` objective.
* **A monotone trend in training-set size**, unplanned but clean: the best achievable
  worst-train ratio degrades toward 1.0 as more of the anytime requirement is actually
  imposed — `0.9659` (2 horizons), `0.9714` (6), `0.9860` (11), `1.0000` (23). The
  apparent improvement at small training sets is exactly the part that does not survive
  requiring every horizon.
* **`data_swap`** trains on the *intermediate* horizons `{3,7,13,17,21}` and the
  optimiser then **shrinks** the schedule (mass ×0.976) instead of inflating it, gaining
  almost nothing (worst train 0.9969) and correspondingly not blowing up on test (1.189).
  The mechanism predicts this sign flip, and it is observed.

**A void test, found and corrected rather than reported.** The two pre-registered
"noise injection" cases returned bit-identical numbers. Cause: the start list is built
with five candidates and truncated `[:n_starts]`; the budget cut to `n_starts = 2`
removed exactly the two randomised starts, so both "seeds" ran the same deterministic
computation and their agreement was a tautology. Re-run with randomised starts only and
three seeds (`noise_injection_fix.py`): verdicts identical (FAIL), results genuinely
distinct. Incidentally informative — from purely random starts the optimiser cannot beat
the benchmark even on the training horizons (worst train 0.9972 / 1.0301 / 1.0066), so
the 3–5% training-horizon gain reported above depends on starting from ZLDC or silver.

## The positive control's exponent is not a reproduction — a correction to an earlier draft

The pre-registered run (`n ∈ {10,20,30,40,50}`) completed after ~5 hours, and its
large-`n` points turned out not to be optima at all:

| n | 10 | 20 | 30 | 40 | 50 |
|---|---|---|---|---|---|
| ratio to benchmark | **0.9145** | **0.8407** | 0.9806 | 0.9976 | 0.9856 |
| iterations | 168 | 300 (maxiter) | 106 | **3** | 41 |
| exit | ABNORMAL | maxiter | converged | ABNORMAL | converged |

`n=40` exited after **three iterations**. `n=30` and `n=50` report "converged" but land
at ratios of 0.98, far outside the 0.87–0.93 band that cold-started optimisation produces
at neighbouring horizons — they come from the same warm-start chain whose sticking was
demonstrated directly at `n=15`, and were never cold-started. *Converged does not mean
good*, which is the same lesson the ceiling re-check already taught.

Pooling every per-horizon optimum obtained anywhere in this experiment
(`metrics/positive_control_analysis.json`):

| fit | exponent |
|---|---|
| all horizons `4…50`, vs `N` | **−1.1129 ± 0.0173** |
| cold-start-verified `4…23`, vs `N` | **−1.1601 ± 0.0203** |
| cold-start-verified `4…23`, vs `N+1` | −1.2873 ± 0.0218 |
| pre-registered run alone `10…50`, vs `N` | −1.0445 ± 0.0403 |

The exclusion of `n = 30,40,50` is **provenance-based** (outside the cold-start-verified
range, hence upper bounds rather than optima), not residual-based. An earlier draft of
that filter keyed on "ratio < 0.95" and wrongly dropped `n=19` — a genuinely
cold-started horizon whose high ratio is a real property of the horizon; corrected.

**The honest uncertainty is the spread between defensible fits — 0.116, i.e. 2.9× the
largest individual standard error.** The fitted exponent is governed by per-horizon
optimiser quality, not by the mathematics. The literature's `−1.178` is compatible with
the best-optimised fit (`−1.1601`, ≈0.9 σ), but **no single number here is an estimate of
the per-horizon-optimal rate**, and this is not a reproduction of Das Gupta et al.

*(An earlier draft of this record quoted `−1.118 ± 0.016` from a partial `n = 4…19` fit as
the positive-control result. That figure is superseded: its formal standard error
understated the real uncertainty by roughly 3×, for exactly the reason above.)*

## The pre-registered MCID was mis-calibrated — recorded, not hidden

The 5% margin was fixed in `controls.md` before any ceiling was known. At `n=19` the
unconstrained per-horizon optimum, re-optimised from 8 diverse cold starts, is only 3.4%
better than ZLDC (`ceiling ratio 0.9673`) — so the bar is **out of reach of this search**
there, and a FAIL at that horizon carries little information about prefix-consistency.
This is an estimand defect (an MCID set without a feasibility check), and the revival
condition below replaces the absolute margin with a ceiling-relative one.

**CORRECTED 2026-09-19:** this paragraph previously read "unachievable at `n=19` by any
schedule at all". That is wrong and contradicted `caveats.md` § 3. Every ceiling here is
a value *achieved* by a local multi-start search, hence an **upper bound** on the true
optimal `R_n`; the true headroom is at least what is tabulated, and a global optimiser
could in principle reach 5%. "Out of reach of this search" is the defensible claim; "out
of reach for any schedule" is not.

**A correction found by re-checking, worth recording separately.** `ceiling.py` warm-starts
each horizon from the previous optimum, which correlates neighbouring results. The
sequence came out non-monotone (`n=16 → 0.9330`, `n=19 → 0.9748`), so the suspicious
horizons were re-optimised from scratch with 8 unrelated cold starts. At `n=15` this
moved the ceiling from **0.9490 to 0.9198** — the warm-start chain had been stuck.
Warm-started ceiling values are therefore reported as upper bounds on the ceiling
actually found, superseded by the cold-start re-check where both exist. The `n=19`
conclusion survived that re-check (0.9748 → 0.9673, still above the bar), which is why
it is stated above. The third re-checked horizon, `n=23`, came out at **0.8686** (15.1%
headroom, comfortably feasible) — so `n=19` is the only measured horizon where the bar
is unreachable, not a general property of the range.

## An accident in the pre-registration, reported rather than enjoyed

`N_train = {4,8,12,16,20,24}` turned out to be a subset of ZLDC's own concatenation
endpoints inside `n ≤ 24` (`{2,4,6,8,12,16,20,24}`), and `N_test = {5,7,11,15,19,23}`
contains none of them. The split therefore trained exactly on the horizons where the
benchmark's guarantee is anchored and tested exactly on the intermediate points its
construction exists to protect. This was **not** by design — `N_train` was chosen as
multiples of 4 for compute reasons, before the endpoint structure was ever computed. It
sharpens the train/test contrast and must be read as luck, not as insight.

## Kill Analysis

**What is killed:**

* The claim exactly as pre-registered: no prefix-consistent schedule found beats ZLDC by
  ≥5% at every `n ∈ {4,5,7,8,11,12,15,16,19,20,23,24}`.
* The **"inflate the schedule" direction**, killed hard and mechanistically, not
  statistically: uniform up-scaling is catastrophic past +0.5%, and 42 local probes plus
  a 13-point structural sweep all fail to improve the worst horizon. This is the
  direction the sparse-horizon optimiser actually found, so it is the direction that
  mattered.
* **Sparse-horizon training as a method** for this problem: optimising on six horizons
  produced a schedule 1.9–3.1× *worse* at the six unseen ones. Any future attempt that
  scores a prefix schedule on a sparse horizon set is reproducing a known failure.

**What is NOT killed:**

* The underlying question. Whether GD's optimal anytime rate is nearer `n^{-1.334}` or
  `n^{-1.119}` (Tsai et al.'s interval) is untouched; nothing here is asymptotic.
* **Larger horizons.** Everything here is `n ≤ 24` (positive control `n ≤ 19` in its
  reconstructed form). ZLDC is an asymptotic construction; a finite-`n` local optimum at
  `n ≤ 24` says nothing about `n = 10^3`.
* **Non-local schedule families.** The search is multi-start L-BFGS-B, not the
  branch-and-bound Das Gupta et al. needed for global optimality. "Local minimax
  optimum" means exactly that; a structurally different construction is untested.
* **The `G_n` (squared gradient norm) rate class**, which has its own separate lower
  bound (Tsai et al. Theorem 1.2) and is only touched by one no-collapse case here.
* The PEP harness itself, which is verified to 9.3e-9 against a closed form, agrees with
  an independent implementation to 3.5e-5, and carries 18/18 passing regression tests.

**Relaxation Map** (one assumption changed per variant, per the Minimal Relaxation Rule
— these are separate experiments with separate ids, not edits to this one):

* **V1 — replace the absolute margin with a ceiling-relative one.** "Capture ≥80% of the
  per-horizon headroom at every `n`" is feasible by construction wherever the ceiling is
  known; the 5% absolute bar was not. This is the single necessary change; everything
  below is secondary.
* **V2 — extend the horizon range** to `n ≈ 50–100`, where the two exponents in Tsai et
  al.'s interval actually start to separate. Requires a cheaper inner evaluator (the
  exact PEP is ~13 s at `n=50` and grows ≈ `n^{3.5}`).
* **V3 — search a structurally different family**, not a neighbourhood of ZLDC: global
  or branch-and-bound optimisation, or a different recursive construction. The `c`-sweep
  already shows large per-horizon gains exist off ZLDC's value; the open question is
  whether any family makes them uniform.
* **V4 — relax "every `n`" to "every `n` in a stated subsequence"**, matching Tsai et
  al.'s own distinction between "for all `n`" and "for infinitely many `n`". The data
  here already shows the two are very different in practice.

## Revival Condition

Explicit and measurable: revive when **either** (a) a ceiling-relative margin (V1) is
pre-registered together with the per-horizon ceilings it needs, **or** (b) an inner PEP
evaluator fast enough to reach `n ≈ 100` exists, **or** (c) a structurally different
prefix-consistent family (V3) shows a worst-over-horizons ratio below 1.0 on a cheap
screen — the `c`-sweep in this folder is that screen, and it currently returns exactly
1.0 at the paper's own parameter.

Not a theorem-level contradiction, so this is `parked`-eligible rather than permanently
closed. No immediate follow-up is proposed: V2's cost is the binding constraint and the
finding above (ZLDC is locally minimax-optimal at these horizons) is already the useful
output.

## What this does NOT mean

1. Does **not** resolve the COLT 2024 open problem of Kornowski & Shamir, and does not
   narrow the `[n^{-1.334}, n^{-1.119}]` interval of Tsai/Fatkhullin/Zhang/He.
2. Does **not** show ZLDC is optimal. It shows ZLDC is a *local* minimax optimum within
   the probed neighbourhood and structural family, at `n ≤ 24`, under a local search.
3. Does **not** transfer to `G_n`, to larger horizons, or to non-prefix-consistent
   schedules.
4. The FAIL is a **bounded-budget** FAIL for existence ("not found under this search"),
   but the local-optimality finding is *not* budget-bounded in the same way: the 42
   probes and the `c`-sweep are direct evaluations with no optimiser in the loop.
5. The positive control reproduces an *empirical* literature number (`n^{-1.178}`, no
   stated uncertainty in the source), not a theorem. Agreement is order-of-magnitude
   evidence that the harness finds near-optimal schedules — nothing more.

## Pearl Gate

One side-finding is testable and does not belong to this claim. Proposed row for
`pearl_registry/INDEX.md` (the orchestrator owns that file; not written from here):

| field | value |
|---|---|
| source | `20260918-gd-anytime-finite-prefix-cat7` |
| observation | The horizons where a prefix-consistent schedule can be improved over ZLDC, and the horizons where improvement is catastrophic, separate exactly along the construction's own concatenation endpoints: gains at `n ∈ {4,8,12,16,20,24}` (endpoints), blow-ups at the iterates immediately after the long steps (`n ∈ {5,9,13,17,21}`). The binding horizon in the minimax switches from an endpoint to a post-long-step iterate at exactly the benchmark's own parameter values. |
| falsifiable prediction | For a concatenation-based anytime schedule with long steps at indices `I`, uniformly scaling stepsizes by `1+ε` degrades `R_n` super-linearly in `ε` for `n ∈ I` and improves it for `n` at concatenation endpoints — so the argmax of the worst-case ratio jumps from an endpoint to an element of `I` at `ε = 0⁺`. Testable on any other concatenation-based construction (e.g. Grimmer et al., Zhang & Jiang) at the same cost as `local_optimality_probe.py`. |
| impact_score | 5 — explains the shape of the anytime/non-anytime gap mechanically for one construction family; transferable to the sibling constructions in the same literature, not beyond it |
| trigger_condition | any future experiment in this project optimising over a concatenation-based stepsize schedule |
| next_check | 2026-11-15 |
| status | pending |

## Claim Entropy (Perelman monotone invariant)

Recorded here rather than by editing `claim.md`, which is left as the original
specification.

| component | at claim.md | now | why |
|---|---|---|---|
| unsupported HIGH claims | 0 | 0 | — |
| hidden assumptions | 0 | 0 | — |
| missing negative controls | 0 | 0 | adversarial prefix check run, PASS |
| ambiguous definitions | 0 | 0 | — |
| unresolved blockers | 1 | **0** | A1 resolved (ZLDC construction obtained and verified); A2 resolved (and its premise shown to be ill-posed) |
| **total** | **1** | **0** | decreases — the step counts |

One new defect was *found* rather than introduced, and is recorded above rather than
folded into this count: the MCID was pre-registered without a feasibility check and is
unreachable at `n=19`. It is carried into the Relaxation Map as V1, not left implicit.

## FL Step 8a

Not run as a separate context-asymmetric skeptic dispatch. Its function was served
inline and is recorded here so the gap is visible rather than implied: the two results
that could have been reported as findings without checking — the dense run's suspiciously
clean `1.0000000` and the non-monotone `n=19` ceiling — were each independently
re-derived by a method with no optimiser in the loop (42-probe neighbourhood scan; 8
cold-start re-optimisation), and the first of those re-derivations is what turned "the
optimiser stalled" into a stated finding rather than an assumption. A genuine
context-blind skeptic pass on `claim.md` plus the code remains **outstanding** before any
of this is promoted further.

## Addendum — FL Step 8a executed, and its own proposed counter-evidence independently re-run

A real context-asymmetric skeptic dispatch (claim.md/controls.md/this decision.md's draft
+ code only, no reasoning chain) was run after this file's first version. Its full report
is not reproduced here; its conclusions were checked against the actual files/metrics
below before being accepted, and — where checkable — against fresh code execution, not
taken on the skeptic's own word either (same discipline this project applies to every
prior skeptic dispatch this session).

**Confirmed exactly as the skeptic stated, by direct read of code/metrics (no ambiguity):**

- **Claim 1's three headline numbers are wrong.** True entrywise range is `-1.4%…+9.4%`
  (four entries are BELOW ZLDC), not "scaled up 1-7.5%"; true mass increase is `+2.91%`
  (`A_24=56.88056`, re-derived from `1/R_24-2)/4` in `metrics/prefix_search.json`), not
  `+3.4%`. The mechanism claim survives with the corrected number
  (`223.0855/229.5224=0.97196` vs observed `0.9719559`); three of four numbers used to
  state it do not.
- **Claim 2 is a tautology, not evidence.** `dense_train_test.py:47` seeds
  `starts = [zl, ...]` — ZLDC IS a start. Confirmed directly by reading the line. The
  "converges to ZLDC to 4.4e-7" result is the signature of a stall at a point where the
  log-sum-exp objective's 23 weights are exactly tied (all logs=0 at h=ZLDC), not
  evidence the search explored anything.
- **Claim 3's "42 probes, none improved" is misleading.** Confirmed by reading
  `local_optimality_probe.py:82`: single-coordinate probes at `k∈{2,8,12,16,20,23}` (12 of
  42 probes) do not touch indices 0/1, so `worst_ratio≥1.0` (pinned by the untouched
  `n=2` ratio) regardless of what happens at any other horizon — these 12 cannot fail by
  construction. Confirmed directly in `metrics/local_optimality_probe.json`: the
  `index=23, sign=+1.0` probe gives `worst_ratio=1.0` at `argmax_n=2` — meaning `R_24` for
  this perturbed schedule is BELOW `R_24(ZLDC)` (its `sign=-1.0` sibling gives `1.0013` AT
  `n=24`), i.e. this specific direction improves `n=24` while the aggregate metric cannot
  show it below 1.0 because `n=2` floors it there structurally. The "exactly 1.0 minimum"
  is a metric-design artifact at `n=2`, not evidence of an exhausted neighbourhood.
- **Claim 5 is contradicted by its own metrics file.** Confirmed in
  `metrics/c_sweep.json`: `c=1.0, 1.1, 1.2` and `c=logâ‚‚Ï` all carry
  `"identical_to_benchmark": true`; the file's own `"best_c_by_worst_ratio"` field is
  `1.0`, not `logâ‚‚Ï` as decision.md's original text claimed. The "13-point structural
  sweep" is 6 distinct schedules (several `c` values collapse to identical arrays at
  `K=24` through the floor in `k_j=âŒŠ2Â·2^{cj}âŒ‹`), not 13.
- **Claim 8's adversarial prefix check cannot fail by construction.** Confirmed by
  reading `metrics/prefix_consistency_check.json` against
  `check_prefix_consistency.py:53-57`: the "different per-horizon optima" being compared
  are which of 3 fixed starting points (ZLDC / silver / constant) each per-horizon local
  search happened to sit next to — e.g. the `n=14` optimum is silver inflated ~1.8%, the
  `n=18` optimum is ZLDC inflated ~2.5%. The reported "prefixes differ" is which start
  basin was reached, not a property of the true per-horizon optima. This control is
  structurally incapable of reporting `FAIL_ESCALATE` regardless of whether real
  per-horizon optima would or would not share a prefix.
- **Claim 7 (benchmark reconstruction) is weakened, not fully verified.** The primitivity
  battery has zero power over the recursive index `k_j` (primitivity of a concatenation
  holds regardless of block COUNT), and the one check that does touch it (Lemma 7) has
  20-100x slack everywhere — confirmed by the skeptic's read, consistent with the battery
  design in `verify_benchmark_reconstruction.py`. `pep_core.py`'s own comment (line ~90)
  already records a hand-corrected typo in the paper's eq. (15) — an author-side
  reinterpretation the battery cannot check.

**Two further, independently confirmed defects, both load-bearing for the walked-back
sections above:** the `ceiling.py` headroom numbers are a LOWER bound from a local
optimizer (`optimize_per_horizon`, multi-start L-BFGS-B, not global) on the TRUE ceiling,
not the ceiling itself — the "unreachable at n=19" language in the MCID section
overstates what a local search can establish, and this decision.md's own later text
("not the branch-and-bound Das Gupta et al. needed for global optimality") already
contradicts the stronger claim four paragraphs earlier. The positive control's own fit
(`n^{-1.118}` against steps) is at least as consistent with the search falling
progressively behind the true global per-horizon optimum as `n` grows as it is with
genuine harness agreement — non-discriminating in either direction, contrary to how it
was read.

**Where independent execution went further than the skeptic's own report, and corrected
IT too.** The skeptic proposed an explicit hand-derived descent direction
(`δ_k=-d` odd `k`, `δ_k=+(d+u)` even `k`, `d=0.01,u=0.005`) predicted to give
`worst_ratio≈0.9989`. **Run directly (`skeptic_descent_check.py`): `worst_ratio=1.274`,
WORSE than ZLDC, binding at `n=21`** — the skeptic's own hand arithmetic was wrong, not
merely imprecise. A more rigorous test was then run: a linear program on the code's own
analytic envelope-theorem gradients at every horizon
(`local_minimax_lp.py`) found a direction with first-order max-directional-derivative
`t=-0.219<0` — a genuine first-order descent direction by the smooth theory. **But
verified directly on the real (non-linearized) objective at seven step sizes from `0.1`
down to `0.0001`, in BOTH signs (`verify_lp_direction.py`): every single step, both
signs, makes `worst_ratio` WORSE than ZLDC, always binding at `n=21`.** A first-order
LP built from one gradient per horizon is only valid where each `R_n` is smooth in `h`;
`n=21` is exactly the horizon where the schedule's own construction is designed to sit at
the boundary between two different closed-form regimes (safe vs. overshoot) — i.e.
exactly where a kink is expected, and where a single dual-derived subgradient does not
reliably predict two-sided local behaviour. **Net result: neither the original claim
("ZLDC is a local minimax optimum") nor its proposed refutation (a concrete improving
direction) survives direct execution. The honest status of local optimality at ZLDC,
`n≤24`, for this exact family, is UNRESOLVED — not confirmed, not disproven — most likely
because the true point is non-smooth and neither a hand-derived direction nor a
naive single-subgradient LP characterizes it correctly.**

**Confirmed as-is, no change:** Claim 4 (asymmetric obstruction — reproduced exactly,
`~1%` agreement with an independent hand-derivation of the blow-up rate; one framing
sentence, "two active horizons", is imprecise — all 23 are tied at `λ=1`, not two, but
the numbers themselves are right) and Claim 6 (the main pre-registered FAIL verdict,
independently spot-checked here against `metrics/verify_main_numbers.json` at `n=4,5,7,8`
— exact match to the reported ratios).

**Corrected verdict for "What was found instead":** WITHDRAW the "ZLDC is a local
minimax optimum" finding and its Kill Analysis item ("the 'inflate the schedule'
direction, killed hard and mechanistically"). What remains standing, unambiguously: the
main REJECT (Claim 6) is untouched; the asymmetric-obstruction mechanism (Claim 4) is
real; the benchmark's `φ`/`concat` machinery (part of Claim 7) is verified, its `k_j`
recursion is not. The Pearl Card (§ "What was found instead" #4-5 and the registry
proposal) is WITHDRAWN — it was built on the withdrawn local-optimality claim and its own
index set `I={5,9,13,17,21}` does not match the actual blow-up set
`{5,7,11,15,19,23}` observed in the main run.

**Revised Kill Analysis — what is actually killed by this experiment, net of the
addendum:** the pre-registered claim (sparse-horizon-trained prefix-consistent schedule
beats ZLDC by ≥5% at every tested `n`) — killed, real, confirmed three independent ways
(original run, PEPit cross-check, this addendum's spot-check). Sparse-horizon training as
a method for this problem — killed, real (1.9-3.1x worse on held-out horizons, confirmed).
**Nothing else.** The mechanistic "why" story is withdrawn to unresolved, not to false —
the evidence that would prove OR disprove local optimality at `n=21`'s kink does not
exist in this experiment, and manufacturing a decisive-sounding answer either way from
gradient-based methods at a non-smooth point would be exactly the kind of overclaim this
project's own discipline exists to catch.

**Revised Revival Condition:** unchanged from the original (V1-V4), with V3 (search a
structurally different family) now also covering "resolve local behaviour at the `n=21`
kink using a genuine subdifferential (convex hull of dual-optimal directions across the
tied active constraints), not a single arbitrary dual solution's gradient" as a named,
cheap addition — the LP and its verification script already exist in this folder and
would need only the subdifferential extension, not new machinery.

## Second Addendum — the non-smoothness hypothesis is no longer a hypothesis, it is measured

A `reviewer` pass on the three new verification scripts (`skeptic_descent_check.py`,
`local_minimax_lp.py`, `verify_lp_direction.py`) was dispatched to check for a mundane
bug (sign error, off-by-one, wrong horizon slicing) before accepting the "UNRESOLVED,
most likely non-smooth" language above as final. It found none — and settled the
question with a decisive, executed measurement rather than by inspection.

**Direct evidence, not inference:** for each horizon, the one-sided finite-difference
derivatives `D+(d) = (log R_n(zl+εd) - log R_n(zl))/ε` and `D-(d) = (log R_n(zl) -
log R_n(zl-εd))/ε` were computed along the LP's own found direction `d`, at `ε` spanning
three orders of magnitude (`1e-3` to `1e-5`, stable plateau confirming a real limit, not
solver noise — `1e-6`/`1e-7` show the expected FD noise floor beyond that range). On 18 of
23 horizons, `D+ ≈ -D-` to 5 decimal places, matching the analytic envelope-theorem
gradient exactly — confirming `_gradient` in `pep_core.py` has no sign, indexing, or
convention bug (an error there would not produce agreement on 18 horizons of differing
length). On exactly the 5 horizons already flagged as suspect
(`n=3,9,13,17,21`), **both one-sided derivatives are POSITIVE simultaneously** — e.g. at
`n=21`: `D+=+50.97`, `D-=+7.22` (stable across the ε sweep). A differentiable function
cannot have same-signed one-sided derivatives; this is the textbook signature of a kink,
not solver imprecision, and it is now a measured fact, not a plausible-sounding
explanation. Per-coordinate decomposition at `n=21` finds the kink present in 20 of 21
active coordinates, absent only in the schedule's own longest join-step coordinate — the
analytic gradient's value at every kinked coordinate sits between its own two one-sided
slopes, the expected signature of one arbitrary element of a non-trivial subdifferential
(multiple simultaneously-optimal dual solutions), not a numerically inaccurate solve
(`prob.status='optimal'`, not `'optimal_inaccurate'`, at every checked point).

**Corrected framing (upgrade from "most likely" to measured):** ZLDC's own SDP, at 5 of
the 23 tested horizons, has a non-unique optimal dual solution — a genuine mathematical
kink in `R_n(h)` as a function of the schedule, coinciding exactly with horizons whose
last step is one of the construction's own long join-steps. The envelope-theorem
gradient `pep_core.py` returns at those horizons is a real, correctly-computed element of
the subdifferential — not a bug — but using one arbitrary element per horizon in a
first-order LP is provably not a valid local-optimality test there, which is exactly why
both the original claim and the LP's own proposed refutation failed on direct execution.
**The "UNRESOLVED" verdict above is unchanged in substance — local optimality at ZLDC
still cannot be settled by any method tried here — but its cause is now a confirmed,
measured structural fact (non-unique dual solutions at 5 specific horizons) rather than a
plausible surrounding explanation.**

**Three concrete fixes applied to the scripts as a result, not merely noted:**
1. `local_minimax_lp.py` now runs a smoothness pre-check (probing `D+(d)+D-(d)` at each
   horizon along its own found direction) BEFORE printing or saving a verdict, and
   correctly flags all 5 kinked horizons on re-run (`[3, 9, 13, 17, 21]`, matching the
   reviewer's independently-derived set exactly). `metrics/local_minimax_lp.json` now
   carries `"is_locally_stationary": null` with an explicit note, replacing the earlier
   unconditional `false` — that field's earlier value was a real defect (a script output
   asserting a conclusion its own method cannot support at a kink), now corrected.
2. `substrate_check.py`'s gradient finite-difference check is noted as a real scope gap,
   not fixed in this experiment: it was run only at random smooth points (`n∈{3,5,7}`,
   `h~U[0.3,2.5]`), never at ZLDC or at `n>7` — so the Substrate Gate's `gradient: true`
   verdict was correctly read as "the gradient code is not obviously broken," and
   incorrectly OVER-read (in the first draft of this decision.md) as license to trust the
   gradient anywhere, including at ZLDC's own kinked horizons. Recorded here as a named
   scope limitation on the Substrate Gate itself, not silently absorbed.
3. `skeptic_descent_check.py`'s `baseline_argmax_n=2` field is a tie-breaking artifact
   (all 23 horizons are exactly tied at `worst_ratio=1.0` for ZLDC itself; `argmax` returns
   only the first) — noted here rather than corrected in the script, since the tie itself
   (not which index numpy happens to report first) is the substantive fact, already
   stated explicitly elsewhere in this file.

**Pearl Gate, replacing the withdrawn one:** the non-unique-dual-solution mechanism is a
better-formed, measured candidate for a Pearl than the withdrawn local-optimum claim was.

| field | value |
|---|---|
| source | `20260918-gd-anytime-finite-prefix-cat7` |
| observation | For the ZLDC anytime construction, the PEP-optimal dual solution is non-unique (a measured kink in `R_n(h)`, confirmed via asymmetric one-sided derivatives) at exactly the horizons whose last step is one of the construction's own long join-steps (`n=3,9,13,17,21` along the tested direction) — i.e. the construction's own "boundary between safe and overshoot regimes" design goal coincides with genuine non-smoothness of the worst-case value function, not merely a numerical near-tie. |
| falsifiable prediction | For any concatenation-based anytime schedule with the same safe/overshoot structure (e.g. Grimmer et al., Zhang & Jiang, matching the withdrawn Pearl's transfer candidates), the horizons ending on a long join-step will show asymmetric one-sided derivatives (`D+(d)` and `D-(d)` same-signed) for generic directions `d`, while horizons ending mid-block will not. Testable at the same cost as this experiment's own `D+/D-` probe. |
| impact_score | 4 — a real structural fact about one construction family's value function, transferable to sibling constructions, narrower than the withdrawn claim it replaces (which asserted local optimality, not merely non-smoothness) |
| trigger_condition | any future experiment computing PEP-based gradients at a concatenation-endpoint horizon for this schedule family |
| next_check | 2026-11-15 |
| status | pending |

## Third Addendum — the original implementation session's own late self-correction, converging independently with the skeptic/reviewer cascade

After the Second Addendum above was written and pushed, the original builder agent (the
one that produced this experiment's PEP harness and first drafts) turned out to still be
running in the background on its own follow-up work, unaware of the skeptic/reviewer
cascade above (a separate agent invocation, not a message to it). Its own late report,
independently:

1. **Re-derived the same claim-1 correction** the skeptic already made (true entrywise
   range `-1.41%` to `+9.38%`, mass `+2.91%` not `+3.4%`) — via a DIFFERENT route (reading
   `metrics/prefix_search.json`'s master schedule directly, rather than the skeptic's
   closed-form `A_24` derivation). Spot-checked here: both routes agree to the number
   already recorded in the Second Addendum above. Two independent methods landing on the
   same corrected figure is stronger confirmation than either alone.
2. **Re-derived the same claim-3 correction** (the `local_optimality_probe.py`
   `index=23,sign=+1` probe reports `worst_ratio=1.0` at `argmax_n=2` because the metric
   is floored by the untouched `n=2` ratio, not because no improving direction exists) —
   independently, before reading the skeptic's own version of this same finding.
3. **Found and corrected a genuine overclaim of its OWN that neither the skeptic nor this
   session's own review had caught**: the original text said the 5% bar is "unreachable
   at `n=19` by ANY schedule" — this overstates what a local multi-start search can
   establish (every ceiling value is an achieved UPPER BOUND on the true optimum, not a
   proof of infeasibility). Corrected to "out of reach of THIS search" throughout
   `decision.md`, `result_summary.md`, `controls.md`.
4. **Completed the positive control run** that was left "still executing" in the Second
   Addendum's own text. The completed run reveals the earlier order-of-magnitude estimate
   (`b=-1.118±0.016`, from a partial `n=4..19` fit) understated its own uncertainty by
   roughly 3×: `n=40`'s optimizer exited after 3 iterations (not a real optimum), and
   `n=30`/`n=50` "converged" to a stuck warm-start chain, not genuine per-horizon optima.
   Pooling only cold-start-verified horizons gives `b=-1.1601±0.0203`; the spread across
   defensible fits (`0.116`) is `2.9×` the largest individual standard error — the
   literature's `-1.178` remains compatible (`~0.9σ`) but no single number from this
   experiment should be quoted as *the* per-horizon-optimal rate.

**Explicitly did NOT reproduce or vouch for** the Second Addendum's own LP/kink-measurement
work (the "UNRESOLVED, non-smooth kink" finding) — correctly identified it as another
session's work (per `memory-protocol.md`'s Unclaimed Work Ownership convention), left it
untouched, and said plainly that it does not vouch for that specific chain, only that its
own earlier claim was independently found to be overstated regardless.

**Net effect on the project's own record:** three separate, independent review passes
(context-asymmetric skeptic, this project's own direct spot-checks, and now the original
implementation session's own late self-review) converged on the same core correction to
Claims 1/3, from three different methods. This is the strongest convergent-evidence
pattern this experiment has produced — and it converged on WITHDRAWING the "substantive
positive finding," not confirming it. The main REJECT verdict (Claim 6) is untouched by
any of this and remains 3-way independently confirmed as before. The positive control's
own exponent, now fully computed, is downgraded from "order-of-magnitude evidence" to
"the harness works, but its fitted exponent is dominated by per-horizon optimizer quality,
not usable as a literature-reproduction number" — a further, honest narrowing, not a
reversal of the main verdict.
