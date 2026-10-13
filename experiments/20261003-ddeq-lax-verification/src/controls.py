"""Positive + negative controls for the zero-curvature checker (ddlax.py)."""

import itertools, json, sys
import sympy as sp

sys.path.insert(0, __file__.rsplit("src", 1)[0] + "src")
from ddlax import *

lam = sp.Symbol("lam")
out = {}


def show(name, R, expect_zero):
    sym0 = mat_sym_zero(R)
    num = mat_num_resid(R)
    ok = sym0 == expect_zero
    out[name] = dict(
        symbolic_zero=bool(sym0), numeric_max=float(num), expected_zero=expect_zero, ok=ok
    )
    print(
        f"{name:55s} sym_zero={sym0!s:5s} num={float(num):.3e} expected_zero={expect_zero} -> {'OK' if ok else 'CONTROL FAILURE'}",
        flush=True,
    )


# ---------- Positive control A: Toda, Flaschka-Manakov coordinates (paper eq (116),(117), textbook Lax pair)
w1, w1m, w10, w11 = [sp.Symbol(n) for n in ("w1_0", "w1_m1", "w1_0", "w1_1")]
w1_0, w1_1, w1_m1 = sp.symbols("w1_0 w1_1 w1_m1")
w2_0, w2_1, w2_m1 = sp.symbols("w2_0 w2_1 w2_m1")
toda = System({"w1": w1_0 * (w2_0 - w2_1), "w2": w1_m1 - w1_0})
M = sp.Matrix([[lam - w2_1, w1_0], [-1, 0]])
U = sp.Matrix([[0, -w1_0], [1, lam - w2_0]])
show("POS Toda (116) with MLR (117)", toda.mlr_residual(M, U), True)
# negative controls (perturbed Lax matrices / equation)
show(
    "NEG Toda: M12 w1_0 -> w1_1",
    toda.mlr_residual(sp.Matrix([[lam - w2_1, w1_1], [-1, 0]]), U),
    False,
)
show(
    "NEG Toda: M11 w2_1 -> w2_0",
    toda.mlr_residual(sp.Matrix([[lam - w2_0, w1_0], [-1, 0]]), U),
    False,
)
show(
    "NEG Toda: U22 w2_0 -> w2_1",
    toda.mlr_residual(M, sp.Matrix([[0, -w1_0], [1, lam - w2_1]])),
    False,
)
show("NEG Toda: U21 1 -> 2", toda.mlr_residual(M, sp.Matrix([[0, -w1_0], [2, lam - w2_0]])), False)
toda_bad = System({"w1": w1_0 * (w2_0 - w2_1), "w2": w1_m1 - w1_0 + w1_0 * w2_0})
show("NEG Toda: perturbed equation F2 += w1_0*w2_0", toda_bad.mlr_residual(M, U), False)
# gauge-covariance sanity: random gauge of a valid MLR stays valid
G = sp.Matrix([[1 + w1_0 * w2_0, w2_0], [w1_0, 3]])
Mg, Ug = gauge(M, U, G, toda)
show("POS gauge-transformed Toda MLR (random G, eq (12))", toda.mlr_residual(Mg, Ug), True)

# ---------- Positive control B: Volterra u_t = u_0(u_1-u_{-1}); Lax pair FOUND by linear algebra (independent of paper)
u0, u1, um1, um2, u2 = sp.symbols("u_0 u_1 u_m1 u_m2 u_2")
vol = System({"u": u0 * (u1 - um1)})
Mv = sp.Matrix([[lam, u0], [-1, 0]])
cs = []


def poly(name):
    # polynomial ansatz: degree <=2 in lam, linear in u_{-1},u_0,u_1, plus constant
    terms = []
    for i in range(3):
        for mon in (1, um1, u0, u1, um1 * u0, u0 * u1, um1 * u1):
            c = sp.Symbol(f"{name}_{i}_{len(cs)}")
            cs.append(c)
            terms.append(c * lam**i * mon)
    return sum(terms)


Uv = sp.Matrix([[poly("a"), poly("b")], [poly("c"), poly("d")]])
Rv = vol.mlr_residual(Mv, Uv)
eqs = []
for e in Rv:
    P = sp.Poly(sp.expand(e), lam, u0, u1, um1, u2, um2)
    eqs += P.coeffs()
sol = sp.solve(eqs, cs, dict=True)
if sol:
    Uv_s = Uv.subs(sol[0])
    free = [c for c in cs if c in Uv_s.free_symbols]
    Uv_s = Uv_s.subs({c: 0 for c in free})  # set free (gauge-like) parameters to 0
    print("Volterra U found:", Uv_s, flush=True)
    out["volterra_U"] = str(Uv_s)
    show("POS Volterra with solver-found Lax pair", vol.mlr_residual(Mv, Uv_s), True)
    show(
        "NEG Volterra: M12 u_0 -> u_1",
        vol.mlr_residual(sp.Matrix([[lam, u1], [-1, 0]]), Uv_s),
        False,
    )
    show(
        "NEG Volterra: U entry perturbed",
        vol.mlr_residual(Mv, Uv_s + sp.Matrix([[0, 0], [0, u0]])),
        False,
    )
else:
    print(
        "Volterra: no U in ansatz for M=[[lam,u0],[-1,0]] (candidate M wrong or ansatz too small)",
        flush=True,
    )
    out["volterra_U"] = "none found"

bad = [k for k, v in out.items() if isinstance(v, dict) and not v["ok"]]
out["controls_valid"] = len(bad) == 0
json.dump(out, open(__file__.rsplit("src", 1)[0] + "controls_result.json", "w"), indent=1)
print("CONTROLS VALID" if not bad else f"CONTROL FAILURES: {bad}")
