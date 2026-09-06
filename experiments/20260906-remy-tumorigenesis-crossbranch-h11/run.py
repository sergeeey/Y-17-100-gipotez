"""run.py — H-B7-11: cross-branch generalization test. Tests whether the permanent
do(p21CIP=0, RBL2=0) clamp, already established as sufficient on the FIRST branch (H-B7-8), also
suffices on the SECOND (and only other) phenotype-divergent branch of the Remy et al. 2015
network: (DNA_damage=0, EGFR_stimulus=1, FGFR3_stimulus=1, Growth_inhibitors=1).

Reuses H-B7-1's pipeline functions (parse_bnet, compile_rules, synchronous_step), H-B7-3's
run_until_attractor, and H-B7-5's apply_combined_clamp UNCHANGED via import.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
H_B7_1_DIR = HERE.parent / "20260906-kauffman-cellcycle-attractors-h1"
H_B7_3_DIR = HERE.parent / "20260906-kauffman-cellcycle-transient-h3"
H_B7_4_DIR = HERE.parent / "20260906-remy-tumorigenesis-transient-h4"
H_B7_5_DIR = HERE.parent / "20260906-remy-tumorigenesis-twohit-h5"
DATA = H_B7_4_DIR / "data" / "remy_tumorigenesis.bnet"
METRICS = HERE / "metrics"

_SPEC1 = importlib.util.spec_from_file_location("kauffman_h1_run", H_B7_1_DIR / "run.py")
h1 = importlib.util.module_from_spec(_SPEC1)
_SPEC1.loader.exec_module(h1)

_SPEC3 = importlib.util.spec_from_file_location("kauffman_h3_run", H_B7_3_DIR / "run.py")
h3 = importlib.util.module_from_spec(_SPEC3)
_SPEC3.loader.exec_module(h3)

_SPEC4 = importlib.util.spec_from_file_location("remy_h4_run", H_B7_4_DIR / "run.py")
h4 = importlib.util.module_from_spec(_SPEC4)
_SPEC4.loader.exec_module(h4)

_SPEC5 = importlib.util.spec_from_file_location("remy_h5_run", H_B7_5_DIR / "run.py")
h5 = importlib.util.module_from_spec(_SPEC5)
_SPEC5.loader.exec_module(h5)

# Same alphabetical-order convention as H-B7-4..10 (pyboolnet's compute_attractors state strings) --
# node ORDER is identical across branches (same 35 nodes), only the INPUT VALUES differ.
PYBOOLNET_NODE_ORDER = h4.PYBOOLNET_NODE_ORDER

# The SECOND phenotype-divergent branch (see data/branch_scoping.md for the Compute-First scan
# that found it -- the only other branch besides H-B7-4's own with genuine GA/PR divergence).
BRANCH_INPUTS_2 = {
    "DNA_damage": False,
    "EGFR_stimulus": True,
    "FGFR3_stimulus": True,
    "Growth_inhibitors": True,
}
GROWTH_ARREST_STATE_2 = "00000000000000000111011000011110001"
SECOND_GA_STATE_2 = "00000000000000010111011000010110011"
PROLIFERATION_STATE_2 = "00000100101001010111001000110010110"

apply_combined_clamp = h5.apply_combined_clamp


def cmd_run() -> dict:
    text = DATA.read_text(encoding="utf-8")
    rules = h1.parse_bnet(text)
    node_names = [name for name, _ in rules]
    wild_type_rules = h1.compile_rules(rules)

    start_state = dict(zip(PYBOOLNET_NODE_ORDER, (c == "1" for c in GROWTH_ARREST_STATE_2)))

    def state_str(d: dict) -> str:
        return "".join("1" if d[n] else "0" for n in PYBOOLNET_NODE_ORDER)

    clamps = {"p21CIP": False, "RBL2": False}
    combined_rules = apply_combined_clamp(wild_type_rules, clamps)

    final_cycle = h3.run_until_attractor(start_state, combined_rules, node_names)
    final_state = final_cycle[0]
    branch_preserved = all(final_state[n] == v for n, v in BRANCH_INPUTS_2.items())
    final_str = state_str(final_state)

    growth_arrest_phenotype = final_state.get("Growth_arrest")
    proliferation_phenotype = final_state.get("Proliferation")

    if proliferation_phenotype and not growth_arrest_phenotype:
        label = "PROLIFERATION (pattern GENERALIZES to second branch)"
    elif growth_arrest_phenotype:
        label = "GROWTH_ARREST (pattern does NOT generalize -- branch-specific)"
    else:
        label = "AMBIGUOUS (neither phenotype node reads 1)"

    out = {
        "branch": "second (EGFR_stimulus=1)",
        "clamps": clamps,
        "branch_inputs": BRANCH_INPUTS_2,
        "growth_arrest_state_2": GROWTH_ARREST_STATE_2,
        "proliferation_state_2": PROLIFERATION_STATE_2,
        "final_attractor_period": len(final_cycle),
        "final_attractor_type": "point" if len(final_cycle) == 1 else "complex",
        "final_state_pyboolnet_order": final_str,
        "growth_arrest_phenotype_node": growth_arrest_phenotype,
        "proliferation_phenotype_node": proliferation_phenotype,
        "final_attractor_identity": label,
        "branch_inputs_preserved": branch_preserved,
        "flipped_to_proliferation": label.startswith("PROLIFERATION"),
        "matches_proliferation_state_2": final_str == PROLIFERATION_STATE_2,
        "comparison_to_h_b7_8_first_branch": (
            "H-B7-8 (first branch, same clamp): CONFIRMED, reached Proliferation"
        ),
    }

    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    cmd_run()
