import sys
import sympy as sp

sys.path.insert(0, __file__.rsplit("src", 1)[0] + "src")
from ddlax import *

c = sp.Symbol("c")
v = mk
u1_0, u1_1, u1_m1 = v("u1", 0), v("u1", 1), v("u1", -1)
u2_0, u2_1, u2_m1 = v("u2", 0), v("u2", 1), v("u2", -1)
al0, alm1 = v("al", 0), v("al", -1)
X = u1_1 * u2_0 * u1_0 + u1_1 - c * u1_0 - al0 * u1_0
D = u1_0 * u2_0 + 1
sys85 = System(
    {
        "u1": 2 * u2_m1 * u1_0**2 - 2 * c * u1_0 - 2 * X / D,
        "u2": 2 * u2_m1 - 2 * al0 * u2_0 - 2 * u2_0**2 * X / D,
    }
)
sys67 = System(
    {
        "u1": 2 * (u2_1 * u1_0**2 + al0 * u1_0 - u1_1),
        "u2": 2 * (u2_m1 - u1_m1 * u2_0**2 - alm1 * u2_0),
    }
)
sys72 = System(
    {
        "u1": 2 * (u2_0 * u1_0**2 + al0 * u1_0 - u1_1),
        "u2": 2 * (u2_m1 - u1_0 * u2_0**2 - al0 * u2_0),
    }
)
r82 = miura_residual(sys85, {"u1": X / D, "u2": u2_0}, sys72)
print("(82) 85->72:", {k: sym_simplify(x) for k, x in r82.items()}, flush=True)
r89 = miura_residual(sys85, {"u1": X / D, "u2": u2_m1}, sys67)
print("(89) 85->67:", {k: sym_simplify(x) for k, x in r89.items()}, flush=True)
# the 'u1' residual in the original (82) check: which eq is nonzero?
# also test: original (67) vs its MLR (68) -> passes; relabel (67)->(72) explicitly
