# claim.md — 20260910-remy-tumorigenesis-point-of-no-return-h24

**Graph node:** `H-B7-24` (bridge `B7-KAUFFMAN-ATTRACTORS`) · **Tier:** Standard
**Parent:** `H-B7-22` (proved SCHEDULE_FRAGILE for `k=1..4`, both branches — a bad schedule EXISTS
— and named a race-condition mechanism: `CyclinA`/`CyclinE1` fire on stale `p21CIP=False`/
`RBL2=False` before those inhibitors re-establish). `H-B7-23` (quantified HOW OFTEN a random
schedule triggers it — 6.7%→33.8%). Neither pinpointed WHEN, along an escaping trajectory, the
commitment becomes irreversible.

## EstimandOps L0 Gate

**Classification: DESCRIPTIVE.** A structural reachability question about a fully specified
deterministic system, applied at successive points along a known trajectory — not causal,
not a generalization claim beyond the tested trajectories.

## Origin — the natural next question after H-B7-22/23's own mechanism finding

H-B7-22's decision.md names the race condition (`CyclinA`/`CyclinE1` racing ahead of `p21CIP`/
`RBL2`) but treats the ENTIRE escaping trajectory as a black box between the release state and
the final `PROLIFERATION` fixed point. This experiment asks: **is there a single, identifiable
STEP along the trajectory after which `GROWTH_ARREST` stops being reachable at all (by ANY
continuation, not just the one specific path taken) — a genuine "point of no return" — or does
irreversibility develop gradually across many steps?**

**Minimal Relaxation Rule compliance:** ONE change relative to H-B7-22 — instead of checking
reachability ONLY from the original release state, this experiment checks reachability from
EVERY state along one already-identified shortest escaping path, using the exact same
`build_reachability_graph`/`find_sink_attractors` machinery, unchanged.

## Compute-First Check (done before committing to all 8 release-states)

A scratchpad diagnostic found the shortest async escaping path for `branch_1, k=1` (11 steps:
`RB1, E2F1_medium, CDC25A, CyclinA, CyclinE1, E2F3_medium, p14ARF, p16INK4a, CyclinD1,
Growth_arrest, Proliferation`), then ran H-B7-22's own exhaustive reachability check at EACH of
the 12 states along that path (release state + after each of the 11 updates). Result: `GROWTH_
ARREST` remains reachable (both fates present, hundreds of states) through step 4 (`CyclinA`
fires), then DROPS OUT ENTIRELY at step 5 (`CyclinE1` fires) — from that point on, only
`PROLIFERATION` is reachable, all the way to the end. **The point of no return is a single,
sharp, identifiable step — not a gradual narrowing** — and it coincides exactly with `CyclinE1`'s
own firing, not `CyclinA`'s (which fires one step earlier but does NOT yet commit the system).

## Mechanism Claim Gate (Step 0a)

**Triggering sentence:** "`CyclinA` firing alone (step 4) does not commit the system to
`PROLIFERATION`, because `CyclinA`'s own rule (`!p21CIP&!RBL2&(E2F3_medium|E2F1_medium)&CDC25A`)
is not monotonic under further async updates — if `p21CIP` or `RBL2` update AFTER `CyclinA` but
BEFORE `Proliferation` itself updates, `CyclinA` would flip back to `False` on its own next
evaluation, and `Proliferation`'s rule (`CyclinE1|CyclinA`) would then depend only on `CyclinE1`."

**Check:** the .bnet file's own rules (`experiments/20260906-remy-tumorigenesis-transient-h4/
data/remy_tumorigenesis.bnet`, lines 31 and 33) show `CyclinA` and `CyclinE1` have the IDENTICAL
rule (`!p21CIP&!RBL2&E2F3_medium&CDC25A | !p21CIP&!RBL2&E2F1_medium&CDC25A`) — a real structural
redundancy in the Remy et al. model, not a coincidence of this experiment's own construction.
This means EITHER firing alone is individually reversible (both depend on the SAME `p21CIP`/
`RBL2` values, so both would flip back together if those update), but the network commits only
once the SPECIFIC state reached after BOTH conditions have been locked in via `CyclinE1`'s own
firing — this experiment's own exhaustive reachability check at each step is the actual test of
this hypothesis, not a hand-wave; the hypothesis is stated here BEFORE running the full 8-state
sweep, to be confirmed or falsified by it.

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | The shortest known async-escaping path (release state to a `PROLIFERATION` fixed point) for each of H-B7-22's 8 confirmed `SCHEDULE_FRAGILE` release-states |
| **Falsifiable predicate** | Along each path, is there a single step index after which `GROWTH_ARREST` becomes permanently unreachable (checked via full exhaustive reachability from that intermediate state, not assumed from the path alone)? |
| **Measurable outcome** | Per release-state: the point-of-no-return step index, the node whose update triggers it, and whether `GROWTH_ARREST` reachability before that point is confirmed (not just assumed to persist) |

## Kill Criterion (set BEFORE running the full sweep)

- **CONFIRMED (sharp point of no return exists):** for ALL 8 release-states, there is exactly ONE
  step index `t*` such that `GROWTH_ARREST` is reachable from every state at step `< t*` and
  unreachable from every state at step `>= t*` along that path (a genuine step function, not a
  gradual decline or an oscillating pattern).
- **REJECTED (no sharp commitment point):** at least one release-state shows `GROWTH_ARREST`
  becoming unreachable, then reachable again later along the SAME path (would indicate the
  "point of no return" framing itself is wrong for this system — reachability is not monotonically
  decreasing along an arbitrary path), or a gradual multi-step transition rather than a single
  sharp step.
- **Mechanism check:** does the triggering node match `CyclinE1` (or, more generally, does it
  belong to the `{CyclinA, CyclinE1}` pair) in ALL 8 cases, confirming the Mechanism Claim Gate's
  own hypothesis generalizes beyond the single `k=1, branch_1` spot-check?

## What This Does NOT Mean

1. This is the point of no return along ONE specific (shortest) path — a DIFFERENT escaping path
   for the same release-state could plausibly commit at a different step (not tested here;
   the shortest path is used as a representative, not claimed to be the unique or canonical one).
2. Does NOT claim this generalizes to nodes/mechanisms outside the `CyclinA`/`CyclinE1`/`p21CIP`/
   `RBL2` feedback loop this whole B7 sub-arc has focused on.
3. Does NOT re-derive H-B7-23's own frequency estimates — a different question (WHEN commitment
   happens along a path, not HOW OFTEN a random schedule reaches one).

## MCID

Not applicable — exact, per-step reachability/existence question, not a statistical comparison.
