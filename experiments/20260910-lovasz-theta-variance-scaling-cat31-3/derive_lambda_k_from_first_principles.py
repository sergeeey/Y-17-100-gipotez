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

k=4 (2026-09-12): extended using the SAME trace identity, but E_3(Y_A) (needed for the first
time -- k=3 only required E_1, E_2) cannot reuse the y_ab/r_ab-style explicit basis without one
more layer of bookkeeping (the "z_abc" basis itself, not just projections onto it). Instead it
is computed via self-adjointness of the already-verified orthogonal projections P1, P2:
    <z_abc, Y_A_c> = <e_abc_c, Y_A_c> - <e_abc_c, P1(Y_A_c)> - <e_abc_c, P2(Y_A_c)>
Each term on the right is a cross-moment, computed by classifying the ground set into 4
REGIONS by (in A?, in triple {a,b,c}?) and summing over region-pairs -- implemented as an
explicit loop (see derive_lambda_4 below), not derived by hand, specifically to avoid the
"hidden hand-algebra error" risk that motivated writing this file symbolically in the first
place. Confirmed: sp.simplify(derived - hypothesis) == 0 for general symbolic N,q.

Not yet extended to k=5 (would need E_4(Y_A), grouping QUADS by |A intersect quad| into 5
types, plus a third self-adjoint cross-term through P3 -- same method, more bookkeeping, not
attempted here, not because of a discovered obstruction).
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


def derive_lambda_4():
    lam2 = lambda_hypothesis(2)
    lam3 = lambda_hypothesis(3)
    p2, p3, p4, p5, p6 = p_m(2), p_m(3), p_m(4), p_m(5), p_m(6)

    # --- E1(Y_A), |A|=4 ---
    mu_in = p4 - p4 * (q / N)
    mu_out = p5 - p4 * (q / N)
    e1 = sp.simplify((4 * mu_in**2 + (N - 4) * mu_out**2) * N * (N - 1) / (q * (N - q)))

    # --- E2(Y_A), |A|=4: pairs grouped by |A intersect pair| ---
    mu_both = p4 - p4 * p2  # both in A -- C(4,2)=6 pairs
    mu_one = p5 - p4 * p2  # one in A -- 4*(N-4) pairs
    mu_none = p6 - p4 * p2  # neither in A -- C(N-4,2) pairs

    s_inA = 3 * mu_both + (N - 4) * mu_one
    s_notA = 4 * mu_one + (N - 5) * mu_none
    big_S = 6 * mu_both + 4 * (N - 4) * mu_one + sp.binomial(N - 4, 2) * mu_none

    def r_of(mu, sa, sb):
        return mu - (sa + sb) / (N - 2) + 2 * big_S / ((N - 1) * (N - 2))

    r_both = sp.simplify(r_of(mu_both, s_inA, s_inA))
    r_one = sp.simplify(r_of(mu_one, s_inA, s_notA))
    r_none = sp.simplify(r_of(mu_none, s_notA, s_notA))
    e2 = sp.simplify(
        (6 * r_both**2 + 4 * (N - 4) * r_one**2 + sp.binomial(N - 4, 2) * r_none**2) / lam2
    )
    # how many of {u,w} land in A -> which r value (reused below for E3's cross-term)
    r_by_inA_count = {2: r_both, 1: r_one, 0: r_none}

    # --- E3(Y_A), |A|=4: triples {a,b,c} grouped by t=|A intersect triple| ---
    # via self-adjointness of P1,P2: <z_abc,Y_A> = <e_abc,Y_A> - <e_abc,P1(Y_A)> - <e_abc,P2(Y_A)>,
    # each cross-term computed by classifying the ground set into 4 regions by (in A?, in
    # triple {a,b,c}?) and summing over region-pairs -- explicit loop, not hand algebra.
    eta_2 = {2: p3 - p3 * p2, 1: p4 - p3 * p2, 0: p5 - p3 * p2}  # x = |{u,w} intersect triple|
    nu_single = {True: p3 - p3 * q / N, False: p4 - p3 * q / N}  # is single elt in triple?
    scale1 = N * (N - 1) / (q * (N - q))

    e3_by_t = {}
    for t in (0, 1, 2, 3):
        regions = [
            {"size": t, "inA": True, "inT": True},  # A ∩ triple
            {"size": 4 - t, "inA": True, "inT": False},  # A \ triple
            {"size": 3 - t, "inA": False, "inT": True},  # triple \ A
            {"size": N - 7 + t, "inA": False, "inT": False},  # neither
        ]
        mu_type_t = p_m(7 - t) - p4 * p3  # Cov(e_abc, Y_A) = <e_abc_c, Y_A_c>

        e1_cross = sum(
            r["size"] * (mu_in if r["inA"] else mu_out) * nu_single[r["inT"]] for r in regions
        )
        e1_cross = sp.simplify(scale1 * e1_cross)

        e2_cross = 0
        for i in range(len(regions)):
            for j in range(i, len(regions)):
                ri, rj = regions[i], regions[j]
                count = sp.binomial(ri["size"], 2) if i == j else ri["size"] * rj["size"]
                r_val = r_by_inA_count[int(ri["inA"]) + int(rj["inA"])]
                eta_val = eta_2[int(ri["inT"]) + int(rj["inT"])]
                nu_sum = nu_single[ri["inT"]] + nu_single[rj["inT"]]
                e2_cross += count * r_val * (eta_val - (q - 1) / (N - 2) * nu_sum)
        e2_cross = sp.simplify(e2_cross / lam2)

        e3_by_t[t] = sp.simplify(mu_type_t - e1_cross - e2_cross)

    triple_count_by_t = {t: sp.binomial(4, t) * sp.binomial(N - 4, 3 - t) for t in (0, 1, 2, 3)}
    e3 = sp.simplify(sum(triple_count_by_t[t] * e3_by_t[t] ** 2 for t in (0, 1, 2, 3)) / lam3)

    z2 = sp.simplify(p4 - p4**2 - e1 - e2 - e3)
    return sp.factor(sp.simplify(sp.binomial(N, 4) * z2 / dim_v(4)))


if __name__ == "__main__":
    results = {}
    for k, derive_fn in [
        (1, derive_lambda_1),
        (2, derive_lambda_2),
        (3, derive_lambda_3),
        (4, derive_lambda_4),
    ]:
        derived = derive_fn()
        hypothesis = lambda_hypothesis(k)
        match = sp.simplify(derived - hypothesis) == 0
        results[k] = {"derived": str(derived), "hypothesis": str(hypothesis), "match": match}
        print(f"k={k}")
        print(f"  derived    = {derived}")
        print(f"  hypothesis = {hypothesis}")
        print(f"  MATCH: {match}")

    all_match = all(r["match"] for r in results.values())
    print(f"\nAll k=1,2,3,4 symbolically confirmed: {all_match}")

    import json
    from pathlib import Path

    metrics_dir = Path(__file__).resolve().parent / "metrics"
    metrics_dir.mkdir(exist_ok=True)
    with open(metrics_dir / "lambda_k_first_principles.json", "w", encoding="utf-8") as f:
        json.dump({"results": results, "all_match": all_match}, f, indent=2)
