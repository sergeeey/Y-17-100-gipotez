"""run.py — H-B7-10: fine duration sweep k=4..9 of the transient do(p21CIP=0, RBL2=0) clamp on
the Remy et al. 2015 network's bistable branch -- pins down the exact relapse/escape threshold
H-B7-9 left open (bracketed between k=3 relapse and k=10 escape).

Reuses H-B7-9's `simulate_transient_clamp_multi` and all its imported helpers UNCHANGED --
Minimal Relaxation Rule: only TESTED_DURATIONS changes, no new pipeline logic.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
H_B7_1_DIR = HERE.parent / "20260906-kauffman-cellcycle-attractors-h1"
H_B7_4_DIR = HERE.parent / "20260906-remy-tumorigenesis-transient-h4"
H_B7_9_DIR = HERE.parent / "20260906-remy-tumorigenesis-transient-necessity-h9"
DATA = H_B7_4_DIR / "data" / "remy_tumorigenesis.bnet"
METRICS = HERE / "metrics"

_SPEC1 = importlib.util.spec_from_file_location("kauffman_h1_run", H_B7_1_DIR / "run.py")
h1 = importlib.util.module_from_spec(_SPEC1)
_SPEC1.loader.exec_module(h1)

_SPEC4 = importlib.util.spec_from_file_location("remy_h4_run", H_B7_4_DIR / "run.py")
h4 = importlib.util.module_from_spec(_SPEC4)
_SPEC4.loader.exec_module(h4)

_SPEC9 = importlib.util.spec_from_file_location("remy_h9_run", H_B7_9_DIR / "run.py")
h9 = importlib.util.module_from_spec(_SPEC9)
_SPEC9.loader.exec_module(h9)

PYBOOLNET_NODE_ORDER = h4.PYBOOLNET_NODE_ORDER
BRANCH_INPUTS = h4.BRANCH_INPUTS
GROWTH_ARREST_STATE = h4.GROWTH_ARREST_STATE
PROLIFERATION_STATE = h4.PROLIFERATION_STATE
SECOND_GROWTH_ARREST_STATE = "00000000000000010011011000010110011"  # found in H-B7-9

simulate_transient_clamp_multi = h9.simulate_transient_clamp_multi

TESTED_DURATIONS = (4, 5, 6, 7, 8, 9)


def cmd_run() -> dict:
    text = DATA.read_text(encoding="utf-8")
    rules = h1.parse_bnet(text)
    node_names = [name for name, _ in rules]
    wild_type_rules = h1.compile_rules(rules)

    start_state = dict(zip(PYBOOLNET_NODE_ORDER, (c == "1" for c in GROWTH_ARREST_STATE)))
    clamps = {"p21CIP": False, "RBL2": False}

    def state_str(d: dict) -> str:
        return "".join("1" if d[n] else "0" for n in PYBOOLNET_NODE_ORDER)

    results_by_k = []
    for k in TESTED_DURATIONS:
        sim = simulate_transient_clamp_multi(start_state, node_names, wild_type_rules, clamps, k)
        final_state = sim["final_state"]
        final_str = state_str(final_state)
        branch_preserved = all(final_state[n] == v for n, v in BRANCH_INPUTS.items())
        growth_arrest_phenotype = final_state.get("Growth_arrest")
        proliferation_phenotype = final_state.get("Proliferation")

        if proliferation_phenotype and not growth_arrest_phenotype:
            label = "PROLIFERATION"
        elif growth_arrest_phenotype:
            label = "GROWTH_ARREST"
        else:
            label = "AMBIGUOUS"

        results_by_k.append(
            {
                "k_steps": k,
                "final_attractor_period": sim["period"],
                "final_attractor_type": sim["type"],
                "final_state_pyboolnet_order": final_str,
                "growth_arrest_phenotype_node": growth_arrest_phenotype,
                "proliferation_phenotype_node": proliferation_phenotype,
                "final_attractor_identity": label,
                "branch_inputs_preserved": branch_preserved,
                "flipped_to_proliferation": label == "PROLIFERATION",
                "matches_proliferation_state": final_str == PROLIFERATION_STATE,
                "matches_original_growth_arrest_state": final_str == GROWTH_ARREST_STATE,
                "matches_second_growth_arrest_state": final_str == SECOND_GROWTH_ARREST_STATE,
            }
        )

    escaped = [r["flipped_to_proliferation"] for r in results_by_k]
    # Find k* : the first tested k (in ascending TESTED_DURATIONS order) that escapes.
    k_star = None
    for k, esc in zip(TESTED_DURATIONS, escaped):
        if esc:
            k_star = k
            break
    is_monotone = True
    if k_star is not None:
        idx_star = TESTED_DURATIONS.index(k_star)
        is_monotone = all(not escaped[i] for i in range(idx_star)) and all(
            escaped[i] for i in range(idx_star, len(escaped))
        )
    else:
        is_monotone = not any(escaped)  # all relapsed -- trivially monotone (no threshold in range)

    out = {
        "clamps": clamps,
        "branch_inputs": BRANCH_INPUTS,
        "growth_arrest_state": GROWTH_ARREST_STATE,
        "second_growth_arrest_state": SECOND_GROWTH_ARREST_STATE,
        "proliferation_state": PROLIFERATION_STATE,
        "tested_durations": list(TESTED_DURATIONS),
        "results_by_k": results_by_k,
        "k_star": k_star,
        "is_clean_monotone_threshold": is_monotone,
        "h_b7_9_boundary_context": (
            "k=3 relapsed (second Growth_arrest), k=10 escaped (Proliferation)"
        ),
    }

    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    cmd_run()
