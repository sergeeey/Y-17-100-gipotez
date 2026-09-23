# H-CAT56-2 — checkpoint freeze (2026-09-22, evening)

L0: **descriptive** status freeze. Not a new experiment.

## Frozen status (canonical one-liner)

> **H-CAT56-2: exact counterexample package internally certified; portability passed via independent local reimplementation; theorem-chain read and consistent; novelty and external reproduction unresolved.**

## Three orthogonal claims — do not merge

| Claim | Status | Evidence |
|---|---|---|
| Math of this object (seed 701082) | **Closed strongly** | Exact PCC, nonsingular QFIM, dimV=463 / dimV⊥=21, max_abs=78; flip/singular controls |
| Portability | **Passed locally** | Path A `verify_exact_Q` + Path B from-scratch (`path_b_independent.py`); share only FORMAT.md + instance |
| Novelty / external scientific validity | **Open** | U2 author reply; U3 third-party human; prior-art risk remains primary |

Main residual risk is **not** “is 463 wrong?” — it is **misreading the theorem chain or prior art**.

## External break from own stack (ordered)

1. **Hand ZIP to a third party** with the brief in `THIRD_PARTY_BRIEF.md` (no expected 463/21).
2. After **24h cooling-off** — send authors email v2 (`SEND_CHECKLIST_channel_A.md`). Owner action required.
3. **No new internal experiments** until at least one external signal on U2 and/or U3.

## Artifacts

| Item | Path |
|---|---|
| Portable ZIP | `outreach/independent-repro-bundle-701082.zip` |
| Bundle + GATE_REPORT | `outreach/independent-repro-bundle-701082/` |
| Author draft (NOT SENT) | `outreach/2026-09-22-authors-email-DRAFT-v2.md` |
| Package inventory | `experiments/20260920-small-exact-qi-instance/PACKAGE_FREEZE_2026-09-22.md` |

## Explicit non-claims

- Not peer review.
- Local Path A≠B is stronger than a single-stack self-check, weaker than an independent human lab.
- Observation 2 / Ref.[29] consistency is a reading gate, not novelty.

## Addendum 2026-09-23 — outreach text frozen, cooling-off started

Email draft went through one more round: v3 got a context-blind skeptic pass (packet `2026-09-23-authors-email-DRAFT-v3-skeptic-packet.md`,
verdict SEND-WITH-EDITS, 7 required fixes: Eq.(16) hedge, local-implementation disclosure, a genuine positive control on the rank step via the
paper's own LMCC example, the full-22×22/484-dim ambient-space detail folded into question 1, the unitary-conjugation parametric-family sentence,
I/we cleanup, search-selection disclosure, softened subject line). v4 (`2026-09-23-authors-email-DRAFT-v4.md`) applies all required fixes.
`independent-repro-bundle-701082/FORMAT.md` also fixed (unnormalised `Tr ρ = 3` now flagged with an invariance note, `s`/size of `F` spelled out)
and the ZIP was rebuilt and re-verified byte-for-byte against the folder.

Split status:

```text
SCIENCE:                        READY FOR AUTHOR INQUIRY
NOVELTY (U2):                   UNRESOLVED
EXTERNAL HUMAN REPRODUCTION (U3): OPEN
EMAIL:                          READY, SUBJECT TO FINAL SUBMISSION GATE
```

No further text edits are planned. The 24h Submission Gate cooling-off is counted from this freeze commit, not from v2 or v3. No new internal
recomputation of 463/21 is planned or needed — the next decision-relevant evidence is external (author reply or third-party reproduction).

## Addendum 2026-09-23, 10:38 — email SENT

The owner sent the email (from sergeikuch80@gmail.com, To Jing Yang, Cc Imai/Pezzè), outside this session's tools. Exact text and a diff against
the frozen v4: `outreach/2026-09-23-authors-email-SENT.md`. All required skeptic fixes are present in the sent text, in places phrased more
precisely than v4. 30-day clock for U2 outcomes (novelty support / FAIL / silence, `PREREG_criteria.md`) starts today.

```text
SCIENCE:                          READY FOR AUTHOR INQUIRY (unchanged)
NOVELTY (U2):                     UNRESOLVED, awaiting reply (30-day clock started 2026-09-23)
EXTERNAL HUMAN REPRODUCTION (U3): OPEN
EMAIL:                            SENT — 2026-09-23, 10:38
```

Next internal action, if any: only in response to an actual reply, or per `THIRD_PARTY_BRIEF.md` for U3. No new recomputation, no resend.
