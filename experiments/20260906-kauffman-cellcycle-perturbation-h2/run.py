"""run.py — H-B7-2: perturbation (do-operator) test of Kauffman's Cancer Attractor hypothesis on
the Fauré et al. 2006 mammalian cell cycle network verified in H-B7-1.

Reuses H-B7-1's already-tested, already-CONFIRMED pipeline functions (parse_bnet, compile_rules,
synchronous_step) UNCHANGED via import -- does not modify H-B7-1's own run.py or its already-
recorded result. Adds ONE new function, `find_attractors_with_membership`, which is the same
brute-force algorithm as H-B7-1's `find_attractors` but ALSO returns which specific initial state
maps to which attractor -- needed here to answer "which CycD=0 states, under the intervention,
reach a NEW attractor" (H-B7-1 only needed aggregate basin sizes, not per-state membership).
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import boolean

HERE = Path(__file__).resolve().parent
H_B7_1_DIR = HERE.parent / "20260906-kauffman-cellcycle-attractors-h1"
METRICS = HERE / "metrics"

_SPEC = importlib.util.spec_from_file_location("kauffman_h1_run", H_B7_1_DIR / "run.py")
h1 = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(h1)

ALGEBRA = h1.ALGEBRA


def clamp_rule(
    compiled_rules: dict[str, boolean.Expression], node: str, value: bool
) -> dict[str, boolean.Expression]:
    """Return a COPY of compiled_rules with `node`'s update rule replaced by the constant
    `value` -- models do(node := value) for all time (permanent loss/gain of function), leaving
    every other node's rule untouched. `node` must already be a key (raises KeyError otherwise --
    fail loudly on a typo'd node name rather than silently adding a new node)."""
    if node not in compiled_rules:
        raise KeyError(f"cannot clamp unknown node {node!r}")
    clamped = dict(compiled_rules)
    clamped[node] = ALGEBRA.TRUE if value else ALGEBRA.FALSE
    return clamped


def find_attractors_with_membership(
    node_names: list[str], compiled_rules: dict[str, boolean.Expression]
) -> dict:
    """Same brute-force algorithm as H-B7-1's find_attractors, but ALSO returns an explicit
    initial-state -> attractor-index mapping, needed to filter results down to a specific
    sub-population of initial states (here: those with CycD=0) after the fact."""
    n = len(node_names)
    all_states = [tuple(bool((bits >> i) & 1) for i in range(n)) for bits in range(2**n)]

    def state_to_dict(state: tuple[bool, ...]) -> dict[str, bool]:
        return dict(zip(node_names, state))

    def dict_to_state(d: dict[str, bool]) -> tuple[bool, ...]:
        return tuple(d[name] for name in node_names)

    attractor_of: dict[tuple[bool, ...], int] = {}
    attractors: list[list[tuple[bool, ...]]] = []

    for start in all_states:
        if start in attractor_of:
            continue
        trajectory = [start]
        seen_index = {start: 0}
        current = start
        while True:
            nxt = dict_to_state(h1.synchronous_step(state_to_dict(current), compiled_rules))
            if nxt in attractor_of:
                target = attractor_of[nxt]
                for s in trajectory:
                    attractor_of[s] = target
                break
            if nxt in seen_index:
                cycle = trajectory[seen_index[nxt] :]
                new_index = len(attractors)
                attractors.append(cycle)
                for s in trajectory:
                    attractor_of[s] = new_index
                break
            trajectory.append(nxt)
            seen_index[nxt] = len(trajectory) - 1
            current = nxt

    def state_str(state: tuple[bool, ...]) -> str:
        return "".join("1" if v else "0" for v in state)

    return {
        "n_states_total": len(all_states),
        "n_attractors": len(attractors),
        "attractors": [
            {
                "period": len(cycle),
                "type": "point" if len(cycle) == 1 else "complex",
                "states": [state_str(s) for s in cycle],
            }
            for cycle in attractors
        ],
        "initial_state_to_attractor": {state_str(s): idx for s, idx in attractor_of.items()},
    }


def cmd_run() -> dict:
    text = h1.DATA.read_text(encoding="utf-8")
    rules = h1.parse_bnet(text)
    node_names = [name for name, _ in rules]
    wild_type_rules = h1.compile_rules(rules)

    cycd_index = node_names.index("CycD")

    def is_cycd_zero(state_str_: str) -> bool:
        return state_str_[cycd_index] == "0"

    out: dict = {"node_order": node_names, "interventions": {}}

    for node in ("Rb", "p27"):
        clamped = clamp_rule(wild_type_rules, node, False)
        result = find_attractors_with_membership(node_names, clamped)

        cycd0_attractor_indices = {
            idx for s, idx in result["initial_state_to_attractor"].items() if is_cycd_zero(s)
        }
        cycd0_attractor_types = {
            result["attractors"][idx]["type"] for idx in cycd0_attractor_indices
        }

        out["interventions"][f"do({node}=0)"] = {
            "n_attractors_total": result["n_attractors"],
            "attractors": result["attractors"],
            "cycd0_reaches_attractor_types": sorted(cycd0_attractor_types),
            "cycd0_reaches_complex_attractor": "complex" in cycd0_attractor_types,
        }

    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    cmd_run()
