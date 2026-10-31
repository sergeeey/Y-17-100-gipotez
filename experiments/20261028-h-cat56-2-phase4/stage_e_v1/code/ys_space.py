# WHY: real linear structure of Y_S(x) = {y in C^20 : A_i^dag y = lambda_i x, lambda_i real, i in S}.
# A_i = 2*im - 2i*re (instance d22 r2 s16, same convention as stage_d/code/povm280_interval_criteria.py).
# For fixed direction x (phase/norm of x do not change the real subspace up to the same phase/scale),
# y = (re + i im) in R^40 satisfies 3 real equations per i: Im(x^dag u_i) = 0 and P_perp u_i = 0,
# where u_i = A_i^dag y in C^2.  Real kernel -> real basis b_a in C^20.
import json
import numpy as np

INST = (r"E:\Проверка Гипотез\работаю над проверкой гипотез\Y-17 100 gipotez\experiments"
        r"\20261027-h-cat56-2-submission-package-v1\data\instance_d22_r2_s16.jsonl")
S_PLUS = list(range(12))


def load_A(indices=S_PLUS):
    rec = json.loads(open(INST, encoding="utf-8").readline())
    A = {}
    for i in indices:
        flat = np.array(rec["blocks"][i], dtype=float)
        re_ = flat[:40].reshape(20, 2)   # flat[2r+a]
        im_ = flat[40:80].reshape(20, 2)  # flat[40+2r+a]
        A[i] = 2.0 * im_ - 2j * re_
    return A


def real_constraint_matrix(x, A, indices=S_PLUS):
    """36 x 40 real matrix M with M @ [Re y; Im y] = 0 <=> A_i^dag y in R x for all i."""
    rows = []
    xp = np.array([-x[1].conjugate(), x[0].conjugate()])  # orthogonal complement direction (unit if x unit)
    for i in indices:
        Ad = A[i].conj().T  # 2 x 20 : u = Ad @ y
        # linear map y -> u (complex 2-vector); write as complex 2x20 matrix G_i
        G = Ad
        # Im(x^dag u) = Im(x^dag G y)
        a = x.conjugate() @ G  # 1 x 20 complex: x^dag G
        # xp^dag u = 0 as complex equation: real and imaginary parts
        b = xp.conjugate() @ G
        # Real representation of complex row c (1x20) acting on y = yr + i yi: c y = (Re c)(yr) - (Im c)(yi) + i[(Im c) yr + (Re c) yi]
        def realrow(c):
            cr, ci = c.real, c.imag
            return np.hstack([cr, -ci]), np.hstack([ci, cr])  # (Re(c y), Im(c y)) as rows on [yr, yi]
        ar, ai = realrow(a)
        br, bi = realrow(b)
        rows.append(ai)            # Im(x^dag u) = 0
        rows.append(br)            # Re(xp^dag u) = 0
        rows.append(bi)            # Im(xp^dag u) = 0
    return np.array(rows)


def y_basis(x, A, indices=S_PLUS, tol=1e-10):
    """Real basis of Y_S(x) as complex 20-vectors (columns), via real kernel of the 36 x 40 system."""
    M = real_constraint_matrix(x, A, indices)
    _, s, Vh = np.linalg.svd(M)
    rank = int((s > tol * s[0]).sum())
    ker = Vh[rank:].T  # 40 x m real
    B = ker[:20] + 1j * ker[20:]  # 20 x m complex
    return B, s, rank


def bloch_x(theta, phi):
    return np.array([np.cos(theta / 2), np.exp(1j * phi) * np.sin(theta / 2)])
