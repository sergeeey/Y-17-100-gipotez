# ruff: noqa
"""Run the separate verifier's exact checks over every built tuple of the given jsonl files; print rank histogram."""

import collections
import json
import sys

sys.set_int_max_str_digits(0)
from pathlib import Path

import exact_certify as ec

hist = collections.Counter()
best = 0
for path in sys.argv[1:]:
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        if not row["blocks"]:
            continue
        blocks = [[int(v) for v in x] for x in row["blocks"]]
        ec.build_blocks = lambda k, r, s, seed_, lll, b=blocks: (b, [0] * s)
        res = ec.certify(20, 2, 16, row["seed"], True)
        rk = min(res["rank_mod_p"])
        hist[(rk, res["qfim_det_nonzero"], res["pcc_exact_zero"])] += 1
        best = max(best, rk)
        if res["exact_certified_dimVperp_lt_d"]:
            print("PASS-CANDIDATE seed", row["seed"], flush=True)
print("rank histogram (rank_mod_p, qfim_nonzero, pcc_exact):", dict(hist), "best", best, "need 463")
