# Caveats — 20260906-riemann-rstat-gue

_Sections "What This Result Does NOT Mean" and "Sensitivity Analysis Plan" written BEFORE the run.
Section "Post-run notes" appended AFTER, clearly marked._

## Post-run notes (2026-09-06, after metrics/run.json)

1. **The PASS is real but thin.** ⟨r⟩ = 0.61092 ± 0.00072; distance to the surmise +0.0083 vs tolerance
   0.01 → margin 0.0017. The claim as pre-registered holds. It would **not** hold with tolerance 0.005, nor
   with the empirical large-N GUE value (0.6006) as target (Δ = +0.0103 ≈ 10σ). Anyone quoting this as
   "zeros agree with GUE" must add "at the 0.01 level, at heights ≲ 7.5·10⁴".
2. **The excess is known physics, not a finding.** Novelty check (FL Step −3, same session): finite-size
   corrections to the gap-ratio distribution of ζ zeros are published — Forrester & Mays 2015
   (arXiv:1506.06531), Nishigaki, PTEP 2026 (arXiv:2507.10193): deviation ∝ (log(T/2π))⁻³, modelled by CUE
   at finite N_eff. Recorded in `pearl_registry` as **known-import**.
3. **The ceiling was mis-specified** (efficiency 1.038 > 1): asymptotic GUE is the privileged answer for
   N → ∞, not for the population actually measured. The correct ceiling for this population is the
   finite-N_eff CUE prediction. Methodology pearl (impact 6) filed.
4. **Assumption A3** ("finite-height drift < 0.01") survives only marginally — the drift *is* ≈ 0.01 at
   this height. Status: `weak_alive`. Not killed (the claim passed), not comfortably alive.
5. Single seed for synthetic controls; confidence MEDIUM, not HIGH, for that reason alone.



## What This Result Does NOT Mean

1. Does NOT prove anything new about ζ zeros — replication of Odlyzko (1987) / Atas et al. (2013).
2. Does NOT establish causality (descriptive).
3. Does NOT apply to chromatin, to other L-functions, or to zeros at height > 7.5·10⁴.
4. Is NOT valid if A4 (file identity) or A5 (pairing implementation) is broken — both are tested, but a
   PASS on synthetic controls with a broken *loader* is still possible; hence the first-zeros assertion.
5. Does NOT validate the methodology stack as a whole — only the FL steps actually exercised (see LEDGER).

## Interpretation Boundaries

| Condition | Value | Consequence if violated |
|---|---|---|
| Population | first 100,000 zeros, Odlyzko `zeros1` | other tables → re-run, do not extrapolate |
| Time window | data static (table published 2000s); run 2026-09-06 | n/a |
| System version | Python 3.13.2, numpy 2.3.4, requests 2.32.5 (`manifest.md`) | numeric drift implausible at 1e-3 level, but re-pin if changed |
| Data source | HTTPS from umn.edu, sha256 recorded | mirror with different precision → re-verify count + first zero |
| ICE handling | abort on s ≤ 0 | dropping instead would bias ⟨r⟩ downward |

## Hard Limitations

1. ⟨r⟩ alone cannot separate GUE from other β = 2 ensembles; it separates β = 0 / 1 / 2 only.
2. 100k zeros is a *low-height* sample by Odlyzko standards; agreement to 0.01 is expected, agreement to
   0.001 is not claimed.
3. The "ceiling" is a surmise (3×3), not the N→∞ value; the gap (~0.003) is inside MCID but nonzero.

## Assumptions Made

| Assumption | Testable? | Evidence | Risk if wrong |
|---|---|---|---|
| A1 ζ zeros ~ GUE | Y (this run) | Odlyzko 1987, Atas 2013 | none for this lab-control purpose |
| A2 r is unfolding-independent | Y (convention flip) | Oganesyan–Huse 2007 | small bias; sensitivity #2 detects |
| A3 finite-height drift < 0.01 | Y (data swap) | qualitative from Atas 2013 | slightly-low result misread as bug |
| A4 file identity | Y (count, monotone, first zero, sha256) | recorded in manifest | garbage in → garbage verdict |
| A5 pairing correct | Y (`tests/test_rstat.py`) | hand-computed 4-level case | GOE-like artefact |

## Unresolved Questions

- [ ] Exact convergence rate of ⟨r⟩ with height for ζ zeros — stress test 1 (first 1,000 zeros) probes, no threshold claimed.
- [ ] Whether shuffled-spacing ⟨r⟩ for ζ matches shuffled synthetic GUE (tests P(s) equality independent of correlations) — reported, not gated.

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| URL moved / down | low | med | cache file; sha256; fallback to `zeros1.gz` mirror listed on index page |
| Silent HTML-as-data | low | high | first-zero + count assertion |
| Off-by-one in pairing | low | high | unit test with known answer |

## What Would Invalidate This in Production

1. Any change to `r_stat()` that breaks `tests/test_rstat.py` — the verdict must be recomputed.
2. Replacing `zeros1` with a table of different precision without re-checking the first-zero assertion.

## Sensitivity Analysis Plan

| Check | What it tests | Expected direction if assumption violated |
|---|---|---|
| Data swap (halves) | A3 finite-height | first half lower than second |
| Convention flip (local unfolding) | A2 | |Δ| > 0.002 would mean r is density-sensitive — contradicting theory |
| Noise injection 10 % | robustness of repulsion signal | ⟨r⟩ falls toward 0.386; PASS iff stays > 0.5 |
| Alternative implementation | A5 | any difference > 1e-12 = bug |
