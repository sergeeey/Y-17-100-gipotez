"""Stage C probe: reformulation I_20 in cone{yy^dag : y in Y_S}  <=>  M_S = B^dag B in cone{ lam lam^T (x) x x^dag }.
Necessary condition: partial transpose on the C^2 factor is PSD. Exploratory (floats); exact version in c2.
Usage: python -I c1_ppt_probe.py <instance.jsonl>
"""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "20261027-h-cat56-2-discovery", "code")))
import s8_admissible_span as sa  # noqa: E402

As = sa.load_A(sys.argv[1])


def M_of(S):
    n = len(S)
    M = np.zeros((2 * n, 2 * n), dtype=complex)
    for a, i in enumerate(S):
        for b, k in enumerate(S):
            M[2 * a:2 * a + 2, 2 * b:2 * b + 2] = As[i].conj().T @ As[k]
    return M


def pt2(M, n):
    P = M.reshape(n, 2, n, 2).transpose(0, 3, 2, 1).reshape(2 * n, 2 * n)  # swap the two C^2 indices
    return P


def report(name, S):
    M = M_of(S); n = len(S)
    sym = max(np.abs(M[2*a:2*a+2, 2*b:2*b+2] - M[2*b:2*b+2, 2*a:2*a+2]).max() for a in range(n) for b in range(n))
    herm_blocks = max(np.abs(M[2*a:2*a+2, 2*b:2*b+2] - M[2*a:2*a+2, 2*b:2*b+2].conj().T).max() for a in range(n) for b in range(n))
    ev = np.linalg.eigvalsh(M); evp = np.linalg.eigvalsh(pt2(M, n))
    print(f"{name:10s} |S|={n:2d} block-sym={sym:.1e} block-herm={herm_blocks:.1e} "
          f"min eig M={ev[0]:.3e} (rank {int((ev>1e-9*ev[-1]).sum())})  min eig PT={evp[0]:.4e}  max eig PT={evp[-1]:.3e}")


report("S+", list(range(12)))
report("S-", list(range(4, 16)))
report("all16", list(range(16)))
for k in range(2, 16):
    report(f"prefix{k}", list(range(k)))
