"""Verify the explicit examples of arXiv:2604.26870 (Igonin) with the ddlax checker.
Equation numbers refer to the paper.  Transcribed from the arXiv HTML (LaTeX alt-text)."""

import json, sys
import sympy as sp

sys.path.insert(0, __file__.rsplit("src", 1)[0] + "src")
from ddlax import *

lam, c, q = sp.symbols("lam c q")
out = {}
Z = sp.Symbol


def v(fam, i):
    return mk(fam, i)


def report(name, R, kind="matrix", symbolic=True):
    """R: Matrix or dict of exprs. Records exact-symbolic zero (if rational) and numeric residual."""
    items = list(R.values()) if isinstance(R, dict) else list(R)
    num = max(num_resid(x, 4, 3) for x in items)
    sym = None
    if symbolic:
        try:
            sym = all(sym_simplify(x) == 0 for x in items)
        except Exception as ex:  # noqa
            sym = f"err:{ex}"
    ok = (num < 1e-40) and (sym in (True, None))
    out[name] = dict(symbolic_zero=sym, numeric_max=float(num), PASS=bool(ok))
    print(
        f"{name:70s} sym={sym!s:6s} num={float(num):.2e} -> {'PASS' if ok else 'FAIL'}", flush=True
    )
    return ok


u1_0, u1_1, u1_m1, u1_2 = v("u1", 0), v("u1", 1), v("u1", -1), v("u1", 2)
u2_0, u2_1, u2_m1, u2_2 = v("u2", 0), v("u2", 1), v("u2", -1), v("u2", 2)
al0, alm1, al1 = v("al", 0), v("al", -1), v("al", 1)

# ===================== (67) + MLR (68)
sys67 = System(
    {
        "u1": 2 * (u2_1 * u1_0**2 + al0 * u1_0 - u1_1),
        "u2": 2 * (u2_m1 - u1_m1 * u2_0**2 - alm1 * u2_0),
    }
)
M68 = sp.Matrix([[lam + al0 + u1_0 * u2_1, u1_0], [u2_1, 1]])
U68 = sp.Matrix([[-lam, -2 * u1_0], [-2 * u2_0, lam]])
report("(68) is MLR for (67)", sys67.mlr_residual(M68, U68))

# ===================== (72) + MLR (71)
sys72 = System(
    {
        "u1": 2 * (u2_0 * u1_0**2 + al0 * u1_0 - u1_1),
        "u2": 2 * (u2_m1 - u1_0 * u2_0**2 - al0 * u2_0),
    }
)
M71 = sp.Matrix([[lam + al0 + u1_0 * u2_0, u1_0], [u2_0, 1]])
U71 = sp.Matrix([[-lam, -2 * u1_0], [-2 * u2_m1, lam]])
report("(71) is MLR for (72)", sys72.mlr_residual(M71, U71))

# ===================== (85): equation, MLR (90,91), MT (89)/(88)
X = u1_1 * u2_0 * u1_0 + u1_1 - c * u1_0 - al0 * u1_0
D = u1_0 * u2_0 + 1
sys85 = System(
    {
        "u1": 2 * u2_m1 * u1_0**2 - 2 * c * u1_0 - 2 * X / D,
        "u2": 2 * u2_m1 - 2 * al0 * u2_0 - 2 * u2_0**2 * X / D,
    }
)
# MT (89): u^1 = X/D, u^2 = tilde u^2_{-1}   from (85) to (67)
Phi89 = {"u1": X / D, "u2": u2_m1}
res = miura_residual(sys85, Phi89, sys67)
report("(89) is MT from (85) to (67): component u1", {"u1": res["u1"]})
report("(89) is MT from (85) to (67): component u2", {"u2": res["u2"]})
# MLR (90),(91)
M90 = sp.Matrix([[lam + al0 + u2_0 * X / D, X / D], [u2_0, 1]])
U91 = sp.Matrix([[-lam, -2 * X / D], [-2 * u2_m1, lam]])
report("(90),(91) is MLR for (85)", sys85.mlr_residual(M90, U91))
# Lemma 4 route: substitute (89) into (68)/(71)-type MLR -> must give (90),(91) (cross-check of derivation)
# (71) with u1 -> X/D, u2 -> u2~_0  [u^2_0 = tilde u^2_{-1}?]  here (71) is for (72) where u2_0 = tilde u2_0
M71s = M71.xreplace({u1_0: X / D, u2_0: u2_0})
U71s = U71.xreplace({u1_0: X / D})
report("Lemma 4: (71)[u->Phi] equals printed (90),(91) (M part)", (M71s - M90))
report("Lemma 4: (71)[u->Phi] equals printed (90),(91) (U part)", (U71s - U91))

