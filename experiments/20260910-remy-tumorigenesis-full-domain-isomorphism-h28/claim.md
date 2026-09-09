# claim.md — 20260910-remy-tumorigenesis-full-domain-isomorphism-h28

**Graph node:** `H-B7-28` (bridge `B7-KAUFFMAN-ATTRACTORS`) · **Tier:** Full
**Parent:** `H-B7-27` (branch isomorphism via φ=flip(EGFR_stimulus), confirmed for the 10 conditions
H-B7-26 tested, k=1..5). Direct continuation under the "hold the mechanism" mission (user's own
explicit instruction after H-B7-27: keep pursuing this structural thread with full FL discipline,
self-paced, rather than switching to a distant new hypothesis). H-B7-27's own claim.md explicitly
scoped itself to k=1..5 and flagged broader generalization as untested. This experiment tests the
cheapest, most natural extension: does the SAME mechanism (FGFR3≡True/GRB2≡False/EGFR≡False
invariant, and the resulting φ=flip(EGFR_stimulus) graph isomorphism) hold across H-B7-22's own
FULL originally-tested domain (k=1..40, both branches, 80 conditions total) -- not just the 10
narrow conditions H-B7-26/27 checked?

## EstimandOps L0 Gate

**Classification: DESCRIPTIVE.** Same as H-B7-26/27 -- exact graph-structural/boolean-invariant
questions on a fully specified deterministic-transition-structure system, extended to a larger
domain. Not causal, not a statistical estimate.

## Origin and design rationale

A Compute-First Check (before any formal artifact) directly tested the generalization: for all 80
of H-B7-22's own originally-tested `(branch, k)` release states (`k=1..40`, both branches, reusing
`h13.simulate_transient_clamp_multi_with_release_state` + `h22.build_reachability_graph`
unchanged), checked `FGFR3=True & GRB2=False & EGFR=False` at EVERY reachable state. Result:
**0 violations across 4516 total states scanned, 80/80 conditions checked.** This directly answers
H-B7-27's own explicitly-flagged open boundary (does it hold beyond `k=1..5`?) — it does, at least
across the entirety of H-B7-22's own tested domain.

**Minimal Relaxation Rule compliance:** ONE change relative to H-B7-27 — the `k` range is extended
from `{1,2,3,4,5}` to `{1,...,40}` (H-B7-22's own full domain). No new mechanism, no new state
space construction, no new branches.

## Mechanism Claim Gate (Step 0a)

**Triggering sentence:** "The same FGFR3=True/GRB2=False/EGFR=False invariant that H-B7-27
established for k=1..5 holds with zero exceptions across H-B7-22's own full originally-tested
domain (k=1..40, both branches) — because nothing about the mechanism (EGFR's rule gating
EGFR_stimulus's relevance behind `!GRB2&!FGFR3`, which never holds) is specific to small k; it is a
property of the two branches' entire reachable universe under this network's dynamics."

**Check performed BEFORE the full artifact (Compute-First Check, scratchpad):**
`diag_h_b7_28_full_sweep_invariant.py` -- 80/80 conditions checked (matching H-B7-22's own tested
domain exactly), 4516 total states scanned, **0 violations**.

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | The full set of H-B7-22's own originally-tested 80 `(branch, k)` reachable graphs (k=1..40, both branches) |
| **Falsifiable predicate** | Does `FGFR3=True & GRB2=False & EGFR=False` hold with zero exceptions at every reachable state across ALL 80 conditions, AND is `φ=flip(EGFR_stimulus)` a genuine graph isomorphism between `branch_1` and `branch_2`'s reachable graphs at every matched `k`? |
| **Measurable outcome** | Per-condition violation count (must be 0 for CONFIRMED); per-k isomorphism pass/fail (node-set bijection + bidirectional edge preservation) |

## Kill Criterion (set BEFORE running the full sweep)

- **Invariant (mandatory):** zero states across ALL 80 conditions violate `FGFR3=True & GRB2=False
  & EGFR=False`. Any violation → CRITERION_INVALID for the FULL-domain claim (does not retroactively
  invalidate H-B7-27's own narrower, already-confirmed k=1..5 result).
- **Isomorphism (mandatory):** for every `k=1..40`, `φ=flip(EGFR_stimulus)` must be a genuine graph
  isomorphism between `branch_1, k` and `branch_2, k`'s reachable graphs (node-set bijection +
  bidirectional edge preservation). Any failure → CRITERION_INVALID.
- **STATE_CAP guard:** if `build_reachability_graph` hits its own `STATE_CAP=30000` for any
  condition, that condition is recorded `BLOCKED-INFRASTRUCTURE`, not treated as a violation or a
  pass (per FL Step 2a — infrastructure limits are never evidence against the claim).

## What This Does NOT Mean

1. Does NOT claim this invariant holds for ANY other clamp scheme, any other pair of base fixed
   points, or ANY k beyond 40 — the domain is exactly H-B7-22's own originally-tested set, not a
   claim about the network's full state space.
2. Does NOT re-derive escape probabilities as a new finding — for k=1..5 these are already committed
   in H-B7-26; for k=6..40 (H-B7-22's own SCHEDULE_ROBUST region), escape probability is already
   known to be exactly 1.0 from H-B7-22's own reachability classification, and this experiment's own
   corollary check is a construction-consistency regression, not a new result.
3. Does NOT itself resolve the large-deviation/Kramers question, still deliberately deferred.
4. Does NOT claim to have found the FULL symmetry group of the network — only that this ONE
   specific bijection (flip EGFR_stimulus) is an automorphism across this specific tested domain.

## MCID

Not applicable — exact boolean/graph-structural claim, no statistical estimate.
