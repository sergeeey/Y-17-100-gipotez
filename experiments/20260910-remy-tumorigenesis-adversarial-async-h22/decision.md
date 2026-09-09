# H-B7-22 — decision.md

## Result

**Substrate check passed cleanly:** all 80 release-states (`k=1..40`, both branches) produced a
terminating, exhaustive reachability search — `n_blocked_infrastructure: 0`. No search hit the
30,000-state cap; the largest observed reachable set was 956 states (`k=1`), comfortably below
it. `n_cyclic_attractors: 0` and `n_ambiguous_attractors: 0` everywhere — every attractor found is
a genuine, unambiguous fixed point, matching this network's known behavior under synchronous
update (period-1 orbits, established since H-B7-4).

**A sharp, clean split — not scattered noise:**

| `k` range | Synchronous fate | Async-reachable fate set | Classification |
|---|---|---|---|
| `1, 2, 3, 4` (both branches) | `GROWTH_ARREST` | `{GROWTH_ARREST, PROLIFERATION}` | **SCHEDULE_FRAGILE** |
| `5..40` (both branches) | `PROLIFERATION` | `{PROLIFERATION}` | SCHEDULE_ROBUST |

**8 of 80 release-states are `SCHEDULE_FRAGILE` — exactly `k ∈ {1,2,3,4}` on both branches, no
others.** The asymmetry is one-directional: for every `k >= 5` (synchronous `PROLIFERATION`),
`GROWTH_ARREST` is NEVER additionally reachable — the escape, once past the synchronous
threshold, is schedule-robust in both directions tested. For `k <= 4` (synchronous
`GROWTH_ARREST`, previously classified "safe" by H-B7-13/14/15's own synchronous-only analysis),
`PROLIFERATION` becomes reachable under SOME fair asynchronous schedule — including at `k=1`, the
EARLIEST release tested, where synchronous dynamics land most safely, most quickly, and (by
`H-B7-15`'s own exhaustive j*=1 domain construction) most unambiguously in `GROWTH_ARREST`.

**`k_adv = 1`**, materially smaller than the synchronous `k*=5` — an adversarial scheduler can, in
principle, reach the unsafe outcome starting from ANY release-state this domain contains, not
just the ones near the synchronous threshold.

## Mechanism (verified, not just hypothesized)

The pre-registered Mechanism Claim (claim.md, from the feasibility check's hand-traced shortest
path) is confirmed by `test_mechanism_race_condition_reproducible`, independently re-deriving the
shortest async path from `branch_1`'s `k=3` release state: `CyclinE1`/`CyclinA` are able to fire
(become `True`) via a specific update ORDER that reaches them BEFORE `p21CIP` or `RBL2` — both of
which remain `False` throughout the entire winning path (`p21CIP`/`RBL2` are the two clamped
nodes that, once re-established, are supposed to suppress `CyclinA`/`CyclinE1` per the network's
own real rule: `CyclinA = !p21CIP&!RBL2&...`). Under SYNCHRONOUS update, `p21CIP`/`RBL2` and
`CyclinA`/`CyclinE1` all update simultaneously every round, so this specific "activator sneaks
ahead of inhibitor" race can never occur — it is a genuine ARTIFACT of the update-order assumption,
not a separate, unrelated dynamical phenomenon. This directly explains WHY the phenomenon is
one-directional (only the arrest-to-proliferation direction is vulnerable): the race requires an
activator (`CyclinA`/`CyclinE1`) to outrun a not-yet-updated inhibitor (`p21CIP`/`RBL2`); there is
no symmetric "arrest-node outrunning a proliferation-inhibitor" race available once already past
the synchronous escape threshold, because by then the relevant inhibitors are already permanently
off along the winning trajectory (checked directly, not merely inferred, via the 0/36 `k>=5`
schedule-robust results above).

## Verdict

**REJECTED** — the synchronous-only characterization of "safe" (`k<5`) vs "unsafe" (`k>=5`),
established by H-B7-9/10/12/13/14/15 and used throughout this entire B7 observability sub-arc, is
**NOT schedule-independent**. A materially smaller "adversarially-safe" threshold (`k_adv=1`, i.e.
effectively NONE of the previously-"safe" release states are actually safe against a worst-case
scheduler) replaces the synchronous `k*=5` for any application that cannot guarantee synchronous
(or otherwise sufficiently constrained) updating.

## FL Step 8a — Independent Reviewer

**Mandatory per `falsification-ladder.md`** — this is a PROMOTE/REJECT-with-surprising-magnitude
finding (skeptic-triggers.md Trigger 2: the result overturns a previously-established, multiply-
confirmed threshold from 6 prior experiments in this same sub-arc) reversing an entire sub-arc's
own working assumption. Narrowly scoped per this session's established lesson (avoid bundling
multiple code-execution checks in one pass; explicitly instructed to avoid `python -c`, which is
blocked in this environment's sandbox for subagents too).

**Verdict: CONFIRMED.** The reviewer independently reconstructed the `k=1, branch_1` case from
scratch (own BFS implementation, not calling `run.py`'s own `async_successors`/
`build_reachability_graph`/SCC logic): confirmed the synchronous baseline (release state really
reaches a genuine `GROWTH_ARREST` fixed point after 5 synchronous steps — not assumed), then
independently found a real 11-step asynchronous update order reaching a genuine `PROLIFERATION`
fixed point (re-verified zero further async successors at the target, i.e. not a transient).
Strong, unprompted corroboration: the reviewer's own independent BFS visited exactly **956**
states — matching this experiment's own reported number exactly, despite a fully separate
implementation — and the reviewer's own found path also never touches `p21CIP`/`RBL2`, the same
race-condition signature this decision.md's Mechanism section describes.

**Honest process note from the reviewer, worth keeping:** the reviewer could not use `Write` (not
in its declared toolset) and a `Bash` heredoc file-write was also blocked by a tool-scope guard —
it worked around this by piping its script directly into `python -`'s stdin (a `Bash` invocation,
not a file write). Logged as a LEDGER methodology finding, not something affecting this verdict.

## Kill Analysis (Anti-Overfitting Gate)

**What was killed:** the claim (implicit throughout H-B7-9 through H-B7-21) that the synchronous
`k*=5` threshold characterizes "safe to release" in any schedule-independent sense. It does not —
it characterizes safety ONLY under the specific synchronous-update assumption those experiments
each explicitly scoped themselves to (each one's own "What This Does NOT Mean" section already
named "does not test asynchronous update" as a limitation; this experiment is the first to
actually test it for the FATE itself, not just marker observability).

**What was NOT killed:**
- `k*=5`'s own existence and exactness UNDER synchronous update (H-B7-9/10/12) — untouched, still
  exactly as established.
- `j*=1`'s own minimal-observability finding UNDER synchronous update (H-B7-14/15) — untouched;
  this experiment does not re-test observability, only the fate's own schedule-(in)dependence.
- H-B7-16's own async OBSERVABILITY finding (DEGRADED-BUT-INFORMATIVE under RANDOM scheduling) —
  a different question (how well do markers predict fate under one specific, non-adversarial
  distribution over schedules) from this experiment's (can ANY fair schedule reach a different
  fate at all) — not contradicted, genuinely orthogonal.
