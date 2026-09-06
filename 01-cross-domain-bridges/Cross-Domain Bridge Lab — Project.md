---
title: "Cross-Domain Bridge Lab"
type: project
status: active
domain: Meta-Research, Cross-Domain Methodology Testing
created: 2026-09-06
related:
  - "[[H-7 GeoSpectra Lab]]"
  - "[[H-7 TAD Spectral Diagnostic]]"
  - "[[[PARKED] Riemann via RMT — H7 Bridge]]"
  - "[[ChernoffPy — Predictions Log]]"
  - "[[Open Problems Catalog — Skeptic Assessment of the 100-item version (2026-09-06)]]"
  - "[[100 Open Problems — raw catalog (source, 2026-09-06)]]"
tags:
  - project
  - cross-domain
  - methodology-testing
  - bridge-problems
  - active
---

## Path: C:/Users/serge/.claude/memory/projects/cross-domain-bridge-lab/

# Cross-Domain Bridge Lab

> Цель: взять мосты, предложенные внешним cross-domain анализом (2026-09-06) поверх 100-problem каталога, отделить **verified** от **unverified**, и по каждому verified мосту поставить один дешёвый вычислительный эксперимент прежде чем инвестировать больше.

**Принцип (по фидбеку сессии — anti-overengineering):** один project-файл, не сложная архитектура. Подпапки/скрипты появляются только когда конкретный bridge реально начинает исполняться.

---

## 🔴 ПЕРЕД СТАРТОМ — нужно от тебя

Три моста из внешнего анализа **не найдены нигде в этом vault** после grep-проверки:

| Ссылка в документе | Статус проверки |
|---|---|
| Frontier R&D (Sentinel-2 OOD, Гипотеза H1) | ❌ NOT FOUND |
| TOFT vs SMT (Soto & Sonnenschein 1999) kill-test | ❌ NOT FOUND |
| RAF Theory / CatlyNet / CatReNet / iRAF / Wood-Ljungdahl | ❌ NOT FOUND |

**Вопрос:** это реальные проекты на другом компьютере (D:\ДНК, E:\Проверка Гипотез) / устные обсуждения не сохранённые в vault, или это правдоподобные, но не имеющие основы связки от внешнего LLM (тот же паттерн, что мы поймали в 100-problem каталоге — реальные источники + шаблонные bridge-claims)?

**Пока не подтверждено → эти 3 моста статус `UNVERIFIED-SOURCE`, не включаются в active execution queue.**

---

## ✅ VERIFIED мосты (grounded in existing vault files)

### Bridge 1 — Spectral universality: RMT ↔ Riemann zeros ↔ Hi-C chromatin (TAD)

**Grounding:**
- `[PARKED] Riemann via RMT — H7 Bridge.md` — план был, но **ссылается на invalidated результат** (см. ниже)
- `H-7 TAD Spectral Diagnostic.md` — реальный код в `E:\Проверка Гипотез\работаю над проверкой гипотез\H-7 test dhk\`
- ⚠️ **Naming collision:** "H-7 GeoSpectra Lab" (S³×S⁶ compactification, физика элементарных частиц) и "H-7 TAD Spectral Diagnostic" (Hi-C хроматин) — это **два разных проекта**, случайно делящих номер "H-7". PARKED-файл ошибочно линкует на GeoSpectra Lab вместо TAD Spectral Diagnostic.

**🔴 КРИТИЧЕСКАЯ НАХОДКА (2026-09-06):** PARKED-заметка (создана 28.05.2026) описывает биологический r-statistic результат как готовый к сравнению. Но сам проект TAD Spectral Diagnostic показывает:

| Заявлено в PARKED | Реальный статус проекта |
|---|---|
| "H-7 уже вычисляет r-статистику на биологических матрицах" | AUC=0.99998 **INVALIDATED 16.05.2026** — label circularity (классификатор предсказывал WT vs auxin через саму разницу как feature — тавтология) |
| Чистый переход Poisson(0.39)→Wigner-Dyson(0.53) | Реальные числа: **WT r=0.5113±0.061, Auxin r=0.5130±0.060**, delta=+0.0018 — обе точки близко к 0.51, никакого чистого перехода на уровне среднего |
| Готов к запуску | **decision: HOLD**, redesign Option A в процессе (ожидаемый честный AUC 0.70-0.85, не завершён) |

PARKED-файл написан на 12 дней позже инвалидации, но ссылается на результат как на живой — stale reference, пойман до запуска нового эксперимента, не после.

**⚠️ Отдельный вопрос ансамбля (GOE vs GUE):** сам TAD-проект уже утверждает через Altland-Zirnbauer tenfold way, что полносвязная (fused) хроматин-матрица → класс **A (GUE)**, а не GOE как я предполагал изначально. Это внутренний теоретический аргумент проекта (симметрия нарушается при fusion), не тривиальный факт "вещественная матрица = GOE". Открытый вопрос, не мой домен для мгновенного решения — фиксирую как unresolved.

**Разделение на честные подэтапы:**

**✅ Phase 1a — READY TODAY, независимо от биологии:**
Чистая репликация известного RMT-факта на нулях Римана. Не требует TAD-данных вообще.
```python
# pip install numpy requests

