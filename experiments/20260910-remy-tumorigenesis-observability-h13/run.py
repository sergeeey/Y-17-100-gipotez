"""run.py -- H-B7-13: observability collision search. Does a small marker set M, observed at the
moment the transient do(p21CIP=0, RBL2=0) clamp would be released, determine the eventual fate
(Growth_arrest vs Proliferation) as reliably as the full state does, across the release-state
domain this bridge's own transient-clamp protocol family already defines (both bistable branches,
k=1..40)?

Reuses H-B7-1's pipeline functions (parse_bnet, compile_rules, synchronous_step), H-B7-2's
clamp_rule, H-B7-3's run_until_attractor, H-B7-4's branch-1 constants, H-B7-11's branch-2
constants -- all UNCHANGED via distinct-name import (H-CAT37-2's established pattern for avoiding
the run.py-collision bug).

Adds ONE new function: simulate_transient_clamp_multi_with_release_state, a thin extension of
H-B7-9's simulate_transient_clamp_multi that also returns the state AT THE MOMENT OF RELEASE
(after k clamp-steps, before the clamp is lifted) -- the actual "observable state" a real release
decision would be made from, which the existing function does not expose (it only returns the
FINAL post-release attractor state).
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
DATA = H_B7_4_DIR / "data" / "remy_tumorigenesis.bnet"
METRICS = HERE / "metrics"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


h1 = _load_module("h_b7_13_h1", H_B7_1_DIR / "run.py")
h2 = _load_module("h_b7_13_h2", H_B7_2_DIR / "run.py")
h3 = _load_module("h_b7_13_h3", H_B7_3_DIR / "run.py")
h4 = _load_module("h_b7_13_h4", H_B7_4_DIR / "run.py")
h11 = _load_module("h_b7_13_h11", H_B7_11_DIR / "run.py")

PYBOOLNET_NODE_ORDER = h4.PYBOOLNET_NODE_ORDER
BRANCH_INPUTS_1 = h4.BRANCH_INPUTS
GROWTH_ARREST_STATE_1 = h4.GROWTH_ARREST_STATE
BRANCH_INPUTS_2 = h11.BRANCH_INPUTS_2
GROWTH_ARREST_STATE_2 = h11.GROWTH_ARREST_STATE_2

CLAMPS = {"p21CIP": False, "RBL2": False}
TESTED_DURATIONS = list(range(1, 41))  # k = 1..40, dense superset of H-B7-9/10/12's sparse sweep

FLOOR_M = {"DNA_damage"}
CEILING_M = set(PYBOOLNET_NODE_ORDER)
CANDIDATE_M1 = {"Growth_arrest", "Proliferation"}
CANDIDATE_M2 = {"p21CIP", "RBL2", "Growth_arrest", "Proliferation"}


def simulate_transient_clamp_multi_with_release_state(
    initial_state: dict, node_names: list, wild_type_rules: dict, clamped_nodes: dict, k_steps: int
) -> dict:
    """Apply `clamped_nodes` for exactly `k_steps` synchronous updates, capture the RELEASE-MOMENT
    state (before the clamp is lifted -- the actual observable at decision time), then release and
    run to the eventual attractor. Extends H-B7-9's simulate_transient_clamp_multi, whose return
    value only exposes the FINAL state, not this intermediate one."""
    clamped_rules = dict(wild_type_rules)
    for node, value in clamped_nodes.items():
        clamped_rules = h2.clamp_rule(clamped_rules, node, value)

    current = dict(initial_state)
    for node, value in clamped_nodes.items():
        current[node] = value
    for _ in range(k_steps):
        current = h1.synchronous_step(current, clamped_rules)
    release_state = dict(current)

    final_cycle = h3.run_until_attractor(current, wild_type_rules, node_names)
    final_state = final_cycle[0]
    return {
        "release_state": release_state,
        "final_state": final_state,
        "period": len(final_cycle),
    }


def fate_label(final_state: dict) -> str:
    ga = final_state.get("Growth_arrest")
    prolif = final_state.get("Proliferation")
    if prolif and not ga:
        return "PROLIFERATION"
    if ga:
        return "GROWTH_ARREST"
    return "AMBIGUOUS"


def marker_projection(state: dict, markers: set) -> tuple:
    return tuple(sorted((n, state[n]) for n in markers))


def find_collisions(domain: list[dict], markers: set) -> list[dict]:
    """domain: list of {branch, k, release_state, fate}. Groups entries by their `markers`
    projection of release_state; returns groups where >=2 distinct fates appear -- each such
    group is a falsifying collision for this marker set."""
    groups: dict[tuple, list[dict]] = {}
    for entry in domain:
        proj = marker_projection(entry["release_state"], markers)
        groups.setdefault(proj, []).append(entry)

    collisions = []
    for proj, entries in groups.items():
        fates = {e["fate"] for e in entries}
        if len(fates) > 1:
            collisions.append(
                {
                    "marker_projection": [{"node": n, "value": v} for n, v in proj],
                    "members": [
                        {"branch": e["branch"], "k": e["k"], "fate": e["fate"]} for e in entries
                    ],
                }
            )
    return collisions


def cmd_run() -> dict:
    text = DATA.read_text(encoding="utf-8")
    rules = h1.parse_bnet(text)
    node_names = [name for name, _ in rules]
    wild_type_rules = h1.compile_rules(rules)

    branches = [
        ("branch_1", GROWTH_ARREST_STATE_1, BRANCH_INPUTS_1),
        ("branch_2", GROWTH_ARREST_STATE_2, BRANCH_INPUTS_2),
    ]

    domain: list[dict] = []
    for branch_name, growth_arrest_state, branch_inputs in branches:
        start_state = dict(zip(PYBOOLNET_NODE_ORDER, (c == "1" for c in growth_arrest_state)))
        for k in TESTED_DURATIONS:
            sim = simulate_transient_clamp_multi_with_release_state(
                start_state, node_names, wild_type_rules, CLAMPS, k
            )
            domain.append(
                {
                    "branch": branch_name,
                    "k": k,
                    "release_state": sim["release_state"],
                    "final_state": sim["final_state"],
                    "fate": fate_label(sim["final_state"]),
                    "branch_inputs_preserved_at_final": all(
                        sim["final_state"][n] == v for n, v in branch_inputs.items()
                    ),
                }
            )

    results = {}
    for m_name, m_set in [
        ("floor_DNA_damage_only", FLOOR_M),
        ("ceiling_full_state", CEILING_M),
        ("candidate_M1_phenotypes_only", CANDIDATE_M1),
        ("candidate_M2_phenotypes_plus_clamp_targets", CANDIDATE_M2),
    ]:
        collisions = find_collisions(domain, m_set)
        results[m_name] = {
            "markers": sorted(m_set),
            "n_collisions": len(collisions),
            "sufficient": len(collisions) == 0,
            "collisions": collisions[:5],  # cap printed detail, full count still reported
        }

    domain_summary = [
        {"branch": e["branch"], "k": e["k"], "fate": e["fate"]}
        for e in domain
        if e["k"] in (1, 4, 5, 6, 40) or e["k"] == TESTED_DURATIONS[0]
    ]

    out = {
        "claim": "H-B7-13 observability collision search",
        "domain_size": len(domain),
        "tested_durations_range": [TESTED_DURATIONS[0], TESTED_DURATIONS[-1]],
        "branches_tested": [b[0] for b in branches],
        "domain_summary_sample": domain_summary,
        "results": results,
        "floor_test_detects_insufficiency": not results["floor_DNA_damage_only"]["sufficient"],
        "ceiling_test_shows_no_spurious_collision": results["ceiling_full_state"]["sufficient"],
    }

    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    print(json.dumps(out, indent=2, default=str))
    return out


if __name__ == "__main__":
    cmd_run()
