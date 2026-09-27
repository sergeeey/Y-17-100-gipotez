# Review packet (v3): a finite-field witness implies a Gaussian-rational point exists (self-contained; no background needed)

**Note on the title.** v1/v2 called this "a lifting argument". It is not: no specific point is carried from characteristic p to characteristic 0 (that would be Hensel lifting, which needs a nonsingularity/Jacobian hypothesis this argument does not use). What actually happens: the F_p point *certifies that a certain polynomial is not identically zero*; that fact, plus Q being infinite, then produces a (generally different) rational point. Renamed to avoid inviting readers to look for a Hensel-lifting-style gap that isn't the actual structure.

v3 differs from v2 in two places, both found by external review (untrusted source, independently re-derived below before accepting): step 3's denominator bookkeeping was imprecise, and step 5 had a real gap — "each polynomial individually has a nonvanishing point" does not imply "one common point where all of them are simultaneously nonzero". Both are fixed below with a standard product argument; no new hypothesis is needed and the conclusion is unchanged. v2's own fixes (an explicit hypothesis (H0), 'over Q' replaced by 'at points with m_j != 0', 'products of powers', 'integral domain', and a note on how Re is taken) are preserved unchanged from v1.

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

1. By (H1), for each j there is a `4(j-1) x 4(j-1)` column submatrix M_j of C_j with nonzero determinant mod p. Fix this choice of columns once (any valid choice works; the finite-field computation's own pivot choice is not needed — (H1) alone is enough to pick one). Its determinant m_j is a polynomial with integer coefficients in the entries of C_j; once earlier blocks are parametrised (see 3) it becomes a rational function of the free coordinates u.
2. Take the columns outside M_j as free coordinates of B_j. Where m_j != 0 the remaining (pivot) coordinates are rational functions of the free ones (Cramer's rule) with denominator m_j. At any point with m_j != 0 (equivalently over the function field Q(u)), rank C_j >= 4(j-1) because M_j is invertible there, and rank C_j <= 4(j-1) because there are only that many rows; so the kernel there has dimension 80 - 4(j-1), and the same parametrisation describes it.
3. Inductively, write every coordinate of every B_j as a fraction with numerator and denominator in Z[u] (u = the free coordinates of B_1..B_j), i.e. m_j(u) = a_j(u)/b_j(u) with a_j, b_j in Z[u] (a_j is the pivot determinant *as a polynomial*, after substituting the already-parametrised earlier blocks; it is a_j, not m_j itself, that is the object tracked from here on). Let `T = det Q * Delta`. Clearing denominators (multiplying through by the b_j's and by the a_j's that appear as denominators of later pivot coordinates) gives a numerator N(u) in Z[i][u].

   **Sub-lemma (why the F_p point t0 is reproduced).** Let u0 in F_p^n be the values of the free coordinates read off from t0. Since t0 satisfies (H0) and each M_j(t0) is invertible by (H1), the pivot coordinates of each B_j(t0) are the UNIQUE solution of C_j(t0)x=0 given the free ones — exactly what Cramer's rule computes. So substituting u0 into the rational parametrisation reproduces t0 exactly (mod p), and in particular a_j(u0) = det M_j(t0) != 0 for every j (by (H1)) and b_j(u0) != 0 (else the parametrisation would be undefined at u0, contradicting that it reproduces t0).
4. At u0, every a_j, b_j, det Q and Delta are nonzero after reduction mod p (the a_j/b_j case by the sub-lemma above; det Q and Delta by (H2)-(H3), since T(t(u0))=T(t0)). A polynomial whose reduction (the ring homomorphism Z[i] -> F_p, i -> sqrt(-1)) is nonzero at a point is a nonzero polynomial. Hence N != 0 and every a_j, b_j is nonzero, as polynomials in Z[u] resp. Z[i][u].
5. Nonvanishing of N and of each a_j, b_j SEPARATELY as polynomials is not yet enough — the construction needs one COMMON point where all of them are simultaneously nonzero. Fix this with a product: let `P(u) := N(u) * prod_j a_j(u) * prod_j b_j(u)` in Z[i][u]. Since Z[i][u] is an integral domain and every factor is nonzero (step 4), P != 0. Write P = A + iB with A, B in Z[u] (splitting each coefficient into its integer real and imaginary parts). P != 0 means A and B are not both the zero polynomial, so `A^2+B^2` is a nonzero polynomial in Z[u] (if A^2+B^2 were the zero polynomial, evaluating at any point would force A and B to vanish there, for every point, over an infinite field — so A=B=0 as polynomials, contradiction). Q is infinite, so a nonzero polynomial over Q does not vanish identically on Q^n: there is a rational point u* in Q^n with A(u*)^2+B(u*)^2 != 0, i.e. P(u*) = A(u*)+iB(u*) != 0 in Q(i). Since P is a product, EVERY factor is nonzero AT THIS SAME u*: N(u*) != 0 and every a_j(u*), b_j(u*) != 0 (a product over a field vanishes only if some factor does). The resulting B_j(u*) are therefore well-defined (every denominator nonzero), lie in Q(i) with coordinates in Q (u* is rational), satisfy all tower constraints (they solve the kernel equations by the rational parametrisation, which is an identity in u, not just at u0), and have det Q(u*) != 0, Delta(u*) != 0.
6. Hence rank S >= 463 over Q(i), at this explicit rational point u*.

## What the reviewer should decide

(a) Does each numbered step follow from the hypotheses and the setting, as stated?
(b) Is anything used that is not listed among the hypotheses (for example a claim about which pivot columns the finite-field computation used)?
(c) Is the final claim exactly what steps 1-6 prove, or something weaker or stronger?

Please answer per step: OK / GAP (with the reason) / CANNOT-TELL.
