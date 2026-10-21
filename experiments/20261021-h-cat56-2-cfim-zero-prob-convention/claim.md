# claim.md: zero-probability outcomes, CFIM conventions, and the geometry of saturating POVMs (H-CAT56-2)

## L0 gate (EstimandOps, mandatory first step)

Question type: **Descriptive**. The task asks for exact statements about specific finite-dimensional
quantum-estimation models (Nurdin Example 2, control points A0, A0+, D, N1) and about definitions
(classical Fisher information at zero-probability outcomes, Hellinger local information, QFIM). No causal or
predictive claim is made.

Falsification tier: **Full** (contradiction with a published corrigendum and with a preprint that carries
similar conditions; requires proofs or exact computations, reproducible numerics, and a context-blind review).

## Scope and notation

- Parameters theta in an open set of R^p; rho_theta smooth; POVM {E_k} fixed (independent of theta), finite.
- p_k(theta) = tr(rho_theta E_k). Regular outcome: p_k(theta_0) > 0. Null outcome: p_k(theta_0) = 0, equivalently
  E_k rho = 0 at theta_0 (range of E_k in ker rho).
- Three local quantities at theta_0 (names fixed here, so that no claim depends on an unstated convention):
  - F_pos_ab = sum over regular outcomes of (d_a p_k)(d_b p_k)/p_k. This is the CFIM at the point, with
    null outcomes excluded (equivalently 0/0 = 0).
  - F_lim (direction-wise limit): lim_{t->0} of the CFIM matrix evaluated at theta_0 + t h, with null outcomes
    included at their own probabilities. Depends a priori on the approach direction h.
  - H_quad (Hellinger local form): lim_{t->0} t^{-2} * sum_k (sqrt(p_k(theta_0 + t h)) - sqrt(p_k(theta_0)))^2,
    a quadratic form in h.
- F^Q_ab = Re tr(rho L_a L_b), with the minimal-norm SLD L_a in an eigenbasis of rho.
- N_E,ab = Re tr(E L_a rho L_b) for each outcome E. Null outcomes: N_E is the entire QFI contribution of E.

## Claims (pre-registered before the computations of this folder)

| id | claim | status | evidence |
| --- | --- | --- | --- |
| Z1 | For the specified POVM of Nurdin Example 2 (2405.01471 v1, p. 11) at theta_0 = (0.3, 0.6): F_pos = diag(4.7619, 0) and F^Q - F_pos = N, where N is the null-outcome term, rank one, equal to 0.525 [[1, 0.7],[0.7, 0.49]]. | pending | `example2_zero_probability_limits.py` |
| Z2 | Null-outcome probability along theta: p_null(theta) = 2 (1 - theta_1)' g^2 (1 - cos(c . (theta - theta_0))) exactly, with g^2 = D^2 (1 - D^2) and (1 - theta_1)' the current value of 1 - theta_1. | pending | `example2_limit_symbolic.py` |
| Z3 | For every direction h, lim_{t->0} F_lim(theta_0 + t h) = F_pos + N = F^Q (the null matrix is rank one, so the limit does not depend on h). | pending | `example2_zero_probability_limits.py` |
| Z4 | For Example 2, lim_{t->0} H_quad(h) = h^T F^Q h / 4 (Hellinger local metric equals the Bures metric). | pending | `example2_zero_probability_limits.py` |
| Z5 | General identity: for every null outcome E and interior theta_0, Hess_E = N_E / 2, where Hess_E is the Hessian of p_E at theta_0. | pending | `zero_prob_identities_random.py` |
| Z6 | General limit: for a null outcome E with h^T N_E h > 0, lim_{t->0} CFIM_E(theta_0 + t h) = (N_E h)(N_E h)^T / (h^T N_E h) (matrix, approach-direction dependent), and the quadratic form along h equals h^T N_E h. | pending | `zero_prob_identities_random.py` |
| Z7 | General Hellinger identity: lim_{t->0} H_quad(h) = h^T (F_pos + sum over null E of N_E) h / 4. | pending | `zero_prob_identities_random.py` |
| Z8 | The printed null conditions are rank-one conditions: E_00 B_l = c_lm E_00 B_m for all pairs (Nurdin Thm 1(2)) and (3) of arXiv:2601.21801 v1 hold if and only if N_E is rank one. Consequently they are the saturation conditions for the direction-wise limit notion, and not the saturation conditions for the point notion. | pending | derivation in memo; numerical check in `zero_prob_identities_random.py` |
| Z9 | Saturation classes: point notion (F_pos = F^Q) iff regular outcomes satisfy the element-wise criterion (Theorem A, real constants incl. 0) AND null outcomes satisfy E L_a rho = 0. Hellinger notion (H_quad = F^Q / 4) iff regular outcomes satisfy Theorem A only. Constant-matrix limit notion iff regular outcomes satisfy Theorem A and each null N_E is rank one. | pending | derivation in memo; checks in random tests |
| Z10 | Decisive resolution: the disagreement with Nurdin's Example 2 is definitional. The specified POVM is not saturating in the point notion, and it is saturating in the Hellinger and the constant-matrix-limit notions. Whether the disagreement "disappears" depends on which notion the source papers use; this must be read from their text (explorer reports). | pending | explorer reports; memo section 1 |
| G1 | Geometric characterization (point notion): a POVM saturates iff for every outcome k there is c^k in R^p with range(E_k) contained in W(c^k) = {v : P_+ (L_a - c^k_a) v = 0 for all a}. Holds for null and regular outcomes, general rank, general L_{++}. | pending | derivation (Theorem A); tests in `geometric_criterion_check.py` |
| G2 | Union U = union over c of W(c) equals the set of vectors v such that for each a the vectors P_+ L_a v and P_+ v are real-proportional (common real multiplier), together with the null vectors P_+ v = 0 and P_+ L_a v = 0 for all a. | pending | derivation; check in `geometric_criterion_check.py` |
| G3 | Projective saturation (point notion) iff there is an orthonormal basis inside U; Hellinger notion: an orthonormal basis such that every vector with P_+ v != 0 lies in U. Lemma 2 (block diagonality) is not needed for these statements. | pending | derivation; checks on D, A0, Example 2 rescue |
| P1 | Literal reading of Condition 2' (finite real constants for every ordered pair (l, m)): control point D violates it. | pending (memo section 5 says VERIFIED) | `point_D_projective_onb_check.py` (sibling folder) and memo |
| P2 | One-sided reading (for each pair, E B_l = c E B_m or E B_m = c' E B_l with real c, c'): control point D satisfies Condition 2' for its own saturating POVMs. Whether the corrected Condition 2' (corrigendum v5, Section 6) is literal or one-sided must be read from the text. | pending (explorer B report) | `condition2_prime_readings.py` |
| P3 | Hence Proposition 6 holds only for the literal reading. If the corrigendum's corrected Condition 2' allows zero constants, Proposition 6 is false, and the claimed contradiction is absent. | pending | memo section 5 after the text is read |

