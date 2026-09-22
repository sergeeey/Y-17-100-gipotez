# ruff: noqa
"""Gate 4b: a control that CAN fail on the V-builder.

The paper's End Matter example (two qubits + qubit ancilla, lambda = 0) comes with an explicit saturating measurement
{|e_v^(a)> (x) |a>} (Eqs. 34-41 of arXiv:2601.21801). By the Hollowization Theorem every projector of a saturating
POVM must lie in V-perp. So, with V built by the SAME generic code as for the counterexample (gate4_source_example.analyse
internals), check <pi|iW|pi> = 0 and <pi|iM|pi> = 0 for all generators, that the projectors sum to I, and that
F^C = F^Q. If the V-builder had a wrong definition, this would (very likely) fail.
"""

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import gate4_source_example as g

X, Z, I2 = g.X, g.Z, g.I2
k0, k1 = g.ket([1, 0]), g.ket([0, 1])
plus, minus = g.ket([1, 1]), g.ket([1, -1])


def two(a, b):
    return np.kron(a, b)


def build(q, theta):
    phi = g.ket([np.cos(theta / 2), np.sin(theta / 2)])
    phip = g.ket([np.sin(theta / 2), -np.cos(theta / 2)])
    phix = X @ phi
    phipx = X @ phip
    zz, xx = g.kron(Z, Z), g.kron(X, X)
    v0, v1 = two(k0, plus), two(k1, phi)
    a0, a1 = np.outer(k0, k0.conj()), np.outer(k1, k1.conj())
    rho = q * np.kron(np.outer(v0, v0.conj()), a0) + (1 - q) * np.kron(np.outer(v1, v1.conj()), a1)
    drhos = [-1j * (np.kron(G, I2) @ rho - rho @ np.kron(G, I2)) for G in (zz, xx)]
    s3, s2 = np.sqrt(3), np.sqrt(2)
    e0 = [
        (two(k0, plus) + 1j * s2 * two(k1, plus)) / s3,
        (two(k0, plus) - 1j / s2 * two(k1, plus) + 1j * np.sqrt(3 / 2) * two(k0, minus)) / s3,
        (two(k0, plus) - 1j / s2 * two(k1, plus) - 1j * np.sqrt(3 / 2) * two(k0, minus)) / s3,
        two(k1, minus),
    ]
    e1 = [
        (two(k1, phi) + 1j * s2 * two(k0, phix)) / s3,
        (two(k1, phi) - 1j / s2 * two(k0, phix) + 1j * np.sqrt(3 / 2) * two(k1, phip)) / s3,
        (two(k1, phi) - 1j / s2 * two(k0, phix) - 1j * np.sqrt(3 / 2) * two(k1, phip)) / s3,
        two(k0, phipx),
    ]
    pis = [np.kron(e, k0) for e in e0] + [np.kron(e, k1) for e in e1]
    return rho, drhos, pis


def generators(rho, drhos, r=2):
    w, u = np.linalg.eigh(rho)
    order = np.argsort(w)[::-1]
    psi = u[:, order[:r]]
    ls = [g.sld(rho, m) for m in drhos]

    def proj(a, b):
        return np.outer(psi[:, a], psi[:, b].conj())

    sig = [proj(a, a) for a in range(r)]
    for a in range(r):
        for b in range(a + 1, r):
            sig.append(proj(a, b) + proj(b, a))
            sig.append(-1j * (proj(a, b) - proj(b, a)))
    gens = []
    for i, li in enumerate(ls):
        for sg in sig:
            gens.append(1j * (sg @ li - li @ sg))
    for i in range(len(ls)):
        for j in range(i + 1, len(ls)):
            for sg in sig:
                x = ls[i] @ sg @ ls[j]
                gens.append(1j * (x - x.conj().T))
    return gens, ls


def main():
    out = []
    for q, th in [(0.3, 0.7), (0.5, 1.1), (0.8, 0.4)]:
        rho, drhos, pis = build(q, th)
        gens, ls = generators(rho, drhos)
        norms = [abs(np.vdot(p, p)) for p in pis]
        comp = np.linalg.norm(sum(np.outer(p, p.conj()) for p in pis) - np.eye(8))
        viol = max(abs(np.vdot(p, gm @ p)) for p in pis for gm in gens)
        # classical Fisher information of the measurement at lambda = 0
        pr = np.array([np.real(np.vdot(p, rho @ p)) for p in pis])
        dp = [np.array([np.real(np.vdot(p, d @ p)) for p in pis]) for d in drhos]
        fc = np.array(
            [
                [
                    sum(dp[i][k] * dp[j][k] / pr[k] for k in range(8) if pr[k] > 1e-12)
                    for j in range(2)
                ]
                for i in range(2)
            ]
        )
        fq = np.array(
            [
                [np.real(np.trace(rho @ (ls[i] @ ls[j] + ls[j] @ ls[i])) / 2) for j in range(2)]
                for i in range(2)
            ]
        )
        # negative control: a random unit vector (not from the paper) must violate the V conditions
        rng = np.random.default_rng(5)
        v = rng.normal(size=8) + 1j * rng.normal(size=8)
        v /= np.linalg.norm(v)
        neg = max(abs(np.vdot(v, gm @ v)) for gm in gens)
        row = {
            "q": q,
            "theta": th,
            "projector_norms_min_max": [min(norms), max(norms)],
            "completeness_residual": float(comp),
            "max_abs_<pi|generator|pi>": float(viol),
            "negative_control_random_vector_max": float(neg),
            "F_C_minus_F_Q_max_abs": float(np.max(np.abs(fc - fq))),
            "n_generators": len(gens),
        }
        out.append(row)
        print(row)
    (HERE / "metrics" / "gate4b_lmcc_in_vperp.json").write_text(
        json.dumps(out, indent=1), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
