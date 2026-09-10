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


# ADR-122: evidence_mode / verification_strength / substrate node type / tested_on edge


def test_substrate_node_valid_passes(tmp_path: Path) -> None:
    nodes = [
        _node("B", "bridge", "verified_grounding"),
        _node("H", "hypothesis", "confirmed"),
        _node("SUB", "substrate", "active", category="model"),
    ]
    edges = [
        {"from": "B", "to": "H", "type": "grounds"},
        {"from": "H", "to": "SUB", "type": "tested_on"},
    ]
    assert lab_check.main(_write(tmp_path, nodes, edges)) == 0


def test_substrate_bad_category_detected(tmp_path: Path, capsys) -> None:
    nodes = [_node("SUB", "substrate", "active", category="vibes")]
    assert lab_check.main(_write(tmp_path, nodes, [])) == 1
    assert "category" in capsys.readouterr().out


def test_evidence_mode_bad_value_detected(tmp_path: Path, capsys) -> None:
    nodes = [
        _node("B", "bridge", "verified_grounding"),
        _node("H", "hypothesis", "confirmed", evidence_mode="vibes"),
    ]
    edges = [{"from": "B", "to": "H", "type": "grounds"}]
    assert lab_check.main(_write(tmp_path, nodes, edges)) == 1
    assert "evidence_mode" in capsys.readouterr().out


def test_verification_strength_bad_value_detected(tmp_path: Path, capsys) -> None:
    nodes = [
        _node("B", "bridge", "verified_grounding"),
        _node("H", "hypothesis", "confirmed", verification_strength="super-strong"),
    ]
    edges = [{"from": "B", "to": "H", "type": "grounds"}]
    assert lab_check.main(_write(tmp_path, nodes, edges)) == 1
    assert "verification_strength" in capsys.readouterr().out


def test_evidence_mode_and_verification_strength_optional(tmp_path: Path) -> None:
    """A node that omits both new fields must still pass -- they are opt-in, not required."""
    nodes = [
        _node("B", "bridge", "verified_grounding"),
        _node("H", "hypothesis", "confirmed"),
    ]
    edges = [{"from": "B", "to": "H", "type": "grounds"}]
    assert lab_check.main(_write(tmp_path, nodes, edges)) == 0


def test_substrate_diversity_report_printed(tmp_path: Path, capsys) -> None:
    nodes = [
        _node("B", "bridge", "verified_grounding"),
        _node("H", "hypothesis", "confirmed"),
        _node("SUB", "substrate", "active", category="dataset"),
    ]
    edges = [
        {"from": "B", "to": "H", "type": "grounds"},
        {"from": "H", "to": "SUB", "type": "tested_on"},
    ]
    assert lab_check.main(_write(tmp_path, nodes, edges)) == 0
    out = capsys.readouterr().out
    assert "substrate diversity: 1 substrate(s), 1/1 hypothesis/artifact node(s) tagged" in out
    assert "SUB: 1 node(s) tested_on" in out


def test_real_graph_has_substrate_nodes_and_tested_on_edges() -> None:
    """Positive control for ADR-122's own real backfill -- not just a synthetic graph check."""
    g = yaml.safe_load(REAL_GRAPH.read_text(encoding="utf-8"))
    substrate_ids = {n["id"] for n in g["nodes"] if n["type"] == "substrate"}
    assert len(substrate_ids) >= 4  # the audit named ~4-6 real substrates
    tested_on_targets = {e["to"] for e in g["edges"] if e["type"] == "tested_on"}
    assert tested_on_targets, "at least one tested_on edge must exist in the real graph"
    assert tested_on_targets <= substrate_ids  # every tested_on edge points at a real substrate
