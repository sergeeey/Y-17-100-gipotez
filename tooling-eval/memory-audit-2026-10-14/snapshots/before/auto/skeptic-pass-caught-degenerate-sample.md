---
name: skeptic-pass-caught-degenerate-sample
description: "Real incident where a context-asymmetric skeptic pass caught a flaw that 8+ rounds of manual self-review missed, in an extended autonomous Y-17 session"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1d8443cd-ffe1-43e0-bdb5-efd0ebc5eada
  modified: 2026-09-07T06:01:23.405Z
---

Running an actual context-asymmetric `Agent(skeptic)` pass (FL Step 8a — claim.md + code only,
no session history, no reasoning chain) catches real flaws that manual self-review reliably
misses, even across many experiments in the same session with the same self-review discipline
applied each time.

**Why:** in the 2026-09-07 Y-17 session, the `iteration-guard` Evaluator-Optimizer cap blocked
the `reviewer` agent partway through the B3 bridge work, and no skeptic agent was invoked again
for the rest of a very long session (H-B2-1h through H-B2-1l, ~8 more experiments) — every
CONFIRMED verdict in that stretch substituted "manual imitation" of skeptic discipline (asking
myself what a skeptic would look for) instead of an actual independent agent call. When a
session-summary report to the user flagged this gap explicitly and a real skeptic pass was
finally run on the session's strongest claim (H-B2-1l: κ(V) explains M1 in "both independent
populations"), it immediately found a genuine, non-cosmetic flaw: one of the two "independent
populations" (a 9-point N-sweep) had its RNG seed hard-coded, making it a single deterministic
curve, not 9 independent draws — invalidating the central "cross-population corroboration"
argument. This exact flaw survived at least 3 rounds of my own self-review (writing claim.md,
writing decision.md, writing the session report) because self-review does not reliably catch
"is this sample actually independent" the way an agent explicitly tasked to falsify does.

**How to apply:** don't let an Evaluator-Optimizer cap or agent-unavailability quietly become a
standing substitution for FL Step 8a across an entire long session. When a cap blocks the
reviewer/skeptic path, that should be flagged as a real, accumulating methodological debt (as
[[y17-lab-repo-and-variant-c]] and this project's own `tooling-eval/LEDGER.md` are set up to
track), not silently absorbed as "I did the equivalent manually." At the first natural
opportunity (a cap reset, a fresh session, or a user check-in), actually run the skeptic on the
highest-value claims accumulated during the gap — it is worth the cost even after the fact,
per this incident's own result (H-B2-1l downgraded CONFIRMED → WEAKENED, with a real,
previously-unnoticed statistical error identified and fixed).

**Update (same session, immediately after): ran the skeptic on 3 accumulated experiments in a
row. All 3 found genuine, previously-uncaught, escalating-severity flaws:**
1. H-B2-1l (above) — degenerate "second population."
2. H-B2-1j — a "single changed assumption" (N_DIM) was actually 3 simultaneous changes
   (dimension, spectral range, coupling-block size); the SAME confound had already been
   recognized and explicitly avoided one experiment later in the same session (H-B2-1k's own
   claim.md), but that recognition never propagated backward to correct the original.
3. H-B2-1k (most severe) — a pre-registered "≥1 sign change in 9 points" kill criterion is
   passed by pure noise with probability ≈0.999994 (only 2 of 9! orderings are monotonic) — a
   textbook FL Step 4a floor defect, missed because the experiment's own boilerplate assumed
   "descriptive" experiments don't need a floor/null check. My own decision.md had even
   pre-written a defense against "this could just be noise," and that defense was itself
   mathematically invalid (didn't depend on swing magnitude, which is what it claimed to rest on).

3-for-3, strictly escalating severity, on claims already carrying full FL documentation and
multiple rounds of my own private re-review. Self-review did not degrade gracefully on this
sample — it missed real, large, mechanically-checkable problems every single time. Treat "I
reviewed it myself carefully" as much weaker evidence than it feels like, specifically for:
(a) whether two "populations" are actually statistically independent, (b) whether a claimed
single changed variable is really the only thing that changed, (c) whether a pre-registered
pass/fail criterion has any power to fail on pure noise.

**Final update: ran the skeptic on 2 more (5 total across the whole H-B2-1* arc tail). 5/5
found real issues, not monotonic in severity — a genuine spread from mild to devastating:**
4. H-B2-1i — mildest: the skeptic explicitly confirmed the core 30 raw measurements were real
   and independent; only the MODERATE label's framing was weakened (Tukey fences on a
   right-skewed distribution; a log-scale reading of the same number reads as unremarkable).
