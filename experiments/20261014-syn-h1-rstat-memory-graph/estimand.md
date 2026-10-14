# estimand.md — 20261014-syn-h1-rstat-memory-graph
# Protocol: rules/estimand-ops.md · question_type = predictive (причинный слой не заполняется)

## L1 Attributes

**Population:** kNN-графы (k=10) памяти из N=400 текстовых чанков; три локальных корпуса (заметки Y-17, skills-md, vault); эмбеддер nomic-embed-text. Исключения: near-duplicates (cos>0.995 к уже взятому), графы с >5% вырожденных зазоров.

**Intervention:** вставка 0.5/1/5/20% «отравленных» чанков (P-targeted: копия чанка + шаблонная фраза; P-bridge: фрагменты трёх чанков из разных глобальных кластеров + та же фраза).

**Comparator:** (1) чистый граф; (2) benign-контроли той же структуры: B-bridge (то же без фразы), B-growth (новые настоящие чанки); (3) детекторы-бейзлайны на тех же графах: число компонент, λ₂, модулярность Louvain, средний cosine к центроиду.

**Endpoint:** graph-level AUROC классификации «отравлен / чист» по детектору ⟨r̃⟩ (bulk нормированного лапласиана, центральные 90%).

**Summary measure:** ΔAUC = AUROC(⟨r̃⟩) − max AUROC(бейзлайнов); 95% bootstrap-CI по графам (парный).

**MCID:** 0.05 AUROC-единиц (согласовано 2026-10-14).

**MDE-строка:** `n=100 графов/арм (оптимистично: подвыборки перекрываются); baseline AUROC≈0.75 (допущение); alpha=0.05 двусторонний; power=0.8; MDE≈0.10; MCID=0.05` → MDE > MCID: null не поддерживает утверждение об отсутствии эффекта размера MCID.

---

## Intercurrent Events (ICE)

| Event | Strategy | Rationale |
|-------|----------|-----------|
| Benign рост памяти (новые настоящие чанки, в т.ч. новые темы) | composite | Это легитимное изменение, дающее сдвиг структуры; отдельный контрольный арм B-growth, FPR на нём — часть критерия C4 |
| Benign «мосты» (обзорные заметки, структурно как яд) | composite | Отдельный арм B-bridge; различие яд-vs-benign — критерий C3 |
| Near-duplicates / вырожденный спектр | while-active | Dedup и исключение графа; счёт исключённых в отчёт; не импутация |

---

## Natural Language Statement

> "We estimate the difference in graph-level AUROC (⟨r̃⟩ detector minus the best of four structural baselines)
> for classifying poisoned vs clean memory graphs of N=400 text chunks, in three local text corpora,
> comparing the ⟨r̃⟩ detector vs {#components, λ₂, modularity, centroid-cosine} at poison rates 0.5/1/5/20 %,
> handling benign growth and benign bridging notes as separate composite-control arms, and duplicates/degenerate spectra by exclusion with counts."

---

## What This Result Does NOT Mean

1. Не доказывает защиту от реальных атак на RAG/память: яд здесь шаблонный, не оптимизированный под retriever.
2. Не устанавливает причинность «отравление → делокализация спектра» (вопрос предсказательный, mechanism=UNTESTED).
3. Не переносится на Hi-C/TAD и на плотные cosine-графы (там база GOE, см. пилот) и на N≪300.
4. Не обобщается за пределы трёх локальных корпусов: единица обобщения = корпус (n=3), подвыборки внутри корпуса не независимы.

---

## Sensitivity Analyses (≥2 для Full)

1. Альтернативные конструкции графа: kNN-5/20 и ε-порог (S3), unfolding cut 0/5/10% (S2).
2. Альтернативный эмбеддер (Qwen3-Embedding-0.6B) — на остаточное время, вне вердикта.
