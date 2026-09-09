"""run.py -- H-B7-16: does {Growth_arrest, Proliferation} observability at j=1 async round
post-release (H-B7-14/15's own synchronous j*=1 finding) survive under general-asynchronous
update -- a genuinely stochastic dynamics, unlike H-B7-13/14/15's deterministic synchronous case?

Mechanism Claim Gate (see claim.md): a single-point readout is UNSTABLE under async (confirmed via
diag_async_mechanism_check.py, scratchpad); a 30-round windowed-majority vote is stable (purity
0.97-1.00). Adopted as the "true" eventual-fate estimator here.

Reuses H-B7-13's FLOOR_M, CEILING_M, CANDIDATE_M1, CANDIDATE_M2, PYBOOLNET_NODE_ORDER,
BRANCH_INPUTS_1/2, GROWTH_ARREST_STATE_1/2, CLAMPS UNCHANGED via distinct-name import.
"""

from __future__ import annotations

import importlib.util
import json
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
H_B7_4_DIR = HERE.parent / "20260906-remy-tumorigenesis-transient-h4"
H_B7_13_DIR = HERE.parent / "20260910-remy-tumorigenesis-observability-h13"
DATA = H_B7_4_DIR / "data" / "remy_tumorigenesis.bnet"
METRICS = HERE / "metrics"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


h13 = _load_module("h_b7_16_h13", H_B7_13_DIR / "run.py")
h1 = h13.h1
h2 = h13.h2

PYBOOLNET_NODE_ORDER = h13.PYBOOLNET_NODE_ORDER
BRANCH_INPUTS_1 = h13.BRANCH_INPUTS_1
GROWTH_ARREST_STATE_1 = h13.GROWTH_ARREST_STATE_1
BRANCH_INPUTS_2 = h13.BRANCH_INPUTS_2
GROWTH_ARREST_STATE_2 = h13.GROWTH_ARREST_STATE_2
CLAMPS = h13.CLAMPS
FLOOR_M = h13.FLOOR_M
CEILING_M = h13.CEILING_M
CANDIDATE_M1 = h13.CANDIDATE_M1
CANDIDATE_M2 = h13.CANDIDATE_M2
marker_projection = h13.marker_projection

TESTED_K = list(range(1, 7))  # matches H-B7-15's own exhaustive orbit range (both branches)
N_TRIALS = 200
READOUT_ROUNDS = 30


def async_random_step(state: dict, rules: dict, rng: random.Random, node_pool: list) -> dict:
    """One general-asynchronous micro-step: pick ONE node uniformly at random, update it from
    the LATEST values of all others (rules are looked up from `rules`, evaluated against the
    CURRENT state -- other nodes unchanged this micro-step)."""
    node = rng.choice(node_pool)
    new_state = dict(state)
    new_state[node] = h1.evaluate_expression(rules[node], state)
    return new_state


def run_async_trial(
    start_state: dict,
    clamped_rules: dict,
    wild_type_rules: dict,
    node_pool: list,
    k_rounds: int,
    j_rounds: int,
    readout_rounds: int,
    seed: int,
) -> dict:
    """Clamp for k_rounds async rounds (n_free micro-steps/round, standard GA convention),
    release, observe at j_rounds, then continue readout_rounds MORE rounds recording a
    windowed-majority-vote phenotype as the trial's own eventual fate estimate (Mechanism Claim
    Gate finding: single-point readout is unstable, windowed majority is stable)."""
    rng = random.Random(seed)
    n_free = len(node_pool)
    state = dict(start_state)
    for node, value in CLAMPS.items():
        state[node] = value
    for _ in range(k_rounds * n_free):
        state = async_random_step(state, clamped_rules, rng, node_pool)
    for _ in range(j_rounds * n_free):
        state = async_random_step(state, wild_type_rules, rng, node_pool)
    observed_state = dict(state)

    ga_votes = []
    pr_votes = []
    for _ in range(readout_rounds):
        for _ in range(n_free):
            state = async_random_step(state, wild_type_rules, rng, node_pool)
        ga_votes.append(state["Growth_arrest"])
        pr_votes.append(state["Proliferation"])
    ga_majority = sum(ga_votes) > len(ga_votes) / 2
    pr_majority = sum(pr_votes) > len(pr_votes) / 2
    if pr_majority and not ga_majority:
        fate = "PROLIFERATION"
    elif ga_majority:
        fate = "GROWTH_ARREST"
    else:
        fate = "AMBIGUOUS"
    ga_purity = max(sum(ga_votes), len(ga_votes) - sum(ga_votes)) / len(ga_votes)
    pr_purity = max(sum(pr_votes), len(pr_votes) - sum(pr_votes)) / len(pr_votes)

    return {
        "observed_state": observed_state,
        "fate": fate,
        "ga_purity": ga_purity,
        "pr_purity": pr_purity,
    }


