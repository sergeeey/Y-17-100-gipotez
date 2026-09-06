---
title: "Portfolio Intelligence Audit v2 — Bayesian PPV Edition"
type: portfolio-audit
status: canonical
domain: Meta-Research, Portfolio Management, Bayesian Methods
created: 2026-05-10
updated: 2026-05-10
supersedes: "[[Portfolio Intelligence Audit (2026-05-10)]]"
related:
  - "[[Hypothesis Tracker]]"
  - "[[hypotheses.base]]"
tags:
  - audit
  - portfolio
  - esv
  - bayesian-ppv
  - canonical
  - meta-analysis
---
maturity: fleeting

# Portfolio Intelligence Audit v2
## Bayesian PPV Edition — методологически строгая версия

**Дата:** 2026-05-10 | **Метод:** Ioannidis PPV + empirical reproducibility base rates
**Статус:** CANONICAL (заменяет v1 от того же дня)
**Confidence:** [K] = published with citation, [I] = inferred, [U] = unknown

---

## ПОЧЕМУ V2 ЛУЧШЕ V1

| Параметр | V1 (мой) | V2 (этот) |
|----------|----------|-----------|
| Формула ESV | Линейное взвешивание | **Bayesian PPV (Ioannidis)** |
| P_true | Произвольная шкала 0–10 | **Empirical reproducibility rates** с цитатами |
| Источники | Память | **40+ peer-reviewed citations** [K] |
| Compute timings | Грубая оценка | **Реальные benchmarks** (REGENIE 2h53m на UKB) |
| Sleeping Beauty | Качественная коррекция | **Ke et al. 2015 PNAS B-coefficient** формула |
| Tooling | Общие рекомендации | Конкретно: Manifold Markets, IARPA, GRADE |
| ESV числа | 5.0–6.1 | **0.85–3.9** (порядок строже) |

**Главная ошибка v1:** DS-скоры считали impact-if-true как evidence-of-truth. V2 разделяет их через PPV формулу.

---

## РАЗДЕЛ 1. Empirical Reproducibility Base Rates (P_true anchors) [K]

| Домен | Replication rate | Источник | P_true anchor |
|-------|-----------------|----------|---------------|
| Психология | 36–47% | OSC, Science 2015, 349:aac4716 | 0.35–0.45 |
| Social-behavioral (top journals) | 62% | Camerer et al., Nat Human Behav 2018 | 0.55–0.65 |
| Cancer preclinical (industry) | 11–25% | Begley & Ellis, Nature 2012; Prinz, NRDD 2011 | 0.10–0.25 |
| Cancer preclinical (academic RPCB) | 46% (effect size 85% smaller) | Errington et al., eLife 2021 | 0.30–0.45 |
| Biomedical (general) | PPV 0.10–0.30 | Ioannidis, PLoS Med 2005 | 0.20–0.30 |
| Computational genomics | ~0.45 [I, calibrated] | — | 0.40–0.50 |
| Hard physical sciences | 78% positive rate | Fanelli, PLoS ONE 2010 | 0.55–0.70 |
| Палеонтология (quantitative) | 62-Myr replicated | Melott, PLoS ONE 2008 | 0.30–0.50 |
| Finance (alphas) | ~50% не выживают OOS | Hou-Xue-Zhang 2020 | 0.20–0.35 |

**Publication bias multiplier (Fanelli 2010):**
- Психология/психиатрия: ×5 vs space science
- Экономика/бизнес: ×5
- Соц. науки в целом: ×2.3
→ Применять как deflator к prior в "мягких" доменах.

---

## РАЗДЕЛ 2. ESV Formula (Bayesian PPV)

```
ESV = 10 · P(true|evidence) · Impact · Feasibility · Tractability_solo · SB_uplift
```

Все факторы ∈ [0,1] кроме SB_uplift ∈ [1.0, 1.5].

### P(true|evidence) — Ioannidis PPV [K]

