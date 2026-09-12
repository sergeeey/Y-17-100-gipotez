"""Exam 3, stage 7: derive lambda_k FROM FIRST PRINCIPLES via symbolic computer algebra (sympy),
closing the gap point 26 explicitly flagged ("the exact closed form lambda_k=(q)_k(N-q)_k/(N)_{2k}
was NOT re-derived from first principles... rests on cited standard facts plus the empirical
5-for-5 pattern match").

Method: the trace identity from point 26's tight-frame theorem gives
    lambda_k = C(N,k) * ||Z_A||^2 / dim(V_k)      (any fixed A works, all equal by symmetry)
where dim(V_k)=C(N,k)-C(N,k-1) (standard Johnson scheme dimension formula, still cited, not
re-derived here -- see decision.md point 27 for exactly what remains cited vs derived) and

    ||Z_A||^2 = <Y_A,Y_A> - sum_{j=0}^{k-1} E_j(Y_A)

i.e. the "self-energy" of the raw k-set indicator Y_A(S)=1[A subseteq S] at every level BELOW k,
computed using the SAME already-verified recursive E_j formulas (E_1 closed form, E_2 analytic
double-centered projection) -- but evaluated SYMBOLICALLY on exact hypergeometric containment
probabilities p_m(N,q):=P(fixed m-subset subseteq random q-subset)=(q)_m/(N)_m (falling
factorials), for GENERAL symbolic N,q, not spot-checked numbers.

Result: symbolically confirmed (sp.simplify of the difference is exactly 0, not just numerically
close) for k=1,2,3 -- MATCH: True in every case, for general N,q. This is a genuine derivation,
not a numeric pattern extrapolation: the k=2,3 cases required expanding sum_{a<b} r_ab^2 by
grouping pairs (for k=3: also triples-worth-of-pair-types) by their intersection size with A,
which is honest combinatorial bookkeeping, not curve-fitting.

Not yet extended to k=4,5 (would need one more recursion level -- E_3(Y_A) for k=4, grouping
TRIPLES by |A intersect triple|, 4 distinct types instead of k=3's 3 -- same method, more
bookkeeping, not attempted here for time budget reasons, not because of a discovered obstruction).
"""

import sympy as sp

N, q = sp.symbols("N q", positive=True)


def p_m(m):
    """P(a fixed m-subset of ground elements is contained in a uniform random q-subset of an
    N-element ground set) = falling_factorial(q,m) / falling_factorial(N,m)."""
    return sp.ff(q, m) / sp.ff(N, m)


def dim_v(k):
    return sp.binomial(N, k) - sp.binomial(N, k - 1)


def lambda_hypothesis(k):
    return sp.factor(sp.ff(q, k) * sp.ff(N - q, k) / sp.ff(N, 2 * k))


def derive_lambda_1():
    p1 = p_m(1)
    z2 = sp.simplify(p1 - p1**2)  # ||Z_a||^2 = Var(Y_a) since Y_a is 0/1
    return sp.factor(sp.simplify(sp.binomial(N, 1) * z2 / dim_v(1)))


def derive_lambda_2():
    p2, p3 = p_m(2), p_m(3)
    e0 = p2**2
    # mu_j: j in A (2 such j, E[Y_A*e_j]=E[Y_A]=p2 since A already implies e_j=1);
    #       j notin A (N-2 such j, E[Y_A*e_j]=p3, one more element forced in)
    mu_in = p2 - p2 * (q / N)
    mu_out = p3 - p2 * (q / N)
    e1 = sp.simplify((2 * mu_in**2 + (N - 2) * mu_out**2) * N * (N - 1) / (q * (N - q)))
    z2 = sp.simplify(p2 - e0 - e1)
    return sp.factor(sp.simplify(sp.binomial(N, 2) * z2 / dim_v(2)))


def derive_lambda_3():
    lam2 = lambda_hypothesis(2)  # already independently derived above; reused as a known constant
    p2, p3, p4, p5 = p_m(2), p_m(3), p_m(4), p_m(5)

    e0 = p3**2
    mu_in = p3 - p3 * (q / N)
    mu_out = p4 - p3 * (q / N)
    e1 = sp.simplify((3 * mu_in**2 + (N - 3) * mu_out**2) * N * (N - 1) / (q * (N - q)))

    # E_2(Y_A), |A|=3: group pairs {a,b} by |A intersect {a,b}|
    mu_both = p3 - p3 * p2  # both a,b in A: 3 such pairs
    mu_one = p4 - p3 * p2  # exactly one in A: 3*(N-3) such pairs
    mu_none = p5 - p3 * p2  # neither in A: C(N-3,2) such pairs

    s_inA = 2 * mu_both + (N - 3) * mu_one  # s_a for a in A
    s_notA = 3 * mu_one + (N - 4) * mu_none  # s_a for a notin A
    big_s = 3 * mu_both + 3 * (N - 3) * mu_one + sp.binomial(N - 3, 2) * mu_none

    def r_of(mu, sa, sb):
        return mu - (sa + sb) / (N - 2) + 2 * big_s / ((N - 1) * (N - 2))

    r_both = r_of(mu_both, s_inA, s_inA)
    r_one = r_of(mu_one, s_inA, s_notA)
    r_none = r_of(mu_none, s_notA, s_notA)
    sum_r_sq = 3 * r_both**2 + 3 * (N - 3) * r_one**2 + sp.binomial(N - 3, 2) * r_none**2
    e2 = sp.simplify(sum_r_sq / lam2)

    z2 = sp.simplify(p3 - e0 - e1 - e2)
    return sp.factor(sp.simplify(sp.binomial(N, 3) * z2 / dim_v(3)))


if __name__ == "__main__":
    results = {}
    for k, derive_fn in [(1, derive_lambda_1), (2, derive_lambda_2), (3, derive_lambda_3)]:
        derived = derive_fn()
        hypothesis = lambda_hypothesis(k)
        match = sp.simplify(derived - hypothesis) == 0
        results[k] = {"derived": str(derived), "hypothesis": str(hypothesis), "match": match}
        print(f"k={k}")
        print(f"  derived    = {derived}")
        print(f"  hypothesis = {hypothesis}")
        print(f"  MATCH: {match}")

    all_match = all(r["match"] for r in results.values())
    print(f"\nAll k=1,2,3 symbolically confirmed: {all_match}")

    import json
    from pathlib import Path

    metrics_dir = Path(__file__).resolve().parent / "metrics"
    metrics_dir.mkdir(exist_ok=True)
    with open(metrics_dir / "lambda_k_first_principles.json", "w", encoding="utf-8") as f:
        json.dump({"results": results, "all_match": all_match}, f, indent=2)
