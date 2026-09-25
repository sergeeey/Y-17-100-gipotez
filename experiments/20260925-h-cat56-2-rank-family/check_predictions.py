# ruff: noqa: E501
"""Compare the F_p certificate outputs with the values registered in claim.md (integer equality, no tolerance).

Predicted dim V-perp = r^2 + max(s, 2kr - s r^2) + 1 (measured generic closed form, decision.md C-CEIL). The check is written
independently of fp_certify.py: it reads only the saved JSON and applies the registered formula.

Kinds (see claim.md and its two 2026-09-25 addenda):
  fire       registered: fires (dim V-perp < d), all flags true, value == formula
  below      registered: does not fire, all flags true, value == formula
  degenerate amended (s > s*, no admissible state): QFIM singular on both primes, F_p rank equals the value at s = s*.
             NOTE (reviewer item 2): singularity is FORCED here (last kernel dimension is s - 1 < s), so the QFIM_NONSINGULAR
             branch below cannot realistically fire; this kind is bookkeeping consistency, not an independent test.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

METRICS = (
    Path(__file__).resolve().parent.parent / "20260919-pcc-generic-quasipure-cat56-2" / "metrics"
)
PRIMES = {67108837, 67108777}

# (d, r, s, kind). r = 2, 3 firing rows already exist from commit 8813a33.
CONFIGS = [
    (22, 2, 16, "fire"),
    (23, 3, 12, "fire"),
    (31, 4, 13, "fire"),
    (41, 5, 14, "fire"),
    (31, 4, 12, "below"),
    (41, 5, 13, "below"),
    (23, 3, 11, "below"),
    (31, 4, 14, "degenerate"),
    (41, 5, 15, "degenerate"),
    (23, 3, 13, "degenerate"),
]


def formula(d: int, r: int, s: int) -> int:
    k = d - r
    return r * r + max(s, 2 * k * r - s * r * r) + 1


def lower_bound(d: int, r: int, s: int) -> int:
    k = d - r
    return r * r + max(s, 2 * k * r - s * r * r) + max(1, k * k - (s * (s - 1) // 2) * r * r)


def evaluate(d: int, r: int, s: int, kind: str, res: dict) -> tuple[list[str], int]:
    """Return (problems, predicted value) for one saved result dict; an empty problem list means OK."""
    runs = res["runs"]
    got = [x["dimVperp_mod_p"] for x in runs]
    qf = [x["qfim_det_nonzero_mod_p"] for x in runs]
    problems: list[str] = []
    if (res.get("d"), res.get("r"), res.get("s")) != (d, r, s):
        problems.append("LABEL_MISMATCH")
    if {x["p"] for x in runs} != PRIMES:
        problems.append("PRIME_MISMATCH")
    if not all(
        x["lyapunov_zero"] and x["pcc_zero"] and x["kernel_dims_equal_float_generic"] for x in runs
    ):
        problems.append("FLAG_FALSE")
    if kind in ("fire", "below"):
        pred = formula(d, r, s)
        if not all(qf):
            problems.append("QFIM_SINGULAR")
        if any(g < lower_bound(d, r, s) for g in got):
            problems.append("BELOW_LB(C-LB falsified or bug)")
        if any(g != pred for g in got):
            problems.append("PRED_MISMATCH")
        if all(g < d for g in got) != (kind == "fire"):
            problems.append("FIRE_MISMATCH")
    else:
        s_star = math.ceil(2 * (d - r) * r / (r * r + 1))
        pred = formula(d, r, s_star)
        if any(qf):
            problems.append("QFIM_NONSINGULAR(s*_is_max_reading_wrong)")
        if any(g != pred for g in got):
            problems.append("VALUE_NOT_AT_s*")
    return problems, pred


def main() -> int:
    bad = 0
    print("d   r  s   kind        pred  got(p1,p2)   qfim_nonzero(p1,p2)  verdict")
    for d, r, s, kind in CONFIGS:
        path = METRICS / f"fp_certify_d{d}_r{r}_s{s}.json"
        if not path.exists():
            print(f"{d:<3} {r}  {s:<3} {kind:<11} MISSING {path.name}")
            bad += 1
            continue
        res = json.loads(path.read_text(encoding="utf-8"))
        problems, pred = evaluate(d, r, s, kind, res)
        got = [x["dimVperp_mod_p"] for x in res["runs"]]
        qf = [x["qfim_det_nonzero_mod_p"] for x in res["runs"]]
        verdict = "OK" if not problems else ",".join(problems)
        bad += bool(problems)
        print(f"{d:<3} {r}  {s:<3} {kind:<11} {pred:<5} {got!s:<12} {qf!s:<20} {verdict}")
    print(
        "ALL REGISTERED / AMENDED PREDICTIONS HELD"
        if bad == 0
        else f"{bad} CONFIG(S) DID NOT MATCH"
    )
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
