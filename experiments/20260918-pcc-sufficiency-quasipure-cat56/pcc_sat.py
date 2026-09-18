"""Saturability decision for H-CAT56-1: does a COMPLETE optimal rank-one POVM exist?

The paper's own End Matter algorithm ("Numerical algorithms for searching the optimal
measurements") says: optimal rank-one POVM elements are exactly the rank-one projectors
lying in `V_perp`, and a complete such POVM exists iff there are weights `alpha_w >= 0`
with `sum_w alpha_w Pi_w = I`. Since `<Pi, A> = <u|A|u>` for `Pi = |u><u|`, the statement
"Pi lies in V_perp" is literally Theorem 1's Eqs. (9)-(10). Hence

    QCRB saturable  <=>  I/d in conv{ |u><u| : |u| = 1, <u|A|u> = 0 for all A in V }.

This module decides that membership with a cutting-plane loop between

  * primal: LP feasibility of `sum_m alpha_m |u_m><u_m| = I` over a sampled solution set;
  * dual:   a traceless Hermitian `X` with `<u_m|X|u_m> >= t > 0` on the whole sampled
            set. If `X` survives a fresh multi-start global minimisation over the solution
            variety, it is a valid non-saturability certificate: any complete POVM would
            give `sum_w alpha_w <u_w|X|u_w> >= t*d > 0`, contradicting `Tr X = 0`.

Verdicts, in decreasing strength:
  NOT_SATURABLE_THEOREM      Observation 2 of the paper (`n < d-1`). Proof-grade.
  SATURABLE                  explicit POVM built AND `CFIM == QFIM` verified. Proof-grade
                             in the constructive direction.
  NOT_SATURABLE_NO_SOLUTION  no single vector satisfies Theorem 1 (search-bounded).
  NOT_SATURABLE_LP           separating certificate survived a fresh probe (search-bounded).
  UNDETERMINED               the loop did not settle. Never counted as evidence either way.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from pcc_core import Analysis, Model, _vec_to_herm, herm_to_real_vec
from scipy.optimize import least_squares, linprog, minimize


def _pack(u: np.ndarray) -> np.ndarray:
    return np.concatenate([np.real(u), np.imag(u)])


def _unpack(x: np.ndarray, d: int) -> np.ndarray:
    return x[:d] + 1j * x[d:]


def _quad_vals_and_jac(x: np.ndarray, d: int, ops: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Values `<u|A_k|u>` and their exact Jacobian w.r.t. `(Re u, Im u)`.

    For Hermitian A: `d/d(Re u) <u|A|u> = 2 Re(A u)`, `d/d(Im u) <u|A|u> = 2 Im(A u)`.
    """
    u = _unpack(x, d)
    au = np.einsum("kij,j->ki", ops, u)
    vals = np.real(np.einsum("i,ki->k", u.conj(), au))
    jac = np.hstack([2 * np.real(au), 2 * np.imag(au)])
    return vals, jac


def _solve_on_variety(x0: np.ndarray, d: int, ops: np.ndarray, tol: float) -> np.ndarray | None:
    """Find a unit `u` with `<u|A_k|u> = 0` for every k, from start `x0`."""
    eye = np.eye(d, dtype=complex)[None, :, :]
    allops = np.concatenate([eye, ops], axis=0) if ops.shape[0] else eye
    offset = np.zeros(allops.shape[0])
    offset[0] = 1.0

    sol = least_squares(
        lambda x: _quad_vals_and_jac(x, d, allops)[0] - offset,
        x0,
        jac=lambda x: _quad_vals_and_jac(x, d, allops)[1],
        xtol=1e-15,
        ftol=1e-15,
        gtol=1e-15,
        max_nfev=200,
    )
    if np.max(np.abs(sol.fun)) >= tol:
        return None
    u = _unpack(sol.x, d)
    return u / np.linalg.norm(u)


def find_hollowizing_vectors(
    v_basis: np.ndarray, d: int, n_starts: int, rng: np.random.Generator, tol: float = 1e-10
) -> list[np.ndarray]:
    """Unit vectors satisfying Theorem 1's Eqs. (9)-(10), i.e. `|u><u|` lies in `V_perp`."""
    out: list[np.ndarray] = []
    for _ in range(n_starts):
        u = _solve_on_variety(rng.normal(size=2 * d), d, v_basis, tol)
        if u is not None:
            out.append(u)
    return out


