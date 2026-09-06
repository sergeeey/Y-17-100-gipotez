# escape_route.md — 20260906-riemann-rstat-gue

_Filled BEFORE `run.py run` was executed. Data not yet downloaded at time of writing._

## Pre-Experiment Escape Route Map

| Possible Result | What it means | Immediate action |
|---|---|---|
| **In band** (|⟨r⟩ − 0.60266| < 0.01) AND both synthetic controls behave | Pipeline reproduces the known result | Verdict PROMOTE (as *replication*, not discovery). graph: `H-B1-1a → confirmed`, `H-B1-1b` stays `blocked`. Run skeptic (asymmetric). Record efficiency. |
| **In band** BUT positive control (synthetic GUE) off by > 0.01 | Data fine, generator broken — agreement is coincidental | Do NOT promote. Fix `synthetic_gue` (check Hermitian construction, bulk selection). Substrate issue, not claim evidence. |
| **In band** BUT negative control (Poisson) does NOT trigger KILLED | Kill criterion cannot fail → CRITERION_INVALID | STOP. The verdict is meaningless. Fix criterion/tolerance, re-run everything. |
| **Out of band, near 0.5359 (GOE)** | Either (a) pairing/implementation error that mimics β=1, or (b) genuinely GOE-like — impossible for ζ zeros | Check A5 (harness test) first. If harness passes → A4 (data file is not what we think). Never conclude "zeros are GOE". |
| **Out of band, near 0.386 (Poisson)** | Spacings uncorrelated → almost certainly parsing produced garbage (e.g. digits split, wrong column) | Inspect first 10 parsed values against the published first zeros (14.134725…, 21.022040…). A4 killed. |
| **Out of band, 0.5996 < ⟨r⟩ … no wait — in band but below surmise by ~0.003** | Expected: finite-N asymptotic value 0.5996 rather than surmise | Not a failure. Record as confirmation of the [MEMORY] numeric value; note in caveats. |
| **Slightly out of band, 0.58–0.5927** | Finite-height drift larger than assumed (A3) | Data-swap sensitivity decides: if last-50k is in band and first-50k is not → A3 killed for this height range only; verdict REPEAT with height ≥ 10⁵ zeros (zeros2 table). |
| **Download fails / count ≠ 100,000** | Infrastructure | Substrate Gate `BLOCKED-INFRASTRUCTURE`. Claim status unchanged. Retry or use cached file. |

## Null Result Pre-Analysis

Out-of-band result would kill, in order of prior probability:
- Primary: **A5** (implementation) or **A4** (data) — tooling, not science.
- Possibly: **A3** (finite-height drift) — only if both controls pass AND data-swap shows a height gradient.

Would NOT be killed under any outcome of this run:
- **A1** (ζ zeros are GUE) — a 100k-zero run cannot overturn Odlyzko's 10²⁰-height computations; a failure here is evidence about *this pipeline*.
- **A2** (r needs no unfolding) — a theorem-level property, tested here only as a sanity check.

## Cheapest Diagnostic Per Outcome

| Outcome | Diagnostic | Cost |
|---|---|---|
| Near GOE | run `pytest tests/test_rstat.py` (pairing test) | 1 s |
| Near Poisson | print first 10 parsed zeros, compare to 14.134725, 21.022040, 25.010858 | 1 s |
| Slightly low | data-swap halves already in `run.json` | 0 (already computed) |
| Controls fail | `python run.py controls --seed 1` (different seed) | 30 s |

## Anti-Overfitting Pre-Commitment

- [x] Minimal Relaxation Rule — one assumption per retry.
- [x] Kill condition pre-specified: |⟨r⟩ − 0.60266| ≥ 0.01 with both controls behaving → verdict REJECT **for the pipeline** (`H-B1-1a → killed`), and `H-B1-1b` gains a new blocker "pipeline unvalidated".
- [x] Stop condition: 2 consecutive out-of-band results after fixing A5 and A4 → archive, escalate to user (Tier 4).

## Unsafe Control Actions — STPA-lite

| Actor | Unsafe Action | Condition | Harm | Mitigation |
|-------|--------------|-----------|------|------------|
| `run.py` | writes `verdict: PASS` while a control failed | controls not re-checked in `run` | false PROMOTE | `run` re-reads `metrics/controls.json` and refuses PASS if any control is FAIL |
| orchestrator (me) | marks graph `confirmed` before skeptic ran | speed pressure | premature promotion | graph status `running` until decision.md has skeptic verdict |
| `requests.get` | silently returns HTML error page | 404 / redirect | garbage parsed as zeros | assert count == 100000 and first zero ≈ 14.134725 |

**Control loop:** `run.py` → `metrics/*.json` → me → `decision.md` → `registry/graph.yaml` → `LEDGER`.
Loss-of-control arrow: `me → graph.yaml` (only human-in-loop step) — mitigated by `lab_check.py` INV3 and the
rule "status changes in graph first, then markdown".

Abort conditions: none of the three template pre-commitments apply (no sensitive files, no non-experiment hooks expected, every number below will carry a tool call).
