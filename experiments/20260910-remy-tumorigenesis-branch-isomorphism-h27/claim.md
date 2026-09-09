# claim.md — 20260910-remy-tumorigenesis-branch-isomorphism-h27

**Graph node:** `H-B7-27` (bridge `B7-KAUFFMAN-ATTRACTORS`) · **Tier:** Full
**Parent:** `H-B7-26` (exact absorption probabilities via absorbing Markov chain, CONFIRMED). Directly
motivated by the user's own observation of H-B7-26's committed `metrics/run.json`: for every one of
the 10 tested conditions, `branch_1` and `branch_2` give NUMERICALLY IDENTICAL exact escape
probabilities, expected steps to absorption, `n_states_in_graph`, `n_transient`, and absorbing-state
counts — despite `branch_1`/`branch_2` release states being confirmed genuinely distinct (H-B7-26's
own regression test). The user proposed this is not coincidence and named the concrete minimal test:
compare reachable subgraphs for graph isomorphism / lumpability / bisimulation, and if a bijection
`φ` exists with `q(x)=q(φ(x))`, the coincidence becomes an explained symmetry rather than "a funny
number."

## EstimandOps L0 Gate

**Classification: DESCRIPTIVE.** Establishing an exact graph-isomorphism relationship (and its
mechanistic cause) between two fully specified finite deterministic-transition-structure objects —
not causal, not a statistical estimate.

## Origin and design rationale

A Compute-First Check (before any formal artifact) found the exact answer faster than the user's own
proposed general isomorphism/lumpability search would have required:

1. `GROWTH_ARREST_STATE_1` and `GROWTH_ARREST_STATE_2` (the two synchronous fixed points underlying
   `branch_1`/`branch_2`) differ at **exactly one node: `EGFR_stimulus`**.
2. At every tested `k` (1-4), the release states differ at exactly that same one node.
3. The candidate bijection `φ = flip(EGFR_stimulus), identity elsewhere` was tested directly (not a
   blind VF2 search): `φ(nodes(g_branch_1)) == nodes(g_branch_2)` exactly, and edge structure is
   preserved in BOTH directions, for every tested k. This is a genuine graph isomorphism, not merely
   matching summary statistics.
4. **Mechanism** (not just the isomorphism's existence): `EGFR`'s own rule is
   `SPRY&!GRB2&!FGFR3 | !GRB2&!FGFR3&EGFR_stimulus` = `!GRB2 & !FGFR3 & (SPRY | EGFR_stimulus)`.
   `EGFR_stimulus` can only ever matter when `!GRB2 & !FGFR3` holds. An exhaustive check over
   **every state in every reachable graph, both branches, k=1..5 (≈4446 states total)** found
   `FGFR3 = True` with **zero exceptions** (equivalently `GRB2 = False` with zero exceptions) — so
   `!FGFR3` is identically `False` throughout the entire reachable region, making `EGFR` identically
   `False` there REGARDLESS of `EGFR_stimulus`, `GRB2`, or `SPRY`. `EGFR_stimulus` is therefore
   **causally inert** in this specific reachable region — not an unexplained empirical coincidence.
   `EGFR_stimulus`'s own rule is a frozen self-loop (`EGFR_stimulus,EGFR_stimulus` in the `.bnet`
   source), so flipping it produces a structurally valid alternate initial condition that never
   diverges from the original trajectory's dynamics.

**Minimal Relaxation Rule compliance:** this is a genuinely new claim (explains H-B7-26's own
unplanned observation), not a relaxation of a prior hypothesis — no assumption is being
loosened/tightened relative to a prior REJECT.

## Mechanism Claim Gate (Step 0a)

**Triggering sentence:** "For every state reachable from either branch's release state (across
k=1..5), FGFR3 is provably True and GRB2 is provably False — a computationally-verified structural
invariant of this specific reachable region, not assumed — which forces EGFR identically False
regardless of EGFR_stimulus, making the single-bit flip of EGFR_stimulus a graph automorphism-inducing
bijection between the two branches' reachable graphs."