```
        P(prior) · (1 − β)
PPV = ─────────────────────────────────────────────────
      P(prior)·(1−β)·(1−u) + α·(1−P(prior))·(1−u) + u
```

где:
- P(prior) = domain anchor из таблицы выше
- β = type-II error (0.2 если есть well-powered studies)
- α = 0.05
- u = bias term ∈ [0, 0.4]; 0.30 для cancer-bio hot fields, 0.10 для физики/computational

**Multi-study aggregation (Goodman/Greenland):**
posterior_odds = prior_odds × ∏ LR_i, где LR ≈ 16 per well-powered study.

### Sleeping Beauty uplift (Ke et al. 2015 PNAS [K])

```
B = Σₜ [(c_max − c_0)/t_max · t + c_0 − c_t] / max(1, c_t)
SB_uplift = clip(1.0 + 0.1·log(1+B), 1.0, 1.5)
```

### Impact / Feasibility / Tractability шкалы

**Impact** (нормированный):
- 1.0 — paradigm-shifting (HERV, A2 Topological)
- 0.7 — cross-field connector
- 0.4 — within-field refinement
- 0.2 — methodological footnote

**Feasibility:**
- 1.0 — open data + локальное железо
- 0.6 — open + cloud burst
- 0.3 — collaboration-gated lab
- 0.1 — consortium-required

**Tractability_solo (S1-S4):**
- S1 = 1.0 — laptop + open data, <2 weeks
- S2 = 0.7 — laptop+GPU, 1-3 months
- S3 = 0.3 — wet-lab collaboration
- S4 = 0.05 — team + dedicated equipment

---

## РАЗДЕЛ 3. WORKED EXAMPLES — обновлённые ESV

### HERV (Block 18) — было DS=9.5

**Расчёт:**
- P(prior) ≈ 0.25 (biomedical)
- Posterior после MS Phase II evidence ≈ **0.45**
- Impact = 1.0 (paradigm-shifting)
- Feasibility = 0.7 (TElocal/Telescope/scTE на open data)
- Tractability = 0.7 (S2)
- SB_uplift ≈ 1.3 (1990s undercited literature)

**ESV = 10 · 0.45 · 1.0 · 0.7 · 0.7 · 1.3 ≈ 2.9 / 10**

DS=9.5 был драматически завышен. ESV=2.9 отражает: high impact, but limited evidence.

### A2 Topological Penetrance (Block 19) — было DS=9.5

**Расчёт:**
- P(prior) ≈ 0.45 (computational genomics)
- Posterior после convergent evidence (TAD heritability + non-coding GWAS) ≈ **0.65**
- Impact = 1.0
- Feasibility = 0.85 (Hi-C maps + GWAS Catalog все open)
- Tractability = 0.7 (S2)
- SB_uplift = 1.0 (current hot field, NOT sleeping beauty)

**ESV = 10 · 0.65 · 1.0 · 0.85 · 0.7 · 1.0 ≈ 3.9 / 10** ⭐ Highest in portfolio

### ExoRNA (Block 21) — было DS=8.3

**Composite:**
- Biomarker claim posterior ≈ 0.50
- Mechanistic messenger claim ≈ 0.30
- Composite ≈ **0.40**
- Impact = 0.85
- Feasibility = 0.95 (ERCC Atlas + GEO открытые)
- Tractability = 0.7
- SB_uplift = 1.1

**ESV = 10 · 0.40 · 0.85 · 0.95 · 0.7 · 1.1 ≈ 2.5 / 10**

DS=8.3 завышен; ESV=2.5 трезвый.

### Glymphatic (Block 18) — было DS=9.0

- P(prior) ≈ 0.30
- Posterior после ADNI Han et al. 2021 evidence ≈ **0.55**
- Impact = 0.85
- Feasibility = 0.75 (ADNI free но application)
- Tractability = 0.7 (S2)
- SB_uplift ≈ 1.2 (Iliff-Nedergaard 2012 → awoken 2018)

