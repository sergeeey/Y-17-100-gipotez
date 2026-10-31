# WHY: store EXACT rational kernel bases (strings) for the certificate step; floats are only for the SDP.
import pickle
from fractions import Fraction
from exact_kernel import exact_kernel
D = pickle.load(open("../logs/exact_dirs.pkl", "rb"))
out = []
for d in D["dirs"]:
    (a0r, a0i), (a1r, a1i) = d
    x = ((Fraction(a0r), Fraction(a0i)), (Fraction(a1r), Fraction(a1i)))
    rank, basis = exact_kernel(x)
    out.append([[(str(v[r]), str(v[20 + r])) for r in range(20)] for v in basis])
pickle.dump({"dirs": D["dirs"], "dims": D["dims"], "bases_exact": out}, open("../logs/exact_bases.pkl", "wb"))
print("exact bases stored for", len(out), "directions; dims", sorted(set(len(b) for b in out)))
