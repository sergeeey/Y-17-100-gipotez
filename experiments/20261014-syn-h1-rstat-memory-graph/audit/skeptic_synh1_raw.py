# ruff: noqa
"""Skeptic tests T1/T2/T5 on metrics/s4.json + metrics/s4_raw.json only (no embeddings needed).

Run:  python skeptic_synh1_raw.py "<D>"
"""

import json
import sys
from pathlib import Path

import numpy as np
from scipy.stats import wilcoxon

D = Path(sys.argv[1])
raw = json.loads((D / "metrics" / "s4_raw.json").read_text(encoding="utf-8"))
s4 = json.loads((D / "metrics" / "s4.json").read_text(encoding="utf-8"))

print(
    "== T1: is the clean-vs-arm AUROC driven by the base-sample SET (clean seeds 0-99 vs arms 100-199)?"
)
for c, arms in raw.items():
    keys = [k for k in arms if k != "clean"]
    clean = np.array(arms["clean"]["r"])
    arm_means = {k: float(np.mean(arms[k]["r"])) for k in keys}
    # all non-clean arms share the same 100 base samples -> their mean offset vs clean is common
    print(
        c,
        "clean mean",
        round(clean.mean(), 5),
        "| arm means range",
        round(min(arm_means.values()), 5),
        round(max(arm_means.values()), 5),
    )
    aucs = [s4["per_corpus"][c]["arms"][k]["auc"]["r"] for k in keys]
    print(
        "   r-AUROC over 16 arms: mean",
        round(float(np.mean(aucs)), 4),
        "share<0.5",
        round(float(np.mean(np.array(aucs) < 0.5)), 3),
    )

print("\n== T2: pairing value. Same seed => same base sample; at 0.5 % only 2 of 400 nodes differ.")
for c, arms in raw.items():
    for rate in ("0.005", "0.01", "0.05", "0.2"):
        a = np.array(arms[f"P_targeted@{rate}"]["r"])
        b = np.array(arms[f"B_growth@{rate}"]["r"])
        p = np.array(arms[f"P_bridge@{rate}"]["r"])
        q = np.array(arms[f"B_bridge@{rate}"]["r"])
        assert len(a) == len(b) == len(p) == len(q) == 100, "exclusions broke seed alignment"
        print(
            c,
            rate,
            "corr(Pt,Bg)=%.3f" % np.corrcoef(a, b)[0, 1],
            "corr(Pb,Bb)=%.3f" % np.corrcoef(p, q)[0, 1],
            "paired d(Pt-Bg)=%.4f p=%.3f" % ((a - b).mean(), wilcoxon(a - b).pvalue),
            "paired d(Pb-Bb)=%.4f p=%.3f" % ((p - q).mean(), wilcoxon(p - q).pvalue),
        )
    for kind in ("P_targeted", "P_bridge", "B_bridge", "B_growth"):
        lo = np.array(arms[f"{kind}@0.005"]["r"])
        hi = np.array(arms[f"{kind}@0.2"]["r"])
        print(
            "   ",
            c,
            kind,
            "paired r(20%%)-r(0.5%%) = %.4f  sd_diff=%.4f  corr=%.3f  p=%.3f"
            % (
                (hi - lo).mean(),
                (hi - lo).std(ddof=1),
                np.corrcoef(hi, lo)[0, 1],
                wilcoxon(hi - lo).pvalue,
            ),
        )

print("\n== T5: re-apply decision with C4 on B_growth (as written in claim.md) + strict reading")
for model, benign in (("P_targeted", "B_growth"), ("P_bridge", "B_bridge")):
    for c, res in s4["per_corpus"].items():
        rows = []
        for rate in ("0.005", "0.01", "0.05"):
            a = res["arms"][f"{model}@{rate}"]
            c2 = a["delta_auc"] >= 0.05 and a["delta_auc_vs_max_ci"][0] > 0
            c3 = a["auc_vs_matched_benign"]["auc"] - 0.5 >= 0.10
            c4_code = (
                a["tpr_or_fpr_at_clean_p95"] >= 0.5
                and res["arms"][f"{benign}@{rate}"]["tpr_or_fpr_at_clean_p95"] <= 0.15
            )
            c4_text = (
                a["tpr_or_fpr_at_clean_p95"] >= 0.5
                and res["arms"][f"B_growth@{rate}"]["tpr_or_fpr_at_clean_p95"] <= 0.15
            )
            rows.append((rate, c2, c3, c4_code, c4_text))
        print(
            model,
            c,
            rows,
            "lenient_all:",
            any(r[1] and r[2] and r[4] for r in rows),
            "strict_all:",
            all(r[1] and r[2] and r[4] for r in rows),
        )