def minimise_on_variety(
    xop: np.ndarray,
    v_basis: np.ndarray,
    d: int,
    rng: np.random.Generator,
    n_starts: int = 50,
    tol: float = 1e-9,
) -> tuple[float, list[np.ndarray]]:
    """Multi-start global minimisation of `<u|X|u>` over `{|u|=1, <u|A_k|u>=0}`."""
    eye = np.eye(d, dtype=complex)[None, :, :]
    cons = [
        {
            "type": "eq",
            "fun": lambda x: _quad_vals_and_jac(x, d, eye)[0] - 1.0,
            "jac": lambda x: _quad_vals_and_jac(x, d, eye)[1],
        }
    ]
    if v_basis.shape[0]:
        cons.append(
            {
                "type": "eq",
                "fun": lambda x: _quad_vals_and_jac(x, d, v_basis)[0],
                "jac": lambda x: _quad_vals_and_jac(x, d, v_basis)[1],
            }
        )
    xops = xop[None, :, :]
    best, pts = float("inf"), []
    for _ in range(n_starts):
        seed = _solve_on_variety(rng.normal(size=2 * d), d, v_basis, 1e-8)
        x0 = _pack(seed) if seed is not None else rng.normal(size=2 * d)
        sol = minimize(
            lambda x: float(_quad_vals_and_jac(x, d, xops)[0][0]),
            x0,
            jac=lambda x: _quad_vals_and_jac(x, d, xops)[1][0],
            constraints=cons,
            method="SLSQP",
            options={"maxiter": 300, "ftol": 1e-12},
        )
        u = _unpack(sol.x, d)
        nrm = float(np.linalg.norm(u))
        if nrm < 1e-9:
            continue
        u = u / nrm
        if v_basis.shape[0] and np.max(np.abs(_quad_vals_and_jac(_pack(u), d, v_basis)[0])) > tol:
            continue
        pts.append(u)
        best = min(best, float(np.real(u.conj() @ (xop @ u))))
    return best, pts


def completeness_lp(vectors: list[np.ndarray], d: int) -> tuple[float, np.ndarray | None]:
    """Minimum L1 slack for `sum_m alpha_m |u_m><u_m| = I`, `alpha_m >= 0`. 0 => saturable."""
    if not vectors:
        return float("inf"), None
    cols = np.array([herm_to_real_vec(np.outer(u, u.conj())) for u in vectors]).T
    b = herm_to_real_vec(np.eye(d, dtype=complex))
    m, dim = len(vectors), cols.shape[0]
    res = linprog(
        np.concatenate([np.zeros(m), np.ones(2 * dim)]),
        A_eq=np.hstack([cols, np.eye(dim), -np.eye(dim)]),
        b_eq=b,
        bounds=[(0, None)] * (m + 2 * dim),
        method="highs",
    )
    if not res.success:
        return float("inf"), None
    return float(res.fun), np.asarray(res.x[:m])


def separation_certificate(vectors: list[np.ndarray], d: int) -> tuple[float, np.ndarray | None]:
    """`max t` s.t. `<u_m|X|u_m> >= t` for all m, `Tr X = 0`, entries of X bounded by 1."""
    if not vectors:
        return float("-inf"), None
    dim = d * d
    rows = np.array([herm_to_real_vec(np.outer(u, u.conj())) for u in vectors])
    trace_row = herm_to_real_vec(np.eye(d, dtype=complex))
    res = linprog(
        np.concatenate([np.zeros(dim), [-1.0]]),
        A_ub=np.hstack([-rows, np.ones((len(vectors), 1))]),
        b_ub=np.zeros(len(vectors)),
        A_eq=np.hstack([trace_row[None, :], np.zeros((1, 1))]),
        b_eq=np.array([0.0]),
        bounds=[(-1, 1)] * dim + [(None, None)],
        method="highs",
    )
    if not res.success:
        return float("-inf"), None
    return float(-res.fun), _vec_to_herm(np.asarray(res.x[:dim]), d)


def direct_povm_search(
    v_basis: np.ndarray,
    d: int,
    n_elements: int,
    rng: np.random.Generator,
    n_starts: int = 6,
    tol: float = 1e-9,
) -> list[np.ndarray] | None:
    """Alternative tool: optimise `n_elements` vectors so that the Theorem-1 conditions
    AND `sum_w |u_w><u_w| = I` hold simultaneously. Shares no code path with the LP route.
    """
    eye_vec = herm_to_real_vec(np.eye(d, dtype=complex))

    def res_fn(x: np.ndarray) -> np.ndarray:
        us = (x[: d * n_elements] + 1j * x[d * n_elements :]).reshape(n_elements, d)
        parts = []
        if v_basis.shape[0]:
            parts.append(np.real(np.einsum("wi,kij,wj->wk", us.conj(), v_basis, us)).ravel())
        parts.append(herm_to_real_vec(np.einsum("wi,wj->ij", us, us.conj())) - eye_vec)
        return np.concatenate(parts)

    for _ in range(n_starts):
        x0 = rng.normal(size=2 * d * n_elements) / np.sqrt(n_elements)
        sol = least_squares(res_fn, x0, xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=1500)
        if np.max(np.abs(sol.fun)) < tol:
            us = (sol.x[: d * n_elements] + 1j * sol.x[d * n_elements :]).reshape(n_elements, d)
            return [us[w] for w in range(n_elements)]
    return None


