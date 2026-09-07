# decision.md — 20260907-chernoff-neuralode-nd-numerical-abscissa-boundary (H-B2-1p)

## Result

Pre-registered discriminating criterion: **MIXED**. N=64 individually significant, positive
(rho=0.298, p=0.0209) — comparable in strength to N=16/N=32. N=80 NOT significant (rho=0.088,
p=0.506) — small positive, but nowhere near N=40/50's near-exact-zero (rho=0.007).

| N_DIM | rho | p | n |
|---|---|---|---|
| 64 | 0.298 | 0.0209 | 60 |
| 80 | 0.088 | 0.506 | 60 |

Fisher combination (context only, not the primary criterion per claim.md — 2 slices is too few
to combine meaningfully): stat=9.10, p=0.0586 — itself borderline, consistent with mixed evidence.

Neither pre-registered clean reading is supported: not REAPPEARS (would need both N=64 AND N=80
significant), not CEILING_CONFIRMED (would need neither significant). The pre-registered MIXED
outcome fired correctly and is itself informative — see below.

## Skeptic Pass on the Post-Hoc Framing (run BEFORE finalizing this decision — the first draft of
this section made a real methodological error, corrected below, not just hedged)

A context-asymmetric skeptic pass on the retrospective FDR/binomial analysis (originally drafted
below) returned **`[WEAKENED]`**, and correctly identified that the first draft's framing was not
just optimistic but methodologically invalid, not merely a caveat-worthy oversimplification:

1. **Retrospective pooling of 3 separately pre-registered experiments into one "7-arm study" for
   BH-FDR is illegitimate.** BH's Type-I control assumes the p-value SET is fixed before
   inspection. Here the set is a post-hoc artifact of which experiments happened to run and how
   they landed — not a pre-planned family.
2. **N_DIM=64 and 80 were NOT chosen from a fixed grid — they were chosen ADAPTIVELY, specifically
   BECAUSE N=40 and N=50 were null, to test whether the signal "reappears."** This is optional-
   continuation / a mild garden-of-forking-paths pattern: `claim.md` for this very experiment says
   so explicitly ("reading 1 predicts recovery... reading 2 predicts continued nullity"). The
   binomial `P(X>=3|null, 7 tests)=0.0038` assumes a fixed, pre-planned set of 7 independent
   tests — that assumption is false here, and the true false-positive rate under adaptive
   continuation is higher than 0.0038, possibly substantially.
3. **N=64's significance (p=0.0209) cannot be treated as independent evidence for a real,
   reappearing relationship** — it was found by a search that was explicitly looking for
   reappearance and would plausibly have tried further dimensions had N=64 also come back null.
   This is drawer-selection, not a clean discriminating test result.
4. **"Intermittent, not monotonic" is NOT established** as a positive claim — the 7 points are
   equally consistent with (a) a real small-N effect plus one adaptively-selected false positive
   at N=64, (b) a genuinely non-monotonic mechanism, or (c) noise amplified by optional
   continuation. This experiment cannot discriminate between them.

**What DOES survive, per the skeptic's own assessment:** `omega(A)` correlates with M1 at small-
to-mid N (N=16, N=32 — pre-registered-strength evidence, p<0.01 each, not weakened by this
critique). The correlation weakens/disappears at N in {40,50,80}. **Whether it "reappears" at
N=64 is NOT established** by this experiment, because N=64 was picked adaptively after seeing the
N=40/50 null, not from a pre-planned grid.

**Kill criterion for resolving this, named but not launched:** pre-register a FIXED grid
(decided before running anything, e.g. N in {56, 64, 72}) in ONE new experiment, blind to the
hope of "recovery." If N=64 replicates at p<0.05 in that pre-registered pass, reappearance is
real. If not, the H-B2-1p result was drawer-selection, and the honest read becomes "signal at
small N only, vanishes by N~40 and does not measurably return."

## Original (Corrected-In-Place) Post-Hoc Framing — Kept For Transparency, Superseded Above

Putting this experiment's 2 new slices alongside the 5 already tested in `H-B2-1o` gives the
full picture the arc has built so far:

| N_DIM | rho | p | individually significant (alpha=0.05)? |
|---|---|---|---|
| 16 | 0.357 | 0.00514 | yes |
| 24 | 0.254 | 0.05049 | borderline (no) |
| 32 | 0.368 | 0.00380 | yes |
| 40 | 0.007 | 0.9587 | no |
| 50 | 0.007 | 0.9570 | no |
| 64 | 0.298 | 0.0209 | yes |
| 80 | 0.088 | 0.506 | no |

This is neither a clean decay (would predict N=64,80 both null, matching N=40,50) nor a clean
recovery (would predict N=64,80 both significant, matching N=16,32) — it is **intermittent**:
significant at N in {16,32,64}, not at N in {24,40,50,80}. Before treating this as evidence of a
real, non-monotonic mechanism, the honest first question is whether 3/7 "hits" at alpha=0.05 is
even distinguishable from a pure multiple-comparisons artifact across 7 independent tests run
over the course of this arc, with no correction applied at any individual step.

