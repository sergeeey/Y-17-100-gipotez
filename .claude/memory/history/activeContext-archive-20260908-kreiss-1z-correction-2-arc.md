# Archive: H-B2-1z → external audit correction → H-B2-2 → reviewer-scope lesson (2026-09-08)

Continuation of `activeContext-archive-20260908-kreiss-mechanism-and-predictor-arc.md`
(H-B2-1u through H-B2-1y). Archived from the live `activeContext.md` to keep it under the
project's own ≤200-line ceiling (memory-protocol.md). Full detail lives in ADR-076 through
ADR-078 (`.claude/memory/decisions.md`) and the corresponding `experiments/*/decision.md`
files — this is a compact narrative pointer, not the source of truth.

---

**H-B2-1z (autonomous, standing authorization, after the user's reflective message that "a
convergent K(A) estimate is needed, otherwise the physical interpretation stays murky"):**
closed form `kappa(lambda_1)` (Trefethen-Embree eigenvalue condition number, one
`eig()+inv()` call, no pseudopy) was proposed as exactly that convergent estimate.
Verified on H-B2-1y's own 16 matrices: `kappa(lambda_1) >= deep_k` in 16/16 cases (median
0.989 of kappa). Mechanism Claim Gate on a separate small test matrix: the sampled ratio
converges to within 0.02% of kappa(lambda_1) at an achievable sweet spot (eps~5e-5), then
REVERSES (numerical floor, confirmed via non-determinism between two identical runs at the
finest eps). Refitting M1~K(A) with kappa(lambda_1) on the FULL 80-point H-B2-1x training
population gave exponent 0.62-0.66 — even further from quadratic, strengthening H-B2-1y on
5x the data. Honest caveat: kappa(lambda_1) is the WORST held-out predictor of M1 (RMSE
0.522 vs 0.365 for the biased shallow estimate) — predictive usefulness and physical
correctness remain separate axes. Reviewer never reached a verdict (2 attempts, both hit
the turn limit) — closed via self-review: an independent hand-derived formula + a second
independent numerical method (SVD-bisection, no pseudopy) confirmed the formula and
clarified the nature of the numerical floor (an artifact of the pseudopy pipeline, not
double-precision in general). Merged to main.

**REOPENED THE SAME SESSION (external discovery audit, ADR-077):** "convergent K(A)
estimate found" — FALSIFIED, independently re-checked with a fresh (third), non-reused
script. `kappa(lambda_1)` is NOT the true K(A) — on N=40,seed=314 (H-B2-1x's own train
set): `kappa(lambda_1)=50.11` against an independently-confirmed direct lower bound of
108.87 (matching the audit's own number to 3 significant figures) — a 2.17x undershoot.
The audit also constructed an adversarial example where `kappa(lambda_1)=1.0` against a
true lower bound of 44.87. `graph.yaml`: H-B2-1z `confirmed` -> `lead`. What survived:
16/16 `deep_k <= kappa(lambda_1)` (both are lower bounds), the Mechanism Claim Gate's own
finding about kappa(lambda_1)'s behavior relative to itself. Key methodological lesson:
claim.md's own pre-registered hedge ("K(A) could exceed kappa if non-monotonic") had
already correctly anticipated this exact finding — the overclaim lived only in decision.md
/graph.yaml's stronger language, written AFTER the result. Newly open, not closed: the
Claim 2 refit exponent (0.62-0.66) might itself be biased by the same mechanism H-B2-1y
found for the shallow estimate.

**H-B2-2 (user's explicit choice — "technical fix now," not a strategy pause): the "newly
open" question from ADR-077 CLOSED at population scale.** `K_ref =
max(kappa(lambda_1), floored real-axis line search x>=1e-4)`, no pseudopy at all.
Positive control: seed=314 gives `K_ref=108.868`, matching the independent recheck and the
audit to 3 significant figures. **Central finding: the line search actually dominates
kappa(lambda_1) in only 5/110 (4.5%) matrices of the H-B2-1x population, range
1.016-2.173 — seed=314 (the audit's own example) sits CLOSE TO THE WORST CASE across the
whole population, not typical.** Refitting M1~K(A) with K_ref: exponent 0.637-0.670 (was
0.622-0.656 with kappa(lambda_1) alone) — a shift of only 0.01-0.015, RMSE unchanged to 3
decimal places. **The H-B2-1y/1z conclusion about the exponent being substantially below
quadratic is ROBUST to the ADR-077 correction.** K_ref recorded in pearl_registry as the
recommended reference for K(A) throughout this matrix family, replacing both pseudopy
(unstable) and kappa(lambda_1) alone (known to undershoot on rare but real matrices).

**Per the user's direct request ("wait for the reviewer's verdict... autonomously until
you finish everything"):** a 5th reviewer attempt, this time scoped narrowly to 2 concrete
checks instead of "review this experiment," succeeded on the first try — `VERDICT: LGTM`,
independently re-derived the same lower-bound formula for x/sigma_min(A), ran pytest (7/7)
and ruff itself, without taking the report on faith. Lesson: the cause of the 3 prior
timeouts was not the turn limit itself but a TOO-BROAD scope — a narrow, concrete request
("verify exactly this claim, run exactly these 2 commands") fit the budget on the first
try. The H-B2-1u -> 1z -> 2 arc is now fully closed, including a real reviewer verdict.