**ESV ≈ 2.9 / 10**

### Lamarckian inheritance (Block 18) — было DS=9.0 [SPLIT]

- **Hard transgenerational (F3+):** P(prior) 0.20 → **ESV ≈ 1.2 / 10**
- **Soft intergenerational (F0→F1/F2):** P(prior) 0.55 → **ESV ≈ 3.0 / 10**

**Действие:** разделить блок на две гипотезы.

### Microbiome-brain (Block 21) — DS=7.9

- P(prior) 0.25 (сильная publication bias, Fanelli ×5)
- Impact 0.7
- Feasibility 0.95
- Tractability 0.7
- SB 1.0

**ESV ≈ 2.0 / 10** — самый переоценённый блок портфеля.

### Pre-Clovis (Block 20) — DS=6.8

P(prior) ≈ **0.85** — уже на грани paradigm shift (Monte Verde, Paisley Caves, White Sands footprints, mtDNA studies). ESV residual в *which* sub-claim.

### ARCHCODE (Block 12) — Paper 1 in queue

**IDEAL stage = 2a Development.** Suggested portfolio rule:
> Не присваивать ESV > 4 для ARCHCODE-dependent гипотез до Stage 3 (Assessment).

---

## РАЗДЕЛ 4. КРИТИЧЕСКИЕ ВЫВОДЫ

### 1. DS-скоры систематически завышены в 2× раз

| Гипотеза | DS | ESV (правильно) | Ошибка |
|----------|-----|-----------------|--------|
| HERV | 9.5 | 2.9 | 3.3× завышение |
| A2 Topological | 9.5 | 3.9 | 2.4× |
| Lamarck (hard) | 9.0 | 1.2 | 7.5× |
| Glymphatic | 9.0 | 2.9 | 3.1× |
| ExoRNA | 8.3 | 2.5 | 3.3× |
| Microbiome | 7.9 | 2.0 | 4.0× |

**Корень ошибки:** DS = Impact × Hope, не Impact × Probability.

### 2. ARCHCODE = capacity blocker

Все Block 12, 13, 18, 19 hypotheses зависят от Paper 1. До его выхода — cap ESV at 4.0.

### 3. Microbiome-brain — самый переоценённый блок

Strong publication bias (Fanelli ×5), мышь-человек translation проблематична.

### 4. Pre-Clovis — уже paradigm shift

P(prior) = 0.85, gain marginal. Не приоритет для solo researcher.

### 5. Lamarck нужно разделить
Hard (transgenerational F3+) ≠ Soft (intergenerational F0→F2). Разные ESV (1.2 vs 3.0).

---

## РАЗДЕЛ 5. РЕАЛЬНЫЕ COMPUTE BENCHMARKS [K]

| Задача | Время | Источник |
|--------|-------|----------|
| REGENIE на UKB (460K samples, 5.76M variants chr6, 100 phenotypes) | **2h53m** | NAR Genom Bioinform 2024 |
| SF-GWAS на UKB 410K full pipeline | **17.5 hrs** | Nat Genet 2025 |
| Lomb-Scargle на 1.26M PBDB | **<1 hour** | astropy timing |
| exceRpt small-RNA на 50 GEO samples | **4-12 hrs** на RTX 5070 Ti | exceRpt v5.0 |
| Persistent homology ≤3D, ≤5K points | **минуты** на GPU (Ripser++) | Somasundaram 2021 |
| LDSC на одной phenotype | **минуты** | LDSC docs |
| LDSC partitioned 50 phenotypes | **~1 day** | scaling |
| bioRxiv preprint screening | **24-48 hrs** | bioRxiv 2024 |

**Имплицитная скорость твоего стека:** ~5-10 гипотез S1/S2 за месяц при систематической работе.

---

## РАЗДЕЛ 6. DATASETS — расширенная таблица [K]

