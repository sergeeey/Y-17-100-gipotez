"""run.py -- H-B7-26: EXACT asynchronous escape probability, via absorbing Markov chain theory,
for each of H-B7-23's own 10 tested (branch, k) conditions. Replaces H-B7-23's Monte Carlo
estimates with exact numbers (linear algebra, not sampling), validated against H-B7-23's own
committed 95% CI as a mandatory oracle gate -- exactly the redirect the user proposed after a
cross-domain/sci-hypothesis report's own informal large-deviation framing was found weaker than
its R^2 suggested, and after a literature check found async-BN-as-Markov-chain already
established.

Reuses H-B7-22's build_reachability_graph/async_successors UNCHANGED; reuses H-B7-13's
release-state construction. The uniform-random-among-unstable-nodes transition model is
H-B7-23's own, not new here -- this experiment solves it exactly instead of sampling it.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
H_B7_22_DIR = HERE.parent / "20260910-remy-tumorigenesis-adversarial-async-h22"
H_B7_23_DIR = HERE.parent / "20260910-remy-tumorigenesis-random-async-vulnerability-h23"
METRICS = HERE / "metrics"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


h22 = _load_module("h_b7_26_h22", H_B7_22_DIR / "run.py")
h13 = h22.h13
h1 = h22.h1

PYBOOLNET_NODE_ORDER = h22.PYBOOLNET_NODE_ORDER
GROWTH_ARREST_STATE_1 = h22.GROWTH_ARREST_STATE_1
GROWTH_ARREST_STATE_2 = h22.GROWTH_ARREST_STATE_2
CLAMPS = h22.CLAMPS
STATE_CAP = h22.STATE_CAP
build_reachability_graph = h22.build_reachability_graph

CONDITIONS_K = [1, 2, 3, 4, 5]  # 5 is the mandatory positive control, matching H-B7-23's own set


def classify_absorbing_state(state_tuple: tuple, node_names: list) -> str:
    prolif_idx = node_names.index("Proliferation")
    ga_idx = node_names.index("Growth_arrest")
    if state_tuple[prolif_idx] and not state_tuple[ga_idx]:
        return "PROLIFERATION"
    if state_tuple[ga_idx]:
        return "GROWTH_ARREST"
    return "AMBIGUOUS"


def solve_absorption(graph, release_tuple, node_names: list) -> dict:
    """Builds the exact transient-to-transient sub-transition-matrix Q and solves
    (I - Q) q = b for absorption probability into PROLIFERATION-class absorbing states, plus
    expected steps to absorption via the fundamental matrix N = (I - Q)^-1."""
    state_list = list(graph.nodes())

    absorbing_prolif = set()
    absorbing_ga = set()
    ambiguous = set()
    transient = []
    for s in state_list:
        if graph.out_degree(s) == 0:
            fate = classify_absorbing_state(s, node_names)
            if fate == "PROLIFERATION":
                absorbing_prolif.add(s)
            elif fate == "GROWTH_ARREST":
                absorbing_ga.add(s)
            else:
                ambiguous.add(s)
        else:
            transient.append(s)

    if ambiguous:
        return {"status": "AMBIGUOUS_ABSORBING_STATE", "n_ambiguous": len(ambiguous)}

    t_index = {s: i for i, s in enumerate(transient)}
    m = len(transient)
    identity_minus_q = np.zeros((m, m))
    b = np.zeros(m)
    for s in transient:
        i = t_index[s]
        succs = list(graph.successors(s))
        deg = len(succs)
        identity_minus_q[i, i] = 1.0
        for y in succs:
            p = 1.0 / deg
            if y in absorbing_prolif:
                b[i] += p
            elif y in absorbing_ga:
                pass
            else:
                identity_minus_q[i, t_index[y]] -= p

    q = np.linalg.solve(identity_minus_q, b)

    # Expected steps to absorption: N = (I-Q)^-1, expected_steps = N @ ones
    n_matrix = np.linalg.inv(identity_minus_q)
    expected_steps_vec = n_matrix @ np.ones(m)

    if release_tuple not in t_index:
        # release state is itself absorbing (e.g. k=5 lands directly on a fixed point)
        if release_tuple in absorbing_prolif:
            return {
                "status": "OK",
                "n_transient": m,
                "n_absorbing_prolif": len(absorbing_prolif),
                "n_absorbing_ga": len(absorbing_ga),
                "exact_escape_probability": 1.0,
                "expected_steps_to_absorption": 0.0,
            }
        if release_tuple in absorbing_ga:
            return {
                "status": "OK",
                "n_transient": m,
                "n_absorbing_prolif": len(absorbing_prolif),
                "n_absorbing_ga": len(absorbing_ga),
                "exact_escape_probability": 0.0,
                "expected_steps_to_absorption": 0.0,
            }

    idx = t_index[release_tuple]
    return {
        "status": "OK",
        "n_transient": m,
        "n_absorbing_prolif": len(absorbing_prolif),
        "n_absorbing_ga": len(absorbing_ga),
        "exact_escape_probability": float(q[idx]),
        "expected_steps_to_absorption": float(expected_steps_vec[idx]),
    }


def cmd_run() -> dict:
    text = h13.DATA.read_text(encoding="utf-8")
    rules = h1.parse_bnet(text)
    node_names = [name for name, _ in rules]
    wild_type_rules = h1.compile_rules(rules)

    h23_data = json.loads((H_B7_23_DIR / "metrics" / "run.json").read_text(encoding="utf-8"))
    mc_by_cond = {(r["branch"], r["k"]): r for r in h23_data["results"]}

    branches = [
        ("branch_1", GROWTH_ARREST_STATE_1),
        ("branch_2", GROWTH_ARREST_STATE_2),
    ]

    results = []
    for branch_name, growth_arrest_state in branches:
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
                results.append({"branch": branch_name, "k": k, "status": "BLOCKED-INFRASTRUCTURE"})
                continue

            solved = solve_absorption(graph_result["graph"], release_tuple, node_names)
            solved["branch"] = branch_name
            solved["k"] = k
            solved["n_states_in_graph"] = graph_result["graph"].number_of_nodes()

            mc = mc_by_cond.get((branch_name, k))
            if mc and solved["status"] == "OK":
                lo, hi = mc["prolif_fraction_ci95"]
                solved["monte_carlo_estimate"] = mc["prolif_fraction"]
                solved["monte_carlo_ci95"] = [lo, hi]
                solved["oracle_gate_passed"] = lo <= solved["exact_escape_probability"] <= hi

            results.append(solved)

    ok_results = [r for r in results if r["status"] == "OK"]
    oracle_results = [r for r in ok_results if "oracle_gate_passed" in r]
    oracle_all_passed = all(r["oracle_gate_passed"] for r in oracle_results)
    n_oracle_checked = len(oracle_results)
    n_oracle_passed = sum(1 for r in oracle_results if r["oracle_gate_passed"])

    k5_results = [r for r in ok_results if r["k"] == 5]
    k5_all_exactly_one = all(r["exact_escape_probability"] == 1.0 for r in k5_results)

    verdict = "CONFIRMED" if (oracle_all_passed and k5_all_exactly_one) else "CRITERION_INVALID"

    out = {
        "claim": "H-B7-26 -- exact asynchronous escape probability via absorbing Markov chain, "
        "validated against H-B7-23's own Monte Carlo CIs as an oracle gate",
        "n_conditions_tested": len(results),
        "n_ok": len(ok_results),
        "n_oracle_checked": n_oracle_checked,
        "n_oracle_passed": n_oracle_passed,
        "oracle_gate_all_passed": oracle_all_passed,
        "k5_positive_control_all_exactly_one": k5_all_exactly_one,
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
                        "status": r["status"],
                        "exact_escape_probability": r.get("exact_escape_probability"),
                        "monte_carlo_estimate": r.get("monte_carlo_estimate"),
                        "oracle_gate_passed": r.get("oracle_gate_passed"),
                        "expected_steps_to_absorption": r.get("expected_steps_to_absorption"),
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
