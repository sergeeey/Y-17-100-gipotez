# WHY: check conditioning of exact rref kernel bases (SDP inaccuracy suspect).
import pickle, numpy as np
from fractions import Fraction
D = pickle.load(open("../logs/exact_bases.pkl", "rb"))
mins, maxs, conds = [], [], []
for bj in D["bases_exact"]:
    Bm = np.array([[complex(float(Fraction(v[r][0])), float(Fraction(v[r][1]))) for r in range(20)] for v in bj]).T
    nrm = np.linalg.norm(Bm, axis=0)
    mins.append(nrm.min()); maxs.append(nrm.max()); conds.append(np.linalg.cond(Bm))
print("column norm min over points:", min(mins), " max:", max(maxs))
print("cond(B) min/median/max:", min(conds), float(np.median(conds)), max(conds))
