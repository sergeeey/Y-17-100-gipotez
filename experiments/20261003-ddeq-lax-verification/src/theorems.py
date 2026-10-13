"""Instance checks of Theorems 1-3 of arXiv:2604.26870 on the paper's MLRs + a deliberately fake MLR."""

import json, sys
import sympy as sp

sys.path.insert(0, __file__.rsplit("src", 1)[0] + "src")
from ddlax import *

lam, c = sp.symbols("lam c")
v = mk
u1_0, u1_1, u1_m1 = v("u1", 0), v("u1", 1), v("u1", -1)
u2_0, u2_1, u2_m1 = v("u2", 0), v("u2", 1), v("u2", -1)
al0, alm1 = v("al", 0), v("al", -1)
out = {}


def rec(name, ok, info=""):
    out[name] = dict(PASS=bool(ok), info=str(info))
    print(f"{name:75s} {'PASS' if ok else 'FAIL'} {info}", flush=True)


def is0(Mx):
    return mat_num_resid(Mx, 3, 5) < 1e-40  # exact-rational random points, mp.dps=60


# ---------- Theorem 3 (fake criterion) ----------
# non-fake candidates: Toda MLR (117) in w-vars; MLR (118) for (114); (100) for (85); (68)
w1_0, w1_1, w2_0, w2_1 = v("u1", 0), v("u1", 1), v("u2", 0), v("u2", 1)
M117 = sp.Matrix([[lam - u2_1, u1_0], [-1, 0]])  # Toda, w=(u1,u2)
M118 = sp.Matrix([[lam - u2_1, u1_0 / u1_1], [-1, 0]])
X = u1_1 * u2_0 * u1_0 + u1_1 - c * u1_0 - al0 * u1_0
D = u1_0 * u2_0 + 1
M90 = sp.Matrix([[lam + al0 + u2_0 * X / D, X / D], [u2_0, 1]])
M100 = sp.Matrix(
    [[(u1_0 * u2_0 * lam + lam + al0 - c * u1_0 * u2_0) / D, (lam - c) * u1_0], [u2_0, D]]
)
M68 = sp.Matrix([[lam + al0 + u1_0 * u2_1, u1_0], [u2_1, 1]])
M120 = sp.Matrix([[lam - u2_0, 1 / u1_0], [-u1_0, 0]])
for name, Mx in [
    ("Toda (117)", M117),
    ("(118)", M118),
    ("(90)", M90),
    ("(100)", M100),
    ("(68)", M68),
    ("(120)", M120),
]:
    ds = [sym_simplify_m for sym_simplify_m in []]
    nz = []
    for fam in ("u1", "u2"):
        Dl = Delta(Mx, fam)
        nz.append(not is0(Dl))
    rec(
        f"Thm3: Delta != 0 for some j (=> NOT fake) : {name}",
        any(nz),
        f"nonzero per component u1,u2 = {nz}",
    )

# deliberately FAKE MLR: gauge of a trivial MLR M0(n) (constants), U0 = 0 -> must give Delta == 0 for all j
M0 = sp.Matrix([[lam, 1], [0, 1]])
Gs = [
    sp.Matrix([[1 + u1_0 * u2_0, u2_1], [u1_0, 3 + u1_m1]]),
    sp.Matrix([[u1_0, 1], [1, u2_0 + u1_1]]),
]
for k, G in enumerate(Gs):
    Mf = S(G) * M0 * G.inv()
    ok = all(is0(Delta(Mf, fam)) for fam in ("u1", "u2"))
    rec(f"Thm3: Delta == 0 for deliberately FAKE MLR S(G)M0G^-1 (G#{k})", ok)
    # Thm 2 covariance: Delta(S(G) M G^-1) = S(G) Delta(M) S(G)^-1 for non-fake M too
for k, G in enumerate(Gs):
    for name, Mx in [("(118)", M118), ("(100)", M100)]:
        Mt = S(G) * Mx * G.inv()
        okc = True
        for fam in ("u1", "u2"):
            lhs = Delta(Mt, fam)
            rhs = S(G) * Delta(Mx, fam) * S(G).inv()
            okc = okc and is0(lhs - rhs)
        rec(f"Thm2 covariance Delta(M~)=S(G)Delta(M)S(G)^-1 : M={name}, G#{k}", okc)
# negative control for Thm2 check: a WRONG covariance formula (no S on conjugator) must fail
G = Gs[0]
Mt = S(G) * M118 * G.inv()
bad = is0(Delta(Mt, "u1") - G * Delta(M118, "u1") * G.inv())
rec("Thm2 NEG control: wrong covariance formula (G instead of S(G)) must FAIL", not bad)


# ---------- Theorem 1 condition (27), p=1:  d_{u^i_0}( d_{u^j_1}(M) M^-1 ) = 0 ----------
def cond27(Mx, p=1):
    ok = True
    for i in ("u1", "u2"):
        for j in ("u1", "u2"):
            sj = mk(j, p)
            si = mk(i, 0)
            Q = Mx.diff(sj) * Mx.inv()
            ok = ok and is0(Q.diff(si))
    return ok


rec("Thm1 cond (27) p=1 holds for (90) [paper says it does]", cond27(M90))
rec("Thm1 cond (27) p=1 holds for (118) [paper says it does]", cond27(M118))
# Theorem 1 positive: cond holds -> explicit gauge G = S^-1(M(n,a0,u1)^-1) removes u_1 (p=1). Check on (118) numerically-symbolically:
a1, a2 = sp.Symbol("a1"), sp.Symbol("a2")
Ma = M118.xreplace({u1_0: a1, u2_0: a2})  # u_0 -> constant a_0 (paper eq (28))
Gt = S(Ma.inv(), -1)
Mh = S(Gt) * M118 * Gt.inv()
rec(
    "Thm1 (28): gauge G=S^-1(M(a0,u1)^-1) applied to (118) leaves no u_1-dependence",
    all(parse(s) is None or parse(s)[1] != 1 for s in sp.simplify(Mh).free_symbols),
    f"free symbols {sorted(map(str, sp.simplify(Mh).free_symbols))}",
)
# Thm1 negative: a matrix violating (27) : M = [[lam, u1_0*u1_1],[1, u1_1]] -> d_{u0}(dM/du_1 M^-1) !=0 expected
Mv = sp.Matrix([[lam, u1_0 * u1_1], [1, u1_1 + u2_0]])
rec("Thm1 NEG control: cond (27) FAILS for a matrix with entangled u_0,u_1", not cond27(Mv))
json.dump(out, open(__file__.rsplit("src", 1)[0] + "theorems_result.json", "w"), indent=1)
print("DONE; FAIL:", [k for k, vv in out.items() if not vv["PASS"]])
