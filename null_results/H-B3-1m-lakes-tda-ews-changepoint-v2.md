# decision.md — H-B3-1m (V2 two-part rule: tau AND Pettitt level-shift, H-B3-1b Row 2)

## FOLLOW-UP: power fix + independent implementation cross-check (2026-09-07, same session,
resolves the CORRECTION ADDENDUM below) — **FINAL VERDICT: REJECT**

Direct action on the two open items from the CORRECTION ADDENDUM (Findings 3, 4, 5 below):

**1. Independent implementation cross-check (resolves Finding 5).** Cross-checked the hand-rolled
`pettitt_test` against the third-party `pyhomogeneity` package (installed for this check) on a
7-item battery: step change up/down, monotone trend with no step, pure white noise, the real
Lower Zurich PCA1 series, an AR(1) surrogate of it, and the rolling-AC1 statistic actually fed to
the test. **The K/U statistic matched exactly on all 7 cases** (own vs. `pyhomogeneity`, to
floating-point precision); the reported change-point index differed by a constant +1 in every
case (a 0- vs 1-indexing convention, not a defect). **No implementation bug found — Finding 5 is
DISMISSED.** As a side effect, this is a SECOND, fully independent confirmation of Finding 1:
`pyhomogeneity` also flags the pure-monotone-trend series (no step change) as significant
(K=900.00, matching exactly; Monte-Carlo p≈0) — the "Pettitt targets step-change, not trend"
claim fails on a third-party implementation too, not just the hand-rolled one.

**2. Power + independence fix (resolves Findings 3 and 4).** `run.py` changed: `floor_reps`
30→**500** per lake (95% CI half-width ~18pp → ~4.4pp, comfortably resolving the pre-registered
50% boundary), and each lake now gets its own seed (`1000*(lake_index+1)`, was a shared `seed=0`
for all three). Re-ran:

| Lake | Floor FP rate (reps=500) | 95% CI |
|---|---|---|
| Lower Zurich | 44.0% | [39.6%, 48.4%] |
| Windermere | 42.8% | [38.5%, 47.1%] |
| Loch Leven | 41.6% | [37.3%, 45.9%] |

**All three lakes now converge tightly to ~42–44%, comfortably and unambiguously below the 50%
threshold — the original divergence (Loch Leven 53.3% vs. Windermere 33.3% at reps=30) was
noise, exactly as Finding 3 predicted.** `max_new_floor_fp_rate=0.44 < 0.5` → Step 1 (floor) now
PASSES cleanly → the pre-registered kill criterion proceeds to Step 2 for the first time.

**Step 2 (real-lake pattern) result: FAILS.** Lower Zurich's own crossing is unchanged (TDA
1999.5, classical 2001.5, lead +24 months — this computation never depended on floor reps/seed).
But Loch Leven's REAL observed data (not its AR(1) null) genuinely two-part-crosses: its classical
AC1 statistic crosses at 1999.25 — a true false positive on a negative-control lake. This was
always present in the underlying computation but was invisible in the original run because Step 1
failed first (floor ≥50%) and the pre-registered criterion never reached Step 2. Per claim.md's
own kill criterion ("REJECT: any negative control still two-part-crosses"), this is now a clean,
unambiguous **REJECT** — not the "unresolved at current power" holding pattern from the
CORRECTION ADDENDUM below.

### Kill Analysis (per Anti-Overfitting Gate / OSA discipline, required for REJECT)

**What is KILLED:** the V2 two-part rule (tau≥0.5 AND Pettitt p<0.05 on the raw statistic) as a
detection rule for THIS 3-lake population, under the specific window/embedding parameters
inherited from `H-B3-1`/`H-B3-1b`. The floor problem that motivated trying this fix is resolved
(all 3 lakes ~42–44%, well under 50%), but the rule still produces a real false positive on
Loch Leven's actual data — adding the Pettitt gate improved specificity against pure AR(1) noise
without eliminating the rule's failure on this specific real negative control.

