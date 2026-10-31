# O1 report: independent check of the H-CAT56-2 phase-3 reduction (PHASE3_PROOF.md, Sections 1-4)

Reviewer derived everything from the source file. No project file was edited. Numeric script: scratchpad/o1_check.py.
Convention throughout: D1/P-reg (outcomes with p=0 contribute 0). Model assumption: Q = diag(1/3,2/3) is invertible (used repeatedly).

## (a) Lemma 1 and Lemma 2 (PHASE3_PROOF.md lines 33-55)

**Lemma 1, rank-one identity: PROVED-by-you.**
- Checked: with pi=(x;y), rho^{1/2}=diag(sqrt Q,0), L_c pi=(A_c^† y; A_c x), so a=(sqrt Q x;0), b=(sqrt Q A_c^† y;0). Then p=w|a|^2, a_c=w Re<a,b> (Tr(rho L m)=<rho^{1/2}pi, rho^{1/2}L pi>), q_c=w|b|^2. Therefore G=w(|b|^2-(Re<a,b>)^2/|a|^2). This is what line 39 says.
- Equality: the chain (Re<a,b>)^2 <= |<a,b>|^2 <= |a|^2|b|^2 is tight iff Im<a,b>=0 and b=t a. Then <a,b>=t|a|^2 is real, so t is real. Since sqrt Q is invertible, A_c^† y = t_c x with t_c real. t_c is linear in c (x≠0), so taking c=e_i gives A_i^† y=lambda_i x with lambda_i real, and the converse holds. This matches line 41.
- Null case x=0: G=w|sqrt Q A_c^† y|^2, zero for all c iff A_i^† y=0 for all i (Q invertible). Correct.
- Note: the task wrote G=q p - a^2. The file writes q - a^2/p. These are equivalent when p>0 (a factor p).

**Lemma 1 for a general PSD m (the form asked in the task): PROVED-by-you, equality condition sharper than the file's.**
- Hilbert-Schmidt Cauchy-Schwarz with B=m^{1/2}L rho^{1/2}, C=m^{1/2}rho^{1/2} gives a^2 <= |<C,B>|^2 <= |B|^2|C|^2=q p, so G>=0 for every PSD m.
- Equality holds iff m^{1/2}(L_c - t_c) rho^{1/2}=0 with ONE real t_c shared by all eigen-pieces of m. The file only claims the per-piece condition (each piece with its own lambda_ik). That is weaker, and sufficient for necessity (Theorem A). It is not an error.

**Lemma 2 (refinement): PROVED-by-you.**
- p, a_c, q_c are linear in m. Pieces with p_k=0 have a_k=0. Sedrakyan/Titu, (sum a_k)^2/sum p_k <= sum a_k^2/p_k, gives G(m) >= sum G(piece_k) >= 0.
- Corollary: G(m)=0 implies every piece has G=0, so every piece is admissible or pure.

**Numeric check (numbers, not proof).**

| Check | Random instance (20x2, 12 indices) | File instance, S={4..15} |
|---|---|---|
| Normalized G/(q p) >= 0 on 20000 random PSD m (rank 1..22, some with the x-block scaled by 1e-3), random c | min = +0.0067 | min = +0.0088 |
| Null space of the real-linear system (y,lambda), dimension (generic 40-3*12=4) | 4 | 4 |
| Rank-one piece (x;y) with y in Y_S(x) from that null space, max over 200 random c of abs(G)/(q p) | 1.4e-12 | 3.0e-9 (consistent with the SVD null space on integer data) |
| Same piece with lambda made imaginary, pi=(x; i y) | G/(q p)=1.0, strictly positive | 1.0 |
| Non-pure null piece (x=0, y random): q_c | 2.6e3 > 0 | 5.8e4 > 0 |
| Sum of two admissible pieces with different x (each G=0): G(sum)/(q p) | up to 0.99999 | 0.99997 |
| Lemma 2 inequality G(m)/p >= sum of piece terms, 200 c | held on all | held on all |

- The sum-of-two-pieces row confirms that "each piece admissible" is necessary, not sufficient, for G(m)=0. This is the sharper condition above and is harmless for Theorem A.

## (b) Theorem A (lines 59-71), step by step

