"""run.py — H-B3-1j: diagram-to-baseline-diagram distance (Wasserstein-2) instead of a scalar
persistence summary -- the "hard branch" named in H-B3-1g's and B3-MAY-TDA's own next-step notes.

Thin wrapper around the sibling V1 experiment's already-tested `cmd_run` -- reuses ALL of its
data loading, null-generation, and verdict logic unchanged, passing only `tda_stat_fn` (the ONE
assumption changed relative to the scalar-summary family: the TDA statistic itself is now a
diagram distance, not a diagram scalar). Null model (AR(1)) is unchanged from V1, isolating the
statistic-family question from the null-model question already explored exhaustively.
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
    # same guard as every prior V1-family variant.
    out = v1.cmd_run(
        surrogate_fn=v1.obrien.ar1_surrogate,  # unchanged from V1 -- isolates statistic question
        detection_rule_label="AR(1)-surrogate + Wasserstein diagram-distance-from-baseline",
        write_output=False,
        tda_stat_fn=v1.obrien.betti1_diagram_distance_series,
    )
    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    cmd_run()
