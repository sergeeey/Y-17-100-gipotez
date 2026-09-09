"""run.py -- H-B7-20: exhaustive single-bit truth-table perturbation robustness of CyclinE1's own
rule -- the third named component of the CyclinE1/RBL2 feedback loop (H-B7-13's own diagnosis).
Unlike RBL2 (H-B7-17) and p21CIP (H-B7-19), CyclinE1 is NOT a clamped node -- it evolves under
its own rule during the clamp phase too, so H-B7-15's fixed orbit CANNOT be reused unchanged: the
clamp-phase orbit must be re-walked for every perturbation.

For each FRAGILE perturbation, additionally runs H-B7-18's own fixed-point-destabilization check
(is PROLIFERATION_STATE/_2 still a fixed point under the perturbed rules?) to classify it
SELF-DESTABILIZING vs OBSERVABILITY-ONLY -- the distinction H-B7-18 showed is mechanistically
load-bearing, checked here systematically rather than for one hand-picked case.

Reuses H-B7-19's TableRule/build_table_from_expression/synchronous_step_with_table_override
UNCHANGED via distinct-name import.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
H_B7_2_DIR = HERE.parent / "20260906-kauffman-cellcycle-perturbation-h2"
H_B7_4_DIR = HERE.parent / "20260906-remy-tumorigenesis-transient-h4"
H_B7_13_DIR = HERE.parent / "20260910-remy-tumorigenesis-observability-h13"
H_B7_19_DIR = HERE.parent / "20260910-remy-tumorigenesis-p21cip-ruleperturbation-h19"
DATA = H_B7_4_DIR / "data" / "remy_tumorigenesis.bnet"
METRICS = HERE / "metrics"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


h13 = _load_module("h_b7_20_h13", H_B7_13_DIR / "run.py")
h19 = _load_module("h_b7_20_h19", H_B7_19_DIR / "run.py")
h2 = _load_module("h_b7_20_h2", H_B7_2_DIR / "run.py")
h1 = h13.h1

PYBOOLNET_NODE_ORDER = h13.PYBOOLNET_NODE_ORDER
GROWTH_ARREST_STATE_1 = h13.GROWTH_ARREST_STATE_1
GROWTH_ARREST_STATE_2 = h13.GROWTH_ARREST_STATE_2
CLAMPS = h13.CLAMPS
FLOOR_M = h13.FLOOR_M
CEILING_M = h13.CEILING_M
CANDIDATE_M1 = h13.CANDIDATE_M1
CANDIDATE_M2 = h13.CANDIDATE_M2
fate_label = h13.fate_label
find_collisions = h13.find_collisions
TableRule = h19.TableRule
build_table_from_expression = h19.build_table_from_expression
synchronous_step_with_table_override = h19.synchronous_step_with_table_override

CYCLIN_E1_INPUTS = ("p21CIP", "RBL2", "E2F3_medium", "CDC25A", "E2F1_medium")
PROLIFERATION_STATE = "00000100101001010011001000110010110"
PROLIFERATION_STATE_2 = "00000100101001010111001000110010110"
MAX_K = 40  # generous cap on how far into the clamped orbit we walk, per perturbation


def state_str_to_dict(s: str) -> dict:
    return dict(zip(PYBOOLNET_NODE_ORDER, (c == "1" for c in s)))


def dict_to_state_str(d: dict) -> str:
    return "".join("1" if d[n] else "0" for n in PYBOOLNET_NODE_ORDER)


def walk_clamped_orbit_with_override(
    start_state: dict,
    node_names: list,
    clamped_rules: dict,
    override_rule: TableRule,
    max_steps: int,
) -> dict:
    """Re-implementation of H-B7-15's walk_clamped_trajectory_until_cycle, generalized to allow
    CyclinE1's rule to be table-overridden DURING the clamp phase too (unlike p21CIP/RBL2, whose
    clamp_rule constant already made an override moot during the clamp)."""

    def key(d: dict) -> tuple:
        return tuple(d[n] for n in node_names)

    trajectory = [dict(start_state)]
    seen = {key(start_state): 0}
    current = dict(start_state)
    for _ in range(max_steps):
        nxt = synchronous_step_with_table_override(
            current, clamped_rules, "CyclinE1", override_rule
        )
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


def run_until_attractor_with_override(
    state: dict, wild_type_rules: dict, node_names: list, override_rule: TableRule, max_steps=200
) -> list[dict]:
    def key(d: dict) -> tuple:
        return tuple(d[n] for n in node_names)

    trajectory = [dict(state)]
    seen = {key(state): 0}
    current = dict(state)
    for _ in range(max_steps):
        nxt = synchronous_step_with_table_override(
            current, wild_type_rules, "CyclinE1", override_rule
        )
        k = key(nxt)
        if k in seen:
            return trajectory[seen[k] :]
        trajectory.append(nxt)
        seen[k] = len(trajectory) - 1
        current = nxt
    raise RuntimeError(f"no attractor found within {max_steps} steps -- likely a bug")


def build_domain_for_perturbation(
    node_names, wild_type_rules, override_rule
) -> tuple[list, list, dict]:
    branches = [
        ("branch_1", GROWTH_ARREST_STATE_1),
        ("branch_2", GROWTH_ARREST_STATE_2),
    ]
    domain_j0, domain_j1 = [], []
    orbit_info = {}
    for branch_name, growth_arrest_state in branches:
        start_state = dict(zip(PYBOOLNET_NODE_ORDER, (c == "1" for c in growth_arrest_state)))
        clamped_rules = dict(wild_type_rules)
        for node, value in CLAMPS.items():
            clamped_rules = h2.clamp_rule(clamped_rules, node, value)
        clamp_applied_start = dict(start_state)
        for node, value in CLAMPS.items():
            clamp_applied_start[node] = value

        orbit = walk_clamped_orbit_with_override(
            clamp_applied_start, node_names, clamped_rules, override_rule, MAX_K * 3
        )
        max_k = min(orbit["orbit_length"] - 1, MAX_K)
        orbit_info[branch_name] = {
            "orbit_length": orbit["orbit_length"],
            "cycle_period": orbit["cycle_period"],
            "max_k_tested": max_k,
        }

        for k in range(1, max_k + 1):
            current = dict(start_state)
            for node, value in CLAMPS.items():
                current[node] = value
            for _ in range(k):
                current = synchronous_step_with_table_override(
                    current, clamped_rules, "CyclinE1", override_rule
                )
            release_state_j0 = dict(current)
            fate_cycle = run_until_attractor_with_override(
                current, wild_type_rules, node_names, override_rule
            )
            fate = fate_label(fate_cycle[0])

            j1_state = synchronous_step_with_table_override(
                current, wild_type_rules, "CyclinE1", override_rule
            )
            domain_j0.append(
                {"branch": branch_name, "k": k, "release_state": release_state_j0, "fate": fate}
            )
            domain_j1.append(
                {"branch": branch_name, "k": k, "release_state": j1_state, "fate": fate}
            )
    return domain_j0, domain_j1, orbit_info


def check_fixed_point_destabilization(wild_type_rules, node_names, override_rule) -> dict:
    """H-B7-18's own methodology, generalized: is PROLIFERATION_STATE/_2 still a fixed point
    under the perturbed rules? If not, does the destabilized trajectory relapse to a
    GROWTH_ARREST-phenotype attractor (as H-B7-18 found for RBL2's fragile row)?"""
    results = {}
    for label, state_str in [
        ("branch_1", PROLIFERATION_STATE),
        ("branch_2", PROLIFERATION_STATE_2),
    ]:
        state = state_str_to_dict(state_str)
        next_state = synchronous_step_with_table_override(
            state, wild_type_rules, "CyclinE1", override_rule
        )
        is_fixed_point = next_state == state
        trajectory_fate = None
        if not is_fixed_point:
            cycle = run_until_attractor_with_override(
                state, wild_type_rules, node_names, override_rule
            )
            trajectory_fate = fate_label(cycle[0])
        results[label] = {
            "is_fixed_point_under_perturbed_rules": is_fixed_point,
            "trajectory_fate_if_destabilized": trajectory_fate,
        }
    both_destabilized = all(not r["is_fixed_point_under_perturbed_rules"] for r in results.values())
    return {"per_branch": results, "self_destabilizing": both_destabilized}


def cmd_run() -> dict:
    text = DATA.read_text(encoding="utf-8")
    rules = h1.parse_bnet(text)
    node_names = [name for name, _ in rules]
    wild_type_rules = h1.compile_rules(rules)

    original_table = build_table_from_expression(wild_type_rules["CyclinE1"], CYCLIN_E1_INPUTS)

    conditions = {"baseline_unperturbed": original_table}
    for row in sorted(original_table.table.keys()):
        row_label = "".join("T" if v else "F" for v in row)
        conditions[f"flip_{row_label}"] = original_table.flipped(row)

    results = {}
    orbit_infos = {}
    for cond_name, table_rule in conditions.items():
        domain_j0, domain_j1, orbit_info = build_domain_for_perturbation(
            node_names, wild_type_rules, table_rule
        )
        orbit_infos[cond_name] = orbit_info

        per_marker = {}
        for m_name, m_set in [
            ("floor_DNA_damage_only", FLOOR_M),
            ("ceiling_full_state", CEILING_M),
            ("candidate_M1_phenotypes_only", CANDIDATE_M1),
            ("candidate_M2_phenotypes_plus_clamp_targets", CANDIDATE_M2),
        ]:
            coll0 = find_collisions(domain_j0, m_set)
            coll1 = find_collisions(domain_j1, m_set)
            per_marker[m_name] = {
                "n_collisions_j0": len(coll0),
                "n_collisions_j1": len(coll1),
                "sufficient_at_j1": len(coll1) == 0,
            }
        results[cond_name] = per_marker

    classification = {}
    destabilization_checks = {}
    for name, r in results.items():
        if name == "baseline_unperturbed":
            continue
        transition_exists = r["floor_DNA_damage_only"]["n_collisions_j0"] > 0
        m1_sufficient_j1 = r["candidate_M1_phenotypes_only"]["sufficient_at_j1"]
        if not transition_exists:
            classification[name] = "CRITERION_INVALID_no_transition"
            # Also destabilization-checked (not only FRAGILE rows): H-B7-18's own investigation
            # was actually of a CRITERION_INVALID case for RBL2 (flip_TF_drop_CyclinE1), not a
            # FRAGILE one -- checking CRITERION_INVALID cases here too keeps the three-way
            # RBL2/p21CIP/CyclinE1 comparison honest, not skipping the exact category H-B7-18
            # already showed can be self-destabilizing.
            destab = check_fixed_point_destabilization(
                wild_type_rules, node_names, conditions[name]
            )
            destabilization_checks[name] = destab
        elif m1_sufficient_j1:
            classification[name] = "ROBUST"
        else:
            classification[name] = "FRAGILE"
            destab = check_fixed_point_destabilization(
                wild_type_rules, node_names, conditions[name]
            )
            destabilization_checks[name] = destab

    robust = [n for n, c in classification.items() if c == "ROBUST"]
    fragile = [n for n, c in classification.items() if c == "FRAGILE"]
    invalid = [n for n, c in classification.items() if c == "CRITERION_INVALID_no_transition"]

    # Covers BOTH FRAGILE and CRITERION_INVALID rows -- see the note above the classification
    # loop for why CRITERION_INVALID must be checked too, not only FRAGILE.
    checked_rows = list(destabilization_checks.keys())
    self_destab = [n for n in checked_rows if destabilization_checks[n]["self_destabilizing"]]
    observability_only = [
        n for n in checked_rows if not destabilization_checks[n]["self_destabilizing"]
    ]

    n_meaningfully_tested = len(robust) + len(fragile)
    if n_meaningfully_tested == 0:
        verdict = "ALL_CRITERION_INVALID"
    elif len(fragile) == 0:
        verdict = "ROBUST"
    elif len(robust) == 0:
        verdict = "FRAGILE"
    else:
        verdict = "PARTIALLY-ROBUST"

    out = {
        "claim": "H-B7-20 exhaustive CyclinE1 rule-perturbation robustness of j*=1 sufficiency",
        "n_perturbations_tested": len(conditions) - 1,
        "orbit_infos": orbit_infos,
        "classification": classification,
        "robust_perturbations": robust,
        "fragile_perturbations": fragile,
        "criterion_invalid_perturbations": invalid,
        "n_robust": len(robust),
        "n_fragile": len(fragile),
        "n_criterion_invalid": len(invalid),
        "self_destabilizing_perturbations": self_destab,
        "observability_only_perturbations": observability_only,
        "destabilization_checks": destabilization_checks,
        "verdict": verdict,
        "results_by_perturbation": results,
    }

    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    print(
        json.dumps(
            {k: v for k, v in out.items() if k != "results_by_perturbation"}, indent=2, default=str
        )
    )
    return out


if __name__ == "__main__":
    cmd_run()
