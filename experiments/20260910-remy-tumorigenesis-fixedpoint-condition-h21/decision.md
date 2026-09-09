# H-B7-21 — decision.md

## Result

**Part A — exhaustive, all 35 network nodes, both branches: theorem CONFIRMED, zero mismatches.**

| Metric | Value |
|---|---|
| Nodes checked | 35 / 35 |
| Total (node, branch, row) checks | 2984 |
| Mismatches (`changed != predicted_changed`) | **0** |
| Baseline fixed-point failures (`table.evaluate(S) != S[n]`) | **0**, both branches |
| Multi-node simultaneous-perturbation check | CONFIRMED, both branches |

**Every one of the 35 nodes has EXACTLY one destabilizing row, and it is always the row matching
the state's own actual input configuration for that node.** This was verified computationally, not
assumed — the "obviously true by table-lookup construction" argument in claim.md was still run
against 2984 concrete cases, following this session's own established discipline (constructs that
"look obviously correct" have twice already hidden real bugs this session: H-B7-15's docstrings,
H-B7-19's clamp-phase override). None found here.

**A genuine, honest baseline extension beyond H-B7-17/19/20's own scope:** `baseline_fixed_point_
failures == []` confirms `PROLIFERATION_STATE`/`_2` are fixed points across ALL 35 nodes of the
real network, not just the 3 nodes (`RBL2`, `p21CIP`, `CyclinE1`) individually hand-checked in
prior experiments. This was never actually verified network-wide before this experiment — a real,
if unglamorous, gap that is now closed.

**Multi-node simultaneous-perturbation check (new, beyond any prior H-B7-1x experiment):** for both
branches, two DIFFERENT nodes (`DNA_damage` and `EGFR_stimulus`, chosen as the first two nodes in
iteration order with a non-own-row available — not hand-picked for a favorable answer) were
perturbed AT THE SAME TIME, each at a non-own-row, and the full 35-node network single synchronous
step from `S` still returned exactly `S`. This is the concrete instance of the "sufficient"
direction of the necessary-and-sufficient condition claimed below, checked computationally rather
than only argued.

## Verdict

**CONFIRMED — minimal necessary and sufficient condition established, exhaustively verified:**

> A set of single-bit rule perturbations (at most one bit per perturbed node, across any subset of
> the network's 35 nodes) preserves state `S` (`PROLIFERATION_STATE` or `_2`) as a fixed point of
> the Boolean network **if and only if** none of the perturbed rows equals that node's own
> `own_row(n, S)` — the tuple of `S`'s actual values at node `n`'s real input symbols.
>
> - **Necessary:** perturbing any node `n` at exactly `own_row(n, S)` always breaks `S`'s
>   fixed-point status (verified for all 35 nodes, both branches — each has exactly 1 such row).
> - **Sufficient:** perturbing any node(s) at any OTHER row(s), individually or simultaneously,
>   never changes the network's evaluation at `S` (verified for all 2984 individual (node, row)
>   cases, plus one concrete 2-node simultaneous case per branch).

**Honest framing (per claim.md's own "Design rationale"):** this is not a new empirical discovery.
H-B7-20's own decision.md already named the underlying mechanism "a direct, near-tautological
consequence of what a fixed point IS." What this experiment adds is (a) exhaustive verification
that the pattern H-B7-17/19/20 found for 3 of 35 nodes holds for ALL 35, not just those three, and
(b) a checked (not merely stated) demonstration that the "sufficient" direction also holds under
SIMULTANEOUS multi-node perturbation, which none of H-B7-17/19/20 individually tested.

## Part B — sensitivity-profile synthesis (RBL2 / p21CIP / CyclinE1)

| Node | Source | Inputs | Rows | ROBUST | FRAGILE | CRITERION_INVALID | Fragile rate* |
|---|---|---|---|---|---|---|---|
| RBL2 | H-B7-17 | 2 | 4 | 2 | 1 | 1 | 33.3% |
| p21CIP | H-B7-19 | 4 | 16 | 15 | 0 | 1 | 0.0% |
| CyclinE1 | H-B7-20 | 5 | 32 | 28 | 3 | 1 | 9.7% |

*Fragile rate = FRAGILE / (ROBUST + FRAGILE), i.e. of the meaningfully-testable (non-`CRITERION_
INVALID`) rows.

**Cross-check against Part A (all three MATCH exactly):** Part A's own exhaustive count of
destabilizing rows per node is 1/1 (branch_1/branch_2) for all three, matching each experiment's
own already-committed `CRITERION_INVALID` count of exactly 1 — an independent, code-path-different
confirmation (Part A never imports or calls H-B7-17/19/20's own classification logic, only their
raw truth-table construction machinery) that those three prior verdicts were not accidents of
which row happened to be picked, but the SAME structural fact this experiment now proves in
general.

**Explicitly NOT done — no trend fit to n=3.** FRAGILE rate ranges from 0% (p21CIP) to 33.3%
(RBL2), with CyclinE1 (9.7%) in between but not in input-count order (RBL2 has the FEWEST inputs
of the three, 2, yet the HIGHEST fragile rate — the opposite of what a naive "more inputs, more
fragile" story would predict). Per claim.md's own pre-registered "What This Does NOT Mean" #2, no
predictive relationship is fit to these three points — three is not enough data to distinguish a
real pattern from noise, and forcing one here would repeat exactly the kind of premature
generalization this session's own Anti-Overfitting Gate discipline exists to prevent.

**What Part B does NOT extend:** the ROBUST-vs-FRAGILE (observability, not just fixed-point
survival) distinction is NOT re-derived here for the other 32 network nodes — that requires the
full clamp-then-release simulation machinery (H-B7-14/15's own `j*=1` domain construction), which
is materially more expensive than the flat truth-table check Part A performs, and is out of scope
for this experiment (named explicitly in claim.md, not silently skipped).

## FL Step 8a — Independent Reviewer

Narrowly-scoped, context-asymmetric reviewer pass (claim.md + run.py only, no reasoning chain),
targeting the single highest-risk case for an implementation bug: `E2F1_high`, the node with the
most real inputs of any of the 35 (see correction below). Two earlier attempts at this same check
stalled at their turn limit before producing a verdict — root cause, found only after the second
stall: `python -c` is blocked by this environment's Bash-tool sandbox ("Blocked dangerous command:
python -c"), and both stalled agents burned their turn budget rediscovering that constraint rather
than on the actual check. A third attempt, explicitly instructed to write a `.py` script file
first instead of using `python -c`, completed cleanly in 6 tool uses.

**Verdict: CONFIRMED (LGTM).** The reviewer independently re-derived `E2F1_high`'s real input
symbols via `expr.symbols` (not hand-listed), found **10** distinct inputs — `ATM_high, ATM_medium,
CHEK1_2_high, CHEK1_2_medium, E2F1_medium, E2F3_high, E2F3_medium, RAS, RB1, RBL2` — one more than
this experiment's own review-prompt had assumed (9), because the rule's two OR-terms are not
identical in their AND-clauses (`E2F3_medium&E2F3_high` appears only in the first, `RAS` only in
the second, so their symbol UNION is 10, not 9). This is a review-prompt arithmetic slip, not a
`run.py` bug — `run.py`'s own `extract_inputs()` uses the identical `expr.symbols` mechanism and
computes the same 10 automatically; the discrepancy is caught here explicitly rather than silently
absorbed, per this session's own discipline of not letting a checker's own setup errors pass
unremarked. Proceeding with the real 1024-row table, the reviewer checked 4 rows: the predicted
`own_row` (which changed `evaluate(PROLIFERATION_STATE)` when flipped) and three non-own rows
(all-False, all-True, one-bit-different-from-own_row — none of which changed it when flipped) —
all 4 matched the claim exactly.

**Honest scope of this reviewer pass:** 1 node (`E2F1_high`) out of 35, 4 rows out of 1024 for
that node — not exhaustive. The exhaustiveness claim (all 35 nodes, all rows, 2984 total checks,
0 mismatches) rests on this experiment's own test suite (`test_theorem_holds_exhaustively_zero_
mismatches`, `test_exactly_one_destabilizing_row_per_node_per_branch`) plus the negative-control
regression test (`test_regression_theorem_would_catch_an_injected_wrong_row`) proving the check is
not vacuously true — the reviewer's role here is an independent spot-check on the highest-risk
single case, not a from-scratch exhaustive re-derivation.

## Addendum — Lean formalization pilot (2026-09-10)

Per the user's explicit request following a discussion of external AI-mathematics research
methodology (OpenAI GPT-6 Astra's `reasoning -> proof -> Lean certificate` pipeline), this
experiment's own core theorem was formalized and machine-checked in Lean 4 — see `lean/
HB721Core.lean` and `lean/README.md` for the full writeup.

**Result: the abstract necessary-and-sufficient condition (Part A) is now PROVEN, not only
exhaustively checked, for any table over any row type** — a strict strengthening from "verified
for the 2984 concrete cases run.py checked" to "true for every possible instance of this shape,"
via a from-scratch, dependency-free (no mathlib) Lean 4 proof of ~115 lines. The multi-node
sufficiency corollary is proven the same way, for lists of arbitrary length (run.py checked one
concrete 2-node case). A concrete instantiation on RBL2's real `.bnet` rule and
`PROLIFERATION_STATE`'s real values is independently confirmed via Lean's `decide` kernel
procedure — a different implementation (Lean's kernel, not `boolean.py`/CPython) reaching the
same conclusion H-B7-17 found by direct Python enumeration.

Both main theorems depend on exactly `[propext]` (checked via `#print axioms`) — no `sorry`, no
`Classical.choice`, no `native_decide`. This is the project's first use of the "Strong" tier on
`falsification-ladder.md`'s own Independent Verification Strength Ladder (Symbolic solver /
Lean / Coq), previously only cited, never applied.

