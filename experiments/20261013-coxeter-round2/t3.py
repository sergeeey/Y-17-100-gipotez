import json, re
from gale_one_pair import gen, canon
from gale_enum import polytope_from_gale
j = json.load(open('C:/Users/serge/.arxiv-mcp-server/papers/.latex/1511.08451.json', encoding='utf8'))
txt = json.dumps(j)
print("json keys/type", type(j), list(j.keys())[:6] if isinstance(j, dict) else len(j))
src = None
def walk(o):
    global src
    if isinstance(o, str) and 'Dimension 4' in o and 'sidesubfloat' in o:
        src = o if (src is None or len(o) > len(src)) else src
    elif isinstance(o, dict):
        for v in o.values(): walk(v)
    elif isinstance(o, list):
        for v in o: walk(v)
walk(j)
if src:
    secs = re.split(r'\subsection\{', src)
    for s in secs[1:]:
        name = s.split('}')[0]
        print(name, "sidesubfloat count:", s.count('\sidesubfloat'), " dashed edges per diagram check later")
        if name.startswith('Dimension 4'):
            # per-diagram: count of 'dashed' draws
            diags = s.split('\sidesubfloat')[1:]
            print("  dim4 dashed per diagram:", [d.count('[dashed]') for d in diags])
G4 = {(k,mu): polytope_from_gale(k,mu) for k,mu in gen(4)}
rob = {"G1_10gon": (5, (1,1,0,2,0,1,0,1,0,1)), "G2_8gon": (4, (1,1,0,1,1,0,3,0))}
for name,(k,mu) in rob.items():
    c = (k, canon(k, mu))
    print(name, "canonical", c, "in one-pair d=4 list:", c in G4, "| disjoint pairs:", len(polytope_from_gale(k, c[1])[2]))
print("all d=4 one-pair types (k, mu, #disjoint):")
for (k,mu),(f,v,dj) in G4.items(): print("  ", k, mu, len(v), len(dj))
