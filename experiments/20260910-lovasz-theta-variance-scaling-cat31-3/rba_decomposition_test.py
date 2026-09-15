"""RBA decomposition test -- R(S) = R0(S) + R1(S) + R2(S) on the central layer.

Reduced (frequency-domain) Lovasz LP for random dense circulant graphs on Z_n,
n odd prime, at the central layer m=(n-1)//2, q=m//2, F=m-q:

    max  w_0
    s.t. w_k >= 0  (k = 0..m),   sum_{k=0}^m w_k = 1,
         w_0 + sum_{k=1}^m w_k cos(2 pi e k / n) = 0   for every e in S,  |S| = q.

This is NOT the "time-domain primal" LP of 20260909-.../run.py::theta_via_lp
(Table 1 of arXiv:2603.29571); it is the frequency-domain reduced-support
formulation specified fresh for this task.  They are, however, provably the same
optimum up to the normalization theta(G) = n * w_0: with
x(e) = w_0 + sum_k w_k cos(2 pi e k/n) one has x(0) = sum_k w_k = 1, the Fourier
transform of x is w/2 >= 0, x vanishes on the connection set S, and
sum_e x(e) = n*w_0.  The substrate gate checks exactly that against
theta_via_lp (imported unchanged) on small primes.

Definitions (verbatim from the task spec):

  support = {k in 1..m : w_k > tol}, |support| = q at the parent optimum
  p_k     = w_k/(1-w_0) on the support        (sum_k p_k = 1)
  s2      = sum p_k^2,  s3 = sum p_k^3
  I(S)    = q * s2        ( = 1 + CV^2 of p over its support )
  D(S)    = q^2 (s3 - s2^2)
  tau     = w_0/(1-w_0)
  m_j     = sum_k p_k cos(2 pi j k/n)
  g_j     = tau + m_j     ( = 0 for j in S, by the LP equalities )
  A_j     = sum_k p_k^2 [cos(2 pi j k/n) - m_j]
  u_j     = p_{S+j} - p_S (both embedded in R^m, zero-filled)

  R0 = I(S)/q = s2
  R1 = 2(q+1) E_j[ <p,u_j> + g_j A_j ]
  R2 = (q+1) E_j[ ||u_j||^2 ]
  R  = R0 + R1 + R2

Mandatory identities, checked for EVERY parent:

  (bulk)    E_{j not in S}[ g_j A_j ] = (n/(4F))(s3 - s2^2) = (n/(4 F q^2)) D(S)
  (delta-I) I(S+j) - I(S) = I(S)/q + 2(q+1)<p,u_j> + (q+1)||u_j||^2

The bulk identity is exact (orthogonality of cos over j=1..m, together with
g_e = 0 for e in S), so it doubles as a check that the parent LP really sits at
an optimal vertex.  g_j/A_j need no LP, so the bulk mean is exactly available for
free; hence two variants of R1 are reported:

  R1 (subset) -- the literal spec: E_j over the SELECTED children, both terms
  R1_bulk     -- E_j over selected children for <p,u_j>, EXACT all-free-j mean
                 for the g_j A_j term

Same expectation (j uniform among free orbits); R1_bulk merely removes sampling
noise on an exactly-computable term.  Spec sanity check 4 is an identity for the
BULK variant, so it is verified there to machine precision; the subset-vs-bulk
gap is reported separately as a sampling diagnostic, not an error.

Outputs are all prefixed rba_ so they cannot collide with concurrent work.
"""

from __future__ import annotations

import os

# Pin every numerical library to ONE thread BEFORE numpy/scipy are imported.
# A first attempt at this sweep ran 22 worker processes that each let HiGHS/BLAS
# spawn their own thread pools; every worker was killed abruptly (BrokenProcessPool,
# no worker-side traceback) partway through n=1021 and n=4093.  One thread per
# worker process, parallelism only across parents.
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")

