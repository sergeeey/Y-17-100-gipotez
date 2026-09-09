# claim.md — 20260910-remy-tumorigenesis-adversarial-async-h22

**Graph node:** `H-B7-22` (bridge `B7-KAUFFMAN-ATTRACTORS`) · **Tier:** Full
**Parent:** `H-B7-13` (release-state domain, k*=5 threshold under synchronous update),
`H-B7-16` (asynchronous update, but RANDOM scheduling only, tested marker OBSERVABILITY not
the fate itself), and `reports/2026-09-09-breakthrough-routes.md` Route 5 (control theory /
observability: "Fairness обновлений... не даёт конечного верхнего срока" — the adversarial-
scheduling concern this experiment tests directly, previously named as reserve/untested).

## EstimandOps L0 Gate

**Classification: DESCRIPTIVE.** A structural question about a fully specified deterministic
system's own dynamics (which attractors are reachable from a given state under the FULL set of
fair asynchronous update schedules) — not a statistical/predictive claim, not causal.

## Origin and why this is a genuinely different question from H-B7-16

H-B7-16 tested whether markers observed under RANDOM asynchronous update reliably PREDICT the
eventual fate — a question about OBSERVABILITY under one specific (stochastic, uniform) update
distribution. This experiment asks a different, more fundamental question: **is the eventual
FATE ITSELF schedule-independent under asynchronous update, or can some (possibly rare, possibly
adversarial) fair update ORDER reach a different attractor than the one synchronous dynamics
reach?** If the fate itself depends on schedule, no marker-based observability scheme can ever be
schedule-robust — this is upstream of and more fundamental than H-B7-16's own question.

**Minimal Relaxation Rule compliance:** exactly ONE assumption changed relative to H-B7-13's own
already-established k*=5 threshold — the update discipline (synchronous → general fair
asynchronous, exhaustively over ALL schedules, not sampled as H-B7-16 did).

## Compute-First Check (done before committing to the full experiment)

A scratchpad feasibility diagnostic (not committed, per this session's established pattern) built
the exhaustive asynchronous reachability graph from H-B7-13's own `k=3,4,5` release states
(branch 1) and found: reachable-state counts are SMALL (200, 111, 2 states respectively — well
within a 30,000-state cap, BFS terminated naturally, not by hitting the cap) — an exhaustive
search is computationally tractable, not a `k^35`-style combinatorial explosion, because most
network nodes are already stable at any given release state (few "active" branching points).

**A striking result already surfaced by this feasibility check, motivating the full experiment:**
at `k=3` and `k=4` (both `GROWTH_ARREST` under synchronous update — the "safe" cases per
H-B7-13), the async-reachable terminal (fixed-point) states include BOTH `GROWTH_ARREST` AND
`PROLIFERATION` phenotypes. At `k=5` (synchronous `PROLIFERATION`), only `PROLIFERATION` is
reachable. This experiment exists to verify this rigorously (not trust an ad hoc script), extend
it across the FULL `k=1..40` domain (not just 3 spot-checked values) on both branches, and check
for cyclic (not just fixed-point) attractors properly via SCC analysis.

## Mechanism Claim Gate (Step 0a)

**Triggering sentence (from the feasibility check's own shortest-path trace, hand-inspected
before trusting the search):** "a specific asynchronous update ORDER lets `CyclinA`/`CyclinE1`
fire while using STALE (not-yet-updated) `p21CIP=False`/`RBL2=False` values, before `p21CIP` or
`RBL2` themselves have a chance to update and re-suppress them — a classic race condition where
an inhibitor's re-establishment loses a race against a downstream activator's premature firing."

**Check performed:** the feasibility diagnostic's shortest async path from `k=3`'s release state
to a `PROLIFERATION` fixed point was hand-traced step by step (6 updates: `CDC25A, CyclinA,
CyclinD1, CyclinE1, p14ARF, Proliferation`) and the tracked node values at each step were printed
and inspected — `CyclinA` fires True at step 2 while `p21CIP`/`RBL2` are STILL `False` (their
own updates never occur along this specific path), directly confirming the race-condition
mechanism BEFORE the full rigorous experiment is built, per this session's established
discipline of stating and checking a mechanism hypothesis early rather than trusting a surprising
computational result blind.

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | The exhaustive asynchronous (single-node-update) reachability graph from each of `H-B7-13`'s own 80 release-states (`k=1..40`, both branches) |
| **Falsifiable predicate** | Is the set of async-reachable ATTRACTOR phenotypes (fixed point or cycle, via proper SCC analysis) at each release-state IDENTICAL to the synchronous fate alone, or a strict superset? |
| **Measurable outcome** | Per release-state: async-reachable attractor phenotype set, classified `SCHEDULE_ROBUST` (matches sync fate exactly) or `SCHEDULE_FRAGILE` (strict superset — an additional, sync-unreachable fate becomes reachable under some fair async order) |

## Kill Criterion (set BEFORE running the full sweep)

- **CONFIRMED (schedule-robust):** for ALL 80 release-states, the async-reachable attractor
  phenotype set exactly equals the singleton `{synchronous fate}` — H-B7-13's threshold is fully
  schedule-independent, and the feasibility check's k=3/k=4 finding would have to be a bug.
- **REJECTED (schedule-fragile, at least somewhere):** for at least one release-state, the
  async-reachable set is a strict superset of `{synchronous fate}` — the synchronous-only
  characterization of "safe" (k<5) vs "unsafe" (k>=5) does NOT survive relaxing the update-order
  assumption, and a NEW quantity — the smallest `k` at which `PROLIFERATION` becomes reachable
  under SOME fair async order (`k_adv`) — should be reported, expected `k_adv <= k*=5` (adversarial
  scheduling can only make escape MORE reachable, never less, since synchronous IS one particular
  fair schedule and is therefore always included in the async-reachable set by construction).
- **Substrate check (mandatory, not optional):** every reachability search must terminate WITHOUT
  hitting its state-count cap; any release-state whose search DOES hit the cap is reported as
  `BLOCKED-INFRASTRUCTURE` for that state specifically (per FL Step 2a — capped search returning
  "no second fate found" would NOT be evidence of schedule-robustness, only of an unfinished
  search), never silently folded into `CONFIRMED`.
- **Attractor detection must use proper SCC analysis**, not just zero-out-degree fixed points —
  a cyclic attractor with no fixed point along some branch would be silently missed by a
  fixed-point-only check, which would then wrongly report unresolved states as still "reachable
  transients" rather than classifying their true eventual fate.

## What This Does NOT Mean

1. Does NOT claim any SPECIFIC probability of an adversarial schedule occurring in practice — this
   is an EXISTENCE question (can some fair schedule reach the other fate), not a frequency
   question (H-B7-16 already addressed frequency under uniform-random scheduling).
2. Does NOT test partial/restricted fairness models (e.g., bounded-delay fairness, where a
   node cannot be starved for more than L steps) — only the standard "eventually updates,
   no finite bound" fairness notion the report's own "Критическая оговорка" names explicitly.
3. Does NOT re-test H-B7-16's own async-observability accuracy claims — orthogonal question,
   already closed.
4. If `SCHEDULE_FRAGILE` is found: does NOT imply H-B7-14/15/17/19/20/21's own SYNCHRONOUS
   findings are wrong or need revisiting — those explicitly scoped themselves to synchronous
   update throughout (named in each experiment's own "What This Does NOT Mean"), and this
   experiment's finding, if confirmed, would be a NEW scope boundary on top of them, not a
   contradiction.

## MCID

Not applicable — exact, exhaustive existence/reachability question over a finite state space
graph, not a statistical comparison.
