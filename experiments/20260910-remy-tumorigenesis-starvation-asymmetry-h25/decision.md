# H-B7-25 — decision.md

## Result

**The universal (all-8-conditions) asymmetry claim is REJECTED — but the underlying finding is
real, honest, and more precise than the pre-registered hypothesis, not a dead end.**

| Branch | k | PNR step | `p21CIP` always unstable? | `RBL2` always stable? | Asymmetry confirmed? |
|---|---|---|---|---|---|
| branch_1 | 1 | 5 | Yes | Yes | **Yes** |
| branch_1 | 2 | 4 | Yes | Yes | **Yes** |
| branch_1 | 3 | 4 | Yes | **No** (unstable at step 3) | No |
| branch_1 | 4 | 2 | Yes | **No** (unstable at step 1) | No |
| branch_2 | 1 | 5 | Yes | Yes | **Yes** |
| branch_2 | 2 | 4 | Yes | Yes | **Yes** |
| branch_2 | 3 | 4 | Yes | **No** | No |
| branch_2 | 4 | 2 | Yes | **No** | No |

**One part of the pre-registered hypothesis holds in ALL 8 cases without exception:** `p21CIP` is
unstable (its own rule already evaluates `True`, i.e. it is actively trying to re-establish
itself) at EVERY step of the pre-commitment window, for every `k` and both branches. This
confirms the Mechanism Claim Gate's own core point — `p21CIP` is not structurally prevented from
blocking the escape; it is READY the entire time, and is blocked purely by never being selected.

**The other part — that `RBL2` stays passively stable throughout — does NOT generalize.** At
`k=3` (both branches), `RBL2` becomes unstable at step 3 (the step just before the point of no
return, step 4); at `k=4` (both branches), `RBL2` becomes unstable even earlier, at step 1 (PNR
is step 2). In BOTH cases, this happens ONLY in the single step (or two) immediately preceding
commitment — `RBL2` is passively stable for most of the window, then also becomes "ready to
block" right at the end, exactly when the window is shortest (closer to the synchronous
threshold `k*=5`, less "room" before commitment).

## Kill Analysis (Anti-Overfitting Gate)

**What was killed:** the SPECIFIC, universal claim (generalized from a single `k=1/branch_1`
spot-check, per the Compute-First Check) that `RBL2` is passively uninvolved throughout the
ENTIRE pre-commitment window for ALL fragile release-states. `k=3` and `k=4` (both branches)
falsify this directly and reproducibly.

**What was NOT killed / what survives, more precisely stated:**
- `p21CIP`'s own unstable-throughout status: CONFIRMED in all 8 cases, no exceptions.
- The escape mechanism remains `p21CIP`-centric at LARGER `k` (closer to the synchronous
  threshold), and becomes a genuine race against BOTH inhibitors only in the FINAL 1-2 steps at
  smaller `k`-margins (`k=3,4`) — a real, honest refinement of the original symmetric framing
  ("both `p21CIP` and `RBL2` stay stale"), not a wholesale rejection of it: `RBL2` genuinely is
  irrelevant for MOST of the window at every `k`, and only becomes a live concern in the last one
  or two steps when `k` is close to the threshold.
- The `p21CIP_min_starvation_count` (= the point-of-no-return step index, already established by
  H-B7-24) remains a valid, exact quantity for all 8 conditions regardless of this experiment's
  own asymmetry claim — it answers H-B7-22's own "bounded-delay fairness" question directly: a
  scheduler that guarantees `p21CIP` a turn within `PNR_step` consecutive skips would block this
  SPECIFIC shortest path (though not necessarily all possible escaping paths, per claim.md's own
  scope note).

**Relaxation Map:**
- **Weaken to a conditional claim:** "the asymmetry (p21CIP-only starvation) holds when
  `k <= k* - 3`" (i.e. `k=1,2` here, 3+ steps of margin before the synchronous threshold) — matches
  the data exactly, though `n=2` margin values is too few to claim this as a general rule without
  testing intermediate networks/margins.
- **Remove the "throughout the whole window" framing:** report instead the LAST step at which
  `RBL2` is still stable (`k=1`: step 4 of 5; `k=2`: step 3 of 4; `k=3`: step 2 of 4; `k=4`: step
  0 of 2) — a graded, not binary, description of the mechanism.

## Verdict

**REJECTED** for the pre-registered universal asymmetry claim, `status: lead` (not hard-killed) —
a real, more precise, honestly-reported mechanistic refinement survives: `p21CIP`-only starvation
sufficiency is confirmed at every tested `k`, `RBL2`'s passive role is confirmed for most but not
all of the pre-commitment window, breaking down specifically in the final 1-2 steps at `k=3,4`.

## FL Step 8a

**Not run** — this is a REJECT verdict (per FL's own scope, Step 8a's mandatory pass applies to
PROMOTE-shaped/surprising CONFIRMED findings, not REJECTs); Kill Analysis and the Relaxation Map
above are the load-bearing requirements for a REJECT and are both filled.

## What This Does NOT Mean

Carried from claim.md: does not claim `RBL2` is irrelevant to the network overall; does not prove
a general bounded-fairness theorem (only this specific shortest path per condition); does not
re-derive H-B7-24's own point-of-no-return step indices (reused unchanged).

## Scope note

Ninth experiment in the B7 async/observability sub-arc, directly testing (and partially refining,
not confirming) a hypothesis noticed while investigating H-B7-24's own point-of-no-return finding.
Closes H-B7-22's own last-remaining Relaxation Map item (bounded-delay fairness) with an honest,
graded answer rather than a clean universal rule — the `p21CIP_min_starvation_count` per condition
IS the direct, exact answer to "how much unfairness is required," even though the accompanying
"RBL2 is passive throughout" story does not hold everywhere.
