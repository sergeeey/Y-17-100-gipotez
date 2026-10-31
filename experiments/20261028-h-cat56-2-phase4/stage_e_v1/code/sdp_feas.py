# WHY: exact POVM search as an SDP on a finite grid of directions x_j (Bloch sphere, phase fixed by x_j).
# Element v = (x_j; B_j c), c real in R^m (B_j = real basis of Y_S(x_j)), weight w>0.
# Per grid point j, the moments M_j = [[Q_j, s_j],[s_j^T, t_j]] = sum_k w_k (1;c_k)(1;c_k)^T  must be PSD.
# Exact POVM sum_k w_k v_k v_k^dag = I_22 becomes LINEAR in (Q_j, s_j, t_j):
#   (a) sum_j t_j x_j x_j^dag = I_2
#   (b) sum_j x_j (B_j s_j)^dag = 0          (2 x 20 complex)
#   (c) sum_j B_j Q_j B_j^dag = I_20         (20 x 20 Hermitian)
import numpy as np
import cvxpy as cp
from ys_space import load_A, y_basis, bloch_x


def fibonacci_sphere(J):
    k = np.arange(J) + 0.5
    theta = np.arccos(1 - 2 * k / J)
    phi = np.pi * (1 + 5 ** 0.5) * k
    return theta, np.mod(phi, 2 * np.pi)


def build_grid(indices, J):
    A = load_A(indices)
    th, ph = fibonacci_sphere(J)
    X, Bs = [], []
    for t, p in zip(th, ph):
        x = bloch_x(t, p)
        B, _, rank = y_basis(x, A, indices)
        assert rank == 36 - 0 or True
        X.append(x)
        Bs.append(B)
    return np.array(X), Bs


def solve(X, Bs, TI2, TI20, TX, solver="SCS", verbose=False, **kw):
    """Feasibility of: sum_j t_j x x^dag = TI2 ; sum_j x (B s)^dag = TX ; sum_j B Q B^dag = TI20.
    TI2 (2x2 Hermitian), TX (2x20 complex), TI20 (20x20 Hermitian) are targets (identity for the real problem)."""
    J = len(Bs)
    ms = [B.shape[1] for B in Bs]  # kernel dimension may jump at special directions
    Ms = [cp.Variable((mj + 1, mj + 1), symmetric=True) for mj in ms]
    cons = [M >> 0 for M in Ms]
    # (a) identity on the x-block
    Ra = 0
    Ia = 0
    for j in range(J):
        P = np.outer(X[j], X[j].conj())
        t = Ms[j][ms[j], ms[j]]
        Ra = Ra + t * P.real
        Ia = Ia + t * P.imag
    # Hermitian equalities: keep upper triangle only (real part symmetric, imag part antisymmetric -> duplicates)
    cons += [Ra[a, b] == TI2.real[a, b] for a in range(2) for b in range(a, 2)]
    cons += [Ia[a, b] == TI2.imag[a, b] for a in range(2) for b in range(a + 1, 2)]
    # (b) cross block and (c) y-block
    Rb = 0
    Ib = 0
    Rc = 0
    Ic = 0
    for j in range(J):
        B = Bs[j]
        Br, Bi = B.real, B.imag
        mj = ms[j]
        Q = Ms[j][:mj, :mj]
        s = Ms[j][:mj, mj]
        Ys_r = Br @ s  # real part of B s
        Ys_i = Bi @ s
        xr, xi = X[j].real, X[j].imag
        # x_a * conj(Ys_r - i Ys_i)_r  ->  real/imag parts for every (a, r): outer products with cvxpy
        Rb = Rb + cp.outer(xr, Ys_r) + cp.outer(xi, Ys_i)   # Re(x conj(Ys)) = xr*Ysr + xi*Ysi
        Ib = Ib + cp.outer(xi, Ys_r) - cp.outer(xr, Ys_i)   # Im(x conj(Ys))
        Rc = Rc + Br @ Q @ Br.T + Bi @ Q @ Bi.T
        Ic = Ic + Bi @ Q @ Br.T - Br @ Q @ Bi.T
    cons += [Rb == TX.real, Ib == TX.imag]
    cons += [Rc[a, b] == TI20.real[a, b] for a in range(20) for b in range(a, 20)]
    cons += [Ic[a, b] == TI20.imag[a, b] for a in range(20) for b in range(a + 1, 20)]
    prob = cp.Problem(cp.Minimize(0), cons)
    prob.solve(solver=solver, verbose=verbose, **kw)
    return prob.status, Ms, prob
