# claim.md — 20260910-remy-tumorigenesis-observability-ruleperturbation-h17

**Graph node:** `H-B7-17` (bridge `B7-KAUFFMAN-ATTRACTORS`) · **Tier:** Standard
**Parent:** `H-B7-15` (THEOREM-LEVEL CONFIRMED, minimal `j*=1` sufficiency, SYNCHRONOUS update,
exact rules). `H-B7-16` tested the update-SCHEDULE half of robustness (asynchronous); this
experiment tests the update-RULE half — the second, previously-named-but-untested half of the
user's "option 2" (2026-09-10: "robustness/generalization: ... rule perturbations").

## EstimandOps L0 Gate

**Classification: PREDICTIVE.** Same framing as H-B7-13/14/15: a formal question about a fully
deterministic, exactly-specified system (once each perturbed rule-set is fixed) — not a
statistical/causal estimand.

## Design rationale — why RBL2's own rule, and why single-bit truth-table flips

**Choice of target rule:** `RBL2`'s own post-release rule (`!CyclinE1 & !CyclinD1`) is the
mechanism this entire arc's own diagnosis (H-B7-13's decision.md) already points to — the
"CyclinE1/RBL2 feedback loop" whose one-step-delayed commitment is the named reason `j=1`
resolves what `j=0` cannot. Perturbing THIS specific rule tests whether the finding depends on
this rule's exact logical form, or is more structurally robust.

**Choice of perturbation scheme — standard, well-defined, no new machinery needed:** a
single-bit truth-table flip (the standard Derrida/robustness-analysis perturbation for Boolean
networks) changes the rule's output for exactly ONE of its `2^(inputs)` rows. `RBL2` has only 2
input symbols (`CyclinE1`, `CyclinD1`), so its truth table has exactly 4 rows — small enough to
perturb EXHAUSTIVELY (all 4 single-bit flips), matching this arc's own established "exhaustive,
not sampled" discipline (H-B7-15).

**Hand-derived (before writing any code) — the 4 perturbations, verified by truth-table
enumeration:**

| Flipped row (`CyclinE1`, `CyclinD1`) | Original → New | New rule as a boolean expression |
|---|---|---|
| `(F,F)` | `T→F` | `0` (constant False — RBL2 can never re-establish; removes the mechanism) |
| `(F,T)` | `F→T` | `!CyclinE1` (drops the `CyclinD1` dependency entirely) |
| `(T,F)` | `F→T` | `!CyclinD1` (drops the `CyclinE1` dependency entirely) |
| `(T,T)` | `F→T` | `(CyclinE1&CyclinD1)|(!CyclinE1&!CyclinD1)` (XNOR — inverts the AND-of-negations structure) |

Each of these is a normal boolean.py-parseable expression — reusing the EXACT SAME
`h1.parse_bnet`/`compile_rules`/`synchronous_step` pipeline, no new evaluation machinery.

## Compute-First Check (why this is cheap, no new orbit-walk needed)

`RBL2` is one of the two CLAMPED nodes (`p21CIP=False, RBL2=False` forced for `k` rounds).
`h2.clamp_rule` REPLACES a node's compiled rule with a constant for the clamp's duration,
regardless of what the underlying rule is — so the CLAMP-PHASE trajectory (and hence H-B7-15's
own already-computed 7-state-per-branch orbit) is provably UNCHANGED by any perturbation to
`RBL2`'s own rule; only the POST-RELEASE dynamics (where `RBL2` reverts to its own, now perturbed,
rule) can differ. This experiment reuses H-B7-15's exact `k=1..6` exhaustive domain, per branch,
unchanged — only the `wild_type_rules` dict passed to
`simulate_transient_clamp_multi_with_delayed_observation` (H-B7-14's own function, unmodified)
differs, one entry (`RBL2`) swapped per perturbation.

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | The same H-B7-15 exhaustive 12-state domain (2 branches × k=1..6), re-evaluated under each of 4 single-bit-flip perturbations of `RBL2`'s post-release rule (plus the unperturbed baseline for direct comparison) |
| **Falsifiable predicate** | Does `M1={Growth_arrest,Proliferation}` at `j=1` remain fully sufficient (0 collisions) under each perturbed rule, or does the mechanism break? |
| **Measurable outcome** | `n_collisions` for M1/M2 at `j=0`/`j=1`, per perturbation, compared to H-B7-15's own baseline (0 collisions at j=1) |

## Kill Criterion (set BEFORE running)

- **ROBUST:** `j*=1` sufficiency (0 collisions, M1) survives ALL 4 perturbations.
- **PARTIALLY-ROBUST:** survives SOME but not all — report exactly which perturbations break it
  and whether a pattern is visible (e.g. removing a dependency vs inverting one).
- **FRAGILE:** breaks under ALL/MOST perturbations — the `j*=1` finding is a property of this
  EXACT rule, not a structurally robust one.
- **Substrate Gate check (not evidence either way):** the clamp-phase orbit (7 states/branch) must
  be IDENTICAL across all 5 conditions (baseline + 4 perturbations) — if it differs, that would
  indicate a bug in how the perturbed rules were applied, not a finding about the network.

## What This Does NOT Mean

1. Tests only ONE rule (`RBL2`) with ONE perturbation scheme (single-bit truth-table flip) — does
   NOT test `p21CIP`'s own rule, `CyclinE1`'s rule (the other named feedback-loop component, a
   32-row truth table, not exhaustively testable this cheaply), or any other node.
2. Does NOT combine rule perturbation with asynchronous update (H-B7-16) — that combination is a
   separate, un-attempted, more expensive follow-up.
3. Even a ROBUST verdict here does not establish general structural robustness of the whole
   network — only that `j*=1` sufficiency is not fragile to this SPECIFIC rule's exact form.

## MCID

Not applicable — exact, finite, exhaustively-enumerated existence question (matching H-B7-15's own
scope, not H-B7-16's statistical one).
