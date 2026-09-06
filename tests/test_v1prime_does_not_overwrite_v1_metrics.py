"""Regression test for a real bug caught before the first V1' run: calling V1's `cmd_run()` from
inside the V1' experiment (to reuse its analysis logic) would, without a `write_output` guard,
overwrite V1's OWN `metrics/run.json` -- silently replacing its committed, historical REJECT
result with a re-run under a different surrogate model. `write_output=False` prevents this.

Uses monkeypatched (fast, synthetic) data loaders so this test does not re-run the real,
ripser-heavy 9-series pipeline.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

_V1_DIR = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "20260906-lakes-tda-ews-surrogate-null-v1"
)
_SPEC = importlib.util.spec_from_file_location("v1_run", _V1_DIR / "run.py")
v1 = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(v1)

V1_METRICS_FILE = _V1_DIR / "metrics" / "run.json"


def _fake_result(role: str) -> dict:
    return {
        "classical_ac1_crossing": None,
        "classical_var_crossing": None,
        "classical_earliest_crossing": None,
        "tda_betti_crossing": None,
        "tda_lead": None,
        "role": role,
        "n_points": 10,
        "false_positive": False,
    }


def test_write_output_false_does_not_touch_v1_own_metrics_file(monkeypatch):
    assert V1_METRICS_FILE.exists(), "V1's historical run.json must already exist for this test"
    before_bytes = V1_METRICS_FILE.read_bytes()
    before_mtime = V1_METRICS_FILE.stat().st_mtime_ns

    monkeypatch.setattr(
        v1,
        "run_obrien_lakes",
        lambda surrogate_fn=None, tda_stat_fn=None: {"o": _fake_result("positive")},
    )
    monkeypatch.setattr(
        v1,
        "run_peter_paul_lake",
        lambda surrogate_fn=None, tda_stat_fn=None: {"p": _fake_result("negative")},
    )

    result = v1.cmd_run(surrogate_fn=v1.obrien.iaaft_surrogate, write_output=False)

    assert isinstance(result, dict)
    assert V1_METRICS_FILE.read_bytes() == before_bytes, (
        "V1's own metrics/run.json was overwritten!"
    )
    assert V1_METRICS_FILE.stat().st_mtime_ns == before_mtime


def test_write_output_true_default_still_writes(monkeypatch, tmp_path):
    """Confirms the default (write_output=True, V1's own standalone `python run.py` behavior)
    is unchanged -- redirects METRICS to a tmp dir so this test doesn't touch the real file."""
    monkeypatch.setattr(v1, "METRICS", tmp_path)
    monkeypatch.setattr(
        v1,
        "run_obrien_lakes",
        lambda surrogate_fn=None, tda_stat_fn=None: {"o": _fake_result("positive")},
    )
    monkeypatch.setattr(
        v1,
        "run_peter_paul_lake",
        lambda surrogate_fn=None, tda_stat_fn=None: {"p": _fake_result("negative")},
    )

    v1.cmd_run()  # write_output defaults to True

    out_file = tmp_path / "run.json"
    assert out_file.exists()
    written = json.loads(out_file.read_text(encoding="utf-8"))
    assert (
        written["config"]["detection_rule"]
        == "per-series per-timepoint AR(1)-surrogate 95th percentile"
    )