def cfim(povm: list[np.ndarray], rho: np.ndarray, drho: list[np.ndarray]) -> np.ndarray:
    """Classical Fisher information matrix of the rank-one POVM `{|u_w><u_w|}`."""
    s = len(drho)
    out = np.zeros((s, s))
    for u in povm:
        e = np.outer(u, u.conj())
        p = float(np.real(np.trace(rho @ e)))
        dp = np.array([float(np.real(np.trace(dr @ e))) for dr in drho])
        if p > 1e-12:
            out += np.outer(dp, dp) / p
        elif np.max(np.abs(dp)) > 1e-8:
            out += np.inf
    return out


@dataclass
class SaturabilityResult:
    """Verdict on whether the QCRB can be saturated for one model.

    `verdict` is derived ONLY from the exact rank test (Observation 2). The optimiser
    fields below are diagnostics and are NEVER allowed to produce a negative verdict --
    see `constructive_probe` for why.
    """

    verdict: str  # NOT_SATURABLE_CERTIFIED | NOT_EXCLUDED
    dim_v_perp: int
    rank_is_robust: bool
    rank_plateau: dict
    rank_gap_ratio: float
    probe_ran: bool = False
    probe_constructed: bool | None = None
    probe_lp_slack: float | None = None
    probe_povm_size: int | None = None
    probe_completeness_error: float | None = None
    probe_cfim_qfim_gap: float | None = None
    outcome: str = ""
    test2_ran: bool = False
    test2_status: str | None = None
    test2_feasible: bool | None = None
    test2_lp_slack: float | None = None
    test2_n_v_sampled: int | None = None
    test2_povm_size: int | None = None
    test2_completeness_error: float | None = None
    test2_cfim_qfim_gap: float | None = None
    detail: str = ""


def alpha_feasibility(
    ana: Analysis, rng: np.random.Generator, n_starts: int, max_rounds: int = 4
) -> dict:
    """EXACT TEST 2 -- the paper's completeness-feasibility criterion (End Matter).

    "Search for non-negative alpha^(w) that satisfies sum_w alpha^(w) = d,
     sum_w alpha^(w) v^(w) = 0 ... If such {alpha^(w)} does not exist, then the QCRB is
     not saturable."

    In the `Pi_w = |u_w><u_w|` parametrisation this is exactly
    `sum_w alpha_w |u_w><u_w| = I, alpha_w >= 0`, an LP feasibility problem -- and the LP
    half IS exact (HiGHS returns feasible/infeasible, not "did not converge").

    THE CAVEAT THAT DECIDES ITS EPISTEMIC STATUS, stated here rather than in a footnote:
    the LP is exact only over the set of `v^(w)` it is GIVEN. Enumerating that set is the
    paper's algorithm step 1, and it is a NON-CONVEX problem -- the admissible `v` form a
    variety of dimension `n - (d-1)`, finite only when `n = d - 1`. Every sample in this
    experiment has `n >> d - 1`, so the set must be sampled, and LP-infeasibility over a
    SAMPLE is not infeasibility over the variety. This experiment measured that gap
    directly: at `d = 8`, where Theorem 3 guarantees feasibility, this same routine
    returned infeasible on 20/20 samples.

    Therefore: `feasible = True` is a sound POSITIVE result (an explicit POVM exists and is
    returned). `feasible = False` is recorded as `LP_INFEASIBLE_ON_SAMPLE` and is NOT a
    certificate. A dual separating hyperplane is also computed and re-probed, and even that
    is only as strong as the global minimisation behind it -- reported, never promoted.
    """
    d = ana.d
    out: dict = {"ran": True, "feasible": None, "lp_slack": None, "n_v_sampled": 0}
    sols = find_hollowizing_vectors(ana.v_basis, d, n_starts, rng)
    out["n_v_sampled"] = len(sols)
    if not sols:
        out["status"] = "NO_ADMISSIBLE_V_FOUND"
        out["note"] = "search-bounded; not a certificate"
        return out

    slack, alphas = float("inf"), None
    for rnd in range(1, max_rounds + 1):
        out["rounds"] = rnd
        slack, alphas = completeness_lp(sols, d)
        out["lp_slack"] = slack
        if slack < 1e-7:
            break
        t_sep, xcert = separation_certificate(sols, d)
        out["separation_t"] = t_sep
        if xcert is None or t_sep <= 0:
            break
        best, pts = minimise_on_variety(xcert, ana.v_basis, d, rng)
        out["separation_reprobe_min"] = best
        fresh = [p for p in pts if float(np.real(p.conj() @ (xcert @ p))) < t_sep]
        if not fresh:
            break
        sols.extend(fresh)
        sols.extend(find_hollowizing_vectors(ana.v_basis, d, n_starts, rng))
        out["n_v_sampled"] = len(sols)

    if slack < 1e-7 and alphas is not None:
        keep = [(a, u) for a, u in zip(alphas, sols, strict=True) if a > 1e-9]
        povm = [np.sqrt(a) * u for a, u in keep]
        total = sum(np.outer(v, v.conj()) for v in povm)
        out["feasible"] = True
        out["status"] = "FEASIBLE_EXPLICIT_POVM"
        out["povm_size"] = len(povm)
        out["completeness_error"] = float(np.linalg.norm(total - np.eye(d)))
        out["povm"] = povm
        return out
    out["feasible"] = False
    out["status"] = "LP_INFEASIBLE_ON_SAMPLE"
    out["note"] = "NOT a certificate -- the v-set was sampled, not enumerated"
    return out


