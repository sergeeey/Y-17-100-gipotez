"""Analyse a near-event point (from an ES run): where is the closest tangency / domain-end event, and does a
single-parameter line search push it across to give count>=4?  Serial, ~1-2 min.
usage: analyze_near.py <line_index_in_search3_runs.jsonl_of_an_es_run>"""

import sys, json, time, numpy as np
from pwl import *
from search import P0, zones, evaluate

runs = [json.loads(l) for l in open("search3_runs.jsonl")]
es = [r for r in runs if r["mode"] == "es"]
idx = int(sys.argv[1])
p = np.array(es[idx]["params"])
t0 = time.time()
zR, zL = zones(p)
print("params", [round(float(x), 6) for x in p])
print(
    "zone R: tr=%.5f det=%.5f w=%.5f   zone L: tr=%.5f det=%.5f w=%.5f"
    % (zR.A.trace(), np.linalg.det(zR.A), zR.w, zL.A.trace(), np.linalg.det(zL.A), zL.w)
)
print("a12_R=%.4g b1_R=%.4g ; a12_L=%.4g b1_L=%.4g" % (zR.a12, zR.b1, zL.a12, zL.b1))
yg = y_grid(zR, 6000, 1e-6, 400.0)
g = G(zR, zL, yg)
fin = np.isfinite(g)
# domain segments
segs = []
i = 0
while i < len(g):
    if not fin[i]:
        i += 1
        continue
    j = i
    while j + 1 < len(g) and fin[j + 1]:
        j += 1
    segs.append((i, j))
    i = j + 1
print(
    "n finite segments:",
    len(segs),
    [(round(float(yg[a]), 5), round(float(yg[b]), 5)) for a, b in segs][:8],
)
sc = [i for i in range(len(g) - 1) if fin[i] and fin[i + 1] and g[i] * g[i + 1] < 0]
print("sign changes (grid):", len(sc), [round(float(yg[i]), 6) for i in sc])
# local extrema not crossing zero
ev = []
for a, b in segs:
    seg = g[a : b + 1]
    for k in range(1, len(seg) - 1):
        if (seg[k] - seg[k - 1]) * (seg[k + 1] - seg[k]) <= 0:
            loc = np.max(np.abs(seg[max(0, k - 12) : k + 13])) + 1e-300
            ev.append((abs(seg[k]) / loc, float(yg[a + k]), float(seg[k])))
    ev.append((abs(seg[0]) / (np.max(np.abs(seg[:25])) + 1e-300), float(yg[a]), float(seg[0])))
    ev.append((abs(seg[-1]) / (np.max(np.abs(seg[-25:])) + 1e-300), float(yg[b]), float(seg[-1])))
ev.sort()
print("closest events (rel size, y0, g):")
for e in ev[:6]:
    print("   %.3e  y0=%.6f  g=%.3e" % e)
# line search over each parameter
print("line search (count at p_j*(1+d)+eps shifts):")
base_c, base_s = evaluate(p)
print("base count", base_c, "score", base_s)
best = (base_c, None)
for j in range(12):
    row = []
    for d in (-3e-2, -1e-2, -3e-3, -1e-3, -1e-4, -1e-5, 1e-5, 1e-4, 1e-3, 3e-3, 1e-2, 3e-2):
        q = p.copy()
        q[j] = q[j] + d * max(1.0, abs(p[j]))
        c, _ = evaluate(q, with_score=False)
        row.append(c)
        if c > best[0]:
            best = (c, (j, d))
    print("  p[%d]=%+.5f: %s" % (j, p[j], row), flush=True)
print("best from line search:", best, " wall", round(time.time() - t0, 1))
