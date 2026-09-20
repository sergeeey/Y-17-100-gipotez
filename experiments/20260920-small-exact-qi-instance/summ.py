# ruff: noqa
import json, glob, collections
rows = [json.loads(l) for f in glob.glob("aprime_part*.jsonl") for l in open(f, encoding="utf-8")]
print("runs", len(rows), "built", sum(r["built"] for r in rows))
cell = collections.defaultdict(list)
for r in rows:
    cell[(r["m"], r["c"])].append(r)
for k in sorted(cell):
    rs = cell[k]
    b = [r for r in rs if r["built"]]
    dv = [r["dimV_float"] for r in b]
    print(k, "n", len(rs), "built", len(b), "maxdimV", max(dv) if dv else None, "median", sorted(dv)[len(dv)//2] if dv else None, "maxbits<=", max((r["max_bits"] for r in b), default=None))
best = max((r for r in rows if r["built"]), key=lambda r: r["dimV_float"])
print("BEST", best["m"], best["c"], best["seed"], best["dimV_float"], best["max_bits"])
print("candidates>=463:", sum(1 for r in rows if r.get("dimV_float", 0) >= 463))