def certified_verdict(ana: Analysis) -> tuple[str, str]:
    """The ONLY decisive non-saturability test available: Observation 2 of the paper.

    `dim V_perp < d`  =>  the QCRB cannot be saturated. This is a theorem plus a rank
    computation -- no search, no optimiser, no initial guess. It is one-directional:
    `dim V_perp >= d` means only "not excluded by this test", NEVER "saturable".
    """
    if not ana.rank_is_robust:
        return (
            "NUMERICALLY_AMBIGUOUS",
            "the rank of the W/M stack is not stable across the pre-registered threshold "
            f"sweep {ana.rank_plateau} / Gram route ({ana.gram_rank} vs {ana.dim_v}) / "
            f"singular-value gap ({ana.rank_gap_ratio:.3e}); no verdict is issued",
        )
    if ana.dim_v_perp < ana.d:
        return (
            "NOT_SATURABLE_CERTIFIED",
            f"Observation 2: dim V_perp = {ana.dim_v_perp} < d = {ana.d} "
            f"(n = {ana.n} < d-1 = {ana.d - 1})",
        )
    return (
        "NOT_EXCLUDED",
        f"dim V_perp = {ana.dim_v_perp} >= d = {ana.d}; the exact rank test does not "
        f"exclude saturation. This is NOT a claim that a saturating POVM exists.",
    )


def constructive_probe(
    ana: Analysis,
    model: Model,
    rng: np.random.Generator,
    n_starts: int = 120,
    max_rounds: int = 4,
    lp_tol: float = 1e-7,
) -> dict:
    """OPTIONAL, NON-DECISIVE. Try to BUILD a complete optimal POVM.

    Success is meaningful: an explicit POVM with `sum E = I` and `CFIM == QFIM` positively
    demonstrates saturation. Failure is meaningless and is recorded as such -- it cannot
    distinguish "no saturating measurement exists" from "the search did not converge".
    This experiment's own positive control demonstrated that concretely: on Eq. (16)
    states ABOVE the Eq. (15) threshold, where Theorem 3 GUARANTEES saturability, the
    cutting-plane route still returned a would-be "not saturable" answer on 2 of 3 samples.
    That is why `verdict` never reads this function's negative side.
    """
    d = ana.d
    out: dict = {"constructed": False, "lp_slack": None, "rounds": 0}
    sols = find_hollowizing_vectors(ana.v_basis, d, n_starts, rng)
    out["n_hollowizing_solutions"] = len(sols)
    if not sols:
        out["note"] = "no vector satisfying Theorem 1 found -- NOT evidence of anything"
        return out

    slack, alphas = float("inf"), None
    for rnd in range(1, max_rounds + 1):
        out["rounds"] = rnd
        slack, alphas = completeness_lp(sols, d)
        out["lp_slack"] = slack
        if slack < lp_tol:
            break
        t, xcert = separation_certificate(sols, d)
        if xcert is None or t <= 0:
            break
        _, pts = minimise_on_variety(xcert, ana.v_basis, d, rng)
        fresh = [p for p in pts if float(np.real(p.conj() @ (xcert @ p))) < t]
        if not fresh:
            out["note"] = (
                "cutting plane stalled; per this function's docstring this is NOT "
                "evidence against saturability"
            )
            break
        sols.extend(fresh)
        sols.extend(find_hollowizing_vectors(ana.v_basis, d, n_starts, rng))

    if slack >= lp_tol or alphas is None:
        out.setdefault("note", "LP did not become feasible -- NOT evidence of anything")
        return out

    keep = [(a, u) for a, u in zip(alphas, sols, strict=True) if a > 1e-9]
    povm = [np.sqrt(a) * u for a, u in keep]
    total = sum(np.outer(v, v.conj()) for v in povm)
    out["constructed"] = True
    out["povm_size"] = len(povm)
    out["completeness_error"] = float(np.linalg.norm(total - np.eye(d)))
    out["cfim_qfim_rel_gap"] = float(
        np.max(np.abs(cfim(povm, model.rho, model.drho) - ana.qfim))
        / max(float(np.max(np.abs(ana.qfim))), 1e-300)
    )
    return out


