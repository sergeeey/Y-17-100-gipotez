"""run.py -- H-B7-27: mechanistic explanation of H-B7-26's own unplanned observation that
branch_1 and branch_2 give numerically identical exact escape probabilities at every k.

Mechanism found by Compute-First Check: GROWTH_ARREST_STATE_1/_2 differ at exactly one node,
EGFR_stimulus. EGFR's own rule (!GRB2 & !FGFR3 & (SPRY | EGFR_stimulus)) only reads EGFR_stimulus
when !GRB2 & !FGFR3 holds -- and FGFR3=True / GRB2=False is a zero-exception invariant across the
ENTIRE reachable region for both branches, all k=1..5. So EGFR_stimulus is causally inert there,
and phi = flip(EGFR_stimulus) is a genuine graph automorphism-inducing bijection between the two
branches' reachable graphs -- not a coincidence.

Reuses H-B7-22's build_reachability_graph UNCHANGED (via H-B7-26's own import); reuses H-B7-26's
solve_absorption UNCHANGED for the corollary re-derivation check.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
H_B7_26_DIR = HERE.parent / "20260910-remy-tumorigenesis-exact-absorption-h26"
METRICS = HERE / "metrics"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


h26 = _load_module("h_b7_27_h26", H_B7_26_DIR / "run.py")
h22 = h26.h22
h13 = h26.h13
h1 = h26.h1

PYBOOLNET_NODE_ORDER = h26.PYBOOLNET_NODE_ORDER
GROWTH_ARREST_STATE_1 = h26.GROWTH_ARREST_STATE_1
GROWTH_ARREST_STATE_2 = h26.GROWTH_ARREST_STATE_2
CLAMPS = h26.CLAMPS
STATE_CAP = h22.STATE_CAP
build_reachability_graph = h22.build_reachability_graph
solve_absorption = h26.solve_absorption

CONDITIONS_K = [1, 2, 3, 4, 5]


def build_phi(node_names: list, flip_node: str):
    """Returns phi(state_tuple) that flips exactly `flip_node`'s coordinate, identity elsewhere."""
    idx = node_names.index(flip_node)

    def phi(state_tuple: tuple) -> tuple:
        state_list = list(state_tuple)
        state_list[idx] = not state_list[idx]
        return tuple(state_list)

    return phi


def check_isomorphism(g1, g2, phi) -> dict:
    g1_nodes = set(g1.nodes())
    g2_nodes = set(g2.nodes())
    phi_g1_nodes = {phi(s) for s in g1_nodes}
    node_set_bijection = phi_g1_nodes == g2_nodes

    if not node_set_bijection:
        return {
            "node_set_bijection": False,
            "edges_g1_to_g2_preserved": None,
            "edges_g2_to_g1_preserved": None,
            "isomorphism_confirmed": False,
        }

    edges_g1_to_g2 = all(g2.has_edge(phi(x), phi(y)) for x, y in g1.edges())
    edges_g2_to_g1 = all(g1.has_edge(phi(x), phi(y)) for x, y in g2.edges())

    return {
        "node_set_bijection": True,
        "edges_g1_to_g2_preserved": edges_g1_to_g2,
        "edges_g2_to_g1_preserved": edges_g2_to_g1,
        "isomorphism_confirmed": edges_g1_to_g2 and edges_g2_to_g1,
    }


def check_invariant(graph, node_names: list) -> dict:
    """Checks FGFR3=True and GRB2=False across every state in the graph -- the actual mechanism."""
    fgfr3_idx = node_names.index("FGFR3")
    grb2_idx = node_names.index("GRB2")
    egfr_idx = node_names.index("EGFR")

    n_states = graph.number_of_nodes()
    n_fgfr3_false = sum(1 for s in graph.nodes() if not s[fgfr3_idx])
    n_grb2_true = sum(1 for s in graph.nodes() if s[grb2_idx])
    n_egfr_true = sum(1 for s in graph.nodes() if s[egfr_idx])

    return {
        "n_states": n_states,
        "n_fgfr3_false": n_fgfr3_false,
        "n_grb2_true": n_grb2_true,
        "n_egfr_true": n_egfr_true,
        "invariant_holds": (n_fgfr3_false == 0 and n_grb2_true == 0 and n_egfr_true == 0),
    }


