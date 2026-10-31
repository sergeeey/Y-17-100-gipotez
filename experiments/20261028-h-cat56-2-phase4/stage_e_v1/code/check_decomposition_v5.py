# WHY: numerical sanity check of the corrected decomposition lemma (THEOREM_S_PLUS_EXISTENCE_v5.md, Lemma D).
# Lemma D: for PD M = C C^T, w := C^T e_n, u := w/|w|, h := (1,...,1)/sqrt(n), O := Householder reflection
# mapping u to h (O symmetric, orthogonal, O u = h).  Then C' := C O satisfies C' C'^T = M, every column c'_k has
# last coordinate s := |w|/sqrt(n) != 0, and M = d * sum_k chat_k chat_k^T with chat_k := c'_k / s (last coord 1)
# and d := s^2 = |w|^2 / n.  This is a float sanity check only; the theorem itself is exact-in-R.
import numpy as np

rng = np.random.default_rng(0)
worst = 0.0
for trial in range(200):
    n = int(rng.integers(2, 8))
    G = rng.standard_normal((n, n))
    M = G @ G.T + 0.1 * np.eye(n)  # PD
    C = np.linalg.cholesky(M)
    assert np.allclose(C @ C.T, M)
    w = C.T[:, n - 1]  # w = C^T e_n
    u = w / np.linalg.norm(w)
    h = np.ones(n) / np.sqrt(n)
    if np.allclose(u, h):
        O = np.eye(n)
    else:
        v = u - h
        O = np.eye(n) - 2.0 * np.outer(v, v) / (v @ v)
    assert np.allclose(O @ O.T, np.eye(n)) and np.allclose(O, O.T)
    assert np.allclose(O @ u, h)
    Cp = C @ O
    s = np.linalg.norm(w) / np.sqrt(n)
    last = Cp[n - 1, :]
    assert np.allclose(last, s), (last, s)
    d = s * s
    chat = Cp / s  # columns, last coordinate 1
    recon = d * chat @ chat.T
    err = np.abs(recon - M).max() / np.abs(M).max()
    worst = max(worst, err)
print("trials ok; worst relative reconstruction error =", worst)

# example from the discussion: M = diag(1, 2)
M = np.diag([1.0, 2.0])
C = np.linalg.cholesky(M)
w = C.T[:, 1]
u = w / np.linalg.norm(w)
h = np.ones(2) / np.sqrt(2)
v = u - h
O = np.eye(2) - 2.0 * np.outer(v, v) / (v @ v)
Cp = C @ O
s = np.linalg.norm(w) / np.sqrt(2)
chat = Cp / s
print(
    "diag(1,2): d =",
    s * s,
    " chat columns =\n",
    chat,
    "\n reconstruction =\n",
    (s * s) * chat @ chat.T,
)
