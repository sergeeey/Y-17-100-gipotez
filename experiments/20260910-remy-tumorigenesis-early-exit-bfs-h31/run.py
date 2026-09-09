"""run.py -- H-B7-31: formalizes and corrects the earlier informal "H9-B cheap precursor" idea.

The original framing (n_states_visited as a "cheap discriminator" of SCHEDULE_FRAGILE vs
SCHEDULE_ROBUST) was circular: computing n_states_visited already requires the full exhaustive
BFS H-B7-22 runs, so it saves nothing. This experiment tests the genuinely cheaper alternative:
an EARLY-EXIT variant of the same BFS that stops as soon as BOTH fates (PROLIFERATION and
GROWTH_ARREST) are confirmed reachable, instead of exhausting the entire state space.

Reuses H-B7-22's own async_successors UNCHANGED; the ONLY change is the BFS termination
condition.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
H_B7_22_DIR = HERE.parent / "20260910-remy-tumorigenesis-adversarial-async-h22"
METRICS = HERE / "metrics"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


h22 = _load_module("h_b7_31_h22", H_B7_22_DIR / "run.py")
h13 = h22.h13
h1 = h22.h1

PYBOOLNET_NODE_ORDER = h22.PYBOOLNET_NODE_ORDER
GROWTH_ARREST_STATE_1 = h22.GROWTH_ARREST_STATE_1
GROWTH_ARREST_STATE_2 = h22.GROWTH_ARREST_STATE_2
CLAMPS = h22.CLAMPS
STATE_CAP = h22.STATE_CAP
async_successors = h22.async_successors

CONDITIONS_K = [1, 2, 3, 4, 5]
SAVINGS_BAR = 0.50  # kill criterion: early-exit savings must exceed 50% for every FRAGILE condition


def bfs_with_early_exit_tracking(
    start_tuple: tuple,
    node_names: list,
    compiled_rules: dict,
    cap: int,
    prolif_idx: int,
    ga_idx: int,
) -> dict:
    """Level-by-level BFS instrumented to record the exact state-visitation count at the moment
    BOTH PROLIFERATION and GROWTH_ARREST fixed points have been observed as reachable."""

    def fate_of(state_tuple: tuple):
        if state_tuple[prolif_idx] and not state_tuple[ga_idx]:
            return "PROLIFERATION"
        if state_tuple[ga_idx]:
            return "GROWTH_ARREST"
        return None

    visited = {start_tuple}
    frontier = [start_tuple]
    fates_seen = set()
    n_visited_at_both_found = None
    hit_cap = False

    f0 = fate_of(start_tuple)
    if f0:
        fates_seen.add(f0)

    while frontier and not hit_cap:
        new_frontier = []
        for state_tuple in frontier:
            for succ in async_successors(state_tuple, node_names, compiled_rules):
                if succ not in visited:
                    if len(visited) >= cap:
                        hit_cap = True
                        break
                    visited.add(succ)
                    new_frontier.append(succ)
                    f = fate_of(succ)
                    if f and f not in fates_seen:
                        fates_seen.add(f)
                        if len(fates_seen) == 2 and n_visited_at_both_found is None:
                            n_visited_at_both_found = len(visited)
            if hit_cap:
                break
        frontier = new_frontier

    return {
        "n_total_visited": len(visited),
        "hit_cap": hit_cap,
        "fates_seen": sorted(fates_seen),
        "n_visited_at_early_exit": n_visited_at_both_found,
    }


def cmd_run() -> dict:
    text = h13.DATA.read_text(encoding="utf-8")
    rules = h1.parse_bnet(text)
    node_names = [name for name, _ in rules]
    wild_type_rules = h1.compile_rules(rules)

    prolif_idx = node_names.index("Proliferation")
    ga_idx = node_names.index("Growth_arrest")

    branches = {
        "branch_1": GROWTH_ARREST_STATE_1,
        "branch_2": GROWTH_ARREST_STATE_2,
    }

    results = []
    for branch_name, growth_arrest_state in branches.items():
        start_state = dict(zip(PYBOOLNET_NODE_ORDER, (c == "1" for c in growth_arrest_state)))
        for k in CONDITIONS_K:
            sim = h13.simulate_transient_clamp_multi_with_release_state(
                start_state, node_names, wild_type_rules, CLAMPS, k
            )
            release_tuple = tuple(sim["release_state"][n] for n in node_names)

            bfs_result = bfs_with_early_exit_tracking(
                release_tuple, node_names, wild_type_rules, STATE_CAP, prolif_idx, ga_idx
            )

            is_fragile = len(bfs_result["fates_seen"]) == 2
            early = bfs_result["n_visited_at_early_exit"]
            total = bfs_result["n_total_visited"]
            savings_fraction = (1 - early / total) if (is_fragile and early) else None

            results.append(
                {
                    "branch": branch_name,
                    "k": k,
                    "classification": "SCHEDULE_FRAGILE" if is_fragile else "SCHEDULE_ROBUST",
                    "fates_seen": bfs_result["fates_seen"],
                    "n_total_visited": total,
                    "n_visited_at_early_exit": early,
                    "savings_fraction": savings_fraction,
                    "hit_cap": bfs_result["hit_cap"],
                }
            )

    fragile_results = [r for r in results if r["classification"] == "SCHEDULE_FRAGILE"]
    robust_results = [r for r in results if r["classification"] == "SCHEDULE_ROBUST"]

    all_fragile_meet_savings_bar = all(
        r["savings_fraction"] is not None and r["savings_fraction"] > SAVINGS_BAR
        for r in fragile_results
    )
    no_false_positives_on_robust = all(len(r["fates_seen"]) <= 1 for r in robust_results)
    n_fragile = len(fragile_results)
    n_robust = len(robust_results)

    verdict = (
        "CONFIRMED"
        if (
            all_fragile_meet_savings_bar
            and no_false_positives_on_robust
            and n_fragile == 8
            and n_robust == 2
        )
        else "CRITERION_INVALID"
    )

    out = {
        "claim": "H-B7-31 -- early-exit BFS (stop once both fates are confirmed reachable) gives "
        "a real, substantial computational shortcut for SCHEDULE_FRAGILE classification, but "
        "NOT for SCHEDULE_ROBUST (which structurally requires exhaustive search) -- corrects "
        "the earlier informal, circular 'n_states_visited as cheap discriminator' framing",
        "savings_bar": SAVINGS_BAR,
        "n_conditions_tested": len(results),
        "n_fragile": n_fragile,
        "n_robust": n_robust,
        "all_fragile_meet_savings_bar": all_fragile_meet_savings_bar,
        "no_false_positives_on_robust": no_false_positives_on_robust,
        "verdict": verdict,
        "results": results,
    }

    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    print(
        json.dumps(
            {k: v for k, v in out.items() if k != "results"}
            | {
                "results_summary": [
                    {
                        "branch": r["branch"],
                        "k": r["k"],
                        "classification": r["classification"],
                        "n_total_visited": r["n_total_visited"],
                        "n_visited_at_early_exit": r["n_visited_at_early_exit"],
                        "savings_fraction": r["savings_fraction"],
                    }
                    for r in results
                ]
            },
            indent=2,
            default=str,
        )
    )
    return out


if __name__ == "__main__":
    cmd_run()