- **(i) Radon-Nikodym: PROVED-by-you.** nu=Tr M dominates every matrix entry (|M_jk(E)| <= nu(E)), nu(Omega)=22, m is PSD a.e., and the integral of m dnu is I. The identity Tr(d_i rho m)=Re Tr(rho L_i m) holds because Tr(rho m L)=conj(Tr(rho L m)). On {p=0}: Tr(rho m)=0 gives m rho=0, so Tr(rho L m)=Tr(L m rho)=0 and the score is 0.
- The SLD kernel block L_22 never enters rho^{1/2}L pi, so the setup is well-defined. This is a remark, not a gap.
- **(ii) Deficit identity: PROVED-by-you.** c^T F^Q c = Tr(rho L_c^2)=Tr(rho L_c (integral of m dnu) L_c)=integral of q_c dnu, and c^T F^C c = integral over {p>0} of a_c^2/p dnu (a_c linear in c). Hence c^T(F^Q-F^C)c = integral of G_c dnu, finite because a_c^2/p <= q_c.
- **(iii) Pointwise vanishing: PROVED-by-you.** G_c>=0 pointwise (Lemma 1/2), so integral zero gives G_c(m(omega))=0 a.e. for each c. For fixed m, G_c is a quadratic form in c for both p>0 and p=0, hence continuous. A countable dense set of c gives one null set N, and G_c=0 for all c off N.
- **(iv) Pieces: PROVED-by-you.** For omega not in N, apply the Corollary to the spectral decomposition. Each piece with w_k>0 is admissible (x_k≠0, y_k in Y_S(x_k)) or pure (x_k=0, y_k in C_S). C_S is contained in Y_S(x) for every x (lambda=0), so every y_k lies in the union script-Y_S. The lower-right block of m is K=sum w_k y_k y_k^†, which lies in the finitely generated cone. No measurable selection is needed, since only K(omega) is used.
- **(v) Integration: PROVED-by-you.** The lower-right block of the integral of m dnu is I_20. This step alone does not put I_20 in the cone; it needs (vi) and (vii) together. The file combines them correctly at line 71.
- **(vi) Closedness: PROVED-by-you.** The condition A_i^† y in R x with |x|=1 is P_{x-perp}(A_i^† y)=0 in R^4. That is bilinear and polynomial in (x,y), so Z in S^3 x S^39 is closed and compact. Its projection to y is compact. Real rescaling of x does not change Y_S(x), so the unit-x parametrization covers all x≠0. Every generator yy^† with |y|=1 has trace 1, so the convex hull is compact in {tr=1} and misses 0, and the cone over it is closed (take t_n X_n -> Z; tr Z=lim t_n bounds t_n). The cone is also convex (finite non-negative sums). The "audit note" at line 70 is right.
- **(vii) Separation: PROVED-by-you** (see (c)).
- **Hidden hypotheses to state, none breaking the argument:**
  - Theorem A holds only under the D1 convention. Under a limit convention, null outcomes contribute a nonzero (4r-type) term and Lemma 1 fails. The file says so (lines 24, 97; ledger H3).
  - The model (rho, L_i) is taken formally. Whether it comes from a positive smooth family rho_theta is not checked here and is not needed for the formulas used.
  - Q invertible is essential in the equality characterization.
- **Remark on finite POVMs (line 73): PROVED.** It is the special case.

## (c) Separation

- **PROVED-by-you.** The cone is closed and convex in the real space of Hermitian 20x20 matrices with inner product tr(RX), and I_20 is not in it. Strict separation gives R and alpha with tr(R I) > alpha >= tr(R X) for all X in the cone. Since 0 is in the cone, alpha>=0. Since the cone is scale-invariant, tr(RX)<=0 on the cone, otherwise scaling violates the bound. So tr(R I_20)>0 and tr(RX)<=0 on the cone. This is the statement at line 71.

## Overall verdict: VALID (no logical gap found in Theorem A under the stated convention)

Gaps and caveats (none invalidating):
1. The result is conditional on the D1 convention for p=0 outcomes (stated in the file; the limit convention is not covered).
2. Lemma 1's equality condition for general PSD m is sharper than the file's (common t_c across pieces). The file only needs the necessary direction, so no effect on Theorem A.
3. I did not verify that (rho, L_i) arises from a genuine smooth positive family. Not needed for the formulas.
4. Nothing was checked here on Theorem B (sufficiency), the S+ and S- certificates, or the literature claims; those were outside the request.
5. Numerics are sanity checks only: 20000 random PSD matrices and 200 random c per case, on one random instance and the file instance (S={4..15}).
