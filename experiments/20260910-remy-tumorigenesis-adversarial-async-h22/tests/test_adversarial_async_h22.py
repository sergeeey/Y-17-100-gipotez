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
def h22():
    return _load_module("test_h22_run", HERE / "run.py")


def test_async_successors_hand_case(h22):
    """A 2-node hand-constructed case using the REAL boolean.py rule compiler/evaluator (no
    monkeypatching): node A's rule is `!B`, node B's rule is `B` (self-stable). At state
    (A=False, B=False), A's rule evaluates to True (a flip) and B's rule evaluates to False
    (no change) -- exactly ONE successor expected (flipping A only)."""
    rules = h22.h1.parse_bnet("targets, factors\nA, !B\nB, B\n")
    compiled_rules = h22.h1.compile_rules(rules)
    node_names = ["A", "B"]
    successors = h22.async_successors((False, False), node_names, compiled_rules)
    assert successors == [(True, False)]


def test_regression_reachable_state_counts_for_branch1_k3(h22):
    """Locks in the feasibility-diagnostic's own numbers for a known case -- a change here would
    mean either the network data or the async-successor logic changed unexpectedly."""
    text = h22.h13.DATA.read_text(encoding="utf-8")
    rules = h22.h1.parse_bnet(text)
    node_names = [name for name, _ in rules]
    wild_type_rules = h22.h1.compile_rules(rules)
    start_state = dict(zip(h22.PYBOOLNET_NODE_ORDER, (c == "1" for c in h22.GROWTH_ARREST_STATE_1)))
    sim = h22.h13.simulate_transient_clamp_multi_with_release_state(
        start_state, node_names, wild_type_rules, h22.CLAMPS, 3
    )
    release_tuple = tuple(sim["release_state"][n] for n in node_names)
    result = h22.build_reachability_graph(release_tuple, node_names, wild_type_rules, h22.STATE_CAP)
    assert result["hit_cap"] is False
    assert result["graph"].number_of_nodes() == 200


def test_no_cyclic_attractors_in_committed_run():
    run_json_path = HERE / "metrics" / "run.json"
    if not run_json_path.exists():
        pytest.skip("metrics/run.json not yet generated")
    data = json.loads(run_json_path.read_text(encoding="utf-8"))
    for r in data["per_state_results"]:
        if r["status"] == "OK":
            assert r["n_cyclic_attractors"] == 0
            assert r["n_ambiguous_attractors"] == 0


def test_committed_run_no_blocked_infrastructure():
    run_json_path = HERE / "metrics" / "run.json"
    if not run_json_path.exists():
        pytest.skip("metrics/run.json not yet generated")
    data = json.loads(run_json_path.read_text(encoding="utf-8"))
    assert data["n_blocked_infrastructure"] == 0
    assert data["n_ok"] == 80


def test_committed_run_fragile_pattern_is_exactly_k1_to_k4_both_branches():
    """Regression-locks the striking, clean pattern found: SCHEDULE_FRAGILE at exactly k=1..4 on
    both branches, SCHEDULE_ROBUST at k=5..40 on both branches -- a sharp split, not scattered
    noise."""
    run_json_path = HERE / "metrics" / "run.json"
    if not run_json_path.exists():
        pytest.skip("metrics/run.json not yet generated")
    data = json.loads(run_json_path.read_text(encoding="utf-8"))
    fragile_keys = {
        (r["branch"], r["k"])
        for r in data["per_state_results"]
        if r["status"] == "OK" and r["classification"] == "SCHEDULE_FRAGILE"
    }
    expected = {(branch, k) for branch in ("branch_1", "branch_2") for k in (1, 2, 3, 4)}
    assert fragile_keys == expected


def test_committed_run_synchronous_fate_always_in_async_reachable_set():
    """Empirical consistency check (NOT a logical necessity -- synchronous multi-bit steps are
    not literally decomposable into the single-bit-flip async graph's edges, so this is real
    data, not a tautology): in every one of the 80 tested release-states, the async-reachable
    fate set includes the synchronous fate."""
    run_json_path = HERE / "metrics" / "run.json"
    if not run_json_path.exists():
        pytest.skip("metrics/run.json not yet generated")
    data = json.loads(run_json_path.read_text(encoding="utf-8"))
    for r in data["per_state_results"]:
        if r["status"] == "OK":
            assert r["sync_fate"] in r["async_reachable_fates"]


def test_committed_run_verdict_is_rejected():
    run_json_path = HERE / "metrics" / "run.json"
    if not run_json_path.exists():
        pytest.skip("metrics/run.json not yet generated")
    data = json.loads(run_json_path.read_text(encoding="utf-8"))
    assert data["verdict"] == "REJECTED"
    assert data["smallest_k_where_prolif_becomes_adversarially_reachable"] == 1


def test_mechanism_race_condition_reproducible(h22):
    """Re-derives the shortest async path from branch_1's k=3 release state to a PROLIFERATION
    fixed point, and confirms the Mechanism Claim Gate's own hypothesis: CyclinA fires while
    p21CIP and RBL2 are BOTH still False (the race-condition mechanism), not some other path."""
    from collections import deque

    text = h22.h13.DATA.read_text(encoding="utf-8")
    rules = h22.h1.parse_bnet(text)
    node_names = [name for name, _ in rules]
    wild_type_rules = h22.h1.compile_rules(rules)
    start_state = dict(zip(h22.PYBOOLNET_NODE_ORDER, (c == "1" for c in h22.GROWTH_ARREST_STATE_1)))
    sim = h22.h13.simulate_transient_clamp_multi_with_release_state(
        start_state, node_names, wild_type_rules, h22.CLAMPS, 3
    )
    release_tuple = tuple(sim["release_state"][n] for n in node_names)
    prolif_idx = node_names.index("Proliferation")
    ga_idx = node_names.index("Growth_arrest")
    p21_idx = node_names.index("p21CIP")
    rbl2_idx = node_names.index("RBL2")
    cyclina_idx = node_names.index("CyclinA")

    visited = {release_tuple: None}
    frontier = deque([release_tuple])
    target = None
    while frontier and target is None:
        state_tuple = frontier.popleft()
        for succ in h22.async_successors(state_tuple, node_names, wild_type_rules):
            if succ not in visited:
                visited[succ] = state_tuple
                nd = dict(zip(node_names, succ))
                unstable = any(
                    h22.h1.evaluate_expression(wild_type_rules[n2], nd) != nd[n2]
                    for n2 in node_names
                )
                if not unstable and succ[prolif_idx] and not succ[ga_idx]:
                    target = succ
                    break
                frontier.append(succ)

    assert target is not None, "expected a reachable PROLIFERATION fixed point"

    path = []
    cur = target
    while visited[cur] is not None:
        path.append(cur)
        cur = visited[cur]
    path.append(release_tuple)
    path.reverse()

    cyclina_fire_index = next(
        i for i, s in enumerate(path) if i > 0 and s[cyclina_idx] and not path[i - 1][cyclina_idx]
    )
    state_when_cyclina_fires = path[cyclina_fire_index]
    assert state_when_cyclina_fires[p21_idx] is False
    assert state_when_cyclina_fires[rbl2_idx] is False
