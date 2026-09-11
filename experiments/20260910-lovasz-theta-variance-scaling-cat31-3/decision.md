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

## Addendum (2026-09-11) — mechanism-level diagnostics, Mechanism Development Mode

**Trigger and provenance.** The user supplied three externally-generated analyses (Perplexity,
Qwen, ChatGPT) of this experiment's own `-0.91` result, explicitly asking for independent
verification, not acceptance at face value. Per `audit-verification-gate.md` ("agent's
`[VERIFIED]` = your `[INFERRED]`"), every claim below was re-derived or checked with a tool
before being used, not copied from the pasted text. This addendum is exploratory (Mechanism
Development Mode, `research-methodology.md`) — it does NOT reopen or change the REJECTED verdict
above, which stands on its own pre-registered Kill Criterion.

**Literature claims — checked against primary sources, not the pasted summaries:**
- `[VERIFIED]` arXiv:2502.16227 (Bandeira, Błasiok, Dmitriev, Faure, Kireeva, Kunisky, Feb 2025):
  read directly from LaTeX source. Theorem 1: `sqrt(n) <= E[theta(G)] <= C*sqrt(n*log(log(n)))`.
  Conjecture: `E[theta(G)] = (1+o(1))*sqrt(n)`, explicitly still open. LP reformulation via DFT
  diagonalization matches the pasted text's structure. The paper contains **no** discussion of
  `Var(theta)` or single-generator sensitivity (0 hits searching the full text for either term)
  — those claims do not come from this paper.
- `[WEAK]` "Faure's earlier work numerically observed `Var(theta)=O(1)` and single-generator
  sensitivity `~n^-1/2`, unresolved." Ulysse Faure is a confirmed co-author of the above paper
  (ETH Zürich), and a WebSearch AI-generated summary of a ResearchGate-hosted report attributed
  to him describes matching numerical findings — but the primary source itself returned HTTP 403
  on direct fetch, so this rests on a search engine's paraphrase, not a quoted primary source.
  Treated as `[WEAK]`, not `[VERIFIED]`, and not required for anything below to hold.
- `[SPECULATIVE]`, explicitly not pursued: the "critical ratio `N/d≈2`" / Wendel-type convex-hull
  framing. The Fourier-point cloud is neither independent nor centrally symmetric in the way
  Wendel's theorem requires; the pasted text's own hedge on this point is correct.

**1. Exact inequality, independently derived and checked on own data.** By the Lovász identity
`theta(G)*theta(Gbar)=n` (already used in this experiment's own substrate gate) and
self-complementarity in distribution at `p=0.5`, `X_n =d= -X_n` exactly, hence `E[X_n]=0` and
`E[e^{X_n}] = E[e^{-X_n}] = E[cosh(X_n)] = E[theta]/sqrt(n)`. Since `cosh(x) >= 1+x^2/2`:

```
V_n <= 2*(E[theta]/sqrt(n) - 1)
```

Checked (`check_cosh_bound.py`, `metrics/cosh_bound_check.json`) against all 9 points of the
main sweep: holds at 7/9 (`n=32..1536`); the two "violations" (`n=2048`, `n=3000`) have margins
(`-0.011`, `-0.0009`) fully explained by sampling noise in the *mean* estimate at those points
(the two lowest replicate counts in the sweep, 80 and 40) — the deviation of `mean_ratio` from 1
is smaller than that estimate's own standard error at both points. Not a contradiction of the
inequality; a reminder that `n=2048`/`n=3000` remain the noisiest points in this dataset (already
flagged as a limitation above).

**2. Q-proxy diagnostic — density explains a substantial, not necessarily complete, share of
`Var(X_n)`.** Tests whether most of `X_n`'s variance traces to `Q` (count of "on" generator
bits, i.e. edge density) rather than *which* generators are on. Proxy
`D_n = 0.5*log((m-Q)/Q)`, `m=(n-1)//2`; `Var(D_n) ~= 1/m ~= 2/n` by a first-order expansion
around `Q=m/2` (independently re-derived, not copied). OLS `X_n ~ D_n` on fresh samples at a
subset of the sweep's own `n` values (`check_q_proxy_diagnostic.py` +
`check_q_proxy_diagnostic_n3000.py`, seeds `332000+`, disjoint from the main sweep):

| n | reps | r² | resid. fraction of Var(X) | n·Var(X) (this run) |
|---:|---:|---:|---:|---:|
| 32 | 300 | 0.662 | 0.338 | 3.43 |
| 128 | 300 | 0.725 | 0.275 | 4.25 |
| 512 | 200 | 0.801 | 0.199 | 4.70 |
| 1536 | 100 | 0.858 | 0.142 | 5.82 |
| 3000 | 40 | 0.818 | 0.182 | 4.98 |

`r²` rises substantially from `n=32` to `n=1536` (density explains 66%→86% of variance) but the
`n=3000` point does **not** continue the trend (drops back to 0.818) — this is the sweep's
lowest-replicate point (40) and the drop is consistent with sampling noise on the `r²` estimate
itself, not treated as a real reversal. **Honest reading: density fluctuation is a real,
substantial, but not exclusive driver of `Var(X_n)`; a genuine "shape" (which generators, not how
many) component remains, of order 14-34% of the total depending on `n`.** This refutes the
stronger form of the externally-suggested hypothesis ("`X_n ≈ D_n`, most of the variance is
density") while confirming a weaker, still useful form (density matters a lot, especially at
mid-range `n`).

**3. Single-generator sensitivity / Efron–Stein bound — the most informative new result.**
Concrete, falsifiable proxy for a bounded-differences argument: flip one generator bit `i`
(toggling the mirrored edge pair it controls), measure
`Delta_i_X = log(theta(G)/sqrt(n)) - log(theta(G^(i))/sqrt(n))` at 3 spread-out indices per
sample (`n` here is not prime, so full transitivity under `Z_n^x` does not apply — averaging
over 3 indices is a partial check on homogeneity, not a full one).
`Var(X_n) <= (1/4)*sum_i E[(Delta_i X)^2]` (`check_single_generator_sensitivity.py` +
`_n3000.py`, seeds `333000+`):

