"""run.py — H-B7-12: transient do(p21CIP=0, RBL2=0) duration sweep on the SECOND branch (H-B7-11:
DNA_damage=0, EGFR_stimulus=1, FGFR3_stimulus=1, Growth_inhibitors=1) -- tests whether H-B7-9's
transient-escape confirmation and H-B7-10's exact threshold k*=5 generalize beyond the first
branch.

Reuses H-B7-1's pipeline functions, H-B7-3's run_until_attractor, H-B7-9's
simulate_transient_clamp_multi, and H-B7-11's second-branch state constants UNCHANGED.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
H_B7_1_DIR = HERE.parent / "20260906-kauffman-cellcycle-attractors-h1"
H_B7_3_DIR = HERE.parent / "20260906-kauffman-cellcycle-transient-h3"
H_B7_4_DIR = HERE.parent / "20260906-remy-tumorigenesis-transient-h4"
H_B7_9_DIR = HERE.parent / "20260906-remy-tumorigenesis-transient-necessity-h9"
H_B7_11_DIR = HERE.parent / "20260906-remy-tumorigenesis-crossbranch-h11"
DATA = H_B7_4_DIR / "data" / "remy_tumorigenesis.bnet"
METRICS = HERE / "metrics"

_SPEC1 = importlib.util.spec_from_file_location("kauffman_h1_run", H_B7_1_DIR / "run.py")
h1 = importlib.util.module_from_spec(_SPEC1)
_SPEC1.loader.exec_module(h1)

_SPEC3 = importlib.util.spec_from_file_location("kauffman_h3_run", H_B7_3_DIR / "run.py")
h3 = importlib.util.module_from_spec(_SPEC3)
_SPEC3.loader.exec_module(h3)

_SPEC9 = importlib.util.spec_from_file_location("remy_h9_run", H_B7_9_DIR / "run.py")
h9 = importlib.util.module_from_spec(_SPEC9)
_SPEC9.loader.exec_module(h9)

_SPEC11 = importlib.util.spec_from_file_location("remy_h11_run", H_B7_11_DIR / "run.py")
h11 = importlib.util.module_from_spec(_SPEC11)
_SPEC11.loader.exec_module(h11)

PYBOOLNET_NODE_ORDER = h11.PYBOOLNET_NODE_ORDER
BRANCH_INPUTS_2 = h11.BRANCH_INPUTS_2
GROWTH_ARREST_STATE_2 = h11.GROWTH_ARREST_STATE_2
SECOND_GA_STATE_2 = h11.SECOND_GA_STATE_2
PROLIFERATION_STATE_2 = h11.PROLIFERATION_STATE_2

simulate_transient_clamp_multi = h9.simulate_transient_clamp_multi

# Same duration set H-B7-9/H-B7-10 tested on the first branch, for direct comparability.
TESTED_DURATIONS = (1, 3, 4, 5, 6, 9, 10, 30)


def cmd_run() -> dict:
    text = DATA.read_text(encoding="utf-8")
    rules = h1.parse_bnet(text)
    node_names = [name for name, _ in rules]
    wild_type_rules = h1.compile_rules(rules)

    start_state = dict(zip(PYBOOLNET_NODE_ORDER, (c == "1" for c in GROWTH_ARREST_STATE_2)))
    clamps = {"p21CIP": False, "RBL2": False}

    def state_str(d: dict) -> str:
        return "".join("1" if d[n] else "0" for n in PYBOOLNET_NODE_ORDER)

    results_by_k = []
    for k in TESTED_DURATIONS:
        sim = simulate_transient_clamp_multi(start_state, node_names, wild_type_rules, clamps, k)
        final_state = sim["final_state"]
        final_str = state_str(final_state)
        branch_preserved = all(final_state[n] == v for n, v in BRANCH_INPUTS_2.items())
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
                "matches_proliferation_state_2": final_str == PROLIFERATION_STATE_2,
                "matches_original_growth_arrest_state_2": final_str == GROWTH_ARREST_STATE_2,
                "matches_second_growth_arrest_state_2": final_str == SECOND_GA_STATE_2,
            }
        )

    escaped = [r["flipped_to_proliferation"] for r in results_by_k]
    k_star = None
    for k, esc in zip(TESTED_DURATIONS, escaped):
        if esc:
            k_star = k
            break
    if k_star is not None:
        idx_star = TESTED_DURATIONS.index(k_star)
        is_monotone = all(not escaped[i] for i in range(idx_star)) and all(
            escaped[i] for i in range(idx_star, len(escaped))
        )
    else:
        is_monotone = not any(escaped)

    out = {
        "branch": "second (EGFR_stimulus=1)",
        "clamps": clamps,
        "branch_inputs": BRANCH_INPUTS_2,
        "growth_arrest_state_2": GROWTH_ARREST_STATE_2,
        "proliferation_state_2": PROLIFERATION_STATE_2,
        "tested_durations": list(TESTED_DURATIONS),
        "results_by_k": results_by_k,
        "k_star": k_star,
        "is_clean_monotone_threshold": is_monotone,
        "h_b7_10_first_branch_threshold": 5,
        "threshold_matches_first_branch": k_star == 5,
    }

    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    cmd_run()