# ---- gauge (95) -> (96),(97)
G95 = sp.Matrix([[1 / (lam + alm1), -u1_0 / (lam + alm1)], [0, 1]])
Mh, Uh = gauge(M90, U91, G95, sys85)
M96 = sp.Matrix(
    [
        [
            (lam + alm1)
            * (u1_0 * u2_0 * lam + lam + al0 - c * u1_0 * u2_0)
            / ((lam + al0) * (u1_0 * u2_0 + 1)),
            (lam - c) * u1_0 / (lam + al0),
        ],
        [(lam + alm1) * u2_0, u1_0 * u2_0 + 1],
    ]
)
U97 = sp.Matrix(
    [
        [2 * u1_0 * u2_m1 - lam, 2 * (c - lam) * u1_0 / (lam + alm1)],
        [-2 * (lam + alm1) * u2_m1, lam - 2 * u1_0 * u2_m1],
    ]
)
report("gauge(95): computed S(G)MG^-1 equals printed (96)", Mh - M96)
report("gauge(95): computed DtG G^-1+GUG^-1 equals printed (97)", Uh - U97)
report("(96),(97) is MLR for (85)", sys85.mlr_residual(M96, U97))
print(
    "(96) depends on u_1? ->",
    any(parse(s) == ("u1", 1) or parse(s) == ("u2", 1) for s in M96.free_symbols),
    flush=True,
)
# ---- gauge diagonal -> (100)
Gd = sp.diag(lam + alm1, 1)
Mhh, Uhh = gauge(M96, U97, Gd, sys85)
M100 = sp.Matrix(
    [
        [(u1_0 * u2_0 * lam + lam + al0 - c * u1_0 * u2_0) / (u1_0 * u2_0 + 1), (lam - c) * u1_0],
        [u2_0, u1_0 * u2_0 + 1],
    ]
)
U100 = sp.Matrix(
    [[2 * u1_0 * u2_m1 - lam, 2 * (c - lam) * u1_0], [-2 * u2_m1, lam - 2 * u1_0 * u2_m1]]
)
report("diag gauge: computed equals printed (100) (M)", Mhh - M100)
report("diag gauge: computed equals printed (100) (U)", Uhh - U100)
report("(100) is MLR for (85)", sys85.mlr_residual(M100, U100))
# is (100) u-tame (depends only on u_0)?
print(
    "(100) u-tame:",
    all(
        parse(s) is None or parse(s)[1] == 0 or parse(s)[0] == "al" or parse(s)[1] == -1
        for s in M100.free_symbols
    ),
    flush=True,
)

# ===================== (113): MT (110) with sqrt formulas, both branches
v1_0, v1_1, v1_2 = v("v1", 0), v("v1", 1), v("v1", 2)
v2_0, v2_1, v2_m1 = v("v2", 0), v("v2", 1), v("v2", -1)
Xb = v2_0 * (v1_0 * (q - v1_1 * v2_0 - c) - 2 * v1_1) - c + q
Yb = 2 * v2_0 * (v1_1 * v2_0 + c - q)
rad = Xb**2 + 2 * (q * v1_0 + al0 * v1_0 - v1_1 * v2_0 * v1_0 - v1_1) * Yb
for sgn in (+1, -1):
    Phi1 = (Xb + sgn * sp.sqrt(rad)) / Yb
    # (107): v1_1 = [...](Phi) ; check Phi solves it
    t = Phi1
    rhs107 = ((t * v2_0 * q + q + al0 - c * t * v2_0) * v1_0 + (q - c) * t * (t * v2_0 + 1)) / (
        (t * v2_0 + 1) * (v2_0 * v1_0 + t * v2_0 + 1)
    )
    report(
        f"(107) satisfied by (108) branch {sgn:+d}",
        {"e": v1_1 - rhs107},
        kind="dict",
        symbolic=False,
    )
    # system (113): first comp (112), second comp H = F2(85)[tilde u -> Phi]
    S1 = S(Phi1)  # Phi at n+1 -> uses v1_1, v1_2 etc
    Phi_map = {"u1": Phi1, "u2": v2_0}
    F85_1, F85_2 = sys85.F["u1"], sys85.F["u2"]

    def sub85(Fi):
        rep = {}
        for s in Fi.free_symbols:
            p = parse(s)
            if p and p[0] in ("u1", "u2"):
                rep[s] = S(Phi_map[p[0]], p[1])
            # rename family u->v for tilde-tilde variables
        return Fi.xreplace(rep)

    # note: sys85 symbols are 'u1_*','u2_*' = tilde variables; Phi_map expressed in v-vars
    H = sub85(F85_2)
    F112 = 2 * v2_m1 * v1_0**2 - 2 * q * v1_0 + (4 * v2_m1 * v1_0 + 2 * (c - q)) * Phi1
    sys113 = System({"v1": F112, "v2": H})
    # MT (110): tilde u1 = Phi1, tilde u2 = v2_0, from (113) to (85); check (20)
    res = miura_residual(sys113, {"u1": Phi1, "u2": v2_0}, sys85)
    report(
        f"(110) is MT from (113) to (85) branch {sgn:+d}: u1",
        {"u1": res["u1"]},
        kind="dict",
        symbolic=False,
    )
    report(
        f"(110) is MT from (113) to (85) branch {sgn:+d}: u2",
        {"u2": res["u2"]},
        kind="dict",
        symbolic=False,
    )
    # MLR (100)[tilde u -> Phi] is MLR for (113)  (Lemma 4 / Remark 6), with lam free; c fixed, q->lam
    rep100 = lambda Mx: Mx.xreplace({u1_0: Phi1, u2_0: v2_0, u2_m1: v2_m1})
    M113, U113 = rep100(M100), rep100(U100)
    # (100) has lam; the MT used q for spectral parameter -> in Remark 6 lam stays free, but (110) was built at lam=q.
    M113q, U113q = M113.xreplace({lam: q}), U113.xreplace({lam: q})
    report(
        f"Remark 6 (100)[->Phi] MLR for (113) at lam=q branch {sgn:+d}",
        sys113.mlr_residual(M113q, U113q),
        symbolic=False,
    )
    out[f"branch{sgn}_note"] = "checked"