| n | reps×idx | n²·E[ΔX²] | ES bound on Var(X) | measured V_n (main sweep) | bound/measured |
|---:|---:|---:|---:|---:|---:|
| 128 | 60×3=180 | 84.5 | 0.0812 | 0.0316 | 2.57 |
| 512 | 60×3=180 | 60.7 | 0.01476 | 0.00885 | 1.67 |
| 1536 | 25×3=75 | 60.7 | 0.00493 | 0.00389 | **1.27** |
| 3000 | 8×3=24 | 121.4 ± 59 (1 SE) | 0.00505 | 0.00181 | 2.79 (wide CI) |

**The striking part:** `n²·E[ΔX²]` is nearly IDENTICAL at `n=512` and `n=1536` (60.7, 60.7),
after a clear finite-size drop from `n=128` (84.5) — a clean signature of an `O(1/n²)`
single-generator influence stabilizing. The bound/measured ratio shrinks monotonically and
substantially over the same three points (2.57 → 1.67 → 1.27), i.e. the Efron–Stein upper bound
is getting *tighter* as `n` grows — exactly the pattern that would be expected if `Var(X_n)`'s
true asymptotic behavior converges toward the bound's own clean `~C/n` scaling (which would mean
exponent `-1`, not `-0.91`).

**This trend is NOT confirmed at `n=3000`, and must not be reported as if it were.** The `n=3000`
point used only 8 replicates × 3 indices = 24 samples (by design, to keep the extension cheap —
`theta_via_lp` costs ~43s/call at this `n`, 4 calls/rep). Its standard error on `n²·E[ΔX²]`
(±59, ~49% relative) is wide enough that the point estimate (121.4) is well within 1 SE of the
`n=512`/`n=1536` value (60.7) — **statistically indistinguishable from continuing the
stabilization**, not evidence against it, but also not evidence for it. The apparent "reversal"
in the point estimate has no more evidential weight here than noise.

**Synthesis — what this does and does NOT establish.** The sensitivity/Efron–Stein diagnostic
produced a genuinely new, structurally-motivated, cheap signal (not a bigger sweep on the
original statistic — a different, targeted measurement) that is *suggestive* of the `-0.91`
being a finite-size transient toward a true `-1` asymptotic, via a mechanism that is now concrete
enough to name: if `sum_i E[(Delta_i X)^2]` genuinely stabilizes at `~C/n` (not `~C/n^0.91`) as
`n` grows, Efron–Stein forces `Var(X_n) = O(1/n)` in the limit, which is a different and stronger
statement than the WLS point estimate on the aggregate 9-point sweep. But this is **not proven**:
(a) only 3 well-powered points (`n=128,512,1536`) show the tightening trend; (b) the `n=3000`
extension is too noisy to confirm or refute continuation; (c) the Efron-Stein bound is an upper
bound, and tightening toward the true value is suggestive, not dispositive, of the true value's
own asymptotic rate. **Status: the `-0.91` vs `-1` question remains genuinely open** — this
addendum sharpens *where* the next decisive check should look (a well-powered, not merely
8-replicate, single-generator sensitivity measurement at `n=3000` and beyond, or a formal proof
of `E[(Delta_i theta)^2] = O(1/n)`), rather than answering it. This is consistent with, and
extends without contradicting, the CORRECTED CALIBRATION note above (`Var(X_n)=C*n^-1*L(n)`
remains the leading un-excluded alternative to a genuine `n^-0.91` law; this addendum names a
concrete candidate mechanism for why such an `L(n)` could exist and shrink toward 1).

**4. Prime-n generator homogeneity — an exact identity, independently proved here (not merely
cited from the pasted external analysis).** The externally-suggested claim was that prime `n`
"should" give homogeneous single-generator sensitivity across indices `i`, via a `Z_n^x`
symmetry heuristic. Re-derived rigorously rather than accepted as a heuristic:

For prime `n`, multiplication by any unit `a in Z_n^x` (i.e. any `a` coprime to `n`, which for
prime `n` is every `a` in `1..n-1`) is a graph automorphism of the underlying labeling — the
random circulant graph on generator set `S subset {1..m}` and the graph on `a*S mod n` (reduced
to `{1..m}` via the `+/-` identification) are ALWAYS isomorphic for any FIXED `S`, so
`theta(G_S) = theta(G_{aS})` deterministically. Since `S` is drawn from i.i.d. Bernoulli(1/2)
bits, and `S -> aS` is a measure-preserving bijection of the sample space (a is invertible mod
`n`), it follows that `E_S[(theta(G_S)-theta(G_{S xor {i}}))^2] = E_S[(theta(G_S)-theta(G_{S xor
{j}}))^2]` EXACTLY whenever `j = a*i mod n` for some unit `a` — i.e. whenever `i` and `j` are in
the same `Z_n^x`-orbit. For prime `n`, `Z_n^x` acts transitively on `{1,...,n-1}`, hence (via
`+/-` identification, since `-1` is always a unit) transitively on `{1,...,m}`. **Conclusion:
for prime `n`, `E[(Delta_i theta)^2]` is EXACTLY equal for every generator index `i` — an exact
symmetry theorem, not an approximation or a heuristic.**

The load-bearing deterministic half of this argument (`theta(G_S)=theta(G_{aS})` for every FIXED
`S`) was checked EXHAUSTIVELY, not by sampling, at `n=7` (prime, `m=3`, `a=3`):
`verify_prime_isomorphism_exhaustive.py` enumerates all `2^3=8` subsets `S` and confirms
`|theta(G_S)-theta(G_{aS})|` is `~5e-15` (floating-point noise) in every case — a real,
tool-verified positive control on the theorem's deterministic core, not merely a symbolic
argument taken on faith.

