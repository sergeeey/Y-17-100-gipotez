"""Bridge 10 check: is the LP-vertex POVM size equal to the rank of the span of the candidates?
The span of candidate outer products is a solver-side quantity; is the branch value 26 that rank?
that rank? Reuses H-CAT56-1's modules unchanged, same seed as lmcc_branch_probe.main (555)."""

import importlib.util
import os
import sys
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np

OLD = Path(
    r"E:\Проверка Гипотез\работаю над проверкой гипотез\Y-17 100 gipotez\experiments"
    r"\20260918-pcc-sufficiency-quasipure-cat56"
)
sys.path.insert(0, str(OLD))
spec = importlib.util.spec_from_file_location("lbp", OLD / "lmcc_branch_probe.py")
lbp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lbp)
pc, ps = lbp.pc, lbp.ps


def rank_of(vectors: list[np.ndarray]) -> tuple[int, np.ndarray]:
    cols = np.array([ps.herm_to_real_vec(np.outer(u, u.conj())) for u in vectors])
    sv = np.linalg.svd(cols, compute_uv=False)
    return int(np.sum(sv > 1e-9 * sv[0])), sv


rng = np.random.default_rng(555)
d_sys, rank, s = 4, 2, 2
for trial in range(3):
    model = None
    while model is None:
        model = pc.sample_bipartite_quasipure(d_sys, rank, s, rng)
    ana = pc.analyse(model)
    random_sols = ps.find_hollowizing_vectors(ana.v_basis, ana.d, 400, rng)
    branch = []
    for a in range(rank):
        branch.extend(lbp.branch_solutions(ana, d_sys, rank, a, 200, rng))
    r_rand, _ = rank_of(random_sols)
    r_branch, sv = rank_of(branch)
    slack, alphas = ps.completeness_lp(branch, ana.d)
    povm = int(np.sum(alphas > 1e-9)) if alphas is not None else -1
    slack_r, alphas_r = ps.completeness_lp(random_sols, ana.d)
    povm_r = int(np.sum(alphas_r > 1e-9)) if alphas_r is not None else -1
    print(
        f"trial {trial}: d={ana.d} dimV_perp={ana.dim_v_perp} | rank(span random cands)={r_rand}"
        f" | rank(span branch cands)={r_branch} LP-povm-size(branch)={povm} slack={slack:.1e}"
        f" | LP(random) size={povm_r} slack={slack_r:.1e}"
    )
