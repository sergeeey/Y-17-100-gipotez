# H-CAT31-3 — decision.md

## Result

### Substrate Gate — passed

Both closed-form checks reused from `H-CAT31-1` passed before any new large-n solve was
trusted: `theta(C_5) = 2.236068` (exact `sqrt(5)`); `theta(G)*theta(Gbar) = 9.000000` (exact,
`n=9` spot-check, Lovász 1979 identity). No environment/dependency drift since the original
sweep.

### Negative control — passed

At `p=0` (degenerate empty graph, 5 seeds): all 5 `theta` values identical
(`15.999999999999991`), `Var(log(theta/sqrt(n))) = 0.0` exactly. The estimator can register
zero, not just report noise as a default.

### Primary finding

| n | reps | mean(θ/√n) | Var(log(θ/√n)) | bootstrap 95% CI |
|---:|---:|---:|---:|---|
| 32 | 300 | 1.0727 | 0.117049 | [0.0977, 0.1389] |
| 64 | 300 | 1.0536 | 0.054780 | [0.0454, 0.0636] |
| 128 | 300 | 1.0270 | 0.031585 | [0.0264, 0.0372] |
| 256 | 250 | 1.0208 | 0.015032 | [0.0126, 0.0175] |
| 512 | 200 | 1.0126 | 0.008854 | [0.0070, 0.0110] |
| 1024 | 150 | 1.0048 | 0.005134 | [0.0042, 0.0061] |
| 1536 | 100 | 1.0099 | 0.003888 | [0.0027, 0.0053] |
| 2048 | 80 | 0.9954 | 0.001936 | [0.0014, 0.0025] |
| 3000 | 40 | 1.0005 | 0.001809 | [0.0010, 0.0027] |