import argparse  # noqa: E402
import csv  # noqa: E402
import importlib.util  # noqa: E402
import json  # noqa: E402
import time  # noqa: E402
from concurrent.futures import ProcessPoolExecutor  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
from scipy.optimize import linprog  # noqa: E402

HERE = Path(__file__).resolve().parent
RUN_PY = HERE.parent / "20260909-lovasz-theta-random-circulant-graphs" / "run.py"

SEED_BASE = 4310000
SUPPORT_TOLS = (1e-10, 1e-9, 1e-8)
PRIMARY_TOL = 1e-9


class ReducedLP:
    """Frequency-domain reduced Lovasz LP on Z_n (n odd prime)."""

    def __init__(self, n, method="highs"):
        self.n = n
        self.m = (n - 1) // 2
        self.method = method
        self.cosval = np.cos(2.0 * np.pi * np.arange(n) / n)
        self.ks = np.arange(1, self.m + 1)

    def cos_row(self, e):
        return self.cosval[(e * self.ks) % self.n]

    def solve(self, S):
        m = self.m
        nS = len(S)
        A = np.empty((nS + 1, m + 1))
        A[0, :] = 1.0
        for i, e in enumerate(S):
            A[i + 1, 0] = 1.0
            A[i + 1, 1:] = self.cos_row(int(e))
        b = np.zeros(nS + 1)
        b[0] = 1.0
        c = np.zeros(m + 1)
        c[0] = -1.0
        t0 = time.perf_counter()
        res = linprog(c, A_eq=A, b_eq=b, bounds=(0, None), method=self.method)
        dt = time.perf_counter() - t0
        if not res.success:
            return None, int(res.status), dt, float("nan"), float("nan")
        w = res.x
        max_resid = float(np.abs(A[1:] @ w).max()) if nS else 0.0
        sum_err = float(abs(w.sum() - 1.0))
        return w, 0, dt, max_resid, sum_err


def support_counts(w_tail):
    return {t: int((w_tail > t).sum()) for t in SUPPORT_TOLS}


def p_from_w(w, tol=PRIMARY_TOL):
    w0 = float(w[0])
    tail = w[1:]
    p = np.where(tail > tol, tail, 0.0) / (1.0 - w0)
    return p, w0


