# H-B7-15 — decision.md

## Result

**The orbit is much smaller than the previously-tested sample range — a genuine finding, not
merely a technicality.** The clamped-trajectory orbit (state after `k` clamped steps, `p21CIP=
RBL2=False` forced) reaches a fixed point after only **7 states** (`orbit_length=7,
cycle_start_index=6, cycle_period=1`) — identically on BOTH branches. This means `k=1..40`
(H-B7-13/14's own tested range) was already a strict superset of every achievable release-state:
`k=6..40` all repeat the SAME fixed-point state. `orbit_fully_within_previously_tested_k_1_to_40:
true` — confirmed directly from the metrics, not assumed.

**Regression check (Substrate Gate) passed exactly:** restricting the new exhaustive domain to
`k≤40` and re-running `find_collisions` for M1/M2 at `j=0` reproduces H-B7-13/14's own committed
collision count (`M1=1, M2=1`) exactly (`matches_h_b7_13_14: true`).

**Theorem-level verdict, both candidates:** `n_collisions=0` for M1 AND M2 at `j=1`, computed over
the COMPLETE 12-state domain (6 states × 2 branches) — not a sample, the FULL closure of every
release-state achievable for ANY `k≥1`, since the orbit provably repeats beyond `k=6`.

## FL Step 8a — Independent Reviewer Verdict (mandatory: PROMOTE-shaped, surprising exhaustive
result, skeptic-triggers.md Trigger 2)

An independently-invoked `Agent(reviewer)`, context-asymmetric (files only, no reasoning chain),
given 2 narrowly-scoped checks, both told explicitly to try to BREAK the claims:

- **Check 1 (orbit-length=7 is correct, not an early false-positive cycle detection):**
  reimplemented the walk INDEPENDENTLY (not importing `walk_clamped_trajectory_until_cycle` —
  rebuilt it from `synchronous_step`/`clamp_rule` directly). **CONFIRMED** — matched
  `orbit_length=7, cycle_start_index=6, cycle_period=1` exactly for both branches, and went
  further than asked: exhaustively compared all `C(7,2)=21` pairs of trajectory states for
  branch_1 (not just the one pair the walk's own dict-based detection flagged) — zero duplicate
  pairs in indices 0–5, `state[6]` matches no earlier state except itself. Rules out a
  hash-collision or shortcut-comparison bug specifically.
- **Check 2 (j=1 exhaustive sufficiency, and j=0 collision, both independently re-derived):**
  called `simulate_transient_clamp_multi_with_delayed_observation` directly for k=1..6 on both
  branches, independent of `build_exhaustive_domain`. **CONFIRMED** — at j=1, the only repeated
  `(Growth_arrest, Proliferation)` projection is `(False,False)` at k=2,3,4 on both branches, and
  ALL SIX of those rows share `fate=GROWTH_ARREST` (no collision). At j=0, the SAME k=3,4 vs k=5
  rows collide exactly as H-B7-13/14 already established, independently cross-checked against
  H-B7-13's own committed collision member list.

**Verdict: `[CONFIRMED-REAL]`**, both checks, no counter-example found on either. Promoted freely.

## Verdict

**THEOREM-LEVEL CONFIRMED**, per claim.md's own pre-registered kill criterion. Within this Boolean
network, for the transient `do(p21CIP=0, RBL2=0)` clamp starting from either known
`Growth_arrest` fixed point:

> The observable pair `{Growth_arrest, Proliferation}`, read exactly ONE synchronous step after
> the clamp is released, determines the eventual fate (relapse to `Growth_arrest` vs escape to
> `Proliferation`) EXACTLY and EXHAUSTIVELY — for every one of the finitely many achievable
> release-states (not a sample of them), on both bistable branches.

This is the closed, complete statement H-B7-14's own sampled sweep could only gesture at.

## Kill Analysis (Anti-Overfitting Gate)

**What was killed (unchanged from H-B7-13):** instant observability (`j=0`) at these marker sets.

**What is now CLOSED, not merely surviving:** H-B7-14's `j*=1` sufficiency claim is no longer a
sampled result that COULD in principle be falsified by an untested `k` — the achievable-state
domain has been shown to be finite and fully enumerated (7 states per branch), and every single
one has been checked. There is no remaining untested `k` within this protocol that could overturn
the verdict.

**Relaxation Map for what remains genuinely open (unchanged from H-B7-13/14, not touched here):**
- Does the small orbit (7 states) and `j*=1` generalize to a DIFFERENT starting attractor, a
  different pair of clamped nodes, or asynchronous updating? None of these are tested here — same
  standing caveats as the whole sub-arc.
- Is `orbit_length=7` itself a general property of this network's clamped dynamics, or specific to
  this exact clamp/starting-state pair? Not characterized — would need testing other clamp/start
  combinations to know.

## Revival Condition

Not applicable in the REJECT sense — nothing here was rejected. The forward-looking equivalent:
this result is now CLOSED for the exact protocol tested; any future work extending it (different
clamp targets, different starting states, asynchronous updating) is a NEW claim requiring its own
Zero-Signal Gate and kill criterion, not a revival of anything here.

## Skeptic Concerns (superseded by the independent reviewer pass above; kept for the audit trail)

- "Could the small orbit_length=7 be a bug that stops the walk early?" → **Checked, dismissed** —
  the independent reviewer's own from-scratch reimplementation confirmed the exact same orbit
  length and additionally ruled out a hash-collision-style false positive via exhaustive pairwise
  comparison.
- "Is 'exhaustive over the clamped-trajectory orbit' actually exhaustive over anything a real
  release decision would face?" → **Accepted limitation, explicitly named in claim.md item 1** —
  this is exhaustive within THIS protocol's reachable domain, not the full hidden state space; a
  materially different intervention could in principle reach states outside this orbit entirely.

## Scope note

Third and final step (for now) of the observability sub-arc within Bridge 7: H-B7-13 (REJECTED at
j=0) → H-B7-14 (CONFIRMED, sampled, j*=1) → H-B7-15 (CONFIRMED, exhaustive, j*=1, closed). Direct
continuation of the user's own explicit request (2026-09-10) to turn the sampled result into a
"model-level theorem" via exhaustive verification over the finite state graph — delivered exactly
as asked, using the structural fact (deterministic finite system must cycle) already implicit in
this bridge's own `find_attractors`/`run_until_attractor` machinery from H-B7-1/H-B7-3, applied
here to the clamped phase specifically for the first time in this arc.
