"""run.py — H-B7-1: independent brute-force verification of the Fauré et al. 2006 mammalian
cell cycle Boolean network's attractors, against the positive control in
data/faure_cellcycle_attractors_pyboolnet.md (Gate 3, Positive-Control Digitization).

PIPELINE (pure functions, no I/O, no verdicts):
    parse_bnet, compile_rules, synchronous_step, find_attractors
EXPERIMENT (I/O, controls, verdicts):
    cmd_run

Uses `boolean.py` (already an installed dependency) to parse/evaluate the .bnet logical
expressions -- no `eval()`, no custom parser, no new dependency.
"""

from __future__ import annotations

import json
from pathlib import Path

import boolean

HERE = Path(__file__).resolve().parent
DATA = HERE / "data" / "faure_cellcycle.bnet"
METRICS = HERE / "metrics"

ALGEBRA = boolean.BooleanAlgebra()


def parse_bnet(text: str) -> list[tuple[str, str]]:
    """Parse a .bnet file's `target, factors` lines into (name, expression_string) pairs, in
    file order. Skips the header line, blank lines, and `#`-comment lines."""
    rules: list[tuple[str, str]] = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.lower().startswith("targets"):
            continue
        name, expr = line.split(",", 1)
        rules.append((name.strip(), expr.strip()))
    return rules


def compile_rules(rules: list[tuple[str, str]]) -> dict[str, boolean.Expression]:
    """Parse each rule's expression string into a boolean.py Expression object."""
    return {name: ALGEBRA.parse(expr) for name, expr in rules}


def evaluate_expression(expr: boolean.Expression, state: dict[str, bool]) -> bool:
    """Substitute `state` into `expr` and reduce to True/False."""
    subs = {
        ALGEBRA.Symbol(name): (ALGEBRA.TRUE if value else ALGEBRA.FALSE)
        for name, value in state.items()
    }
    result = expr.subs(subs).simplify()
    return result == ALGEBRA.TRUE


def synchronous_step(
    state: dict[str, bool], compiled_rules: dict[str, boolean.Expression]
) -> dict[str, bool]:
    """Apply every node's update rule simultaneously (synchronous Boolean network update)."""
    return {name: evaluate_expression(compiled_rules[name], state) for name in compiled_rules}


def find_attractors(node_names: list[str], compiled_rules: dict[str, boolean.Expression]) -> dict:
    """Exhaustive brute-force attractor search under synchronous updating: enumerate ALL
    2^len(node_names) initial states, follow each trajectory until a previously-seen state
    recurs (guaranteed in a finite deterministic system), and group states by which attractor
    (cycle) they eventually reach. Returns distinct attractors (as ordered lists of states) and
    each attractor's basin size."""
    n = len(node_names)
    all_states = []
    for bits in range(2**n):
        state = tuple(bool((bits >> i) & 1) for i in range(n))
        all_states.append(state)

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
            nxt = dict_to_state(synchronous_step(state_to_dict(current), compiled_rules))
            if nxt in attractor_of:
                # trajectory feeds into an already-known attractor
                target = attractor_of[nxt]
                for s in trajectory:
                    attractor_of[s] = target
                break
            if nxt in seen_index:
                # found a NEW cycle: states from seen_index[nxt] onward form the attractor
                cycle = trajectory[seen_index[nxt] :]
                new_index = len(attractors)
                attractors.append(cycle)
                for s in trajectory:
                    attractor_of[s] = new_index
                break
            trajectory.append(nxt)
            seen_index[nxt] = len(trajectory) - 1
            current = nxt

    basin_sizes = [0] * len(attractors)
    for idx in attractor_of.values():
        basin_sizes[idx] += 1

    return {
        "n_states_total": len(all_states),
        "n_attractors": len(attractors),
        "attractors": [
            {
                "period": len(cycle),
                "type": "point" if len(cycle) == 1 else "complex",
                "states": ["".join("1" if v else "0" for v in s) for s in cycle],
                "basin_size": basin_sizes[i],
            }
            for i, cycle in enumerate(attractors)
        ],
    }


def cmd_run() -> dict:
    text = DATA.read_text(encoding="utf-8")
    rules = parse_bnet(text)
    node_names = [name for name, _ in rules]
    compiled = compile_rules(rules)

    result = find_attractors(node_names, compiled)
    result["node_order"] = node_names
    result["source"] = "data/faure_cellcycle.bnet"

    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    cmd_run()