def weighted_accuracy(domain: list[dict], markers: set) -> dict:
    """Group trials by their markers projection; within each group, majority fate = the group's
    prediction, purity = majority fraction. Overall accuracy = size-weighted average purity --
    the probabilistic generalization of H-B7-13/14/15's exact 'zero collisions' notion (purity=1.0
    everywhere recovers the deterministic case exactly)."""
    groups: dict[tuple, list[str]] = {}
    for entry in domain:
        proj = marker_projection(entry["observed_state"], markers)
        groups.setdefault(proj, []).append(entry["fate"])

    total = len(domain)
    correct = 0
    group_summaries = []
    for proj, fates in groups.items():
        counts: dict[str, int] = {}
        for f in fates:
            counts[f] = counts.get(f, 0) + 1
        majority_fate, majority_count = max(counts.items(), key=lambda kv: kv[1])
        correct += majority_count
        group_summaries.append(
            {
                "projection": [{"node": n, "value": v} for n, v in proj],
                "n": len(fates),
                "majority_fate": majority_fate,
                "purity": majority_count / len(fates),
            }
        )
    return {
        "n_groups": len(groups),
        "overall_accuracy": correct / total if total else None,
        "group_summaries": sorted(group_summaries, key=lambda g: -g["n"])[:10],
    }


def cmd_run() -> dict:
    text = DATA.read_text(encoding="utf-8")
    rules = h1.parse_bnet(text)
    node_names = [name for name, _ in rules]
    wild_type_rules = h1.compile_rules(rules)
    clamped_rules = dict(wild_type_rules)
    for node, value in CLAMPS.items():
        clamped_rules = h2.clamp_rule(clamped_rules, node, value)

    branches = [
        ("branch_1", GROWTH_ARREST_STATE_1),
        ("branch_2", GROWTH_ARREST_STATE_2),
    ]

    domain_j0 = []
    domain_j1 = []
    trial_log_sample = []
    seed_counter = 0
    for branch_name, growth_arrest_state in branches:
        start_state = dict(zip(PYBOOLNET_NODE_ORDER, (c == "1" for c in growth_arrest_state)))
        for k in TESTED_K:
            for trial in range(N_TRIALS):
                seed_counter += 1
                result0 = run_async_trial(
                    start_state,
                    clamped_rules,
                    wild_type_rules,
                    node_names,
                    k,
                    0,
                    READOUT_ROUNDS,
                    seed=seed_counter,
                )
                result1 = run_async_trial(
                    start_state,
                    clamped_rules,
                    wild_type_rules,
                    node_names,
                    k,
                    1,
                    READOUT_ROUNDS,
                    seed=seed_counter,  # same seed -> same clamp trajectory, j only shifts readout
                )
                domain_j0.append(
                    {
                        "branch": branch_name,
                        "k": k,
                        "trial": trial,
                        "observed_state": result0["observed_state"],
                        "fate": result0["fate"],
                    }
                )
                domain_j1.append(
                    {
                        "branch": branch_name,
                        "k": k,
                        "trial": trial,
                        "observed_state": result1["observed_state"],
                        "fate": result1["fate"],
                    }
                )
                if trial < 3:
                    trial_log_sample.append(
                        {
                            "branch": branch_name,
                            "k": k,
                            "trial": trial,
                            "fate_j0_trial": result0["fate"],
                            "fate_j1_trial": result1["fate"],
                        }
                    )

    results_j0 = {}
    results_j1 = {}
    for m_name, m_set in [
        ("floor_DNA_damage_only", FLOOR_M),
        ("ceiling_full_state", CEILING_M),
        ("candidate_M1_phenotypes_only", CANDIDATE_M1),
        ("candidate_M2_phenotypes_plus_clamp_targets", CANDIDATE_M2),
    ]:
        results_j0[m_name] = weighted_accuracy(domain_j0, m_set)
        results_j1[m_name] = weighted_accuracy(domain_j1, m_set)

    fate_distribution_by_k = {}
    for branch_name, _ in branches:
        for k in TESTED_K:
            key = f"{branch_name}_k{k}"
            fates = [e["fate"] for e in domain_j1 if e["branch"] == branch_name and e["k"] == k]
            counts: dict[str, int] = {}
            for f in fates:
                counts[f] = counts.get(f, 0) + 1
            fate_distribution_by_k[key] = counts

    out = {
        "claim": "H-B7-16 asynchronous-update robustness of j*=1 observability",
        "n_trials_per_condition": N_TRIALS,
        "tested_k": TESTED_K,
        "readout_rounds": READOUT_ROUNDS,
        "domain_size": len(domain_j0),
        "fate_distribution_by_k_at_j1": fate_distribution_by_k,
        "results_at_j0": {
            k: {"n_groups": v["n_groups"], "overall_accuracy": v["overall_accuracy"]}
            for k, v in results_j0.items()
        },
        "results_at_j1": {
            k: {"n_groups": v["n_groups"], "overall_accuracy": v["overall_accuracy"]}
            for k, v in results_j1.items()
        },
        "M1_accuracy_improvement_j0_to_j1": (
            results_j1["candidate_M1_phenotypes_only"]["overall_accuracy"]
            - results_j0["candidate_M1_phenotypes_only"]["overall_accuracy"]
        ),
    }

    METRICS.mkdir(exist_ok=True)
    (METRICS / "run.json").write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    print(json.dumps(out, indent=2, default=str))
    return out


if __name__ == "__main__":
    cmd_run()
