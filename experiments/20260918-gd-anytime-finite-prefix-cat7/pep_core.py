"""PEP core for H-CAT7-1 (GD-ANYTIME-FINITE-v1).

Direct cvxpy implementation of the Performance Estimation Problem (PEP) for
gradient descent on 1-smooth convex functions, plus the two published stepsize
schedules used as comparators.

Conventions (stated once, used everywhere)
------------------------------------------
GD with N gradient steps::

    x_{k+1} = x_k - h_k * grad f(x_k),   k = 0, ..., N-1

so a schedule of length N drives N steps and produces iterates x_0 .. x_N.
Normalisation: L = 1, ||x_0 - x*||^2 <= 1, f* = 0.

    R_N(h) := max { f(x_N) }        ("function value", Tsai et al. R_n)
    G_N(h) := max { ||grad f(x_N)||^2 }   ("squared gradient norm", their G_n)

Index mapping to the literature: Zhang-Lee-Du-Chen (arXiv:2411.17668) index
iterates from x_1, so their stopping time T corresponds to N = T - 1 gradient
steps here.  Both comparator and candidate are evaluated through the SAME
routine, so the offset cancels in every ratio; it only shifts fitted exponents
by O(1/N), and both fits are reported where that matters.

PEP formulation (Taylor-Hendrickx-Glineur 2017 interpolation, exact)
-------------------------------------------------------------------
Basis of the Gram matrix G (size N+2): column 0 is (x_0 - x*), column 1+i is
g_i = grad f(x_i) for i = 0..N.  With u_i the coordinates of (x_i - x*) and
v_i = e_{1+i} the coordinates of g_i, the 1-smooth convex interpolation
conditions over the index set {0..N} u {*} read, for every ordered pair i != j,

    f_j - f_i + v_j^T G (u_i - u_j) + 0.5 (v_i - v_j)^T G (v_i - v_j) <= 0 .

That is linear in (G, f) for fixed h, and the whole system is assembled as one
vectorised sparse constraint for speed.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import cvxpy as cp
import numpy as np
import scipy.sparse as sp

RHO = 1.0 + math.sqrt(2.0)  # silver ratio
LOG2_RHO = math.log2(RHO)  # ~ 1.2715533


# --------------------------------------------------------------------------
# Published stepsize schedules
# --------------------------------------------------------------------------
def phi(x: float, y: float) -> float:
    """Join stepsize of Zhang & Jiang (2024), eq. (10) of arXiv:2411.17668."""
    return (-(x + y) + math.sqrt((x + y + 2.0) ** 2 + 4.0 * (x + 1.0) * (y + 1.0))) / 2.0


def concat(s: list[float], r: list[float]) -> list[float]:
    """concat(s, r) = [s, phi(sum s, sum r), r]  -- eq. (11)."""
    return [*list(s), phi(float(sum(s)), float(sum(r))), *list(r)]


def silver_schedule(order: int) -> list[float]:
    """i-th order silver stepsize schedule (Altschuler & Parrilo), length 2^i - 1.

    Definition 5 of arXiv:2411.17668: sbar_0 = [], sbar_i = concat(sbar_{i-1}, sbar_{i-1}).
    """
    s: list[float] = []
    for _ in range(order):
        s = concat(s, s)
    return s


def silver_prefix(n: int) -> list[float]:
    """First n entries of the limiting silver schedule (each sbar_i is a prefix)."""
    order = 1
    while 2**order - 1 < n:
        order += 1
    return silver_schedule(order)[:n]


def zldc_anytime_schedule(n: int, c: float | None = None) -> list[float]:
    """First n entries of the Zhang-Lee-Du-Chen anytime schedule, arXiv:2411.17668 sec. 3.1.

    c = log2(rho) gives the O(T^{-2 log2 rho / (1 + log2 rho)}) ~ O(T^{-1.119}) anytime rate.
    Building blocks: repeat the j-th order silver schedule k_j = floor(2 * 2^{c j}) times,
    then fold everything together with the concatenation operator (12).

    Note: eq. (15) of the paper prints ``M_i = sum_{j=1}^{i} k_i``; the index is a
    typo for ``k_j`` (otherwise M_i would not be the running total the construction
    needs).  ``k_j`` is used here.
    """
    if c is None:
        c = LOG2_RHO
    out: list[float] = []
    j = 0
    while len(out) < n:
        j += 1
        k_j = math.floor(2.0 * 2.0 ** (c * j))
        block = silver_schedule(j)
        for _ in range(k_j):
            out = concat(out, block)
            if len(out) >= n:
                break
    return out[:n]


def zldc_concat_endpoints(n: int, c: float | None = None) -> list[int]:
    """Lengths t_i of the partial concatenations s-hat_i inside the first n entries.

    Only at these lengths does the ZLDC schedule claim primitivity (Lemma 4); an
    arbitrary prefix in between is not claimed to be primitive.
    """
    if c is None:
        c = LOG2_RHO
    out: list[float] = []
    ends: list[int] = []
    j = 0
    while len(out) < n:
        j += 1
        k_j = math.floor(2.0 * 2.0 ** (c * j))
        block = silver_schedule(j)
        for _ in range(k_j):
            out = concat(out, block)
            ends.append(len(out))
            if len(out) >= n:
                break
    return [e for e in ends if e <= n]


def constant_schedule(n: int, h: float = 1.0) -> list[float]:
    return [h] * n


# --------------------------------------------------------------------------
# PEP problem assembly
# --------------------------------------------------------------------------
@dataclass
class PEPResult:
    value: float
    grad: np.ndarray | None
    status: str


class GDPep:
    """Exact PEP for N steps of GD on 1-smooth convex functions.

    The sparsity pattern of the interpolation system is fixed by N; only the
    numerical coefficients depend on h.  The system is rebuilt per solve (cheap
    relative to the SDP itself) and handed to cvxpy as one vectorised constraint.
    """

    def __init__(self, n_steps: int, objective: str = "R"):
        if objective not in ("R", "G"):
            raise ValueError("objective must be 'R' or 'G'")
        self.n = int(n_steps)
        self.objective = objective
        self.dim = self.n + 2  # Gram dimension
        # ordered pairs (i, j), i != j, over {0..n} u {star}; star encoded as n+1
        self.star = self.n + 1
        self.pairs = [(i, j) for i in range(self.n + 2) for j in range(self.n + 2) if i != j]

    # -- coordinate helpers -------------------------------------------------
    def _u(self, i: int, h: np.ndarray) -> np.ndarray:
        """Coordinates of x_i - x* in the Gram basis (zero for i == star)."""
        u = np.zeros(self.dim)
        if i == self.star:
            return u
        u[0] = 1.0
        for k in range(i):
            u[1 + k] = -h[k]
        return u

    def _v(self, i: int) -> np.ndarray:
        v = np.zeros(self.dim)
        if i != self.star:
            v[1 + i] = 1.0
        return v

    def _build(self, h: np.ndarray) -> tuple[sp.csr_matrix, sp.csr_matrix]:
        """Return (A, F): constraint = F @ f + A @ vec(G) <= 0, row per pair."""
        m = len(self.pairs)
        d = self.dim
        rows_a: list[int] = []
        cols_a: list[int] = []
        vals_a: list[float] = []
        rows_f: list[int] = []
        cols_f: list[int] = []
        vals_f: list[float] = []

        us = [self._u(i, h) for i in range(self.n + 2)]

        for r, (i, j) in enumerate(self.pairs):
            # f_j - f_i   (f_star == 0, not a variable)
            if j != self.star:
                rows_f.append(r)
                cols_f.append(j)
                vals_f.append(1.0)
            if i != self.star:
                rows_f.append(r)
                cols_f.append(i)
                vals_f.append(-1.0)

            # A = sym(v_j (u_i - u_j)^T) + 0.5 (v_i - v_j)(v_i - v_j)^T
            mat = np.zeros((d, d))
            if j != self.star:
                du = us[i] - us[j]
                col = 1 + j
                mat[col, :] += 0.5 * du
                mat[:, col] += 0.5 * du
            dv = self._v(i) - self._v(j)
            mat += 0.5 * np.outer(dv, dv)

            nz = np.nonzero(mat)
            for a, b in zip(nz[0], nz[1], strict=True):
                rows_a.append(r)
                cols_a.append(a * d + b)
                vals_a.append(mat[a, b])

        amat = sp.csr_matrix((vals_a, (rows_a, cols_a)), shape=(m, d * d))
        fmat = sp.csr_matrix((vals_f, (rows_f, cols_f)), shape=(m, self.n + 1))
        return amat, fmat

    # -- solve --------------------------------------------------------------
    def solve_primitivity(self, h: np.ndarray, solver: str = "CLARABEL") -> float:
        """Worst case of the Zhang & Jiang "primitive schedule" potential.

        Definition 2 of arXiv:2411.17668 says a schedule alpha_{1:k-1} is *primitive* iff

            A_k (f_k - f*) + C_k ||g_k||^2 + 0.5 ||x_k - x*||^2  <=  0.5 ||x_1 - x*||^2

        with A_k the sum of the stepsizes and C_k = A_k (A_k + 1) / 2.  That is a
        worst-case statement over the whole function class, so it is exactly a PEP with
        a different linear objective -- which makes it an INDEPENDENT check on the
        reconstruction of ``phi``/``concat`` here: a wrong join stepsize would break
        primitivity, and this returns the amount by which it breaks.

        Returns the maximum of the left-hand side under ||x_0 - x*||^2 <= 1, so the
        schedule is primitive iff the returned value is <= 0.5 (up to solver tolerance).
        """
        h = np.asarray(h, dtype=float)
        amat, fmat = self._build(h)
        a_k = float(np.sum(h))
        c_k = a_k * (a_k + 1.0) / 2.0
        u_n = self._u(self.n, h)

        gram = cp.Variable((self.dim, self.dim), PSD=True)
        fvals = cp.Variable(self.n + 1)
        interp = fmat @ fvals + amat @ cp.vec(gram, order="C") <= 0
        init = gram[0, 0] <= 1.0

        obj = (
            a_k * fvals[self.n]
            + c_k * gram[1 + self.n, 1 + self.n]
            + 0.5 * cp.quad_form(u_n, gram, assume_PSD=True)
        )
        prob = cp.Problem(cp.Maximize(obj), [interp, init])
        try:
            prob.solve(solver=solver, tol_gap_abs=1e-9, tol_gap_rel=1e-9, max_iter=2000)
        except Exception:
            prob.solve(solver="SCS")
        if prob.status not in ("optimal", "optimal_inaccurate"):
            return float("nan")
        return float(prob.value)

    def solve(
        self,
        h: np.ndarray,
        want_grad: bool = False,
        solver: str = "CLARABEL",
        tol: float = 1e-9,
    ) -> PEPResult:
        h = np.asarray(h, dtype=float)
        if h.size != self.n:
            raise ValueError(f"expected {self.n} stepsizes, got {h.size}")
        amat, fmat = self._build(h)

        gram = cp.Variable((self.dim, self.dim), PSD=True)
        fvals = cp.Variable(self.n + 1)

        interp = fmat @ fvals + amat @ cp.vec(gram, order="C") <= 0
        init = gram[0, 0] <= 1.0

        if self.objective == "R":
            obj = fvals[self.n]
        else:
            obj = gram[1 + self.n, 1 + self.n]

        prob = cp.Problem(cp.Maximize(obj), [interp, init])
        # WHY: default solver tolerances (~1e-8) put the finite-difference check of the
        # analytic gradient right at its own noise floor; tightening here makes the
        # substrate checks measure the implementation rather than the solver's slack.
        #
        # WHY the fallback chain: an outer search wanders into badly conditioned
        # schedules (very large steps) where CLARABEL raises SolverError.  That is a
        # statement about one trial point, not about the claim -- it must not abort the
        # run, and it must not be silently scored as a good value either.  A failed
        # point returns NaN, which the optimiser maps to a large penalty.
        attempts: list[tuple[str, dict]] = []
        if solver == "CLARABEL":
            attempts = [
                (
                    "CLARABEL",
                    {"tol_gap_abs": tol, "tol_gap_rel": tol, "tol_feas": tol, "max_iter": 2000},
                ),
                (
                    "CLARABEL",
                    {"tol_gap_abs": 1e-7, "tol_gap_rel": 1e-7, "tol_feas": 1e-7, "max_iter": 4000},
                ),
                ("SCS", {}),
            ]
        else:
            attempts = [(solver, {})]

        ok = False
        for name, kwargs in attempts:
            try:
                prob.solve(solver=name, **kwargs)
            except Exception:
                continue
            if prob.status in ("optimal", "optimal_inaccurate"):
                ok = True
                break
        if not ok:
            return PEPResult(float("nan"), None, str(prob.status))

        grad = None
        if want_grad:
            if interp.dual_value is None or gram.value is None:
                return PEPResult(float("nan"), None, "no_dual")
            lam = np.asarray(interp.dual_value).ravel()
            gval = np.asarray(gram.value)
            grad = self._gradient(lam, gval)
        return PEPResult(float(prob.value), grad, prob.status)

    def _gradient(self, lam: np.ndarray, gram: np.ndarray) -> np.ndarray:
        """d(value)/d h_k from the optimal primal-dual pair.

        Only ``v_j^T G (u_i - u_j)`` depends on h, and
        d(u_i)/d h_k = -e_{1+k} * 1[k < i].  With v_j = e_{1+j},
        d/dh_k of the (i,j) constraint expression is
        -(1[k<i] - 1[k<j]) * G[1+j, 1+k].
        Envelope theorem for max_z c^T z s.t. A(h) z <= 0 gives
        dV/dh_k = -sum_c lam_c * d(expr_c)/dh_k.
        """
        n = self.n
        grad = np.zeros(n)
        for r, (i, j) in enumerate(self.pairs):
            lc = lam[r]
            if lc == 0.0 or j == self.star:
                continue
            ii = n + 1 if i == self.star else i  # star has u = 0 -> no k < star
            i_eff = 0 if i == self.star else ii
            j_eff = 0 if j == self.star else j
            lo, hi = (j_eff, i_eff) if i_eff > j_eff else (i_eff, j_eff)
            sign = 1.0 if i_eff > j_eff else -1.0
            if lo == hi:
                continue
            for k in range(lo, hi):
                grad[k] += lc * sign * gram[1 + j, 1 + k]
        return grad


def rn_value(h, objective: str = "R", solver: str = "CLARABEL") -> float:
    h = np.asarray(h, dtype=float)
    pep = GDPep(h.size, objective=objective)
    return pep.solve(h, solver=solver).value
