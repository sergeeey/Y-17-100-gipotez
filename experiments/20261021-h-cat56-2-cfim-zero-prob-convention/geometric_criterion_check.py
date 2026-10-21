"""Element-level geometric criterion for saturation (claims G1, G2 of claim.md),
numerical check in float64.

Scope: element level. Each check takes a rank-one element E = |v><v| and tests the criterion
for it. The POVM-level statement for outcomes of rank >= 2 (one constant c^k for a whole range)
is not checked here (decision.md, limitation L7).

Setting (algebraic, no family needed): rho = diag(P, 0) with P > 0 on R (dim 2) inside C^d;
random Hermitian L_a, tangent operators dRho_a = (rho L_a + L_a rho)/2. For a rank-one
element E = |v><v|:
  p_v = <v|rho|v>, dp_a = Re <v|dRho_a|v>, N_v,ab = Re <v| L_a rho L_b |v>.
  Point-notion deficiency D_v = N_v - dp dp^T / p_v (regular v, p_v > 0),
  D_v = N_v (null v, p_v = 0).
Claims tested:
  G1: D_v = 0  iff  P_+ (L_a - c_a) v = 0 for all a, where c_a = dp_a / p_v (regular v);
      for null v: D_v = 0 iff P_+ L_a v = 0.
  G2: v in U = union_c W(c) iff for each a: P_+ L_a v is a real multiple of P_+ v
      (with P_+ v = 0 forcing P_+ L_a v = 0).
  Identity: the sum over all outcomes of N_E equals F^Q for any POVM summing to I. For
  regular outcomes D_E + dp dp^T / p = N_E, so F_pos cancels: the check tests the N-level
  identity, and the null branch is exercised only with the block basis.

Each class is counted separately and asserted on, so agreement cannot be vacuous:
  G1 regular: generic vectors (expected False) and vectors constructed in W(c) (expected True).
  G1 null: generic kernel vectors (expected False); a kernel vector k0 with P_+ L_a k0 = 0 in a
  family modified so that this holds (expected True).
  G2: vectors constructed in W(c) (members, expected True), generic vectors (non-members,
  expected False), and the zero branch P_+ v = 0 with P_+ L_a v = 0 (members) or not
  (non-members).
For p = 3 the third generator is a real-affine combination of the first two (L_3 = alpha L_1 +
beta L_2 + gamma I), so the constant c_3 is tied to c_1 and c_2 by the same coefficients.
"""

import json
from pathlib import Path

import numpy as np

RNG = np.random.default_rng(20261021)
DIM = 5
R_DIM = 2
OUT = Path(__file__).resolve().parent / "metrics" / "geometric_criterion_check_2026-10-21.json"


def complex_normal(rows, cols):
    return RNG.normal(size=(rows, cols)) + 1j * RNG.normal(size=(rows, cols))


def random_hermitian(n):
    g = complex_normal(n, n)
    return (g + g.conj().T) / 2


def setup(p_params):
    """Return rho, the generators, their tangents, P_+, and the affine coefficients for p = 3
    (None for p = 2). The coefficients are the only source of the affine relation."""
    rho = np.zeros((DIM, DIM), dtype=complex)
    rho[:R_DIM, :R_DIM] = np.diag([0.6, 0.4])
    ls = [random_hermitian(DIM), random_hermitian(DIM)]
    if p_params == 3:
        alpha, beta, gamma = 0.7, -1.3, 0.25
        ls.append(alpha * ls[0] + beta * ls[1] + gamma * np.eye(DIM))
        ls_coeff = (alpha, beta, gamma)
    else:
        ls_coeff = None
    ls = ls[:p_params]
    drhos = [(rho @ L + L @ rho) / 2 for L in ls]
    p_plus = np.diag([1.0] * R_DIM + [0.0] * (DIM - R_DIM)).astype(complex)
    return rho, ls, drhos, p_plus, ls_coeff


def element_quantities(v, rho, ls, drhos):
    p = float(np.real(v.conj() @ rho @ v))
    dp = np.array([float(np.real(v.conj() @ dr @ v)) for dr in drhos])
    n_mat = np.array(
        [[float(np.real(v.conj() @ (L_a @ rho @ L_b) @ v)) for L_b in ls] for L_a in ls]
    )
    return p, dp, n_mat