def process_parent(task):
    (n, q, seed, parent_id, n_children, full_j, method, fixed_j) = task

    lp = ReducedLP(n, method=method)
    m = lp.m
    F = m - q
    rng = np.random.default_rng(seed)

    pool = np.arange(1, m + 1)
    if fixed_j is not None:
        pool = pool[pool != fixed_j]
    S = np.sort(rng.choice(pool, size=q, replace=False))

    w, status, t_par, max_resid, sum_err = lp.solve(S)
    rec = {
        "n": n, "q": q, "F": F, "seed": seed, "parent_id": parent_id,
        "method": method,
        "solver_status": status, "solve_time_parent": t_par,
        "fourier_resid_parent": max_resid, "sum_w_err_parent": sum_err,
        "full_j": bool(full_j), "fixed_j": -1 if fixed_j is None else fixed_j,
    }
    if w is None:
        rec["ok"] = False
        return rec

    tail = w[1:]
    sc = support_counts(tail)
    rec["support_1em10"] = sc[1e-10]
    rec["support_1em9"] = sc[1e-9]
    rec["support_1em8"] = sc[1e-8]
    rec["min_w"] = float(tail.min())
    rec["ambiguous_support"] = bool(len(set(sc.values())) > 1 or sc[PRIMARY_TOL] != q)

    p, w0 = p_from_w(w)
    rec["w0"] = float(w0)
    rec["theta_like_value"] = float(n * w0)

    supp = np.nonzero(p)[0]
    pk = p[supp]
    s2 = float(np.dot(pk, pk))
    s3 = float(np.dot(pk * pk, pk))
    I_S = q * s2
    D_S = q * q * (s3 - s2 * s2)
    tau = float(w0 / (1.0 - w0))
    rec.update({"I": I_S, "D": D_S, "s2": s2, "s3": s3, "tau": tau, "R0": s2})

    orbit = supp + 1
    m_all = np.empty(m)
    Acos_all = np.empty(m)
    pk2 = pk * pk
    BLK = 256
    for a in range(0, m, BLK):
        jb = np.arange(a + 1, min(a + BLK, m) + 1)
        C = lp.cosval[(np.outer(jb, orbit)) % n]
        m_all[a:a + len(jb)] = C @ pk
        Acos_all[a:a + len(jb)] = C @ pk2
    g_all = tau + m_all
    A_all = Acos_all - m_all * s2

    rec["max_abs_g_on_S"] = float(np.abs(g_all[S - 1]).max())

    free = np.setdiff1d(np.arange(1, m + 1), S)
    gA_free = g_all[free - 1] * A_all[free - 1]
    bulk_obs = float(gA_free.mean())
    bulk_pred = (n / (4.0 * F)) * (s3 - s2 * s2)
    rec["bulk_gA_observed"] = bulk_obs
    rec["bulk_gA_predicted"] = bulk_pred
    rec["bulk_identity_error"] = float(abs(bulk_obs - bulk_pred))

    if fixed_j is not None:
        chosen = np.array([fixed_j])
    elif full_j:
        chosen = free.copy()
    else:
        chosen = rng.choice(free, size=min(n_children, F), replace=False)

    inner, unorm, gA_sel, dI_err, ctimes = [], [], [], [], []
    child_fail = 0
    child_amb = 0
    child_resid = 0.0
    for j in chosen:
        j = int(j)
        Sc = np.sort(np.append(S, j))
        wc, _st, tc, rsd, _ = lp.solve(Sc)
        ctimes.append(tc)
        if wc is None:
            child_fail += 1
            continue
        child_resid = max(child_resid, rsd)
        scc = support_counts(wc[1:])
        if len(set(scc.values())) > 1 or scc[PRIMARY_TOL] != q + 1:
            child_amb += 1
        pc, _ = p_from_w(wc)
        u = pc - p
        ip = float(np.dot(p, u))
        un = float(np.dot(u, u))
        inner.append(ip)
        unorm.append(un)
        gA_sel.append(float(g_all[j - 1] * A_all[j - 1]))
        I_child = (q + 1) * float(np.dot(pc, pc))
        pred = I_S / q + 2.0 * (q + 1) * ip + (q + 1) * un
        dI_err.append(abs((I_child - I_S) - pred))

    rec["num_children"] = len(inner)
    rec["child_failures"] = child_fail
    rec["child_ambiguous"] = child_amb
    rec["fourier_resid_child_max"] = child_resid
    rec["mean_solve_time_child"] = float(np.mean(ctimes)) if ctimes else float("nan")
    rec["delta_I_identity_error"] = float(max(dI_err)) if dI_err else float("nan")

    if not inner:
        rec["ok"] = False
        return rec

    inner = np.asarray(inner)
    unorm = np.asarray(unorm)
    gA_sel = np.asarray(gA_sel)

    r1_child = 2.0 * (q + 1) * (inner + gA_sel)
    r2_child = (q + 1) * unorm
    rec["mean_R1"] = float(r1_child.mean())
    rec["mean_R2"] = float(r2_child.mean())
    rec["R1_plus_R2"] = rec["mean_R1"] + rec["mean_R2"]
    rec["R_total"] = s2 + rec["R1_plus_R2"]
    nc = len(r1_child)
    rec["std_child_R1"] = float(r1_child.std(ddof=1)) if nc > 1 else 0.0
    rec["std_child_R2"] = float(r2_child.std(ddof=1)) if nc > 1 else 0.0
    rec["std_child_Rsum"] = float((r1_child + r2_child).std(ddof=1)) if nc > 1 else 0.0
    rec["mean_inner"] = float(inner.mean())
    rec["mean_unorm"] = float(unorm.mean())

    # Sanity check 1: for a full-j audit parent, also record what a RANDOM
    # subset of n_children of the same children would have estimated, so the
    # subset estimator can be compared against the exact all-free-j mean on the
    # SAME parent (not merely against other parents).
    if full_j and nc > n_children:
        rs = np.random.default_rng(seed + 777)
        idx = rs.choice(nc, size=n_children, replace=False)
        rec["audit_sub_size"] = int(n_children)
        rec["audit_sub_R1"] = float(r1_child[idx].mean())
        rec["audit_sub_R2"] = float(r2_child[idx].mean())
        rec["audit_sub_R_total"] = float(s2 + r1_child[idx].mean() + r2_child[idx].mean())

    rec["mean_R1_bulk"] = float(2.0 * (q + 1) * (inner.mean() + bulk_pred))
    rec["R1_plus_R2_bulk"] = rec["mean_R1_bulk"] + rec["mean_R2"]
    rec["R_total_bulk"] = s2 + rec["R1_plus_R2_bulk"]

    mean_dI = float((s2 + 2.0 * (q + 1) * inner + (q + 1) * unorm).mean())
    alt = mean_dI + (q + 1) / (2.0 * q) * (n / (F * q)) * D_S
    rec["check4_error"] = float(abs(alt - rec["R_total_bulk"]))
    rec["subset_vs_bulk_gap"] = float(abs(rec["R_total"] - rec["R_total_bulk"]))
    rec["ok"] = True
    return rec


