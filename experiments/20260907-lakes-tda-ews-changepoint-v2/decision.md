# decision.md — H-B3-1m (V2 two-part rule: tau AND Pettitt level-shift, H-B3-1b Row 2)

## Result

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
