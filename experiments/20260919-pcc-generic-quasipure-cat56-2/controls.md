# H-CAT56-2 — controls.md (numbers fixed before the verification/search runs)

## Configurations

Required set (r^2+1<d region marked): `(d,r,s)` with `s` = pilot value of the largest number
of parameters keeping QFIM full-rank (re-measured by the run, not assumed):

| d | r | k | s | r^2+1 < d ? |
|---|---|---|---|---|
| 6 | 2 | 4 | 4 | yes |
| 7 | 2 | 5 | 4 | yes |
| 8 | 2 | 6 | 5 | yes |
| 10 | 3 | 7 | 5 | **no** (10 = d): arithmetic control, cannot fire |
| 11 | 3 | 8 | 5 | yes |

`k = 1` is quarantined (QFIM-degenerate, H-CAT56-1). Extended set (pilot-informed,
registered here before verification): `(22,2,16)`, `(23,2,17)`, `(24,2,18)`, `(23,3,12)`,
`(24,3,13)`, plus sub-`s*` variants `(22,2,4)`, `(22,2,10)` as "no fire expected".

## Sample sizes / seeds

| run | N | base seed |
|---|---|---|
| random sequential-nullspace sampling, required configs | 200 each | 20260919 |
| random sampling, extended configs | 40 each | 20260920 |
| structured-start sampler (rank-deficient / real / sparse B_1), required configs | 100 each | 20260921 |
| adaptive surrogate optimisation, required configs (6,2),(7,2),(8,2) | 12 restarts each | 20260922 |
| adaptive, (10,3),(11,3) | 6 restarts each | 20260922 |
| Eq. (16) negative control | 20 each at d_sys r = 8, 12, 22 | 20260923 |
| data-swap replication | seeds 20260919+{0,1,2,3} for the main tables | |

Adaptive-search budget: SLSQP, `maxiter = 300`, PCC as equality constraints
(`||A||_F^2 = s r` normalisation), objective `-(sigma_{T_M}(M)/||A|| + sigma_{T_W}(W)/||A||^2)`
with `T_M = 2kr - s`, `T_W = min(C(s,2) r^2, k^2-1)`; starts: random and structured. Stop after
two materially different strategies (S-B structured start, S-C surrogate optimisation) if no new
maximum of `dim V` appears.

## Exact numeric thresholds

* Certified counterexample requires ALL of: (a) reduced-pipeline `dim V_perp < d`;
  (b) rank identical at relative tolerances 1e-5,1e-6,1e-8,1e-10,1e-12 (tolerance scaled to the
  EXTERNAL norm of the A blocks, never to a singular value of the matrix itself), Gram-eigenvalue
  route equal, singular gap `>= 1e4` (or dropped block exactly 0); (c) full `d x d` pipeline
  (`pcc_core.analyse`, Lyapunov-formula SLD from `rho`, `d rho`) gives the same `dim V`;
  (d) exact: rational (Gaussian) blocks with PCC residual **exactly 0** (Fractions) and the SLD
  Lyapunov equation `L rho + rho L = 2 d rho` exactly 0, QFIM determinant exactly non-zero, and
  `rank_{F_p} >= d^2 - d + 1` on the full `d x d` definition of `iW, iM` for two primes
  (`p` ~ 2^31, `p = 1 mod 4`), which lower-bounds the rank over `Q(i)`.
* Failing any of (a)-(d) -> `NUMERICALLY_AMBIGUOUS` / not certified; no verdict issued.
* PCC "true": relative violation `< 1e-9` (float), exactly 0 (exact arm).
* C-LB kill: any state with `dim V_perp < LB` (integer comparison, ranks robust) -> derived bound
  falsified.
* C-ID kill: `dim V_perp != r^2 + dim P + dim Q` on any robust-rank sample (dim P, dim Q
  computed by an independent nullspace route, not from V).

## Positive controls

1. **Rank-detector injection:** hand-built stack with exact rank `d^2-d+1` (float and exact
   Fractions/F_p arms), `d = 4..22`: the certificate MUST fire 40/40; with rank `d^2-d+5` MUST
   fire 0/40.
2. **Identity control:** the certificate machinery (a)-(d) applied to the pilot-firing state
   must reproduce identical `dim V` in reduced, full-float and F_p routes.

## Negative controls

1. **Eq. (16) class** (theorem: saturable) at `d = 8, 12, 22` (`d_sys r`): `dim V_perp >= d`
   MUST hold for all 20/20 samples each; any certified firing there falsifies either the paper's
   theorem or this harness.
2. **Random Hermitian substituted for SLDs:** PCC true in 0/200 (non-vacuity of the PCC check).
3. **Generic PCC states at `d = 22` with small `s`** (`s = 4, 10`): `dim V_perp >= d` expected
   (LB >= d); firing there falsifies C-LB.

## Stop rules

* Certified counterexample confirmed by (a)-(d) -> stop searching, save parameters, report.
* Wall-clock ~2.5 h, <= 10 processes; any reduction of N logged in the metrics with reason.
* Two materially different adaptive strategies without a new maximum -> stop.