def substrate_gate(method="highs-ipm"):
    """Positive control: n*w_0 of THIS reduced LP must equal theta_via_lp of the
    project's own (unchanged, different-formulation) time-domain primal LP."""
    spec = importlib.util.spec_from_file_location("h1run", str(RUN_PY))
    h1 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(h1)
    rng = np.random.default_rng(12345)
    rows = []
    for n in (11, 13, 17, 23, 31, 37, 41, 47):
        m = (n - 1) // 2
        q = m // 2
        S = np.sort(rng.choice(np.arange(1, m + 1), size=q, replace=False))
        for meth in dict.fromkeys([method, "highs"]):
            lp = ReducedLP(n, method=meth)
            w, _st, _, resid, _ = lp.solve(S)
            c = np.zeros(n)
            for e in S:
                c[int(e)] = 1.0
                c[n - int(e)] = 1.0
            th = float(h1.theta_via_lp(c))
            rows.append({
                "n": n, "q": q, "method": meth, "n_w0": float(n * w[0]),
                "theta_via_lp": th, "abs_diff": float(abs(n * w[0] - th)),
                "support": int((w[1:] > PRIMARY_TOL).sum()),
                "max_fourier_resid": resid,
            })
    return rows


def _append_jsonl(path, rec):
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec) + "\n")


def _load_jsonl(path):
    if not path.exists():
        return []
    out = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def build_tasks(n, parents, children, method, seed_offset, full_j_parents, fixed_j):
    m = (n - 1) // 2
    q = m // 2
    tasks = []
    for i in range(parents):
        tasks.append((n, q, SEED_BASE + seed_offset + n * 1000 + i, i, children,
                      False, method, fixed_j))
    for i in range(full_j_parents):
        tasks.append((n, q, SEED_BASE + seed_offset + n * 1000 + 900000 + i,
                      900000 + i, children, True, method, None))
    return tasks