Checked empirically (`check_prime_symmetry_homogeneity.py`, `n=127` prime vs `n=128` composite,
150 reps × 7 spread indices each, seeds `334000+`): the observed across-index CV came out
**higher** for the prime case (`0.231`) than the composite case (`0.132`) — the OPPOSITE
direction from a naive reading of "symmetry implies less variability." This is **not a
refutation of the theorem above** (which is proven, not conjectured) — per-index standard
errors at this replicate count (~15-25% relative, `n=127`, 150 reps) are large enough that a
*true* CV of exactly 0 (as the theorem requires for prime `n`) is fully consistent with an
*observed* CV of 0.23 from sampling noise alone. **This diagnostic, as run, lacks the power to
detect the proven identity — it neither confirms nor refutes it; it establishes that 150 reps at
this `n` is not enough, not that the symmetry is absent.**

**Practical implication for future work (not executed here):** since the identity is exact for
prime `n`, any future well-powered sensitivity measurement should (a) use prime `n` to get the
Efron–Stein sum from a SINGLE generator index instead of averaging over several (removes the
composite-n heterogeneity confound entirely, and roughly halves the per-replicate cost versus
the 3-index design used above), and (b) put replicate budget into that one index's precision
rather than splitting it across multiple indices to "check" homogeneity that is already proven.

**5. Density-response experiment — independent cross-check via directly varying `p`, not a
within-sample regression.** Exact symmetry re-derived (extends the `p=0.5` self-complementary
argument already used for the cosh bound above): since `theta(G)*theta(Gbar)=n` holds pathwise
(Lovász 1979) and `Gbar` for `G~G(n,p)` has exactly the distribution `G(n,1-p)`,

```
X_n(1-p) =d= -X_n(p)   =>   M_n(1-p) = -M_n(p),   M_n(p) := E[X_n(p)]
```

i.e. `M_n` is EXACTLY odd around `p=0.5` — a checkable prediction independent of any model fit,
not merely assumed. Measured `M_n(p)` at `p in {0.45,0.475,0.5,0.525,0.55}`
(`check_density_response.py`, `n=128` reps=300, `n=512` reps=200, seeds `335000+`):

| n | λ̂ (h=0.025) | λ̂ (h=0.05) | symmetry check (4 pairs) |
|---:|---:|---:|---|
| 128 | -2.175 ± 0.300 | -2.433 ± 0.153 | diffs 0.019, 0.029 — both < 2 SE of 0 |
| 512 | -3.311 ± 0.202 | -2.892 ± 0.101 | diffs 0.016, 0.007 — both < 1.6 SE of 0 |

`λ̂ = (M_n(0.5+h)-M_n(0.5-h))/(2h)` — a direct, symmetric finite-difference measurement of
`M_n'(0.5)`, structurally independent of the Q-proxy regression in point 2 above (that was a
within-sample regression at fixed `p=0.5`; this is a response to an actually-changed parameter).

**Sign note (own calibration correction, caught before it became an error, not after):** the
Q-proxy diagnostic's slope `b` (`X_n ~ D_n` regression) is positive, and it would be a mistake
to read that directly as "sensitivity to `p` is positive" — `D_n = 0.5*log((m-Q)/Q)` DECREASES
as density increases, with `dD_n/dp ~= -2` near `p=0.5` (from `D_n(p) ~= 0.5*log((1-p)/p)`,
Taylor-expanded). Converting through the chain rule, `dM_n/dp ~= b * dD_n/dp ~= -2b` — negative,
matching the sign observed here directly. **Magnitude cross-check:** at `n=512`,
`-2*b = -2*1.4505 = -2.901`, versus this experiment's own `λ̂(h=0.05) = -2.892` — agreement to
within 0.3%. At `n=128`, `-2*b = -2*1.2357 = -2.471` versus `λ̂(h=0.05) = -2.433` — agreement to
within 1.5%. **Two structurally independent measurements (a within-sample proxy regression at
fixed `p`, and a direct response to varying `p`) agree closely once the sign/scale conversion is
done correctly — real, non-circular consistency evidence for the underlying density-driven
mechanism, not an artifact of either method alone.**

**6. Attempted formal proof of `E[(Delta_i theta)^2]=O(1/n)` — real partial progress, gap
explicitly NOT closed.** Per direct user request to continue the Efron–Stein target toward a
formal proof. Honest verdict up front, so it cannot be missed: **a full proof was NOT achieved
this session.** What follows is the actual mechanism identified, tool-verified where possible,
with the precise remaining gap named — not a disguised negative result, but real progress on
what to prove next.

**The mechanism (standard LP theory, independently derived, then numerically verified — not
copied from any external source).** Fix the generator set `S` and index `i in S`. Define
`S_rest = S \ {i}` and the one-parameter family of LPs

```
V(t) = max{ <y,g> : y feasible for S_rest, <y,f_i> = t }
```

so `theta(G_S) = V(0)` and `theta(G_{S_rest}) = max_t V(t)` (dropping generator `i` is exactly
relaxing the RHS of its constraint from a fixed `0` to "free," then taking the best achievable
value). By LP duality, `V(t)` equals the pointwise infimum, over the (compact) dual-feasible
set, of an affine function of `t` — hence **`V(t)` is concave and piecewise-linear in `t`**, a
completely standard parametric-LP fact, not specific to this problem. This gives, via the
concave function's tangent-line property at `t=0`, a genuine (if qualitative) sensitivity bound
connecting `Delta_i theta = V(t*) - V(0)` to the LP's dual variable (shadow price) for
constraint `i` and the distance `t*` that the relaxed optimum wants to move.