**Post-hoc, walled off from the pre-registered MIXED verdict above (same Anti-Overfitting Gate
discipline as `H-B2-1o`'s own partial-conjunction check — computed on already-collected/already-
published data, no new experiment, reported for honest context, NOT used to promote or demote
any individual experiment's verdict):**

- `P(X>=3 significant out of 7 independent tests | pure null, alpha=0.05) = 0.0038`. Getting 3
  (or more) "hits" purely by chance across 7 tests, if there were truly NO relationship anywhere,
  is unlikely. This weighs AGAINST the "it's all multiple-comparisons noise" reading.
- **Benjamini-Hochberg FDR correction (q=0.05) across all 7 slices ever tested for `omega(A)` vs
  M1 in this arc:** N=32, N=16, and N=64 survive FDR correction (ranks 1-3 of 7, p <= BH
  threshold); N=24, N=80, N=50, N=40 do not. This is the same 3 slices the raw per-slice test
  flagged — the FDR-corrected result is not weaker than the naive one here, which is itself
  informative (a real, if scattered, signal, not simply "the loosest test happened to catch 3").
- Fisher combination across ALL 7 slices ever tested: p=0.00076 (carries the SAME heterogeneity-
  hiding caveat `H-B2-1o`'s skeptic pass raised for the 5-slice case — reported for completeness,
  not read as "uniform across N").

**What this means, stated carefully:** the `omega(A)`-M1 relationship in this population is real
at SOME dimensions (N in {16,32,64}, surviving FDR correction) and genuinely absent at others
(N in {40,50}, rho~=0.007 twice — not just underpowered) with intermediate/ambiguous cases in
between (N=24 borderline, N=80 weak-but-not-significant). Neither "decays with N" nor "recovers
uniformly beyond a boundary" describes this — the honest description is **intermittent**, and
this arc does not currently have a mechanistic explanation for WHICH dimensions show the
relationship and which don't. This is a genuine, informative, if unsatisfying, result.

## Kill Analysis

**What this experiment killed:** the clean "unlucky pair, signal recovers uniformly" reading
(REAPPEARS) — N=80 stayed null, so recovery is not uniform. It did NOT kill "genuine ceiling",
because N=64's status is itself unresolved (adaptive-selection confound, see skeptic pass above)
— CEILING_CONFIRMED is not established false, only not cleanly confirmed either.

**What this experiment did NOT kill:** the solid small-N result (N=16, N=32 — real, pre-
registered-strength, unaffected by the skeptic's critique). **What remains genuinely unresolved,
corrected from the first-draft framing:** whether N=64's apparent recovery is real or an artifact
of adaptively choosing to test exactly the dimension most likely to look interesting after two
nulls. This is now the open question, not "what distinguishes {16,32,64} from {24,40,50,80}" —
that framing assumed N=64 was solid evidence, which the skeptic pass showed it is not.

## What This Does NOT Mean

1. Does NOT establish `omega(A)` as periodic, oscillating, or "intermittent" in N — the skeptic
   pass showed this reading rests on an invalid retrospective multiple-comparisons correction
   over an adaptively-selected, not fixed-in-advance, set of N_DIM values.
2. Does NOT retroactively change `H-B2-1o`'s CONFIRMED-but-scoped verdict, or `H-B2-1n`'s
   WEAKENED verdict — those stand on their own pre-registered criteria, unaffected by this
   experiment's own N=64/80 adaptive-selection issue.
3. Does NOT establish causality.
4. Does NOT establish that N=64's significance is spurious either — only that it CANNOT be
   trusted as independent evidence given how it was selected. A genuine pre-registered fixed-grid
   replication (see Relaxation Map) is required to resolve it either way.

## Relaxation Map / Next Steps (not auto-launched)

- **The correct next step, named by the skeptic pass:** pre-register a FIXED grid (e.g. N in
  {56, 64, 72}, chosen before running anything, not because 40/50 were null) in ONE new
  experiment. If N=64 replicates at p<0.05 there, reappearance is real, not drawer-selection.
- This session stops the H-B2-1* chain here per the explicit user framing ("все по очереди")
  having reached a natural inflection point: the honest state of the arc is now "solid at small-
  mid N (16,32), vanishes by N~40-50, N=64's status unresolved pending a properly pre-registered
  fixed-grid replication" — not a mechanistic hypothesis to chase further without that
  replication first.

## Pearl Registry Update

Corrected finding (the FIRST DRAFT of this decision.md briefly asserted an "intermittent, not
monotonic" pattern using a retrospective FDR correction over adaptively-selected N_DIM values —
a real methodological error, caught by a same-session skeptic pass and corrected in place, not
just caveated): `omega(A)`-M1 correlates solidly at N in {16,32}, is genuinely null at N in
{40,50}, and N=64's apparent significance (p=0.021) cannot be trusted as independent evidence
because it was selected specifically to test for "reappearance" after the N=40/50 null — a mild
optional-stopping / garden-of-forking-paths pattern. A concrete, pre-registered fixed-grid
replication (N in {56,64,72}, decided before running) is named as the correct next test to
resolve N=64's true status, but not launched.
