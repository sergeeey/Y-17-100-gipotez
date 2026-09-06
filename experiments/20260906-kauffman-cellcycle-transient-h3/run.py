"""run.py — H-B7-3: transient (finite-duration) perturbation test -- the STRICT operationalization
of Kauffman's Cancer Attractor hypothesis named in H-B7-2's own Relaxation Map.

Reuses H-B7-1's pipeline functions (parse_bnet, compile_rules, synchronous_step) and H-B7-2's
clamp_rule UNCHANGED via import -- adds only the "clamp for k steps, then release" simulation
logic, which neither prior experiment needed.

Per claim.md's Compute-First Check, the outcome here is DEDUCIBLE from H-B7-1's own already-
verified result (the CycD=0 region has exactly one global attractor under the true, unperturbed
rules) -- this experiment verifies that deduction against concrete simulated trajectories rather
than trusting the argument alone (Gate-3-style discipline: check, don't just reason).
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
H_B7_1_DIR = HERE.parent / "20260906-kauffman-cellcycle-attractors-h1"
H_B7_2_DIR = HERE.parent / "20260906-kauffman-cellcycle-perturbation-h2"
METRICS = HERE / "metrics"

_SPEC1 = importlib.util.spec_from_file_location("kauffman_h1_run", H_B7_1_DIR / "run.py")
h1 = importlib.util.module_from_spec(_SPEC1)
_SPEC1.loader.exec_module(h1)

_SPEC2 = importlib.util.spec_from_file_location("kauffman_h2_run", H_B7_2_DIR / "run.py")
h2 = importlib.util.module_from_spec(_SPEC2)
_SPEC2.loader.exec_module(h2)


def run_until_attractor(
    state: dict[str, bool],
    compiled_rules: dict,
    node_names: list[str],
    max_steps: int = 200,
) -> list[dict[str, bool]]:
    """Iterate synchronous_step from `state` under `compiled_rules` until a previously-visited
    state recurs; return the cycle (list of states, length 1 for a point attractor) it settles
    into. Raises if no cycle is found within `max_steps` (would indicate a bug -- a finite
    deterministic system MUST cycle)."""

    def key(d: dict[str, bool]) -> tuple:
        return tuple(d[n] for n in node_names)

    trajectory = [dict(state)]
    seen = {key(state): 0}
    current = dict(state)
    for _ in range(max_steps):
        nxt = h1.synchronous_step(current, compiled_rules)
        k = key(nxt)
        if k in seen:
            return trajectory[seen[k] :]
        trajectory.append(nxt)
        seen[k] = len(trajectory) - 1
        current = nxt
    raise RuntimeError(f"no attractor found within {max_steps} steps -- likely a bug")


def simulate_transient_clamp(
    initial_state: dict[str, bool],
    node_names: list[str],
    wild_type_rules: dict,
    clamped_nodes: dict[str, bool],
    k_steps: int,
) -> dict:
    """Apply `clamped_nodes` (do(node := value) for each) for exactly `k_steps` synchronous
    updates, then RELEASE every clamped node back to its own wild-type rule and continue until
    an attractor is reached. Returns the final attractor (states + type)."""
    clamped_rules = dict(wild_type_rules)
    for node, value in clamped_nodes.items():
        clamped_rules = h2.clamp_rule(clamped_rules, node, value)

    current = dict(initial_state)
    for node, value in clamped_nodes.items():
        current[node] = value  # apply the clamp to the initial state itself, step 0
    for _ in range(k_steps):
        current = h1.synchronous_step(current, clamped_rules)

    final_cycle = run_until_attractor(current, wild_type_rules, node_names)
    states = ["".join("1" if v else "0" for v in (s[n] for n in node_names)) for s in final_cycle]
    return {
        "period": len(final_cycle),
        "type": "point" if len(final_cycle) == 1 else "complex",
        "states": states,
        "post_release_start_state": "".join(
            "1" if v else "0" for v in (current[n] for n in node_names)
        ),
    }


def cmd_run() -> dict:
    text = h1.DATA.read_text(encoding="utf-8")
    rules = h1.parse_bnet(text)
    node_names = [name for name, _ in rules]
    wild_type_rules = h1.compile_rules(rules)

    wild_type_quiescent_state = "0000001011"  # from H-B7-1, the verified positive control

    # Concrete test matrix: different clamp targets, durations, and starting states, always
    # with CycD=0 (the region whose single-attractor structure this experiment checks).
    cycd0_zero_state = dict.fromkeys(node_names, False)  # the all-zero CycD=0 state
    # a state visited mid-trajectory under do(Rb=0) permanent clamp in H-B7-2, used here as a
    # "harder" starting point already partway into the perturbed dynamics
    h_b7_2_mid_state_str = "0010110011"
    h_b7_2_mid_state = dict(zip(node_names, (c == "1" for c in h_b7_2_mid_state_str)))

    cases = [
        {
            "label": "all-zero start, clamp Rb, k=1",
            "start": cycd0_zero_state,
            "clamp": {"Rb": False},
            "k": 1,
        },
        {
            "label": "all-zero start, clamp Rb, k=5",
            "start": cycd0_zero_state,
            "clamp": {"Rb": False},
            "k": 5,
        },
        {
            "label": "all-zero start, clamp Rb, k=20",
            "start": cycd0_zero_state,
            "clamp": {"Rb": False},
            "k": 20,
        },
        {
            "label": "all-zero start, clamp p27, k=5",
            "start": cycd0_zero_state,
            "clamp": {"p27": False},
            "k": 5,
        },
        {
            "label": "all-zero start, clamp Rb+p27, k=5",
            "start": cycd0_zero_state,
            "clamp": {"Rb": False, "p27": False},
            "k": 5,
        },
        {
            "label": "H-B7-2-mid-trajectory start, clamp Rb, k=3",
            "start": h_b7_2_mid_state,
            "clamp": {"Rb": False},
            "k": 3,
        },
    ]

    results = []
    for case in cases:
        outcome = simulate_transient_clamp(
            case["start"], node_names, wild_type_rules, case["clamp"], case["k"]
        )
        outcome["label"] = case["label"]
        outcome["clamp"] = case["clamp"]
        outcome["k_steps"] = case["k"]
        outcome["returned_to_wild_type_quiescence"] = outcome["type"] == "point" and outcome[
            "states"
        ] == [wild_type_quiescent_state]
        results.append(outcome)

    out = {
        "node_order": node_names,
        "wild_type_quiescent_state": wild_type_quiescent_state,
        "cases": results,
        "all_cases_returned_to_quiescence": all(
            r["returned_to_wild_type_quiescence"] for r in results
        ),
    }

    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    cmd_run()
