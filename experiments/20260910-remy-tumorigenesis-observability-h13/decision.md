# H-B7-13 — decision.md

## Result

**Substrate/sanity checks both passed as required by claim.md before the candidate result counts:**
- **Floor** (`M = {DNA_damage}`, a branch input constant along any single trajectory):
  `n_collisions=1` — correctly detects insufficiency (the same DNA_damage value spans both
  GROWTH_ARREST and PROLIFERATION outcomes on both branches). Detector is not vacuously permissive.
- **Ceiling** (`M = full 35-node state`): `n_collisions=0` — tautologically sufficient, as required.
  Detector is not vacuously restrictive either.

**Both candidate marker sets: REJECTED.**

| Marker set | Members | Collisions | Verdict |
|---|---|---|---|
| M1 `{Growth_arrest, Proliferation}` | 2 markers, this arc's own decision readouts throughout H-B7-4..12 | 1 group, 6 members | **INSUFFICIENT** |
| M2 `{Growth_arrest, Proliferation, p21CIP, RBL2}` | M1 + the 2 directly-clamped nodes | 1 group, 6 members (identical) | **INSUFFICIENT** |

**The single collision, exact and reproducible:** at release moment, both branch_1 and branch_2
read `(Growth_arrest=False, Proliferation=False, RBL2=False, p21CIP=False)` for `k ∈ {3, 4}` AND
for `k=5` — but `k=3,4` relapse to `GROWTH_ARREST` while `k=5` escapes to `PROLIFERATION`. Adding
`p21CIP`/`RBL2` to M1 did not break the collision because BOTH nodes are still `False` at release
for all three colliding `k` values — the clamp has not yet allowed the downstream feedback
(`RBL2 = !CyclinE1 & !CyclinD1`, `CyclinE1`'s own commitment) to visibly diverge at the exact
release step. The observable readouts LAG the trajectory's actual committed fate by roughly one
synchronous step, at exactly the threshold where it matters most.

**Interpretation:** the escape/relapse decision is not yet legible in these 2-4 output-phenotype
markers AT the release instant — it becomes legible only a few steps later, once the underlying
`CyclinE1`/`RBL2` feedback loop has propagated. A release policy that decides at the exact instant
of clamp removal, observing only `{Growth_arrest, Proliferation}` (or that pair plus the clamp
targets), CANNOT distinguish the safe (`k=3,4`) from unsafe (`k=5`) case in this domain.

## Verdict

**REJECTED** for both M1 and M2, per the pre-registered "BOTH REJECTED" branch of claim.md's kill
criterion. This is a clean, exact, reproducible falsification (not a statistical/sampled result —
the domain was enumerated in full, 80/80 release-states across both branches and `k=1..40`).

## Kill Analysis (Anti-Overfitting Gate)

**What was killed:** the specific claim that this arc's own existing output-phenotype nodes
(`Growth_arrest`, `Proliferation`), observed exactly at the instant of clamp release, are
sufficient to decide safely whether to release — even when augmented with the two directly-clamped
nodes (`p21CIP`, `RBL2`). Both marker sets fail on the SAME collision, at exactly the safety-
critical threshold (`k*=5`).

**What was NOT killed:**
- The underlying dynamical system remains fully deterministic and fully identifiable from the
  COMPLETE state (ceiling test, tautological but structurally confirmed correct).
- The existence of SOME sufficient small marker set is not disproven — only these two specific
  candidates, at this specific decision instant, fail.
- `k*=5`'s clean, monotone threshold structure (H-B7-10/H-B7-12) is unaffected; this experiment
  does not touch or re-test the threshold's existence, only whether it is legible from M1/M2 alone.

**Relaxation Map for surviving assumptions (one change per future variant, per Minimal Relaxation Rule):**
- **Remove** the "observe exactly at release instant" assumption: re-run the SAME collision search
  observing M1/M2 one or two steps AFTER release (while dynamics continue, before deciding) instead
  of at the instant of removal — cheapest, most likely fix given the observed one-step lag.
- **Weaken** the marker set size constraint: search for the MINIMAL marker set (not just M1/M2) that
  eliminates the collision at the exact release instant — a genuine "minimal observability"
  question, not yet attempted here.
- **Replace** the release-instant decision rule with a different DECISION POLICY class entirely
  (e.g., a policy that waits for markers to stabilize for `j` consecutive steps before releasing,
  not a snapshot rule) — a structurally different claim, out of scope for this cheap first test.

## Revival Condition

**Contingent, not theorem-level** — the kill rests on (a) the specific instant chosen (release
moment, not a few steps later) and (b) the specific two marker-set candidates tested (M1, M2), not
an exhaustive search over all marker sets or decision instants. Revival requires relaxing (a) or (b):

- **Cheapest, most likely to succeed:** re-run the identical collision search with markers observed
  `j` steps after release (`j=1,2,3`) instead of at the instant of removal — directly named above in
  the Relaxation Map's "Remove" row, and directly motivated by the observed one-step lag mechanism.
- **Minimal marker search:** if the release-instant timing is kept fixed, search over other small
  marker subsets (not just M1/M2) — e.g. adding `CyclinE1` directly (the feedback loop's own
  reported node, one step upstream of `RBL2`'s own rule) is a concrete, named next candidate.
- **No revival** on the exact claim as tested (M1 or M2, AT the release instant, this domain) — that
  specific combination is REJECTED and should not be retried unmodified.

## Skeptic Concerns (pre-answered, `[SKEPTIC-PRE-ANSWERED]` — REJECT verdict, not PROMOTE, so Step
8a's mandatory skeptic pass does not apply per FL's own scope; Kill Analysis + Revival Condition are
the load-bearing requirements for a REJECT and are both filled above. Predictable concerns answered
directly here since this is a small, exact, deterministic result, not a statistical claim requiring
independent falsification pressure)

- "Domain is only 80 states (2 branches × 40 k) — too small to generalize" → **Accepted limitation,
  explicitly scoped in claim.md § What This Does NOT Mean (item 1)**: this result is about the
  reachable release-state domain THIS arc's own protocol defines, not the full ~2^31 hidden state
  space. The collision found is exact WITHIN that domain, regardless of the domain's size.
- "The collision might be a bug in `simulate_transient_clamp_multi_with_release_state`, not a real
  finding" → **Checked, dismissed**: `test_release_state_captured_before_release_not_after`
  independently confirms the function's FINAL-state outputs (post-release attractor) match H-B7-10's
  own already-committed ground truth exactly for k=4 (GROWTH_ARREST) and k=5 (PROLIFERATION) — the
  new function's only addition is capturing an intermediate snapshot using the SAME already-verified
  `synchronous_step`/`clamp_rule` calls, in the same order, as H-B7-9's original function.
- "Floor/ceiling sanity checks could themselves be trivially satisfied without proving the detector
  works" → **Checked, dismissed**: floor test's collision group spans ALL 40 k-values per branch
  (correctly grouping by the single constant marker), and ceiling's zero-collision result is
  logically forced (identical projection under the full state implies identical state) — both are
  hand-traceable from the printed `metrics/run.json`, not just asserted.

## Honesty note (caught while writing this, not before)

H-B7-12's own decision.md already established that branch_1 and branch_2 are DYNAMICALLY
EQUIVALENT for this exact intervention (FGFR3_stimulus=1, fixed identically in both branches,
gates EGFR to 0 regardless of EGFR_stimulus — the one differing input bit never propagates). The
collision found here reproduces byte-identically across both branches at the same k-values, which
is consistent with — not independent confirmation of, just not contradicting — that known
equivalence. This experiment's domain is therefore effectively ~40 independent release-states
(one branch's worth, duplicated), not 80 independently-informative ones. Does not change the
verdict (the collision is exact regardless of how many independent branches contributed it), but
the "domain_size: 80" figure in metrics/run.json should not be read as 80 independent data points.

## Scope note

First cheap test of the user's own proposed B7 observability direction (2026-09-10, direct
follow-up after B2 and B3 both closed negative): "достаточен ли текущий набор наблюдаемых маркеров,
чтобы однозначно решить, можно ли снять intervention без риска возврата в нежелательный attractor?"
Per the user's own staged plan, this test answers ONLY the binary "sufficient or not" question for
the two most natural candidate marker sets — it does NOT yet search for a minimal augmentation
(named as the Revival Condition's next step, not attempted here, consistent with Minimal Relaxation
Rule discipline: one assumption changed per future variant, not bundled into this experiment).
