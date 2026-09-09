# claim.md — 20260910-remy-tumorigenesis-starvation-asymmetry-h25

**Graph node:** `H-B7-25` (bridge `B7-KAUFFMAN-ATTRACTORS`) · **Tier:** Standard
**Parent:** `H-B7-22` (race-condition mechanism, framed symmetrically as "`p21CIP`/`RBL2` stay
stale"), `H-B7-24` (found the exact point-of-no-return step and that `CyclinE1` alone triggers
it). Directly closes H-B7-22's own remaining Relaxation Map item ("quantify vulnerability" was
closed by H-B7-23; "bounded-delay fairness" is the one item left open).

## EstimandOps L0 Gate

**Classification: DESCRIPTIVE.** Exact structural questions (node stability status, minimum
required starvation count) about a fully specified deterministic system at known states — not
causal, not statistical.

## Origin — a genuine asymmetry noticed while investigating H-B7-24's own point-of-no-return

H-B7-22's decision.md frames the mechanism symmetrically: "`CyclinA`/`CyclinE1` fire using STALE
`p21CIP=False`/`RBL2=False` values." A Compute-First Check (scratchpad, checking node-stability
status at each pre-commitment step of the `k=1, branch_1` shortest path) found this framing is
**not symmetric in practice**: `p21CIP` is UNSTABLE (its own rule already evaluates `True` —
i.e. it is actively "trying" to re-establish itself) at EVERY step from the release state through
the step just before the point of no return, while `RBL2` is STABLE (its own rule already agrees
with its current `False` value — it has no active tendency to change) throughout the same window.
**The escape requires `p21CIP` specifically to be starved of its turn; `RBL2` is passively
`False` regardless of scheduling, not a second active participant in the race.**

**Minimal Relaxation Rule compliance:** ONE change relative to H-B7-24 — instead of asking WHEN
commitment occurs, this experiment asks WHICH of the two "stale" inhibitors is actively
suppressed by adversarial scheduling versus passively uninvolved, at every state already computed
by H-B7-24's own shortest-path construction.

## Mechanism Claim Gate (Step 0a)

**Triggering sentence:** "`p21CIP`'s rule (`TP53&!CyclinE1&!AKT | Growth_inhibitors&!CyclinE1&
!AKT`) evaluates `True` at the release state and remains `True` (i.e. `p21CIP` is unstable, ready
to re-establish itself) for as long as `CyclinE1` has not yet fired — meaning `p21CIP`'s own
`!CyclinE1` term is what keeps it eligible to update, and once `CyclinE1` fires (the point of no
return, per H-B7-24), `p21CIP`'s own rule flips to `False` and blocking it becomes moot (too
late, exactly as H-B7-22's decision.md already noted for the `p21CIP` side specifically)."

**Check:** verified directly against the real `.bnet` rule text (not memory) and against the
computed node-stability status at every step of the `k=1, branch_1` shortest path (a scratchpad
diagnostic, not committed) — `p21CIP` unstable at steps 0-4, stable (rule agrees, now `False`) at
step 5 onward, exactly matching the hypothesis stated here BEFORE the full 8-condition sweep.

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | The shortest async-escaping path for each of H-B7-22's 8 confirmed `SCHEDULE_FRAGILE` release-states (already constructed by H-B7-24, reused unchanged) |
| **Falsifiable predicate** | At every pre-point-of-no-return step, is `p21CIP` unstable (actively ready to fire) while `RBL2` is stable (passively `False`)? |
| **Measurable outcome** | Per release-state: the stability status of `p21CIP` and `RBL2` at every step from 0 through the point-of-no-return step (inclusive), and the resulting minimum "starvation count" (number of consecutive turns `p21CIP` must be skipped) required for escape |

## Kill Criterion (set BEFORE running)

- **CONFIRMED (asymmetry generalizes):** in ALL 8 release-states, `p21CIP` is unstable (rule says
  `True`) at every step from 0 through (point-of-no-return step minus 1), and `RBL2` is stable
  throughout that same window (rule agrees with its current value).
- **REJECTED (asymmetry does not generalize):** at least one release-state shows the OPPOSITE
  pattern (`RBL2` unstable, `p21CIP` stable), or BOTH unstable, or BOTH stable, contradicting the
  `k=1/branch_1` spot-check's own pattern.
- **Direct answer to the bounded-fairness question:** the minimum starvation count for `p21CIP`
  (number of consecutive turns it must be skipped) equals the point-of-no-return step index
  already computed by H-B7-24 — reported per condition, not assumed to be a single universal
  number.

## What This Does NOT Mean

1. Does NOT claim `RBL2` is irrelevant to the network's overall dynamics — only that, ALONG THIS
   SPECIFIC ESCAPING TRAJECTORY, it happens to already be settled at `False` and does not need
   active suppression via scheduling, unlike `p21CIP`.
2. Does NOT prove a GENERAL bounded-fairness theorem (e.g. "any fairness bound `>= L` guarantees
   safety") — only that THIS specific shortest path requires `p21CIP` to be skipped a specific,
   reported number of times; a fairness-respecting scheduler could still find a DIFFERENT,
   longer escaping path with a different (potentially smaller) required starvation count, not
   searched for here.
3. Does NOT re-derive H-B7-24's own point-of-no-return step indices — reused directly, unchanged.

## MCID

Not applicable — exact stability/count questions, not a statistical comparison.
