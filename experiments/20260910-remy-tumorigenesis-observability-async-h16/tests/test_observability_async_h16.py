import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from run import (
    async_random_step,
    h1,
    run_async_trial,
    weighted_accuracy,
)


def test_async_random_step_only_changes_one_node():
    """Hand-verified: a single async micro-step must change AT MOST one node's value (it may
    change zero if the chosen node's new value happens to equal its old one) -- never more."""
    import boolean

    algebra = boolean.BooleanAlgebra()
    rules = {"A": algebra.parse("!B"), "B": algebra.parse("!A"), "C": algebra.parse("A&B")}
    state = {"A": True, "B": False, "C": False}
    rng = random.Random(42)
    new_state = async_random_step(state, rules, rng, ["A", "B", "C"])
    diffs = [n for n in state if state[n] != new_state[n]]
    assert len(diffs) <= 1


def test_async_random_step_deterministic_given_seed():
    """Hand-verified: same rng seed state must pick the same node and produce the same result --
    async_random_step must not have hidden nondeterminism beyond the passed rng."""
    import boolean

    algebra = boolean.BooleanAlgebra()
    rules = {"A": algebra.parse("!B"), "B": algebra.parse("!A")}
    state = {"A": True, "B": False}
    rng1 = random.Random(7)
    rng2 = random.Random(7)
    r1 = async_random_step(state, rules, rng1, ["A", "B"])
    r2 = async_random_step(state, rules, rng2, ["A", "B"])
    assert r1 == r2


def test_weighted_accuracy_hand_computed():
    """Hand-verified: 3 groups by marker X. Group X=True has fates [A,A,B] -> majority A,
    purity=2/3, contributes 2 correct. Group X=False has fates [B,B] -> majority B, purity=1.0,
    contributes 2 correct. Total domain=5, total correct=4 -> overall_accuracy=4/5=0.8."""
    domain = [
        {"observed_state": {"X": True}, "fate": "A"},
        {"observed_state": {"X": True}, "fate": "A"},
        {"observed_state": {"X": True}, "fate": "B"},
        {"observed_state": {"X": False}, "fate": "B"},
        {"observed_state": {"X": False}, "fate": "B"},
    ]
    result = weighted_accuracy(domain, {"X"})
    assert result["n_groups"] == 2
    assert abs(result["overall_accuracy"] - 0.8) < 1e-9


def test_weighted_accuracy_perfect_purity_gives_accuracy_one():
    """Hand-verified: if every group has a single, uniform fate, overall_accuracy must be
    exactly 1.0 -- recovers the deterministic 'zero collisions' case."""
    domain = [
        {"observed_state": {"X": True}, "fate": "A"},
        {"observed_state": {"X": True}, "fate": "A"},
        {"observed_state": {"X": False}, "fate": "B"},
    ]
    result = weighted_accuracy(domain, {"X"})
    assert result["overall_accuracy"] == 1.0


def test_run_async_trial_reproducible_with_same_seed():
    """Substrate sanity check: the SAME seed must give the SAME trial result end-to-end (no
    hidden global RNG state, no dict-ordering nondeterminism)."""
    text = (
        Path(__file__).resolve().parents[2]
        / "20260906-remy-tumorigenesis-transient-h4"
        / "data"
        / "remy_tumorigenesis.bnet"
    ).read_text(encoding="utf-8")
    rules = h1.parse_bnet(text)
    node_names = [n for n, _ in rules]
    wild_type_rules = h1.compile_rules(rules)

    import importlib.util

    h2_spec = importlib.util.spec_from_file_location(
        "h_b7_16_test_h2",
        Path(__file__).resolve().parents[2]
        / "20260906-kauffman-cellcycle-perturbation-h2"
        / "run.py",
    )
    h2 = importlib.util.module_from_spec(h2_spec)
    h2_spec.loader.exec_module(h2)

    from run import CLAMPS, GROWTH_ARREST_STATE_1, PYBOOLNET_NODE_ORDER

    clamped_rules = dict(wild_type_rules)
    for node, value in CLAMPS.items():
        clamped_rules = h2.clamp_rule(clamped_rules, node, value)
    start_state = dict(zip(PYBOOLNET_NODE_ORDER, (c == "1" for c in GROWTH_ARREST_STATE_1)))

    r1 = run_async_trial(start_state, clamped_rules, wild_type_rules, node_names, 4, 1, 10, seed=99)
    r2 = run_async_trial(start_state, clamped_rules, wild_type_rules, node_names, 4, 1, 10, seed=99)
    assert r1["observed_state"] == r2["observed_state"]
    assert r1["fate"] == r2["fate"]


def test_run_async_trial_different_seeds_can_diverge():
    """Sanity check that the simulation is actually stochastic (not silently deterministic
    despite different seeds) -- at least SOME of a handful of trials at a boundary k must differ,
    matching the Mechanism Claim Gate finding of real trial-to-trial variability."""
    text = (
        Path(__file__).resolve().parents[2]
        / "20260906-remy-tumorigenesis-transient-h4"
        / "data"
        / "remy_tumorigenesis.bnet"
    ).read_text(encoding="utf-8")
    rules = h1.parse_bnet(text)
    node_names = [n for n, _ in rules]
    wild_type_rules = h1.compile_rules(rules)

    import importlib.util

    h2_spec = importlib.util.spec_from_file_location(
        "h_b7_16_test_h2b",
        Path(__file__).resolve().parents[2]
        / "20260906-kauffman-cellcycle-perturbation-h2"
        / "run.py",
    )
    h2 = importlib.util.module_from_spec(h2_spec)
    h2_spec.loader.exec_module(h2)

    from run import CLAMPS, GROWTH_ARREST_STATE_1, PYBOOLNET_NODE_ORDER

    clamped_rules = dict(wild_type_rules)
    for node, value in CLAMPS.items():
        clamped_rules = h2.clamp_rule(clamped_rules, node, value)
    start_state = dict(zip(PYBOOLNET_NODE_ORDER, (c == "1" for c in GROWTH_ARREST_STATE_1)))

    fates = set()
    for seed in range(10):
        r = run_async_trial(
            start_state, clamped_rules, wild_type_rules, node_names, 4, 1, 20, seed=seed
        )
        fates.add(r["fate"])
    assert len(fates) >= 2  # k=4 is a boundary k -- must show real variability across seeds
