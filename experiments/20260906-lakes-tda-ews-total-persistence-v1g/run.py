"""run.py — H-B3-1g: same detection machinery as V1 (AR(1)-surrogate null), but a DIFFERENT
topological invariant -- Betti-1 TOTAL PERSISTENCE instead of persistence ENTROPY. The "hard
branch" named in H-B3-1f's decision.md, attempted directly.

Thin wrapper around the sibling V1 experiment's already-tested `cmd_run` -- reuses ALL of its
data loading, null-generation, and verdict logic unchanged, passing only
`tda_stat_fn=obrien.betti1_total_persistence_series` (the ONE assumption changed from V1, per
the Minimal Relaxation Rule). No pipeline logic is duplicated here.
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
    # WHY write_output=False: v1.cmd_run() would otherwise write to V1's OWN metrics/run.json --
    # same guard as V1'/V2', see tests/test_v1prime_does_not_overwrite_v1_metrics.py.
    out = v1.cmd_run(
        surrogate_fn=v1.obrien.ar1_surrogate,  # unchanged from V1 -- isolates invariant question
        detection_rule_label="AR(1)-surrogate + total-persistence",
        write_output=False,
        tda_stat_fn=v1.obrien.betti1_total_persistence_series,
    )
    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    cmd_run()
