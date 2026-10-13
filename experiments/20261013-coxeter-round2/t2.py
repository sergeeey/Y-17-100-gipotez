from exact3 import *
from gale_enum import *
cases = {
 "PA": "0-1:inf 0-6:4 1-5:4 2-3:4 2-6:6 3-4:4 4-5:6",
 "PB": "0-1:inf 0-6:4 1-5:4 2-3:4 2-6:6 3-4:4 3-5:3 3-6:3 4-5:6",
}
G4 = gale_diagrams(4)
for name,s in cases.items():
    e = parse_edges(s); v = validate(7, e)
    # vertex-facet incidence
    verts = [set(t) for t in v['_tight']]
    g = inc_graph(7, [frozenset(t) for t in verts])
    print(name, "vertex degrees", v['vertex_degrees'])
    for k,mu in G4:
        facets, vs, disj = polytope_from_gale(k, mu)
        if len(vs) != len(verts): continue
        if iso(g, inc_graph(7, vs)):
            print("   MATCHES Gale k=%d mu=%s"%(k,mu))
