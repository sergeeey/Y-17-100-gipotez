"""run.py — H-B7-6: combined permanent do(RAS=1, TP53=0, p21CIP=0) three-hit perturbation on the
Remy et al. 2015 bladder tumorigenesis network's bistable branch -- the deliberate three-assumption
follow-up named in H-B7-5's own Relaxation Map, directly removing the TP53-independent p21CIP
blocker H-B7-5 traced as the reason the two-hit RAS+TP53 combination failed.

Reuses H-B7-1's pipeline functions (parse_bnet, compile_rules, synchronous_step), H-B7-2's
clamp_rule, H-B7-3's run_until_attractor, and H-B7-5's apply_combined_clamp UNCHANGED via import --
all already generic, no modification needed.
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

# Same alphabetical-order convention as H-B7-4/H-B7-5 (pyboolnet's compute_attractors state
# strings).
PYBOOLNET_NODE_ORDER = h4.PYBOOLNET_NODE_ORDER
BRANCH_INPUTS = h4.BRANCH_INPUTS
GROWTH_ARREST_STATE = h4.GROWTH_ARREST_STATE
PROLIFERATION_STATE = h4.PROLIFERATION_STATE

apply_combined_clamp = h5.apply_combined_clamp


def cmd_run() -> dict:
    text = DATA.read_text(encoding="utf-8")
    rules = h1.parse_bnet(text)
    node_names = [name for name, _ in rules]
    wild_type_rules = h1.compile_rules(rules)

    start_state = dict(zip(PYBOOLNET_NODE_ORDER, (c == "1" for c in GROWTH_ARREST_STATE)))

    def state_str(d: dict) -> str:
        return "".join("1" if d[n] else "0" for n in PYBOOLNET_NODE_ORDER)

    clamps = {"RAS": True, "TP53": False, "p21CIP": False}
    combined_rules = apply_combined_clamp(wild_type_rules, clamps)

    final_cycle = h3.run_until_attractor(start_state, combined_rules, node_names)
    final_state_nodeorder = final_cycle[0]
    branch_preserved = all(final_state_nodeorder[n] == v for n, v in BRANCH_INPUTS.items())
    final_pyboolnet_order_str = state_str(final_state_nodeorder)

    if final_pyboolnet_order_str == GROWTH_ARREST_STATE:
        final_label = "GROWTH_ARREST (unchanged -- three-hit insufficient)"
    elif final_pyboolnet_order_str == PROLIFERATION_STATE:
        final_label = "PROLIFERATION (flipped! checkpoint-removal mechanism confirmed)"
    else:
        final_label = "OTHER/NEW attractor (not seen in H-B7-4/H-B7-5's runs)"

    out = {
        "clamps": clamps,
        "branch_inputs": BRANCH_INPUTS,
        "growth_arrest_state": GROWTH_ARREST_STATE,
        "proliferation_state": PROLIFERATION_STATE,
        "final_attractor_period": len(final_cycle),
        "final_attractor_type": "point" if len(final_cycle) == 1 else "complex",
        "final_state_pyboolnet_order": final_pyboolnet_order_str,
        "final_attractor_identity": final_label,
        "branch_inputs_preserved": branch_preserved,
        "flipped_to_proliferation": final_label.startswith("PROLIFERATION"),
        "comparison_to_h_b7_5_two_hit": (
            "H-B7-5 (RAS+TP53): REJECTED, returned to Growth_arrest "
            "via TP53-independent p21CIP route"
        ),
    }

    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    cmd_run()
