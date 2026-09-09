"""run.py -- H-B7-25: along each of H-B7-22's 8 confirmed SCHEDULE_FRAGILE shortest escaping
paths (constructed by H-B7-24), is p21CIP actively unstable (ready to fire) at every pre-point-
of-no-return step while RBL2 is passively stable (already False, no active tendency to change)?
Closes H-B7-22's own remaining Relaxation Map item (bounded-delay fairness) by reporting the
exact minimum "starvation count" p21CIP must be skipped for escape to succeed.

Reuses H-B7-24's find_shortest_prolif_path/build_reachability_graph/find_sink_attractors chain
(via H-B7-22) UNCHANGED; reuses H-B7-13's release-state construction.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
H_B7_24_DIR = HERE.parent / "20260910-remy-tumorigenesis-point-of-no-return-h24"
METRICS = HERE / "metrics"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


h24 = _load_module("h_b7_25_h24", H_B7_24_DIR / "run.py")
h13 = h24.h13
h1 = h24.h1

PYBOOLNET_NODE_ORDER = h24.PYBOOLNET_NODE_ORDER
GROWTH_ARREST_STATE_1 = h24.GROWTH_ARREST_STATE_1
GROWTH_ARREST_STATE_2 = h24.GROWTH_ARREST_STATE_2
CLAMPS = h24.CLAMPS
FRAGILE_KS = h24.FRAGILE_KS
find_shortest_prolif_path = h24.find_shortest_prolif_path
analyze_path = h24.analyze_path


def node_stability(state: dict, node: str, compiled_rules: dict) -> dict:
    rule_val = h1.evaluate_expression(compiled_rules[node], state)
    return {"value": state[node], "rule_says": rule_val, "unstable": rule_val != state[node]}


def analyze_starvation(
    path: list[tuple], pnr_step: int, node_names: list, compiled_rules: dict
) -> dict:
    """For steps 0 through pnr_step-1 (the pre-commitment window), record p21CIP/RBL2 stability
    at each state along the path."""
    per_step = []
    p21_always_unstable = True
    rbl2_always_stable = True
    for i in range(pnr_step):
        state = dict(zip(node_names, path[i]))
        p21_status = node_stability(state, "p21CIP", compiled_rules)
        rbl2_status = node_stability(state, "RBL2", compiled_rules)
        per_step.append({"step": i, "p21CIP": p21_status, "RBL2": rbl2_status})
        if not p21_status["unstable"]:
            p21_always_unstable = False
        if rbl2_status["unstable"]:
            rbl2_always_stable = False

    return {
        "pre_commitment_steps": per_step,
        "p21CIP_always_unstable_pre_commitment": p21_always_unstable,
        "RBL2_always_stable_pre_commitment": rbl2_always_stable,
        "asymmetry_confirmed": p21_always_unstable and rbl2_always_stable,
        "p21CIP_min_starvation_count": pnr_step,
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
            path_analysis = analyze_path(path, node_names, wild_type_rules)
            pnr_step = path_analysis["point_of_no_return_step"]

            starvation = analyze_starvation(path, pnr_step, node_names, wild_type_rules)
            starvation["branch"] = branch_name
            starvation["k"] = k
            starvation["point_of_no_return_step"] = pnr_step
            starvation["path_length"] = path_analysis["path_length"]
            per_state_results.append(starvation)

    all_confirmed = all(r["asymmetry_confirmed"] for r in per_state_results)
    verdict = "CONFIRMED" if all_confirmed else "REJECTED"

    out = {
        "claim": "H-B7-25 -- p21CIP-specific starvation asymmetry along H-B7-22's own "
        "8 confirmed SCHEDULE_FRAGILE shortest escaping paths",
        "n_release_states_tested": len(per_state_results),
        "all_asymmetry_confirmed": all_confirmed,
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
                        "point_of_no_return_step": r["point_of_no_return_step"],
                        "p21CIP_min_starvation_count": r["p21CIP_min_starvation_count"],
                        "asymmetry_confirmed": r["asymmetry_confirmed"],
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
