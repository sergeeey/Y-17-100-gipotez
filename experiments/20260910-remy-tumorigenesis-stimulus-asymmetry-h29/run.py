"""run.py -- H-B7-29: contrast/control test for H-B7-27/28's own EGFR_stimulus-inertness finding.

Tests whether FGFR3_stimulus (the OTHER frozen self-loop exogenous stimulus node in this model)
is ALSO inert like EGFR_stimulus, or -- as predicted from FGFR3's own rule directly reading
FGFR3_stimulus -- genuinely load-bearing, breaking the isomorphism when flipped.

Reuses H-B7-27's own build_phi/check_isomorphism UNCHANGED. Does NOT reuse solve_absorption --
a condition that hits STATE_CAP cannot have its absorption probability computed (the transition
matrix would be incomplete), so this experiment only checks graph-structural facts, never solves
a linear system on a capped graph.
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


h27 = _load_module("h_b7_29_h27", H_B7_27_DIR / "run.py")
h22 = h27.h22
h13 = h27.h13
h1 = h27.h1

PYBOOLNET_NODE_ORDER = h27.PYBOOLNET_NODE_ORDER
GROWTH_ARREST_STATE_1 = h27.GROWTH_ARREST_STATE_1
GROWTH_ARREST_STATE_2 = h27.GROWTH_ARREST_STATE_2
CLAMPS = h27.CLAMPS
STATE_CAP = h22.STATE_CAP
build_reachability_graph = h22.build_reachability_graph
build_phi = h27.build_phi
check_isomorphism = h27.check_isomorphism

CONDITIONS_K = [1, 2, 3, 4, 5]
FLIP_NODE = "FGFR3_stimulus"


def cmd_run() -> dict:
    text = h13.DATA.read_text(encoding="utf-8")
    rules = h1.parse_bnet(text)
    node_names = [name for name, _ in rules]
    wild_type_rules = h1.compile_rules(rules)

    phi_prime = build_phi(node_names, FLIP_NODE)
    fgfr3_idx = node_names.index("FGFR3")

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
            release_orig = tuple(sim["release_state"][n] for n in node_names)
            release_flipped = phi_prime(release_orig)

            graph_orig_result = build_reachability_graph(
                release_orig, node_names, wild_type_rules, STATE_CAP
            )
            graph_flipped_result = build_reachability_graph(
                release_flipped, node_names, wild_type_rules, STATE_CAP
            )

            g_orig = graph_orig_result["graph"]
            g_flipped = graph_flipped_result["graph"]

            iso = check_isomorphism(g_orig, g_flipped, phi_prime)

            n_orig = g_orig.number_of_nodes()
            n_flipped_capped = g_flipped.number_of_nodes()
            flipped_hit_cap = graph_flipped_result["hit_cap"]

            # cap-independent non-bijection check: if the flipped (possibly capped) graph's
            # node count already differs from the original, no bijection is possible, no
            # uncapped count needed
            size_alone_rules_out_bijection = n_orig != n_flipped_capped

            n_fgfr3_false_flipped = None
            if not flipped_hit_cap:
                n_fgfr3_false_flipped = sum(1 for s in g_flipped.nodes() if not s[fgfr3_idx])

            results.append(
                {
                    "branch": branch_name,
                    "k": k,
                    "n_states_original": n_orig,
                    "n_states_flipped_capped": n_flipped_capped,
                    "flipped_hit_cap": flipped_hit_cap,
                    "size_alone_rules_out_bijection": size_alone_rules_out_bijection,
                    "isomorphism": iso,
                    "isomorphism_confirmed": iso["isomorphism_confirmed"],
                    "n_fgfr3_false_in_flipped_graph": n_fgfr3_false_flipped,
                    "asymmetry_confirmed_this_condition": not iso["isomorphism_confirmed"],
                }
            )

    all_asymmetry_confirmed = all(r["asymmetry_confirmed_this_condition"] for r in results)
    n_hit_cap = sum(1 for r in results if r["flipped_hit_cap"])

    verdict = "CONFIRMED" if all_asymmetry_confirmed else "CRITERION_INVALID"

    out = {
        "claim": "H-B7-29 -- unlike EGFR_stimulus (H-B7-27/28), FGFR3_stimulus is NOT causally "
        "inert: flipping it breaks the isomorphism, confirming a genuine structural asymmetry "
        "between the two structurally-similar frozen self-loop stimulus nodes",
        "flip_node": FLIP_NODE,
        "n_conditions_tested": len(results),
        "n_hit_state_cap": n_hit_cap,
        "all_asymmetry_confirmed": all_asymmetry_confirmed,
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
                        "n_states_original": r["n_states_original"],
                        "n_states_flipped_capped": r["n_states_flipped_capped"],
                        "flipped_hit_cap": r["flipped_hit_cap"],
                        "isomorphism_confirmed": r["isomorphism_confirmed"],
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
