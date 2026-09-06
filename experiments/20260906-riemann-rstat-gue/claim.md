# claim.md — 20260906-riemann-rstat-gue

**Graph node:** `H-B1-1a` · **Bridge:** `B1-RMT-RIEMANN-HIC` · **Tier:** Full (chosen for the *meta*-goal — exercise every FL step once — not for scientific difficulty)

> **Role of this experiment:** positive control of the LAB, not of the science. The answer is known
> (Montgomery–Odlyzko: zeta zeros follow GUE statistics). If the pipeline cannot reproduce it,
> the pipeline is broken — nothing about the Riemann zeros follows from a failure here.

## Zero-Signal Gate

| Field | Value |
|-------|-------|
| **Entity** | The sequence of imaginary parts of the first 100,000 nontrivial zeros of ζ(s) (Odlyzko table `zeros1`) |
| **Falsifiable predicate** | Its mean consecutive-spacing ratio ⟨r⟩ equals the GUE value, not the Poisson or GOE value |
| **Measurable outcome** | `python run.py run` → `metrics/run.json: r_mean`; PASS iff `abs(r_mean − 0.602658) < 0.01`; FAIL otherwise |

Gate: `(∃ entity) ∧ (∃ predicate) ∧ (∃ outcome)` — all three filled from the input alone. **PROCEED.**

## L0: Question Type

- [x] Descriptive — "what is ⟨r⟩ in population P (first 100k zeta zeros)?"
- [ ] Predictive
- [ ] Causal

No intervention, no counterfactual. `estimand.md` filled without the causal layer.

## Natural Language Statement (written before any data was downloaded)

> "We estimate the **mean ratio of consecutive level spacings ⟨r⟩** for the **first 100,000 nontrivial
> zeros of ζ(s)** (Odlyzko `zeros1`), comparing it to the **GUE Wigner-like surmise 0.602658** (Atas et al.
> 2013) with the **Poisson value 0.38629** as null model, handling the only intercurrent event
> (**a non-positive spacing, i.e. corrupted/duplicated zero**) by **aborting the run** (composite:
> corruption = pipeline failure, never imputed)."

## Constants and their provenance (Gate 1 / FL Step -4)

| Constant | Value | Provenance | Evidence |
|---|---|---|---|
| ⟨r⟩ Poisson | 2 ln 2 − 1 = 0.386294 | analytic; Atas et al. PRL 110, 084101 (2013), arXiv:1212.5611 | `[VERIFIED]` (web, 2026-09-06) |
| ⟨r⟩ GOE surmise (3×3) | 4 − 2√3 = 0.535898 | same | `[VERIFIED]` |
| ⟨r⟩ GUE surmise (3×3) | 2√3/π − 1/2 = 0.602658 | same | `[VERIFIED]` |
| ⟨r⟩ GOE large-N numeric | ≈ 0.5307 | same paper, numerics | `[MEMORY]` → measured by positive control below |
| ⟨r⟩ GUE large-N numeric | ≈ 0.5996 | same paper, numerics | `[MEMORY]` → measured by positive control below |
| Data | Odlyzko `zeros1`, 100,000 zeros, accuracy 3·10⁻⁹ | https://www-users.cse.umn.edu/~odlyzko/zeta_tables/zeros1 | `[VERIFIED]` (web) |

**Resolved ambiguity:** the project's original code targets **0.6027** = the 3×3 *surmise*, whereas the
N→∞ value is ≈0.5996. They differ by 0.003 < tolerance 0.01, so the kill criterion is unaffected — but
the target is now named explicitly: **primary target = surmise 0.602658**, and the run also reports the
distance to the empirical large-N GUE value produced by the positive control.

## Claim Entropy

| Component | Before design | After design (now) | After run |
|---|---|---|---|
| Unsupported HIGH claims | 1 (constants from memory) | 0 (surmise values web-verified; numerics demoted to "measured by control") | |
| Hidden assumptions | 2 (low-height zeros already GUE-like; r needs no unfolding) | 1 (low-height; unfolding-independence is a *property* of r, tested by convention flip) | |
| Missing negative controls | 1 | 0 (Poisson + GOE planned) | |
| Ambiguous definitions | 1 (0.6027 surmise vs 0.5996 asymptotic) | 0 (resolved above) | |
| Unresolved blockers | 0 | 0 | |
| **Total** | **5** | **1** | |

