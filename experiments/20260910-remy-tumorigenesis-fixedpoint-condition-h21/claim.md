# claim.md — 20260910-remy-tumorigenesis-fixedpoint-condition-h21

**Graph node:** `H-B7-21` (bridge `B7-KAUFFMAN-ATTRACTORS`) · **Tier:** Standard
**Parent:** `H-B7-17` (`RBL2`), `H-B7-19` (`p21CIP`), `H-B7-20` (`CyclinE1`) — all three explicitly
found the SAME pattern: among all single-bit perturbations of a node's own rule, exactly one row
(the one matching `PROLIFERATION_STATE`'s own input configuration for that node) destabilizes the
attractor; H-B7-20's own "What This Does NOT Mean" explicitly flagged this as untested beyond
these 3 of 35 network nodes. User's explicit instruction (2026-09-10): synthesize the three
sensitivity profiles, then attempt to derive a minimal necessary/sufficient condition for the
Proliferation attractor's own existence, continuing autonomously until resolved.

## EstimandOps L0 Gate

**Classification: DESCRIPTIVE.** Two parts, both about a fully specified deterministic system, no
causal claim: (A) a formal structural characterization (proven by direct inspection of the
table-lookup evaluation mechanism, then exhaustively verified computationally, not assumed) of
when a single-bit rule perturbation preserves vs breaks the Proliferation attractor's fixed-point
status; (B) a synthesis of already-collected data from H-B7-17/19/20, no new primary simulation
beyond what Part A computes.

## Design rationale — what is genuinely new here, and what is not

**Part A is not a new empirical discovery — it is a generalization of scope, from 3 of 35 network
nodes to all 35, plus an honest statement of WHY the pattern holds.** H-B7-20's own decision.md
already named the mechanism as "a direct, near-tautological consequence of what a fixed point IS."
This experiment does not claim to have found something new about the mechanism; it claims to have
CHECKED, exhaustively and computationally (not merely asserted from the 3-node pattern), that the
mechanism holds for every node in the network, not just the three already tested. The check is
cheap (a Boolean network with 35 nodes, largest single-node in-degree 9) and directly answers the
open question H-B7-20 itself flagged as out of scope.

**The exact claim being tested, precisely:** for state `S` (`PROLIFERATION_STATE` or `_2`, both
already-verified fixed points of the wild-type network) and any node `n`, let `own_row(n, S)` be
the tuple of `S`'s own values at `n`'s actual input symbols (extracted from the real compiled
`.bnet` expression via `boolean.py`'s `.symbols`, not hand-listed). Then: flipping row `r` of `n`'s
truth table changes `evaluate(S)` for node `n` **if and only if** `r == own_row(n, S)`. This is
true by construction of a table-lookup evaluator (evaluating `S` only ever consults the ONE row
matching `S`'s own projected inputs), so the logical content is close to trivial — but "close to
trivial" is not the same as "verified," and this session has twice already caught real bugs in
constructs that looked obviously correct (H-B7-15's docstrings, H-B7-19's clamp-phase override).
The exhaustive run is the actual check, not a formality.

**Consequence — the minimal necessary and sufficient condition the user asked for:** a set of
single-bit rule perturbations (one bit per perturbed node, at most) preserves the Proliferation
attractor `S` as a fixed point if and only if NONE of the perturbed rows equals that node's
`own_row(n, S)`. Necessary: perturbing `own_row(n, S)` always breaks it (proven + verified below).
Sufficient: perturbing any OTHER row can never change `evaluate(S)` for that node, by the same
table-lookup argument, so if no perturbed row is any node's `own_row`, `S` remains a fixed point
under simultaneous perturbation of ALL such nodes at once (not just one at a time) — this multi-
node extension is a real, if easy, generalization beyond H-B7-17/19/20's own one-node-at-a-time
scope, and is checked explicitly (not just asserted) in this experiment's tests.

**Part B (sensitivity-profile synthesis)** stays honestly scoped: only 3 of 35 nodes have the FULL
`j*=1`-observability machinery run (clamp+release simulation, ROBUST/FRAGILE/CRITERION_INVALID
classification) — Part A extends CRITERION_INVALID-equivalent coverage (fixed-point preservation)
to all 35 nodes, but does NOT extend the ROBUST-vs-FRAGILE (observability) distinction beyond the
3 already tested, since that requires the much more expensive full simulation per node. This
experiment does not attempt that extension — named explicitly as future scope, not silently
skipped.

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | Every one of the 35 network nodes' own truth tables (extracted from the real `.bnet` expressions), each row, evaluated against both known Proliferation fixed points |
| **Falsifiable predicate** | Flipping table row `r` of node `n` changes `evaluate(S)` for `n` if and only if `r == own_row(n, S)` |
| **Measurable outcome** | Exhaustive per-node, per-row boolean comparison (`baseline == perturbed?`) against the `r == own_row` predicate, for both `S` branches |

## Kill Criterion (set BEFORE running)

- **CONFIRMED (theorem holds exhaustively):** for all 35 nodes × both branches × every row of
  every node's table, `(flip changes evaluate(S)) == (r == own_row(n, S))` holds exactly.
- **REJECTED (real bug or genuine exception found):** any single (node, row, branch) triple where
  this equivalence fails — would indicate either an implementation bug (table construction, input
  extraction, or lookup) or a genuine flaw in the reasoning above; either way, stop and diagnose
  before writing any synthesis claim.
- **Multi-node simultaneous-perturbation check:** additionally verify on at least one concrete
  multi-node combination (perturbing 2+ nodes' rules at once, none at their `own_row`) that `S`
  remains a fixed point under the FULL simultaneous rule set, not just individually.

## What This Does NOT Mean

1. Part A does NOT establish anything about `j*=1` OBSERVABILITY robustness (ROBUST vs FRAGILE)
   for the 32 untested nodes — only fixed-point PRESERVATION (i.e., whether the attractor still
   exists at all). A node could preserve the fixed point while still breaking observability
   timing, as H-B7-17/19/20's own FRAGILE rows already demonstrate for the 3 tested nodes.
2. Does NOT claim the FRAGILE-rate pattern across RBL2/p21CIP/CyclinE1 (Part B) generalizes to a
   predictive rule (e.g., "higher in-degree means higher FRAGILE rate") — n=3 nodes is far too few
   to fit or trust such a relationship; Part B reports the three numbers honestly without fitting
   a trend to them.
3. Does NOT test double-bit or higher-order simultaneous perturbations of a SINGLE node's own
   table (only single-bit per node, potentially across multiple nodes at once).
4. Does NOT test asynchronous update (H-B7-16) in combination with this — orthogonal, untested.

## MCID

Not applicable — exact, exhaustive existence/equivalence questions, not a statistical comparison.
