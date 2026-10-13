import json, collections
d = json.load(open("search_stage1_seed2.json"))
print("screen", d["screen"])
c = d["counted"]
h = collections.Counter((o["k"], o["count"]) for o in c)
print("k,count:n", dict(sorted(h.items())))
print("hidden_pairs>0:", sum(1 for o in c if o["hidden_pairs"]>0), " near_tangent>0:", sum(1 for o in c if o["n_near_tangent"]>0), " rejected>0:", sum(1 for o in c if o["rejected"]>0))
print("count>=2 systems:", [(o["k"], o["count"], round(o["delta"],3), [round(x,3) for x in o["p"]]) for o in c if o["count"]>=2][:12])
print("n counted", len(c), " with k>=2:", sum(1 for o in c if o["k"]>=2), " k==3:", sum(1 for o in c if o["k"]==3), " k==4:", sum(1 for o in c if o["k"]>=4))