## Counterfactual Frame

| Question | Answer |
|---|---|
| What must change for H to be true? | Nothing — H is the established Montgomery–Odlyzko regime. The *interesting* counterfactual is the inverse: in what world does the run FAIL while the theory holds? → (a) parsing bug, (b) off-by-one in ratio pairing, (c) wrong target constant, (d) low-height finite-size drift exceeding 0.01 |
| How many independent changes required? | 0 for H; any ONE of (a)–(d) for a failure |
| Known system where these conditions already hold? | Yes — Atas et al. 2013 §"zeros of the Riemann zeta function" report exactly this agreement |

**Verdict:** `within-framework`. A PASS here is a replication, not a discovery.

## Falsifiable Claim

**Claim:** For Odlyzko `zeros1`, `abs(mean_r − 0.602658) < 0.01`.
**Check:** `python experiments/20260906-riemann-rstat-gue/run.py run` → reads `metrics/run.json["verdict"]`.

## HD-MAVP Decomposition

| # | Assumption | Type | Role | Depends On | Evidence | Status |
|---|---|---|---|---|---|---|
| A1 | ζ zeros in the bulk follow GUE spacing statistics (Montgomery–Odlyzko) | mathematical/empirical | core | — | Odlyzko 1987; Atas 2013 | alive |
| A2 | ⟨r⟩ is invariant to local density (no unfolding needed) | mathematical | core | — | Oganesyan–Huse 2007; Atas 2013 abstract | alive |
| A3 | Finite-height drift over the first 100k zeros stays below 0.01 in ⟨r⟩ | empirical | protective_belt | A1 | Atas 2013 example (qualitative) | unknown → tested by data-swap (first vs last 50k) |
| A4 | The downloaded file is the file described (100,000 monotone zeros, 3·10⁻⁹) | measurement | protective_belt | — | count + monotonicity + sha256 recorded | unknown → tested at load |
| A5 | The r-pairing `(s_n, s_{n+1})` is implemented without off-by-one | tooling | hidden | — | unit test on a hand-computed 4-level array | unknown → `tests/test_rstat.py` |

**Principal Assumption (cut vertex):** A1 — but it is the *known* truth here. For a lab positive control the
assumption to attack first is **A5** (tooling), because it is the only one whose failure would be
indistinguishable from a scientific failure without the harness test.

### Constraints
- Applies only to the r-statistic (ratio of consecutive spacings); says nothing about the nearest-neighbour
  spacing distribution P(s), number variance, or form factor.
- Applies to the first 100,000 zeros only (heights ≲ 7.5·10⁴).

### Unknowns
- [U] Exact finite-N GUE ⟨r⟩ at N→∞ (the 0.5996 figure) — measured, not assumed.
- [W] How fast the first ~1000 zeros converge to GUE (stress test 1 probes this, no pass threshold claimed).

### Dependencies
- Odlyzko table reachable over HTTPS at run time (cached to `data/zeros1.txt` afterwards).

## Pearl Card

**Prediction:** `mean_r` ∈ (0.5927, 0.6127); positive control (synthetic GUE) lands in the same band;
negative control (Poisson) lands near 0.386 and the kill criterion **fires** on it.
**Falsification:** `mean_r` outside the band while both synthetic controls behave → A3 or A4 is wrong
(finite-height drift or corrupted data), NOT A1.

## What This Does NOT Mean

1. Does NOT prove anything new about the Riemann zeros — it is a replication of a 1987 observation.
2. Does NOT establish that Hi-C chromatin spectra are GUE (that is `H-B1-1b`, currently `blocked`).
3. Does NOT establish causality (descriptive question).
4. Does NOT resolve `Q-GOE-vs-GUE` for chromatin — it only confirms the *metric* separates GOE from GUE
   (Δ⟨r⟩ ≈ 0.07 ≫ tolerance), which is a precondition for that question, not its answer.
5. Does NOT validate the *whole* methodology stack — only the steps it exercises (listed in LEDGER).

## MCID

MCID = **0.01** in ⟨r⟩ (≈ 5 % of the Poisson–GUE interval 0.216; ≈ 12 standard errors at N = 10⁵ given
sd(r) ≈ 0.25). Chosen to match the project's pre-existing kill criterion; deliberately generous because a
positive control should fail only on real breakage.
