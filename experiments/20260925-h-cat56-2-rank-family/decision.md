# Decision: rank family r = 2..5 (2026-09-25)

**Verdict: PARTIALLY_SUPPORTED (Perelman vocabulary), NOT PROMOTE.** Breadth at F_p level for r = 2..5 (existence, not explicit instances), same lab and same code, own review only until the blind lemma review and an independent skeptic pass exist. An earlier draft of this line said "PROMOTE"; the independent reviewer (below) correctly called that overstated and it was relabelled. No change to H-CAT56-2 status, no change to U2/U3.

## What was run
`fp_certify.py d r s` unchanged, two primes, ten configurations (claim.md + addendum). Output: `check_predictions_output.txt`; raw JSONs in
`../20260919-pcc-generic-quasipure-cat56-2/metrics/fp_certify_d*_r*_s*.json`; closed-form scan: `closed_form_check.py/.json`; regression tests:
`tests/test_h_cat56_2_rank_family.py` (5 tests).

## Result against the pre-registration
| group | configs | outcome |
|---|---|---|
| firing (r = 2, 3 pre-existing; r = 4, 5 new) | (22,2,16) (23,3,12) (31,4,13) (41,5,14) | dim V-perp = 21, 22, 30, 40, all `< d`, integer equal to the registered formula, both primes |
| below crossing | (31,4,12) (41,5,13) (23,3,11) | 41, 61, 31, exact, none fires |
| above crossing | (31,4,14) (41,5,15) (23,3,13) | **all three registered predictions FAILED** (registered 31, 41, 23; got 30, 40, 22, QFIM singular). 7 of 10 registered predictions held, 3 of 10 failed; the failure is a pre-registration error (no admissible state exists there). The amended reading matched, but see "Reviewer pass" item 2: that match was forced, not a risky test |

## Skeptic Concerns / self-review (own, not yet an independent skeptic)
- **Kill criterion 2 fired on (31,4,14)** (value below the registered formula, "C-LB falsified or bug"). Debugged before continuing: float QFIM rank at s = 14 is 13, so the state is outside the class; C-LB's precondition fails; no falsification. Recorded in claim.md addendum with the timing (written before the other two above-crossing runs were read).
- **My pre-registration error**: "s above the crossing" controls do not exist as admissible states in the sequential tower (s* is the largest non-degenerate s). Stated, not hidden; the amendment is prospective for two of the three.
- **Same-lab, same-code breadth.** The r = 4, 5 rows use the code that produced r = 2, 3: it widens the claim, it does not add independence. A different-code check of one of them (as Path B was for r = 2) is the natural next step and has not been done.
- **Lifting lemma is unreviewed.** Result 2 in the note is `[INFERRED]` through it. The blind lemma-review packet is the route; not handed to anyone.

## Reviewer pass (independent `reviewer` agent, iteration 1 of 3, verdict NEEDS_WORK, severity P2, no numbers wrong)
Dispositions; each accepted finding was re-checked by me before acting.
1. "PROMOTE" overstated: **accepted**, relabelled to PARTIALLY_SUPPORTED above.
2. The amended above-crossing predictions are near-corollaries: **accepted and re-verified.** The last kernel dimension in the JSON is exactly `s - 1` in all three (13 < 14, 14 < 15, 12 < 13); a nonsingular QFIM is a positive-weighted Gram matrix of the `s` blocks, all of which lie in that kernel, so it needs `dim K_s >= s`. Singularity was forced, the clause "if a QFIM comes out nonsingular there, the reading is wrong" could not have fired, and `QFIM_NONSINGULAR` in `check_predictions.py` is a dead falsifier. What the match shows: bookkeeping consistent with a counting argument, not an independent test. The counting argument itself is the useful part and is now in the note as the reason `s*` is the maximum `[INFERRED]`.
3. Kill criterion 3 (integer mismatch) also fired on (31,4,14) and was not named: **accepted**, added to claim.md (second addendum). Plain count: 3 of 10 registered predictions failed.
4. The first half of claim.md cannot be proven to predate the runs from repository history (it was only staged, no earlier commit): **accepted as a limit.** It rests on my word; the addendum's timing is checkable from file mtimes. Rule for next time: commit claim.md before the first run.
5. `check_predictions.py` never read d, r, s or the primes, and the degenerate rows skipped the Lyapunov/PCC/kernel flags: **fixed** (label and prime assertions, flags checked for all kinds).
6. One test did not check what its docstring said, and `check_predictions.py` had no test: **fixed** (the LB test now compares against the saved F_p result; new tests feed mutated results and require failures).
7. "up to 232" imprecise: **fixed** ("k up to 220").
8. "seven registered configs" matched no set: **fixed** (7 of 10 held, 3 failed as registered).
9. "d = 22 is minimal within this test": **confirmed** by the reviewer with a wider s and k range.
10. Title reads like a priority claim: **softened**. External-source sentences (Nurdin, Yang-Imai-Pezze) were not checkable by the reviewer; they stay `[DOCS, read]` from my own direct reads.
11. Max entry 78: **verified by me** against `instance_d22_r2_s16.jsonl` (blocks key, max |entry| = 78); the reviewer could not open it.