**Mean ratio confirms `E[theta]/sqrt(n) -> 1`** (as required by `E[theta]>=sqrt(n)`, already
`KNOWN-BY-GENERAL-THEOREM` per the deep external novelty audit's Track 2) — converges cleanly
from 1.073 at `n=32` to within +/-0.5% of 1.0 by `n=3000`, no drift, no anomaly.

**Variance fit (pre-registered weighted OLS, weights from bootstrap-CI-derived precision):**

```
slope  = -0.9126  (unweighted OLS: -0.9122, near-identical)
SE     =  0.0264
95% CI = [-0.9751, -0.8501]   (t(7), 2-sided)
```

**Stability check (not pre-registered, run after the fact as a sanity diagnostic):** slope on
the first 6 points (`n=32..1024`) = **-0.900**; slope on the last 6 points (`n=256..3000`) =
**-0.897** — near-identical across the two halves of the range.

**CORRECTED CALIBRATION (2026-09-10, user-caught overclaim in the first version of this
section):** the original wording here said the stability check "argues against" / "excludes" a
finite-size-correction-toward-`-1` explanation. That is stronger than the data supports and has
been walked back. The precise, defensible statement is:

> No detectable drift toward -1 over `n=32..3000`; a *simple* finite-range correction
> explanation is disfavored, but an asymptotic `-1` beyond the observed range is NOT ruled out.

Specifically NOT excluded by this check: a slowly-varying correction of the form
`Var(X_n) = C*n^-1*L(n)` where `L(n)` changes slowly enough that the *effective* exponent stays
near `-0.9` across several decades of `n` (a well-known phenomenon in statistical mechanics and
number theory — e.g. `L(n) ~ (log n)^p` or similar — would be invisible to a same-slope check
over only ~2 orders of magnitude). A genuine crossover to `-1` at `n >> 3000` is also not
excluded. The split-half check only rules out the SPECIFIC, simplest story (a correction term
that has mostly decayed away by `n=1024` and continues decaying at the same visible rate) — it
is one falsified sub-hypothesis among several possible explanations, not a general exclusion.

## Verdict

**REJECTED for the pre-registered `-1` exponent hypothesis** (per `claim.md`'s own Kill
Criterion: the weighted-OLS 95% CI `[-0.9751, -0.8501]` does NOT contain `-1.0`). The CI DOES
cleanly exclude both `-0.5` and `-2.0` as well — this is a **precise, well-powered
measurement**, not an inconclusive one: the data discriminates `-1` from its neighbors with
real statistical power (CI half-width ~0.06), not a wide, uninformative interval that happens
to miss `-1` by construction.

**This is a genuine, informative negative result for the specific `-1` conjecture — not a
failure of the experiment.** The exponent is real, precisely measured, and close to but
distinctly different from `-1`: **best estimate `-0.91`, 95% CI `[-0.98, -0.85]`.**

## Kill Analysis (Anti-Overfitting Gate)

**What was killed:** the specific hypothesis `Var(log(theta(G)/sqrt(n))) =~ C/n` (exponent
exactly `-1`) for this ensemble (`p=0.5` random dense circulant graphs), tested over
`n in [32, 3000]`. The 95% CI excludes `-1` with real precision, not marginally.

**What was NOT killed:**
1. The underlying phenomenon — `Var(log(theta/sqrt(n)))` DOES shrink with `n` in a clean,
   stable power-law-like fashion (`n^-0.91`, consistent across two independently-fit halves of
   the range) — this survives, more precisely measured than before (the original informal
   `n^-0.96` estimate came from 9 much-noisier points, `n_reps` tapering to 6 at `n=2560`; this
   sweep's `n=2048` point alone has 80 reps, and the fit uses 9 points spanning `n=32..3000`
   with 40-300 reps each).
2. `E[theta(G)] >= sqrt(n)` and the mean-ratio convergence to 1 — unaffected, already
   `KNOWN-BY-GENERAL-THEOREM` per the audit's own Track 2, unrelated to this variance question.
3. The possibility that the TRUE asymptotic exponent is exactly `-1` at `n` far beyond this
   experiment's reach (`n >> 3000`), reached via a slowly-varying correction
   `Var(X_n) = C*n^-1*L(n)` (e.g. a logarithmic factor) that would produce an effective exponent
   near `-0.9` across several decades of `n` without the split-half slope showing any drift —
   this is NOT distinguishable from a genuine `n^-0.91` law using only same-functional-form OLS
   on 9 points. The stability check rules out only the SIMPLEST alternative story (a correction
   already mostly decayed by `n=1024`, still visibly decaying at the same rate thereafter) — see
   the CORRECTED CALIBRATION note above.

**Relaxation Map for the surviving phenomenon** (per Minimal Relaxation Rule — one change per
variant, not attempted here):
- **Remove** the `p=0.5` restriction: does the exponent shift at other `p`? (Would require
  abandoning the `sqrt(n)` normalization too, since self-complementarity — the basis for
  `E[theta]>=sqrt(n)` — is `p=0.5`-specific; a genuinely different, more expensive redesign.)
- **Weaken** the exact-exponent question to a bracket: is `Var = O(n^-0.8)` and
  `Var = Omega(n^-1)` simultaneously defensible as a two-sided bound, without committing to one
  point estimate? Cheaper than resolving the exact value, and may be the more honest claim to
  carry forward.
- **Replace** the empirical power-law model with a more structured ansatz fit to the SAME
  already-collected 9 points (NOT a bigger sweep at larger `n` — the recommended next cheap step,
  per explicit user direction) — e.g. `Var(n) = C*log(n)/n` or `C*(log n)^p/n` against the plain
  `C*n^-alpha` fit already done here. **Hard constraint on this comparison, stated explicitly so
  it is not silently violated later:** a correction model is only admissible here if it can be
  motivated from the actual structure of the problem (the random-circulant/DFT representation
  `theta_via_lp` itself uses, or a known mechanism from concentration-of-measure theory for
  similar LP/SDP relaxations) — NOT chosen by trying several functional forms on these 9 points
  and picking whichever fits best. An unmotivated multi-model fit on 9 points is a beauty
  contest among curves, not a scientific comparison, and must not be reported as one.

## Skeptic Concerns (self-review, FL Step 8a — Standard-tier, not causal/architectural; the
substrate gate + negative control + post-hoc stability check substitute for an external
adversarial pass on a numerically well-understood, already-partially-verified pipeline)

