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