def run_tasks(tasks, jsonl, workers, batch_mult=2, label=""):
    """Batched pools + per-record checkpointing + one serial retry per batch.

    A single ProcessPoolExecutor spanning the whole sweep loses EVERY completed
    result when one worker dies (that is exactly what happened on the first
    attempt).  Here each batch gets a fresh pool, every finished record is
    appended to `jsonl` immediately, and a batch whose pool breaks is retried
    once serially before being reported as failed.
    """
    done_ids = {(r["n"], r["parent_id"], r["seed"]) for r in _load_jsonl(jsonl)}
    todo = [t for t in tasks if (t[0], t[3], t[2]) not in done_ids]
    if len(todo) < len(tasks):
        print(
            f"  [{label}] resuming: {len(tasks) - len(todo)}/{len(tasks)} already done",
            flush=True,
        )
    t0 = time.perf_counter()
    bs = max(1, workers * batch_mult)
    failures = 0
    for a in range(0, len(todo), bs):
        batch = todo[a:a + bs]
        try:
            with ProcessPoolExecutor(max_workers=workers) as ex:
                for r in ex.map(process_parent, batch):
                    _append_jsonl(jsonl, r)
        except Exception as exc:
            print(
                f"  [{label}] pool broke ({type(exc).__name__}) -- "
                f"retrying {len(batch)} tasks serially",
                flush=True,
            )
            got = {(r["n"], r["parent_id"], r["seed"]) for r in _load_jsonl(jsonl)}
            for t in batch:
                if (t[0], t[3], t[2]) in got:
                    continue
                try:
                    _append_jsonl(jsonl, process_parent(t))
                except Exception as exc2:
                    failures += 1
                    print(f"  [{label}] task {t[3]} FAILED: {exc2!r}", flush=True)
        print(
            f"  [{label}] {min(a + bs, len(todo))}/{len(todo)}  "
            f"elapsed={time.perf_counter() - t0:.0f}s",
            flush=True,
        )
    return time.perf_counter() - t0, failures


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, nargs="+", required=True)
    ap.add_argument("--parents", type=int, nargs="+", required=True)
    ap.add_argument("--children", type=int, nargs="+", required=True)
    ap.add_argument("--full-j-parents", type=int, nargs="+", default=None)
    ap.add_argument("--method", default="highs-ipm")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--seed-offset", type=int, default=0)
    ap.add_argument("--fixed-j", type=int, default=None)
    ap.add_argument("--tag", default="")
    ap.add_argument("--skip-gate", action="store_true")
    args = ap.parse_args()

    tag = "_" + args.tag if args.tag else ""
    out_parent = HERE / ("rba_parent_level" + tag + ".csv")
    jsonl = HERE / ("rba_parent_level" + tag + ".jsonl")
    out_json = HERE / "metrics" / ("rba_decomposition" + tag + ".json")
    out_json.parent.mkdir(exist_ok=True)

    gate = [] if args.skip_gate else substrate_gate(args.method)
    if gate:
        worst = max(r["abs_diff"] for r in gate)
        print(f"[substrate gate] max |n*w0 - theta_via_lp| = {worst:.3e}", flush=True)
        if worst > 1e-8:
            raise SystemExit("SUBSTRATE GATE FAILED")

    fjp = args.full_j_parents or [0] * len(args.n)
    timing = {}
    total_fail = 0
    for n, P, C, FJ in zip(args.n, args.parents, args.children, fjp):
        tasks = build_tasks(n, P, C, args.method, args.seed_offset, FJ, args.fixed_j)
        el, nf = run_tasks(tasks, jsonl, args.workers, label=f"n={n}")
        timing[str(n)] = el
        total_fail += nf
        print(f"[n={n}] stage done in {el:.1f}s ({nf} failures)", flush=True)

    all_recs = _load_jsonl(jsonl)
    keys = sorted({k for r in all_recs for k in r})
    with open(out_parent, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for r in all_recs:
            w.writerow({k: r.get(k, "") for k in keys})
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump({"substrate_gate": gate, "config": vars(args),
                   "elapsed_by_n": timing, "n_records": len(all_recs),
                   "task_failures": total_fail,
                   "thread_env": {v: os.environ.get(v) for v in
                                  ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS",
                                   "MKL_NUM_THREADS")}}, f, indent=2)
    print(
        f"wrote {out_parent} ({len(all_recs)} records, {total_fail} failures)",
        flush=True,
    )


if __name__ == "__main__":
    main()
