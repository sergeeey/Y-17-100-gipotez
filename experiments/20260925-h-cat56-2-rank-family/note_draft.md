# DRAFT, LOCAL ONLY. Not for release, not for sending.

Status header (read this first): the exact d = 22 instance and its checks are frozen (`20260920-small-exact-qi-instance`, PACKAGE_FREEZE_2026-09-22).
**Novelty (U2) is open**: the author email was sent 2026-09-23 and no reply exists, and the 24 h Submission Gate cooling-off was not observed.
**Independent human reproduction (U3) is open.** Nothing below has passed the Submission Gate (integrity.md); this file is a working structure,
so every claim carries its evidence marker and its source.

Working title (novelty unresolved, no priority claim): *A partially commuting, non-saturable generic quasi-pure example in d = 22, and where the dimension test can first fire.*

## 1. Question and what is already known
- Setting: a state family rho(theta), theta in R^s, rank r < d, generic quasi-pure (Pi_r d_i rho Pi_r = 0, Yang arXiv:2405.00405 Eq. 12), nonsingular
  QFIM, single-copy measurements. PCC: Pi_r [L_i, L_j] Pi_r = 0. PCC is necessary for saturation (Yang, Pang, Zhou, Jordan, PRA 100, 032104 = Ref. [13] of Nurdin).
- Yang, Imai, Pezze (arXiv:2601.21801): "for generic quasi-pure states, whether PCC is sufficient or not is still open, as conjectured in Ref. [38]"
  `[DOCS, read]`. Their Observation 2: `dim V-perp < d` implies the QCRB cannot be saturated. They give no explicit example in this class `[DOCS, read]`.
