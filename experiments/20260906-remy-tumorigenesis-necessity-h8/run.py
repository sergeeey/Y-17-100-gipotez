"""run.py — H-B7-8: necessity test do(p21CIP=0, RBL2=0) on the Remy et al. 2015 bladder
tumorigenesis network's bistable branch, WITHOUT clamping RAS/TP53 -- directly operationalizes the
FL Step 8a skeptic WEAKENING finding from H-B7-7 (RAS=1, TP53=0 are already true at
GROWTH_ARREST_STATE, so permanently clamping them may have been redundant).

Reuses H-B7-1's pipeline functions (parse_bnet, compile_rules, synchronous_step), H-B7-3's
run_until_attractor, and H-B7-5's apply_combined_clamp UNCHANGED via import -- all already
generic, no modification needed. Unlike H-B7-4/5/6/7, RAS and TP53 are NOT in the clamps dict --
they evolve under their own wild-type rules, so their final values are reported (not assumed) to
check whether they drifted.
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

# Same alphabetical-order convention as H-B7-4/H-B7-5/H-B7-6/H-B7-7 (pyboolnet's
# compute_attractors state strings).
PYBOOLNET_NODE_ORDER = h4.PYBOOLNET_NODE_ORDER
BRANCH_INPUTS = h4.BRANCH_INPUTS
GROWTH_ARREST_STATE = h4.GROWTH_ARREST_STATE
PROLIFERATION_STATE = h4.PROLIFERATION_STATE

apply_combined_clamp = h5.apply_combined_clamp

# H-B7-7's clamped values, for comparison against this experiment's UNCLAMPED final RAS/TP53.
H_B7_7_RAS_CLAMP = True
H_B7_7_TP53_CLAMP = False


def cmd_run() -> dict:
    text = DATA.read_text(encoding="utf-8")
    rules = h1.parse_bnet(text)
    node_names = [name for name, _ in rules]
    wild_type_rules = h1.compile_rules(rules)

    start_state = dict(zip(PYBOOLNET_NODE_ORDER, (c == "1" for c in GROWTH_ARREST_STATE)))

    def state_str(d: dict) -> str:
        return "".join("1" if d[n] else "0" for n in PYBOOLNET_NODE_ORDER)

    # Only p21CIP and RBL2 are clamped -- RAS and TP53 are left to evolve under their own rules.
    clamps = {"p21CIP": False, "RBL2": False}
    combined_rules = apply_combined_clamp(wild_type_rules, clamps)

    final_cycle = h3.run_until_attractor(start_state, combined_rules, node_names)
    final_state_nodeorder = final_cycle[0]
    branch_preserved = all(final_state_nodeorder[n] == v for n, v in BRANCH_INPUTS.items())
    final_pyboolnet_order_str = state_str(final_state_nodeorder)

    growth_arrest_phenotype = final_state_nodeorder.get("Growth_arrest")
    proliferation_phenotype = final_state_nodeorder.get("Proliferation")
    final_ras = final_state_nodeorder.get("RAS")
    final_tp53 = final_state_nodeorder.get("TP53")
    ras_matches_h_b7_7 = final_ras == H_B7_7_RAS_CLAMP
    tp53_matches_h_b7_7 = final_tp53 == H_B7_7_TP53_CLAMP

    if proliferation_phenotype and not growth_arrest_phenotype:
        final_label = "PROLIFERATION (necessity confirmed for p21CIP/RBL2 alone)"
    elif growth_arrest_phenotype:
        final_label = "GROWTH_ARREST (necessity NOT confirmed -- RAS/TP53 were load-bearing)"
    else:
        final_label = "AMBIGUOUS (neither phenotype node reads 1 -- requires manual inspection)"

    out = {
        "clamps": clamps,
        "ras_tp53_unclamped": True,
        "branch_inputs": BRANCH_INPUTS,
        "growth_arrest_state": GROWTH_ARREST_STATE,
        "proliferation_state": PROLIFERATION_STATE,
        "final_attractor_period": len(final_cycle),
        "final_attractor_type": "point" if len(final_cycle) == 1 else "complex",
        "final_state_pyboolnet_order": final_pyboolnet_order_str,
        "growth_arrest_phenotype_node": growth_arrest_phenotype,
        "proliferation_phenotype_node": proliferation_phenotype,
        "final_ras_unclamped": final_ras,
        "final_tp53_unclamped": final_tp53,
        "ras_matches_h_b7_7_clamped_value": ras_matches_h_b7_7,
        "tp53_matches_h_b7_7_clamped_value": tp53_matches_h_b7_7,
        "final_attractor_identity": final_label,
        "branch_inputs_preserved": branch_preserved,
        "flipped_to_proliferation": final_label.startswith("PROLIFERATION"),
        "comparison_to_h_b7_7_four_hit": (
            "H-B7-7 (RAS+TP53+p21CIP+RBL2, all clamped): CONFIRMED, reached Proliferation"
        ),
    }

    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    cmd_run()