5. H-B2-1h — strongest: `np.random.default_rng(SEED)` was re-seeded to the SAME constant on
   every call across a 10-point "sweep," so all 10 points evaluated ONE fixed random direction
   linearly dilated by a scalar, not 10 different matrices. I independently verified this by
   direct computation (off_diagonal(2c) == 2×off_diagonal(c) to machine precision) before
   trusting it. Consequence: for the nilpotent coupling structure involved, the measured
   quantity is PROVABLY a bounded-degree polynomial in the swept parameter — true exponential
   growth was algebraically impossible, no matter what any R² comparison said. The claimed
   "exponential growth, R²=0.9994" verdict was flipped to REJECTED on mathematical proof, not
   just a statistical re-argument.

**Cross-cutting root cause across 4 of the 5 findings above:** the same subtle bug pattern — a
fixed or self-referencing RNG seed silently defeating an experiment's own claim of testing N
independent things — appeared in DIFFERENT disguises in H-B2-1l (a "second population" that was
one curve), H-B2-1k (sweep points that were independent draws with a floor-defect criterion,
the opposite-shaped instance of the same seed-handling family of bugs), and H-B2-1h (sweep
points that were NOT independent draws, the direct instance). Worth a specific verification
habit: whenever an experiment claims "N points/samples/draws," check exactly how the RNG is
seeded at each one — fresh each call with a constant seed is a red flag in either direction
(sometimes over-independent when it should be one curve, sometimes falsely coherent when it
should be independent).

**Final update (session end): ran the skeptic on the last 2 experiments in the systematic sweep
(7 total across the entire session — every flagged "no real skeptic pass" experiment). 7/7 found
real issues:**
6. H-B3-1l (bridge B3, not B2 — same bug pattern generalizes across bridges) — found a second
   layer on top of a confound I had ALREADY self-caught and documented: `classical_ac1_peak_date`
   independently verified (direct read of committed `metrics/run.json`) to be BEFORE
   `tda_betti_peak_date` — the code's classical-statistic selection rule was oracle-informed
   (picks whichever is closer to the known transition) for the positive case but "earliest of
   two" for negative controls, an asymmetry that itself explains part of the reported TDA
   advantage. Lesson: self-catching one confound does not mean the review is done — a skeptic
   pass on an "already confessed" experiment still found something new.
7. H-B3-1m (the LAST of the 7) — the single most severe finding of the whole 7-pass sweep, and a
   NEW bug category (not RNG seeding this time): the experiment's central mechanistic
   justification for why an AND-gate of two statistical tests should add specificity ("test B
   targets a different signal than test A, so a false positive on A won't also fire B") was
   independently proven FALSE by direct computation — for a `Pettitt` change-point test combined
   with a Kendall-tau trend test, Pettitt has near-full power against pure monotone trend alone
   (verified: for a strictly monotone series with zero noise, K=n²/4 exactly, matching a clean
   closed-form derivation, giving p≈3.7e-5 at n=30 — no step-change required at all). General
   lesson, NOT specific to this one test pair: combining two statistical tests via AND does NOT
   automatically buy specificity — verify computationally that the second test's power profile
   is actually orthogonal to the first's before claiming the combination filters out what the
   first alone would miss. A plausible-sounding "these target different signals" story is not a
   substitute for checking the second test's actual power curve against the first's failure mode.

**Session-final tally: 7 out of 7 context-asymmetric skeptic passes found real, previously-
uncaught problems**, spanning two different project bridges (5 on one, 2 on the other), severity
ranging from a label-only weakening (core data confirmed intact) to two separate mathematically/
computationally airtight refutations (H-B2-1h: claimed exponential growth was algebraically
impossible for the tested construction; H-B3-1m: the claimed test-combination mechanism was
disproven by direct calculation). Zero experiments in the flagged set survived unchanged. This is
about as clean a demonstration as this session produced that self-review — even careful,
FL-disciplined, repeated self-review — is not a substitute for an actual adversarial pass with a
fresh, context-blind reader, regardless of how confident the author feels or how many times they
have already re-checked their own work.
