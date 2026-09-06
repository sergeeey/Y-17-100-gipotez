"""run.py — H-B7-9: transient do(p21CIP=0, RBL2=0) for k steps then RELEASED, on the Remy et al.
2015 bladder tumorigenesis network's bistable branch -- the sharpest available test of Kauffman's
STRICT original hypothesis in this bridge (pathology as a pre-existing attractor of the
UNPERTURBED network, revealed by a temporary push, not requiring the perturbation to persist).

Reuses H-B7-1's pipeline functions (parse_bnet, compile_rules, synchronous_step), H-B7-2's
clamp_rule, H-B7-3's run_until_attractor, and H-B7-5's DATA path UNCHANGED via import. Adds
`simulate_transient_clamp_multi`, a thin generalization of H-B7-3's own `simulate_transient_clamp`
that (a) accepts an already-compiled clamps dict for MULTIPLE simultaneous nodes (H-B7-3's version
already supported this via its `clamped_nodes` dict, reused as-is) and (b) returns the final STATE
DICT directly (not only an encoded string), so callers can read individual node/phenotype values.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
H_B7_1_DIR = HERE.parent / "20260906-kauffman-cellcycle-attractors-h1"
H_B7_2_DIR = HERE.parent / "20260906-kauffman-cellcycle-perturbation-h2"
H_B7_3_DIR = HERE.parent / "20260906-kauffman-cellcycle-transient-h3"
H_B7_4_DIR = HERE.parent / "20260906-remy-tumorigenesis-transient-h4"
H_B7_5_DIR = HERE.parent / "20260906-remy-tumorigenesis-twohit-h5"
DATA = H_B7_4_DIR / "data" / "remy_tumorigenesis.bnet"
METRICS = HERE / "metrics"

_SPEC1 = importlib.util.spec_from_file_location("kauffman_h1_run", H_B7_1_DIR / "run.py")
h1 = importlib.util.module_from_spec(_SPEC1)
_SPEC1.loader.exec_module(h1)

_SPEC2 = importlib.util.spec_from_file_location("kauffman_h2_run", H_B7_2_DIR / "run.py")
h2 = importlib.util.module_from_spec(_SPEC2)
_SPEC2.loader.exec_module(h2)

_SPEC3 = importlib.util.spec_from_file_location("kauffman_h3_run", H_B7_3_DIR / "run.py")
h3 = importlib.util.module_from_spec(_SPEC3)
_SPEC3.loader.exec_module(h3)

_SPEC4 = importlib.util.spec_from_file_location("remy_h4_run", H_B7_4_DIR / "run.py")
h4 = importlib.util.module_from_spec(_SPEC4)
_SPEC4.loader.exec_module(h4)

_SPEC5 = importlib.util.spec_from_file_location("remy_h5_run", H_B7_5_DIR / "run.py")
h5 = importlib.util.module_from_spec(_SPEC5)
_SPEC5.loader.exec_module(h5)

# Same alphabetical-order convention as H-B7-4..8 (pyboolnet's compute_attractors state strings).
PYBOOLNET_NODE_ORDER = h4.PYBOOLNET_NODE_ORDER
BRANCH_INPUTS = h4.BRANCH_INPUTS
GROWTH_ARREST_STATE = h4.GROWTH_ARREST_STATE
PROLIFERATION_STATE = h4.PROLIFERATION_STATE

TESTED_DURATIONS = (1, 3, 10, 30)


def simulate_transient_clamp_multi(
    initial_state: dict,
    node_names: list,
    wild_type_rules: dict,
    clamped_nodes: dict,
    k_steps: int,
) -> dict:
    """Apply `clamped_nodes` for exactly `k_steps` synchronous updates, then RELEASE every
    clamped node back to its own wild-type rule and continue until an attractor is reached.
    Generalizes H-B7-3's `simulate_transient_clamp` to return the final STATE DICT (not only an
    encoded string), so callers can read individual node/phenotype values directly."""
    clamped_rules = dict(wild_type_rules)
    for node, value in clamped_nodes.items():
        clamped_rules = h2.clamp_rule(clamped_rules, node, value)

    current = dict(initial_state)
    for node, value in clamped_nodes.items():
        current[node] = value  # apply the clamp to the initial state itself, step 0
    for _ in range(k_steps):
        current = h1.synchronous_step(current, clamped_rules)

    final_cycle = h3.run_until_attractor(current, wild_type_rules, node_names)
    return {
        "final_state": final_cycle[0],
        "period": len(final_cycle),
        "type": "point" if len(final_cycle) == 1 else "complex",
    }


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
            label = "PROLIFERATION (strict Kauffman claim CONFIRMED for this k)"
        elif growth_arrest_phenotype:
            label = "GROWTH_ARREST (relapsed after release)"
        else:
            label = "AMBIGUOUS (neither phenotype node reads 1)"

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
                "flipped_to_proliferation": label.startswith("PROLIFERATION"),
                "matches_proliferation_state": final_str == PROLIFERATION_STATE,
                "matches_growth_arrest_state": final_str == GROWTH_ARREST_STATE,
            }
        )

    any_flipped = any(r["flipped_to_proliferation"] for r in results_by_k)

    out = {
        "clamps": clamps,
        "branch_inputs": BRANCH_INPUTS,
        "growth_arrest_state": GROWTH_ARREST_STATE,
        "proliferation_state": PROLIFERATION_STATE,
        "tested_durations": list(TESTED_DURATIONS),
        "results_by_k": results_by_k,
        "any_case_flipped_to_proliferation": any_flipped,
        "comparison_to_h_b7_8_permanent": (
            "H-B7-8 (permanent do(p21CIP=0, RBL2=0)): CONFIRMED, reached Proliferation"
        ),
    }

    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    cmd_run()