- Nurdin (arXiv:2402.11567 v5, read pp. 5-13): necessary-and-sufficient conditions (Condition 1 and corrected Condition 2'); all of its examples are
  saturable cases; it states PCC as necessary and does not claim it sufficient. The earlier lab audit line "Nurdin says PCC is not sufficient" was wrong and is withdrawn (novelty_audit.md addendum). `[DOCS, read]`

## 2. Construction
rho_0 = diag(q, 0), q = (1, 2, ..., r) (unnormalised representative, invariant under rho -> rho / Tr rho); SLD blocks
L_i = [[0, A_i^dag],[A_i, 0]], A_i = -2i B_i, B_i in C^{k x r}, k = d - r; state family rho(theta) = exp(-i sum theta_i G_i) rho_0 exp(+i sum theta_i G_i),
G_i = [[0, B_i^dag],[B_i, 0]]. Then PCC is equivalent to "B_i^dag B_j Hermitian for all i, j", the QFIM is
F_ij = Re sum_a q_a (A_i^dag A_j)_aa, and `V^perp = Herm(r) + P + Q` with `P = {Y : A_i^dag Y Hermitian}`, `Q = {Z in Herm(k) : A_i^dag Z A_j Hermitian, i != j}`
(decision.md C-ID, exact; verified on 234/234 robust samples). Blocks are built as a sequential tower: each B_j lies in the integer-linear kernel of the
Hermiticity constraints against B_1..B_{j-1}.

## 3. The test (re-derived, not only cited)
If some single-copy POVM has F^C = F^Q, refine it to rank-one elements (this cannot lower F^C), so every outcome projector lies in `V^perp`
(regular outcomes: derived; null outcomes: Supplemental S1.A/B of 2601.21801 and the convention of Ref. [29], read on the PDF but Ref. [29] not read).
The outcome vectors span C^d, so `d` of them are linearly independent, and their projectors are real-linearly independent, hence `dim V^perp >= d`.
Contrapositive: `dim V^perp < d` forbids saturation. For every positive-definite weight W the scalar bound is saturated iff the matrix bound is
(proof_and_scope.md, Section 3), so the conclusion covers scalar bounds with full-rank weights. It does NOT cover singular weights, N-copy or collective measurements, or the Holevo bound.

## 4. Result 1: an explicit exact instance (d = 22, r = 2, s = 16)
Seed 701082 (`instance_d22_r2_s16.jsonl`), Gaussian-integer blocks, max |entry| = 78. Two unrelated exact implementations (F_p rank at two primes with
the full 22 x 22 definitions; own integer-arithmetic rank over Q(i) with FLINT) agree: PCC holds exactly on the full commutators, det QFIM != 0 exactly,
`dim V = 463`, `dim V^perp = 484 - 463 = 21 < 22`. `[VERIFIED]` by both, same laboratory. The lower bound `dim V >= 463` is all the non-saturation theorem needs.

## 5. Result 2: the same mechanism at ranks 2-5 (existence, not explicit)
F_p-lifting certificate (`fp_certify.py`, primes 67108837 and 67108777), predictions registered before the r = 4, 5 runs (claim.md):

| d | r | k | s | dim V^perp (F_p, both primes) | < d |
|---|---|---|---|---|---|
| 22 | 2 | 20 | 16 | 21 | yes |
| 23 | 3 | 20 | 12 | 22 | yes |
| 31 | 4 | 27 | 13 | 30 | yes |
| 41 | 5 | 36 | 14 | 40 | yes |

`[VERIFIED]` at F_p; for r = 3 and r = 4 additionally reproduced by a blind from-scratch implementation (`independent_r3/REPORT.md`: dim V-perp 22 on two other primes and in float, blind d = 8 control matched; `independent_r4/REPORT.md`: 30 on four exact runs and in float, same unchanged library; same definitions, different model instance). These become Q(i) instances only through the lifting lemma (`lifting_lemma.md`), which is my derivation, not machine-checked and not
reviewed by anyone else; treat Result 2 as `[INFERRED]` until it is.

## 6. Where the dimension test can first fire (computed, not proven for all k)
`LB(k,r,s) = r^2 + max(s, 2kr - s r^2) + max(1, k^2 - C(s,2) r^2)` is a rigorous lower bound on `dim V^perp` (decision.md C-LB, rank-nullity).
Exhaustive integer scan, r = 2..12, k = 1..220 (`closed_form_check.py`): the smallest d with `min_s LB < d` is d*(r) = 22, 23, 31, 41, 54, 69, 85, 104, 125, 148, 173;
the test then fires for every larger d in the scan (k up to 220); and `min_s LB = r^2 + ceil(2kr/(r^2+1)) + 1` exactly for every k >= r (mismatches only for k < r).
So for r = 2 no quasi-pure PCC state with d <= 21 can have `dim V^perp < d`: **within this test** d = 22 is minimal. `[VERIFIED-computation]`, not a proof for all k,
and NOT a statement that no counterexample exists in smaller d by other means.

### Controls (registered in claim.md; amended once, see the addendum there)
Below the crossing, `s < s*`, the closed form `dim V^perp = r^2 + (2kr - s r^2) + 1` was hit exactly, both primes: (d,r,s) = (31,4,12) -> 41, (41,5,13) -> 61, (23,3,11) -> 31 (none fires).
Above the crossing there is no admissible state in this construction: for `s = s* + 1` the QFIM is singular on both primes and the F_p value equals the value at `s*`
((31,4,14), (41,5,15), (23,3,13) -> 30, 40, 22). That was a pre-registration error of mine (I had registered these as ordinary controls); it surfaced on (31,4,14),
the amendment was written before the other two were read, and both matched it. Reading `[INFERRED]`: in the tower, every block B_i lies in the kernel K_s of the Hermiticity constraints against B_1..B_{s-1}, and a nonsingular QFIM (a positive-weighted Gram matrix of the blocks) needs dim K_s >= s; the last kernel dimension is exactly s - 1 in all three above-crossing configs (13, 14, 12), which is why `s*` is the largest non-degenerate `s` and why the match above is forced. The lower bound is tight at `s*`. This says nothing about non-sequential constructions. `[VERIFIED]` at F_p: of the 10 registered configs, the 4 firing and 3 below-crossing rows (7 of 10) held exactly; the 3 above-crossing rows failed as registered (see claim.md, both addenda, and decision.md, reviewer pass item 2: the amended match was forced, not an independent test). Output in `check_predictions_output.txt`.

## 7. What is not claimed
No general solution of optimal single-copy measurements; no priority claim (U2 open); no minimality over all constructions; no practical sensing advantage;
no statement outside single-copy, matrix-bound, positive-definite-weight saturation; Result 2 is not an explicit instance.
