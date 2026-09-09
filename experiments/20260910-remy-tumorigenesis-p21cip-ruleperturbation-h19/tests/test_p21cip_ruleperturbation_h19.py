import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from run import (
    CLAMPS,
    DATA,
    GROWTH_ARREST_STATE_1,
    P21CIP_INPUTS,
    PYBOOLNET_NODE_ORDER,
    build_table_from_expression,
    h1,
    simulate_with_table_override,
)


def _hand_p21cip(tp53: bool, cyclin_e1: bool, akt: bool, growth_inhibitors: bool) -> bool:
    """Hand-derived, factored form of the REAL rule (claim.md, Design rationale):
    TP53&!CyclinE1&!AKT | Growth_inhibitors&!CyclinE1&!AKT
      = !CyclinE1 & !AKT & (TP53 | Growth_inhibitors)   (distributive law)."""
    return (not cyclin_e1) and (not akt) and (tp53 or growth_inhibitors)


def _load_original_p21cip_expr():
    text = DATA.read_text(encoding="utf-8")
    rules = h1.parse_bnet(text)
    compiled = h1.compile_rules(rules)
    return compiled["p21CIP"]


def test_table_construction_matches_hand_factored_form_all_16_rows():
    """The auto-built truth table (from the REAL boolean.py expression, not hand-derived) must
    match the hand-factored form at ALL 16 rows -- not spot-checked, exhaustive, since 16 rows
    is cheap to check completely and this is the ground-truth table every perturbation is built
    from."""
    expr = _load_original_p21cip_expr()
    table_rule = build_table_from_expression(expr, P21CIP_INPUTS)
    for combo in itertools.product([False, True], repeat=4):
        tp53, cyclin_e1, akt, gi = combo
        expected = _hand_p21cip(tp53, cyclin_e1, akt, gi)
        state = dict(zip(P21CIP_INPUTS, combo))
        assert h1.evaluate_expression(expr, state) == expected, f"real expr mismatch at {combo}"
        assert table_rule.evaluate(state) == expected, f"table mismatch at {combo}"


def test_original_table_has_exactly_3_true_rows():
    """Hand-derived: !CyclinE1 & !AKT & (TP53 | Growth_inhibitors) is True at exactly 3 of 16
    rows (CyclinE1=False, AKT=False fixed; TP53/Growth_inhibitors not both False -> 3 of 4
    combinations of those two)."""
    expr = _load_original_p21cip_expr()
    table_rule = build_table_from_expression(expr, P21CIP_INPUTS)
    n_true = sum(1 for v in table_rule.table.values() if v)
    assert n_true == 3


def test_flipped_differs_at_exactly_one_row():
    """Structural sanity check: TableRule.flipped(row) must differ from the original at EXACTLY
    that one row, matching every OTHER row exactly -- confirms a genuine single-bit flip."""
    expr = _load_original_p21cip_expr()
    original = build_table_from_expression(expr, P21CIP_INPUTS)
    target_row = (False, False, False, False)  # TP53=F, CyclinE1=F, AKT=F, GI=F
    flipped = original.flipped(target_row)
    diffs = [row for row in original.table if original.table[row] != flipped.table[row]]
    assert diffs == [target_row]


def test_evaluate_uses_input_order_not_state_dict_order():
    """Hand-verified: TableRule.evaluate must key the lookup by P21CIP_INPUTS order, not by
    whatever order a state dict happens to iterate in -- confirmed by passing a state dict with
    EXTRA unrelated keys in a different insertion order and checking the result is unaffected."""
    expr = _load_original_p21cip_expr()
    table_rule = build_table_from_expression(expr, P21CIP_INPUTS)
    state = {
        "Growth_inhibitors": True,
        "AKT": False,
        "SomeOtherNode": True,
        "TP53": True,
        "CyclinE1": False,
        "YetAnotherNode": False,
    }
    # TP53=T, CyclinE1=F, AKT=F, GI=T -> hand rule: !F & !F & (T|T) = True
    assert table_rule.evaluate(state) is True


def test_clamp_phase_ignores_override_uses_the_clamp_constant():
    """Regression test for a bug caught BEFORE running anything (not by the reviewer): during
    the k-round clamp phase, p21CIP is ALREADY forced to False by clamp_rule, regardless of its
    own rule. simulate_with_table_override must respect that constant during the clamp and only
    consult override_rule AFTER release -- confirmed here by using a DELIBERATELY WRONG
    override_rule (constant True for every row) and checking that k=1 (a single clamp step,
    zero release steps observed) still shows p21CIP=False at the observed release state, proving
    the clamp's constant won, not the override table."""
    text = DATA.read_text(encoding="utf-8")
    rules = h1.parse_bnet(text)
    node_names = [n for n, _ in rules]
    wild_type_rules = h1.compile_rules(rules)

    always_true_table = build_table_from_expression(wild_type_rules["p21CIP"], P21CIP_INPUTS)
    for row in always_true_table.table:
        always_true_table.table[row] = True  # deliberately wrong: p21CIP always True if consulted

    start_state = dict(zip(PYBOOLNET_NODE_ORDER, (c == "1" for c in GROWTH_ARREST_STATE_1)))
    sim = simulate_with_table_override(
        start_state, node_names, wild_type_rules, CLAMPS, 1, 0, "p21CIP", always_true_table
    )
    assert sim["observed_state"]["p21CIP"] is False  # clamp constant, not the wrong override
