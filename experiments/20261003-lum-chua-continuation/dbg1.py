import json, numpy as np
from pwl import *
from continuation import BASE, build
d = json.load(open("continuation.json"))
rows = d["aL_aR"]
rows.sort(key=lambda r: -r[1])
for key, n, amb, ys in rows[:6]:
    print(key, n, ["%.3g"%y for y in ys[:8]])
key, n, amb, ys = rows[0]
p = dict(BASE, aL=key[0], aR=key[1])
zR, zL = build(p)
r = count_cycles(zR, zL, n=3000, dmin=1e-5, dmax=400.0)
for x in r["roots"][:10]: print(x)
# smaller n counts
for key, n, amb, ys in rows[:6]:
    p = dict(BASE, aL=key[0], aR=key[1]); zR, zL = build(p)
    print(key, [count_cycles(zR,zL,n=m,dmin=1e-5,dmax=400.0)["n_sign_changes"] for m in (500,1500,3000,6000)])
# list of low-count aL_aR where n>=2
cnt2 = [(k,n) for k,n,a,y in d["aL_aR"] if 2<=n<=6]
print(len(cnt2), cnt2[:10])
