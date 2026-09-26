# r = 6 F_p certificate (d = 54, s = 16), pre-registered 2026-09-26, COMMITTED BEFORE the run

Question type (EstimandOps L0): descriptive / existence (a mathematical object with a stated property); no causal layer. Tier: Standard, an extension of the r = 2..5 family
(claim.md there). Nothing here changes the frozen r = 2 claim, the sent email, or any status.

## Why this and only this
The r = 2..5 firing rows and controls were certified at F_p, and r = 3, 4, 5 were reproduced by an independent implementation. r = 6 is the next unfilled cell of the same table
(closed_form_check.json: d*(6) = 54, k* = 48, s = 16). It only widens the family; it is not new information about novelty. An independent-code check at d = 54 is deliberately NOT part of
this claim: the largest exact run at d = 41 took 801 s, so d = 54 would be about an hour per run.

## Registered predictions (from the closed form r^2 + max(s, 2kr - s r^2) + 1, exact for k >= r in closed_form_check; LB from decision.md C-LB)
`fp_certify.py 54 6 16` and `fp_certify.py 54 6 15`, unchanged code, primes 67108837 and 67108777, seeds 20260919 and 20260920:

| d | r | k | s | kind | predicted dim V-perp | LB | fires (< d)? |
|---|---|---|---|---|---|---|---|
| 54 | 6 | 48 | 16 | fire | **53** | 53 | YES |
| 54 | 6 | 48 | 15 | below | 73 | 73 | no |

- Both primes must give the same integers; all flags true (Lyapunov, PCC on full commutators, det QFIM != 0, kernel dims equal the float generic ones).
- Stage solution-space dims (from the counting formula 2kr - r^2 (j - 1) = 576 - 36 (j - 1)): 540, 504, ..., 72, 36 at j = 2..16 for s = 16.
- An above-crossing config (s = 17) is NOT registered: as recorded in claim.md there (both addenda), its result is forced by a kernel-dimension count (last kernel dimension < s), so it is bookkeeping, not a test.

## Kill criteria (fixed now)
1. Fire row with any flag false on either prime => r = 6 NOT certified.
2. Any result with dim V-perp < LB => C-LB falsified or the code is wrong: STOP and debug before anything else.
3. Any integer mismatch with the prediction => the closed form is not general at r = 6; record it, do not refit silently.
4. Below row that fires => the closed form is wrong from the other side.
5. A run that does not finish within its per-config timeout (900 s per config in the earlier batch; here 3600 s): INCONCLUSIVE, no claim about r = 6.

## What this does NOT show
Same lab, same code as r = 2..5 (breadth, not independence); existence only (lifting lemma unreviewed, no explicit Q(i) instance); nothing about novelty (U2 open) or external reproduction (U3 open).
