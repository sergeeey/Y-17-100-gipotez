"""run.py — H-B3-1e (V2'): detrend-then-IAAFT surrogate-null, re-run on the same 9 series as V1/V1'.

Thin wrapper around the sibling V1 experiment's already-tested `cmd_run` -- reuses ALL of its
data loading, analysis, and verdict logic unchanged, passing only `surrogate_fn=detrend_surrogate`
(the ONE assumption changed from V1', per the Minimal Relaxation Rule). No pipeline logic is
duplicated here.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
METRICS = HERE / "metrics"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


v1 = _load_module("v1_run", HERE.parent / "20260906-lakes-tda-ews-surrogate-null-v1" / "run.py")


def cmd_run() -> dict:
    # WHY write_output=False: v1.cmd_run() would otherwise write to V1's OWN metrics/run.json
    # (its historical REJECT result) -- same guard as V1' (H-B3-1d), see
    # tests/test_v1prime_does_not_overwrite_v1_metrics.py for the original catch.
    out = v1.cmd_run(
        surrogate_fn=v1.obrien.detrend_surrogate,
        detection_rule_label="detrend+IAAFT-surrogate",
        write_output=False,
    )
    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    cmd_run()
