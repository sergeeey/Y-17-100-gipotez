"""Positive control (b): do the solver's dim-2 random-start solutions cover the signatures of ALL 11 Hietarinta families
(+ flip P, + identity-type)? Signature = (spec, dimL, cc, tangent, moduli, rank) from ybe.invariants."""
import numpy as np, collections
from ybe import *
from analyze import sig_of
fam = hiet_families(np.random.default_rng(5))
fam['P(flip)'] = flip(2).astype(complex)
fam['Id'] = np.eye(4, dtype=complex)
fsig = {}
for nm, R in fam.items():
    assert rel_res(R, 2) < 1e-12, nm
    s, _ = sig_of(R, 2)
    fsig[nm] = s
d = np.load('dim2_search2.npz')
found = collections.Counter()
for R in d['R']:
    if rel_res(R, 2) > 1e-10: continue
    sv = np.linalg.svd(R, compute_uv=False)
    if sv[0]/sv[-1] > 1e6: continue
    found[sig_of(R, 2)[0]] += 1
print('n solutions', sum(found.values()), 'n signatures', len(found))
for nm, s in fsig.items():
    print('%-8s %s  found-count=%d' % (nm, s, found.get(s, 0)))
unmatched = [(s, c) for s, c in found.items() if s not in fsig.values()]
print('solver signatures not equal to any family generic signature (could be special sub-loci):')
for s, c in sorted(unmatched, key=lambda t: -t[1]): print(c, s)
