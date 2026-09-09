# claim.md — 20260910-remy-tumorigenesis-observability-exhaustive-h15

**Graph node:** `H-B7-15` (bridge `B7-KAUFFMAN-ATTRACTORS`) · **Tier:** Standard
**Parent:** `H-B7-14` (CONFIRMED, `j*=1` sufficiency, but only tested on the truncated sweep
`k=1..40`, both branches — a SAMPLE of the release-state domain, not its full closure).

## EstimandOps L0 Gate

**Classification: PREDICTIVE** — same deterministic-system framing as H-B7-13/14, unchanged.

## Origin — user's own explicit next step (2026-09-10, "согласен ... го автономно")

User's own framing of what would make H-B7-14 a "model-level theorem" rather than a sample-based
result: *"существует ли общий минимальный observation delay j*, при котором данный marker set
становится sufficient для всех достижимых release states? ... Следующий уровень должен быть не ещё
один sweep, а доказательство или exhaustive verification ... если это можно доказать по конечному
state graph, это уже очень приличный model-level theorem."*

## The key structural fact that makes exhaustive verification CHEAP here (Compute-First Check)

The clamped phase (`p21CIP=False, RBL2=False` forced for `k` synchronous steps) is itself a
**deterministic walk under a FIXED clamped rule-set** — the clamp never changes, so the sequence of
states visited as `k=1,2,3,...` is a single deterministic trajectory of a finite-state system
(31 free nodes once the 4 branch inputs are fixed). By the same pigeonhole argument this bridge's
own `find_attractors`/`run_until_attractor` already rely on (H-B7-1, H-B7-3): **this trajectory MUST
eventually revisit a state and enter a cycle** — after that point, `k` and `k+period` produce the
IDENTICAL release-state. Therefore the set of achievable release-states for `k ∈ {1, 2, 3, ...}`
(unbounded) is NOT infinite — it is exactly `{states visited from k=1 up to the first full cycle}`,
a finite, explicitly computable set. Walking until that cycle is detected (not sampling a truncated
range) gives EXHAUSTIVE coverage of every achievable release-state, for ANY `k`, not just
`k=1..40` — turning H-B7-14's sampled sweep into a closed, complete verification.

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | The COMPLETE clamped-trajectory orbit (transient states + the cycle they enter) for BOTH branches, walked until a previously-visited state recurs — not a truncated `k=1..40` sample |
| **Falsifiable predicate** | Does `j*=1` sufficiency (H-B7-14) hold for EVERY state in this complete orbit, or only for the sampled subset already tested? |
| **Measurable outcome** | `n_collisions` for `M1`/`M2` at `j=1`, computed over the FULL orbit (both branches); additionally, whether `k=1..40` already covered the full orbit (i.e. whether the cycle is reached within 40 steps) — itself a checkable fact, not assumed |

## Design

Adds ONE new function, `walk_clamped_trajectory_until_cycle`, a direct structural analogue of
H-B7-3's own `run_until_attractor` (same "seen-state dict" cycle-detection pattern, same
`h1.synchronous_step` calls) but applied to the CLAMPED rule-set instead of the wild-type rule-set,
and returning the FULL trajectory (not just the cycle) so every achievable release-state is
available, not only the eventual repeating ones. Reuses H-B7-13/14's `fate_label`,
`marker_projection`, `find_collisions`, `CANDIDATE_M1`, `CANDIDATE_M2`, and the delayed-observation
function (`j=1` continuation under wild-type rules to determine eventual fate) UNCHANGED.

**Mandatory regression check:** for every `k` in the ORIGINAL `k=1..40` sweep that is ALSO within
the newly-computed orbit's transient+cycle range, this experiment's collision result at `j=0`/`j=1`
must exactly match H-B7-13/14's own already-committed numbers.

## Kill Criterion (set BEFORE running)

- **THEOREM-LEVEL CONFIRMED:** `n_collisions=0` for M1 at `j=1` over the COMPLETE orbit (both
  branches) — `j*=1` sufficiency is not a sampling artifact, it holds for literally every
  achievable release-state under this protocol, a closed, exhaustive result.
- **REJECTED-BY-A-LATER-STATE:** the orbit extends beyond `k=40` and a collision appears among the
  previously-untested states — `j*=1` would need revision (either a larger `j*`, or acceptance that
  no single `j*` suffices for the full orbit).
- **SUBSTRATE-GATE FAILURE:** the regression check against H-B7-13/14's own committed numbers fails
  for the overlapping `k` range — a bug in the new orbit-walking function, not a finding about the
  network.

## What This Does NOT Mean

1. "Exhaustive over the clamped-trajectory orbit" is NOT the same as "exhaustive over the full
   ~2^31-node hidden state space" — this remains scoped to states reachable by THIS SPECIFIC
   protocol (clamp `p21CIP=RBL2=False` starting from the known `Growth_arrest` fixed point), same
   domain-scope caveat as H-B7-13/14, now made airtight WITHIN that domain rather than merely
   sampled within it.
2. Does NOT generalize to a different starting state, a different pair of clamped nodes, or
   asynchronous updating — same standing caveats as the whole H-B7-13/14/15 sub-arc.
3. A THEOREM-LEVEL CONFIRMED verdict is a closed statement about THIS Boolean network's THIS
   protocol — not a claim of biological applicability (`[NEEDS-REAL-DATA]`, unchanged).

## MCID

Not applicable — exact, finite, exhaustively-enumerated existence question.
