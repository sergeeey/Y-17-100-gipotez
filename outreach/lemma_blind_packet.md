# Review packet (v2): a lifting argument (self-contained; no background needed)

v2 differs from v1 only by editorial fixes prompted by one blind pass on v1: an explicit hypothesis (H0), 'over Q' replaced by 'at points with m_j != 0', 'products of powers', 'integral domain', and a note on how Re is taken. No mathematics changed.

Task for the reviewer: decide whether the argument below is valid. List every step that does not follow from the stated
hypotheses, or confirm that you could reproduce each step yourself. If you find a gap, say exactly where and why.
Do not assume the conclusion is true or false. Please report which steps you checked line by line and which you only skimmed.

## Setting

Integers d = 22, r = 2, k = d - r = 20, s = 16. Unknowns: for each j = 1..s a complex k x r matrix B_j = X_j + i Y_j, where X_j, Y_j are
integer k x r matrices; the 2kr = 80 integer entries of (X_j, Y_j) are the *coordinates* of B_j. Write `t` for the vector of all coordinates.

**Constraints (the tower).** B_1 is unconstrained. For j >= 2 the coordinates of B_j must satisfy, for every i < j, the requirement
"the r x r matrix B_i^† B_j is Hermitian". Writing N = B_i^† B_j, this is: Re(N) - Re(N)^T = 0 (r(r-1)/2 = 1 real equation) and
Im(N) + Im(N)^T = 0 (r(r+1)/2 = 3 real equations). So for fixed B_1..B_{j-1} the coordinates of B_j solve a homogeneous linear system
`C_j x = 0`, where `C_j` is a `4(j-1) x 80` matrix whose entries are integer-linear in the coordinates of B_1..B_{j-1}.

**Two further polynomial quantities.** Let q = (q_1, q_2) be fixed positive integers. Let `Q(t)` be the s x s real matrix
`Q_{ij} = Re sum_{a=1..2} q_a (A_i^† A_j)_{aa}` with `A_i = -2i B_i`, and let `S(t)` be the 544 x 484 complex matrix whose rows are
the vectorisations of a fixed finite list of matrices of the form `i (L_i sigma L_j - L_j sigma L_i)` and `i [sigma, L_i]`,
where `L_i` is the 22 x 22 matrix `[[0, A_i^†],[A_i, 0]]` and `sigma` runs over a fixed finite list of 2 x 2-block constant matrices.
Only the following is needed about them: **every entry of `Q` and of `S` is a polynomial in the coordinates `t` (real and imaginary
parts as separate variables) with coefficients in Z[i].**

## Hypotheses (data from a computation over the finite field F_p, p prime, p = 1 mod 4, sqrt(-1) a fixed root of -1 mod p)

Reduce Z[i] -> F_p by i -> sqrt(-1). Note: `Re` in the definition of Q is taken on the real/imaginary *coordinates* (a polynomial with integer coefficients in the coordinates), never as a 'real part mod p'. Suppose there is a point `t0` in F_p^N (values of all coordinates), built stage by stage with each
B_j drawn from the kernel of C_j mod p, such that:

- (H0) each B_j(t0) lies in the kernel of C_j(t0) mod p (the point is built stage by stage from kernels, so all constraints hold mod p);
- (H1) for every j = 2..16, `C_j(t0)` has full row rank `4(j-1)` over F_p (equivalently its kernel mod p has dimension 80 - 4(j-1));
- (H2) `det Q(t0) != 0` in F_p;
- (H3) `S(t0)` has rank 463 over F_p, so some 463 x 463 minor `Delta(t0)` is nonzero.

## Claim to be examined

Under (H0)-(H3), there exist Gaussian-rational blocks B_1..B_16 (coordinates in Q) satisfying all the constraints exactly, with
`det Q != 0` and `rank S >= 463` over Q(i).

## Argument as given

1. By (H1), for each j there is a `4(j-1) x 4(j-1)` column submatrix M_j of C_j with nonzero determinant mod p. Its determinant m_j is a polynomial with integer coefficients in the entries of C_j, hence a rational function of the free coordinates once earlier blocks are parametrised (see 3); it is nonzero mod p at t0, so it is not the zero rational function.
2. Take the columns outside M_j as free coordinates of B_j. Where m_j != 0 the remaining (pivot) coordinates are rational functions of the free ones (Cramer's rule) with denominator m_j. At any point with m_j != 0 (equivalently over the function field Q(u)), rank C_j >= 4(j-1) because M_j is invertible there, and rank C_j <= 4(j-1) because there are only that many rows; so the kernel there has dimension 80 - 4(j-1), and the same parametrisation describes it.
3. Inductively every B_j is a rational function with integer coefficients of the free coordinates u of B_1..B_j, with denominators products of powers of the m_l (l <= j). Let `T = det Q * Delta`. Clearing denominators gives a numerator N(u) in Z[i][u].
4. At the F_p point corresponding to t0, every m_l, det Q and Delta are nonzero after reduction. A polynomial whose reduction (a ring homomorphism Z[i] -> F_p) is nonzero at a point is a nonzero polynomial. Hence N != 0 and the numerator of every m_l is nonzero, as polynomials.
5. A nonzero polynomial over Z (an infinite integral domain) does not vanish identically on Z^n, so it has an integer point where it does not vanish. So there is an integer u with N(u) != 0 and all m_l(u) != 0. The resulting B_j are Gaussian rational, satisfy all constraints (they lie in the kernels), and have det Q != 0 and Delta != 0.
6. Hence rank S >= 463 over Q(i).

## What the reviewer should decide

(a) Does each numbered step follow from the hypotheses and the setting, as stated?
(b) Is anything used that is not listed among the hypotheses (for example a claim about which pivot columns the finite-field computation used)?
(c) Is the final claim exactly what steps 1-6 prove, or something weaker or stronger?

Please answer per step: OK / GAP (with the reason) / CANNOT-TELL.
