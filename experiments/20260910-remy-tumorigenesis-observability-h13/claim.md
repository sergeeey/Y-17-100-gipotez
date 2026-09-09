# claim.md — 20260910-remy-tumorigenesis-observability-h13

**Graph node:** `H-B7-13` (bridge `B7-KAUFFMAN-ATTRACTORS`) · **Tier:** Standard
**Parent:** `H-B7-10`/`H-B7-12` (both branches, transient `do(p21CIP=0, RBL2=0)` duration sweep,
clean monotone escape threshold `k*=5` on BOTH branches).

## EstimandOps L0 Gate

**Classification: PREDICTIVE**, not causal in the ICH E9 population sense. The system under test
is a single, fully deterministic, already-verified Boolean network (pyboolnet cross-checked,
H-B7-1/H-B7-4) — there is no population, no confounding, no unmeasured variable. The question is a
formal identifiability/observability question about a KNOWN dynamical system: does a small marker
set `M`, observed at the moment the transient clamp would be released, determine the trajectory's
eventual fate as reliably as the full state does? This is prediction from a partial observation of
a deterministic system, not estimation of a causal effect under uncertainty.

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | States reached at the moment of clamp-release in the `do(p21CIP=0, RBL2=0)` transient protocol (H-B7-9/10/12), for `k = 1..40` synchronous clamp-steps, on BOTH known bistable branches (branch 1: `H-B7-4`'s `BRANCH_INPUTS`; branch 2: `H-B7-11`'s `BRANCH_INPUTS_2`) |
| **Falsifiable predicate** | For a given marker set `M` (subset of node names), does the value of `M` at release time determine the eventual fate (`Growth_arrest` vs `Proliferation`) uniquely across this entire domain? |
| **Measurable outcome** | Existence of a "collision pair": two (branch, k) release-states with identical `M`-projection but different eventual fate — computed exactly, not sampled |

## Origin

User's own proposed next step (2026-09-10, direction-scoping follow-up after B2/B3 both closed
negative): "достаточен ли текущий набор наблюдаемых маркеров, чтобы однозначно решить, можно ли
снять intervention без риска возврата в нежелательный attractor?" — operationalized here as a
cheap, exact collision search over the reachable release-state domain this arc's own protocol
family already defines (not a claim about the full 2^31 hidden state space, see caveats below).

## Design (Floor–Ceiling discipline, reused for a boolean sufficiency question, not a numeric ratio)

| Role | Marker set `M` | Purpose |
|---|---|---|
| **Floor (negative control)** | `{"DNA_damage"}` — a branch input, CONSTANT along any single trajectory | Must show a collision (k=4 vs k=5 on branch 1 differ in fate, identical on this M) — confirms the collision-detector itself is not vacuously "always sufficient" |
| **Ceiling (positive control)** | Full state (all 35 nodes) | Tautologically sufficient (identical M ⟺ identical state) — confirms the detector correctly reports zero collisions when none can exist by construction |
| **Candidate M1** | `{"Growth_arrest", "Proliferation"}` — the two phenotype nodes this entire arc has used as its own decision readouts throughout H-B7-4..12 | Primary claim: are the markers ALREADY being used operationally in this repo's own methodology actually sufficient? |
| **Candidate M2** | `{"p21CIP", "RBL2", "Growth_arrest", "Proliferation"}` — M1 plus the two directly-clamped nodes | Minimal-augmentation follow-up if M1 fails |

## Kill Criterion (set BEFORE running)

- **M1 CONFIRMED-SUFFICIENT:** zero collision pairs for `M1` across the full (branch × k=1..40)
  domain — release decisions based on `{Growth_arrest, Proliferation}` alone are exact within this
  domain.
- **M1 REJECTED, M2 CONFIRMED-SUFFICIENT:** ≥1 collision for `M1` but zero for `M2` — minimal
  augmentation (`+p21CIP, +RBL2`) restores sufficiency.
- **BOTH REJECTED:** collisions persist even with 4 markers — genuine insufficiency within this
  domain, would need a differently-scoped marker set, not just a larger one.
- **Floor test fails to show a collision, or ceiling test shows a spurious collision:** `BLOCKED-
  INFRASTRUCTURE` (Substrate Gate) — the collision detector itself is broken, not a finding about
  the network.

## What This Does NOT Mean

1. Does **NOT** establish sufficiency over the full ~2^31-state hidden space (31 non-input nodes) —
   only over states actually reachable by this arc's specific transient-clamp-then-release protocol
   family (`k=1..40`, the two already-characterized bistable branches). A collision could exist
   outside this domain even if none is found inside it.
2. Does **NOT** test asynchronous updating or rule uncertainty — synchronous, deterministic
   updating throughout, matching every prior experiment in this bridge. Robustness to asynchrony is
   an explicit, separate follow-up question, not addressed here.
3. Does **NOT** claim biological applicability — `[NEEDS-REAL-DATA]`, same standing caveat as every
   other H-B7-N experiment in this arc.
4. A CONFIRMED-SUFFICIENT verdict for M1/M2 does **NOT** prove these are the MINIMAL sufficient
   marker sets — only that they ARE sufficient within the tested domain; no search over smaller or
   alternative marker sets is performed here.

## MCID

Not applicable — this is an exact combinatorial existence question (does ≥1 collision exist in a
finite, explicitly enumerated domain), not an estimated quantity with a practical-significance
threshold.
