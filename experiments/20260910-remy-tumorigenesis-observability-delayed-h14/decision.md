# H-B7-14 — decision.md

## Result

**Regression/continuity check (Substrate Gate) passed:** `j=0` reproduces H-B7-13's own committed
`metrics/run.json` collision counts exactly (M1: 1 collision, M2: 1 collision — `matches_h_b7_13:
true`), and `test_j0_reproduces_h_b7_13_release_state_exactly` confirms the new delayed-observation
function's `j=0` output is byte-identical to H-B7-13's own `release_state`, per-entry, for a spread
of k values. The new function did not silently change H-B7-13's already-verified behavior.

**Sweep result — clean, fast resolution, both candidates:**

| j | Floor (`DNA_damage`) | Ceiling (full state) | M1 (`{Growth_arrest,Proliferation}`) | M2 (`+{p21CIP,RBL2}`) |
|---|---|---|---|---|
| 0 | insufficient | sufficient | **insufficient** (H-B7-13) | **insufficient** (H-B7-13) |
| 1 | insufficient | sufficient | **sufficient** | **sufficient** |
| 2, 3, 4, 5, 7, 10 | insufficient | sufficient | sufficient | sufficient |

`first_sufficient_j`: M1 = **1**, M2 = **1**. Floor stays insufficient across the entire sweep (as
expected — `DNA_damage` is a branch input, constant regardless of `j`). Ceiling stays sufficient
throughout (tautological, as expected).

**Directly verified on raw output (not just the aggregate collision count), per this session's own
"inspect raw diagnostic output before trusting a summary number" discipline** — a small diagnostic
script (`diag_h14_verify_j1.py`, scratchpad, not part of the committed repo) printed the actual
marker values for branch 1, k=3/4/5, at j=0 and j=1:

```
k=3 j=0: Growth_arrest=False Proliferation=False -> final fate=GROWTH_ARREST
k=3 j=1: Growth_arrest=False Proliferation=False -> final fate=GROWTH_ARREST
k=4 j=0: Growth_arrest=False Proliferation=False -> final fate=GROWTH_ARREST
k=4 j=1: Growth_arrest=False Proliferation=False -> final fate=GROWTH_ARREST
k=5 j=0: Growth_arrest=False Proliferation=False -> final fate=PROLIFERATION   <- the collision (H-B7-13)
k=5 j=1: Growth_arrest=False Proliferation=True  -> final fate=PROLIFERATION   <- resolved
```

`Proliferation` flips to `True` for k=5 exactly at `j=1`, while staying `False` for k=3/4 — a real,
directly-observed divergence, not an artifact of the aggregate collision-counting logic.

## Verdict

**RESOLVED-QUICKLY**, per claim.md's own pre-registered kill criterion (`j* ≤ 3`). H-B7-13's own
mechanistic diagnosis ("the observable readouts lag the trajectory's actual committed fate by
roughly one synchronous step") is confirmed almost exactly: `j*=1` for BOTH candidates. Notably,
the SMALLER marker set (M1, just the 2 phenotype nodes) resolves at the same `j*` as the augmented
M2 — the `p21CIP`/`RBL2` addition tested in H-B7-13 turns out not to have been the missing
ingredient; waiting one more step was.

**Corrected claim, replacing H-B7-13's own negative one:** a release policy that waits ONE
synchronous step after clamp removal before reading `{Growth_arrest, Proliferation}` alone (no
augmentation needed) correctly and exactly distinguishes safe (`k≤4`) from unsafe (`k≥5`) release,
across the full tested domain (both branches, `k=1..40`).

## Kill Analysis (Anti-Overfitting Gate) — applies to H-B7-13's REJECTED claim, now superseded

**What was killed (by H-B7-13, and NOT revived by this experiment):** the specific claim that M1
or M2, observed AT THE INSTANT of release (`j=0`), are sufficient. This experiment does not
challenge or retest that — `j=0` reproduces the exact same collision, unchanged.

**What is NEW here, surviving and CONFIRMED:** M1 (and M2, redundantly) ARE sufficient across the
full tested domain when observed `j≥1` steps after release. This is a genuinely different,
positive claim from H-B7-13's negative one — not a relaxation of H-B7-13's claim in the AOG sense
(this is Minimal Relaxation Rule territory: ONE assumption changed — WHEN, not WHAT, is observed —
producing a new, independently falsifiable, and now-confirmed claim).

**Relaxation Map for what remains untested:**
- **Not yet checked:** whether `j=1` generalizes beyond this specific `k=1..40` domain — e.g. a
  much larger `k` (say `k=100`) might behave differently if the network has richer dynamics not
  explored by the tested range. Cheap to check, not done here (scope discipline: this experiment
  answered exactly the one question it pre-registered).
- **Not yet checked:** robustness to asynchronous updating (same caveat H-B7-13 already named,
  unchanged by this experiment — synchronous throughout).
- **Not yet checked:** whether `j=1` is the SAME across the two branches by coincidence (both
  happened to need exactly 1 step) or because of the already-established branch dynamical
  equivalence (H-B7-12) — plausible the latter, not independently disentangled here.

## Revival Condition

Not applicable in the REJECT sense — this experiment did not reject a claim, it CONFIRMED one
(the delayed-observation variant). The "hard rule" here is forward-looking, not backward:

- **Next natural extension (named, not attempted):** does `j=1` remain sufficient if the domain is
  widened (larger `k`, or a genuinely different perturbation target, not just `p21CIP`/`RBL2`)? A
  cheap follow-up given the machinery is now fully in place (a one-line change to `TESTED_DURATIONS`
  or `CLAMPS`).

## FL Step 8a — Independent Reviewer Verdict (mandatory for this PROMOTE-shaped result, per
skeptic-triggers.md Trigger 2: surprising clean success after a REJECT)

