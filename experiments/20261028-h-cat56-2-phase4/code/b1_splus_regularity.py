"""Stage B check 1: does the S+ POVM have any zero-probability outcome at rho (A0)?
If every outcome has p_k(theta0) > 0, the point, limit and Hellinger CFIM coincide for ANY smooth family
with the given first-order data (F^C is continuous where all p_k > 0).
Usage: python -I b1_splus_regularity.py <instance.jsonl> <povm.npz> <out.json>
"""
import json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OLD = os.path.normpath(os.path.join(HERE, "..", "..", "20261027-h-cat56-2-discovery", "code"))
sys.path.insert(0, OLD)
import s8_admissible_span as sa  # noqa: E402

path, npz, out = sys.argv[1:4]
As = sa.load_A(path)
z = np.load(npz, allow_pickle=True)
w, V = z["weights"], z["vectors"]
Q = np.diag([1 / 3, 2 / 3])
E_tot = sum(wk * np.outer(v, v.conj()) for wk, v in zip(w, V))
p = np.array([wk * np.real(v[:2].conj() @ Q @ v[:2]) for wk, v in zip(w, V)])
xn = np.array([np.linalg.norm(v[:2]) / np.linalg.norm(v) for v in V])
res = {
    "n_outcomes": int(len(w)),
    "completeness_err": float(np.linalg.norm(E_tot - np.eye(22))),
    "min_p": float(p.min()), "max_p": float(p.max()), "sum_p": float(p.sum()),
    "n_p_below_1e-12": int((p < 1e-12).sum()),
    "min_support_share": float(xn.min()), "median_support_share": float(np.median(xn)),
    "rank_one": True,
}
# smallest relative p (p / weight)
res["min_p_over_weight"] = float((p / w).min())
json.dump(res, open(out, "w"), indent=1)
print(json.dumps(res, indent=1))