**What is NOT killed:**
- The underlying floor-improvement MECHANISM is real and substantial (83%/80%/83% → ~42–44%
  uniformly) — even though Finding 1 shows the claimed "trend vs. step-change" story doesn't
  explain WHY it works, something about jointly requiring both conditions does cut the AR(1)
  false-positive rate roughly in half, verified now with adequate power.
- `H-B3-1l`'s peak-tau CONFIRMED-with-confound result (a different fix, on the same population)
  is untouched by this REJECT.
- `H-B7-*`, `H-B2-*`, and every other bridge's own findings are unaffected — this REJECT is
  scoped to one specific detection-rule variant on one specific 3-lake population.

**Relaxation Map (untested directions, if this line of investigation is resumed):**
- Diagnose the mechanism behind the real floor improvement (Findings 1+2 together suggest it is
  NOT "Pettitt filters step-change from trend" — some other, unidentified interaction between the
  τ-crossing index and the Pettitt gate on THESE specific rolling statistics is doing the work).
- Try a stricter Pettitt alpha (e.g. 0.01) specifically to see if Loch Leven's real false positive
  clears while Lower Zurich's real detection survives — a genuinely new, one-assumption-changed
  variant (Minimal Relaxation Rule), not attempted here.
- Combine with `H-B3-1l`'s peak-tau reporting instead of first-crossing — untested combination.

**Practical consequence for the bridge:** all 3 of `H-B3-1b`'s originally-named Relaxation Map
rows are now cleanly resolved: Row 1 (surrogate null) REJECTED via H-B3-1c/d/e; Row 2 (this
experiment, change-point co-requirement) REJECTED, now with adequate power and an independently
cross-checked implementation; Row 3 (peak-tau, H-B3-1l) CONFIRMED-with-confound. The 3-lake
`H-B3-1`/`H-B3-1b` population's threshold-based detection-rule framing has no surviving clean
PROMOTE across any of its 3 named fixes — the 5-series `H-B3-1g-k` population and its
conjunction-based approach (`H-B3-1h`) remains the strongest surviving result on this bridge, as
already noted in the original Pearl Card Update below.

---

## CORRECTION ADDENDUM (2026-09-07, FL Step 8a skeptic pass — seventh and final of the systematic
sweep this session)

**This experiment's own decision.md (below, "FL Step 8a — Skeptic Pass") explicitly noted the
context-asymmetric skeptic agent was NOT run** ("Evaluator-Optimizer cap still in effect
session-wide") — only manual self-review was applied. Running the actual agent this session (as
done for six other flagged experiments) found real, previously-uncaught issues, the most serious
of which independently-verified computation confirms is load-bearing.