An independently-invoked `Agent(reviewer)` was given exactly 2 narrowly-scoped, checkable claims
(context-asymmetric: `claim.md` + code + the two `metrics/run.json` files only, no reasoning chain
or session history) and told to try to BREAK them, not confirm them:

- **Check 1 (regression correctness, j=0 vs H-B7-13):** independently re-ran
  `build_domain_for_j(..., j=0)` + `find_collisions`, bypassing `cmd_run()`. **CONFIRMED** — not
  just a count match (`M1=1, M2=1` collisions), the actual colliding `(branch, k, fate)` members
  matched H-B7-13's own committed collision exactly.
- **Check 2 (j=1 sufficiency across the full domain):** wrote a standalone verification calling
  `simulate_transient_clamp_multi_with_delayed_observation(..., j_steps=1)` directly for k=1..40 on
  both branches (80 rows, not sampled). **CONFIRMED** — `n_collisions=0`; the reviewer's own words:
  "the mechanism is visible directly in the data... a real, mechanistically legible resolution, not
  a coincidence of the sampled range."

**Verdict: `[CONFIRMED-REAL]`** — no counter-example found on either check. Promoted freely, per FL
Step 8a's own Response Matrix.

## Skeptic Concerns (self-review, predating the independent reviewer pass above — kept for the
audit trail; the independent pass superseded these as the load-bearing verification)

- "Could `j=1` sufficiency be a coincidence of this specific 2-branch, `k=1..40` domain, not a real
  structural fact about the network?" → **Accepted limitation, named above** in the Relaxation Map
  — not independently checked against a wider domain in this experiment.
- "Is the collision-resolution genuinely about `Proliferation` becoming legible, or could it be an
  artifact of `find_collisions`' grouping logic (reused unchanged from H-B7-13, already tested
  there)?" → **Checked, dismissed**: the raw diagnostic output above shows the actual boolean flip
  directly (`Proliferation: False→True` for k=5 specifically, unchanged for k=3/4) — not inferred
  from the collision count alone.
- "Does `j=1` sufficiency actually help a REAL release decision, given you have to wait 1 step
  either way?" → **Accepted limitation, explicitly named in claim.md § What This Does NOT Mean
  (item 1)** — this is a weaker guarantee than instant observability and should be reported as
  such, not oversold as equivalent to H-B7-13's original (failed) instant-observability goal.

## Scope note

Second step of the observability sub-arc within Bridge 7, direct continuation of H-B7-13 via
Minimal Relaxation Rule (user's own explicit instruction, 2026-09-10: "наблюдай маркеры через j
шагов после снятия клэмпа"), exactly the Revival Condition H-B7-13's own decision.md named as the
cheapest, most-likely-to-succeed next step. Confirmed as stated.