# ===================== (114) + (118,119), MT (115)->(116), Toda MLR (117), gauge (120), MT (126), (128)
sys114 = System({"u1": u1_0 * u2_0, "u2": u1_m1 / u1_0 - u1_0 / u1_1})
M118 = sp.Matrix([[lam - u2_1, u1_0 / u1_1], [-1, 0]])
U119 = sp.Matrix([[0, -u1_0 / u1_1], [1, lam - u2_0]])
report("(118),(119) is MLR for (114)", sys114.mlr_residual(M118, U119))
w1_0, w1_1, w1_m1 = v("w1", 0), v("w1", 1), v("w1", -1)
w2_0, w2_1 = v("w2", 0), v("w2", 1)
toda = System({"w1": w1_0 * (w2_0 - w2_1), "w2": w1_m1 - w1_0})
res = miura_residual(sys114, {"w1": u1_0 / u1_1, "w2": u2_0}, toda)
report("(115) is MT from (114) to Toda (116)", res, kind="dict")
M117 = sp.Matrix([[lam - w2_1, w1_0], [-1, 0]])
U117 = sp.Matrix([[0, -w1_0], [1, lam - w2_0]])
report("(117) is MLR for Toda (116)", toda.mlr_residual(M117, U117))
G3 = sp.Matrix([[0, -1], [u1_0, u1_0 * (lam - u2_0)]])
Mh, Uh = gauge(M118, U119, G3, sys114)
M120 = sp.Matrix([[lam - u2_0, 1 / u1_0], [-u1_0, 0]])
U120 = sp.Matrix([[0, -1 / u1_0], [u1_m1, lam]])
report("gauge G(3.2): computed equals printed (120) (M)", Mh - M120)
report("gauge G(3.2): computed equals printed (120) (U)", Uh - U120)
report("(120) is MLR for (114)", sys114.mlr_residual(M120, U120))
# (128) and MT (126)  [tilde variables = family 'v']
t1_0, t1_1, t1_m1 = v("t1", 0), v("t1", 1), v("t1", -1)
t2_0, t2_1, t2_m1 = v("t2", 0), v("t2", 1), v("t2", -1)
sys128 = System({"t1": t1_0 * t2_0 / t2_1, "t2": t2_0 * (c * t1_m1 - t1_0) / t1_m1})
Phi126 = {"u1": -t2_1 / t1_0, "u2": (c * t1_0 * t2_1 - t1_0 * t2_0 - t1_1 * t2_1) / (t1_0 * t2_1)}
res = miura_residual(sys128, {"u1": Phi126["u1"], "u2": Phi126["u2"]}, sys114)
# sys128 uses fams t1,t2 ; miura_residual's tilde_sys.Dt uses tilde_sys.F keys -> good
report("(126) is MT from (128) to (114): u1", {"u1": res["u1"]}, kind="dict")
report("(126) is MT from (128) to (114): u2", {"u2": res["u2"]}, kind="dict")
# Remark 7: (120)[u -> Phi126] is MLR for (128)
rep = {u1_0: Phi126["u1"], u2_0: Phi126["u2"], u1_m1: S(Phi126["u1"], -1)}
M128, U128 = M120.xreplace(rep), U120.xreplace(rep)
# note (120) uses lam; MT uses lam=c
M128c, U128c = M128.xreplace({lam: c}), U128.xreplace({lam: c})
report("Remark 7: (120)[->Phi126] MLR for (128) at lam=c", sys128.mlr_residual(M128c, U128c))
report(
    "Remark 7: same with free lam (NOT claimed by paper; informational)",
    sys128.mlr_residual(M128, U128),
)

json.dump(
    out, open(__file__.rsplit("src", 1)[0] + "verify_paper_result.json", "w"), indent=1, default=str
)
print(
    "DONE; any FAIL:",
    [k for k, vv in out.items() if isinstance(vv, dict) and not vv.get("PASS", True)],
)