**Finding 1 — CONFIRMED (independently re-verified by direct computation, not accepted on the
skeptic's derivation alone): claim.md's central mechanistic justification is false as stated.**
claim.md argues Pettitt's test adds specificity because it "targets a DIFFERENT signal — a
genuine level shift — which pure AR(1) red noise should NOT reliably produce, even though it CAN
produce spurious monotone trend." This is not correct: Pettitt's test has near-full power against
a pure monotone trend with NO step change at all, because the underlying Mann-Whitney-style rank
statistic responds to *any* systematic ordering, not specifically to a discrete jump. Verified
directly: for a strictly monotone series of length n with zero noise, `K = n²/4` exactly (matches
the closed-form derivation), giving p≈3.7×10⁻⁵ at n=30 — i.e., the test rejects the null with
near-certainty on trend alone, no step change involved. The "AND" gate is therefore closer to
"trend AND (trend-is-not-flat)" than "trend AND genuine regime shift" — the claimed mechanism by
which AR(1)-faked-trend gets filtered out does not operate as described. This does NOT change the
reported floor false-positive numbers (those remain real empirical measurements of the actual
rule as coded), but it invalidates the "why this works" narrative in claim.md's "Why This
Experiment, Specifically" section and the MCID framing that attributes any observed floor drop to
a trend-vs-step-change mechanism.

**Finding 2 — CONFIRMED (visible directly in code, no independent verification needed):
Pettitt's p-value approximation assumes IID observations; the inputs are rolling-window
statistics with (window−1)/window inter-sample correlation by construction.** The nominal
`alpha=0.05` in `two_part_crossing` is therefore not a real 5% type-I rate on these inputs — the
test is known to be anti-conservative on autocorrelated series. The floor computation still
honestly measures whatever the coded rule does (surrogates go through the identical
rolling→Pettitt path as real data), but "we chose α=0.05" should be read as "we chose a nominal
label whose true significance level is unknown and likely inflated," not a calibrated 5% gate.

**Finding 3 — CONFIRMED (binomial arithmetic): `reps=30` per lake gives SE≈9.1pp, 95% CI
half-width≈18pp — the pre-registered 50% decision boundary sits well inside this noise band.**
Loch Leven's reported 53.3% (CRITERION_INVALID) and Windermere's 33.3% (well under) are not
reliably distinguishable from each other or from the 50% line at this rep count. The "roughly
halved" characterization of the floor improvement, and the CRITERION_INVALID verdict itself, are
both underpowered as measured — a re-run at reps≥500 could plausibly move Loch Leven below 50% or
push Windermere/Lower Zurich above it. This was not caught before the claim was finalized, despite
the project's own established precedent (`H-B2-1i` et al.) of scrutinizing sample-size adequacy
near decision thresholds.

**Finding 4 — CONFIRMED (visible directly in code):
`floor_false_positive_rate_v2(pca1, window, reps=30, seed=0)` is called with the literal same
`seed=0` for all three lakes.** Each lake's `pca1` differs, so surrogates are still lake-specific,
but the shared RNG start correlates the innovation sequences across lakes' surrogate draws —
effectively fewer than 3 independent floor measurements (skeptic estimates ~1.5). Weakens the
"improvement seen independently at 2/3 lakes" framing in the original decision.md.

**Finding 5 — plausible, not independently verified this pass: validation-theater risk.** The
Pettitt implementation's own positive/negative-control tests were written in the same session as
the implementation, and a positive control using an obvious step change does not discriminate a
correct p-value formula from a mis-scaled one (any monotone function of K that shrinks with larger
K would "pass" such a test). No cross-check against an independent third-party Pettitt
implementation (e.g. `pyhomogeneity`, R's `trend::pettitt.test`) was run. Flagged for follow-up,
not confirmed as an actual bug — no arithmetic error was found in the formula itself.

**Response Matrix disposition:** Finding 1 — **Accepted, core correction** (mechanism narrative in
claim.md and MCID section is wrong; independently re-verified, not just re-argued). Finding 2 —
**Accepted, reframe** (α=0.05 is nominal only; document as such). Finding 3 — **Accepted,
significant** (verdict CRITERION_INVALID should be read as "unresolved at this power," not a
confident conclusion; re-run at higher reps is the correct next step, not a new claim). Finding 4
— **Accepted, documented weakness** (per-lake seeding needed for a genuinely independent 3-lake
result). Finding 5 — **Accepted as open item, not yet confirmed or dismissed** (independent
cross-check is cheap and should be done before this rule is trusted further).

**Practical consequence:** the numeric floor measurements (83.3%/80.0%/83.3% → 40.0%/33.3%/53.3%)
stand as honest empirical readings of the coded rule, but every downstream interpretation this
project has drawn from them — "the mechanism works, just not sufficiently at Loch Leven," "a real
substantial improvement, not a clean no-progress result," even the CRITERION_INVALID verdict
itself — rests on an underpowered measurement (Finding 3) interpreted through a mechanistic story
that Finding 1 shows is not actually operating as claimed. This is weaker than a clean REJECT: the
raw numbers are not shown to be wrong, but neither the "why" nor the precision needed to trust
"which side of 50%" is currently defensible. Verdict downgraded: CRITERION_INVALID (as reported)
→ **CRITERION_INVALID, UNRESOLVED AT CURRENT POWER** — re-run at reps≥500 with per-lake seeding
and an independent Pettitt cross-check is required before this experiment's numbers support any
further claim in either direction.

Seventh and final skeptic pass of this session's systematic sweep: **7/7 found real,
previously-uncaught issues** — ranging from label-only weakening (H-B2-1i) through rigorous
mathematical impossibility (H-B2-1h) to, here, a foundational mechanism-justification error
confirmed by independent computation. No experiment in the flagged set survived a genuine
context-asymmetric skeptic pass unchanged.

## Result (ORIGINAL TEXT, superseded above for interpretation — raw numbers stand as measured)

**Verdict: CRITERION_INVALID** (per FL Step 4a — NOT evidence against the claim), but with a
real, substantial, per-lake floor improvement that a flat "still invalid" label would obscure.

| Lake | Original floor FP rate | New (two-part) floor FP rate | Change |
|---|---|---|---|
| Lower Zurich | 83.3% | **40.0%** | roughly halved |
| Windermere | 80.0% | **33.3%** | roughly halved |
| Loch Leven | 83.3% | **53.3%** | reduced, but still ≥ the pre-registered 50% invalidity bound |

`max_new_floor_fp_rate = 53.3%` (Loch Leven) ≥ the pre-registered 50% threshold → per
`claim.md`'s own kill criterion, this is `CRITERION_INVALID`: the detection rule STILL cannot be
trusted as informative on this population, driven specifically by one lake, not by the mechanism
failing uniformly.

## Why This Is Not a Clean "No Progress" Result

Requiring BOTH a trend (tau≥0.5) AND a genuine level shift (Pettitt p<0.05) cut the AR(1)
false-positive rate roughly in HALF at two of the three lakes (83%→40%, 80%→33%) — a real,
substantial, mechanistically-sensible improvement (pure red noise CAN fake a monotone trend by
chance, but is less likely to also fake a clean step-change in level). The fix did not fully
solve the floor-invalidity problem, and the pre-registered 50% bound must be honored as written
(no post-hoc relaxation to declare victory), but "made real progress at 2/3 lakes, insufficient
at the third" is a different, more informative finding than "the fix doesn't work."

## What Was Confirmed

- [x] Pettitt's test implementation is correct: positive controls (obvious step changes, both
  directions) locate the change-point within 3 index-positions of the true midpoint with
  p<0.001; negative controls (white noise, a constant series) do not spuriously fire (constant
  series: K=0, p=1.0 exactly; 200 white-noise trials: false-positive rate <20% at alpha=0.05, not
  wildly miscalibrated).
- [x] The two-part rule's mechanism works as designed: it only REMOVES crossings relative to the
  original rule (an AND-gate), never adds new ones or shifts timing — confirmed directly: Lower
  Zurich's surviving crossing dates (TDA 1999.5, classical/var 2001.5, lead +24 months) are
  IDENTICAL to `H-B3-1`'s own original result, because that crossing also passes the new Pettitt
  gate.
- [x] The floor drops substantially (roughly halved) at Lower Zurich and Windermere.

## What Remains Open

- **Why does Loch Leven specifically resist the fix** (53.3%, barely over the bound) while
  Windermere (a similarly non-transitioning lake) drops to 33.3%? Not diagnosed here. Loch
  Leven's own real negative-control crossing (both AC1 and variance) survived the Pettitt gate —
  meaning its AR(1) surrogate construction (matched to Loch Leven's own length/mean/variance/AC1)
  produces enough surrogates with a REAL, Pettitt-significant level shift by chance. Possibly
  related to Loch Leven's specific autocorrelation structure or shorter series length (n=152, the
  shortest of the three) giving Pettitt's test less power to reject.
- Whether the SAME two-part rule crosses the invalidity bound on the 5-series population used in
  `H-B3-1g-k` is untested (explicit scope decision, same as `H-B3-1l`).
- The 50% invalidity threshold itself was a judgment call (documented in claim.md as "still
  clearly at-floor"), not derived from a formal power calculation — a stricter or looser bound
  could change which side of the line Loch Leven falls on. Reported honestly at exactly 53.3%
  rather than rounded to "about half."

## Relaxation Map

- **Diagnose Loch Leven specifically** — compare its own AR(1) parameters (phi, sigma) and
  length against Windermere's; check whether a longer/more autocorrelated surrogate construction
  is intrinsically more likely to produce a spurious Pettitt-significant level shift.
- **Try a stricter Pettitt alpha** (e.g. 0.01 instead of 0.05) — would further cut the floor at
  the cost of also reducing power to detect Lower Zurich's real transition; a genuinely new,
  one-assumption-changed variant if pursued (Minimal Relaxation Rule).
- **Combine with V1's surrogate-null approach** (per-series calibrated significance instead of a
  literature-borrowed Pettitt alpha=0.05) — the two fixes are not mutually exclusive; a combined
  V1+V2 rule is a natural, more expensive follow-up.

## Note on Floor–Ceiling (FL Step 4a)

This experiment's own floor computation IS the Step 4a check, run BEFORE any real-lake
interpretation, per the pre-registered order in `claim.md`. The verdict (`CRITERION_INVALID`) is
explicitly NOT evidence against the underlying TDA-leads-EWS claim, per the hard rule — it is a
statement about the detection rule's remaining inadequacy on this specific 3-lake population,
now narrowed to one specific lake rather than all three uniformly.

## FL Step 8a — Skeptic Pass

Not run as a separate agent invocation (Evaluator-Optimizer cap still in effect session-wide).
Manual discipline applied: the pre-registered 50% bound was honored exactly as written even
though the actual value (53.3%) is close enough that a motivated reading could have been tempted
to call it "close enough, basically resolved" — it was not rounded down. The substantial
per-lake improvement is reported prominently (not buried) precisely because it is real and
informative, not to soften an inconvenient CRITERION_INVALID label.

**Anticipated FALSIFIED-equivalent concern:** "the hand-implemented Pettitt's test could have a
subtle bug that happens to produce this specific pattern." **Response: Mitigated** — 4 dedicated
validation tests (2 positive control directions, white-noise calibration, degenerate constant
case) all pass, run and reported BEFORE the real experiment's own results, matching this
project's established precedent for `ar1_surrogate`/`iaaft_surrogate`.

## EstimandOps — What This Does NOT Mean (restated per claim.md)

1. Does NOT retroactively validate or invalidate `H-B3-1`/`H-B3-1b`'s own `CRITERION_INVALID`
   verdict on the original single-condition rule.
2. Does NOT generalize to the 5-series population used in `H-B3-1g-k`.
3. Does NOT establish that Pettitt's test (or change-point tests generally) cannot fix the floor
   problem — it made real, substantial progress at 2/3 lakes; the result is population-specific
   insufficiency (Loch Leven), not mechanism failure.
4. `CRITERION_INVALID` here is NOT evidence against TDA-leads-classical-EWS as a claim — per the
   FL Step 4a hard rule, restated explicitly because this is the second consecutive
   `CRITERION_INVALID` verdict in the `H-B3-1*` arc's history (the first being `H-B3-1`/`H-B3-1b`
   itself) and the two must not be conflated as "tried twice, failed twice" — they are different
   detection rules with different, independently-diagnosed floor problems.

## Pearl Card Update

**Closes H-B3-1b's Relaxation Map Row 2 — the last of its 3 originally-named fixes.** All three
rows are now tried: Row 1 (surrogate null) REJECTED cleanly; Row 2 (this experiment, change-point
co-requirement) CRITERION_INVALID with substantial partial improvement; Row 3 (peak-tau,
`H-B3-1l`) CONFIRMED-with-confound. None produced a clean PROMOTE — a useful, honest summary for
anyone considering further investment in the original 3-lake `H-B3-1`/`H-B3-1b` population's
threshold-based detection-rule framing specifically (the 5-series `H-B3-1g-k` population and its
own conjunction-based approach, `H-B3-1h`, remain the strongest surviving result in this bridge).
