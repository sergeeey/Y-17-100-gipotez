from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent.parent


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def h25():
    return _load_module("test_h25_run", HERE / "run.py")


def test_node_stability_matches_manual_check(h25):
    text = h25.h13.DATA.read_text(encoding="utf-8")
    rules = h25.h1.parse_bnet(text)
    node_names = [name for name, _ in rules]
    wild_type_rules = h25.h1.compile_rules(rules)
    start_state = dict(zip(h25.PYBOOLNET_NODE_ORDER, (c == "1" for c in h25.GROWTH_ARREST_STATE_1)))
    sim = h25.h13.simulate_transient_clamp_multi_with_release_state(
        start_state, node_names, wild_type_rules, h25.CLAMPS, 1
    )
    release_state = sim["release_state"]
    status = h25.node_stability(release_state, "p21CIP", wild_type_rules)
    manual_rule_val = h25.h1.evaluate_expression(wild_type_rules["p21CIP"], release_state)
    assert status["rule_says"] == manual_rule_val
    assert status["value"] == release_state["p21CIP"]
    assert status["unstable"] == (manual_rule_val != release_state["p21CIP"])


def test_committed_run_k1_k2_confirmed_asymmetry():
    """k=1,2 (both branches) are the cases where the pre-registered asymmetry (p21CIP always
    unstable, RBL2 always stable pre-commitment) actually held."""
    run_json_path = HERE / "metrics" / "run.json"
    if not run_json_path.exists():
        pytest.skip("metrics/run.json not yet generated")
    data = json.loads(run_json_path.read_text(encoding="utf-8"))
    for r in data["per_state_results"]:
        if r["k"] in (1, 2):
            assert r["asymmetry_confirmed"] is True, f"{r['branch']}/k={r['k']} expected True"


def test_committed_run_k3_k4_break_asymmetry():
    """Regression: k=3,4 (both branches) are the cases where RBL2 ALSO becomes unstable late in
    the pre-commitment window, breaking the simple asymmetry -- must be reported honestly as
    such, not silently smoothed over."""
    run_json_path = HERE / "metrics" / "run.json"
    if not run_json_path.exists():
        pytest.skip("metrics/run.json not yet generated")
    data = json.loads(run_json_path.read_text(encoding="utf-8"))
    for r in data["per_state_results"]:
        if r["k"] in (3, 4):
            assert r["asymmetry_confirmed"] is False, f"{r['branch']}/k={r['k']} expected False"
            assert r["p21CIP_always_unstable_pre_commitment"] is True
            assert r["RBL2_always_stable_pre_commitment"] is False


def test_committed_run_p21cip_always_unstable_regardless_of_k():
    """The part of the hypothesis that DID survive in all 8 cases: p21CIP is always unstable
    (actively trying to re-establish) throughout the pre-commitment window, regardless of k."""
    run_json_path = HERE / "metrics" / "run.json"
    if not run_json_path.exists():
        pytest.skip("metrics/run.json not yet generated")
    data = json.loads(run_json_path.read_text(encoding="utf-8"))
    for r in data["per_state_results"]:
        assert r["p21CIP_always_unstable_pre_commitment"] is True


def test_committed_run_overall_verdict_rejected():
    run_json_path = HERE / "metrics" / "run.json"
    if not run_json_path.exists():
        pytest.skip("metrics/run.json not yet generated")
    data = json.loads(run_json_path.read_text(encoding="utf-8"))
    assert data["verdict"] == "REJECTED"
    assert data["all_asymmetry_confirmed"] is False


def test_committed_run_starvation_count_matches_pnr_step():
    run_json_path = HERE / "metrics" / "run.json"
    if not run_json_path.exists():
        pytest.skip("metrics/run.json not yet generated")
    data = json.loads(run_json_path.read_text(encoding="utf-8"))
    for r in data["per_state_results"]:
        assert r["p21CIP_min_starvation_count"] == r["point_of_no_return_step"]