## Non-claims

- No claim about which notion is operationally correct for a particular estimation task; the memo states the
  operational meaning of each notion only where it is derived (for example the local Poisson structure of
  null outcomes).
- No claim that any published paper is wrong unless the claim is verified from its own text and definitions.
- No claim of scientific novelty without a priority check; the prior-art comparison is recorded as a separate
  result with its evidence.
- No contact with authors, no submission, no push, no publication, no modification of the original certificates
  or of earlier folders.

## Falsifiers (pre-registered)

- Z1 falsified if F_pos equals F^Q at theta_0 for the specified POVM of Example 2.
- Z3 falsified if the limit of F_lim along any direction differs from F^Q at theta_0 by more than 1e-6.
- Z5 falsified if the Hessian identity fails on any random null outcome (tolerance 1e-8 relative).
- Z6 falsified if the limit matrix differs from (N_E h)(N_E h)^T/(h^T N_E h) for a rank-two example.
- Z8 falsified if a null outcome with rank-one N_E violates the printed proportional condition, or the reverse.
- G1/G2 falsified if random tests produce a POVM whose element ranges violate the W(c) criterion while saturating
  numerically (point notion), or the reverse.
- P2 falsified if the corrected Condition 2' is literal and D violates it (then P2 is replaced by P1).

## Status after referee and reviewer rounds (appended 2026-10-21)

The pre-registered text above is unchanged. Amendments and reasons are in `decision.md` (A1–A8). Verdict: REJECT for the general forms of Z3 (directions with c·h = 0), Z5–Z7 and the limit/Hellinger clauses of Z9; PROMOTE for their amended forms (A1, A7).

| id | status |
|---|---|
| Z1, Z2 | CONFIRMED (Example 2) |
| Z3 | REFUTED as stated for c·h = 0 (A7); CONFIRMED for c·h ≠ 0 |
| Z4 | CONFIRMED for Example 2 (constant rank, A1) |
| Z5, Z6, Z7 | REFUTED as stated (rank jump); CONFIRMED with the rank hypothesis (A1, A2) |
| Z8 | CONFIRMED |
| Z9 | point clause CONFIRMED; limit and Hellinger clauses CONFIRMED with A1 |
| Z10 | CONFLICT (source-internal); POVM facts CONFIRMED for Example 2 |
| G1 | CONFIRMED for rank-one elements (regular and null, all classes counted; scope L7) |
| G2 | CONFIRMED for rank-one elements (members, non-members, zero branch; the ⇒ direction is by construction, L8; complex-multiplier non-members not tested, L9; the earlier check was vacuous) |
| G3 | PARTIAL |
| P1, P2 | CONFIRMED (P2 evidence file: `prop6_readings_check.py`, A8) |
| P3 | NOT SUPPORTED as written; OPEN until corrigendum v5 Section 6 is read |
