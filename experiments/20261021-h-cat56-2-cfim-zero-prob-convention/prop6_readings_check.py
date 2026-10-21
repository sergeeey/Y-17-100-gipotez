"""Proposition 6 readings at control point D (claims P1, P2 of claim.md), exact arithmetic.

Two POVMs of point D (model as in dmdp/controls/point_D_saturation_exact.py): the 22-outcome
projective ONB built from H_9 = I_9 - (2/9) J_9 (see
../20261021-h-cat56-2-projective-criterion/point_D_projective_onb_check.py), and the 36-outcome
rank-one POVM of the control script (blocks of weight s_k/2, plus four kernel projectors). For
every outcome k the kernel block is E_k00 = w v_K v_K^T (real vectors), and B_l = A_l (K x 2).

Readings of the kernel-block condition for all parameters l, m:
  literal: for every ORDERED pair (l, m) there is a finite real c with E_k00 B_l = c E_k00 B_m;
  one-sided: for every UNORDERED pair {l, m} at least one of E_k00 B_l = c E_k00 B_m or
  E_k00 B_m = c' E_k00 B_l holds (real c, c', zero allowed).
The check reports how many outcomes and pairs fail under each reading. No float arithmetic.
"""

from fractions import Fraction as Fr

K = 20
R = 2
NPAR = 16


def a_matrices():
    """A_l as K x R lists: A_l = e_{kernel row l} e_0^T (l < 8),
    A_{8+j} = e_{kernel row 10+j} e_1^T."""
    out = [[[Fr(0)] * R for _ in range(K)] for _ in range(NPAR)]
    for i in range(8):
        out[i][i][0] = Fr(1)
    for j in range(8):
        out[8 + j][10 + j][1] = Fr(1)
    return out


def projective_onb_kernel_parts():
    """Kernel parts (length K, rational) and weights of the 22-outcome ONB;
    kernel row r has index r."""
    h9 = [[(Fr(1) if r == c else Fr(0)) - Fr(2, 9) for c in range(9)] for r in range(9)]
    # block 1: support R0 with kernel rows 0..7; block 2: support R1 with kernel rows 10..17
    outcomes = []
    for kern_rows in ([0, 1, 2, 3, 4, 5, 6, 7], [10, 11, 12, 13, 14, 15, 16, 17]):
        for col in range(9):
            vk = [Fr(0)] * K
            for row in range(8):
                vk[kern_rows[row]] = h9[row + 1][col]
            outcomes.append((Fr(1), vk))
    for r in (8, 9, 18, 19):
        vk = [Fr(0)] * K
        vk[r] = Fr(1)
        outcomes.append((Fr(1), vk))
    return outcomes


def povm36_kernel_parts():
    """Kernel parts of the 36-outcome rank-one POVM of point_D_saturation_exact.py (weights w_k)."""
    s_vals = [Fr(9, 100) if k % 2 == 0 else Fr(16, 100) for k in range(8)]
    a_vals = [Fr(10, 3) if k % 2 == 0 else Fr(5, 2) for k in range(8)]
    w_vals = [s / 2 for s in s_vals]
    outcomes = []
    for kern0 in (0, 10):  # kernel rows 0..7 (block 1) and 10..17 (block 2)
        for k in range(8):
            for eps in (1, -1):
                vk = [Fr(0)] * K
                vk[kern0 + k] = eps * a_vals[k]
                outcomes.append((w_vals[k], vk))
    for r in (8, 9, 18, 19):
        vk = [Fr(0)] * K
        vk[r] = Fr(1)
        outcomes.append((Fr(1), vk))
    return outcomes


def e00_b(w, vk, a_list, i):
    """E_k00 B_l = w * vK (vK^T B_l), a K x R matrix."""
    row = [
        sum((vk[r] * a_list[i][r][c] for r in range(K)), Fr(0)) for c in range(R)
    ]  # vK^T B_l, 1 x R
    return [[w * vk[r] * row[c] for c in range(R)] for r in range(K)]


def is_zero(m):
    return all(x == 0 for row in m for x in row)


def proportional_with_real_c(m1, m2):
    """True iff m1 = c m2 for some real c (c = 0 allowed)."""
    if is_zero(m2):
        return is_zero(m1)
    c = None
    for r in range(K):
        for col in range(R):
            if m2[r][col] != 0:
                c = m1[r][col] / m2[r][col]
                break
        if c is not None:
            break
    return all(m1[r][col] == c * m2[r][col] for r in range(K) for col in range(R))


def check(outcomes, name):
    a_list = a_matrices()
    literal_fail_outcomes = 0
    literal_fail_pairs = 0
    onesided_fail_pairs = 0
    total_pairs = 0
    for w, vk in outcomes:
        mats = [e00_b(w, vk, a_list, i) for i in range(NPAR)]
        outcome_literal_ok = True
        for i in range(NPAR):
            for j in range(NPAR):
                if i == j:
                    continue
                if not proportional_with_real_c(mats[i], mats[j]):
                    literal_fail_pairs += 1
                    outcome_literal_ok = False
        if not outcome_literal_ok:
            literal_fail_outcomes += 1
        for i in range(NPAR):
            for j in range(i + 1, NPAR):
                total_pairs += 1
                ok = proportional_with_real_c(mats[i], mats[j]) or proportional_with_real_c(
                    mats[j], mats[i]
                )
                if not ok:
                    onesided_fail_pairs += 1
    return {
        "POVM": name,
        "outcomes": len(outcomes),
        "literal_failing_outcomes": literal_fail_outcomes,
        "literal_failing_ordered_pairs": literal_fail_pairs,
        "one_sided_failing_unordered_pairs": onesided_fail_pairs,
        "unordered_pairs_checked": total_pairs,
    }


def main():
    results = [
        check(projective_onb_kernel_parts(), "22-outcome projective ONB at D"),
        check(povm36_kernel_parts(), "36-outcome rank-one POVM at D"),
    ]
    for r in results:
        print(r)
    return results


if __name__ == "__main__":
    main()
