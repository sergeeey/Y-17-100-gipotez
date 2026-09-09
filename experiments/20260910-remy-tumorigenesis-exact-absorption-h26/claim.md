# claim.md — 20260910-remy-tumorigenesis-exact-absorption-h26

**Graph node:** `H-B7-26` (bridge `B7-KAUFFMAN-ATTRACTORS`) · **Tier:** Full
**Parent:** `H-B7-22` (exhaustive reachability graph + SCC attractor detection, reused unchanged),
`H-B7-23` (Monte Carlo escape-probability estimates, the exact target this experiment computes
precisely and validates against). Directly redirected by the user, who — after reviewing a
`cross-domain`/`sci-hypothesis` report proposing an informal Kramers/large-deviations framing for
H-B7-22..25's own findings — identified (a) a real statistical weakness in that report's own
headline result (H9-A's `r²=0.89` rests on only 3 distinct barrier levels `{2,4,5}` with two
highly-correlated branches, not 8 independent points — informative "LEAD," not "PROMOTE") and
(b) via a real literature check, that asynchronous Boolean networks are ALREADY routinely
formalized as finite Markov chains with computable absorption probabilities in the published
literature (not a novel bridge) — and proposed the objectively stronger, exact reformulation
this experiment executes.

## EstimandOps L0 Gate

**Classification: DESCRIPTIVE.** Computing an exact quantity (absorption probability of a fully
specified finite Markov chain) for a fully specified deterministic-transition-structure system —
not causal, not a statistical estimate.

## Origin and design rationale

H-B7-23 measured escape probabilities via Monte Carlo (3000 trials/condition, uniform random
selection among currently-unstable nodes at each micro-step — a well-defined stochastic process).
H-B7-22 already proved (exhaustive SCC analysis, 0 cyclic attractors found anywhere) that this
process, restricted to any one release-state's reachable set, is a **finite absorbing Markov
chain**: every state either has outgoing transitions (transient) or none (absorbing — a genuine
fixed point). H-B7-23's own uniform-random-among-unstable selection rule assigns each transient
state's outgoing edges EQUAL probability `1/|unstable(x)|` — this is not an approximation of the
transition structure, it is the EXACT transition structure H-B7-23 already simulates. Standard
absorbing-Markov-chain theory (Kemeny & Snell 1960) therefore gives EXACT hitting/absorption
probabilities via a linear system, replacing H-B7-23's own Monte Carlo estimates with exact
numbers, at a fraction of the compute cost (no sampling variance, one linear solve instead of
3000 simulated trajectories).

**Minimal Relaxation Rule compliance:** ONE change relative to H-B7-23 — the SAME transition
model (uniform random among unstable nodes) is now solved EXACTLY via linear algebra instead of
approximated via Monte Carlo sampling. No new stochastic model, no new state space.

## Mechanism Claim Gate (Step 0a)

**Triggering sentence:** "the async reachability graph H-B7-22 already builds, restricted to any
one release-state's own reachable component, is a genuine finite absorbing Markov chain — every
transient state has `|unstable(x)| >= 1` outgoing edges each with probability `1/|unstable(x)|`,
and H-B7-22's own exhaustive SCC analysis (0 cyclic attractors, `n_ambiguous_attractors=0`
everywhere) already proved every absorbing class is a single fixed point, not a larger recurrent
set — the standard theory applies without modification."

**Check performed BEFORE the full sweep (Compute-First Check, scratchpad):** built the exact
transition matrix for `branch_1, k=1` (956 states, 953 transient, 3 absorbing: 1 `PROLIFERATION`,
2 `GROWTH_ARREST`), solved `(I - Q)q = b` via `numpy.linalg.solve` (0.03s), and got
`q(release_state) = 0.068866` — falling inside H-B7-23's own committed Monte Carlo 95% CI
`[0.0592, 0.0772]` (point estimate `0.0677`) for the exact same condition. Also directly verified
(re-running `simulate_transient_clamp_multi_with_release_state` for both branches at all 4
fragile `k` values) that `branch_1` and `branch_2`'s own release states are NOT identical at any
tested `k` — confirming the user's own point that they are correlated but genuinely distinct
computations, not literal duplicates, before trusting anything about their independence.

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | The exact absorbing Markov chain defined by H-B7-22's own async reachability graph, for each of H-B7-23's 10 tested (branch, k) conditions (the 8 fragile `k=1..4` plus `k=5` per branch as a positive control) |
| **Falsifiable predicate** | Does the exact absorption probability of the `PROLIFERATION`-class absorbing states, from the release state, fall within H-B7-23's own committed 95% Monte Carlo confidence interval for the same condition? |
| **Measurable outcome** | Per-condition exact escape probability, expected steps to absorption, and the oracle-gate pass/fail against H-B7-23's own CI |

## Kill Criterion (set BEFORE running the full sweep)

- **Oracle gate (mandatory, checked first, per the user's own explicit design):** for ALL 10
  conditions, the exact probability must fall inside H-B7-23's own reported 95% CI. If it does
  NOT for some condition, STOP — this indicates either (a) a Monte Carlo semantics mismatch
  between H-B7-23's own trial code and this experiment's transition-matrix construction, (b) an
  incorrectly-built transition matrix, or (c) a misclassified absorbing state — diagnose before
  trusting any exact number from that condition.
- **`k=5` positive control:** exact probability must equal exactly `1.0` for both branches (H-B7-22
  already proved `SCHEDULE_ROBUST` there — only `PROLIFERATION` reachable at all).
- **This experiment does NOT, by itself, resolve the large-deviation/Kramers question** (per the
  user's own explicit priority order) — it only replaces Monte Carlo estimates with exact numbers
  and computes expected absorption time. Re-assessing the log-linear/large-deviation framing on
  the now-EXACT numbers (not the Monte Carlo estimates) is named as future work, not attempted
  here.

## What This Does NOT Mean

1. Does NOT attempt path decomposition or per-path probability-mass analysis (the user's own
   explicitly-named FOLLOW-UP question, "why do the exact probabilities take these specific
   values") — this experiment computes the exact aggregate probability and expected absorption
   time only, named as the next natural step, not attempted here.
2. Does NOT claim this transition-matrix-solve approach is itself novel in the Boolean-network
   literature — per the user's own literature check, asynchronous-BN-as-Markov-chain is an
   established technique; the contribution here is applying it to THIS project's own specific
   model and validating it against THIS project's own Monte Carlo data, not inventing the method.
3. Does NOT re-derive or re-test H9-A's own large-deviation/log-linear claim from the earlier
   cross-domain report — deliberately deferred until exact (not Monte Carlo) numbers exist for
   more than the current 3 barrier levels, per the user's own stated priority order.

## MCID

Not applicable — exact linear-algebra computation, not a statistical estimate with sampling
uncertainty of its own (though it IS compared against H-B7-23's own Monte Carlo CI as an oracle
gate, which does carry sampling uncertainty on the Monte Carlo side).
