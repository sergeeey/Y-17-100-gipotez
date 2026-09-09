"""run.py -- H-B7-17: does H-B7-15's exhaustive j*=1 sufficiency survive single-bit truth-table
perturbations of RBL2's own post-release rule -- the update-RULE half of robustness (the
update-SCHEDULE half was tested in H-B7-16, asynchronous update).

Compute-First Check (see claim.md): RBL2 is one of the two CLAMPED nodes -- h2.clamp_rule
replaces its compiled rule with a constant during the clamp, regardless of the underlying rule,
so H-B7-15's own 7-state-per-branch clamp-phase orbit is provably unaffected by any RBL2 rule
perturbation. Only the POST-RELEASE dynamics differ. This experiment reuses H-B7-15's exact
k=1..6 domain and H-B7-14's simulate_transient_clamp_multi_with_delayed_observation UNCHANGED,
swapping only the RBL2 entry in wild_type_rules per perturbation.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import boolean

HERE = Path(__file__).resolve().parent
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


h13 = _load_module("h_b7_17_h13", H_B7_13_DIR / "run.py")
h14 = _load_module("h_b7_17_h14", H_B7_14_DIR / "run.py")
h1 = h13.h1

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

ALGEBRA = boolean.BooleanAlgebra()

# H-B7-15's own established exhaustive orbit range (both branches): k=1..6 (orbit_length=7,
# indices 0..6, achievable k=1..6). Reused verbatim, not re-derived.
TESTED_K = list(range(1, 7))

# Hand-derived (claim.md): 4 single-bit truth-table flips of RBL2's original rule
# "!CyclinE1 & !CyclinD1" (true only at CyclinE1=False, CyclinD1=False).
RBL2_PERTURBATIONS = {
    "baseline_unperturbed": None,  # sentinel: use the original wild_type rule, no substitution
    "flip_FF_constant_false": ALGEBRA.FALSE,
    "flip_FT_drop_CyclinD1": ALGEBRA.parse("!CyclinE1"),
    "flip_TF_drop_CyclinE1": ALGEBRA.parse("!CyclinD1"),
    "flip_TT_xnor": ALGEBRA.parse("(CyclinE1&CyclinD1)|(!CyclinE1&!CyclinD1)"),
}


def build_domain(node_names, wild_type_rules) -> list[dict]:
    branches = [
        ("branch_1", GROWTH_ARREST_STATE_1),
        ("branch_2", GROWTH_ARREST_STATE_2),
    ]
    domain_j0 = []
    domain_j1 = []
    for branch_name, growth_arrest_state in branches:
        start_state = dict(zip(PYBOOLNET_NODE_ORDER, (c == "1" for c in growth_arrest_state)))
        for k in TESTED_K:
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
    return domain_j0, domain_j1


def cmd_run() -> dict:
    text = DATA.read_text(encoding="utf-8")
    rules = h1.parse_bnet(text)
    node_names = [name for name, _ in rules]
    original_wild_type_rules = h1.compile_rules(rules)

    results = {}
    orbit_lengths_seen = set()
    for pert_name, pert_expr in RBL2_PERTURBATIONS.items():
        wild_type_rules = dict(original_wild_type_rules)
        if pert_expr is not None:
            wild_type_rules["RBL2"] = pert_expr

        domain_j0, domain_j1 = build_domain(node_names, wild_type_rules)
        orbit_lengths_seen.add(
            len(domain_j0)
        )  # substrate sanity: must be 12 (2 branches x 6) always

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
        results[pert_name] = per_marker

    # Floor-Ceiling discipline (FL Step 4a), applied per perturbation: floor's OWN collision
    # count (grouping only by the branch-constant DNA_damage marker) is 0 precisely when NO
    # k-dependent fate transition exists at all under that perturbation -- i.e. the underlying
    # phenomenon (transient escape) has been abolished, not merely made observable/unobservable.
    # A perturbation in that state is NOT evidence about M1's robustness either way: there is
    # nothing for M1 to succeed or fail at distinguishing. Classify separately, do not fold into
    # "robust" (a perturbation can trivially look "sufficient" by having nothing to predict).
    per_perturbation_classification = {}
    for name, r in results.items():
        if name == "baseline_unperturbed":
            continue
        transition_exists = r["floor_DNA_damage_only"]["n_collisions_j0"] > 0
        m1_sufficient_j1 = r["candidate_M1_phenotypes_only"]["sufficient_at_j1"]
        if not transition_exists:
            classification = "CRITERION_INVALID_no_transition"
        elif m1_sufficient_j1:
            classification = "ROBUST"
        else:
            classification = "FRAGILE"
        per_perturbation_classification[name] = classification

    genuinely_robust = [n for n, c in per_perturbation_classification.items() if c == "ROBUST"]
    genuinely_fragile = [n for n, c in per_perturbation_classification.items() if c == "FRAGILE"]
    criterion_invalid = [
        n
        for n, c in per_perturbation_classification.items()
        if c == "CRITERION_INVALID_no_transition"
    ]

    n_meaningfully_tested = len(genuinely_robust) + len(genuinely_fragile)
    if n_meaningfully_tested == 0:
        verdict = "ALL_CRITERION_INVALID"
    elif len(genuinely_fragile) == 0:
        verdict = "ROBUST"
    elif len(genuinely_robust) == 0:
        verdict = "FRAGILE"
    else:
        verdict = "PARTIALLY-ROBUST"

    out = {
        "claim": "H-B7-17 rule-perturbation robustness of j*=1 sufficiency (RBL2 single-bit flips)",
        "tested_k": TESTED_K,
        "perturbations_tested": list(RBL2_PERTURBATIONS.keys()),
        "orbit_lengths_seen": sorted(orbit_lengths_seen),
        "substrate_check_orbit_unchanged_across_all_conditions": len(orbit_lengths_seen) == 1,
        "results_by_perturbation": results,
        "per_perturbation_classification": per_perturbation_classification,
        "genuinely_robust_perturbations": genuinely_robust,
        "genuinely_fragile_perturbations": genuinely_fragile,
        "criterion_invalid_perturbations": criterion_invalid,
        "verdict": verdict,
    }

    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    print(json.dumps(out, indent=2, default=str))
    return out


if __name__ == "__main__":
    cmd_run()
