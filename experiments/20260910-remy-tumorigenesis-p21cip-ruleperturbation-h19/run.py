"""run.py -- H-B7-19: exhaustive single-bit truth-table perturbation robustness of p21CIP's own
rule -- the OTHER clamped node (RBL2's rule was tested in H-B7-17). p21CIP has 4 input symbols
(16-row truth table), too many to hand-derive a symbolic replacement expression per row safely
(H-B7-15's own tests already caught one hand-arithmetic error this session). Instead, this file
builds a GENERIC table-based rule representation: the truth table is computed ONCE from the real
boolean expression, each perturbation flips exactly one row, and evaluation is direct lookup --
no further boolean algebra, eliminating that entire error class.

Compute-First Check (see claim.md): p21CIP is one of the two clamped nodes -- h2.clamp_rule
replaces its compiled rule with a constant during the clamp, regardless of the underlying rule,
so H-B7-15's own 7-state-per-branch clamp-phase orbit is provably unaffected. Only post-release
dynamics differ. Reuses H-B7-15's exact k=1..6 domain.
"""

from __future__ import annotations

import importlib.util
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
H_B7_4_DIR = HERE.parent / "20260906-remy-tumorigenesis-transient-h4"
H_B7_13_DIR = HERE.parent / "20260910-remy-tumorigenesis-observability-h13"
H_B7_14_DIR = HERE.parent / "20260910-remy-tumorigenesis-observability-delayed-h14"
DATA = H_B7_4_DIR / "data" / "remy_tumorigenesis.bnet"
METRICS = HERE / "metrics"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


h13 = _load_module("h_b7_19_h13", H_B7_13_DIR / "run.py")
h14 = _load_module("h_b7_19_h14", H_B7_14_DIR / "run.py")
h1 = h13.h1

PYBOOLNET_NODE_ORDER = h13.PYBOOLNET_NODE_ORDER
GROWTH_ARREST_STATE_1 = h13.GROWTH_ARREST_STATE_1
GROWTH_ARREST_STATE_2 = h13.GROWTH_ARREST_STATE_2
CLAMPS = h13.CLAMPS
FLOOR_M = h13.FLOOR_M
CEILING_M = h13.CEILING_M
CANDIDATE_M1 = h13.CANDIDATE_M1
CANDIDATE_M2 = h13.CANDIDATE_M2
fate_label = h13.fate_label
find_collisions = h13.find_collisions

TESTED_K = list(range(1, 7))  # H-B7-15's own established exhaustive orbit range, both branches

P21CIP_INPUTS = ("TP53", "CyclinE1", "AKT", "Growth_inhibitors")


class TableRule:
    """A node's update rule represented as an explicit truth table over `inputs`, instead of a
    boolean.py Expression. `table` maps a tuple of input bool-values (in `inputs` order) to the
    node's output value. Evaluation is direct dict lookup -- no boolean algebra involved, so a
    single-bit perturbation (one flipped table entry) cannot introduce a symbolic-derivation
    error the way hand-writing a replacement expression could."""

    def __init__(self, inputs: tuple, table: dict):
        self.inputs = inputs
        self.table = table

    def evaluate(self, state: dict) -> bool:
        key = tuple(state[n] for n in self.inputs)
        return self.table[key]

    def flipped(self, row: tuple) -> TableRule:
        new_table = dict(self.table)
        new_table[row] = not new_table[row]
        return TableRule(self.inputs, new_table)


def build_table_from_expression(expr, inputs: tuple) -> TableRule:
    """Compute a node's full truth table by evaluating its REAL boolean.py expression at every
    input combination -- not hand-derived, so this is the ground truth the perturbations are
    built from."""
    table = {}
    for combo in itertools.product([False, True], repeat=len(inputs)):
        state = dict(zip(inputs, combo))
        table[combo] = h1.evaluate_expression(expr, state)
    return TableRule(inputs, table)


