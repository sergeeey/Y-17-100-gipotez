"""Gale diagrams of d-polytopes with d+3 facets having EXACTLY ONE opposite nonzero pair (both weight 1) and (optionally) zero
combinatorially disjoint facet pairs.  Efficient generator: rotate so the nonzero pair sits at positions 0 and k."""
import itertools, sys, json
from gale_enum import fits_halfplane, polytope_from_gale

def canon(k, mu):
    m = 2*k; forms = []
    for r in range(m):
        rot = mu[r:]+mu[:r]; forms.append(rot); forms.append(tuple(reversed(rot)))
    return min(forms)

def gen(d):
    n = d + 3
    seen = set()
    out = []
    for k in range(2, n):  # k-1 pairs with single nonzero side, each weight>=1, total d+1
        npairs = k - 1
        if npairs > d + 1: break
        # compositions of d+1 into npairs parts >=1
        for cuts in itertools.combinations(range(1, d + 1), npairs - 1):
            parts = [b - a for a, b in zip((0,) + cuts, cuts + (d + 1,))]
            for sides in itertools.product((0, 1), repeat=npairs):
                mu = [0] * (2 * k)
                mu[0] = 1; mu[k] = 1
                for j in range(npairs):
                    pos = (j + 1) + (k if sides[j] else 0)
                    mu[pos] = parts[j]
                # no neighbouring zeros
                if any(mu[i] == 0 and mu[(i + 1) % (2 * k)] == 0 for i in range(2 * k)):
                    continue
                # half-plane condition: k-1 consecutive sum >= 2
                if any(sum(mu[(s + t) % (2 * k)] for t in range(1, k)) < 2 for s in range(2 * k)):
                    continue
                c = (k, canon(k, tuple(mu)))
                if c in seen: continue
                seen.add(c); out.append(c)
    return out

if __name__ == "__main__":
    for d in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
        types = gen(d)
        res = []
        for k, mu in types:
            facets, verts, disj = polytope_from_gale(k, mu)
            res.append((k, mu, len(verts), len(disj)))
        z = [r for r in res if r[3] == 0]
        print("d=%d: %d one-pair Gale types, %d with zero disjoint pairs" % (d, len(res), len(z)), flush=True)
        for r in z: print("    ZERO-DISJOINT k=%d mu=%s verts=%d" % (r[0], r[1], r[2]), flush=True)