def nullspace(mat, tol=1e-10):
    _u, s, vh = np.linalg.svd(mat)
    rank = int(np.sum(s > tol))
    return vh[rank:].conj().T


def tie_constants(c, ls_coeff):
    """For p = 3 the third constant satisfies the same affine relation as the generators:
    c_3 = alpha c_1 + beta c_2 + gamma (see setup)."""
    if ls_coeff is not None:
        alpha, beta, gamma = ls_coeff
        c[2] = alpha * c[0] + beta * c[1] + gamma
    return c


def random_in_w(ls, p_plus, ls_coeff):
    """Random vector of W(c) = {v : P_+ (L_a - c_a) v = 0 for all a}, with c random and real.
    Returns None when the constraints leave no nonzero vector."""
    c = tie_constants(RNG.normal(size=len(ls)), ls_coeff)
    m = np.vstack([p_plus @ (L - c_a * np.eye(DIM)) for L, c_a in zip(ls, c)])
    ns = nullspace(m)
    if ns.shape[1] == 0:
        return None
    return ns @ (RNG.normal(size=ns.shape[1]) + 1j * RNG.normal(size=ns.shape[1]))


def random_kernel_vector():
    v = np.zeros(DIM, dtype=complex)
    v[R_DIM:] = complex_normal(DIM - R_DIM, 1)[:, 0]
    return v


def g1_check(rho, ls, drhos, p_plus, ls_coeff, trials=120):
    """G1 for regular and generic null vectors, with every class counted separately.

    regular_pos: vectors constructed in W(c); expected D_v = 0 and residual 0 (True).
    regular_neg: generic vectors; expected False.
    null_neg: generic kernel vectors; expected False. The null positive case is in g1_null_check.
    """
    tested = {"regular_pos": 0, "regular_neg": 0, "null_neg": 0}
    agree = {"regular_pos": 0, "regular_neg": 0, "null_neg": 0}
    skipped = 0
    for trial in range(trials):
        mode = trial % 3
        if mode == 0:
            kind = "regular_neg"
            v = complex_normal(DIM, 1)[:, 0]
        elif mode == 1:
            kind = "regular_pos"
            v = random_in_w(ls, p_plus, ls_coeff)
            if v is None:
                skipped += 1
                continue
        else:
            kind = "null_neg"
            v = random_kernel_vector()
        expected = kind == "regular_pos"
        p, dp, n_mat = element_quantities(v, rho, ls, drhos)
        if p > 1e-12:
            d_v = n_mat - np.outer(dp, dp) / p
            c_vec = dp / p
            resid = np.concatenate(
                [p_plus @ (L - c_a * np.eye(DIM)) @ v for L, c_a in zip(ls, c_vec)]
            )
        else:
            d_v = n_mat
            resid = np.concatenate([p_plus @ L @ v for L in ls])
        scale = max(1.0, float(np.max(np.abs(n_mat))))
        d_zero = np.max(np.abs(d_v)) < 1e-9 * scale
        r_zero = np.max(np.abs(resid)) < 1e-9 * max(1.0, np.linalg.norm(v))
        tested[kind] += 1
        agree[kind] += int(d_zero == expected and r_zero == expected)
    return {
        "agree": sum(agree.values()),
        "tested": sum(tested.values()),
        "skipped": skipped,
        "regular_pos_tested": tested["regular_pos"],
        "regular_pos_agree": agree["regular_pos"],
        "regular_neg_tested": tested["regular_neg"],
        "regular_neg_agree": agree["regular_neg"],
        "null_vectors_tested": tested["null_neg"],
        "null_agree": agree["null_neg"],
    }


def annihilate_coupling(L, k0):
    """Hermitian copy of L whose support-kernel block annihilates k0, i.e. P_+ L k0 = 0."""
    block = L[:R_DIM, R_DIM:]
    block = block - np.outer(block @ k0, k0.conj()) / np.vdot(k0, k0).real
    out = L.copy()
    out[:R_DIM, R_DIM:] = block
    out[R_DIM:, :R_DIM] = block.conj().T
    return out


