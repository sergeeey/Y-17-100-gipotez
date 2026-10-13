"""Q-A: compare cand88/cand101 with the monomial shift family (H-CYBE-002), in braid form.
Controls P1 (form conversion), P2 (conjugation invariance), N1 (comparison can return both answers)."""
import sys, json, numpy as np, sympy as sp
R1 = "E:/Проверка Гипотез/работаю над проверкой гипотез/Y-17 100 gipotez/experiments/20261003-ybe-dim3-beyond-acc"
sys.path.insert(0, R1)
from ybe import braid_residual, ybe_residual_R, flip, L_algebra
N = 3
P = flip(3)
d = np.load(R1 + '/d3_w001.npz', allow_pickle=True)
def clean(R):  # same as round-1 'clean' semantic: just zero tiny entries
    R = R.copy(); R[abs(R) < 1e-13] = 0; return R
cands = {88: d['R'][88], 101: d['R'][101]}
def shiftR(A, B, C, D, E):
    w = [[A*E/D, C, A*E/B], [A, B, C], [C, D, E]]
    R = np.zeros((9, 9), dtype=object)
    for i in range(3):
        for j in range(3):
            R[3*((i+1) % 3) + (j-1) % 3, 3*i + j] = w[i][j]
    return R
# P1: exact check, vertex and braid form, witness and random rationals
import random
random.seed(1)
def exact_res(M, form):
    M = sp.Matrix(M.tolist()) if isinstance(M, np.ndarray) else M
    I3 = sp.eye(3)
    if form == 'braid':
        A = sp.kronecker_product(M, I3); B = sp.kronecker_product(I3, M)
        return (A*B*A - B*A*B).applyfunc(sp.nsimplify)
    P23 = sp.zeros(27, 27)
    for i in range(3):
        for j in range(3):
            for k in range(3):
                P23[9*i+3*k+j, 9*i+3*j+k] = 1
    R12 = sp.kronecker_product(M, I3); R23 = sp.kronecker_product(I3, M); R13 = P23*R12*P23
    return R12*R13*R23 - R23*R13*R12
Pq = sp.Matrix(9, 9, lambda a, b: 1 if (a == 3*(b % 3) + b//3) else 0)
out = {}
for params in [(2, 3, 5, 7, 11)] + [tuple(sp.Rational(random.randint(1, 9), random.randint(1, 9)) for _ in range(5)) for _ in range(3)]:
    Rv = sp.Matrix(shiftR(*[sp.Integer(x) if not isinstance(x, sp.Rational) else x for x in params]).tolist())
    rv = exact_res(Rv, 'vertex'); rb = exact_res(Pq*Rv, 'braid')
    print('P1 params', params, 'vertex nnz', sum(1 for x in rv if x != 0), 'braid(P*Rv) nnz', sum(1 for x in rb if x != 0), flush=True)
    out[str(params)] = [sum(1 for x in rv if x != 0), sum(1 for x in rb if x != 0)]
# symbolic spectrum of the braid form of the shift family
A, B, C, D, E = sp.symbols('A B C D E', positive=True)
Rv = sp.Matrix(shiftR(A, B, C, D, E).tolist())
Rb = Pq * Rv
x = sp.symbols('x')
cp = sp.factor(Rb.charpoly(x).as_expr())
print('braid-form charpoly of shift family:', cp)
print('Rb^2 diagonal?', (Rb*Rb).is_diagonal())
out['charpoly'] = str(cp)
# candidates: spectrum multiplicities
def spec_mult(M, tol=1e-6):
    ev = np.linalg.eigvals(M); cl = []
    for e in ev:
        for c in cl:
            if abs(c[0]-e) < tol*max(1, abs(e)): c[1] += 1; break
        else: cl.append([e, 1])
    return sorted([(np.round(c[0], 5), c[1]) for c in cl], key=lambda t: -t[1])
for k, R in cands.items():
    R = clean(R)
    print('cand', k, 'braid res', np.linalg.norm(braid_residual(R, 3))/np.linalg.norm(R)**3, 'spectrum', spec_mult(R))
    Rn = R @ np.linalg.inv(R) # dummy
    # P2: conjugation invariance
    rng = np.random.default_rng(3)
    g = rng.normal(size=(3, 3)) + 1j*rng.normal(size=(3, 3)); G = np.kron(g, g)
    Rc = G @ R @ np.linalg.inv(G)
    print('  P2: conj-spectrum', spec_mult(Rc), 'res', np.linalg.norm(braid_residual(Rc, 3))/np.linalg.norm(Rc)**3)
    lam = [c for c in spec_mult(R)]
    # Hecke check (R-lam)(R-mu)=0
    ev = [c[0] for c in lam]
    if len(ev) == 2:
        H = (R - ev[0]*np.eye(9)) @ (R - ev[1]*np.eye(9))
        print('  Hecke relation residual', np.abs(H).max())
# witness numeric spectrum
Rw = np.array((P @ shiftR(2., 3., 5., 7., 11.).astype(float)))
print('shift witness braid res', np.linalg.norm(braid_residual(Rw, 3))/np.linalg.norm(Rw)**3, 'spectrum', spec_mult(Rw))
# N1: a deliberately built 2-eigenvalue Hecke braid solution of the same shape: R = c*Id has 1 eigenvalue; flip P has (6,3) -> comparison routine distinguishes
print('N1: flip spectrum', spec_mult(P), ' Id spectrum', spec_mult(np.eye(9)))
json.dump(out, open('s01_out.json', 'w'), indent=1)
