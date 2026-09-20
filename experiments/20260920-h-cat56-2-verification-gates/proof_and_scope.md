# H-CAT56-2: proof of the non-saturation test, and the scope of the claim (gates 3 and 8)

Date 2026-09-20. Evidence markers: `[PROOF]` derived here on paper, `[DOCS]` taken from arXiv:2601.21801
(Yang, Imai, Pezze) as fetched on 2026-09-20 and NOT re-derived, `[VERIFIED]` recomputed by code.

## 1. What is claimed

Setting: a finite-dimensional state family rho(theta), theta in R^s, rank r < d, Pi_r d_i rho Pi_r = 0
(generic quasi-pure, Yang Eq. 12), nonsingular QFIM, partial commutativity Pi_r [L_i, L_j] Pi_r = 0.
`dim V^perp < d  =>  no single-copy measurement has F^C = F^Q`  (Observation 2).

## 2. Proof, split by what is and is not re-derived

Let {E_w} be a POVM with F^C = F^Q. Refining every element into rank-one pieces cannot lower F^C
(coarse-graining only loses information, F^C <= F^Q always), so assume all E_w = |u_w><u_w|.

**(a) Regular outcomes** (<u_w|rho|u_w> > 0). `[PROOF]`, this is the re-derivation recorded in
`20260919-pcc-generic-quasipure-cat56-2/decision.md`: equality in the Cauchy-Schwarz step that gives
F^C <= F^Q holds iff (L_i - c_i)|u_w> lies in ker rho with real c_i. This forces
<u_w| iM_{i,ab} |u_w> = 0 and <u_w| iW_{ij,ab} |u_w> = 0, i.e. |u_w><u_w| is orthogonal to V.

**(b) Null outcomes** (<u_w|rho|u_w> = 0, u_w in ker rho). These are needed to complete the identity; how F^C_w is defined for them (limit convention) comes from Ref. [29], not read here. **Now checked against the PDF (arXiv:2601.21801v1, read pages 2, 6-9, incl.
Supplemental S1) rather than a summary.** `[DOCS, read]`:
- Main text, Eq. (3): for null operators, equality F^C_w = F^Q_w holds iff `<psi_a|L_i|pi_w> = eta_{w,ij} <psi_a|L_j|pi_w>`
  with real eta independent of a. The necessary-and-sufficient conditions (2),(3) are attributed to Ref. [29]
  (Yang, Pang, Zhou, Jordan, PRA 100, 032104), which also fixes the convention for F^C_w of a null outcome; I did not read [29].
- Supplemental S1.A: for null operators Eq. (3) is equivalent to `<pi_w|W_{ij,ab}|pi_w> = 0` for all i, j, a, b (their S1-S2).
- Supplemental S1.B: the M-condition `<pi_w|M_{i,ab}|pi_w> = 0` is "automatic" when E_w is null. I re-derived this in one
  line: M_{i,ab} = L_i|psi_a><psi_b| - |psi_a><psi_b|L_i and <psi_b|pi_w> = 0 for pi_w in ker rho, so both terms vanish.
- Conclusion in the source: for an operator of any type, null or regular, saturation is equivalent to (4) and (5), i.e.
  |pi_w><pi_w| is orthogonal to V. So null outcomes are in V^perp as well.

Remaining dependence: the "iff" between saturation and Eq. (3) for null outcomes comes from Ref. [29] (a published paper), not
from anything derived here. That is a much smaller dependence than "Supplemental not read".


**(c) Counting.** Given (a)+(b), every outcome projector lies in V^perp. sum_w |u_w><u_w| = I forces the
vectors u_w to span C^d, so some d of them, b_1..b_d, form a basis. `[PROOF]` The projectors
|b_i><b_i| are linearly independent in Herm(d): if sum c_i |b_i><b_i| = 0, apply <b~_j| . |b~_j> with
the dual basis (<b~_j|b_i> = delta_ij) to get c_j = 0. Hence dim V^perp >= d. No "reduction to a linearly
independent POVM" is needed (the external audit inserted one; it is harmless but unnecessary, and the
number of POVM elements may exceed d).

## 3. Scope of the result (gate 8)

Refuted: "PCC is sufficient for **single-copy, matrix** saturation F^C = F^Q of the QCRB for generic
quasi-pure states". Not addressed by anything here: scalar bounds with singular weights,
collective measurements on N copies or asymptotics, the Holevo bound, the Eq. (16) ancilla subclass
(sufficiency already proven there), any pure-state limit.

Correction 2026-09-20 (later): for every POSITIVE-DEFINITE weight W the scalar bound Tr[W F^-1] is saturated iff the matrix bound is. `[PROOF]`: F^C <= F^Q gives (F^C)^-1 >= (F^Q)^-1 (if F^C is singular the scalar cost is infinite, no saturation); Tr[W((F^C)^-1 - (F^Q)^-1)] = 0 with W > 0 and a PSD difference forces the difference to be 0, i.e. F^C = F^Q. So single-copy non-saturation of the matrix bound implies non-saturation of the scalar bound for every full-rank weight. It does NOT cover singular weights (for example estimating one parameter of the s), where saturation can still occur.

## 4. Two corrections to the previous report

1. **Upper bound is not needed for the theorem.** The counterexample needs dim V >= d^2 - d + 1 = 463,
   a LOWER bound on rank. for a Q(i) instance reducing to the F_p data, rank over F_p <= rank over Q(i), so rank_p = 463 gives dim V-perp <= 21 < 22
   (existence of such an instance is exactly the lifting lemma, item 2).
   The upper bound rank <= 463 (from dim V^perp >= 21) is only needed to say "exactly 463".
2. **Exactness gap that remains real:** the F_p certificate (`fp_certify.py`) plus a lifting argument
   is not an explicit Q(i) point. See `decision.md` in this folder for gate 1.
