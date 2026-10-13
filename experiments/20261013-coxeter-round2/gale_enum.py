"""Enumerate standard Gale diagrams (Gruenbaum / Tumarkin sec.1 definition, as restated in Roberts 1511.08451 Def 4.1)
for d-polytopes with d+3 facets, derive vertex-facet incidences, and match against given polytopes."""
import itertools, sys
import networkx as nx

def fits_halfplane(positions, k):
    """True iff all positions (mod 2k) lie in k cyclically consecutive positions  <=>  origin NOT in conv."""
    if not positions: return True
    P = set(p % (2*k) for p in positions)
    for s in range(2*k):
        if all(((p - s) % (2*k)) < k for p in P):
            return True
    return False

def gale_diagrams(d, kmax=None):
    n = d + 3
    res = []
    for k in range(2, n + 1 + 1):
        m = 2*k
        # compositions of n into m nonneg parts
        def rec(i, left, cur):
            if i == m-1:
                yield cur + [left]; return
            for x in range(left+1):
                yield from rec(i+1, left-x, cur+[x])
        for mu in rec(0, n, []):
            if any(mu[i]==0 and mu[(i+1)%m]==0 for i in range(m)): continue
            if any(mu[i]==0 and mu[(i+k)%m]==0 for i in range(k)): continue
            # every open half-plane has sum >= 2 : check k-1 consecutive and also windows
            ok = True
            for s in range(m):
                if sum(mu[(s+t)%m] for t in range(1, k)) < 2:   # line through s and s+k: open half-plane = s+1..s+k-1
                    ok = False; break
            if not ok: continue
            res.append((k, tuple(mu)))
    # canonical up to dihedral symmetry
    canon = {}
    for k, mu in res:
        m = 2*k
        forms = []
        for r in range(m):
            rot = mu[r:]+mu[:r]
            forms.append(rot); forms.append(tuple(reversed(rot)))
        c = min(forms)
        canon[(k, c)] = 1
    return sorted(canon)

def polytope_from_gale(k, mu):
    m = 2*k
    facets = []  # position of each facet
    for p, c in enumerate(mu):
        facets += [p]*c
    n = len(facets)
    # cofaces C: nonempty subset with origin in conv
    cof = []
    for r in range(1, n+1):
        for C in itertools.combinations(range(n), r):
            if not fits_halfplane([facets[i] for i in C], k):
                cof.append(frozenset(C))
    cofset = set(cof)
    minimal = [C for C in cof if not any((D < C) for D in cofset)]
    verts = [frozenset(range(n)) - C for C in minimal]
    # disjoint facet pairs: pair {i,j} is a face iff complement in cof
    disj = [(i,j) for i,j in itertools.combinations(range(n),2) if not any((i in V and j in V) for V in verts)]  # share no vertex => disjoint
    return facets, verts, disj

def inc_graph(nf, verts):
    g = nx.Graph()
    for i in range(nf): g.add_node(('f',i), t='f')
    for vi, V in enumerate(verts):
        g.add_node(('v',vi), t='v')
        for f in V: g.add_edge(('f',f), ('v',vi))
    return g

def iso(g1, g2):
    return nx.is_isomorphic(g1, g2, node_match=lambda a,b: a['t']==b['t'])

if __name__ == "__main__":
    d = int(sys.argv[1])
    G = gale_diagrams(d)
    print("d=%d: %d standard Gale diagrams (dihedral classes)" % (d, len(G)))
    for k, mu in G:
        facets, verts, disj = polytope_from_gale(k, mu)
        degs = sorted(len(V) for V in verts)
        nonsimple = sum(1 for x in degs if x > d)
        opp = sum(1 for i in range(k) if mu[i] > 0 and mu[i+k] > 0)
        print("k=%d mu=%s  verts=%d nonsimple=%d opposite-nonzero-pairs=%d disjoint-pairs=%d" % (k, mu, len(verts), nonsimple, opp, len(disj)))
