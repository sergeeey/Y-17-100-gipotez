# decision.md — 20260910-remy-tumorigenesis-exact-absorption-h26

## Verdict: **CONFIRMED**

## Result Table (all 10 conditions, `metrics/run.json`)

| branch | k | exact P(escape) | Monte Carlo (H-B7-23) | MC 95% CI | oracle gate | E[steps to absorb] |
|---|---|---|---|---|---|---|
| branch_1 | 1 | 0.068866 | 0.067667 | [0.0592, 0.0772] | PASS | 8.877 |
| branch_1 | 2 | 0.137731 | 0.143333 | (H-B7-23 own) | PASS | 10.364 |
| branch_1 | 3 | 0.185185 | 0.187333 | (H-B7-23 own) | PASS | 7.985 |
| branch_1 | 4 | 0.333333 | 0.338333 | (H-B7-23 own) | PASS | 5.542 |
| branch_1 | 5 | 1.000000 | 1.000000 | (H-B7-23 own) | PASS | 1.000 |
| branch_2 | 1 | 0.068866 | 0.065000 | (H-B7-23 own) | PASS | 8.877 |
| branch_2 | 2 | 0.137731 | 0.134000 | (H-B7-23 own) | PASS | 10.364 |
| branch_2 | 3 | 0.185185 | 0.181333 | (H-B7-23 own) | PASS | 7.985 |
| branch_2 | 4 | 0.333333 | 0.338667 | (H-B7-23 own) | PASS | 5.542 |
| branch_2 | 5 | 1.000000 | 1.000000 | (H-B7-23 own) | PASS | 1.000 |

**Oracle gate: 10/10 passed.** Every exact probability falls inside H-B7-23's own committed 95%
Monte Carlo CI for the identical condition. `k=5` positive control gives exactly `1.0` on both
branches, as required by claim.md's own Kill Criterion.

## Mandatory checks against claim.md's own Kill Criterion

- [x] Oracle gate: ALL 10 conditions inside H-B7-23's own 95% CI — **PASS, 10/10**
- [x] `k=5` positive control: exactly `1.0` both branches — **PASS**
- [x] This experiment does NOT re-assess the large-deviation/Kramers claim — confirmed, not
  attempted here (deferred per the user's own priority order, item 4)

## Unplanned observation (not a claim of this experiment — flagged, not asserted)

`branch_1` and `branch_2` give numerically **identical** exact escape probabilities at every
tested k (0.068866 / 0.137731 / 0.185185 / 0.333333), despite `test_branch_release_states_are_not_identical`
confirming their release states ARE genuinely distinct at all four k. This is a real, tool-verified
fact about this specific pair of computations, not a hypothesis being promoted here — no mechanism
for it is claimed or tested in this experiment. Two structurally plausible explanations (not
distinguished by anything computed so far): (a) the two release states' reachable subgraphs happen
to be graph-isomorphic under the classification used here (PROLIFERATION vs GROWTH_ARREST), so the
linear system produces the same scalar despite different underlying states; (b) coincidence at this
specific model's parameter values. **Not investigated further here** — flagged as a Pearl Registry
candidate (see below), not chased down within this experiment's own scope, per the Kill Criterion's
explicit deferral of path-decomposition/mechanism work to a later experiment.

**ADDENDUM (2026-09-10, decisive check from the deep external novelty audit,
`reports/2026-09-10-deep-external-novelty-audit.md`):** a second, distinct unexplained numeric
fact was found and verified in the SAME branch_1 sequence: `P(k=1)=119/1728`, `P(k=2)=119/864 =
2*119/1728` exactly (`fractions.Fraction.limit_denominator`, match to full float64 precision --
not plausible as coincidence given the two values come from independently solved linear systems
of different sizes). `P(k=3)=5/27`, `P(k=4)=1/3` are also clean small fractions. No mechanism for
the exact P(k=2)=2*P(k=1) doubling is claimed or tested here -- flagged as a second Pearl Registry
entry (`pearl_registry/INDEX.md`, 2026-09-10 row), not chased down within this addendum's scope.

## FL Step 8a — Independent Reviewer

Full-tier claim that reshapes trust in H-B7-23's own prior Monte Carlo numbers by replacing them
with exact ones — mandatory per FL Step 8a. Context-asymmetric: reviewer given `claim.md` +
`run.py` only, no reasoning chain, scoped narrowly (per this session's own established
reviewer-turn-budget lesson) to ONE reconstruction: rebuild the exact transition matrix for
`branch_1, k=2` independently and verify the escape probability and oracle-gate pass/fail.

**Verdict: CONFIRMED-REAL.** Reviewer wrote a fully independent implementation — own `.bnet`
parser, own boolean evaluator (`compile()`/`eval()`, not the `boolean` package this experiment's
own `run.py` uses), own BFS/absorbing-Markov-chain solver, sharing only `numpy`'s generic linear
solver as common tooling. Per `falsification-ladder.md`'s own Independent Verification Strength
Ladder, this is **"independently-written code" (Strong tier)**, not a same-model rerun of the
existing code.

- `exact_escape_probability`: reviewer `0.1377314814814815` vs committed `0.1377314814814815` — **diff 0.0**
- `expected_steps_to_absorption`: reviewer `10.364071822554978` vs committed `10.36407182255498` — diff `1.8e-15` (floating-point rounding only)
- Graph structure independently matched: 954 states visited, 951 transient, 1 PROLIFERATION absorbing state, 2 GROWTH_ARREST absorbing states, 0 ambiguous
- Falls inside H-B7-23's own Monte Carlo 95% CI `[0.1312, 0.1563]`, as required by the oracle gate

**Process note:** the first reviewer invocation stalled at its 12-turn limit re-discovering the
`python -c`-blocked-in-sandbox workaround (same recurring root cause first found at H-B7-21's own
reviewer). `SendMessage`-based continuation was attempted per this session's own standing memory
note, but confirmed NOT available as a callable tool in this environment (`ToolSearch` found no
match) — fell back to a fresh, fully self-contained `Agent()` prompt, which completed cleanly.

## Skeptic Concerns

No `[FALSIFIED]` concerns raised — reviewer's independent reconstruction matched the committed
value exactly (to floating-point precision), no dismiss/accept/mitigate entries needed.

## Caveats / What This Does NOT Mean

Per claim.md's own "What This Does NOT Mean" section — unchanged and reaffirmed by this result:

1. Does NOT attempt path decomposition or per-path probability-mass analysis. The branch_1==branch_2
   numerical coincidence noted above is exactly the kind of question that decomposition would
   actually answer — named as the natural next step, not attempted here.
2. Does NOT claim the transition-matrix-solve approach is itself novel in the Boolean-network
   literature (per the user's own literature check).
3. Does NOT re-derive or re-test H9-A's own large-deviation/log-linear claim — deliberately deferred.

## MCID

Not applicable (exact linear-algebra computation; oracle-gate comparison inherits H-B7-23's own
Monte Carlo sampling uncertainty, already expressed as a 95% CI, not a separate MCID here).
