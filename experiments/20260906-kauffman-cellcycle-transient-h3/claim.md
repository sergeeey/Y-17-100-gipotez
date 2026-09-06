# claim.md — 20260906-kauffman-cellcycle-transient-h3

**Graph node:** `H-B7-3` (bridge `B7-KAUFFMAN-ATTRACTORS`) · **Tier:** Standard
**Parent:** `H-B7-2` (Relaxation Map item 1: "Transient perturbation: force Rb=0 for a FEW steps then
release it back to its own update rule ... does the system settle into the wild-type quiescent point
attractor again, or does it get trapped in cycling even after Rb is 'restored'? This is the STRICTER
test of Kauffman's original hypothesis").

## EstimandOps L0 Gate

**Classification: CAUSAL.** `do(Rb=0)` applied for a FIXED, FINITE number of steps `k`, then released
back to the node's own update rule — compared against the never-perturbed comparator (`H-B7-1`'s wild
type). Same deterministic-mechanism structure as `H-B7-2`; the 4 identifiability assumptions are
trivially satisfied for the same reason (fully specified, exhaustively enumerable mechanism).

## Compute-First Check (done BEFORE writing any new simulation code — this is the actual finding)

Before simulating anything, checked what `H-B7-1`'s ALREADY-VERIFIED result implies about whether this
specific test can even be informative in this model. Re-derived the per-state attractor membership for
the UNPERTURBED (wild-type) network (cheap: reused `H-B7-2`'s own `find_attractors_with_membership` on
the unclamped rules — zero new simulation design, ~1 second) and confirmed directly:

```
n_attractors (unperturbed, wild-type): 2
distinct attractors reached from CycD=0 states: {0}   <- ALL 512 states, ONE attractor
distinct attractors reached from CycD=1 states: {1}   <- ALL 512 states, ONE attractor
```

**Logical consequence, stated precisely:** `CycD`'s own rule is `CycD' = CycD` (an unregulated input —
verified in `H-B7-1`'s Gate-1 source trace of the `.bnet` file) — nothing else in the network can
change it, and clamping `Rb` or `p27` does not touch it either. So ANY trajectory that starts with
`CycD=0` stays in the 512-state `CycD=0` region FOREVER, transient perturbation or not. Once a
perturbation of `Rb` (or `p27`) alone is RELEASED, the system evolves under the network's own true,
unperturbed rules from whatever state it landed on — and `H-B7-1`'s exhaustive enumeration already
proved that EVERY one of the 512 `CycD=0` states, under those true rules, flows to the SAME single
point attractor. There is no second attractor in that region for a transient push to reveal.

**This means the outcome of this experiment is DEDUCIBLE, not an open empirical question:** for ANY
finite-duration clamp of `Rb` and/or `p27` alone, starting from `CycD=0` and released back to normal
dynamics, the system MUST eventually return to the quiescent point attractor. This is analogous to a
`NO_HEADROOM`/`TASK_INFEASIBLE` finding (FL Step 4a spirit, applied to a deterministic rather than
population setting): the test cannot discriminate anything in THIS model, because the `CycD=0`
region's basin structure has no second attractor to discover, regardless of hypothesis truth.

## Why Run Anything At All, Then (this is not skipped, it is re-scoped)

Two reasons this experiment still exists and is worth doing, per the "does not stop at proving a
negative" discipline:

1. **A logical deduction is not the same as a verified simulation** — the deduction could be wrong if
   there is a bug in the reasoning, an edge case (e.g., a perturbation that ALSO happens to touch a
   node whose value affects whether `CycD`'s update is truly unconditional — re-checked: `CycD,CycD` in
   the `.bnet` file, confirmed unconditional), or a subtlety in what "the same attractor" means under a
   transient vs. permanent clamp. Running the ACTUAL simulation on concrete example trajectories is the
   Gate-3-style discipline of not trusting reasoning alone without a computational check.
2. **The genuinely informative re-scoped test:** since single-node transient perturbation is
   deductively guaranteed uninformative in the `CycD=0` branch, the useful next question is whether
   this "single global attractor per branch" structure is a property of THIS SPECIFIC 10-node model
   (likely, given its origin as a simplified, curated textbook example) or whether even a SHORT,
   MULTI-NODE transient kick (not touching `CycD`) can ever escape the single attractor — if the answer
   is provably always "no" (which it must be, by the same argument, since ANY trajectory confined to
   the 512-state `CycD=0` region is subject to that region's single-attractor structure regardless of
   how many nodes were perturbed, AS LONG AS `CycD` itself is untouched), this generalizes the negative
   finding cleanly: **no transient perturbation of any subset of the other 9 nodes, however constructed,
   can be informative for Kauffman's strict hypothesis in this model** — only a perturbation that also
   changes `CycD` (which is a different node's "input", not the same falsification target) could move
   the trajectory into the other basin, and that case reduces to the (uninteresting, already-implied)
   observation that flipping the model's own designated input switch changes the outcome.

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | The Fauré et al. 2006 network, `Rb` and/or `p27` clamped to 0 for a finite window `k` then released |
| **Falsifiable predicate** | Every simulated trajectory, started at `CycD=0`, released after a finite clamp window, converges to the wild-type quiescent point attractor |
| **Measurable outcome** | Final attractor reached, for several concrete `(initial_state, clamped_node(s), k)` combinations |

## Kill Criterion (set BEFORE running — a genuine positive-control-style check, not a novel PROMOTE/REJECT bar)

- **PREDICTED / CONFIRMED (the deduction holds):** every simulated trajectory returns to the wild-type
  quiescent point attractor after release, for every `(node, k)` combination tried.
- **FALSIFIED (deduction or code is wrong — a red flag requiring investigation, not a biology finding):**
  any simulated trajectory does NOT return to quiescence after release — would mean either a bug in
  `H-B7-1`'s or `H-B7-2`'s already-reused pipeline functions, or an error in this experiment's own
  "clamp-then-release" simulation code, and must be resolved before trusting ANY of this bridge's prior
  results, not just this one.

## What This Does NOT Mean

1. Does NOT mean Kauffman's Cancer Attractor hypothesis is false — it means this SPECIFIC small,
   simplified 10-node model's `CycD=0` branch has no secondary attractor, so the STRICT
   transient-perturbation operationalization cannot be tested here at all, regardless of truth. A
   model with a richer, multi-attractor basin per branch (e.g., a larger network with more redundant
   regulators) would be needed for a genuine test of the strict claim.
2. Does NOT mean `H-B7-2`'s `do(Rb=0)` result is invalidated — that experiment used a PERMANENT clamp
   (never released), which is a structurally different intervention that DOES create a genuinely new
   attractor (verified in `H-B7-2`), precisely because it never returns the system to the true,
   unperturbed rule set.
3. Does NOT test perturbations that also change `CycD` — that would test something else (the model's
   designated input switch), not a "hidden pre-existing attractor" claim.

## MCID

None in the PROMOTE/REJECT sense — this experiment either confirms a logical deduction (expected) or
uncovers a bug (a hard stop requiring investigation before continuing this bridge).
