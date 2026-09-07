# decision.md — H-B3-1l (peak-tau reporting, H-B3-1b's Relaxation Map Row 3)

## CORRECTION ADDENDUM (2026-09-07, FL Step 8a skeptic pass — sixth in a row, session-wide)

**Verdict downgraded CONFIRMED → WEAKENED, more seriously than the original confound already
implied.** Original text kept unedited below (Hindsight Distortion Gap discipline). Sixth
`Agent(skeptic)` invocation in the same `/loop` continuation (fifth on bridge B2, first on
bridge B3) — explicitly told the original author had ALREADY caught and disclosed the
negative-control confound, and asked to find something NOT already caught, not just repeat it.
It did.

**Finding 1 — a mechanistic explanation for the confound (plausible, NOT yet empirically
confirmed):** `expanding_kendall_tau`'s early Kendall-tau values are noisier (sampling variance
shrinks roughly as `1/k`), so `argmax` is structurally pulled toward early indices. This bias is
NOT equal across signal families: `rolling_stat` (AC1/variance) changes smoothly between
adjacent windows (they share `window−1` points), producing a smooth, weakly-spiking tau
trajectory; `betti1_entropy_series` reduces each window through a full Vietoris–Rips → H1
diagram → entropy pipeline, where one new/dropped point can discontinuously add or remove a
topological feature — a much jumpier, more early-spiking tau trajectory. Predicted consequence:
TDA's argmax should land systematically earlier than classical's on ANY series, mechanism or no
mechanism — matching the observed all-3-lakes pattern exactly. **Not yet verified empirically**
(the skeptic's own suggested check — run this same peak-lead comparison on ~500 AR(1) surrogates
of Lower Zurich and see whether the median gap already reaches ~50 months — was not run this
pass; flagged in Relaxation Map, not treated as proven).

**Finding 2 — independently VERIFIED, not speculative:** the code selects
`classical_peak_date_used` differently for Lower Zurich (whichever of AC1/variance is CLOSEST to
the known transition — an oracle-informed choice using the answer being tested) than for the
negative controls (`min(...)`, the earliest of the two — the harder bar). Checked directly
against `metrics/run.json`: on Lower Zurich, `classical_ac1_peak_date = 1999.25` — **which is
BEFORE `tda_betti_peak_date = 2000.5`.** AC1 alone, a legitimate classical EWS statistic, already
peaked earlier than TDA on the one positive case. The reported "TDA leads classical" framing is
true only relative to the OTHER classical statistic (variance, 2004.67), selected specifically
because it happened to sit closer to the transition. **The CONFIRMED verdict is conditional on
which classical statistic the oracle-informed rule happens to pick, not on TDA outperforming
classical EWS as a family.**

**What survives:** the raw peak dates themselves (real, computed correctly) and the fact that
this design does sidestep the ORIGINAL threshold-crossing floor problem (CRITERION_INVALID from
`H-B3-1`/`H-B3-1b`) — that specific failure mode is genuinely avoided. **What does NOT survive:**
"TDA's peak genuinely anticipates the real transition better than classical's peak does" as an
unqualified claim — one classical statistic (AC1) already beat TDA on the only positive case
tested, and a plausible (not yet confirmed) structural mechanism could explain the entire
negative-control confound without any real signal at all.

**Corrected honest statement:** *On Lower Zurich, TDA's peak (2000.5) is closer to the documented
transition (2002.0) than the CLOSEST of the two classical statistics (variance, 2004.67) — but
AC1 alone (1999.25) already peaked before TDA. The "TDA leads classical" framing depends on which
classical statistic is selected for comparison, using knowledge of the answer being tested. A
structural mechanism (differential early-argmax bias between smooth and jumpy tau trajectories)
plausibly explains the entire observed pattern, including the positive case, without invoking any
real transition-detection ability — not yet empirically ruled out.*

**Response Matrix disposition:** Confirmed (Finding 2, HIGH confidence, independently verified
against committed data), Plausible-not-yet-confirmed (Finding 1, would need the AR(1)-surrogate
check named in Relaxation Map), Weak/non-diagnostic (the identical +8.0-month coincidence — the
skeptic's own Finding 3, kept as a minor open item, not load-bearing).

**Corrected Relaxation Map priority:** the AR(1)-surrogate peak-lead-gap check (already named
below, previously treated as one option among several) is now the SINGLE highest-priority
follow-up — it would directly test Finding 1's mechanism and could settle whether Lower Zurich's
+50.0-month lead is distinguishable from a pure floor artifact at all.

---

## Result (ORIGINAL TEXT, superseded in interpretation by the correction above — kept for the audit trail)

**Verdict: CONFIRMED (per the literal pre-registered criterion) — but with a serious,
pre-registered confound found in the negative controls that substantially weakens the practical
interpretation.**

| | TDA peak date | Classical peak date (best case) | Distance to transition (2002.0) |
|---|---|---|---|
| Lower Zurich (transition ≈2002) | 2000.5 | 2004.67 (var) | TDA: 1.5y **vs** classical: 2.67y |

TDA's peak is closer to the documented transition than classical's best-case peak, AND occurs no
later than it (2000.5 ≤ 2004.67) — literally satisfies the pre-registered CONFIRMED criterion.

## The Confound — Found Because the Design Anticipated Looking For It

`claim.md` pre-registered a qualitative check for exactly this failure mode: *"does
Windermere/Loch Leven [negative controls, no real transition] show the SAME directional bias as
Lower Zurich — which would suggest a structural artifact of the two statistics' smoothing
properties rather than a real signal?"*

**Answer: yes, on both.**

| | TDA peak date | Classical peak date | `peak_lead_months_tda_minus_classical` |
|---|---|---|---|
| Lower Zurich (positive) | 2000.5 | 2004.67 | **+50.0** |
| Windermere (negative) | 1989.75 | 1990.42 | **+8.0** |
| Loch Leven (negative) | 1999.25 | 1999.92 | **+8.0** |

TDA's peak precedes classical's peak on **all three lakes**, including the two with no documented
transition at all. The negative controls' lead (+8.0 months, suspiciously IDENTICAL to full
floating-point precision on both, unexplained — see Open Questions) is smaller in magnitude than
Lower Zurich's (+50.0), but shares the exact same sign. This is consistent with "TDA's peak
generically occurs earlier than classical's peak, independent of whether a real transition is
present" being at least a partial driver of the Lower Zurich result — not proof the Lower Zurich
finding is purely an artifact (the magnitude IS much larger there, and it IS closer to the true
transition), but enough to prevent a clean, confident CONFIRMED reading.

