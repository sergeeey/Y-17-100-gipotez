---
title: "Hypothesis Revival Targets — 9 классических гипотез для реанимации"
type: hypothesis-group
status: not_started
domain: Science-of-Science, Biology, Evolution, Virology, Cancer
created: 2026-05-10
updated: 2026-05-10
discovery_score: 8.5
confidence: 0.70
tags:
  - hypothesis-group
  - hypothesis-revival
  - sleeping-beauty
  - classic-science
---
maturity: fleeting

Целевые гипотезы для [[pipeline/inbox/Hypothesis Revival Engine — метасистема поиска похороненных гипотез]].

| # | Гипотеза | Год | Современный инструмент | Статус |
|---|---------|-----|----------------------|--------|
| R1 | Stability-Complexity Paradox (May) | 1972 | GNN на глобальных пищевых сетях | NOT STARTED |
| R2 | Epigenetic Landscape (Waddington) | 1957 | scRNA-seq + ML потенциал | NOT STARTED |
| R3 | Autocatalytic Sets / RAF (Kauffman) | 1971 | KEGG + LUCA метаболизм | NOT STARTED |
| R4 | Error Threshold / Quasispecies (Eigen) | 1971 | Deep sequencing + ML | NOT STARTED |
| R5 | Tissue Organization Field Theory (Soto/Sonnenschein) | 1999 | Spatial transcriptomics | NOT STARTED |
| R6 | Cancer Attractors (Kauffman) | 1971 | Gene network attractor analysis | NOT STARTED |
| R7 | Second Chargaff Rule | 1968 | AlphaGenome in silico | NOT STARTED |
| R8 | Ribosome Filter (Mauro/Edelman) | 2002 | Ribo-Seq databases | NOT STARTED |
| R9 | Metamorphic Proteins (Murzin) | 2008 | AlphaFold + MSA Subsampling | NOT STARTED |

## Kill criterion (общий для всех Revival targets)

Гипотеза не «воскрешается» если: (a) уже опровергнута публикациями 2015–2026, ИЛИ (b) новые инструменты не дают ΔAUC/ΔF1 ≥ 0.05 по сравнению с моделями на момент формулировки гипотезы.

## Быстрый MVP для Revival Engine

- R2 (Waddington): scRNA-seq данные публично доступны (GEO), ML реализация — 1–2 недели
- R7 (Chargaff): AlphaGenome API + in silico — 3–5 дней
- R9 (Murzin): AlphaFold2 + ESMFold on known metamorphic proteins — 1 неделя

## Связи

- [[pipeline/inbox/Hypothesis Revival Engine — метасистема поиска похороненных гипотез]]
- [[Hypothesis — Persistent Homology DNA Evolution]]
