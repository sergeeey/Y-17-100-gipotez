"""Reproduce the audit without rerunning or overwriting research experiments.

Constructed numerical examples test mathematical claims, not empirical biology.
The only file written is evidence.json beside this script.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import platform
from collections import Counter
from pathlib import Path

import numpy as np
import scipy
import yaml
from scipy.linalg import eig, expm

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
BUILDER = ROOT / "experiments/20260907-chernoff-neuralode-nd-multiseed-multin/run.py"
POPULATION = (
    ROOT
    / "experiments/20260908-chernoff-neuralode-nd-tighter-predictor-robustness/metrics/run.json"
)


def condition_number(a: np.ndarray) -> float:
    # Independent scipy left/right eigenvectors; project uses numpy eig + inverse.
    vals, left, right = eig(a, left=True, right=True)
    i = int(np.argmax(vals.real))
    return float(
        np.linalg.norm(left[:, i])
        * np.linalg.norm(right[:, i])
        / abs(np.vdot(left[:, i], right[:, i]))
    )


def main() -> None:
    spec = importlib.util.spec_from_file_location("audit_builder", BUILDER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    graph = yaml.safe_load((ROOT / "registry/graph.yaml").read_text(encoding="utf-8"))
    hypotheses = [n for n in graph["nodes"] if n["type"] == "hypothesis"]
    population = json.loads(POPULATION.read_text(encoding="utf-8"))
    rows = population["train_data"] + population["test_data"]

    # Pre-existing training matrix: one resolvent evaluation already disproves equality.
    n, seed, x = 40, 314, 0.7405684692
    assert any(r["n_dim"] == n and r["seed"] == seed for r in population["train_data"])
    a = module.build_matrix_with_seed_and_n(n, seed)
    b = a - 0.5 * np.eye(n)
    kappa = condition_number(a)
    k_lower = float(x / np.linalg.svd(x * np.eye(n) - b, compute_uv=False)[-1])
    assert k_lower > 2 * kappa

    # Analytically separated dominant mode; all entries respect the generator support.
    crafted = np.diag(np.r_[0.5, np.linspace(-50.0, -1.0, 39)])
    crafted[-5:, -5:] += np.triu(np.full((5, 5), 14.0), 1)
    shifted = crafted - 0.5 * np.eye(40)
    crafted_x = 1.059637
    crafted_lower = float(
        crafted_x / np.linalg.svd(crafted_x * np.eye(40) - shifted, compute_uv=False)[-1]
    )
    assert abs(condition_number(crafted) - 1) < 1e-12
    assert crafted_lower > 40

    horizon_rows = []
    for row in rows:
        mat = module.build_matrix_with_seed_and_n(row["n_dim"], row["seed"])
        kap = condition_number(mat)
        horizon_rows.append(
            {
                "n_dim": row["n_dim"],
                "seed": row["seed"],
                "stored_m1_t_le_1": row["m1"],
                "asymptotic_norm": kap,
                "asymptotic_over_stored": kap / row["m1"],
            }
        )
    worst = max(horizon_rows, key=lambda r: r["asymptotic_over_stored"])

    # Fairer alpha baseline: fit both alpha and log N, solely on existing TRAIN.
    def design(data):
        return np.array([[1, np.log(r["alpha_eps"]), np.log(r["n_dim"])] for r in data])

    y_train = np.log([r["m1"] for r in population["train_data"]])
    y_test = np.log([r["m1"] for r in population["test_data"]])
    coef = np.linalg.lstsq(design(population["train_data"]), y_train, rcond=None)[0]
    rmse = float(np.sqrt(np.mean((design(population["test_data"]) @ coef - y_test) ** 2)))

    result = {
        "scope": "Retrospective audit; counterexamples are numerical/model evidence, not a new discovery.",  # noqa: E501
        "environment": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
        },
        "input_sha256": {
            str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in [BUILDER, POPULATION, ROOT / "registry/graph.yaml"]
        },
        "inventory": {
            "nodes": len(graph["nodes"]),
            "edges": len(graph["edges"]),
            "hypotheses": len(hypotheses),
            "status": dict(Counter(n["status"] for n in hypotheses)),
            "evidence_labels": dict(Counter(n["evidence"] for n in hypotheses)),
            "branches": dict(Counter(n["id"].split("-")[1] for n in hypotheses)),
        },
        "shift_counterexample": {
            "A": "0.5 I_2",
            "K(A-0.5I)": 1,
            "raw_norm_t10": float(np.exp(5)),
            "wrong_ceiling": float(2 * np.e),
            "true_K_A_and_raw_infinite_horizon_sup": "infinity",
        },
        "existing_training_counterexample": {
            "n": n,
            "seed": seed,
            "x": x,
            "kappa_lambda1": kappa,
            "K_shifted_lower_bound": k_lower,
            "ratio": k_lower / kappa,
        },
        "constructed_support_counterexample": {
            "n": 40,
            "last_block_size": 5,
            "coupling": 14,
            "kappa_lambda1": condition_number(crafted),
            "K_shifted_lower_bound": crafted_lower,
            "norm_exp_shifted_t1": float(np.linalg.norm(expm(shifted), 2)),
        },
        "horizon": {
            "population_size": len(rows),
            "asymptotic_exceeds_stored_m1": sum(
                r["asymptotic_over_stored"] > 1 + 1e-6 for r in horizon_rows
            ),
            "worst": worst,
            "interpretation": "Finite-horizon M1 is not the all-time semigroup supremum; this does not invalidate it as a finite-horizon prediction target.",  # noqa: E501
        },
        "fairer_baseline_retrospective": {
            "features": ["intercept", "log_alpha_eps", "log_N"],
            "test_rmse": rmse,
            "original_k_model_test_rmse": population["rmse_expanded_model_on_fresh_test"],
            "note": "Diagnostic reuse of revealed test data; not a new confirmatory model-selection experiment.",  # noqa: E501
        },
    }
    (OUT / "evidence.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
