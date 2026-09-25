# Novelty audit, H-CAT56-2 (2026-09-20). Verdict: NOT FOUND in prior work, NOT CERTIFIED as new

Every reading here went through WebFetch's summarising model unless stated; `[WEAK]` throughout except the PDF pages I read directly.

| Source | What I checked | Finding |
|---|---|---|
| arXiv:2601.21801 (Yang, Imai, Pezze), PDF read directly | main text p. 4, End Matter, Supplemental S1 | States "for generic quasi-pure states, whether PCC is sufficient or not is still open, as conjectured in Ref. [38]". No counterexample. `[DOCS, read]` |
| arXiv:2405.00405 (Yang) | v4 definition, Eq. (12) | Defines quasi-pure states; the conjecture. Citation list unavailable: Semantic Scholar 0, INSPIRE query returned garbage (1607 unrelated hits) |
| arXiv:2602.12097 | full-text search for `quasi-pure` | absent; its counterexamples concern other rank-deficient classes |
| arXiv:2608.10490 | abstract | single-parameter Heisenberg-limit metrology, unrelated |
| arXiv:2609.18558, 2504.06812 | abstracts | semiclassical geometric tensor; no PCC / quasi-pure / counterexample |
| arXiv:2402.11567 v5 (Nurdin) | abstract + html summary | Says PCC is not sufficient for general mixed states, gives no explicit rank-deficient or quasi-pure example; v5 has a corrigendum on its Condition 2. Not read in full. **CORRECTED 2026-09-25, see addendum: the "PCC not sufficient" attribution was wrong; v5 now read pp. 5-13 directly.** |
| arXiv API queries | `"partial commutativity condition"` (3 hits: 2601.21801, 2402.11567, 2109.05807); `"quasi-pure" AND (PCC or Cramer-Rao)` (0 hits) | nothing new |

## Reading of the result

- Consistent with "open question, no published counterexample", but every negative here is a keyword search plus abstracts.
- What would change it: a full read of 2402.11567 and 2109.05807, the Ref. [38]/Yang 2405.00405 text around the conjecture, the two Semantic Scholar-unindexed
  citers of 2405.00405, and above all the authors' reply.
- One caveat on scope: Nurdin's general statement "PCC is not sufficient for general mixed states" is not in conflict, because the open question is specifically
  the generic quasi-pure class.

## Addendum 2026-09-25: Nurdin read directly (item 1 of the day-test in the Hypothesis Discovery run)

Direct PDF reads (page images, not a summariser): arXiv:2402.11567 v5 pp. 5-13 including the corrigendum, and arXiv:2405.01471 v1 pp. 1-13. `[DOCS, read]`.

| Source | Finding |
|---|---|
| 2402.11567 v5, p. 5 | "For general mixed density operators ... [the average commutativity] condition is no longer sufficient in the single copy case." That is the *average* condition, not PCC. PCC is stated as **necessary** (shown by Yang et al. 2019, Ref. [13]). No sufficiency claim, no counterexample for PCC. |
| 2402.11567 v5, pp. 6-8, 10-11 | Full necessary-and-sufficient characterisation: Condition 1 ([L++,L++]=0) and Condition 2' (corrected, pp. 10-11). Conditions 1+3 imply PCC (Condition 3 is the null-block part of eq. (10)). Conditions 1+4 sufficient. |
| 2402.11567 v5, Examples 1-4 (pp. 9, 12) | Qutrit rank-2 two-parameter state, plus fixed-subspace and V-isometry cases. **All are saturable cases** (conditions fulfilled). No PCC-holds-but-not-saturable example. |
| 2405.01471 v1 (withdrawn: Lemma 2 error), Examples 1 and 2 (pp. 7, 11) | Both read in full. Example 1 fixed support subspace, Example 2 the same qutrit. **Both saturable.** The withdrawal note says these two examples remain valid, so the withdrawn text contains no counterexample either. |

Corrections and consequences:

- **The earlier audit line "Nurdin says PCC is not sufficient for general mixed states" is withdrawn.** The primary text supports only "PCC necessary", and the average-commutativity insufficiency. The place where PCC insufficiency is asserted in general is 2601.21801's own Observation 2 (existence through dim V-perp < d), which the authors present alongside the open question for the generic quasi-pure class.
- **Prior-art status for the exact object:** no explicit PCC-satisfying non-saturable example found in Nurdin (any version read) or in the withdrawn text. Still a keyword-and-read search, not exhaustive. `[WEAK]` as before, but two prior "not read" entries are now closed.
- **Nurdin's characterisation is not an independent second certificate of our instance** `[INFERRED]`. With SLD blocks of the form [[0, A†],[A, 0]] the support block L++ is zero, so Condition 1 holds trivially and Condition 3 is PCC itself (already exact-verified). What remains, Condition 2' / the null-POVM feasibility with sum E_k00 = I, is the same null-space object that Observation 2's dim V-perp count bounds. Treat it as a reformulation of the same certificate, not a separate one. Actually solving that feasibility on the instance would be a real cross-check of Observation 2 and is recorded as an open, unbuilt step.
- **Still not read:** the LCSYS published versions (DOI 10.1109/LCSYS.2024.3382330 for 2402.11567; the "3451468" DOI from the withdrawal note is unresolved), Yang 2405.00405 text around Eq. (12), 2109.05807 beyond its abstract, and the authors' reply.

## Recommended next novelty step

Send the minimal reproducible package to the authors of 2601.21801 with the single question "is a PCC-satisfying, non-saturable generic quasi-pure example already known?". Needs an explicit go, as it leaves this machine.
