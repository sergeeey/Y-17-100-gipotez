# decision.md — 20260906-riemann-rstat-gue

**Graph node:** `H-B1-1a` · **Date:** 2026-09-06 · **Role:** positive control of the lab (known-answer replication)

## Verdict

- [x] **PROMOTE** — claim holds as pre-registered; **marker `[WEAKENED]`** (skeptic Step 8a) — scope narrowed, see below
- [ ] REPEAT
- [ ] REJECT
- [ ] ARCHIVE

**Promoted statement (narrowed):** *The r-statistic of the first 100,000 Odlyzko zeros (⟨r⟩ = 0.61092;
SE 0.0005–0.0009 depending on estimator) lies inside the pre-registered ±0.01 band around the GUE surmise
0.602658, with margin 0.0017. It does NOT agree with the matched-size empirical GUE control (0.60060) within
the same tolerance (Δ = +0.0103, z ≥ 10 under i.i.d., Bartlett and block-bootstrap SEs). The excess is the
known finite-height correction (∝ (log T/2π)⁻³; Forrester–Mays 2015, Nishigaki 2026), decreasing
monotonically with height. Treat as: pipeline VALIDATED; scientific replication MARGINAL-AS-EXPECTED at this
height.*

## Result Classification (diamond scan)

- [ ] 🥇 Gold
- [ ] 💎 Diamond
- [x] 🥈 **Silver** — three transferable methodology findings (below), none about the zeros themselves
- [x] 🪨 Stone — the *scientific* content is a replication of known results (by design)

| Инсайт | Куда применимо |
|--------|----------------|
| Step 4a ceiling must be stated *for the measured population*; `efficiency > 1` = CEILING_MISSPECIFIED, never "beat theory" | every FL Full experiment; pearl impact 6 |
| Novelty check (Step −3) killed a would-be discovery in one query — *before* it became a hypothesis | any "unexpected observation" in any project |
| State-reading tools → CAUGHT; keyword-reading hooks → NOISE (12/12 vs 9/9 this session) | tooling stack design; pearl |

## Evidence Summary

| Check | Result |
|-------|--------|
| Positive control (synthetic GUE) | PASS — 0.60060 ± 0.00073, in band |
| Discriminating control (GOE) | PASS — 0.53102, separated by 0.070 |
| Negative control (Poisson) | PASS — 0.38666, **kill criterion fired** |
| No-collapse (7) | 6 PASS + 1 REPORTED |
| Stress (3) | 2 PASS + 1 REPORTED (first 1,000 zeros: 0.617, out of band, expected direction) |
| Substrate gate | READY after fix #1 (document rounding) |
| Floor–ceiling | CRITERION_VALID, TASK_FEASIBLE; **efficiency 1.038 → CEILING_MISSPECIFIED** |
| Skeptic verdict | **WEAKENED** (context-asymmetric; agent had no execution tool — arithmetic on recorded numbers only, disclosed) |

## Skeptic Concerns and Resolution

| # | Concern (skeptic, verbatim gist) | Resolution |
|---|---|---|
| 1 | Identical kill rule applied to the run's own matched-size empirical GUE control (0.60060) instead of the literature surmise → 0.0103 ≥ 0.01 → **KILLED**. PASS depends on an unstated choice between two "what is GUE" references that differ by more than the tolerance. | **Accepted limitation → `[WEAKENED]`.** The pre-registered target was the surmise (claim.md § Constants, written before the run), so the PASS stands as worded — but the skeptic is right that the *scientific* reading must carry both references. Fix for follow-up (`H-B1-1c`): the primary reference becomes the finite-N_eff CUE prediction for *this* height, which is the correct ceiling; then the tolerance can shrink to ~0.002. |
| 1b | Reported SE assumes i.i.d. r_n; adjacent r_n share a spacing → SE understated, "10σ" overstated. | **Accepted → verified by `diag_se.py`** (`metrics/diag_se.json`): ρ₁ = 0.284 (direction confirmed); Bartlett(≤5) SE = 0.00086 (×1.44); block bootstrap SE = 0.00054 (spectral rigidity: negative lags 2–5 shrink block variance). z vs empirical GUE = 10.05 under both i.i.d. and block-bootstrap combined SEs. **Direction right, conclusion unchanged.** Honest residual: the two corrected estimators disagree by ×1.6; quote SE as a range. |
| 2 | All four height windows sit *above* the surmise and converge downward (0.617 → 0.6119 → 0.6109 → 0.6100), consuming 73–92 % of a "deliberately generous" tolerance; `escape_route.md` pre-registered only the *undershoot* case (→ 0.5996), not this overshoot. | **Accepted.** (a) Physics: known finite-height correction — novelty check found Forrester–Mays 2015 (arXiv:1506.06531) and Nishigaki PTEP 2026 (arXiv:2507.10193), so this is import, not anomaly (pearl: known-import). (b) Process: **Escape Point** below — the outcome map had a blind spot. |
| 3 | `efficiency = 1.038 > 1` computed and recorded but ungated; FL Step 4a table has no row for "observed beats ceiling"; anomaly silently absorbed into PASS. | **Mitigated.** `run.py` now emits `ceiling_check: CEILING_MISSPECIFIED` when efficiency ∉ [0, 1] (additive field, verdict logic untouched, r_mean bit-identical on re-run). Methodology pearl (impact 6) proposes adding "population the ceiling applies to" as a required Step 4a field. |

**Recomposition Gate:** the claim was not atomized; N/A.
**Paraphrase-Sensitivity Probe:** not run — cost discipline; this is a known-answer control, not a high-stakes promotion. Recorded as a conscious skip.

## Rationale

PROMOTE rather than REPEAT because every pre-registered element held and the pipeline demonstrably (a) reproduces
the known regime, (b) can fail (Poisson fired the kill), (c) discriminates β = 1 from β = 2. The lab's positive
control passed. `[WEAKENED]` rather than clean because the *scientific* margin is thin and reference-dependent,
which the skeptic correctly exposed and which the diagnostics confirm.

## Escape Point (where should this have been caught earlier?)

- **Should have been caught at:** `escape_route.md` (pre-registration) — the "in band but significantly *above*
  the empirical ceiling" outcome was missing; only "below" was mapped.
- **Why it wasn't:** I anchored on the surmise-vs-asymptotic gap (which points *down*) and did not ask "what
  if the population is not yet asymptotic?" — the same blind spot as the ceiling mis-specification.
- **Guard to add:** escape_route template — require one row per *sign* of deviation from each reference
  value, not per "kind" of result. Cheap; filed in the methodology pearl.

## Surgery Log

None — no component replaced. `ceiling_check` is an additive diagnostic field, not a replacement.

## Pearl Card Update

**Was the Prediction correct?** Yes — `mean_r` ∈ (0.5927, 0.6127) ✓; synthetic GUE in band ✓; Poisson fired kill ✓.
**Falsification condition triggered?** No.
**Unexpected:** overshoot direction; known physics; filed as known-import pearl + methodology pearl.

## Follow-ups created

| id | what | status |
|---|---|---|
| `H-B1-1c` (graph) | known-answer test #2: does the excess match Nishigaki's finite-N_eff CUE ⟨r⟩ at this height? Tolerance ~0.002. Requires pre-registering N_eff formula and the CUE finite-N value BEFORE computing. | `ready_to_scope` |
| pearl (methodology) | Step 4a: ceiling population field; escape_route: one row per sign | `pending`, next_check 2026-11-01 |
| pearl (known-import) | finite-height excess of ⟨r⟩ | `known-import`, next_check 2026-10-01 |