**Check performed BEFORE the full sweep (Compute-First Check, scratchpad):**
- `diag_h_b7_27_branch_equivalence.py`: confirmed `φ = flip(EGFR_stimulus)` is a full graph
  isomorphism (node-set bijection + edges preserved both directions) for k=1,2,3,4.
- `diag_h_b7_27_masking_check.py`: confirmed 0/2211 states (both branches, k=1-4) satisfy
  `!GRB2 & !FGFR3 & !SPRY`, and separately 0 states satisfy `!GRB2 & !FGFR3 & SPRY` — i.e. the
  gating condition `!GRB2 & !FGFR3` for EGFR never holds anywhere in this region.
- `diag_h_b7_27_fgfr3_invariant.py`: sharpened to the precise invariant — `FGFR3 = True` with 0
  exceptions and `GRB2 = False` with 0 exceptions, across all 10 conditions (both branches, k=1-5,
  ≈4446 states total, including the k=5 positive-control condition).

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | The pair of async reachability graphs (branch_1, branch_2) at each of H-B7-26's own 10 tested (branch, k) conditions, and the candidate bijection φ = flip(EGFR_stimulus) between them |
| **Falsifiable predicate** | Is φ a genuine graph isomorphism (node-set bijection + edge-structure preservation, both directions) between branch_1's and branch_2's reachable graphs at every condition, AND is FGFR3≡True / GRB2≡False a genuine zero-exception invariant across every reachable state? |
| **Measurable outcome** | Per-condition: node-set-bijection pass/fail, edge-preservation pass/fail (both directions), FGFR3/GRB2 invariant violation count; corollary: independently re-solved exact escape probability on both graphs, checked for exact equality |

## Kill Criterion (set BEFORE running the full sweep)

- **Isomorphism (mandatory, checked for ALL 10 conditions, not just the 4 already spot-checked):**
  `φ(nodes(g_branch_1)) == nodes(g_branch_2)` exactly, AND every edge of `g_branch_1` maps under φ to
  an edge of `g_branch_2`, AND every edge of `g_branch_2` maps under φ to an edge of `g_branch_1`.
  REJECT/CRITERION_INVALID if this fails for ANY condition (including the two trivial k=5 cases).
- **Mechanism (mandatory):** zero states across ALL 10 conditions' reachable graphs violate
  `FGFR3=True` (equivalently zero states violate `GRB2=False`). If ANY violation is found, the
  mechanism claim is FALSIFIED even if the isomorphism itself still happens to hold for an unrelated
  reason — the two parts of this claim are checked independently, not inferred from each other.
- **Corollary (sanity re-derivation, not the primary claim):** independently re-solving the exact
  absorption probability on both `g_branch_1` and `g_branch_2` (reusing H-B7-26's own
  `solve_absorption`) must give identical numbers to H-B7-26's own committed `metrics/run.json` — a
  regression check that this experiment's own graph construction matches H-B7-26's, not a new
  computation of the probabilities themselves.

## What This Does NOT Mean

1. Does NOT generalize beyond `k=1..5` on THESE two specific release-state branches — a different
   perturbation of `GROWTH_ARREST_STATE_1`/`_2` (e.g. a different clamp pair, or a different pair of
   base fixed points differing at more than one node) is NOT claimed to exhibit the same
   isomorphism; the mechanism is specific to `EGFR_stimulus`'s inertness in THIS reachable region,
   not a general theorem about single-bit-differing initial conditions.
2. Does NOT claim `FGFR3≡True`/`GRB2≡False` holds outside the checked reachable region (e.g. under a
   different clamp scheme, or for k values >5 not yet tested against H-B7-22's own SCHEDULE_ROBUST
   classification) — the invariant is verified only for the specific 10 conditions checked.
3. Does NOT re-test H-B7-26's own oracle-gate result — this experiment's corollary check reuses
   H-B7-26's `solve_absorption` machinery on independently-built graphs, which is a construction
   regression check, not a re-validation of H-B7-26's Monte Carlo oracle gate.
4. Does NOT itself resolve the large-deviation/Kramers question, still deliberately deferred per the
   user's own explicit priority order (unchanged from H-B7-26).

## MCID

Not applicable — exact boolean/graph-structural claim (isomorphism existence, invariant zero-count),
no statistical estimate with sampling uncertainty.
