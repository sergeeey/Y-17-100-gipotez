"""run.py -- H-B7-14: does observing marker set M a fixed delay `j` steps AFTER the transient
clamp is released (instead of AT the release instant, H-B7-13's own finding: REJECTED for both
M1/M2) restore observability? Minimal Relaxation Rule variant of H-B7-13 -- ONE assumption
changed (observation timing), everything else held fixed.

Reuses H-B7-13's simulate_transient_clamp_multi_with_release_state, fate_label,
marker_projection, find_collisions, FLOOR_M, CEILING_M, CANDIDATE_M1, CANDIDATE_M2 UNCHANGED via
distinct-name import (H-CAT37-2's established run.py-collision-avoidance pattern).
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
H_B7_1_DIR = HERE.parent / "20260906-kauffman-cellcycle-attractors-h1"
H_B7_2_DIR = HERE.parent / "20260906-kauffman-cellcycle-perturbation-h2"
H_B7_3_DIR = HERE.parent / "20260906-kauffman-cellcycle-transient-h3"
H_B7_4_DIR = HERE.parent / "20260906-remy-tumorigenesis-transient-h4"
H_B7_11_DIR = HERE.parent / "20260906-remy-tumorigenesis-crossbranch-h11"
H_B7_13_DIR = HERE.parent / "20260910-remy-tumorigenesis-observability-h13"
DATA = H_B7_4_DIR / "data" / "remy_tumorigenesis.bnet"
METRICS = HERE / "metrics"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


h1 = _load_module("h_b7_14_h1", H_B7_1_DIR / "run.py")
h2 = _load_module("h_b7_14_h2", H_B7_2_DIR / "run.py")
h3 = _load_module("h_b7_14_h3", H_B7_3_DIR / "run.py")
h4 = _load_module("h_b7_14_h4", H_B7_4_DIR / "run.py")
h11 = _load_module("h_b7_14_h11", H_B7_11_DIR / "run.py")
h13 = _load_module("h_b7_14_h13", H_B7_13_DIR / "run.py")

PYBOOLNET_NODE_ORDER = h13.PYBOOLNET_NODE_ORDER
BRANCH_INPUTS_1 = h13.BRANCH_INPUTS_1
GROWTH_ARREST_STATE_1 = h13.GROWTH_ARREST_STATE_1
BRANCH_INPUTS_2 = h13.BRANCH_INPUTS_2
GROWTH_ARREST_STATE_2 = h13.GROWTH_ARREST_STATE_2
CLAMPS = h13.CLAMPS
TESTED_DURATIONS = h13.TESTED_DURATIONS
FLOOR_M = h13.FLOOR_M
CEILING_M = h13.CEILING_M
CANDIDATE_M1 = h13.CANDIDATE_M1
CANDIDATE_M2 = h13.CANDIDATE_M2
fate_label = h13.fate_label
find_collisions = h13.find_collisions

SWEPT_J = [0, 1, 2, 3, 4, 5, 7, 10]


def simulate_transient_clamp_multi_with_delayed_observation(
    initial_state: dict,
    node_names: list,
    wild_type_rules: dict,
    clamped_nodes: dict,
    k_steps: int,
    j_steps: int,
) -> dict:
    """Apply `clamped_nodes` for `k_steps`, release, run `j_steps` MORE synchronous steps under
    WILD-TYPE rules, capture that as `observed_state`, then continue to the eventual attractor for
    `final_state`. `j_steps=0` must reproduce H-B7-13's own `release_state` exactly (regression
    check, verified in tests/)."""
    clamped_rules = dict(wild_type_rules)
    for node, value in clamped_nodes.items():
        clamped_rules = h2.clamp_rule(clamped_rules, node, value)

    current = dict(initial_state)
    for node, value in clamped_nodes.items():
        current[node] = value
    for _ in range(k_steps):
        current = h1.synchronous_step(current, clamped_rules)
    # released: continue under wild-type rules from here
    for _ in range(j_steps):
        current = h1.synchronous_step(current, wild_type_rules)
    observed_state = dict(current)

    final_cycle = h3.run_until_attractor(current, wild_type_rules, node_names)
    return {"observed_state": observed_state, "final_state": final_cycle[0]}


def build_domain_for_j(node_names, wild_type_rules, j: int) -> list[dict]:
    branches = [
        ("branch_1", GROWTH_ARREST_STATE_1),
        ("branch_2", GROWTH_ARREST_STATE_2),
    ]
    domain = []
    for branch_name, growth_arrest_state in branches:
        start_state = dict(zip(PYBOOLNET_NODE_ORDER, (c == "1" for c in growth_arrest_state)))
        for k in TESTED_DURATIONS:
            sim = simulate_transient_clamp_multi_with_delayed_observation(
                start_state, node_names, wild_type_rules, CLAMPS, k, j
            )
            domain.append(
                {
                    "branch": branch_name,
                    "k": k,
                    "release_state": sim["observed_state"],  # find_collisions reads this key
                    "fate": fate_label(sim["final_state"]),
                }
            )
    return domain


def cmd_run() -> dict:
    text = DATA.read_text(encoding="utf-8")
    rules = h1.parse_bnet(text)
    node_names = [name for name, _ in rules]
    wild_type_rules = h1.compile_rules(rules)

    sweep_results = []
    for j in SWEPT_J:
        domain = build_domain_for_j(node_names, wild_type_rules, j)
        per_marker_set = {}
        for m_name, m_set in [
            ("floor_DNA_damage_only", FLOOR_M),
            ("ceiling_full_state", CEILING_M),
            ("candidate_M1_phenotypes_only", CANDIDATE_M1),
            ("candidate_M2_phenotypes_plus_clamp_targets", CANDIDATE_M2),
        ]:
            collisions = find_collisions(domain, m_set)
            per_marker_set[m_name] = {
                "n_collisions": len(collisions),
                "sufficient": len(collisions) == 0,
            }
        sweep_results.append({"j": j, "results": per_marker_set})

    def first_sufficient_j(marker_set_key: str):
        for row in sweep_results:
            if row["results"][marker_set_key]["sufficient"]:
                return row["j"]
        return None

    m1_j0 = sweep_results[0]["results"]["candidate_M1_phenotypes_only"]
    m2_j0 = sweep_results[0]["results"]["candidate_M2_phenotypes_plus_clamp_targets"]

    out = {
        "claim": "H-B7-14 delayed-observation sweep (Minimal Relaxation Rule variant of H-B7-13)",
        "swept_j": SWEPT_J,
        "sweep_results": sweep_results,
        "j0_regression_check": {
            "candidate_M1_n_collisions": m1_j0["n_collisions"],
            "candidate_M2_n_collisions": m2_j0["n_collisions"],
            "h_b7_13_committed_M1_n_collisions": 1,
            "h_b7_13_committed_M2_n_collisions": 1,
            "matches_h_b7_13": (m1_j0["n_collisions"] == 1 and m2_j0["n_collisions"] == 1),
        },
        "first_sufficient_j": {
            "candidate_M1_phenotypes_only": first_sufficient_j("candidate_M1_phenotypes_only"),
            "candidate_M2_phenotypes_plus_clamp_targets": first_sufficient_j(
                "candidate_M2_phenotypes_plus_clamp_targets"
            ),
        },
    }

    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    print(json.dumps(out, indent=2, default=str))
    return out


if __name__ == "__main__":
    cmd_run()