def g1_null_check(p_params, trials=60):
    """G1 for null vectors: D_v = N_v = 0 iff P_+ L_a v = 0 for all a (v in the kernel of rho).

    Generic kernel vectors are the negative case. A positive case needs a kernel vector k0 with
    P_+ L_a k0 = 0. For generic L_a there is none (four complex conditions on a three-dimensional
    kernel), so the generators are modified with annihilate_coupling.
    """
    rho, ls, _, p_plus, _ = setup(p_params)
    k0 = complex_normal(DIM - R_DIM, 1)[:, 0]
    ls_mod = [annihilate_coupling(L, k0) for L in ls]
    counts = {
        "positive_tested": 0,
        "positive_agree": 0,
        "negative_tested": 0,
        "negative_agree": 0,
    }
    for trial in range(trials):
        positive = trial % 2 == 0
        if positive:
            v = np.zeros(DIM, dtype=complex)
            v[R_DIM:] = (RNG.normal() + 1j * RNG.normal()) * k0
        else:
            v = random_kernel_vector()
        n_mat = np.array(
            [[float(np.real(v.conj() @ (La @ rho @ Lb) @ v)) for Lb in ls_mod] for La in ls_mod]
        )
        resid = np.concatenate([p_plus @ La @ v for La in ls_mod])
        d_zero = np.max(np.abs(n_mat)) < 1e-9 * max(1.0, float(np.linalg.norm(v)) ** 2)
        r_zero = np.max(np.abs(resid)) < 1e-9 * max(1.0, float(np.linalg.norm(v)))
        key = "positive" if positive else "negative"
        counts[f"{key}_tested"] += 1
        counts[f"{key}_agree"] += int(d_zero == positive and r_zero == positive)
    return counts


def in_union(v, ls, p_plus, tol=1e-9):
    """G2 predicate: for each a, P_+ L_a v is a real multiple of P_+ v (zero if P_+ v = 0)."""
    pv = p_plus @ v
    pv_norm2 = float(np.real(np.vdot(pv, pv)))
    for L in ls:
        w = p_plus @ L @ v
        if pv_norm2 < 1e-24:
            if np.linalg.norm(w) > tol * max(1.0, np.linalg.norm(v)):
                return False
            continue
        c = np.vdot(pv, w) / pv_norm2
        if abs(c.imag) > tol * max(1.0, abs(c)):
            return False
        if np.linalg.norm(w - c.real * pv) > tol * max(1.0, np.linalg.norm(w)):
            return False
    return True


G2_CLASSES = ("members", "non_members", "null_members", "null_non_members")


def g2_check(ls, p_plus, ls_coeff, trials=100):
    """G2: v in U iff in_union(v), with four classes counted separately.

    members: constructed in W(c), so in U by definition (expected True).
    non_members: generic vectors, outside U almost surely (expected False).
    null_members / null_non_members: the zero branch P_+ v = 0, in a family modified so that a
    kernel vector k0 satisfies P_+ L_a k0 = 0 (expected True for k0, False for generic kernel
    vectors of the same family).
    """
    k0 = complex_normal(DIM - R_DIM, 1)[:, 0]
    ls_mod = [annihilate_coupling(L, k0) for L in ls]
    tested = {name: 0 for name in G2_CLASSES}
    agree = {name: 0 for name in G2_CLASSES}
    skipped = 0
    for trial in range(trials):
        kind = G2_CLASSES[trial % len(G2_CLASSES)]
        if kind == "members":
            v = random_in_w(ls, p_plus, ls_coeff)
            if v is None:
                skipped += 1
                continue
            family, expected = ls, True
        elif kind == "non_members":
            v = complex_normal(DIM, 1)[:, 0]
            family, expected = ls, False
        elif kind == "null_members":
            v = np.zeros(DIM, dtype=complex)
            v[R_DIM:] = (RNG.normal() + 1j * RNG.normal()) * k0
            family, expected = ls_mod, True
        else:
            v = random_kernel_vector()
            family, expected = ls_mod, False
        tested[kind] += 1
        agree[kind] += int(in_union(v, family, p_plus) == expected)
    result = {
        "agree": sum(agree.values()),
        "tested": sum(tested.values()),
        "skipped": skipped,
    }
    for name in G2_CLASSES:
        result[f"{name}_tested"] = tested[name]
        result[f"{name}_agree"] = agree[name]
    return result