## What this does NOT change
Novelty (U2) is unchanged and still `WEAK`; the email is sent and not to be resent; 463/21 not recomputed. `verification_strength` stays medium.

## Not done and why
- **Explicit Q(i) instance for r = 3**: the d = 22 search needed three pre-registered stages and hard-coded 22/2/16 in four scripts; a repeat is a multi-hour CPU bet for a modest gain (it would make the r = 3 row explicit rather than existential). Left as an optional pre-registered follow-up, not started.
- **SDP cross-check of non-saturation** (plan B): dropped. Nurdin's conditions for this block form reduce to the same null-space object as Observation 2 (Condition 1 trivial since L++ = 0, Condition 3 = PCC), so it is a reformulation, not an independent certificate.
- **Preprint**: `note_draft.md` is a local structure only; Submission Gate not run; not to be released before the U2 outcome.

## Next (all optional, none started)
1. Independent-code check (Path B style) of the r = 3 or r = 4 certificate.
2. Hand `lifting_lemma.md` to a blind reviewer (owner action).
3. When the authors reply: classify per outreach/PREREG_criteria.md.

## Full-suite check (pre-commit rule for 3+ files)
`python -m pytest tests/ -q --tb=short -x`: **338 passed in 2:04:27, 0 failed** (log: `full_pytest_log.txt`). The run collected 338 tests because
`tests/test_h_cat56_2_rank_family.py` was extended from 5 to 10 tests after it started; the extended file (10 tests) was run separately together with
`test_h_cat56_2_gates`, `test_lab_check`, `test_h_cat56_2_caps`: 29 passed. `ruff check` clean, `scripts/lab_check.py` OK, independent `reviewer` pass done (above).
Side effect recorded for ADR-125: the full run rewrote two unrelated tracked files (`experiments/20260908-chernoff-neuralode-nd-kreiss-crossimpl-smalleps/metrics/run.json`
and `...-kreiss-estimate-bias-check/metrics/run.json`); both were restored with `git checkout` before this commit and are NOT part of it.

## Addendum 2026-09-26: r = 6 (d = 54, s = 16)
Registered and committed BEFORE the run (`claim_r6.md`, commit f02dc51), prediction from the closed form, unchanged `fp_certify.py`, same two primes: **(54,6,16) fires with dim V-perp = 53 (< 54), (54,6,15) gives 73 (no fire), both on both primes, all flags true**,
kernel dims 576, 540, ..., 36 as counted; `check_predictions.py` reports OK for both. Runtimes 588 s and about 16 min for the two configs. Count of registered predictions across both claim files: 12, of which 9 held and 3 failed (the three ill-posed
above-crossing rows of the r = 2..5 batch, see claim.md addenda); the two r = 6 predictions both held. Same lab and same code: breadth, not independence; existence only (lifting lemma unreviewed); no independent-code check at d = 54 (too slow, said in advance).
Status unchanged (PARTIALLY_SUPPORTED); U2 and U3 unchanged.
