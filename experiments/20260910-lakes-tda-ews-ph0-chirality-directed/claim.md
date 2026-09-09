# H-B3-2 — claim.md

## Origin

Route 3 of the user's 2026-09-09 direction-scoping report: "проверить потерю направления
времени." Bridge 3's closed arc (H-B3-1 through H-B3-1p, informative negative, ADR-090-era
closure) used H1 Vietoris-Rips persistence on a Takens embedding of each rolling window as
its TDA statistic. The user's claim: this construction cannot distinguish a window from its
own time-reversal, because it depends only on pairwise distances between embedded points,
which time-reversal permutes but does not change.

**Source Trace (FL Step -4):** Yuliy Baryshnikov, "Time Series, Persistent Homology and
Chirality" (2022-12-05, University of Illinois). Fetched and read directly (WebFetch +
local PDF extraction, not a snippet). Central finding relevant here: the paper's own
"chirality" construction is **0-dimensional persistent homology (PH_0) of the raw scalar
function** (via its merge tree), NOT H1 on a Takens-embedded point cloud -- a structurally
different, simpler construction than anything Bridge 3 has used. A bar `(b,d)` corresponds
to a coupled local-minimum/local-maximum pair `(s,t)` with `f(s)=b`, `f(t)=d`; it is type
**"L"** (labeled Л in the paper) if the minimum precedes the maximum (`s<t`), and type
**"N"** otherwise (`s>t`) (Definition 2.6). The paper explicitly notes (Remark 2.7) that
chirality is a natural tool for time-reversal asymmetry, and (Section 4) that a positive
drift should produce an excess of N-type bars over L-type.

## Mechanism Claim Gate (Step 0a) — checked BEFORE building anything else

**Triggering sentence:** "the existing H1-VR-on-Takens-embedding statistic (`betti1_entropy_series`
/ `betti1_total_persistence_series`, `20260906-may1972-tda-ews-obrienlakes/run.py`) gives
an IDENTICAL diagram for a window and its time-reversal."

**Check:** direct numerical test (`diag_time_reversal_h1.py`, this session) -- 5 independent
random windows (with trend, matching real-series character), each embedded forward and
reversed, H1 diagrams computed via the arc's own unchanged `takens_embed` + `ripser` call.
**HOLDS exactly** -- diagrams are byte-identical (not merely close) across all 5 trials, in
both shape and sorted values. This is not a numerical coincidence of small sample size; it
follows from the embedding's own structure (reversing the window's index order reverses the
POINT ORDER in the embedded cloud, and a point cloud's Vietoris-Rips persistence depends
only on the pairwise-distance matrix, which reordering points leaves unchanged as a
multiset of distances). Confirmed, not merely asserted.

**Consequence:** this does NOT explain why Bridge 3's H1-VR statistics failed to reliably
lead classical EWS (many other explanations remain, per Bridge 3's own closure) -- it
establishes ONE thing precisely: whatever information the TDA statistic captured, it could
not have been distinguishing "approach to transition" from "recovery from transition"
purely on the basis of within-window temporal ORDER, since that information is provably
discarded by the H1-VR-on-embedded-cloud construction as used.

## EstimandOps L0

**Question type:** Descriptive/predictive comparison. "Does a genuinely order-sensitive TDA
statistic (PH_0 chirality excess, computed on the raw scalar window, no embedding needed)
provide additional discriminating information beyond (a) a simple rolling trend/slope
statistic and (b) a classical time-reversal-asymmetry statistic, for detecting approach to
a real ecological regime shift -- at a MATCHED false-positive rate, on real lake data
(O'Brien et al., the same Lower Zurich/Windermere/Loch Leven series H-B3-1 used)?"

## The chirality-excess statistic (implemented per Definition 2.5/2.6, not reinvented)

For each rolling window (same `WINDOW_FRAC=0.5` convention as the arc's own classical/H1
statistics, reused unchanged): find all local minima and local maxima of the raw scalar
series in that window (simple derivative-sign-change detection); pair them via the
merge-tree/Elder-rule procedure (a local min pairs with the nearest-in-height local max it
"tops," per the paper's own recursive stem-pruning definition -- implemented directly, not
approximated); classify each pair as L (min-time < max-time) or N (min-time > max-time);
report `chirality_excess = (n_N - n_L) / (n_N + n_L)`.

## Baselines (both pre-registered, not chosen after seeing results)

1. **Simple trend:** rolling linear-regression slope of the raw series over the same window.
2. **Classical time-reversal asymmetry:** the standard nonlinear-time-series statistic
   `TR(tau) = mean((x_{t+tau} - x_t)^3)` (Diks et al. 1995 and standard nonlinear TSA
   practice), at `tau=1`, on the same rolling window.

## The claim (falsifiable)

Using the arc's own established detection rule (expanding Kendall tau of each statistic,
threshold `tau>=0.5`, `first_crossing`, reused unchanged) and the arc's own AR(1)-surrogate
false-positive floor check (`ar1_surrogate`/`floor_false_positive_rate`, reused unchanged):

1. **First test (matches the user's own framing):** does chirality-excess cross its
   detection threshold earlier than BOTH baselines on Lower Zurich (the positive control,
   known transition 2002.0), while NOT crossing (or crossing no earlier than the floor) on
   Windermere/Loch Leven (negative controls)?
2. **CONFIRMED (real additional contribution):** chirality-excess leads both baselines on
   the positive control by a nontrivial margin, AND its false-positive floor rate (on
   AR(1) surrogates of the negative-control lakes) is not worse than the baselines'.
3. **REJECTED (closes the idea, per the user's own pre-registered criterion):** chirality
   -excess's lead time is not distinguishable from the simple trend statistic's (i.e. it is
   recoverable from slope alone), OR it merely tracks a sensor/seasonality artifact
   detectable by inspection of its raw trace.

## What this does NOT mean

1. A CONFIRMED verdict here would NOT reopen Bridge 3's own closed finding (the H1-VR
   statistics' informative-negative status) -- chirality-excess is a structurally different
   statistic family, tested here for the first time, not a Relaxation Map variant of the
   H1-VR chain.
2. Does NOT test whether chirality-excess distinguishes "approach" from "recovery" directly
   (the user's own deeper question) -- only whether it adds value over trend/classical
   asymmetry for detecting approach on the available real data. Distinguishing approach vs
   recovery would need real recovery-phase data, not established here to exist for these lakes.
3. Does NOT establish physical recovery is equivalent to a reversed collapse recording --
   the user's own explicit caution, respected here by not claiming otherwise.
