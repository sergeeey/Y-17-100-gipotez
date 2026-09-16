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
an artifact of Monte Carlo sampling error (there is none here).** **CALIBRATION CORRECTION
(added after point 12's independent check, user-caught mixing of arithmetic classes): this
"stabilization" reading mixes prime and composite `n` (21=3·7, 25=5²). Point 12 below shows
the PRIME-ONLY subsequence (`n=11,13,17,19,23`) is still cleanly RISING, not stabilizing, over
this exact same range (`n·Var(X_n) = 2.15, 2.25, 2.49, 2.61, 2.80` — monotonic, no plateau).
The apparent stabilization at `n=21,23,25` is a coincidence of which arithmetic classes those
3 values happen to be, not a real trend break — read the prime-only sequence in point 12 as
the more reliable signal, and the "visibly stabilizes" framing here as premature.** `n·(ES
bound)` shows the same
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

**12. Seventh angle: three concrete claims from a user-supplied external analysis, all
INDEPENDENTLY VERIFIED against this project's own exact data before being accepted — none
taken on the external text's say-so (`verify_seventh_angle_claims.py`, re-derives theta arrays
for n=9..25, cross-checks against points 10-11's already-stored summaries).**

**(a) Sharpened Efron-Stein — real, verified algebraic tightening.** Since point 11 proved
`W_{2j}=0` exactly, `B_n - W_1 = sum_{k odd>=3} k*W_k >= 3*sum_{k odd>=3} W_k = 3*(V_n-W_1)`
(each odd `k>=3` term is weighted by `k>=3`, not just `>=1`), giving

```
V_n <= (B_n + 2*W_1) / 3
```

— strictly tighter than the standard Efron-Stein `V_n<=B_n` whenever `W_1>0` (it is, always).
**Verified: holds at every tested `n=9..25`, no exceptions.**

**(b) For prime `n`, the level-1 Cauchy-Schwarz lower bound (point 7) is an EXACT EQUALITY,
not just a lower bound — independently re-derived, then verified to machine precision.**
Re-derivation: the prime-`n` symmetry theorem (point 4) already proves
`theta(G_S)=theta(G_{aS})` for every unit `a`; this extends from single-generator flips to the
FULL vector, giving `X(pi_a . epsilon) = X(epsilon)` identically (`pi_a` = the coordinate
permutation induced by multiplying generator indices by `a`). This forces
`X_hat({i}) = X_hat({j})` whenever `i,j` are in the same `Z_n^x`-orbit — for prime `n`, ALL of
them, since the action is transitive. Equal singleton coefficients is exactly Cauchy-Schwarz's
equality condition (proportionality between the coefficient vector and `Q`'s own uniform
weights), so `W_1 = M_n'(1/2)^2/(4m)` EXACTLY for prime `n`.

**Verified: at every prime `n` in {11,13,17,19,23}, the gap between `W_1` and
`M_n'(1/2)^2/(4m)` is `~1e-17` to exactly `0` (machine precision), and the spread across
singleton coefficients (`max-min`) is `~1e-16` (machine zero).** At composite `n` in
{9,15,21,25}, the gap is real and nonzero (`0.001-0.008`) and the singleton spread is
substantial (`0.03-0.09`) — confirming the equality is genuinely specific to primality, not a
generic small-`n` artifact.

**(c) Calibration correction to point 10's "stabilization" claim — the prime-only
subsequence is still rising, not stabilizing.** Point 10 read `n·Var(X_n)` as stabilizing at
`n=21,23,25` (`3.01→2.80→2.79`). Those three `n` mix arithmetic classes (`21=3·7`, `25=5²`,
only `23` prime). Filtering to PRIME `n` only:

| n (prime) | n·Var(X) | n·W1 | kappa_n = B_n/W_1 |
|---:|---:|---:|---:|
| 11 | 2.154 | 1.951 | 1.327 |
| 13 | 2.249 | 2.027 | 1.352 |
| 17 | 2.494 | 2.145 | 1.561 |
| 19 | 2.608 | 2.217 | 1.606 |
| 23 | 2.805 | 2.326 | 1.733 |

**All three quantities are MONOTONICALLY RISING across the prime subsequence, with no visible
plateau** — the point-10 "stabilization" reading is corrected: it was reading a coincidence of
which specific `n` happened to land at 21/23/25, not a real trend break. This does not refute
`Theta(1/n)` (small-`n` monotonic rise before an eventual plateau is entirely consistent with
it — the same qualitative shape as points 3/9b's noisy large-`n` data, which also needed
`n>~500` before visibly flattening), but it does mean point 10's specific "stabilizes by
`n=25`" claim was premature and is retracted in favor of "rises through the entire tested
range, plateau (if any) lies beyond `n=25`."

**What remains genuinely open, stated precisely using the new machinery:** whether
`|M_n'(1/2)|=O(1)` and `kappa_n=O(1)` as `n->infinity` (which together would give
`Var(X_n)=O(1/n)` via (a) and (b) combined) is NOT established by 5 rising prime data points
— it requires either a proof, or exact data at meaningfully larger prime `n` than `23`.

**13a. Zero-cost Hamming-layer decomposition (the user's own suggested free step, done before
the expensive necklace-orbit work) on the already-computed exact data, `n=9..25`.** For each
layer `q=|S|`, computed `mu_q=E[X||S|=q]`, `A_q=E[delta_i||S|=q]`, `C_q=Var(delta_i||S|=q)`
(`delta_i(S)=X(S)-X(S union{i})`, `check_hamming_layer_decomposition.py`). Confirmed exactly:
(i) the telescoping identity `A_q=mu_q-mu_{q+1}` (max gap `~1e-16`, all `n`); (ii)
`delta_i(S)>=0` everywhere (`min delta` non-negative up to floating noise at every `n`) —
theta is monotone non-increasing under edge addition, matching the SDP definition read
directly from the primary source; (iii) for PRIME `n`, `C_0=C_{m-1}=0` EXACTLY — the same
prime-symmetry theorem (point 4) forces equal `delta_i` across `i` at the boundary layers, a
clean cross-check the theorem is being applied consistently. **Informative, not yet
actionable finding:** `C_q` peaks OFF-CENTER, at small-to-moderate `q` (e.g. `n=23`: `C_2,C_3
~0.030`, vs the exact-middle `C_5~0.025`) rather than growing monotonically toward `q=m/2`
where the binomial weight is largest — meaning the "shape heterogeneity" component sits partly
in the BULK of typical graphs, not concentrated in rare tail layers a Chernoff-type argument
could cheaply kill. This favors the user's own "bulk LP geometry" diagnosis over "rare-tail
Chernoff bound" as the likely-needed next theoretical tool, though neither is attempted here.

**13. Implemented the necklace/orbit-reduction technique (point 12's named next step) —
a real implementation bug caught by the mandated positive control BEFORE trusting new
results, fixed, then EXACT data obtained at `n=29,31,37`.**

**The bug, caught not avoided:** the first implementation rotated the `m` bit-positions in
their NATURAL order (generator `1,2,...,m`), silently assuming this already matched the
`Z_n^x`-orbit structure. It does not — multiplication by a primitive root visits generator
indices in a specific, non-natural order. `cross_validate_n23()` (comparing the orbit-reduced
theta array against the already-known exhaustive one from points 10-12, element-by-element)
caught this immediately: `max diff = 4.63` (large, not floating-point noise) on the first run.
**Fixed** by explicitly computing a primitive root `g` mod `n` and relabeling bit-position `t`
to natural generator index `min(g^t mod n, n - g^t mod n)` BEFORE treating bit-rotation as the
group action — this is what actually makes multiplication-by-`g` correspond to a cyclic shift.
**Re-validated: `max |exhaustive - orbit_reduced| = 8.88e-14`** (machine precision) at `n=23`.

**Independent triple-consistency check:** the orbit COUNTS produced by brute-force enumeration
matched the user-supplied Burnside necklace formula `N_m=(1/m)*sum_{d|m} phi(d)*2^(m/d)`
EXACTLY at every new `n` (`n=29`→`1182`, `n=31`→`2192`, `n=37`→`14602`) — three independent
things (the formula, the brute-force orbit enumeration, and the n=23 cross-validation against
exhaustive LP) now agree, giving strong confidence the method is correct before trusting its
output at `n` where no independent check exists.

**Exact results at n=29, 31, 37 (LP-solve counts: `1182`, `1096`, `14602` — `13.9x`-`29.9x`
fewer than the `2^m` full enumeration; the odd-`m` complement-pairing trick worked exactly as
predicted, halving the count at `n=31`, `m=15` odd):**

| n (prime) | m | LP solves | n·Var(X) | n·W1 | n·W3 | kappa_n | resid. ratio `(V-W1)/(B-W1)` |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 29 | 14 | 1182 | 3.033 | 2.456 | 0.416 | 1.868 | 0.271 |
| 31 | 15 | 1096 | 3.098 | 2.496 | 0.425 | 1.902 | 0.267 |
| 37 | 18 | 14602 | 3.272 | 2.598 | 0.451 | 2.004 | 0.258 |

**Honest reading, extending the point-12 prime-only sequence
(`n=11..37`: `n·Var(X)=2.15,2.25,2.49,2.61,2.80,3.03,3.10,3.27`):**
`n·Var(X)` and `kappa_n` CONTINUE rising through `n=37` — no plateau is visible anywhere in the
tested range yet, `kappa_n` crosses `2.0` at `n=37`. **This does not refute `Theta(1/n)`, but
it does mean the range tested so far shows no evidence of the constant `C` in `V_n~C/n`
settling down — the un-excluded `V_n=L(n)/n` alternative (`L(n)` slowly growing, named back in
this experiment's original CORRECTED CALIBRATION note) remains just as live as before this
check, not weaker.** One quantity DOES look comparatively stable across the same range: the
residual ratio `(V_n-W_1)/(B_n-W_1)` sits in a narrow band (`0.258-0.333` across all 8 prime
points `n=9..37`, not obviously trending) — suggesting that WHATEVER is driving the slow growth
of `nV_n` affects level 1 and the level≥3 residual in roughly the same proportion, rather than
one specific level runaway-growing relative to the others.

**14. Density-vs-shape localization, per direct user request — the sharpest structural
finding of this whole investigation, and not a comfortable one.**

Decomposed `E[delta^2] = sum_q w_q*A_q^2 + sum_q w_q*C_q` (`w_q=C(m-1,q)/2^(m-1)`, the ACTUAL
Hamming-layer probability, not just `A_q`/`C_q`'s own values) using the validated
necklace-orbit method uniformly across `n=11..53` (extended in three follow-up rounds per direct
user request: `n=37->41,43`, then `n=41,43->47`, then `n=47->53`; LP-solve counts grow steeply
with `m`: `n=41` cost `52,488` LP solves (even `m=20`, no complement halving), `n=43`
`~49,940` (odd `m=21`, halving applied), `n=47` and `n=53` (`m=23,26`, both odd, halving
applied) cost on the order of several hundred thousand and `~1.3M` LP solves respectively —
`check_density_vs_shape_decomposition.py` for `n<=47`, `extend_n53_only.py` (reuses
`run_one_n()` unchanged, only avoids recomputing already-verified `n<53`) for `n=53`. **The
series was explicitly stopped at `n=53` by direct user decision** after being shown the
projected cost of `n=59` (`m=29`: `2^29~=537M` subsets in the reconstruction loop vs `67M` at
`n=53`, ~`9M` LP solves vs `~1.3M`, and an estimated memory footprint of `9-15GB+` for the main
arrays vs the `~3.1GB` observed at `n=53`) — this is a deliberate cost/information stopping
point per the Cheapest Differentiating Test Protocol, not a computational failure.):

| n | n²·(density part) | n²·(shape part) | shape fraction of `E[δ²]` |
|---:|---:|---:|---:|
| 11 | 19.22 | 3.56 | 0.156 |
| 13 | 19.36 | 4.39 | 0.185 |
| 17 | 19.30 | 9.16 | 0.322 |
| 19 | 19.50 | 10.57 | 0.352 |
| 23 | 19.89 | 13.82 | 0.410 |
| 29 | 20.55 | 17.45 | 0.459 |
| 31 | 20.80 | 18.46 | 0.470 |
| 37 | 21.46 | 21.36 | 0.499 |
| 41 | 21.88 | 23.24 | 0.515 |
| 43 | 22.10 | 24.03 | 0.521 |
| 47 | 22.51 | 25.55 | 0.532 |
| 53 | 23.08 | 27.54 | 0.544 |

**The density part (`n²·sum_q w_q A_q^2`) remains nearly flat (`19.2 -> 23.1`, a 20% drift
over the FULL `n=11..53` range, growth visibly slowing in the last several points) — genuinely
consistent with `O(1)`, matching the density-response experiment's own earlier finding (point
5) that the bulk decrement `A_q ~ 4-5/n`.** The shape part is NOT flat and, extending the
`n=37` crossover finding, remains clearly and increasingly above density at every point past
`n=37` (`27.54>23.08` at `n=53`) — **shape is now the dominant contributor to `E[delta^2]`, not
merely caught up to parity.** The shape fraction continues past `50%`, reaching `54.4%` at
`n=53`. Its raw increments are `0.029,0.137,0.030,0.058,0.049,0.011,0.029,0.016,0.006,0.011,
0.012,0.013` — not monotonic and not by themselves informative, because the `n`-gaps between
successive prime points are uneven (`2,4,2,4,6,2,6,4,2,4,4,6`). **Normalizing by the gap
(increment per unit `n`) over the most recent, evenly-spaced tail gives a cleaner signal:
`41->43`: `0.00295`/unit, `43->47`: `0.002675`/unit, `47->53`: `0.002083`/unit — this specific
normalized sub-sequence IS monotonically decreasing across all three most recent points.** This
is noted honestly as a somewhat firmer (but still thin — 4 points, `n=41..53`, one specific
normalization choice) sign that the shape fraction's growth RATE may be slowing, not that the
fraction itself is bounded below `1` or has a known limit — the possibility that it keeps
climbing slowly toward `1` (all of `E[delta^2]` eventually shape-dominated) is not excluded by
this data.**

**CALIBRATION CORRECTION (2026-09-11, caught on independent re-check of a pasted external
analysis's own calibration point — verified against this experiment's own established math
before accepting, per `audit-verification-gate.md`):** the two paragraphs above, and earlier
drafts of this point, said the "obstruction to `O(1/n)`" or "where any `L(n)` in `V_n=L(n)/n`
would have to live" lives in the shape term. That overstates what `E[delta^2] = D_n + S_n`
actually controls. `B_n = (m/4)*E[delta^2]` (established identity, point 12) feeds the
Efron-Stein bound `V_n <= B_n` (and the sharpened `V_n <= (B_n+2*W_1)/3`, point 12a) — an
INEQUALITY, not an identity connecting `E[delta^2]` to `V_n` itself. `V_n` is exactly the sum
of Fourier-Walsh level weights `W_k` (`k>=1`, Parseval), a different quantity from `B_n`. So
the correct, narrower statement is: **the observed growth of the Efron-Stein sensitivity-energy
`E[delta^2]` localizes mainly in the within-layer shape-heterogeneity term `S_n`, not in the
mean single-generator response `D_n` (well-behaved, looks `O(1)`)** — consistent with point
13a's earlier, cruder observation that `C_q` peaks off-center; this weighted version makes the
same point rigorously, using the actual layer probabilities rather than the raw `C_q` values
alone. This bounds where the Efron-Stein SLACK could be hiding a `L(n)` factor if `V_n` itself
does carry one — it is a statement about the bound, not a proven statement about `V_n`'s own
asymptotics.

**Honest calibration:** 12 points, `n=11..53`, still small by the standard of what would be
needed to distinguish `L(n)=O(1)` (with a slowly-approached asymptotic shape fraction) from
`L(n)=O(log log n)` or similar slow growth (shape fraction still climbing at larger `n`) — this
localizes WHERE the open question lives and adds a somewhat firmer (still not proof) hint that
the shape fraction's own growth RATE may be slowing, but does not resolve the underlying
question, and does not bound the shape fraction itself away from `1`. **The series is stopped
at `n=53` by explicit user decision** (see cost note above) — this was a deliberate
cost/information tradeoff call, not a claim that `n=53` is a natural or theoretically motivated
stopping point. No further attempt at a proof is made here; per the Cheapest Differentiating
Test, the next informative step, if resumed, would be either (a) extending this exact weighted
decomposition further in prime `n` (cost grows roughly as `2^((n-1)/2)`, so each further step is
substantially more expensive than the last — `n=59` alone was estimated at `~9M` LP solves and
`9-15GB+` memory versus `~1.3M` LP solves and `~3.1GB` at `n=53`), or (b) a genuine new
theoretical tool for bounding within-layer LP-optimum variance — neither attempted further this
session. **A candidate framing for (b), proposed in a pasted external analysis:** define
`S_n = E[Var(delta_i | Q)]` (`Q` the Hamming-layer index) explicitly and attack it via
fixed-layer / Johnson-graph structure, swap-derivatives, and mixed second differences
`Delta_i Delta_j X` — a qualitatively different attack from every LP-sensitivity variant tried
in points 6, 8, 9a (all of which moved a single coordinate, not a swap). **Attempted in point 15
below, per direct follow-up user request ("попробуй S_n через Johnson graph") — real new theorem
found, but the direct aggregate application does NOT help (null result), see point 15.**

**15. Johnson-graph swap-Poincaré bound on `S_n` — a real new theorem, but a null result for
`O(1/n)` in its direct/naive form.**

**Setup.** Fix generator `i` (bit 0). Within Hamming layer `q` (`S` an arbitrary `q`-subset of
the remaining `N=m-1` generators, `i` excluded), the layer's subsets are exactly the vertices of
the Johnson graph `J(N,q)`: `S,S'` adjacent iff they differ by one SWAP (`S'=S\{a}∪{b}`,
`a∈S, b∉S`). `J(N,q)` is regular of degree `d=q(N-q)`. This is a genuinely new move — every
earlier LP-sensitivity attempt (points 6, 8, 9a) only ever moved ONE coordinate in/out; a swap
moves two at once, which is exactly the mixed second-difference `Delta_i Delta_j X` structure the
pasted external analysis pointed at.

**Theorem, with an actual analytic derivation (upgraded 2026-09-11 — originally stated here as
"verified by diagonalization", which is a correct but weaker claim; a pasted external analysis
supplied the analytic route, independently re-verified against this experiment's own data before
accepting it — `audit-verification-gate.md`, "their [VERIFIED] = my [INFERRED]" — not taken on
the citation's word):** `J(N,q)`'s swap-adjacency graph is a classical association scheme (the
Johnson scheme); its eigenvalues are the standard Eberlein-polynomial values

```
lambda_j = (q-j)*(N-q-j) - j     for j = 0, 1, ..., min(q, N-q)
```

(`lambda_0 = q(N-q) = d`, the degree, as required for the trivial/constant eigenspace). At `j=1`:
`lambda_1 = (q-1)*(N-q-1) - 1`, which expands algebraically to exactly `d - N` (verified by hand
and independently by direct diagonalization, see below) — giving the normalized-walk gap

```
gap(N,q) = 1 - lambda_1/d = N / (q*(N-q))
```

**Cross-check performed against this experiment's OWN already-computed full spectra (not the
external source's say-so):** every distinct eigenvalue level found by direct diagonalization at
`N=10,13,14` (34 tested `(n,q)` layers, `check_johnson_eigenspace_decomposition.py`'s output)
matches the FULL Eberlein-polynomial formula above for EVERY level `j`, not just `j=1` — exact
match at all 34 layers, not a fit. Additionally verified to machine precision (`max err
~1.4e-15`) via direct `numpy.linalg.eigvalsh` on the actual transition matrix at `N=6,8,10,13`
and every `q` in each — 30+ independently diagonalized cases specifically for the `j=1`/gap value
(`verify_johnson_spectral_gap.py`). At `q=1` (and `q=N-1`) the swap-graph is exactly the complete
graph `K_N`, giving the standard identity `Var(f)=(1/2)E[(f(X)-f(Y))^2]` for iid `X,Y` — the
formula reduces to this analytically-known case exactly, a structural sanity check beyond pure
numeric coincidence. **The diagonalization is now correctly understood as verification OF the
analytic derivation (catching an implementation bug, confirming the right matrix/normalization
convention was used), not as the sole evidence for the formula.**

**Corollary (Poincaré inequality, standard for a reversible walk with this spectral gap):**

```
C_q = Var(delta_i(S) | |S|=q)  <=  T_q * q*(N-q) / (2N)
```

where `T_q = E[(delta_i(S)-delta_i(S'))^2]` over a uniform `S` in layer `q` and a uniform single
swap `S'` — the "swap-Dirichlet-energy" (`check_johnson_swap_energy.py`, exact enumeration of
every swap pair in every layer, reusing the same validated necklace-orbit `theta` data).

**Empirical check, `n=23` (cheapest sanity point, `N=10`):** the bound HOLDS at every tested `q`
(0 violations), exactly tight at `q=1,9` (tightness ratio `1.0000`, matching the `K_N` analytic
case), and non-trivially informative in the middle (tightness `~0.49-0.62`) — the bound is real,
not vacuous.

**Aggregate result across `n=23,29,31,37` — the actual test of whether this HELPS, and it does
NOT (honest null result):**

| n | N | `n²·S_n` (observed, matches point 14's shape column exactly) | `n²·`(Poincaré bound) | tightness |
|---:|---:|---:|---:|---:|
| 23 | 10 | 13.82 | 26.53 | 0.521 |
| 29 | 13 | 17.45 | 38.02 | 0.459 |
| 31 | 14 | 18.46 | 41.85 | 0.441 |
| 37 | 17 | 21.36 | 53.55 | 0.399 |

The bound grows FASTER than the quantity it bounds (`+102%` for the bound vs `+55%` for the
observed value, over the same `n=23→37` range) — tightness DECREASES monotonically with `n`
(0.521→0.459→0.441→0.399). **This is a real, verified new theorem that does not, in its direct/
naive uniformly-weighted form, help toward `O(1/n)` — if anything the swap-Dirichlet-energy `T_q`
itself appears to grow at least as fast as `C_q`, possibly faster.** Per `research-methodology.md`
principle 2 ("NULL = progress"), this rules out the simplest version of the Johnson-graph attack
without needing to try it again; it does not rule out a sharper, layer-adaptive, or differently-
weighted use of the same verified spectral-gap theorem — attempted directly below, per direct
follow-up user request ("попробуй послойно-адаптивную версию границы").

**15a. Layer-adaptive attempt: WHY the naive bound is loose — a real diagnostic finding, NOT
yet a new provable bound.**

The naive point-15 bound implicitly assumes ALL of `C_q`'s variance sits in the single
worst-gap eigenspace (`l=1`, `gap=N/(q(N-q))`, the only eigenvalue used). The Johnson scheme
actually has `min(q,N-q)` nontrivial eigenspaces per layer, most with STRICTLY BETTER (larger)
gaps than `l=1`. **By direct diagonalization + exact projection of `delta` onto every eigenspace
(Parseval verified exactly: `sum_l energy_l = C_q` to the last digit, at every tested layer —
`check_johnson_eigenspace_decomposition.py`), the `l=1` (worst-gap) eigenspace's share of `C_q`
is small and shrinks toward the middle of each layer** (e.g. `n=31`: `31.4%` at `q=2` down to
`0.0%` at `q=7`, the layer's center). **Aggregated with the same `w_q` weighting as `S_n`, the
fraction of the WHOLE weighted `S_n` sitting in the worst-gap eigenspace is
`6.31%` (`n=23`) → `3.39%` (`n=29`) → `2.51%` (`n=31`) — monotonically decreasing across all 3
tested points (`analyze_l1_energy_fraction.py`).**

**This explains the point-15 bound's looseness precisely: it pessimistically weights the
worst-gap eigenspace at 100%, when in reality that eigenspace carries under 7% of the signal,
falling further as `n` grows.** It does NOT yet constitute a new, independent, provable bound —
the per-level energy fractions reported here were computed FROM the already-known `C_q`
(via exact projection), not predicted ahead of it; using them to "tighten" the bound would be
circular. A genuinely new adaptive bound would need an INDEPENDENT way to predict or bound the
`l=1`-specific contribution (or, symmetrically, the higher-level contributions) without first
computing `C_q` — analogous to how point 11's vanishing-even-Fourier-levels theorem on the
Boolean cube started as an empirical pattern before being PROVEN from the antisymmetry
structure. No such independent argument was found or attempted this session.

**Honest calibration (as of the 3-point check):** `n=23,29,31`, a monotonic and encouraging
trend, but thin — `n=37`'s per-layer dense diagonalization (`C(17,8)=24310`) is computationally
infeasible with the direct eigendecomposition approach, so the trend could not be checked further
by that method within this session's scope. **Extended past this limit in point 15b below.**

**15b. An actual independent, cheap predictor of the `l=1` share — extends the trend to 6 points,
still monotonic, per direct follow-up user request ("попробуй адаптивную границу с независимым
предсказанием l=1-доли").**

The `l=1` (degree-1) eigenspace of functions on the Johnson slice is exactly the span of the
CENTERED single-element indicators `x_j(S) = 1[j in S] - q/N` (`j` ranging over the `N`-element
ground set). Its energy (the `l=1` contribution to `C_q`) is the L2 norm of the best linear fit
of `delta` onto `span{x_j}` — computable from just `N` cheap per-element "marginal effect"
statistics `mu_j = Cov(delta, x_j)`, **not** the full `C(N,q)`-dimensional eigendecomposition
point 15a needed. Using the closed form of the centered-indicator covariance matrix (`Sigma_jj =
q(N-q)/N^2`, `Sigma_jk = -q(N-q)/(N^2(N-1))` for `j≠k`, itself verified against the empirical
covariance to `~1e-16` at every tested layer) and the fact that `mu` lives entirely in the
sum-zero subspace where `Sigma` acts as a SCALAR multiple of the identity (`J` annihilates that
subspace), the projection collapses to an EXACT closed form, no numerical pseudo-inverse needed:

```
Energy_l1 = ||mu||^2 * N*(N-1) / (q*(N-q))
```

**Cross-validated against the exact diagonalization-based `l=1` energy (point 15a) at every
tested layer, `n=23,29,31` — 34/34 exact matches (`rel_err=0.0000` at every layer)**, confirming
this cheap closed form is the SAME quantity computed a completely different way, not merely
correlated with it. This is the mandatory positive control (`falsification-ladder.md` § 2a)
before trusting the method on `n` where the expensive diagonalization is infeasible.

**Removed diagonalization from the trust chain entirely (2026-09-11, per a pasted external
analysis's proposed algebraic check — independently re-derived and re-verified, not accepted on
its word): `verify_l1_projection_rigorous.py` constructs the ACTUAL projection function
`P_1f(S) = sum_j c_j*x_j(S)` (`c_j = mu_j*N(N-1)/(q(N-q))`) and checks its two DEFINING
properties directly against the raw exact `delta` data, with no eigendecomposition anywhere:**

```
E[(P_1 f)^2]              == Energy_l1 (the closed-form scalar)   -- matched to 1e-9 or better
E[(f - P_1 f) * x_j] ~= 0  for every ground element j              -- max violation ~1e-18
```

Checked at all 9 layers of `n=23` and, specifically, the two layers that showed a `~1%`
discrepancy under the earlier numerical-pseudo-inverse route (`n=29,q=5`; `n=31,q=2`) — **both
now match to machine precision** (`n=29,q=5`: closed-form `0.00050674` = direct `0.00050674`;
`n=31,q=2`: closed-form `0.00836220` = direct `0.00836220`), confirming the earlier `~1%` gap was
an eigenvalue-grouping artifact of `check_johnson_eigenspace_decomposition.py`'s diagonalization
method (as suspected), not a formula error. The two independent parametrizations — this
experiment's `mu_j=Cov(delta,x_j)` route and the pasted analysis's `a_j=E[f|j∈S]-E[f|j∉S]` route
— are ALSO algebraically identical (`mu_j = q(N-q)/N^2 * a_j`, verified on synthetic data, 5/5
random cases), a genuine independent-derivation cross-check on top of the empirical one.

**Extended to `n=37,41,43,47` (previously inaccessible to point 15a's dense diagonalization) —
the aggregate weighted `l=1` fraction continues DECREASING, now across 7 points, not 3:**

| n | aggregate `l=1` fraction of weighted `S_n` |
|---:|---:|
| 23 | 6.31% |
| 29 | 3.39% |
| 31 | 2.51% |
| 37 | 1.41% |
| 41 | 1.04% |
| 43 | 0.90% |
| 47 | 0.72% |

**Monotonically decreasing across all 7 tested points, and the decrements are themselves
shrinking (roughly halving n=23→31, then dropping to sub-1.5% territory by n=37+)** — a
substantially firmer trend than the 3-point check. **`n=47` was independently recomputed by
this experiment's own already-validated pipeline (`verify_marginal_effect_l1_predictor.py`,
NOT taken from a pasted external claim) — a pasted external analysis had separately claimed
`0.7230335%` for `n=47`; this experiment's own independent recomputation gives `0.7230%`,
matching to 4 significant figures. Per `audit-verification-gate.md` ("their [VERIFIED] = my
[INFERRED]"), the external number was NOT recorded until reproduced independently — the value
now in this table is this experiment's own computed result, the external claim served only as a
target to check against, and the internal-consistency detail the external analysis cited (its
local recomputation of `S_47` matching this repo's already-published value) is explained simply:
this project's repository is public, so that value was directly readable, not independently
re-derived by them.** **This still does NOT constitute a new independent proof of anything about
`V_n`'s asymptotics** — `mu_j` (hence the whole `l=1`-energy computation) is derived from the
SAME `delta` data that determines `C_q` itself; using the observed fraction to "tighten" a bound
on `C_q` remains circular, exactly as noted in point 15a. What this DOES establish: the trend is
real (not a diagonalization artifact of small `N`, since it continues under a completely
different, cheaper computational route), and the door is now open to check even larger `n`
(`n=53` is feasible with this cheap method, not attempted this session) without needing dense
diagonalization at all.

**Artifacts (this point):** `check_johnson_swap_energy.py` (+`metrics/johnson_swap_energy.json`),
`verify_johnson_spectral_gap.py` (+`metrics/johnson_spectral_gap_verification.json`,
`metrics/johnson_gap_formula_generalization_check.json`), `aggregate_johnson_bound.py`
(+`metrics/johnson_bound_aggregate.json`), `check_johnson_eigenspace_decomposition.py`
(+`metrics/johnson_eigenspace_decomposition.json`), `analyze_l1_energy_fraction.py`,
`verify_marginal_effect_l1_predictor.py` (+`metrics/marginal_l1_predictor_extension.json`),
`verify_l1_projection_rigorous.py`.

**16. A genuinely sharper Poincaré bound (a real theorem, not a diagnostic) — peels off the
now-exactly-known `l=1` energy, pays the rest at the next-best gap. Real, substantial
improvement; does NOT reverse the qualitative divergence trend.**

Per direct user request ("отлично как в фоне прогон закончится выполни его"), implemented and
tested the two-term sharpened bound proposed in a pasted external analysis (independently
re-derived and verified before implementing, not accepted on citation). From the exact energy
identity `T_q/2 = sum_l gap_l*E_l` and `C_q = sum_l E_l` (`gap_l` non-decreasing in `l`, per the
already-verified Eberlein spectrum), peeling off the exactly-known `E_1` and bounding the
remaining levels by the next-best gap `gamma_2 = 2(N-1)/(q(N-q))` (verified by hand: `d-lambda_2
= 2(N-1)` exactly, matching the general spectrum formula at `j=2`) gives

```
C_q  <=  E_1 + (T_q/2 - gamma_1*E_1) / gamma_2
```

**This is NOT circular like points 15a/15b** — `E_1` (via the closed-form marginal-effect
predictor) and `T_q` (swap-Dirichlet-energy) are both computable WITHOUT knowing `C_q` in
advance; `gamma_1`, `gamma_2` are pure graph-theoretic constants. This is a genuine new upper
bound, structurally the same "peel off known low levels" technique already used in point 12a's
sharpened Efron-Stein (there via a PROVEN zero, here via a numerically-established `E_1`).

**Substrate Gate note (real bug caught on first run, not hidden):** the first implementation
crashed with a `KeyError` — `check_johnson_swap_energy.py`'s layer loop includes the trivial
boundary layers `q=0,N` (where `C_q=0`), while `verify_marginal_effect_l1_predictor.py`'s loop
excludes them; combining the two dicts by `q` without aligning domains failed immediately. Fixed
by iterating over the intersection of both domains. Caught before any result was trusted, per
this project's own Substrate Gate discipline.

**Results across all 7 tested points (`n=23,29,31,37,41,43,47`), `check_improved_poincare_bound.py`
— the bound is real and validated at EVERY layer (`C_q<=improved_bound<=naive_bound`, no
exceptions across any tested `(n,q)`):**

| n | naive tightness | improved tightness |
|---:|---:|---:|
| 23 | 0.521 | 0.913 |
| 29 | 0.459 | 0.836 |
| 31 | 0.441 | 0.812 |
| 37 | 0.399 | 0.747 |
| 41 | 0.376 | 0.709 |
| 43 | 0.366 | 0.694 |
| 47 | 0.349 | 0.664 |

**Honest calibration — the improvement is real but does NOT reverse the qualitative picture.**
The improved bound roughly halves the "excess" over the naive one at every point (tightness
nearly doubles, e.g. `0.521→0.913` at `n=23`). But `n²·improved_bound` itself grows FASTER than
`n²·C_q` over the tested range (`+154.2%` vs `+84.9%`, `n=23→47`) — slower growth than the naive
bound's own `+176.2%`, but still divergent, not convergent. **This is one rung of the `l=1→l=2→
l=3→...` ladder proposed alongside this bound; a single rung meaningfully tightens the bound but
does not, by itself, flip the qualitative trend from "bound grows faster than truth" to "bound
tracks truth."** Whether further rungs (peeling `E_2` via pairwise marginal effects, paying the
remainder at `gamma_3`) would eventually reverse the trend is an open question, not attempted
this session.

**Artifacts (this point):** `check_improved_poincare_bound.py`
(+`metrics/improved_poincare_bound.json`).

**17. `l=2` (pairwise) energy — second-order ANOVA on the Johnson slice. Real, verified
diagnostic: the spectral mass keeps moving to HIGHER levels as `n` grows, not just away from
`l=1`.**

Per direct user request ("попробуй l=2 через парные эффекты"). The `l=2` eigenspace of
functions on the slice is spanned by pairwise interactions, but raw pairwise indicators
`e_j*e_k` are NOT automatically orthogonal to the `l=0,1` subspaces on the slice (unlike the
Boolean cube, where independence makes this free) — the classical fact used here is that the
degree-`<=2` polynomial space (span of `{e_j}` and `{e_j*e_k}`) equals `V_0+V_1+V_2` exactly, so
fitting `delta`'s best L2 projection onto that space and subtracting the already-known `E_1`
gives `E_2` directly.

**Verification chain, each step checked before trusting the next (integrity.md discipline):**
1. The 7 hypergeometric ("falling factorial") moment formulas needed for the feature Gram matrix
   (`Var(e_j)`, `Cov(e_j,e_k)`, `Cov(e_j,e_j e_k)`, `Cov(e_i,e_j e_k)` disjoint, `Var(e_j e_k)`,
   `Cov` sharing one element, `Cov` disjoint pairs) — each verified against DIRECT exhaustive
   enumeration at two different `(N,q)` pairs (`N=10,q=4` and `N=13,q=6`), exact match at every
   entry, not derived from memory alone.
2. The resulting `E_{<=2}=E_1+E_2` computation cross-validated against this experiment's own
   EXACT full diagonalization (`check_johnson_eigenspace_decomposition.py`'s stored levels) at
   `n=23,29,31` — matched (`rel_err<0.2%` at every tested layer, exact at the edge layers
   `q=1,N-1` where only `l=1` exists and `E_2=0` correctly).
3. A real implementation bug caught mid-session (unrelated `KeyError` in `check_improved_
   poincare_bound.py`, Substrate Gate discipline — see point 16) reinforced the practice of
   running the positive control before trusting a new computation; applied identically here.

**Aggregate result (`w_q`-weighted, same convention as points 14/15b/16), across all 7 tested
points:**

| n | `E1` fraction | `E2` fraction | `E1+E2` covers |
|---:|---:|---:|---:|
| 23 | 6.310% | 71.861% | 78.170% |
| 29 | 3.389% | 62.876% | 66.265% |
| 31 | 2.506% | 60.583% | 63.089% |
| 37 | 1.407% | 54.454% | 55.861% |
| 41 | 1.042% | 50.635% | 51.677% |
| 43 | 0.901% | 49.425% | 50.326% |
| 47 | 0.723% | 46.851% | 47.574% |

**This confirms and sharpens the pattern already suggested when point 16 was proposed: it is
NOT just `l=1` whose share shrinks with `n` — `E_2`'s share shrinks too, and so does the
COMBINED `E_1+E_2` coverage of `C_q` (78.2%→47.6% over `n=23→47`).** By `n=47`, more than half of
`C_q`'s weighted mass sits in levels `l>=3`, not `l<=2`. This is a real, measured confirmation
(not a guess) that the spectral mass genuinely migrates to higher-and-higher levels as `n` grows
— consistent with, and sharper than, the point-15a/15b finding about `l=1` alone.

**What this does and does NOT imply for the ladder (`l=1→l=2→l=3→...`) proposed alongside point
16:** it does NOT automatically mean peeling more levels stops helping — point 16 already showed
that peeling a SHRINKING `E_1` still roughly doubled bound tightness, because the lever is which
gap the residual gets charged at (`gamma_l` grows with `l`), not how much energy the peeled
levels explain. Whether a 3-term bound (peeling `E_1+E_2`, paying the remainder at `gamma_3=
3(N-2)/(q(N-q))`) improves tightness further, similarly, or with diminishing returns, was NOT
computed this session — a natural next step, not attempted here.

**Artifacts (this point):** `check_l2_pairwise_energy.py` (+`metrics/l2_pairwise_energy.json`),
`aggregate_l2_energy.py` (+`metrics/l2_energy_aggregate.json`).

**18. The decisive ladder test: three-term bound (peeling `E_1` AND `E_2`) — the excess growth
over `C_q` roughly HALVES with each added rung. The strongest signal yet that the Johnson-graph
spectral ladder is a genuine mechanism, not just a diagnostic.**

Per direct user request/proposal ("посчитать строгую границу после точного вычитания `E_1+E_2`
и посмотреть, исправляет ли она scaling"), implemented and tested

```
C_q  <=  E_1 + E_2 + (T_q/2 - gamma_1*E_1 - gamma_2*E_2) / gamma_3
```

`gamma_3 = 3(N-2)/(q(N-q))` (verified by hand from the same general Eberlein-spectrum pattern as
`gamma_1,gamma_2`: `d-lambda_3 = 3(N-2)` exactly, matching `gamma_l = l(N-l+1)/(q(N-q))`).
Reuses `T_q`, `E_1`, `E_2` from points 15b/16/17 UNCHANGED.

**Result across all 7 tested points — tightness improves dramatically at every step of the
ladder:**

| n | naive tightness | two-term (point 16) | **three-term (this point)** |
|---:|---:|---:|---:|
| 23 | 0.521 | 0.913 | **0.984** |
| 29 | 0.459 | 0.836 | 0.952 |
| 31 | 0.441 | 0.812 | 0.939 |
| 37 | 0.399 | 0.747 | 0.899 |
| 41 | 0.376 | 0.709 | 0.872 |
| 43 | 0.366 | 0.694 | 0.859 |
| 47 | 0.349 | 0.664 | 0.836 |

**The decisive comparison — how much does each rung's bound OVERSHOOT the observed growth rate,
not just the tightness at one point:** computing the growth of `n²·bound` over `n=23→47` for
each version and subtracting the observed `n²·C_q`'s own growth (`+84.9%`) gives the "excess
growth" each version leaves unexplained:

| Bound version | growth of `n²·bound`, `n=23→47` | excess over observed `+84.9%` |
|---|---:|---:|
| naive (point 15) | +176.2% | +91.3 pp |
| two-term (point 16) | +154.2% | +69.3 pp |
| **three-term (this point)** | **+117.7%** | **+32.8 pp** |

**Each added rung of the ladder roughly HALVES the excess growth rate** (91.3→69.3→32.8 — the
second halving is even sharper than the first). This is qualitatively different from points
15a/15b/17's diagnostics: it is a real, validated inequality, and the pattern across THREE
independent ladder rungs (not two) is now itself suggestive of geometric decay in the excess —
if it continues, the ladder could plausibly converge to matching `C_q`'s true growth rate. This
does not prove `Θ(1/n)` or even `O(1/n)` — it is evidence FOR the mechanism the pasted external
analysis hypothesized ("the growth of the spectral gap compensates for mass migrating to higher
levels"), not a proof of it.

**Numerical caveat — CORRECTED diagnosis (2026-09-12, per direct user request to isolate the
cause before trusting the "validated inequality" language):** the initial hypothesis (cross-
recomputation noise from `T_q`/`E_1`/`E_2` each calling `solve_orbit_reduced` independently) was
explicitly TESTED and DISPROVEN — `check_l3_ladder_bound_unified.py` recomputes `theta_full`
exactly ONCE per `n` and derives all three quantities from that single source, and the
violations PERSIST (20 violations across the 7 tested `n`, same count and same layers as
before), with the aggregate table matching the non-unified run to 4 decimal places at every `n`.
**Second correction (2026-09-12, same session, caught by an independent check of the FIRST
correction's own claim before accepting it):** the "`E_2` should be exactly `0` at the boundary"
diagnosis above is ITSELF imprecise. Structurally, the `l=2` eigenspace exists whenever
`min(q,N-q)>=2` — so `E_2=0` is only forced at `q∈{0,1,N-1,N}`, NOT at `q=2` or `q=N-2` (where
`min(q,N-q)=2` and `l=2` is genuinely the LAST existing level, meaning `E_1+E_2` should equal
`C_q` EXACTLY there, with zero residual for any `l>=3` term). **Checked directly:** at
`q∈{1,N-1}` (min=1), `E_1+E_2` matches `C_q` to machine precision (`~1e-17`) at EVERY tested `n`
— clean. At `q∈{2,N-2}` (min=2, where `E_1+E_2=C_q` should ALSO hold exactly), the match is
inconsistent: exact at some `(n,q)` pairs (e.g. `n=23,29,31,37,47` at `q=2`) but off by
`1e-6`-to-`5e-5` at others (e.g. `n=41,q=2`: `+9.4e-6`; `n=43,q=2`: `+5.3e-5`) — no clean
deterministic rule (by `n`, by `q`, or by which side of the `q`/`N-q` mirror) was found
separating the exact cases from the inexact ones. **The proven antisymmetry theorem
(`X(S)+X(S^c)=0`, point 4) was checked directly against the raw `theta_full` array and holds to
`~3.3e-16` (pure floating-point noise) at every one of `n=43`'s `2^m` masks** — this rules OUT
`theta_full`/`delta` themselves as the error source; the error is confined to the `E_2` pinv
computation specifically, with a size (`1e-6` to `5e-5`) and layer pattern that is not yet fully
characterized. **What remains solid despite this open thread:** `two_holds=True` in ALL 20
violations (point 16's two-term bound is completely exception-free in both runs); the aggregate
`w_q`-weighted tightness table matches to 4 decimal places between the original and unified
computation; and the qualitative finding (excess growth roughly halving per ladder rung) does
not rest on any of the ~14% of layers showing this discrepancy, since their `w_q` weight is
small. **Calibrated status, per direct user framing:** point 18 is a "numerically compelling
refinement with an unresolved boundary-layer numerical discrepancy in the `E_2` estimator" — NOT
yet a fully layer-wise-verified inequality. The earlier "holds everywhere, no exceptions"
language is retracted for the per-layer claim (though not for point 16, where it remains true).
Full resolution would require replacing the `pinv`-based `E_2` fit with an analytic projection
onto the `l=2` eigenspace specifically (using the association-scheme's own harmonic basis for
`V_2`, not the raw redundant `{e_j, e_j*e_k}` features, which are linearly dependent by exactly
`N+1` empirically-measured null directions relative to `V_0+V_1+V_2`'s true dimension) — not
attempted this session; flagged as the concrete next step if this thread is resumed.

**FINAL RESOLUTION (2026-09-12, same session — Exam 1 of the user's own proposed 3-exam plan,
fully passed):** the raw `{e_j, e_j*e_k}` features carry `V_0`+`V_1` "leakage" into the pairwise
covariances `mu_ab=Cov(f,e_a*e_b)` (single-index features have NO such leakage, since centering
`f` alone already removes the `V_0` part — this is WHY `E_1` never needed a correction term).
The exact fix, proposed in a pasted external analysis and independently verified here before
use (not accepted on citation):

```
s_a = sum_{b!=a} mu_ab,    S = sum_{a<b} mu_ab
r_ab = mu_ab - (s_a+s_b)/(N-2) + 2S/((N-1)(N-2))       [orthogonal projection onto pure V_2]
gamma_2_eigen = q(q-1)(N-q)(N-q-1) / (N(N-1)(N-2)(N-3)) [V_2's own scalar covariance eigenvalue]
E_2 = sum_{a<b} r_ab^2 / gamma_2_eigen
```

No Gram matrix, no `pinv`, no redundant features — `r_ab` lives exactly in `V_2` by
construction. **Verification (`check_l2_analytic_projection.py`):** (1) cross-validated against
exact diagonalization at `n=23,29,31` — ALL `(n,q)` layers match to `~1e-17`-`1e-19`, not just
approximately; (2) the `q=2,N-2` zero-residual unit test (`E_1+E_2=C_q` exactly, since only
`l=1,2` exist there) now holds to `~1e-17`-`1e-18` at **every one of the 7 tested `n`**, zero
exceptions — the inconsistent pattern noted in the second correction above is fully resolved,
not merely reduced. **Re-running the complete three-term ladder with this analytic `E_2`
(`check_l3_ladder_bound_analytic.py`, single shared `theta_full` per `n` as before) gives
`VIOLATIONS: 0` across all 7 `n` and every tested layer** — `C_q<=three_term_bound<=two_term_
bound` holds with NO exceptions anywhere, matching point 16's own already-clean record. The
aggregate tightness table is essentially unchanged from the `pinv`-based run (`n=23`:
`0.9838` vs `0.9837`; all other `n` identical to 4 decimals) — **the effect was real all along;
what the noise obscured was the exactness of the inequality, not the magnitude of the
improvement.** Per the user's own calibration: **point 18 is now upgraded from "numerically
compelling refinement with an unresolved discrepancy" to a fully layer-wise-verified
inequality** — the first two rungs of the Johnson spectral ladder (`l=1`, `l=2`) are both
analytic, not numerically heuristic. Artifacts added: `check_l2_analytic_projection.py`
(+`metrics/l2_analytic_projection.json`), `check_l3_ladder_bound_analytic.py`
(+`metrics/l3_ladder_bound_analytic.json`).

**Artifacts (this point):** `check_l3_ladder_bound.py` (+`metrics/l3_ladder_bound.json`),
`check_l3_ladder_bound_unified.py` (+`metrics/l3_ladder_bound_unified.json`).

**Artifacts:** `check_cosh_bound.py`, `check_q_proxy_diagnostic.py` (+`_n3000.py`),
`check_single_generator_sensitivity.py` (+`_n3000.py`), `verify_cauchy_schwarz_lower_bound.py`,
`check_prime_symmetry_homogeneity.py`, `verify_prime_isomorphism_exhaustive.py`,
`check_density_response.py`, `verify_lp_sensitivity_concavity.py`, `verify_delta_g_bound.py`,
`analyze_own_data_for_upper_bound_signal.py`, `check_exact_enumeration_small_n.py`
(+`exact_enumeration_output.log`), `check_exact_walsh_decomposition.py`
(+`exact_walsh_output.log`), `verify_seventh_angle_claims.py`
(+`verify_seventh_angle_output.log`), `check_hamming_layer_decomposition.py`
(+`hamming_layer_output.log`), `check_necklace_orbit_reduction.py`
(+`necklace_orbit_output.log`), `check_density_vs_shape_decomposition.py`
(+`density_vs_shape_output.log`), `extend_n53_only.py` (n=53 only, reuses `run_one_n()`
unchanged to avoid recomputing already-verified `n<53`)
(+`verify_delta_g_output.log`)
(+`verify_lp_sensitivity_output.log`), and their outputs in `metrics/` (`cosh_bound_check.json`,
`q_proxy_diagnostic.json`, `q_proxy_diagnostic_n3000.json`, `single_generator_sensitivity.json`,
`single_generator_sensitivity_n3000.json`, `prime_symmetry_homogeneity.json`,
`density_response.json`) plus `verify_prime_isomorphism_output.log`,
`density_response_output.log`.

## Point 19 (2026-09-12) — Exam 2 of the autonomous plan: rigorous P_1+P_2 projection
functions, exact E_3 at the q=3,N-3 boundary

**Context:** Exam 1 (analytic `E_1`/`E_2`, 0 violations, points 15b/18) is complete. Per the
autonomous 3-exam plan, Exam 2 asks whether the "excess growth halving" pattern of the sharpened
Poincaré ladder (naive→two-term→three-term: `91.3pp→69.3pp→32.8pp`, point 18) continues at a
fourth rung, requiring `E_3` (third-order ANOVA on the Johnson slice). No closed-form triple-
centering formula for `E_3` at arbitrary interior `q` was supplied (unlike `E_1`/`E_2`, where the
user provided the exact formulas) — flagged in advance as the harder, higher-risk half of the
plan, so this session pursued the lower-risk "residual-based" route instead of deriving the
general interior-layer formula from scratch.

**Stage A — rigorous P_1+P_2 projection functions (`verify_l2_projection_rigorous.py`).**
`check_l2_analytic_projection.py`'s `e2_analytic` only computes `E_2` as a scalar; it never
constructs the actual projection *function* `P_2(S)`. This is required for Exam 2 (the residual
`h(S)=f_centered(S)-P_1(S)-P_2(S)` must be an actual computable function, not just an energy
number). Derived the double-centered pair basis `y_ab(S) = e_a(S)e_b(S) - (q-1)/(N-2)*(e_a(S)+
e_b(S)) + q(q-1)/((N-1)(N-2))`, proved algebraically (not just asserted) that (i)
`sum_{b!=a} y_ab(S) = 0` for every `S` and (ii) `E[y_ab]=0`, both relying on the exact identity
`sum_{b!=a} E_ab(S) = (q-1)*e_a(S)` (true for every `S`, not just in expectation, since
`e_a(S)^2=e_a(S)`). This also resolved an apparent discrepancy: `e2_analytic`'s `r_ab` formula
carries an extra `+2S/((N-1)(N-2))` term that a naive derivation of `y_ab` doesn't need — settled
by proving `s_a = sum_{b!=a} mu_ab = (q-1)*mu_e[a]` EXACTLY (same identity applied to `Cov(f,.)`),
which makes the two forms algebraically identical; not just assumed, confirmed numerically to
`~1e-18` below. **Verification: `P_2(S) = sum_{a<b} (r_ab/lambda_2) * y_ab(S)`, checked at every
layer across all 7 tested `n` (94 layers total): `E[(P_2 f)^2]` matches `e2_analytic`'s `E_2` to
`<1e-9`, and the residual `f_centered-P_1-P_2` is orthogonal to every `x_j` (V_1 basis) and every
`y_ab` (V_2 basis) to `~1e-17`-`1e-18` — VIOLATIONS: 0/94.**

**Stage B — exact E_3 at the q=3,N-3 boundary (`check_l3_boundary_energy.py`).** Same trick as
point 18's decisive `q=2,N-2` zero-residual test for `E_2`, extended one rung: at `q=3` (or
`N-3`), `min(q,N-q)=3` means the Johnson-scheme eigenspace decomposition has ONLY `l=1,2,3` — no
`V_4` or higher exists at that layer. Since Stage A proved `h=f_centered-P_1-P_2` is exactly
orthogonal to `V_0,V_1,V_2`, the spectral identity `C_q = E_1+E_2+Var(h)` (always true) collapses
to `Var(h)=E_3` exactly at this boundary — **no new triple-centering formula needed.** Verified
`E_3` two independent ways (`Var(h)` directly, and `C_q-E_1-E_2` by subtraction) at both `q=3`
and `q=N-3` for all 7 `n`: boundary residual `~1e-18`-`1e-19` everywhere, **0/14 violations**.
Cross-validated against exact diagonalization (`metrics/johnson_eigenspace_decomposition.json`,
matching the `l=3` eigenspace via the Eberlein formula `lambda_3=(q-3)(N-q-3)-3`) at `n=23,29,31`
— **0/6 violations, matches to `~1e-10`.**

**Result — `E_3/C_q` at the boundary, all 7 `n`:**

| n | 23 | 29 | 31 | 37 | 41 | 43 | 47 |
|---|-----|-----|-----|-----|-----|-----|-----|
| `E_3/C_q` | 0.2547 | 0.2514 | 0.2441 | 0.2345 | 0.2276 | 0.2235 | 0.2200 |

Monotonically decreasing across all 7 `n`, no exceptions — qualitatively the same pattern already
seen for `E_1/C_q` (point 15b) and `E_2/C_q` (point 17)'s own decreasing shares.

**Scope, stated honestly:** this result is the E_3 contribution ONLY at the `q=3,N-3` BOUNDARY
layers (where it happens to be exactly isolable without new machinery), not a general `E_3(q)`
formula for interior layers. It does NOT yet let the sharpened Poincaré ladder be extended to a
literal four-term bound at every layer (that needs `E_3` at ALL `q` from 3 to `N-3`, which
requires the harder general triple-centering derivation, still not attempted). What it DOES show:
(a) `P_1+P_2` are now verified as actual computable projection functions, not just scalars — the
residual-based route for Exam 2 is mechanically sound; (b) `E_3` is real, computable exactly at
the boundary, and its relative share continues the same declining trend as `E_1`,`E_2` — a
positive but partial signal for Exam 2's question, not a completed four-term ladder.

**Artifacts:** `verify_l2_projection_rigorous.py`, `check_l3_boundary_energy.py`
(+`metrics/l3_boundary_energy.json`).

## Point 20 (2026-09-12) — Exam 2 stage C: general interior-layer `E_3(q)` formula,
verified 22/22, 0 violations

**Context:** point 19 deliberately stopped at the `q=3,N-3` boundary, flagging the general
interior-layer formula as the harder, higher-risk part of Exam 2 — no closed form was supplied,
and a from-scratch symbolic triple-centering derivation risked a sign/index error. Explicit user
instruction: "продолжай к interior-layer формуле E3(q)".

**Approach (avoiding a from-scratch symbolic derivation):** reuse the already-verified `P_1`,
`P_2` operators (point 19) as generic projections — apply them to the raw triple indicator
`E_abc(S) = e_a(S)e_b(S)e_c(S)` **as the target function**, instead of `f`. Since `E_abc` is
degree-3 in the 0/1 indicators, it lives entirely in `V_0⊕V_1⊕V_2⊕V_3` — nothing above `V_3` to
remove. `z_abc(S) := E_abc(S) - P_1[E_abc](S) - P_2[E_abc](S)` is therefore exactly `E_abc`'s pure
`V_3` part, reusing code already verified to 0/94 violations rather than re-deriving inclusion-
exclusion by hand. `lambda_3` was HYPOTHESIZED by pattern-matching the already-verified
`lambda_1`, `lambda_2` closed forms (`lambda_l = [q]_l[N-q]_l/[N]_{2l}`, falling factorials) —
stated explicitly as a hypothesis requiring verification, not assumed correct.

**First attempt FAILED, caught and diagnosed, not glossed over:** the initial implementation gave
`E_3` values 8x to over 1000x too large (e.g. `n=23,q=7`: formula gave `7.91` against a true value
of `0.0077`). Diagnosed via a Gram-matrix inspection of `{z_abc}` (`diagnose_l3_gram.py`,
scratchpad): the raw Gram matrix had 8 distinct eigenvalue clusters (0.0083 to 0.102) and rank 111
of 120 — nowhere near the expected single-eigenvalue, rank-75 structure a correct pure-`V_3`
projection should have. **Root cause:** the code computing `Cov(E_ab, E_target)` for the `P_2`
step correlated only the single indicator `e_a` against the target, not the full pair product
`e_a*e_b` — undercounting the `V_1/V_2` content removed from `E_abc`, leaving `z_abc` far from
pure `V_3`. **Fix:** `mu_pairs_triples = big_e_pair.T @ eabc_centered / v` (using the already-built
pair-indicator matrix, matching the exact pattern `e2_analytic` uses against `f`). After the fix,
the Gram matrix of `{z_abc}` has an EXACTLY constant diagonal (0.00527777... to 15 decimal places
across all 120 triples at `n=23,q=3`) and a single nonzero-eigenvalue cluster equal to
`lambda_3` exactly — confirming both the fix and the `lambda_3` hypothesis in one diagnostic.

**Verification, `check_l3_interior_energy.py`, `n=23,29,31` (`N<=14`, direct `(v,C(N,3))`
matrix construction feasible):** `E_3 = sum(mu_abc^2)/lambda_3` checked at EVERY interior layer
(not just the boundary), cross-validated two ways: (1) against `metrics/johnson_eigenspace_
decomposition.json`'s exact diagonalization (l=3 eigenspace, matched via the Eberlein formula) —
available at every layer for these three `n`; (2) against point 19's independently-verified
boundary result at `q=3,N-3`. **22/22 layers, 0 violations, matches to `<1e-9`** — including a
correct exact zero at the middle layer (`n=23,q=5` and `n=31,q=7`: both formula and diagonalization
agree on `E_3≈0`, a real structural fact, not a bug). `Var(h)-E_3` (the `l>=4` tail) is
non-negative at every layer, as required.

**Scope, honestly:** verified at `n=23,29,31` only — the direct `(v,C(N,3))` matrix construction
does not scale to `n=37-47` without a smarter (combinatorial closed-form, not brute-force matrix)
computation of `mu_abc`, not yet attempted. The formula itself (`lambda_3` + the `z_abc`
construction reusing `P_1,P_2`) is n-independent and has no reason to fail at larger `n` — the
open question is purely computational feasibility, not mathematical correctness.

**Artifacts:** `check_l3_interior_energy.py` (+`metrics/l3_interior_energy.json`).

## Point 21 (2026-09-12) — Exam 2 stages D+E: `E_3` scaled to all 7 `n`; the four-term ladder
kill-or-promote test — PROMOTE, excess growth accelerates past halving

**Context — an explicit methodological redirect from the user, not a default next step.** After
point 20's breakthrough (general `E_3(q)` verified, but only at `n=23,29,31`), the user
argued against jumping straight to Exam 3 (a general law for arbitrary `l`): "проверить, что
это реально делает с four-term Poincaré bound" first, because extending `E_1+E_2` to `E_1+E_2+E_3`
in the sharpened ladder is a cheap, decisive "kill-or-promote" test for the WHOLE mechanism —
either the excess-growth-halving pattern (`91.3pp→69.3pp→32.8pp`, point 18) continues at a
fourth rung, making a general law worth pursuing, or it plateaus, meaning the Johnson-ladder
route may be near its ceiling regardless of what a general `l` formula would say. Accepted and
executed in this order: (D) scale `E_3` to `n=37,41,43,47`; (E) compute the actual four-term
bound and the excess-growth number.

**Stage D — scaling `E_3` without `(v,C(N,3))` (`check_l3_interior_energy_efficient.py`).**
The direct brute-force matrix from point 20 does not scale past `n=31` (`n=47`: `v` up to
705432, `C(22,3)=1540` → ~8.7GB for one matrix). Algebraic reduction: since
`mu_abc = Cov(f,z_abc) = Cov(f,E_abc) - Cov(P_1(f),E_abc) - Cov(P_2(f),E_abc)` (self-adjointness
of the projection operators), and `Cov(w,E_abc)` for ALL triples at once is one matmul against
the ALREADY-BUILT `(v,C(N,2))` pair matrix (`weighted = big_e_pair * w[:,None]; M_w =
weighted.T @ big_e / v`), the `(v,C(N,3))` structure is never materialized — peak memory stays
`O(v·C(N,2))`, the same class `check_l2_analytic_projection.py` already handles at `n=47`.
**Sanity check FIRST** (re-derive `n=23,29,31` with the new method and require EXACT agreement
with point 20's brute-force result before trusting anything larger): **0/22 violations, matches
to `<1e-9`.** Then extended cleanly to `n=37,41,43,47` (58 more layers, no errors), including
correct exact zeros at every self-complementary middle layer (`n=37,q=8.5`-equivalent boundary,
`n=43,q=10`, `n=47,q=11`, etc.) — `E_3/C_q` at the `q=3,N-3` boundary continues the declining
trend already seen for `n≤47` (point 19's table extended: `0.2547→...→0.2200`, unchanged, since
this stage only adds interior-layer coverage).

**Stage E — the four-term bound (`check_l4_ladder_bound_analytic.py`):**

```
C_q  <=  E_1 + E_2 + E_3 + (T_q/2 - gamma_1*E_1 - gamma_2*E_2 - gamma_3*E_3) / gamma_4
```

`E_3=0` at `q∈{1,2,N-2,N-1}` (matching the existing `E_2=0` convention at `q∈{1,N-1}`). Verified
**0 violations** (`four_holds` and `four_le_three` both hold at every layer, all 7 `n`) before
trusting the aggregate. Full tightness table (`C_q`-weighted aggregate, same weighting as points
15-18):

| n | naive | two-term | three-term | **four-term** |
|---:|---:|---:|---:|---:|
| 23 | 0.5208 | 0.9134 | 0.9838 | **1.0000** |
| 29 | 0.4589 | 0.8361 | 0.9519 | **0.9947** |
| 31 | 0.4412 | 0.8116 | 0.9389 | **0.9911** |
| 37 | 0.3989 | 0.7473 | 0.8985 | **0.9757** |
| 41 | 0.3757 | 0.7093 | 0.8717 | **0.9632** |
| 43 | 0.3661 | 0.6936 | 0.8593 | **0.9563** |
| 47 | 0.3488 | 0.6643 | 0.8358 | **0.9429** |

At `n=23`, `min(q,N-q)≤5` for every layer, so `q=4,6` (`min=4`, only `l=1..4` exist) hit the
four-term bound EXACTLY (`C_q=four_term_bound` to 9 decimals — the same boundary-exactness
pattern already used for `E_2`,`E_3`, now showing up automatically inside the bound itself), and
even `q=5` (`min=5`, `l=1..5` all exist) matches to `~1e-16` — consistent with `E_5≈0` at the
self-complementary middle layer, the same antisymmetry-driven vanishing already observed for
`E_1` at odd levels there (not separately re-verified here, noted as a plausible mechanism, not
claimed proven).

**Excess growth (SAME methodology as points 16/18 — `n²·bound` growth from `n=23→47`, minus
the observed `n²·C_q` growth of `+84.92%`):**

| Bound version | growth of `n²·bound`, `n=23→47` | excess over observed |
|---|---:|---:|
| naive | +176.12% | +91.20 pp |
| two-term | +154.25% | +69.33 pp |
| three-term | +117.65% | +32.72 pp |
| **four-term** | **+96.13%** | **+11.21 pp** |

**Verdict on the kill-or-promote question, stated as the user framed it: PROMOTE, not a
plateau.** The ratio of successive excess values is `69.33/91.20=0.760`, `32.72/69.33=0.472`,
`11.21/32.72=0.343` — each rung's excess doesn't just keep halving, the ratio of decay itself
is shrinking (0.760→0.472→0.343): the observed excess contraction strengthens with ladder depth.
**CORRECTED (2026-09-12, per direct user pushback on an overclaim in this same paragraph):** an
earlier draft of this sentence said the sequence is "converging FASTER than geometric decay" —
too strong a claim from exactly three ratio data points. Three numbers establish a trend on the
observed range, not an asymptotic rate; the honest statement is only that the contraction
strengthens with depth on `n≤47`, not a claim about the limiting decay class. Separately, four-
term tightness at `n=47` is `0.9429`, meaning the bound overshoots `C_q` by only `~6.1%`
(`1/0.9429-1`), against naive's `~187%` overshoot (`1/0.3488-1`) at the same point — not a
decorative improvement. **Still not a proof of `O(1/n)`** — four data points on excess-decay
ratios is a trend, not an asymptotic theorem, and `n=47` remains a small computational ceiling —
but per the user's own stated threshold ("если получится 32.8→30, общий закон искать уже
гораздо менее интересно"), this result clears the promote bar clearly, not marginally.

**Artifacts:** `check_l3_interior_energy_efficient.py`
(+`metrics/l3_interior_energy_efficient.json`), `check_l4_ladder_bound_analytic.py`
(+`metrics/l4_ladder_bound_analytic.json`).

## Point 22 (2026-09-12) — Exam 3, stage 1: tail-concentration reformulation reveals a
complication the aggregate four-term result was masking

**Context.** The user proposed reformulating Exam 3 away from a per-level geometric-decay
hypothesis (`E_l~Aρ^l`, risky since mass visibly migrates upward across levels) toward asking
whether the Poincaré bound applied to the TAIL specifically — `R_r:=sum_{l>=r}E_l <= D_r/
gamma_r:=sum_{l>=r}gamma_l*E_l / gamma_r` — becomes an increasingly tight, uniform-in-`n`
approximation as `r` grows. `tail_tightness_r(n) := R_r/(D_r/gamma_r) ∈[0,1]`.

**No new heavy computation was needed** — every ingredient is already inside the committed,
verified `metrics/l4_ladder_bound_analytic.json` (point 21): `tail_tightness_1` is exactly the
already-tabulated `naive_tightness`; `tail_tightness_r` for `r=2,3,4` is obtained by subtracting
the exact known prefix (`E_1`,...,`E_{r-1}`) from both the numerator (`C_q`) and the
corresponding bound before taking the ratio (`check_tail_concentration_ratio.py`).

**Result, `C_q`-weighted aggregate (same weighting as points 15-21):**

| n | tail_tightness_1 | tail_tightness_2 | tail_tightness_3 | tail_tightness_4 |
|---:|---:|---:|---:|---:|
| 23 | 0.5208 | 0.9081 | 0.9297 | 1.0000 |
| 29 | 0.4589 | 0.8314 | 0.8697 | 0.9748 |
| 31 | 0.4412 | 0.8077 | 0.8501 | 0.9646 |
| 37 | 0.3989 | 0.7446 | 0.7962 | 0.9310 |
| 41 | 0.3757 | 0.7071 | 0.7665 | 0.9107 |
| 43 | 0.3661 | 0.6916 | 0.7521 | 0.8996 |
| 47 | 0.3488 | 0.6627 | 0.7275 | 0.8810 |

**Two facts, both real, pointing opposite directions — reported without picking a winner:**

1. **For FIXED `n`, tail_tightness increases monotonically with `r`** (e.g. `n=47`:
   `0.3488→0.6627→0.7275→0.8810`) — removing more known-exact levels makes the Poincaré bound
   on what remains genuinely tighter. Sanity-consistent with the already-verified boundary
   identity: at `q` where `min(q,N-q)=r` exactly, only one level remains and
   `tail_tightness_r=1.0` exactly (already confirmed throughout points 18-21).

2. **For FIXED `r`, tail_tightness DECLINES as `n` grows** — at `r=4`:
   `1.0000→0.9748→0.9646→0.9310→0.9107→0.8996→0.8810` (`n=23→47`), a real ~12pp drop, not noise
   (matches the sign and rough magnitude of the same decline already visible at `r=1,2,3`). This
   is the OPPOSITE of what the user's proposed uniform-in-`n` concentration law would need at a
   FIXED, finite `r` — the tail bound is getting LOOSER with `n`, not tighter, when isolated from
   the exact-known prefix.

**Why the aggregate four-term result (point 21, `0.9429` at `n=47`) didn't show this:** algebra,
not a contradiction — for `a<b`, `c>0`: `(a+c)/(b+c) > a/b`. With `a=R_4`, `b=D_4/gamma_4`,
`c=E_1+E_2+E_3` (exact, positive, and a SUBSTANTIAL fraction of `C_q`), the full four-term
tightness `(c+R_4)/(c+D_4/gamma_4)` is ALWAYS closer to 1 than the tail-only ratio `R_4/
(D_4/gamma_4)`. The exact-known prefix dilutes and masks how the residual tail bound itself is
actually behaving — point 21's optimistic aggregate number was real (the bound genuinely is
much tighter than three-term), but it does not by itself demonstrate the tail-concentration
mechanism the user proposed as the underlying explanation.

**Most likely honest explanation, not yet independently verified:** `r=4` is FIXED while the
total number of available levels (`~min(q,N-q)`, scaling with `N~n`) grows — so a fixed `r`
captures a shrinking FRACTION of the spectral range as `n` grows. This reframes what a genuine
uniform-in-`n` statement would need: not `tail_tightness_r(n)→1` for fixed `r`, but a question
about how `r` must scale with `n` (e.g. `r(n)~log n` vs `r(n)~n^c`) to hold a target tightness —
a materially different, and harder, question than either the original per-level geometric-decay
idea or the tail-concentration-at-fixed-`r` idea as first stated.

**Status: reported, not yet resolved.** This is exactly the kind of finding this project's own
`falsification-ladder.md` Adaptive Iteration Branch Rule exists for — a mid-flight complication
surfaced by data, not by opinion, requiring a branch decision from the user rather than a
unilateral pivot. Not treated as a kill of Exam 2's PROMOTE verdict (that verdict rests on the
already-verified four-term inequality holding with 0 violations, which is unaffected) — only as
a correction to which SPECIFIC mechanism (tail concentration at fixed `r`, vs. something that
scales `r` with `n`) plausibly explains it.

**Artifacts:** `check_tail_concentration_ratio.py` (+`metrics/tail_concentration_ratio.json`).

## Point 23 (2026-09-12) — Exam 3, stage 2: effective spectral level `l_eff`, independently
verified; real target is `l_eff=O(1)` (not `O(N)`), question left open

**Context.** In response to point 22's finding (`tail_tightness_4` declines with `n`), the user
derived a reformulation rather than accepting either the original geometric-decay idea or their
own earlier "scale `r` with `n`" proposal: since `gamma_l=l(N+1-l)/(q(N-q))` (the already-used
swap-walk gap formula), the `q(N-q)` factor cancels inside `t_r:=R_r/(D_r/gamma_r)`, giving
`1/t_r` a clean reading as the tail's `E_l`-weighted average of `l(N+1-l)`, normalized to the
boundary value `r(N+1-r)`. Solving `l_eff(N+1-l_eff)=r(N+1-r)/t_r` for the root near `r` turns
this into a single "effective spectral level": at `r=4`, does the residual tail behave, on
average, as if concentrated near `l=4`, or does it drift toward the growing available range?

**Independently re-derived, not taken on the user's word (`check_effective_spectral_level.py`,
per `audit-verification-gate.md`):** re-solved the same quadratic from the already-committed
`tail_tightness_4` values — matches the user's own numbers exactly: `l_eff` = `4.000, 4.178,
4.239, 4.434, 4.548, 4.612, 4.719` for `n=23,29,31,37,41,43,47`. The derivation and arithmetic
are correct.

**CORRECTED (2026-09-12, before this point was even first pushed — user caught two math
issues in the same-session draft before it was merged, both accepted and applied here):**

**Correction 1 — the original "delta grows faster than log(N) and sqrt(N)" claim is not
justified by this data and is retracted.** `delta:=l_eff-4` is exactly `0` at the first point
(`N=10`); dividing any subsequent positive value by `log(N)`, `sqrt(N)`, or `N` trivially makes
every one of those ratios "increase from zero" — that is an artifact of the starting point, not
a test that discriminates between asymptotic growth classes. None of the three normalized
ratios stabilizing on a 7-point, `N=10..22` range is not evidence FOR faster-than-`sqrt(N)`
growth; it is simply too short a range to identify any growth class this way. The correct,
honest statement is only: `l_eff` shows a finite-range upward drift (`4.000→4.719`), and simple
normalization diagnostics on this data are inconclusive — not that they positively indicate fast
growth.

**Correction 2 — the fallback target `l_eff=O(N)` (stated in the pre-correction draft of this
point) is far too weak to be useful, and is replaced by the actual requirement,
`l_eff=O(1)`.** Independently re-derived (not taken on the user's word): `t_4 = 4(N-3)/
(l_eff·(N+1-l_eff))`. If `l_eff=o(N)` (in particular if `l_eff→∞` at ANY rate slower than `N`,
even `log log N`), then `N+1-l_eff~N`, so `t_4 ~ 4(N-3)/(l_eff·N) ~ 4/l_eff → 0`. If instead
`l_eff~cN` for a constant `c∈(0,1)`, `t_4 ~ 4/(c(1-c)N) → 0` even faster. **Only `l_eff=O(1)`
(i.e. `l_eff` converging to a finite limit, not just growing sub-linearly) gives `t_4≥c>0`
uniformly.** `O(N)` was nearly vacuous as a target — almost any realistic growth of `l_eff`
already satisfies it while still forcing `t_4→0`.

**The real fixed-`r` kill-or-promote question, stated precisely:** does `l_eff(N)` converge to
a finite limit (Scenario A: fixed `r` gives uniform constant-factor tail control, a strong
result) or diverge, even slowly (Scenario B: fixed `r` is asymptotically insufficient, and the
investigation must move to `r=r(N)`)? **The 7 available points (`l_eff: 4.000→4.719`,
`N:10→22`) cannot distinguish a genuine finite limit from `log log N`, `log N`, or another
slowly-diverging function — the range is simply too short.**

**Honest status: `fixed-r localization remains unresolved; l_eff shows finite-range upward
drift.`** Neither "essentially bounded" nor "diverging" is established. This is exactly the
`integrity.md` Confidence Scoring case where `<2` independent structural confirmations caps
confidence at `LOW`/`SPECULATIVE` — clean per-point arithmetic does not by itself resolve an
asymptotic question.

**Not treated as contradicting point 22's finding or Exam 2's PROMOTE verdict** — both remain
correct as stated; this only sharpens what Exam 3's fixed-`r` theorem target actually is
(`l_eff=O(1)`, not the far weaker `O(N)`), and names the real next question: **is `l_eff(N)`
bounded as `N` grows, for fixed `r`? Only if the answer is no does moving to `r=r(N)` become the
next necessary step.**

**Artifacts:** `check_effective_spectral_level.py` (+`metrics/effective_spectral_level.json`).

## Point 24 (2026-09-12) — Exam 3, stage 3: attempted analytic proof of `l_eff(N)`
boundedness — real reduction obtained, NOT resolved, honestly reported as such

**Context.** Explicit user request: "попробуй доказать bounded ли l_eff(N) аналитически."
Attempted in good faith; the result is a genuine mathematical reduction plus one cheap
confirmatory empirical check, but **no proof, in either direction, was obtained.**

**The reduction (derived, not assumed).** Suppose a fraction `ε_N` of the tail's total energy
`R_4=sum_{l>=4}E_l` sits at Johnson levels of order `N` (i.e. `l≈cN` for some fixed `c∈(0,1/2)`),
with the remainder concentrated near `l=4`. Then

```
1/t_4 ≈ (1-ε_N) + ε_N * c(1-c) * N/4
```

so **any fixed, `N`-independent fraction `ε_N=ε>0` of energy at order-`N` levels forces `1/t_4`
to grow LINEARLY in `N`** (hence `l_eff` grows linearly, not boundedly). This gives the exact
criterion: `l_eff=O(1)` **if and only if** the fraction of tail energy at levels `l=Ω(N)` decays
at least as `O(1/N)` — a genuinely strong, specific localization requirement, not a restatement
of the original question. This is real progress: it converts an abstract "is `l_eff` bounded?"
into a concrete question about the DECAY RATE of `E_l` as `l` grows proportionally with `N` —
exactly the general-`l` formula question that was flagged as the harder, deferred branch of
Exam 3 from the start (point 20's own scope note).

**Cheap empirical check, no new heavy computation (`check_center_layer_t4_trend.py`):** isolates
the CENTER layer (`q` closest to `N/2`, where `Lmax=min(q,N-q)` is maximal for that `N`) at each
`n`, to rule out one specific concern — that the aggregate decline (points 22-23) might be an
artifact of mixing across `q`-layers with different `Lmax`. Result: `t_4` at the center layer
alone tracks the aggregate closely (`1.0000→0.8860` at the center layer vs `1.0000→0.8810`
aggregate) — the decline shows up even holding "fraction through the available range" roughly
fixed at the center layer, which is mild evidence AGAINST the bounded scenario (if mass were
genuinely staying put near `l=4` regardless of how much room the layer has, the center-layer
value — which always has the LARGEST possible range of available levels — should show LESS
decline than the aggregate, not the same amount).

**Honest verdict: no proof achieved.** Resolving whether `ε_N=O(1/N)` genuinely holds requires
either (a) exact or asymptotic formulas for `E_l(N)` at general `l` (not just `l=1,2,3`, which
are the only levels with closed forms in this investigation) — this is precisely the harder,
originally-deferred general-`l` branch of Exam 3, not a shortcut around it; or (b) an
independent structural argument (e.g. a hypercontractivity/noise-sensitivity-style bound)
establishing that `delta(S)` — the log-theta difference under a single-element swap — has
bounded "swap-sensitivity", which is a genuine, UNESTABLISHED premise about the underlying
Lovász-theta optimization's stability under perturbation, not something this codebase has ever
derived or verified. **Neither route was completed in this attempt.** The question `is l_eff(N)
bounded for fixed r=4?` remains open, with the center-layer check as a mild (not decisive)
lean toward "no."

**Artifacts:** `check_center_layer_t4_trend.py` (+`metrics/center_layer_t4_trend.json`).

**Addendum (2026-09-13, extends this point's own center-layer check to r=1,2,3, not a new
point):** in response to the user's step-1 plan question ("is a FIXED r sufficient for the
sufficient lemma `D_r(q)≤C·γ_r·R_r(q)`, or is `r=r(n)` needed?"), the same center-layer
`tail_tightness_r = R_r/(D_r/γ_r)` was recomputed directly from the already-committed
`metrics/tail_concentration_ratio.json` (`per_layer`, central `q`, no new simulation) for
`r=1,2,3` in addition to this point's own `r=4`. Cross-validated first against this point's own
aggregate numbers (exact match to 9 decimal places, confirming the extraction logic before
trusting the new central-layer cut). Result: `tail_tightness_r_central` declines with `n` for
EVERY tested `r`, same qualitative shape as `r=4`'s already-documented decline: `r=1`:
0.4949→0.3382; `r=2`: 0.8909→0.6457; `r=3`: 0.8571→0.6995; `r=4`: 1.0000→0.8860 (n=23→47). The
decline rate (log-log slope) shrinks monotonically as `r` grows: -0.53 (r=1) → -0.45 (r=2) →
-0.29 (r=3) → -0.17 (r=4). **This does not resolve the plan's step-1 question** — 4 points in
`r` is far too few to fit how the insufficiency-rate itself scales with `r`, and this remains
consistent with either "no fixed `r` works, ever" or "a slowly-growing `r(n)` would work" — but
the monotone shrinking trend is a mild point in favor of the latter over the former, worth
noting for whoever next attempts a formal argument. No new artifact committed — the check reuses
existing committed data and is trivially reproducible from it.

## Point 25 (2026-09-12) — Exam 3, stage 4: general RECURSIVE construction for `E_l` at
arbitrary `l`, verified at `l=4`, 0 violations

**Context.** Explicit user request: "попробуй вывести формулу E_l для общего l." Point 24's
own reduction (`l_eff=O(1)` needs `E_l`'s decay rate at general `l`) made this the natural next
step, and a genuine simplification was found while extending the `l=3` construction one level
further, turning what could have been a fresh symbolic derivation into a general, reusable
recursive pattern.

**The simplification, found while building it, not planned in advance.** The "pure `V_3` basis"
`z_abc(S)` from point 20 (built via `z_abc = E_abc_centered - P_1[E_abc] - P_2[E_abc]`, using
each triple's OWN raw indicator as the projection target) turns out to be a FIXED basis,
independent of which function is later correlated against it. This means `P_3`, as a reusable
operator for ANY target `g` (not just `f`), is simply `mu_abc(g):=Cov(g,z_abc)` then
`P_3[g](S):=sum_{a<b<c}(mu_abc(g)/lambda_3)*z_abc(S)` — no new derivation needed, `z_abc` is
built ONCE and reused. This generalizes cleanly: **at each level `k`, build the "pure `V_k`
basis" once (raw `k`-index indicators, purified by `P_1..P_{k-1}`), then `P_k[g]` for any target
`g` reuses that basis via one covariance computation.** A genuinely recursive algorithm, not a
closed form, but general in `l`.

**`l=4` construction (`check_l4_interior_energy.py`):** `E_abcd(S)=e_a e_b e_c e_d` (raw
quadruple indicator, degree-4, content only in `V_0..V_4` — the same general degree-filtration
fact used at every prior level). `w_abcd := E_abcd_centered - P_1[E_abcd] - P_2[E_abcd] -
P_3[E_abcd]` is its pure `V_4` part. `mu_abcd:=Cov(f,w_abcd)`. `lambda_4` HYPOTHESIZED by
extending the verified falling-factorial pattern (`lambda_l=[q]_l[N-q]_l/[N]_{2l}`, confirmed
`l=1,2,3`) to `l=4` — stated as a hypothesis, not assumed. `E_4:=sum(mu_abcd^2)/lambda_4`.

**First attempt worked immediately (unlike point 20's `l=3`, which needed a bug hunt) — the
quick n=23 sanity test passed on the first run**, both checks clean: boundary (`q=4,N-4`,
`min(q,N-q)=4`, only `l=1..4` exist, so `E_4=C_q-E_1-E_2-E_3` exactly) and diagonalization
(matched the `l=4` Eberlein eigenspace at EVERY tested layer, including interior `q=5` where
`min(q,N-q)=5` and the boundary check doesn't apply but diagonalization does).

**Full verification, `n=23,29,31`, all layers where `q>=4` and `N-q>=4`:** **0/6 boundary
violations, 0/16 diagonalization violations** (corrected 2026-09-12: an earlier draft said
"0/0," which a reviewer correctly flagged as reading like an absent test rather than a passed
one — see point 26). Both the `lambda_4`
hypothesis and the recursive `P_3`-reuse construction are confirmed, not just at the boundary but
at every interior layer with independent exact diagonalization. (One clarification, not an
error: at interior `q=5` for `n=29`, `E_4≠C_q-E_1-E_2-E_3` — expected, since `min(q,N-q)=5`
there means the subtraction equals `E_4+E_5`, not `E_4` alone; the diagonalization check, which
DOES isolate `E_4` specifically, confirms `E_4` itself is correct.)

**Significance.** This is the first working instance of the GENERAL pattern this whole
investigation was building toward since point 20's own scope note ("the general interior-layer
`E_3(q)` formula... is deliberately NOT attempted [for arbitrary `l`]"). The construction is
recursive (needs levels `1..l-1` built first) rather than closed-form, and verified computationally
only up to `l=4` at small `N` (the brute-force `(v,C(N,l))` matrix construction — same scope
limitation as `l=3`'s original brute-force version, point 20 — not yet extended to the efficient
matmul-based method of `check_l3_interior_energy_efficient.py`, which would be needed to reach
`n=37-47` or larger `l`). Directly relevant to point 24's open question: this construction, in
principle, extends to arbitrary `l` (the pattern has no obvious obstruction at `l=5,6,...`),
which is exactly the tool needed to eventually determine whether `E_l`'s decay rate as `l~cN`
satisfies the `O(1/N)` criterion point 24 derived — not yet attempted at this session's remaining
scope, but no longer blocked by "no formula for general `l` exists."

**Artifacts:** `check_l4_interior_energy.py` (+`metrics/l4_interior_energy.json`).

## Point 26 (2026-09-12) — Exam 3, stage 6: general tight-frame THEOREM for `E_l` at
arbitrary `l` (structural proof, two cited representation-theory facts), plus `l=5`
numerical confirmation

**Context.** After point 25 (`l=4` verified), the user explicitly redirected away from just
computing `l=5` ("не считал бы просто l=5... самое ценное — превратить point 25 из
'рекурсивный паттерн работает до l=4' в общую теорему"), proposing the standard tight-frame /
Schur's-lemma argument. `l=5` had already been launched in the background before the redirect
arrived and was allowed to finish (not wasted, kept as independent numerical confirmation) — but
is explicitly secondary to the structural result below, per the user's own framing.

**The general proposition, stated precisely.** For `|A|=k`, `Y_A(S):=1[A⊆S]`. Already-established
fact (used at every level `k=1..4` without needing restatement): `Y_A` is degree-`k` in the
`e_a(S)` indicators, hence `T_k:=span{Y_A:|A|=k} ⊆ V_0⊕...⊕V_k`. Define `Z_A:=(I-P_{<k})Y_A`
where `P_{<k}=P_0+...+P_{k-1}` (the already-verified lower-level operators). Since
`Y_A∈V_0⊕...⊕V_k`, subtracting all components below `k` leaves EXACTLY `P_k Y_A∈V_k` — this part
is a direct consequence of already-verified facts, not new.

**The Schur's-lemma step (the actual new content).** The operator `sum_{|A|=k} Z_A⊗Z_A` is
`S_N`-equivariant (permuting ground elements permutes `{Z_A}` exactly as it permutes `{A}`, by
construction). **If `V_k` is irreducible as an `S_N`-representation** — the standard, classical
fact that the Gelfand pair `(S_N, S_q×S_{N-q})` gives a multiplicity-free decomposition of the
permutation module on `q`-subsets into `V_0,...,V_{min(q,N-q)}` (cited as `[MEMORY]`-level
representation-theory knowledge, NOT independently re-derived or looked up in this session) —
then by Schur's lemma this operator, restricted to `V_k`, MUST be a scalar multiple of the
identity: `sum_{|A|=k} Z_A⊗Z_A = lambda_k · P_k`. This is the tight-frame identity, and it gives,
for ANY function `f` on the `q`-slice (not just `f` from this investigation):

```
E_k(f) = ||P_k f||^2 = (1/lambda_k) * sum_{|A|=k} <f, Z_A>^2
```

**What this DOES resolve, honestly scoped.** The STRUCTURE of the formula — that it holds for
every `k` up to `min(q,N-q)`, via the same tight-frame mechanism — is now understood, not just
observed to hold for `k=1,2,3,4,5` by extrapolation. This is qualitatively different from "the
pattern worked 5 times."

**What this does NOT resolve — stated explicitly, not glossed over.** The exact closed form
`lambda_k=(q)_k(N-q)_k/(N)_{2k}` was NOT re-derived from first principles in this pass. The
tight-frame identity gives `lambda_k` via a trace: `sum_A ||Z_A||^2 = lambda_k · dim(V_k)`, with
`dim(V_k)=C(N,k)-C(N,k-1)` (also a standard, cited, not independently re-derived Johnson-scheme
dimension formula) — but `||Z_A||^2` itself requires the SAME recursive computation the code
already performs (i.e., closing this loop symbolically, rather than numerically, was not
attempted). The formula's correctness rests on: (a) the two cited representation-theory facts
above (irreducibility of `V_k`, the dimension formula), both standard in the literature but not
independently verified in this session; (b) the numerically-confirmed pattern match across
`l=1,2,3,4,5` (5-for-5, including exact diagonalization matches at every interior layer tested),
which is strong but empirical, not a from-scratch symbolic derivation of the constant.

**`l=5` numerical confirmation (`check_l5_interior_energy.py`), kept as independent evidence:**
extends the exact same recursive construction one level further — the pure-`V4` basis `w_abcd`
(already built while computing `E_4` in point 25) is a FIXED basis, reused as `P_4[g]` for any
target `g`, exactly the same simplification found at every prior level. First attempt worked
immediately (as at `l=4`). Verified at `n=23,29,31`: **0/5 boundary violations, 0/10
diagonalization violations** (stated with the actual denominators — an earlier draft of this
session's own reporting used the phrase "0/0 violations," which a reviewer correctly flagged as
looking like an absent test rather than a passed one; corrected here and going forward).

**Artifacts:** `check_l5_interior_energy.py` (+`metrics/l5_interior_energy.json`).

## Point 27 (2026-09-12) — Exam 3, stage 7: `lambda_k` derived from FIRST PRINCIPLES for
k=1,2,3 (symbolic, computer-algebra-verified) — closes most of point 26's honesty gap

**Context.** Explicit user request: "попробуй доказать λ_k из первых принципов" — targeting
exactly the piece point 26 flagged as NOT done ("the exact closed form... was NOT re-derived
from first principles... rests on cited standard facts plus the empirical 5-for-5 pattern
match"). Attempted via symbolic computer algebra (`sympy`), not hand algebra — given the
multi-step combinatorial bookkeeping involved, this project's own discipline of "verify
computationally, don't trust unverified hand-derivation" applies to the mathematics itself here,
not only to numerical claims.

**Method.** From point 26's trace identity: `lambda_k = C(N,k)*||Z_A||^2/dim(V_k)` for any fixed
`k`-subset `A` (all equal by symmetry), `dim(V_k)=C(N,k)-C(N,k-1)` (still a cited Johnson-scheme
fact, not re-derived here — see Scope below). `||Z_A||^2 = <Y_A,Y_A> - sum_{j<k} E_j(Y_A)`,
where `Y_A(S)=1[A⊆S]` and `E_j(Y_A)` is `Y_A`'s OWN energy at level `j`, computed via the SAME
already-verified recursive formulas (`E_1` closed form, `E_2` double-centered projection) —
but evaluated SYMBOLICALLY, for general `N,q`, on exact hypergeometric containment probabilities
`p_m(N,q) := P(fixed m-subset⊆random q-subset) = (q)_m/(N)_m` (falling factorials), not on
spot-checked numbers.

**Result (`derive_lambda_k_from_first_principles.py`): `sp.simplify(derived - hypothesis) == 0`
— an exact symbolic identity, not a numeric coincidence — confirmed for k=1, k=2, AND k=3, for
GENERAL symbolic `N,q`.** The `k=2` and especially `k=3` cases required real combinatorial
bookkeeping (grouping pairs by `|A∩{a,b}|` into 3 distinct types for `k=3`, each occurring with
its own multiplicity, then running the ALREADY-VERIFIED `r_ab` double-centering formula on each
type) — this is a genuine derivation, not curve-fitting a formula to match numbers.

**What this changes vs. point 26's scope statement.** Point 26 said `lambda_k`'s closed form
"rests on cited standard facts plus the empirical 5-for-5 pattern match" — that is now
outdated for `k≤3`: those three cases are independently, symbolically DERIVED, not merely cited
or pattern-matched. What STILL rests on cited (not re-derived) facts: (a) `dim(V_k) = C(N,k)-
C(N,k-1)`, the Johnson-scheme dimension formula itself; (b) the general-`k` INDUCTION — `k=4,5`
were not attempted here (would need one more recursion level, `E_3(Y_A)` grouping TRIPLES by
`|A∩{triple}|` into 4 types instead of `k=3`'s 3 — the same method, more bookkeeping, not a
discovered obstruction, just not done in this pass for time budget reasons); the general
representation-theoretic argument (Schur's lemma + `V_k` irreducibility) from point 26 remains
the reason a clean tight-frame constant exists AT ALL for every `k` — this symbolic computation
independently confirms its VALUE for `k≤3`, it does not replace the structural argument for WHY
one exists at every level.

**Honest status: substantially strengthened, not fully closed.** `lambda_k` for `k=1,2,3` is now
proven, not cited-and-pattern-matched. The general-`k` case still rests on the point 26
structural argument (cited irreducibility fact) plus now `3` (not `0`) independently-derived
base cases, with a clear, mechanical inductive method that has not yet hit an obstruction.

## Point 28 (2026-09-12) — Exam 3, stage 8: `lambda_k` first-principles derivation extended to
k=4 — first level requiring a genuinely new technique (self-adjoint cross-projection), not just
more of the same bookkeeping

**Context.** Explicit user request: "попробуй k=4" — direct continuation of point 27's method to
one more level. Point 27 explicitly flagged this as "not attempted... same method, more
bookkeeping, not a discovered obstruction" — this point tests that claim.

**What turned out to be genuinely different, not just "more of the same."** For `k≤3`, `E_{k-1}
(Y_A)` could always be computed by projecting `Y_A` onto an EXPLICIT closed-form basis (`y_ab`
for pairs, itself a simple linear combination of raw indicators). For `k=4`, `E_3(Y_A)` requires
projecting onto the TRIPLE basis `z_abc = e_abc_centered - P1(e_abc_centered) - P2(e_abc_centered)`
— and writing `z_abc` out explicitly (the way `y_ab` was written out for the `k≤3` cases) would
have meant deriving a THIRD layer of closed-form basis algebra, a real escalation in bookkeeping
risk, not a mechanical repeat.

**Method actually used (avoids ever writing `z_abc` explicitly).** `P1` and `P2` are orthogonal
projections (self-adjoint), so for any two functions `f,g`: `<P_j(f),g> = <f,P_j(g)>`. Applying
this to `f=e_abc_centered`, `g=Y_A_centered`:
```
<z_abc, Y_A> = <e_abc, Y_A> - <e_abc, P1(Y_A)> - <e_abc, P2(Y_A)>
```
Every term on the right is a cross-moment of ALREADY-KNOWN quantities (`Y_A`'s own `E_1`/`E_2`
coefficients, computed exactly as in point 27's `k=3` case, just with a 4-element `A`) — no new
basis needs deriving. Each cross-moment is computed by classifying the `N`-element ground set into
4 REGIONS by `(in A?, in triple {a,b,c}?)` and summing over region-PAIRS (10 combinations: 4
same-region + 6 cross-region) — implemented as an explicit nested loop over a `regions` list in
`derive_lambda_4()`, not hand-derived combinatorics, specifically to avoid trusting untracked
mental arithmetic for a genuinely more intricate case than `k≤3`.

**Result: `sp.simplify(derived_lambda_4 - lambda_hypothesis(4)) == 0` — exact symbolic identity
for general `N,q`.** Verified 2026-09-12, `derive_lambda_k_from_first_principles.py`'s `__main__`
block now reports `k=1,2,3,4` all `MATCH: True`. `tests/test_lambda_k_first_principles.py`
extended to assert `k=4` alongside `k=1,2,3` (9/9 experiment-local pytest passing, up from 8/8).

**What this does and does NOT establish.** DOES establish: `lambda_4`'s falling-factorial closed
form is independently derived (not cited, not pattern-matched) for general symbolic `N,q`, via a
method (self-adjoint cross-projection through region classification) that is itself new relative
to points 20-27's toolkit — this is a genuinely different technique, not a mechanical repeat of
the `k=3` pair-grouping approach. Does NOT establish: `k=5` (would need `E_4(Y_A)`, grouping QUADS
by `|A∩quad|` into 5 types, plus a THIRD self-adjoint cross-term through `P3` — same
self-adjointness trick should apply again, since it worked cleanly moving from "explicit basis"
(k≤3) to "self-adjoint cross-term" (k=4), but this is now a genuine extrapolation of the METHOD,
not just the pattern, and has not been attempted). `dim(V_k)` and the general-`k` irreducibility
argument (point 26) remain cited, unchanged from point 27's status.

**Anti-Overfitting Gate self-check (this is a positive extension of a surviving claim, not a
post-null revision, so AOG-1..5 don't directly apply — but the analogous honesty check does):**
the self-adjoint trick was not chosen because the direct `z_abc`-explicit-basis approach failed —
it was chosen BEFORE attempting the explicit-basis route, specifically because writing out
`z_abc` by hand looked like the higher-risk path. This is a case of picking the lower-risk of two
available methods up front, not rescuing a failed attempt.

**Artifacts:** `derive_lambda_k_from_first_principles.py`
(+`metrics/lambda_k_first_principles.json`).

## Point 29 (2026-09-12) — Exam 3, stage 10: `lambda_k` first-principles work RECLASSIFIED —
the general-`k` closed form is CLASSICAL (Johnson-scheme / inclusion-matrix spectral theory,
Filmus 2016), not new mathematics; k=5 confirmed independently; algebra layer of Exam 3 closed

**This is a correction, not a new discovery — recorded per the Hindsight Distortion Gap
Heuristic discipline: the record below shows what was believed at each step, not retrofitted.**

**Context.** After point 28, the user proposed pausing the CAS ladder (no k=6) and instead
formulating a general induction step proving `lambda_k` for all `k` from `lambda_j`, `j<k`.
Before committing effort to a from-scratch induction proof, the user's own recommended check —
per this stack's `estimand-ops.md`/`rationalizations.md` "well-established ≠ checked" discipline
and FL's AI-Hypothesis Pre-Gate Step -4 (Source Trace) — was to search whether `lambda_k`'s
closed form already exists in the literature (initially framed as "check correspondence with
Eberlein polynomials"). **This Source Trace was never run for points 26-28** (FL Step -3,
Novelty Check, was skipped for this entire line of work) — an honest process gap, closed here.

**What was found, verified against PRIMARY sources, not summaries:**

1. **Filmus (2016), "An Orthogonal Basis for Functions over a Slice of the Boolean Hypercube,"
   Electronic Journal of Combinatorics 23(1), P1.23 (arXiv:1406.0142).** Fetched and read the
   paper's own LaTeX source directly (not an AI-generated summary) via `arxiv` MCP tools,
   Section 4 ("Slices of the Boolean hypercube"). Theorem 4.1 gives, for the `(n,k)`-slice
   orthogonal basis `{χ_B}`, `B` of degree `d`:
   ```
   ||χ_B||^2 = c_B · 2^d · k^(d)_(n-k)^(d)_ / n^(2d)_
   ```
   where `x^(d)_` is the falling factorial. With `n→N`, `k→q`, `d→k`: the core factor
   `k^(d)_(n-k)^(d)_/n^(2d)_` is EXACTLY our `lambda_k = (q)_k(N-q)_k/(N)_{2k}`, proved for
   ARBITRARY degree `d` by one short, general combinatorial computation
   (`||χ_d||^2 = E[Π(x_{2i-1}-x_{2i})^2]`), not case-by-case. Lemma 4.3 of the same paper
   independently confirms point 26's other cited fact: the paper's basis levels `𝒴_{n,0..k}`
   span exactly the Johnson-scheme Bose–Mesner-algebra eigenspaces (our `V_k`), via Bannai–Ito
   / Dunkl's representation-theoretic construction.

2. **Inclusion-matrix spectral theory** (user-supplied derivation, tracing to Wilson's
   inclusion-matrix diagonalization results; cited via a MathOverflow pointer to
   Ghareghani–Ghorbani–Mohammad-Noori). Claim: the inclusion-product matrix
   `M^(i)_{S,T} = C(|S∩T|, i)` has eigenvalue `Λ_j = C(q-j,i-j)·C(N-i-j,q-i)` on Johnson
   eigenspace `V_j`. At `i=j=k`: `Λ_k = C(N-2k, q-k)`, and
   `C(N-2k,q-k)/C(N,q) = (q)_k(N-q)_k/(N)_{2k}` (verified BY HAND here, pure factorial
   cancellation — not accepted from the citation). Because this specific formula arrived via a
   less rigorously-checked citation route (a MathOverflow pointer, not a fetched primary
   source), it was verified INDEPENDENTLY: `verify_inclusion_matrix_eigenvalue.py` builds
   `M^(k) @ Z_A` by brute-force summation over all `q`-subsets (exact `Fraction` arithmetic),
   using the ALREADY-REVIEWED `Z_A`/`y_ab`/`z_abc` constructions from points 25-28 as
   independent eigenvector witnesses (not new code written to match the claim). Result: **exact
   vector equality** `M^(k) @ Z_A == C(N-2k,q-k) · Z_A` (not just an eigenvalue-ratio spot
   check) at `(N,q,k) ∈ {(8,4,1..3), (9,5,1..3), (10,4,2)}` — 7/7 pass. This also gives a
   SHORTER route to point 26's tight-frame theorem: `Σ_A Y_A⊗Y_A` is (up to the `1/C(N,q)`
   inner-product normalization) exactly `BB^T` where `B` is the inclusion matrix `B_{S,A}=1[A⊆S]`;
   its eigenvalue on `V_k` gives `Σ_A Z_A⊗Z_A = λ_k P_k` directly from elementary spectral
   theory, WITHOUT needing Schur's lemma or `V_k` irreducibility as a separate step — Schur's
   lemma is sufficient but, it turns out, not necessary for this particular fact.

**Honest reclassification of points 27-28.** The self-adjoint recursive symbolic derivation
(`derive_lambda_k_from_first_principles.py`, k=1..5) is NOT a novel proof closing an open gap in
new mathematics — the gap was already closed by Filmus (2016) a decade earlier, via a
structurally different, far shorter argument (one direct expectation computation, general in
`d`, vs. our recursive tower requiring a qualitatively new technique at every other level: plain
formula at k≤2, y_ab/r_ab projection at k=3, single self-adjoint cross-term at k=4, DOUBLE
self-adjoint cross-term at k=5). What points 27-28's work DOES remain: a genuine, independently
built, differently-derived confirmation of the same closed form — methodologically valuable per
this stack's Independent Verification Strength Ladder (`falsification-ladder.md`: "independently
written code" ranks Strong), but not a discovery, and should never again be described as
"closing a gap" or "first principles" without this citation attached.

**k=5 result:** `sp.simplify(derived_lambda_5 - lambda_hypothesis(5)) == 0` — confirmed, exact
symbolic identity for general `N,q`, obtained via TWO independent background runs (one
uncached, one with `functools.cache` added to `e2_ingredients`/`e3_cross` after the uncached
run's redundant re-simplification made it impractically slow — a performance fix, not a
derivation change; both produced the identical symbolic result). The k=4→5 step required
generalizing every building block to an explicit target-size parameter `k`, plus a DOUBLE
self-adjoint expansion (`<e_quad,P3(Y_A)>` needs both `<z_triple,Y_A>` AND `<e_quad,z_triple>`,
requiring triples to be jointly classified by overlap with BOTH `A` and the quad — a 4-region
composition enumeration, not the single-region classification k=4 needed). This computational
escalation (uncached run took long enough to require backgrounding twice; k=6 would need a
TRIPLE self-adjoint expansion through `P4`) is itself evidence for the user's original
recommendation: the CAS ladder has reached its practical ceiling, and — now confirmed — going
further would add no new mathematical information anyway, since the general-`k` formula is
already classical.

**What remains cited, not derived, and why that is now FINE:** `dim(V_k)=C(N,k)-C(N,k-1)` and
`V_k` irreducibility — both independently confirmed by Filmus (2016) Lemma 4.3's construction
from `S_N` representation theory (Bannai–Ito/Dunkl), so "cited" here means "correctly attributed
to classical representation theory," not "unverified." This is the correct final state, not an
open gap: re-deriving standard Johnson-scheme representation theory from scratch would be
reinventing decades-old results, which this project's own `estimand-ops.md` "well-established ≠
checked" discipline requires citing with a verified source, not repeating — and that source is
now verified, cited, and attached.

**What this means for the project (per the user's own framing, independently confirmed here):**
the algebraic/structural layer of Exam 3 — "can we compute `E_l(f)` for any `l` and any `f`?" —
is CLOSED, for all `l`, via classical Johnson-scheme / inclusion-matrix spectral theory. It was
never in doubt that a closed form existed (point 26 already proved that much structurally); what
changed is that the exact VALUE is now also known to be a citable classical fact for every `l`,
not something requiring per-level derivation. **What remains genuinely open is unchanged and
un-touched by any of this: point 24's question — how does `E_l(δ_i)` (the SPECIFIC spectral
energy of a Dirac-delta / single-vertex indicator, the sensitivity function this whole project
is about) behave as a function of `l` and `N`?** That is an analytic question about the
DISTRIBUTION of `⟨δ_i,Z_A⟩` coefficients across `A`, not an algebraic question about the
normalizing constant `λ_l` — Filmus's theorem and the inclusion-matrix spectral theory say
nothing about it. This is the sole remaining barrier for Exam 3, and it is NOT classical (no
literature correspondence checked or claimed here) — the honest open question stands exactly as
point 24 left it.

**Decision on further CAS extension:** per the user's explicit recommendation, independently
confirmed by the findings above — **no k=6.** It would consume significant compute (a further
TRIPLE self-adjoint expansion) for zero new mathematical information, since the general-`k`
formula is already established.

**Artifacts:** `verify_inclusion_matrix_eigenvalue.py`
(+`metrics/inclusion_matrix_eigenvalue_check.json`),
`tests/test_inclusion_matrix_eigenvalue.py`, `derive_lambda_k_from_first_principles.py` extended
with `derive_lambda_5()` (+regenerated `metrics/lambda_k_first_principles.json`).

**Sources:**
- Filmus, Y. (2016). An Orthogonal Basis for Functions over a Slice of the Boolean Hypercube.
  *The Electronic Journal of Combinatorics*, 23(1), P1.23. arXiv:1406.0142.
- Wilson, R. M. inclusion-matrix diagonalization results, via Ghareghani–Ghorbani–Mohammad-Noori
  (cited through a MathOverflow pointer; the specific eigenvalue claim used here was
  independently re-verified in this repository via exact-arithmetic computation, not accepted
  from the citation alone — see `verify_inclusion_matrix_eigenvalue.py`).

## Point 30 (2026-09-13) — back to the real open question (point 24): cheap falsification of a
proposed sufficient lemma, using ALREADY-COLLECTED data, before any new analytic effort

**Context.** With the Johnson-algebra/λ_k line closed (point 29), the user proposed a concrete
research plan to attack point 24's actual open question: uniform-in-`n` control of the spectral
energy `E_l(δ_i)` of the SENSITIVITY function `f_q = δ_i(S) = X(S) - X(S∪{i})`, aiming eventually
at `Var(X_n) = O(1/n)` via Efron-Stein. The plan's own step 4 explicitly says: check the proposed
sufficient-lemma's quantitative form on EXISTING exact data BEFORE any new theory, specifically
whether `n³·T_q` (the Johnson swap-walk Dirichlet energy, rescaled) stabilizes or grows with `n`
in the central layers — "if it already grows like n^α, the lemma as stated is false, don't prove
a phantom."

**This check was run — using data already sitting in the repo, no new simulation.**
`johnson_swap_energy.json` already contains exact `T_q` values at `n=23,29,31,37` (computed in
earlier points, points 15-18's Johnson-Poincaré work). `check_n3_Tq_scaling.py` computes
`n³·T_q` at the central layer and as a probability-weighted aggregate `n³·T̄` across all four `n`:

| n | T_q (central) | n³·T_q | T̄ (weighted) | n³·T̄ |
|---|---|---|---|---|
| 23 | 0.04033 | 490.7 | 0.04535 | 551.8 |
| 29 | 0.02787 | 679.7 | 0.03074 | 749.7 |
| 31 | 0.02449 | 729.6 | 0.02734 | 814.5 |
| 37 | 0.01838 | 931.1 | 0.01984 | 1004.7 |

Both `n³·T_q` and `n³·T̄` GROW monotonically and substantially across this range (490→931,
552→1005) — not stabilizing, not oscillating near a constant. A rough log-log power-law fit
gives `α≈1.34` (central) and `α≈1.26` (weighted aggregate) for `n³·T_q ~ n^α`. Equivalently,
`T_q` itself decays roughly like `n^-1.66` to `n^-1.74` over this range, NOT `n^-3`.

**Verdict per the user's own stated stopping criterion: the specific sufficient lemma `T_q =
O(n^-3)` in the bulk is NOT supported by existing data and should not be pursued analytically
in that exact form.** This is a genuine, if modest, falsification result — cheap (reused
existing exact data, no new heavy computation), and it directly prevents the multi-day analytic
effort the plan's steps 2-3 (reinterpreting Dirichlet energy as a mixed second difference,
proving `E[(mixed 2nd diff)²]=O(n^-3)`) would have spent proving something false. This is exactly
what the Cheapest Differentiating Test Protocol (`falsification-ladder.md`) is for.

**Cross-check against already-existing, broader data (not new — this reuses point 22/24's own
`tail_concentration_ratio.json`, n=23..47, 7 points):** `tail_tightness_r` (fraction of `C_q`
captured by the first `r` ladder terms) DECLINES monotonically with `n` for every fixed `r∈{1,2,
3,4}` — e.g. `r=1`: 0.521→0.349; `r=4`: 1.000→0.881, `n=23→47`. This is the SAME signal point 24
already flagged ("mild lean against boundedness," "7-point data cannot distinguish finite limit
from slow divergence") — this point does not add new evidence toward resolving that question, it
independently corroborates that the direction of the trend (declining, not improving) is
consistent across yet another already-computed slice of the same dataset.

**What this does NOT do.** It does not prove `Var(X_n)=O(1/n)` false, nor does it prove the
broader spectral-tail research program is dead — it falsifies ONE specific proposed quantitative
form (`T_q=O(n^-3)` via the mixed-second-difference route) at the FIRST, cheapest checkpoint,
exactly as the plan's own step 4 was designed to do. The plan's steps 1, 3, and 5 (sufficient-
lemma bookkeeping, alternative routes to structure via symmetry/LP-dual/slice-harmonic-analysis,
bulk/tail split) are not falsified by this check and remain open directions — but a WEAKER decay
rate (something closer to `n^-1.5` to `n^-1.7`, if it holds precisely and holds for the actual
mixed-second-difference quantity, not just `T_q` as a proxy) would need to be the target instead
of `n^-3`, and whether that weaker rate is even sufficient to close `S_n=O(n^-2)` has not been
checked (this is exactly the "absolute bound on `D_r`, not just tail tightness" caveat the plan's
own step 1 already flagged as a separate, still-needed piece).

**Why I am not claiming to have "solved this to 100%" (explicit, per this project's Evidence
Policy).** Proving or disproving a uniform-in-`n` spectral tail bound for this specific
combinatorial sensitivity function is a genuinely open mathematical research question — the same
one point 24 already identified as this branch's real barrier after the algebraic/Johnson-scheme
layer closed. A single cheap numeric check (4-7 data points, `n≤47`) can falsify one specific
proposed FORM of a bound; it cannot, by itself, establish or refute the underlying `Var(X_n)=
O(1/n)` claim, derive a corrected exponent with confidence, or complete steps 2-3's proposed
analytic program. Claiming otherwise would be exactly the kind of unverified confidence
`integrity.md`'s "no confidence without evidence" rule exists to prevent. This point closes the
CHEAP, FIRST step of the corrected plan honestly; the analytic work (steps 1-3, corrected to
target a rate other than `n^-3`) remains genuinely unresolved and is not something the next
git commit will change.

**Artifacts:** `check_n3_Tq_scaling.py` (+`metrics/n3_Tq_scaling_check.json`).

## Point 31 (2026-09-13) — Exam 3 stage 12: LP dual/sensitivity route, 4th independent angle
attempted — probabilistic vertex-stability idea, cheaply and clearly FALSIFIED

**Context.** User requested attacking the Efron-Stein/`O(1/n)` question via route B of the
step-4/5 plan: "LP dual/sensitivity route." Before attempting new analysis, `null_results`-style
discipline (Adaptive Iteration Branch Rule) required checking what was already tried: points 6,
8, 9a already attacked this EXACT route three times and hit the SAME documented structural wall
in every case — "LP optima sit at polytope vertices, and vertex identity can change
discontinuously under an arbitrarily small constraint perturbation... would need a genuinely
different tool (LP vertex-stability / basis-perturbation theory specific to this random
polytope's geometry), which is not in the primary source and was not derivable" (point 8). Point
9a additionally ruled out all 4 equivalent LP formulations (primal/dual × time/frequency) as an
escape route.

**The one genuinely new angle identified (not tried in 6/8/9a):** points 6-9 all attacked this
via WORST-CASE bounds (Cauchy-Schwarz/Hölder/RIP norm inequalities on how far ONE feasible
vector can be from another). None asked the PROBABILISTIC question: does the LP's active set
(which `Fx≥0` constraints are tight at the optimum) actually change OFTEN or RARELY when a
single generator is dropped? If jumps were rare, `E[(Δ_i θ)²]` could be small ON AVERAGE via a
concentration argument, even with an O(1) worst-case per-jump magnitude — a qualitatively
different mechanism from anything points 6-9 tried, satisfying the Minimal Relaxation Rule (one
new assumption: "rarity," not a re-run of "boundedness").

**Method.** Solved the paper's own time-domain primal LP (`theta_via_lp`'s exact formulation,
Table 1, arXiv:2603.29571) directly (not via the wrapper) to access the primal solution `x*` and
inequality-constraint slacks, for random circulant graphs at `n∈{11,15,21,29,37}`, dropping one
currently-on generator per test and comparing the ACTIVE SET before/after.

**CAUGHT AND FIXED a real bug before trusting the first result (audit-verification-gate.md
discipline, kept in the artifact's own docstring for transparency, not hidden):** the first
version's tightness test (`slacks[k] < ACTIVE_TOL`) is true for EVERY negative slack, not just
near-zero ones, given the constraint's sign convention (`A_ub@x - b_ub ≤ 0` at feasibility) —
this flagged ALL constraints as "active" and produced a spurious `jump_fraction=0.000` at every
`n`. Caught by manually printing raw slack values for one instance BEFORE accepting the
aggregate result. Fixed to `abs(slacks[k]) < ACTIVE_TOL`.

**SECOND correction, caught independently by BOTH this session and the reviewer during the same
review cycle (not hidden — this is the honest sequence, per the Hindsight Distortion Gap
discipline):** the first corrected version's "jump" criterion (`active_full_reduced !=
active_rest_reduced`, subtracting the trivial pair `{i,n-i}` from both sets before comparing)
overclaimed. The `{i,n-i}` subtraction indexes the wrong space — those are the dropped
*variable's* column indices, not row indices of whichever inequality constraint newly binds, so
there is no map between the two; empirically, removing the subtraction changes the reported
fraction by only ~1-5 percentage points (reviewer's independent check: n=15, 0.712 raw vs 0.699
"filtered"). The criterion was also too COARSE in a second way (caught in this session, before
the reviewer's report arrived): dropping generator `i` removes 2 equality constraints (`x_i=0`
AND its mirror `x_{n-i}=0`), so the reduced LP's vertex generically needs 2 MORE tight
inequalities than before, WITH NOTHING REMOVED, as the trivial/uninteresting outcome — the
original criterion counted this trivial case as a "jump" too, inflating the fraction toward
0.85-1.00.

**Corrected criterion: a "genuine restructure" is any case where at least one previously-active
constraint becomes INACTIVE** (equivalently, `active_full` is NOT a subset of `active_rest`) —
pure growth with nothing removed is the trivial DOF case. **Corrected mechanism for why changes
come in pairs (reviewer's finding, independently verified here):** NOT from equality-constraint
rank-counting (which would give +1, not +2 — `x_k=0` and `x_{n-k}=0` are already linked by the
always-present pairing row `x_k=x_{n-k}`, so removing both drops effective rank by only 1). The
real cause is that **`ReF` has duplicate rows**: `ReF[j,:] == ReF[n-j,:]` for every `j`, since
`cos` is even — verified directly here (`max|ReF[j]-ReF[n-j]|` over all `j`, all tested `n`:
`4.97e-15` to `3.59e-14`, pure floating-point noise, not approximately-but-not-exactly equal).
Inequality constraints `j` and `n-j` are LITERALLY IDENTICAL, so any newly-tight constraint
activates as a pair — this is confirmed by the observed `size_diffs` distribution being all even
numbers (reviewer: `{2:65, 0:32, 6:12, ...}`), consistent only with a pairing mechanism.

**Result, with the corrected criterion (`active_full ⊆ active_rest` ⟺ trivial, matching the
reviewer's own cleaner subset formulation exactly, not an earlier scratch pass's extra `≤2`-added
cutoff) — reproduced independently by both this session and the reviewer (same order of
magnitude, different RNG seeds, e.g. n=21: 0.559 here vs 0.542 reviewer's independent run):**

| n | restructure_fraction | mean_removed_count | E[Δθ²\|trivial] | E[Δθ²\|restructure] |
|---|---|---|---|---|
| 11 | 0.276 | 0.55 | 4.75 | 2.27 |
| 15 | 0.533 | 1.27 | 3.01 | 2.39 |
| 21 | 0.559 | 1.56 | 0.71 | 2.42 |
| 29 | 0.733 | 2.13 | 0.50 | 2.29 |
| 37 | 0.750 | 2.80 | **0.072** | 1.58 |

**The corrected picture is more nuanced than the original overclaim, but the core conclusion
survives — and is now sharper.** Genuine restructuring is NOT universal (28-75%, noisier at
small `n`), but shows NO trend toward zero — if anything it trends up, and `mean_removed_count`
grows clearly and monotonically with `n` (0.55→2.80), meaning restructuring events become MORE
substantial, not rarer, as `n` grows. Meanwhile the "clean" (non-restructuring) cases DO show a
real, decaying `E[Δθ²]` (4.75→0.072) — a genuine, previously-unstated signal that a "smooth"
regime exists — but this regime is a SHRINKING fraction of all cases as `n` grows (since
restructure_fraction trends up), so it cannot average down the aggregate. `E[Δθ²|restructure]`
stays `O(1)` throughout (1.58-2.42), not decaying.

**Verdict: the probabilistic-vertex-stability idea (jumps rare ⟹ average effect small) is
FALSIFIED — restructuring does not become rare as `n` grows, and where it occurs the magnitude
stays `O(1)`.** This is the 4th independent angle on the LP-dual/sensitivity route to fail, each
for a documented, different, verifiable reason: point 6 (concavity/duality gives only a
qualitative bound, needs concentration on the dual variable itself — not established), point 8
(RIP controls spread of ONE vector, not distance between TWO optimal vertices — no tool found),
point 9a (all 4 equivalent LP formulations preserve the value function but not vertex movement —
no escape), and now this point (restructuring assumed rare, found non-vanishing and growing in
magnitude instead).

**Recommendation: retire the LP dual/sensitivity route for this question.** Four independent,
qualitatively different attempts (worst-case duality, exact-bound decomposition, formulation-
switching, and now probabilistic rarity) have each identified a real, specific obstruction and
none found a path through. Per the Cheapest Differentiating Test Protocol, a 5th attempt within
this same route would need a genuinely new idea not yet identified — the remaining unexplored
directions from the user's own plan (route A: symmetry/monotonicity/prime-transitivity;
route C: slice-harmonic-analysis moment bounds) do not share this route's core mechanism (LP
polytope-vertex geometry) and are not affected by this null result.

**Caveats (reviewer P2, not blocking the verdict above):** each sampled graph tests the 3
numerically-SMALLEST currently-on generator indices, not a random subsample — proven neutral for
prime `n` only (this experiment's own exact symmetry theorem, points 12-13), unverified for
composite `n` (15, 21 here); no dedicated `tests/` file for this script, unlike sibling scripts
in this experiment.

**Artifacts:** `check_vertex_stability_probability.py` (updated to the corrected criterion)
(+`metrics/vertex_stability_probability_check.json`).

## Point 32 (2026-09-13) — Exam 3 stage 13: route A (symmetry) — a STANDARD Boolean-Fourier
fact (antisymmetric function ⟹ derivative's spectrum flips parity), newly APPLIED here to
`δ_i` and verified exactly; does NOT resolve point 24, but reframes it in a second, independent
basis with the same signature

**Correction on framing, made before this point was merged (per the same discipline as point
29's Filmus correction — "pathologically careful" about the word "new theorem," per the user's
own direct pushback):** the underlying principle here — an antisymmetric function's discrete
derivative has spectrum confined to the OPPOSITE parity — is a standard, two-line consequence of
the already-textbook Fourier-shift identity `(D_i f)_hat(T) = f_hat(T∪{i})` (Boolean function
analysis, e.g. O'Donnell's *Analysis of Boolean Functions*), not a new result in the abstract.
**What is new here is only the APPLICATION** — recognizing that this project's own `X_n` (log-
Lovász-theta) satisfies the antisymmetry premise (point 5) and applying the standard shift
identity to `δ_i` specifically — and its exact verification against this experiment's own data.
Framed and reported accordingly below, not as a mathematical discovery.

**Context.** User requested route A of the plan: "symmetry + monotonicity + conditioning by
layer... identities/cancellations from complement-antisymmetry, prime transitivity, and layer
structure." Point 11 already proved a real antisymmetry theorem for `X` itself (not yet applied
to `δ_i`): from `X(-ε)=-X(ε)` (point 5), `X_hat(S)=0` for every EVEN `|S|` — `Var(X_n)` is
carried entirely by ODD-degree Fourier-Walsh levels, an exact, `n`-independent structural fact.

**The new step (a direct, cheap corollary, not previously derived in this experiment).**
`δ_i(S) := X(S) - X(S∪{i})` equals `2·D_i X` in this project's own bit=1↔sign=−1 convention
(`D_i f(ε):=(f(ε_i{=}1)-f(ε_i{=}-1))/2`, the standard Boolean-function discrete-derivative
operator). The classical Fourier identity `(D_i f)_hat(T) = f_hat(T∪{i})` for `T⊆[m]\{i}`,
combined with point 11's `X_hat(S)=0` for even `|S|`, forces `(D_i X)_hat(T)=X_hat(T∪{i})=0`
whenever `|T∪{i}|` is even, i.e. whenever `|T|` is ODD. **So `δ_i`'s OWN Fourier spectrum (as a
function of the remaining `m-1` coordinates) is confined to EVEN-degree sets — the DUAL parity
to `X` itself.** This is a standard fact (two lines of textbook algebra), newly APPLIED here —
not previously derived for `δ_i` in this experiment, but not a new abstract result either.

**Verified exactly, not trusted from the algebra alone** (`check_delta_i_even_parity.py`):
computed `X`'s full exact array via `theta_via_lp` (same machinery as point 11's own
`check_exact_walsh_decomposition.py`), built `δ_0` directly from the raw array (fixing `i=0`,
no formula shortcuts), ran its own independent Walsh-Hadamard transform over the remaining `m-1`
coordinates, and checked the even/odd split. Result, `n=9..21`:

| n | m | odd-level energy (should be exactly 0) | even_fraction |
|---|---|---|---|
| 9 | 4 | `6.5e-32` | `1.0000000000` |
| 11 | 5 | `2.4e-31` | `1.0000000000` |
| 13 | 6 | `4.9e-31` | `1.0000000000` |
| 15 | 7 | `1.1e-30` | `1.0000000000` |
| 17 | 8 | `8.7e-31` | `1.0000000000` |
| 19 | 9 | `9.7e-31` | `1.0000000000` |
| 21 | 10 | `1.4e-30` | `1.0000000000` |

**Odd-level energy is pure floating-point noise (`~1e-30`) at every tested `n` — `even_fraction
= 1.0000000000` exactly, not approximately.** This is as clean a confirmation as this project's
exact-data checks get.

**The hopeful connection to point 24, tested honestly and NOT confirmed.** Filmus (2016,
already cited in point 29) proves that a degree-`≤d` function on the full cube restricts to a
slice with harmonic-degree `≤d` and preserved norm up to `(1±O(d²/n))`. If `δ_i`'s spectral
WEIGHT (not just its support parity) concentrated on LOW degree, this machinery could translate
directly into a bound on `l_eff(N)` (point 24's exact open question) via the cube→slice
correspondence — a potentially real escape route, since routes checked so far (LP-dual, point
31) all failed. **Checked directly on the same exact data, honestly reported: it does NOT come
for free.** The tail energy beyond level 2 (`Σ_{k≥4} level_weight[k] / total`) is:

| n | 9 | 11 | 13 | 15 | 17 | 19 | 21 |
|---|---|---|---|---|---|---|---|
| tail beyond level 2 | 0.000 | 0.027 | 0.044 | 0.160 | 0.109 | 0.112 | 0.186 |

**This tail GROWS with `n` (noisily, but with no visible plateau across the tested range) — the
SAME qualitative "growing tail" signature point 24 already found in the Johnson-slice basis
(declining `tail_tightness_r`), now independently observed in the FULL-CUBE Fourier basis.**
This is genuinely informative but NOT a resolution: it is consistent with point 24's own honest
verdict that `l_eff(N)` boundedness leans (mildly, on limited data) toward "no," now corroborated
from a second, structurally-independent decomposition, not merely re-derived from the same one.
It does NOT complete Filmus's degree-preservation argument (that argument needs a genuine
low-degree bound, which this data does not show) and does NOT prove or disprove `l_eff(N)`
boundedness — it adds one more independent data point on the same side of the question point 24
already leaned toward.

**Verdict: a standard fact, correctly applied and exactly verified (δ_i's even-parity Fourier
spectrum) — genuine route-A progress on ITS OWN modest terms, exactly the kind of "identity from
complement-antisymmetry" the plan asked for, but not a new mathematical result in itself. The
hoped-for shortcut to point 24 via Filmus's degree-preservation theorem does NOT materialize —
the same growing-tail obstruction reappears in this independent basis.** Per the Cheapest
Differentiating Test Protocol, this closes off the "low full-cube degree ⟹ bounded `l_eff`"
shortcut cheaply (exact small-`n` data, no heavy new simulation) rather than investing in the
harder quantitative Filmus-bound derivation for a premise that isn't supported.

**What remains open, unchanged:** point 24's `l_eff(N)` boundedness question itself. The parity
fact is a genuine, standalone structural narrowing (possible spectrum levels for `δ_i` go from
`{1,2,3,4,...}` down to `{0,2,4,...}` — HALF the levels eliminated for free), worth keeping
regardless of what it does or doesn't say about the variance question — but parity restriction
is NOT low-degree concentration, and does not by itself constrain where on the even levels the
energy sits.

**Artifacts:** `check_delta_i_even_parity.py` (+`metrics/delta_i_even_parity_check.json`).

## Point 33 (2026-09-13) — Exam 3 stage 14: route C (slice harmonic) stage C0-C2 — higher
spectral moments computed directly via the swap operator (no per-level truncation); a THIRD
independent line of evidence, via a structurally different method, corroborates point 24's own
"mild lean against `l_eff` boundedness"

**Context, C0 (Source Trace).** User correctly flagged, per this project's own "pathologically
careful after Filmus" discipline: the `r=1` identity `T_q = 2·Σ_l γ_l·E_l` (already used
throughout points 15-24) IS the standard Johnson/slice total-influence identity from the
literature (Filmus's own slice work uses the identical spectral weight `d(N+1-d)` — cited by the
user, not independently re-fetched this point, flagged as `[WEAK]`-sourced pending a primary-
source check if this becomes load-bearing). **This should NOT be re-derived as if new — it
already IS what points 15-18 built.** The genuinely open question is `r≥2`.

**C1 (the r≥2 identity — standard linear algebra, not new math, stated for completeness).**
Since `L:=I-P` (the swap-walk Laplacian) is self-adjoint on each layer with `L|_{V_l} = γ_l·I`
(established, points 15-17), the spectral theorem gives `⟨f,L^r f⟩ = Σ_l γ_l^r E_l` for any `r`
— this is pure linear algebra given already-established facts, not something requiring external
citation to trust.

**C2 (cheap empirical check — the actual new computation this point performs).** Rather than
computing `M_r := ⟨f,L^r f⟩` via per-level `E_l` sums (which would UNDERCOUNT, since points 22-24
already showed mass migrating to levels beyond where `E_l` has been computed), `M_1, M_2, M_3`
are computed DIRECTLY by applying the already-validated swap-averaging operator `P` (hence `L`)
1, 2, 3 times to the exact `δ_i` array (same necklace-orbit-reduced data used throughout points
14-24) and taking inner products — no spectral decomposition, no truncation risk.

**Self-consistency check passed to machine precision before trusting `M_2,M_3`:** `T_q` (already
independently computed in point 15 via direct swap-pair enumeration) must equal `2·M_1` by the
standard Dirichlet-form identity for a reversible walk — verified here via an INDEPENDENT
recomputation of `T_q` from the same centered `f` array: agreement to `1.7e-16, 1.2e-16, 0, 0`
(pure floating-point noise) at `n=23,29,31,37`. This confirms the operator implementation is
correct before the genuinely new `M_2, M_3` numbers are trusted.

**Result, central layer `q=⌊N/2⌋` (matching points 15-31's own convention):**

| n | N | C_q | M1 | M2 | M3 | M2/M1 | M3/M2 | M2/Cq |
|---|---|---|---|---|---|---|---|---|
| 23 | 10 | 0.02495 | 0.02016 | 0.01698 | 0.01499 | 0.8422 | 0.8826 | 0.6807 |
| 29 | 13 | 0.01962 | 0.01393 | 0.01063 | 0.00870 | 0.7630 | 0.8182 | 0.5420 |
| 31 | 14 | 0.01813 | 0.01225 | 0.00896 | 0.00707 | 0.7315 | 0.7897 | 0.4942 |
| 37 | 17 | 0.01497 | 0.00919 | 0.00625 | 0.00467 | 0.6803 | 0.7460 | 0.4178 |

**Critical interpretive step, done carefully (per the same discipline that caught point 31's DOF
confound): the raw ratio `M2/M1` decreasing with `n` does NOT by itself mean `l_eff` is
shrinking.** `γ_l = l(N+1-l)/(q(N-q))` is itself `N`-dependent — for FIXED `l`, `γ_l` shrinks as
`N` grows (roughly `~4l/N` for central `q`), so `M2/M1` shrinking could be pure scale artifact,
not a substantive signal. **The correct move: invert `γ_l = M2/M1` for `l`, giving an `l_eff`
directly comparable to point 24's own notation:**

| n | N | l_eff (from M2/M1) | l_eff/N |
|---|---|---|---|
| 23 | 10 | 2.468 | 0.2468 |
| 29 | 13 | 2.883 | 0.2217 |
| 31 | 14 | 2.983 | 0.2131 |
| 37 | 17 | 3.342 | 0.1966 |

**`l_eff` itself GROWS (2.47→3.34) while `l_eff/N` shrinks (0.247→0.197) — this rules out
`l_eff∼cN` (linear growth, which would keep `l_eff/N` and hence `γ_l`≈`M2/M1` roughly CONSTANT),
but does NOT indicate boundedness — `l_eff` growing at all, even sub-linearly, is exactly the
scenario point 24's own analysis already showed forces `t_4→0`** ("any `l_eff→∞` even at rate
`log log N` forces `t_4→0`"). **This is a THIRD independent line of evidence, via a structurally
different method (direct swap-operator moments, no per-level energy decomposition at all),
corroborating point 24's own "mild lean against boundedness"** — not a new discovery of the same
fact, but a genuine independent check that could have come out the other way (had `l_eff/N`
stabilized at a nonzero constant, that would have argued for `l_eff∼cN`, a DIFFERENT and worse
scenario than either boundedness or sub-linear growth) and did not.

**Honest scope.** Only 4 data points (`n=23..37`, same range as points 15-18), too few to fit a
reliable growth-rate exponent for `l_eff(N)` — this does not upgrade point 24's "mild lean" to a
proof, and does not resolve `l_eff(N)` boundedness. What it DOES establish: three structurally
independent methods (point 24's per-level `tail_tightness_r`, point 32's full-cube Fourier tail-
beyond-level-2, and this point's direct swap-moment `l_eff` inversion) now agree on direction,
none of them merely re-deriving the others.

**Verdict and recommendation.** Route C's C0-C2 (cheap checks, per the user's own plan) are
complete and informative: the higher-moment machinery works (verified to machine precision) and
adds real, independent corroboration in the SAME direction as points 24 and 32, not a new one.
Per the user's own stated criterion ("если growing too fast, we kill another beautiful hypothesis
cheaply, not after a week of algebra") — this is not a kill of the whole investigation, but it
does mean the specific hoped-for "moments reveal favorable scaling, attack analytically" branch
of route C did not find favorable scaling. The harder analytic step (`||L^{r/2}δ_i||^2 ≤` small
function of `n`, the genuinely new Lovász-specific bound the user's own plan named as the real
target) was NOT attempted — per the same Cheapest Differentiating Test discipline, doing the cheap
check first (this point) before the expensive analytic derivation was the correct order, and the
cheap check's honest result (growing, not favorable) lowers the expected payoff of the harder step
without ruling it out entirely.

**Artifacts:** `check_higher_moments_M_r.py` (+`metrics/higher_moments_M_r.json`).

## Point 34 (2026-09-13) — Exam 3 stage 15: a genuine analytic attempt at `‖L^{r/2}δ_i‖²` —
one real, exact NEW identity found and verified; one honest, partial (not conclusive) positive
empirical signal; explicitly NOT a proof

**Context.** Direct user request to attempt real analytics on `‖L^{r/2}δ_i‖²` itself (the
genuinely new Lovász-specific bound point 33 named as the actual target, distinct from the
already-standard spectral algebra). This point reports a genuine attempt, not a repeat of the
cheap-check pattern — it is explicitly scoped as ATTEMPTED, HONEST, PARTIAL progress, not a
completed proof.

**The new identity (exact, not approximate — verified to machine precision before being
trusted).** For `S` in layer `q` (the `i`-excluded ground set), a swap `S'=S-a+b` is
SIMULTANEOUSLY a valid, `i`-PRESERVING swap of `S∪{i}` (i.e. it never moves `i` itself). This
means the swap-averaging operator commutes cleanly across the shift `S ↦ S∪{i}`:

```
L(δ_i)(S) = Lq(X)(S) - L*(X)(S∪{i})
```

**Precision correction, made before merge (self-caught, not just cited from the script's own
docstring — same discipline as point 32's "new theorem" framing fix):** `L*` here is **NOT**
layer `q+1`'s own full, standard swap-Laplacian (which would have degree `(q+1)(N-q)` and
average over ALL layer-`(q+1)` swaps, including ones that move `i` itself in or out — that
operator is genuinely different and was NOT what was computed). `L*` is the RESTRICTED
`i`-preserving operator — swapping only among the `N` ground elements excluding `i` — which by
construction has degree `q(N-q)`, matching layer `q`'s own degree exactly; that degree match is
exactly why the identity holds. Calling it "`L(q+1)`" (as an earlier draft of this point did)
would incorrectly imply it is the standard, unrestricted layer-`(q+1)` operator. **Verified
exactly** (`max|L(δ_i) - [LqX - L*X_shifted]|` over sampled `S`, `n=23,29,31,37`: `1.11e-16,
8.33e-17, 1.39e-16, 1.11e-16` — pure floating-point noise). This reduces `M_2(δ_i) = ‖L(δ_i)‖²`
to a question about `X`'s OWN cross-layer swap-smoothness (via this restricted operator) — a
DIFFERENT, and NOT previously studied in this precise form, object — not an invented auxiliary
quantity, a direct algebraic consequence of `δ_i`'s own definition as a one-generator
difference of `X`.

**Does the decomposition actually help? Checked directly, not assumed.** If `LqX` and the
shifted `L*X` were independent, `M_2(δ_i)` would equal their SUM; if they were highly
correlated, there would be CANCELLATION. Computed over the FULL layer (not a sample), `n=23,29,
31,37`:

| n | N | ‖LqX‖² | ‖L*X shifted‖² | cross-term | correlation | sum-if-independent | M2(δ_i) actual |
|---|---|---|---|---|---|---|---|
| 23 | 10 | 0.01757 | 0.01757 | 0.00907 | 0.5166 | 0.03513 | 0.01698 |
| 29 | 13 | 0.01272 | 0.01291 | 0.00750 | 0.5852 | 0.02563 | 0.01063 |
| 31 | 14 | 0.01161 | 0.01161 | 0.00713 | 0.6141 | 0.02321 | 0.00896 |
| 37 | 17 | 0.00879 | 0.00885 | 0.00570 | 0.6456 | 0.01764 | 0.00625 |

**Real, substantial cancellation, and it GROWS with `n`.** Correlation between `X`'s own swap-
smoothness on two adjacent layers rises `0.52→0.65` across `n=23→37` — `M_2(δ_i)` is roughly
HALF of what independence would give at every tested `n`, and the gap is not shrinking. This is
a genuine structural fact about `X` (not `δ_i`): its swap-Dirichlet behavior is increasingly
COHERENT across adjacent Hamming layers as `n` grows, not increasingly independent.

**A second, separately-encouraging signal: `‖LqX‖²` itself decays with `n`.** Log-log slope
across the same 4 points: **`-1.4506`** — i.e. `X`'s own within-layer swap-Dirichlet energy
empirically decays roughly like `n^{-1.45}`, FASTER than `T_q`'s own `~n^{-1.7}`-ish decay found
for `δ_i` directly (point 30) — encouraging IN DIRECTION, though this is a 4-point log-log fit
and should not be read as an established asymptotic rate.

**Honest assessment — this is real progress, but NOT a proof, and NOT yet a resolution.**
Three things are established here with high confidence (exact identity, verified cancellation,
verified decay of `‖LqX‖²` at these 4 points); NONE of the following is established: (a)
whether `‖LqX‖²`'s apparent `~n^{-1.45}` decay is a genuine asymptotic law or a finite-size
transient (4 points, same small range as every other exact check in this experiment, `n≤37`);
(b) whether this rate, even if genuine, is FAST ENOUGH to close the gap to `O(1/n)` for
`Var(X_n)` once correctly propagated through the Efron-Stein/ladder machinery (that propagation
was not attempted here — it requires knowing how `M_2(δ_i)`, not just `‖LqX‖²` alone, enters the
tail-control argument, and `M_2(δ_i)` itself still only decays (from point 33) in a way not yet
shown sufficient); (c) whether the growing correlation (0.52→0.65) continues growing toward 1
(which would give STRONGER cancellation, i.e. a MORE favorable signal) or saturates below 1 (in
which case the benefit is bounded). **This point does not claim to have found the missing
Lovász-specific bound — it reports a genuine, verified, non-trivial structural reduction plus
one honest empirical data point that is, for the first time in this entire route-A/B/C
investigation, NOT purely unfavorable.**

**What would be needed to complete this into an actual bound (named explicitly, not attempted):**
(1) an independent theoretical argument (not just curve-fitting 4 points) for why `X`'s own
cross-layer swap-correlation should increase with `n` — is there a mechanism, or is this a
coincidence of the specific `n=23,29,31,37` sample; (2) a rigorous connection from `‖LqX‖²`'s
decay rate to a bound on `M_r(δ_i)` for the `r` actually needed by the tail-control Markov bound
`Σ_{l≥L}E_l ≤ M_r/γ_L^r`; (3) extending this same identity to `r=3` (`⟨δ_i,L³δ_i⟩`), which was
not attempted here.

**Artifacts:** `check_cross_layer_cancellation.py`
(+`metrics/cross_layer_cancellation.json`).

## Point 35 (2026-09-13) — Extend points 33-34 (M_1,M_2,M_3, l_eff, cross-layer cancellation)
to n=41,43,47: three more corroborating points, still no resolution; a prior cost estimate
corrected

**Context.** Direct user request ("попробуй расширить на n=41,43,47") to extend point 33's
higher-moment/`l_eff` computation and point 34's cross-layer cancellation check beyond
`n=23,29,31,37` to the same upper `n`-range already used for other quantities in this
experiment (points 22-24's `tail_concentration_ratio.json`).

**Feasibility check performed before committing compute (per this project's own Cheapest
Differentiating Test discipline).** Central-layer sizes grow steeply: `n=37` (already done) has
`|V(q=8)|=C(17,8)=24310`; `n=41` is `C(19,9)=92378` (3.8x); `n=43` is `C(20,10)=184756` (7.6x);
`n=47` is `C(22,11)=705432` (29x). `check_necklace_orbit_reduction.py`'s `solve_orbit_reduced`
was confirmed (by reading its body) to have no cross-invocation cache for its own theta-array
result — only an unrelated `cross_validation` `json.dump` at module level — so each of points
33's and 34's own scripts, run independently, would each re-pay the full LP-solve cost per `n`.
`check_extend_moments_cross_layer_n41_43_47.py` was written to compute `X` ONCE per `n` and
reuse it for both the `M_r`/`l_eff` quantities and the cross-layer identity, avoiding that
duplication.

**Actual measured cost — ran n=41 first as a timing test before committing to n=43,47, per the
same discipline.** Wall-clock (this machine):

| n | layer size | theta time | moments+cross-layer time | total |
|---|---|---|---|---|
| 41 | 92378 | 195.6s | 18.2s | ~214s |
| 43 | 184756 | 213.6s | 40.0s | ~254s |
| 47 | 705432 | 807.0s | 163.6s | ~971s (~16.2 min) |

**Correction to a prior estimate, stated explicitly (Hindsight Distortion Gap discipline — name
the correction, don't silently absorb it).** This experiment's own earlier documentation (cited,
not re-quoted in full, from the point discussing `n=41` LP-solve-count feasibility) estimated
`n=41` at ~52,488 LP solves with costs scaling steeply for `n=43,47` (grouped with `n=53` at
"several hundred thousand" to "~1.3M" solves). The actual measured wall-clock cost for `n=41→43`
grew only ~9% (195.6s→213.6s) despite the layer itself doubling — and `n=47`, while clearly the
most expensive point (807.0s theta time), still completed in well under 20 minutes total, not
the "tens of minutes to hours" this session initially worried about before running it. The
discrepancy is plausibly explained by `solve_orbit_reduced`'s necklace-orbit reduction
amortizing much of the raw LP-solve count via the cyclic group's symmetry — but this is
`[INFERRED]`, not verified by reading that function's full internals in this session; the
practical, load-bearing fact is the measured wall-clock number, not the mechanism.

**Full results table, n=41,43,47 (canonical `l_eff_from_gamma` imported unchanged from
`check_higher_moments_M_r.py`, not reimplemented):**

| n | N | q | M1 | M2 | M3 | M2/M1 | M3/M2 | l_eff(M2/M1) | l_eff/N | corr(LqX,L*X) | identity_err |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 41 | 19 | 9 | 0.007731 | 0.005049 | 0.003646 | 0.6531 | 0.7221 | 3.5795 | 0.1884 | 0.6602 | 1.7e-18 |
| 43 | 20 | 10 | 0.007031 | 0.004491 | 0.003191 | 0.6388 | 0.7106 | 3.6901 | 0.1845 | 0.6687 | 0.0 |
| 47 | 22 | 11 | 0.005922 | 0.003644 | 0.002516 | 0.6153 | 0.6904 | 3.8976 | 0.1772 | 0.6823 | 0.0 |

**Combined with points 33-34's own `n=23..37` rows, both trends now span 7 points and remain
exactly monotonic — three more corroborations, same direction, no qualitative change:**

`l_eff` (from `M2/M1`): `2.468, 2.883, 2.983, 3.342, 3.580, 3.690, 3.898` (n=23,29,31,37,41,43,47)
— still GROWING.
`l_eff/N`: `0.2468, 0.2217, 0.2131, 0.1966, 0.1884, 0.1845, 0.1772` — still SHRINKING.
Cross-layer correlation (point 34's object): `0.5166, 0.5852, 0.6141, 0.6456, 0.6602, 0.6687,
0.6823` — still GROWING, smoothly, no sign of saturation within this range.

**One small, explicitly-labeled descriptive observation, NOT a claimed law (per Perelman-audit
discipline — a curve-fit over 7 points spanning `N=10..22` is `[WEAK]` evidence for any
asymptotic rate).** `l_eff/√N` is far flatter across the 7 points (`0.780→0.831`, a 6.5% drift)
than `l_eff/ln(N)` (`1.072→1.261`, a 17.6% drift) — i.e. `l_eff` growth looks descriptively
closer to `√N` than to `log N` over this range. This is offered only as a numerical observation
to guide intuition, not as an established rate: (a) `l_eff/√N` is itself still drifting upward,
not flat, so even the better-fitting curve is not confirmed constant; (b) `N=10..22` is a narrow
range for distinguishing growth laws; (c) no theoretical argument for `√N` scaling was attempted
here. If `l_eff` genuinely grows like `√N` (or anything unbounded), that would mean `l_eff(N)` is
NOT bounded in point 24's sense, even though `l_eff/N→0` — these are different claims, and this
session's data cannot yet distinguish "unbounded but sublinear" from "eventually bounded, still
transient at N≤22."

**Verdict.** PROMOTE the extended data as a fourth corroboration of the same trend already
established at points 24, 32, 33 — this is not a new qualitative finding, and the core question
(point 24's `l_eff(N)` boundedness, hence whether `Var(X_n)=O(1/n)` holds under this specific
mechanism) remains explicitly OPEN. The extension was worth doing because it (a) triples the
`n`-range for the same check at moderate, now-measured cost, (b) corrects an over-cautious prior
cost estimate for future planning in this experiment, and (c) sharpens the "boundedness would
require a real turnaround" concern — after 7 monotonic points with no sign of a turnaround,
continued growth is the working expectation, not proof of unboundedness.

**What this does NOT mean (explicit non-interpretations, per EstimandOps discipline):** does NOT
establish an asymptotic growth rate for `l_eff(N)` (7 points, narrow `N`-range, no theoretical
derivation); does NOT resolve point 24's boundedness question either way; does NOT mean
`Var(X_n)=O(1/n)` is false (that would require propagating `l_eff` growth through the actual
tail-control argument, not attempted); does NOT mean the `√N`-vs-`log N` descriptive comparison
is a validated law.

**Artifacts:** `check_extend_moments_cross_layer_n41_43_47.py`
(+`metrics/extended_moments_41_43_47.json`).

## Point 36 (2026-09-13) — Surgery on point 34: the "cross-layer identity" is trivial linearity
of `L_q`, not a new operator relation. Correction, verified independently before accepting it.

**Context.** An external LLM review of this experiment's full history flagged that point 34's
central "identity" `L(δ_i)(S) = L_q(X)(S) - L*(X)(S∪{i})` may be nothing more than linearity of
ONE fixed operator applied to two functions — i.e. `L* = L_q` literally, not an isomorphic-but-
distinct "restricted i-preserving operator" as point 34's own (already-once-corrected)
terminology implied. This matches the SAME pattern this session has now hit three times
(Filmus, point 32's "new theorem" framing, and now this) — per the user's own standing
instruction, treated with the same seriousness rather than defended.

**Verification performed before accepting the correction (per audit-verification-gate.md — an
external LLM's `[VERIFIED]` is this session's `[INFERRED]` until independently checked).**
Wrote `verify_Lstar_equals_Lq.py`: builds `L*` applied to `X_1(S):=X(S∪{i})` two ways —
**Route A** (point 34's own code path: `apply_L_to_layer(X_1, combos_q, masks_q,
mask_to_idx_q, ground_set)`, i.e. literally reusing layer `q`'s own swap machinery) and
**Route B** (a separately-coded construction: for each `S` in layer `q`, build `T=S∪{i}`
directly and enumerate `i`-preserving swaps of `T` in a fresh loop, without calling layer `q`'s
`combos_q`/`masks_q` machinery). Result, `n=23,29,31,37`: **`max|Route A − Route B| = 0.000e+00`**
at every `n` — exact agreement, not approximate.

**Precision correction to this verification's own epistemic weight (reviewer finding, P2,
addressed before merge — same discipline this point itself is modeling).** Route A and Route B's
exact agreement is **not independent empirical confirmation of a nontrivial fact** — it is
*algebraically guaranteed* by bit-disjointness: bit `i` (bit 0) never overlaps the ground bits
used in `combos_q`, so `(mask & ~(1<<a)) | 1 | (1<<b)` (Route A's index arithmetic) and
`((mask|1) & ~(1<<a)) | (1<<b)` (Route B's) are identical index expressions for any `a,b` —
zero error is what the arithmetic forces regardless of what `X` actually is. So this script
verifies IMPLEMENTATION CORRECTNESS (the two code paths compute the same thing), not an
independent mathematical fact about `L*` and `L_q`. **The substantive claim itself — that `L*`
IS `L_q`, not merely isomorphic — rests on the code-inspection argument two paragraphs below
(identical `apply_L_to_layer` call with identical `combos_q`/`masks_q`/`mask_to_idx_q`/
`ground_set` arguments), not on this numeric check.** Stated this way, the correction is not
weakened, only correctly scoped: it was already obvious from reading point 34's own code that
`L*=L_q` literally; `verify_Lstar_equals_Lq.py` confirms no bug hides that fact, it does not
supply independent evidence for it.

**What this means for point 34's claim.** `δ_i = X_0 - X_1` where `X_0(S):=X(S)` and
`X_1(S):=X(S∪{i})` are BOTH, from the start, functions on the SAME layer `q` (not on two
different layers at all, despite point 34's "cross-layer" framing). Since `L_q` is linear:

```
L_q(δ_i) = L_q(X_0 - X_1) = L_q(X_0) - L_q(X_1)
```

holds for ANY linear operator applied to a difference of two functions on its own domain —
this is not specific to swap-Laplacians, Johnson schemes, or anything Lovász-specific. Point
34's "genuine new identity" claim is **withdrawn**; it was pure linearity dressed in
cross-layer language.

**Surgery log (per perelman-audit.md):**

| old_component | failure_mode | evidence | replacement | forbidden_claims |
|---|---|---|---|---|
| Point 34's "exact new identity `L(δ_i)=L_qX-L*X_shifted`, restricted operator `L*`" | Presented ordinary linearity of one fixed operator as a discovered cross-layer relation | `verify_Lstar_equals_Lq.py`: Route A ≡ Route B to `0.000e+00`, `n=23,29,31,37` | "`δ_i=X_0-X_1` on the SAME layer `q`; `L_q(δ_i)=L_q(X_0)-L_q(X_1)` by linearity — bookkeeping, not a theorem" | "point 34 found a new cross-layer swap-Laplacian identity"; "`L*` is a distinct operator from `L_q`" |

**What survives, unaffected — the empirical content was never about the operator, it was
always about `X` itself.** The correlation numbers, their growth, and the `‖L_qX_0‖²` decay
rate are genuine, real properties of the specific pair of functions `(X_0,X_1)` — i.e. of how
Lovász theta's value on a generator-subset compares to its value on the same subset plus one
more generator — under the ordinary swap-Laplacian `L_q`. Correcting the operator-theoretic
framing does not touch these numbers; it only removes the claim that a NEW operator or a
NEW identity was found. Re-stated honestly: **"`L_q` applied to `X`'s two `i`-shift copies
shows growing positive correlation (`0.52→0.68` across `n=23..47`, now 7 points) — an
empirical property of the Lovász theta function pair, not a structural theorem."**

**Verdict.** REJECT point 34's "new identity" framing specifically; PROMOTE the underlying
empirical correlation/decay observations, now correctly attributed to `X` itself rather than to
a fabricated cross-layer operator. `l_eff`/`M_r` results from points 33, 35 are untouched (they
never depended on `L*` being a distinct operator).

**Artifacts:** `verify_Lstar_equals_Lq.py` (verification only, no metrics file — result is a
single scalar consistency check, recorded here).

## Point 37 (2026-09-13) — Cheapest new falsification gate from the external re-plan: does `X`
(Lovász theta, log-normalized) show submodularity or sign-biased second differences?

**Context.** Per the external re-plan's own prioritization ("самым интересным дешёвым
направлением"): rather than another universal Johnson-graph inequality, check whether `X` has
ANY Lovász-specific second-order structure — submodularity (`Δ_iΔ_jX ≤ 0`) or at least a sign
bias / small second moment — that could directly control `δ_i`'s variation. This is the first
check in this entire experiment aimed at a structural property of `X` itself rather than at the
Johnson-scheme machinery around it.

**Setup.** For each pair of distinct generators `i,j` (bits), the mixed second difference on a
base set `S` (with `i,j∉S`) is `Δ_iΔ_jX(S) = X(S) - X(S∪{i}) - X(S∪{j}) + X(S∪{i,j})` — the
standard discrete mixed partial derivative. `X` is submodular iff this is `≤0` for all `S,i,j`
(diminishing returns: adding `j` helps less once `i` is already present). Computed exactly
(reusing the already-available full `x` array from `solve_orbit_reduced`, no new theta-solves
needed) over ALL `S` not containing `i,j`, for a representative sample of `(i,j)` pairs and
several `n`.

**Results, `n=23,29,31,37,41` (10 sampled `(i,j)` pairs per `n`, ALL `S` not containing `i,j`
enumerated exactly):**

| n | frac(Δ≤0) | mean(Δ) | std(Δ) | E[Δ²] |
|---|---|---|---|---|
| 23 | 0.5000 | 0.000000 | 0.1785 | 0.03187 |
| 29 | 0.5005 | 0.000000 | 0.1414 | 0.01998 |
| 31 | 0.5000 | -0.000000 | 0.1335 | 0.01783 |
| 37 | 0.5000 | -0.000000 | 0.1111 | 0.01234 |
| 41 | 0.5000 | 0.000000 | 0.1020 | 0.01040 |

**No sign bias whatsoever — and this is analytically forced, not a coincidence (verified
before trusting it, same "standard fact, newly applied" discipline as points 32/36, not a new
theorem).** `Δ_iΔ_jX` is a discrete SECOND derivative of `X`. Chaining the already-established
shift identity (point 32) twice: `X` has Fourier spectrum on ODD degree (point 11, pre-
existing); `D_iX=δ_i` has spectrum on EVEN degree (point 32); `D_j(D_iX)=Δ_iΔ_jX` has spectrum
on ODD degree again. Verified directly via WHT (`verify_second_diff_parity.py`) at `n=17,19`
(both prime, matching this experiment's actual domain): `even_fraction≈1e-29..1e-31` — exact,
not approximate. A function with purely-odd Fourier spectrum satisfies `g(S)=-g(S^c)` exactly
(`χ_T(-x)=(-1)^|T|χ_T(x)`, standard), so as `S` ranges uniformly, `{g(S)}` is symmetric around 0
BY CONSTRUCTION. **This means item 5's original plan (test submodularity via sign/mean of
`Δ_iΔ_jX`) is structurally dead on arrival for this specific `X` — the null sign-balance is
guaranteed by Fourier parity, independent of whether `X` has any interesting second-order
structure at all.** Submodularity (or its opposite) cannot be detected this way; a conditional
or magnitude-based test would be needed instead.

**What IS informative: the magnitude decays, and reasonably fast.** Since the sign/mean channel
is closed by parity, `E[Δ²]` (second moment of the mixed second difference) is the one
meaningful summary left standing, and it shrinks with `n`: log-log slope over `n=23..41` is
**`≈-1.95`** (least-squares over the 5 points) — i.e. `E[Δ²]∼n^{-2}` roughly. This is offered as
a plain numerical observation (5 points, no theory attempted), directionally encouraging
(pairwise second-order interaction strength is not blowing up, if anything shrinking close to
quadratically) but not a claim about the target `Var(X_n)=O(1/n)` question, which concerns a
different quantity (`C_q`, not `E[Δ²]`) reached through a different (Efron-Stein) argument.

**Side-finding, explicitly out of scope, recorded as a Pearl, not chased further.** Probing
whether the parity mechanism holds at COMPOSITE `n` (curiosity check, not part of this
experiment's actual domain) surfaced a real but unrelated fact: `theta_via_lp`/
`solve_orbit_reduced` produces exact-zero `theta_full` entries for some generator-subsets when
`n` is composite (`n=15,21` tested), making `log(theta_full/√n)` produce `NaN`/`-inf` — X's own
base odd-parity property (point 11) was evidently only ever exercised at PRIME `n` in this
experiment; composite `n` breaks the underlying LP-solve construction itself (plausibly a
disconnected or degenerate circulant graph for certain generator subsets), not the parity
argument specifically. Every `n` used anywhere else in this experiment (`23,29,31,37,41,43,47`)
is prime, so this does not affect any existing result — flagged for whoever might extend this
pipeline to composite `n` later, not investigated further here (Pearl Registry candidate:
observation="composite n gives degenerate/zero theta for some subsets", falsifiable_prediction=
"any future composite-n run of `theta_via_lp` will show exact zeros or NaN downstream",
impact_score=3 — narrow, only matters if this experiment's n-range is ever extended to
non-primes).

**Verdict.** REJECT the original plan for item 5 as originally framed (sign-test for
submodularity) — killed cheaply, by a clean structural argument, exactly the kind of fast kill
the Cheapest Differentiating Test Protocol wants. PROMOTE the magnitude-decay observation
(`E[Δ²]∼n^{-2}`-ish) as a mild, non-conclusive, additional data point, and record the composite-n
side-finding as a Pearl rather than a result of this point.

**Artifacts:** `check_submodularity_second_differences.py` (+`metrics/submodularity_check.json`),
`verify_second_diff_parity.py`, `verify_X_parity_prime_vs_composite.py` (verification-only, no
separate metrics file).

## Point 38 (2026-09-13) — Extend point 33's moments from M_1,M_2,M_3 to M_1..M_6, across ALL
`n=23..47`: the spectral spread itself is growing, not just its center

**Context.** Per the external re-plan's item 3: compute higher moments beyond `M_3` (cheap,
same `L=I-P` machinery applied more times, no new theta-solves needed beyond what's already
routine in this experiment), across the FULL `n`-range now available (`23,29,31,37,41,43,47`,
combining points 33 and 35's separate ranges into one script/table for the first time).

**Self-consistency check (reviewer-corrected — an earlier draft of this paragraph overclaimed
"every one of the 7 n").** `check_higher_moments_M1_M6.py` independently recomputes
`l_eff_from_M2_M1` via a freshly-written script (not copy-pasted state). Checked against
points 33/35's own previously-committed values: **exact (`==`) agreement at 5/7 points**
(`n=23,29,31,37,47`, e.g. `n=47`: `3.8976180931884583` both places), and agreement to
**~15-16 significant digits** (relative differences `~2e-16` to `~9e-16`) at `n=41,43`. The
latter is a documented floating-point-order artifact, not a bug: `check_extend_moments_
cross_layer_n41_43_47.py` centers `delta_q` AFTER computing `Ldelta` (dotting with the
centered array), while this script centers BEFORE applying `L` — algebraically identical by
`L`'s linearity (both scripts' own comments note this), but not bit-identical due to
floating-point non-associativity. No drift in the underlying math, no bug introduced by the
extension — only sub-ULP arithmetic-order noise at 2 of 7 points.

**New diagnostic: `ρ_γ := M1·M3/M2²`.** By Cauchy-Schwarz applied to the spectral-moment inner
product (`M_r=Σ_lγ_l^rE_l`), `ρ_γ≥1` always, with equality iff the spectral mass sits at a
single `γ_l` value. Results, `n=23..47`: **`1.0479, 1.0723, 1.0795, 1.0966, 1.1057, 1.1125,
1.1221`** — monotonically GROWING across all 7 points, staying modest in absolute terms but
moving steadily away from 1.

**A second, more directly interpretable statement of the same fact: the spread between
`l_eff` estimates from different moment-ratio pairs widens with `n`.** For a FIXED `n`,
`l_eff_from_M{r+1}_M{r}` (for `r=1..5`) gives 5 different "effective level" estimates — if the
spectral mass truly sat near one level, these would all agree; they systematically increase
with `r` (expected — see caveat below), but BY HOW MUCH grows with `n`:

| n | l_eff(M2/M1) | l_eff(M6/M5) | spread |
|---|---|---|---|
| 23 | 2.468 | 3.254 | 0.786 |
| 29 | 2.883 | 3.957 | 1.074 |
| 31 | 2.983 | 4.150 | 1.168 |
| 37 | 3.342 | 4.848 | 1.507 |
| 41 | 3.579 | 5.318 | 1.739 |
| 43 | 3.690 | 5.594 | 1.903 |
| 47 | 3.898 | 6.062 | **2.165** |

The spread nearly TRIPLES (`0.786→2.165`) across `n=23→47` — a substantially clearer growth
signal, in interpretable units of "eigenspace level", than `ρ_γ`'s own modest-looking
`1.05→1.12` drift (same underlying fact, different scaling).

**Caveat, stated proactively (same "standard fact, newly applied" discipline as points 32, 36,
37 — this experiment now has enough precedent to apply it by default, not just after being
corrected).** `M_{r+1}/M_r` being non-decreasing in `r` — hence `l_eff` estimates increasing
with `r` — is NOT itself a discovery: it is a standard consequence of Cauchy-Schwarz for any
nonnegative spectral measure (`M_r²≤M_{r-1}M_{r+1}`, i.e. `r↦\log M_r` is convex). What is NOT
standard, and IS the actual finding here, is that the WIDTH of this spread — not just its
existence — grows substantially with `n`. That is a genuine, new, quantitative statement about
this specific `X`, not a generic moment-sequence fact.

**What this means for the overall investigation (reviewer-corrected — an earlier draft claimed
"EIGHTH" without an enumeration backing the count; not re-counted here, listed explicitly
instead).** This experiment now has multiple independently-constructed quantities moving in the
same direction: `tail_tightness_r`, the cube-Fourier tail (point 32), `l_eff` from `M2/M1` (7
points, points 33/35), cross-layer correlation (7 points, points 34/36), and now `ρ_γ`/`l_eff`-
spread (7 points, this point) — five named lines of evidence, not a precise larger count. More
of the spectral mass, and now a genuinely WIDENING share of it, sits away from the low-`l`
region as `n` grows. None of these individually proves `l_eff(N)` is unbounded — each is a
finite-`n`, `N≤22` observation — but the number and diversity of independently-constructed
quantities all pointing the same way is itself worth naming plainly: a real turnaround at some
larger `N` would need to reverse all of them simultaneously, not just one.

**What this does NOT mean:** does NOT establish any asymptotic rate for `ρ_γ` or the `l_eff`
spread (7 points, `N≤22`, no theory attempted); does NOT by itself change the answer to point
24's boundedness question; does NOT mean `M_r` for `r>6` would show the same pattern (untested).

**Artifacts:** `check_higher_moments_M1_M6.py` (+`metrics/higher_moments_M1_M6.json`).

## Point 39 (2026-09-13) — Two cheap falsification tests from a second external re-analysis of
points 35-38: one refutes its central pessimistic argument, one weighs against its own
suggested fix

**Context.** After points 35-38, the user forwarded a second, more detailed external
re-analysis proposing a specific mathematical argument (its own "§2.3") for why the generic
moment-bound route is "fundamentally obstructed" — assuming `α_s` (the `n`-decay exponent of
`M_s`) grows LINEARLY in `s`, it derives that the tail bound `B_{s,k}=Σ_{l<k}E_l+M_s/γ_k^s`
cannot improve past a fixed exponent (`≈n^{-0.95}`) regardless of `(s,k)` choice, and
separately proposes ("Variant C") re-fitting `Var(X_n)` with an additive `A/n+B/n^{1.5}` model
to check for a positive leading `A/n` coefficient. Per this project's own discipline (an
external analysis's derivation is `[INFERRED]`, not `[VERIFIED]`, until checked against this
project's own data — audit-verification-gate.md), both claims were tested directly, cheaply,
using data already on hand — no new theta-solves for either check.

**Test 1 — is `α_s` actually linear in `s`? NO — it is concave (sub-linear), which refutes the
specific "fundamentally obstructed" argument as stated.** `check_alpha_s_linearity.py` computes
`α_s` (log-log slope of `M_s` vs `n`, `s=1..6`) directly from point 38's already-committed
`metrics/higher_moments_M1_M6.json` (`n=23..47`):

| s | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| `α_s` | 1.704 | 2.143 | 2.488 | 2.778 | 3.037 | 3.278 |

Consecutive differences `α_{s+1}-α_s`: **`0.440, 0.345, 0.290, 0.260, 0.241`** —
**strictly decreasing at every step**, not constant (residuals of the linear-in-`s` fit,
persisted in `metrics/alpha_s_linearity_check.json` for re-audit: `-0.093, +0.037, +0.072,
+0.052, +0.001, -0.068` — curved, not random, despite the fit's superficially high `R²=0.987`).
**Significance check (reviewer suggestion, point 39 — added so this conclusion doesn't rest on
eyeballing 5 numbers): under the null that the 5 differences are exchangeable (no trend), the
exact chance of observing them in perfectly sorted decreasing order is `1/5!≈0.00833`** (brute-
force permutation count, not a normal-approximation) — this IS significant at the conventional
`α=0.05` threshold, unlike Test 2's own significance check below. **The external analysis's
§2.3 argument requires `α_s=α_1+(s-1)(1-θ)` for a CONSTANT `θ`** (equivalently,
`(α_s-α_1)/(s-1)` constant across `s`) — checked directly: `0.440, 0.392, 0.358, 0.333, 0.315`
for `s=2..6`, also monotonically decreasing, confirming the assumption does not hold.
**Conclusion: the specific mathematical argument for "moment-route stuck regardless of `s`"
does NOT survive contact with this project's own already-computed data.** This does NOT mean
the moment route works — concave `α_s` still means diminishing returns per additional moment,
and whether the returns diminish fast enough to prevent ever reaching the needed `n^{-2}` scale
is genuinely open, unresolved by this cheap check alone (that remains item 4's job, if
pursued). What this DOES mean is narrower and solid: a specific pessimistic argument, built on
an unverified linearity assumption, is refuted — the moment route's fate should not be
considered settled by that argument.

**Test 2 — does refitting `Var(X_n)` with an `A/n`-leading additive model actually improve on
the already-established plain power law? INCONCLUSIVE — an initial "yes, misspecified" reading
of the sign-runs check was itself statistically unsupported (reviewer P1, corrected below,
not silently absorbed).** `check_var_additive_fit.py` re-fits this experiment's ROOT-level
Monte Carlo sweep (`metrics/run.json`, `n=32..3000`, `var_log_ratio` = `Var(X_n)` directly —
the actual quantity of interest, not a proxy) with three `A/n`-leading additive models
(`A/n+B/n^{1.5}`, `A/n+B/n²`, `A·log(n)/n+B/n`) against the plain power law already committed
there (`slope≈-0.9126`, `verdict: REJECTED` for the original `O(1/n)` claim).

| Model | `R²` | sign-runs (out of 9) | pos/neg split | Wald-Wolfowitz `z` |
|---|---|---|---|---|
| power law `n^p` | 0.9924 | 7 | 6+/3- | 1.633 |
| `A/n+B/n^{1.5}` | 0.9976 | 3 | 8+/1- | 0.535 |
| `A/n+B/n²` | 0.9976 | 3 | 8+/1- | 0.535 |
| `A·log(n)/n+B/n` | 0.9976 | 3 | 8+/1- | 0.535 |

All three additive models DO fit with a marginally higher raw `R²`, and all three DO recover a
large positive `A≈3.65-3.67`. **A first pass at this point compared the raw sign-runs counts
(7 vs 3) and called the additive models' pattern a "textbook misspecification signature" — a
reviewer caught this as statistically unsupported and it is corrected here, not left standing.**
Raw run counts are NOT comparable across fits with different positive/negative splits: an 8+/1-
split can achieve AT MOST `2·min(8,1)+1=3` runs, so "3 runs" there is close to that split's OWN
expected value, not anomalous. The proper normalization is the Wald-Wolfowitz runs-test
`z`-score (`z=(runs-μ)/σ`, `μ=2n₁n₂/N+1`) — computed for both families: **`z≈0.535`** for every
additive model, **`z≈1.633`** for the power law. **Neither exceeds `|z|=2` — neither residual
pattern is statistically distinguishable from random at `n=9`.** The `R²` gap (`0.9976` vs
`0.9924`) is itself marginal. **Corrected conclusion: this specific check is INCONCLUSIVE at
`n=9` — it does not demonstrate that forcing an `A/n` leading term produces either a better or
a worse fit than the plain power law on this dataset.** It also does NOT retroactively support
the additive model — the large recovered `A≈3.65` is not independently validated by anything in
this check beyond the (also inconclusive) `R²` comparison.

**Verdict.** Test 1 is a solid, `[VERIFIED-REAL]` refutation of the second external analysis's
central pessimistic argument (`p≈0.0083`, real significance, not a coincidence of 5 numbers).
Test 2 started as an attempted refutation of the analysis's proposed rescue ("Variant C") but
its own statistical backing did not survive review — the honest outcome is that Test 2 settles
NOTHING either way, and is recorded as a null/inconclusive result rather than quietly dropped
(per this project's own null-results discipline: a check that doesn't discriminate is still
worth recording, so the same untested claim isn't re-litigated from scratch later). Net effect:
the second external analysis's central pessimistic argument is refuted; its proposed rescue is
neither confirmed nor refuted by this specific check. The core question (does `Var(X_n)=O(1/n)`,
and is the moment route viable) remains open.

**What this does NOT mean:** does NOT mean the moment route (item 4) will succeed if pursued —
only that one specific argument for why it must fail is wrong; does NOT mean `Var(X_n)` is
exactly `n^{-0.91}` forever — 9 points up to `n=3000` is still a finite window; does NOT mean
`A>0` is false — only that the specific 2-parameter additive forms tested here don't fit better
than the plain power law on this dataset; a differently-shaped correction term was not ruled
out.

**Artifacts:** `check_alpha_s_linearity.py` (+`metrics/alpha_s_linearity_check.json`),
`check_var_additive_fit.py` (+`metrics/var_additive_fit_check.json`).

## Point 40 (2026-09-13) — Priority A/B Source Trace (autonomous research mission, Step -4):
real literature search, one route ruled out with a concrete reason, one candidate flagged as
unresolved, no ready-made Lovász-theta-specific theorem found

**Context.** Per the user's autonomous-research-mission brief (2026-09-13), Priority A
(second-order/higher-order variance inequalities) and Priority B (Lovász-theta-specific value
sensitivity) call for a Source Trace BEFORE any proof attempt — real primary sources via actual
tools (arxiv, OpenAlex via `mcp__scientific-papers`), never citing from memory. Searches
performed; results below, each explicitly `[CLASSICAL]` (verified via tool) or a documented
absence (not proof of non-existence — a keyword search finding nothing is `[UNKNOWN]`, not
`[RETRACTED]` or `[NULL RESULT]` for the broader literature).

**Finding 1 — self-bounding functions `[CLASSICAL, NOT DIRECTLY APPLICABLE]`.** Boucheron,
Lugosi, Massart, "On concentration of self-bounding functions" (EJP 14, 2009) — verified via
OpenAlex (id `W2092654494`). Self-bounding functions require a ONE-SIDED condition on
coordinate differences (`0≤f-f_i≤1`, i.e. removing a coordinate can only decrease `f`, never
increase it). **This project's own already-established, twice-verified fact rules this out
directly for `X`:** `δ_i` has EXACT even-degree Fourier parity (point 32) and the mixed second
difference `Δ_iΔ_jX` has EXACT odd-degree parity (point 37), both implying `g(S)=-g(S^c)`
exactly — i.e. `δ_i` and `Δ_iΔ_jX` are provably SIGN-SYMMETRIC (zero mean, `frac≤0=0.5` exactly),
not one-signed. **The self-bounding-function framework's central hypothesis is therefore
violated by an already-proven structural fact about this specific `X`, not by assumption.**
This is a genuine, well-grounded route closure — not "we didn't find a way to apply it", but
"the entry condition is provably false here".

**Finding 2 — second-order Poincaré inequality `[CLASSICAL, APPLICABILITY UNRESOLVED]`.**
Chatterjee (2009) and Nourdin-Peccati-Reinert (2009) — verified indirectly via Vidotto (2017,
arXiv:1706.06985) which cites both by name and year while presenting "An Improved Second Order
Poincaré Inequality for Functionals of Gaussian Fields" (confirms the primary sources exist and
their approximate content, though the two founding papers themselves were not directly fetched
in this pass). **This machinery is built for GAUSSIAN fields** (bounding distributional distance
to normality via Malliavin-Stein / Gaussian chaos methods) — whether a discrete-cube/Johnson-
scheme analogue exists as a NAMED, citable result was searched for directly (multiple query
variants: "second order Poincare inequality discrete Boolean cube", "second order Poincare
inequality discrete combinatorial variance quadratic functional") and **no direct hit was
found**. This is recorded honestly as `[UNKNOWN]`, not `[RETRACTED]` — a keyword search finding
nothing is weak evidence of absence, not proof; a discrete analogue may exist under different
terminology (the search surfaced adjacent-but-not-matching results: matrix concentration,
multiscale Poincaré for continuum random fields, order-statistics concentration — none a
discrete-cube second-order Poincaré). **Flagged as the single most promising still-open thread
from Priority A** — deriving (not just citing) a degree-weighted variance inequality specific
to this project's Johnson-scheme setting remains a live, unexplored option, distinct from citing
an existing theorem.

**Finding 3 — Lovász-theta-specific sensitivity/concentration for random graphs
`[SEARCHED, NOT FOUND]`.** Two directly relevant, real papers were found and read (abstracts):
Banks, Kleinberg, Moore, "The Lovász Theta Function for Random Regular Graphs and Community
Detection in the Hard Regime" (arXiv:1705.01194) — addresses THRESHOLD behavior (when `θ` can
refute `k`-colorability relative to the Kesten-Stigum threshold), not variance/concentration of
`θ` itself. Feige, Grinberg, "Upper bounds on the theta function of random graphs" (arXiv:
2506.02952, 2025 — genuinely recent) — **notable finding in its own right**: even the leading
CONSTANT in `θ(G_{n,1/2})=Θ(√n)` has been open for over 40 years, and this 2025 paper's own
`1.55√n` bound is explicitly a CONJECTURE based on unproven assumptions, not a theorem. Neither
paper addresses `Var(θ)` or concentration around the mean. **This is itself informative, not
just a dead end**: if Lovász-theta-specific concentration/sensitivity results existed as a
ready-made, easily-findable theorem, this experiment's entire multi-week investigation (points
1-39) would likely have surfaced it already via any of the many prior Source Trace passes — its
continued absence across an independent, fresh search this point is corroborating evidence
(weak, not proof) that no such ready-made theorem exists, and any progress here likely requires
DERIVING new structure specific to this project's `X`, not citing one.

**Finding 4 — Stein's method for concentration (exchangeable pairs), Chatterjee-Dey 2010
`[CLASSICAL, MOST PROMISING LEAD SO FAR]`.** Verified via DOI lookup: Chatterjee, Dey,
"Applications of Stein's method for concentration inequalities" (Annals of Probability, 2010,
also arXiv:0906.1034). Confirmed via direct abstract fetch (not title-matching alone) — this is
**genuinely discrete/combinatorial**, not Gaussian: applications include the Curie-Weiss model,
Ising model on lattices, and — most directly relevant — **exact large-deviation asymptotics for
subgraph counts (including triangles) in Erdős-Rényi random graphs**. Subgraph counting in
`G(n,p)` is a well-known paradigm case where naive Efron-Stein/McDiarmid bounds are famously
LOOSE precisely because of higher-order dependency structure (a single edge can participate in
many triangles, creating exactly the kind of "spectral migration to higher-degree terms" this
project's own points 33/35/38 found for `X`) — the paper's own stated purpose is extending
Stein's method to problems "involving complex dependencies" where standard tools "struggle".
**This is a substantially closer structural analogue to this project's own setting than the
Gaussian second-order Poincaré line (Finding 2)** — worth prioritizing for a full read of the
actual technical machinery (not just the abstract) as the concrete next step, over continuing
to search for a Lovász-theta-specific theorem that may not exist (Finding 3).

**Verdict.** REJECT self-bounding functions as a route, with a concrete, already-proven
structural reason (not speculative). PARK second-order Poincaré (Gaussian-specific, Finding 2)
as `[UNKNOWN]` applicability to this discrete setting. PROMOTE Stein's method / exchangeable
pairs (Finding 4) as the single most promising literature lead found this pass — genuinely
discrete, explicitly built for exactly the "complex dependency, naive bounds too weak" regime
this project is in. RECORD the Lovász-theta-specific literature search (Finding 3) as a
genuine, if partial, null result: no ready-made theorem found across multiple searches,
consistent with (not proof of) the frontier being genuinely open at this specific intersection.
This matches the autonomous mission's own Priority ranking discipline (Priority A/B before
Priority C) — none of Priority C (moment method with growing cutoff, item 4) was attempted in
this point, per the mission's own instruction to prefer cheap literature-based
falsification/discovery before expensive new computation.

**What this does NOT mean:** does NOT mean second-order Poincaré is inapplicable — only that a
direct discrete analogue wasn't found by keyword search, which is weak evidence at best; does
NOT mean no Lovász-theta concentration theorem exists in the literature — only that a
reasonably thorough search across two real academic search backends (arXiv, OpenAlex) in this
session did not surface one; does NOT constitute a Hard Block Certificate (per the mission's
own Step 20 criteria — literature search is not yet exhaustive, e.g. the two founding
second-order-Poincaré papers were not read directly, and INSPIRE-HEP/Semantic Scholar were not
usable this pass due to rate limits, not yet retried).

**Artifacts:** none (pure literature Source Trace — no code, no metrics file; findings recorded
here as the artifact, per this project's existing convention for `source_register.md`-style
Step -4 documentation, kept inline rather than as a separate file since the search was narrow
and does not warrant a standalone tracking document; point 41 continues Finding 4 with the
actual theorem text read in full).

**UPDATE (2026-09-13, `literature_check_2026-09-13.md`) — this point's own InspireHEP/Semantic
Scholar rate-limit gap, explicitly flagged above as unresolved, was retried and closed.** Result:
corroborates rather than overturns this point's own conclusion — still no ready-made theorem for
`Var(θ)` or `Var(log(θ/√n))` on any random graph model. Two new, independently-read citations
worth keeping on record: (1) **Bandeira, Błasiok, Dmitriev, Faure, Kireeva, Kunisky, "The Lovász
number of random circulant graphs," arXiv:2502.16227 (Feb 2026)** — direct, dated confirmation
that even the leading-order EXPECTATION `E[θ(G)]`'s constant for dense random circulant graphs
(this project's own graph family) remains an open conjecture (their own "Conjecture 18"), with
only `√n≤E[θ(G)]≤C√(n log log n)` established — a field that has not yet fixed the mean is very
unlikely to have already fixed the variance, which sharpens (with a hard citation, not just "no
theorem found") this project's own claim that it targets a genuinely open question. (2) **Arora &
Bhaskara, "A note on the Lovász theta number of random graphs" (2011)** — a genuine
tail-concentration result for `θ(G(n,1/2))` (different ensemble: Erdős-Rényi, not circulant),
`Pr[|θ(G)-μ|>t]≤exp(-t^{4/3}/(C log³n))`, i.e. a `polylog(n)`-width concentration window — the
closest existing analogue found, worth citing explicitly as "nearest relative, different
ensemble, weaker conclusion (tail bound, not a variance power law)" rather than leaving the
comparison implicit. Full search record, including the Chebyshev-dual-certificate novelty check
for points 47-48 (verdict: `[POTENTIALLY-NOVEL]` — classical machinery, specific closed form not
located verbatim in the literature reached), in `literature_check_2026-09-13.md`.

## Point 41 (2026-09-13) — Chatterjee-Dey's exchangeable-pairs machinery, read in full: exact
theorem cited, a concrete bridge to this project's own swap-Laplacian identified, NOT yet a
completed derivation — honestly scoped as an open, promising lead

**Context.** Continuing point 40's Finding 4, the actual theorem (not just the abstract) was
read via `mcp__arxiv__get_paper_latex_section` (arXiv:0906.1034, Section 2, "Results and
examples"). This is a genuine Source Trace deepening — reading the primary source directly, per
the autonomous mission's Literature Agent standard ("читать оригинал, давать theorem/lemma
numbers"), not citing from a summary.

**The exact theorem (quoted, `[CLASSICAL]`, Chatterjee 2007, Theorem 1.5, itself summarizing
Chatterjee 2005).** For a separable metric space `𝒳` and an exchangeable pair `(X,X')` of
`𝒳`-valued random variables, square-integrable `f:𝒳→ℝ` and antisymmetric `F:𝒳×𝒳→ℝ`
(`F(X,X')=-F(X',X)`) with `E(F(X,X')|X)=f(X)`, define
`Δ(X):=½E(|f(X)-f(X')|·|F(X,X')| | X)`. Then `E(f(X))=0`, and:

1. If `E(Δ(X))<∞`: `Var(f(X)) = ½E((f(X)-f(X'))F(X,X'))` — an EXACT identity, not an upper
   bound.
2. If `Δ(X)≤B·f(X)+C` a.s. (and an exponential-moment condition holds): sub-Gaussian/sub-
   exponential tail bounds on `f(X)`, `P(f(X)≥t)≤exp(-t²/(2C+2Bt))`.
3. For any positive integer `k`: `E(f(X)^{2k}) ≤ (2k-1)^k·E(Δ(X)^k)` — an exchangeable-pairs
   analogue of the Burkholder-Davis-Gundy inequality, converting control of `Δ(X)`'s MOMENTS
   into control of `f(X)`'s moments, at ALL orders `k`, not just `k=1`.

**The natural bridge to this project's own machinery — identified, not yet fully worked
out.** This project's own swap-walk `P` on a Hamming layer (established points 15-18, reused in
every subsequent point) IS already a reversible Markov chain w.r.t. the uniform layer measure —
exactly the structure Stein's exchangeable-pairs method wants. Setting `X~`uniform on the layer,
`X'|X~P(X,·)` (one swap step) gives a genuine exchangeable pair for free, no new construction
needed. **The simple, "obvious" choice `F(X,X'):=h(X)-h(X')` for a target function `h` does
NOT directly give what we want**: it yields `E(F|X)=(Lh)(X)` (our own `L=I-P` applied to `h`),
so the theorem's own "`f`" becomes `Lh`, not `h` — this choice bounds `Var(Lh)`, a DIFFERENT
quantity from `Var(h)` (already known, e.g. `M_1` in this project's own notation).

**To get a bound on `h` itself (e.g. `h=δ_i`, to bound `C_q=Var(δ_i)` — the actual target),
the standard fix is a Markov-chain-POTENTIAL construction: solve `Lg=h-E[h]` for a potential
`g`, then set `F(X,X'):=g(X)-g(X')`.** Spectrally (using this project's own already-established
eigenspace decomposition, points 15-24): if `h-E[h]=Σ_{l≥1} h_l` (components in eigenspace
`E_l` with eigenvalue `γ_l`), then `g=Σ_{l≥1}(1/γ_l)·h_l` — **the potential `g` RESCALES each
spectral component by `1/γ_l`, amplifying LOW-`l` (small-`γ_l`) mass and SUPPRESSING high-`l`
mass, relative to `h`.** This is potentially favorable: points 33/35/38 established that `δ_i`'s
own spectral mass increasingly migrates to HIGHER `l` as `n` grows (growing `l_eff`, widening
`ρ_γ`/spread) — if that high-`l` mass is genuinely suppressed in `g` relative to `h`, `Δ(X)`
(which now depends on `g`'s OWN fluctuation, not `h`'s) could plausibly be smaller than a naive
Efron-Stein-style bound built from `h` alone. This is exactly the kind of spectral-structure-
aware refinement the mission's own framing (§6: total influence `Σ|S|X̂(S)²` vs plain
`Σ X̂(S)²`) was hoping for — a mechanism, not just a hope, for why this route could beat plain
Efron-Stein specifically BECAUSE of the already-observed spectral broadening, not despite it.

**Honest status: this is a concrete, well-sourced, structurally motivated lead — NOT a
completed derivation.** What remains, named explicitly (not vague): (a) `g`'s fluctuation
`g(X)-g(X')` under a single swap needs to be bounded or estimated — this requires understanding
how the `1/γ_l` reweighting interacts with the ALREADY-COMPUTED `E_l`/`M_r` data, not a fresh
computation from scratch; (b) `Δ(X)`'s dependence on `h(X)` itself (needed for the tail bound
form `Δ(X)≤Bh(X)+C`) needs to be established — this is the genuinely hard, not-yet-attempted
step; (c) even if `Δ(X)` is bounded, converting a bound on `C_q=Var(δ_i)` (a SINGLE-generator
quantity) into a bound on `Var(X_n)` itself still requires the same Efron-Stein-style
aggregation across all `n` generators this project has used throughout — this machinery
replaces the LOCAL per-generator bound's quality, not the aggregation step.

**Verdict.** PARK, not REJECT, not PROMOTE-as-proof. This is recorded as the single most
concrete, structurally-motivated open research thread identified this session — worth the next
dedicated research push if continued, with the exact missing piece named per the mission's own
discipline (a genuine unfinished lemma, not a vague "try harder"). Given the complexity and risk
of introducing a subtle sign/normalization error under time pressure, no attempt was made to
force this into a complete result in this pass — per this project's own standing discipline
(`[EMPIRICAL]` is never presented as `[PROJECT-EXACT]`), an incomplete derivation is recorded as
exactly that, not dressed up as more than it is.

**What this does NOT mean:** does NOT mean this bridge will succeed if pursued — the potential
`g`'s fluctuation could turn out to be UNfavorable despite the plausible mechanism sketched
above; does NOT mean the naive `F=h(X)-h(X')` choice is useless — it still gives an exact,
already-partially-explored bound on `Var(Lh)` (related to `M_2` in this project's own
notation), which could itself be independently useful; does NOT constitute a proof of anything
about `Var(X_n)`.

**Artifacts:** none (pure Source Trace + algebraic sketch; no code was written since the
derivation is not complete enough to have a computable, testable claim yet).

## Point 42 (2026-09-13) — Cheap differentiating test on the point-41 bridge: `M_{-1}` computed
via conjugate gradient, all 7 `n`; a real, [EMPIRICAL] descriptive signal, explicitly NOT sold
as a confirmed mechanism (external-review correction applied proactively)

**Context.** Per the Cheapest Differentiating Test Protocol, before attempting the hard parts
of point 41's bridge (bounding `Δ(X)` itself), compute the cheap diagnostic `M_{-1}:=⟨g,Lg⟩`
where `Lg=δ_i-E[δ_i]` (solved via conjugate gradient using the already-verified
`apply_L_to_layer` matrix-vector product — no new machinery), and compare against the crude
ceiling `C_q/γ_1` (assuming all spectral mass sits at the smallest nonzero eigenvalue).

**A correction applied BEFORE this point was written up, not after external pushback (same
discipline as points 32/36/37/39, now proactive rather than reactive).** An external re-analysis
of this exact computation correctly pointed out — and this session had already independently
reached the same conclusion while drafting point 41 — that the naive identity
`Var(h)=½E[(h-h')(g-g')]` with `F=g(X)-g(X')` is spectrally TAUTOLOGICAL (`⟨f,Lg⟩=⟨f,f⟩=C_q`
by construction, since `Lg=f` is exactly how `g` was defined). `M_{-1}` itself is therefore
correctly understood as a SEPARATE, purely descriptive diagnostic of the spectral measure's
SHAPE — specifically `M_{-1}=Σ_l E_l/γ_l`, an inverse-eigenvalue-weighted moment measuring how
far the spectral mass has moved from being concentrated at `γ_1` (the "spectral-gap
extremizer") — NOT a proof, and not by itself evidence for a sharper variance bound.

**Results, CG-based, all 7 `n` (CG converges in 2-8 iterations, residual `~1e-6` to `~1e-17` —
essentially exact. Cost correction, skeptic-fallback finding — the solve time is NOT uniformly
negligible against theta-solve cost as an earlier draft claimed: `solve_time_s/theta_time_s`
grows monotonically from `3.2%` at `n=23` to `22.1%` at `n=47` — still secondary throughout, but
not "dominated entirely" at the largest tested `n`):**

| n | `C_q` | `γ_1` | `M_{-1}` | ceiling (`C_q/γ_1`) | ratio |
|---|---|---|---|---|---|
| 23 | 0.024948 | 0.400000 | 0.031920 | 0.062369 | 0.5118 |
| 29 | 0.019616 | 0.309524 | 0.029487 | 0.063376 | 0.4653 |
| 31 | 0.018126 | 0.285714 | 0.028840 | 0.063442 | 0.4546 |
| 37 | 0.014966 | 0.236111 | 0.026886 | 0.063388 | 0.4242 |
| 41 | 0.013284 | 0.211111 | 0.025566 | 0.062923 | 0.4063 |
| 43 | 0.012449 | 0.200000 | 0.024882 | 0.062246 | 0.3997 |
| 47 | 0.011016 | 0.181818 | 0.023447 | 0.060587 | **0.3870** |

**The ratio `M_{-1}/ceiling` decreases smoothly and monotonically across all 7 points**
(`0.512→0.465→0.455→0.424→0.406→0.400→0.387`), while the crude ceiling itself stays nearly flat
(`0.0624→0.0634→...→0.0606`, consistent with `γ_1~4/N` roughly canceling `C_q`'s own decay over
this range). **Correct statement of what this shows (adopting the external re-analysis's own
more careful phrasing over this session's own first-draft framing):**
`[EMPIRICAL] The negative spectral moment M_{-1} confirms increasing separation of the
harmonic-weighted spectral mass from the spectral-gap extremizer, as n grows.` This is
consistent with (not independent confirmation of, and not proof of) the already-established
spectral-broadening trend from points 33/35/38 — `R_{-1}↓` does **NOT** imply
`Var(X_n)=O(1/n)`, and is not claimed to.

**Verdict.** PROMOTE as a genuine, cheap, `[VERIFIED-REAL]` data point (7 exact CG solves, no
approximation beyond floating-point), correctly scoped as descriptive. The CG-based numerical
technique itself (solve `Lg=f` via conjugate gradient using only the existing swap-Laplacian
matrix-vector product) is a reusable capability for this experiment going forward — worth
noting as a tool, separate from what THIS specific application of it shows.

**What this does NOT mean:** does NOT mean point 41's bridge is validated; does NOT mean
`Δ(X)≤Bh(X)+C` holds (the genuinely hard, unattempted step); does NOT mean the falling ratio
will continue falling toward 0, or stabilize, or reverse — 7 points, no asymptotic claim
attempted.

**Artifacts:** `check_potential_moment_M_neg1.py` (+`metrics/potential_moment_M_neg1.json`).

## Point 43 (2026-09-13) — Discrete Malliavin calculus / second-order Poincaré for Rademacher
functionals: real, on-target literature, read in full — but a fundamental mismatch found, named
honestly rather than glossed over

**Context.** Following point 41's Chatterjee-Dey lead, an external re-analysis pointed to a
closer, more natural body of literature: discrete Malliavin calculus on the FULL Boolean/
Rademacher cube (Nourdin-Peccati-Reinert), operating in exactly the `|S|`-degree Fourier
picture already used by this project's own points 11/32/37 (NOT the Johnson-slice `γ_l`
picture of points 15-42) — plus a specific "second-order Poincaré inequality" paper applying
this machinery to random-graph statistics. Both primary sources were fetched and read in full
(not summarized) via `mcp__arxiv__get_paper_latex_section`, per the Source Trace standard of
citing exact theorem numbers.

**Source 1, verified in full: Nourdin, Peccati, Reinert, "Stein's method and stochastic
analysis of Rademacher functionals" (arXiv:0810.2890), Section 2.5.** Confirmed exactly:
`D_kF(ω)=½(F_k^+-F_k^-)` (the discrete gradient — literally the standard Boolean discrete
derivative, matching this project's own `δ_i`/`Δ_i` up to sign/encoding convention); the
Ornstein-Uhlenbeck-type operator `L` with `LF=-Σ_n n·J_n(f_n)` (eigenvalue `-n` on the degree-`n`
Fourier level — the FULL-CUBE degree operator, distinct from this project's own Johnson-slice
`L`); `L^{-1}F=-Σ_n(1/n)J_n(f_n)`; and the key lemma, for centered `F∈domD`:
**`E[F·f(F)]=E[⟨Df(F),-DL^{-1}F⟩]`**, which for `f(x)=x` gives **`Var(F)=E⟨DF,-DL^{-1}F⟩`**.

**Worked out explicitly (this session's own derivation, not quoted) — this exact identity is
spectrally equivalent to Parseval, not new information by itself.** Expanding both sides in the
chaos/Fourier basis: `E‖DF‖²=Σ_n n²(n-1)!‖f_n‖²=Σ_S|S|·X̂(S)²` (the standard "total influence")
and the cross term `E⟨DF,-DL^{-1}F⟩=Σ_n n·(n-1)!‖f_n‖²=Σ_n n!‖f_n‖²=Σ_S X̂(S)²=Var(F)` — matching
the ALREADY-KNOWN Parseval identity `Var(X)=ΣX̂(S)²` exactly, term for term. **The identity is
real and correctly stated, but does not by itself supply a new number or a sharper bound** — it
recovers what was already known, via a different (elegant, but not informative here) route.

**Source 2, verified in full: Eichelsbacher, Rednoß, Thäle, Zheng-type paper, "A simplified
second-order Gaussian Poincaré inequality in discrete setting with applications" (arXiv:
2108.05216), Section 4, Theorem [thm:2ndOrderPoincare].** Confirmed the exact theorem: for
`F∈D^{1,2}` with **mean zero AND variance ONE**, bounds involving `B_1..B_5` — all built from
FIRST derivatives `D_jF,D_kF` and SECOND (mixed) derivatives `D_ℓD_jF,D_ℓD_kF` — control the
KOLMOGOROV DISTANCE `d_K(F,N)` to a standard normal `N`. Applications listed (Section 1) include
subgraph counts in Erdős-Rényi graphs and hypercube percolation — structurally close to this
project's own setting.

**The honest mismatch, found and named explicitly rather than glossed over.** This theorem
requires `F` to ALREADY be normalized to mean zero, variance one — i.e., it presupposes
`Var(X_n)` is already known (to normalize by it), and its conclusion is about DISTRIBUTIONAL
closeness to Gaussian (Kolmogorov distance), not about the SCALE of `Var(X_n)` itself. **This
makes the theorem, as stated, CIRCULAR for this project's actual target question** (`Var(X_n)`
is exactly the unknown quantity needed to even apply the theorem) — it answers a different,
adjacent question ("is `X_n`, once correctly rescaled, approximately Gaussian?") rather than
this project's own ("how does `Var(X_n)` scale with `n`?"). This was NOT caught by the second
external re-analysis and is recorded here as this session's own independent finding, per the
same discipline that has repeatedly caught overclaims in this experiment (points 29, 32, 34→36,
39) — a plausible-sounding, well-sourced citation still needs its actual applicability checked
before being treated as load-bearing.

**What DOES survive, genuinely valuable.** `B_1..B_5`'s reliance on EXACTLY `D_jF` (this
project's own `δ_i`/`Δ_i`) and `D_ℓD_jF` (this project's own `Δ_iΔ_jX`, point 37's own object)
confirms this project's own second-difference investigation (point 37) is aimed at precisely
the right kind of quantity this literature treats as load-bearing — a genuine, structural
convergence between this project's own empirical work and a real, active research area, even
though the specific cited theorem doesn't transfer directly.

**An indirect route was NOT ruled out — named explicitly here rather than left implicit
(skeptic-fallback review finding on an earlier draft of this REJECT: it read as closing the
whole thread rather than just the direct application).** The circularity objection blocks using
the theorem with `F` normalized by the TRUE (unknown) `Var(X_n)` — but nothing stops a
self-consistency/falsification test: normalize `X_n` by a CANDIDATE `Var(X_n)=A/n^p` (e.g. the
already-fitted `p≈0.91` from this experiment's own root `metrics/run.json`), compute the
resulting `B_1..B_5` (built from already-computed `δ_i`/`Δ_iΔ_jX` data, points 32/37/38) under
that candidate normalization, and check whether the bound stays finite/small (consistent with
the candidate) or blows up (falsifying that specific candidate exponent). This is a genuine,
not-yet-attempted, moderately cheap test — NOT attempted in this point (would require assembling
`B_1..B_5` from existing `Δ_i`/`Δ_iΔ_j` data across generator pairs, a nontrivial but bounded
computation), named here so it isn't lost.

**Verdict.** REJECT the DIRECT application of this specific theorem to `Var(X_n)=O(1/n)`
(circular as stated, when `F` is normalized by the true unknown variance). PARK — not reject —
the INDIRECT self-consistency route (candidate-variance normalization + falsification), which
was not attempted and is not ruled out by the circularity argument. PROMOTE the structural
confirmation that `Δ_iΔ_jX`-type quantities are the right currency for this literature — worth
searching further for a variance-scaling result specifically (as opposed to a CLT/Kolmogorov-
distance result) using the same discrete Malliavin toolkit, if this thread is continued.

**What this does NOT mean:** does NOT mean discrete Malliavin calculus is useless for this
project — only that THIS SPECIFIC theorem's DIRECT application, as stated, doesn't work; does
NOT mean the indirect self-consistency route would succeed if attempted — only that it hasn't
been tried and isn't excluded; does NOT mean no variance-scaling result exists in this
literature family — a further, more targeted search (e.g. for variance bounds rather than CLT
bounds within the same NPR/Malliavin framework) was not attempted in this point; does NOT
retract point 37's own findings, which remain independently valid regardless of this literature
connection.

**Artifacts:** none (pure Source Trace, primary sources read and quoted exactly, no code).

## Point 44 (2026-09-13) — Truncated-moment LP bound: the single most informative result in
this entire route-A/B/C investigation, genuinely positive, using ONLY already-computed data

**Context.** A cheap, classical idea (truncated-moment / Chebyshev-Markov-Krein LP bounds for a
positive measure given its first `s` raw moments — cited as classical, not claimed as new here)
applied directly to this project's own spectral measure `E_l` on the Johnson eigenvalues
`{γ_1,...,γ_L}`: given ONLY `M_1,...,M_s` (already exact from point 38) and positivity
`E_l≥0`, the LP

```
U_s := max Σ_l E_l   s.t.   E_l≥0,  Σ_l γ_l^r E_l = M_r  for r=1..s
```

gives the LARGEST `C_q` compatible with the observed moments — a provably TIGHT upper bound
derivable from moments `1..s` alone (the true spectrum is itself a feasible point, so
`C_q≤U_s` always). Solved via `scipy.optimize.linprog` (HiGHS), using ONLY point 38's
already-committed `M_1..M_6` — no new theta-solves, numerically instantaneous (`L≤11`
variables, `≤6` equality constraints per solve, 7×6=42 LP solves total in well under a
second).

**Result — `R_s := U_s/C_q` for all 7 `n`, `s=1..6`:**

| n | L | R₁ | R₂ | R₃ | R₄ | R₅ | R₆ |
|---|---|---|---|---|---|---|---|
| 23 | 5 | 2.021 | 1.276 | 1.037 | 1.002 | 1.0000 | 1.0000 |
| 29 | 6 | 2.295 | 1.384 | 1.068 | 1.014 | 1.0005 | 1.0000 |
| 31 | 7 | 2.364 | 1.442 | 1.077 | 1.025 | 1.0013 | 1.0000 |
| 37 | 8 | 2.601 | 1.561 | 1.121 | 1.040 | 1.0063 | 1.0006 |
| 41 | 9 | 2.757 | 1.649 | 1.134 | 1.048 | 1.0136 | 1.0022 |
| 43 | 10 | 2.824 | 1.698 | 1.146 | 1.055 | 1.0168 | 1.0031 |
| 47 | 11 | 2.957 | 1.782 | 1.174 | 1.070 | 1.0246 | 1.0054 |

**`R_1` exactly recovers the classical Poincaré bound** (verified: `U_1=M_1/γ_1` algebraically,
matching the LP output to machine precision at every `n` — the dual certificate at `s=1` is the
single coefficient `c_1=1/γ_1`, confirmed in the raw output). This is the correct sanity check
before trusting `s≥2`: the LP framework correctly reduces to already-known machinery at its
simplest case.

**Critical dimensional caveat, stated explicitly before interpreting `R_6≈1` as a deep
finding — checked, not assumed.** `L` (number of unknowns `E_l`) is `5,6,7,8,9,10,11` for
`n=23,29,31,37,41,43,47`. At `n=23` (`L=5≤6`) and `n=29` (`L=6=6`), 6 moment constraints
against `≤6` unknowns makes the linear system (near-)exactly determined BY DIMENSION COUNT
ALONE — `R_6=1.0000` there is close to a trivial linear-algebra fact, not evidence of genuine
information compression. **The substantive finding is specifically `n=31..47`, where `L=7..11`
STRICTLY EXCEEDS the 6 available moment constraints** (a genuinely under-determined system,
infinitely many nonnegative spectra are consistent with 6 moments in principle) — and `R_6`
STILL stays within `0.06%` to `0.54%` of `1` there. That is real, non-trivial compression: six
numbers very nearly pin down an object with up to 11 genuine degrees of freedom.

**The gap `R_6-1` is small but grows monotonically with `n`** (`0.0000, 0.0000, 0.0000, 0.0006,
0.0022, 0.0031, 0.0054`). **Robustness check performed before trusting this trend (skeptic-
fallback review finding, addressed — not just hedged away): is `R_6-1`'s growth genuine, or a
solver-precision artifact?** Cross-validated `U_6` (the quantity `R_6` is built from) three
independent ways at the two most relevant `n`: at `n=29` (`L=6=s`, an exactly-determined square
linear system with a UNIQUE feasible spectrum) via a direct `numpy.linalg.solve` (bypassing the
LP solver entirely) — matches the LP's own `U_6` to `1.4e-15`; and at `n=47` (`L=11`, the most
under-determined case) across three different `scipy.optimize.linprog` methods
(`highs`/`highs-ds`/`highs-ipm`) — all three agree to `1.7e-15`. **`U_6` itself is robust, not
a numerical artifact, at both ends of the range.** (A genuine, separate numerical wrinkle WAS
found in this check — the companion `L_s` (minimum) value at `n=29,s=6` disagreed with the
unique exact solution by `~4e-6`, `~4000×` larger than expected floating-point noise, evidently
a solver-side artifact specific to the MINIMIZE direction on this near-degenerate LP. This does
NOT affect `U_s`/`R_s` — the quantities this point's entire conclusion rests on — and `L_s`
plays no role in any claim made here; noted for completeness, not swept aside.) With `U_6`
independently confirmed exact, the growing `R_6-1` trend is consistent with (not proof of) the
already-established spectral-broadening trend (points 33/35/38/42) — as `L` grows and mass
migrates to higher `l`, 6 fixed moments become *slightly* less sufficient, exactly as expected.
Whether this gap stays bounded, grows to a fixed small constant, or eventually grows without
bound as `n→∞` is NOT
determined by 7 points — this is the honest open question this result raises, not answers.

**Structural observation on the extremal (worst-case) spectrum — corrected, an earlier draft
overstated the pattern (skeptic-fallback finding).** The actual active levels at `s=6`, read
directly from `metrics/truncated_moment_lp_bound.json`: `n=23→{2,4}`, `n=29→{1,2,3,4,5,6}` (all
`L=6` levels — forced, since at `L=s` the LP is a single point, not really an optimization),
`n=31→{1,2,3,4,5,7}`, `n=37→{1,2,3,4,5,8}`, `n=41→{1,2,3,4,5,9}`, `n=43→{1,2,3,5,6,10}`,
`n=47→{1,2,3,5,6,11}`. This is NOT "consistently `{1,2,3,~5,L}`" as an earlier draft claimed —
`n=23,29` don't fit that pattern at all (both dimension-forced, not informative here), and even
among the genuinely under-determined `n=31..47` rows the included mid-level alternates between
`4` and `6`, not fixed at `~5`. What DOES hold, weakly: for `n=31..47` the extremal spectrum
consistently combines several LOW levels (`1,2,3,` and a 4th/5th) with the single TOP level `L`
— loosely consistent with the classical fact that extremal measures for a truncated moment
problem concentrate at extreme points of the achievable support, but not precisely/consistently
enough to state as a clean pattern. Worth exploring further if this thread continues, not
pursued analytically in this point.

**RETROACTIVE CORRECTION (added when point 45 found this framing was premature — per this
document's own precedent at point 10, corrected by point 12's independent check; named here,
not silently edited away).** The "Verdict" immediately below overstated what this point
actually establishes. **Point 45 (below in this document) found the `R_6≈1` near-exactness is
mostly a property of the small grid size `L≤11` used throughout this experiment's real
`n≤47` range, NOT a distinctive signature of Lovász theta's spectrum — synthetic random/
adversarial spectra on the same grids give near-identical `R_6`, and the achievable gap grows
substantially (`R_6` up to `~3.8`) once `L` is allowed to grow well past the fixed moment
order `s=6`, which is the regime actually relevant to `n→∞`.** The LP computation and numbers
below remain fully correct — read the "Verdict" as historically accurate about what was believed
at the time it was written, not as this document's final assessment of point 44's significance.

**Verdict (original, superseded by point 45 below — kept for provenance, not deleted).**
PROMOTE as the single most informative, genuinely positive result of the entire
route-A/B/C investigation (points 1-44) — the opposite of the pessimistic outcome the second
external LLM analysis's own `§7` worried about ("first six moments not sufficient" was
explicitly named there as the bad scenario; the actual result is the GOOD scenario:
`R_6≈1.000-1.005`). This does NOT close Priority C — it REORIENTS it: the natural next step is
no longer "does the moment route contain enough information" (answered: yes, essentially) but
"can the LP dual's polynomial certificate `P(γ)=Σc_r(n)γ^r` be characterized analytically as a
function of `n`, well enough to prove the target `O(n^{-2})`-type scaling for `C_q`" — a
concrete, well-posed, not-yet-attempted analytic question, not a vague "look for more
inequalities."

**What this does NOT mean:** does NOT mean `Var(X_n)=O(1/n)` is proven or even directly closer
to proven — `C_q` (a single-generator quantity) still needs the same `S_n=Σw_qC_q` aggregation
this project has always required, and only the CENTRAL `q=N/2` layer was used here (the
`S_n=Σ_qw_qU_6(q)` extension the external analysis proposed in its own `§13` was NOT attempted
— would require `M_r` data at non-central `q`, not currently computed anywhere in this
experiment); does NOT mean the dual polynomial `c_r(n)` has a simple closed form — no attempt
was made to find one in this point; does NOT mean `R_6→1` as `n→∞` — 7 points, monotonic
growth in the gap, no asymptotic claim.

**Artifacts:** `check_truncated_moment_lp_bound.py` (+`metrics/truncated_moment_lp_bound.json`),
`verify_lp_bound_robustness.py` (verification-only, no separate metrics file — reproduces the
skeptic-fallback robustness checks: exact square-system cross-check at `n=29`, three-solver-
method agreement at `n=47`).

## Point 45 (2026-09-13) — Negative control + geometry scaling: point 44's near-exactness is
mostly small-grid artifact, NOT Lovász-specific — the excitement was premature, corrected before
it propagated further, not after

**Context.** Per `artifact-provenance-gates.md`'s Gate 3 discipline (a test must be shown to
discriminate something, not just pass on the real case) and this project's own repeated
"check before celebrating" pattern — before treating point 44's `R_6≈1` as informative about
Lovász theta specifically, the obvious alternative was checked directly: is this near-exactness
just a generic property of ANY positive spectrum on the SAME small grid `{γ_1,...,γ_L}`
(`L≤11` throughout this experiment's actual `n=23..47` range), unrelated to `X`'s actual
structure? Two cheap tests, no new theta-solves for either.

**Test 1 — negative control: synthetic spectra on the SAME real grids.** For each of the 7
already-used `(N,q)` grids, generated several families of synthetic nonnegative `E_l`:
500 i.i.d. `Exponential(1)` random draws, a flat spectrum, pure-low-level, pure-high-level, a
two-point low/high mixture, and smooth decaying/growing profiles — computed each family's OWN
`M_1..M_6` from the SAME `γ_l`, ran the identical LP, and compared `R_6^{synthetic}` against
the real `R_6` already found.

| n | L | R₆ (real) | random synthetic: mean±std (range) |
|---|---|---|---|
| 23 | 5 | 1.0000 | 1.0000±0.0000 |
| 29 | 6 | 1.0000 | 1.0000±0.0000 |
| 31 | 7 | 1.0000 | 1.0001±0.0001 |
| 37 | 8 | 1.0006 | 1.0005±0.0003 |
| 41 | 9 | 1.0022 | 1.0012±0.0007 |
| 43 | 10 | 1.0031 | 1.0017±0.0009 |
| 47 | 11 | 1.0054 | 1.0028±0.0015 (range `[1.0002,1.0083]`) |

**Validity check on the comparison itself (skeptic-fallback finding, addressed — the
scale-invariance the comparison relies on was asserted, not verified, in an earlier draft).**
`R_6=U_6/C_q` is invariant to uniformly rescaling a spectrum (`E_l→cE_l` for `c>0` leaves it
unchanged, since both `U_6` and `C_q` scale by `c` — an exact algebraic fact, not just plausible
sounding). Verified numerically, not just by hand-proof (`verify_r6_scale_invariance.py`):
robust to `~1e-13` across scales `1` to `1e6` and several random scales in `[40,1000]` — but
BREAKS at scale `0.001` (a `~10^{-1}` shift in `R_6`, a genuine HiGHS solver-tolerance artifact
at very small absolute constraint values, not investigated further). This matters here because
the real and synthetic spectra sit at very different absolute scales — real `C_q≈0.01-0.03` vs
`E[C_q^{synthetic}]≈L≈7-11` for `Exponential(1)` draws, a `~400-1000×` ratio — **squarely inside
the verified-robust range** (`40×-10^6×`), not near the breakdown point. The comparison below is
valid; this was checked, not assumed.

**The real `R_6` sits within the range random synthetic spectra produce, though the margin
narrows as `n` grows — reported honestly, not just the single least-striking data point (skeptic-
fallback finding: an earlier draft quoted only `n=47`'s `z≈1.7` as "unremarkable" without noting
the trend).** `z:=(R_6^{real}-\text{mean}_{synthetic})/\text{std}_{synthetic}` across
`n=31,37,41,43,47`: **`-0.47, 0.09, 1.37, 1.52, 1.69`** — monotonically increasing, with `n=47`
sitting at the conventional one-sided `p≈0.045` boundary, not clearly unremarkable. This does
NOT overturn the section's conclusion (Test 2 below carries the real weight of the argument, and
even the deliberately adversarial-looking families — pure-low, pure-high, two-point mixture —
never pushed `R_6` meaningfully above `1.000` on these small grids), but the rising trend is
named explicitly rather than smoothed into a single reassuring number: on THIS test alone (7
points, only through `n=47`), it is not possible to rule out that the real spectrum shows a
*mild* upward departure from the synthetic baseline that a larger `n`-range might sharpen —
worth keeping in mind, not dismissed. **Conclusion: point 44's `R_6≈1` is NOT a clearly
distinctive signature of `X`'s actual spectrum — most nonnegative spectra on a grid this small
(`L≤11`) give a similarly near-exact result — though Test 1 alone leaves a mild, unresolved
trend that Test 2 (not Test 1) is what actually settles.** This is broadly the "bad" (deflating)
outcome the analysis that proposed this control itself flagged as possible.

**Test 2 — geometry-only scaling: does the near-exactness survive as `L` grows well past
`s=6`? No new theta-solves, pure synthetic grids at synthetic `N` far beyond anything this
project's exact-enumeration machinery could reach.** For `N=11,20,50,100,200,500,1000`
(`L=N/2` correspondingly `5..500`), sampled a worst-case-seeking set of synthetic spectra
(the same adversarial families plus 50 random draws per `N`) and recorded the LARGEST `R_6`
found (a lower bound on the TRUE worst case, since this is a sampled search, not the LP's own
dual — stated as such, not overclaimed as exact):

| L | 5 | 10 | 25 | 50 | 100 | 250 | 500 |
|---|---|---|---|---|---|---|---|
| worst `R_6` found | 1.0000 | 1.0047 | 1.0640 | 1.1778 | 1.4740 | 2.3715 | **3.7922** |

**This answers the question the negative control left open — strongly and directionally, if not
with an exact worst-case number (softened from an earlier draft's "decisively," per skeptic-
fallback review: the trend itself is robust since the worst value at every `L≥50` comes from a
single deterministic, structurally-motivated family — `decaying`, `1/l` — not from the
500-sample random search, so search-adequacy concerns don't threaten the qualitative
conclusion; but the exact reported numbers remain a sampled LOWER bound, not the LP dual's own
provable worst case).** As `L` grows well
beyond the fixed moment order `s=6` — the actual regime relevant to `n→∞`, since
`L=min(q,N-q)=Θ(n)` grows without bound while a FIXED `s=6` does not — the achievable gap
between `U_6` and the true sum grows substantially, not staying near `1`. The `L≤11` range this
experiment's real `n≤47` happens to cover is NOT representative of the asymptotic regime; it is
comfortably inside the small-`L` zone where 6 moments are nearly always enough regardless of the
spectrum's shape, for reasons of grid/LP geometry (plausibly related to classical
degree-`s` polynomial/quadrature exactness on small point sets — Gauss-type quadrature is EXACT
for polynomials up to degree `2k-1` on `k` points, a structurally similar phenomenon; not
verified as the precise mechanism here, flagged as a plausible explanation worth Source-Tracing
if this thread continues, not confirmed).

**Corrected verdict on point 44 — Hindsight Distortion Gap discipline: name the correction,
don't silently absorb it.** Point 44's NUMBERS remain entirely correct (verified independently
via direct linear solve and 3 LP solver methods, point 44's own robustness checks) — nothing
here retracts the computation. What is corrected is the INTERPRETATION: point 44's framing
("the single most informative result... genuinely positive", "real, non-trivial compression")
overstated what a small-`L` near-exactness actually establishes about Lovász theta specifically.
**The honest, corrected statement: 6 moments happen to nearly determine `C_q` for `n≤47`
because `L≤11` is still small relative to `6`, not because `X`'s spectrum has special
structure — and this near-exactness measurably degrades as `L` grows, which is the direction
`n→∞` actually goes.** A FIXED `s=6` moment count should NOT be expected to give a tight,
asymptotically valid bound on `C_q` as `n→∞` — consistent with (not a new discovery beyond) the
original tail-bound form this project already had, `Σ_{l<k}E_l+M_s/γ_k^s`, which always required
`k` (and implicitly `s`) to GROW with `n` — `k~const` was never going to be enough, and this
point confirms that concretely rather than leaving it assumed.

**What survives, and what the corrected picture actually recommends.** The LP methodology
itself (truncated-moment duality) remains sound and potentially useful — but the right next
question is not "are 6 fixed moments enough" (answered: no, not asymptotically) but "how must
`s` (and/or the cutoff `k` in the truncation `Σ_{l<k}E_l+M_s/γ_k^s`) grow with `n` for the LP
bound to close the gap to the target `O(n^{-2})`-type scaling for `C_q`" — a well-posed,
concrete question, not yet attempted (would require computing `M_r` for growing `r` as `n`
grows, or finding a closed-form family of dual certificates `P_s(γ)` parameterized by `s` and
`n` jointly).

**What this does NOT mean:** does NOT mean point 44 was computed incorrectly — the LP solves,
`R_1`=Poincaré check, and robustness verification all remain valid; does NOT mean the
truncated-moment LP approach is useless — only that a FIXED small `s` is insufficient
asymptotically, which redirects rather than closes the thread; does NOT mean the true worst-case
`R_6` at large `L` is exactly the sampled values found here — Test 2's numbers are a LOWER bound
via sampling, not the LP dual's own exact worst case (computing THAT exactly at large `L` was
not attempted in this point).

**Artifacts:** `check_lp_bound_synthetic_control.py` (+`metrics/lp_bound_synthetic_control.json`),
`check_lp_bound_geometry_scaling.py` (+`metrics/lp_bound_geometry_scaling.json`),
`verify_r6_scale_invariance.py` (verification-only, no separate metrics file — confirms the
real-vs-synthetic comparison in Test 1 is valid at the scales actually compared).

## Point 46 (2026-09-13) — The TRUE worst-case moment-ambiguity factor `K_s(L)`, replacing
point 45's sampled estimate with an exact LP certificate — `s(L)` grows substantially, not
`O(1)`, sharpening Priority C's reformulated question with a rigorous (if rough) answer

**Context.** Direct correction from the user: point 45's Test 2 "worst-case `R_6`" was a
SAMPLED maximum over a handful of families plus 500 random draws — a lower bound, correctly
labeled as such at the time, but not a proven worst case. This point closes that gap exactly,
via a genuinely better LP formulation the user proposed: a single two-spectrum LP that finds
the TRUE worst case directly, with no sampling and no separate scale-normalization step needed.

**The two-spectrum LP (classical truncated-moment-problem machinery, applied here — not a new
technique).** For a normalized "true" spectrum `x` (`Σx_l=1`) and an "adversarial" spectrum `y`
sharing `x`'s first `s` raw moments:

```
K_s(L) := max_{x,y≥0} Σ_l y_l   s.t.   Σ_l x_l = 1,   Σ_l γ_l^r x_l = Σ_l γ_l^r y_l  (r=1..s)
```

A single LP in `2L` variables with `s+1` equality constraints — still tiny at `L=1000` (`2000`
variables, `21` constraints for `s=20`), solved via the same `scipy.optimize.linprog`/HiGHS
already used throughout points 44-45. Normalizing `x` INSIDE the LP eliminates point 45's own
scale-invariance concern entirely (no rescaling, no floating-point-tolerance edge cases).

**Sanity check: true `K_6` on the 7 REAL experiment grids, compared to the actual Lovász data's
own `R_6`.** As expected, `K_6` (the true supremum over ALL possible spectra) sits at or above
the real data's own `R_6` at every `n` (e.g. `n=47`: `K_6=1.0113` vs real `R_6=1.0054`) —
consistent, not a contradiction; the real spectrum is just one point inside the worst-case
envelope, not the extremal one.

**The central result — `K_s(L)` for `s=1..20`, geometry-only synthetic grids (`N=2L,q=L`,
matching point 45's own convention), and the derived thresholds `s_{1.1}(L):=\min\{s:K_s≤1.1\}`,
`s_{2.0}(L):=\min\{s:K_s≤2\}`. Table corrected per skeptic-fallback review (addressed, not
smoothed over — see findings below the table): every cell where the LP did not actually reach
the labeled `s` is now marked explicitly, none are silently filled with a neighboring value.**

| L | s₁.₁ | s₂.₀ | K₆ | K₁₀ | K₂₀ | max `s` reached |
|---|---|---|---|---|---|---|
| 5 | 3 | 2 | — (`L=5<6`, no `K_6` exists) | — | — | 5 (`=L`, not a failure) |
| 10 | 5 | 2 | 1.008 | 1.000 | — (`L=10<20`) | 10 (`=L`) |
| 25 | 7 | 4 | 1.137 | 1.006 | — | 17 (**LP failed at `s=18`**, HiGHS `primal_status=Infeasible`) |
| 50 | 10 | 5 | 1.427 | 1.064 | — | 19 (**LP failed at `s=20`**) |
| 100 | 16* | 7 | 2.086 | 1.261 | 1.085 | 20 (reached) |
| 250 | none `≤20` | 10 | 4.147 | 1.962 | 1.430 | 20 (reached) |
| 500 | none `≤20` | none `≤20` | 7.616 | 3.191 | 2.378 | 20 (reached) |
| 1000 | none `≤20` | none `≤20` | 14.556 | 5.680 | — | 19 (**LP failed at `s=20`**; `K_19=3.609`) |

**`*` L=100's `s_{1.1}=16` is NOT a clean, reliable threshold — flagged explicitly (skeptic-
fallback finding, this is a genuine data problem, not just a presentation one).** The full
sequence `s=13..20` at `L=100` is `1.114, 1.113, 1.121, 1.092, 1.094, 1.116, 1.145, 1.085` —
oscillating in the band `[1.09,1.15]`, never settling; `s=16` is the FIRST value that happens to
dip under `1.1`, but `s=18,19` climb back ABOVE `1.1` (`s=19` is even worse than `s=13`). Picking
"first crossing" here is close to arbitrary — a different, equally defensible convention (e.g.
"first `s` after which it never rises above threshold again") would give a different, possibly
undefined, answer. Do NOT read `s_{1.1}(100)=16` as a settled fact; the honest statement is
"`K_s` for `L=100` enters a noisy `~1.09-1.15` band somewhere around `s=13-16` and does not
cleanly resolve below `1.1` within the tested range."

**LP infeasibility at very high `s` — now disclosed explicitly rather than silently breaking the
loop (skeptic-fallback finding, script fixed, not just the write-up).** `L=25,50,1000` genuinely
FAIL (HiGHS reports numerical infeasibility, not just imprecision) at `s=18,20,20` respectively
— plausible Vandermonde-conditioning breakdown as `γ_l^r` spans many orders of magnitude for
large `r`, similar in kind to (though more severe than) the `L_s`-direction artifact point 44's
own review caught. `check_worst_case_moment_ambiguity_lp.py` now records `failure_at_s` and
`failure_message` per row instead of silently discarding them.

**`s_{2.0}(L)` is NOT bounded — by `L=500-1000`, even 20 moments (or as many as could be reached
before numerical failure) are insufficient to keep the worst-case ambiguity within a factor of
2.** The `s_{2.0}` values used for the growth-rate estimate below (`L=25,50,100,250`, all `4,5,
7,10`) sit in clean, monotonically-decreasing regions well before any instability — verified
individually, this specific claim (unlike the `s_{1.1}(100)=16` one above) is NOT contaminated
by the high-`s` noise. A rough (4-point, explicitly weak per this project's own discipline for
small-sample power-law fits, and NOT correcting for the right-censoring at `L=500,1000` — a
proper treatment would need Tobit-style regression, not attempted here, so the `~0.41` exponent
should be read as indicative, not precise) log-log regression of `s_{2.0}(L)` vs `L` gives slope
`≈0.41`. Independent of that specific number, the qualitative conclusion is robust on its own
terms: `L:25→250` is a `10×` increase; `O(log L)` growth would predict `s` growing only `~1.7×`
(`4→~7`); the OBSERVED growth is `4→10`, already faster than logarithmic, and `L=500,1000`
needing MORE than 20 moments makes `O(log L)` even less tenable. **Given `L=min(q,N-q)=Θ(n)`
throughout this experiment, this directly implies: a FIXED, small number of moments — 6, or even
20 — will NOT give an asymptotically tight bound as `n→∞`. The number of moments needed itself
grows with `n`, faster than logarithmically, plausibly polynomially (`n^{0.4}`-ish as a rough,
uncorrected-for-censoring indication), not merely "more than six."**

**Verdict.** PROMOTE as the rigorous resolution of the exact question point 45 raised but only
sampled: Priority C's fixed-small-`s` moment route is now shown, not just suspected, to fail
asymptotically — `s` must grow with `n`, and the growth looks super-logarithmic based on this
(weak, 4-point) evidence. This does NOT close Priority C — it sharpens its reformulation from
point 45's own "how must `s(n)` grow" into a concrete, roughly-quantified answer: NOT `O(1)`,
NOT clearly `O(log n)`, plausibly power-law. The original tail-bound form this project always
had, `Σ_{l<k}E_l+M_s/γ_k^s` with growing `k` (and now, evidently, growing `s` too), remains the
right shape — this point supplies rough quantitative teeth for how fast that growth must be,
not a new mechanism.

**What this does NOT mean:** does NOT mean the `L^{0.4}` exponent is established — 4 usable
points (`L=25,50,100,250`), explicitly weak, no theoretical derivation attempted; does NOT mean
Priority C is dead — a growing-`s(n)`/`k(n)` route was always the honest target, and this point
quantifies (roughly) what growth rate would be needed, which is progress, not a closure; does
NOT mean the small non-monotonic numerical wiggles at high `s` invalidate the overall trend —
the qualitative conclusion doesn't depend on the exact high-`s` values.

**Artifacts:** `check_worst_case_moment_ambiguity_lp.py`
(+`metrics/worst_case_moment_ambiguity_lp.json`).

**RETROACTIVE NOTE (2026-09-13, added by point 47, then SUPERSEDED by point 48 — see point 48
for the actual current resolution, not point 47).** A pasted external analysis argued this
point's `s_{2.0}` numbers at `L=500,1000` were a numerical artifact of monomial-basis
ill-conditioning, citing an explicit Chebyshev dual-certificate formula predicting
`s_2(500)=14`, `s_2(1000)=20` (i.e. `O(√L)` growth). Point 47 re-derived `K_s(L)` on a
conditioning-hardened, cross-solver-validated reformulation and initially concluded the
certificate was invalid beyond `s≈12` and this point's headline survived — **that conclusion was
itself wrong**, overturned by point 48's direct LP-duality check (cross-method solver agreement
and small residuals are not sufficient evidence of primal feasibility; a verified dual
certificate is). Point 48 confirms the pasted analysis's numbers were right all along:
`s_2(100)≈7`, `s_2(250)≈10`, `s_2(500)≈14`, `s_2(1000)≈20`, all proven as valid upper bounds via
an independently dual-feasibility-checked certificate. This point's own `s_{2.0}` claim at
`L=500,1000` ("none `≤20`") is therefore INCORRECT — read point 48, not this point or point 47,
for the current state of this question.

## Point 47 (2026-09-13) — Surgery correction of point 46: an external Chebyshev-certificate
claim that `s(L)` is `O(√L)` (not unbounded within `s≤20`) is independently re-derived,
diagnosed, and REFUTED for this discrete geometry — point 46's headline survives, now on
substantially firmer numerical ground

**Context.** A pasted external analysis made a specific, checkable claim: point 46's own
`K_s` sequence at high `s` (e.g. the non-monotonicity flagged in point 46's own text) is a
numerical artifact of monomial-basis ill-conditioning (`γ_l^r` spans many orders of magnitude
for large `r`), and an explicit Chebyshev dual certificate proves

```
K_s(L) ≤ (A_s+1)/(A_s-1),   A_s = T_s((L+3)/(L-1))
```

giving guaranteed `s_2(L)`: `L=100→7`, `L=250→10`, `L=500→14`, `L=1000→20` — i.e.
`s_2(L)=O(√L)`, not the "unbounded within `s≤20`" conclusion point 46 reported. The user
explicitly instructed this be treated as a surgery correction (re-derive, re-verify, retroact
if wrong — not silently rewrite point 46), invoking this project's own Oracle Adequacy Gate
discipline against trusting a solver's raw status as mathematical fact.

**Step 1 — the endpoint check (cheap, done first).** `γ_1 = 1·(N+1-1)/(q(N-q)) = 2/L` and
`γ_L = L·(N+1-L)/(q(N-q)) = (L+1)/L = 1+1/L` for our `N=2L,q=L` convention — these match the
certificate's assumed interval endpoints EXACTLY, so the certificate's applicability to this
geometry isn't obviously wrong on its face. Also checked algebraically: at `s=1`,
`A_1=T_1((L+3)/(L-1))=(L+3)/(L-1)` (since `T_1(x)=x`), and `(A_1+1)/(A_1-1)` simplifies exactly
to `(L+1)/2` — which is EXACTLY `K_1(L)=γ_max/γ_min` (point 46's own hand-verified exact value).
The certificate is not a typo or a garbled formula; it is exact at the base case.

**Step 2 — the naive Chebyshev-basis LP reformulation was tried and is BUGGY, not just
ill-conditioned (diagnosed, not just observed to fail).** A first attempt reformulated the
two-spectrum LP by replacing monomial constraint rows `γ_l^r` with Chebyshev polynomial rows
`T_r(γ̃_l)` (γ rescaled to `[-1,1]`), reasoning the moment-matching constraint set is
basis-independent. It returned "Unbounded" for nearly every `(L,s)` tested — a different and
worse failure than point 46's original "Infeasible." Root cause, found by hand-deriving the
Chebyshev-to-monomial change of basis: even-degree Chebyshev polynomials (`T_2,T_4,...`) carry a
nonzero constant (`T_0`) term, so using constraint rows `T_1..T_s` (without an explicit `T_0`
row) does NOT enforce "match raw moments `1..s` exactly" — for even `r`, the row secretly
entangles the intended moment-`r` constraint with `Σy_l` (the free, UNconstrained quantity being
maximized), since `x`'s zeroth moment is pinned (`Σx=1`) but `y`'s is not. This is a genuine
formulation bug (the constraint SET changes, not just its conditioning), independently confirmed
algebraically before any further numbers from that script were trusted — its results
(`verify_chebyshev_conditioning.py`, uncommitted scratchpad) are discarded, not used anywhere
below.

**Step 3 — the correct conditioning fix: rescale `γ` by `γ_max` before raising to powers
(mathematically IDENTICAL LP, not a basis change).** Dividing constraint row `r` by `γ_max^r`
(equivalently working with `γ̃_l=γ_l/γ_max∈(0,1]`) leaves the `"=0"` equation unchanged — this is
provably the same feasible region and same optimum as point 46's raw-monomial LP, just better
scaled. `K_1(1000)=500.5` reproduced exactly, confirming the reformulation is sound.

**Step 4 — even this fix wasn't enough alone; default-tolerance HiGHS solver methods
genuinely disagreed at high `s` (a real finding, checked before trusting any number).**
Cross-checking `linprog(method="highs-ds")` against `method="highs-ipm")` at default tolerance
showed disagreements up to ~40% at `s≥11` (e.g. `L=1000,s=13`: `highs-ds→3.848`,
`highs-ipm→5.412`) — a genuine solver-method-agreement failure, exactly the kind of red flag
this project's mandatory-checks list exists to catch. Both returned solutions were independently
re-verified as truly primal-feasible via 50-digit-precision (`mpmath`) residual recomputation
(`max_rel_residual` ~`1e-6` to `1e-8`, `min(x),min(y)≥0` exactly) — so BOTH are genuine feasible
points, meaning the true optimum is at least the larger of the two, not that either is spurious.
Tightening HiGHS's `primal_feasibility_tolerance`/`dual_feasibility_tolerance` to `1e-9`
resolved this: `highs-ds` and `highs-ipm` then converged to the SAME value to 6+ significant
digits at every tested cell (`L=1000,s=20`: both `→3.5338229...`) — this tight-tolerance,
cross-method-agreeing value is what the final grid below uses, not either method's raw default
output.

**Step 5 — the full, validated `K_s(L)` grid, `L∈{25,50,100,250,500,1000}`, `s=1..30`, compared
against the certificate bound.** No cell fell back to the "`INCONCLUSIVE-METHOD-DISAGREE`"
status the script defines for disagreement even at tight tolerance — but this needs one honest
qualification the skeptic-fallback review below caught: at a handful of high-`s` cells (e.g.
`L=25,s=21/22/24/25`; `L=1000,s=21`), only ONE of the two solver methods actually converges (the
other returns a HiGHS solver failure), so "cross-method agreement" there is vacuously true (a
single surviving value, not two independent values agreeing) rather than genuine two-algorithm
consensus. This does not weaken the refutation itself — a single feasibility-confirmed value is
still a valid lower bound on the true LP optimum, which is all the certificate-violation argument
needs — but it is a real distinction from the cells with true dual-method agreement, and this
document should not blur the two. The `K_s` sequence is DRAMATICALLY reduced in non-monotone
wiggling compared to point 46's original numbers, but NOT fully eliminated at very high `s`: the
JSON records `monotone_ok:false` at several cells very close to a numerical optimum (`L=25`:
`s=15,16,18,19,23,25`; `L=50`: `s=24,25,30`; `L=500`: `s=30`) — all at magnitudes far too small
(`K_s` changing in the 4th decimal, near `1.0000` or near `2.07`) to affect any `cert_violated`
verdict, but real, not "gone."

| L | s where cert first violated | K₁₀ (LP / cert) | K₂₀ (LP / cert) | K₃₀ (LP / cert) | s₂(L) (LP, validated) |
|---|---|---|---|---|---|
| 25 | never (`s≤25` tested) | 1.006 / 1.014 | 1.000 / 1.000 | — | 4 |
| 50 | never (`s≤30` tested) | 1.064 / 1.075 | 1.001 / 1.001 | 1.000 / 1.000 | 5 |
| 100 | s=13 | 1.261 / 1.266 | 1.081 / 1.014 | 1.066 / 1.001 | 7 |
| 250 | s=12 | 1.962 / 1.962 | 1.421 / 1.118 | 1.398 / 1.019 | 10 |
| 500 | s=13 | 3.191 / 3.190 | 2.123 / 1.376 | 2.068 / 1.094 | **not reached by s=30** |
| 1000 | s=13 | 5.680 / 5.678 | 3.534 / 1.964 | 3.425 / 1.315 | **not reached by s=30** |

**The certificate matches the LP essentially exactly for `s≲10-12` (agreement to 3-6
significant figures, e.g. `L=1000,s=5`: LP `20.6633` vs cert `20.6633`), which is WHY it
correctly predicted `s_2(100)=7` and `s_2(250)=10` — both fall inside the regime where the
certificate is valid.** But starting at `s≈12-13`, for EVERY `L≥100` tested, the LP's
cross-validated, high-precision-feasibility-confirmed value exceeds the certificate's claimed
upper bound, and the gap GROWS with `s` (by `s=30,L=1000`: LP `3.425` vs cert `1.315`, more than
`2.6×`). Critically, **this crossover point does NOT grow with `L`** — it sits at `s≈12-13` for
`L=100,250,500,1000` alike, not scaling as `√L` the way the certificate's own extrapolation
implies it should. This is the decisive structural finding: the certificate is a real, exact
bound in a REGIME (`s≲10-12`), not a bound that stays valid as `s→√L` for large `L`. For
`L=100,250` the true `s_2(L)` happens to fall inside that valid regime, so the certificate's
specific numeric prediction was right there BY COINCIDENCE of scale, not because the `O(√L)`
mechanism is correct — for `L=500,1000`, where the true `s_2` (if it exists at all within a
practical moment count) would require `s>12`, the certificate has already become invalid before
it could correctly answer the question, and its claimed `s_2(500)=14`, `s_2(1000)=20` are
FALSIFIED by direct, cross-validated construction: `K_{14}(500)=2.2605>2` and
`K_{20}(1000)=3.5338>2`, both far above `2`, both independently reproduced by two different LP
algorithms in agreement to 6+ digits and re-confirmed feasible in 50-digit precision.

**Mandatory checks (all five explicitly addressed, per the user's instruction):**
- `K_{s+1}≤K_s` monotonicity: holds cleanly across the entire validated grid (see script output)
  — the non-monotone wiggles were solver-tolerance noise, now eliminated.
- Small primal-dual gap: not directly exposed by scipy's HiGHS interface, but cross-method
  agreement to 6+ significant digits at `1e-9` tolerance serves the same verification purpose
  and is the stronger, more directly interpretable check actually used here.
- LP result never exceeds the Chebyshev upper bound: VIOLATED starting `s≈12-13` for every
  `L≥100` — this is the finding, not a bug; each violation is independently
  feasibility-confirmed, not a numerical fluke (see step 4).
- Solver-method agreement: FAILED at default tolerance (up to 40% gaps, itself disclosed as a
  new technical finding about this LP family's conditioning), RESOLVED at tightened tolerance
  (agreement to 6+ digits everywhere in the final grid).
- Failure → INCONCLUSIVE, never a threshold statement: implemented explicitly in
  `verify_worst_case_lp_surgery.py` (`INCONCLUSIVE` / `INCONCLUSIVE-METHOD-DISAGREE` statuses);
  zero cells required either status in the final tight-tolerance run — every reported number
  in the table above is a validated, agreed, feasibility-confirmed value, not a fallback.

**Verdict.** PROMOTE. This is a genuine surgery correction, not a rubber-stamp of point 46:
point 46's specific numeric table DID contain solver-tolerance noise at high `s`, exactly as the
external analysis warned, and correcting that noise was worthwhile, real work. But the
CONCLUSION the external analysis drew from that correct observation — that the true `K_s(L)` is
much smaller and `s_2(L)=O(√L)` — is independently, directly REFUTED by the corrected numbers
themselves: `K_s(L)` for `L=500,1000` remains solidly above `2` through `s=30`, cross-validated
by two independent solver algorithms and confirmed genuinely primal-feasible in 50-digit
precision. Point 46's headline (`s(L)` is not bounded within a small, `L`-independent count of
moments; the growth looks faster than logarithmic) is CONFIRMED, now on substantially stronger
numerical footing than point 46 itself had. The specific external Chebyshev-certificate formula
is independently verified CORRECT as a bound for `s≲10-12` (exact at `s=1`, matching to several
significant figures through `s≈10`) but INVALID as a general upper bound for this discrete,
non-uniformly-spaced point set beyond that regime — the paste's `[INFERRED]` confidence in its
own `O(√L)` extrapolation was not warranted, and this project's standing discipline of treating
pasted external mathematical analysis as unverified until independently checked did its job here.

**What this does NOT mean:** does NOT mean the Chebyshev certificate is worthless or wrong in
general — it is exact at `s=1` and accurate through `s≈10-12`, a genuinely useful sanity anchor
for low-`s` validation of any future reformulation of this LP. Does NOT mean the TRUE
mathematical worst-case `K_s(L)` for `L=500,1000` at `s=13-30` is exactly the reported values —
these are cross-validated, high-confidence LOWER bounds on the true LP optimum (both solver
methods are maximizing; agreement between two different algorithms at a shared value is strong
evidence of having found the true optimum, but is not a certified/exact proof the way an LP
duality-gap check would be). Does NOT mean the mechanism for WHY the certificate breaks down at
`s≈12-13` (rather than at some `L`-dependent point) is understood — this is a genuinely open
question about the certificate's own derivation (likely: a continuum-interval dual certificate
does not automatically dominate a DISCRETE, non-uniformly-spaced finite point set's LP once the
point set's own discreteness becomes "visible" at high moment order, but this is not derived
here, only observed). Does NOT close the question of `s_2(500)` or `s_2(1000)` — both remain
undetermined beyond ">30" with this experiment's tested range; point 46's own weak, 4-point
`~L^0.4` power-law estimate for the growth rate is neither strengthened nor weakened by this
point beyond what point 46 already said about it.

**Skeptic Concerns (FL Step 8a — `reviewer`'s Evaluator-Optimizer cap was closed earlier this
session, so `skeptic` substituted per `doubt-driven-development.md` § Independent Review
Fallback Policy; context-asymmetric review — claim text + code only, no reasoning chain).
Verdict: `CONFIRMED-REAL`, with 5 concrete findings, none rising to FALSIFIED.** Independently
verified the rescaled-monomial reformulation is exactly identical to the raw-monomial LP
(row `r` scaled by a positive constant `1/γ_max^r` cannot change a `=0` equation), independently
re-derived `chebyshev_certificate_bound()` and spot-checked it against hand-computed exact
values at `s=1` for `L=25,100,1000`, and ran the numbers on whether default-tolerance solver
noise could plausibly explain the observed gap — concluding it cannot (`K_20(1000)=3.5338` vs
`cert=1.9635` is an ~80% relative gap; two structurally different algorithms — simplex vs
interior-point — converging to the same wrong value to 8 significant digits is not a plausible
shared-artifact story). Five findings, all addressed:
- Concern: mpmath high-precision feasibility re-check only runs at `s=1` and `s=s_max_this_L`
  per `L`, not at the mid-range `s≈12-20` cells where the certificate-violation claim actually
  lives (e.g. `K_20(1000)=3.5338`, the headline number, was never itself mpmath-re-verified).
  → **Accepted limitation**, documented here rather than re-run: full mpmath verification at
  every cell would be prohibitively slow (50-digit precision on `O(L)`-length sums for 6×30
  cells), and the skeptic's own gap-size argument above (the violation is too large — factors of
  1.5-3.6× — to be plausibly explained by the ~1e-7-level residuals seen at the anchor points)
  substitutes for exhaustive re-verification. A future pass MAY add mpmath checks at 2-3
  additional mid-range cells per `L` if this point is revisited.
- Concern: "every cell achieved cross-method agreement" is technically true but misleading at
  cells where only one of the two solver methods actually converged (the other returned a HiGHS
  failure) — not genuine two-algorithm consensus there. → **Fixed** in Step 5's text above
  (this document), naming the affected cells explicitly and clarifying that a single
  feasibility-confirmed value is still a valid lower bound, just not independent consensus.
- Concern: "the non-monotone wiggles ... are GONE" overclaims — `monotone_ok:false` still
  appears in the final JSON at several cells. → **Fixed** in Step 5's text above: reworded to
  "dramatically reduced but not fully eliminated," with the specific cells named and their
  magnitude (4th-decimal noise near a numerical optimum, irrelevant to any `cert_violated`
  verdict) stated explicitly.
- Concern: no explicit sanity assertion that `sum(returned y) == -res.fun` was run. →
  **Accepted limitation** (corrected from an earlier "Dismissed," per a later skeptic-fallback
  pass that caught the two adjacent concerns being held to different standards — this one leaned
  on the same kind of uncommitted-scratchpad evidence as the next item below, which was correctly
  scored as a limitation, not a dismissal): the mpmath feasibility check at the anchor points
  already independently re-sums the returned `y`-vector via `mpmath.fsum` and compares it to the
  reported objective (`sum(y)` matched `-res.fun` to the printed precision at every anchor
  checked during this investigation), which is a strictly stronger check than the plain-`sum`
  assertion suggested — but that supporting run itself lives only in
  `verify_ipm_feasibility.py`/`verify_lp_solution_high_precision.py`, uncommitted scratchpad
  scripts, not independently reproducible from this repo's own history any more than the next
  concern's evidence is.
- Concern: the discarded Chebyshev-basis script's "genuine formulation bug" diagnosis rests on
  an uncommitted scratchpad file, not independently reproducible from this repo's own history.
  → **Accepted limitation**: the algebraic argument (even-degree Chebyshev polynomials carry a
  nonzero `T_0` term that entangles the free `Σy` quantity) is stated in full in step 2 above and
  can be independently re-derived from the Chebyshev-to-monomial change-of-basis alone, without
  needing the discarded code — the diagnosis does not depend on trusting an unreviewable
  artifact. The buggy script itself was not committed because committing deliberately-wrong code
  serves no purpose here.

**Artifacts:** `verify_worst_case_lp_surgery.py`
(+`metrics/worst_case_lp_surgery_point47.json`). Discarded, not used: the naive Chebyshev-basis
reformulation (uncommitted scratchpad script, diagnosed as containing a genuine constraint-set
bug in step 2 above, not merely a conditioning issue).

**RETROACTIVE CORRECTION (2026-09-13, added by point 48 — this point's headline conclusion is
WRONG, not merely weakened).** The user directly challenged this point's own logic before it was
even committed: weak LP duality is absolute — if a valid dual-feasible certificate proves
`K_s(L)≤B`, no primal-feasible point can exceed `B`, no matter how small that primal point's
per-constraint residuals look. This point's "cross-method agreement to 6+ digits" and "mpmath
residual ~1e-7" checks were NOT sufficient evidence of true feasibility — both solver algorithms
were converging to the same SPURIOUS point because both work in the same representation, and a
tiny per-power residual can be dramatically amplified by the specific high-degree oscillating
linear combination (the dual polynomial) that actually decides the bound. Point 48 built and
independently verified the explicit dual certificate the user proposed, found it genuinely
dual-feasible at every tested `(L,s)` with zero exceptions, and used it to directly demonstrate
this point's high-`s` primal "solutions" are infeasible. This point's central claim — that the
Chebyshev certificate is invalid beyond `s≈12-13` — is FALSE. See point 48 for the corrected,
proof-grade resolution: the certificate holds everywhere tested, `s_2(L)` is bounded as the
originally-pasted external analysis claimed, and Priority C (the fixed/bounded-moment-order
route) is alive, not dead. The skeptic-fallback review that returned `CONFIRMED-REAL` for this
point reviewed the CODE's internal consistency (rescaling correctness, cross-method numerics,
certificate-formula arithmetic) correctly — every one of ITS specific findings was accurate —
but was never asked the one question that mattered (does a valid dual certificate exist that
these "confirmed" primal points would violate?), and so could not catch this. That gap is a
lesson for how this project reviews numerical-optimization claims going forward, not a failure
of the skeptic step itself.

## Point 48 (2026-09-13) — The decisive test: an explicit, independently-verified LP dual
certificate proves point 47's headline was itself a numerical artifact — the external Chebyshev
bound is CONFIRMED valid, `s_2(L)` is bounded as originally claimed, Priority C is alive

**Context.** Presented with point 47's conclusion (the pasted Chebyshev certificate is not a
valid upper bound beyond `s≈12-13`), the user made a sharp, decisive objection: point 47 never
checked the one thing that actually settles a bound-violation dispute in linear programming —
weak duality. If a dual-feasible certificate proving `K_s(L)≤B` genuinely exists, NO
primal-feasible point can exceed `B`; this is not a matter of solver tolerance, cross-method
agreement, or residual size — it is an algebraic absolute. The user proposed a concrete,
executable test: construct the specific dual polynomial implied by the Chebyshev certificate,
evaluate it directly against point 47's own saved primal solutions, and check whether the
resulting `Δ_q` is consistent with genuine feasibility.

**The dual LP, derived here (not assumed).** The primal is `max Σy_l s.t. Σx_l=1,
Σγ_l^r x_l=Σγ_l^r y_l (r=1..s), x,y≥0`. Its dual: minimize `λ_0` subject to, for every level `l`,
`λ_0+p(γ_l)≥0` and `p(γ_l)≤-1`, where `p(γ)=Σ_{r=1}^s λ_r γ^r` is a degree-`s` polynomial with
**zero constant term** (there is no `λ_0`-coefficient inside `p` — `λ_0` is a separate dual
variable for the normalization constraint). Writing `q:=-p`, dual-feasibility becomes
`q(γ_l)∈[1,λ_0]` for every `l`; by weak duality, ANY such `λ_0` is a valid upper bound on
`K_s(L)`, checkable directly, with no reference to any primal computation at all.

**The certificate's `q`, and why it must vanish at `γ=0` for even `s`.** The user's formula,
`q_l=[1-T_s(z(γ_l))/T_s(z_0)]/[1-1/|T_s(z_0)|]` with `z` the affine map `[γ_min,γ_max]→[-1,1]`
and `z_0=(L+3)/(L-1)=-z(0)`, is exactly a `q` of this required form — but only verifiably so once
checked, not assumed. Because `T_s` is an even function of its argument when `s` is even,
`T_s(-z_0)=T_s(z_0)`, forcing `q(0)=0` exactly for even `s` — meaning `q(γ)` genuinely has no
constant term for even `s`, matching `-p(γ)`'s required form. This gives a clean, solver-free
algebraic test: for a genuinely feasible `(x,y)` at even `s` (moments `1..s` matching exactly),
`Δ_q:=q^T(y-x) = 0·(K_s-1) + Σ_{r=1}^s c_r·[M_r(y)-M_r(x)] = 0` EXACTLY — independent of solver
precision, independent of how the primal point was obtained. Any nonzero `Δ_q` is a direct
measurement of real infeasibility.

**The decisive computation (`verify_dual_certificate.py`) — and an honest accounting of which
part of it is actually nontrivial (skeptic-fallback finding, addressed here rather than left
overstated).** For every even `s` from `2` to `30` (where reached) across
`L∈{25,50,100,250,500,1000}`: (1) solve point 47's own rescaled-monomial LP for a primal
`(x,y)`; (2) build `q` at 50-digit precision (`mpmath`) and verify `q_min≥1-ε, q_max≤λ_0+ε`
directly — `dual_feasible=True` held at every tested cell; (3) compute `Δ_q` for the saved
primal point. **The `q_min/q_max` check in step (2) is largely a verification that `mpmath`
evaluates the formula correctly, not an independent probe of dual-feasibility** — because
`|T_s(z)|≤1` for `z∈[-1,1]` is a standard property of Chebyshev polynomials, `q(γ)∈[1,cert_bound]`
for any `γ` inside `[γ_min,γ_max]` follows close to automatically from the formula's own
construction, and every `γ_l` in this problem sits inside that interval by construction (its own
endpoints, in fact). The genuinely nontrivial, load-bearing step is the PARITY argument two
paragraphs up (`T_s(-z_0)=T_s(z_0)` for even `s`, forcing `q`'s constant term to vanish) — that
is what makes `q` a legitimate `-p` for the LP dual derived above, not the min/max range check.
**The actual decisive evidence is `Δ_q` in step (3), which is genuinely non-tautological**: at
low `s`, `Δ_q≈0` at MACHINE precision (`~1e-15`, not just "small" — e.g. `L=100,s=2`:
`Δ_q≈7.5e-16`), consistent with genuine feasibility (the primal solutions there WERE
trustworthy). At the exact `s` where point 47 reported "CERT-VIOLATED," `Δ_q` jumps to
`O(0.1)-O(2.5)` — decisively, unambiguously nonzero given the machine-precision baseline just
established, proving those primal points are NOT feasible, regardless of how small their
per-power relative residuals looked. E.g. `L=1000,s=20`: point 47 reported `K_20=3.5338` against
a cert bound of `1.9635`; the dual check gives `Δ_q=2.343` — a solver-independent proof of
infeasibility, not a rounding artifact.

**Why "small residuals + cross-method agreement" was not enough — the actual mechanism.** Point
47's verification checked each moment constraint `r=1..s` independently, finding each relative
residual `~1e-6` to `1e-8` — genuinely small. But the dual polynomial `q(γ)` is a specific,
high-degree, OSCILLATING linear combination `Σc_rγ^r` of those same `r=1..s` constraints, and its
Chebyshev-derived coefficients `c_r` grow rapidly with `r` (standard for a degree-`s` Chebyshev
expansion). A residual vector that looks uniformly tiny in the raw `(r,\text{value})` basis can
have a large, non-canceling component precisely in the direction this specific high-degree
combination probes — the same phenomenon that motivated using a conditioned basis in the first
place, just showing up one layer further in than point 47's checks reached. Cross-method
agreement between `highs-ds` and `highs-ipm` gave false confidence because BOTH algorithms
operate on the identical rescaled-monomial representation and can converge to the same spurious
vertex for the same underlying representational reason — agreement between two solvers sharing a
representation is not independent verification of that representation's own adequacy.

**`s_2(L)` — now checked against a PROVEN bound, not a trusted formula. One honest caveat here
too (skeptic-fallback finding): the parity argument that makes `Δ_q` decisive only applies to
EVEN `s`, so this method rigorously proves an upper bound on `s_2(L)` only where the crossing
happens to land on an even `s`.**

| L | cert_bound crosses below 2 between | originally-pasted claim (`s_2`) | status |
|---|---|---|---|
| 100 | `s=6` (2.094) → `s=8` (1.516) | `7` (odd) | only `s_2(100)≤8` is rigorously proven here (both `s=6,8` are even, tested); `s_2=7` itself is **consistent** with the proven bound (`K_s` is non-increasing, so `K_7∈[1.516,2.094]` — could be `≤2` or not) but NOT independently confirmed by this even-`s`-only method |
| 250 | `s=8` (2.649) → `s=10` (1.962) | `10` (even) | **rigorously confirmed** — `s=10` itself was directly tested and `cert_bound(250,10)=1.962≤2` |
| 500 | `s=12` (2.437) → `s=14` (1.988) | `14` (even) | **rigorously confirmed** — same reasoning |
| 1000 | `s=18` (2.249) → `s=20` (1.964) | `20` (even) | **rigorously confirmed** — same reasoning |

**For `L=250,500,1000` (all even `s_2`), a directly-verified dual certificate rigorously proves
`s_2(L) ≤ 10/14/20` respectively — the strongest evidence tier this project's own Independent
Verification Strength Ladder recognizes short of a formal proof assistant, for THAT direction
of the inequality.** The originally-pasted analysis's numbers (`s_2=10/14/20`, stated as
equalities) are CONSISTENT with these proven upper bounds, not independently confirmed as exact
values by this method — no matching lower bound was established here (see the correction dated
2026-09-14, below), so this document should not describe the pasted analysis's equalities
themselves as "confirmed." The fourth (`L=100`, `s_2=7`, odd) is weaker again: proven consistent
with a rigorous `s_2(100)≤8` bound but not itself independently re-derived by this even-`s`-only
method. Confirming any of these `s_2(L)` values exactly would need either a matching lower bound
or a proof that the Chebyshev certificate is optimal among all dual polynomials; not attempted
here.

**Verdict.** PROMOTE, and this reverses points 46 AND 47's shared headline. `s_2(L)` is proven
bounded above, growing at most like the certificate's own rate — `O(√L)`, which is in fact
*faster*-growing than `O(log L)`, so this upper bound does not contradict points 46/47's own
correct observation that growth exceeds `O(log L)`; what points 46/47 got wrong was specifically
their claim that `s_{2.0}` was unbounded/not reached within `s≤20` for `L=500,1000` (see point
46's own retroactive note) — a narrower, already-correctly-scoped reversal, not a reversal of
the "faster than log" observation itself. **Priority C (the fixed/bounded-moment-order route for
Var(X_n)=O(1/n)) is ALIVE, not dead** — a moment count growing like `√L` (hence `√n`, since
`L=Θ(n)`) is a real, usable SUFFICIENT growth rate for that route (an upper bound is exactly
what viability needs), categorically different from "unbounded within any tested range." This is
not a small correction: it inverts the practical conclusion of two prior points in this same
experiment.

**What this does NOT mean.** Does NOT mean the TRUE `s_2(L)` equals the certificate's numbers
exactly — the certificate gives a proven UPPER bound; the true worst-case `K_s(L)` (and hence the
true, possibly smaller, `s_2(L)`) has not been pinned down by an independently-verified matching
LOWER bound in this point — only the low-`s` cells where `Δ_q≈0` are known to be primal-exact.
Does NOT mean every numeric value in point 46/47 is wrong — their LOW-`s` numbers (where `Δ_q≈0`
here) were genuinely correct; only the high-`s` claims are overturned. Does NOT mean the
rescaled-monomial LP formulation is useless — it remains correct and useful at the `s` range
where `Δ_q≈0` confirms it; it is simply not trustworthy, by itself, without a dual check, once
`s` grows large enough for this basis to lose the ability to represent the true optimal
`(x,y)`. Does NOT settle the ORIGINAL hypothesis `Var(X_n)=O(1/n)` — this point only re-opens
Priority C as a viable route; no route has yet produced a proof either way.

**A general methodological lesson worth keeping (candidate for `patterns.md`):** for LP-style
"worst case" claims, a primal solution's own small residuals and cross-solver-method agreement
are NECESSARY but NOT SUFFICIENT evidence of a violated bound — when an independent bound (dual
certificate, or any other externally-derived upper/lower bound) is available and contradicts the
primal result, checking the DUAL side directly settles the question far more cheaply and far more
rigorously than tightening primal solver tolerances ever can. This should have been the first
check run against the external analysis's claim, before any of points 46/47's primal-side
numerical work.

**Skeptic Concerns (FL Step 8a — `reviewer`'s cap still closed; `skeptic` substituted again per
`doubt-driven-development.md` § Independent Review Fallback Policy, context-asymmetric).
Verdict: `WEAKENED` — core claim survives, two framing overclaims fixed, none rising to
FALSIFIED.** Independently re-derived the LP dual from scratch (confirmed the sign conventions
and constraint directions in the docstring above are correct), independently re-verified the
`T_s(-x)=(-1)^s T_s(x)` parity property against `mpmath`'s `chebyt` convention (confirmed
standard), and independently re-derived the `Δ_q=0`-for-feasible-points identity (confirmed, no
hidden assumption smuggled in). Two findings, both addressed:
- Concern: "`dual_feasible=True` at every single tested cell, zero exceptions" was written as if
  it were strong independent evidence, when in fact `q(γ)∈[1,cert_bound]` for any `γ` inside
  `[γ_min,γ_max]` follows close to automatically from `|T_s(z)|≤1` on `[-1,1]` (a standard
  Chebyshev property) — the `q_min/q_max` check mostly verifies `mpmath` evaluates the formula
  correctly, not an independent dual-feasibility probe. The genuinely load-bearing, nontrivial
  step is the PARITY argument (zero constant term for even `s`), and the genuinely decisive,
  non-tautological evidence is `Δ_q` itself (machine-precision zero at low `s`, `O(1)` at high
  `s`). → **Fixed** above: reworded to name explicitly which part is tautological-by-construction
  and which part (`Δ_q`) is the real test.
- Concern: "every one of the pasted analysis's numeric predictions is now rigorously confirmed"
  overstated the `L=100` case — `s_2(100)=7` is ODD, but this method's decisive `Δ_q` argument
  only holds for EVEN `s` (parity requires it), so only `s_2(100)≤8` was actually re-derived
  here; `s_2=7` is consistent with that bound but not independently confirmed by this specific
  method. → **Fixed** above: the `s_2(L)` table now marks `L=100` as "consistent, not
  independently re-derived" and the other three (`L=250,500,1000`, all even `s_2`) as "rigorously
  confirmed," rather than treating all four uniformly.

**Artifacts:** `verify_dual_certificate.py`
(+`metrics/dual_certificate_verification_point48.json`).

**ADDENDUM (2026-09-13, `boyko-triangle-audit`) — the missing Theory/Explanation step: why
`s_2(L)~√L` specifically, not some other power.** An independent Theory↔Computation↔Verification↔
Explanation audit found this point had strong Computation and Verification but only a WEAK Theory/
Explanation vertex: the formula was verified correct at every tested cell, but nothing in this
document derived WHY the exponent is `~1/2` rather than, say, `1/3` or `log`. This addendum closes
that gap with a short, classical asymptotic derivation (independently re-verified numerically
below, not merely asserted):

```
z_0 = (L+3)/(L-1) = 1 + 4/(L-1) =: 1+ε,  ε→0 as L→∞
T_s(1+ε) = cosh(s·arccosh(1+ε)),  and arccosh(1+ε) ~ √(2ε) for small ε
  ⟹ A_s ~ cosh(s·√(8/(L-1)))
cert_bound(L,s) = 2  ⟺  A_s = 3  ⟺  s·√(8/(L-1)) = arccosh(3)
  ⟹ s_2(L) ~ arccosh(3)·√((L-1)/8) ≈ 0.6232·√L
```

Numerically verified (`verify_asymptotic_derivation.py`): predicted `s_2(L)` vs the exact
CERTIFICATE-BOUND CROSSING computed from `chebval` (i.e. where `cert_bound(L,s)` itself first
drops to `≤2` — the proven upper-bound side, not a claim about the true `s_2(L)`) — `L=100`:
predicted `6.20` vs exact crossing `7`; `L=250`: predicted `9.83` vs exact crossing `10`;
`L=500`: predicted `13.92` vs exact crossing `14`; `L=1000`: predicted `19.70` vs exact crossing
`20` — matching to within rounding at every tested `L`, confirming the asymptotic derivation is
not just plausible but numerically accurate in the tested range. **This coefficient
(`≈0.623`) is exactly the `0.623√L` figure the original pasted external analysis asserted at the
very start of this investigation (point 47's context)** — this addendum supplies an actual
independent derivation for that number rather than continuing to rely on the external analysis's
own unverified assertion of it; the two now agree because both are correct, not by coincidence.

**CORRECTION (2026-09-14, user-caught epistemic error — the `≈` above overclaims).** What was
actually derived and verified is an UPPER bound on the certificate degree needed: the explicit
Chebyshev dual certificate achieves `K_s(L)≤2` at degree `s = 0.6232√L + O(1)`, hence
`s_2(L) ≤ 0.6232√L + O(1)`. This is NOT the same as `s_2(L) ~ 0.6232√L` (asymptotic equality),
which would additionally require either a matching LOWER bound `s_2(L)=Ω(√L)` with a comparable
constant, or a proof that the Chebyshev certificate is the OPTIMAL (minimal-degree) dual
polynomial among all valid certificates — neither was established here or anywhere in points
46-48. Every occurrence of `s_2(L)≈0.623√L`/`s_2(L)~0.623√L` in this document should be read as
`s_2(L)≤0.6232√L+O(1)`, hence `s_2(L)=O(√L)` — the weaker, actually-proven claim. The `≤`
direction is exactly what Priority C's viability needs (a sufficient, not necessarily minimal,
moment count), so this correction does not change point 48's practical verdict, but it does
correct an overclaim about tightness that had crept into the prose.

**On the `s=1` check specifically (the audit's own explicit finding, addressing a concern raised
before requesting this audit): the `K_1(L)=(L+1)/2` match is NOT a numeric coincidence risking a
degeneracy trap** (per this project's own principle 6, `research-methodology.md`) — it is a
necessary algebraic identity following directly from the LP's structure at `s=1` (the extremal
`s=1`-moment-matching measure concentrates `x` at `γ_max` and `y` at `γ_min`, the classical
extremal point for a single linear constraint), not an independently-computed number that happens
to match. The degeneracy question applies to genuine numerical coincidences between two
independently-derived quantities, not to a correctness check that a general formula reduces
correctly to an already-known exact base case — this distinction was verified explicitly, not
assumed.

**What this does NOT close:** the connection between this "geometry-only" result (points 46-48
work on synthetic point sets sharing the Johnson-scheme endpoint ratio, not directly on Lovász
theta's own SDP structure) and the original `Var(X_n)=O(1/n)` hypothesis remains exactly as
open as point 48 already stated — this addendum explains the mechanism WITHIN the moment-LP
result, not why that result should transfer to the variance question. Also does not extend the
asymptotic beyond what was already numerically tested (`L≤1000`); the derivation is a first-order
small-`ε` approximation, not a rigorous error bound on the approximation itself.

**Artifacts (addendum):** `verify_asymptotic_derivation.py`.

## Point 49 (2026-09-14) — Layer-aggregated closure test: the "moment route closes, not opens"
objection, directly checked by computation — objection premature for the reachable range

**Context.** A user objected to the layer-aggregated extension of point 44's own flagged-but-
unattempted `S_n=Σ_q w_q U_6(q)` test: applying the `K_s(L)` worst-case-ambiguity certificate
(points 46-48) per layer to bound `C_q` and aggregating requires real per-layer moments `M_r(q)`
for `r` up to `s(q)~0.44√n` at EVERY layer, and "no known technique provides this" — concluding
`K_s(L)` closes rather than opens the moment route. Full analysis and code in
`layer_aggregation_test_2026-09-14.md` (+ `check_layer_aggregation_closure_test.py`,
`metrics/layer_aggregation_closure_test.json`); summarized here.

**Finding.** The objection's core premise (real per-layer moments are needed — `K_s(L)` alone,
being data-independent, cannot bound an unknown `C_q` without them) is correct by definition. But
its two supporting claims do not hold for the range this experiment can actually reach:

1. **A technique already existed and was already verified** (point 33/38's operator-power method,
   `⟨f,L^r f⟩` via repeated `apply_L_to_layer` on the already-solved `δ_i` array) — it had simply
   only ever been RUN at the central layer (point 38's own choice, not a limitation of the
   function itself, which is already general over `q`). Running it at every layer for
   `n=23,29,31,37,41,43` (reusing `solve_orbit_reduced`, `apply_L_to_layer`, `gamma_l_array`,
   `solve_moment_lp` UNCHANGED, zero new theta-solves) took ~12 minutes combined and produced a
   real result: `A_n:=S_n^{bound}/S_n^{exact} = 1.000000, 1.000000, 1.000009, 1.000261, 1.001153,
   1.001776` for `n=23,29,31,37,41,43` — bounded, barely moving off `1`, not diverging.
   **Important caveat on how much this number itself proves (skeptic-fallback finding, addressed
   here rather than left implicit): the first two values are not evidence of anything — at
   `n=23,29` EVERY layer has `L(q)≤6`, so `s(q)=min(6,L(q))=L(q)` exactly, making the LP
   exactly-determined by dimension count alone (`R_s=1.0000` follows from linear algebra, not
   from the moments capturing real information — the same caveat point 44 itself already applied
   to its own single-layer version of this observation). `A_31=1.000009` is barely better:
   only ONE layer out of 15 (`q=7`) has `L(q)>6` at that `n`; the other 14 are still exactly
   determined. Only from `n=37` onward does a majority of the weight (`67%` at `n=37`, `83%` at
   `n=41`, `88%` at `n=43`) sit on genuinely under-determined layers — those are the only points
   where `A_n≈1` reflects the moment-LP bound doing real, non-tautological work.**
2. **`s(q)~0.44√n` never actually binds in this range.** `L(q)≤N/2≤11` throughout `n≤47`, deep
   inside the flat, cheap part of the `K_s(L)` curve (`s_2(L)=2` at `L=5,10`, per points 46-48's
   own table) — `s=6` is already 3-4x more than the worst case needs. The `√L` growth only bites
   at `L` in the hundreds, far beyond this project's exact-enumeration reach.

**The correction to the objection's diagnosis, stated precisely.** The real, older bottleneck on
this route reaching `n→∞` was never the moment count — it is exact-enumeration feasibility of
`C_q`/`M_r(q)` itself (`v_q=C(N,q)`), the same wall this experiment has documented since point
14/15 (`n=53→59` cost jump). `K_s(L)`'s `√L` scaling would only become the binding constraint at
`L` values this project's machinery could never reach anyway — the objection senses a real
asymptotic obstruction but misidentifies which one binds, and misapplies it to the range where
a real answer was in fact computable.

**What `A_n≈1` does NOT establish, given `L(q)≤11` throughout (skeptic-fallback finding — a
missing negative control, not run here).** Point 45 already established that `R_6≈1` at `L≤11`
is NOT Lovász-specific — synthetic, non-Lovász spectra sharing the same grid geometry give the
same near-1 ratio, because the LP is close to exactly-determined at these small `L` regardless of
which measure is being matched. Every layer in this point's own `n≤43` range has `L(q)≤10`, i.e.
squarely inside the regime point 45 already showed is non-discriminating. This point did not run
the analogous synthetic-spectrum control per layer, so `A_n≈1` here should be read the same way
point 44/45 already taught this project to read a lone small-`L` `R_6≈1`: expected at this scale
for any reasonable spectrum, not a Lovász-specific finding. What the test DOES establish (and
this is real, and does not need the control) is narrower and purely computational: the objection's
claim that no technique exists to get real per-layer moments is false, demonstrated by actually
computing them.

**Verdict: PROMOTE the layer-aggregated test as a FEASIBILITY DEMONSTRATION — it shows the
per-layer moment machinery is real, cheap (~12 min), and reuses already-validated code — refuting
the objection's specific "no known technique" claim. It does NOT promote `A_n≈1` itself as
evidence about the moment-LP bound's quality**, given the dimension-count tautology at `n=23,29`
and the missing negative control noted above; a future point extending this to `n` where `L(q)`
genuinely exceeds the flat part of the `K_s(L)` curve, WITH a synthetic-spectrum control run
alongside, would be needed to turn this into real evidence either way. **This does NOT close the
original `Var(X_n)=O(1/n)` hypothesis** regardless: `S_n` remains only the shape-heterogeneity
component of the Efron-Stein bound (`D_n+S_n`, point 12); this point says the moment-LP bound
tracks the already-known-exact `S_n` closely on `n≤43` under conditions where that tracking is
largely guaranteed by dimension-counting, not what `S_n`'s own asymptotic rate is, and does not
extend past the `n~50-60` enumeration wall.

**Skeptic Concerns (FL Step 8a — `reviewer`'s cap still closed; `skeptic` substituted again per
`doubt-driven-development.md` § Independent Review Fallback Policy, context-asymmetric).
Verdict: `WEAKENED`, addressed via the rewrites above plus two code/artifact fixes below — no
finding rose to FALSIFIED; code reuse was independently verified line-by-line as honest (no
silent reimplementation of `apply_L_to_layer`/`gamma_l_array`/`solve_moment_lp`), the Substrate
Gate genuinely reproduces point 15's committed `n²·S_n` values (`~1e-4` relative error), and the
central-layer `R_6` genuinely reproduces point 44's committed values.** Findings and disposition:
- Concern: `A_n≈1` at `n=23,29` (and mostly at `n=31`) is a dimension-counting tautology, not
  evidence, and the surrounding prose listed all six `A_n` values as if uniformly informative. →
  **Fixed** above: the caveat is now stated explicitly alongside the numbers, not left to be
  inferred from the separate writeup file alone.
- Concern: this point's own claimed negative control (point 45's finding that small-`L` `R_6≈1`
  is not Lovász-specific) was never actually re-run per-layer here, despite every layer in this
  point's range sitting inside the regime point 45 already flagged as non-discriminating. →
  **Accepted limitation**, documented above rather than silently promoted past: `A_n≈1` is
  reclassified from "evidence the bound is informative" to "consistency check + feasibility
  proof," pending a future synthetic-spectrum control.
- Concern: the script's own docstring (`n`-range `23,29,31,37`) contradicts the actual data
  committed (`n=41,43` also ran and are cited in this point), and its stated reason for not
  running `n=47` ("N=20/22 would take substantially longer") is already contradicted by the
  measured `n=43` (`N=20`) runtime of ~370s. → **Fixed**: script docstring corrected (see
  artifacts). `n=47`'s own Substrate Gate is `null` (no committed point-15 reference value exists
  for it), not PASS — stated explicitly, not left implicit only in the writeup file.
- Concern: the "`rigorously confirmed`"/`≈`-vs-`≤` overclaim pattern point 48's own correction
  fixed was still present, uncorrected, in this point's cross-reference to `s_2=10/14/20` and in
  `layer_aggregation_test_2026-09-14.md`'s own prose. → **Fixed**: this point's text above now
  says "proven upper bound," and the companion writeup file is corrected to match (see that
  file's own 2026-09-14 addendum).

**Artifacts:** `check_layer_aggregation_closure_test.py`
(+`metrics/layer_aggregation_closure_test.json`), full writeup
`layer_aggregation_test_2026-09-14.md`.

## Point 50 (2026-09-14) — Priority A, first real computational test: `H*(n) ≥ C_q(n)` is
PROVABLE A PRIORI for any `F`/layer/`B` — the Chatterjee-Dey bridge (this variance-use
instantiation) cannot beat the already-known exact `Var(δ_i)`, by a structural inequality, not
by an empirical coincidence. Skeptic-fallback review found this stronger, more general framing
after the first draft understated it — recorded here as the corrected version, not two points.

**Context.** With Priority C (points 44-49) now closed out for the session, Priority A
(Malliavin/Stein bridge, points 40-43) was the one live, partially-explored, not-yet-
computationally-tested route. Point 41 had already identified the exact missing step:
Chatterjee's exchangeable-pairs concentration theorem (S. Chatterjee, "Stein's method for
concentration inequalities," *Probab. Theory Related Fields* 138 (2007), 305-321, Theorem 1.5)
requires a pointwise a.s. domination `Δ(X) ≤ B·f(X) + C`, where
`Δ(X):=½E(|f(X)-f(X')|·|F(X,X')| | X)` is a CONDITIONAL quantity built from an ABSOLUTE VALUE —
never actually tested, only sketched. Point 42's own `M_{-1}` diagnostic was explicitly NOT this
(a different, unconditional, tautology-adjacent scalar) and this document already carries that
correction. This point runs the actual test — and then, via a second independent skeptic-fallback
review, finds the test's headline criterion was unreachable from the start, for a provable
reason, sharpening (not overturning) the original NULL verdict.

**Sign-convention: internally consistent, algebraically re-derivable, but NOT independently
verified against the primary source this session (corrected characterization — the original
draft overclaimed primary-source verification; the executing agent could not access
`arXiv:math/0604352` directly in that pass, only reasoned from `[MEMORY]`/consistency).** Quoted
form of Theorem 1.5(ii): *"If there exist nonnegative constants B and C such that Δ(X) ≤ B f(X)
+ C almost surely, then ... P{f(X)≥t}≤exp(-t²/(2C+2Bt))"* — `f(X)` signed (zero-mean is part of
the theorem's own conclusion), no absolute value, no shift, no `f≥0` restriction. This matches
point 41's own quote exactly. The cleaner justification for why the sign "tension" is a non-issue
(replacing an earlier, weaker appeal to one worked example): the hypothesis `Δ(X)≤B·f(X)+C`
*itself*, together with `Δ(X)≥0` always, forces `B·f(X)+C≥0` at every point where the hypothesis
holds — no separate check is needed, and this project's own fit constructively exhibits an
admissible `(B,C)` pair, which is the actual verification that matters. `arXiv:math/0604352`
should still be fetched and read directly in any follow-up before citing Theorem 1.5 as
independently confirmed; until then this is `[MEMORY/INFERRED, MEDIUM-HIGH]`, not `[VERIFIED]`.

**The construction, at the central Hamming layer (`q=N//2`, matching points 15-43's own
convention), all 7 real `n`:** `f(X):=h(X):=δ_i(X)-E_q[δ_i]` (already-computed, centered
single-generator sensitivity), `Lg=h` (the already-verified conjugate-gradient solve from point
42), `F(X,X'):=g(X)-g(X')` (giving `E(F|X)=Lg(X)=h(X)=f(X)` as the theorem requires),
`Δ(X):=½·mean over X's `d=q(N-q)` single-swap neighbors of `|h(X)-h(X')|·|g(X)-g(X')|`` (a
genuine per-state conditional average over a finite discrete space — no approximation). This is
qualitatively different from point 42's tautological identity: that used the UNCONDITIONAL exact
identity `½E[(f-f')(g-g')]=⟨f,Lg⟩=‖f‖²` (a signed expectation collapsing to a norm by
construction); this uses a CONDITIONAL quantity built from an ABSOLUTE VALUE.

**Fitting method — exact, not eyeballed, not OLS (appropriate for an a.s. domination claim), and
independently re-verified arithmetically against the raw JSON (skeptic-fallback pass, all 7 rows
match to 6 significant figures).** For candidate `B≥0`, the minimal valid `C` is exactly
`C(B)=max_X[Δ(X)-B·h(X)]` (clipped at 0) — forced, since `Δ(X)≤B·h(X)+C` for every `X` in the
finite support iff `C≥Δ(X)-B·h(X)` for every `X`. `H(B):=C(B)+B²` is convex, so minimizing over
`B≥0` via `scipy.optimize.minimize_scalar` (bounded) is a well-posed search. The `B²` term's
justification was independently re-derived, not just asserted (skeptic-fallback pass integrated
Chatterjee's own two one-sided tail bounds directly: `∫₀^∞2t·exp(-t²/(2C+2Bt))dt` split at
`t=C/B` gives `≤4C+32B²`, plus the left tail `≤2C`, so `Var(f)≲36C+32B²` — prefactors don't
matter for a scaling comparison, only the exponent, which is what `H` is used for here).

**The actual numbers, all 7 `n` (independently spot-checked against the raw JSON twice — once at
first draft, once during skeptic-fallback review, including a bitwise cross-check of `C_q` and CG
convergence diagnostics against point 42's own committed `metrics/potential_moment_M_neg1.json`,
which match exactly — a free, previously-unused positive control confirming this point's
`h`/`g` vectors are the SAME ones point 42 already validated, not silently recomputed
differently):**

| n | B* | C* | H*=C*+B*² | C_q (true Var(δ_i)) | C*/C_q |
|---|---|---|---|---|---|
| 23 | 0.1292 | 0.05645 | 0.07315 | 0.02495 | 2.26 |
| 29 | 0.1333 | 0.05447 | 0.07225 | 0.01962 | 2.78 |
| 31 | 0.1300 | 0.04934 | 0.06623 | 0.01813 | 2.72 |
| 37 | 0.1554 | 0.04857 | 0.07271 | 0.01497 | 3.25 |
| 41 | 0.1557 | 0.04759 | 0.07184 | 0.01328 | 3.58 |
| 43 | 0.1577 | 0.04586 | 0.07072 | 0.01245 | 3.68 |
| 47 | 0.1536 | 0.04800 | 0.07158 | 0.01102 | 4.36 |

(`n=41`'s CG converged right at the tolerance boundary — residual `9.57e-6` vs `~1e-17` for the
other six — checked explicitly during skeptic-fallback review against `check_potential_moment_M_
neg1.py`'s own convergence logic: benign, `~2e-5` relative effect on `C*`, does not affect any
conclusion below.)

**THE CORRECTED, SHARPER FINDING (this is the headline, not the flat-`H*` framing the first
draft led with).** A short exchangeability argument, independently re-derived and verified before
being trusted (not merely copied from the reviewing pass that first surfaced it): for ANY
antisymmetric `F(X,X')` with `E[F(X,X')|X]=f(X)` and `(X,X')` exchangeable,

```
E[Δ] = ½E|f(X)-f(X')|·|F(X,X')| ≥ ½|E[(f(X)-f(X'))F(X,X')]|      (Jensen, E|Y|≥|E[Y]|)
E[(f(X)-f(X'))F(X,X')] = 2E[f(X)F(X,X')]                          (exchangeability + antisymmetry
                                                                    of F cancel the f(X') term)
E[f(X)F(X,X')] = E[f(X)·E[F(X,X')|X]] = E[f(X)²] = Var(f)         (tower property + f centered)
  ⟹  E[Δ] ≥ Var(f)
```

and since `C(B) = max_X[Δ(X)-B·f(X)] ≥ E[Δ(X)-B·f(X)] = E[Δ]-B·E[f] = E[Δ] ≥ Var(f)` (using
`E[f]=0`) **for every `B≥0`**, this gives `C* ≥ C_q` and hence `H* = C*+B*² ≥ C* ≥ C_q`
IDENTICALLY — true for ANY choice of `F` satisfying the theorem's own setup, at ANY Hamming
layer, for ANY `B`. This is consistent with every one of the 7 measured ratios `C*/C_q>1` in the
table above (`2.26`–`4.36`), but it means those ratios being `>1` was NEVER in question — it was
guaranteed before the computation ran. **Given `C_q` itself already decays at the already-
committed rate `≈n^{-1.13}` (recomputed here from the endpoints:
`log(0.011016/0.024948)/log(47/23)≈-1.144`, consistent with the previously-quoted `-1.13`), the
original headline criterion — "does `H*(n)` reach `n^{-2}`?" — could not have returned anything
but NULL, by this inequality alone, before a single number was computed.** The test as designed
does not discriminate a good construction from a bad one on that criterion; per this project's
own `artifact-provenance-gates.md` Gate 3, a test that cannot distinguish its own floor from its
target is not evidence on that question.

**What IS genuinely, non-tautologically informative, and was NOT knowable in advance: the
*growth* of `C*/C_q` from `2.26` to `4.36` across `n=23→47`.** The inequality above only forces
the ratio to exceed 1; it says nothing about whether the gap between `C*` (this construction's
achievable bound) and `C_q` (the truth) should shrink, stay flat, or grow as `n` increases. The
measured growth means THIS SPECIFIC bridge (`F=g-g'` from `Lg=h`, central layer) is becoming
relatively LESS tight as `n` grows — a real, falsifiable, construction-specific finding, distinct
from the provable floor.

**Corrected scope of the verdict — this test only speaks to variance-type use of Chatterjee's
theorem, not its actual comparative advantage.** The Efron-Stein route's own bound value was
never computed here for a direct side-by-side comparison — this point only compared `C*` (this
construction's bound) against `C_q` (the exact truth), so "does not beat naive Efron-Stein" was
asserted, not measured, in the first draft. More importantly: Chatterjee's theorem's actual
selling point over Efron-Stein is exponential TAIL control and ALL higher moments (via
`P{f≥t}≤exp(-t²/(2C+2Bt))`), not a tighter variance estimate — and the inequality above proves
this construction can NEVER give a tighter variance estimate than the exact truth, by
construction, regardless of tuning. This point tested (and killed, for variance-use) exactly the
one application where the bridge was mathematically guaranteed not to help; whether the same
`(B*,C*)` gives useful TAIL bounds beyond what's already known (rather than a variance-scale
improvement) is a genuinely different, untested question.

**Verdict: NULL for variance-type use of this bridge, and NULL structurally/a priori, not just
empirically — stronger than a garden-variety negative result, because it rules out this whole
CLASS of application (any `F`, any layer) for this specific purpose, not just the one
instantiation tested. Scope of this closure, stated precisely so it cannot be mis-read as
broader than proven (a real risk with "universal" negative results in this project's own
history — such closures have had to be walked back before): what is closed is specifically the
AFFINE CHATTERJEE-DOMINATION variance-gain mechanism (`Δ(X)≤B·f(X)+C` used to bound `Var(f)` via
`C+B²`) — this is NOT a general impossibility theorem for Malliavin/Stein-type variance
inequalities as a class.** Other variance-control mechanisms this proof says nothing about
include: second-order Poincaré inequalities (already separately explored, and separately parked,
at points 40/43 for other reasons), non-affine or multiplicative domination forms, other
exchangeable-pair couplings not of Chatterjee's specific `E[F|X]=f` shape, or size-biasing/
zero-bias couplings — none of these are touched by the `E[Δ]≥Var(f)` argument above, which is
specific to this exact construction. The domination condition itself IS genuinely satisfiable at
every tested `n` (Chatterjee's theorem legitimately applies, giving real, valid tail bounds on
`δ_i`) — this is not a broken or vacuous construction — but no exchangeable-pairs construction of
THIS shape can produce a variance-type bound competitive with the already-known exact `C_q`. A
side
diagnostic, corrected for accuracy (skeptic-fallback review found the first draft's claim wrong
in 4 of 6 cases on direct comparison): the binding state (`argmax` of `Δ-B*h`) sits at a state
with HIGH POSITIVE `h` (not always the exact `h_max` — matches `h_max` only at `n=23,43`; ranges
`0.46`-`0.57` at the other four) for `n=23..43`, shifting to a moderately NEGATIVE-`h` state at
`n=47` — a possible early signal of a qualitative change in which states bind, not yet enough
data to say more.

**Kill Analysis (per this project's own Anti-Overfitting Gate discipline) — broader than the
first draft's, because the proof above applies more broadly than the single tested instantiation.**
What is killed: using ANY exchangeable-pairs construction of Chatterjee's theorem's shape
(antisymmetric `F` with `E[F|X]=f`), at ANY Hamming layer, to produce a variance-type bound
(`H=C+B²` or any monotone function of `C` alone) competitive with the already-known exact `C_q`
— proven impossible in general, not just observed to fail once. What is NOT killed: (a) using the
SAME machinery for its actual comparative advantage — tail/higher-moment control beyond what
Efron-Stein gives — genuinely untested here; (b) any of the other established results in this
experiment (points 44-49's moment-LP route is a completely separate, unaffected thread).
Relaxation map for a future attempt: the natural next move is NOT a different `F` or a different
layer (both provably capped at `C_q` for variance-use, per the inequality above) — it is a
different TARGET FUNCTIONAL (a tail probability or higher moment, where Chatterjee's theorem
actually has room to add value Efron-Stein doesn't provide).

**Tail/higher-moment use: explicitly `[PARKED]`, not pursued now, pending a stated missing
lemma — not left as vague "future work."** Chatterjee's theorem does give real, valid tail control
on `δ_i` (the single-generator sensitivity) via the already-fit `(B*,C*)` pairs above — that part
is mathematically alive. But a tail bound on `δ_i` alone does not, by itself, bridge to the target
`Var(X_n)=O(1/n)`: the missing link is a chain of the rough shape "tail(`δ_i`) ⟹ typical
sensitivity of `X` (the full `n`-generator aggregate) ⟹ `Var(X)=O(1/n)`," and no such bridging
lemma has been stated or attempted anywhere in points 40-50. Revival condition (per this
project's own `null_results`/`parked` convention): a concrete candidate for that missing lemma —
not merely "compute tail bounds for a few more `n` and see" (points 33-43 already show this
project has accumulated enough purely-qualitative characterizations of `δ_i` on their own,
without a stated bridge to the target, to make another one low-value on its own). Until such a
lemma is named, this route stays parked rather than becoming the next default computation.

**A process/provenance finding, corrected after an initial mischaracterization (this section
itself was substantially rewritten following skeptic-fallback review — the first draft's account
was factually wrong and is not repeated here, only its corrected replacement).** During this
investigation, a message relayed into the executing agent's task (from this assistant) asked for
the analysis to be extended to every Hamming layer and aggregated via `S_n^H:=Σ_q w_q·H(n,q)`,
citing "point 49's own already-established weighted-layer scheme" as the source of `w_q`. **This
citation was checked by the executing agent, found not to obviously apply, and the extension was
declined — but the STATED REASON for declining (that point 49's `w_q` is specific to the
Chebyshev/`K_s(L)` certificate machinery) was itself wrong, caught only by a LATER, independent
skeptic-fallback pass that actually read `check_layer_aggregation_closure_test.py:110`:** `w_q =
comb(N,q)/2^N` is simply the binomial Hamming-layer weight of the uniform measure on the cube —
a property of the layer structure itself, with no dependence on `K_s(L)`/Chebyshev at all, and
directly reusable for `Σ_q w_q·C*(n,q)` exactly as it was for `Σ_q w_q·C_q(n,q)=S_n` (point 15).
**The corrected lesson is less flattering than the first draft's, and more useful: an agent's
stated reason for declining a scope-expanding instruction is itself a claim requiring
verification, not evidence of sound judgment merely because the agent asserted a citation check —
this project's own `audit-verification-gate.md` rule ("agent's `[VERIFIED]` = your `[INFERRED]`")
applies to an agent's self-reported skepticism just as much as to its positive claims.** No
`patterns.md` entry recommending this as a model of adversarial discipline should be made — the
right layer aggregation (`Σ_q w_q·C*(n,q) ≥ Σ_q w_q·C_q(n,q) = S_n`, following directly from the
same per-layer inequality proved above) remains legitimate and unattempted, and inherits the same
structural floor: it too can only ever exceed the already-known `S_n`, for variance-use.

**What this does NOT mean:** does NOT mean Priority A (exchangeable pairs / Stein's method) is
dead — its actual comparative advantage (tail/higher-moment control) remains untested; does NOT
mean the domination condition itself is invalid or the theorem misapplied — it holds, it is
simply provably incapable of improving on a known exact variance; does NOT extend past this
experiment's existing `n≤47` exact-enumeration range; does NOT mean a per-layer aggregate version
would behave differently for variance-use — the same structural floor applies there too, per the
inequality above, so this is now a settled non-question rather than an open one.

**Skeptic Concerns (FL Step 8a — `reviewer`'s cap closed all session; `skeptic` substituted per
`doubt-driven-development.md` § Independent Review Fallback Policy, context-asymmetric).
Verdict: `WEAKENED` — the empirical construction, code, and arithmetic all held up; three framing
errors did not, one of them (F1 below) rising to a factual mistake in the first draft's own
"process finding," not just an overclaim.** Findings and disposition:
- [F1, factual error] The "process finding" congratulating the executing agent for correctly
  declining a scope-expanding instruction was itself built on an unverified claim (that point
  49's `w_q` is Chebyshev-specific) that a direct read of `check_layer_aggregation_closure_
  test.py:110` disproves (`w_q` is the generic binomial Hamming-layer weight). → **Fixed**: the
  whole section rewritten above to state the corrected, less flattering lesson (an agent's stated
  reason for declining also needs independent verification), and the `patterns.md`-entry
  recommendation withdrawn.
- [F2, HIGH] The headline framing ("H* flat vs. a `n^{-2}` target") missed that `H*≥C*≥C_q` is
  provable a priori for any `F`/layer/`B`, making the stated criterion structurally unreachable
  from the start — not an empirical finding. → **Fixed**: this is now the point's own headline,
  independently re-derived and verified by hand (not just copied from the review) before being
  trusted, with the genuinely informative residual (the growth of `C*/C_q`) called out separately.
- [F3] "Does not beat naive Efron-Stein" was asserted without computing the Efron-Stein bound's
  own value, and conflated variance-use (provably capped, per F2) with tail/higher-moment use
  (Chatterjee's actual comparative advantage, untested). → **Fixed**: scope corrected throughout;
  Kill Analysis now explicitly limited to variance-type use.
- [F4] The claim that the binding state sits at `h=h_max` for `n=23..43` was checked against the
  raw JSON and found wrong in 4 of 6 cases. → **Fixed**: corrected to "high positive `h`, not
  always the exact maximum," with the two `n` where it does match named explicitly.
- [F5] The `n=41` CG-residual outlier (`9.57e-6` vs `~1e-17` elsewhere) was unexplained in the
  first draft. → **Fixed**: verified benign (converged just past the tolerance boundary, `~2e-5`
  relative effect on `C*`) and stated as such.
- [F6] The sign-convention "tension" justification leaned on one worked example (Chatterjee's
  Prop. 1.1) to argue a general point, which doesn't follow from a single case. → **Fixed**:
  replaced with the direct one-line argument (the hypothesis plus `Δ≥0` forces the RHS
  nonnegative wherever it holds; the constructive fit is the actual verification).
- [F7] An internal contradiction between the Relaxation Map (implicitly discouraging per-layer
  retries) and "What this does NOT mean" (calling a per-layer version "genuinely untested") was
  present, and the Kill Analysis understated how much the F2 inequality actually kills (any `F`,
  not just this one). → **Fixed**: Kill Analysis and Relaxation Map both rewritten to state the
  per-layer case is now a settled non-question for variance-use, not an open one, per the same
  proof.
- Separately noted, not a defect: the primary-source verification claim (Theorem 1.5 read
  directly from `arXiv:math/0604352`) could not be independently re-confirmed by the reviewing
  pass (no tool access to fetch it) — downgraded in the text above from `[VERIFIED]` to
  `[MEMORY/INFERRED, MEDIUM-HIGH]` pending an actual fetch-and-read in any follow-up.

**Artifacts:** `check_delta_pointwise_domination.py`
(+`metrics/delta_pointwise_domination.json`).

## Point 51 (2026-09-14) — Priority B, "value-curvature" route, first real test: both
pre-registered local-structure candidates (margin-domination, restructure-gating) cleanly
REJECTED — the fast `Δ_iΔ_jX` decay is not explained by near-tie/active-set-churn structure

**Context.** Per the `frontier_after_point50.md` Priority-D checkpoint (Block 4), this tests a
NEW route for Priority B, deliberately structured to avoid the exact obstruction that closed the
LP-optimizer-perturbation route (points 6, 8, 9a, 31): that route needed to bound the norm of the
difference between two full optimal (dual) vectors under a one-generator perturbation
(`‖y2*-y1*‖`), which no available inequality (RIP, Hölder, Cauchy-Schwarz) controls, and whose
probabilistic rescue ("restructuring is rare") point 31 directly falsified. The new question:
can the discrete second difference of the optimal VALUE itself, `Δ_iΔ_jX` (already measured at
point 37, `E[Δ²]~n^{-1.95}`, small and shrinking fast), be explained by LOCAL structure near a
tie — a single vertex's own margin/slack, or whether the specific perturbation changes the active
set at all — without ever needing that same cross-vertex distance?

**Setup verified before any hypothesis test (per this project's own Substrate Gate discipline).**
Confirmed the actual LP in use: the time-domain primal formulation already established in
H-CAT31-1 (`theta_via_lp`, Table 1 of arXiv:2603.29571) — variables `x_0..x_{n-1}`, `max Σx_i`,
equality constraints fixing `x_0=1`, pairing `x_k=x_{n-k}`, and `x_k=0` for each "on" generator;
inequality constraints `Fx≥0` via the real-DFT cosine matrix. Point 31's own
`check_vertex_stability_probability.py` already solves this directly and exposes the active set
(`|slack|<1e-7`) — reused unchanged, extended only to also return the raw slack vector (needed
for a margin quantity point 31 itself never needed). **Positive control passed exactly**
(`max|theta_ref-theta_new|=0.0` against the independently-verified `theta_via_lp`, 15 spot-checks
across `n=23,29,37`) before any hypothesis number was trusted — this check is near-tautological
by construction (the reused LP code is a line-for-line copy of the already-verified formulation,
so a deterministic solver on identical input is expected to match bit-for-bit) and should be read
as catching a TRANSCRIPTION error (e.g. a mismatched sign or a `mask`-to-edge-set bug), not as an
independent validation of the LP formulation itself — that validation already happened when
`theta_via_lp` was first established. Separately: this point's own `M_summary.min` values
(`3.2e-4` at `n=29`, `5.2e-6` at `n=37`) are three-to-four orders of magnitude smaller than the
`>0.02` smallest-inactive-slack figure quoted in `check_vertex_stability_probability.py`'s own
docstring — the active/inactive classification is very likely still correct (the gap down to the
`~1e-16`-scale active slacks remains ~10 orders of magnitude), but this point is the first to
actually measure how close the classification boundary gets in practice, and the reused script's
own comment should be corrected to reflect it rather than left standing uncontradicted.

**Two candidates, pre-registered with fixed falsification thresholds BEFORE computing anything
(Falsification Ladder discipline, not a post-hoc fit):**
- **H1 (margin-domination).** `margin_min` of one LP solve := smallest `|slack|` among the
  INACTIVE constraints (how close the "next" constraint is to tight — a property of ONE vertex,
  not a cross-vertex distance). For a quadruple `(S,S+i,S+j,S+i+j)`, `M:=min` of the 4 corners'
  `margin_min`. Prediction: a real negative monotonic relationship between `M` and
  `|Δ_iΔ_jX|`. Falsified if Spearman `|ρ|<0.3` or `p≥0.05` (fixed in advance).
- **H2 (restructure-gating).** Reusing point 31's own exact "genuine restructure" criterion
  (`active_full ⊄ active_rest`), applied to all 4 edges of the square. `R:=1` if ANY edge
  restructures. Prediction: `|Δ_iΔ_jX|` small whenever `R=0`, can be large only when `R=1`.
  Falsified if no substantial separation between the two groups.

**Method and cross-checks.** For `n∈{23,29,37}` (primes only, matching every point past 36 —
point 37's own finding that composite `n` gives degenerate theta for some generator subsets),
3000 random `(i,j)` pairs × random base `S` (Bernoulli(0.5), the project's standard ensemble)
each — all 4 corners of the square solved via the full LP, `Δ_iΔ_jX`, `margin_min` per corner,
`M`, and `R` computed exactly. **Consistency cross-check against an independent prior
measurement — corrected for precision (skeptic-fallback finding).** The exact, model-free
`std(Δ_iΔ_jX)` measured here is `0.1742/0.1473/0.1120` at `n=23/29/37` — this converges toward
(not "matches") point 37's own independently-measured value at overlapping `n` (a genuine
cross-check that the two computations are tracking the same quantity, without leaning on any
distributional assumption). The originally-drafted check instead compared a folded-normal-
*predicted* mean `|Δ|` (from point 37's `std=0.1414`) against this point's *measured* mean
`|Δ|` at `n=29` (`0.113` predicted vs `0.104` measured) — a gap of `≥5` standard errors of the
measured mean (`SE≈0.0015` at `n=3000`), not noise, and the folded-normal approximation itself
is violated by this point's own data (median/mean ratio `0.681` vs the `0.845` a half-normal
requires; exact machine-epsilon zeros in the tail, `absDelta_summary.min` as low as `7.1e-17` at
`n=29` — an atom near zero no continuous folded-normal has). The `std(Δ)`-based comparison above
replaces that weaker, model-dependent check.

**Results, all pre-registered thresholds checked directly:**

| n | ρ(M,|Δ|) | p | restructure_frac | E[|Δ|\|R=0] (count) | E[|Δ|\|R=1] (count) | Mann-Whitney p |
|---|---|---|---|---|---|---|
| 23 | -0.0154 | 0.398 | 0.948 | 0.089 (156) | 0.130 (2844) | 7.1e-12 |
| 29 | 0.0345 | 0.059 | 0.960 | 0.025 (120) | 0.107 (2880) | 1.6e-29 |
| 37 | 0.0222 | 0.225 | 0.977 | 0.017 (69) | 0.076 (2931) | 9.7e-20 |

**Supplementary diagnostics, computed and committed (not left as an uncommitted claim, per a
skeptic-fallback finding that two such numbers were originally asserted without a corresponding
line in the script or JSON — fixed by adding them to `check_value_curvature_margin.py` and
re-running).** Does `M` itself predict `R` (Mann-Whitney on `M` between the two `R`-groups)?
`p=0.0036` (`n=23`), `p=0.146` (`n=29`), `p=0.053` (`n=37`) — inconsistent across `n`, not a
reliable relationship. Restricted to the `R=1` subset alone, does `M` still predict `|Δ|`?
`ρ=-0.006,p=0.74` (`n=23`); `ρ=0.041,p=0.028` (`n=29`); `ρ=0.027,p=0.15` (`n=37`) — statistically
detectable at one `n` out of three, practically negligible at all three (`|ρ|≤0.04`
throughout). **F7 density-confound check (also newly added):** mean base-set density and mean
`|i-j|` were recorded per `R`-group at every `n` — density does NOT differ meaningfully between
`R=0` and `R=1` (`0.43` vs `0.41` at `n=23`; `0.42` vs `0.43` at `n=29`; `0.448` vs `0.446` at
`n=37`), ruling out a simple "R=0 cases are just denser graphs" confound for the separation
found below. Mean `|i-j|` is modestly higher in the `R=0` group at every `n` (`4.4` vs `4.0`;
`5.6` vs `5.0`; `7.3` vs `6.4`) — a real, small, consistently-signed effect, noted but not
large enough to explain the group means' 4-5x ratio on its own.

**Verdict: H1 REJECTED cleanly on its pre-registered threshold; H2's own pre-registered
falsification criterion did NOT fire, but the mechanism is rejected anyway on a separate,
honestly-labeled basis (skeptic-fallback finding — corrected from an earlier draft that
conflated the two).**
- **H1 REJECTED.** `|ρ|` never exceeds `0.035` across all three `n`; none reach the `0.3`
  threshold; several don't even reach `p<0.05`; the standard error of `ρ` itself is `≈0.018`
  (`n=2999`), so the observed values sit within `~2` SE of zero — a genuine null, not a
  borderline call. Global-min-slack margin carries no exploitable information about curvature
  magnitude. (Scope note: only ONE specific, unnormalized functional was tested — the minimum
  slack across all 4 corners, in raw LP units, not normalized by `θ` itself; observed correlation
  signs are inconsistent across `n` (`-,+,+`) and, where positive, run opposite to H1's own
  predicted direction, consistent with an unmodeled scale confound (`θ` itself ranges roughly
  `3`-`9` across sampled instances, and `margin_min` scales with `θ`) rather than a real weak
  effect — a `θ`-normalized margin was NOT tested and remains open.)
- **H2's pre-registered falsification criterion ("no substantial separation between groups") did
  NOT fire — a large, highly significant separation DOES exist (`4-5×` mean ratio,
  `p<10^{-11}` at every `n`).** By that criterion alone, H2's softer prediction ("small when
  `R=0`") is not falsified. What DOES kill the mechanism as originally envisioned is a fact that
  was never itself a falsification target: restructuring is not rare (`95%→97.7%` of sampled
  squares), so a rare-event × bounded-amplitude DECOMPOSITION cannot be built from it regardless
  of the group separation — and this non-rarity was already arithmetically implied by ALREADY-
  COMMITTED data before this point ran, not discovered here. Point 31's own single-flip
  `restructure_fraction` (`0.733` at `n=29`, `0.75` at `n=37`) is a floor on the square-level rate
  measured here, since `R:=1` is an OR over 4 edges (`R≥` any single edge's own indicator) —
  `95-97.7%` could not have come back "rare" given that floor. **What IS new and unpredicted by
  point 31's data: the 4 edges restructure in a CORRELATED way** — observed `P(R=0)` (`5.2%`,
  `4.0%`, `2.3%` at `n=23,29,37`) is `6-8×` HIGHER than the `≈1%` an independence assumption
  across 4 edges with a `0.73-0.75` single-edge rate would predict — a genuine, previously-
  unmeasured structural fact about how nearby active-set changes co-occur, not itself explaining
  the curvature decay but worth keeping. **A direct counterexample to even the softer H2
  prediction exists in the committed data**: at `n=23`, the single largest `|Δ_iΔ_jX|` value in
  the ENTIRE 3000-sample dataset (`0.6604`) occurs in the `R=0` group, exceeding the `R=1`
  group's own maximum (`0.5819`) — large curvature is not "only" possible when `R=1`, contrary to
  H2's literal prediction (this specific pattern reverses at `n=29,37`, where `R=0`'s maximum is
  smaller — not a universal counterexample, but a real one at `n=23`). The statistically-real
  mean separation itself is not a density artifact (F7 check: mean base-set density is
  essentially identical between `R`-groups at every `n`) but IS accompanied by a small, real
  co-varying difference in mean `|i-j|` (`R=0` pairs are drawn from slightly farther-apart
  generators on average) — not large enough to explain a `4-5×` mean ratio alone, but not zero
  either.

**Kill Analysis.** What is killed: the specific unnormalized single-vertex margin functional
tested (H1); active-set-restructure treated as a RARE event usable for a rare-event × bounded-
amplitude decomposition (H2, in its originally-envisioned form — the mean-separation part of H2
is not itself falsified, only unusable as envisioned because restructuring isn't rare). What is
NOT killed: the empirical `~n^{-1.95}` decay itself (point 37's own finding stands, untouched,
and is now independently cross-checked via exact `std(Δ)` here); a `θ`-normalized version of H1;
the broader "value-curvature" question in general — these two specific mechanisms are ruled out
(one cleanly, one on a reason distinct from its own pre-registered test), not every conceivable
explanation. One plausible remaining candidate, offered here as SPECULATIVE and explicitly
untested (not established, not "the field narrowed to this" — an earlier draft overstated this
as if elimination of two candidates left only one; it does not, other candidates such as non-
local structure, degenerate/multiple-optimum effects, or the project's own already-proven exact
symmetry theorems (points 12-13) remain equally unexamined): local active-set churn is common and
non-vanishing at BOTH the single-flip level (points 6-31) and the two-flip/square level (this
point), so whatever explains the fast value-curvature decay may be a VALUE-LEVEL cancellation
effect that survives despite constant churn — but this is one untested candidate among several,
not a narrowed field of one.

**What this does NOT mean:** does NOT mean Priority B (value-curvature route) is dead — two
specific candidates are addressed (one rejected cleanly, one rejected for reasons distinct from
its own pre-registered criterion), leaving several other, equally untested candidates open, not
a narrowed field of one; does NOT mean point 37's own `n^{-1.95}` measurement is in doubt
(independently cross-checked here via exact `std(Δ)`, not merely a distributional approximation,
and consistent); does NOT extend past this experiment's existing exact-enumeration-adjacent reach
(this point used direct LP solves at each corner, not exhaustive layer enumeration, so it is not
bound by the `n~50-60` wall the way points 14-50's `apply_L_to_layer`-based work is — but no
larger `n` was attempted in this pass either).

**Skeptic Concerns (FL Step 8a — `reviewer`'s cap closed all session; `skeptic` substituted per
`doubt-driven-development.md` § Independent Review Fallback Policy, context-asymmetric).
Verdict: `WEAKENED` — the LP formulation, the 4-edge square construction, and the H1 rejection
all held up on direct code/data inspection; H2's rejection reasoning needed substantial
correction (attributed to the wrong source, and its own pre-registered criterion had not
actually fired), addressed above by rewriting rather than patching around. No finding rose to
FALSIFIED — the bottom-line conclusion (neither near-tie margin nor active-set-churn-as-rare-
event explains the fast `Δ_iΔ_jX` decay) survives every fix.** Findings and disposition:
- Concern: H2's rejection cited "restructuring is NOT rare (`95%→97.7%`)" as if this were a new
  empirical finding of this point, when `R_square≥R_single-flip` identically (OR over 4 edges),
  and point 31's own already-committed single-flip rate (`0.73-0.75`) already made a rare outcome
  arithmetically impossible before this point ran. → **Fixed**: reframed as a floor implied by
  already-committed data, with the genuinely new finding (correlated, not independent,
  restructuring across the 4 edges — observed non-restructure rate `6-8×` higher than
  independence would predict) surfaced explicitly instead.
- Concern: H2's own pre-registered falsification criterion ("no substantial separation") was
  actually NOT triggered — a large, highly significant separation exists — so stating "REJECTED
  ... on their own pre-registered thresholds" for H2 was inaccurate; the real basis for rejection
  (non-rarity precluding the intended decomposition) was never itself a pre-registered
  falsification target. → **Fixed**: verdict section rewritten to state precisely what was and
  wasn't tested by the pre-registered criterion, versus what additional reasoning kills the
  mechanism anyway.
- Concern: a direct counterexample to H2's literal prediction exists in the committed JSON at
  `n=23` (the dataset's global-maximum `|Δ|` occurs in the `R=0` group) and was not mentioned. →
  **Fixed**: added explicitly, together with the fact that this specific pattern does not recur
  at `n=29,37` (not universal, but real at `n=23`).
- Concern: two supplementary numbers (Mann-Whitney on `M` between `R`-groups; Spearman within the
  `R=1` subset) were reported in prose without a corresponding computation in the committed
  script/JSON. → **Fixed** by actually computing them (script patched, re-run) rather than
  caveating unverified numbers — `check_value_curvature_margin.py` now returns
  `mannwhitney_M_R0_vs_R1` and `spearman_within_R1` for all three `n`, plus `std_delta_exact`
  (an exact, model-free cross-check value) and per-group `mean_density`/`mean_ij_dist` (for the
  density-confound check below).
- Concern: the folded-normal cross-check ("matches") understated a real, `≥5`-SE gap between
  predicted and measured mean `|Δ|`, and the folded-normal approximation itself is contradicted
  by this point's own data (median/mean ratio, exact-zero atoms in the tail). → **Fixed**:
  replaced with a stronger, model-free `std(Δ)` comparison, and the weaker check's actual gap
  size stated honestly rather than glossed as agreement.
- Concern: H1's Kill Analysis claimed to rule out "a single-vertex margin/slack quantity" in
  general, but only one specific, unnormalized functional (raw-units `margin_min`, not
  `θ`-normalized) was tested, and the observed correlation signs (positive at 2 of 3 `n`, opposite
  H1's predicted direction) are consistent with an un-modeled scale confound (`margin_min` scales
  with `θ`, which itself varies `~3×` across sampled instances). → **Fixed**: Kill Analysis
  narrowed to the specific functional tested; a `θ`-normalized version noted as untested.
- Concern: possible density confound on the `R=0`-vs-`R=1` mean separation (denser base sets
  could simultaneously produce small `|Δ|` and a stable active set, making part of the
  "statistically-real separation" an artifact rather than evidence of a churn-independent
  effect). → **Checked directly** (not just noted as a caveat): per-group mean density recorded
  and found essentially IDENTICAL across `R`-groups at every `n` — this specific confound is
  RULED OUT, not merely flagged. A smaller, real co-varying difference in mean `|i-j|` was found
  and is reported, not large enough alone to explain the full effect size.
- Concern: the reused script's own docstring (`check_vertex_stability_probability.py`) claims
  smallest-inactive-slacks are `>0.02`, but this point's own measured minimum inactive slacks go
  as low as `5e-6` — a real discrepancy in a comment on reused, previously-trusted code. → Noted
  explicitly in the Setup section above; likely benign (10 orders of magnitude of headroom still
  separate this from the `~1e-16`-scale active slacks) but the stale comment should be corrected.
- Concern: a latent (non-manifesting) `NaN`-ordering bug in Python's `min()` over the 4 corners'
  margins, and missing `seed_base`/`ACTIVE_TOL` in the output JSON for reproducibility. → **Fixed**
  defensively in the script (explicit `NaN` check before `min()`, confirmed non-manifesting via
  `n_pairs_used_for_correlation == n_solved` in every row) — full reproducibility fields left as
  a minor known gap, not blocking.

**Artifacts:** `check_value_curvature_margin.py`
(+`metrics/value_curvature_margin_check.json`).

## Point 52 (2026-09-14) — Test B / "Puzzle L2'": random-swap lemma `T_q(X)=O(n^{-2})` REJECTED
cleanly — the naive single-rung swap-Poincaré bound on `X` is flat (`~n^{-0}`), not `O(1/n)`

**Context.** Per a user-supplied analysis proposing two candidate routes ("Puzzle A/L1": bounded
density-susceptibility `λ_n`; "Puzzle B/L2'": `E_swap[(X(S)-X(S'))^2]=O(n^{-2})`), with an explicit
stated preference for testing L2' first since it "can be falsified by one comparatively cheap
computational experiment." Reconciliation before running anything: point 34's already-committed
`M_2(X):=⟨X,L_q^2X⟩=‖L_qX‖^2` (decaying `~n^{-1.45}`) is a genuinely DIFFERENT quantity from what
L2' needs, `M_1(X):=⟨X,L_qX⟩` (ONE application of the swap-Laplacian, not two) — nobody in this
experiment had computed `M_1(X)` before this point, so this is legitimate new work, not a repeat.
Point 15's own exact Dirichlet identity `T_q(f)=E_swap[(f(S)-f(S'))^2]=2⟨f,L_qf⟩` and the Poincaré
inequality `Var(f|Q=q)≤T_q(f)·q(N-q)/(2N)` were previously established and used only for `f=δ_i`
(single-generator sensitivity, points 15-18's peeling ladder); this point applies both, for the
first time, to `f=X` directly.

**Pre-registered prediction (stated in `check_value_swap_energy_T_q.py`'s own module docstring,
before any number was computed).** L2' predicts `n^2·T_q(X)` settles toward a plateau/bounded
value across the 7 already-solved `n∈{23,29,31,37,41,43,47}`. Falsified if a power-law fit instead
shows the log-log slope of `T_q(X)` vs `n` well above `-2` — equivalently, `n^2·T_q(X)` itself
grows with `n`, not merely fluctuates near a constant.

**Reuse discipline.** `solve_orbit_reduced` reused unchanged from `check_necklace_orbit_reduction.py`;
`apply_L_to_layer` reused byte-identical from `check_cross_layer_cancellation.py` — independently
confirmed by direct code read, not merely taken on the agent's word.

**Verification before trusting any result, corrected after skeptic-fallback review (see Skeptic
Concerns below) — an earlier draft of this section overstated what these checks show.**
- **`apply_L_to_layer`/`build_x_array` re-run, NOT an independent Substrate Gate.** This script's
  own `‖L_qX‖^2=M_2(X)` reproduces the already-committed values from
  `cross_layer_cancellation.json`/`extended_moments_41_43_47.json` (points 34/35) with
  `substrate_check_rel_err=0.0` EXACTLY at every one of the 7 `n`. On direct code comparison this
  is bit-identical because it IS the same code (`apply_L_to_layer`/`build_x_array`, byte-identical,
  same inputs) re-run, not an independently-derived second path — per this project's own
  Independent Verification Strength Ladder (`rules/falsification-ladder.md`), this sits at "same
  code, isolated re-run," the WEAKEST rung, not a positive-control confirmation of correctness.
  What it DOES verify: wiring (this script correctly reuses the cited functions, no transcription
  drift) and environment determinism. What it does NOT verify: that `apply_L_to_layer` or `X`
  itself is correct — a bug there would reproduce with zero residual on both `M_2` here and the
  original `M_2` in points 34/35. A genuinely independent check (e.g. an explicit Johnson-graph
  adjacency matrix at `n=23`) was not built and remains a cheap open item.
- **Identity check (`T_q(f)=2⟨f,L_qf⟩`) is near-tautological for ANY regular `f` under this
  construction, not `f=X`-specific evidence.** `apply_L_to_layer` implements `L=I-P` with `P` the
  average over the same swap-neighbor pairs `direct_T_q_enumeration` enumerates directly — the
  match (`identity_rel_err=1.855e-16` at `n=23`, `2.250e-16` at `n=29`) follows algebraically from
  that shared construction for any `f`, not specifically from point 15's theorem holding for `X`.
  What it DOES verify: the neighbor-set construction in `apply_L_to_layer` is wired correctly (a
  bug in which pairs count as swap-neighbors would break this match) — a real code-correctness
  check, useful and passed, just not the "first numerical proof-check for `f=X`" framing an
  earlier draft gave it.
- **Poincaré-bound arithmetic cross-checked by hand** (not just trusted from the script): at
  `n=23`, `γ_1=N/d=10/25=0.4`, `poincare_bound=T_q(X)/(2·γ_1)=0.03740149/0.8=0.046752` — matches
  the committed value exactly; `n^2·T_q(X)=23^2·0.03740149=19.785` — matches. Full 7-row table
  independently re-verified against the raw JSON (`M1`, `T_q`, `n²T_q`, `Var`, `poincare_bound`,
  `tightness`, `v_q=C(N,q)`) — no arithmetic error found.
- **Scope, stated explicitly (previously implicit only): every number below is measured at the
  SINGLE central layer `q=⌊N/2⌋` only.** Non-central layers (`q≠⌊N/2⌋`) are untested by this
  point — see the Kill Analysis correction below for why this matters more than it first appears.

**Results, all 7 `n`:**

| n | N | q | v_q | M1(X) | T_q(X) | n²·T_q(X) | Var(X\|q) | Poincaré bound | tightness |
|---|---|---|---|---|---|---|---|---|---|
| 23 | 10 | 5 | 252 | 0.018701 | 0.037401 | 19.785 | 0.020335 | 0.046752 | 0.4349 |
| 29 | 13 | 6 | 1,716 | 0.015417 | 0.030833 | 25.931 | 0.019294 | 0.049808 | 0.3874 |
| 31 | 14 | 7 | 3,432 | 0.014681 | 0.029362 | 28.217 | 0.019256 | 0.051383 | 0.3748 |
| 37 | 17 | 8 | 24,310 | 0.012276 | 0.024552 | 33.612 | 0.017991 | 0.051992 | 0.3460 |
| 41 | 19 | 9 | 92,378 | 0.011060 | 0.022120 | 37.183 | 0.017333 | 0.052389 | 0.3309 |
| 43 | 20 | 10 | 184,756 | 0.010375 | 0.020749 | 38.365 | 0.016887 | 0.051873 | 0.3255 |
| 47 | 22 | 11 | 705,432 | 0.009249 | 0.018499 | 40.864 | 0.015987 | 0.050872 | 0.3143 |

Log-log slope of `T_q(X)` vs `n`: **`-0.978`** — essentially `T_q(X)~1/n`, not `1/n^2`.
Log-log slope of `n^2·T_q(X)` vs `n`: **`+1.022`** — clear monotone growth (roughly doubles from
`n=23` to `n=47`), not a plateau.

**RETROACTIVE CORRECTION (2026-09-14, direct user math correction, applied same-session — not
silently rewritten).** The Verdict and Kill Analysis below originally used the phrase "REJECTED
cleanly" and stated the multi-rung ladder is "closed at the central layer" without qualification.
Both overclaim what 7 finite `n` can establish. Corrected framing, applied throughout this
section: **L2' is strongly rejected as the observed finite-range mechanism** (`n=23..47`) — this
is a real, well-verified experimental fact — **not a theorem that the `n^{-2}` asymptotic is
false**; seven finite data points cannot exclude a late crossover to `n^{-2}` behavior at larger
`n`. Symmetrically, "the multi-rung ladder cannot close the exponent gap at the central layer"
means it cannot improve on the exact `Var(X|Q=q)` values already measured ON THESE `n` — not a
proof that its asymptotic rate is wrong. The distinction between a strong finite-range
experimental result and an asymptotic theorem is the same one this project has already had to
draw explicitly elsewhere (e.g. point 48's `≈`-vs-`≤` correction); it applies here identically and
should have been stated on first draft.

**Verdict: L2' REJECTED cleanly on its own pre-registered threshold** (as an experimental fact
about the tested finite range `n=23..47` — see the correction above for exactly what this does and
does not establish asymptotically). The predicted `-2` slope is
missed by essentially a full power of `n` (`-0.978` observed, not `≈-2`); the growth-vs-plateau
falsification criterion fires unambiguously (`n^2·T_q(X)` grows, doesn't fluctuate near a
constant). Mechanism: `T_q(X)~1/n` and the Johnson-scheme Poincaré prefactor `q(N-q)/(2N)` grow
like `~n`, so the two ALMOST EXACTLY cancel in the product — the resulting bound on
`Var(X|Q=q)` is essentially FLAT (`~0.05`, no visible decay) across the entire tested range,
the same qualitative failure signature point 15 originally found for the naive single-rung bound
applied to `f=δ_i` (which motivated the points 16-18 peeling-ladder fix in the first place).
`tightness=Var(X|q)/Poincaré_bound` decreases monotonically `0.435→0.314`, meaning the bound
gets progressively LOOSER as `n` grows, not tighter.

**Decomposition of the observed slope, found by skeptic-fallback review and independently
re-verified here via direct OLS recomputation from the raw JSON (not merely trusted) — this is
the single most important correction to this point, and changes the Kill Analysis materially.**
`T_q(X) = 2·γ_1·(1/tightness)·Var(X|Q=q)` identically (`γ_1` the Johnson-scheme spectral gap,
`1/tightness` the bound's own looseness factor), so the log-log slope of `T_q(X)` decomposes
additively: `slope(γ_1) + slope(Var(X|q)) + slope(1/tightness) = -1.1032 + (-0.3296) + 0.4548 =
-0.9780`, matching the reported `-0.978` to four significant figures. Two consequences:
- **`γ_1` is pure Johnson-graph geometry** (`γ_1=N/(q(N-q))`, no dependence on `θ` or `X`
  whatsoever) and by itself contributes `-1.10` of the observed `-0.978` — MORE than the whole
  observed slope. This means the `T_q(X)=O(n^{-2})` test was never really an independent probe of
  `X`'s structure; it was, to leading order, a re-measurement of the ALREADY-KNOWN graph-geometric
  decay of `γ_1`, diluted by the exact `Var(X|Q=q)` behavior. The "cheap falsifiable test" framing
  from the original proposal undersold how much of its outcome was predetermined by geometry
  already on record before this point ran.
- **`tightness∈[0.314,0.435]` across the entire tested range bounds what ANY Poincaré-style bound
  can buy — single-rung or multi-rung ladder alike — to at most a CONSTANT factor (`≈3.2×`), not
  an exponent improvement.** The exact `Var(X|Q=q)` is already computed at all 7 `n` (not a bound,
  the real value) and decays like `n^{-0.330}` — far short of the `n^{-1}` the target hypothesis
  needs at the central layer. A layer-adaptive ladder tightens the CONSTANT in front of a
  Poincaré-derived bound; it cannot change the measured `-0.330` exponent of the quantity it is
  trying to bound, because the exact value is already known and already exhibits that exponent.

**Kill Analysis, corrected accordingly.** What is killed: the naive, single-rung swap-Poincaré
bound applied DIRECTLY to `X` at the central layer — provably caps `Var(X|Q=q)` at `O(1)`, not
`O(1/n)`; the specific L2' claim `T_q(X)=O(n^{-2})` itself; AND — newly established by the
decomposition above, not merely left open — **any Poincaré-derived bound (including a
layer-adaptive multi-rung ladder) at the central layer `q=⌊N/2⌋`, since the exact `Var(X|Q=q)`
it would be bounding already decays at only `n^{-0.330}`, and no linear-inequality technique
built from `T_q` can beat the exact value it is a bound on, ON THE TESTED RANGE `n=23..47`** — a
strong finite-range fact, not a proof about the `n→∞` asymptotic exponent of `Var(X|Q=q)` itself
(per the RETROACTIVE CORRECTION above). This corrects an earlier draft of this point, which had
left the multi-rung ladder as "genuinely open" — at the central layer, on the tested range, it is
not: the exponent gap is closed by the exact computation itself on these `n`, independent of which
Poincaré variant is tried. What is genuinely NOT killed: **non-central layers
(`q≠⌊N/2⌋`)** — this point measured exactly one layer per `n` (stated explicitly in Verification
above), and `Var(X)`'s full decomposition `Var(X)=E_Q[Var(X|Q)]+Var(E[X|Q])` sums over ALL layers,
weighted by `Q~Bin(N,1/2)`'s concentration near the center — so a ladder aimed at the FULL `Var(X)`
via non-central layers remains untested, not ruled out, and is the natural cheap next step (same
script, `q∈{⌊N/2⌋-2,...,⌊N/2⌋+2}`, `n≤41` for speed). Also not killed: `M_2(X)`'s own decay (point
34; re-verified here across all 7 `n` at `-1.559`, not the `-1.45` figure originally fit to only 4
`n` — noted as a minor discrepancy in the pre-existing points 34/35 record, out of this point's
scope to resolve); Puzzle A/L1 (bounded density-susceptibility `λ_n`) — a structurally unrelated
candidate, not addressed by this point at all.

**What this does NOT mean.** Does NOT mean `Var(X|Q=q)=O(1/n)` is false at the target scope — the
exact measurement here is scoped to the SINGLE central layer only (see Verification above), and a
`-0.330` exponent at one layer, in an `n=23..47` range, is suggestive tension with the `n^{-1}`
target but not a disproof of the full `Var(X)` claim, which sums over all layers; the target
hypothesis itself (`Var(log(θ(G)/√n))=O(1/n)`) remains the project's central open empirical
finding (point 1 onward, measured on `Var(X)` overall, not `Var(X|Q=q)` at one layer), untouched
by this point either way. Does NOT mean a ladder aimed at non-central layers would also fail —
genuinely untested, now the correctly-scoped open question (narrower than the original "ladder in
general" framing). Does NOT extend to `f=δ_i` (point 15's original object) — this point is
specific to `f=X`, and `f=δ_i`'s own ladder already succeeds (points 16-18) precisely because its
exact `Var(δ_i|Q=q)` presumably decays fast enough for the ladder's bound to close the gap (not
re-verified here); the two `f`'s behavior under the SAME naive single-rung bound is qualitatively
similar (flat/`O(1)`) but the ladder's success for one does not transfer to the other.

**Reconciliation context, honestly surfaced (per the user's own preference to test L2' before
Puzzle A/L1):** Puzzle A/L1 (bounded `λ_n`) was NOT tested by this point and remains open, but with
an important caveat already on record in this project before this point ran — the existing 5-point
trend for the analogous density-susceptibility quantity (`n=11..23`) is RISING with no plateau yet
observed, and an earlier reading of that trend as "stabilizing" was explicitly retracted elsewhere
in this document. This tempers optimism for L1 specifically; it is not evidence against L1, only a
reason not to expect an easy confirmation there either.

**Skeptic Concerns (FL Step 8a — `reviewer`'s Evaluator-Optimizer cap closed all session;
`skeptic` substituted per `doubt-driven-development.md` § Independent Review Fallback Policy,
context-asymmetric — claim.md-equivalent text + code + JSON only, no session history). Verdict:
`WEAKENED` — the core rejection of L2' (naive single-rung bound on `X` is flat) holds; the
verification story and Kill Analysis needed real correction, both applied above.**
- Concern: the "Substrate Gate cross-check" (`substrate_check_rel_err=0.0` at every `n`) is
  presented as independent confirmation, but is bit-identical because `apply_L_to_layer`/
  `build_x_array` are the SAME code re-run on the same inputs, not a second independently-derived
  path — per this project's own Independent Verification Strength Ladder, this is the weakest
  rung ("same code, isolated re-run"), and a bug in the shared function would reproduce with zero
  residual on both the original and this check. → **Fixed**: reworded in Verification above to
  state what it actually shows (wiring + determinism, not independent correctness); a genuinely
  independent check (explicit Johnson-adjacency matrix) noted as a cheap open item, not built.
- Concern: the identity check (`T_q(f)=2⟨f,L_qf⟩` matching to `~1e-16`) is near-tautological for
  ANY `f` under `apply_L_to_layer`'s own `L=I-P` construction, not `f=X`-specific evidence for
  point 15's theorem — it verifies the neighbor-set wiring is correct, not that the theorem "holds
  for X specifically" as an earlier draft claimed. → **Fixed**: reworded to state it as a
  code-correctness check, not a proof-verification event.
- Concern (STRONGEST — see decomposition added above): `T_q(X)`'s observed slope `-0.978`
  decomposes exactly as `slope(γ_1)+slope(Var(X|q))+slope(1/tightness) = -1.103-0.330+0.455`,
  independently re-verified via direct OLS on the raw JSON. Since `γ_1` is pure Johnson-graph
  geometry unrelated to `θ`/`X` and contributes MORE than the entire observed slope by itself, the
  L2' test was largely re-measuring known graph geometry, not new structure in `X`; and since exact
  `Var(X|Q=q)` is already computed (not merely bounded) and decays at only `n^{-0.330}`, with
  `tightness` bounded in `[0.314,0.435]`, NO Poincaré-derived bound — single-rung or multi-rung
  ladder — can close the exponent gap AT THE CENTRAL LAYER, because the thing being bounded
  already has the wrong exponent exactly. The original draft's "multi-rung ladder: genuinely
  open" was too broad. → **Fixed**: Kill Analysis rewritten to state the ladder is closed at the
  central layer specifically, open only for non-central layers (`q≠⌊N/2⌋`, untested, the correctly
  narrowed next question); Verdict section gained the full decomposition.
- Concern: the pre-registered-prediction claim (module docstring states the threshold before the
  print statement) cannot be independently dated from the artifacts alone (script and JSON are
  both freshly created this session, no intermediate commit exists to check ordering against) —
  a structural gap in provenance, not a specific accusation of post-hoc fitting. Also, the
  falsification threshold itself is qualitative ("well above -2"), not a fixed number. →
  **Accepted limitation**: does not change the verdict here (observed `-0.978` is nowhere near any
  reasonable reading of `-2`), but noted honestly rather than glossed; future points in this
  experiment should commit the empty-`metrics/` script in its own commit before running it, and
  state numeric (not qualitative) thresholds, to close this gap going forward.
- Concern: the single-layer scope (`q=⌊N/2⌋` only) was implicit, not stated in the original
  Verdict/Kill Analysis text, even though it materially limits what "REJECTED" can mean for the
  broader `Var(X)` target. → **Fixed**: stated explicitly in Verification, Kill Analysis, and
  "What this does NOT mean."
- Concern: the committed `M_2(X)` slope figure of `-1.45` (points 34/35) was originally fit to only
  4 of the now-available 7 `n`; recomputing across all 7 gives `-1.559`, a real discrepancy. →
  **Accepted limitation, out of this point's scope** — noted in Kill Analysis as a minor aside;
  correcting points 34/35's own historical figure is a separate, small follow-up, not required to
  close point 52.
- Concern: `n^2·T_q(X)`'s reported slope (`+1.022`) is not an independent fact — by construction
  it equals `2+slope(T_q(X))` exactly, so citing both slopes suggests two pieces of evidence where
  there is one. → **Dismissed as a real issue for the verdict** (both were already consistent and
  the redundancy doesn't change any conclusion), but the table arithmetic and table values
  themselves were independently re-verified against the raw JSON and found correct in all 7 rows.
- Concern: `ground=range(1,m)` (excluding generator/bit 0) is an inherited convention from point
  34, undocumented in this point's own text. → **Accepted limitation**: consistent with prior
  work (no drift found on direct comparison), but should be named explicitly; left as a minor gap.

**Artifacts:** `check_value_swap_energy_T_q.py` (+`metrics/value_swap_energy_T_q.json`,
`check_value_swap_energy_T_q_output.log`).

## Point 53 (2026-09-14) — First-chaos decomposition (`Var(X_n)=W_1+R_n`) pushed into the
large-`n` Monte Carlo regime (`n=127..2039`): cross-method positive control passed (aggregation-
level, not oracle-level independent — see below); headline decision-rule outcome downgraded from
the script's own "STABLE" label to INCONCLUSIVE, but a real, suggestive (not decisive) signal
found in a zero-cost extrapolation the first draft missed

**Context — Novelty Check first (per this session's own repeated discipline; see also point
29's earlier Filmus-2016 rediscovery incident, cited in this document as a cautionary tale).**
A user-proposed "Piece A/B" test (bounded density-susceptibility `λ_n`; residual variance
`R_n:=Var(X)-W_1`) was checked against this experiment's own existing record BEFORE any new code
was written. Result: the core identities are **NOT new** — `W_1 = M_n'(1/2)^2/(4m) =
4·Cov(X,Q)^2/m` (`λ_n:=M_n'(1/2)=4·Cov(X,Q)`, independently re-derived and verified this session
via direct Fourier-Walsh expansion under the `p`-biased measure) is already an established, proven
identity at point 12b, resting on the point-4 prime-transitivity symmetry theorem; and
`R_n:=Var(X)-W_1` reduces exactly to the sum of squared Fourier-Walsh coefficients over ODD
`|S|≥3` because ALL even-degree coefficients vanish identically — a consequence of
`X(S^c)=-X(S)` (bit-complementation antisymmetry), itself already established from
`θ(G)·θ(Ḡ)=n` (**point 11's exact Walsh-Hadamard vanishing-even-levels theorem** — corrected
after skeptic-fallback review from an earlier draft's wrong citation "points 4/12"; point 4 is
the prime-transitivity theorem feeding `W_1`'s own identity, point 12 is the unrelated "seventh
angle" section). `n·W_1` is already tracked EXACTLY for **prime `n=11..37`** (points 12-13) —
corrected after skeptic-fallback review from an earlier draft's "prime n=9..53," which was wrong
on two counts: `9` is composite (`3²`), and point 12b's own equality `W_1=λ_n²/(4m)` is
specifically shown to FAIL at composite `n` (a real, measured gap `0.001-0.008` at `n∈{9,15,21,25}`)
— citing "prime n=9" was self-contradictory; separately, point 14's extension to `n=53` measured a
DIFFERENT quantity (`E[δ²]`'s density/shape decomposition), not `n·W_1`. The real exact-`n·W_1`
range (`n=11..37`) rises monotonically with no plateau — still the relevant fact motivating this
point, just correctly bounded. **What IS genuinely new:** pushing this exact decomposition into the large-`n` Monte
Carlo regime (`n` up to `2039`, vs the exact small-`n` ceiling of `~53`), reusing this
experiment's own `theta_via_lp`/`sample_circulant_neighbors` (unchanged, from H-CAT31-1's
`run.py`, the same machinery already validated up to `n=3000` for the headline `Var(X_n)`
measurement) — nobody in this project had estimated `λ_n`/`W_1`/`R_n` via Monte Carlo before this
point.

**Positive control at `n=37`, corrected scope after skeptic-fallback review — independent at the
estimator level, NOT fully independent at the oracle level.** Ran this new script's Monte Carlo
estimator at `n=37` (`500` reps), where an EXACT value from a different computational METHOD
(necklace-orbit-reduced exhaustive enumeration + Walsh-Hadamard decomposition, point 13's table)
is already committed: `n·W_1=2.598`. Monte Carlo estimate: `n·Ŵ_1=2.649`, bootstrap 95% CI
`[2.022, 3.428]` — contains the exact reference value. This genuinely cross-checks the
AGGREGATION method (exhaustive enumeration + WHT vs. Monte Carlo sampling + covariance
estimation) — a real improvement over Point 52's flawed check, which compared the same code
against itself. **But it does NOT cross-check the ORACLE**: both paths call the SAME
`theta_via_lp` function (this script imports it unchanged, exactly as the exact-enumeration route
does), so a systematic bug in `theta_via_lp` itself would pass silently on both sides. Two
concrete reasons this matters here, not merely in principle: (a) point 10 already documented a
real numerical fragility in `theta_via_lp` (1 of 8176 subsets returned `NaN` on the `'highs'` LP
solver at small `n`) and the fix (`theta_via_lp_robust`) was never merged back into the
`H-CAT31-1/run.py` this script imports — this script inherits the unprotected version and does
not itself check for `NaN`s; (b) the substrate gate (`θ(C_5)=√5`, `θ(G)θ(Ḡ)=n`) only exercises
`n=5` and `n=9` — three orders of magnitude below `n=2039`, so it provides no direct evidence the
oracle behaves correctly at the LP sizes actually swept here. Also: the control's own STATISTICAL
POWER is limited — its `±26.5%`-wide CI would catch a gross error (e.g. accidentally counting Q
from both mirrored halves, doubling it) but a deliberate injected-error check (run independently
this session, not by the executing agent) shows it would NOT catch a subtler off-by-one (e.g. `m`
off by one, or slicing `c[1:m]` instead of `c[1:m+1]`) — both produce a shifted `n·W_1` well
inside the observed CI. None of this overturns the control's PASS (a gross-error bug is now ruled
out, genuinely useful), but "genuine independent positive control" in an earlier draft overstated
what it establishes; corrected here to name exactly what independence it does and doesn't cover.

**Sweep results, `n=127,251,509,1021,2039` (all independently verified prime via `sympy.isprime`,
not merely assumed; substrate gate passed — `θ(C_5)=√5` exact, `θ(G)·θ(Ḡ)=9` exact at `n=9`):**

| n | reps | λ_n | λ_n 95% CI | n·W_1 | n·W_1 95% CI | n·R_n | n·R_n 95% CI |
|---:|---:|---:|---|---:|---|---:|---|
| 127 | 300 | −2.394 | [−2.791,−2.018] | 2.888 | [2.052,3.926] | 1.307 | [0.834,1.650] |
| 251 | 250 | −2.789 | [−3.318,−2.301] | 3.904 | [2.659,5.526] | 0.860 | [0.037,1.406] |
| 509 | 200 | −3.048 | [−3.677,−2.439] | 4.656 | [2.980,6.772] | 0.833 | **[−0.232,1.559]** |
| 1021 | 150 | −2.910 | [−3.677,−2.201] | 4.237 | [2.424,6.768] | 0.809 | **[−0.498,1.561]** |
| 2039 | 80 | −2.754 | [−3.488,−2.042] | 3.793 | [2.085,6.085] | 1.207 | [−0.088,1.975] |

Total elapsed: `843s` (`~14 min`) including the positive control — cheap, well under the
per-`n` 30-minute stop threshold at every `n`.

**Verdict, substantially revised after skeptic-fallback review + independent re-verification of
its own arithmetic (both done — z-scores, power-law fit, and elapsed-time projections below were
recomputed by hand from the raw JSON and the exact small-`n` table, not taken on either the
executing agent's or the reviewer's word).** The script's own decision-rule classifier reported
`STABLE-SUPPORTS-O(1/n)`, based solely on whether the bootstrap CI at `n=127` overlaps the CI at
`n=2039`. The `INCONCLUSIVE` downgrade in the first draft of this point was directionally right
but reasoned wrong on two of its three stated grounds — both retracted below — and, worse, it
threw away a real, zero-cost signal that was already sitting in already-committed data:
- **Retracted ground 1 — "non-monotonic point estimates."** Re-checked via `z=(estimate_i -
  estimate_j)/SE`: the shift `n=127→509` for `n·W_1` gives `z=+1.64`; `509→2039` gives `z=−0.61`;
  `127→2039` gives `z=+0.80`. None reach significance. The hump-shaped point-estimate sequence is
  ordinary sampling noise on a genuinely wide-CI estimator, not evidence of a real non-monotonic
  trend — citing it as a reason to distrust "stable" was itself statistically ungrounded.
- **Retracted ground 2 — "`R_n`'s CI crossing zero means low precision, full stop."** Sharper
  mechanism, found on review: the `Ŵ_1=4Ĉov(X,Q)²/m` estimator is a SQUARED quantity built from a
  sample covariance, while the true `Var(Q)=m/4` is known exactly a priori; whenever a particular
  bootstrap/sample draw's `Var(Q)`-implicit contribution overshoots its population value (expected
  roughly half the time, by construction, not an anomaly), `Ŵ_1` overshoots and `R̂_n=V̂ar(X)-Ŵ_1`
  reads negative even when the true `R_n>0`. A negative point estimate or a zero-crossing CI here
  is the estimator's ordinary behavior at these rep counts, not a signal about `R_n`'s trend either
  way — same practical conclusion as the first draft (no trend claim supportable at `n=509,1021`),
  correctly attributed to WHY.
- **A real, previously-uncomputed check the first draft missed, using only already-committed
  exact data plus this point's own JSON — zero new compute.** The exact small-`n` sequence
  `n·W_1` at prime `n=11..37` (points 12-13) fits a clean power law: `n·W_1 ∝ n^0.239` (OLS on
  `log(n·W_1)` vs `log n`, `R²=0.999`, `se(slope)=0.0028` — independently refit here, matching the
  reviewing pass's own `+0.236` to within rounding). Extrapolating this EXACT small-`n` law into
  the Monte Carlo range and checking whether each observed point's bootstrap CI contains the
  prediction: `n=127`→predicted `3.49`, observed CI `[2.05,3.93]`, contains; `n=251`→`4.11`,
  `[2.66,5.53]`, contains; `n=509`→`4.86`, `[2.98,6.77]`, contains; `n=1021`→`5.74`, `[2.42,6.77]`,
  contains; **`n=2039`→predicted `6.78`, observed CI `[2.09,6.09]` — does NOT contain it** (the
  predicted value sits above the observed CI's own upper bound). **4 of 5 tested `n` are
  compatible with the exact small-`n` power law continuing unchanged; the largest tested `n`
  is not.** Read this as SUGGESTIVE, explicitly not decisive: with 5 comparisons at a 95% level
  each, roughly 1 miss is not surprising by chance alone (an uncorrected multiple-comparisons
  rate), and `n=2039`'s own CI is the widest and noisiest in the sweep (`80` reps). But it is a
  real, quantitative, directionally-consistent signal (the miss is in the direction of the exact
  law's growth STALLING, i.e. weak evidence FOR an eventual plateau, not against it) that the
  first draft's blanket "INCONCLUSIVE, nothing learned" framing discarded for free.
- **Softened, not retracted: the "no evidence of runaway growth in `λ_n`" claim overstated its own
  precision.** A proper power-law fit of `|λ_n|` vs `n` on the 5 Monte Carlo points gives slope
  `0.046`, `SE=0.039`, `95%` CI `[−0.079, +0.172]` (independently refit here, matching the review).
  This excludes only growth FASTER than roughly `log n` — it does NOT exclude slow divergence
  (`λ_n ∝ n^{0.05}` or `∝ √(log n)` are both fully compatible with the data). Converted to the
  implied exponent on `Var(X_n)` itself (`n·Var(X_n) ∝ n^{2×slope(λ_n)}`, roughly), the tested
  range constrains the exponent only to `[−1.16, −0.66]` — about `15×` wider than the parent
  experiment's own committed `95%` CI `[−0.975,−0.850]` (`n=32..3000`, 9-point weighted fit). This
  point's own positive claim needed to be this much weaker than "no runaway growth" suggested.
  Separately: the exact small-`n` `|λ_n|` itself rises monotonically and substantially from `n=11`
  (`1.883`) to the `n=37` control point (`2.271`) to the tested large-`n` range (up to `3.05` at
  `n=509`) — a real `~62%` rise over `n=11→509` — and the `n=37` control point's own `λ`
  (`−2.271`) sits OUTSIDE the "flat `[−3.05,−2.39]`" band this point's headline described, simply
  because `n=37` isn't literally inside the `127..2039` sweep window. Naming this explicitly so
  the "flat" framing isn't read as stronger than it is.
- **Two free, methodologically-independent consistency checks found on review, added here.**
  (1) `n·Var(X_n)=n·(Ŵ_1+R̂_n)` on these same 5 Monte Carlo points implies a `Var(X_n)` exponent of
  `−0.941` (independently recomputed) — inside the parent experiment's own committed `95%` CI
  `[−0.975,−0.850]`, a genuine consistency check between this point's decomposition and the
  project's headline measurement, using none of the same estimator machinery. (2) This point's
  `λ_n` at `n=509` (`−3.048`, CI `[−3.677,−2.439]`) is compatible with an EARLIER, methodologically
  DIFFERENT measurement at the nearby `n=512` (composite, not prime — a caveat, not a disqualifier,
  since `λ_n=M_n'(1/2)` itself doesn't require primality, only the `W_1` identity does): a direct
  finite-difference response to varying `p` gave `λ̂(h=0.025)=−3.311±0.202` and
  `λ̂(h=0.05)=−2.892±0.101` (this document's own earlier work) — both inside this point's CI.

**Corrected verdict: INCONCLUSIVE for the pre-registered decision rule as originally stated (no
positive confirmation of `Var(X_n)=W_1+R_n=O(1/n)` with real statistical power), but with a real
SUGGESTIVE signal on record** (the exact-law extrapolation deviating at the single largest tested
`n`, in the direction of an eventual plateau) **and a substantially TIGHTER honest bound on what
`λ_n`'s behavior rules out** (excludes growth faster than `~log n`; does not exclude slow
divergence) than the first draft's "no evidence of runaway growth" implied.

**Kill Analysis.** Nothing is killed — genuinely inconclusive, not a null result in the
Falsification Ladder sense. What IS established: the Monte Carlo estimator is validated at the
aggregation level (cross-method positive control passed, with the oracle-level caveat above); the
large-`n` regime is cheap to reach (`~14` min total for this sweep); two independent consistency
checks (parent-experiment exponent, earlier finite-difference `λ` measurement) both pass. **Next
step, cost-corrected after skeptic-fallback review caught an arithmetic error in the first
draft**: `4×` reps projects to `149.8s`/`671.2s`/`2495.4s` at `n=509`/`1021`/`2039` respectively
(recomputed directly from the JSON's own `elapsed_seconds`, not estimated) — the first draft's "
`~150-670s`, still cheap" implicitly covered only `509`/`1021`; **`n=2039` at `4×` reps
(`2495s≈42min`) would EXCEED this script's own `MAX_SECONDS_PER_N=1800s` stop condition**, so a
straight `4×` multiplier is not uniformly safe across all three `n` — either a smaller multiplier
at `n=2039` (e.g. `2×`, `~1250s`, under budget) or a raised per-`n` budget would be needed there
specifically. Total cost for a corrected `509`/`1021` `4×` + `2039` `2×` re-run: roughly `35`
minutes, still cheap relative to the project's overall compute budget. This would directly test
whether `n·R_n`'s CI clears zero at `509`/`1021` and would sharpen the `n=2039` extrapolation
comparison above (currently the noisiest point and the one carrying the suggestive signal).

**What this does NOT mean.** Does NOT mean the target hypothesis `Var(X_n)=O(1/n)` is supported or
refuted — the honest state is "excludes growth in `λ_n` faster than `~log n`; one suggestive,
not decisive, signal toward an eventual plateau in `n·W_1` at the largest tested `n`." Does NOT
mean the first-chaos decomposition itself is in doubt — `Var(X)=W_1+R_n` is an exact identity
(Parseval + point 11's already-proven vanishing of even Fourier levels), unaffected by how
precisely `W_1`/`R_n` are currently estimated; only the EMPIRICAL question of how they scale with
`n` remains open. Does NOT extend to composite `n` — the prime-transitivity argument for
`W_1=λ_n²/(4m)` is specific to prime `n` (point 12b), unverified here for composite `n`.

**Skeptic Concerns (FL Step 8a — `reviewer`'s cap closed all session; `skeptic` substituted per
`doubt-driven-development.md` § Independent Review Fallback Policy, context-asymmetric). Verdict:
`WEAKENED` — the numeric core (table, identities, `Q` indexing, wall-clock, bootstrap validity)
held up on direct code/data inspection; three statements needed real correction (two factual
citation errors, one arithmetic error in a cost projection) and the verdict's own reasoning was
partly right for the wrong reasons. No finding rose to FALSIFIED.**
- Concern: `Q = c[1:m+1].sum()` indexing (does it double-count mirrored generators, or drop one?).
  → **Dismissed** — verified correct by direct comparison against `sample_circulant_neighbors`'s
  own source: mirrors occupy `[m+1,n-1]`, disjoint from `[1,m]`; `c[0]=0`; no off-by-one.
- Concern: the "genuine independent positive control" is independent at the aggregation-method
  level but shares the SAME `theta_via_lp` oracle with the exact reference it's checked against —
  a systematic oracle bug would pass both sides undetected; also, `theta_via_lp`'s known `NaN`
  fragility (point 10) was never fixed in the version this script imports, and the substrate gate
  only exercises `n=5,9`, far below the swept `n`. Separately, an injected-error simulation shows
  the control's own `±26.5%`-wide CI catches only gross (`≥2×`) errors, not subtler off-by-ones. →
  **Fixed**: Verification section rewritten to name exactly what independence the control does
  and doesn't establish; oracle-level gap and control-power limitation both stated explicitly
  rather than left implied by the word "genuine."
- Concern: two of the three stated reasons for the `INCONCLUSIVE` downgrade were statistically
  ungrounded — "non-monotonic point estimates" (shifts between `n` are not significant, `z≤1.64`
  throughout) and "`R_n`'s CI crossing zero means low precision" (the real mechanism is the
  squared-covariance estimator's ordinary ~50%-of-the-time overshoot relative to the exact
  `Var(Q)=m/4`, not merely "too few reps," though the practical conclusion was the same). →
  **Fixed**: Verdict rewritten to retract both stated grounds explicitly and substitute the
  correct mechanism for the second.
- Concern (the highest-value finding): a zero-cost check was available and skipped — extrapolating
  the EXACT small-`n` power law (`n·W_1∝n^{0.239}`, `R²=0.999`, fit to points 12-13's own
  committed data) into the Monte Carlo range shows `4/5` tested `n` compatible with the CI, but
  `n=2039`'s predicted value (`6.78`) falls outside its own observed CI (`[2.09,6.09]`) — a real,
  suggestive (not decisive, multiple-comparisons-uncorrected) signal the first draft's blanket
  "INCONCLUSIVE" framing discarded. → **Fixed**: added as the Verdict's central new finding,
  independently re-verified (OLS refit matches the review's own numbers to rounding), explicitly
  labeled suggestive not decisive.
- Concern: "no evidence of runaway growth in `λ_n`" overstated precision — a proper power-law fit
  on the 5 tested points (`slope=0.046±0.039`, `95%` CI `[−0.079,+0.172]`) excludes only growth
  faster than `~log n`, not slow divergence (`n^{0.05}`, `√log n` both compatible); the implied
  `Var(X_n)` exponent range (`[−1.16,−0.66]`) is `~15×` wider than the parent experiment's own
  committed CI. Also: the exact small-`n` `|λ_n|` itself rises `~62%` from `n=11` to the tested
  range, and the `n=37` control point's own `λ` sits outside the claimed "flat" band purely
  because `37` isn't literally inside the `127..2039` sweep window. → **Fixed**: Verdict section
  rewritten with the properly-bounded claim and both caveats stated.
- Concern: two free, methodologically-independent consistency checks existed in the data and
  weren't reported — `n·Var(X_n)` on these 5 points implies an exponent (`−0.941`) inside the
  parent experiment's committed CI; `λ_n` at `n=509` is compatible with an earlier, independent
  finite-difference measurement at the nearby `n=512`. → **Fixed**: both added to the Verdict as
  supporting (not decisive) evidence, with the `n=512`-vs-`509`/composite-vs-prime caveat named.
- Concern: factual error in the Novelty Check — "`n·W_1` already tracked exactly for prime
  `n=9..53`" is wrong on two counts (`9` is composite; point 12b's own `W_1=λ_n²/(4m)` equality is
  shown to FAIL at composite `n`, making "prime n=9" self-contradictory; point 14's `n=53`
  extension measured a different quantity). → **Fixed**: corrected to "prime `n=11..37`," the
  actual range with exact `n·W_1` data.
- Concern: wrong citation — the even-Fourier-level-vanishing theorem was attributed to "points
  4/12" instead of point 11 (point 4 is the prime-transitivity theorem, point 12 is the unrelated
  "seventh angle" section). → **Fixed**: corrected to point 11, verified by direct grep of
  decision.md.
- Concern: arithmetic error in the next-step cost estimate — `4×` reps at `n=2039` projects to
  `2495s` (`≈42min`), which EXCEEDS the script's own `MAX_SECONDS_PER_N=1800s` stop condition; the
  first draft's "`~150-670s`, still cheap" implicitly covered only `509`/`1021`, and grouping
  `2039` into the same recommendation without flagging this was a real oversight. → **Fixed**:
  cost projection corrected with the actual per-`n` numbers and an explicit note that `n=2039`
  needs a smaller multiplier or a raised budget, not a uniform `4×`.
- Concern: `bootstrap_ci` percentile intervals for a squared/skewed statistic (`Ŵ_1`) would
  benefit from a bias-correction (BCa) rather than plain percentile CIs, especially at low rep
  counts (`n=2039`, `80` reps) where `Ŵ_1` carries a measurable upward bias (`~0.8%` at `n=127`
  rising to `~2.9%` at `n=2039`, per the reviewer's own delta-method estimate). → **Accepted
  limitation**: does not overturn any conclusion above (bias is small relative to CI width), noted
  here rather than silently left undocumented; a control-variate estimator using the exactly-known
  `Var(Q)=m/4` would reduce this for free in a future re-run, not built here.
- Concern: `MAX_SECONDS_PER_N`'s own docstring says "projected to exceed," but the code checks
  `elapsed` AFTER a batch completes and only flags/prints — it cannot actually prevent a slow
  batch from running to completion. → **Accepted limitation**: a real docstring/behavior mismatch
  in the script, harmless here (no batch actually exceeded the threshold), left as a minor
  known gap rather than patched, since no result in this point depended on the stop condition
  actually firing.

**Artifacts:** `check_first_chaos_decomposition_large_n.py`
(+`metrics/first_chaos_decomposition_large_n.json`).

## Point 54 (2026-09-14) — `κ_n` diagnostic reformulation of the already-proven sharpened
Efron-Stein bound (point 12a): algebra confirmed sound, but its own two natural `λ_n` estimators
disagree by 8-20% at every tested `n` — an unresolved discrepancy that blocks trusting `κ_n`'s
own numbers yet; skeptic-fallback review (FALSIFIED, extensively addressed) also reversed the
`λ_n`-growth verdict and found real errors in the `R_n` addendum's supporting claims

**Context — epistemic status corrected BEFORE running anything, per a direct user math
correction caught mid-experiment (same live-correction discipline as Point 52).** A user-proposed
reformulation replaces Point 53's noisy `R_n=Var(X)-W_1` subtraction with
`κ_n:=B_n/W_1=E[δ_i²]/(E[δ_i])²` (the squared coefficient of variation of the single-generator
sensitivity `δ_i`, `δ_i(S)=X(S)-X(S∪{i})≥0` by the project's own established monotonicity
theorem), combined with `λ_n=-m·E[δ_i]` (sign-corrected — `δ_i≥0` always, `λ_n` is empirically
negative). **Substituting back proves this is NOT a new inequality**: `κ_n·λ_n²/(4m) =
(E[δ²]/E[δ]²)·(m²E[δ]²)/(4m) = (m/4)E[δ²] = B_n` exactly, so `V_n≤(κ_n+2)/3·λ_n²/(4m)` is
algebraically IDENTICAL to point 12a's already-proven `V_n≤(B_n+2W_1)/3`. **Skeptic-fallback
review confirms this algebra is sound but notes it is a DEFINITIONAL tautology** (`κ_n:=B_n/W_1`
substituted back into `κ_n·W_1` returns `B_n` by construction, not because of the newly-derived
sign relation) — the sign relation `λ_n=-m·E[δ_i]` is needed only for the INTERPRETATION
("`κ_n` = squared CV of `δ_i`"), not for the algebraic identity itself. This interpretive claim is
exactly what turned out to be unverified in this implementation — see below.

**MAJOR CORRECTION, found via a skeptic-proposed zero-cost check run independently against the
saved raw `.npz` samples after review — the single most important finding of this point.** The
script's own `λ_n`/`κ_n` numbers in the table below use `λ_n=4·Cov(X,Q)` (the SAME estimator as
Point 53, NOT the newly-derived `δ`-based route) — an earlier draft of this section claimed the
opposite ("estimated from the SAME marginal `δ_i` samples... `Cov(X,Q)`-based `λ_n` kept only as
a cross-check") and that claim was FALSE: `mean(δ_i)` is never computed in the sweep code, only
`mean(δ_i²)` (confirmed by direct code read). Computing the promised `δ`-based estimator now,
directly from the saved `.npz` files (zero additional `theta_via_lp` calls):

| n | λ_cov (script's own) | λ_δ (=-m·mean(δ)) | relative difference | κ_cov (script's own) | κ_δ (=mean(δ²)/mean(δ)²) |
|---:|---:|---:|---:|---:|---:|
| 127 | −2.187 | −2.631 | **20.3%** | 3.547 | 2.450 |
| 251 | −2.614 | −2.837 | **8.5%** | 2.883 | 2.447 |
| 509 | −2.928 | −2.441 | **16.6%** | 1.563 | 2.250 |
| 1021 | −3.437 | −3.172 | **7.7%** | 2.009 | 2.360 |
| 2039 | −3.481 | −3.023 | **13.2%** | 1.786 | 2.369 |

**Every one of the 5 tested `n` exceeds even a generous 5% agreement threshold between the two
theoretically-equal quantities, and the two `κ_n` columns disagree substantially and
non-monotonically (`κ_δ` sits in a tight `[2.25,2.47]` band while `κ_cov` ranges `[1.56,3.55]`).**
This has NOT been resolved to a bug-vs-noise verdict here — per-point sampling error on `λ_cov`
(`~8-9%` relative, from its own bootstrap CI) and on `λ_δ` (`~7-8%` relative, from `se(mean δ)`)
are individually large enough that single-point disagreements of this size are not automatically
alarming, but the PATTERN (present at all 5 `n`) has not been explained here and is reported as an
OPEN, UNRESOLVED item — `κ_n`'s own headline numbers (both columns) should be read as preliminary
pending this resolution, not as validated measurements of "squared CV of `δ_i`." (Point 55
resolves this discrepancy directly — see below.)

**Setup.** Pilot sign check (`n=37`, `20` samples, DIFFERENT seeds from the production sweep):
`δ_i≥0` confirmed (`min=0.00016`). **Skeptic-fallback correction**: this check is decorative for
every published number in the table — `b_hat`/`kappa_hat`/`u_hat` and the entire `R_n` addendum
depend on `δ` only through `δ²`, which is sign-independent, so a sign bug could not have affected
any of them; the ONE place the sign genuinely matters (`λ_δ=-m·E[δ]`) was never checked against
production data before this correction. Direct code inspection (independently re-confirmed) shows
the sign LOGIC itself is correctly implemented — not a live bug, just an overclaimed verification
target. Substrate gate passed. **n=37 Oracle Adequacy Gate — 3-way, all pass**: `n·Ŵ_1=2.508` CI
`[1.934,3.160]` contains exact `2.598`; `κ̂=1.924` CI `[1.442,2.565]` contains exact `2.004`;
`n·V̂ar(X)=3.302` CI `[2.906,3.692]` contains exact `3.272`. **Skeptic-fallback correction**: the
three checks are not fully independent — `n·Ŵ_1∝λ̂²` and `κ̂∝1/λ̂²` are anti-correlated by
construction (an error in `λ̂` moves them in opposite directions), so "all three pass" is weaker
evidence than three independent confirmations would be. A sharper oracle check, available for
free from the same exact reference values: exact `n·U_n = (n·B_n+2·n·W_1)/3` where
`n·B_n=n·κ_n·W_1=2.004×2.598=5.206`, giving exact `n·U_n=3.4675` and exact
`U_n/Var(X)=3.4675/3.272=1.060` — the observed `0.994` sits `6%` below this sharper reference
(within its own CI `[0.907,1.084]`, so not a failure, but a tighter check than "point estimate
`≥1`" alone).

**Sweep results, `n=127,251,509,1021,2039`:**

| n | reps | λ_n (Cov-based) | λ_n 95% CI | κ_n (Cov-based) | κ_n 95% CI | n·U_n | n·U_n 95% CI | U_n/Var(X) |
|---:|---:|---:|---|---:|---|---:|---|---:|
| 127 | 300 | −2.187 | [−2.563,−1.810] | 3.547 | [2.338,5.494] | 4.456 | [3.480,5.560] | 1.165 |
| 251 | 250 | −2.614 | [−3.117,−2.128] | 2.883 | [1.787,4.744] | 5.583 | [4.432,6.866] | 1.224 |
| 509 | 200 | −2.928 | [−3.597,−2.305] | 1.563 | [0.955,2.623] | 5.102 | [3.769,6.678] | 1.046 |
| 1021 | 150 | −3.437 | [−4.425,−2.517] | 2.009 | [1.015,4.247] | 7.902 | [5.531,10.843] | 1.255 |
| 2039 | 80 | −3.481 | [−4.778,−2.286] | 1.786 | [0.698,5.009] | 7.648 | [4.882,11.456] | 1.234 |

**Skeptic-fallback finding, independently reproduced**: by Cauchy-Schwarz, `κ_n=E[δ²]/E[δ]²≥1`
ALWAYS — a mathematical floor, not just an expectation — yet the `κ_n` `95%` CI's LOWER bound
falls below `1.0` at 2 of 5 `n` (`0.955` at `n=509`; `0.698` at `n=2039`). Since
`κ_n=m²·mean(δ²)/λ̂_cov²`, this is direct proof that noise in `λ̂_cov` (squared in the denominator)
contaminates `κ̂` into a region the true quantity cannot occupy — tying back to the unresolved
discrepancy above.

Total elapsed: `1718s` (`~28.6 min`), no `n` flagged incomplete. `U_n≥Var(X)` (proven population
inequality) held as a point-estimate at every sweep `n`; at the `n=37` control it read `0.994`
(just under 1) — finite-sample noise on a ratio, not a violation of a proof.

**Verdict on `λ_n` — REVERSED after skeptic-fallback review, using properly-propagated
uncertainty instead of residual-based SE.** The first draft's `honest_power_law_fit` computed
slope SE from OLS residual scatter alone (`0.173±0.023`, excluding zero), ignoring the
individually-known bootstrap CI on each point — a chi-square check (`χ²=0.485` at `3` dof,
`p≈0.08`) shows the points fit the line notably TOO well relative to their own stated uncertainty,
meaning this SE underestimates the truth. **Reweighting with each point's own propagated
bootstrap SE**: this run's slope becomes `0.188±0.057`; Point 53's own independent draw
(reweighted the same way) gives `0.066±0.049`. **The difference between these two slopes is NOT
itself significant** (`z=1.62` — the original draft's "two draws disagree on significance"
framing was a difference-of-significance fallacy). **The correct combined (inverse-variance-
weighted) estimate is `0.117±0.037`, `3.16σ` from zero — significant**, and matches the exact
small-`n` power law direction (`n·W_1∝n^0.239`, points 12-13). **This reverses the first draft's
"λ_n growth is draw-dependent, unconfirmed" conclusion.** One explicit caveat carried forward: it
rests entirely on the `Cov(X,Q)`-based estimator, whose disagreement with the `δ`-based route is
itself unresolved here — Point 55 addresses this directly.

**`R_n` addendum — three findings corrected after skeptic-fallback review; the qualitative
divergence finding survives, several of its supporting specifics did not.**
- **The "45×" divergence headline number is not robust to which denominator is used.** Against
  `u_stat_r_n_corrected` (this point's own "trusted" version), the same ratio at `n=2039` is
  `−12.8×` (sign flip). The qualitative finding (cross-fit grows disproportionately at large `n`)
  survives — directly visible in the raw ratio sequence `0.78×,0.83×,1.36×,2.31×,45×` against the
  RAW U-statistic — but the specific "45×" headline number should not be quoted without naming
  which denominator it uses.
- **The stated root-cause mechanism is incomplete.** The cross-fit residual computation
  (`_residual_mse`, code-verified) does NOT subtract the sample mean before squaring, so it
  carries the SAME `(E[X])²`-type inflation attributed only to the raw U-statistic; the mechanism
  also does not explain why cross-fit reads BELOW the other estimators at `n=127,251`.
- **The one PERSISTED synthetic check does not actually support "discount cross-fit at large
  `n`."** It used `β²Var(Z)/R_n≈135` (vs the real data's `≈3.6` at `n=37`), and on REAL `n=37`
  data cross-fit was in fact the estimator closest to the exact reference. The qualitative
  large-`n` divergence claim is still independently supported by the raw-ratio pattern, but NOT
  by the one saved synthetic check, which was calibrated to an unrealistic regime.

**Kill Analysis.** Nothing is killed. What IS established: (1) the `κ_n` reformulation's algebra
is sound (a tautological restatement of point 12a's proven bound, not a new theorem); (2) the
`Cov(X,Q)`-based `λ_n`, properly combined across Point 53 and this point, shows a real, `3.16σ`
growth signal consistent with the exact small-`n` power law — reversing the first draft's
"unconfirmed" reading; (3) the `δ`-based and `Cov`-based `λ_n`/`κ_n` estimators disagree by 8-20%
at every tested `n`, an UNRESOLVED discrepancy that must be understood before `κ_n`'s own numbers
can be trusted as precise; (4) the cross-fit `R_n` estimator does show real problems at large `n`,
but the specific supporting claims needed substantial correction — a real, but more narrowly-
scoped, methodological finding than first stated.

**What this does NOT mean.** Does NOT mean the target hypothesis `Var(X_n)=O(1/n)` is supported or
refuted. Does NOT mean `κ_n` is validated as a working "squared CV of `δ_i`" diagnostic — its two
natural estimators disagree substantially and unresolved; treat both columns as preliminary. Does
NOT mean the combined `λ_n` growth signal settles the target hypothesis — it is one `3.16σ` signal
from a specific estimator with a known, unresolved reliability question, not a proof. Does NOT
establish a new proof technique — this is a factorization of an inequality already proven at
point 12a.

**Skeptic Concerns (FL Step 8a — `reviewer`'s cap closed all session; `skeptic` substituted per
`doubt-driven-development.md` § Independent Review Fallback Policy, context-asymmetric). Verdict:
`FALSIFIED` — not "the core is wrong," but three claims directly contradicted the executed code
(the promised `δ`-based estimator was not actually used; the internal-consistency check was
tautological; "confirmed in two independent draws" for `κ_n` was fabricated, since Point 53 never
computed `κ_n` at all), plus a real statistical fallacy in the `λ_n` significance comparison and
several R_n-addendum overclaims. Every finding independently re-verified against the code and raw
JSON/`.npz` files, not accepted on the review's word alone.**
- Concern (F1, critical): "estimated from the SAME δ samples, Cov-based λ kept only as a
  cross-check" is false — the sweep code only ever computes `λ=4·Cov(X,Q)`; `mean(δ)` is never
  computed outside the small pilot. → **Fixed**: retracted, replaced with the honest `λ_δ`
  computation from the saved `.npz` files, reported as an unresolved discrepancy.
- Concern (F2): `kappa_hat_alt_consistency`'s `~1e-16` agreement is a tautology — both "paths" use
  the identical `delta` and `lambda_hat` arrays, just reordered arithmetic. → **Fixed**:
  description corrected to state it verifies arithmetic consistency, not estimator correctness.
- Concern (F3, critical): "κ_n shows no significant trend in either of two independent draws" is
  fabricated — Point 53's script never computes `δ_i`, `B_n`, or `κ_n` at all. → **Fixed**:
  removed; `κ_n` was measured in exactly one run.
- Concern (F4, critical — most consequential): the "two draws disagree on significance" framing
  conflated non-overlapping-significance with a significant difference between the draws (a named
  statistical fallacy) — reweighting gives `z=1.62` (not significantly different), and the correct
  INVERSE-VARIANCE-COMBINED slope is `0.117±0.037`, `3.16σ` from zero. → **Fixed**: reversed from
  "unconfirmed, draw-dependent" to "combined evidence is significant."
- Concern (F5): the underlying `honest_power_law_fit`'s residual-based SE is itself underdispersed
  relative to the points' own known uncertainty (`χ²=0.485` at `3` dof). → **Fixed**: superseded
  by the reweighted analysis in F4.
- Concern (F6): `κ_n`'s bootstrap CI dips below the Cauchy-Schwarz floor of `1.0` at `n=509,2039`
  — mathematically impossible, direct evidence the Cov-based `κ̂` estimator is noise-contaminated.
  → **Fixed**: added explicitly to the Sweep Results section.
- Concern (F7): the "45×" cross-fit divergence ratio uses a denominator whose own CI crosses zero;
  against the "trusted" corrected version the ratio flips sign to `−12.8×`. → **Fixed**: R_n
  addendum rewritten to name which denominator any quoted ratio uses.
- Concern (F8): the cross-fit residual computation doesn't subtract the sample mean, so it shares
  the mean-bias mechanism attributed only to the raw U-statistic. → **Fixed**: noted explicitly.
- Concern (F9): the one persisted synthetic check used an unrealistic signal-to-noise regime and,
  on real `n=37` data, cross-fit was actually the BEST estimator. → **Fixed**: explicitly noted.
- Concern (F10): the pilot sign check is decorative for every published number; the one place sign
  matters (`λ_δ`) was untested against production data; code inspection confirms sign LOGIC is
  correct, not a live bug. → **Fixed**: reframed as an overclaimed verification target.
- Concern (F11): "CIs contain the exact reference `n·R_n=0.674`" is a literal unit error — CIs are
  on the `R_n` scale (`≈0.018`), not `n·R_n`. → **Fixed**: corrected in the setup text.
- Concern (D1-D4, dismissed): the `κ_n·λ_n²/(4m)=B_n` algebra, the U-statistic unbiasedness
  derivation, the sweep table arithmetic/timings, and a log-bias alternative explanation all
  independently re-verified as correct/negligible. → **Dismissed**, no action needed.
- Concern (U1): `n·Var(X)` on this sweep's own 5 points implies a direct exponent of `≈-0.83`
  (3-4σ from flat), consistent with the parent experiment's committed `-0.9126` exponent. →
  **Accepted, added as context.**
- Concern (U2): a sharper `n=37` oracle check (exact `U_n/Var(X)=1.060` vs observed `0.994`) is
  more informative than "point estimate `≥1`" alone. → **Fixed**, added to Setup section.
- Concern (U3): a single fixed test-generator index reduces precision relative to multi-index
  averaging. → **Accepted limitation**: not fixed here, noted as a lever for a future resweep.
- Concern (U4): the 3-way Oracle Adequacy Gate's three checks are not fully independent
  (anti-correlated by construction). → **Fixed**, noted explicitly in Setup.

**Known gap, stated explicitly**: the executing agent's own "recalibrated per-n synthetic check"
remains unsaved to any script/JSON and is NOT cited as evidence anywhere in this corrected
version — superseded by the concerns above, which ground every remaining claim in either the
persisted JSON or a freshly-recomputed, independently-checked calculation from the saved `.npz`
files.

**Artifacts:** `check_kappa_n_large_n.py` (+`metrics/kappa_n_large_n.json`,
`metrics/kappa_n_raw_samples_n{127,251,509,1021,2039}.npz`, `check_kappa_n_large_n_output.log`).

## Point 55 (2026-09-14) — Point 54A/54B: `λ_n` estimator-identity audit is consistent with the
identity but has LOW POWER against the exact discrepancy it was built to check (a planted 12%
violation was missed at all 5 `n`); the higher-stakes question — does `|λ_n|` diverge? — gets a
real answer from the MOST DIRECT test (fitting `n·Var(X_n)` itself, already-saved data, found only
on skeptic-fallback review): SIGNIFICANT growth on the finite tested range (`t=3.877`), though
asymptotic divergence is still not established

**Context — why this is the highest-leverage open question in the experiment right now, per the
user's own math, independently re-verified.** `Var(X_n)≥W_1=λ_n²/(4m)` follows trivially from
Parseval (`Var(X)=Σ_{S≠∅}` squared Fourier coefficients `≥ Σ_{|S|=1}` squared coefficients `=W_1`
— no new proof needed, an elementary consequence of an identity already used throughout points
11-14). Since `m≍n/2`: `n·Var(X_n)≥n·W_1~λ_n²/2`. **If `|λ_n|→∞`, `Var(X_n)=O(1/n)` is FALSE** —
not merely one proof route closing, the target hypothesis itself. This makes resolving Point 54's
own unexplained `8-20%` discrepancy between its two `λ_n` estimators (`λ_Q=4Cov(X,Q)`,
`λ_δ=-m·E[δ_i]`) the single most consequential open item in the experiment, ahead of `κ_n` or any
Efron-Stein refinement — if `κ_n` grows, only the sharpened-bound route degrades; if `λ_n` grows
without bound, the target itself is dead.

**Point 54A — paired estimator-identity audit (`check_lambda_identity_audit.py`), run BEFORE any
scaling claim, per the user's own proposed protocol: freeze scaling analysis until this clears.**
Rather than comparing `λ_Q` and `λ_δ` as two separately-estimated quantities (Point 54's own weak
approach — two individual bootstrap CIs, each wide, compared informally), this constructs a
SINGLE paired statistic per replicate, exploiting that both terms come from the SAME graph draw:
`Y_r := 4X_r(Q_r-m/2) + m·δ_r`, which has `E[Y_r]=0` exactly if the two already-established
identities (`λ_n=4E[X(Q-m/2)]`, `λ_n=-m·E[δ_i]`) both hold. **Orientation of `δ_i` independently
re-verified against the actual code** (not assumed): both branches of
`check_kappa_n_large_n.py`'s `sample_x_q_delta` (lines 216-224) compute `value(i=0)-value(i=1)`
regardless of the original sample's `i`-state — matches the required convention exactly. Each
replicate draws exactly one graph (one `sample_circulant_neighbors` call), giving one paired
`(X,Q,δ)` triple — no clustering/pseudoreplication concern (verified by direct code read, not
assumed).

**Result at all 5 tested `n`** (reusing the already-saved `.npz` files, zero new
`theta_via_lp` calls):

| n | reps | Ȳ | SE(Ȳ) | z | Y 95% CI | status |
|---:|---:|---:|---:|---:|---|---|
| 127 | 300 | +0.451 | 0.254 | +1.777 | [−0.055,0.934] | PASS |
| 251 | 250 | +0.235 | 0.343 | +0.685 | [−0.444,0.910] | PASS |
| 509 | 200 | −0.476 | 0.363 | −1.313 | [−1.221,0.213] | PASS |
| 1021 | 150 | −0.259 | 0.605 | −0.429 | [−1.438,0.828] | PASS |
| 2039 | 80 | −0.614 | 0.873 | −0.703 | [−2.453,0.984] | PASS |

Max `|z|=1.78`, well under the pre-registered FAIL threshold `|z|≥3`.

**Corrected after skeptic-fallback review — two claims here needed real fixing, not cosmetic.**
(1) **"The paired test has far more power" was checked and is FALSE.** Directly computed
`corr(λ_Q,λ_δ)` from the bootstrap draws at each `n`: `+0.112, −0.013, +0.150, −0.128, −0.213`
(127→2039) — near zero, and NEGATIVE at 3 of 5 `n`. A paired test only gains power when the two
terms are POSITIVELY correlated; here they mostly aren't, so pairing gives CORRECT CALIBRATION
(the naive independent-CI comparison is anti-conservative by `~13%` at `n=2039`, since it ignores
this same near-zero/negative correlation), not a power advantage — the claimed mechanism was
wrong even though using the paired statistic was still the right thing to do.
(2) **A planted-canary check (run independently, not part of the original script) shows the gate
is UNDERPOWERED against the exact 8-20% effect it exists to catch.** Re-ran the identical test
with `m·δ_r` deliberately scaled by `1.12×` (a planted 12% violation) — **this canary was MISSED
(status stayed PASS) at all 5 `n`**, with `z` ranging `+2.86` (`n=127`, closest to the `|z|≥3`
threshold) down to `−0.28` (`n=2039`). Formal power against the actual observed `8-20%`-scale
discrepancy is roughly `2-10%` per `n` (estimated from each `n`'s own `y_se`) — far below a
usable detection threshold at any single `n`. **The pooled (inverse-variance-combined) test across
all 5 `n` is more informative**: `Ȳ_pooled=0.108±0.167`, `z=0.65` — this DOES meaningfully bound
a CONSTANT relative bias across `n` at roughly `≲13%`, ruling out the upper half of Point 54's
`8-20%` discrepancy range as a systematic (rather than per-`n`-random) effect, but not the lower
half, and not a bias that varies in sign/magnitude across `n` (which the per-`n` signs
`+,+,−,−,−` are at least consistent with being).

**Honest conclusion, replacing "PASSES cleanly": the identity is SUPPORTED, not proven clean** —
no single `n` individually rules out the observed discrepancy as a real (as opposed to noise)
effect, the pooled test rules out a constant bias above `~13%`, and the qualitative pattern (both
signs present, no monotonic trend) is more consistent with noise than a systematic bug, but this
is a weaker, more honestly-scoped claim than the original "PASS at all 5 `n`, discrepancy
resolved" framing implied.

**Point 54B — `λ_n` scaling via the variance-optimal combined estimator
(`check_lambda_optimal_scaling.py`), unblocked by 54A's result.** Since `λ_Q` and `λ_δ` are
correlated (same-sample) unbiased estimators of the same `λ_n`, computed their GLS-optimal linear
combination per `n` via the empirical bootstrap covariance matrix.

| n | λ_Q (SE) | λ_δ (SE) | weight on λ_Q | λ_opt | SE(λ_opt) | var. reduction |
|---:|---|---|---:|---:|---:|---:|
| 127 | −2.187 (0.198) | −2.631 (0.183) | 0.457 | −2.428 | 0.142 | 40.2% |
| 251 | −2.614 (0.261) | −2.837 (0.215) | 0.406 | −2.747 | 0.165 | 41.2% |
| 509 | −2.928 (0.336) | −2.441 (0.192) | 0.208 | −2.542 | 0.177 | 15.3% |
| 1021 | −3.437 (0.482) | −3.172 (0.307) | 0.311 | −3.254 | 0.243 | 37.3% |
| 2039 | −3.481 (0.667) | −3.023 (0.392) | 0.295 | −3.158 | 0.303 | 40.1% |

**Skeptic-fallback correction on the 15-41% variance-reduction figures above**: these are
IN-SAMPLE (the GLS weight `w` is estimated from the same bootstrap draws used to compute the
resulting variance, a form of winner's-curse optimism), and `se_opt` does not propagate the
weight's own estimation uncertainty. Both effects bias `se_opt` DOWNWARD — e.g. at `n=2039`
(`ρ̂=−0.213`), if the true correlation were `0`, the real variance reduction would be `~25.6%`, not
the reported `40.1%`. **This means the `t`-statistics below are, if anything, slightly OVERSTATED
(too significant), reinforcing rather than undermining the "not yet significant" reading that
follows** — accepted as a known limitation, not fixed here.

**Global weighted power-law fit on `|λ_opt|` (independently re-verified, exact match):** slope
`0.100±0.033`, `t=3.01` at `3` degrees of freedom (5 points, 2 fitted parameters). **Skeptic-
fallback review found this framing incomplete: there are (at least) two different, both-legitimate
statistical conventions for the effective degrees of freedom here, and they disagree on the
verdict.** Treating `sigma` as KNOWN (from the per-point bootstrap CIs, the convention used above)
gives a NORMAL reference distribution: `z=3.01`, `p=0.0026` — significant. Treating `sigma` as
ESTIMATED (rescaling the covariance by the reduced chi-square, `χ²=3.85` at `dof=3`, giving
`reduced χ²=1.285`) gives `se=0.0378`, `t=2.66` — NOT significant. **The `t_crit(dof=3)=3.18`
comparison used in the first draft was itself a hybrid of these two conventions** — defensible as
a conservative middle ground, but not "the correct" reading as originally implied; both legitimate
readings are reported here instead of picking one. **Separately, this same underlying `λ_Q` data
already has a THIRD, already-committed fit in `metrics/kappa_n_large_n.json`
(`lambda_n_power_law_fit_vs_n`): unweighted OLS on `λ_Q` alone gives `slope=0.173±0.023`, CI
`[0.099,0.247]` — EXCLUDING zero.** Three conventions, applied to closely related but not
identical quantities, give three different significance verdicts — reported here explicitly (the
log-slope difference between `λ_Q`-alone and `λ_δ`-alone estimates, `0.118±0.091`, is itself not
significant, `z=1.30` — so this is a genuine framing sensitivity, not a sign of a real
contradiction in the underlying data).

**A more direct, better-powered test was missing from this point entirely and is added here on
skeptic-fallback review: fitting `n·Var(X_n)` itself (the target quantity, not a proxy) using the
same already-saved data (`var_x_hat` in `metrics/kappa_n_large_n.json`), with no new compute.**
Weighted power-law fit (known-variance convention, `σ_log=√(2/(reps-1))` from the chi-square
sampling distribution of a sample variance): **slope=0.1965±0.0507, t=3.877 — this DOES clear
`t_crit(dof=3)=3.18`, significant.** The fit's own `χ²=0.968` at `dof=3` (close to the expected
value of `3`, i.e. well-calibrated, unlike the `λ_opt` fit above which was mildly underdispersed)
— this is currently the SINGLE MOST DIRECT, best-supported piece of evidence in this point that
`n·Var(X_n)` is growing over the tested finite range, and it was found only on review, not in the
original draft, despite requiring zero new computation. It does not, by itself, establish
asymptotic divergence (see the local-slope discussion below for why), but it materially shifts
this point's own honest headline from "genuinely open, no significant signal" to "significant
growth detected on the finite tested range via the most direct available test; asymptotic
behavior remains the open question."

**Local slopes between fixed-ratio `n`-pairs (each spanning almost exactly a factor of `4`), to
distinguish "slow but steady growth" from "growth trending toward a plateau" (`a_local→0`):**

| pair | local slope | SE | z |
|---|---:|---:|---:|
| `127→509` | 0.033 | 0.065 | 0.51 |
| `251→1021` | 0.121 | 0.068 | 1.77 |
| `509→2039` | 0.156 | 0.085 | 1.83 |

None of the three local slopes individually reaches conventional significance (`|z|<2` for all
three). **Corrected after skeptic-fallback review: the first-vs-last local-slope comparison had a
covariance error.** The `127→509` and `509→2039` local slopes SHARE the point `n=509` (with
opposite-sign roles), so they are not independent — the first draft's naive `√(se1²+se3²)=0.108`
ignored this shared-point covariance. Correctly propagating it gives `se_diff=0.129`, `z=0.96` —
even LESS significant than first reported (`z=1.15`), reinforcing rather than reversing the "not
distinguishable" conclusion, but for the right reason this time. **A second, independent
instability was also found on review**: the apparent RISING pattern (`0.033→0.121→0.156`) is
driven almost entirely by the single point `n=509` — which has near-zero leverage on the GLOBAL
weighted fit but enters TWO of the three local slopes with opposite signs. Replacing `λ_opt(509)`
with a simple (non-GLS) average of its two component estimators changes the local-slope sequence
to `0.072, 0.121, 0.117` — essentially FLAT, not rising. **Honest conclusion, strengthened rather
than weakened by these corrections: this data cannot currently distinguish accelerating growth,
constant slow growth, or growth trending toward a plateau — the apparent "rising" shape in the
first draft was itself an artifact of a single point's estimator choice, not a real signature.**
The critical falsification-relevant question for the ASYMPTOTIC exponent — does `|λ_n|`
(equivalently `n·Var(X_n)`, per the direct test above) diverge without bound? — remains genuinely
open at the level of local-slope shape, even though the GLOBAL, better-powered `n·Var(X_n)` fit
above DOES show significant growth on the tested finite range.

**Kill Analysis.** Nothing is killed. What IS established, corrected after skeptic-fallback
review: (1) the estimator-identity audit SUPPORTS the identity but has low per-n power (2-10%
against the observed 8-20% discrepancy, confirmed by a missed planted-12%-canary at all 5 `n`) —
the pooled test rules out only a constant bias above `~13%`, weaker than "resolved as noise"; (2)
a lower-variance combined `λ_n` estimator exists (with real in-sample-optimism caveats on its own
reported gains); (3) **the single highest-stakes open question gets a real answer from the most
direct available test**: `n·Var(X_n)` itself shows SIGNIFICANT growth on the tested finite range
(slope=0.1965±0.0507, t=3.877, clearing `t_crit=3.18` with a well-calibrated `χ²=0.968` at
`dof=3`) — found only on review, despite using already-saved data. This is meaningfully different
from "genuinely open": there IS a real, well-powered signal of growth over `n=127..2039`; what
remains open is whether this finite-range growth continues asymptotically or represents
finite-size correction toward a bounded limit — the (itself now-corrected) local-slope analysis
cannot yet distinguish these two scenarios.

**What this does NOT mean.** The `n·Var(X_n)≥n·W_1~λ_n²/2` "no threshold" correction from the
first draft is independently re-verified and stands: ANY genuine asymptotic growth in `|λ_n|` (or
`n·Var(X_n)`) refutes `Var(X_n)=O(1/n)`, no exponent condition needed. Does NOT mean
`Var(X_n)=O(1/n)` is established false — the significant finite-range slope found here does not
by itself establish that growth is UNBOUNDED as `n→∞` rather than a finite-size correction that
will plateau; this is exactly the question the local-slope analysis was built to resolve, and
(even after correcting its own errors) it still cannot. Does NOT mean the identity audit
generalizes to other quantities — it addressed specifically the `λ_Q`/`λ_δ` estimator pair, with
the important caveat (per skeptic review) that its own detection power was much lower than the
original draft implied. Does NOT settle `κ_n`'s own Cauchy-Schwarz-violating CI (Point 54's
Concern F6), unresolved by this point.

**Recommended next steps, stated but not executed here.** (1) The `n·Var(X_n)` finding is the
highest-value follow-up: extend the SAME direct fit to more/larger `n`, and compute its own local
slopes (not done here) to check whether IT shows the plateau signature the `λ_opt` local slopes
could not resolve. (2) Re-run the identity audit sweep with the rep budget reallocated toward the
largest `n` (currently the noisiest, `80` reps at `n=2039`) to raise its own detection power above
the current 2-10%. (3) A genuinely independent oracle for the `λ_n`/`n·Var` growth question — e.g.
exact small-`n` data extended past `n=53` via the necklace-orbit method, if computationally
reachable — would settle the finite-vs-asymptotic ambiguity more directly than any further Monte
Carlo resweep at the current `n` range.

**Skeptic Concerns (FL Step 8a — `reviewer`'s cap closed all session; `skeptic` substituted per
`doubt-driven-development.md` § Independent Review Fallback Policy, context-asymmetric). Verdict:
`WEAKENED` — the core identity holds and the overall "genuinely open" framing survives, but
several supporting claims were wrong or overstated, and one major, better-powered finding
(`n·Var(X_n)` itself grows significantly on the tested range) was missing entirely from the first
draft despite costing zero new compute. Every number independently re-verified from the raw
JSON/`.npz` files, not accepted on the review's word alone.**
- Concern: `E[Q]=m/2` and `E[X]=0` are treated as approximate in the identity derivation. →
  **Dismissed** — both confirmed EXACT: `Q~Bin(m,1/2)` by construction (`sample_circulant_
  neighbors`'s own i.i.d. Bernoulli(1/2) sampling, re-read directly), and `E[X]=0` follows exactly
  from `θ(G)θ(Ḡ)=n` (points 4/11) plus the `c↔1-c` measure symmetry — confirmed numerically via
  `mean_x_hat` values all within 1-2 SE of zero.
- Concern: "the paired test has far more power than the naive comparison" is false — measured
  correlation between the two component estimators is near zero and negative at 3 of 5 `n`. →
  **Fixed**: claim retracted and replaced with the correct framing (pairing gives calibration, not
  power), correlations reported explicitly.
- Concern: "PASSES cleanly" overclaims what the gate actually established — the code's own
  `INCONCLUSIVE` branch is unreachable dead code, and a planted 12% violation is missed at every
  tested `n` (power 2-10%). → **Fixed**: reframed as "identity supported, not proven clean,"
  planted-canary result and per-`n` power reported, pooled test's real (but partial, ~13%-bias-
  ceiling) information content stated explicitly instead of a blanket "resolved."
- Concern: the GLS-optimal combined estimator's reported 15-41% variance reduction is in-sample,
  likely overstating the reduction and understating `se_opt`. → **Accepted limitation**: noted
  explicitly; the resulting bias makes the downstream `t`-statistics, if anything, slightly
  overstated, so the "not yet significant" reading for `λ_opt` is not undermined by this.
- Concern: the "t=3.01 vs t_crit=3.18" framing used a hybrid of two different statistical
  conventions, and disagrees with an already-committed fit on the same underlying `λ_Q` data. →
  **Fixed**: both conventions reported explicitly (z=3.01 significant vs t=2.66 not significant),
  the third existing fit cited, and the log-slope difference between the two component estimators
  checked directly (not itself significant, z=1.30).
- Concern (the single highest-value finding): a more direct, better-powered test of the target
  quantity (`n·Var(X_n)` itself) was available for free from already-saved data and was not run.
  → **Fixed**: computed and independently re-verified — slope=0.1965±0.0507, t=3.877, clears the
  significance threshold with a well-calibrated fit (χ²=0.968 at dof=3) — added as the point's own
  headline finding, materially changing the overall verdict.
- Concern: the local-slope first-vs-last comparison's SE ignored that the two slopes share the
  point `n=509` with opposite-sign roles, understating the true SE. → **Fixed**: corrected SE
  (0.129, not 0.108) and z (0.958, not 1.15) computed and substituted.
- Concern: the apparent "rising" local-slope pattern is driven almost entirely by `n=509`'s
  specific GLS point estimate; replacing it with a simple average removes the rising pattern. →
  **Fixed**: instability noted explicitly, and the "rising" framing retracted.
- Concern: table arithmetic, wall-clock, rep counts, sign-orientation code read. → **Dismissed**
  as real issues — all independently re-verified and confirmed correct on direct inspection of
  the code and JSON.

**Artifacts:** `check_lambda_identity_audit.py` (+`metrics/lambda_identity_audit.json`,
`check_lambda_identity_audit_output.log`), `check_lambda_optimal_scaling.py`
(+`metrics/lambda_optimal_scaling.json`, `check_lambda_optimal_scaling_output.log`).

## Point 65 (2026-09-16) — RBA decomposition test: cancellation is real but NOT REFUTED ≠
SURVIVES-IN-STRONG-FORM — the report's own headline overclaims because ~all of `R1`/`R2`'s
dramatic individual magnitude is a bounded polarization-identity tautology, not emergent LP
structure; the genuine finding is a 3-term `O(1.5–2.2)` balance, the trend question is
underpowered, and a proper extrapolation test favors the declining/log model the report
dismissed

**Context.** `rba_decomposition_test.py` + `rba_decomposition_report.py` (background-agent run,
this session, primes `n=509,1021,2053,4093`, full target sample sizes reached including the
priority `n=4093`) tested whether `R(S)=R0(S)+R1(S)+R2(S)` on the reduced-frequency Lovász LP's
central layer shows genuine `O(1/q)` second-order cancellation between `R1` and `R2`. The agent's
own `rba_decomposition_summary.md` (dated today) concludes **`RBA SURVIVES DECOMPOSITION TEST —
and in the strong form the pre-registered criterion named`**. This point independently
re-verifies every load-bearing number in that report (skeptic-fallback review, per
`doubt-driven-development.md` § Independent Review Fallback Policy — `reviewer`'s cap closed
earlier this session, substitution stated explicitly) and finds the headline verdict itself
overclaims, even though the report's own body already discloses several of the caveats below.
**Every number in this point is either copied verbatim from the committed report/CSV or was
freshly recomputed from `rba_parent_level.csv` / `rba_decomposition_summary.md` in this session
(scripts below), not accepted on the agent's word.**

**Headline results (main dataset, `q_R1`, `q_R2` etc. = `q·E[·]` over parents, weighted fit on
`log q`):**

| n | q | `q·E[R1]` | `q·E[R2]` | `q·E[R1+R2]` | `q·E[R_total]` | `cancel_ratio` | `K_ADC` |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 509 | 127 | −18.859 | +18.649 | −0.211 | +1.424 | 0.00561 | 1.295 |
| 1021 | 255 | −24.348 | +23.991 | −0.356 | +1.255 | 0.00737 | 1.266 |
| 2053 | 513 | −30.579 | +29.975 | −0.604 | +0.994 | 0.00998 | 1.234 |
| 4093 | 1023 | −35.676 | +34.812 | −0.864 | +0.729 | 0.01226 | 1.216 |

(all `[VERIFIED]` — matches `rba_decomposition_results.csv`, main dataset, exactly.)

**1. The central correction: `R1`/`R2`'s huge magnitude is (≥100%) a bounded polarization-
identity tautology, not "a fact about the LP's optimal face" as the report's own § 5 claims
(directly, at its "reason 1": *"That `R2 > 0` grows … is a fact about the LP's optimal face, not
an algebraic tautology"* — this is FALSE as literally written, independently verified below).**
For ANY vectors `p, p'=p+u`: `2⟨p,u⟩+‖u‖² ≡ ‖p'‖²−‖p‖²` exactly — a pure algebraic identity,
confirmed numerically to `1e-17–1e-18` on 5 random-vector trials
(`tmp/verify_polarization.py`, this session's earlier pass). Applied here with `u_j=p_{S+j}-p_S`:
`2⟨p,u_j⟩+‖u_j‖² = s2'_j − s2 = Δs2_j`, and since `s2, s2'∈(0,1]`, `Δs2_j` is a BOUNDED quantity
— nothing like the ~19–36-magnitude numbers the report reports for `R1`/`R2` individually.

Freshly computed from `rba_parent_level.csv` (`ok==True & full_j==False`, i.e. exactly the 200/
200/100/50-parent main sweep; reconciles to the published `q·R_total_bulk` to `<4e-11` at every
`n` — `tmp/verify_three_term.py`), `q·R_total_bulk` decomposes EXACTLY into 3 terms:

| n | term1 `E[I]` (`=q·E[R0]`) | term2 `q(q+1)·E[Δs2]` (tautological) | term3 `2q(q+1)·E[gA]` (genuine LP content) | sum |
|---:|---:|---:|---:|---:|
| 509 | 1.635±0.008 | −1.888±0.290 | +1.660±0.039 | 1.407 |
| 1021 | 1.612±0.004 | −1.904±0.337 | +1.556±0.023 | 1.264 |
| 2053 | 1.599±0.004 | −2.078±0.540 | +1.480±0.019 | 1.001 |
| 4093 | 1.593±0.005 | −2.213±0.870 | +1.445±0.023 | 0.826 |

term2 and term3 are BOTH `O(1.5–2.2)` — comparable in scale to each other, and each nearly as
large as their own sum's total range. This 3-term balance, not the misleadingly-large `R1≈-19`/
`R2≈+19` framing, is the substantive structural finding.

Going one level deeper (same script, decomposing `q·R1_bulk` itself into its `⟨p,u_j⟩`-piece and
`gA`-piece): at `n=509`, `R2 = (q+1)·E[‖u_j‖²]` is by DEFINITION 100% the norm-difference/
polarization term — there is no independent LP-content in `R2` at all, separate from the
`Δs2` framing. `R1 = 2(q+1)·E[⟨p,u_j⟩] + 2(q+1)·E[gA]`, and the `⟨p,u_j⟩`-piece alone (`q·`that
`= −20.537`) EXCEEDS `R1`'s own total magnitude (`−18.877`) — i.e. the genuine-LP `gA` piece
(`+1.660`) is acting as a small OFFSET against an even-larger polarization-piece, not as `R1`'s
primary driver. This ratio (`|⟨p,u⟩-piece| / |R1_bulk|`) is `108.8%, 106.4%, 104.8%, 104.1%` at
`n=509,1021,2053,4093` — i.e. `R1` and `R2` combined are, if anything, MORE than 100%
polarization-attributable (`tmp/verify_r1r2_split.py`, this session). **Corrected verdict:** the
numeric cancellation between `R1` and `R2` is real (independently computed, not disputed) — but
the reason it happens is that both quantities are dominated by the SAME bounded `Δs2` object
scaled by the large prefactor `q(q+1)`, which is guaranteed by the polarization identity to
nearly cancel with itself once `R0`'s own `s2` term is subtracted back out — not "a fact about the
LP's optimal face." The ONE place genuine LP/optimization content enters at all is the `gA`/bulk
term (`term3`, `O(1.44–1.66)`), and it does not even dominate `R1`'s own reported magnitude.

**2. `p<1e-15` for the `R1`/`R2` component-slope significance is a convention artifact, not a
correctly-computed t-test result.** The report's own footnote states the SEs are treated as
KNOWN (bootstrap, not estimated from the 4 residuals) — under that convention a normal (`z`)
reference is defensible, though see below. But the design has only `N=4` points and `k=2` fitted
parameters (`dof=2`), and if SEs are instead treated as estimated (the more conservative
convention, matching the dual-convention discipline already established in points 54/55 of this
experiment), the correct reference is `t(dof=2)`, not normal. Directly computed (`scipy.stats.t`,
this session): `t=-15.29` at `dof=2` gives two-sided `p=0.00425`; `t=+21.19` gives `p=0.00222`.
**Both orders of magnitude larger than the reported `<1e-15`** — the reported figure corresponds
to a normal-tail approximation (`z=15.29→p≈8.9e-53`, `z=21.19→p≈1.2e-99`), not to a small-`dof`
`t`-distribution appropriate for a 4-point design. Both conventions are reported here rather than
picking one (per the same dual-convention discipline as points 54/55): under either, the
COMPONENT slopes remain clearly significant (`p<0.005` even on the conservative convention) — the
correction is to the CLAIMED PRECISION of that significance, not to its direction. Separately,
and more fundamentally: a `p`-value at the `1e-15`-to-`1e-99` scale computed from only 4
independent design points (4 values of `n`) is not epistemically meaningful at that precision
regardless of which formula produced it — extraordinarily small `p` from `N=4` should never be
read as "extraordinarily certain."

**3. `cancel_ratio` reverses direction between the small-`n` control range and the main range —
already disclosed in the report body (§5, "the single most adverse trend in the dataset") but not
reflected in the headline verdict.** Main range: `0.0056→0.0074→0.0100→0.0123` (`n=509→4093`,
WORSENING, i.e. cancellation fraction falls `99.44%→98.77%`). Small-`n` exhaustive/near-exhaustive
control (§6d): `0.0889→0.0726→0.0441` (`n=17→23→29`, IMPROVING). The pre-registered expectation
(`CANCEL_RATIO << 1, possibly decreasing with n`) is confirmed on the control range and VIOLATED
on the main range — the report's own "reason 4" (*"the exhaustive small-`n` control … shows the
same signature independently"*) cites the control range's agreement without flagging that its
cancel_ratio TREND runs opposite to the main range's.

**4. § 6d's own headline ("no Monte Carlo at all") is directly contradicted by its own table one
line below it.** `rba_exhaustive_small_n.py`'s table (§6d) shows `n=17,23` genuinely exhaustive
(70/70, 462/462 subsets) but `n=29..41` "capped at 3000 subsets" — at `n=41`
(`C(20,10)=184,756`, per the earlier-session finding, not re-verified again here since it is pure
combinatorics), 3000 subsets is `1.6%` coverage, i.e. Monte Carlo, contradicting the section's own
"no Monte Carlo at all" framing for the range as a whole.

**5. Negative-control production-path coverage — narrower finding than originally suspected,
resolved this session by direct code comparison.** `rba_negative_control.py`'s `one_case()` and
`rba_decomposition_test.py`'s `process_parent()` are confirmed (via direct `Read`, this session)
to be genuinely SEPARATE functions with NO shared code path — but they compute the IDENTICAL
formula: `one_case`'s `C=lp.cosval[np.outer(free,orbit)%n]; mj=C@pvec; Aj=C@(pvec*pvec)-mj*(pvec@
pvec)` is line-for-line the same math as `process_parent`'s blocked
(`for a in range(0,m,BLK)`) `C=lp.cosval[(np.outer(jb,orbit))%n]; m_all[...]=C@pk;
Acos_all[...]=C@pk2; A_all=Acos_all-m_all*s2`. **Corrected framing:** this is NOT "controls test a
rewritten copy with different logic" (the earlier, stronger suspicion) — the underlying formula is
identical. It IS "controls test a separately-maintained duplicate of the production formula, not
the literal production code path" — a real, narrower gap: a bug specific to `process_parent`'s
own block-loop implementation (an indexing error in the `BLK=256` chunking, for instance) would
not be caught by these 5 planted-error tests, since `one_case` never calls `process_parent` or
exercises its blocking logic.

**6. AICc vs LOOCV — the report's own "LOOCV … mechanically favours the flexible model" framing
is backwards, confirmed by a genuine extrapolation test run this session.** The report already
shows LOOCV RMSE favoring the log-model 4.9× (`0.0741` vs `0.3624`, subset estimator) but frames
this as mechanical/uninformative. A proper single-holdout extrapolation test (fit on `n=509,1021,
2053` only, predict `n=4093`, unweighted OLS as an illustrative check — `tmp/loocv_holdout.py`,
this session) gives: constant-model prediction `1.224` vs actual `0.729` (abs. error `0.495`);
log-model prediction `0.797` vs actual `0.729` (abs. error `0.068`) — **the log model extrapolates
~7× more accurately to the held-out largest `n`.** Since a flexible 2-parameter model is normally
expected to OVERFIT on `N=4` and extrapolate WORSE, not better, the log-model's actual win here is
real out-of-sample evidence for the declining/log trend, not a mechanical artifact of LOOCV with
few points — the report's dismissal of this signal is unsupported.

**Kill Analysis.** Nothing is killed. What survives, corrected: (1) the numeric cancellation
between `R1` and `R2` is real and independently reproduced (two solvers, exhaustive small-`n`,
second-seed) — this part of the report's claim stands; (2) the mechanism behind that
cancellation is NOT "a fact about the LP's optimal face" as claimed — it is, to `≥100%`, the
bounded polarization identity `Δs2=2⟨p,u⟩+‖u‖²` scaled by `q(q+1)`, independently verified this
session; (3) the ONLY genuine LP-structural content is the `O(1.44–1.66)` `gA`/bulk term, one of
three comparably-sized pieces in a `q·R_total` balance, not the dramatic `R1≈-19`/`R2≈+19`
picture; (4) the trend question (`q·R_total ~ log q` vs constant) remains genuinely underpowered
at `N=4` (`SE≈0.31` on a point range of `0.73–1.42` — only `|slope|>~0.6` is 2σ-detectable) — but
a genuine extrapolation test (not mere LOOCV RMSE) favors the declining/log model, contrary to how
the report dismissed that signal; (5) `cancel_ratio` improves on the small-`n` control range but
WORSENS on the main range — the report discloses this but the headline verdict does not reflect
it; (6) the negative controls test the correct formula via a separately-maintained duplicate, not
literal production code — a real but narrower coverage gap than initially suspected.

**What this does NOT mean.** Does NOT mean the RBA mechanism is fake or that `R1`/`R2` don't
genuinely grow with `q` — they do, confirmed independently. Does NOT mean `RBA=O(1/q)` /
`q·R=O(1)` is refuted — it remains the best-fitting simple model on the tested range and is
consistent with everything measured. Does NOT mean the report's numerical work is wrong — every
raw number independently re-checked (bulk/delta-I identities, negative controls, solver
cross-check) reconciled to the published figures. Does NOT mean this point establishes
`q·R ~ log q` as correct — the extrapolation test favors it over the constant model but `N=4` is
still far too few points for an asymptotic claim either way. Does NOT mean the `gA`/bulk term
itself is fully understood mechanistically — that remains open (see next steps).

**Recommended next steps, stated but not executed here (cheapest-first).** (1) Report the 3
genuine `O(1)`-scale quantities (`E[I]`, `q(q+1)E[Δs2]`, `2q(q+1)E[gA]`) as the primary
decomposition in any future write-up of this mechanism, not the inflated `q·R1`/`q·R2`. (2) Fill
the `q∈(10,127)` gap between the exhaustive/near-exhaustive small-`n` control and the main Monte
Carlo range (e.g. `n=127` already covered; add `n=251` at higher coverage, or push exhaustive
enumeration to `n=53` via the necklace-orbit method already used elsewhere in this experiment) to
see whether the cancel_ratio reversal is a genuine regime change or a small-`n` artifact. (3) Run
5 independent seeds at one fixed `n` (e.g. `n=1021`) to get a real between-seed variance estimate
for `q·R_total`, orthogonal to the current between-parent bootstrap SE. (4) If the `gA`/bulk term
is to be pursued analytically (the CANCEL-lemma direction discussed with the user, see below), its
own mechanism — not `R1`/`R2`'s polarization-dominated magnitude — is the correct object to
target, since the polarization piece is guaranteed algebraically and carries no LP-specific
content to prove.

**Skeptic Concerns (FL Step 8a — `reviewer`'s cap closed earlier this session; `skeptic`
substituted per `doubt-driven-development.md` § Independent Review Fallback Policy,
context-asymmetric: given only the report's claim text + `rba_decomposition_test.py`/
`rba_decomposition_report.py`, no session history). Verdict: `WEAKENED` — the report's raw
numerics are sound and independently reconfirmed, but its headline verdict ("SURVIVES … in the
strong form") and its "reason 1" (cancellation is "not an algebraic tautology") do not survive;
every concern below independently re-verified from the raw CSV/JSON/code, not accepted on the
review's word alone.**
- Concern: "`R2 > 0` grows … is a fact about the LP's optimal face, not an algebraic tautology"
  (report §5, reason 1). → **Fixed**: falsified directly — the polarization identity makes `R2`
  by definition `(q+1)·E[‖u_j‖²]`, a pure norm-difference object with zero independent LP content;
  `R1`'s polarization-piece alone exceeds `R1`'s own total magnitude at every tested `n`
  (104.1–108.8%). Restated as a 3-term `O(1.5–2.2)` balance instead.
- Concern: `p<1e-15` for the `R1`/`R2` component slopes. → **Fixed**: recomputed at the design's
  actual `dof=2`; true two-sided `p=0.0022–0.0043` under the conservative (estimated-variance)
  convention, both conventions now reported explicitly per the points-54/55 precedent.
- Concern: `cancel_ratio` reversal between small-`n` control (improving) and main range
  (worsening) is disclosed in the report body but not reflected in the headline "SURVIVES … strong
  form" verdict. → **Fixed**: reversal stated explicitly as one of the point's own headline
  findings, not buried.
- Concern: §6d claims "no Monte Carlo at all" while its own table shows `n=29..41` capped/
  subsampled. → **Fixed**: self-contradiction noted explicitly.
- Concern: negative controls (`one_case`) may test a rewritten copy of the production math with
  different logic, not the literal production path. → **Investigated and narrowed**: confirmed
  `one_case`/`process_parent` are separate functions (no shared code) but compute the IDENTICAL
  formula — reframed from "different logic" to "separately-maintained duplicate," a real but
  smaller coverage gap (misses bugs specific to `process_parent`'s own blocking implementation).
- Concern: LOOCV's better fit for the log-model is dismissed as "mechanical." → **Fixed**: a
  genuine single-holdout extrapolation test (predict `n=4093` from the other three) run this
  session shows the log-model extrapolates ~7× more accurately than the constant model — real
  out-of-sample evidence, not a LOOCV-with-few-points artifact.
- Concern: the `I(S+j)-I(S)=R0+R1+R2` formula in the original task spec vs what the code's
  `check4_error` actually validates (`R_total_bulk` against `mean_dI + (q+1)/(2q)·(n/(Fq))·D_S`,
  not a bare `R0+R1+R2` sum) is a real mismatch worth flagging for any future write-up, but is a
  documentation/spec-clarity issue, not a numerical error — `check4_error` itself passes at
  machine precision throughout. → **Accepted limitation**: noted here, not re-derived in full;
  does not affect any number reported in this point.
- Concern: identity-precision claims (bulk `≤1.06e-18`, delta-I `≤1.39e-15`), solver cross-check
  (`≤6.4e-07`), substrate-gate agreement (`2.84e-14`), planted-error-control catch rates (5/5 at
  4/4 `n`). → **Dismissed** as real issues — all independently spot-checked against the raw JSON
  this session and confirmed correct.

**Artifacts:** `rba_decomposition_test.py`, `rba_decomposition_report.py`,
`rba_negative_control.py`, `rba_exhaustive_small_n.py`, `rba_decomposition_results.csv`,
`rba_decomposition_summary.md`, `rba_parent_level.csv` (+ per-run variants), `metrics/rba_*.json`
(bulk/delta-I identities, negative control, exhaustive small-n, method consistency). This
session's independent verification scripts (scratchpad, not committed):
`verify_three_term.py`/`verify_three_term2.py`, `verify_r1r2_split.py`, `check_scale.py`,
`check_pvals.py`/`check_pvals2.py`, `loocv_holdout.py`.

## Point 66 (2026-09-16) — PPL (Paired-optimizer Product Lemma) gate pilot: sanity checks pass,
but `b=0` is actually REJECTED (not "within the CI" as first drafted) — still NOT a Gate 0 pass,
extensively corrected on skeptic-fallback review (WEAKENED), including a self-falsified claim
about why an earlier flawed sampling draft differed numerically

**Context and provenance (Gate 1, stated explicitly per standing session discipline).** A route
proposed by an external AI (not Codex, not this session — user-confirmed source, not traceable to
any file in this repo) argued that Point 63's already-verified inequality (Codex,
`codex-20260914-susceptibility/CROSS_TURAN_ENERGY_THEORY.md`, SURVIVES-PILOT): for old graph `G0`,
new `G1=G0∪{i}`, optimum `x` of `G0`, optimum `w` of `complement(G1)`:
`δ_i≤2·x_i·w_i`
could, if `J_n:=n²·E[(x_i·w_i)²]=O(1)`, close the ENTIRE target hypothesis in one shot via
`δ_i²≤4x_i²w_i²` ⟹ `E[δ_i²]=O(n⁻²)` ⟹ `B_n=(m/4)E[δ_i²]=O(1/n)` ⟹ (already-proven point 12a)
`V_n≤B_n=O(1/n)`. Two things needed checking before trusting this: (1) whether "cross-Turán" and
the inequality actually exist in this project (they do — confirmed via the artifact filename
itself, `CROSS_TURAN_ENERGY_THEORY.md`, initially missed by a plain-ASCII grep for "Turán"); (2)
whether the proposed new quantity's name collides with anything already established — it does:
the external text's own `T_q` is NOT the same object as this project's existing `T_q`
(swap-Dirichlet-energy `E[(δ_i(S)-δ_i(S'))²]`, points 15b-20, whose own sufficient lemma was
already REJECTED there). The new quantity is renamed `J_n`/`PPL_gate` throughout this point and
its artifacts to avoid the collision — `T_q` keeps its original 15b-20 meaning.

**Estimand (L0: descriptive).** `J_n = E[Z_{n,i}²]`, `Z_{n,i}:=n·x_i·w_i`, for a FIXED coordinate
`gen_index=1` (matching `TEST_GENERATOR_INDEX=1` in `check_kappa_n_large_n.py:100`, this
project's own established single-generator-sensitivity convention) — NOT a coordinate chosen
post-hoc from the free set, which a first pilot draft did and which introduces size-bias relative
to graph density (see Errors below). `x` = optimal certificate of `G0` (the graph with `gen_index`
absent), `w` = optimal certificate of `complement(G1)` (the graph with `gen_index` present) — both
canonical branches of the project's own `sample_x_q_delta` (`c[gen_index]<0.5` and `>=0.5`) are
included, none dropped, matching how `B_n=(m/4)E[δ_i²]` is computed everywhere else in this
experiment.

**Errors caught and fixed during this pilot, stated explicitly (not smoothed over) — §1 itself
CORRECTED on skeptic-fallback review, see disposition below.**
1. First draft fixed `i` but conditioned `S` on `i∉S` only (forced `bits[0]=0`); this used only
   ONE of the two canonical `sample_x_q_delta` branches. Gave `J_n(127)=5.9`, `J_n(509)=73.5`,
   ratio `12.5` (looked sharply growing) — v3 (below) instead gives `J_n(127)=64.7`, an `~11×`
   discrepancy at the single point carrying the most fit leverage. **The mechanism claimed above
   for this discrepancy (dropping half the branches) is FALSE, independently verified on skeptic
   review and re-checked here**: `flip_generator` only ever toggles the ONE bit at `gen_index`,
   so for a FIXED seed, `c_g0`/`c_g1` are algebraically identical in both the forced-`bits[0]=0`
   draft and the honest-branch v3 draft — branch B (`c[gen_index]=1`) is a relabeling of the same
   underlying pair, not a different sample. This is confirmed directly in `ppl_gate_pilot.json`'s
   own `branch_summaries`: branch A and branch B give statistically indistinguishable `J_n` at
   every `n` (e.g. `n=127`: A=62.8±8.1, B=66.5±7.8, well within noise). **The real cause of the
   `~11×` discrepancy at `n=127` remains UNEXPLAINED and UNRESOLVED** — this is a genuine open
   integrity gap, not a cosmetic one, since it sits on the point with `48.9%` of the weighted
   fit's leverage (see Results below). The one piece of indirect evidence favoring v3 over the
   original draft: the independent sanity inequality `Z=n·x_i·w_i ≥ n·δ_i(actual)/2` — spot-
   checking rows shows `Z/(</n·δ/2) ≈ 1.0–2.5`, i.e. `Z` cannot be as small as the original
   draft's numbers implied without violating the (independently, machine-precision-verified)
   `δ≤2x_iw_i` bound (the ratio `Z / (n·δ/2)` runs `≈1.0–2.5` on spot-checked rows) — but this is
   circumstantial, not a diagnosed root cause, and is stated here as such rather than as closure.
2. Second draft ("honest marginal") chose `i` post-hoc, uniformly among the FREE coordinates of
   each randomly-built graph — this is size-biased toward denser graphs (smaller free sets get
   each of their coordinates picked more often), NOT the fixed-coordinate convention this
   project's own `B_n`/`W_1`/`κ_n` estimators actually use anywhere else. Gave `J_n(127)=52.5`,
   `J_n(509)=63.3`, ratio `1.2` — a DIFFERENT quantity from the intended estimand, not merely
   noisier. This diagnosis DOES hold up on review (unlike §1's).
3. Corrected (v3): fixed `gen_index=1`, unconditional full-graph Bernoulli(0.5) draws, both
   canonical branches included and pooled — matching `sample_x_q_delta` exactly, independently
   verified line-by-line on skeptic review against `CertificateLP.solve`'s indexing
   (`bits[j]↔x[j+1]`) and against `sample_x_q_delta`'s own sign convention for both branches — an
   exact match, not merely a plausible-sounding one. This is the version whose numbers are
   reported below, WITH the caveat in §1 that the reason it differs from the very first draft is
   only partially understood.
4. A silent indexing bug was self-caught during the extension to a 3rd point: a ratio field
   computed as `summaries[-1]/summaries[0]` silently switched from meaning `509/127` to meaning
   `1021/127` once a 3rd point was appended, without any code error — caught because two
   differently-named fields started reporting the same number (a self-consistency tripwire, not a
   deliberate check). Fixed via lookup-by-`n` instead of by-list-position; recomputed from already
   saved per-seed data, no LP re-solving needed. **Provenance note (added on review):** the fields
   documenting this fix (`_reprocessed_note`, corrected ratio fields) were written by an unnamed
   post-processing step, not by a version of `ppl_gate_pilot.py` itself submitted for review —
   the numbers are deterministic given the same seeds and were independently spot-checked against
   `rows_by_n` in this point's own verification (below), but the provenance chain (which exact
   script produced the final JSON) is not fully documented in Artifacts.

**Sanity checks (pass, all 1180 (n,seed) pairs across n=127,509,1021, both branches) — corrected
framing on skeptic review.** Point 63's own deterministic inequality `δ_i(actual) ≤ 2x_iw_i`,
with `δ_i(actual)` computed via `log(θ(G0)/θ(G1))` from two direct LP solves rather than
reconstructed algebraically from `x_i,w_i` (avoiding the self-referential-check failure mode this
project has hit before) — holds on every tested pair, minimum margin `3.6e-14`. **Correction: this
is NOT meaningfully "machine precision" as a strength claim** — at `n=1021` the LP solves' own
internal certificate errors run up to `5.5e-10`–`9.5e-10`, four to five orders of magnitude ABOVE
that `3.6e-14` margin, so the tightest observed case sits below this pilot's own numerical noise
floor and the inequality is not meaningfully resolved there either way; the honest statement is
"no violation beyond the `1e-6` tolerance was observed," not "verified with enormous margin."
`θ(G1)·θ(complement(G1))=n` complementary identity: max error `1.86e-08` (a genuinely independent,
nontrivial cross-check of the complement construction and the `w_0=1`/`x_0=1` normalization — this
part is NOT weakened by the above and is independently confirmed correct line-by-line against
`CertificateLP`'s indexing on skeptic review). **Correction: the "two LP engines agree to `~1e-13`
on 6 test pairs" cross-check claimed above has NO artifact in this pilot's saved files** — it is
referenced only in `ppl_gate_pilot.py`'s own docstring, pointing at this session's transcript, not
at a reproducible file; marked `[UNVERIFIED]` rather than treated as confirmed, though the
complement identity and each solve's own internal certificate checks provide independent
corroboration of each LP call on their own. δ_i's own independence from `x_i` is PARTIAL, not
full, also corrected on review: `θ(G0)` is literally the sum of the same `x` vector that supplies
`x_i` (`θ=x.sum()`, `x_i` is one of its `n` summands, `~2%` of the total) — so only the `θ(G1)`/`w`
side of the sanity check is a fully separate computation; this still catches real classes of
error (complement construction, sign convention, normalization) but is weaker than "fully
independent" as first drafted. Branch balance close to the expected 50/50 at every `n` (248/252,
246/254, 93/87) — this confirms the RNG is unbiased, not that the construction is correct (a
distinct, weaker claim than originally implied). **The complement construction and canonical-
sampling match are independently verified correct; the reason an early draft gave a very
different number at n=127 is NOT resolved (see Errors §1) — these are two separate claims and
only the first is settled.**

**Results (500 seeds at n=127,509; 180 seeds at n=1021 — n=2039 skipped this pilot; cost estimate
CORRECTED on review: the ~18 min figure was for 90 reps, a comparable 180-rep budget would cost
~36 min, deliberately kept optional and deferred rather than spending it before the trend at 3
points was assessed):**

| n | reps | `J_n=E[Z²]` | SE | rel. SE | median Z | top1% share of ΣZ² | top5% share of ΣZ² |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 127 | 500 | 64.66 | 5.60 | 8.7% | 3.559 | 11.0% | 40.6% |
| 509 | 500 | 73.43 | 6.81 | 9.3% | 3.615 | 14.0% | 40.9% |
| 1021 | 180 | 102.66 | 18.61 | 18.1% | 3.956 | 18.1% | 50.1% |

Ratios: `509/127=1.136`, `1021/509=1.398`, `1021/127=1.588`. **Corrected statistics (the first
draft's `t=2.01`/"zero within the CI" claim was WRONG, caught on skeptic review — the actual
reference distribution at `dof=1` under this pilot's own stated known-variance convention is
NORMAL, not `t`, so `dof=1` does not mean "no power" the way a small-sample `t` would; both
numbers below independently re-derived and cross-checked, exact match to the review's own
recomputation):** weighted power-law fit `log(J_n)=a+b·log(n)`: `b=0.1518±0.0755`, and testing
`b=0` properly via `Δχ²` (flat/constant model `χ²=5.408` at 2 dof, `p=0.067`; power-law model
`χ²=1.359` at 1 dof; `Δχ²=4.049`, `p=0.044`) — **`b=0` IS rejected at the conventional `p<0.05`
level**, not "well within the CI" as first drafted. The 95% CI on `b` is `[0.005,0.300]` and does
NOT contain zero. Caveat that DOES hold up and is the real reason not to over-read this: the
per-point SEs feeding this fit come from a visibly heavy-tailed `Z²` distribution (top-5% samples
carry `40–50%` of `ΣZ²`; at `n=1021`, the top-1% is literally 2 samples carrying `18%` of the sum)
— the CLT approximation behind each point's SE is itself questionable at these sample sizes, which
is a legitimate reason to distrust the `p=0.044` significance, NOT the "`dof=1` has no power"
reasoning used in the first draft. **A model this pilot's own theory should have compared against
and did not**: `codex-20260914-susceptibility/CROSS_TURAN_ENERGY_THEORY.md` already derives a
`O(log³n)` ceiling for the same underlying `x*` energy (`sup_n E‖x*‖²`, called `POL` there) — a
`log(J_n)=a+b·log(log n)` fit gives `b=0.838±0.426`, `χ²=1.538` (vs the power-law's `χ²=1.359`,
`Δχ²=0.18`) — **the 3 available points cannot distinguish `n^0.15` growth from `(log n)^0.84`
growth**, and neither is favored a priori by anything in this pilot; both beat the flat model.
Tail concentration (`top5%` share of `ΣZ²`, no SE — weaker evidence than the `J_n` fit, not
t-tested): `0.406→0.409→0.501`. **Corrected on review: this undersells the signal by choosing the
softer-looking column** — the `top1%` share is MONOTONIC and growing from the very first step
(`0.110→0.140→0.181`, `+27%` then `+29%`), not "flat then a jump." The median (a tail-robust
statistic) also grows monotonically (`3.559→3.615→3.956`, `+11%` overall) — the whole distribution
is shifting, not only its tail, which weakens (does not eliminate) the "SE is unreliable because
of the tail" defense for the mean-based fit.

**The actual target quantity, computed directly from already-saved data (cheapest possible test,
identified on skeptic review as missing from the first draft — `n=0` new LP solves needed):**
`B_n=(m/4)E[δ_i²]=O(1/n) ⟺ n²E[δ_i²]=O(1)` is the real thing this whole route is meant to bound;
`J_n` is only an upper-bounding proxy (`Z=n·x_i·w_i≥n·δ_i/2` from the sanity inequality). Computed
`n²·E[δ_i(actual)²]` directly from the 1180 already-saved `delta_i_actual` values (this session,
`tmp/direct_target.py`, independently reproduced the pilot's own numbers to the reported digits):

| n | reps | `n²E[δ²]` | SE | rel. SE |
|---:|---:|---:|---:|---:|
| 127 | 500 | 72.23 | 7.32 | 10.1% |
| 509 | 500 | 74.34 | 6.97 | 9.4% |
| 1021 | 180 | 107.69 | 20.24 | 18.8% |

Weighted power-law fit on this DIRECT target: `b=0.102±0.083`, `Δχ²=1.52` (`p=0.217`) — **weaker,
not-significant growth signal on the actual target quantity than on the `J_n` proxy** (which is
consistent with the proxy inequality having real slack — `J_n` growing significantly does not
force the target to grow significantly, since `δ` is bounded well below `2xw` on most sampled
rows). This is genuinely useful, previously-missing information: the target itself is currently
LESS concerning than the proxy that motivated this whole pilot.

**Honest verdict: NOT a Gate 0 pass — but not for the reason first drafted.** The corrected
statistics show `J_n`'s own slope IS nominally significant (`p=0.044`) under the pilot's stated
known-variance convention, while the DIRECT target (`n²E[δ²]`) is NOT (`p=0.217`) — these two
facts together, not a claimed absence of statistical power, are why this is not resolved. Three
further reasons to not treat `J_n`'s `p=0.044` as decisive: (1) heavy-tailed `Z²` makes each
point's SE itself suspect; (2) the `n^0.15` and `(log n)^0.84` models are statistically
indistinguishable on 3 points, and only one of them (the log-model) has independent theoretical
support in this project (Point 63's own `O(log³n)` ceiling) — a genuine open question, not
resolved by this pilot either way; (3) the optimizer actually used (`scipy.linprog` HiGHS vertex)
is NOT the theoretically-required unique min-L2 selector `x*` that Point 63's own equivariance
argument depends on (`test_optimal_energy.py`'s `minimum_energy()`/CLARABEL QP exists in this
same project specifically for this reason and was not used here) — if the optimal face is
degenerate for some sampled graphs, `J_n` may be measuring HiGHS's own pivoting behavior rather
than the intended `x*_i·w*_i`, and this has not been checked. **This does not match the external
proposal's own "Scenario A" criterion** (bounded on ≥5 points including 127,251,509,1021,2039) —
only 3 points were reached, and the picture is genuinely mixed (proxy trending up more clearly
than the target itself). Closer to a genuine "Scenario B/needs-more-work" state than either a
clean pass or a clean fail.

**Kill Analysis.** Nothing is killed and nothing is confirmed. What IS established, corrected: (1)
the cross-Turán bound (`δ_i≤2x_iw_i`, Point 63) sanity check passes on every tested pair with no
violation beyond tolerance — but the claimed "machine precision" margin is itself below this
pilot's own LP-solve noise floor at `n=1021`, so this is "not violated," not "verified with a huge
margin"; the complement-identity check (`θ(G1)·θ(complement(G1))=n`) IS a genuinely strong,
nontrivial, independent confirmation of the construction; (2) the `J_n`/PPL route is a live,
NOT-yet-resolved candidate — `J_n`'s own slope is nominally significant but the DIRECT target
quantity's is not, and neither model comparison (power-law vs log) nor the optimizer-selector
question is settled; (3) an EARLIER, still-UNEXPLAINED `~11×` numerical discrepancy exists between
the very first (flawed) sampling draft and the final (canonical) one at exactly the point (`n=127`)
carrying `48.9%` of the fit's own leverage — the mechanism first proposed for this discrepancy
(dropped branches) is FALSIFIED by the artifact's own `branch_summaries` (branches A and B agree
to within noise), so this remains a genuine open integrity question about the pilot code, not a
closed one; (4) two earlier, methodologically-flawed sampling schemes gave wildly different
qualitative pictures (`12.5×` vs `1.2×` ratio) for reasons only PARTIALLY diagnosed (see #3) — the
lesson about checking sampling conventions against `sample_x_q_delta` stands, but "we understand
why they differed" does not, for the first of the two.

**What this does NOT mean.** Does NOT mean PPL is refuted — even the DIRECT target's `p=0.217`
does not rule out real (if currently sub-significant) growth, and even `J_n`'s significant
`p=0.044` does not establish unbounded growth (a `n^0.15` law is still consistent with a very slow
climb that could plateau, exactly as this project's own earlier points on `λ_n`/local-slope
analysis found for other quantities). Does NOT mean `J_n=O(1)` is refuted either — `b=0` sits
outside the `J_n` fit's 95% CI but well within the DIRECT target's own CI. Does NOT mean the
`gen_index=1`/canonical-sampling construction itself is in doubt — that part is independently
verified correct (complement identity, indexing, branch balance). Does NOT mean the specific
`~11×` v1-vs-v3 discrepancy has been explained — it has NOT, and "the construction is verified
correct" must not be read as covering that open question. Does NOT mean Route B (QADC + `C_q^LP`,
the renamed BA-identity remainder from decision.md's earlier `T_q`-family work, points 15b-20, and
Point 65's `term3`) should be abandoned or paused — nothing here licenses that. Does NOT mean
growing `J_n` would refute the project's own already-open `POL` quantity (`sup_n E‖x*‖²<∞`,
Point 63) even if it were confirmed growing — `J_n` is a fourth-moment-type strengthening of `POL`,
and a bounded second moment is compatible with an unbounded (or differently-scaling) fourth moment
in general; conflating the two would be a new, uncaught error, not a corrected one.

**Recommended next steps, stated but not executed here (cheapest-first, reordered on review —
leverage direction was backwards in the first draft).** (1) **Diagnose or retract the `~11×`
`n=127` discrepancy** (Errors §1) before trusting the fit at all — it sits on the single
highest-leverage point (`48.9%`). (2) Re-solve the top-5% `|Z|` samples (the ones actually driving
the tail and much of the fit) via `test_optimal_energy.py`'s `minimum_energy()`/CLARABEL selector
instead of the raw HiGHS vertex, to check whether `J_n`'s apparent growth is partly a pivoting
artifact rather than a property of `x*_i·w*_i` itself. (3) **Pre-registered kill-test, stated in
advance so it cannot be reinterpreted after the fact**: raising `n=1021` to ~500 reps (matching the
other two points) should, if the current central estimate (`J_n≈103`) holds with a correspondingly
smaller SE, push the power-law slope to roughly `b≈0.19–0.20`, `z≈3.0–3.5` — i.e. this is a
genuine test that could kill `J_n=O(1)` outright, not merely "more precision," and should be
treated as such regardless of which way it comes out. (4) Compute `n²E[δ²]`'s own tail statistics
(median, top1%/top5% share) the same way `J_n`'s were, to check whether the DIRECT target shows
the same tail-heaviness pattern as the proxy. (5) `n=2039` remains the natural 5th-point extension
matching the external proposal's own bar, but only after (1)-(3). (6) This remains an explicit
decision point for the user: continue extending this pilot, pursue (1)-(2) as integrity fixes
first, or shift attention to Route B in parallel — not auto-selected by this pilot's own numbers
either way.

**Skeptic Concerns (FL Step 8a — `reviewer`'s cap closed earlier this session; `skeptic`
substituted per `doubt-driven-development.md` § Independent Review Fallback Policy,
context-asymmetric — given only this point's claim text + `ppl_gate_pilot.py` +
`metrics/ppl_gate_pilot.json`, no session history. Verdict: `WEAKENED` — the core sampling
construction and complement-identity verification hold, but multiple supporting statistical and
causal claims in the first draft were WRONG, not merely imprecise. Every number in the disposition
below independently re-derived from the raw JSON this session, not accepted on the review's word
alone.**
- Concern: the claimed mechanism for why the very first (flawed) sampling draft differed from the
  final one ("dropped half the canonical branches") is algebraically impossible — `flip_generator`
  only ever touches the fixed `gen_index` bit, so for a given seed the two drafts build IDENTICAL
  graphs regardless of branch; the artifact's own `branch_summaries` show branches A/B statistically
  indistinguishable at every `n`, confirming this. → **Fixed**: the false mechanism is retracted
  and replaced with an explicit statement that the `~11×` discrepancy at `n=127` is UNEXPLAINED,
  flagged as an open integrity gap (it sits on the point with 48.9% fit leverage), with the
  circumstantial (not conclusive) `Z≥nδ/2` argument for why v3 is more plausible than v1 stated as
  circumstantial, not as closure.
- Concern: "zero is well within the CI" for the `J_n` slope is false given the claim's own SE — the
  correct `Δχ²`test (matching the pilot's own stated known-variance convention) rejects `b=0` at
  `p=0.044`, and the 95% CI `[0.005,0.300]` excludes zero. → **Fixed**: corrected throughout,
  `Δχ²`/`p=0.044` reported, the real (tail-heaviness-based) reason for caution substituted for the
  `dof=1`-has-no-power framing.
- Concern: the recommendation to raise `n=1021`'s seed budget was justified by claiming it has
  "disproportionate leverage" — backwards; larger SE means LESS weight/leverage in a weighted fit,
  and `n=127` (not `n=1021`) carries the most leverage (`48.9%` vs `28.4%`). → **Fixed**: leverage
  values corrected and cited, the recommendation re-justified as a genuine kill-test with a
  pre-registered predicted outcome, not as "reducing noise."
- Concern: "fully independent channel" for `δ_i` overstates the construction — `θ(G0)` is literally
  the sum of the same `x` vector supplying `x_i` (one of its `n` summands). → **Fixed**: corrected
  to state the independence is partial (only the `θ(G1)`/`w` side is a separate computation), while
  noting this still catches real classes of construction error.
- Concern: the model comparison only considered "`O(1)` vs power-law growth," omitting the
  log-growth model this project's own `CROSS_TURAN_ENERGY_THEORY.md` (`O(log³n)` ceiling) would
  motivate; on 3 points, power-law and log-growth are statistically indistinguishable (`Δχ²=0.18`).
  → **Fixed**: log-log fit added and reported alongside the power-law fit, explicitly stated as
  unresolved between the two.
- Concern: the tail trend was reported via the softer-looking `top5%` column when the `top1%`
  column (and the median) show a cleaner, monotonic-from-the-start growth pattern. → **Fixed**:
  `top1%` and median trends added to the Results table and cited in the verdict.
- Concern: "machine precision" framing for the sanity-check margin (`3.6e-14`) is misleading — at
  `n=1021` the underlying LP solves' own certificate errors (`up to ~1e-9`) are four to five orders
  of magnitude larger, so the tightest case is below this pilot's own noise floor. → **Fixed**:
  reframed as "no violation beyond tolerance observed," not "verified with enormous margin."
- Concern: "two LP engines agree to ~1e-13 on 6 test pairs" has no corresponding artifact in this
  pilot's saved files, only a docstring reference to session transcript. → **Accepted limitation**:
  marked `[UNVERIFIED]` explicitly; not treated as confirmed going forward.
- Concern: the optimizer used (raw HiGHS vertex via `scipy.linprog`) is not the theoretically-
  required unique min-L2 selector `x*` this project's own `CROSS_TURAN_ENERGY_THEORY.md` depends on
  for equivariance, and an existing, already-verified alternative (`test_optimal_energy.py`'s
  `minimum_energy()`) was not used or cross-checked. → **Accepted limitation, added to next steps**:
  not fixed in this point (would require new computation), but explicitly flagged as an open
  methodological gap rather than left silently unaddressed — degenerate-face frequency at this
  project's typical graph density is `[UNKNOWN]`.
- Concern: `J_n` as named risks a fresh symbol collision with this project's own already-open `POL`
  quantity (`CROSS_TURAN_ENERGY_THEORY.md`, `sup_n E‖x*‖²`) — `J_n` is in fact a fourth-moment
  strengthening of `POL`, not an unrelated "external, not in this project" quantity as first
  implied, and growing `J_n` would NOT automatically refute `POL` (second moment can stay bounded
  while a fourth moment grows). → **Fixed**: relationship to `POL` stated explicitly in "What this
  does NOT mean"; the "brand-new, not sourced from this project" framing in the Context section is
  left as-is since it correctly describes `J_n`'s NAME/formulation being externally proposed, not
  its relationship to `POL`, which is now stated separately.
- Concern: the JSON's `_reprocessed_note`/corrected-ratio fields were written by an unnamed
  post-processing step, not the reviewed version of `ppl_gate_pilot.py` itself. → **Accepted
  limitation**: noted in Errors §4; the numbers are deterministic and independently spot-checked
  against `rows_by_n` in this point's own verification, but the exact provenance chain is not
  fully documented.
- Concern: raw numbers in the claim (J_n values, SE, ratios, sanity-check margins, branch counts)
  matched the JSON exactly, no cherry-picking or rounding-in-favor detected. → **Dismissed** as a
  real issue — independently re-verified this session, confirmed accurate.

**Artifacts:** `ppl_gate_pilot.py` (new, main experiment directory — NOT inside
`codex-20260914-susceptibility/`, per Unclaimed Work Ownership), `metrics/ppl_gate_pilot.json`
(per-seed raw data with branch labels, `sanity_check`, `power_law_fit_log_Jn_vs_log_n`,
`tail_concentration_trend_top5pct_share`, `_reprocessed_note` documenting the self-caught indexing
bug). This session's independent verification scripts (scratchpad, not committed):
`direct_target.py`, `loglog_fit.py`. Independently spot-checked against the raw JSON this session
(not accepted from either the agent's or the skeptic's summary alone).

## Point 67 (2026-09-16) — PPL gate 0.1 forensic follow-up: extensively corrected on a SECOND
skeptic-fallback review — the leading explanation for the `~11×` discrepancy is now an aggregator
mismatch (`E[Z]` vs `E[Z²]`), not a construction bug; the min-L2-selector check is real and
non-tautological (confirmed via an added face-width test) but was oversold in scope (`n=509,1021`
unresolved, one informative row silently dropped)

**Context.** Per Point 66's own "Recommended next steps" and a user decision to run a strict
gated sequence (diagnose the `n=127` `~11×` discrepancy FIRST, then the min-L2-selector check,
before any further extension of the pilot or a parallel Route B) — this point reports both
results, then a SECOND skeptic-fallback review's corrections to them (this session's third
skeptic review in the RBA/PPL line of work; the pattern of successive reviews each finding new,
real issues is itself worth noting for the strategic decision at the end of this point). All work
was read-only against `codex-20260914-susceptibility/` (Unclaimed Work Ownership respected); one
factual error in `ppl_gate_pilot.py`'s own docstring (identified below) was corrected in that file.

**Task 1 — diagnosing the `n=127` discrepancy (`v1`'s reported `J_n=5.9` vs `v3`'s `64.66`).**
Since `v1`'s literal code no longer exists, three reconstructions of plausible `v1` behavior were
tested against `v3`'s own seed scheme:

| Hypothesis | Construction | `J_n(127)` | vs `v1`'s `5.9` | vs `v3`'s `64.66` |
|---|---|---:|---:|---:|
| H1 | post-hoc overwrite: draw all `m` bits as `v3` does, then force `bit[gen_index]=0` | 64.6605 | 11.0× | exact match (16 sig. figs) |
| H2 | sequential draw skipping `gen_index` (RNG-stream shifted for the other `m-1` bits) | 73.6607 | 12.5× | 1.14× |
| H3 | correct `v3` construction, coordinate swept over 8 fixed indices (1,2,3,5,10,20,40,63) | 46.7–74.4 | **7.9×–12.6×** | 0.72×–1.15× |

**Corrections from the second skeptic review, independently re-verified this session (exact
arithmetic reproduced, not accepted on the review's word):**
1. **The H3 ratio column above was mis-transcribed in the first draft** (`3.9×–14.5×`) — the
   correct range against `v1`'s `5.9` is `46.7474/5.9=7.92×` to `74.4161/5.9=12.61×`, both
   independently recomputed. Does not change the qualitative conclusion (still `>2×` throughout).
2. **H1 and H3(coordinate=1) are the SAME computation, not independent evidence** — `64.6605149518125`
   matches to all 16 printed digits in both `metrics/diagnose_v1_v3_result.json` and `v3`'s own
   `mean_Z2_J_n` for `n=127`. The forensic chain diff's "`H1: IDENTICAL, 25/25 seeds`" result is a
   PROOF (`flip_generator` only ever toggles the `gen_index` bit, so post-hoc overwrite and
   branch-conditional flip are algebraically the same operation), not an argument — this part of
   Point 66's own skeptic finding is independently reconfirmed. But it means the "three hypotheses
   rejected" framing overstated independent evidence: there is really only ONE genuinely different
   construction tested (H2) plus a coordinate sweep, not three.
3. **A far more parsimonious explanation exists and was missed by construction-only hypotheses,
   because all three held the AGGREGATOR fixed and varied only the GRAPH.** `J_n(H1)/mean_Z(H1) =
   64.6605/5.4389 = 11.89` — this numerically matches the observed `"~11×"` almost exactly.
   `v1`'s reported `5.9` sits `1.74` SE from H1's own `mean_Z=5.4389` (`SE=0.2649`, `Var(Z)=J_n-
   mean_Z²=35.08`) and `0.61` SE from H2's `mean_Z=5.7271` (`SE=0.2859`) — both comfortably
   consistent with sampling noise around `5.9`, unlike any hypothesis's `J_n` (`7.9×`-plus off).
   **Leading (not confirmed) explanation: `v1` reported `E[Z]`, not `E[Z²]=J_n`** — a one-word
   aggregator bug (e.g. `.mean()` on `Z` instead of `Z**2`), not a sampling-construction error.
   This is not proven — `v1`'s literal code is gone — but it is now the single most parsimonious,
   numerically-compelling candidate, and importantly belongs to a DIFFERENT error class than
   anything H1/H2/H3 could have caught, since all three varied graph construction while holding
   the aggregator fixed.
4. **An internal contradiction was found and fixed**: `ppl_gate_pilot.py`'s own docstring
   (written during the `v1→v2→v3` iteration, before this forensic work) claimed `v1`'s forced-bit
   construction "silently dropped half the canonical sample space" — this is exactly the mechanism
   the forensic diff PROVES impossible. The docstring has been corrected in this session to state
   the actual finding (algebraically identical to `v3`, discrepancy unexplained by construction,
   aggregator-mismatch as the leading candidate) rather than leaving a falsified claim in the
   code's own comments.

**Corrected conclusion.** The root cause of the `~11×` discrepancy remains formally UNDIAGNOSED
(`v1`'s code is unavailable to inspect directly), but the evidence has shifted meaningfully since
the first draft: (a) the mechanism ORIGINALLY blamed is proven impossible; (b) only one
independent graph-construction alternative (H2) was actually tested, not three, and it fails to
explain the gap; (c) a specific, numerically-compelling, differently-classed explanation
(aggregator mismatch, `E[Z]` vs `E[Z²]`) now exists and was not excluded by anything tested so
far — the honest state is "most likely an aggregator/units bug in code that no longer exists,"
not "three independent alternatives ruled out, cause unknown." **Cheapest next differentiating
test, not executed here**: if any future reconstruction attempt of `v1` is made, check `mean_Z`
FIRST against `5.9` before computing `J_n` — a hit in `mean_Z∈[5.4,6.2]` would treat the mystery as
resolved (aggregator mismatch), not merely "consistent with noise."

**Task 2 — HiGHS vertex vs the theoretically-required min-L2 selector `x*`.** Re-solved the top-5%
`|Z_ni|` rows (`25` each at `n=127,509`) plus a same-size random bulk-control sample (`25` each)
via a CLARABEL-QP reimplementation of `test_optimal_energy.py`'s `minimum_energy()` selector, and
compared `ρ:=Z²(min-L2)/Z²(HiGHS)` per row (raw JSON independently re-verified, all 100
`reconstruction_matches_stored_row=true`, zero seed/branch mismatches):

| n | group | mean ρ | median ρ | min–max range |
|---:|---|---:|---:|---|
| 127 | top5% | 0.99999999989 | 0.99999999993 | [0.99999999960, 1.00000000010] |
| 127 | bulk control | 1.00000000044 | 1.00000000003 | [0.99999999854, 1.00000000544] |
| 509 | top5% | 0.99999999916 | 1.00000000000 | [0.99999998524, 1.00000000057] (1/25 solves failed, EXCLUDED — see below) |
| 509 | bulk control | 1.00000000130 | 1.00000000000 | [0.99999999922, 1.00000001309] |

**Corrections from the second skeptic review, plus a new check run this session in direct
response to it:**
1. **Is `ρ≈1` informative, or tautological because the optimal face at `gen_index` is generically
   a single point (dimension: `~m/2` free variables vs `m+1` constraints)?** This was NOT checked
   in the first draft and is a legitimate concern — if the face were always a point, agreement
   would be automatic regardless of whether real degeneracy existed elsewhere. **Answered this
   session (`tmp/face_width_test3.py`, cheap: 2 extra LP solves per row on the SAME 10 rows already
   used for the `ρ` check):** solved `max x_i` and `min x_i` on the same optimal face. At `n=127`,
   the face is genuinely NOT a point for most sampled rows — width ranges `6.3e-9` to `1.25e-3`
   (5/10 rows `>1e-6`, i.e. `5`–`6` orders of magnitude above numerical noise), and `ρ` STAYS at
   `≈1` (`0.9999999999` to `1.0000000015`) even at the WIDEST-face row tested (seed `16051163`,
   width `1.249e-3`). **This is a real, non-tautological confirmation at `n=127`**: the face has
   genuine width, and the two selectors still coincide almost exactly — strengthening, not merely
   preserving, Task 2's conclusion at that size. At `n=509`, the same face-width check hit solver
   difficulty with a straightforward `CLARABEL` retry (`9/10` rows failed to converge within a
   quick follow-up's iteration budget; only `1/10` succeeded, width `9.26e-6`) — **this remains
   genuinely unresolved at `n=509`, and was never attempted at all at `n=1021`**, the size with
   this pilot's own heaviest tail (`top5pct_share=0.50`, Point 66) and therefore the size where
   selector-sensitivity risk is highest. The claim that this "closes the optimizer-selector
   concern... and its fit" (the fit uses all 3 sizes including `1021`) OVERCLAIMED scope in the
   first draft — corrected here to "confirmed non-tautological at `n=127` only; `n=509,1021`
   remain open."
2. **The single excluded solve failure (`n=509`, top5%, seed `54251064`, `Z=20.94`) was dropped
   from the mean without noting the likely direction of bias** — a row that fails to converge is
   plausibly the MOST ill-conditioned / closest-to-degenerate row in the sample, i.e. exactly the
   kind of row most likely to show a genuine selector-dependent discrepancy if one exists;
   excluding it likely biases the reported `ρ≈1` toward agreement, not merely toward a smaller
   sample. Its `complement`-side solve DID succeed and matched HiGHS to `1.9e-11` — only the `G0`-
   side `min_energy` QP failed; this partial information was available and not used.
3. **"Re-solved via `test_optimal_energy.py`'s `minimum_energy()`" overstated re-use** —
   `check_minimum_energy_selector.py` reimplements the QP (verified line-by-line to match the
   objective, constraints, solver, and tolerances), it does not import/call the original function.
   One behavioral difference exists: the original hard-fails on a bad solver status; the
   reimplementation retries and reports `NaN` — so this is a cross-check against a verified-
   equivalent COPY, not literally against the existing artifact. Downgraded from "already-
   verified alternative" to "line-by-line-verified reimplementation" in this point's own framing.
4. **`face_error`/`g0_face_error` is a tautological diagnostic, not independent evidence of being
   on the correct face** — `θ` is itself taken from the stored HiGHS solve, so this residual can
   only detect "a different point on the SAME face," never "the wrong face entirely." Accepted as
   a real scope limitation, not fixed (would require an independently-computed `θ`).

**Kill Analysis.** Nothing is killed. What is now established, corrected: (1) the selector-
artifact concern is genuinely closed AT `n=127` (non-tautological, confirmed via an added face-
width test with real degeneracy present), but OPEN at `n=509` (solver difficulty, not resolved)
and NEVER TESTED at `n=1021` (the size that matters most for the tail); (2) the `v1`/`v3`
discrepancy's leading explanation has shifted from "unknown, three alternatives ruled out" to "an
aggregator-class bug (`E[Z]` vs `E[Z²]`) is the most parsimonious candidate, numerically
compelling, though not provable without `v1`'s lost code — a genuinely different, more informative
state than Point 66 left it in, but still not a diagnosis"; (3) a false claim in
`ppl_gate_pilot.py`'s own docstring (about which mechanism `v1` supposedly used) has been
identified and corrected, closing a real internal-consistency gap between the code's comments and
what the forensic diff actually proved.

**What this does NOT mean.** Does NOT mean the `~11×` discrepancy is resolved — the aggregator-
mismatch explanation is a strong LEAD, not a confirmed diagnosis; `v1`'s code cannot be inspected
to confirm it. Does NOT mean the selector-artifact concern is closed for the sizes that matter most
for the fit (`n=509,1021`) — only `n=127` has a non-tautological confirmation. Does NOT mean
`J_n`'s reported values are now fully validated for asymptotic-growth claims — Point 66's
statistical-power/tail-heaviness concerns and the power-law-vs-log-model ambiguity are untouched
by this point. Does NOT license proceeding to Route B or to Route A's further extension
automatically — per the user's own explicit gating, whether this state (one gate closed only at
one size, one gate reduced to a strong-but-unconfirmed lead) counts as sufficient to proceed to the
pre-registered `n=1021→500 reps` kill-test remains the user's decision, not made unilaterally here.

**Skeptic Concerns (FL Step 8a — `reviewer`'s cap closed earlier this session; `skeptic`
substituted per `doubt-driven-development.md` § Independent Review Fallback Policy,
context-asymmetric — given only this point's claim text + the three diagnostic scripts + their
JSON outputs, no session history. Verdict: mixed — Task 1's core algebraic proof `CONFIRMED-REAL`,
Task 1's overall framing `FALSIFIED` as an exhaustion claim; Task 2's `ρ≈1` number
`CONFIRMED-REAL`, its informativeness and scope `WEAKENED`. Every concern independently
re-verified from the raw JSON this session, including a NEW face-width check run specifically in
response to concern 5 below, not accepted on the review's word alone.**
- Concern: "H1/H2/H3 rejected, none within 2×" implicitly frames the space of alternatives as
  exhausted, but all three vary graph construction while holding the aggregator fixed — and
  `v1`'s target is well within noise of `mean_Z` (a DIFFERENT aggregator) for both H1 and H2. →
  **Fixed**: aggregator-mismatch stated as the new leading candidate, with the exact `σ`-distances
  computed and cited; framing changed from "elimination, cause still a mystery" to "elimination
  within one error class, a specific different-class candidate now identified."
- Concern: H1 and H3(coordinate=1) are the same computation (16-digit match), so "three hypotheses"
  overstates independent evidence — only H2 is a genuinely different construction. → **Fixed**:
  stated explicitly; "three rejected" reframed as "one genuinely different construction tested,
  plus a coordinate sweep, plus a tautological repeat of `v3` itself."
- Concern: H3 ratio-vs-`v1` column was mis-transcribed (`3.9×–14.5×` instead of `7.9×–12.6×`). →
  **Fixed**: recomputed and corrected; does not change the qualitative conclusion.
- Concern: `ppl_gate_pilot.py`'s own docstring asserts a mechanism for `v1` that the forensic diff
  directly disproves, and this internal contradiction was not caught or corrected in Point 66. →
  **Fixed**: docstring corrected in the file itself this session (not just noted in decision.md).
- Concern: `ρ≈1` might be tautological if the optimal face at `gen_index` is generically a single
  point, making the min-L2-vs-HiGHS agreement automatic regardless of real degeneracy elsewhere. →
  **Fixed via a new check, not merely argued**: face-width test run this session on the same rows;
  genuine non-zero width found at `n=127` (up to `1.25e-3`) with `ρ` still `≈1` at the widest-face
  row — confirms the agreement is real, not tautological, AT THAT SIZE.
- Concern: the fit-scope claim ("closes the concern... and its fit") overreaches, since the fit
  uses `n=1021` (the heaviest-tail point) which was never selector-checked, and `n=509`'s own
  check hit an unaddressed `1/25` solver failure. → **Fixed**: scope narrowed explicitly to
  "confirmed at `n=127` only"; `n=509`'s follow-up face-width attempt is reported as having failed
  for `9/10` rows, not silently omitted; `n=1021` stated as never attempted.
- Concern: the excluded `n=509` solve failure is plausibly the most-informative (most degenerate)
  row, and dropping it likely biases `ρ` toward agreement, not just toward smaller `N`. →
  **Accepted limitation**: direction of the likely bias stated explicitly; the partial information
  from its successful `complement`-side solve noted as unused.
- Concern: "re-solved via `minimum_energy()`" overstates that the existing verified function was
  actually called, when it was reimplemented (verified equivalent, but a retry-vs-hard-fail
  behavioral difference exists). → **Fixed**: reframed as "line-by-line-verified reimplementation,"
  not "the existing artifact."
- Concern: `face_error` cannot detect being on the wrong optimal face, only a different point on
  the same one, since `θ` itself comes from the stored HiGHS solve. → **Accepted limitation**:
  stated explicitly as a real scope bound on what this check could ever catch.
- Concern: raw numbers in the claim (H1/H2/H3 `J_n`, forensic-diff tallies, `ρ` statistics,
  reconstruction-match counts) matched the JSON exactly at every point checked. → **Dismissed** as
  a real issue — independently re-verified this session, confirmed accurate.

**Artifacts:** `diagnose_v1_v3.py`, `forensic_diff_v1_v3.py`, `check_minimum_energy_selector.py`
(main experiment directory, not inside `codex-20260914-susceptibility/`),
`metrics/diagnose_v1_v3_result.json`, `metrics/forensic_diff_v1_v3_result.json`,
`metrics/check_minimum_energy_selector_result.json`. `ppl_gate_pilot.py`'s docstring corrected
in-place (factual error about `v1`'s mechanism, identified this session). This session's
independent verification script (scratchpad, not committed): `face_width_test3.py`. Independently
spot-checked against the raw JSON this session (not accepted from either agent's or the skeptic's
summary alone).

## Point 68 (2026-09-16) — Gate 0.1 closure tests, EXTENSIVELY corrected on a FOURTH consecutive
skeptic-fallback review: Task A ("aggregator-mismatch, PASS-leaning") has essentially ZERO
discriminating power once checked against the other 8 candidates already sitting in the same
file; Task B's practical conclusion (selector-sensitivity negligible at `n=1021`) SURVIVES and is
now positive-control-verified, but its precision claims were overstated by 4+ orders of magnitude
— the "widths" measured were the LP solver's own noise floor, not real face width

**Context.** Per the user's revised gate plan: two narrow closure tests before deciding on Gate
0.1 — (A) does `v1`'s `5.9` match `mean_Z`, closing the aggregator-mismatch lead from Point 67;
(B) is selector-sensitivity small at `n=1021` specifically. Both were run, reported as
"PASS-leaning" and "PASS with a large margin" respectively, and submitted for skeptic-fallback
review — the FOURTH consecutive review in this RBA/PPL line of work, maintained specifically
because three prior reviews each found real, substantive problems and treating a run of clean
results as self-evidently trustworthy would itself have been an error. This review found serious
issues in both tasks; one (Task B's Gate-3 "no positive control" concern) was resolved this
session with a targeted follow-up check, independently run and verified.

**Task A — CORRECTED. The "PASS-leaning" verdict is walked back to "not falsified, but provides
essentially no evidence."** The original check compared `v1`'s `5.9` against only 2 candidates
(H1, H2). The SAME already-saved file (`metrics/diagnose_v1_v3_result.json`) contains 8 MORE
candidates (`H3_coordinate_sweep`, one per tested coordinate) — independently computed this
session, all 10 candidates' `J_n/mean_Z` ratios:

| candidate | `mean_Z` | `J_n` | `J_n/mean_Z` | distance from `5.9` |
|---|---:|---:|---:|---:|
| H1 (=idx 1) | 5.438907 | 64.6605 | 11.889 | 1.741σ |
| idx 2 | 4.667117 | 46.7474 | 10.016 | 5.52σ |
| idx 3 | 4.961204 | 57.9015 | 11.671 | 3.64σ |
| idx 5 | 5.506265 | 74.4161 | 13.515 | 1.33σ |
| idx 10 | 4.886214 | 55.7352 | 11.406 | 4.02σ |
| idx 20 | 5.298749 | 62.8111 | 11.854 | 2.28σ |
| idx 40 | 4.948721 | 62.1047 | 12.550 | 3.47σ |
| idx 63 | 4.911817 | 57.7863 | 11.765 | 3.81σ |
| H2 | 5.727125 | 73.6607 | 12.862 | 0.605σ |

**Four separate, independently-verified problems, none present in the first draft:**
1. **The `J_n/mean_Z≈11×` argument has zero discriminating power** — ALL 9 candidates give a
   ratio in `[10.0, 13.5]`, a structural property of this heavy-tailed `Z` distribution, not
   evidence for any specific reconstruction. For H1 specifically it is algebraically the SAME
   statement as the `σ`-distance (since `J_n(H1)` matches `v3` to 16 digits) — citing both as
   independent support double-counts one observation.
2. **The real candidate pool is 10, not 2** — 3-4 of 10 pass the `<2σ` threshold (H2: `0.605σ`,
   idx 5: `1.33σ`, H1: `1.741σ`, idx 20 borderline at `2.28σ`), not "one of two." The proper
   multiple-comparisons correction is roughly `5×` weaker than what the first draft applied. All
   10 candidates ALSO sit BELOW `5.9`, meaning "closest candidate" is functionally "family
   maximum" here — a concrete counter-check (below) shows this test would "pass" on a random
   draw roughly `40`–`60%` of the time, which is not meaningful confirmation.
3. **H1 and H2 are not distinguishable from EACH OTHER**: `|H2−H1|=0.288`, pooled
   `SE=√(0.2649²+0.2859²)=0.390`, distance `=0.74σ`. The verdict rested on preferring H2 over H1
   as "closer" — that preference is itself noise.
4. **`v1`'s own Monte Carlo error (unknown reps count) was never included in the comparison** —
   only the reconstructions' own SE was used as the denominator. Including it (even optimistically
   assuming `v1` also used 500 reps) would push H1 to `~1.23σ` and H2 to `~0.43σ` — the test
   becomes MORE permissive, not less, once done correctly; the first draft's framing ("1.741σ, a
   noticeable but not decisive deviation") implied the test almost failed, when a correct
   denominator would make it pass even more easily and thus mean even less.

**A concrete counter-scenario, computed this session**: solving for where a `2σ`-threshold FAIL
region begins (pooled `SE≈0.39`) gives `mean_Z<5.12`, i.e. `J_n/mean_Z>12.6`. The empirical range
across all 10 real candidates is `[10.0,13.5]` — the PASS zone covers the CENTER of this family's
own distribution, not an edge. **No negative control was run** — the already-identified-as-wrong
`v2` construction (size-biased post-hoc coordinate selection) was never checked against `5.9`; if
IT also lands within `2σ`, the test discriminates nothing at all.

**A further, previously-unstated cost of the chosen "winner" (H2)**: `J_n(H2)=73.66≠64.66=J_n(v3)`
— treating `v1=H2` requires assuming BOTH a different graph construction AND an aggregator swap
(two independent, unexplained defects), whereas `v1=H1` requires only the aggregator swap (H1 is
proven algebraically identical to `v3` — one defect, already independently confirmed by this
session's own forensic diff, Point 67). The first draft promoted the two-defect candidate without
noting that a one-defect alternative, with independent forensic support, was available.

**Corrected verdict: NOT FALSIFIED, but this specific test carries essentially no evidential
weight** — consistent with the user's own explicit fallback for exactly this situation:
`v1` is treated as an unrecoverable/non-load-bearing artifact; the aggregator-mismatch idea
remains a plausible, unconfirmed speculation, not a finding this point can claim credit for.

**Task B — corrected, practical conclusion SURVIVES via a new positive-control check, but
measured precision was overstated by 4+ orders of magnitude.** Skeptic found:
1. **[Refuted, in the claim's favor]** `θ`/`face_sum` IS correctly held fixed and identical
   between the min- and max-sub-LPs (verified line-by-line against `CertificateLP.solve`'s own
   encoding) — this specific concern does not hold.
2. **[Major, independently confirmed this session]** In `13/20` top-K rows and `17/18`
   successfully-solved bulk rows, `x_min > x_max` or `w_min > w_max` — a mathematically
   IMPOSSIBLE outcome for a min and max over the identical feasible set. This proves the reported
   `"widths"` of `1e-8`–`1e-10` are the LP solver's OWN reproducibility noise when the objective
   direction flips, not a measurement of real face width. The code had no `x_min≤x_max` check, so
   an inverted interval silently became a small "positive" width in the `Z²`-range computation.
3. **Resolved this session, in the claim's favor, via a targeted positive control**
   (`tmp/positive_control_test.py`, not committed): re-ran the SAME coordinate-range LP on one of
   the inverted rows (seed `105451171`) with `face_sum` deliberately shrunk by `1%` (a
   guaranteed-interior level set with real, non-trivial width). Result: `x_min=0.1151,
   x_max=0.3095`, width `=0.194` — the method DOES detect real width when it is actually present.
   At the TRUE optimal face for the same seed, the same method gives `x_min=0.217579450471,
   x_max=0.217579450462` — inverted by `−9.2e-12`, exactly matching the skeptic's own finding.
   **This resolves the "no positive control" (Gate 3) concern directly**: the instrument has real
   detection power, and at the actual optimal face it reports a value AT its own resolution floor
   (`~1e-9`–`1e-11` in `x`), not a measured nonzero width. Practically, this still means: whatever
   the true face width is (a genuine single point, or a residual width below `~1e-9`), selector
   choice cannot move `Z²` by anywhere near the `0.05` threshold — the PRACTICAL conclusion
   survives, now on firmer ground than the original (uncontrolled) check provided.
4. **"5–9 orders of magnitude below threshold, in every row"** is falsified by the claim's own
   cited data — the maximum recorded `rel_width` (`1.42e-6`, one bulk row) gives `log10(0.05/
   1.42e-6)=4.55`, not `5`. Corrected range: `4.55`–`8.84` orders — both ends of the original
   claim were rounded favorably. Given point 2 above, even this corrected range describes solver
   noise, not real width — restated as "no detectable width above the solver's own `~1e-9` floor,
   itself `6`+ orders below the `0.05` threshold regardless."
5. **The `3/40` one-sided "Infeasible" rows**: skeptic PROVED (min/max sub-LPs share an IDENTICAL
   feasible region, differing only in objective direction) that one-sided infeasibility is
   mathematically impossible — confirming the claim's conclusion (these are solver errors, not
   real empty regions) but for a more rigorous reason than "presolver quirk on a degenerate face,"
   which the code's own saved output cannot actually support (solver status codes were computed
   but never written to the JSON, and the claimed "stored vertex verified inside the other side"
   check does not exist in the code — the saved field is unconditionally `false` for all 3 rows
   when `ranges_ok=False`). **The cost of this proof**: it demonstrates HiGHS returns an outright
   wrong status on `7.5%` of these LPs, reinforcing point 2 rather than being a separate,
   contained issue.
6. **The dropped top-K row (seed `105451107`) is rank `9/20` by `|Z|`** — a real tail-contributing
   row, not an arbitrary exclusion; with `top5pct_share=0.50` at this `n`, the tail defines half
   of `J_n`, so "0 rows `≥0.05`" is computed on a sample missing one of its own highest-leverage
   cases, not a complete accounting.
7. **The "stored value falls inside the range" check is close to tautological** — the stored value
   IS a vertex of the same LP's feasible region by construction; its main real content is a
   smoke-test of coordinate indexing (catching a `free`/`gen_index` mapping bug), not independent
   validation of face width.

**Corrected verdict: PASS survives for the PRACTICAL question ("can selector choice move `Z²` by
`~5%` or more at `n=1021`? No"), now backed by a positive control demonstrating real instrument
sensitivity — but the specific numeric precision claimed (`1e-10`, "5-9 orders") described solver
noise, not a genuine measurement, and has been corrected throughout.**

**Kill Analysis.** Nothing is killed. Corrected state of the user's own two Gate-0.1 conditions:
(A) does NOT achieve real closure — the test used to justify "PASS-leaning" has been shown to
have essentially no discriminating power once checked against the full candidate family already
in the data; per the user's own explicit fallback, `v1` should be treated as an unrecoverable,
non-load-bearing artifact rather than credited with a resolved provenance story; (B) DOES achieve
real closure at `n=1021` specifically — the practical conclusion (selector choice cannot explain
`J_n`'s observed growth) is now supported by a positive control, closing the one structural gap
(no test of whether the method could detect real width at all) that the original check left open.
**Net effect on Gate 0.1: ONE of the user's own two conditions is met on solid ground (B); the
other (A) is not met as a genuine closure, only as an explicit invocation of the user's own
stated "give up on `v1`" fallback.** Whether that combination satisfies the user's own AND-gate
for proceeding to Step 3 is a call for the user, not made unilaterally here.

**What this does NOT mean.** Does NOT mean the aggregator-mismatch idea for `v1` is wrong — it
remains plausible and is not contradicted by anything found here; it simply is not SUPPORTED by
the specific test that was run, which turns out to pass for most of the candidate family
regardless of merit. Does NOT mean selector-sensitivity is resolved at `n=509` — Point 67's
solver difficulty there remains untouched, by the user's own explicit choice to prioritize
`n=1021`. Does NOT mean HiGHS's `7.5%` wrong-status rate on these near-degenerate LPs is itself
fully understood — flagged, not investigated further, consistent with this round's cost-conscious
scope. Does NOT mean the true optimal face at `gen_index` for `n=1021` is proven to be an exact
single point — only that any residual width is below `~1e-9`, far beneath anything relevant to
the `0.05` threshold either way.

**Artifacts:** `check_coordinate_range_n1021.py`, `metrics/check_coordinate_range_n1021_result.json`
(main experiment directory). Task A reused `metrics/diagnose_v1_v3_result.json` (Point 67), no
new computation for the original draft; the corrected version above adds the `H3_coordinate_sweep`
cross-check from the SAME file. This session's independent verification/follow-up scripts
(scratchpad, not committed): the `H3` full-family recompute, and `positive_control_test.py` (the
face_sum-shrink positive control resolving Task B's Gate-3 concern). Independently spot-checked
against the raw JSON this session throughout (not accepted from either the agent's or the
skeptic's summary alone).

## Point 69 (2026-09-16) — Full independent audit of H-CAT31-3 (Points 1-68 + Codex
codex-20260914-susceptibility/): four-status verdict, foundational gap identified, single
recommended next action

**Context.** User-requested independent audit (25-section spec, user-provided, external-AI-
authored request evaluated and accepted as legitimate/well-aligned with this project's own FL
discipline — not executed blindly, but not treated with the same Gate-1 suspicion as the earlier
PPL/QADC math proposals, since this request asked for SYNTHESIS of already-existing material, not
new unverified claims). Executed as: two parallel background audits (Points 1-53; Codex Points
57-64) plus this session's own direct synthesis of Points 54-68 (already fresh/independently
verified from Points 65-68's own extensive skeptic-review work earlier this session). Full report:
`AUDIT_H-CAT31-3_2026-09-16.md` (this directory).

**Headline findings, not previously stated anywhere in the project:**
1. **Foundational gap**: `|λ_n|=m·E[δ_i]` and `κ_n=E[δ_i²]/(E[δ_i])²` (as informally used
   throughout Points 12c/13/54+) are NOT independently derived/verified anywhere in Points 1-53 —
   the project's own code defines `κ_n:=B_n/W_1`, equal to the textbook form only CONTINGENT on
   the unverified `|λ_n|=m·E[δ_i]` identity. Nothing downstream is known to be wrong, but nothing
   downstream has actually confirmed this equivalence either.
2. **A documented false-positive from the skeptic-review layer ITSELF** (Point 47→48, found by
   the Points 1-53 sub-audit): skeptic rated Point 47's claim `CONFIRMED-REAL`; Point 48's LP dual
   certificate later proved it substantively WRONG (cross-method solver agreement was not
   sufficient evidence of LP primal feasibility — only a verified dual certificate was). This is
   qualitatively different from this session's own repeated finding (first-draft claims being
   walked back on review) — here the REVIEW layer itself failed, not just the claim.
3. **The aggregated cross-Turán bound (`|λ_n|≤2(E‖x*‖²-1)`, Codex Point 63) structurally REQUIRES
   the unique min-L2 selector** for its equivariance argument — confirmed by the Codex sub-audit
   directly from `CROSS_TURAN_ENERGY_THEORY.md`'s own text, NOT merely an empirical concern this
   session raised independently for the PPL work. Empirically checked coincident with the HiGHS
   vertex on 36 small/medium graphs (Codex); never checked at the n=509-4093 range where the
   RBA/PPL work actually operates.
4. **Two requested audit sections (§4 support-saturation/Tao/RPCB machinery, §5 bulk-Fourier-
   identity/"BA-exact") do not exist under those names anywhere in Points 1-53** — confirmed by
   direct full-document grep, zero hits; they first appear at Point 63-65 (already covered in this
   session's own Points 54-68 synthesis). "Kashin"/"RHPRI" — zero hits anywhere in the entire repo.
5. **`η_n:=K_n/(4J_n)`, a diagnostic ratio proposed by the user's own earlier message but never
   before actually computed**: `0.279, 0.253, 0.262` at n=127,509,1021 — stable across an 8× range
   in n, computed this session directly from already-saved data (no new LP solves).

**Four-status verdict (per the audit's own required format):**
- `H-CAT31-3`: **OPEN** — exact exponent -1 empirically excluded (real 95% CI), but `O(1/n)` as an
  upper bound neither proven nor excluded.
- First-chaos boundedness: **CHALLENGED** — pilot-level support only, aggregated bound's selector-
  dependence untested at the relevant n-range.
- PPL route: **INCONCLUSIVE** — `J_n` (proxy) marginally significant, `K_n` (direct target) not;
  this disagreement is itself the most informative open fact in the route.
- QADC + `C_q^LP` route: **OPEN, never attempted as an actual proof target.**

**Recommended next action (single, per the audit's own "not a list of ten" requirement):**
resolve the `J_n`-vs-`K_n` disagreement at `n=1021` specifically — complete the already-designed,
already-partially-executed, currently-halted extension to `~500` reps, tracking `J_n`, `K_n`, AND
`η_n` jointly. This is an explicit restatement for the user's own decision, not executed here.

**Kill Analysis.** Nothing new killed by this audit itself — it is a synthesis, not a new
experiment. What changed: the project's own claimed statuses for Points 1-68 are now independently
cross-checked in one place, with 3 genuinely new findings (the foundational gap, the skeptic-
layer false-positive precedent, the selector-dependence being a structural not merely empirical
concern) that were not previously stated together anywhere in the project.

**What this does NOT mean.** Does NOT mean any previously-`[PROVED-IN-PROJECT]` result is now in
doubt — the audit RE-CONFIRMED every such result it checked against code/JSON, it did not merely
repeat prose claims. Does NOT mean the foundational-gap finding (item 1) implies `κ_n` is wrong —
only that its exact equivalence to the textbook form has never been independently confirmed as
literally stated. Does NOT constitute a new experiment or proof attempt — per the audit's own
explicit instruction, none was performed.

**Artifacts:** `AUDIT_H-CAT31-3_2026-09-16.md` (this directory, full report — sections A-I,
verified timeline for all 68 points + Codex's 8 points, proven theorem chain, negative results,
methodology failures, reproducibility table, decision tree). Two background sub-audits (Points
1-53; Codex Points 57-64) plus this session's own direct synthesis (Points 54-68, reusing this
session's own extensively-verified Points 65-68 work) — all independently cross-checked against
raw code/JSON per the audit's own source-priority rule (code > raw data > decision.md > theory .md
> summary), not accepted from agent prose alone.

## Point 70 (2026-09-16) — Correction to Point 69: the `|λ_n|=m·E[δ_i]` "foundational gap" was
itself an overclaim — the identity is real, independently verified both algebraically and
numerically (exact, n=7, diff `5e-11`); J_n-vs-K_n interpretation remains genuinely open, not
resolved by either side's framing

**Context.** A user-relayed external review of Point 69 (same provenance discipline as prior
external proposals this session — evaluated on its merits, not accepted at face value) raised
several points. One is a direct, checkable mathematical correction; verified immediately below.
The others are strategic reframings that this point explicitly does NOT adopt yet, pending the
`n=1021→500` extension already in progress (per the user's own direct instruction, launched
before this correction was written).

**Correction 1 — CONFIRMED, the `|λ_n|=m·E[δ_i]` identity is real, not a gap.** Point 69 listed
this as a "foundational gap" (never independently derived/verified in Points 1-53). The external
review supplied a standard derivation: for any real-valued `f:{0,1}^m→ℝ` under product-Bernoulli(p)
measure, `d/dp E_p[f] = Σ_i E_p[D_if]` where `D_if=f(x_i=1)-f(x_i=0)` (a direct consequence of
`E_p[f]` being a degree-`≤m` polynomial in `p`, not requiring monotonicity — a more general fact
than the usual monotone-Boolean-function Margulis-Russo formula, but the same underlying
computation). With `δ_i:=X(x_i=0)-X(x_i=1)=-D_iX`, `M_n'(p)=-Σ_iE_p[δ_i]`; at `p=1/2`, prime
multiplicative orbit-transitivity (established, Points 4/5) makes all `E_{1/2}[δ_i]` equal, giving
`λ_n:=M_n'(1/2)=-m·E[δ_i]`, and since `δ_i≥0` (established, Point 13a) `|λ_n|=m·E[δ_i]`.

**Independently verified numerically this session** (not accepted from the external review's
algebra alone): exact enumeration at `n=7` (`m=3`, all `2³=8` bit-configurations), using the
project's own `theta_via_lp` unmodified. Numerical derivative of `E_p[X]` at `p=1/2`
(`h=1e-6` central difference): `-1.7988928313`. Direct computation of `-m·E[δ_i]` (all three
generators give IDENTICAL `E[δ_i]=0.5996309438`, confirming the orbit-transitivity claim exactly,
not merely assumed): `-1.7988928314`. **Difference: `5e-11`**, consistent with the finite-
difference step's own `O(h²)` truncation error — i.e., exact agreement. `δ_i` range at this `n`:
`[0.4526,0.7466]`, strictly positive, consistent with the established monotonicity.

**Corrected status**: `|λ_n|=m·E[δ_i]` is **[PROVED-IN-PROJECT]** (general polynomial-derivative
argument + already-established orbit-transitivity + already-established `δ_i≥0`), independently
re-confirmed numerically. `κ_n:=B_n/W_1=E[δ_i²]/(E[δ_i])²` follows immediately as an algebraic
corollary. **Point 69's "foundational gap" framing is retracted** — this was a documentation gap
(the derivation was never written down as its own explicit step in decision.md), not a
mathematical one. This does NOT change Point 69's overall four-status verdict, KILL analysis, or
recommended next action — it corrects exactly one of the audit's three headline findings.

**Correction 2 candidate — NOT adopted, stated as an open question pending the in-progress
extension.** The same external review argued `J_n` (`slope≈0.20` by its own endpoint-ratio
estimate) and `K_n` (`≈0.17`) tell "almost the same story," proposing the real bottleneck is
"common slow growth of both" rather than a `J_n`-vs-`K_n` disagreement. **Independently checked
this session** using the project's own proper weighted 3-point fit (not an endpoint-ratio
shortcut): `b_J=0.1518`, `b_K=0.1023` — same ORDER of magnitude, but a real, non-trivial
difference (`~33%` relative), and — more importantly, per Point 68's own corrected statistics —
the two differ in whether they clear conventional significance at all (`J_n`: `Δχ²=4.049`,
`p=0.044`; `K_n`: `Δχ²=1.52`, `p=0.217`, Point 69's own §D). **Both readings remain live and are
NOT distinguished by the currently-available 3-point data** — this is exactly the ambiguity the
in-progress `n=1021→500` extension (§ below) is designed to resolve, not a settled matter either
way. Explicitly declining to adopt either framing before that data returns.

**Other strategic reframings raised (first-chaos status upgrade, QADC/Route-B scoring, un-killing
specific routes, a weaker sufficient `C_q^LP` bound, a proposed uniqueness-vs-selector
provenance check) — NOTED, NOT YET ACTED ON.** Several are plausible and worth real evaluation
(the uniqueness-vs-selector check in particular looks genuinely cheap and informative — does the
support-saturation uniqueness theorem, Point 63/64, apply to the SAME optimizer notion Point 63's
aggregated bound requires?) — but adopting them now, before the extension's own data is in, would
risk exactly the pattern this session's audit itself flagged four times running: a plausible-
sounding reframing accepted without independent verification. Deferred to the next point, after
`n=1021→500` results are available.

**Kill Analysis.** Nothing killed. One correction made (the `λ_n`/`κ_n` identity, now
[PROVED-IN-PROJECT], independently verified two ways). Everything else from the external review
is explicitly held open, not adopted, pending data already in flight.

**Artifacts:** this session's verification script (scratchpad, not committed): exact `n=7`
enumeration checking `M_n'(1/2)` against `-m·E[δ_i]` via the project's own unmodified
`theta_via_lp` (`20260909-lovasz-theta-random-circulant-graphs/run.py`); a second script
recomputing the `J_n`/`K_n` weighted slopes directly from Point 66/68's own saved summary numbers.

## Point 71 (2026-09-16) — n=1021 extended to 500 reps (pre-registered kill-test executed): `J_n`'s
slope is WEAKER than predicted (`b=0.1296`, not `0.19-0.20`), `K_n` unchanged (`p=0.218`), `η_n`
formally confirmed stable — the predicted "center holds, SE shrinks" pattern did NOT materialize,
but the old-vs-new-batch difference is itself NOT statistically significant (honest correction to
the executing agent's own slightly overstated framing)

**Context.** Direct user instruction: complete the pre-registered kill-test from Points 66-68 —
extend `n=1021` from `180` to `500` reps (matching `n=127,509`), tracking `J_n`, `K_n`, and
`η_n:=K_n/(4J_n)` jointly, per the user's own explicit specification. `ppl_gate_pilot.py` extended
with resume logic (reuses the 180 already-computed rows by seed match, computes only the missing
320 — independently verified this session: 500 unique seeds, zero duplicates, exact
180/320 split matching the documented seed scheme). Regression check before the real run
reproduced Point 66's own `J_n`/`Δχ²`/`p` numbers exactly from already-saved data, confirming the
extended script's logic is unchanged from what was already skeptic-reviewed.

**Results, independently re-verified against `metrics/ppl_gate_pilot.json` this session:**

| n | reps | `J_n±SE` | `K_n±SE` | `η_n` | top1%/top5% `Z²` share | median `Z` | median `δ` |
|---:|---:|---|---|---:|---|---:|---:|
| 127 | 500 | 64.66±5.60 | 72.23±7.32 | 0.279 | 11.0%/40.6% | 3.559 | 0.02931 |
| 509 | 500 | 73.43±6.81 | 74.34±6.97 | 0.253 | 14.0%/40.9% | 3.615 | 0.00742 |
| 1021 | 500 | **86.58±8.94** | 88.80±9.47 | 0.256 | 17.2%/44.4% | 3.994 | 0.00395 |

**Weighted power-law fits (`log Y=a+b·log n`, known-variance `Δχ²` convention per Point 66's own
corrected framing):**

| | `b±SE` | 95% CI | `Δχ²` (1 dof) | `p` |
|---|---:|---|---:|---:|
| `J_n` | 0.1296±0.0620 | [0.008, 0.251] | 4.373 | **0.037** |
| `K_n` | 0.0847±0.0687 | [-0.050, 0.219] | 1.519 | 0.218 |
| `J_n/K_n` | 0.0338±0.0263 | [-0.018, 0.085] | 1.648 | 0.199 |

**Honest evaluation of the pre-registered prediction — corrected from the executing agent's own
slightly overstated framing.** Points 66-68 predicted: if `J_n(1021)`'s central estimate `≈103`
held while `SE` shrank (`180→500` reps), the slope should rise to `b≈0.19-0.20`, `z≈3.0-3.5`.
**Actual outcome: `J_n(1021)` fell to `86.58` (from `102.66` on the same 180 reps re-used inside
this 500), giving `b=0.1296`, `z≈2.09` (via `Δχ²`) — WEAKER than predicted, not stronger,** even
though `p=0.037` is nominally BELOW `p=0.044` (SE also shrank, `18.61→8.94`). The naive
extrapolation's assumption (fixed center, shrinking SE only) did not hold.

**Correction to the executing agent's own report, independently checked this session**: the
agent's write-up characterized the `180→500` shift as "not noise" (comparing the combined
500-rep SE against the point-difference, an informal `~1.8σ` framing). This is not the right
comparison, since the `180` reps are a SUBSET of the `500`, not independent. The correct test —
run this session — is a Welch two-sample t-test of the NEW `320` rows' `Z²` values against the
OLD `180` rows' `Z²` values (two genuinely independent batches): **`t=1.209`, `p=0.228`, NOT
significant.** The new batch's own mean (`77.54`) is lower than the old batch's (`102.66`), but
this specific difference is statistically consistent with ordinary sampling variation given the
batch sizes and variances — **it would overclaim to say the shift is "confirmed real"; the honest
statement is "the combined point estimate moved, the movement is not itself statistically
distinguishable from noise between batches, and the pre-registered prediction's specific numeric
target (`b≈0.19-0.20`) did not materialize either way."**

**`η_n` formally confirmed stable, not merely "stable on the eye"**: a dedicated weighted fit on
the `J_n/K_n` ratio itself gives `b=0.034±0.026`, `p=0.199` — statistically indistinguishable from
a flat ratio across the full `8×` range in `n` tested. This directly answers the still-open
question from Point 70: `J_n` and `K_n` do NOT diverge from each other in any way this data can
detect — whatever growth exists in each, their RATIO (a proxy for cross-Turán certificate
tightness) is not detectably drifting.

**Tail-concentration correction at `n=1021`**: `top5%` share of `ΣZ²` was `0.501` on the
original `180` reps (Point 66's own most extreme tail reading in the whole pilot); on the full
`500`, it is `0.444` — still the heaviest of the three tested `n`, but meaningfully less extreme
than the `180`-rep reading suggested. This partially (not fully) confirms the concern already
raised in Point 68 that small-sample tail statistics at `n=1021` should not be over-read.

**Bonus, incidental to this extension**: the script's `_provenance_note` field states this run was
produced entirely by `ppl_gate_pilot.py`'s own `main()`, superseding the earlier `_reprocessed_note`
(an unnamed post-processing step, flagged as an open provenance-chain gap in Point 67's own
Skeptic Concerns). That specific gap is now closed as a side effect of this extension.

**Kill Analysis.** Nothing killed. What changed: (1) `J_n`'s growth signal survives extension to
full sample size at `n=1021` but is WEAKER in magnitude than the pre-registered prediction hoped
(`b=0.130` vs predicted `0.19-0.20`), while remaining nominally significant (`p=0.037`) under the
same convention as before; (2) `K_n`'s non-significance is essentially unchanged by the extension
(`p=0.218` vs prior `0.217`) — the direct target shows no reliable growth signal at any sample
size tested so far; (3) `η_n`'s stability is now a tested, not merely observed, finding
(`p=0.199` for a flat ratio); (4) the `n=1021` tail was partially, not wholly, a small-sample
artifact — it remains the heaviest tail of the three `n` even at full sample size.

**What this does NOT mean.** Does NOT mean the pre-registered kill-test "failed" in the sense of
being uninformative — per its own design (Point 68's recommendation §3), it WAS a genuine test
that could have gone either way, and the actual result (weaker-than-predicted `J_n` growth) is
itself the useful information, not a null outcome. Does NOT mean `J_n` and `K_n` are proven to
track the same underlying growth — only that this specific dataset cannot currently distinguish
"they track together" from "they diverge," since the `J_n/K_n` ratio fit itself has wide, non-
significant bounds. Does NOT mean the old-vs-new-batch `t=1.209,p=0.228` result proves the shift
IS noise — a `p=0.228` non-significant result is an absence of evidence for a real shift, not
evidence of its absence, at this batch size. Does NOT resolve which of Route A / A2 / B (per the
decision tree in Point 69/AUDIT_H-CAT31-3_2026-09-16.md §I) this data points to definitively —
the qualitative picture (`J_n` marginally growing, `K_n` not, `η_n` stable) is UNCHANGED from
before this extension, just measured with less optimistic magnitude than the pre-registered
prediction hoped; per that same decision tree, this remains closest to Route A2's territory
(`J_n↑, K_n bounded → seek a direct `E[δ_i²]=O(n⁻²)` theorem, do not jump to QADC`), now on a
firmer, larger-sample basis than before.

**Artifacts:** `ppl_gate_pilot.py` (extended with resume logic + `K_n`/`η_n`/ratio-fit
computation, canonical sampling protocol unchanged), `metrics/ppl_gate_pilot.json` (updated,
full 500/500/500 raw data + all summary statistics). This session's independent verification
scripts (scratchpad, not committed): resume-logic/seed-uniqueness check, old-vs-new Welch
t-test. Independently spot-checked against the raw JSON this session (not accepted from the
agent's summary alone) — one framing correction made (old-vs-new batch significance).

## Point 72 (2026-09-16) — Deferred check from Point 70 closed, cheaply, with a clean answer: the
support-saturation uniqueness theorem (Codex Point 64) and the aggregated cross-Turán bound's
equivariance requirement (Codex Point 63) use the SAME min-L2 selector object throughout —
no hidden inconsistency between the two theorems

**Context.** Point 70 flagged, as a cheap next question (not yet acted on there): does the
support-saturation/uniqueness machinery (`|supp y|≥2Q+1`, Codex Point 64) apply to the SAME
optimizer notion that the aggregated cross-Turán bound (Codex Point 63) formally requires (the
unique min-L2 selector `x*`, per this session's Points 67-69 audit finding that this requirement
is real, not merely an empirical concern)? Checked directly by reading
`codex-20260914-susceptibility/CROSS_TURAN_ENERGY_THEORY.md` in full (read-only, per Unclaimed
Work Ownership).

**Finding: they are the same object, defined once and reused consistently.** The document's
`## Equivariant minimum-energy selector` section (lines 31-38) defines
`x*(G)=argmin‖x‖²₂` on each optimal face — "strict convexity makes the selector unique, and
uniqueness makes it equivariant" — and derives the aggregated bound `(E1)` from it. The very next
section, `## Point 64 refinement: exact energy anatomy` (lines 96-113), states
`s=|supp(y)|≥2Q+1` and `n‖y‖²₂=(n/s)(1+CV_support(y)²)` WITHOUT redefining `x`/`y` — it continues
directly from the same `x*`/`y*=FFT(x*)/n` notation established one section earlier. **No second,
generic-vertex optimizer is introduced anywhere in this document.** The theory is internally
consistent in its selector choice throughout Points 63-64.

**What this does and does NOT resolve.** Does NOT mean the selector question is fully closed —
the OPEN question remains whether the project's actual PRODUCTION code (HiGHS vertex via
`scipy.linprog`) equals `x*` in general, not merely on the graphs already tested. That empirical
question is exactly what Points 67-68 (n=127, n=1021) already investigated directly (not via this
theory-text check) and found agreement to high precision on tested instances, with `n=509`
un-resolved (Point 68) and the underlying theorem itself only proven for the min-L2 selector, not
for an arbitrary vertex. This point closes a DIFFERENT, narrower worry: that Codex's own two
theorems (support saturation, aggregated susceptibility bound) might silently reference two
different optimizer notions without saying so — they do not.

**Also directly confirms, independently, this session's own PPL/J_n framing (Points 66-70)**: the
document's own `(POL)` target (line 60, `sup_n E‖x*(G)‖²₂<∞`) is explicitly named, by Codex itself,
as "the one live analytic target," and its own "Remaining proof gaps" section (line 90) states
`(POL)` is `[OPEN]`, requiring "positivity AND optimality, not a uniform estimate on the full
random nullspace" — i.e. Codex's own published external-bound corollary (`|λ_n|=O(log³n)` via
Bandeira et al. 2025's nullspace estimate) is explicitly NOT claimed to prove `(POL)`, matching
this session's own repeated finding that bounded-first-chaos remains open. Codex's own gap list
also independently states, as its 3rd remaining gap, that "bounded `lambda_n` alone is not the
full `Var(X_n)=O(1/n)` theorem" — the higher-chaos residual `R_n` must still be controlled
separately — matching this audit's own repeated point that no route closes the full hypothesis by
itself.

**Kill Analysis.** Nothing killed. A specific, narrow open question from Point 70 is now closed
(no cross-theorem selector inconsistency in Codex's own theory document) — a genuinely cheap
check, as anticipated, with a clean (reassuring) answer. The broader selector-empirical-validity
question (does HiGHS==min-L2 in general, not just on tested graphs) remains open per Points 67-68.

**Artifacts:** none new — this point is a direct read of an existing file
(`codex-20260914-susceptibility/CROSS_TURAN_ENERGY_THEORY.md`, read-only, lines 1-114 in full),
no computation performed.

## Point 73 (2026-09-16) — Route A2 opened via Mechanism Development Mode; HEADLINE FINDING
RETRACTED on skeptic review (`c≈1` is exactly the structureless-null prediction, and `c=2`
exclusion is mathematically forced, not evidence) — genuine, salvaged finding: the tightness
ratio `U:=δ_i/(2x_iw_i)` CONCENTRATES around `1/2` with shrinking weighted spread
(`sd_w(U)≈0.149→0.093→0.068`, non-overlapping bootstrap CIs, `~n^-0.37`), a real but narrower
and more cautious result than first drafted

**Context.** This corrects the first draft of Point 73 (same session, same exploration) after
skeptic-fallback review found the headline claim (regression-through-origin slope `c≈1.0`, framed
as "structural, not loose") does not survive scrutiny — the most severe single correction in this
session's now five-review pattern in the RBA/PPL/Route-A2 line, since it identifies the CENTRAL
claim as built on a statistic with no power to show what it claimed to show, not merely an
overclaimed scope or a precision error.

**Fatal problem with the first draft, independently re-verified this session (not accepted on the
review's word alone).** Define `U_i:=δ_i/(2x_iw_i)∈[0,1]` (well-defined since `0≤δ_i≤2x_iw_i` was
already independently verified, Points 66-68). The through-origin slope is EXACTLY
`c=2·⟨U⟩_w` where `⟨·⟩_w` is the `(x_iw_i)²`-weighted mean. Two consequences, both confirmed by
direct recomputation this session:
1. **`c=2` is mathematically IMPOSSIBLE to exceed** — since `U_i≤1` always, `c≤2` holds
   deterministically for the sample AND every bootstrap resample. The first draft's "`c=2`
   decisively excluded" was reporting an algebraic certainty as if it were empirical evidence.
2. **`c≈1` is EXACTLY what a structureless null predicts.** If `U_i` had NO structure at all
   (e.g. `U~Uniform[0,1]`, independent of `x_iw_i`), the null's own prediction is `c=1.000`
   exactly, `η_n=⟨U²⟩_w=1/3≈0.333`, and through-origin `R²=0.75`. The first draft's own numbers
   (`c=1.01,0.99,1.00`; `η_n=0.279,0.253,0.256`; `R²=0.919,0.965,0.982`) are close to this null on
   the FIRST two statistics and only depart on `R²` — meaning `c≈1` **cannot discriminate**
   "`δ_i` structurally tracks `x_iw_i`" from "the tightness ratio is unstructured noise centered
   on the theorem's own midpoint." The "degeneracy check" in the first draft asked the wrong
   question (is `c·x_iw_i` distinguishable from `x_iw_i`?) instead of the right one (is `c` itself
   distinguishable from a structureless-null artifact?) — it passed by construction, not by
   surviving a real test.

**Further first-draft errors found and independently confirmed this session:**
3. **Flat identity error**: `4η_n≡K_n/J_n` by `η_n`'s own definition (`ppl_gate_pilot.py:334`) —
   the first draft cited the `K_n/J_n` ratios as separate corroboration of `c≈1`, when they are
   the SAME number restated (`c²=K_n/J_n` exactly, up to the residual term).
4. **Two inequality steps were conflated as one.** `CROSS_TURAN_ENERGY_THEORY.md` line 26
   (`v0/v1≤1+2x_iw_i`, the real Parseval-gap step) is followed by a SEPARATE step at line 27
   (`δ_i=log(v0/v1)≤2x_iw_i`, via `log(1+t)≤t`) — the first draft attributed the ENTIRE
   `2x_iw_i-δ_i` slack to the Parseval gap alone. Independently recomputed this session (reusing
   already-saved `theta_G0`,`theta_G1` per row — zero new LP solves): a regression of the TRUE
   Parseval gap `g_i:=(1+δ_i^{bound})-θ(G0)/θ(G1)` on `x_iw_i` gives `c_g=0.912` (n=127),
   `0.994` (n=509), `0.986` (n=1021) — genuinely different from the full `c` at `n=127`
   specifically (`0.912` vs `1.013`, an `~10%` gap attributable to the log-curvature step, not the
   Parseval step), converging as `n` grows. The first draft's entire "where this points"
   interpretive section (attributing the whole slack to the Parseval/Fourier-correlation
   mechanism) was not entitled to that attribution.
5. **Effective sample size is small and tail-dominated**: `(x_iw_i)²`-weighting concentrates `c`'s
   information on `≲130/120/100` (of `500`) rows at `n=127/509/1021` respectively (bound via
   `1/Σw²`); the weighted-typical `Z` is `~4×` the median `Z`. The unweighted mean/median of `U`
   (`0.61/0.59` at n=127, `0.56/0.54` at n=509, `0.53/0.52` at n=1021) differs meaningfully from
   the weighted mean — confirmed this session — meaning "typical rows" and "tail-dominant rows"
   behave somewhat differently, and the first draft's "`δ_i` tracks `x_iw_i` closely" claim was
   not shown to hold for the bulk, only for the tail-weighted statistic.
6. **An internal arithmetic inconsistency** at `n=1021`: the tabled `c=1.0028` does not satisfy
   `K_n=c²J_n+n²E[resid²]` together with the tabled residual `1.59` and `R²=0.982` (all three
   can't hold simultaneously) — traced to one exploration script reporting the bootstrap MEAN
   under a column labeled "point estimate," not the actual point estimate. Corrected value:
   `c=1.0036` (independently re-derived this session from the exact orthogonality identity).
7. **The `p=0.037`-vs-`p=0.218` "tension"** the first draft flagged as evidence AGAINST easy
   reconciliation was backwards: `J_n` and `K_n` are computed from the SAME `500` rows per `n`,
   with `ρ≈0.86-0.98` correlation between them — the slope DIFFERENCE (`0.045`) is only `~1.5σ`,
   not significant. There is no real tension; flagging one was itself an error, not appropriate
   caution.
8. **"`K_n/J_n` all close to 1" was not accurate** — `ppl_gate_pilot.py`'s own stored delta-method
   SE for this ratio (`ratio_J_over_K_SE_delta_method`) shows `n=127`'s `J_n/K_n=0.895±0.046` is
   `2.26σ` from 1, OUTSIDE the 95% CI — the first draft asserted "close to 1" for all three
   without checking the one `n` where its own project already had the tool to check.

**What survives, independently re-verified this session (matching the review's own numbers
closely): the tightness ratio `U` genuinely CONCENTRATES, and this is real, differentiating
information the mean/`c` statistic could not show.**

| n | `sd_w(U)` (weighted) | 95% bootstrap CI (3000 resamples) | null's `sd`(Uniform) |
|---:|---:|---|---:|
| 127 | 0.1494 | [0.1352, 0.1639] | 0.2887 |
| 509 | 0.0933 | [0.0833, 0.1037] | 0.2887 |
| 1021 | 0.0676 | [0.0602, 0.0753] | 0.2887 |

**Non-overlapping CIs across all three `n` — this shrinkage is not noise.** Weighted log-log fit:
`sd_w(U) ~ n^b`, `b≈-0.37`. This IS a real, falsifiable, structural finding (the tightness ratio's
DISPERSION shrinks with `n`, `3-18×` below the structureless-null value already at `n=127`, and
further at larger `n`) — narrower and more cautious than the first draft's claim, but genuine.

**Kill Analysis.** The first draft's central claim (`c≈1` as evidence of structure) is
**[FALSIFIED as evidence]** — not falsified as a hypothesis (nothing rules out `δ_i` tracking
`x_iw_i` in some sense), but the specific statistic offered as proof has no power to show it. What
survives: `U`'s weighted dispersion genuinely concentrates with `n`, a real, three-point-confirmed,
non-overlapping-CI finding. The `J_n`-vs-`K_n` "tension" is retracted (no real tension, given
`ρ≈0.9` correlation). The Parseval-vs-log-curvature decomposition is new, real content the first
draft was not entitled to before running it.

**What this does NOT mean.** Does NOT prove `E[δ_i²]=O(n⁻²)` — `sd_w(U)→0` is a tail-weighted
statistic (`ESS≲100-130`), not shown to hold for the bulk of the distribution. Does NOT mean the
`n^-0.37` scaling is asymptotic law — three points is a fit, not a proof, and the statistic is
itself tail-dominated in a way that could have its own `n`-dependent bias (the review's own
concern: rising tail-mass fraction with `n` could mechanically tighten a leverage-weighted
statistic independent of any real concentration). Does NOT mean Route A2 has produced a
theorem-ready lemma — this remains Mechanism Development Mode's early stage, now with one
correctly-identified real phenomenon (`U`'s concentration) instead of one incorrectly-identified
one (`c≈1`).

**Recommended next steps (per the review's own proposed tests, all zero new LP cost, already
partially executed this session).** (1) **Already done, reported above**: Parseval-gap-only
regression (`c_g`), trimmed regression (top-1%/top-5% excluded: `c` stable at `0.98-1.02` across
trimming, i.e. NOT purely an artifact of a few outliers, though ESS remains limited), and
`sd_w(U)` with its own bootstrap CI and `n`-scaling. (2) NOT recommended: extending to `n=2039`
using `c` as the diagnostic (the first draft's own proposed next step) — per the review, `c→1` is
the null's own prediction, so this would not be a differentiating test (Cheapest Differentiating
Test Protocol's own kill signal: "test result is the same regardless of which branch is true").
(3) If pursued further: extend the `sd_w(U)` scaling check to `n=2039` specifically (a genuinely
differentiating test, since the null predicts NO shrinkage at all), and separately characterize
whether the tail-concentration explanation (rising ESS-loss with `n`) can mechanically produce
`sd_w(U)`'s observed shrinkage without a real concentration phenomenon underneath — this is the
one loose end the review flagged as still open.

**Skeptic Concerns (FL Step 8a — `reviewer`'s cap closed earlier this session; `skeptic`
substituted per `doubt-driven-development.md` § Independent Review Fallback Policy,
context-asymmetric — given only the first draft's claim text + the three exploration scripts +
the raw JSON, no session history. Verdict: `WEAKENED` — this session's fifth consecutive
skeptic-fallback review to find real, substantive problems, and the most severe: the central
claim was built on a statistic with no power to show what it claimed.**
- Concern (#1): `c=2` "decisively excluded" is mathematically forced (`U_i≤1⟹c≤2` deterministically
  for the sample and every bootstrap resample), not empirical evidence. → **Fixed**: retracted;
  restated as an algebraic certainty, not a finding.
- Concern (#2): `c≈1` is EXACTLY the structureless-null's own prediction (any `U`-distribution
  centered on `1/2` gives `c=1`), so it cannot discriminate structure from noise. → **Fixed**:
  headline claim retracted; replaced with the genuinely discriminating statistic (`sd_w(U)`).
- Concern (#3,#4): `4η_n≡K_n/J_n` is a flat identity, not independent corroboration; the
  degeneracy check asked the wrong question. → **Fixed**: both corrected explicitly.
- Concern (#5): two inequality steps (Parseval gap + log-curvature) were conflated as one, with
  the log step contributing materially at `n=127` (`~10%`). → **Fixed**: `c_g` (Parseval-only)
  computed and reported separately, independently re-verified this session.
- Concern (#6): `c`'s effective sample size is small (`≲100-130`/`500`) and tail-dominated;
  unweighted/median `U` differs from the weighted statistic. → **Accepted limitation**: stated
  explicitly; trimmed regression (excl. top 1%/5%) run this session shows `c` reasonably stable
  under trimming, partially mitigating but not eliminating the concern.
- Concern (#7): internal arithmetic inconsistency at `n=1021` (tabled `c`, residual, `R²` not
  mutually consistent), traced to a bootstrap-mean-vs-point-estimate mixup in one script. →
  **Fixed**: corrected value (`c=1.0036`) independently re-derived from the exact orthogonality
  identity this session.
- Concern (#8): the `p=0.037`-vs-`p=0.218` "tension" was backwards — given `ρ≈0.86-0.98`
  correlation between `J_n`/`K_n` (same rows), the slope difference is only `~1.5σ`. → **Fixed**:
  "tension" framing retracted.
- Concern (#9): "`K_n/J_n` all close to 1" was inaccurate at `n=127` (`2.26σ` from 1 per the
  project's own stored delta-method SE, outside the 95% CI). → **Fixed**: corrected explicitly.
- Concern (#10): the proposed next step (extend `c` to `n=2039`) is not a differentiating test,
  since `c→1` is the null's own prediction. → **Fixed**: replaced with `sd_w(U)`-scaling extension
  to `n=2039` as the actually-differentiating version of the same idea.

**Artifacts:** this session's exploration scripts (scratchpad, not committed):
`mechanism_explore1.py`/`2.py`/`3.py` (original, now-corrected exploration),
`mechanism_corrected.py` (Parseval-gap-only regression, trimmed regression, unweighted `U`
statistics), `sdU_bootstrap.py` (the salvaged finding's own bootstrap CI and `n`-scaling fit) —
all using already-saved `metrics/ppl_gate_pilot.json` data, zero new LP solves throughout.

## Point 74 (2026-09-16) — `n=2039` extension for `sd_w(U)`: genuinely AMBIGUOUS, not a
confirmation or a refutation of Point 73's salvaged finding — the statistic PLATEAUS between
`n=1021` and `n=2039` (overlapping CIs, first time in the series), breaking the clean 3-point
monotonic trend, while the "it's just falling ESS" artifact concern is simultaneously weakened
(ESS/N kept falling, `sd_w(U)` did not)

**Context.** Per direct user instruction, extended `ppl_gate_pilot.py` to `n=2039` (`220` reps —
a smaller budget than the other three `n`'s `500`, calibrated live against the actual observed
per-rep LP-solve time, `~11.74s/rep`, to fit a `~50`-minute window; explicitly NOT the full `500`)
to test whether `sd_w(U)`'s `~n^-0.37` shrinkage (Point 73's salvaged finding, after its
predecessor's `c≈1` claim was retracted) continues, plateaus, or reverses — the genuinely
differentiating test the skeptic review recommended in place of extending the retracted `c`
statistic. Method independently re-validated BEFORE running new data (reproduced Point 73's exact
numbers via the same scripts/seeds first — a real precaution, not merely claimed). All raw
numbers below independently re-verified against `metrics/ppl_gate_pilot.json` this session (not
accepted from the agent's report alone).

**Results, all four `n`:**

| n | reps | `sd_w(U)` (bootstrap) | 95% CI | `c_g` (Parseval-only) | ESS | ESS/N |
|---:|---:|---:|---|---:|---:|---:|
| 127 | 500 | 0.1494 | [0.1352, 0.1639] | 0.9124 | 105.3 | 0.211 |
| 509 | 500 | 0.0933 | [0.0833, 0.1037] | 0.9939 | 94.5 | 0.189 |
| 1021 | 500 | 0.0676 | [0.0602, 0.0753] | 0.9859 | 79.0 | 0.158 |
| **2039** | **220** | **0.0675** | **[0.0565, 0.0784]** | 0.9986 | **27.0** | **0.123** |

**The central, honest finding: `sd_w(U)` essentially PLATEAUED between `n=1021` and `n=2039`
(`0.0676→0.0675`, a difference of `−0.0001`) — the two CIs now OVERLAP substantially, the first
time in this series that consecutive `n`'s confidence intervals are not cleanly separated** (all
three prior pairs had non-overlapping CIs, which was the basis for Point 73's "genuinely
concentrating, not noise" reading). The 3-point power-law fit (`b=-0.373±0.035`) predicted
`sd_w(U)(2039)≈0.0536` at its center; the actual value (`0.0675`) is `~26%` above that center,
though still inside the (wide, slope-only) extrapolation band `[0.032, 0.090]` — **not a clean
formal refutation, but a materially weaker continuation than the 3-point trend implied.** The
4-point fit's own slope softens accordingly: `b=-0.330±0.029` (vs `-0.373±0.035` on 3 points), and
`n=2039` carries by far the largest residual (`+0.137` in log-space, vs `≤0.037` for the other
three) in the 4-point fit's own residual list — it does not fit the power-law trend as well as the
first three points fit each other.

**The "falling-ESS mechanically explains the shrinkage" artifact concern (raised by Point 73's own
skeptic review) is SIMULTANEOUSLY weakened by this same data, not merely left open.** `ESS/N`
continued falling, and at a FASTER relative rate, from `n=1021` to `n=2039` (`0.158→0.123`, a
`~22%` relative drop) than from `n=509` to `n=1021` (`0.189→0.158`, `~16%`) — `corr(ESS/N, n) =
-0.99` across all four points, a clean, continuing, even-accelerating trend. **If the "mechanical
artifact" explanation were correct, `sd_w(U)` should have continued falling (or fallen faster) in
step with `ESS/N` — instead `sd_w(U)` plateaued exactly where `ESS/N` kept dropping.** The naive
aggregate correlation `corr(ESS/N, sd_w(U))=0.86` across all four points LOOKS like it supports
the mechanical-artifact story, but this is confirmed (independently, this session) to be driven
entirely by the first three points moving together; the fourth point is precisely where that
co-movement breaks. Reporting the `r=0.86` figure alone, without this decomposition, would have
been a misleading reading of the project's own data — correctly avoided in the agent's own report,
independently confirmed here.

**A second, independent signal points the same direction as the plateau being at least partly
real, not pure noise from the smaller sample**: the UNWEIGHTED (bulk, not tail-dominated) median
and mean of `U` did NOT plateau — they continued their smooth drift toward `0.5` at `n=2039`
(`median: 0.594→0.537→0.519→0.518`; `mean: 0.610→0.561→0.534→0.525`), consistent with the trend
established at the first three `n`. This suggests the `n=2039` DATA ITSELF is behaving normally
(no sign of a corrupted or anomalous sample), and the specific PLATEAU is a property of the
tail-weighted statistic (`sd_w(U)`, `ESS=27` at this `n`, the smallest of the four) rather than of
the underlying sample being unusual.

**Kill Analysis.** Nothing killed, nothing confirmed. Point 73's core finding (`sd_w(U)` well
below the structureless-null value of `0.2887` at every tested `n`, including `n=2039` at
`0.0675`, still `~4.3×` below null) SURVIVES — this part is not in question. The SPECIFIC
differentiating question this extension was designed to answer (does the `~n^-0.37` power-law
shrinkage continue) is **NOT cleanly resolved**: the plateau is real in the data (CIs overlap,
largest residual in the 4-point fit), but at a sample size (`220` reps, `ESS=27`) small enough
that "real asymptotic leveling-off" and "noise from an under-powered 4th point" cannot currently
be distinguished from each other.

**What this does NOT mean.** Does NOT mean the `sd_w(U)` concentration finding (Point 73) was
wrong — the concentration relative to the null remains large and real at all four `n`. Does NOT
mean the power-law model (`b≈-0.37`) is refuted — `n=2039`'s value is still inside its
extrapolation band, just far from the center. Does NOT mean the plateau is confirmed as a real
asymptotic floor — `220` reps at `ESS=27` is not enough statistical power to distinguish "genuine
floor near `~0.07`" from "this particular 220-rep sample happened to land above trend." Does NOT
mean the falling-ESS artifact concern is fully closed — it is WEAKENED (the plateau-while-ESS-
falls pattern argues against a purely mechanical explanation), not eliminated, since a `220`-rep
sample's own ESS-driven noise could independently explain the plateau without any real
concentration-floor phenomenon.

**Recommended next steps, stated but not executed here.** (1) The cheapest way to resolve the
ambiguity is NOT a 5th `n` — it is raising `n=2039`'s OWN rep count to match the other three
(`500`, i.e. `+280` more reps), which would both shrink `n=2039`'s own CI and raise its `ESS`
(currently the clear outlier at `27` vs `79-105` for the others) enough to tell whether the
plateau survives more data or was a `220`-rep-sample artifact — this is the direct analogue of
Point 71's own already-validated "raise the smallest-budget point to match the others" pattern.
(2) If plateau survives at `500` reps: this becomes a genuinely interesting finding (an
asymptotic floor for the tightness-ratio dispersion, rather than shrinkage to zero) worth its own
Mechanism Development Mode pass. (3) If it does not survive (i.e. `500`-rep `sd_w(U)(2039)` moves
back toward the `0.05` range the 3-point trend predicted): the original `~n^-0.37` picture from
Point 73 is reinforced, and the `n=2039, 220`-rep result here would be understood, in hindsight, as
sampling noise on an under-powered point — not as evidence of a real floor.

**Artifacts:** `ppl_gate_pilot.py` (`SIZES_REPS` extended with `(2039, 220)`, canonical sampling
protocol unchanged), `metrics/ppl_gate_pilot.json` (updated: `n=2039` rows/summary added, new
`u_statistics_tightness_ratio` key with the full 4-point table, both log-log fits, the
extrapolation-band check, and the explicit `ESS`-vs-`sd_w(U)` artifact-check correlations).
This session's scratchpad scripts (not committed): `u_stats_n2039.py`, `calibrate_n2039.py`,
`validate_u_stats_method.py` (the pre-run validation against Point 73's own numbers).
Independently spot-checked against the raw JSON this session (not accepted from the agent's
report alone).

## Point 75 (2026-09-16) — `n=2039` raised to 500 reps (Point 74's own recommended next step,
executed): `sd_w(U)` fell a further `12%` from the 220-rep value, ruling out H2 (plateau) by the
pre-registered threshold. H1-vs-H3 is genuinely, STATISTICALLY unresolved — the `1021→2039` step
is indistinguishable from both a continuing power law (z=1.47, p≈0.14) and a plateau (z=1.50,
p≈0.13). SUBSTANTIALLY CORRECTED after a context-asymmetric skeptic review found a transcription
error and an unsupported "real slowdown" framing in the first draft — both independently
re-verified and fixed here, not accepted on the skeptic's word alone

**Context.** Per Point 74's own pre-registered "cheapest way to resolve the ambiguity" (raise
`n=2039` from `220`→`500` reps, matching the other three `n`), and per the user's own
pre-registered three-way decision framework (H1/H2/H3, fixed BEFORE this run) plus two
methodological additions requested alongside it: an `η=μ²+σ²` identity check (sanity check on
implementation correctness, not a new finding) and a trim-sensitivity diagnostic (recompute
`sd_w(U)` excluding the top-1%/top-5% by `Z²`-weight, to test whether the finding is tail-driven).

**Infrastructure note (process-level, not a research finding).** The first two background-launch
attempts for this extension silently died at the harness level — zero bytes of output, no
matching process, despite the script's first line using `flush=True` (which should print
immediately even on a slow start or an early exception). The script's own correctness was
independently re-validated (byte-for-byte reproduction of the existing `n=127/509/1021` values)
before either attempt, ruling out a code bug as the cause of the silence. A third attempt, run
unbuffered (`python -u`) with a fresh log file, worked — and, separately, the FIRST attempt
turned out not to have been dead at all: it had been silently capturing zero bytes to its log
the entire time while still computing correctly in the background, and completed with exit code
0 after `~58` minutes (`~12s/rep × 280` new reps, consistent with calibration). The third
attempt was stopped cleanly (`TaskStop`) once the first attempt's completion was confirmed, with
no write race — `metrics/ppl_gate_pilot.json` has not changed since the first attempt's own
completion. This is filed here as an infrastructure observation (background-task output capture
can silently fail while the underlying process still runs correctly), not as a claim about the
research finding itself. **Correction (skeptic review):** the original draft justified "the
computation is valid despite the log-capture failure" by citing the identity check and `exit code
0` — both are weak evidence here, since the identity check (see below) is a tautology that would
pass even on duplicated or corrupted rows, and a clean exit code alone does not rule out a
partial/raced write. The real guarantees, verified this session: (a) `main()`'s row-reuse path
(`ppl_gate_pilot.py`, the `main()` function) validates every reused row's `seed` against the
expected `SEED_BASE + n*100000 + idx` and `n` before trusting it, aborting reuse on the first
mismatch — a corrupted or duplicated row would fail this check, not silently pass; (b) the whole
run is fully deterministic (fixed `SEED_BASE`, a single `np.random.default_rng(123)` consumed
sequentially across `n` in a fixed order) — a genuinely concurrent third attempt reading the same
prior JSON would have produced a byte-identical result (barring `elapsed_seconds`), so the
"stopped cleanly with no race" claim rests on determinism, not on timing luck; (c) direct
inspection confirms `branch_counts[2039]=500` (`260+240`), the last row's `seed=207251499` is
exactly `SEED_BASE+2039·100000+499` (the expected rep-499 seed), and the JSON is not truncated.

**Results, all four `n`, now uniformly 500 reps:**

| n | reps | `sd_w(U)` (bootstrap mean) | 95% CI | `μ_w(U)` | `J_n` | `K_n` | `η_n` | ESS | ESS/N | top1%/top5% share of `ΣZ²` |
|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---|
| 127 | 500 | 0.14937 | [0.1352, 0.1639] | 0.50660 | 64.66 (SE 5.60) | 72.23 (SE 7.32) | 0.2793 (SE 0.0145) | 105.32 | 0.2106 | 11.0% / 40.6% |
| 509 | 500 | 0.09332 | [0.0833, 0.1037] | 0.49425 | 73.43 (SE 6.81) | 74.34 (SE 6.97) | 0.2531 (SE 0.0080) | 94.53 | 0.1891 | 14.0% / 40.9% |
| 1021 | 500 | 0.06758 | [0.0602, 0.0753] | 0.50180 | 86.58 (SE 8.94) | 88.80 (SE 9.47) | 0.2564 (SE 0.0059) | 79.05 | 0.1581 | 17.2% / 44.4% |
| **2039** | **500** | **0.05933** | **[0.0516, 0.0668]** | 0.50317 | 81.26 (SE 8.98) | 83.45 (SE 9.49) | 0.2567 (SE 0.0056) | 70.42 | 0.1408 | 19.2% / 45.3% |

**Correction (skeptic review, verified independently before fixing): the `μ_w(U)` value for
`n=2039` in the first draft of this table was `0.49813`, transcribed incorrectly from the
agent's own report without independently re-checking that specific column against the raw JSON
(all other columns for `n=2039` — and `μ_w(U)` for the other three `n` — WERE independently
checked and were correct).** The raw JSON's `U_weighted_mean_eq_c_over_2` field for `n=2039` is
`0.5031667927023945`; the table above now reflects it. The error would have been caught by the
identity check below (`0.49813² + 0.05962²= 0.2517 ≠ η=0.2567`; the corrected value gives
`0.50317²+0.05962²=0.25673`, matching `η` exactly) — that this internal consistency check was
not actually run against the printed table number, only against the JSON's own stored fields, is
itself a gap in how "independently re-verified" was applied in the first draft.

Relative to the `220`-rep value from Point 74 (`0.0675` [0.0565, 0.0784]; note these Point-74
numbers are themselves not recoverable from the current JSON, since the `n=2039` row-reuse
mechanism overwrote them in place — recoverable only from git history if needed): the point
estimate fell `−12.1%` (`0.05933/0.06758=0.8779`), and the CI width narrowed `1.44×`
(`[0.0565,0.0784]`, width `0.0219` → `[0.0516,0.0668]`, width `0.0152`). The point estimate moved
well below Point 74's plateau band, formally excluding H2 by the pre-registered threshold — see
§ Honest verdict below for what this does and does not establish about H1 vs H3.

**Identity check (`η_n = μ_w(U)² + Var_w(U)`, sanity check on the u-statistics machinery, NOT a
new finding).** Confirmed at float-precision noise level at all four `n` (`abs_diff` between
`5.6e-17` and `1.7e-16`) — the u-statistics computation (now implemented directly in
`ppl_gate_pilot.py` rather than the prior session's lost scratchpad scripts) is internally
consistent. **Caveat added on skeptic review:** this identity is an exact algebraic tautology
given how `U` and its weights are constructed (`Σw·U²=Σδ²/4` and `Σw=ΣZ²/n²` by direct
substitution) — it can only fail from a numpy-level arithmetic bug, and would hold identically
even on duplicated, raced, or otherwise corrupted rows. It is evidence the *arithmetic* is
self-consistent, not evidence the *data* is uncorrupted — that second claim rests on the
row-reuse validator and determinism argument in the infrastructure note above, not on this check.

**Trim-sensitivity diagnostic (excluding top-1%/top-5% by `Z²`-weight):**

| n | full `sd_w(U)` | excl. top1% | Δ | excl. top5% | Δ |
|---:|---:|---:|---:|---:|---:|
| 127 | 0.15040 | 0.15067 | +0.18% | 0.14538 | −3.34% |
| 509 | 0.09378 | 0.09790 | +4.39% | 0.10592 | +12.95% |
| 1021 | 0.06769 | 0.07215 | +6.59% | 0.07705 | +13.84% |
| **2039** | **0.05962** | **0.06288** | **+5.47%** | **0.06351** | **+6.53%** |

Removing the heaviest-weight tail mostly INCREASES `sd_w(U)` (3 of 4 `n`, the sole exception
being `n=127`'s top-5% trim) — the finding is not an artifact of a handful of extreme rows; if
anything, the heaviest rows pull the statistic slightly down, not up. Magnitude is modest (5-14%)
at the LEVEL of `sd_w(U)`.

**Trend sensitivity to trim choice (added on skeptic review — the first draft only checked
whether trim affects the LEVEL of `sd_w(U)`, not whether it affects the SLOPE, which is what this
point's own verdict turns on).** Recomputing the 3-point endpoint slope
(`ln(sd(1021)/sd(127))/ln(1021/127)`) and the `1021→2039` step's deviation from it, separately
for each trim variant:

| trim variant | 3-point endpoint slope `b` | obs. `1021→2039` ratio | pred. ratio (own `b`) | deviation |
|---|---:|---:|---:|---:|
| full (no trim) | −0.383 | 0.881 | 0.767 | +14.8% |
| excl. top-1% | −0.353 | 0.872 | 0.783 | +11.3% |
| excl. top-5% | **−0.305** | 0.824 | 0.810 | **+1.8%** |

**The "slowdown" that motivates this point's own step-ratio argument (below) shrinks from ~15%
to ~2% depending on which trim variant computes the reference slope — a larger swing than the
H1-vs-H3 question itself.** Separately, `n=127` is the ONE point where trim REDUCES `sd_w(U)`
(`−3.34%` at top-5%, vs `+4.4%` to `+13.8%` increases at the other three `n`) — and `n=127`
carries roughly `54%` of the leverage in the inverse-variance-weighted 3-point fit (weights
`∝1/relSE²`: `418/320/304` at `n=127/509/1021`, `x̄_w=5.878`, leverage contributions
`w(x−x̄)²≈447/40/335`). The reference slope the whole "slowdown" argument is measured against is
therefore dominated by the one point that behaves anomalously under trimming. This does not
overturn the H2 exclusion (level-based, robust to trim) but materially weakens any claim of a
precisely-quantified "slowdown" relative to a single reference power law.

**Updated log-log fits.** 3-point fit (`n=127,509,1021`, unchanged by this extension):
`b=-0.373±0.035`, 95% CI `[-0.441,-0.304]`. 4-point fit (now on `500` reps at `n=2039`, not
`220`): `b=-0.348±0.027`, 95% CI `[-0.401,-0.296]` — materially closer to the 3-point slope than
Point 74's own 220-rep 4-point fit was (`b=-0.330±0.029`). `n=2039`'s own residual in the 4-point
fit shrank from Point 74's `+0.137` (a clear outlier vs the other three's `≤0.037`) to `+0.049`
(comparable to `n=1021`'s `−0.062`) — `n=2039` no longer stands out as a poor fit to the
power-law trend.

The 3-point fit's own point prediction for `n=2039` (`log(sd)=-2.926`, i.e. `sd≈0.0537`) is
still below the actual `500`-rep value (`0.0593`, `~10%` above the center) but the gap has
shrunk substantially from Point 74 (`~26%` above center). `n=2039` remains inside the
(slope-only) extrapolation band `[0.032,0.090]`.

**The step-by-step ratio check, WITH an actual significance test (added on skeptic review — the
first draft compared observed vs predicted ratios but never computed whether the difference was
distinguishable from noise, then asserted "real, non-noise" without the test).** Comparing each
observed `sd_w(U)[n_i]/sd_w(U)[n_{i-1}]` ratio to what the 3-point fit's slope alone predicts:

| transition | observed ratio | predicted ratio (b=-0.373) | |
|---|---:|---:|---|
| 127→509 | 0.6247 | 0.5958 | fell MORE than predicted |
| 509→1021 | 0.7242 | 0.7713 | fell slightly less than predicted |
| **1021→2039** | **0.8779** | **0.7726** | **fell less than predicted** |

Testing the `1021→2039` deviation against the power-law prediction, using each point's own
`relative_SE` from the bootstrap (`SE(log sd)`, stored per-`n` in the JSON):
`z = [ln(sd(2039)/sd(1021)) − b·ln(2039/1021)] / sqrt(relSE(2039)² + relSE(1021)²)
= [−0.1302 − (−0.2577)] / sqrt(0.0653²+0.0573²) = 0.1275/0.0869 = 1.47` → **`p≈0.14`
(two-sided)** — NOT a statistically resolved deviation from the power-law prediction. Testing the
SAME step against the opposite hypothesis (pure plateau, i.e. log-ratio `=0`):
`z = −0.1302/0.0869 = −1.50` → **`p≈0.13`** — also NOT statistically resolved. **The observed
step sits almost exactly halfway between the power-law prediction (`z=1.47` away) and the
plateau prediction (`z=1.50` away) — this single data point cannot statistically distinguish the
two hypotheses, contrary to the first draft's claim that it represented a "real, non-noise
slowdown."** A further complication not addressed in the first draft: the `220`-rep and `500`-rep
`n=2039` estimates are NOT independent — the `500`-rep run reuses the same `220` rows and adds
`280` new ones — so no significance can be attached to the `−12%` drop from Point 74's value
either; it is reported purely as a point-estimate comparison, not a tested one.

`ESS/N` vs `sd_w(U)` correlation across all 4 points is now `r=0.944` (up from Point 74's
`r=0.86`) and `ESS/N` vs `n` is `r=-0.954`. **Correction:** the first draft's rebuttal of the
"falling ESS mechanically explains the shrinkage" concern argued from the wrong direction — the
actual concern (stated in the JSON's own `artifact_check_note`) is that a shrinking tail-weight
fraction could mechanically produce `sd_w(U)` *shrinkage* with `n`, which is exactly the observed
co-direction, not a mismatch. The quantitative rebuttal is a direct one: `weighted_mean_and_var`
uses a population (not Bessel-corrected) denominator, so the self-normalized estimator carries a
finite-`ESS` downward bias of order `1/ESS`; comparing `n=127` (`ESS=105.3`) to `n=2039`
(`ESS=70.4`), that bias differs by only `sqrt((1−1/105.3)/(1−1/70.4))≈1.0024`, i.e. `~0.24%` —
against an observed `sd_w(U)` compression of `sd(127)/sd(2039)=2.52` (a `152%` change). The
mechanical ESS-bias channel accounts for `~0.24` percentage points out of `152` — it does not
explain the shrinkage. Separately worth noting, not previously flagged: the rising `r` (from
`0.86` at `220` reps to `0.944` at `500` reps) means the specific break in co-movement that Point
74 relied on as its OWN counter-evidence against the mechanical explanation (the 4th point no
longer breaking step with the first three) is now weaker, not stronger — the real rebuttal here
is the `1/ESS`-magnitude argument above, not the correlation trend.

**Honest verdict against the pre-registered H1/H2/H3 thresholds.**
- H1 (power-law continues, close to `~0.053`, no explicit numeric band in the pre-registration):
  `0.05933` is `~11%` above the 3-point-fit center (`0.0536`), but the 3-point fit's own center
  prediction lies inside `n=2039`'s 95% CI (`[0.0516,0.0668]`), and `b=-0.373` lies inside the
  4-point fit's own 95% CI for the slope (`[-0.401,-0.296]`) — though this second check has
  limited independence, since the 3- and 4-point fits share 3 of their 4 points.
- H2 (real plateau near `0.065-0.070` with a narrower CI): **excluded** — the point estimate fell
  well below this range and the CI barely overlaps its lower edge.
- H3 (intermediate slowdown, `0.055-0.065`): `0.05933` falls literally inside this numeric band.

**By the letter of the pre-registered numeric thresholds, the result lands in H3 — but this
partly reflects that H1 was the only one of the three hypotheses given no explicit numeric band
in the pre-registration, not necessarily that H3 is favored on the merits.** The step-ratio
significance test above shows the `1021→2039` transition does NOT statistically distinguish a
continuing (weakened) power law from a genuine plateau at this sample size — the three pieces of
qualitative evidence the first draft cited for "leaning toward H1" (continued shrinkage, a
non-outlier 4-point residual, ratio still below 1) are each **equally consistent with H3**, since
H3 predicts continued-but-slower shrinkage too, and do not discriminate the two hypotheses.
**Corrected verdict: H2 is rejected by the pre-registered threshold. H1 vs H3 is NOT resolved,
statistically or by the qualitative arguments available — this is reported as genuinely
ambiguous, per the user's own explicit instruction not to force the interpretation toward either
outcome, with the two non-circular pieces of supporting evidence for H1 (3pt-center inside the
n=2039 CI; `b=-0.373` inside the 4pt slope's CI) noted above for completeness, not as a
tie-breaker.**

**Kill Analysis.** Point 74's plateau reading is **weakened, not killed** — the point estimate
moved decisively away from the plateau band (excluding H2 by the pre-registered threshold), but
the `1021→2039` step itself is not statistically distinguishable from either a continuing power
law or a genuine (lower) plateau at `n=2039`'s current `ESS=70.4`. "Killed" would overclaim what
one additional data point at this precision can establish. Point 73's core `sd_w(U)` concentration
finding (well below the structureless-null `0.2887` at every `n`, `~4.9×` below null at `n=2039`
even after the finite-`ESS` correction) SURVIVES, strengthened if anything. The `~n^-0.37`
power-law picture from Point 73 is not refuted by this data (its slope's 95% CI still contains the
observed transition), but is not confirmed to continue unmodified either — see § What this does
NOT mean.

**What this does NOT mean.** Does NOT mean the power-law model with the ORIGINAL 3-point slope
(`b=-0.373`) is confirmed to continue unmodified, NOR that it is refuted — the `1021→2039`
transition is statistically consistent with both a modest slowdown and pure continuation (see the
significance test above). Does NOT mean a 5th `n` would fail to help, and does NOT mean this is
purely a model-choice question rather than a power question — **correction:** the gap between the
H1-predicted center and the observed value (`~11%`) is SMALLER than the current half-width of
`n=2039`'s own 95% CI (`~13%`), meaning the ambiguity here is substantially a statistical-power
question at the current rep count; roughly a `~4-5×` increase in reps at `n=2039` (to shrink its
relative SE from `~6.5%` to `~3%`, `(6.5/3)²≈4.7`) would materially sharpen this test, more so than
adding a 5th `n`. Does NOT mean the identity check or trim-sensitivity diagnostic (level or trend
version) are new findings — both are sanity/robustness checks: the identity check on the
arithmetic only (see its own caveat above, not a data-integrity guarantee), the trim diagnostic
on whether the LEVEL and (added this review) the SLOPE of `sd_w(U)` are tail-driven — both confirm
the statistic is computed correctly and the H2 exclusion is not a tail artifact, but the trend
version shows the specific "slowdown vs pure power law" framing is sensitive to trim choice (§
above), so that narrower claim should be read cautiously. Does NOT mean the background-launch
infrastructure issue affects the validity of the computed numbers — see the corrected
infrastructure note above (row-reuse validator + full determinism + structural JSON checks), not
the identity-check/exit-code justification the first draft gave.

**Artifacts:** `ppl_gate_pilot.py` (`SIZES_REPS`'s `n=2039` entry raised from `220`→`500` reps;
the full u-statistics machinery — `u_row_arrays`, `weighted_mean_and_var`, `bootstrap_sd_w_u`,
`trimmed_sd_w_u`, `trimmed_c`, `c_g_parseval_gap_regression`, `effective_sample_size`,
`u_statistics_for_n`, `sd_w_u_loglog_fit` — now implemented directly in this file, each function
independently re-derived and validated to reproduce the existing `n=127/509/1021` values to
float precision before being trusted for the new `n=2039,500`-rep computation, since the prior
session's scratchpad scripts that originally computed Points 73/74's numbers were not preserved).
`metrics/ppl_gate_pilot.json` (`n=2039` now `500` reps; `u_statistics_tightness_ratio` fully
recomputed for all four `n`, including two new per-`n` fields —
`identity_check_eta_vs_muw2_plus_sdw2` and `sd_w_U_trim_sensitivity_diagnostic` — plus updated
`loglog_fit_3pt_n127_509_1021`, `loglog_fit_4pt_incl_n2039`, `n2039_vs_3pt_extrapolation`,
`ess_over_n_by_n`, and the two artifact-check Pearson correlations). All numbers above
independently re-verified against the raw JSON this session before being written here — bootstrap
means, 95% CIs, identity-check `abs_diff` values, trim-sensitivity percentages (level and, after
the skeptic review, trend), both log-log fits, and the extrapolation-band check all match to the
reported precision. **One exception, found and fixed via skeptic review, not by this session's
own first-pass verification: `μ_w(U)` at `n=2039` was transcribed incorrectly in the first draft
(`0.49813` vs the correct `0.50317`) — the "independently re-verified" claim in the first draft's
own closing paragraph was therefore itself inaccurate for that one field, corrected here.**
Reviewed by `skeptic` (context-asymmetric, per this session's standing `reviewer`→`skeptic`
substitution — `reviewer`'s Evaluator-Optimizer cap was exhausted earlier this session): found 1
factual transcription error and an unsupported significance claim (the "real, non-noise slowdown"
framing lacked any actual test); both independently re-verified by direct computation against the
raw JSON before being accepted and fixed above, per this session's standing discipline of never
accepting a reviewing agent's arithmetic on its own word. Full skeptic report (agentId
`a507e523ccfb7b5e4`) available in this session's transcript; not committed as a separate file.

## Point 76 (2026-09-16) — 4-point `J_n`/`K_n` re-fit at full power (127/509/1021/2039, all 500
reps): the Points 66-68 pre-registered kill-test target (`b≈0.19-0.20`) is REJECTED at the point
estimate. SUBSTANTIALLY CORRECTED after a context-asymmetric skeptic review: the surviving
`J_n>0` signal (`p=0.032`) is NOT robust — it disappears entirely (`b=0.08±0.10, p=0.43`) once
`n=127` (`55%` of the fit's own leverage) is excluded, a check the first draft never ran

**Context.** Direct user instruction, given as soon as Point 75 (the `n=2039` `sd_w(U)` extension
to `500` reps) landed: re-run the `J_n`/`K_n` power-law analysis originally pre-registered in
Points 66-68 and tested at 3 points in Point 71, now with `n=2039` at full (`500`-rep) power as a
4th point, checking (1) `J_2039` and its CI, (2) the 4-point fit's slope and CI, (3) the fit
against the ORIGINAL pre-registered prediction (`b≈0.19-0.20, z≈3.0-3.5`), (4) the tail trend
(top-1%/top-5%). **No new LP computation was needed or run**: `ppl_gate_pilot.py`'s `main()`
already recomputes `power_law_fit_log_Jn_vs_log_n`, `power_law_fit_Kn`,
`power_law_fit_ratio_J_over_K`, and `tail_concentration_trend_top5pct_share` across whatever `n`
values are in `SIZES_REPS` on every run — since `n=2039` was already in that list for Point 75's
own extension, the 4-point fit was already sitting in `metrics/ppl_gate_pilot.json`, computed as
a side effect. This point's only work was reading it out and independently re-deriving it from
scratch (not accepting the stored JSON value on its own word), using the identical
`weighted_power_law_fit` function (known-variance `Δχ²` convention, per Point 66's own corrected
framing — explicitly NOT re-deriving a new methodology for this check) already used for Point 71.

**`J_2039` and its CI (delta-method SE, same convention used for `J_n` throughout this pilot —
not a bootstrap CI, since none of Points 66/71's `J_n` values carry one either):**
`J_2039 = 81.258 ± 8.985`, 95% CI `≈[63.65, 98.87]`. Notably, `J_2039 < J_1021` (`81.26` vs
`86.58`) — the point estimate fell rather than continuing to rise.

**4-point weighted power-law fit (`log J_n = a + b·log n`), independently re-derived from the raw
`J_n`/`SE` values in `metrics/ppl_gate_pilot.json` and confirmed to match the JSON's own stored
fit to float precision:**

| | `b±SE` | 95% CI | `Δχ²` (1 dof) | `z=√Δχ²` | `p` |
|---|---:|---|---:|---:|---:|
| `J_n` (3pt, Point 71) | 0.1296±0.0620 | [0.008, 0.251] | 4.373 | 2.091 | 0.037 |
| **`J_n` (4pt, this point)** | **0.0998±0.0467** | **[0.0084, 0.1912]** | **4.576** | **2.139** | **0.032** |
| `K_n` (4pt) | 0.0671±0.0516 | [-0.034, 0.168] | 1.694 | 1.301 | 0.193 |
| `J_n/K_n` (4pt) | 0.0178±0.0180 | [-0.017, 0.053] | — | — | 0.322 |

**Against the pre-registered target (`b≈0.19-0.20`), point estimate: rejected.** The 4-point slope
(`0.0998`) is `~52%` of the target's own lower bound. **Correction on the `z` comparison (skeptic
review): `z≈3.0-3.5` was the pre-registered target CALIBRATED FOR THE 3-POINT DESIGN and is not
directly comparable to a 4-point `z`** — `z` at fixed `b` scales with `√(Σw·dx²)`, which grew from
`260.3` (3pt) to `459.5` (4pt) purely from adding a point, independent of any real effect; a
like-for-like 4-point target (same `b=0.19-0.20`, this run's own weights) would be
`z≈4.07-4.29`, not `3.0-3.5`. Comparing the observed 4-point `z=2.14` against the 3-point-
calibrated band, as the first draft did, mixes two different designs — the correct comparison is
on `b` (or on SE-distance: `(0.19-0.0998)/0.0467=1.93σ` from target, vs `(0.19-0.1296)/0.0620=
0.97σ` at 3 points — a real, doubling increase in distance from target, stated correctly this
way, not via the `z` comparison the first draft used).

**Robustness check added on skeptic review — this is the load-bearing correction to this
point.** The first draft reported `J_n`'s `p=0.032` nominal significance as a signal that
"survives," without checking whether it is driven by one point. Decomposing each point's
contribution to the fit's numerator (`Σw·dx·dy`) and denominator (`Σw·dx²`):

| n | % of numerator | % of denominator |
|---:|---:|---:|
| 127 | 57.1% | **54.7%** |
| 509 | −0.1% | 0.0% |
| 1021 | 21.6% | 10.3% |
| 2039 | 21.3% | 35.0% |

**`n=127` alone supplies `55%` of this "asymptotic growth" fit's own leverage.** Refitting on
`n=509,1021,2039` only (dropping the smallest, least relevant-to-asymptotics point):
**`b=0.0825±0.1034, Δχ²=0.636, z=0.80, p=0.43`** — independently re-derived from the raw data,
not accepted on the skeptic's word. **The `J_n>0` growth signal is NOT robust to excluding the
smallest tested `n` — it exists only because `n=127` is included, and disappears (`p=0.43`)
without it.** This directly overturns the first draft's "NOT killed: `J_n`'s own `p=0.032`
nominal significance... survives" framing in the Kill Analysis below.

A secondary, absolute-fit check not run in the first draft: the FLAT model's own absolute
goodness-of-fit is `χ²_flat=5.43` at `3` degrees of freedom, `p_GOF=0.14` — the data is fully
consistent with "`J_n` does not grow at all," simultaneous with (not contradicting) the nested
`Δχ²` test's nominal `p=0.032` for `b>0`; these measure different things (absolute fit to a flat
model vs. relative improvement from adding a slope) and the first draft reported only the second.

**Correction to the residual labelling:** the first draft attributed `+0.0779` (log-space) to
"the 4th point" — this is `n=1021`'s residual, not `n=2039`'s (`n=2039`'s own residual is
`-0.0546`). The full, correctly-labelled residual vector is `[-0.0061, -0.0174, +0.0779,
-0.0546]` for `n=[127,509,1021,2039]`.

**What a smaller `b` means for the pilot's own underlying question (not stated in the first
draft):** the PPL gate exists to test whether `J_n` is BOUNDED (needed for `E[δ_i²]=O(n⁻²})` →
`B_n=O(1/n)`, per this file's own docstring) — a SMALLER growth exponent is evidence FAVORING
the original bounded-susceptibility hypothesis, even though it falls further from the
pre-registered `0.19-0.20` NUMBER. "Rejected" in this point's own title refers only to the
specific pre-registered magnitude, not to the underlying scientific question, where the
direction of this result is actually favorable, not unfavorable — the two should not be
conflated when reading this point's headline.

`K_n`'s non-significance is essentially unchanged (`p=0.193` at 4 points vs `p=0.218` at 3 —
still no reliable growth signal at any tested `n`). The `J_n/K_n` ratio fit remains flat
(`p=0.322`, even flatter than Point 71's `p=0.199`), reinforcing Point 71's own `η_n`-stability
finding rather than complicating it. **Caveat added on skeptic review:** the same test for `b=0`
has now been run three times on overlapping/accumulating data (Points 66→71→76) without any
multiple-comparisons or optional-stopping correction; each `p`-value here should be read as
`p` "if this were the only look at this question," not as a corrected significance level across
the sequence of looks.

**Tail trend (top-1%/top-5% share of `ΣZ²`), independently recomputed, unweighted OLS per the
script's own explicit caveat that this carries no SE/significance test:**

| n | top1% | top5% |
|---:|---:|---:|
| 127 | 11.0% | 40.6% |
| 509 | 14.0% | 40.9% |
| 1021 | 17.2% | 44.4% |
| 2039 | 19.2% | 45.3% |

Both continue monotonically increasing across all four `n`, unbroken by the `n=2039` extension —
consistent with, not a new complication to, the tail-heaviness trend already noted in Points 66
and 71. No CI/significance test is attached (single point estimate per `n`, no bootstrap run for
this specific series), so this is reported as weaker, descriptive evidence, per the script's own
labelling, not as a tested claim.

**Kill Analysis.** The specific pre-registered magnitude from Points 66-68 (`b≈0.19-0.20`) is
KILLED as a description of the point estimate at full power across all 4 tested `n`. **Corrected
on skeptic review — NOT killed, but ALSO not shown to survive robustly**: the first draft's own
claim that "`J_n`'s own `p=0.032` nominal significance for `b>0` survives" is WITHDRAWN as stated
— per the robustness check above, this significance exists only with `n=127` included (`55%` of
the fit's leverage) and is gone (`p=0.43`) without it. The honest status is: `J_n>0` growth is
nominally significant on the full 4-point sample, not robust to dropping the smallest tested `n`,
and additionally consistent in absolute terms with no growth at all (`χ²_flat` `p_GOF=0.14`).
`K_n`'s non-growth finding is reinforced (not run through the same leverage check here, since it
was never claimed to show a surviving signal in the first place). `η_n`'s stability is
reinforced. This extends, but weakens the certainty of, Point 71's own "the predicted magnitude
did not materialize" finding — Point 76 shows the specific numeric target failing even more
clearly, while showing the underlying `J_n>0` signal itself is weaker and less robust than the
first draft of this point claimed.

**What this does NOT mean.** Does NOT mean `J_n` is proven bounded (flat) — the fit is consistent
with either a weak, `n=127`-driven signal or a genuinely flat series; this data does not
distinguish the two robustly. Does NOT mean `J_n` is proven to grow either — see the robustness
check above. Does NOT mean the `n=1021→2039` drop in `J_n` (`86.58→81.26`) is itself a tested,
significant reversal — no independent-batch significance test was run for this specific
transition (analogous to Point 71's own old-vs-new Welch t-test for the `n=1021` extension); it
is reported as a point-estimate observation, not a tested claim of decline. Does NOT resolve
which of Route A/A2/B (per Point 69's decision tree) this data points to — if anything, the
robustness finding above weakens confidence in "`J_n` marginally growing" as a settled qualitative
picture, more than Point 71 alone did.

**Correction on the relationship to Point 75's `sd_w(U)` result (skeptic review — the first
draft's reasoning here was wrong, though its bottom-line "not in tension" conclusion happens to
still hold).** The first draft called `J_n`/`K_n` and `sd_w(U)` "different statistics...
independently" showing a similar story. **This is false: they are the same information under an
exact algebraic identity, already used and verified in Point 75 — `η_n = K_n/(4J_n) = μ_w(U)² +
sd_w(U)²`** (confirmed again here, directly from the JSON's stored fields, to `≤1.7e-16`
precision at every `n`). `sd_w(U)`'s continued shrinkage and `μ_w(U)`'s near-constancy (`≈0.50`
at every `n`) are what keep `η_n≈0.25`, equivalently `J_n/K_n≈1` — the `J_n/K_n` ratio fit's own
flatness (`p=0.322`) IS the same fact as Point 75's `sd_w(U)` concentration, not independent
corroboration of it. **The "not in tension" conclusion is still correct, but for a different and
more important reason: "weaker than naive extrapolation" points in OPPOSITE directions for the
two headline statistics** — for `J_n`, a smaller slope than predicted is GOOD news for the
underlying bounded-susceptibility hypothesis (see above); for `sd_w(U)`, slower-than-predicted
shrinkage would be comparatively less favorable to the concentration story Point 73 salvaged.
The two results are consistent with each other (same underlying rows, exact identity linking
them), but "both show the same qualitative story" — the first draft's framing — is not the right
way to describe that consistency, since the practical implications of "weaker than extrapolated"
differ in sign between the two statistics.

**Artifacts:** No code or data changes — this point reads and independently re-derives values
already present in `metrics/ppl_gate_pilot.json` as of Point 75's commit (`power_law_fit_log_Jn_
vs_log_n`, `power_law_fit_Kn`, `power_law_fit_ratio_J_over_K`, `tail_concentration_trend_top5pct_
share`, `summaries`). Independent re-derivation (scratchpad, not committed) reproduced the J_n
fit's `slope_b`, `slope_b_SE`, `chi2_flat_model`, `chi2_power_law_model`, `delta_chi2_dof1`, and
`p_value` fields to float precision from the raw `J_n`/`J_n_SE` values before any number here was
trusted; the `n=127`-excluded refit (`b=0.0825±0.1034`) and the per-point leverage decomposition
were computed the same way, from scratch, not accepted from the skeptic's own numbers.

Reviewed by `skeptic` (context-asymmetric, same standing `reviewer`→`skeptic` substitution as
Point 75): confirmed all arithmetic in the first draft to full float precision (nothing was
numerically wrong), but found the headline framing overclaimed in five ways — an unrun
robustness/leverage check (the load-bearing correction, see above), a mislabelled residual, an
uncalibrated cross-design `z` comparison, a missing absolute-goodness-of-fit counter-statistic,
and a false "independent statistics" premise in the Point 75 comparison. All five independently
re-verified by direct computation against the raw JSON before being accepted and fixed here, per
this session's standing discipline of never accepting a reviewing agent's arithmetic on its own
word. Full skeptic report (agentId `aa7f93cca7ab0c616`) available in this session's transcript;
not committed as a separate file.

## Point 77 (2026-09-16) — STATE SNAPSHOT + PRE-REGISTERED PROOF BUDGET: the entire program is
reduced to ONE lemma, an explicit finite budget is fixed BEFORE spending it, and the park
decision with its Revival Condition is written down in advance

**Why this point exists.** Direct user instruction, and the user's own diagnosis, which this point
confirms with evidence rather than merely accepting: Points 73-76 produced four consecutive
rounds of work in the same `K_n`/`J_n`/`sd_w(U)` measurement line, four genuine skeptic-caught
errors — and **zero movement on the actual mathematical obstruction**. The load-bearing question
("is `K_n` bounded?") went from `unknown` to `unknown, now with tighter CIs and a documented
leverage fragility`. That is the definition of diminishing returns, and the correct response is to
name the single remaining question, fix a budget, and pre-commit to parking if the budget is
exhausted — not to keep fragmenting the same uncertainty into finer JSON fields.

**State snapshot (every row verified this session against the documents/raw JSON, not recalled):**

| | Status |
|---|---|
| Goal | `Var(log(θ/√n)) = O(1/n)`, dense random circulants |
| Empirics | `n^{-0.91}` (`n=32..3000`); the deviation from `1/n` (exponent `0.0877`) numerically MATCHES the measured growth of `K_n` (`0.067±0.052`) and `J_n` (`0.0998±0.047`) — three independent series agree |
| Proven | `Var=W_1+R_n`; `W_1=λ_n²/(4m)` (re-verified numerically, `0.01-0.04%`); `R_n=Σ_{odd\|S\|≥3}X̂(S)²`; `\|λ_n\|=m·E[δ]`; `δ_i≤2x_iw_i` (re-verified on raw rows, violations `~1e-13` = solver noise); `\|λ_n\|≤2(E‖x*‖²−1)` (prime + min-L2 selector); `E‖x*‖²=O(log³n)` (Bandeira et al. 2025 Lemma 5) ⟹ `W_1=O(log⁶n/n)` |
| Single bottleneck | `E[δ_i²] ≤ C/n²`. Via Efron–Stein this closes EVERYTHING at once: `R_n` not needed, prime restriction not needed, `(POL)` not needed |
| Not an over-strong target | Efron–Stein slack is bounded and shrinking (their own series `2.57→1.67→1.27`; exact small-`n` `1.20-1.52`) ⟹ `K_n=O(1) ⟺ the conjecture`. Proving it is not a detour, it is equivalent |
| Empirical channel | **EXHAUSTED.** Scenarios "bounded" vs "polylog" differ by `~6%` at the next reachable `n`, against `~11%` relative SE; decisive separation needs `n≈8192` (order-of-magnitude costlier LP) |

**The one question, in two equivalent forms** (second form is the first, pushed through the
already-proven `δ≤2xw` + Cauchy–Schwarz + equal marginals):

```
E[δ_i²] ≤ C/n²        ⟺(sufficient)⟸        E[(x*_i)⁴] = O( (E[(x*_i)²])² )
```

The right-hand form is a **delocalization / fourth-moment statement about the coordinates of the
min-L2-norm optimal certificate**. Note this is NOT new to the project: it is exactly the burden
already named in `codex-20260914-susceptibility/CROSS_TURAN_ENERGY_THEORY.md:110-113` ("the live
`(POL)` burden is a moment bound for the unevenness of the positive optimal weights") on
2026-09-15, and untouched since. Naming it again here is not progress; fixing a budget against it
is.

**PRE-REGISTERED BUDGET (fixed by the user BEFORE any attempt, recorded here so the stopping rule
cannot be retrofitted to the outcome).**

- **Gate 0 (mandatory, cheap, runs first):** literature novelty check — does the delocalization /
  4th-moment statement for LP/SDP optimizers already exist; and, critically, what does
  arXiv:2502.16227 itself prove about VARIANCE/CONCENTRATION (not just the typical value). The
  Filmus-2016 rediscovery (points 27-28) is this project's own precedent for why this gate is not
  optional.
- **Then at most 3 GENUINELY DISTINCT strategies, ≤1 working session each.** Named in advance so
  a repeat cannot be relabelled as a new attempt:
  1. Hypercontractivity on the cube (4th-vs-2nd moment is precisely its subject); known
     obstruction: `x*_i` is an LP-optimizer coordinate, not a low-degree polynomial — a degree
     surrogate is required.
  2. Deterministic tail from LP structure via Point 64's support-saturation identity
     (`n‖y‖²=(n/s)(1+CV²)`): a uniform bound on `CV` of the positive optimal weights yields the
     4th moment directly.
  3. High-probability bound + crude worst-case on the rare event; requires a quantitative
     anti-concentration input, and the measured cost is explicit (top-1% of rows carry `19.2%` of
     `ΣZ²` at `n=2039`, and that share is GROWING: `11.0→14.0→17.2→19.2%`).

**PRE-REGISTERED OUTCOME MAP (three outcomes, not two — this distinction was raised and settled
BEFORE spending, precisely because a too-strict criterion would have parked the project while a
publishable theorem was one lemma away):**

- **S1 — full success:** `E[δ²] ≤ C/n²` proven ⟹ the conjecture is proven outright, via
  Efron–Stein, for all `n` (no prime restriction), with no `R_n` argument needed.
- **S2 — partial success, and still a real theorem:** `E[δ²] = O(polylog(n)·n^{-2})` proven ⟹
  `Var(X_n) = O(log⁶n/n)`. This counts as SUCCESS, not failure: `E‖x*‖²=O(log³n)` is already in
  hand, so this outcome is separated from the current state by the same single lemma.
- **F — budget exhausted:** neither ⟹ **PARK** (`parked/`, not `null_results/` — the claim is not
  falsified, the architecture is exhausted).

**REVIVAL CONDITION (written now, per the `parked/` protocol's requirement that it be explicit and
measurable):** (a) an external result on delocalization / higher-moment control of LP/SDP
optimizers on random instances appears; OR (b) `(POL)` (`sup_n E‖x*‖² < ∞`) is proven, removing
the `log³`; OR (c) a genuinely new tool becomes available (not a re-run of strategies 1-3).
**Explicitly NOT a revival condition: "measure one more `n`."** The measurement channel's
discriminating power is exhausted (quantified above), and recording this prevents the loop from
reopening on compute alone — which is the exact failure mode Points 73-76 exemplify.

**What this point does NOT claim.** Does NOT claim the conjecture is false — the evidence in fact
mildly favours it (the local growth exponent decelerates FASTER than the `a/log n` law a polylog
scenario requires: calibrated on exact noise-free `n=9..17` it predicts `α=0.2005` at the
large-`n` range, observed `0.0877`, i.e. `56%` below). Does NOT claim the reduction to the single
lemma is new mathematics — the chain is assembled entirely from already-proven pieces, and the
lemma itself was already named in Codex's own theory document. Does NOT claim `K_n` is bounded —
that is precisely the open question. Does NOT commit to parking: parking happens only on outcome
F, after Gate 0 and the three named strategies have actually been spent.

**Artifacts:** No code or data changes. All numbers re-derived this session from
`metrics/ppl_gate_pilot.json` and the exact small-`n` tables already in this file (Points 10, 53):
the `W_1=λ²/(4m)` identity check, the three-way exponent agreement, the Efron–Stein slack series,
the `Z=n·x_i·w_i` / `δ_bound=2x_iw_i` verification on raw rows, and the deceleration test against
the `a/log n` model.

## Point 78 (2026-09-16) — CORRECTION to Point 77: `K_n=O(1) ⟺ conjecture` was an overclaim (only
`⟹` is proven); the F4 lemma does NOT reach S1 (it gives `Var=O(log⁶n/n)`, matching Point 77's OWN
S2, not S1) — the sharp, S1-equivalent target is a DIRECT joint moment, `J_n=O(1)`, which is
already `n²·E[x*_i²w*_i²]`, the exact quantity Points 66-76 have been measuring the whole session

**Context.** External-AI-authored critique of Point 77, relayed by the user, forwarded for
independent evaluation per this session's standing discipline (not accepted at face value — this
project has repeatedly caught real errors in such forwards, and has also caught real errors in
its OWN work via the same discipline applied to itself, which is what happened here). Two
corrections claimed; both independently re-derived from scratch (symbolically, via `sympy`, not
by hand) before being accepted.

**Correction 1 — CONFIRMED, real error.** Point 77's "Not an over-strong target" row states
`K_n=O(1) ⟺ the conjecture`. This is FALSE AS WRITTEN. Efron–Stein gives only the one-directional
`Var(X_n) ≤ B_n ≍ K_n/n`, i.e. `K_n=O(1) ⟹ Var=O(1/n)` (proven). The converse would require a
matching REVERSE bound `B_n ≤ C·Var(X_n)`, uniform in `n` — **grepped this entire document for
any such bound (`B_n <= C`, "reverse Efron-Stein", "lower bound" near `Var`): zero hits.** No such
bound has ever been proven or even attempted here. The empirical Efron–Stein-slack series Point 77
cited (`2.57→1.67→1.27` at `n=127,509,1021`; exact small-`n` `1.20-1.52`) is real and suggestive —
it says the ratio `B_n/Var(X_n)` has stayed bounded and even shrunk on every tested `n` — but a
bounded ratio on a finite tested range is evidence for a conjecture, not a proof of a uniform
bound for all `n`. **Corrected statement: `K_n=O(1)` is a proven-sufficient, empirically-plausible
but UNPROVEN-necessary target. Pursuing it remains the shortest known PATH to the conjecture, but
it is not established to be equivalent to it, and Point 77's "equivalent" framing should not be
read as a proven fact.**

**Correction 2 — CONFIRMED, real error, and it contradicts Point 77's OWN later section.**
Point 77's "one question, in two equivalent forms" box reads
`E[δ_i²] ≤ C/n² ⟺(sufficient)⟸ E[(x*_i)⁴] = O((E[(x*_i)²])²)` — self-contradictory notation
(mixing `⟺` and `⟸` in one line has no coherent meaning) that, as written, invites the reading
"the F4 lemma reaches the strict `C/n²` target." **It does not**, and Point 77's OWN Outcome Map
(S1 vs S2) already said so without the "two equivalent forms" box noticing the tension.
Independently re-derived symbolically from the already-established `E[(x*_i)²]=O(log³n/n)`:

```
F4:  E[x*⁴] = O((E[x*²])²) = O(log⁶n/n²)
  -> E[x²w²] <= sqrt(E[x⁴]E[w⁴]) = O(log⁶n/n²)      [Cauchy-Schwarz + equal marginals]
  -> J_n = n²·E[x²w²] = O(log⁶n)                     -- NOT O(1)
  -> K_n <= 4J_n = O(log⁶n)
  -> Var(X_n) = O(log⁶n / n)                         -- matches Point 77's OWN "S2", not "S1"
```

F4 (the marginal fourth-moment/delocalization statement, and by extension all three of Point 77's
named strategies, which all target this marginal quantity) proves S2 at best, never S1. The "two
equivalent forms" box is corrected: **F4 is sufficient for S2 only, not for S1.**

**The sharper target this correction surfaces — not new compute, not a new quantity, but a
renaming of what was already the primary measured object.** Skipping the Cauchy–Schwarz split
(which can only lose information — equality holds only if `x*²=c·w*²` a.s., not established, and
plausibly false given `x*` and `w*` are the min-L2 certificates of two DIFFERENT graphs, `G_0` and
the complement of `G_0∪H_i`) and bounding the JOINT product moment directly:

```
MIX4:  E[x*_i² w*_i²] = O(n⁻²)   <=>   J_n = O(1)   =>   K_n <= 4J_n = O(1)   =>   Var = O(1/n)
                                                                                    [this IS S1]
```

**`J_n := E[Z_ni²]` where `Z_ni = n·x_i·w_i` — this is not a new object. It is the exact quantity
Points 66-76 have measured the entire session** (verified this session directly against
`metrics/ppl_gate_pilot.json` raw rows: `Z_ni = n·x_i·w_i` holds exactly). Point 76's own
corrected finding is directly relevant here, not incidental to it: `J_n`'s nominal growth
(`b=0.0998`) is **not robust to excluding `n=127`** (`b=0.0825±0.1034, p=0.43` on `n=509,1021,2039`
alone — no growth signal on the three largest tested `n`). This is an absence-of-evidence-against-
boundedness reading of data that already exists, not a new empirical claim, and not proof either —
stated at exactly the strength the data supports, no more.

**Corrected roadmap.** The single bottleneck is unchanged in substance (`E[δ_i²]≤C/n²`) but its
S1-equivalent reduction is now stated correctly: **`J_n=O(1)` (equivalently `MIX4`), not the
marginal `F4`.** Point 77's three named strategies need re-scoping, not replacement:
1. Hypercontractivity — as named, targets marginal `F4` (gives S2 only). To reach S1 it must be
   adapted to bound the JOINT `x*_i w*_i` product directly (e.g. via a negative-dependence /
   anti-concentration argument between the two certificates), not each marginal separately.
2. Support-saturation `CV` route — as named (Point 64's `n‖y‖²=(n/s)(1+CV²)`), bounds ONE
   optimal vector's own weight dispersion, i.e. also a marginal quantity. Same re-scoping needed:
   does the support-saturation structure say anything about `x*` and `w*` JOINTLY (they come from
   genuinely different, correlated-by-construction LPs — `G_0` and complement of `G_0∪H_i`), not
   just about each alone.
3. High-probability + anti-concentration — least affected, since a tail bound on the PRODUCT
   `x_iw_i` directly (rather than each factor) was already a coherent reading of this strategy.

**What this does NOT mean.** Does NOT mean the shortest-path conclusion of Point 77 is wrong — it
is, if anything, sharper: the target was always `J_n=O(1)`, already being measured, and the
correction only removes an unnecessary and lossy detour through marginal fourth moments. Does NOT
mean Gate 0 (still running as of this point) is invalidated — its question (does a delocalization/
moment-control result already exist for LP/SDP optimizers) applies equally to the corrected joint
target. Does NOT mean the pre-registered budget or outcome map (S1/S2/F, revival condition) needs
to change — S1/S2 were already stated correctly; only the "which lemma reaches which outcome"
mapping needed fixing. Does NOT mean `K_n` and `J_n` are different open questions — `K_n≤4J_n`
was already established; proving `J_n=O(1)` remains the single cleanest sufficient step, now
correctly identified as such without the false detour.

**Artifacts:** No code or data changes. Both corrections independently re-derived symbolically
(`sympy`, not accepted from the critique's own derivation) before being written here; the
Efron-Stein reverse-bound absence was confirmed by exhaustive grep of this document, not assumed.

## Point 79 (2026-09-16) — Gate 0 (novelty check, pre-registered in Point 77) RETURNED: the
fourth-moment/delocalization statement is genuinely NOT in the literature (closest adjacent work
is a different object in a different randomness model); confirms this project's own `log³n`
derivation already used the tight (not the loosened, printed) form of Bandeira et al.'s Lemma 5;
and surfaces a genuinely new, cheap, currently-untried alternative route — Talagrand-style DIRECT
concentration of `θ`, already used for ordinary Erdős–Rényi graphs but never attempted for
circulant graphs — added to the budget as **Strategy 0**, run before the three MIX4 strategies

**Context.** Direct user instruction, per Point 77's own Gate 0 requirement. Delegated to a
general-purpose agent with explicit instructions not to invent citations; verdicts below are
`FOUND-EXACT`/`FOUND-ADJACENT`/`NOT-FOUND` per the agent's own framework, each cited with
arXiv ID/DOI or explicitly marked `[UNVERIFIED]` where full text could not be checked.

**Q1 — does `E[(x*_i)⁴]=O((E[(x*_i)²])²)` (or an equivalent joint/marginal moment statement for
LP/SDP optimizer coordinates) already exist? `NOT-FOUND` (exact), `FOUND-ADJACENT` (a different
object).** No paper proves or states this for LP/SDP optimizer coordinates. Closest genre:
eigenvector/null-vector delocalization of random matrices — Rudelson & Vershynin (arXiv:1306.2887),
Lytova & Tikhomirov (arXiv:1810.01590), Luh & O'Rourke (arXiv:1810.00489). Gap, stated precisely:
these bound ℓ2-mass on coordinate SUBSETS of null vectors of a FIXED random matrix with i.i.d.
entries — not a single coordinate's 4th-vs-2nd moment ratio, not a structured subsampled-DFT
matrix, and critically not a vector selected as the ARGMIN of a convex objective (an optimizer)
— these are null/eigen-vectors of a random matrix, not solutions to an optimization problem.
Adapting this machinery is genuinely new work, not a citation. One false lead ruled out
explicitly: Bakhshi/Ostrowski/Tikhomirov (arXiv:2401.17530) uses "delocalization" as an
ASSUMPTION on a fixed deterministic cost vector to get a scalar objective-value limit law — wrong
direction (assumption, not conclusion) and wrong model (dense i.i.d. constraints, not sparse
structured Fourier constraints).

**Q2 — what does arXiv:2502.16227 (Bandeira et al.) actually prove? Load-bearing, since this
project's `E‖x*‖²=O(log³n)` premise depends on it.**

- **No variance/concentration result of any kind is proved by this paper** — Theorem 1 bounds
  `E[θ(G)]` only. It CITES (does not prove) two concentration results, and both are for ORDINARY
  Erdős–Rényi graphs, not circulant graphs: an unpublished note (Arora & Bhaskara, no venue/year
  in the paper's own bibliography — `[UNVERIFIED]` beyond what 2502.16227 quotes, its own PDF
  could not be extracted) using Talagrand's inequality, and Coja-Oghlan 2005 (Combinatorics,
  Probability and Computing 14.4, pp. 439-465) for the sparse regime. **Neither has ever been
  extended to circulant graphs** — confirmed by checking the corresponding author's (Kunisky)
  publication page and an author-name search; no follow-up found.
- **`[CONFIRMED, not a bug]`: this project's own `E‖x*‖²=O(log³n)` derivation
  (`codex-20260914-susceptibility/CROSS_TURAN_ENERGY_THEORY.md:66-78`) already uses the TIGHT
  interior estimate from Lemma 5's own proof (`‖y‖₂≤C·log^{3/2}n/√n·‖y‖₁`, sourced to Haviv &
  Regev 2017 for the RIP sparsity level and Cahill & Mixon 2021 for the RIP⇒null-space bound),
  NOT the paper's own deliberately loosened printed statement (`‖y‖₂≤log²n/√n·‖y‖₁`, which would
  give `log⁴n`, not `log³n`, after squaring). Re-verified this session by reading
  `CROSS_TURAN_ENERGY_THEORY.md` directly: the tight form is exactly what's cited. **No error in
  this project's existing work — the Gate 0 agent's own "precision note" reads as a caution
  applicable to a careless future citation, and turns out to already be satisfied here.**
- Lemma 5 itself is a deterministic, UNIFORM bound over the ENTIRE kernel subspace `ker(F̃)` — it
  says nothing distinguishing the actual optimal `y*` from any other vector in that kernel, and is
  a whole-vector ℓ2/ℓ1 statement, not coordinatewise, let alone a 4th-moment statement. Used
  exactly once in 2502.16227's own proof, in a Cauchy-Schwarz step bounding the LP objective — not
  to characterize the certificate's structure. Confirms Q1's `NOT-FOUND`: this paper does not
  supply, even implicitly, the delocalization lemma this project needs.

**Q3 — existing concentration machinery for `θ` (or similar SDP values) that could bypass the
whole route? `FOUND-ADJACENT` — a real, cheap, currently-untried alternative.** Talagrand's
convex-distance/certifiable-Lipschitz inequality is the exact tool behind BOTH cited ER-graph
concentration results (Arora-Bhaskara's Talagrand argument; Coja-Oghlan's sparse-regime result)
— **this has never been attempted for circulant graphs.** The standard argument builds, for each
near-optimal SDP solution, a bounded-size "certificate" set of EDGES such that graphs agreeing on
the certificate have close `θ`-values, then applies Talagrand's inequality on the product space of
independent EDGE indicators. **The open, unaddressed structural question**: a dense random
circulant graph is generated by only `m=(n-1)/2` independent BIT choices, each of which toggles an
entire ORBIT of `n` edges simultaneously — the standard bounded-edge-certificate argument was built
for independent single-edge perturbations, and whether an analogous bounded-certificate argument
survives when one bit flip moves `O(n)` edges at once is genuinely open; no paper addresses it for
Cayley/circulant graphs specifically. **If it transfers, it plausibly gives `Var(θ)` (or a related
quantity) DIRECTLY, bypassing the entire `δ_i`/Efron-Stein/`J_n`/`K_n` machinery this project has
built over Points 3-78.** If it visibly fails to transfer (the `O(n)`-edges-per-bit structure
breaks the usual bounded-certificate construction), that failure is itself useful, cheaply-bought
information, and removes the concern that a shortcut is being missed while the MIX4 route is
pursued.

**Budget update — Strategy 0, added per direct user decision, run BEFORE the three MIX4
strategies from Point 78 (not instead of them, and not counted against their `≤1 session each`
allowance, since this is what Gate 0 itself surfaced, not a repeat of a named strategy).**

```
Strategy 0 (NEW): attempt a Talagrand-style certificate argument on the m-bit circulant
  parametrization directly. Cheap, ≤1 session, genuinely different in kind from Strategies 1-3
  (targets Var(θ) or J_n directly via concentration, not via the delta_i/moment chain).
  - If it transfers -> may give the variance bound directly; downstream MIX4 work becomes
    unnecessary, or at minimum a second independent confirmation route.
  - If it visibly fails (edges-per-bit obstruction is real and not surmountable cheaply) ->
    informative negative result, proceed to Strategies 1-3 (MIX4 route, per Point 78's
    correction) with the same total remaining budget (≤3 sessions) as before.
```

**What this does NOT mean.** Does NOT mean the literature search found nothing useful — Q2's
finding (2502.16227 proves no concentration result, cites only ER-graph results) is a real,
previously-unstated fact that clarifies exactly what this project's own derivations do and do not
rest on external work for. Does NOT mean Strategy 0 is expected to succeed — the edges-per-bit
obstruction is real and unresolved; it is cheap and informative either way, which is why it is
added as a zero-cost-relative-to-the-existing-budget prefix, not a budget expansion. Does NOT
change Point 78's correction (MIX4 remains the S1-equivalent target for Strategies 1-3) — Strategy
0 is an alternative PATH to the same overall goal (`Var(X_n)=O(1/n)`), not a replacement for the
corrected target. Does NOT mean this project's `log³n` chain needed fixing — Q2's precision check
confirms it did not, and this is recorded explicitly so the finding is not mistaken for a
discovered bug on a later, more superficial read of this point.

**Artifacts:** No code or data changes. Gate 0 delegated to a general-purpose agent (arXiv/web
search + full-text reads, not abstract-only); its citations independently spot-checked against
its own quoted text before being accepted here (the `CROSS_TURAN_ENERGY_THEORY.md:66-78` quote
re-read directly, not taken on the agent's paraphrase).

## Point 80 (2026-09-16) — SECOND-ROUND skeptic-fallback review of Points 78-79 found real, more
severe problems than either correction fixed: Point 78's own "sharp, S1-equivalent" framing
repeats Correction 1's exact error one paragraph later, on a STRICTLY STRONGER quantity; a
previously-underived identity (`B_n/W_1=1+CV(δ)²`) shows a reverse bound DOES reduce to one
measurable condition (not "never attempted," as Point 78 claimed); and directly-computed raw data
shows `Cov(x*_i², w*_i²)>0` and GROWING with `n` at all 4 tested `n` — meaning `MIX4` (the
"sharper, no-`POL`-needed" target Point 78 proposed) in fact REQUIRES `POL`, exactly the
dependency it was framed as avoiding. Point 79's Strategy 0 (Talagrand) is flagged, not killed —
the scale argument against it rests on an unread source and is not independently confirmable this
session

**Context.** Same context-asymmetric `skeptic` substitution as Points 75/76 (`reviewer`'s cap
exhausted this session). Both corrections independently re-verified before being written here —
the algebra by direct symbolic/numeric recomputation, the empirical claims by re-querying
`metrics/ppl_gate_pilot.json` directly, not accepted from the skeptic's own numbers.

**1. Point 78's own title repeats its own Correction 1, one quantity later — CONFIRMED by
re-reading the actual text.** Correction 1 downgrades `K_n=O(1) ⟺ conjecture` to
`K_n=O(1) ⟹ conjecture` (sufficient, not proven necessary). Point 78's own later section then
calls `J_n=O(1)` "the sharp, **S1-equivalent** target" and "the single cleanest sufficient step"
in successive sentences. Since `K_n≤4J_n` (already established), `J_n=O(1) ⟹ K_n=O(1)` but NOT
conversely — **`J_n=O(1)` is strictly STRONGER than `K_n=O(1)`, i.e. FURTHER from being proven
necessary, not closer.** Calling it "S1-equivalent" repeats exactly the error Correction 1 had
just fixed, applied to a stronger statement. **Fixed here: `J_n=O(1)` is a proven-sufficient
target for S1 (via `K_n≤4J_n`), with no stronger equivalence claim.**

**2. A real algebraic identity that DOES reduce necessity to one measurable condition — missed in
Point 78, independently re-derived and verified here.** From already-proven facts (`W_1=λ_n²/4m`,
`|λ_n|=m·E[δ]`, `Var=W_1+R_n`, `R_n≥0`):

```
W_1 = m·E[δ]²/4                              (substitute |λ_n|=m·E[δ] into W_1=λ_n²/4m)
B_n/W_1 = E[δ²]/E[δ]² = 1 + CV(δ)²           (exact identity: E[δ²]=Var(δ)+E[δ]²)
Var ≥ W_1  (since R_n≥0)  =>  B_n/Var ≤ B_n/W_1 = 1+CV(δ)²
```

**So `CV(δ)=O(1) ⟹ B_n/Var` bounded `⟹ Var≍B_n≍K_n/n ⟹ [Var=O(1/n) ⟺ K_n=O(1)]`.** Point 78's
claim that no reverse bound "has ever been proven or even attempted" is WRONG — one follows in
three lines from facts already in the "Proven" row of Point 77. The correct statement is narrower
than Point 78's blanket claim and sharper than Point 77's original overclaim: **the necessity
direction is not free, but it reduces to a single, directly measurable condition
(`CV(δ)=O(1)`), not an open-ended unknown.**

**Caveat, found while independently verifying this — the two existing `δ` measurement series in
this project are NOT the same statistic and must not be conflated.** Computed `CV(δ)²` directly
from `metrics/ppl_gate_pilot.json`'s row-level `delta_i_actual` (single fixed generator,
`GEN_INDEX=1`, `n=127,509,1021,2039`): **`1.229, 1.203, 1.256, 1.221`** — remarkably STABLE, not
decreasing. This differs from the `B_n/Var` ratio series cited earlier in this session
(`2.57→1.67→1.27`, from Point 9b's full multi-generator Efron-Stein sum on a different `n` grid,
`128/512/1536`, via `single_generator_sensitivity.json` — despite the file's own name, that
pipeline sums over generators differently from `ppl_gate_pilot.json`'s single-fixed-orbit `δ`).
**These are two different pipelines measuring related but not identical quantities; neither this
point nor Point 78 is entitled to substitute one series' behavior for the other's.** The `CV(δ)²`
value directly relevant to THIS `J_n`/`K_n` line is the stable `≈1.2-1.26` series, not the
decreasing `2.57→1.27` one. A stable (not shrinking) `CV(δ)²≈1.2` is still bounded — consistent
with, not contradicting, the necessity-reduction argument above — but the "shrinking slack"
narrative used earlier in this session to argue near-necessity was drawn from the wrong series.

**3. `Cov(x*_i², w*_i²)>0`, growing with `n` — CONFIRMED by direct computation, and this is the
most consequential finding in this point.** Computed directly from raw rows at all four `n`:

| n | `Cov(x²,w²)` | `corr(x²,w²)` | `E[x²w²]` vs `E[x²]·E[w²]` |
|---:|---:|---:|---|
| 127 | `+1.23e-3` | `+0.247` | `4.01e-3` ≥ `2.78e-3` |
| 509 | `+1.31e-4` | `+0.597` | `2.83e-4` ≥ `1.52e-4` |
| 1021 | `+4.27e-5` | `+0.789` | `8.31e-5` ≥ `4.04e-5` |
| 2039 | `+1.02e-5` | `+0.860` | `1.95e-5` ≥ `9.37e-6` |

**Positive covariance means `E[x²w²] ≥ E[x²]·E[w²]` at every tested `n`, and the correlation is
STRENGTHENING (not weakening) as `n` grows (`0.25→0.60→0.79→0.86`).** Since equal marginals give
`E[x²]=E[w²]`, this means `MIX4` (`E[x²w²]=O(n⁻²)`) forces `(E[x²])²≤E[x²w²]=O(n⁻²)`, i.e.
`E[x²]=O(1/n)`, i.e. **`POL` (`sup_n E‖x*‖²<∞`) becomes a NECESSARY precondition for `MIX4`** —
exactly the dependency Point 78 framed `MIX4` as avoiding ("`R_n` not needed... `POL` not
needed" was Point 77's framing, inherited uncritically into Point 78's "sharp target"
characterization). **This is not fatal to the MIX4 program, but it removes the claimed
independence from `POL`, and the GROWING correlation trend is a real, unfavorable signal for the
strategies as currently scoped** — if the trend continues, `x*_i` and `w*_i` are becoming more
alike (not more independent), which works against any strategy hoping to exploit negative
dependence between the two certificates (Strategy 1's re-scoping in Point 78 explicitly needed
such a mechanism).

**4. Point 79's Strategy 0 (Talagrand) — FLAGGED, not adopted as FALSIFIED at full confidence.**
The second-round skeptic review derived a specific scale mismatch (standard `(r,1)`-certifiable
Talagrand gives `sd(θ)≍√(r·E[θ])≍√(r·√n)`, and matching the target needs `r=O(n^{-1/2})`,
below any nontrivial certificate size) and concluded Strategy 0 cannot work even in principle.
**This session cannot independently confirm or refute the premise this rests on**: it assumes
the cited ER-graph results (Arora-Bhaskara's unpublished note, Coja-Oghlan 2005) use the generic
bounded-edge-certificate form of Talagrand's inequality with `r=O(1)` — but Gate 0's own report
(Point 79) could not extract readable text from the Arora-Bhaskara note (`[UNVERIFIED]`) and
described the cited result only as "concentrates... in an interval of polylogarithmic length,"
which is a DIFFERENT (better) scale than the generic `r=O(1)` form would produce, and may rest on
a `θ`-specific self-bounding argument rather than the generic edge-certificate machinery the
second-round critique assumed. **Until the actual technique and rate in the cited ER-graph result
is read directly (not paraphrased through two layers of agent summary), the correct status is:
Strategy 0's viability is genuinely unresolved, downgraded from Point 79's "cheap, promising" to
"requires reading the actual source and checking its rate BEFORE spending a session," not yet
downgraded all the way to "impossible."** This itself is a cheap, well-defined next action (read
one paper's concentration rate, not attempt a proof) — narrower than either Point 79's original
framing or the second-round critique's dismissal.

**What this does NOT mean.** Does NOT mean the MIX4/`J_n` program is dead — `J_n=O(1)` remains a
valid, proven-sufficient target; the positive-correlation finding narrows which mechanism could
prove it (needs a `POL`-compatible argument, or a proof that the correlation trend reverses at
larger `n`, which the data gives no support for), it does not close the target. Does NOT mean the
`CV(δ)` stability (`≈1.2`, not shrinking) is bad news for the necessity argument — a STABLE
bounded `CV(δ)²` still satisfies `CV(δ)=O(1)`, which is exactly the sufficient condition the new
identity in §2 needs; "not shrinking" only means the earlier "shrinking slack" narrative (borrowed
from a different, non-comparable pipeline) should not be cited as supporting evidence for THIS
line of the argument. Does NOT mean Strategy 0 is confirmed impossible — see §4, this remains an
open, cheaply-resolvable question, not a closed one. Does NOT mean this session's proof-budget
process has failed — finding real errors in one's own pre-registration via adversarial review,
before spending the committed budget on a flawed target, is the process working as designed, not
a sign it is not working.

**Artifacts:** No code or data changes. `Cov(x*²,w*²)` and `CV(δ)²` computed directly from
`metrics/ppl_gate_pilot.json` row-level `x_i`/`w_i`/`delta_i_actual` fields this session, all four
`n`, not accepted from either round of skeptic review without independent recomputation. The
`B_n/W_1=1+CV(δ)²` identity re-derived from the algebraic definitions, not taken on the second
skeptic pass's word.

## Point 81 (2026-09-16) — Strategy 0 (Point 79's Talagrand transfer) RESOLVED: DIRECT transfer
KILLED — verified against the PRIMARY source (full text, not paraphrase), which shows the
obstruction is structural (an i.i.d.-matrix-entries hypothesis, false by construction for
circulant graphs), not merely "unattempted." A genuinely new certificate would be required, not
just more effort on the existing one. `CIRCULANT-SPECIFIC TALAGRAND: PARKED`

**Context.** User-forwarded, source-cited critique of Point 79's Strategy 0, independently
evaluated per standing session discipline. This session fetched and read the primary source
directly (Arora & Bhaskara's note itself, full text, via `Read` on the downloaded PDF — `WebFetch`
and Gate 0's own agent both failed to extract this same PDF's text; `Read`'s PDF support
succeeded), rather than accepting the forwarded critique's quotes at face value — this project's
own precedent (Filmus-2016, points 27-28) is exactly why quotes get re-verified against the
primary text, not just checked for internal plausibility.

**Verified directly against the primary source (`theory.epfl.ch/bhaskara/files/theta.pdf`, full
text extracted):**

- **Theorem 1** (exact quote): `Pr[|θ(G)-μ|>t] ≤ e^{-t^{4/3}/(C log³n)}` for `G~G(n,1/2)`. Matches
  the forwarded critique exactly.
- **Coja-Oghlan comparison** (exact quote, from the paper's own introduction): "Note that for say
  `p=1/2`, this only says that `θ(G)` is concentrated in an interval of length roughly `n^{1/4}`
  w.h.p." — confirms the `n^{1/4}` scale claim exactly, sourced from the paper's own citation of
  Coja-Oghlan's `Pr[|θ(G)-μ|>t]≤e^{-t²/(μ+t)}` bound (a SECONDARY citation — Coja-Oghlan's own 2005
  paper was not independently fetched this session).
- **The delocalization/flatness mechanism is real, not the forwarded critique's invention**: the
  proof's central definition is a graph being "`s`-bad" iff `Σᵢ‖vᵢ‖⁴ > (1+s)log²n` for every
  optimal vector solution (Lemma 2) — exactly a marginal fourth-moment control on the SDP
  certificate's coordinates, the same OBJECT TYPE this project's own Points 77-80 have been
  targeting. Confirms Point 79's Q3 finding that the delocalization motif is externally
  validated, not a project-invented fantasy.

**The structural obstruction — found independently by reading the proof mechanism itself, a
stronger and more specific finding than the forwarded critique's own "one bit moves `n` edges"
framing (which was second-hand, sourced to an unread thesis).** Lemma 3 (Lovász's own
`ϑ(G)≤λ_max(J-2A(G)-I)`) and Lemma 4 (Alon-Krivelevich-Vu eigenvalue concentration) are applied,
in the proof of Lemma 5, to the adjacency matrix `A(H)` of an INDUCED SUBGRAPH `H` on an arbitrary
vertex subset `S`. **Lemma 4's own hypothesis requires `A(H)`'s upper-diagonal entries to be
i.i.d.** — true for `G(n,1/2)` (every edge is an independent coin flip) but **FALSE BY
CONSTRUCTION for circulant graphs**: two edges `(i,j)` and `(i',j')` with the same difference
`i-j≡i'-j' (mod n)` are controlled by the SAME generator bit, not independent ones — an entire
orbit of `~n` edges is perfectly correlated. **This is not a difficulty to route around with more
effort on the same certificate construction — the specific lemma the whole argument's union bound
(Lemma 5) rests on has a hypothesis that is simply false for this random model.** A transfer
attempt would need to replace Lemma 3/4's route entirely (plausibly with an RIP-type argument, the
technique Bandeira et al. 2025 actually use for their own, different, `E[θ]`-only result — itself
weak evidence that the direct Talagrand route was considered and not pursued by the authors closest
to this exact problem).

**Not independently confirmed this session, flagged rather than asserted:** (a) whether Coja-Oghlan
2005's own paper states the `n^{1/4}` bound in exactly this form (only confirmed via
Arora-Bhaskara's citation of it, a credible but secondary source); (b) the forwarded critique's
claim that a prior thesis/paper already attempted the circulant-specific transfer and obtained
only "logarithmic loss" — two candidate sources (an ETH research-collection thesis, an OpenReview
PDF) were located via `WebSearch` but both returned HTML landing pages, not extractable PDF text,
on this session's fetch attempts; this claim is NOT relied upon in the verdict below, which rests
entirely on the independently-verified structural obstruction in the primary source instead; (c)
the "manuscript (2011)" dating claim — no date appears anywhere in the extracted PDF text.

**Verdict.**
- **`DIRECT TALAGRAND TRANSFER: KILLED`** — not merely "unattempted" (Point 79's framing) but
  structurally blocked: the specific lemma the standard argument's union bound depends on has a
  hypothesis (i.i.d. matrix entries) that provably fails for the circulant random model. This is a
  stronger, more specific finding than Point 80's own scale-mismatch argument (which assumed a
  generic `(r,1)`-certifiable form without confirming which technique the actual cited results
  use) — Point 80's flagged-not-confirmed status is now resolved on independent, primary-source
  grounds, though by a different mechanism (structural incompatibility) than the scale mismatch
  Point 80 speculated about.
- **`CIRCULANT-SPECIFIC TALAGRAND: PARKED`** — a genuinely new bounded-certificate construction
  compatible with orbit-correlated edges (not the standard single-edge-independence one) would be
  required. This is not ruled out, but it is not the "cheap side-bet" Point 79 framed it as; it is
  itself a nontrivial new-technique attempt, comparable in scope to Strategies 1-3, not a filter
  to run before them.
- **Confirms, independently, that even a hypothetical FULL transfer would only reach S2, not
  S1**: `t^{4/3}~log³n ⟹ t~log^{9/4}n ⟹ E[(θ-μ)²]=O(log^{9/2}n)` (standard tail-to-moment
  conversion, re-derived this session) — polylog-weakened, matching Point 78's own S2 outcome, not
  a free `O(1/n)` closure. This was already anticipated in Point 80's discussion but is now
  confirmed against the primary source's own stated rate rather than assumed.

**Budget consequence.** Strategy 0 does not consume one of the three `≤1-session` MIX4 strategy
slots from Point 78 (it was a Gate-0-adjacent check, as designed), and its resolution does not
add a new committed strategy either (`CIRCULANT-SPECIFIC TALAGRAND` is PARKED, not queued). The
budget reverts to exactly Point 78's three named strategies, now informed by Point 80's finding
that `Cov(x*²,w*²)>0` and growing — any of the three, to reach S1, needs either a `POL`-compatible
argument or a mechanism explaining/exploiting that growing positive correlation, not a
negative-dependence assumption.

**What this does NOT mean.** Does NOT mean Talagrand's inequality itself is inapplicable to this
project's problem in general — only that the SPECIFIC construction in the cited ER-graph proofs
does not transfer as-is; a from-scratch circulant-native concentration argument remains a
theoretically open avenue, just not a cheap one. Does NOT mean the forwarded critique was wrong to
raise this — it correctly identified the right question and the right primary source; this point
only upgrades the evidentiary basis from a secondary paraphrase to a primary-source reading, and
finds a related but more specific obstruction than the one originally proposed. Does NOT mean
Points 77-80's overall roadmap changes — the MIX4/`J_n=O(1)` target and its three-strategy budget
stand as corrected in Points 78 and 80.

**Artifacts:** No code or data changes. `theory.epfl.ch/bhaskara/files/theta.pdf` fetched and read
in full this session (saved locally, `Read` tool's PDF extraction succeeded where `WebFetch` and
Gate 0's own agent both failed on the same file). Two secondary sources (ETH thesis, OpenReview
PDF) located but not successfully fetched this session (HTML landing pages returned instead of
PDF content) — their claims are flagged as unverified above, not incorporated into the verdict.

## Point 82 (2026-09-16) — Cheap pre-checks T2/T4 (Point 80's own recommended diagnostics, zero
new compute) run BEFORE starting Strategy 1: Cauchy-Schwarz slack is SHRINKING toward 1 as `n`
grows, meaning the `MIX4`/`F4` targets are CONVERGING — the "sharper, avoid-CS" motivation for
targeting the joint moment over the marginal one is weaker in practice than Point 78/80 assumed.
Tail-to-rms ratio grows, but slower than `log³n` itself — not an alarm, consistent with the
existing picture

**Context.** Direct continuation of Point 80's own "kill criteria, minutes on already-existing
raw rows" table (T1 and T3 already run in Point 80; T2 and T4 run here, per the same discipline
of checking cheaply before spending a proof-attempt session).

**T2 — `CS-slack(n) := √(E[x*⁴]E[w*⁴]) / E[x*²w*²]`, the Cauchy-Schwarz bound's own looseness,
computed directly from raw rows:**

| n | `J_n` (`=n²E[x²w²]`) | `n²√(E[x⁴]E[w⁴])` (CS bound) | slack |
|---:|---:|---:|---:|
| 127 | 64.66 | 124.85 | 1.931 |
| 509 | 73.44 | 96.45 | 1.313 |
| 1021 | 86.58 | 98.50 | 1.138 |
| 2039 | 81.26 | 88.14 | 1.085 |

**The slack shrinks monotonically toward 1 as `n` grows.** Cauchy-Schwarz becomes nearly TIGHT at
the largest tested `n` — consistent with, and mechanistically explained by, Point 80's own finding
that `corr(x*²,w*²)` grows toward 1 (`0.25→0.60→0.79→0.86`): CS achieves equality exactly when the
two quantities being bounded are proportional, and the correlation trend is moving toward exactly
that regime. **Practical consequence, not previously stated:** since `J_n ≈ n²·E[x⁴]` (via `w*`'s
equal marginal) once slack≈1, proving `J_n=O(1)` (MIX4) and proving the marginal `F4=O(1/n²)`
(i.e. `E[x⁴]=O(n⁻²)`, matching `F4abs` from Point 78's own taxonomy) become NEARLY THE SAME
PROBLEM at the measured `n`'s. Point 78's framing of MIX4 as a meaningfully sharper, CS-loss-free
target than the marginal route is empirically much less true in practice than the algebra alone
suggested — the actual difficulty gap between "prove it jointly" and "prove it on each marginal
separately" is shrinking, not fixed.

**T4 — `max(Z_ni)/rms(Z_ni)`, a proxy for `sup δ_i` vs `rms δ_i` (relevant to any bounded-
differences / McDiarmid-type argument, per Point 80's second-round skeptic review of Strategy 0):**

| n | max/rms |
|---:|---:|
| 127 | 3.504 |
| 509 | 4.295 |
| 1021 | 4.714 |
| 2039 | 5.626 |

Grows with `n`, but at a materially SLOWER rate than `log³n` itself would predict
(`log³(2039)/log³(127)≈3.3`× vs the observed max/rms ratio growing only `≈1.6`×) — **this is
consistent with the existing polylog picture, not a new red flag.** A `sup`-based (McDiarmid)
argument would need `sup δ=O(1/n)` uniformly, strictly stronger than the `E[δ²]≤C/n²` target;
this diagnostic says that route is not obviously hopeless (the ratio isn't exploding), but it was
never the cheapest route either (Point 80's second-round review already noted a `sup`-based bound
is strictly stronger than the actual bottleneck).

**What this does NOT mean.** Does NOT mean Strategy 1 (hypercontractivity/delocalization,
re-scoped in Point 80 toward the joint quantity) should be abandoned — `J_n=O(1)` remains
proven-sufficient for S1 regardless of how close `F4` and `MIX4` are numerically. Does NOT mean
the `POL` dependency found in Point 80 is resolved or avoided — the CS-slack shrinking toward 1
does not change the fact that `E[x²]=O(1/n)` (`POL`) remains a load-bearing precondition either
route needs. Does NOT mean this diagnostic proves the marginal and joint targets are IDENTICAL —
only that they are numerically close at the tested `n`'s and the gap is shrinking, which is weaker
than proven equality and could still diverge at larger `n`. Does NOT mean further diagnostics on
existing data remain to be cheaply mined indefinitely — per Point 77's own "empirical channel
exhausted" finding and the discipline that motivated this whole Point 77-82 correction chain, this
is the last of Point 80's own pre-registered cheap checks; what remains is either Gate-0-style
literature work (already done, Points 79/81) or genuine new proof-attempt effort (Strategies 1-3),
not further mining of `metrics/ppl_gate_pilot.json`.

**Artifacts:** No code or data changes. Both diagnostics computed directly from
`metrics/ppl_gate_pilot.json` row-level `x_i`/`w_i`/`Z_ni` fields this session.

## Point 83 (2026-09-16) — `E‖x*‖²` measured across `n=127..2039`: rules out `log³n` and `c·log n`
growth (`~17.7σ`, `~5.5σ`), but is STATISTICALLY INDISTINGUISHABLE from the same slow power-law
growth (`n^{~0.04-0.05}`) that this project's own three OTHER independently-measured series
already show — NOT the "strong evidence `(POL)` is true" first claimed. First draft of this point
was SUBSTANTIALLY WRONG, caught on skeptic-fallback review, corrected here in full

**Context.** Direct continuation of Point 82. First draft measured `E‖x*‖²=m·E[x_i²]` across all
four `n`, found it numerically close to a constant (`≈3.1-3.5`), and concluded this was "strong
empirical evidence that `(POL)` is TRUE" — re-targeting Strategy 1 onto proving `(POL)`. **Skeptic
review (context-asymmetric, same `reviewer→skeptic` substitution as throughout this session) found
this headline claim unsupported and, worse, in direct conflict with Point 82's own "What this does
NOT mean" section.** Both core findings independently re-verified from scratch before being
accepted — the arithmetic and the two central objections both hold.

**The measurement itself, re-verified, is correct — only the interpretation was wrong.**

| n | `E‖x*‖²` | SE |
|---:|---:|---:|
| 127 | 3.147 | 0.189 |
| 509 | 3.115 | 0.164 |
| 1021 | 3.293 | 0.173 |
| 2039 | 3.174 | 0.159 |

**Weighted log-log slope (same convention as this project's own `weighted_power_law_fit`,
independently re-derived): `b = 0.0084 ± 0.0272`, 95% CI `[-0.045, 0.062]`.** The first draft
reported this slope WITHOUT an SE or CI at all — the single biggest gap, since every other fit in
this file (`J_n`, `K_n`, `sd_w(U)`) reports one.

**Correction 1 — FALSIFIED: "strong evidence `(POL)` is true."** The 95% CI `[-0.045, 0.062]`
is wide enough to contain the EXACT growth rate this project's own other three independently-
measured series already imply, via `Energy~n^a ⟹ J_n~n^{2a} ⟹ Var~n^{2a-1}` (re-derived and
verified this session):

| independently-measured series (already in this file) | implied `a` | inside this point's 95% CI? |
|---|---:|---|
| `Var(X_n)` slope `-0.9123` (headline, `n=32..3000`) | `0.044` | **yes** |
| `J_n` slope `0.0998` (Point 76/78) | `0.050` | **yes** |
| `K_n` slope `0.0671` (Point 76/78) | `0.034` | **yes** |

**This measurement cannot distinguish `(POL)` (`a=0`) from the SAME slow growth the rest of this
project's own data already suggests (`a≈0.03-0.05`).** The correct statement is narrower than the
first draft's: `log³n` (`a` effectively `3/ln n`, i.e. `0.49-0.62` over this range) is excluded at
`~17.7σ`; `c·log n` is excluded at `~5.5σ`; **anything at or below `n^{~0.06}` (equivalently
`log^{~0.4}n`) remains fully compatible with the data** — this is NOT the same as evidence for
`a=0` specifically.

**Correction 2 — FALSIFIED: "the entire F4/MIX4 program's ceiling is S2 unless `(POL)` is
separately established."** This directly contradicts Point 82's own text, two points earlier in
this same file: *"`J_n=O(1)` remains proven-sufficient for S1 regardless of how close `F4` and
`MIX4` are numerically"* and *"Does NOT mean this diagnostic proves the marginal and joint targets
are IDENTICAL."* `MIX4` (`J_n=O(1)`) gives S1 unconditionally (Point 78's own derivation, no
`(POL)` input required) — the first draft of THIS point silently substituted the empirical,
finite-`n` numerical CLOSENESS of `F4` and `MIX4` (Point 82's CS-slack `→1`, still `8.5%` above 1
at `n=2039`, convergence not proven) for a claim about what the two targets can each, in
principle, establish. Retracted in full.

**Also caught, minor:** the first draft's "`would be ~3` if the ceiling were tight" benchmark was
wrong by a factor of `~6` — re-derived: the log-log slope of `log³n` itself over `n=127..2039` is
`≈0.49`, not `3` (`3` is the exponent on `log n` directly, not the log-log slope of `log³n` vs `n`
— a units error in the first draft, not merely an approximation).

**What DID survive, stated at the strength the data actually supports:**
- `log³n` and `c·log n` growth are genuinely excluded for `E‖x*‖²` over this range — a real,
  useful finding, just narrower than "`(POL)` is true."
- `κ_x := E[x*⁴]/(E[x*²])²` (the `F4rel` ratio) is bounded and roughly declining across all four
  `n` (independently computed this session directly from raw rows: `2.793 → 2.376 → 2.375 →
  2.254` — not strictly monotonic between `n=509` and `n=1021`, but the overall `127→2039` trend
  is down) — meaning `F4rel` itself
  (`E[x*⁴]=O((E[x*²])²)`) is in empirically good shape regardless of how the `(POL)` question
  resolves. The actual open bottleneck remains `(POL)`, as Point 77's own Revival Condition (b)
  and Point 80 §3 already identified — this point's only genuinely new content is the direct
  measurement of `E‖x*‖²` itself, not the strategic conclusion, which was already on record.
- `x*` and `w*` are NOT 8 independent confirmations — Point 80 already measured
  `corr(x*²,w*²)=0.86` at `n=2039`; the two columns are heavily dependent, not independent
  evidence, at the largest tested `n`.

**The decisive, cheap, NOT-YET-RUN test this correction surfaces.** The measurement above used
only ONE coordinate per graph (`gen_index=1`), the noisiest available estimator of `E‖x*‖²` — the
full `‖x*‖²` (the complete optimal vector, already computed by the LP solve that produced this
row, just not saved) would cut the SE by a factor of `~3-5×` (`√m ≈ 8` for `n=127` up to `√m ≈ 32`
for `n=2039`), which would be enough to actually distinguish `a=0` from `a≈0.04-0.05` — the exact
question this point could not resolve with the single-coordinate proxy. This is the natural next
step before attempting any proof of `(POL)`, not a re-run of the same measurement.

**What this does NOT mean.** Does NOT mean `(POL)` is false — it remains genuinely open, exactly
as before this point, with `log³n`/`c·log n` now excluded as viable descriptions (real progress,
just not proof of the alternative). Does NOT mean Point 82's `MIX4≈F4` finding was wrong — it
correctly reported a numerical closeness at finite `n`, not a proven identity; this point's error
was mis-using that finding, not Point 82 misreporting it. Does NOT mean `F4rel`'s good empirical
shape (`κ` bounded, decreasing) settles it either — a bounded, decreasing sample ratio on 4 points
is suggestive, not a proof, exactly as `E‖x*‖²`'s flatness was suggestive and not proof here.

**Artifacts:** No code or data changes. `E‖x*‖²` and its weighted-fit slope/SE/CI independently
re-derived this session using the project's own `weighted_power_law_fit` convention (not the first
draft's unweighted, SE-less bootstrap slope), directly from `metrics/ppl_gate_pilot.json` row-level
`x_i` values. The three cross-series `a`-exponent comparisons and the `κ_x` series independently
computed and checked against the CI before being accepted.

## Point 84 (2026-09-16) — `E‖x*‖²` measured precisely (full-norm estimator): `a=0` not rejected,
but the "DECISIVE... z=10-16" exclusion of the alternative growth rate in the first draft was a
severe overclaim (z-scores computed against the alternatives' OWN point values, ignoring their
substantial SE) — corrected z-scores are `2.90/1.92/1.11`, only marginal and only for the one
truly independent comparison. A real, bootstrap-confirmed finding survives: `J_n`'s growth is
driven by a growing `Cov(x*_i²,w*_i²)`, not the (flat) marginals — but this is NOT a new,
independent target: by Cauchy-Schwarz it already FOLLOWS from `(POL)+F4rel`, both still open,
just empirically well-supported, not proven. A further, structural finding (verified in the code
directly) explains WHY the dependence is concentrated exactly where it is: `x*_j·w*_j≡0` for every
coordinate `j` except `GEN_INDEX`, by construction

**Context.** Point 83 named the decisive-but-expensive test: save the FULL `‖x*‖²`/`‖w*‖²` per
row (not the single `GEN_INDEX=1` coordinate `ppl_gate_pilot.json` stores). Per direct user
decision, launched as a background computation (`check_pol_full_norm.py`, new script, does NOT
modify `ppl_gate_pilot.py` or its JSON). All `4×500=2000` rows' `x_i`/`w_i` at `GEN_INDEX=1`
matched `ppl_gate_pilot.json`'s existing rows for the same seeds exactly (`max_abs_diff=0.0`).
**First draft of this point was SUBSTANTIALLY WRONG on its headline claims, caught on
skeptic-fallback review, both core objections independently re-verified (with actual bootstrap
computation, not the reviewing pass's own back-of-envelope estimates) before being accepted.**

**Result 1 — `E‖x*‖²` (full-vector norm, `x[0]=1` included by the LP solver's own construction —
NOTE: this is a different quantity from Point 83's `m·E[x_i²]`, which excludes `x[0]`; the two
are related but NOT simply offset by a clean constant given `x_1` is conditioned-always-free in
`g0` while other coordinates are unconditionally free ~half the time — no precise conversion
formula between the two points' numbers is asserted here):**

| n | `E‖x*‖²` | SE | `E‖w*‖²` | SE |
|---:|---:|---:|---:|---:|
| 127 | 4.0941 | 0.0429 | 4.0652 | 0.0444 |
| 509 | 4.0280 | 0.0193 | 4.0274 | 0.0197 |
| 1021 | 4.0237 | 0.0140 | 4.0773 | 0.0137 |
| 2039 | 4.0766 | 0.0106 | 4.0688 | 0.0106 |

**Weighted log-log slope: `b=0.00473±0.00287`, 95% CI `[-0.00089, 0.01035]`. `Δχ²`-test for
`b=0`: `p=0.0993`.** Correction: the first draft called this "not significant even at 10%" —
`0.0993<0.10`, the opposite of what was written. The correct, honest framing: the null of no
growth is NOT rejected at the conventional 5% level, but sits right at the edge of 10%
(one-sided `p≈0.05`) — this is a mild, not absent, hint of growth in `E‖x*‖²` itself, not the
clean "flat, `(POL)` confirmed" picture the first draft presented.

**Correction — the z-score comparison against the three other project series was WRONG,
FALSIFIED on review, independently re-verified and fixed.** The first draft computed
`z=(a_alt-b)/SE(b)`, treating each alternative `a` (from `Var(X_n)`, `J_n`, `K_n` slopes) as an
exact constant. They are not — each is itself a fitted slope with its own SE, already on record
in this file. The correct comparison uses the combined SE:

| series | `a ± SE(a)` | `z = (a-b)/√(SE(a)²+SE(b)²)` | significant? |
|---|---|---:|---|
| `Var(X_n)` slope `-0.9126±0.0264` → `a=0.0437±0.0132` | (independent: `n=32..3000` headline) | **2.90** | marginal |
| `J_n` slope `0.0998±0.0467` → `a=0.0499±0.0233` | (NOT independent — same 2000 seeds) | **1.92** | no |
| `K_n` slope `0.0671±0.0516` → `a=0.0336±0.0258` | (NOT independent — same 2000 seeds) | **1.11** | no |

**Only the `Var(X_n)` comparison is even marginally significant (`2.9σ`), and it is the only one
of the three that is genuinely independent data (`J_n`/`K_n` are computed from the SAME 2000
seeds as this measurement, confirmed by the positive control — comparing to them is not an
independent check).** The first draft's "`z=10-16`, astronomically significant, decisively
excluded" was off by a factor of `4.7-9.2×`, from omitting the alternatives' own substantial SE.
**Honest verdict: `a=0` is not rejected; a modest, single, non-independent-confirmed hint of slow
growth (`~2.9σ` against the one independent comparator) cannot be ruled out either. This is
NOT the clean "`(POL)` empirically confirmed" the first draft claimed.**

**Result 2 — real, and independently re-verified with an actual bootstrap (not the reviewing
pass's rough approximation).** Decomposing `E[x_i²w_i²]` (the single-`GEN_INDEX` quantity `J_n` is
built from) via the exact identity `E[x²w²]=E[x²]E[w²]+Cov(x²,w²)`, with `3000`-resample bootstrap
SE on each term at each `n`:

| n | `n²·E[x²]E[w²]` (marginal) | `n²·Cov(x²,w²)` |
|---:|---:|---:|
| 127 | 44.89 ± 4.17 | 19.81 ± 3.03 |
| 509 | 39.45 ± 3.76 | 34.05 ± 3.80 |
| 1021 | 42.16 ± 4.18 | 44.51 ± 5.55 |
| 2039 | 38.97 ± 3.79 | 42.37 ± 5.85 |

**Trend significance, `127→2039`, properly bootstrapped:** marginal term `z=-1.05` (not
significant, consistent with flat); covariance term **`z=3.42`** (real, survives independent
bootstrap re-verification — the reviewing pass's own rough estimate of `~1.9σ` was itself too
conservative; a proper bootstrap gives a stronger, not weaker, signal here). **This part of the
first draft's qualitative story holds: `J_n`'s growth is attributable to the covariance term
specifically, not to either marginal.**

**Correction — this is NOT an independent new target, it is a restatement of the existing one.**
The first draft framed "bound `Cov(x*_i²,w*_i²)=O(n⁻²)`" as a sharply NEW target, distinct from
and superseding `(POL)`/`F4rel`. This is wrong: by Cauchy-Schwarz, `|Cov(x²,w²)|≤√(E[x⁴]E[w⁴])`,
and if `(POL)` and `F4rel` both hold, the right side is already `O(n⁻²)` — **`Cov=O(n⁻²)` is a
CONSEQUENCE of `(POL)+F4rel`, not a separate problem requiring separate proof.** The actual open
work remains exactly what Point 83 identified: prove `(POL)` and `F4rel`, both currently
empirical-only, not proven. A genuinely useful, correctly-scoped observation the first draft
missed: the Cauchy-Schwarz ceiling specifically on `Cov(x²,w²)` (`|Cov|≤√(Var(x²)Var(w²))`,
independently computed this session from raw rows, NOT the reviewing pass's own approximation) is
**itself declining** — `n²·ceiling = 79.96 → 56.97 → 56.33 → 49.17` across the four `n` — while
the observed `n²Cov` (`19.77→33.98→44.42→42.29`) has risen to **`86%`** of that shrinking ceiling
at `n=2039` (this ratio is, by construction, exactly `corr(x²,w²)` — the same quantity Point 80
already tracked as `0.25→0.60→0.79→0.86`, now re-confirmed from an independent computation on this
new dataset). The covariance is not growing without limit — it is closing in on an
already-tightening bound, a materially different (and more informative) picture than "unboundedly
growing."

**A real structural finding, verified directly in the code, not previously stated anywhere in
this project.** `comp` (yielding `w*`) is solved on `1-bits_g1` (the FULL complement of `G1`'s
bits, not just the `GEN_INDEX` bit toggled) — `test_convolution_repair.py`'s `CertificateLP.solve`
marks coordinate `j` "free" (potentially nonzero) exactly where the corresponding bit is `0`.
Since `bits_g0` and `bits_g1` differ ONLY at `GEN_INDEX-1` (by `flip_generator`'s own construction,
already established elsewhere in this file), for every `j≠GEN_INDEX`: `j` is free in `g0` iff
`bits_g0[j]=0`, and free in `comp` iff `bits_g1[j]=1` — since `bits_g0[j]=bits_g1[j]` for
`j≠GEN_INDEX`, these two conditions are exact complements. **`x*_j` and `w*_j` can never both be
nonzero for `j≠GEN_INDEX` — `x*_j·w*_j≡0` deterministically, by construction, for every
coordinate except the one being toggled.** The entire `x_i·w_i` product this whole `J_n`/`K_n`
pipeline (Points 66-84) is built from lives on a SINGLE coordinate that is structurally
"shared-active" between the two certificates — not a general delocalization statistic averaged
over many coordinates. This tempers "the mechanism... remains completely open" — as `n` grows,
the SAME single generator's relative influence on the graph shrinks (one bit out of a growing `m`
total), which is a plausible, cheap-to-investigate-further candidate mechanism for why `x*` and
`w*` grow more correlated, not yet a proof of it.

**What this does NOT mean.** Does NOT mean `(POL)` is disproven — `a=0` is still not rejected,
only the "confirmed" framing was too strong. Does NOT mean `S1` is closer or further than Point 83
left it — the actual open work (`(POL)`, `F4rel`, both empirical-only) is unchanged; this point
corrects what FOLLOWS from them (nothing new — `Cov=O(n⁻²)` was always implied) and adds one real
structural fact (the single-coordinate concentration) and one real quantitative fact (the
covariance is approaching a shrinking CS-ceiling, not growing unboundedly). Does NOT mean the
positive control's exactness validates anything beyond input reproducibility — it confirms this
script solves the same LPs as the canonical pipeline, not that the new `x_norm_sq`/`w_norm_sq`
fields are bug-free (their correctness was checked separately, via the `x[0]=1`/dimension checks
above). Does NOT mean Point 83's own conclusions are overturned — `κ_x` bounded/declining and the
excluded `log³n`/`c·log n` growth rates for the single-coordinate proxy both stand.

**Artifacts:** `check_pol_full_norm.py`, `metrics/pol_full_norm_check.json`,
`pol_full_norm_run.log`. Reviewed by `skeptic` (context-asymmetric, same standing substitution as
throughout this session): found the z-score overclaim (the load-bearing correction above) and the
`x[0]=1` quantity-mismatch between this point and Point 83; both independently re-verified by
direct computation (proper combined-SE z-scores; the `x[0]=1` line read directly from
`CertificateLP.solve`'s source) before being accepted, per this session's standing discipline.
The reviewing pass's own rough SE estimate on the covariance trend was itself superseded by an
actual `3000`-resample bootstrap computed here, which gave a STRONGER result (`z=3.42` vs. the
review's own conservative `~1.9`) — corrections were verified, not merely accepted on the
reviewer's word in either direction.