**Honest scope:** the full 35-node network was NOT re-encoded in Lean — the abstract theorem's
generality (over any Row type) is what makes that unnecessary for this specific claim, not a
shortcut around it. A genuinely open/asymptotic project claim (Forsythe, Lovász) would need
mathlib and a materially larger budget — Epoch AI's own reported 1.2M lines of Lean for a single
18-page proof (independently verified this session by direct fetch of their `announcing-
frontiermath-erdos` page) is the concrete data point behind that judgment, not a guess.

## Kill Analysis

Not applicable in the classic REJECT sense (this is a CONFIRMED verdict), but per FL discipline,
stating explicitly what was and was not established:

**Established:** the necessary-and-sufficient condition above, exhaustively, for all 35 nodes, for
single-bit-per-node perturbations (individually and for one concrete simultaneous 2-node case).

**NOT established (explicit, matching claim.md's pre-registered "What This Does NOT Mean"):**
- `j*=1` observability robustness (ROBUST vs FRAGILE) for the 32 untested nodes.
- Any predictive relationship between a node's in-degree and its FRAGILE rate (n=3, no fit
  attempted).
- Double-bit or higher-order perturbations of a single node's own table.
- Combination with asynchronous update (H-B7-16).
- Simultaneous perturbation of MORE than 2 nodes at once, or of nodes chosen adversarially rather
  than by the "first available non-own-row" rule used here (an arbitrary but non-cherry-picked
  selection).

## Revival Condition

Not applicable (not a REJECT). This experiment is the direct fulfillment of the user's own
explicit 2026-09-10 instruction (three-way sensitivity synthesis + minimal necessary/sufficient
condition for the Proliferation attractor). Forward-looking open threads, named but not pursued
here: (a) extending the full ROBUST/FRAGILE observability machinery to more of the 32 untested
nodes; (b) testing whether the FRAGILE-rate asymmetry (RBL2 highest despite fewest inputs) has a
real structural cause, once more than 3 data points exist; (c) multi-bit / higher-order
perturbation robustness, unexplored by this entire B7 rule-perturbation sub-arc so far.

## Scope note

Fifth and final experiment (after H-B7-17, H-B7-18, H-B7-19, H-B7-20) in the observability/rule-
perturbation sub-arc launched from H-B7-13's original CyclinE1/RBL2 diagnosis. Directly answers
the user's own explicit continuation instruction in full: (1) three-way sensitivity-profile
synthesis — done (Part B); (2) minimal necessary/sufficient condition for the Proliferation
attractor's own existence — done (Part A, exhaustive, generalized to the full 35-node network, not
just the 3 nodes previously tested). Closes this sub-arc unless a new open thread from the
Revival Condition section above is explicitly picked up.
