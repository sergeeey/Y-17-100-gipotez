"""run.py -- H-B7-24: along the shortest async-escaping path from each of H-B7-22's 8 confirmed
SCHEDULE_FRAGILE release-states, is there a single, sharp step ("point of no return") after
which GROWTH_ARREST becomes permanently unreachable -- checked via H-B7-22's own exhaustive
reachability machinery applied at EVERY intermediate state along the path, not assumed from the
path's own endpoint.

Reuses H-B7-22's async_successors/build_reachability_graph/find_sink_attractors/STATE_CAP
UNCHANGED via distinct-name import; reuses H-B7-13's release-state construction.
"""

from __future__ import annotations

import importlib.util
import json
from collections import deque
from pathlib import Path

HERE = Path(__file__).resolve().parent
H_B7_22_DIR = HERE.parent / "20260910-remy-tumorigenesis-adversarial-async-h22"
METRICS = HERE / "metrics"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


h22 = _load_module("h_b7_24_h22", H_B7_22_DIR / "run.py")
h13 = h22.h13
h1 = h22.h1

PYBOOLNET_NODE_ORDER = h22.PYBOOLNET_NODE_ORDER
GROWTH_ARREST_STATE_1 = h22.GROWTH_ARREST_STATE_1
GROWTH_ARREST_STATE_2 = h22.GROWTH_ARREST_STATE_2
CLAMPS = h22.CLAMPS
fate_label = h22.fate_label
async_successors = h22.async_successors
build_reachability_graph = h22.build_reachability_graph
find_sink_attractors = h22.find_sink_attractors
STATE_CAP = h22.STATE_CAP

FRAGILE_KS = [1, 2, 3, 4]


def find_shortest_prolif_path(
    start_tuple: tuple, node_names: list, compiled_rules: dict
) -> list[tuple]:
    """BFS shortest path (by hop count) from start_tuple to a genuine PROLIFERATION fixed point,
    via single-node async updates. Returns the full sequence of states (start ... target)."""
    visited = {start_tuple: None}
    frontier = deque([start_tuple])
    prolif_idx = node_names.index("Proliferation")
    ga_idx = node_names.index("Growth_arrest")
    while frontier:
        cur = frontier.popleft()
        for succ in async_successors(cur, node_names, compiled_rules):
            if succ not in visited:
                visited[succ] = cur
                nd = dict(zip(node_names, succ))
                unstable = any(
                    h1.evaluate_expression(compiled_rules[n2], nd) != nd[n2] for n2 in node_names
                )
                if not unstable and succ[prolif_idx] and not succ[ga_idx]:
                    path = [succ]
                    while visited[path[-1]] is not None:
                        path.append(visited[path[-1]])
                    path.reverse()
                    return path
                frontier.append(succ)
    raise RuntimeError("no PROLIFERATION fixed point found -- unexpected given H-B7-22's own data")


def analyze_path(path: list[tuple], node_names: list, compiled_rules: dict) -> dict:
    step_reachability = []
    for i, state_tuple in enumerate(path):
        result = build_reachability_graph(state_tuple, node_names, compiled_rules, STATE_CAP)
        if result["hit_cap"]:
            step_reachability.append({"step": i, "status": "BLOCKED-INFRASTRUCTURE"})
            continue
        attractors = find_sink_attractors(result["graph"], node_names)
        fates = set()
        for a in attractors:
            fates.update(a["fates"])
        step_reachability.append(
            {
                "step": i,
                "status": "OK",
                "n_states_from_here": result["graph"].number_of_nodes(),
                "reachable_fates": sorted(fates),
                "growth_arrest_reachable": "GROWTH_ARREST" in fates,
            }
        )

    if any(r["status"] != "OK" for r in step_reachability):
        return {
            "path_length": len(path) - 1,
            "step_reachability": step_reachability,
            "point_of_no_return_step": None,
            "triggering_node": None,
            "is_sharp_single_step": False,
            "status": "BLOCKED-INFRASTRUCTURE",
        }

    ga_reachable_flags = [r["growth_arrest_reachable"] for r in step_reachability]
    # find the point of no return: first index where growth_arrest_reachable is False
    pnr_step = None
    for i, flag in enumerate(ga_reachable_flags):
        if not flag:
            pnr_step = i
            break

    is_sharp = True
    if pnr_step is not None:
        # sharp = monotonic: True for all steps < pnr_step, False for all steps >= pnr_step
        is_sharp = all(ga_reachable_flags[:pnr_step]) and not any(ga_reachable_flags[pnr_step:])
    else:
        # GROWTH_ARREST reachable at every step, including the final PROLIFERATION fixed point
        # itself -- would be a genuine anomaly given the final state IS a PROLIFERATION fixed
        # point (0 outgoing edges), so this branch should not occur; report honestly if it does.
        is_sharp = False

    triggering_node = None
    if pnr_step is not None and pnr_step > 0:
        prev_state = path[pnr_step - 1]
        cur_state = path[pnr_step]
        diffs = [n for j, n in enumerate(node_names) if cur_state[j] != prev_state[j]]
        triggering_node = diffs[0] if len(diffs) == 1 else diffs

    return {
        "path_length": len(path) - 1,
        "step_reachability": step_reachability,
        "point_of_no_return_step": pnr_step,
        "triggering_node": triggering_node,
        "is_sharp_single_step": is_sharp,
        "status": "OK",
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
        for k in FRAGILE_KS:
            sim = h13.simulate_transient_clamp_multi_with_release_state(
                start_state, node_names, wild_type_rules, CLAMPS, k
            )
            release_tuple = tuple(sim["release_state"][n] for n in node_names)
            path = find_shortest_prolif_path(release_tuple, node_names, wild_type_rules)
            analysis = analyze_path(path, node_names, wild_type_rules)
            analysis["branch"] = branch_name
            analysis["k"] = k
            per_state_results.append(analysis)

    ok_results = [r for r in per_state_results if r["status"] == "OK"]
    all_sharp = all(r["is_sharp_single_step"] for r in ok_results)
    triggering_nodes = {r["branch"] + "/" + str(r["k"]): r["triggering_node"] for r in ok_results}
    cyclin_ae1_trigger_count = sum(
        1 for r in ok_results if r["triggering_node"] in ("CyclinA", "CyclinE1")
    )

    verdict = (
        "CONFIRMED" if (len(ok_results) == len(per_state_results) and all_sharp) else "REJECTED"
    )

    out = {
        "claim": "H-B7-24 -- point of no return along the shortest async-escaping path, "
        "for each of H-B7-22's 8 confirmed SCHEDULE_FRAGILE release-states",
        "n_release_states_tested": len(per_state_results),
        "n_ok": len(ok_results),
        "all_sharp_single_step": all_sharp,
        "triggering_nodes_by_condition": triggering_nodes,
        "n_triggered_by_cyclinA_or_cyclinE1": cyclin_ae1_trigger_count,
        "verdict": verdict,
        "per_state_results": per_state_results,
    }

    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    print(
        json.dumps(
            {k: v for k, v in out.items() if k != "per_state_results"}
            | {
                "per_state_summary": [
                    {
                        "branch": r["branch"],
                        "k": r["k"],
                        "path_length": r["path_length"],
                        "point_of_no_return_step": r["point_of_no_return_step"],
                        "triggering_node": r["triggering_node"],
                        "is_sharp_single_step": r["is_sharp_single_step"],
                    }
                    for r in per_state_results
                ]
            },
            indent=2,
            default=str,
        )
    )
    return out


if __name__ == "__main__":
    cmd_run()
