"""Independent numerical test of the separator (NOT a certificate).

For a grid of x = (cos(t/2), sin(t/2) e^{i p}) on the Bloch sphere, compute the kernel
K(x) = { y in R^40 : Phi_x y = 0 } (real form of Y_S(x), S = blocks 4..15), and
M(x) = lambda_max( N^T H N ), where N is an orthonormal basis of K(x) and H is the real
40x40 form of the Hermitian matrix R, so that y^H R y = y^T H y for y = (Re y, Im y).

sup_x M(x) estimates sup over unit y in the union of Y_S(x) of y^H R y. The separator
requires this supremum to be < s* = fl(0.9 tr R / 20). Grid values are lower bounds on the
true supremum, so a grid value above s* is a counterexample; a grid value below s* is
only evidence.

Also checks the real form H against the complex quadratic form on random y.

Usage: python -I dense_sup_grid.py <n_theta> <n_phi> <out.json>
"""

import hashlib
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = r"E:\Проверка Гипотез\работаю над проверкой гипотез\Y-17 100 gipotez\experiments"
INST = BASE + r"\20261027-h-cat56-2-submission-package-v1\data\instance_d22_r2_s16.jsonl"
RPATH = (
    BASE
    + r"\20261028-h-cat56-2-phase3\metrics\inputs\s14_R_4-5-6-7-8-9-10-11-12-13-14-15_nx250.npz"
)
S8DIR = BASE + r"\20261027-h-cat56-2-discovery\code"
sys.path.insert(0, S8DIR)
import s8_admissible_span as sa  # noqa: E402

S = list(range(4, 16))
S_STAR = 0.9 * float(np.trace(np.load(RPATH)["R"]).real) / 20.0


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def real_form(R):
    """40x40 real matrix H with y^H R y = y^T H y for y = (Re y, Im y)."""
    A = R.real
    B = R.imag
    # y = u + i v, R = A + iB (A symmetric, B antisymmetric for Hermitian R), B^T = -B:
    # y^H R y = u^T A u + v^T A v - u^T B v + v^T B u = u^T A u + v^T A v - 2 u^T B v
    # so H = [[A, -B], [B, A]] gives [u;v]^T H [u;v] = y^H R y (checked numerically in main)
    return np.block([[A, -B], [B, A]])


def kernel_basis(Phi):
    _, sv, Vh = np.linalg.svd(Phi)
    full = np.zeros(40)
    full[: len(sv)] = sv
    return Vh[-4:].T, full  # 40 x 4 orthonormal basis of the 4-dim kernel (generic rank 36)


def main():
    n_t, n_p, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    As = sa.load_A(INST)
    R = np.load(RPATH)["R"]
    H = real_form(R)

    # check 1: real form against complex quadratic form
    rng = np.random.default_rng(1)
    worst = 0.0
    for _ in range(200):
        y = rng.normal(size=20) + 1j * rng.normal(size=20)
        q_c = np.vdot(y, R @ y).real
        v = np.concatenate([y.real, y.imag])
        q_r = v @ H @ v
        worst = max(worst, abs(q_c - q_r))
    herm_err = float(np.abs(R - R.conj().T).max())

    # check 2: kernel vectors satisfy A_i^dag y in R x
    x = np.array([0.6, 0.8 * np.exp(0.3j)])
    Phi = sa.phi_rows(As, S, x)
    N, sv = kernel_basis(Phi)
    kres = 0.0
    for k in range(4):
        yk = N[:, k]
        yc = yk[:20] + 1j * yk[20:]
        for i in S:
            v = As[i].conj().T @ yc
            # v must be real multiple of x: Im(conj(x).v) = 0 and v - lam x = 0
            lam = np.vdot(x, v) / np.vdot(x, x)
            kres = max(kres, float(np.abs(v - lam * x).max()), float(abs(lam.imag)))

    # grid sup
    thetas = np.linspace(0.0, np.pi, n_t)
    phis = np.linspace(0.0, 2 * np.pi, n_p, endpoint=False)
    best = (-1.0, None, None)
    smin_global = np.inf
    vals = np.zeros((n_t, n_p))
    for a, t in enumerate(thetas):
        for b, p in enumerate(phis):
            xx = np.array([np.cos(t / 2), np.sin(t / 2) * np.exp(1j * p)])
            Phi = sa.phi_rows(As, S, xx)
            N, sv = kernel_basis(Phi)
            smin_global = min(smin_global, sv[35])
            K = N.T @ H @ N
            lam = float(np.linalg.eigvalsh(0.5 * (K + K.T))[-1])
            vals[a, b] = lam
            if lam > best[0]:
                best = (lam, float(t), float(p))

    result = {
        "instance_sha256": sha256_file(INST),
        "R_sha256": sha256_file(RPATH),
        "s_star": S_STAR,
        "real_form_max_error_random_y": worst,
        "hermitian_error_R": herm_err,
        "kernel_check_max_residual": kres,
        "grid": {"n_theta": n_t, "n_phi": n_p},
        "grid_sup": best[0],
        "grid_sup_at_theta_phi": [best[1], best[2]],
        "grid_sup_minus_s_star": best[0] - S_STAR,
        "min_sigma_36_over_grid": float(smin_global),
        "verdict_grid_below_s_star": bool(best[0] < S_STAR),
    }
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=1)
    print(json.dumps(result, indent=1))


if __name__ == "__main__":
    main()
