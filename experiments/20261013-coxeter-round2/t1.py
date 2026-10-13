import time
from exact3 import *
cases = {
 "PA": "0-1:inf 0-6:4 1-5:4 2-3:4 2-6:6 3-4:4 4-5:6",
 "PB": "0-1:inf 0-6:4 1-5:4 2-3:4 2-6:6 3-4:4 3-5:3 3-6:3 4-5:6",
 "ctrl_simplex_H4like_3d [3,3,6]?": "0-1:3 1-2:3 2-3:6",
}
for k,s in cases.items():
    n = 1+max(max(a) for a in parse_edges(s))
    t=time.time()
    v = validate(n, parse_edges(s))
    print(k, {a:b for a,b in v.items() if not a.startswith('_')}, round(time.time()-t,1),'s')
    print("   vinberg_exact", vinberg_exact(n, parse_edges(s)))
