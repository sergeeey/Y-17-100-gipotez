# Lifting lemma for the H-CAT56-2 counterexample (for an independent checker)

Status: my derivation, same author as the code, not machine-checked, not reviewed by anyone else.
The checker's job is to find a false step, not to confirm the conclusion.

## Statement

Let d = 22, r = 2, k = d - r = 20, s = 16. Let `X = (Re B_1, Im B_1, ..., Re B_s, Im B_s)` be the integer coordinates of s complex
k x r blocks (n = 2kr = 80 real coordinates per block). Define the PCC tower: B_1 arbitrary, and for j >= 2 the
block B_j must satisfy the integer-linear system `C_j(B_1..B_{j-1}) x_j = 0`, where the rows say "B_i^dag B_j is Hermitian" for every i < j
(r^2 = 4 real rows per earlier block, so `C_j` is a `4(j-1) x 80` integer matrix whose entries are linear in the earlier coordinates).

Claim. There exist Gaussian-rational blocks B_1..B_16 satisfying the tower exactly such that, for the state
rho = diag(q_1, q_2, 0, ..., 0) (q rational, positive; the F_p run uses q = (1, 2), trace 3, harmless because L and V are unchanged and the QFIM only rescales) with SLD blocks `A_i = -2i B_i`:
(i) the QFIM is nonsingular, and (ii) the real dimension of `V = span_R{iW, iM}` is at least 463.
Consequently `dim V_perp <= 484 - 463 = 21 < 22 = d`.

## Data the proof uses (from `fp_certify_d22_r2_s16.json`, two primes p = 67108837 and 67108777, both = 1 mod 4)

For the F_p run: (D1) at every stage j the kernel of `C_j` mod p has dimension `80 - 4(j-1)`, i.e. `C_j` has FULL ROW RANK mod p;
(D2) the QFIM determinant is nonzero mod p; (D3) the stack of iW, iM vectors (544 x 484 over F_p, `i -> sqrt(-1) mod p`)
has rank 463; PCC and the SLD equation hold exactly mod p.

## Proof

1. **Minors.** By (D1), for each j there is a `4(j-1) x 4(j-1)` column-submatrix M_j of `C_j` with nonzero determinant mod p.
   `m_j = det M_j` is a polynomial with integer coefficients in the entries of the earlier blocks (themselves rational functions of the free coordinates, handled in step 3); it is nonzero mod p at the F_p point, hence
   is not the zero polynomial.
2. **Parametrisation valid over Q.** Fix the pivot columns of M_j; treat the other `80 - 4(j-1)` coordinates of B_j as free.
   On `{m_j != 0}` the pivot coordinates are rational functions (Cramer) of the free ones with denominator m_j, and this gives exactly
   the kernel: the kernel of `C_j` over Q has dimension at most `80 - 4(j-1)` (rank >= 4(j-1) because M_j is invertible over Q)
   and at least that (rank <= number of rows). So the same parametrisation describes the kernel over Q and over F_p.
3. **Rational function of the free coordinates.** Inductively each B_j is a rational function, with integer coefficients, of the free
   coordinates t of B_1..B_j (denominators: products of the m_l). Let `Delta` be a 463 x 463 minor of the stack that is nonzero mod p
   at the F_p point (exists by D3), and `T = det(QFIM) * Delta`. Both are polynomials in the entries of the B_j and of q, and i enters
   only through `i^2 = -1`, so `T` is a rational function with numerator `N` in `Z[i][t]` after clearing denominators.
4. **Nonvanishing.** The F_p point is a point where all `m_j`, `det QFIM`, `Delta` are nonzero after reducing `Z[i] -> F_p`
   (`i -> sqrt(-1)`, a ring homomorphism). Reduction of a nonzero polynomial value being nonzero implies the polynomial is nonzero, so
   `N != 0` and all `m_j != 0` as polynomials over `Z[i]`.
5. **A Q(i)-point.** A nonzero polynomial over an infinite field has a nonvanishing integer point; so there is an integer t with
   `N(t) != 0` and all `m_j(t) != 0`. The resulting B_j are Gaussian rationals, satisfy PCC exactly (they lie in the kernels), and give a state
   with `det QFIM != 0` and a 463 x 463 minor `Delta != 0`.
6. **Conclusion.** The stack has rank >= 463 over Q(i), hence over C. For a set of Hermitian matrices the complex span has the same
   dimension as the real span, so `dim_R V >= 463`.

## Things a checker should attack

- Step 2: is full row rank of `C_j` at the F_p point really enough to fix the kernel dimension over Q? (Argument: `4(j-1)` rows, so rank <= rows
  always; M_j invertible mod p => invertible over Q => rank >= rows.)
- Step 3/4: pivot consistency. Checked by the reviewer: `fp_certify.py` builds the kernel basis with the identity on the free (non-pivot) columns and draws random free coordinates, so every F_p block lies in the same Cramer parametrisation the lemma uses (resolved, not open).
- The `Z[i] -> F_p` map: the integer real/imag coordinates are the unknowns; `i -> sqrt(-1)` is used only in evaluating `iW`, `iM`, QFIM.
- Whether the QFIM and V of the state defined from the SLD blocks `A_i` match the paper's definitions (checked numerically in
  `orchestrator_independent_check.py` and in the p2-stability gate, not proved here).
- That "rho = diag(q, 0)" with rational weights and derivatives `d_i rho = (rho L_i + L_i rho)/2` corresponds to a genuine state family
  (yes: `rho(theta) = exp(-i sum theta_i G_i) rho_0 exp(+i ...)` with `G_i = [[0, B_i^dag],[B_i, 0]]`, whose first derivative at 0 has that form).

## What this does NOT show

An explicit Q(i) instance (bit growth in `gate1_exact_qi_flint.py`: 221, 1241, 15541, 76707 bits at d = 8, 10, 12, 14) or a machine-checked proof.
It is an existence argument.