**Verified, not just asserted:** `verify_lp_sensitivity_concavity.py` (n=11 toy case, 3
generators, drop one, sweep `t` over `[-1,1]`) confirms all three predicted structural facts:
(a) piecewise-linearity — second differences are `~1e-15` (floating-point noise) within each
linear segment; (b) a genuine concave kink — the swept `V(t)` rises then falls, `min` second
difference `-0.28` marks the kink; (c) `max_t V(t)` from the grid sweep (`4.5541`) matches
`theta(G_{S_rest})` computed completely independently via `theta_via_lp` on the reduced
generator set directly (`4.5677`, `0.30%` grid-resolution gap, not a discrepancy in the
mechanism). The mechanism is real.

**Why this does NOT close the gap to `O(1/n)`.** The tangent-line bound, on its own, only
converts the question "how much does `theta` change" into two DIFFERENT unknowns — the dual
variable (shadow price) magnitude at `i`, and how far `t*` sits from `0` — and bounding EITHER
of those TIGHTLY for the specific RANDOM ensemble here is exactly as hard as the original
question. A crude bound using only `||y||_1=1` and `|f_i(k)|<=1` (Hölder/Cauchy–Schwarz) gives
`|t*|<=1` and a shadow-price magnitude that, summed "conservatively" across the `~n/2`
generators, is consistent with an aggregate change of order `n` (matching, e.g., the full range
`theta(empty)-theta(complete) = n-1`) — spread evenly across `~n/2` generators that is `O(1)`
PER GENERATOR, not the `O(1/n)` needed. **Getting from `O(1)` per generator down to `O(1/n)`
requires a genuine concentration/cancellation argument on the dual solution specific to the
random ensemble** — structurally the same kind of restricted-isometry-property (RIP) argument
arXiv:2502.16227 uses for its OWN (still only qualitative, `E[theta]=(1+o(1))*sqrt(n)`,
unresolved) conjecture about the mean. That argument is not established in the one primary
source directly verified this session, and deriving it from scratch here would be new research,
not a routine continuation.

**What is honestly claimed:** (1) a real, verified mechanism connecting single-generator
sensitivity to LP dual variables via a standard, correctly-applied parametric-LP concavity
argument; (2) a precisely-named missing ingredient (concentration of the dual/shadow-price
structure across generators) required to turn this into `O(1/n)`; (3) an explicit statement
that closing this gap is NOT achieved here and is adjacent to genuinely open research (the
paper's own mean conjecture is unresolved, and it does not address variance at all — whether
the variance question is actually HARDER than the mean question, merely similarly-flavored, or
possibly easier is not established either way here; that comparison is not claimed). This is
not a disguised failure — it converts a vague ask ("prove
Efron-Stein O(1/n)") into a precise, well-defined open sub-problem (characterize the dual
variable's typical magnitude and the relaxed-optimum's typical correlation `t*` with a dropped
constraint, for the random circulant ensemble), which is real, if incomplete, mathematical
progress.

**7. A real, EXACT lower bound — independently re-derived and verified, applied only to
already-collected data.** The user's next message included an unverified external analysis
claiming (a) a new, larger `n=3000` sensitivity experiment with specific numbers, and (b) a
useful exact identity/bound. These are handled very differently below — see the explicit
provenance note before the artifacts list.