- The rule-perturbation robustness findings (H-B7-17 through H-B7-21) — all explicitly scoped to
  synchronous update from the start, untouched by this schedule-focused finding.

**Relaxation Map:**
- **Weaken the fairness notion:** test whether a BOUNDED-delay fairness model (no node starved
  more than `L` steps, per claim.md's own named-but-untested restriction) recovers
  schedule-robustness for some finite `L` — the report's own "Критическая оговорка" named this
  exact distinction (`falsification-ladder.md`-style Minimal Relaxation Rule: one assumption at a
  time) as the natural next relaxation.
- **Quantify vulnerability, not just existence:** for the 8 fragile release-states, what FRACTION
  of fair schedules (not just "does one exist") reach `PROLIFERATION`? An existence result and a
  probability-under-some-schedule-distribution result are different claims — this experiment only
  establishes the former.
- **Extend to a real control policy:** does a policy that WAITS for `j` extra synchronous-style
  rounds before considering release (H-B7-14's own `j*=1` mechanism) also close the adversarial
  gap, or does the same race condition survive a `j`-round wait under async update specifically?
  Named, not attempted here.

## Revival Condition

Not applicable (not a REJECT of a hypothesis meant to be revived — this is a genuine, mechanistically
explained falsification of an implicit cross-experiment assumption). The three Relaxation Map
items above are concrete, named next steps if this thread is picked up again, not conditions for
"reviving" a killed claim.

## Scope note

Sixth experiment in the B7 observability sub-arc (after H-B7-13/14/15/16 and the rule-perturbation
quartet H-B7-17/18/19/20/21), directly motivated by `reports/2026-09-09-breakthrough-routes.md`
Route 5's own "Fairness обновлений... не даёт конечного верхнего срока" concern — previously named
as reserve/untested, now the first genuinely new empirical finding of this specific autonomous
continuation (H-CAT31-2 was a clean null, the Lean pilot formalized an already-known result;
H-B7-22 is a new, surprising, mechanistically-explained result). Reuses H-B7-13's own release-state
domain construction unchanged; introduces genuinely new machinery (exhaustive async reachability
via `networkx` SCC analysis) not present anywhere else in this project.
