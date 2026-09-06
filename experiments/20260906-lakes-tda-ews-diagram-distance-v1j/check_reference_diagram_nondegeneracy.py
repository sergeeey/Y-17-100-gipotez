"""check_reference_diagram_nondegeneracy.py -- reviewer-flagged P2 check (code review of this
experiment's commit): does betti1_diagram_distance_series's fixed REFERENCE diagram (the first
valid window's H1 diagram) actually have real H1 structure, or is it degenerate (empty/near-empty)?

If the reference diagram is degenerate, "distance from baseline" collapses toward measuring the
raw magnitude of each subsequent window's diagram alone -- numerically close to
betti1_total_persistence_series, undermining the "genuinely different detection FAMILY" framing
in claim.md. Cheap, fully verifiable against the real data already used in the 9-series run --
no new surrogate compute, just ONE ripser call per series (the first window only).
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np
import pyreadr
from ripser import ripser

HERE = Path(__file__).resolve().parent


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


obrien = _load_module(
    "obrien_lakes_run", HERE.parent / "20260906-may1972-tda-ews-obrienlakes" / "run.py"
)
peter = _load_module("peterlake_run", HERE.parent / "20260906-may1972-tda-ews-peterlake" / "run.py")


def reference_diagram_stats(x: np.ndarray, window: int) -> dict:
    w = x[:window]
    cloud = obrien.takens_embed(w, obrien.EMBED_DIM, obrien.EMBED_DELAY)
    dgms = ripser(cloud, maxdim=1)["dgms"][1]
    finite = dgms[np.isfinite(dgms[:, 1])]
    life = finite[:, 1] - finite[:, 0]
    life = life[life > 0]
    return {
        "n_bars": int(life.size),
        "total_persistence": float(life.sum()) if life.size else 0.0,
        "max_bar_length": float(life.max()) if life.size else 0.0,
    }


def main() -> dict:
    rdata = pyreadr.read_r(str(obrien.DATA))
    out = {}

    for lake_key, cfg in obrien.LAKES.items():
        _dates, pca1 = obrien.load_series(rdata, lake_key)
        n = len(pca1)
        window = round(obrien.WINDOW_FRAC * n)
        window = max(window, obrien.EMBED_DIM * obrien.EMBED_DELAY + 8)
        out[f"obrien_{lake_key}"] = reference_diagram_stats(pca1, window)

    for lake, role in peter.LAKES.items():
        for var in peter.VARIABLES:
            _season_time, x, _t = peter.load_daily_series(var, lake)
            n = len(x)
            window = round(obrien.WINDOW_FRAC * n)
            window = max(window, obrien.EMBED_DIM * obrien.EMBED_DELAY + 8)
            out[f"peterlake_{lake}_{var}"] = reference_diagram_stats(x, window)

    n_degenerate = sum(1 for v in out.values() if v["n_bars"] == 0)
    summary = {
        "per_series": out,
        "n_series": len(out),
        "n_degenerate_reference_diagrams": n_degenerate,
        "verdict": (
            "NON-DEGENERATE: all 9 reference diagrams have real H1 structure"
            if n_degenerate == 0
            else f"DEGENERATE: {n_degenerate}/9 reference diagrams have zero H1 bars -- "
            "the 'genuinely different family' framing needs qualification for those series"
        ),
    }
    print(json.dumps(summary, indent=2))
    return summary


if __name__ == "__main__":
    main()
