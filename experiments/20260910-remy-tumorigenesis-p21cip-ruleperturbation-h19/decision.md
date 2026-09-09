# H-B7-19 — decision.md

## Result

**A real bug caught BEFORE running anything, not by the reviewer.** While writing
`simulate_with_table_override`, re-reading the Compute-First Check made clear that the initial
draft would have ignored the clamp's own constant override for `p21CIP` during the `k`-round
clamp phase, substituting the perturbed truth table instead — exactly backward, since `clamp_rule`
already forces `p21CIP` to a constant regardless of its own rule during that phase (the same
reasoning H-B7-17 relied on for `RBL2`). Fixed by using plain, unmodified `h1.synchronous_step`
during the clamp phase and reserving the table-override only for post-release dynamics. A
dedicated regression test (`test_clamp_phase_ignores_override_uses_the_clamp_constant`) locks this
in: a DELIBERATELY WRONG override (constant `True` for every row) is passed, and the clamp phase
is confirmed to still show `p21CIP=False` at the observation point — proving the clamp constant
wins, not the override table.

**Substrate check passed:** the clamp-phase orbit (12 states, 2 branches × k=1..6) is IDENTICAL
across all 17 conditions (baseline + 16 perturbations) — `substrate_check_orbit_unchanged: true`
— confirming the Compute-First Check's prediction directly, not just assuming it.

**Baseline regression-matches H-B7-15/17's own committed numbers exactly**
(M1: `n_collisions_j0=1, n_collisions_j1=0, sufficient_at_j1=true`).

**Exhaustive result, all 16 single-bit perturbations of `p21CIP`'s rule:**

| Classification | Count | Rows |
|---|---|---|
| ROBUST | **15** | all except `flip_FTFT` |
| FRAGILE | **0** | none |
| CRITERION_INVALID (no transition) | **1** | `flip_FTFT` (TP53=False, CyclinE1=True, AKT=False, Growth_inhibitors=True) |

**A striking, clean asymmetry with H-B7-17's own `RBL2` result:** `RBL2`'s 4-row table gave
2 ROBUST / 1 FRAGILE / 1 CRITERION_INVALID (PARTIALLY-ROBUST). `p21CIP`'s 16-row table gives
15 ROBUST / 0 FRAGILE / 1 CRITERION_INVALID — every SINGLE meaningfully-testable perturbation of
`p21CIP`'s rule preserves `j*=1` sufficiency. The two clamped nodes are NOT symmetric in how
fragile their own rule structure is to single-bit truth-table perturbation.

## Verdict

**ROBUST**, per claim.md's own pre-registered kill criterion (`j*=1` sufficiency survives ALL
meaningfully-testable perturbations — here, all 15 of 15 with a real transition to detect).

**Sharpest defensible statement:**

> Within this Boolean model, `j*=1` sufficiency of `{Growth_arrest, Proliferation}` is fully
> robust to every single-bit truth-table perturbation of `p21CIP`'s own rule that leaves the
> underlying transient-escape phenomenon intact (15 of 16; the 16th abolishes the phenomenon
> itself, uninformative either way, same discipline H-B7-17 established for `RBL2`). This is a
> materially stronger robustness result than `RBL2`'s own (2 of 3 meaningfully-tested), suggesting
> the observability mechanism is NOT equally sensitive to perturbing either clamped node's rule —
> `p21CIP`'s specific logical form matters less to the `j*=1` finding than `RBL2`'s does.

## FL Step 8a — Independent Reviewer

Narrowly-scoped, context-asymmetric reviewer pass (single script, one invocation), targeting the
two most load-bearing rows: the one `CRITERION_INVALID` case (`flip_FTFT`) and one representative
`ROBUST` case (`flip_TTTT`, all-True row). **Both `[CONFIRMED-REAL]`** — reproduced the exact
same floor/M1 collision counts and classification for both, using the real functions imported
from `run.py`, not reimplemented.

**Honest scope limitation, stated by the reviewer itself and accepted here rather than chased
further:** this confirms 2 of 16 rows, not all 16 — the reviewer explicitly flagged this as a
scope note, not a defect, since the code path is identical and deterministic for every row (a
fixed function of `floor_j0`/`M1_j1`, no per-row special-casing). Combined with this experiment's
own test suite, which DID exhaustively verify the underlying truth-table CONSTRUCTION against the
hand-derived factored form for all 16 rows
(`test_table_construction_matches_hand_factored_form_all_16_rows`), the residual unverified
surface is narrow: the classification LOGIC (verified on 2 representative outcomes) applied to a
table CONSTRUCTION (verified exhaustively) — accepted as sufficient rather than re-running the
reviewer a second time for marginal additional confidence, per Cheapest Differentiating Test
discipline (a third reviewer pass checking more of the same deterministic function would not be
differentiating).

## Kill Analysis (Anti-Overfitting Gate)

**What was killed:** the possibility (open before this experiment) that `p21CIP`'s rule structure
is AS fragile to perturbation as `RBL2`'s — it is not; it is decisively more robust.

**What was NOT killed:** `RBL2`'s own PARTIALLY-ROBUST result (H-B7-17) stands unchanged — this
experiment does not retest `RBL2`, only `p21CIP`.

**Relaxation Map:**
- **Remove** the "p21CIP only" restriction: `CyclinE1`'s own rule (32-row table, the other named
  feedback-loop component) remains the one clamped-adjacent node never tested — still the
  cheapest, most mechanistically-motivated next step (would need the same table-based approach
  used here, scaled to 32 rows, entirely feasible with the machinery already built).
- **Weaken:** investigate WHY `flip_FTFT` specifically abolishes the transition (mirroring
  H-B7-18's own investigation of `RBL2`'s analogous case) — not attempted here, a cheap, named,
  concrete follow-up given H-B7-18 already built the exact methodology for this kind of question.

## Revival Condition

Not applicable (not a REJECT). Forward-looking: `CyclinE1`'s rule perturbation (32 rows) is now
straightforwardly tractable using this experiment's own `TableRule`/`build_domain` machinery,
reusable with only the input-symbol list and target node name changed.

## Scope note

Third rule-perturbation experiment in the observability sub-arc (H-B7-17: `RBL2`, H-B7-18:
mechanistic explanation of `RBL2`'s one fragile case, H-B7-19: `p21CIP`, this experiment).
Completes single-bit perturbation testing of BOTH clamped nodes; `CyclinE1`'s rule (the third
named feedback-loop component) remains the one open, larger-scale target.
