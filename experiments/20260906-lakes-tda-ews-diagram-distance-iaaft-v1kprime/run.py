"""run.py — H-B3-1k: IAAFT-surrogate null combined with diagram-distance (the "V1k'" cell) --
fourth and last cell of the {total persistence, diagram-distance} x {AR(1), IAAFT} design.

Thin wrapper around the sibling V1 experiment's already-tested `cmd_run` -- reuses ALL of its
data loading, null-generation, and verdict logic unchanged, passing BOTH `surrogate_fn` and
`tda_stat_fn` together. Relative to H-B3-1j (AR(1)+diagram-distance), the ONE assumption changed
is the null model, per the Minimal Relaxation Rule.
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
        surrogate_fn=v1.obrien.iaaft_surrogate,  # changed from H-B3-1j's AR(1)
        detection_rule_label="IAAFT-surrogate + Wasserstein diagram-distance-from-baseline",
        write_output=False,
        tda_stat_fn=v1.obrien.betti1_diagram_distance_series,  # unchanged from H-B3-1j
    )
    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    cmd_run()
