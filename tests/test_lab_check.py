"""Tests for scripts/lab_check.py.

Positive control: the real registry/graph.yaml passes.
Negative controls: the validator must be able to FAIL — a validator that cannot fail
is validation theater. The key negative control reproduces the 2026-05-28 incident
(a `ready` hypothesis resting on an `invalidated` artifact) and asserts INV3 fires.
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import lab_check  # noqa: E402  # WHY: scripts/ is not a package; path insert must precede import

REAL_GRAPH = ROOT / "registry" / "graph.yaml"


def _node(id_: str, type_: str, status: str, **extra: object) -> dict:
    base = {
        "id": id_,
        "type": type_,
        "title": id_,
        "status": status,
        "evidence": "HYPOTHESIS",
        "source": "test",
        "updated": "2026-09-06",
    }
    defaults = {
        "bridge": {"mechanism": "m"},
        "hypothesis": {
            "l0_type": "descriptive",
            "kill_criterion": "k",
            "experiment_dir": None,
            "fl_tier": "micro",
        },
        "artifact": {"date_created": "2026-05-16", "provenance": "fit"},
    }
    base.update(defaults.get(type_, {}))
    base.update(extra)
    return base


def _write(tmp_path: Path, nodes: list[dict], edges: list[dict]) -> Path:
    p = tmp_path / "graph.yaml"
    p.write_text(yaml.safe_dump({"nodes": nodes, "edges": edges}), encoding="utf-8")
    return p


def test_real_graph_passes() -> None:
    assert lab_check.main(REAL_GRAPH) == 0


def test_inv3_catches_stale_parked_incident(tmp_path: Path, capsys) -> None:
    # Replica of 2026-05-28: hypothesis marked ready while its grounding artifact is dead.
    nodes = [
        _node("B", "bridge", "verified_grounding"),
        _node("ART-DEAD", "artifact", "invalidated"),
        _node("ART-FIX", "artifact", "valid"),
        _node("H", "hypothesis", "ready"),
    ]
    edges = [
        {"from": "B", "to": "H", "type": "grounds"},
        {"from": "ART-FIX", "to": "ART-DEAD", "type": "invalidates"},
        {"from": "ART-DEAD", "to": "H", "type": "depends_on"},
    ]
    assert lab_check.main(_write(tmp_path, nodes, edges)) == 1
    assert "INV3 H" in capsys.readouterr().out


def test_dangling_edge_and_bad_status_detected(tmp_path: Path, capsys) -> None:
    nodes = [_node("H", "hypothesis", "almost_done")]  # status not in vocabulary
    edges = [{"from": "GHOST", "to": "H", "type": "grounds"}]
    assert lab_check.main(_write(tmp_path, nodes, edges)) == 1
    out = capsys.readouterr().out
    assert "dangling" in out
    assert "not allowed" in out
