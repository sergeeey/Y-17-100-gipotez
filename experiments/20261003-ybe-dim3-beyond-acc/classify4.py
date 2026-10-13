"""Cluster converged dim-3 solutions (npz from run_serial.py) by conjugation-invariant signature.
usage: classify4.py out.json file1.npz [file2.npz ...]
verdict: distinct & dimL==2 -> ACC-equivalent ; distinct & dimL>=3 -> SCC-or-more ; U1-free/degenerate -> BEYOND-ACC candidate."""
import sys, json, collections
import numpy as np
from ybe import *
from classify3 import analyse, clean

out = sys.argv[1]
rows, Rs = [], []
for f in sys.argv[2:]:
    d = np.load(f, allow_pickle=True)
    for i, R in enumerate(d["R"]):
        a = analyse(R)
        if a["res"] > 1e-10 or a["cond"] > 1e6:
            continue
        Rn = clean(R)
        td, _ = tangent_dim(Rn, 3)
        a["tangent"] = int(td)
        a["file"], a["idx"], a["seed"], a["mode"] = f, i, int(d["seed"][i]), str(d["mode"][i])
        if a["label"] == "distinct":
            a["verdict"] = "ACC" if a["dimL"] == 2 else "SCC+"
        else:
            a["verdict"] = "BEYOND-ACC-candidate"
        rows.append(a)
        Rs.append(Rn)
print("good solutions (res<1e-10, cond<1e6):", len(rows))
print("verdicts:", dict(collections.Counter(r["verdict"] for r in rows)))
grp = collections.defaultdict(list)
for r in rows:
    grp[(r["verdict"], r["label"], r["dimL"], r["ltype"], r["mults"], r["geom"], r["monomial"], r["rank"], r["tangent"])].append(r)
for k, v in sorted(grp.items(), key=lambda t: (t[0][0] != "BEYOND-ACC-candidate", -len(t[1]))):
    print(len(v), k, "| e.g.", v[0]["file"], v[0]["idx"])
json.dump(rows, open(out, "w"), default=str)
np.save(out.replace(".json", "_R.npy"), np.array(Rs))
