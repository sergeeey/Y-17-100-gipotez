from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent.parent


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def h21():
    return _load_module("test_h21_run", HERE / "run.py")


@pytest.fixture(scope="module")
def result(h21):
    return h21.cmd_run()


def test_extract_inputs_matches_hand_known_cases(h21):
    text = h21.DATA.read_text(encoding="utf-8")
    rules = h21.h1.parse_bnet(text)
    compiled = h21.h1.compile_rules(rules)
    compiled_by_name = dict(rules)
    del compiled_by_name

    assert set(h21.extract_inputs(compiled["RBL2"])) == {"CyclinE1", "CyclinD1"}
    assert set(h21.extract_inputs(compiled["p21CIP"])) == {
        "TP53",
        "CyclinE1",
        "AKT",
        "Growth_inhibitors",
    }
    assert set(h21.extract_inputs(compiled["CyclinE1"])) == {
        "p21CIP",
        "RBL2",
        "E2F3_medium",
        "CDC25A",
        "E2F1_medium",
    }


def test_baseline_is_fixed_point_for_all_nodes_both_branches(result):
    assert result["part_a"]["baseline_fixed_point_failures"] == []


def test_theorem_holds_exhaustively_zero_mismatches(result):
    assert result["part_a"]["n_mismatches"] == 0
    assert result["part_a"]["n_total_row_checks"] > 0
    assert result["part_a"]["theorem_confirmed_exhaustively"] is True


def test_all_35_nodes_checked(result):
    assert result["part_a"]["n_nodes_checked"] == 35


def test_exactly_one_destabilizing_row_per_node_per_branch(h21, result):
    text = h21.DATA.read_text(encoding="utf-8")
    rules = h21.h1.parse_bnet(text)
    node_names = [name for name, _ in rules]
    compiled_rules = h21.h1.compile_rules(rules)
    node_inputs = {n: h21.extract_inputs(compiled_rules[n]) for n in node_names}
    node_tables = {
        n: h21.build_table_from_expression(compiled_rules[n], node_inputs[n]) for n in node_names
    }

    for branch_name, state_str in h21.BRANCHES:
        state = h21.state_str_to_dict(state_str)
        for n in node_names:
            table = node_tables[n]
            inputs = node_inputs[n]
            own_row = tuple(state[i] for i in inputs)
            baseline_val = table.evaluate(state)
            n_destabilizing = 0
            for row in table.table:
                flipped = table.flipped(row)
                if flipped.evaluate(state) != baseline_val:
                    n_destabilizing += 1
                    assert row == own_row, (
                        f"{n}/{branch_name}: unexpected destabilizing row "
                        f"{row} != own_row {own_row}"
                    )
            assert n_destabilizing == 1, f"{n}/{branch_name}: expected exactly 1 destabilizing row"


def test_multi_node_simultaneous_perturbation_preserves_fixed_point(result):
    assert result["part_a"]["multi_node_confirmed"] is True
    for branch_data in result["part_a"]["multi_node_simultaneous_check"].values():
        assert len(branch_data["chosen_perturbations"]) == 2
        assert branch_data["still_fixed_point_under_simultaneous_perturbation"] is True


def test_synthesis_cross_check_matches_prior_criterion_invalid_counts(result):
    cross_check = result["part_b"]["synthesis_cross_check"]
    for node in ("RBL2", "p21CIP", "CyclinE1"):
        assert cross_check[node]["part_a_n_destabilizing_branch_1"] == 1
        assert cross_check[node]["part_a_n_destabilizing_branch_2"] == 1
        assert cross_check[node]["matches_prior_criterion_invalid_count_of_1"] is True


def test_overall_verdict_confirmed(result):
    assert result["verdict"] == "CONFIRMED"


def test_regression_theorem_would_catch_an_injected_wrong_row(h21):
    """Negative control: deliberately claim a WRONG row is the destabilizing one for a real node,
    and confirm the theorem-check logic (changed == predicted_changed) would flag it as a
    mismatch -- proving the check is not vacuously true."""
    text = h21.DATA.read_text(encoding="utf-8")
    rules = h21.h1.parse_bnet(text)
    compiled_rules = h21.h1.compile_rules(rules)
    inputs = h21.extract_inputs(compiled_rules["RBL2"])
    table = h21.build_table_from_expression(compiled_rules["RBL2"], inputs)

    state = h21.state_str_to_dict(h21.PROLIFERATION_STATE)
    own_row = tuple(state[i] for i in inputs)
    baseline_val = table.evaluate(state)

    wrong_row = next(r for r in table.table if r != own_row)
    flipped = table.flipped(wrong_row)
    changed = flipped.evaluate(state) != baseline_val
    predicted_changed_if_wrong_row_were_own_row = True
    assert changed != predicted_changed_if_wrong_row_were_own_row, (
        "a non-own-row perturbation must NOT change evaluate(S) -- if it did, the theorem itself "
        "would be false for this node, not just a bookkeeping bug"
    )
