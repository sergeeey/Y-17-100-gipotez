"""run.py -- H-B7-28: extends H-B7-27's own branch-isomorphism mechanism (phi=flip(EGFR_stimulus))
to H-B7-22's own FULL originally-tested domain (k=1..40, both branches, 80 conditions), not just
the 10 conditions H-B7-26/27 checked (k=1..5).

Reuses H-B7-27's own check_isomorphism/check_invariant/build_phi UNCHANGED; reuses H-B7-26's
solve_absorption UNCHANGED for the corollary re-derivation check.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
H_B7_27_DIR = HERE.parent / "20260910-remy-tumorigenesis-branch-isomorphism-h27"
METRICS = HERE / "metrics"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


h27 = _load_module("h_b7_28_h27", H_B7_27_DIR / "run.py")
h26 = h27.h26
h22 = h27.h22
h13 = h27.h13
h1 = h27.h1

PYBOOLNET_NODE_ORDER = h27.PYBOOLNET_NODE_ORDER
GROWTH_ARREST_STATE_1 = h27.GROWTH_ARREST_STATE_1
GROWTH_ARREST_STATE_2 = h27.GROWTH_ARREST_STATE_2
CLAMPS = h27.CLAMPS
STATE_CAP = h22.STATE_CAP
build_reachability_graph = h22.build_reachability_graph
solve_absorption = h26.solve_absorption
build_phi = h27.build_phi
check_isomorphism = h27.check_isomorphism
check_invariant = h27.check_invariant

CONDITIONS_K = list(range(1, 41))  # H-B7-22's own full originally-tested domain


def cmd_run() -> dict:
    text = h13.DATA.read_text(encoding="utf-8")
    rules = h1.parse_bnet(text)
    node_names = [name for name, _ in rules]
    wild_type_rules = h1.compile_rules(rules)

    phi = build_phi(node_names, "EGFR_stimulus")

    branches = {
        "branch_1": GROWTH_ARREST_STATE_1,
        "branch_2": GROWTH_ARREST_STATE_2,
    }

    graphs_by_cond = {}
    release_by_cond = {}
    blocked_conditions = []
    for branch_name, growth_arrest_state in branches.items():
        start_state = dict(zip(PYBOOLNET_NODE_ORDER, (c == "1" for c in growth_arrest_state)))
        for k in CONDITIONS_K:
            sim = h13.simulate_transient_clamp_multi_with_release_state(
                start_state, node_names, wild_type_rules, CLAMPS, k
            )
            release_tuple = tuple(sim["release_state"][n] for n in node_names)
            graph_result = build_reachability_graph(
                release_tuple, node_names, wild_type_rules, STATE_CAP
            )
            if graph_result["hit_cap"]:
                blocked_conditions.append({"branch": branch_name, "k": k})
                continue
            graphs_by_cond[(branch_name, k)] = graph_result["graph"]
            release_by_cond[(branch_name, k)] = release_tuple

    results = []
    for k in CONDITIONS_K:
        if ("branch_1", k) not in graphs_by_cond or ("branch_2", k) not in graphs_by_cond:
            results.append({"k": k, "status": "BLOCKED-INFRASTRUCTURE"})
            continue

        g1 = graphs_by_cond[("branch_1", k)]
        g2 = graphs_by_cond[("branch_2", k)]
        release_1 = release_by_cond[("branch_1", k)]
        release_2 = release_by_cond[("branch_2", k)]

        iso = check_isomorphism(g1, g2, phi)
        phi_release_matches = phi(release_1) == release_2

        inv_1 = check_invariant(g1, node_names)
        inv_2 = check_invariant(g2, node_names)

        solved_1 = solve_absorption(g1, release_1, node_names)
        solved_2 = solve_absorption(g2, release_2, node_names)
        corollary_matches = (
            solved_1["status"] == "OK"
            and solved_2["status"] == "OK"
            and abs(solved_1["exact_escape_probability"] - solved_2["exact_escape_probability"])
            < 1e-9
        )

        results.append(
            {
                "status": "OK",
                "k": k,
                "n_states_branch_1": g1.number_of_nodes(),
                "n_states_branch_2": g2.number_of_nodes(),
                "phi_release_1_equals_release_2": phi_release_matches,
                "isomorphism": iso,
                "invariant_branch_1": inv_1,
                "invariant_branch_2": inv_2,
                "corollary_escape_probability_matches": corollary_matches,
                "exact_escape_probability_branch_1": solved_1["exact_escape_probability"],
                "exact_escape_probability_branch_2": solved_2["exact_escape_probability"],
            }
        )

    ok_results = [r for r in results if r["status"] == "OK"]
    n_blocked = len(blocked_conditions) + sum(
        1 for r in results if r["status"] == "BLOCKED-INFRASTRUCTURE"
    )

    all_isomorphisms_confirmed = all(r["isomorphism"]["isomorphism_confirmed"] for r in ok_results)
    all_phi_release_matches = all(r["phi_release_1_equals_release_2"] for r in ok_results)
    all_invariants_hold = all(
        r["invariant_branch_1"]["invariant_holds"] and r["invariant_branch_2"]["invariant_holds"]
        for r in ok_results
    )
    all_corollaries_match = all(r["corollary_escape_probability_matches"] for r in ok_results)

    n_states_scanned = sum(
        r["invariant_branch_1"]["n_states"] + r["invariant_branch_2"]["n_states"]
        for r in ok_results
    )

    verdict = (
        "CONFIRMED"
        if (
            n_blocked == 0
            and all_isomorphisms_confirmed
            and all_phi_release_matches
            and all_invariants_hold
            and all_corollaries_match
        )
        else "CRITERION_INVALID"
    )

    out = {
        "claim": "H-B7-28 -- FGFR3=True/GRB2=False/EGFR=False invariant and the resulting "
        "phi=flip(EGFR_stimulus) branch isomorphism, extended to H-B7-22's own full "
        "originally-tested domain (k=1..40, both branches, 80 conditions)",
        "n_conditions_tested": len(results),
        "n_ok": len(ok_results),
        "n_blocked_infrastructure": n_blocked,
        "n_states_scanned": n_states_scanned,
        "all_isomorphisms_confirmed": all_isomorphisms_confirmed,
        "all_phi_release_matches": all_phi_release_matches,
        "all_invariants_hold": all_invariants_hold,
        "all_corollaries_match": all_corollaries_match,
        "verdict": verdict,
        "results": results,
    }

    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    print(
        json.dumps(
            {k: v for k, v in out.items() if k != "results"}
            | {
                "sample_results": [
                    {
                        "k": r["k"],
                        "status": r["status"],
                        "isomorphism_confirmed": r.get("isomorphism", {}).get(
                            "isomorphism_confirmed"
                        ),
                        "invariant_holds_both": (
                            r["invariant_branch_1"]["invariant_holds"]
                            and r["invariant_branch_2"]["invariant_holds"]
                        )
                        if r["status"] == "OK"
                        else None,
                    }
                    for r in results
                    if r["k"] in (1, 4, 5, 6, 20, 40)
                ]
            },
            indent=2,
            default=str,
        )
    )
    return out


if __name__ == "__main__":
    cmd_run()