def synchronous_step_with_table_override(
    state: dict, compiled_rules: dict, override_node: str, override_rule: TableRule
) -> dict:
    """H-B7-1's synchronous_step, generalized to allow ONE node's rule to be a TableRule instead
    of a boolean.py Expression -- every other node uses h1.evaluate_expression unchanged."""
    new_state = {}
    for name, expr in compiled_rules.items():
        if name == override_node:
            new_state[name] = override_rule.evaluate(state)
        else:
            new_state[name] = h1.evaluate_expression(expr, state)
    return new_state


def run_until_attractor_with_table_override(
    state: dict, compiled_rules: dict, node_names: list, override_node, override_rule, max_steps=200
) -> list[dict]:
    """h3.run_until_attractor's cycle-detection loop, generalized for a table-overridden node."""

    def key(d: dict) -> tuple:
        return tuple(d[n] for n in node_names)

    trajectory = [dict(state)]
    seen = {key(state): 0}
    current = dict(state)
    for _ in range(max_steps):
        nxt = synchronous_step_with_table_override(
            current, compiled_rules, override_node, override_rule
        )
        k = key(nxt)
        if k in seen:
            return trajectory[seen[k] :]
        trajectory.append(nxt)
        seen[k] = len(trajectory) - 1
        current = nxt
    raise RuntimeError(f"no attractor found within {max_steps} steps -- likely a bug")


def simulate_with_table_override(
    initial_state: dict,
    node_names: list,
    wild_type_rules: dict,
    clamped_nodes: dict,
    k_steps: int,
    j_steps: int,
    override_node: str,
    override_rule: TableRule,
) -> dict:
    """H-B7-14's simulate_transient_clamp_multi_with_delayed_observation, generalized for a
    table-overridden node. Note: clamp_rule (applied below) unconditionally overwrites
    p21CIP/RBL2 to a constant during the clamp phase -- so the override_rule is ONLY consulted
    post-release, exactly matching H-B7-17's own Compute-First reasoning for RBL2."""
    import importlib.util as _ilu

    h2_spec = _ilu.spec_from_file_location(
        "h_b7_19_h2_local",
        HERE.parent / "20260906-kauffman-cellcycle-perturbation-h2" / "run.py",
    )
    h2 = _ilu.module_from_spec(h2_spec)
    h2_spec.loader.exec_module(h2)

    clamped_rules = dict(wild_type_rules)
    for node, value in clamped_nodes.items():
        clamped_rules = h2.clamp_rule(clamped_rules, node, value)

    current = dict(initial_state)
    for node, value in clamped_nodes.items():
        current[node] = value
    for _ in range(k_steps):
        # NOTE: during the clamp phase, override_node (p21CIP) is ALREADY forced to a constant
        # by clamp_rule above -- using synchronous_step_with_table_override here would WRONGLY
        # ignore that constant and substitute the perturbed table instead, defeating the very
        # Compute-First Check this experiment's claim.md relies on (caught before running, not
        # by the reviewer: the override must apply ONLY post-release, matching H-B7-17's own
        # reasoning that the clamp makes the node's own rule irrelevant during the clamp).
        current = h1.synchronous_step(current, clamped_rules)
    for _ in range(j_steps):
        current = synchronous_step_with_table_override(
            current, wild_type_rules, override_node, override_rule
        )
    observed_state = dict(current)

    final_cycle = run_until_attractor_with_table_override(
        current, wild_type_rules, node_names, override_node, override_rule
    )
    return {"observed_state": observed_state, "final_state": final_cycle[0]}


def build_domain(node_names, wild_type_rules, override_rule) -> tuple[list, list]:
    branches = [
        ("branch_1", GROWTH_ARREST_STATE_1),
        ("branch_2", GROWTH_ARREST_STATE_2),
    ]
    domain_j0, domain_j1 = [], []
    for branch_name, growth_arrest_state in branches:
        start_state = dict(zip(PYBOOLNET_NODE_ORDER, (c == "1" for c in growth_arrest_state)))
        for k in TESTED_K:
            sim0 = simulate_with_table_override(
                start_state, node_names, wild_type_rules, CLAMPS, k, 0, "p21CIP", override_rule
            )
            sim1 = simulate_with_table_override(
                start_state, node_names, wild_type_rules, CLAMPS, k, 1, "p21CIP", override_rule
            )
            fate = fate_label(sim0["final_state"])
            domain_j0.append(
                {
                    "branch": branch_name,
                    "k": k,
                    "release_state": sim0["observed_state"],
                    "fate": fate,
                }
            )
            domain_j1.append(
                {
                    "branch": branch_name,
                    "k": k,
                    "release_state": sim1["observed_state"],
                    "fate": fate,
                }
            )
    return domain_j0, domain_j1


