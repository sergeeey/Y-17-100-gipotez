# Novelty audit, H-CAT56-2 (2026-09-20). Verdict: NOT FOUND in prior work, NOT CERTIFIED as new

Every reading here went through WebFetch's summarising model unless stated; `[WEAK]` throughout except the PDF pages I read directly.

| Source | What I checked | Finding |
|---|---|---|
| arXiv:2601.21801 (Yang, Imai, Pezze), PDF read directly | main text p. 4, End Matter, Supplemental S1 | States "for generic quasi-pure states, whether PCC is sufficient or not is still open, as conjectured in Ref. [38]". No counterexample. `[DOCS, read]` |
| arXiv:2405.00405 (Yang) | v4 definition, Eq. (12) | Defines quasi-pure states; the conjecture. Citation list unavailable: Semantic Scholar 0, INSPIRE query returned garbage (1607 unrelated hits) |
| arXiv:2602.12097 | full-text search for `quasi-pure` | absent; its counterexamples concern other rank-deficient classes |
| arXiv:2608.10490 | abstract | single-parameter Heisenberg-limit metrology, unrelated |
| arXiv:2609.18558, 2504.06812 | abstracts | semiclassical geometric tensor; no PCC / quasi-pure / counterexample |
| arXiv:2402.11567 v5 (Nurdin) | abstract + html summary | Says PCC is not sufficient for general mixed states, gives no explicit rank-deficient or quasi-pure example; v5 has a corrigendum on its Condition 2. Not read in full |
| arXiv API queries | `"partial commutativity condition"` (3 hits: 2601.21801, 2402.11567, 2109.05807); `"quasi-pure" AND (PCC or Cramer-Rao)` (0 hits) | nothing new |

## Reading of the result

- Consistent with "open question, no published counterexample", but every negative here is a keyword search plus abstracts.
- What would change it: a full read of 2402.11567 and 2109.05807, the Ref. [38]/Yang 2405.00405 text around the conjecture, the two Semantic Scholar-unindexed
  citers of 2405.00405, and above all the authors' reply.
- One caveat on scope: Nurdin's general statement "PCC is not sufficient for general mixed states" is not in conflict, because the open question is specifically
  the generic quasi-pure class.

## Recommended next novelty step

Send the minimal reproducible package to the authors of 2601.21801 with the single question "is a PCC-satisfying, non-saturable generic quasi-pure example already known?". Needs an explicit go, as it leaves this machine.
