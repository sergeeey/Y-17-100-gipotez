"""Addendum A3: re-embed the frozen Syn-H1 text pools with a SECOND embedder, Qwen3-Embedding-0.6B.

Inputs (never committed; they hold private vault text): SYNH1_CACHE = the nomic cache written by
`run.py prep`, containing {C1,C2,C3}_texts.json and {C1,C2,C3}.npz (base/held/labels).
Output: SYNH1_QWEN_CACHE/{C}.npz with the SAME base/held/labels and Qwen embeddings of the SAME
pool texts and poison texts. Everything else (dedup, K-means labels, samples) is inherited from the
nomic cache on purpose: the only thing that changes between the two runs is the embedder.

Frozen choices (see claim.md, Addendum A3): last-token pooling, L2 normalisation, documents without
an instruction prefix, max 512 tokens, the tokenizer's own special tokens (it appends
<|endoftext|>), fp32 on CPU, batch 8, length-sorted batches with exact restoration of order.
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path

import numpy as np
import torch
from transformers import AutoModel, AutoTokenizer

MODEL = "Qwen/Qwen3-Embedding-0.6B"
MAXLEN = 512
BATCH = 8
CORPORA = ("C1", "C2", "C3")
POISON_KEYS = ("P_targeted", "P_bridge", "B_bridge")


def embed(model, tok, texts: list[str]) -> np.ndarray:
    order = np.argsort([len(t) for t in texts], kind="stable")
    out = np.zeros((len(texts), model.config.hidden_size), dtype=np.float32)
    with torch.inference_mode():
        for i in range(0, len(texts), BATCH):
            idx = order[i : i + BATCH]
            batch = tok(
                [texts[j] for j in idx],
                padding=True,
                truncation=True,
                max_length=MAXLEN,
                return_tensors="pt",
            )
            last = model(**batch).last_hidden_state[:, -1]  # left padding: final real token
            out[idx] = torch.nn.functional.normalize(last, p=2, dim=1).numpy()
    return out


def main() -> None:
    src = Path(os.environ["SYNH1_CACHE"])
    dst = Path(os.environ["SYNH1_QWEN_CACHE"])
    dst.mkdir(parents=True, exist_ok=True)
    tok = AutoTokenizer.from_pretrained(MODEL, padding_side="left")
    model = AutoModel.from_pretrained(MODEL, dtype=torch.float32).eval()
    torch.set_num_threads(os.cpu_count() or 4)
    log = {"model": MODEL, "maxlen": MAXLEN, "batch": BATCH, "corpora": {}}
    for c in CORPORA:
        t0 = time.time()
        texts = json.loads((src / f"{c}_texts.json").read_text(encoding="utf-8"))
        z = np.load(src / f"{c}.npz")
        X = embed(model, tok, texts["pool"])
        arrays = {"X": X, "base": z["base"], "held": z["held"], "labels": z["labels"]}
        for k in POISON_KEYS:
            arrays[f"E_{k}"] = embed(model, tok, texts["poison"][k])
        np.savez_compressed(dst / f"{c}.npz", **arrays)
        # sanity: related pair vs unrelated pair cosine, recorded (not used for any decision)
        cos = X[:50] @ X[:50].T
        log["corpora"][c] = {
            "n_pool": int(len(X)),
            "n_poison": {k: int(len(texts["poison"][k])) for k in POISON_KEYS},
            "mean_offdiag_cos_50": float((cos.sum() - np.trace(cos)) / (50 * 49)),
            "elapsed_s": round(time.time() - t0, 1),
        }
        print(c, log["corpora"][c], flush=True)
    (dst / "embed_log.json").write_text(json.dumps(log, indent=2), encoding="utf-8")
    print("QWEN DONE", flush=True)


if __name__ == "__main__":
    main()
