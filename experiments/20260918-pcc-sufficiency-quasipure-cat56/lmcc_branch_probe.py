"""Why does the constructive search fail at d=8? Structural branch vs. budget.

`probe_start_sweep.py` shows the failure is not a budget problem: 16x more random starts
changes nothing. This asks the sharper question -- is the solution the theorem promises
sitting in a part of the solution variety that Gaussian random starts never reach?

The paper's own End Matter says the optimal POVM for an Eq. (16) state has the LMCC form
`|pi_{nu,a}> = |e^(a)_nu> (x) |a>` -- every element is a PRODUCT vector with a DEFINITE
ancilla index. The set of such vectors is a measure-zero subvariety of the sphere, so a
Gaussian random start converges to it with probability zero.

So: repeat the search restricted to each ancilla branch (fix `a`, solve inside that
4-dimensional block), pool the branches, and re-run the same LP. If the LP becomes
feasible, the `d = 8` failure is a COVERAGE failure of the random sampler -- the search
was looking in the wrong place, not failing to find something that exists -- which is a
sharper statement than "search is unreliable", and still supports the conclusion that a
failed search must never be read as a certificate.

Run:  python lmcc_branch_probe.py
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pcc_core as pc
import pcc_sat as ps

OUT = Path(__file__).parent / "metrics" / "lmcc_branch_probe.json"


def branch_solutions(
    ana: pc.Analysis, d_sys: int, rank: int, a: int, n_starts: int, rng: np.random.Generator
) -> list[np.ndarray]:
    """Unit vectors of the form |e> (x) |a> satisfying Theorem 1's conditions.

    Ordering is primary (x) ancilla, so index = p * rank + a.
    """
    idx = np.array([p * rank + a for p in range(d_sys)])
    ops = ana.v_basis[:, idx][:, :, idx] if ana.v_basis.shape[0] else ana.v_basis
    out = []
    for _ in range(n_starts):
        u_small = ps._solve_on_variety(rng.normal(size=2 * d_sys), d_sys, ops, 1e-10)
        if u_small is None:
            continue
        full = np.zeros(ana.d, dtype=complex)
        full[idx] = u_small
        out.append(full)
    return out


def main() -> None:
    rng = np.random.default_rng(555)
    d_sys, rank, s = 4, 2, 2
    rows = []
    for trial in range(3):
        model = None
        while model is None:
            model = pc.sample_bipartite_quasipure(d_sys, rank, s, rng)
        ana = pc.analyse(model)

        random_sols = ps.find_hollowizing_vectors(ana.v_basis, ana.d, 400, rng)
        slack_random, _ = ps.completeness_lp(random_sols, ana.d)

        branch_sols: list[np.ndarray] = []
        per_branch = []
        for a in range(rank):
            got = branch_solutions(ana, d_sys, rank, a, 200, rng)
            per_branch.append(len(got))
            branch_sols.extend(got)

        # verify the branch vectors really satisfy the FULL Theorem 1 conditions
        worst = 0.0
        for u in branch_sols:
            vals = np.real(np.einsum("i,kij,j->k", u.conj(), ana.v_basis, u))
            worst = max(worst, float(np.max(np.abs(vals))) if vals.size else 0.0)

        pooled = random_sols + branch_sols
        slack_branch, alphas = ps.completeness_lp(branch_sols, ana.d)
        slack_pooled, _ = ps.completeness_lp(pooled, ana.d)

        built = None
        if slack_branch < 1e-7 and alphas is not None:
            keep = [(al, u) for al, u in zip(alphas, branch_sols, strict=True) if al > 1e-9]
            povm = [np.sqrt(al) * u for al, u in keep]
            total = sum(np.outer(v, v.conj()) for v in povm)
            built = {
                "povm_size": len(povm),
                "completeness_error": float(np.linalg.norm(total - np.eye(ana.d))),
                "cfim_qfim_rel_gap": float(
                    np.max(np.abs(ps.cfim(povm, model.rho, model.drho) - ana.qfim))
                    / max(float(np.max(np.abs(ana.qfim))), 1e-300)
                ),
            }

        rows.append(
            {
                "trial": trial,
                "d": ana.d,
                "dim_V": ana.dim_v,
                "dim_V_perp": ana.dim_v_perp,
                "random_starts": 400,
                "random_solutions": len(random_sols),
                "lp_slack_random_only": slack_random,
                "branch_solutions_per_ancilla": per_branch,
                "max_theorem1_violation_of_branch_vectors": worst,
                "lp_slack_branch_only": slack_branch,
                "lp_slack_pooled": slack_pooled,
                "constructed_from_branches": built,
            }
        )
        print(
            f"  trial {trial}: random LP slack {slack_random:.4f} | branch LP slack "
            f"{slack_branch:.3e} | pooled {slack_pooled:.3e} | built={built}"
        )

    fixed = all(r["lp_slack_branch_only"] < 1e-7 for r in rows)
    payload = {
        "question": "is the d=8 constructive failure a budget problem or a coverage problem?",
        "rows": rows,
        "branch_restricted_search_succeeds": bool(fixed),
        "conclusion": (
            "The optimal POVM the paper constructs is a product basis with a definite "
            "ancilla index -- a measure-zero subvariety that Gaussian random starts reach "
            "with probability zero. Restricting the search to those branches recovers it. "
            "The failure was therefore a COVERAGE failure of the sampler, which is exactly "
            "why a failed search can never be read as a non-existence certificate: the "
            "same code, same budget, same state, different start distribution, opposite "
            "answer."
            if fixed
            else "Branch restriction did not recover a POVM either; the cause is not "
            "identified and the failure is recorded as unexplained."
        ),
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print("branch_restricted_search_succeeds:", fixed)


if __name__ == "__main__":
    main()
