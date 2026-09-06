---
title: "Open Problems Catalog — Skeptic Assessment (100-item version)"
type: analysis
status: active
domain: Meta-Research, Research Scouting, Validation Theater
created: 2026-09-06
source: "100_open_scientific_problems_verified_2026-09-06.md (external, likely ChatGPT/o-series)"
related:
  - "[[Open Problems Catalog — Phase 1 (44 of 100, 2026-09-06)]]"
  - "[[100 Open Problems — raw catalog (source, 2026-09-06)]]"
  - "[[raw/lesson-text-figures-consistency-check]]"
tags:
  - analysis
  - validation-theater
  - open-problems
  - skeptic-review
  - meta-research
---

# Skeptic Assessment: the 100-item Open Problems catalog

> Applying the same discipline used all session on ARCHCODE manuscript v2 (text↔figures mismatch) to this new artifact. Same principle: **structural validity ≠ per-item depth.**

---

## Verdict: real primary sources, templated reasoning — not hallucination, but shallow

### ✅ What's genuinely solid

1. **27 real, citable primary sources** — checked several by pattern: COLT 2024/2025 Open Problems (PMLR 247/291), Dagstuhl Reports 15(1) 2025 (DOI given), RIMS Kyoto topology problems list, Bandeira's "Randomstrasse101" arXiv:2603.29571, npj Systems Biology 11:101 (2025), Nature Biotechnology 43 (2025, single-cell benchmarks), ACS Nano 18 (2024), PRX Quantum 3:010101 (2022, Horodecki's "Five Open Problems"). These are the kind of documents that genuinely DO publish curated open-problem lists — this is a legitimate harvesting strategy, not fabrication.
2. **Two explicit, correctly-reasoned exclusions**: a COLT-2025 problem solved at COLT-2026, and a Werner-state problem from PRX Quantum solved July 2026. This is exactly the "verify current status, don't trust old open-problem claims" discipline the prompt demanded — real evidence the author actually checked something, not just copy-pasted a static list.
3. **"First Research Experiment" field varies genuinely per problem** — spot-checked 3 consecutive COLT entries, each proposes a distinct, plausible computational starting point (enumerate small multiclass classes / compare privatized bandit algorithms / solve minimax testing games for small alphabets). This field has real content.
4. **Domain coverage is near-fully complementary to my own Phase 1 catalog** (see below) — almost zero overlap in specific problems, which is a good sign against copy-generation from the same seed list.
5. **Honest closing caveat**: "absence of a found solution ≠ proof of non-resolution; re-verify before serious commitment" — correct epistemic hedge, not overclaiming.

### 🔴 What's validation theater (verified pattern, not suspicion)

1. **Identical boilerplate paragraphs across problem clusters.** The exact sentence *"Главный барьер обычно в разрыве между worst-case lower bounds и конструктивными алгоритмами; локально хорошие эвристики не дают tight общей гарантии"* appears **13 times verbatim** (grep-confirmed) across all 9 COLT-2024-sourced problems and more. Same pattern for "Why This Problem Matters" and "Interdisciplinary Bridge" — each source-cluster (e.g. the 9 COLT24 problems, the 6 Dagstuhl graph problems, the 6 RIMS topology problems, the 12 Amsel-et-al numerical linear algebra problems) shares **one templated explanation**, with only the problem title substituted in.
2. **This means the "Why still open" / "Why it matters" / "Bridge" content is generic per-SOURCE, not per-PROBLEM.** It tells you the source document exists and lists problems — it does NOT give problem-specific reasoning. A reader cannot distinguish, from this text alone, why problem #1 specifically is hard vs. problem #2.
3. **Scores are compressed into a narrow high band (7-10 nearly everywhere)**, with no problem scoring below 6 in the samples checked. This is the same "round numbers / suspiciously narrow high range" pattern flagged by `skeptic-triggers.md` Trigger 1/4 — not literally round numbers, but a compressed, non-discriminating range that doesn't function as a real filter. A scoring system where everything is "8-10" isn't ranking, it's decoration.
4. **The rankings (Top-20/Top-20/Top-20/Top-10) are therefore built substantially on these compressed, non-discriminating scores** — the composite numbers (8.71, 8.68, 8.46...) look precise but are downstream of templated inputs. Precision theater: three decimal digits computed from a 7-10 qualitative scale.

### What this means practically

**Use this catalog as:**
- ✅ A real, citable **index of 100 problem names + primary sources** — genuinely useful for discovering that e.g. Dagstuhl Report 15(1) 2025 has 6 named open graph-algorithm problems, or that npj Sys Bio 2025 has 5 open UDE-identifiability problems you didn't know existed.
- ✅ A **starting point for YOUR OWN deep dive** into any single problem — go read the actual cited source, not the templated summary.

**Do NOT use this catalog as:**
- ❌ Evidence that problem-specific analysis was actually done for each of the 100 entries
- ❌ A reliable ranking (composite scores are precision theater over compressed inputs)
- ❌ A substitute for reading the primary source before committing research time to any specific problem

---

## Cross-reference: complementarity with my Phase 1 catalog (43 items)

| | My Phase 1 (43 items) | This 100-item catalog |
|---|---|---|
| Depth per problem | High — live-searched status, distinct reasoning, real "why open" per problem | Shallow — templated reasoning per source-cluster |
| Breadth | 4 domain clusters (math, physics, CS, bio/chem/geo) | 27 source documents across ~15 sub-fields incl. quantum info, topology, finite groups, numerical linear algebra, UDE/systems bio, single-cell benchmarking, ecology, synthetic bio, neuroscience theory |
| Overlap | — | **Near zero** — spot-checked, no shared specific problems (mine: Erdős-Straus, KPZ, matrix mult exponent, etc.; this one: COLT learning-theory problems, RIMS topology, MUB/SIC quantum info, UDE identifiability) |
| Verified exclusions | 3 (Kakeya 3D, Moving Sofa, Casas-Alvero) | 2 (COLT noisy-query, Werner-state) |
| Combined unique total | **~141 problems** (43 + 100, minus MBL/B2≡D3 dedup already noted in mine) | |

**Recommendation:** treat the two catalogs as complementary layers of the same Phase-1 effort — mine for depth on 43, this one as a breadth index pointing to 27 real source documents worth mining individually if a specific sub-field becomes relevant.

---

## Actionable

1. If picking a problem to actually pursue from the 100-item list: **re-read the actual cited primary source first** (e.g., go to the actual COLT 2024 Open Problems session paper, not the templated summary here) — the templated text will not tell you anything the title doesn't already say.
2. Do not cite this catalog's numeric scores externally — they are a within-batch heuristic sort, not a calibrated instrument.
3. The 2 self-reported exclusions (COLT noisy-query, Werner-state) are worth spot-verifying if this catalog is ever used for an external-facing claim (Submission Gate applies).

---

*Assessment: 2026-09-06. Same skeptic discipline as ARCHCODE manuscript v2 review — structural soundness checked before accepting per-item claims at face value.*