import numpy as np
import requests

# Odlyzko zeros — публичные, первые ~100k достаточно для sanity check
url = "https://www-users.cse.umn.edu/~odlyzko/zeta_tables/zeros1"
resp = requests.get(url, timeout=60)
zeros = np.array([float(x) for x in resp.text.split()])

spacings = np.diff(zeros)
spacings_norm = spacings / spacings.mean()

r = np.minimum(spacings_norm[:-1], spacings_norm[1:]) / \
    np.maximum(spacings_norm[:-1], spacings_norm[1:])
r_mean = r.mean()

print(f"r_mean (Riemann zeros): {r_mean:.4f}")
print(f"GUE theory prediction:  0.6027")
print(f"Delta: {abs(r_mean - 0.6027):.4f}")

# Kill-критерий: |r_mean - 0.6027| должен быть < 0.01 (иначе методология сломана,
# это НЕ открытие — Montgomery-Odlyzko закон известен с 1972/1987)
```
**Kill-критерий:** если `r_mean` не совпадает с 0.6027 в пределах ~0.01 — ошибка в коде/данных, не научный результат. Это replication известного факта, не гипотеза.
**Цель этого шага:** не "открытие", а sanity-check инфраструктуры + личная проверка что pipeline работает, прежде чем трогать что-либо биологическое.

**🔴 Phase 1b — BLOCKED до завершения H-7 TAD Option A:**
Сравнение с хроматином невозможно честно, пока сам biological r-statistic result не прошёл redesign. Смотреть `H-7 TAD Spectral Diagnostic.md` → Next Steps → Option A.

**Status:** Phase 1a READY, Phase 1b BLOCKED (upstream dependency invalidated).

---

### Bridge 2 — ChernoffPy operator semigroups ↔ Neural ODE/UDE stability

**Grounding:**
- `Distribution-free bound — Markov Chernoff для Skeptic.md`
- `ChernoffPy — Predictions Log.md` — активный прогнозный трек

**Claim (из внешнего анализа):** формула Чернова "локальный оператор → глобальная эволюция" может дать строгую верхнюю оценку ошибки для Neural ODE / UDE, решая проблему Uncertainty Calibration из #79 100-problem каталога.

**Что нужно проверить прежде чем брать всерьёз:** это **[HYPOTHESIS]**, не проверенный факт. Формула Чернова даёт границу для аппроксимации $C_0$-полугрупп конечно-разностными операторами — нужно явно показать, что ResNet/Neural-ODE слой **является** дискретной аппроксимацией полугруппы в смысле теоремы Чернова (не просто аналогия по звучанию).

**Kill-критерий:** взять простой Neural ODE (1D, известное аналитическое решение), сравнить error bound из теоремы Чернова с эмпирической ошибкой. Если граница Чернова НЕ доминирует эмпирическую ошибку (bound слабее реальности) — bridge не работает практически, даже если формально корректен.

**Status:** NEEDS FORMALIZATION — сначала доказать что Neural-ODE слой удовлетворяет условиям теоремы Чернова, потом тестировать.

---

### Bridge 3 — May 1972 stability-complexity ↔ TDA early-warning signals

**Grounding:**
- `Hypothesis Revival Targets — 9 классических гипотез` (R1, эта же сессия)
- Внешний анализ предлагал: GNN на реальных сетях (Mangal, GloBI database) + persistent homology (Betti numbers, персистентная энтропия) вместо классических статистик (автокорреляция, дисперсия) для early-warning signals

**🔴 SCOPING CORRECTION (2026-09-06):** источники данных из внешнего анализа (Mangal, GloBI) **непригодны** для этой задачи — проверено WebSearch до запуска, не после:
- **Mangal** [VERIFIED]: 187 статичных кросс-секционных сетей хищничества из *разных* систем (медиана 19 узлов). Это не повторные снимки ОДНОЙ системы во времени — нет временно́й оси внутри одной сети.
- **GloBI** [VERIFIED]: агрегатор записей взаимодействий видов; "snapshots" в его описании — это версии всей базы раз в полгода, не экологический временной ряд одной системы.
- Тот же паттерн, что уже поймали в этой папке дважды (Frontier R&D/TOFT/RAF; каталог 100 задач): правдоподобно звучащая связка от внешнего LLM, источник реален по названию, но не по функции.

**Правильный источник (найден и проверен, 2026-09-06):**
- **Carpenter et al. 2011, *Science* 332:1079** — «Early Warnings of Regime Shifts: A Whole-Ecosystem Experiment» [VERIFIED]. Peter Lake (манипуляция: постепенное добавление хищной рыбы, 2008–2011) vs Paul Lake (неманипулируемый референс, тот же период) — парный дизайн с **известной датой** начала манипуляции и зафиксированного трофического сдвига; классический EWS (рост автокорреляции и дисперсии хлорофилла/pH/O₂/зоопланктона) обнаружен **более чем за год** до сдвига в оригинальной публикации — это готовый baseline для сравнения, не только датасет.
- Данные — Environmental Data Initiative (EDI), NTL-LTER Cascade Project, публично доступны: `portal.edirepository.org` (пакеты серии `knb-lter-ntl`, high-frequency chlorophyll/temperature/DO 2008–2019) [VERIFIED, точные ID пакетов — WEAK, уточнить при загрузке].
- Follow-up: Cline et al. 2014, *Ecosphere* — пространственные индикаторы на той же системе.

**⚠️ Критическая находка для kill-критерия (novelty/feasibility check, FL Step -3):** Wang et al. 2023, *Nature Communications* — «Early warning signals have limited applicability to empirical lake data» [VERIFIED]: систематический анализ по множеству реальных озёр показал, что чистые critical transitions **редки**, а классические EWS-индикаторы на реальных (не экспериментальных) данных часто работают не лучше случайного угадывания. Значит исходный kill-критерий «≥3 задокументированных коллапса» был оптимистичен — набрать 3 независимых случая с надёжным ground truth *дороже*, чем предполагалось. Peter Lake — редкое исключение именно потому что это контролируемый эксперимент с референс-озером, а не наблюдательные данные.

**Novelty check:** общий метод (TDA/persistent homology как EWS) уже применяется в экологии описательно (Bailey 2026, обзор `arXiv:2603.25760`, включая приложение к 500 рядам BioTIME) и в финансах — с явной гонкой лидирования против classical EWS и измеренным опережением (~34 дня, Frontiers 2022). Но **прямого применения TDA к датасету Peter Lake / гонки лидирования именно на нём не найдено** — целевой тест не является пере­форму­лировкой уже опубликованного результата.

**Пересмотренная гипотеза (Phase 1, честно достижимая):**
- Population: Peter Lake (манипуляция) + Paul Lake (референс) — не «≥3 коллапса», а один эксперимент со встроенным негативным контролем (референс-озеро не должно показывать сдвиг ни в TDA, ни в classical EWS)
- Метод: time-delay embedding (Takens) многомерного ряда (хлорофилл, pH, DO, зоопланктон) → Vietoris–Rips → Betti-1/персистентная энтропия; baseline — автокорреляция и дисперсия на тех же рядах
- Kill-критерий (Phase 1): на Peter Lake TDA-сигнал не опережает classical EWS ни на одном из ≥2 рядов (при этом на Paul Lake оба метода корректно молчат) → KILLED для этого случая. ≥3 случая — цель Phase 2, только если Phase 1 не убит

**Status:** READY (скоупинг завершён 2026-09-06) — источник данных исправлен и проверен, метод, baseline и honest kill-критерий определены. Экспериментальная папка создана, расчёт (загрузка EDI + Ripser) — следующий шаг.

---

## ❌ Отклонённые/не найденные (park until located)

**Frontier R&D, TOFT vs SMT, RAF/CatlyNet** — см. раздел выше. Не добавлять в execution queue пока не подтверждена реальность этих проектов.

---

## Execution Rules (переиспользуем H6 lesson)

Каждый bridge при реальном запуске должен иметь (см. [[raw/lesson-hypothesis-execution-rules]]):
1. Разделение Pipeline vs Experiment
2. Kill criterion ДО запуска
3. Минимум одна sensitivity-проверка (не единственный run)
4. Evidence label: `VERIFIED-REAL` / `HYPOTHESIS` / `UNVERIFIED`
5. Same-day vault update

**Три исхода, не "почти":** KILLED / CONFIRMED / LEAD.

---

## Приоритет запуска

| # | Bridge | Готовность | Первый шаг |
|---|--------|-----------|-----------|
| 1 | RMT/Riemann/Hi-C (с исправлением GOE≠GUE) | READY | Скачать Odlyzko zeros, развести ансамбли, запустить существующий H-7 код |
| 2 | TDA early-warning vs classical EWS | READY TO SCOPE | Найти Mangal/GloBI датасет с известным коллапсом |
| 3 | Chernoff/UDE stability bound | NEEDS FORMALIZATION | Доказать applicability теоремы Чернова к конкретному Neural-ODE слою |
| — | Frontier R&D / TOFT / RAF | BLOCKED | Локализовать реальность источника |

---

*Создан: 2026-09-06. Метод: skeptic-verified cross-referencing внешнего анализа против реального содержимого vault.*
