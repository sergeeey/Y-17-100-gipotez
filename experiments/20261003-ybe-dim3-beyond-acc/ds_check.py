"""DS-move test (Doikou-Smoktunowitz style, as described in arXiv:2609.38290 sec 2.2): find all T (GL_N) with [T(x)T, R] = 0,
form R_T = (T(x)1) R (T(x)1)^{-1}. R_T is again a YBE solution and is infinity-equivalent (not locally) to R."""
import os
os.environ.setdefault('OMP_NUM_THREADS', '1')
import numpy as np
from ybe import *

def residT(T, U, R, N, w):
    TT = np.kron(T, T)
    return np.concatenate([(TT @ R - R @ TT).reshape(-1), (T @ U - np.eye(N)).reshape(-1), [np.sum(w * T) - 1.0]])

def jacT(T, U, R, N, w):
    n2 = N * N
    nr = (N * N) ** 2
    J = np.zeros((nr + n2 + 1, 2 * n2), dtype=complex)
    for k in range(n2):
        a, b = divmod(k, N)
        E = np.zeros((N, N)); E[a, b] = 1
        D = np.kron(E, T) + np.kron(T, E)
        J[:nr, k] = (D @ R - R @ D).reshape(-1)
        J[nr:nr + n2, k] = (E @ U).reshape(-1)
        J[nr:nr + n2, n2 + k] = (T @ E).reshape(-1)
    J[-1, :n2] = w.reshape(-1)
    return J

def find_T(R, N, seed, maxit=100):
    rng = np.random.default_rng(seed)
    w = rng.normal(size=(N, N)) + 1j * rng.normal(size=(N, N))
    T = rng.normal(size=(N, N)) + 1j * rng.normal(size=(N, N)); T = T / np.sum(w * T)
    U = np.linalg.inv(T)
    mu = 1e-2
    r = residT(T, U, R, N, w); f = np.linalg.norm(r)
    for _ in range(maxit):
        J = jacT(T, U, R, N, w); H = J.conj().T @ J; g = J.conj().T @ r
        ok = False
        for _ in range(10):
            d = np.linalg.solve(H + mu * np.eye(H.shape[0]), -g)
            Tn = T + d[:N * N].reshape(N, N); Un = U + d[N * N:].reshape(N, N)
            rn = residT(Tn, Un, R, N, w); fn = np.linalg.norm(rn)
            if fn < f: T, U, r, f, mu, ok = Tn, Un, rn, fn, max(mu / 5, 1e-14), True; break
            mu *= 4
        if f < 1e-13 or not ok: break
    return (T, f)

def proj_dist(A, B):
    # distance between A and B up to scalar
    c = np.vdot(B.ravel(), A.ravel()) / np.vdot(B.ravel(), B.ravel())
    return np.linalg.norm(A - c * B) / np.linalg.norm(A)

def ds_moves(R, N, nstarts=60):
    R = R / abs(np.linalg.det(R)) ** (1.0 / (N * N))
    Ts = []
    for s in range(nstarts):
        T, f = find_T(R, N, s)
        if f > 1e-10: continue
        T = T / abs(np.linalg.det(T)) ** (1.0 / N)
        if proj_dist(T, np.eye(N)) < 1e-6: continue
        if any(proj_dist(T, T2) < 1e-6 for T2 in Ts): continue
        Ts.append(T)
    out = []
    for T in Ts:
        A = np.kron(T, np.eye(N))
        RT = A @ R @ np.linalg.inv(A)
        out.append((T, RT, rel_res(RT, N), cc_class(RT, N)))
    return Ts, out

if __name__ == '__main__':
    # self-test: the Gaussian solution has finite Pauli-type local automorphisms; the 'ex:texas2step'-type flip example (dim 2) too
    w3 = np.exp(2j*np.pi/3); Xm = np.roll(np.eye(3), 1, axis=0); Zm = np.diag([w3**j for j in range(3)])
    PS = np.kron(Xm, Zm); G1 = (np.eye(9) + w3*(PS + PS@PS))/np.sqrt(3)
    Ts, out = ds_moves(G1, 3, 40)
    print('Gaussian: distinct non-scalar T with [T(x)T,R]=0:', len(Ts))
    for T, RT, res, cc in out[:6]:
        print('   R_T residual %.1e dimL(R_T)=%d %s' % (res, cc['dimL'], cc['label']))
    # positive control: ACC-generic family has DS partner(s)? and dim2 8-vertex check from 2609.38290: only diagonal T
    rng = np.random.default_rng(3)
    Rg = fam_generic(0.3+0.2j, 0.7-0.4j, 1.1+0.3j, 0)
    Ts, out = ds_moves(Rg, 3, 40)
    print('ACC generic family: nonscalar T found:', len(Ts), '(group contains the torus exp(t*h), h in L; random starts see a continuum)')
