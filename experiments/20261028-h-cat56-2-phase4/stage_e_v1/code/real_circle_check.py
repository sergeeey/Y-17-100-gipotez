# WHY: is the rank drop (kernel dim 6) exact on real directions x = (cos a, sin a)?
# For exactly real x, machine-zero singular values (~1e-15) would indicate an exact rank drop.
import numpy as np
from ys_space import load_A, y_basis, S_PLUS
A = load_A(S_PLUS)
for a in [0.0, 0.3, 0.7, 1.1, np.pi / 4, np.pi / 2, 2.0]:
    x = np.array([np.cos(a), np.sin(a)], dtype=complex)
    B, s, rank = y_basis(x, A, S_PLUS, tol=1e-12)
    print(f"a={a:.4f}  kernel dim={B.shape[1]}  rank={rank}  s[rank-1]={s[rank-1]:.3e}  s[rank]={s[rank] if rank < len(s) else 0:.3e}")
