"""Q-B: generic-start sampler for the constant braid YBE with R = expm(X) (always invertible, no collapse to R=0),
holomorphic Levenberg-Marquardt. usage: s09_sampler.py N nstarts scale seed maxit outfile"""
import sys, time, numpy as np
from scipy.linalg import expm, expm_frechet
R1 = "E:/Проверка Гипотез/работаю над проверкой гипотез/Y-17 100 gipotez/experiments/20261003-ybe-dim3-beyond-acc"
sys.path.insert(0, R1)
from ybe import braid_residual, jac_F, L_algebra, hiet_families, flip

def solve(N, X0, maxit=300, tol=1e-12):
    n2 = N*N; X = X0 - np.trace(X0)/n2*np.eye(n2); mu = 1e-2
    Pj = np.eye(n2*n2) - np.outer(np.eye(n2).reshape(-1), np.eye(n2).reshape(-1))/n2
    def res(X):
        R = expm(X); return R, braid_residual(R, N).reshape(-1)
    R, F = res(X); f = np.linalg.norm(F)
    for it in range(maxit):
        if f/np.linalg.norm(R)**3 < tol: return X, R, f/np.linalg.norm(R)**3, it, True
        J1 = jac_F(R, N)                               # (N^6, N^4)
        D = np.empty((n2*n2, n2*n2), complex)
        for k in range(n2*n2):
            E = np.zeros((n2, n2), complex); E[k//n2, k % n2] = 1
            D[:, k] = expm_frechet(X, E, compute_expm=False).reshape(-1)
        J = (J1 @ D) @ Pj
        g = J.conj().T @ F; H = J.conj().T @ J
        ok = False
        for _ in range(12):
            try: dX = np.linalg.solve(H + mu*np.eye(len(H)), -g)
            except np.linalg.LinAlgError: mu *= 10; continue
            Xn = X + (Pj @ dX).reshape(n2, n2)
            if np.abs(Xn).max() > 60: mu *= 10; continue
            Rn, Fn = res(Xn); fn = np.linalg.norm(Fn)
            if fn < f: X, R, F, f = Xn, Rn, Fn, fn; mu = max(mu/3, 1e-12); ok = True; break
            mu *= 4
        if not ok: break
    return X, R, f/np.linalg.norm(R)**3, it, f/np.linalg.norm(R)**3 < tol

def spec_geom(R, N, tol=1e-5):
    ev = np.linalg.eigvals(R); cl = []
    for e in ev:
        for c in cl:
            if abs(c[0]-e) < tol*max(1, abs(e)): c[1] += 1; break
        else: cl.append([e, 1])
    out = []
    for lam, alg in cl:
        s = np.linalg.svd(R - lam*np.eye(N*N), compute_uv=False)
        geo = int((s < 1e-5*max(1, s[0])).sum())
        out.append((alg, geo))
    return tuple(sorted(out, reverse=True))

if __name__ == '__main__':
    N = int(sys.argv[1]); ns = int(sys.argv[2]); scale = float(sys.argv[3]); seed = int(sys.argv[4]); maxit = int(sys.argv[5]); outf = sys.argv[6]
    rng = np.random.default_rng(seed); rows = []; Rs = []; t0 = time.time()
    for s in range(ns):
        X0 = scale*(rng.normal(size=(N*N, N*N)) + 1j*rng.normal(size=(N*N, N*N)))/np.sqrt(2)*0 if False else scale*(rng.normal(size=(N, N)) + 1j*rng.normal(size=(N, N)))/np.sqrt(2)
        X, R, f, it, ok = solve(N, X0 if X0.shape == (N, N) else None, maxit) if False else (None,)*5
        break
    # R = expm(X) with X an N^2 x N^2 matrix
    n2 = N*N
    for s in range(ns):
        X0 = scale*(rng.normal(size=(n2, n2)) + 1j*rng.normal(size=(n2, n2)))/np.sqrt(2)
        X, R, f, it, ok = solve(N, X0, maxit)
        if ok:
            Rn = R/np.abs(np.linalg.det(R))**(1.0/n2)
            dL, sv = L_algebra(Rn, N, tol=1e-8)
            sg = spec_geom(Rn, N)
            rows.append((s, len(dL), sg)); Rs.append(R)
        if (s+1) % 10 == 0: print('start', s+1, 'converged', len(rows), 'time %.0fs' % (time.time()-t0), flush=True)
    np.savez(outf, R=np.array(Rs) if Rs else np.zeros((0, n2, n2)), info=np.array([str(r) for r in rows]))
    import collections
    c = collections.Counter((r[1], r[2]) for r in rows)
    print('N', N, 'starts', ns, 'scale', scale, 'converged', len(rows))
    for k, v in c.most_common(): print(v, 'dimL=%d' % k[0], 'spec(alg,geo)=', k[1])
    if N == 2:
        fam = hiet_families(np.random.default_rng(5)); fam['Id'] = np.eye(4, dtype=complex)
        for nm, F in fam.items():
            Fn = F/abs(np.linalg.det(F))**0.25
            dL, _ = L_algebra(Fn, 2, tol=1e-8)
            print('  ref', nm, 'dimL=%d' % len(dL), spec_geom(Fn, 2), ' hit count', sum(v for k, v in c.items() if k == (len(dL), spec_geom(Fn, 2))))