**The identity (independently re-derived and checked step by step, not accepted on the
external text's say-so):** for `X_n=f(z_1,...,z_m)`, `z_i` i.i.d. Bernoulli(p), `Q=sum z_i`,
the log-likelihood is `Q*log(p)+(m-Q)*log(1-p)`, so `d/dp log P_p(z) = (Q-mp)/(p(1-p))`, and
since `d/dp E_p[X_n] = E_p[X_n * d/dp log P_p(z)]`:

```
M_n'(p) = Cov_p(X_n,Q) / (p(1-p))   =>   M_n'(1/2) = 4*Cov(X_n,Q)
```

a standard exponential-family score-function identity, elementary once stated, verified here
by direct algebra (not merely cited). Combined with Cauchy–Schwarz
(`Cov(X_n,Q)^2 <= Var(X_n)*Var(Q)`) and `Var(Q)=m/4` at `p=1/2`:

```
Var(X_n) >= M_n'(1/2)^2 / (4m)  ~=  M_n'(1/2)^2 / (2n)
```

**This is EXACT — no LP structure, no concavity heuristic, no concentration assumption
required — unlike the LP-sensitivity attempt in point 6, which only produced a qualitative
mechanism.** Applied directly to this experiment's OWN already-verified
`check_density_response.py` measurements (`verify_cauchy_schwarz_lower_bound.py`):

| n | h | λ̂ (finite diff.) | plug-in estimate | measured `V_n` | estimate/measured |
|---:|---:|---:|---:|---:|---:|
| 128 | 0.025 | -2.175 | 0.01877 | 0.03159 | 0.594 |
| 128 | 0.050 | -2.433 | 0.02349 | 0.03159 | 0.744 |
| 512 | 0.025 | -3.311 | 0.01075 | 0.00885 | 1.214 |
| 512 | 0.050 | -2.892 | 0.00820 | 0.00885 | **0.926** |

**Calibration correction (caught by re-reading this section against the exact inequality, the
same discipline this session used on an earlier overclaim in §0):** the table's "plug-in
estimate" column is `λ̂²/(4m)` using the FINITE-DIFFERENCE `λ̂`, not the true derivative
`M_n'(1/2)` — the exact inequality `Var(X_n) >= M_n'(1/2)²/(4m)` is a statement about the
POPULATION derivative. Calling the plugged-in numbers themselves "the rigorous lower bound"
(an earlier draft of this section did) overstates what a finite difference establishes: `λ̂`
carries its own sampling noise AND a curvature/`O(h²)` bias from the (unverified) cubic term
in `M_n(p)`'s odd expansion, neither of which is bounded here. **The exact inequality itself
is fully rigorous; the numbers in this table are a diagnostic plug-in evaluation of it, not a
proven bound on `V_n` at these specific `n`.** The 59-93% figures should be read as "how much
of the measured variance this diagnostic ties to the density channel," not as a certified
numeric lower bound.

**What this rigorously establishes, stated without dropping the condition anywhere:**

```
Var(X_n) >= M_n'(1/2)^2/(4m)          <- PROVED, population-level, unconditional
Var(X_n) = Omega(1/n)                  <- FOLLOWS ONLY IF liminf_n |M_n'(1/2)| > 0
```

The second line is a **conditional consequence**, not itself an established theorem — the
`liminf |M_n'(1/2)|>0` nondegeneracy condition is NOT proven here. It is *consistent with* the
two tested points (`λ̂~-2.2` at `n=128`, `λ̂~-2.9` at `n=512`, neither shrinking toward 0), but
2 points is empirical support, not a proof ruling out `M_n'(1/2)->0` for larger `n`. **Every
later restatement of this result in this document (including any that say "established" or
"real, rigorous Omega(1/n)" without repeating this condition) should be read as shorthand for
the conditional statement above, not as claiming the condition itself was proven.** Combined
with point 6's unresolved upper bound, the honest current state is: one new, unconditionally
EXACT population inequality (real progress), a plausible but unproven path from it to
`Omega(1/n)`, and a named-but-unclosed path to the matching `O(1/n)` upper bound — not
`Theta(1/n)`, and not yet an unconditional `Omega(1/n)` either.

**Explicit provenance note — what was and was NOT used from the external analysis.** The
pasted text also claimed a new `n=3000` experiment (191/240 planned replicates, checkpoint
`n^2*E[(Delta_I X)^2]=65.96+-11.91` at `N=102`, an antipodal-generator check giving `61.43`,
"five independent complement checks at `~1e-14` relative error", etc.), presented with high
specificity and confidence. **These specific numbers are NOT incorporated anywhere in this
document and are not treated as evidence.** Reasoning, stated plainly per
`audit-verification-gate.md` ("agent's `[VERIFIED]` = your `[INFERRED]`") and
`skeptic-triggers.md` (suspiciously specific, confident numbers from an unverifiable source
require a check, not acceptance): (a) there is no way to verify these numbers were actually
computed — no output log, no reproducible seed-to-value chain checkable in this session;
(b) a rough compute-time estimate is a red flag, not reassurance: 191 replicates at `n=3000`
using `theta_via_lp` (measured at ~43s/call earlier this session) with 2 calls/replicate
(baseline + one flip) is ~4.6 hours of compute — implausible for the "available compute window"
framing without any supporting log; (c) this project's own repo is public, so an external tool
COULD in principle have fetched the code, but plausibility of access is not evidence of an
actual run. **Per this project's standing discipline (the exact same discipline that caught
this session's own earlier overclaim on 2026-09-10), unverifiable numbers from an external
source are not promoted to findings, however precisely they are stated.**

**What WAS checked and used from that text — real, verifiable claims about THIS project's own
code, checked directly against the actual files, not accepted on say-so:**
- **Real, confirmed gap:** for even `n`, `sample_circulant_neighbors` (H-CAT31-1's own function)
  samples an extra "antipodal" generator bit at index `n/2`, separate from the `m=(n-1)/2`
  paired bits. Every sensitivity script in this addendum (`check_single_generator_sensitivity
  {,_n3000}.py`) uses `half=(n-1)//2` and never tests the antipodal index — the reported
  Efron–Stein sums are missing that one term. Its weight in the full sum is `1` out of `~n/2`
  generators (e.g. `1/1500` at `n=3000`), so its likely quantitative impact on the reported
  bounds is small, but the omission is real and now documented rather than silently present.
- **Real, confirmed bug (never triggered in this session's actual runs):** `flip_generator(c,i)`
  toggles `c[i]` then `c[n-i]`; for the antipodal case `i=n/2`, `n-i=i`, so the same element is
  toggled twice — a silent no-op. Checked directly: this session's `n=3000` sensitivity test
  indices were `{1,499,999}` (from `spread_indices`/`max(1,half//3)` logic) — the antipodal
  index `1500` was never among them, so this bug did not corrupt any reported number here, but
  the function itself is broken for that one case and should not be trusted if reused for it.
- **Real, verifiable observation:** `gcd(999,3000)=3` while `gcd(1,3000)=gcd(499,3000)=1` —
  confirmed via `verify_cauchy_schwarz_lower_bound.py`'s own gcd check. The 3-index sample used
  for `n=3000` sensitivity is small and not demonstrated to be representative; this is a real,
  already-implicit limitation (the addendum's point 3 already noted composite-`n` heterogeneity
  is unresolved, not proven small) rather than a new invalidating flaw.
- **Real, valid critique, not yet acted on:** pooling all `(replicate, index)` pairs together
  when computing `se_dx2` in `check_single_generator_sensitivity{,_n3000}.py` treats correlated
  observations (3 indices sharing one baseline graph per replicate) as if independent, which
  understates the true standard error to an unquantified degree. This does not change any
  point estimate, only the previously-reported uncertainty bands on `n^2*E[(Delta_i X)^2]` in
  point 3 above, which should be read as a lower bound on the true uncertainty, not an exact SE.

**8. Third and final attempt at the upper bound, per direct user request to "try harder" — a
genuinely new structural fact found and verified, still insufficient to close the gap.**
Went back to the primary source (arXiv:2502.16227, `Proof of main theorem` section, read
directly from LaTeX, not from memory) to find whatever structural facts its OWN proof uses,
looking for something not yet exploited in points 6-7.

**New fact, derived then verified numerically (not assumed):** flipping ONE generator bit `i`
changes the LP objective vector `g=Fb` by EXACTLY

```
Delta_g_k = +/- 4*cos(2*pi*k*i/n)   for every k   =>   |Delta_g_k| <= 4 EXACTLY, for all n
```

— a bound that does NOT grow with `n`, unlike `g` itself (whose entries are `~sqrt(n log n)`
typically per the paper's own `Lemma lem:nlogn_ub`). Verified directly (`verify_delta_g_bound.py`,
`n=3000`): two independently-computed `g` vectors differing in one generator match the
predicted `4*cos(...)` formula to `~1e-12`, and `max|Delta_g_k|=4.000000` exactly.

**Why this still doesn't close the gap.** Write `y1*` = optimal for `S`, `y2*` = optimal for
`S\{i}`. The natural decomposition
`theta(G_{S\{i}}) - theta(G_S) = <y2*-y1*, g_S> + <y2*, Delta_g>` splits into a term bounded by
the NEW fact (`|<y2*,Delta_g>| <= ||y2*||_1 * ||Delta_g||_inf <= 1*4 = 4`, a genuine `O(1)`
constant, better than anything found in points 6-7) and a term `<y2*-y1*,g_S>` that this
approach does NOT control. Using the paper's own RIP lemma (`||y||_2 <= (log^2 n/sqrt(n))*
||y||_1` for `y` in the relevant kernel), `||y2*-y1*||_2 <= 2*log^2(n)/sqrt(n)` is small, but
combined with `||g_S||_2=n` (exact, deterministic — `||b||_2^2=n` since `b in {+-1}^n`) via
Cauchy-Schwarz this only gives `O(sqrt(n)*log^2 n)` for that term — the SAME order as `theta`
itself, not smaller. The alternative Hölder route
(`||y2*-y1*||_1 <= 2`, `||g_S||_infty ~ sqrt(n log n)`) gives the same `O(sqrt(n log n))` order.
**The obstruction is structural, not a missing inequality to look up:** LP optima sit at
polytope VERTICES, and vertex identity can change discontinuously under an arbitrarily small
constraint perturbation — the paper's RIP machinery controls how SPREAD OUT any one feasible
`y` is (`||y||_2` vs `||y||_1`), but says nothing about how FAR APART two different optimal
vertices are from each other under a one-constraint change. Bounding `||y2*-y1*||` tightly
would need a genuinely different tool (LP vertex-stability / basis-perturbation theory
specific to this random polytope's geometry), which is not in the primary source and was not
derivable here.

**Final, honest verdict on the O(1/n) upper bound, after two independent attempts specifically
targeting it (LP concavity/duality in point 6, and this `Delta_g`-boundedness attempt) — point
7 was a SEPARATE, successful result on the LOWER-bound side, not a failed upper-bound variant,
correcting an earlier miscategorization in this sentence: NOT achieved.** Both upper-bound
attempts found something real (the concavity mechanism, the exact `Delta_g` bound) and both
hit the SAME underlying wall — controlling how far the LP OPTIMIZER itself moves under a
one-constraint perturbation, not just how large the perturbation is. This is assessed, after
genuine effort across two angles, as very likely requiring new research-level insight, not a
routine continuation of either this project's own tools or the primary source's published
techniques. Per this project's Cheapest Differentiating Test protocol, a further attempt
without a qualitatively new idea would have low expected information value — stopping here
rather than repeating variations of the same mechanism.

**Where this leaves H-CAT31-3's mechanism investigation, stated without dropping conditions:**
`Var(X_n) >= M_n'(1/2)^2/(4m)` is an unconditionally PROVED population inequality (point 7).
`Var(X_n) = Omega(1/n)` is a CONDITIONAL consequence of it, pending the unproven nondegeneracy
condition `liminf|M_n'(1/2)|>0` (empirically consistent with, not established by, 2 tested
points) — any shorter restatement of this result elsewhere in this document is shorthand for
that conditional statement. `Var(X_n) = O(1/n)` remains open. Whether closing the upper bound
is genuinely AS HARD as the primary source's own unresolved mean conjecture, or merely
similarly-flavored, is itself not established here — that comparison is a plausible but
unverified analogy, not a proven equivalence, and should not be read as one. The REJECTED
verdict on exponent `=-1` stands unchanged throughout — this entire investigation (points 1-8)
is exploratory Mechanism Development Mode work on WHY the `-0.91` exponent might or might not
be a finite-size transient, not a re-litigation of the pre-registered falsification result.

**9. Fourth check, per direct user request to keep trying: one reformulation ruled out, and a
genuine (non-proof) empirical synthesis of already-collected data that had not been stated
explicitly before.**

**(a) Checked whether the paper's OTHER primal/dual LP pair offers an escape — it does not,
and this is a ruled-out check, not a new open attempt.** arXiv:2502.16227's own Table 1 lists 4
equivalent LPs for `theta(G)` (`time`/`frequency` domain × primal/dual). Points 6 and 8 both
used the `frequency`-domain primal (`y`, objective `<y,g>`). The `time`-domain primal
(`max sum(x_i)` s.t. `Fx>=0`, `x_0=1`, `x_k=0` for edges) looked promising because dropping a
generator there means FREEING a variable (`x_i` no longer fixed at `0`) rather than removing an
orthogonality constraint — a more classical-looking LP sensitivity question. Reasoned through
(not computed, since the reasoning alone is sufficient to rule it out): freeing `x_i` is still
governed by a value function `V(t)=max{sum(x): x feasible, x_i=t}` that is concave and
piecewise-linear in `t` for exactly the same reason as before (LP duality, point 6) — same kind
of vertex-jump obstruction, just relabeled. The 4 LPs are connected by an invertible linear map
(the Fourier transform, `y:=Fx`) and by strong LP duality, both of which preserve the OPTIMAL
VALUE exactly but do nothing to trivialize how far an optimal VERTEX moves under a one-
constraint change. **No escape found via this reformulation — ruled out, not left open.**

**(b) Reframing this investigation's OWN already-collected data (`single_generator_
sensitivity.json`, no new computation) as evidence — explicitly distinguished from a proof.**
`n*(Efron-Stein bound)`, computed directly from point 3's own numbers
(`analyze_own_data_for_upper_bound_signal.py`):

| n | ES bound | n·(ES bound) |
|---:|---:|---:|
| 128 | 0.08125 | 10.40 |
| 512 | 0.01476 | 7.55 |
| 1536 | 0.00493 | 7.58 |

**This is exactly the signature the O(1/n) upper bound would produce: `n*(ES bound)` drops
from a finite-size value at `n=128` and then stabilizes (`7.55 -> 7.58`) at `n=512,1536`,**
consistent with `Sum_i E[(Delta_i X)^2] = Theta(1/n)`. This was already implicit in point 3's
table but had not been stated in these terms — it is real, honest EMPIRICAL support for the
target upper bound, gathered across 3 points, not a fourth data point beyond what exists. **It
remains exactly what it is: numerical evidence, not a proof.** The `n=3000` extension of the
same measurement (point 3) was too underpowered (8 replicates) to extend this table reliably,
and re-running it with proper power was not attempted here (would cost real compute, and per
the Cheapest Differentiating Test this is a confirmatory re-measurement, not a new
differentiating check).

**Updated final assessment after 4 honest attempts (3 proof attempts in points 6/8 plus this
reformulation check, all ruled out or unsuccessful for a PROOF; one genuine empirical-evidence
synthesis in 9b):** the O(1/n) upper bound is not proven, is assessed as requiring
research-level insight beyond the tools available here, AND is now supported by real (if
modest) numerical evidence from data already on disk. The honest, complete current status:
`Var(X_n) >= M_n'(1/2)^2/(4m)` (proved, unconditional), `Var(X_n)=Omega(1/n)` (conditional on
an unproven but empirically-consistent nondegeneracy condition), `Var(X_n)=O(1/n)` (not proven,
but the specific quantity that would need to be `O(1/n)` — the Efron-Stein sum — shows exactly
the right empirical signature across the 3 well-powered points measured).

**10. A genuinely different angle (5th attempt), per direct user request to try again: EXACT
(exhaustive, not Monte Carlo) enumeration at small `n`, removing all sampling noise.** All
prior evidence (points 1-9) was either Monte Carlo at large `n` (sampling noise) or abstract
worst-case LP bounds (too loose). Neither is ground truth. This computes the TRUE population
`Var(X_n)` and Efron-Stein sum EXACTLY, for small odd `n`, by enumerating ALL `2^m` generator
subsets (`m=(n-1)/2`) rather than sampling — since every subset is equally likely at `p=0.5`,
this is the entire population, not an estimate of it (`check_exact_enumeration_small_n.py`,
`n=9..25`, `theta_via_lp` reused unchanged, one extra LP solve per subset — no separate
sensitivity-measurement compute needed since `Delta_i(theta)` for any subset is just a table
lookup once all `2^m` values are known):

| n | m | subsets | exact `n·Var(X)` | exact `n·(ES bound)` | ES bound / Var(X) |
|---:|---:|---:|---:|---:|---:|
| 9 | 4 | 16 | 1.830 | 2.273 | 1.242 |
| 11 | 5 | 32 | 2.154 | 2.588 | 1.202 |
| 13 | 6 | 64 | 2.249 | 2.740 | 1.218 |
| 15 | 7 | 128 | 2.347 | 3.570 | 1.521 |
| 17 | 8 | 256 | 2.494 | 3.349 | 1.342 |
| 19 | 9 | 512 | 2.608 | 3.561 | 1.365 |
| 21 | 10 | 1024 | 3.007 | 4.639 | 1.543 |
| 23 | 11 | 2048 | 2.805 | 4.031 | 1.437 |
| 25 | 12 | 4096 | 2.788 | 4.372 | 1.568 |

**`n·Var(X_n)` rises from `n=9` to `n=21` and then visibly stabilizes (`3.01 -> 2.80 -> 2.79`
at `n=21,23,25`) — a real, ZERO-noise signal of `Var(X_n)` converging toward a `C/n` law, not
an artifact of Monte Carlo sampling error (there is none here).** `n·(ES bound)` shows the same
qualitative pattern (rises then wobbles in a bounded range, `4.0-4.6`, rather than growing),
and the ratio between the two stays bounded (`1.20-1.57`) across the whole range, consistent
with BOTH quantities being `Theta(1/n)` together. **This is the cleanest evidence gathered in
this entire investigation** — not because `n<=25` is asymptotic (it is not; this remains
small-`n` data, and stabilization by `n=25` does not prove it persists at `n=3000`), but
because it is EXACT: no sampling noise to explain away, no finite-reps caveat, no confidence
interval — a real fact about these 9 specific finite populations.

**Substrate-level finding, documented rather than silently worked around:** exhaustive
enumeration exposed a genuine numerical fragility in `theta_via_lp`'s default `'highs'`
(simplex) method — 1 out of 8,176 total subsets across `n=9..25` (`n=21`, generators
`{6,7,9}`) returned an ambiguous/unrecognized HiGHS status and `NaN`, while the interior-point
method (`method='highs-ipm'`) solved the SAME LP cleanly (`theta=6.3297`). Per the Substrate
Gate (`falsification-ladder.md` Step 2a): this is an infrastructure numerics issue, not
evidence about the claim — `check_exact_enumeration_small_n.py` adds a `theta_via_lp_robust`
wrapper that falls back to `highs-ipm` on `NaN` and hard-fails (rather than silently dropping
the subset) if the fallback ALSO fails, so the exact population figures above are computed
over the true full `2^m`-subset population, not `2^m - 1`. (Not fixed in H-CAT31-1's own
`theta_via_lp` — out of scope for this experiment folder, but worth a future note there.)

**Updated status after 5 honest attempts:** proof of `Var(X_n)=O(1/n)` still not achieved (4
attempts at a proof/reformulation, all ruled out or unsuccessful; this 5th attempt is exact
small-`n` evidence, not a proof either). But the evidence base is now qualitatively stronger:
noisy large-`n` Monte Carlo (points 3, 9b) AND noise-free small-`n` exact enumeration (this
point) both show the same `Theta(1/n)`-consistent signature. `Var(X_n) >= M_n'(1/2)^2/(4m)`
remains the one unconditionally PROVED result from this whole investigation.

**11. Sixth angle, per direct user request to try yet again: EXACT Walsh-Hadamard
decomposition of the small-`n` data from point 10 — a genuine new PROVED theorem, still not
closing the upper-bound gap.**

Rather than another abstract argument or estimate, this computes the FULL exact Fourier-Walsh
spectrum of `X_n` (all `2^m` coefficients `X_hat(S)`, `S subset {1,...,m}`) at each `n=9..25`
via a fast Walsh-Hadamard transform on the already-exact population from point 10
(`check_exact_walsh_decomposition.py`). Self-check: Parseval's identity
(`sum_S X_hat(S)^2 = E[X^2]`) holds to `~1e-15` at every `n` — the transform is verified
correct, not merely trusted.

**A genuine new theorem fell out, independently derived (not the goal of running this check,
but a real consequence of it):** at EVERY `n` tested, `sum_{|S|=k} X_hat(S)^2 ~ 0` (machine
precision, `~1e-31`) for every EVEN `k`. This is not a numerical coincidence — it follows
directly from the exact antisymmetry already proved in point 5
(`X_n(1-p) =d= -X_n(p)`, equivalently `X(-epsilon)=-X(epsilon)` under the GLOBAL sign flip of
all `m` generator bits). Proof: `X_hat(S) = E[X(epsilon)chi_S(epsilon)]`, and relabeling
`epsilon -> -epsilon` (same distribution, since each `epsilon_i` is symmetric `+-1`) combined
with `X(-epsilon)=-X(epsilon)` and `chi_S(-epsilon)=(-1)^{|S|}chi_S(epsilon)` gives
`X_hat(S) = -(-1)^{|S|} X_hat(S)`, forcing `X_hat(S)=0` whenever `|S|` is EVEN (no constraint
when `|S|` is odd). **`Var(X_n)` is carried ENTIRELY by odd-degree Fourier levels** — an
exact, general, `n`-independent structural fact about this specific ensemble.

**What this changes for the upper-bound program:** the "unknown" part of `Var(X_n)` beyond
level 1 (already lower-bounded via Cauchy-Schwarz in point 7) is now provably confined to
`k=3,5,7,...` only — HALF the levels are eliminated for free. The exact data shows level 3
dominates the remainder at every tested `n` (e.g. `n=25`: level 3 weight `0.0171` vs level 5
`0.0058`, level 7 `0.00093`, level 9 `0.0000627` — rapid decay), and `n*(level-3 weight)`
stays in a bounded range (`0.19-0.55`) across `n=9..25`, the same qualitative signature as
levels 1 and total `Var(X)`.

**Why the level-1 Cauchy-Schwarz trick does NOT generalize to an upper bound, stated
precisely so this avenue is not silently re-attempted later:** the same technique applies to
level 3 via a natural test statistic (the elementary symmetric polynomial
`e_3(epsilon)=sum_{i<j<k} epsilon_i epsilon_j epsilon_k`), giving
`W^3[X] >= Cov(X,e_3)^2 / C(m,3)` — ANOTHER exact LOWER bound (strengthening `Omega(1/n)`
further, if `Cov(X,e_3)` can be shown bounded away from 0, not attempted here), but
Cauchy-Schwarz structurally can only lower-bound a sum-of-squares from a single linear
functional's correlation — it has no upper-bound analogue. This clarifies, precisely, why
this entire family of test-statistic tricks (used successfully for point 7's lower bound) is
the wrong tool for the upper bound regardless of which level it is applied to, closing off a
plausible-looking "just do the same trick at every level" idea before it wastes a future
session's time.

**Updated status after 6 honest attempts:** `Var(X_n)=O(1/n)` still not proven. But this
session's investigation has now produced: one unconditionally PROVED lower bound (point 7),
one unconditionally PROVED structural theorem about the Fourier spectrum (this point, vanishing
even levels), noisy large-`n` Monte Carlo evidence (points 3, 9b), and noise-free small-`n`
exact evidence (points 10-11) — all pointing the same direction, none of them a proof of the
upper bound itself.

**Artifacts:** `check_cosh_bound.py`, `check_q_proxy_diagnostic.py` (+`_n3000.py`),
`check_single_generator_sensitivity.py` (+`_n3000.py`), `verify_cauchy_schwarz_lower_bound.py`,
`check_prime_symmetry_homogeneity.py`, `verify_prime_isomorphism_exhaustive.py`,
`check_density_response.py`, `verify_lp_sensitivity_concavity.py`, `verify_delta_g_bound.py`,
`analyze_own_data_for_upper_bound_signal.py`, `check_exact_enumeration_small_n.py`
(+`exact_enumeration_output.log`), `check_exact_walsh_decomposition.py`
(+`exact_walsh_output.log`)
(+`verify_delta_g_output.log`)
(+`verify_lp_sensitivity_output.log`), and their outputs in `metrics/` (`cosh_bound_check.json`,
`q_proxy_diagnostic.json`, `q_proxy_diagnostic_n3000.json`, `single_generator_sensitivity.json`,
`single_generator_sensitivity_n3000.json`, `prime_symmetry_homogeneity.json`,
`density_response.json`) plus `verify_prime_isomorphism_output.log`,
`density_response_output.log`.
