# H-B7-20 — decision.md

## Result

**Substrate check passed (critical, given the real structural difference from H-B7-17/19):**
the UNPERTURBED (baseline) table-lookup evaluation of `CyclinE1` reproduces H-B7-15's own
symbolic-expression-computed orbit EXACTLY — 7 states/branch, `cycle_period=1` — confirmed via a
dedicated regression test using a DIFFERENT code path (table lookup vs the original boolean.py
expression evaluation) than either prior sibling experiment, giving genuine cross-implementation
confidence, not just internal self-consistency.

**Exhaustive result, all 32 single-bit perturbations of `CyclinE1`'s rule:**

| Classification | Count |
|---|---|
| ROBUST | **28** |
| FRAGILE | **3** (`flip_FFFFF`, `flip_TTTFF`, `flip_TTTTT`) |
| CRITERION_INVALID (no transition) | **1** (`flip_FFTTT`) |

**The key new finding — a systematic, per-row destabilization check, not limited to FRAGILE
rows.** Per the user's own explicit request, EVERY fragile-or-invalid row was checked for
whether `PROLIFERATION_STATE`/`_2` remain fixed points under the perturbed rules (H-B7-18's own
methodology, applied systematically here, not to one hand-picked case):

- The ONE `CRITERION_INVALID` row (`flip_FFTTT`) **IS self-destabilizing** — both branches: no
  longer a fixed point, relapses to a `GROWTH_ARREST`-phenotype attractor.
- **ALL 3 `FRAGILE` rows are `OBSERVABILITY-ONLY`** — both branches remain fixed points under
  every one of them; the Proliferation attractor survives, only the `j*=1` timing-based
  discrimination breaks.

**A precise, mechanistically exact, and now THREE-TIMES independently verified general
principle**, discovered by decoding which specific truth-table row each destabilizing
perturbation corresponds to:

> **For each of the three tested nodes (`RBL2`, `p21CIP`, `CyclinE1`), among all single-bit
> truth-table perturbations, the UNIQUE destabilizing (self-destabilizing / `CRITERION_INVALID`)
> perturbation is EXACTLY the row matching `PROLIFERATION_STATE`'s own actual input
> configuration for that node — never any other row.**

Verified directly, computationally (not by hand alone, after this session's own established
caution around hand-derived bit-string decoding):
- `RBL2` (H-B7-17/18): destabilizing row = `flip_TF_drop_CyclinE1` = `(CyclinE1=True,
  CyclinD1=False)` = `PROLIFERATION_STATE`'s own `(CyclinE1, CyclinD1)` values exactly.
- `p21CIP` (H-B7-19, decoded and computationally re-verified as part of THIS experiment via a
  scratchpad script): destabilizing row = `flip_FTFT` = `(TP53=False, CyclinE1=True, AKT=False,
  Growth_inhibitors=True)` = `PROLIFERATION_STATE`'s own values exactly. Independently confirmed
  the baseline table IS a fixed point and the flipped table IS NOT, on both branches.
- `CyclinE1` (this experiment): destabilizing row = `flip_FFTTT` = `(p21CIP=False, RBL2=False,
  E2F3_medium=True, CDC25A=True, E2F1_medium=True)` = `PROLIFERATION_STATE`'s own values exactly.

**This is not a coincidence needing further explanation — it is a direct, near-tautological
consequence of what a fixed point IS** (a state whose own input row must map to its own output
value under every node's rule; perturbing exactly that row necessarily breaks self-consistency),
but it was NOT obvious in advance which of several candidate rows (only one per node, out of 4,
16, and 32 respectively) would turn out to be the destabilizing one — and the fact that it is
*always exactly the state's own row, never any other*, is the real, informative, now-verified
structural finding, replacing an earlier (wrong, discarded before writing this document) working
hypothesis that fragility correlated with "removing vs adding" a True condition in the abstract
truth table.

## Verdict

**PARTIALLY-ROBUST** for `CyclinE1` (matching H-B7-17's own verdict shape for `RBL2`, unlike
H-B7-19's clean `ROBUST` for `p21CIP`) — but with a materially richer, now fully mechanistically
resolved picture than a bare classification count:

> Robustness of the `j*=1` observability mechanism to single-bit rule perturbation is governed by
> exactly ONE structural fact per node: whether the perturbed row is the Proliferation
> attractor's own defining input row (destabilizes the attractor itself, `CRITERION_INVALID`) or
> any other row (at worst impairs `j*=1` observability while leaving the attractor intact,
> `FRAGILE`/`OBSERVABILITY-ONLY`, or has no effect at all, `ROBUST`). This holds identically
> across all three tested feedback-loop nodes.

## FL Step 8a — Independent Reviewer

Narrowly-scoped, context-asymmetric reviewer pass targeting the two most load-bearing rows (the
one `CRITERION_INVALID` case and one representative `FRAGILE` case): **both `[CONFIRMED-REAL]`**
— exact match on collision counts and destabilization booleans for both rows. Honestly flagged
by the reviewer itself as a code-PATH re-execution (calling this experiment's own functions),
not an independent reimplementation of the underlying Boolean-network semantics from scratch —
accepted as adequate given this experiment's OWN test suite already provides a genuine
cross-implementation check (`test_baseline_orbit_matches_h_b7_15_exactly`, comparing the
table-lookup evaluation against H-B7-15's original symbolic-expression evaluation, a materially
different code path, not just a different invocation of the same one).

## Kill Analysis (Anti-Overfitting Gate)

**What was killed:** an initial (undocumented, discarded before this file was written) working
hypothesis that fragility correlates with the DIRECTION of a truth-table flip (True→False =
"removing" vs False→True = "adding") — `RBL2`'s own destabilizing case was an ADDED row while
`CyclinE1`'s was a REMOVED row, the opposite pattern, disproving that framing before it was ever
committed to any artifact.

**What was NOT killed / newly established:** the correct, more precise, and now
three-times-verified principle stated above (destabilization = perturbing the attractor's OWN
input row, regardless of that row's original True/False direction).

**Relaxation Map:**
- **Remove** the "these 3 named nodes only" restriction: the same check could in principle be run
  on any other node in the 35-node network, though `RBL2`/`p21CIP`/`CyclinE1` were specifically
  chosen as the arc's own named feedback-loop components, not arbitrarily.
- **Weaken:** characterize WHY the 3 `CyclinE1` fragile-but-non-destabilizing rows specifically
  impair `j*=1` observability (which intermediate release-state trajectory passes through them,
  and why) — not attempted here, a concrete, cheap, named follow-up.

## Revival Condition

Not applicable (not a REJECT). Forward-looking: this experiment's own finding is now itself the
direct input to the user's next explicitly requested step — a three-way sensitivity-profile
synthesis across `RBL2`/`p21CIP`/`CyclinE1`, and an attempt at a minimal necessary/sufficient
condition for the Proliferation attractor's own existence, both addressed in the next experiment
(`H-B7-21`).

## Scope note

Fourth rule-perturbation experiment in the observability sub-arc (H-B7-17: `RBL2`, H-B7-18:
mechanistic explanation, H-B7-19: `p21CIP`, H-B7-20: `CyclinE1`, this experiment). Completes
single-bit perturbation testing of all three named feedback-loop components. Directly answers the
user's explicit added requirement (destabilizes-attractor vs observability-only classification,
applied systematically, not to one hand-picked case) and surfaces the general destabilization
principle that ties H-B7-18's original finding to this experiment's own new data.
