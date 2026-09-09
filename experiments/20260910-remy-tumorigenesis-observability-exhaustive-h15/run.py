"""run.py -- H-B7-15: EXHAUSTIVE (not sampled) verification of H-B7-14's j*=1 sufficiency claim,
over the COMPLETE clamped-trajectory orbit -- every achievable release-state for k=1,2,3,...
(unbounded), not just the tested k=1..40 sweep.

Key structural fact (Compute-First Check, see claim.md): the clamped phase is a deterministic walk
under a FIXED rule-set, so it MUST eventually enter a cycle (pigeonhole, same argument H-B7-1's
find_attractors and H-B7-3's run_until_attractor already rely on). Walking until that cycle is
detected gives the COMPLETE, finite set of achievable release-states for ANY k -- not a truncated
sample.

Reuses H-B7-13's PYBOOLNET_NODE_ORDER, BRANCH_INPUTS_1/2, GROWTH_ARREST_STATE_1/2, CLAMPS,
FLOOR_M, CEILING_M, CANDIDATE_M1, CANDIDATE_M2, fate_label, marker_projection, find_collisions,
and H-B7-14's simulate_transient_clamp_multi_with_delayed_observation UNCHANGED via distinct-name
import. Adds ONE new function: walk_clamped_trajectory_until_cycle.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
H_B7_1_DIR = HERE.parent / "20260906-kauffman-cellcycle-attractors-h1"
H_B7_2_DIR = HERE.parent / "20260906-kauffman-cellcycle-perturbation-h2"
H_B7_4_DIR = HERE.parent / "20260906-remy-tumorigenesis-transient-h4"
H_B7_13_DIR = HERE.parent / "20260910-remy-tumorigenesis-observability-h13"
H_B7_14_DIR = HERE.parent / "20260910-remy-tumorigenesis-observability-delayed-h14"
DATA = H_B7_4_DIR / "data" / "remy_tumorigenesis.bnet"
METRICS = HERE / "metrics"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


h1 = _load_module("h_b7_15_h1", H_B7_1_DIR / "run.py")
h2 = _load_module("h_b7_15_h2", H_B7_2_DIR / "run.py")
h13 = _load_module("h_b7_15_h13", H_B7_13_DIR / "run.py")
h14 = _load_module("h_b7_15_h14", H_B7_14_DIR / "run.py")

PYBOOLNET_NODE_ORDER = h13.PYBOOLNET_NODE_ORDER
BRANCH_INPUTS_1 = h13.BRANCH_INPUTS_1
GROWTH_ARREST_STATE_1 = h13.GROWTH_ARREST_STATE_1
BRANCH_INPUTS_2 = h13.BRANCH_INPUTS_2
GROWTH_ARREST_STATE_2 = h13.GROWTH_ARREST_STATE_2
CLAMPS = h13.CLAMPS
FLOOR_M = h13.FLOOR_M
CEILING_M = h13.CEILING_M
CANDIDATE_M1 = h13.CANDIDATE_M1
CANDIDATE_M2 = h13.CANDIDATE_M2
fate_label = h13.fate_label
find_collisions = h13.find_collisions
simulate_transient_clamp_multi_with_delayed_observation = (
    h14.simulate_transient_clamp_multi_with_delayed_observation
)


def walk_clamped_trajectory_until_cycle(
    initial_state: dict, node_names: list, clamped_rules: dict, max_steps: int = 2000
) -> dict:
    """Walk synchronous_step under the FIXED clamped rule-set from `initial_state`, recording
    every distinct state visited, until a previously-seen state recurs (structural analogue of
    H-B7-3's run_until_attractor, but returns the FULL trajectory including the transient prefix,
    not only the eventual cycle -- every state in the trajectory is an achievable release-state
    for SOME k). Raises if no cycle found within max_steps (would indicate a bug -- a finite
    deterministic system MUST cycle)."""

    def key(d: dict) -> tuple:
        return tuple(d[n] for n in node_names)

    trajectory = [dict(initial_state)]
    seen = {key(initial_state): 0}
    current = dict(initial_state)
    for _ in range(max_steps):
        nxt = h1.synchronous_step(current, clamped_rules)
        k = key(nxt)
        if k in seen:
            return {
                "trajectory": trajectory,
                "cycle_start_index": seen[k],
                "cycle_period": len(trajectory) - seen[k],
                "orbit_length": len(trajectory),
            }
        trajectory.append(nxt)
        seen[k] = len(trajectory) - 1
        current = nxt
    raise RuntimeError(f"no cycle found within {max_steps} steps -- likely a bug")


def build_exhaustive_domain(node_names, wild_type_rules) -> dict:
    """For each branch: walk the clamped trajectory to its cycle, then for EVERY k=1..orbit_length
    (the full closed orbit -- covers every achievable release-state for any k, since k beyond
    orbit_length repeats a state already in [1, orbit_length]), compute release-state (j=0) and
    j=1 delayed observation + eventual fate."""
    branches = [
        ("branch_1", GROWTH_ARREST_STATE_1),
        ("branch_2", GROWTH_ARREST_STATE_2),
    ]
    orbit_info = {}
    domain_j0 = []
    domain_j1 = []
    for branch_name, growth_arrest_state in branches:
        start_state = dict(zip(PYBOOLNET_NODE_ORDER, (c == "1" for c in growth_arrest_state)))
        clamped_rules = dict(wild_type_rules)
        for node, value in CLAMPS.items():
            clamped_rules = h2.clamp_rule(clamped_rules, node, value)
        # note: the clamp is applied to the initial state itself before walking, matching
        # simulate_transient_clamp_multi_with_release_state's own "apply clamp to state, step 0"
        clamp_applied_start = dict(start_state)
        for node, value in CLAMPS.items():
            clamp_applied_start[node] = value

        orbit = walk_clamped_trajectory_until_cycle(clamp_applied_start, node_names, clamped_rules)
        orbit_info[branch_name] = {
            "orbit_length": orbit["orbit_length"],
            "cycle_start_index": orbit["cycle_start_index"],
            "cycle_period": orbit["cycle_period"],
        }
        # orbit["trajectory"][k] is the state after exactly k clamped steps (index 0 = state
        # right after the clamp is first applied, i.e. k=0 in this indexing corresponds to k=... )
        # trajectory[0] is the clamp-applied START state (0 wild-type clamp steps taken yet from
        # THIS walk's perspective it's step 0). Achievable release-states for k=1..orbit_length-1
        # (using 1-indexed k as in H-B7-13/14) are trajectory[1], trajectory[2], ... -- but since
        # simulate_transient_clamp_multi_with_delayed_observation re-derives from scratch each
        # time (not reusing this walk), we just call it directly for every k in the full orbit
        # range for full apples-to-apples consistency with H-B7-13/14's own functions.
        max_k = orbit["orbit_length"] - 1  # trajectory indices 0..orbit_length-1
        for k in range(1, max_k + 1):
            sim0 = simulate_transient_clamp_multi_with_delayed_observation(
                start_state, node_names, wild_type_rules, CLAMPS, k, 0
            )
            sim1 = simulate_transient_clamp_multi_with_delayed_observation(
                start_state, node_names, wild_type_rules, CLAMPS, k, 1
            )
            fate = fate_label(sim0["final_state"])
            domain_j0.append(
                {
                    "branch": branch_name,
                    "k": k,
                    "release_state": sim0["observed_state"],
                    "fate": fate,
                }
            )
            domain_j1.append(
                {
                    "branch": branch_name,
                    "k": k,
                    "release_state": sim1["observed_state"],
                    "fate": fate,
                }
            )

    return {"orbit_info": orbit_info, "domain_j0": domain_j0, "domain_j1": domain_j1}


def cmd_run() -> dict:
    text = DATA.read_text(encoding="utf-8")
    rules = h1.parse_bnet(text)
    node_names = [name for name, _ in rules]
    wild_type_rules = h1.compile_rules(rules)

    built = build_exhaustive_domain(node_names, wild_type_rules)
    domain_j0 = built["domain_j0"]
    domain_j1 = built["domain_j1"]

    results_j0 = {}
    results_j1 = {}
    for m_name, m_set in [
        ("floor_DNA_damage_only", FLOOR_M),
        ("ceiling_full_state", CEILING_M),
        ("candidate_M1_phenotypes_only", CANDIDATE_M1),
        ("candidate_M2_phenotypes_plus_clamp_targets", CANDIDATE_M2),
    ]:
        coll0 = find_collisions(domain_j0, m_set)
        coll1 = find_collisions(domain_j1, m_set)
        results_j0[m_name] = {"n_collisions": len(coll0), "sufficient": len(coll0) == 0}
        results_j1[m_name] = {
            "n_collisions": len(coll1),
            "sufficient": len(coll1) == 0,
            "collisions": coll1[:5],
        }

    # regression check: for k in the overlap with H-B7-13/14's own tested range (k=1..40),
    # results must match those experiments' own committed collision structure for M1/M2 at j=0.
    overlap_j0 = [e for e in domain_j0 if e["k"] <= 40]
    m1_overlap_collisions = find_collisions(overlap_j0, CANDIDATE_M1)
    m2_overlap_collisions = find_collisions(overlap_j0, CANDIDATE_M2)

    out = {
        "claim": "H-B7-15 exhaustive verification of j*=1 sufficiency over the full orbit",
        "orbit_info": built["orbit_info"],
        "domain_size_j0": len(domain_j0),
        "domain_size_j1": len(domain_j1),
        "orbit_fully_within_previously_tested_k_1_to_40": all(
            info["orbit_length"] - 1 <= 40 for info in built["orbit_info"].values()
        ),
        "results_at_release_j0": results_j0,
        "results_at_j1": results_j1,
        "regression_check_overlap_k_1_to_40": {
            "M1_n_collisions": len(m1_overlap_collisions),
            "M2_n_collisions": len(m2_overlap_collisions),
            "matches_h_b7_13_14": (
                len(m1_overlap_collisions) == 1 and len(m2_overlap_collisions) == 1
            ),
        },
        "theorem_level_verdict": {
            "M1_sufficient_over_full_orbit_at_j1": results_j1["candidate_M1_phenotypes_only"][
                "sufficient"
            ],
            "M2_sufficient_over_full_orbit_at_j1": results_j1[
                "candidate_M2_phenotypes_plus_clamp_targets"
            ]["sufficient"],
        },
    }

    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    print(json.dumps(out, indent=2, default=str))
    return out


if __name__ == "__main__":
    cmd_run()
