# H-CAT56-2 — claim.md (registered before any main search)

## Registration honesty note (read first)

Before this file was written, a **pilot** (`pilot_scratch.py`, throw-away, results not used as
evidence) was run to learn feasible `s` per `(d, r)`. The pilot happened to show
`dim V_perp < d` at `d >= 22`, `r = 2`. Therefore the statement "a certified instance
exists" is **not** a pre-registered blind prediction; it is a pilot observation that this
experiment must now re-verify under the Rank-Certificate Gate and by independent routes.
Everything numeric below (thresholds, N, seeds, configs) is fixed now, before the verification
and search runs. Anything added after is labelled `post-registration`.

## L0 classification (EstimandOps)

**Descriptive / existence + structure** question about a mathematical object class. No causal
claim, no population inference. Estimand-style sentence:

> We determine, for generic quasi-pure states (Yang arXiv:2405.00405 Eq. 12, NOT the
> Eq. (16) subclass) that satisfy PCC and have a full-rank QFIM, whether any state has an
> exactly certified `dim V_perp < d` (Observation 2 of Yang-Imai-Pezze arXiv:2601.21801),
> and which closed-form function of `(d, r, k, s)` bounds `dim V_perp` from below.

## Zero-Signal gate

| field | content |
|---|---|
| entity | quasi-pure state `rho` (rank `r`, dimension `d`, `s` parameters) with SLDs `L_i = [[0,A_i^dag],[A_i,0]]` |
| falsifiable predicate | "there exists such a state with PCC true, QFIM rank `s`, and `dim V_perp < d`" |
| measurable outcome | exact-rank certificate: rank of the stacked `{iW, iM}` matrices `>= d^2 - d + 1` (lower bound suffices) with exact PCC, exact QFIM non-singularity |

## Claims

**C-EX (existence).** There is a `(d, r, s)` with `r^2 + 1 < d` and a generic quasi-pure
state satisfying PCC, with full-rank QFIM, such that `dim V_perp < d` is certified by the
exact-rank certificate of the Rank-Certificate Gate. Prior expectation from H-CAT56-1:
**false** (observed max `dim V` 24/40/54 at d=6/7/8 vs needed 31/43/57). The pilot suggests
true at `d >= 22`. Kill condition for C-EX at a config: none of the N samples nor the
adaptive search reaches certification -> report "no certified counterexample under this
sampler/optimizer" (NOT a proof).

**C-ID (derived identity, to be verified numerically and by proof).** With
`P = {Y in C^{k x r}: A_i^dag Y Hermitian for all i}` and
`Q = {Z in Herm(k): A_i^dag Z A_j Hermitian for all i != j}`:

    V_M^perp (inside C^{k x r}) = P,   V_W^perp (inside Herm(k)) = Q,
    dim V_perp = r^2 + dim P + dim Q          (r^2 = support-support block, always in V_perp)

**C-LB (rigorous lower bound, rank-nullity).** If the `s` blocks `A_i` are real-linearly
independent (implied by a full-rank QFIM) then

    dim V_perp >= LB(k, r, s) := r^2 + max(s, 2kr - s r^2) + max(1, k^2 - C(s,2) r^2).

**C-CEIL (structural consequence, exact).** `min_{s>=2} LB(k,r,s) < d` first happens at
`d = 22` for `r = 2` and `d = 23` for `r = 3` (computed, `pilot_scratch2.py`, recomputed in the
main script). Hence for `r = 2, d <= 21` and `r = 3, d <= 22` the certified test can NEVER
fire (theorem, conditional on C-LB proof), and for larger `d` it can, generically.

Falsification of the derived claims: **any** PCC state found (sampled or optimized) with
real-independent blocks and `dim V_perp < LB(k, r, s)`, or any state where
`dim V_perp != r^2 + dim P + dim Q` (tolerance-swept), kills C-ID / C-LB.

## What this does NOT mean (>= 3)

1. A certified `dim V_perp < d` is a counterexample to *sufficiency of PCC* only through
   Observation 2 / Theorem 1 of the source paper. This experiment does not re-prove those
   theorems; it re-derives the linear-independence step of Observation 2 in prose but the
   dependence on the paper's Theorem 1 (that saturation <=> every POVM vector is hollow for all
   `W, M`) is inherited, `[DOCS]`.
2. It says nothing about the Eq. (16) class (proven sufficient in the paper's End Matter) and
   nothing about states with a `lambda`-dependent spectrum (only the constant-spectrum,
   `rho = U rho_0 U^dag` family is sampled).
3. A failed search at `d <= 21` (r=2) is **not** the evidence for absence; the absence there
   comes from C-LB (a bound), and C-LB's proof is what carries the weight.
4. `N` random samples or optimizer restarts prove nothing about states off the sampled
   distribution; the sequential-nullspace sampler reaches generic points of each PCC component
   it starts from, not measure-zero sub-branches unless started there.
5. Nothing here concerns experimental metrology; all objects are mathematical models with
   exactly-specified SLDs.

## Claim entropy (start)

unsupported HIGH claims 0 · hidden assumptions 2 (Observation 2 inherited; constant-spectrum
family) · missing negative controls 0 · ambiguous definitions 0 · unresolved blockers 0 ·
**total 2**.
