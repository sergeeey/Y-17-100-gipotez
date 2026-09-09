"""run.py -- H-B7-22: exhaustive asynchronous reachability from H-B7-13's own release-state
domain (k=1..40, both branches). Tests whether the eventual FATE (not just its observability,
H-B7-16's own question) is schedule-independent under general fair asynchronous update, or
whether some fair schedule can reach a fate synchronous dynamics never reaches.

Builds the full nondeterministic single-node-update reachability graph from each release-state
(bounded by STATE_CAP, reported as BLOCKED-INFRASTRUCTURE if hit -- never silently treated as
exhaustive), then finds ATTRACTORS via proper SCC analysis (networkx) -- sink strongly-connected
components, not just zero-out-degree fixed points, so a genuine cyclic attractor is not missed.

Reuses H-B7-13's release-state construction (simulate_transient_clamp_multi_with_release_state,
CLAMPS, TESTED_DURATIONS, branch constants) UNCHANGED via distinct-name import; reuses H-B7-1's
parse_bnet/compile_rules/evaluate_expression.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import networkx as nx

HERE = Path(__file__).resolve().parent
H_B7_13_DIR = HERE.parent / "20260910-remy-tumorigenesis-observability-h13"
METRICS = HERE / "metrics"

STATE_CAP = 30000


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


h13 = _load_module("h_b7_22_h13", H_B7_13_DIR / "run.py")
h1 = h13.h1

PYBOOLNET_NODE_ORDER = h13.PYBOOLNET_NODE_ORDER
GROWTH_ARREST_STATE_1 = h13.GROWTH_ARREST_STATE_1
GROWTH_ARREST_STATE_2 = h13.GROWTH_ARREST_STATE_2
BRANCH_INPUTS_1 = h13.BRANCH_INPUTS_1
BRANCH_INPUTS_2 = h13.BRANCH_INPUTS_2
CLAMPS = h13.CLAMPS
TESTED_DURATIONS = h13.TESTED_DURATIONS
fate_label = h13.fate_label


def async_successors(state_tuple: tuple, node_names: list, compiled_rules: dict) -> list:
    """All distinct states reachable by updating exactly ONE node (the standard general
    asynchronous Boolean-network transition relation) -- a node contributes a successor only if
    updating it would actually change its value (a no-op update is not a new state/edge)."""
    state_dict = dict(zip(node_names, state_tuple))
    successors = []
    for i, node in enumerate(node_names):
        new_val = h1.evaluate_expression(compiled_rules[node], state_dict)
        if new_val != state_tuple[i]:
            successors.append((*state_tuple[:i], new_val, *state_tuple[i + 1 :]))
    return successors


def build_reachability_graph(
    start_tuple: tuple, node_names: list, compiled_rules: dict, cap: int
) -> dict:
    """Exhaustive BFS over the async transition graph from `start_tuple`. Returns
    {'graph': nx.DiGraph, 'hit_cap': bool} -- if hit_cap is True, the graph is INCOMPLETE and
    must not be used for any CONFIRMED/REJECTED classification (FL Step 2a Substrate Gate)."""
    graph = nx.DiGraph()
    graph.add_node(start_tuple)
    visited = {start_tuple}
    frontier = [start_tuple]
    hit_cap = False
    while frontier:
        new_frontier = []
        for state_tuple in frontier:
            for succ in async_successors(state_tuple, node_names, compiled_rules):
                graph.add_edge(state_tuple, succ)
                if succ not in visited:
                    if len(visited) >= cap:
                        hit_cap = True
                        continue
                    visited.add(succ)
                    new_frontier.append(succ)
        if hit_cap:
            break
        frontier = new_frontier
    return {"graph": graph, "hit_cap": hit_cap}


def find_sink_attractors(graph: nx.DiGraph, node_names: list) -> list:
    """Proper attractor detection via SCC analysis (not just zero-out-degree fixed points): a
    sink SCC (no edges leaving it to a different SCC) is an attractor -- either a single fixed
    point (SCC of size 1 with no self-loop needed, since a fixed point has zero outgoing edges
    entirely) or a genuine cyclic attractor (SCC of size > 1). Returns one entry per sink SCC."""
    condensation = nx.condensation(graph)
    attractors = []
    for comp_id in condensation.nodes:
        if condensation.out_degree(comp_id) == 0:
            members = condensation.nodes[comp_id]["members"]
            fates = {fate_label(dict(zip(node_names, m))) for m in members}
            attractors.append(
                {
                    "size": len(members),
                    "is_cyclic": len(members) > 1,
                    "fates": sorted(fates),
                    "example_state": "".join("1" if v else "0" for v in next(iter(members))),
                }
            )
    return attractors


def analyze_release_state(
    branch_name: str,
    k: int,
    release_tuple: tuple,
    sync_fate: str,
    node_names: list,
    compiled_rules: dict,
) -> dict:
    result = build_reachability_graph(release_tuple, node_names, compiled_rules, STATE_CAP)
    if result["hit_cap"]:
        return {
            "branch": branch_name,
            "k": k,
            "sync_fate": sync_fate,
            "status": "BLOCKED-INFRASTRUCTURE",
            "reason": f"reachability search hit the {STATE_CAP}-state cap before terminating",
        }

    graph = result["graph"]
    attractors = find_sink_attractors(graph, node_names)
    all_fates = set()
    ambiguous_attractors = 0
    for a in attractors:
        if len(a["fates"]) == 1:
            all_fates.add(a["fates"][0])
        else:
            ambiguous_attractors += 1
            all_fates.update(a["fates"])

    schedule_robust = all_fates == {sync_fate}
    return {
        "branch": branch_name,
        "k": k,
        "sync_fate": sync_fate,
        "status": "OK",
        "n_states_visited": graph.number_of_nodes(),
        "n_attractors": len(attractors),
        "n_cyclic_attractors": sum(1 for a in attractors if a["is_cyclic"]),
        "n_ambiguous_attractors": ambiguous_attractors,
        "async_reachable_fates": sorted(all_fates),
        "classification": "SCHEDULE_ROBUST" if schedule_robust else "SCHEDULE_FRAGILE",
    }


def cmd_run() -> dict:
    text = h13.DATA.read_text(encoding="utf-8")
    rules = h1.parse_bnet(text)
    node_names = [name for name, _ in rules]
    wild_type_rules = h1.compile_rules(rules)

    branches = [
        ("branch_1", GROWTH_ARREST_STATE_1),
        ("branch_2", GROWTH_ARREST_STATE_2),
    ]

    per_state_results = []
    for branch_name, growth_arrest_state in branches:
        start_state = dict(zip(PYBOOLNET_NODE_ORDER, (c == "1" for c in growth_arrest_state)))
        for k in TESTED_DURATIONS:
            sim = h13.simulate_transient_clamp_multi_with_release_state(
                start_state, node_names, wild_type_rules, CLAMPS, k
            )
            release_tuple = tuple(sim["release_state"][n] for n in node_names)
            sync_fate = fate_label(sim["final_state"])
            per_state_results.append(
                analyze_release_state(
                    branch_name, k, release_tuple, sync_fate, node_names, wild_type_rules
                )
            )

    ok_results = [r for r in per_state_results if r["status"] == "OK"]
    blocked_results = [r for r in per_state_results if r["status"] != "OK"]
    fragile_results = [r for r in ok_results if r["classification"] == "SCHEDULE_FRAGILE"]
    robust_results = [r for r in ok_results if r["classification"] == "SCHEDULE_ROBUST"]

    k_adv = None
    if fragile_results:
        prolif_fragile_ks = [
            r["k"] for r in fragile_results if "PROLIFERATION" in r["async_reachable_fates"]
        ]
        if prolif_fragile_ks:
            k_adv = min(prolif_fragile_ks)

    if blocked_results:
        verdict = "CRITERION_INVALID"
    elif fragile_results:
        verdict = "REJECTED"
    else:
        verdict = "CONFIRMED"

    out = {
        "claim": "H-B7-22 -- does the async-reachable attractor set match the synchronous fate "
        "exactly, across H-B7-13's own k=1..40 release-state domain (both branches)?",
        "state_cap": STATE_CAP,
        "n_release_states_tested": len(per_state_results),
        "n_ok": len(ok_results),
        "n_blocked_infrastructure": len(blocked_results),
        "n_schedule_robust": len(robust_results),
        "n_schedule_fragile": len(fragile_results),
        "smallest_k_where_prolif_becomes_adversarially_reachable": k_adv,
        "verdict": verdict,
        "per_state_results": per_state_results,
    }

    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    print(
        json.dumps(
            {k: v for k, v in out.items() if k != "per_state_results"},
            indent=2,
            default=str,
        )
    )
    return out


if __name__ == "__main__":
    cmd_run()