## What Was Confirmed

- [x] The literal pre-registered criterion (TDA peak closer to the true transition, and not
  later than classical's) — satisfied on Lower Zurich.
- [x] The pre-registered confound check itself did its job: built into the design BEFORE running
  (not a post-hoc rescue), and it surfaced a real, informative caveat rather than a clean
  positive result.
- [x] `H-B3-1b`'s Relaxation Map Row 3 is no longer untested — peak-tau reporting has now been
  tried, and unlike Row 1 (surrogate null, cleanly REJECTED), this produces a genuinely mixed
  result requiring a qualifier, not a clean binary outcome.

## What Remains Open

- **Why is the negative-control lead EXACTLY +8.0 months on both Windermere and Loch Leven?**
  Not explained by this experiment. Candidates: (a) a genuine, generic property of how Betti-1
  persistence entropy's expanding-tau trajectory shape differs from AC1/variance's (plausible —
  entropy of a topological summary and a linear autocorrelation statistic could have
  systematically different "settling" dynamics under a rolling window, independent of any real
  transition); (b) a coincidence of the specific two series' sampling grids; (c) an artifact of
  `expanding_kendall_tau`'s shared `min_points=8` floor interacting identically with two
  differently-shaped but similarly-lengthed series. Not diagnosed here — a genuine open question,
  not swept aside.
- Whether the SAME confound would appear on the 5-series population used in `H-B3-1g-k` is
  untested (explicit scope decision in `claim.md` — this experiment used the original 3-lake
  population only).

## Relaxation Map

- **Diagnose the +8.0-month coincidence directly** — plot or inspect the raw tau trajectories for
  Windermere/Loch Leven to see whether the mechanism is shared smoothing-lag or a coincidence.
- **Combine peak-reporting WITH a surrogate null** (per `claim.md`'s own explicit scope note) — a
  peak-lead distribution over AR(1)/IAAFT surrogates would tell whether Lower Zurich's +50.0
  month lead is statistically distinguishable from the generic +8.0-month baseline observed on
  the negative controls, resolving the confound quantitatively instead of qualitatively.
- **Row 2 of H-B3-1b's own Relaxation Map** (change-point co-requirement, Pettitt's test) remains
  the one item never tried at all across the whole `H-B3-1*` arc.

## Note on Floor–Ceiling (FL Step 4a)

Not applicable in the arm/null-model sense as originally scoped — this experiment deliberately
removes statistical machinery (no surrogate null, no threshold) per Row 3's own wording. The
Relaxation Map above names the natural way to add a floor back in (surrogate-null peak-lead
distribution) as a concrete follow-up, not as evidence this run is invalid as designed.

## FL Step 8a — Skeptic Pass

Not run as a separate agent invocation (Evaluator-Optimizer cap still in effect session-wide).
Manual discipline applied: the exact confound a skeptic would be expected to find (negative
controls sharing the positive's directional bias) was built into the pre-registered design and
is reported prominently, not discovered after the fact and downplayed. The verdict is stated as
literally CONFIRMED per the pre-registered criterion, with the confound given equal prominence —
neither suppressed nor allowed to silently downgrade the verdict without explanation (that would
be its own kind of dishonesty, changing a pre-registered decision rule after seeing the data).

**Anticipated FALSIFIED-equivalent concern:** "CONFIRMED is misleading given the negative-control
confound — this should just be called REJECTED or AMBIGUOUS." **Response: Accepted as a valid
critique of headline labeling, mitigated by presentation** — the verdict field literally reports
what the pre-registered criterion says (CONFIRMED), but every summary of this result (this file's
own title, `activeContext.md`, `LAB.md`) must carry the confound qualifier, never citing
"CONFIRMED" alone. This is now an explicit written rule for anyone citing `H-B3-1l`.

## EstimandOps — What This Does NOT Mean (restated per claim.md)

1. Does NOT retroactively validate or invalidate `H-B3-1`/`H-B3-1b`'s own `CRITERION_INVALID`
   verdict on the threshold-crossing rule.
2. Does NOT generalize to the 5-series population used in `H-B3-1g-k`.
3. Does NOT establish causality or mechanism.
4. Does NOT stand as a strong, standalone confirmation — the negative-control confound means this
   result should be read as "suggestive, worth a quantitative surrogate-null follow-up," not as
   settled evidence that TDA's peak timing meaningfully anticipates real transitions.

## Pearl Card Update

**Closes H-B3-1b's Relaxation Map Row 3** with a genuinely mixed, non-clean-binary result — a
useful counter-example to the pattern where every prior `H-B3-1*` variant produced a clean
REJECT. The unexplained identical +8.0-month negative-control lead is flagged as its own open
question (not yet pearled separately — see Relaxation Map; would need a concrete
falsifiable_prediction about the mechanism before it earns a registry row of its own).
