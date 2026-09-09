"""run.py -- H-B7-21: minimal necessary/sufficient condition for the Proliferation attractor's own
fixed-point status under single-bit rule perturbation, checked EXHAUSTIVELY across all 35 network
nodes (not just the 3 already tested in H-B7-17/19/20), plus a synthesis of the three existing
sensitivity profiles.

Part A -- the general theorem: for state S (a known fixed point) and node n, flipping row r of n's
own truth table changes evaluate(S) for n IFF r == own_row(n, S) (S's own projected input values
for n). This is close to tautological given a table-lookup evaluator, but is CHECKED exhaustively
here rather than assumed -- this session has twice already found real bugs in constructs that
looked "obviously correct" (H-B7-15, H-B7-19).

Part B -- synthesis of H-B7-17 (RBL2, 4 rows), H-B7-19 (p21CIP, 16 rows), H-B7-20 (CyclinE1, 32
rows): ROBUST/FRAGILE/CRITERION_INVALID counts, explicitly NOT fitting a trend to n=3 points.

Reuses H-B7-19's TableRule/build_table_from_expression UNCHANGED via distinct-name import; reuses
H-B7-1's parse_bnet/compile_rules/evaluate_expression; reuses H-B7-13/20's PYBOOLNET_NODE_ORDER,
PROLIFERATION_STATE(_2).
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
H_B7_4_DIR = HERE.parent / "20260906-remy-tumorigenesis-transient-h4"
H_B7_13_DIR = HERE.parent / "20260910-remy-tumorigenesis-observability-h13"
H_B7_19_DIR = HERE.parent / "20260910-remy-tumorigenesis-p21cip-ruleperturbation-h19"
DATA = H_B7_4_DIR / "data" / "remy_tumorigenesis.bnet"
METRICS = HERE / "metrics"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


h13 = _load_module("h_b7_21_h13", H_B7_13_DIR / "run.py")
h19 = _load_module("h_b7_21_h19", H_B7_19_DIR / "run.py")
h1 = h13.h1

PYBOOLNET_NODE_ORDER = h13.PYBOOLNET_NODE_ORDER
TableRule = h19.TableRule
build_table_from_expression = h19.build_table_from_expression

PROLIFERATION_STATE = "00000100101001010011001000110010110"
PROLIFERATION_STATE_2 = "00000100101001010111001000110010110"

BRANCHES = [("branch_1", PROLIFERATION_STATE), ("branch_2", PROLIFERATION_STATE_2)]


def state_str_to_dict(s: str) -> dict:
    return dict(zip(PYBOOLNET_NODE_ORDER, (c == "1" for c in s)))


def extract_inputs(expr) -> tuple:
    """Real input symbols of a compiled boolean.py expression, sorted for a deterministic row
    order (order only needs to be internally consistent per node, not matching any other
    experiment's hand-chosen ordering)."""
    return tuple(sorted(str(s) for s in expr.symbols))


def synchronous_step_with_multi_override(
    state: dict, compiled_rules: dict, overrides: dict
) -> dict:
    """Generalizes H-B7-19's synchronous_step_with_table_override to allow SEVERAL nodes to use a
    table-lookup override simultaneously (overrides: {node_name: TableRule}), while every other
    node uses the normal boolean.py expression evaluation unchanged."""
    result = {}
    for name, expr in compiled_rules.items():
        if name in overrides:
            result[name] = overrides[name].evaluate(state)
        else:
            result[name] = h1.evaluate_expression(expr, state)
    return result


def cmd_run() -> dict:
    text = DATA.read_text(encoding="utf-8")
    rules = h1.parse_bnet(text)
    node_names = [name for name, _ in rules]
    compiled_rules = h1.compile_rules(rules)

    node_inputs = {n: extract_inputs(compiled_rules[n]) for n in node_names}
    node_tables = {
        n: build_table_from_expression(compiled_rules[n], node_inputs[n]) for n in node_names
    }

    per_node_results = {}
    n_total_checks = 0
    n_mismatches = 0
    mismatches: list[dict] = []
    baseline_fixed_point_failures: list[dict] = []
    destabilizing_row_by_node_branch = {}

    for branch_name, state_str in BRANCHES:
        state = state_str_to_dict(state_str)
        for n in node_names:
            table = node_tables[n]
            inputs = node_inputs[n]
            baseline_val = table.evaluate(state)
            if baseline_val != state[n]:
                baseline_fixed_point_failures.append(
                    {
                        "node": n,
                        "branch": branch_name,
                        "expected": state[n],
                        "table_gave": baseline_val,
                    }
                )
            own_row = tuple(state[i] for i in inputs)

            node_key = f"{n}|{branch_name}"
            per_node_results[node_key] = {
                "node": n,
                "branch": branch_name,
                "n_inputs": len(inputs),
                "n_rows": len(table.table),
                "own_row": list(own_row),
                "rows_checked": 0,
                "n_destabilizing": 0,
            }

            for row in sorted(table.table.keys()):
                flipped = table.flipped(row)
                flipped_val = flipped.evaluate(state)
                changed = flipped_val != baseline_val
                predicted_changed = row == own_row
                n_total_checks += 1
                per_node_results[node_key]["rows_checked"] += 1
                if changed:
                    per_node_results[node_key]["n_destabilizing"] += 1
                    destabilizing_row_by_node_branch[node_key] = list(row)
                if changed != predicted_changed:
                    n_mismatches += 1
                    mismatches.append(
                        {
                            "node": n,
                            "branch": branch_name,
                            "row": list(row),
                            "changed": changed,
                            "predicted_changed": predicted_changed,
                        }
                    )

    # Multi-node simultaneous-perturbation check: pick two nodes, one non-own-row perturbation
    # each, verify the FULL network single synchronous step from S is still S under BOTH
    # perturbations applied at once (not just individually, as H-B7-17/19/20 each tested).
    multi_node_check = {}
    for branch_name, state_str in BRANCHES:
        state = state_str_to_dict(state_str)
        overrides = {}
        chosen = []
        for n in node_names:
            table = node_tables[n]
            inputs = node_inputs[n]
            own_row = tuple(state[i] for i in inputs)
            non_own_rows = [r for r in table.table if r != own_row]
            if non_own_rows and len(chosen) < 2:
                pick_row = non_own_rows[0]
                overrides[n] = table.flipped(pick_row)
                chosen.append({"node": n, "flipped_row": list(pick_row)})
            if len(chosen) == 2:
                break

        next_state = synchronous_step_with_multi_override(state, compiled_rules, overrides)
        still_fixed_point = next_state == state
        multi_node_check[branch_name] = {
            "chosen_perturbations": chosen,
            "still_fixed_point_under_simultaneous_perturbation": still_fixed_point,
        }

    theorem_confirmed = n_mismatches == 0 and not baseline_fixed_point_failures
    multi_node_confirmed = all(
        v["still_fixed_point_under_simultaneous_perturbation"] for v in multi_node_check.values()
    )

    # Part B -- synthesis of already-collected H-B7-17/19/20 sensitivity profiles (no new compute,
    # transcribed from each experiment's own committed metrics/run.json / decision.md).
    sensitivity_synthesis = {
        "RBL2": {
            "source": "H-B7-17",
            "n_inputs": 2,
            "n_rows": 4,
            "n_robust": 2,
            "n_fragile": 1,
            "n_criterion_invalid": 1,
            "fragile_rate_of_meaningfully_tested": round(1 / 3, 4),
        },
        "p21CIP": {
            "source": "H-B7-19",
            "n_inputs": 4,
            "n_rows": 16,
            "n_robust": 15,
            "n_fragile": 0,
            "n_criterion_invalid": 1,
            "fragile_rate_of_meaningfully_tested": round(0 / 15, 4),
        },
        "CyclinE1": {
            "source": "H-B7-20",
            "n_inputs": 5,
            "n_rows": 32,
            "n_robust": 28,
            "n_fragile": 3,
            "n_criterion_invalid": 1,
            "fragile_rate_of_meaningfully_tested": round(3 / 31, 4),
        },
    }
    # cross-check: does Part A's exhaustive n_destabilizing (per node, per branch) equal 1, and
    # does it match the criterion_invalid count of 1 each already found in H-B7-17/19/20?
    synthesis_cross_check = {}
    for node in ("RBL2", "p21CIP", "CyclinE1"):
        b1 = per_node_results[f"{node}|branch_1"]["n_destabilizing"]
        b2 = per_node_results[f"{node}|branch_2"]["n_destabilizing"]
        synthesis_cross_check[node] = {
            "part_a_n_destabilizing_branch_1": b1,
            "part_a_n_destabilizing_branch_2": b2,
            "matches_prior_criterion_invalid_count_of_1": (b1 == 1 and b2 == 1),
        }

    out = {
        "claim": "H-B7-21 -- network-wide minimal necessary/sufficient condition for "
        "Proliferation fixed-point preservation under single-bit rule perturbation, "
        "+ three-node sensitivity synthesis",
        "part_a": {
            "n_nodes_checked": len(node_names),
            "n_total_row_checks": n_total_checks,
            "n_mismatches": n_mismatches,
            "mismatches": mismatches,
            "baseline_fixed_point_failures": baseline_fixed_point_failures,
            "theorem_confirmed_exhaustively": theorem_confirmed,
            "destabilizing_row_by_node_branch": destabilizing_row_by_node_branch,
            "multi_node_simultaneous_check": multi_node_check,
            "multi_node_confirmed": multi_node_confirmed,
        },
        "part_b": {
            "sensitivity_synthesis": sensitivity_synthesis,
            "synthesis_cross_check": synthesis_cross_check,
        },
        "verdict": "CONFIRMED" if (theorem_confirmed and multi_node_confirmed) else "REJECTED",
    }

    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    print(
        json.dumps(
            {k: v for k, v in out.items() if k != "part_a"}
            | {
                "part_a_summary": {
                    k: v for k, v in out["part_a"].items() if k not in ("mismatches",)
                }
            },
            indent=2,
            default=str,
        )
    )
    return out


if __name__ == "__main__":
    cmd_run()
