"""run.py -- H-B7-18: does the flip_TF_drop_CyclinE1 perturbation (RBL2 := !CyclinD1) destabilize
PROLIFERATION_STATE's own fixed-point status directly -- explaining H-B7-17's CRITERION_INVALID
finding (this perturbation abolishes the transient escape entirely, not merely shifting or
hiding its threshold) at the mechanism level, not just observing it.

Hand-derivation (claim.md, Compute-First Check): at PROLIFERATION_STATE, CyclinD1=False,
CyclinE1=True. Original RBL2 rule (!CyclinE1 & !CyclinD1) gives False, consistent with the
state's own RBL2=False. Perturbed rule (!CyclinD1) gives True -- inconsistent, not a fixed point.

Reuses H-B7-13's h1 (synchronous_step, parse_bnet, compile_rules), h3-equivalent
run_until_attractor (via H-B7-17's own h13 module reference chain), PYBOOLNET_NODE_ORDER,
GROWTH_ARREST_STATE_1/2, and H-B7-17's exact RBL2_PERTURBATIONS UNCHANGED.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
H_B7_3_DIR = HERE.parent / "20260906-kauffman-cellcycle-transient-h3"
H_B7_4_DIR = HERE.parent / "20260906-remy-tumorigenesis-transient-h4"
H_B7_11_DIR = HERE.parent / "20260906-remy-tumorigenesis-crossbranch-h11"
H_B7_13_DIR = HERE.parent / "20260910-remy-tumorigenesis-observability-h13"
H_B7_17_DIR = HERE.parent / "20260910-remy-tumorigenesis-observability-ruleperturbation-h17"
DATA = H_B7_4_DIR / "data" / "remy_tumorigenesis.bnet"
METRICS = HERE / "metrics"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


h13 = _load_module("h_b7_18_h13", H_B7_13_DIR / "run.py")
h17 = _load_module("h_b7_18_h17", H_B7_17_DIR / "run.py")
h3 = _load_module("h_b7_18_h3", H_B7_3_DIR / "run.py")
h1 = h13.h1

PYBOOLNET_NODE_ORDER = h13.PYBOOLNET_NODE_ORDER
GROWTH_ARREST_STATE_1 = h13.GROWTH_ARREST_STATE_1
GROWTH_ARREST_STATE_2 = h13.GROWTH_ARREST_STATE_2
BRANCH_INPUTS_1 = h13.BRANCH_INPUTS_1
fate_label = h13.fate_label
RBL2_PERTURBATIONS = h17.RBL2_PERTURBATIONS

PROLIFERATION_STATE = "00000100101001010011001000110010110"  # H-B7-4's own constant, branch 1
PROLIFERATION_STATE_2 = "00000100101001010111001000110010110"  # H-B7-11's own constant, branch 2


def state_str_to_dict(s: str) -> dict:
    return dict(zip(PYBOOLNET_NODE_ORDER, (c == "1" for c in s)))


def dict_to_state_str(d: dict) -> str:
    return "".join("1" if d[n] else "0" for n in PYBOOLNET_NODE_ORDER)


def cmd_run() -> dict:
    text = DATA.read_text(encoding="utf-8")
    rules = h1.parse_bnet(text)
    node_names = [name for name, _ in rules]
    original_wild_type_rules = h1.compile_rules(rules)

    perturbed_rules = dict(original_wild_type_rules)
    perturbed_rules["RBL2"] = RBL2_PERTURBATIONS["flip_TF_drop_CyclinE1"]

    results = {}
    for label, state_str in [
        ("branch_1", PROLIFERATION_STATE),
        ("branch_2", PROLIFERATION_STATE_2),
    ]:
        state = state_str_to_dict(state_str)

        # 1. Verify hand-derivation: what does RBL2 evaluate to at this exact state, under
        #    original vs perturbed rules?
        rbl2_original = h1.evaluate_expression(original_wild_type_rules["RBL2"], state)
        rbl2_perturbed = h1.evaluate_expression(perturbed_rules["RBL2"], state)
        cyclin_d1 = state["CyclinD1"]
        cyclin_e1 = state["CyclinE1"]

        # 2. One synchronous step under perturbed rules -- still the same state (fixed point)?
        next_state = h1.synchronous_step(state, perturbed_rules)
        is_still_fixed_point = next_state == state

        # 3. If destabilized, trace the FULL trajectory to its eventual attractor.
        trajectory_result = None
        if not is_still_fixed_point:
            cycle = h3.run_until_attractor(state, perturbed_rules, node_names)
            trajectory_result = {
                "final_state": dict_to_state_str(cycle[0]),
                "period": len(cycle),
                "type": "point" if len(cycle) == 1 else "complex",
                "final_fate": fate_label(cycle[0]),
                "matches_growth_arrest_state_1": (
                    dict_to_state_str(cycle[0]) == GROWTH_ARREST_STATE_1
                ),
                "matches_growth_arrest_state_2": (
                    dict_to_state_str(cycle[0]) == GROWTH_ARREST_STATE_2
                ),
            }

        results[label] = {
            "starting_state": state_str,
            "CyclinD1_at_state": cyclin_d1,
            "CyclinE1_at_state": cyclin_e1,
            "RBL2_original_rule_eval": rbl2_original,
            "RBL2_perturbed_rule_eval": rbl2_perturbed,
            "RBL2_consistent_with_state (state's own RBL2 must be False for Proliferation)": (
                rbl2_perturbed == state["RBL2"]
            ),
            "state_RBL2_value": state["RBL2"],
            "is_still_fixed_point_under_perturbed_rules": is_still_fixed_point,
            "destabilization_trajectory": trajectory_result,
        }

    both_destabilized = all(
        not r["is_still_fixed_point_under_perturbed_rules"] for r in results.values()
    )
    both_relapse_to_growth_arrest = all(
        r["destabilization_trajectory"] is not None
        and r["destabilization_trajectory"]["final_fate"] == "GROWTH_ARREST"
        for r in results.values()
    )

    if both_destabilized and both_relapse_to_growth_arrest:
        verdict = "CONFIRMED-SELF-DESTABILIZING"
    elif both_destabilized:
        verdict = "CONFIRMED-DESTABILIZED-DIFFERENT-FATE"
    else:
        verdict = "REJECTED"

    out = {
        "claim": "H-B7-18: does flip_TF_drop_CyclinE1 destabilize the Proliferation fixed point",
        "results_by_branch": results,
        "both_states_destabilized": both_destabilized,
        "both_relapse_to_growth_arrest": both_relapse_to_growth_arrest,
        "verdict": verdict,
    }

    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    print(json.dumps(out, indent=2, default=str))
    return out


if __name__ == "__main__":
    cmd_run()
