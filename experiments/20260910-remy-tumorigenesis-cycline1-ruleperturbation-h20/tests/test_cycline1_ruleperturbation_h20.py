import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from run import (
    CLAMPS,
    CYCLIN_E1_INPUTS,
    DATA,
    GROWTH_ARREST_STATE_1,
    PYBOOLNET_NODE_ORDER,
    build_domain_for_perturbation,
    build_table_from_expression,
    h1,
    h2,
    walk_clamped_orbit_with_override,
)


def _hand_cyclin_e1(p21cip, rbl2, e2f3_medium, cdc25a, e2f1_medium) -> bool:
    """Hand-derived, factored form (claim.md): !p21CIP&!RBL2&E2F3_medium&CDC25A |
    !p21CIP&!RBL2&E2F1_medium&CDC25A = !p21CIP & !RBL2 & CDC25A & (E2F3_medium | E2F1_medium)."""
    return (not p21cip) and (not rbl2) and cdc25a and (e2f3_medium or e2f1_medium)


def _load_original_cyclin_e1_expr():
    text = DATA.read_text(encoding="utf-8")
    rules = h1.parse_bnet(text)
    compiled = h1.compile_rules(rules)
    return compiled["CyclinE1"]


def test_table_construction_matches_hand_factored_form_all_32_rows():
    """The auto-built truth table (from the REAL boolean.py expression) must match the
    hand-factored form at ALL 32 rows -- exhaustive, not spot-checked."""
    expr = _load_original_cyclin_e1_expr()
    table_rule = build_table_from_expression(expr, CYCLIN_E1_INPUTS)
    for combo in itertools.product([False, True], repeat=5):
        expected = _hand_cyclin_e1(*combo)
        state = dict(zip(CYCLIN_E1_INPUTS, combo))
        assert h1.evaluate_expression(expr, state) == expected, f"real expr mismatch at {combo}"
        assert table_rule.evaluate(state) == expected, f"table mismatch at {combo}"


def test_original_table_has_exactly_3_true_rows():
    """Hand-derived: !p21CIP&!RBL2&CDC25A&(E2F3_medium|E2F1_medium) is True at exactly 3 of 32
    rows (p21CIP=F,RBL2=F,CDC25A=T fixed; E2F3_medium/E2F1_medium not both False -> 3 of 4)."""
    expr = _load_original_cyclin_e1_expr()
    table_rule = build_table_from_expression(expr, CYCLIN_E1_INPUTS)
    n_true = sum(1 for v in table_rule.table.values() if v)
    assert n_true == 3


def test_baseline_orbit_matches_h_b7_15_exactly():
    """Critical Substrate Gate check: the UNPERTURBED CyclinE1 table (via table-lookup override)
    must reproduce EXACTLY the same clamp-phase orbit H-B7-15 found via the original symbolic
    expression (7 states per branch, cycle_period=1) -- if this doesn't match, the table-override
    machinery has a bug and NOTHING downstream can be trusted."""
    text = DATA.read_text(encoding="utf-8")
    rules = h1.parse_bnet(text)
    node_names = [n for n, _ in rules]
    wild_type_rules = h1.compile_rules(rules)
    original_table = build_table_from_expression(wild_type_rules["CyclinE1"], CYCLIN_E1_INPUTS)

    clamped_rules = dict(wild_type_rules)
    for node, value in CLAMPS.items():
        clamped_rules = h2.clamp_rule(clamped_rules, node, value)
    start_state = dict(zip(PYBOOLNET_NODE_ORDER, (c == "1" for c in GROWTH_ARREST_STATE_1)))
    clamp_applied_start = dict(start_state)
    for node, value in CLAMPS.items():
        clamp_applied_start[node] = value

    orbit = walk_clamped_orbit_with_override(
        clamp_applied_start, node_names, clamped_rules, original_table, 200
    )
    assert orbit["orbit_length"] == 7  # H-B7-15's own committed constant, branch_1
    assert orbit["cycle_period"] == 1


def test_flipped_row_can_change_orbit_length():
    """Structural sanity check (real difference from H-B7-17/19, per claim.md): since CyclinE1
    is NOT a clamped node, a perturbation CAN in principle change the clamp-phase orbit length --
    this test just confirms the machinery runs end-to-end for a perturbed table without crashing
    and returns a well-formed domain, not that the length necessarily changes for this specific
    row (which is an empirical question the main experiment answers, not asserted here)."""
    text = DATA.read_text(encoding="utf-8")
    rules = h1.parse_bnet(text)
    node_names = [n for n, _ in rules]
    wild_type_rules = h1.compile_rules(rules)
    original_table = build_table_from_expression(wild_type_rules["CyclinE1"], CYCLIN_E1_INPUTS)
    flipped = original_table.flipped((False, False, False, False, False))

    domain_j0, domain_j1, orbit_info = build_domain_for_perturbation(
        node_names, wild_type_rules, flipped
    )
    assert len(domain_j0) > 0
    assert len(domain_j1) == len(domain_j0)
    assert "branch_1" in orbit_info and "branch_2" in orbit_info
