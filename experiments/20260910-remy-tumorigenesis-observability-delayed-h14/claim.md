# claim.md — 20260910-remy-tumorigenesis-observability-delayed-h14

**Graph node:** `H-B7-14` (bridge `B7-KAUFFMAN-ATTRACTORS`) · **Tier:** Standard
**Parent:** `H-B7-13` (BOTH candidate marker sets REJECTED when observed AT the release instant).

## EstimandOps L0 Gate

**Classification: PREDICTIVE** — same deterministic-system framing as `H-B7-13`, unchanged.

## Origin — Minimal Relaxation Rule (ONE assumption changed from H-B7-13)

`H-B7-13`'s own Revival Condition named this exact follow-up as the cheapest, most-likely-to-
succeed relaxation: *"re-run the identical collision search with markers observed `j` steps after
release instead of at the instant of removal."* User confirmed directly (2026-09-10): "наблюдай
маркеры через j шагов после снятия клэмпа."

**The ONE changed assumption:** WHEN the marker set is observed (`j` steps after release, instead
of at the instant `j=0`). Everything else is held fixed: same two branches, same `k=1..40` domain,
same two candidate marker sets `M1={Growth_arrest,Proliferation}` and
`M2=M1+{p21CIP,RBL2}`, same floor/ceiling controls, same collision-detection logic
(`marker_projection`, `find_collisions`, reused UNCHANGED from `H-B7-13`).

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | Same release-state domain as `H-B7-13` (2 branches × `k=1..40`), but the marker snapshot is taken `j` synchronous WILD-TYPE steps after the clamp is released, not at the instant of release |
| **Falsifiable predicate** | Does a delay `j` exist (swept `j=0..10`) at which M1 and/or M2's collision (found at `j=0` in H-B7-13) disappears? |
| **Measurable outcome** | `n_collisions` for M1/M2 as a function of `j`; the smallest `j` at which each reaches 0, if any within the swept range |

## Design

Reuses H-B7-13's `simulate_transient_clamp_multi_with_release_state`, `fate_label`,
`marker_projection`, `find_collisions`, `FLOOR_M`, `CEILING_M`, `CANDIDATE_M1`, `CANDIDATE_M2`
UNCHANGED via distinct-name import (this session's established pattern). Adds ONE new function,
`simulate_transient_clamp_multi_with_delayed_observation`, a minimal extension of H-B7-13's own
release-state function that also runs `j` additional wild-type synchronous steps after release
before capturing the "observed" snapshot — everything else (clamp application, eventual-attractor
convergence) is byte-identical to H-B7-13's logic. `j=0` must reproduce H-B7-13's own committed
`metrics/run.json` collision counts EXACTLY — this is the regression/continuity check that the new
function did not silently change H-B7-13's own already-verified behavior.

**Swept range:** `j = 0, 1, 2, 3, 4, 5, 7, 10` — cheap (each `j` re-runs the same 80-state domain,
tens of synchronous steps per state, sub-second per `j`), no reason to bound tighter a priori.

## Kill Criterion (set BEFORE running)

- **RESOLVED-QUICKLY:** M1 and/or M2 reach `n_collisions=0` at some `j ≤ 3` — confirms H-B7-13's
  own mechanistic diagnosis (one-step feedback lag) essentially as stated.
- **RESOLVED-SLOWLY:** first `j` with `n_collisions=0` is `> 3` — the lag is real but longer than
  H-B7-13's own text suggested; still a positive finding, just a correction to the estimated delay.
- **UNRESOLVED:** collisions persist for BOTH M1 and M2 across the entire swept range (`j` up to
  10) — the "delay" relaxation does NOT rescue observability with these marker sets; a genuinely
  different marker set (not just a later observation time) would be needed.
- **REGRESSION FAILURE (Substrate Gate, not a finding about the network):** `j=0` results do not
  exactly match H-B7-13's own committed `metrics/run.json` — would indicate a bug in the new
  function, not evidence about the claim; must be fixed before any `j>0` result is trusted.

## What This Does NOT Mean

1. A RESOLVED verdict for M1/M2 at some `j*` does NOT mean `j*` steps of continued observation
   after release is cost-free in the intended application (a real "should I release now" decision
   still has to wait `j*` steps before it can trust the readout) — this is a genuinely different,
   weaker guarantee than instant observability, and should be reported as such.
2. Does NOT search over marker sets other than M1/M2, or over decision-POLICY classes beyond "wait
   `j` fixed steps then read once" (e.g. a policy that waits for markers to STABILIZE rather than a
   fixed count) — both explicitly named as separate, un-attempted follow-ups in H-B7-13.
3. Same domain-scope caveat as H-B7-13: this is about the release-state domain THIS arc's own
   protocol defines (2 branches × `k=1..40`), not the full hidden state space.

## MCID

Not applicable — exact combinatorial existence question, same as H-B7-13.