- **"The LP solver's own numerical precision at large n could inflate or deflate the measured
  variance."** → Partially addressed: the substrate gate re-confirms `theta_via_lp`'s
  correctness at small `n` (unchanged from `H-CAT31-1`'s own established validation), but this
  experiment did NOT specifically stress-test HiGHS's numerical precision at `n=3000` against an
  independent solver. **Accepted as an open limitation** — the `n=3000` point's own reps (40,
  the fewest in the sweep) is also its weakest link precision-wise; the stability check
  (matching slopes on two independently-fit halves) partially mitigates this by showing the
  `n=256..3000` half agrees with the `n=32..1024` half, which does not depend on the `n=3000`
  point's own precision alone.
- **"9 points is still not many for a power-law fit, even with better reps than before."** →
  **Accepted limitation**, explicit in `claim.md`'s own "What This Does NOT Mean" — the
  4096-and-beyond range the user originally asked for was not reached due to a disclosed
  compute-cost constraint (LP solve time empirically scales closer to `O(n^3)`-`O(n^4)` than the
  originally-assumed `O(n^2)` in this regime, confirmed by direct benchmarking this session:
  0.17s/0.94s/6.68s/34.38s/88.68s at n=500/1000/2000/3000/4096).
- **"Weighted-OLS weights derived from bootstrap CI width via a delta-method approximation are
  themselves approximate, not exact."** → **Accepted**, but the unweighted and weighted fits
  agree closely (-0.9122 vs -0.9126, well within each other's CI), so the specific weighting
  choice is not driving the conclusion.

## Caveats / What This Does NOT Mean

Per `claim.md`'s own section, unchanged and reaffirmed, plus:

5. Does NOT establish a theoretical explanation for why the exponent is close to but not
   exactly `-1` — purely an empirical measurement. A natural next question (not attempted here)
   is whether `-0.91` itself is a recognizable constant/rational related to the ensemble's own
   structure, or simply this range's own best power-law approximation to a more complex true
   function of `n`.
6. Does NOT rule out that a genuinely wider range (the user's own originally-requested
   `n` up to `4096`, or beyond) could shift the estimate further — the stability check argues
   against a SIMPLE finite-size story, but is not a proof of asymptotic constancy.

## Novelty status (per the deep external novelty audit's own vocabulary,
`reports/2026-09-10-deep-external-novelty-audit.md`)

**`BENCHMARK-SPECIFIC-NUMERIC-RESULT` — NOT `POSSIBLE-NOVEL-SPECIAL-CASE`, downgraded from the
audit's own preliminary framing.** The audit's Track 1/Track 2 write-up treated
`Var(log(theta/sqrt(n))) ~ n^-0.96` as the single strongest surviving novelty candidate,
contingent on this exact deepening check. That check now shows the exponent is NOT close enough
to a "clean" value (`-1`, or any other obviously-theorem-shaped constant checked here) to look
like a discoverable closed-form result — it is a precisely measured empirical number
(`-0.91, CI [-0.98,-0.85]`) without an accompanying mechanism or candidate theorem. Per this
project's own hard rule (`falsification-ladder.md`, `research-methodology.md` Q6): a numeric
fact without a structural explanation is a benchmark measurement, not a special case of anything
identifiable yet — promoting it further would require the theoretical work in the Relaxation Map
above, not more compute at larger `n` alone.

**Final one-line status (user-refined, 2026-09-10):** a robust, unexplained empirical
concentration law on random circulant Lovász theta, with the natural `n^-1` law falsified over
the tested range — `BENCHMARK-SPECIFIC-NUMERIC-RESULT` / graph status `lead`. Not a discovery,
not a failure: the project's single strongest surviving novelty candidate was given a real,
pre-registered chance to die by its own named criterion, and did — which is a stronger
demonstration of this project's own methodology working correctly than a CI that happened to
land on `[-1.02, -0.98]` and got waved through would have been.

## MCID

Not formally applicable to a scaling-exponent CI — the pre-registered qualitative bar (does the
CI discriminate `-1` from `-0.5`/`-2`) was met, and answered "the exponent is not `-1`," not
"the answer is unclear."