def cmd_run() -> dict:
    text = h13.DATA.read_text(encoding="utf-8")
    rules = h1.parse_bnet(text)
    node_names = [name for name, _ in rules]
    wild_type_rules = h1.compile_rules(rules)

    phi = build_phi(node_names, "EGFR_stimulus")

    h26_data = json.loads((H_B7_26_DIR / "metrics" / "run.json").read_text(encoding="utf-8"))
    h26_by_cond = {(r["branch"], r["k"]): r for r in h26_data["results"]}

    branches = {
        "branch_1": GROWTH_ARREST_STATE_1,
        "branch_2": GROWTH_ARREST_STATE_2,
    }

    graphs_by_cond = {}
    release_by_cond = {}
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
            graphs_by_cond[(branch_name, k)] = graph_result["graph"]
            release_by_cond[(branch_name, k)] = release_tuple

    results = []
    for k in CONDITIONS_K:
        g1 = graphs_by_cond[("branch_1", k)]
        g2 = graphs_by_cond[("branch_2", k)]
        release_1 = release_by_cond[("branch_1", k)]
        release_2 = release_by_cond[("branch_2", k)]

        iso = check_isomorphism(g1, g2, phi)
        phi_release_matches = phi(release_1) == release_2

        inv_1 = check_invariant(g1, node_names)
        inv_2 = check_invariant(g2, node_names)

        # corollary: independently re-derive exact escape probability on both graphs, compare
        # to H-B7-26's own committed values (regression check on graph construction, not a
        # re-validation of H-B7-26's Monte Carlo oracle gate)
        solved_1 = solve_absorption(g1, release_1, node_names)
        solved_2 = solve_absorption(g2, release_2, node_names)
        h26_1 = h26_by_cond[("branch_1", k)]
        h26_2 = h26_by_cond[("branch_2", k)]
        corollary_matches = (
            solved_1["status"] == "OK"
            and solved_2["status"] == "OK"
            and abs(solved_1["exact_escape_probability"] - h26_1["exact_escape_probability"]) < 1e-9
            and abs(solved_2["exact_escape_probability"] - h26_2["exact_escape_probability"]) < 1e-9
            and abs(solved_1["exact_escape_probability"] - solved_2["exact_escape_probability"])
            < 1e-9
        )

        results.append(
            {
                "k": k,
                "phi_release_1_equals_release_2": phi_release_matches,
                "isomorphism": iso,
                "invariant_branch_1": inv_1,
                "invariant_branch_2": inv_2,
                "corollary_escape_probability_matches": corollary_matches,
                "exact_escape_probability_branch_1": solved_1["exact_escape_probability"],
                "exact_escape_probability_branch_2": solved_2["exact_escape_probability"],
            }
        )

    all_isomorphisms_confirmed = all(r["isomorphism"]["isomorphism_confirmed"] for r in results)
    all_phi_release_matches = all(r["phi_release_1_equals_release_2"] for r in results)
    all_invariants_hold = all(
        r["invariant_branch_1"]["invariant_holds"] and r["invariant_branch_2"]["invariant_holds"]
        for r in results
    )
    all_corollaries_match = all(r["corollary_escape_probability_matches"] for r in results)

    verdict = (
        "CONFIRMED"
        if (
            all_isomorphisms_confirmed
            and all_phi_release_matches
            and all_invariants_hold
            and all_corollaries_match
        )
        else "CRITERION_INVALID"
    )

    out = {
        "claim": "H-B7-27 -- phi=flip(EGFR_stimulus) is a graph automorphism-inducing bijection "
        "between branch_1 and branch_2's reachable graphs, mechanistically caused by a "
        "zero-exception FGFR3=True/GRB2=False invariant across the entire reachable region",
        "n_conditions_tested": len(results),
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
                "results_summary": [
                    {
                        "k": r["k"],
                        "isomorphism_confirmed": r["isomorphism"]["isomorphism_confirmed"],
                        "invariant_holds_both": (
                            r["invariant_branch_1"]["invariant_holds"]
                            and r["invariant_branch_2"]["invariant_holds"]
                        ),
                        "corollary_matches": r["corollary_escape_probability_matches"],
                        "exact_escape_probability": r["exact_escape_probability_branch_1"],
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
