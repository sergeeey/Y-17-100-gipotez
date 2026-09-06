# substrate_gate.md — 20260906-riemann-rstat-gue

_Step 2a. Resolved BEFORE controls ran. First pass was NOT READY (see fix log)._

## Checklist

| Check | What it verifies | Result | Notes |
|---|---|---|---|
| Environment | Versions/platform pinned | [x] PASS | Python 3.13.2, numpy 2.3.4, requests 2.32.5, PyYAML 6.0.3 (`pip show`, 2026-09-06); Windows 11 |
| Code provenance | Source of every function/constant known | [x] PASS | r-statistic: Oganesyan–Huse 2007 / Atas et al. 2013; surmise constants derived from closed forms in code, not typed in; data URL + sha256 recorded in run.json |
| Dependencies | Pinning exists | [x] PASS | `requirements.txt` (floors) + exact versions in `manifest.md` |
| Exactness | Verdict not hinging on float rounding | [x] PASS | tolerance 0.01 vs data precision 3e-9 and SE 7e-4; scale test agrees to 1e-13 |
| Test-harness sanity | Harness has its own smoke test | [x] PASS | `tests/test_rstat.py`: hand-computed pairing (0.5, 1/3), pure-Python parity, scale invariance, duplicate abort, constants — 5 tests, all pass after fix #1 |
| Artifacts | Output persisted | [x] PASS | `metrics/controls.json`, `run.json`, `stress.json` |
| Security/integrity | Hooks don't distort the run | [x] PASS | Permission guard blocked `python -c` once (version print) — worked around with `pip show`; no hook touched the experiment files. Formatter hook rewrote `run.py` layout only (no semantic change; harness re-passed) |
| Clean state | Uncommitted scope known | [x] PASS | Uncommitted at gate time: `.gitignore`, `registry/graph.yaml` (experiment_dir), this experiment dir, `tests/test_rstat.py` — all in-scope |

## Verdict

- [x] `READY` — proceeded to Step 3 (after fix #1)
- [ ] `BLOCKED-INFRASTRUCTURE`
- [ ] `UNTRUSTED-ENVIRONMENT`

## Fix log

| Attempt | Problem found | Fix applied | Re-run result |
|---|---|---|---|
| 1 | `test_constants_match_surmise_formulas` FAILED: documents quoted GUE surmise as 0.60266 (literature rounding), code computes exact 2√3/π − ½ = 0.6026578; test tolerance 1e-6 too tight for a 5-digit literature value | Corrected documents (claim/experiment/estimand) to 0.602658; test tolerance → 5e-6 with WHY comment. **Constant itself was never wrong** — the ambiguity was in the prose. | 8/8 tests pass |
| 1b | ruff: 4 E501 (docstrings), 2 RUF007 (`zip`→`pairwise`), 1 RUF003 (`×`), 1 I001 (import order) | fixed; `ruff check --fix && ruff format` now runs *inside* the chain before tests | clean |

**Lesson for the harness (not the claim):** a Substrate Gate that catches a documentation-vs-code
discrepancy before the run is doing its job — that discrepancy would otherwise have surfaced as a
"why is the target 0.60266 here and 0.6027 there" question in the skeptic pass.