def cmd_run() -> dict:
    text = DATA.read_text(encoding="utf-8")
    rules = h1.parse_bnet(text)
    node_names = [name for name, _ in rules]
    wild_type_rules = h1.compile_rules(rules)

    original_p21cip_table = build_table_from_expression(wild_type_rules["p21CIP"], P21CIP_INPUTS)

    conditions = {"baseline_unperturbed": original_p21cip_table}
    for row in sorted(original_p21cip_table.table.keys()):
        row_label = "".join("T" if v else "F" for v in row)
        conditions[f"flip_{row_label}"] = original_p21cip_table.flipped(row)

    results = {}
    orbit_lengths_seen = set()
    for cond_name, table_rule in conditions.items():
        domain_j0, domain_j1 = build_domain(node_names, wild_type_rules, table_rule)
        orbit_lengths_seen.add(len(domain_j0))

        per_marker = {}
        for m_name, m_set in [
            ("floor_DNA_damage_only", FLOOR_M),
            ("ceiling_full_state", CEILING_M),
            ("candidate_M1_phenotypes_only", CANDIDATE_M1),
            ("candidate_M2_phenotypes_plus_clamp_targets", CANDIDATE_M2),
        ]:
            coll0 = find_collisions(domain_j0, m_set)
            coll1 = find_collisions(domain_j1, m_set)
            per_marker[m_name] = {
                "n_collisions_j0": len(coll0),
                "n_collisions_j1": len(coll1),
                "sufficient_at_j1": len(coll1) == 0,
            }
        results[cond_name] = per_marker

    classification = {}
    for name, r in results.items():
        if name == "baseline_unperturbed":
            continue
        transition_exists = r["floor_DNA_damage_only"]["n_collisions_j0"] > 0
        m1_sufficient_j1 = r["candidate_M1_phenotypes_only"]["sufficient_at_j1"]
        if not transition_exists:
            classification[name] = "CRITERION_INVALID_no_transition"
        elif m1_sufficient_j1:
            classification[name] = "ROBUST"
        else:
            classification[name] = "FRAGILE"

    robust = [n for n, c in classification.items() if c == "ROBUST"]
    fragile = [n for n, c in classification.items() if c == "FRAGILE"]
    invalid = [n for n, c in classification.items() if c == "CRITERION_INVALID_no_transition"]

    n_meaningfully_tested = len(robust) + len(fragile)
    if n_meaningfully_tested == 0:
        verdict = "ALL_CRITERION_INVALID"
    elif len(fragile) == 0:
        verdict = "ROBUST"
    elif len(robust) == 0:
        verdict = "FRAGILE"
    else:
        verdict = "PARTIALLY-ROBUST"

    out = {
        "claim": "H-B7-19 exhaustive p21CIP rule-perturbation robustness of j*=1 sufficiency",
        "tested_k": TESTED_K,
        "n_perturbations_tested": len(conditions) - 1,
        "orbit_lengths_seen": sorted(orbit_lengths_seen),
        "substrate_check_orbit_unchanged": len(orbit_lengths_seen) == 1,
        "classification": classification,
        "robust_perturbations": robust,
        "fragile_perturbations": fragile,
        "criterion_invalid_perturbations": invalid,
        "n_robust": len(robust),
        "n_fragile": len(fragile),
        "n_criterion_invalid": len(invalid),
        "verdict": verdict,
        "results_by_perturbation": results,
    }

    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    print(json.dumps(out, indent=2, default=str))
    return out


if __name__ == "__main__":
    cmd_run()