def identity_check(rho, ls, drhos, trials=20, block=False):
    """Sum over all outcomes of N_E equals F^Q for a POVM summing to I, written with the
    regular/null split of the criterion (D_E + dp dp^T / p = N_E for regular E). F_pos cancels,
    so the check is an identity between N_E and the trace formula. block=True uses a basis
    adapted to support plus kernel (2 regular and 3 null outcomes); the default random basis
    gives regular outcomes only.
    """
    worst = 0.0
    null_outcomes = regular_outcomes = 0
    for _ in range(trials):
        if block:
            q = np.zeros((DIM, DIM), dtype=complex)
            qs, _ = np.linalg.qr(complex_normal(R_DIM, R_DIM))
            qk, _ = np.linalg.qr(complex_normal(DIM - R_DIM, DIM - R_DIM))
            q[:R_DIM, :R_DIM] = qs
            q[R_DIM:, R_DIM:] = qk
        else:
            q, _ = np.linalg.qr(complex_normal(DIM, DIM))
        fq = np.array([[np.real(np.trace(rho @ La @ Lb)) for Lb in ls] for La in ls])
        f_pos = np.zeros((len(ls), len(ls)))
        n_null = np.zeros((len(ls), len(ls)))
        d_reg = np.zeros((len(ls), len(ls)))
        for k in range(DIM):
            v = q[:, k]
            p, dp, n_mat = element_quantities(v, rho, ls, drhos)
            if p > 1e-12:
                regular_outcomes += 1
                f_pos += np.outer(dp, dp) / p
                d_reg += n_mat - np.outer(dp, dp) / p
            else:
                null_outcomes += 1
                n_null += n_mat
        worst = max(worst, float(np.max(np.abs(fq - (f_pos + n_null + d_reg)))))
    return {
        "worst_abs": worst,
        "regular_outcomes": regular_outcomes,
        "null_outcomes": null_outcomes,
    }


def main():
    results = {"G1": [], "G1_null": [], "G2": [], "identity": []}
    for p_params in [2, 3]:
        rho, ls, drhos, p_plus, ls_coeff = setup(p_params)
        g1 = g1_check(rho, ls, drhos, p_plus, ls_coeff)
        g1n = g1_null_check(p_params)
        g2 = g2_check(ls, p_plus, ls_coeff)
        w_random = identity_check(rho, ls, drhos)
        w_block = identity_check(rho, ls, drhos, block=True)
        results["G1"].append({"p": p_params, **g1})
        results["G1_null"].append({"p": p_params, **g1n})
        results["G2"].append({"p": p_params, **g2})
        results["identity"].append(
            {"p": p_params, "random_basis": w_random, "block_basis": w_block}
        )
        print(
            f"p={p_params}: G1 regular positive {g1['regular_pos_agree']}/"
            f"{g1['regular_pos_tested']}, regular negative {g1['regular_neg_agree']}/"
            f"{g1['regular_neg_tested']}, null negative {g1['null_agree']}/"
            f"{g1['null_vectors_tested']} (skipped {g1['skipped']}); "
            f"G1 null positive {g1n['positive_agree']}/{g1n['positive_tested']}, "
            f"negative {g1n['negative_agree']}/{g1n['negative_tested']}"
        )
        print(
            "  G2 "
            + ", ".join(
                f"{name} {g2[f'{name}_agree']}/{g2[f'{name}_tested']}" for name in G2_CLASSES
            )
            + f"; identity worst abs error {w_random['worst_abs']:.2e} (random basis), "
            f"{w_block['worst_abs']:.2e} (block basis, {w_block['null_outcomes']} null outcomes)"
        )
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"WROTE {OUT}")


if __name__ == "__main__":
    main()
