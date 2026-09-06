"""run.py — H-B7-4: transient RAS perturbation on the Remy et al. 2015 bladder tumorigenesis
network's bistable (Growth_arrest / Proliferation) branch -- the faithful, structurally-capable
test of Kauffman's strict Cancer Attractor hypothesis that H-B7-3 showed the small Fauré model
could not provide.

Reuses H-B7-1's pipeline functions (parse_bnet, compile_rules, synchronous_step) and H-B7-3's
simulate_transient_clamp / run_until_attractor UNCHANGED via import -- both are already generic
(parameterized by node_names), no modification needed for this new, larger network.

The independent ground truth for this branch's attractor structure comes from `pyboolnet`
(installed as a real dependency, not just a source of .bnet files) -- see claim.md's
Compute-First Check and Gate 3 discipline.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
H_B7_1_DIR = HERE.parent / "20260906-kauffman-cellcycle-attractors-h1"
H_B7_3_DIR = HERE.parent / "20260906-kauffman-cellcycle-transient-h3"
DATA = HERE / "data" / "remy_tumorigenesis.bnet"
METRICS = HERE / "metrics"

_SPEC1 = importlib.util.spec_from_file_location("kauffman_h1_run", H_B7_1_DIR / "run.py")
h1 = importlib.util.module_from_spec(_SPEC1)
_SPEC1.loader.exec_module(h1)

_SPEC3 = importlib.util.spec_from_file_location("kauffman_h3_run", H_B7_3_DIR / "run.py")
h3 = importlib.util.module_from_spec(_SPEC3)
_SPEC3.loader.exec_module(h3)

# pyboolnet's compute_attractors() reports state strings in ALPHABETICAL node order (its
# primes.keys() order), NOT this .bnet file's declaration order -- same subtlety already
# resolved once in H-B7-1's decision.md. Recorded explicitly here so every state string in
# this file is decoded consistently.
PYBOOLNET_NODE_ORDER = [
    "AKT",
    "ATM_high",
    "ATM_medium",
    "Apoptosis_high",
    "Apoptosis_medium",
    "CDC25A",
    "CHEK1_2_high",
    "CHEK1_2_medium",
    "CyclinA",
    "CyclinD1",
    "CyclinE1",
    "DNA_damage",
    "E2F1_high",
    "E2F1_medium",
    "E2F3_high",
    "E2F3_medium",
    "EGFR",
    "EGFR_stimulus",
    "FGFR3",
    "FGFR3_stimulus",
    "GRB2",
    "Growth_arrest",
    "Growth_inhibitors",
    "MDM2",
    "PI3K",
    "PTEN",
    "Proliferation",
    "RAS",
    "RB1",
    "RBL2",
    "SPRY",
    "TP53",
    "p14ARF",
    "p16INK4a",
    "p21CIP",
]

BRANCH_INPUTS = {
    "DNA_damage": False,
    "EGFR_stimulus": False,
    "FGFR3_stimulus": True,
    "Growth_inhibitors": True,
}

# Ground truth from pyboolnet.attractors.compute_attractors() run against this exact .bnet file
# (see claim.md's Compute-First Check) -- independently cross-checked in
# tests/test_remy_tumorigenesis_transient.py against this project's own synchronous_step.
GROWTH_ARREST_STATE = "00000000000000000011011000011110001"
PROLIFERATION_STATE = "00000100101001010011001000110010110"


def cmd_run() -> dict:
    text = DATA.read_text(encoding="utf-8")
    rules = h1.parse_bnet(text)
    node_names = [name for name, _ in rules]
    wild_type_rules = h1.compile_rules(rules)

    start_state = dict(zip(PYBOOLNET_NODE_ORDER, (c == "1" for c in GROWTH_ARREST_STATE)))

    def state_str(d: dict) -> str:
        return "".join("1" if d[n] else "0" for n in PYBOOLNET_NODE_ORDER)

    cases_spec = [
        {"label": "clamp RAS=1, k=1", "clamp": {"RAS": True}, "k": 1},
        {"label": "clamp RAS=1, k=3", "clamp": {"RAS": True}, "k": 3},
        {"label": "clamp RAS=1, k=10", "clamp": {"RAS": True}, "k": 10},
        {"label": "clamp RAS=1, k=30", "clamp": {"RAS": True}, "k": 30},
    ]

    results = []
    for spec in cases_spec:
        outcome = h3.simulate_transient_clamp(
            start_state, node_names, wild_type_rules, spec["clamp"], spec["k"]
        )

        # Decode the final attractor's first state back into a dict keyed by node_names (the
        # order simulate_transient_clamp/run_until_attractor actually used internally) to
        # check the branch-defining inputs, then re-encode in PYBOOLNET_NODE_ORDER for
        # comparison against the known attractor strings.
        final_state_nodeorder = dict(zip(node_names, (c == "1" for c in outcome["states"][0])))
        branch_preserved = all(final_state_nodeorder[n] == v for n, v in BRANCH_INPUTS.items())
        final_pyboolnet_order_str = state_str(final_state_nodeorder)

        if final_pyboolnet_order_str == GROWTH_ARREST_STATE:
            final_label = "GROWTH_ARREST (original)"
        elif final_pyboolnet_order_str == PROLIFERATION_STATE:
            final_label = "PROLIFERATION (flipped!)"
        else:
            final_label = "OTHER/UNKNOWN attractor"

        results.append(
            {
                "label": spec["label"],
                "clamp": spec["clamp"],
                "k_steps": spec["k"],
                "final_attractor_type": outcome["type"],
                "final_attractor_period": outcome["period"],
                "final_state_pyboolnet_order": final_pyboolnet_order_str,
                "final_attractor_identity": final_label,
                "branch_inputs_preserved": branch_preserved,
                "flipped_to_proliferation": final_label == "PROLIFERATION (flipped!)",
            }
        )

    out = {
        "branch_inputs": BRANCH_INPUTS,
        "growth_arrest_state": GROWTH_ARREST_STATE,
        "proliferation_state": PROLIFERATION_STATE,
        "cases": results,
        "any_case_flipped_to_proliferation": any(r["flipped_to_proliferation"] for r in results),
    }

    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    cmd_run()