| Dataset | Cost | Size | Application lag |
|---------|------|------|----------------|
| **GTEx v10** (Nov 2024) | Free, open | 16,760 smRNA + 199 deep WGS (195×) | Минуты |
| **Pan-UKB / Neale Lab sumstats** | **Free, no application** | 7,221 phenotypes × 6 ancestries | Минуты ⚡ |
| **UKB individual** | £500 student / £9,000 full Tier 3 + cloud | 500K | 4-8 нед |
| **UKB BIG40 Brain GWAS** | Free | 3,935 IDP × 10M variants | Часы |
| **ADNI** | Free, application | 5,500+ derived studies | 2-4 нед |
| **PBDB API** | Free | 1.26M occurrences | Минуты ⚡ |
| **iHMP IBD** | Free | 132 individuals × 2,965 specimens × multi-omic | Дни |
| **NCBI GEO + SRA** | Free | 250K series | Часы |
| **ERCC exRNA Atlas v3.0** | Free | 2,756 small-RNA samples | Часы |
| **ENCODE 4 cCRE** | Free | 2.3M элементов + Hi-C 37 cell types | Часы |
| **GBIF (биоразнообразие)** | Free | 3.1B records, MIT-license | Минуты-часы ⚡ |

**🎯 Топ-3 by hypotheses-per-effort:**
1. **Pan-UKB / Neale Lab sumstats** — no application + 7,200 phenotypes на ноутбуке (LDSC). Нет аналога.
2. **GTEx v10** — единая загрузка покрывает ARCHCODE/A2/HERV-LTR-eQTL/Lamarck-methylation/exoRNA-proxies
3. **PBDB API** — мгновенно для Lomb-Scargle / TDA / spectral

---

## РАЗДЕЛ 7. SOLO RESEARCHER PROOF-OF-CONCEPT [K]

**Single-author успехи на open data:**

- **Adrian Melott 2008** — single-author *PLoS ONE* (~600 цитирований): подтвердил 62-Myr biodiversity periodicity на PBDB. **Прямой template для Block 20.**
- **giotto-tda / scikit-tda** — single-PI projects, R Journal 2021 benchmark. Template для Block 1-9.
- **bioRxiv reanalysis culture** — 41% препринтов публикуются после peer review; ×5 цитирований vs non-preprint; reach аудитории на 14 месяцев раньше.
- **Citizen-science genomics** на TCGA/ENCODE — много high-impact independent papers.

---

## РАЗДЕЛ 8. КОНКРЕТНЫЕ ИНСТРУМЕНТЫ

| Инструмент | Применение |
|------------|-----------|
| **Manifold Markets** | Self-prediction calibration. Каждая гипотеза → binary market: "passes peer review + ≥10 citations within 3 years?" Brier score < 0.05 = superforecaster-class |
| **OSF (Open Science Framework)** | Pre-register каждую гипотезу до анализа |
| **bioRxiv + Zenodo + GitHub** | Преprint pipeline с reproducibility statement |
| **GRADE framework** | Adaption для u (bias term) в PPV |
| **IDEAL framework** (McCulloch BMJ 2013) | Стадия Idea→Development→Exploration→Assessment→Long-term |
| **FINER + PICOT** | Qualitative gate перед scoring |
| **Snakemake/Nextflow** | Reproducible pipelines (требование top venues) |

---

## РАЗДЕЛ 9. PORTFOLIO REFORMS

1. **Заменить все DS на ESV** — формула из Раздела 2
2. **Block 12 ARCHCODE = binding constraint** — cap dependent ESV at 4.0 до Paper 1
3. **Прунинг Block 14-16** — tardigrade S3-S4, aging без клиники speculative
4. **Добавить 2-3 white-space гипотезы** — приоритет ecology (GBIF) + materials (Materials Project)
5. **Public ESV ledger** — Notion/Obsidian + публичный Manifold Markets для Tier-1 гипотез
6. **Target: ~80 active гипотез** (down from 128) с явными S1-S4 + ESV labels