def saturability(
    ana: Analysis,
    model: Model,
    rng: np.random.Generator,
    run_probe: bool = False,
    run_test2: bool = False,
    n_starts: int = 120,
) -> SaturabilityResult:
    """Run BOTH of the paper's non-optimiser tests and classify the sample.

    Test 1 (Observation 2): dim V_perp < d => not saturable. Exact and one-directional.
    Test 2 (End Matter completeness-feasibility): no non-negative alpha with
            sum_w alpha_w Pi_w = I => not saturable. The LP half is exact; the enumeration
            of admissible Pi_w it depends on is NOT (see `alpha_feasibility`), so its
            negative side is recorded, never certified.

    Outcomes:
      NUMERICALLY_AMBIGUOUS           rank not stable over the pre-registered sweep
      CERTIFIED_NON_SATURABLE_RANK    test 1 fired -- a counterexample
      LP_INFEASIBLE_ON_SAMPLE         test 2 infeasible over a SAMPLED v-set; NOT a
                                      certificate, kept as its own category
      UNRESOLVED_BY_BOTH_EXACT_TESTS  test 1 did not fire and test 2 returned an explicit
                                      complete POVM. NOT a claim of saturability in
                                      general -- neither test excludes other mechanisms
    """
    verdict, detail = certified_verdict(ana)
    res = SaturabilityResult(
        verdict=verdict,
        dim_v_perp=ana.dim_v_perp,
        rank_is_robust=ana.rank_is_robust,
        rank_plateau=ana.rank_plateau,
        rank_gap_ratio=ana.rank_gap_ratio,
        detail=detail,
    )
    res.outcome = verdict
    if verdict == "NOT_SATURABLE_CERTIFIED":
        res.outcome = "CERTIFIED_NON_SATURABLE_RANK"
        return res
    if verdict == "NUMERICALLY_AMBIGUOUS":
        return res

    if run_test2:
        t2 = alpha_feasibility(ana, rng, n_starts=n_starts)
        res.test2_ran = True
        res.test2_status = t2.get("status")
        res.test2_feasible = t2.get("feasible")
        res.test2_lp_slack = t2.get("lp_slack")
        res.test2_n_v_sampled = t2.get("n_v_sampled")
        res.test2_povm_size = t2.get("povm_size")
        res.test2_completeness_error = t2.get("completeness_error")
        if t2.get("feasible"):
            res.outcome = "UNRESOLVED_BY_BOTH_EXACT_TESTS"
            povm = t2.get("povm")
            if povm:
                res.test2_cfim_qfim_gap = float(
                    np.max(np.abs(cfim(povm, model.rho, model.drho) - ana.qfim))
                    / max(float(np.max(np.abs(ana.qfim))), 1e-300)
                )
        else:
            res.outcome = "LP_INFEASIBLE_ON_SAMPLE"

    if run_probe:
        probe = constructive_probe(ana, model, rng, n_starts=n_starts)
        res.probe_ran = True
        res.probe_constructed = bool(probe["constructed"])
        res.probe_lp_slack = probe.get("lp_slack")
        res.probe_povm_size = probe.get("povm_size")
        res.probe_completeness_error = probe.get("completeness_error")
        res.probe_cfim_qfim_gap = probe.get("cfim_qfim_rel_gap")
    return res
