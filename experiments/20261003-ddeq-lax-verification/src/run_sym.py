import json, sys
import sympy as sp

sys.path.insert(0, __file__.rsplit("src", 1)[0] + "src")
from ddlax import mk
from symmetry import run

which = sys.argv[1]
v = mk
results = {}

if which in ("toda", "toda_bad"):
    w1_0, w1_m1, w2_0, w2_1 = v("w1", 0), v("w1", -1), v("w2", 0), v("w2", 1)
    F = {"w1": w1_0 * (w2_0 - w2_1), "w2": w1_m1 - w1_0}
    if which == "toda_bad":
        F = {
            "w1": w1_0 * (w2_0 - w2_1) + w2_0**3,
            "w2": w1_m1 - w1_0,
        }  # homogeneous (w1:2,w2:1) non-Toda perturbation
    # weights w1=2,w2=1 ; F1 weight 3, F2 weight 2 ; first higher flow: weight +1
    res, sols, basis = run(
        which, F, ["w1", "w2"], -2, 2, {"w1": 2, "w2": 1}, {"w1": 4, "w2": 3}, maxdeg=4
    )
    # also the base flow itself F (weights 3,2) must be in nullspace (sanity: positive control of solver)
    res0, sols0, _ = run(
        which + "_baseweight",
        F,
        ["w1", "w2"],
        -2,
        2,
        {"w1": 2, "w2": 1},
        {"w1": 3, "w2": 2},
        maxdeg=3,
    )
    results = dict(higher=res, base=res0)

elif which in ("kn", "kn_bad", "kn0"):
    al = sp.Rational(3, 2) if which != "kn0" else 0
    u1_0, u1_1, u2_0, u2_m1 = v("u1", 0), v("u1", 1), v("u2", 0), v("u2", -1)
    F = {
        "u1": 2 * (u2_0 * u1_0**2 + al * u1_0 - u1_1),
        "u2": 2 * (u2_m1 - u1_0 * u2_0**2 - al * u2_0),
    }  # eq (72) with alpha = const
    if which == "kn_bad":
        F["u1"] = F["u1"] + u1_0**3 * u2_0**2  # quintic perturbation, same charge
    # charge: u1:+1, u2:-1 ; G^1 charge +1, G^2 charge -1 ; degree <= 5
    res, sols, basis = run(
        which, F, ["u1", "u2"], -2, 2, {"u1": 1, "u2": -1}, {"u1": 1, "u2": -1}, maxdeg=5
    )
    results = dict(higher=res)

json.dump(
    results,
    open(__file__.rsplit("src", 1)[0] + f"symmetry_{which}.json", "w"),
    indent=1,
    default=str,
)
print("SAVED", which, flush=True)