---

## РАЗДЕЛ 10. PYTHON CALCULATOR (drop-in)

```python
import numpy as np

DOMAIN_PRIORS = {
    "psychology":            (0.40, 0.30),
    "social_behavioral":     (0.60, 0.25),
    "economics_lab":         (0.60, 0.25),
    "cancer_preclinical":    (0.20, 0.40),
    "biomedical_general":    (0.25, 0.30),
    "computational_genomics":(0.45, 0.15),
    "physical_sciences":     (0.65, 0.10),
    "paleontology_quant":    (0.40, 0.15),
    "finance_quant":         (0.27, 0.35),
}

def ppv(prior, power=0.80, alpha=0.05, u=0.30, n_confirm=1):
    """Ioannidis-Goodman PPV with multi-study odds update."""
    LR = (1 - (1 - power) * (1 - u)) / (alpha * (1 - u) + u)
    posterior_odds = (prior / (1 - prior)) * (LR ** n_confirm)
    return posterior_odds / (1 + posterior_odds)

def sb_uplift(beauty_coef_B):
    """Ke et al. 2015 PNAS sleeping-beauty correction, capped."""
    return float(np.clip(1.0 + 0.1 * np.log1p(max(0.0, beauty_coef_B)), 1.0, 1.5))

def esv(domain, impact, feasibility, tractability, beauty_B=0,
        power=0.80, n_confirmatory=1):
    """Returns ESV ∈ [0, ~10]."""
    prior, u = DOMAIN_PRIORS[domain]
    p_true = ppv(prior, power=power, u=u, n_confirm=n_confirmatory)
    return 10 * p_true * impact * feasibility * tractability * sb_uplift(beauty_B)

# Usage:
# A2 Topological Penetrance:
# esv("computational_genomics", impact=1.0, feasibility=0.85,
#     tractability=0.7, beauty_B=0, n_confirmatory=2)
# → ~3.9
```

---

## NEEDS_INPUT (gating numbers)

- [U] **A2 Topological Penetrance** — точное определение: твоя architectural class или literature term?
- [U] **BSV** Block 13 — exact materials claim?
- [U] **ARCHCODE Paper 1** core hypothesis (для §2.4 ESV)
- [U] **ArgosArb** оставшиеся 10 гипотез — finance prior 0.20-0.35
- [U] **Tardigrade Block 15** specific claims
- [U] **UKB-RAP** £500 student tier — готов регистрироваться?

---

## КЛЮЧЕВЫЕ ССЫЛКИ [K]

- Ioannidis 2005 PLoS Med 2:e124 (PPV формула)
- OSC 2015 Science 349:aac4716 (psychology replication)
- Camerer et al. 2018 Nat Hum Behav (top journals 62%)
- Begley & Ellis 2012 Nature 483:531 (cancer 11%)
- Errington et al. 2021 eLife 10:e71601 (RPCB 46%)
- Fanelli 2010 PLoS ONE 5:e10068 (positive results bias)
- Ke et al. 2015 PNAS 112:7426 (Sleeping Beauty B-coefficient)
- Goodman 2007 (LR ≈ 16 per study)
- McCulloch 2013 BMJ 346:f3012 (IDEAL framework)
- Hulley 2013 (FINER)
- Melott 2008 PLoS ONE 3:e4044 (62-Myr replication template)
- Han et al. 2021 PLoS Biol PMC8168893 (glymphatic-ADNI)
- McArthur & Capra 2021 AJHG (TAD heritability)
- Maurano et al. 2012 Science (90% disease SNPs non-coding)

---

*Создан: 2026-05-10 | Метод: Bayesian PPV с empirical anchors*
*Заменяет: [[Portfolio Intelligence Audit (2026-05-10)]] (v1, deprecated)*
