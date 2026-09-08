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

## ⚫ ОТВЕЧЕНО (2026-09-07) — не переспрашивать

Три моста из внешнего анализа **не найдены нигде в этом vault** после grep-проверки:

| Ссылка в документе | Статус проверки |
|---|---|
| Frontier R&D (Sentinel-2 OOD, Гипотеза H1) | ❌ NOT FOUND |
| TOFT vs SMT (Soto & Sonnenschein 1999) kill-test | ❌ NOT FOUND |
| RAF Theory / CatlyNet / CatReNet / iRAF / Wood-Ljungdahl | ❌ NOT FOUND |

**[VERIFIED — прямая цитата пользователя, 2026-09-07]:** «на другой машине может и раньше были но сейчас у меня нет доступа к этой машине». Это ПОСТОЯННОЕ состояние, не временный открытый вопрос — эти 3 моста остаются `unverified_source` в `registry/graph.yaml` без дальнейшего переспрашивания. Не строить на них выводы, не поднимать вопрос снова без новой информации от пользователя.

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

**Что нужно было проверить прежде чем брать всерьёз:** это было **[HYPOTHESIS]**, не проверенный факт — формула Чернова даёт границу для аппроксимации $C_0$-полугрупп конечно-разностными операторами, нужно было явно показать, что ResNet/Neural-ODE слой **является** дискретной аппроксимацией полугруппы в смысле теоремы Чернова (не просто аналогия по звучанию).

**Kill-критерий (исходный):** взять простой Neural ODE (1D, известное аналитическое решение), сравнить error bound из теоремы Чернова с эмпирической ошибкой. Если граница Чернова НЕ доминирует эмпирическую ошибку (bound слабее реальности) — bridge не работает практически, даже если формально корректен.

**Status: CONFIRMED-WITH-CAVEATS (закрыто 2026-09-08, арка H-B2-1↔1v, полная хронология в `registry/graph.yaml` и `.claude/memory/decisions.md` ADR-014…072 [VERIFIED — grep] — этот раздел даёт КОНЦЕНТРАТ, не дублирует детали.)**

**Что реально произошло, коротко:**
1. Neural-ODE/ResNet слой формализован и проверен как дискретная аппроксимация $C_0$-полугруппы в смысле теоремы Чернова (H-B2-1, CONFIRMED — исходный `KILLED` вердикт был скорректирован в той же сессии после чтения основной теоремы источника, не упрощённого следствия). M1 (transient growth constant, `sup_t||exp(tA)||`) далее используется как измеряемая эмпирическая величина для сравнения с теоретической границей.
2. Первая попытка объяснить большие значения M1 через собственные векторы матрицы связи — κ(V) (eigenvector condition number). Работает при малом N, **твёрдый потолок объяснительной силы между N=32 и N=40** (H-B2-1m→1q, 4 эксперимента подряд, шеститочечный null на двух независимых диапазонах сидов — `hard_killed`, первая полноценная запись в `null_results/INDEX.md`).
3. Вторая попытка — ω(A) (numerical abscissa, Bendixson/Lumer-Phillips) — тот же потолок, тот же диапазон N.
4. **Третий дескриптор закрыл дырку**: pseudospectral abscissa α_ε(A) — CONFIRMED на N=40,50 **трижды независимо подряд** (H-B2-1r: собственная реализация, после найденного и исправленного бага grid-search; H-B2-1s: независимый пакет `pseudopy`, ρ=0.989-0.995; H-B2-1t: полностью свежие сиды, ещё сильнее). Обоснование через теорему Крейса: $K(A) \le \sup_t||\exp(tA)|| \le e{\cdot}n{\cdot}K(A)$.
5. **Механистическая проверка** (H-B2-1u, прямая проверка неравенства Крейса, не только корреляции): граница держится (0/20 нарушений после самопойманного бага в собственном eps-сэмплировании), но **efficiency ratio (observed/ceiling) низкий** — медиана 3.7-6.3%. Граница формально валидна, но практически рыхлая — известное классическое ограничение множителя $e{\cdot}n$ самой теоремы (Trefethen & Embree 2005), не дефект вычисления.
6. **Двойная независимая cross-implementation проверка** (H-B2-1s для α_ε при eps~1; H-B2-1v для малых eps теоремы Крейса, через `pseudopy.NonnormalAuto` — другой алгоритм) подтвердила: рост K(A) при малых eps — реальное свойство матрицы (для матриц с большим K), не артефакт сетки; для матриц с малым K константа честно сходится.

**Ответ на исходный kill-критерий:** граница Чернова/Крейса формально ДОМИНИРУЕТ эмпирическую ошибку (проверено напрямую, не предположено) — но КРАЙНЕ рыхло (efficiency 3.7-31%, вероятно ещё ниже — см. H-B2-1u Convergence Caveat). Bridge работает как *объяснение существования* (pseudospectral abscissa — правильный дескриптор transient growth при большом N), но НЕ как *количественно точный предиктор* величины M1.

**Открытый следующий уровень (назван пользователем, не запущен):** можно ли получить tighter predictor/bound для M1 из pseudospectral quantities, а не просто корреляцию/loose bound? Требует новой теории (numerical-range или resolvent-norm bound для этого конкретного семейства матриц), не просто нового прогона.

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

**Арка закрыта (2026-09-09).** 15 под-гипотез (H-B3-1 → H-B3-1p), 0 confirmed, 8 killed, 1 parked, остальные — verified_grounding/consistency-проверки, которые сами не претендовали на promote. Ключевая цепочка:
- H-B3-1l дал headline TDA-лид на Lower Zurich (+50.0 мес) → **дважды опровергнут независимо**: (1) H-B3-1n — против честного AR(1) surrogate null тот же лид оказался лишь на 90.4-м перцентиле (p80=33.0, p95=61.0) → `INCONCLUSIVE_AT_THIS_SAMPLE_SIZE`, статус понижен confirmed→lead; (2) H-B3-1p — 6-й skeptic-проход нашёл, что classical-статистика выбиралась РАЗНЫМИ правилами для целевого случая (oracle-informed) и для негативных контролей (симметричное); честный пересчёт тем же правилом **инвертировал вердикт** CONFIRMED→REJECTED (лид стал −15.0 мес). H-B3-1l downgrade `lead`→`killed`, полный ретроскан потомков выполнен.
- H-B3-1o (Peter pH lag diagnostic) — метрика (persistent homology total-persistence) не прошла positive-control gate на известном случае (77.0-дневный разрыв на doSat при требовании ≤20) — `METRIC_UNRELIABLE`, парковано, несмотря на визуально убедительное 0.0-дневное совпадение по pH. Не затронуто: Peter doSat's независимый +13-месячный лид (4× реплицирован) — единственный настоящий выживший позитивный сигнал моста теперь.
- H-B2-2-класса "positive-control gate перед доверием диагностике" урок применён здесь напрямую и поймал именно то, для чего он предназначен.

**Научный смысл (не «ничего не получилось», а информативный отрицательный результат):** в этом классе озёрных рядов TDA-based early-warning criteria оказались чувствительны к структуре сигнала и способны создавать убедительные, но недискриминирующие лиды; несколько естественных исправлений (AR(1)-null, симметричный отбор статистики, positive-control gate) не устранили проблему, а последовательно её сузили. Мост Bridge 3 закрыт как construct-validity результат, не как провал реализации.

**Revival condition:** новый TDA-EWS вариант на этой же паре озёр возобновляется ТОЛЬКО с (а) внешним свежим датасетом другого manipulated-lake эксперимента (не Cascade/Peter-Paul) ИЛИ (б) механистической моделью failure mode (почему TDA-Betti чувствителен к структуре сигнала на этом классе рядов), а не очередным вариантом статистики отбора на тех же данных.

**Status:** CLOSED (2026-09-09) — 15/15 под-гипотез resolved, арка не даёт дальнейших дешёвых вариантов на этих данных. См. `null_results/H-B3-1l-lakes-tda-ews-peaktau-v3.md`, `parked/H-B3-1o-peterph-lag-diagnostic.md`.

---

### Bridge 8 (REJECTED at scoping gate, 2026-09-09) — UDE parameter identifiability ↔ ChernoffPy

**Почему это новый мост, а не продолжение Bridge 2 (первоначальный аргумент, см. коррекцию ниже):** Bridge 2 тестировал transient-growth/stability предсказание (pseudospectral abscissa как bound для M1). Этот источник называет ОТКРЫТОЙ другую, структурно иную задачу того же UDE-стека: **параметрическая идентифицируемость** нейросетевого компонента деградирует при ограниченном observable mapping (не все переменные системы наблюдаемы) и малом/шумном датасете. Разные вопросы, общая инфраструктура (`PRJ-CHERNOFFPY`) — переносится код, не вывод.

**🔴 Коррекция (2026-09-09, тот же день): фраза «общая инфраструктура» была непроверенным допущением, не фактом.** Feasibility-gate (пункт 1 ниже) выполнен — и провалился. Прямой grep по всей папке `experiments/` на `import torch|nn.Module|.backward()` — **0 совпадений**. Тот же grep по РЕАЛЬНОМУ внешнему репозиторию `E:/MarkovChains/ChernoffPy` (`chernoffpy/`, `examples/`, `tests/`) на `torch|neural|UDE|identifiab` — **0 совпадений**. Весь фрейминг Bridge 2 «Neural-ODE/UDE» — теоретическая аналогия (теорема Чернова применена к линейному оператору A / матричной экспоненте), НЕ обученная нейросеть. Нигде в `PRJ-CHERNOFFPY` (ни внутри Y-17, ни во внешнем репо) нет: обученной модели, модели шума, ограничения observable mapping. Построение реальной UDE-инфраструктуры (ODE-солвер + обучаемая сеть + оптимизатор + модель шума + метрика practical identifiability) с нуля — это НЕ дешёвое переиспользование, а новый ML-пайплайн, непропорциональный собственному же feasibility-критерию этого моста (пункт 1 ниже).

**Урок процесса (честно, не заметая под ковёр):** при регистрации Bridge 8 я написал «общая инфраструктура» ДО того как прочитал реальный код `PRJ-CHERNOFFPY` — непроверенное умозаключение, поданное как факт, ровно тот класс ошибки, что integrity.md запрещает (`[INFERRED]` без цепочки проверки = не `[VERIFIED]`). Novelty/transfer gate, который я же сам определил ДО scoping, сработал ровно для того, для чего был создан — поймал ложную посылку до какого-либо реального вложения (0 экспериментов запущено). Это тот же паттерн, что Bridge 3's собственная SCOPING CORRECTION (Mangal/GloBI), только пойман на день раньше в цикле, а не после первой попытки.

**Grounding (источник проверен WebSearch этой сессией, не принят на веру):**
- Philipps, Schmid, Hasenauer (2025), *«Current state and open problems in universal differential equations for systems biology»*, npj Systems Biology and Applications 11, [s41540-025-00550-w](https://www.nature.com/articles/s41540-025-00550-w) [VERIFIED — DOI резолвится, статья реальна, опубликована Nature]. Явно называет открытой проблемой: "Observable mappings can restrict the identifiability of model parameters, particularly when data availability is low and resolution is limited."

**Novelty check (FL Step -3, выполнен ДО scoping):** grep по `null_results/INDEX.md`, `parked/INDEX.md`, `pearl_registry/INDEX.md` на "identifiab*" — 0 совпадений с этой конкретной задачей (единственное совпадение в graph.yaml — не связанный causal-identifiability вопрос в H-7-2/Kauffman). Не переоткрытие.

**⚠️ Novelty/Transfer Gate — определён СЕЙЧАС, до какого-либо scoping-вложения (именно то, чего не хватало Bridge 3 на старте — источник данных Mangal/GloBI оказался непригоден и был пойман только ПОСЛЕ первой попытки скоупинга):**
1. **Feasibility:** содержит ли `PRJ-CHERNOFFPY` (или можно ли дёшево добавить) синтетическую систему с ИЗВЕСТНЫМИ истинными параметрами, чтобы деградацию идентифицируемости можно было измерить против проверяемого эталона — не просто "сеть подогналась под данные"? Если требует непропорциональной новой инфраструктуры симуляции → мост паркуется на этом шаге, не выполняется.
2. **Различимость от Bridge 2:** гипотеза должна делать предсказание, которое было бы ЛОЖНЫМ, если бы идентифицируемость деградировала как обычная noise-robustness кривая, а не именно как «ограничение observable mapping» из источника — иначе это просто Bridge 2 под другим именем.
3. **Kill-критерий для самого этапа scoping (до claim.md):** если `PRJ-CHERNOFFPY`'s код не предоставляет способ дёшево строить partial-observable варианты одной и той же системы (не переписывая симулятор с нуля) — `status: blocked` на scoping-уровне, эксперимент не начинается.

**Revival condition:** этот конкретный мост (через `PRJ-CHERNOFFPY`) возобновляется ТОЛЬКО если (а) кто-то реально построит UDE-training инфраструктуру (обученная сеть + шум + observable-restriction + identifiability-метрика) — непропорциональное вложение, сейчас не оправдано ради одного моста, ИЛИ (б) найдётся другой уже существующий проект/репозиторий (среди 54 в meta-graph или локальных) с РЕАЛЬНОЙ UDE-training инфраструктурой — при этом переносится не «Bridge 8 на ChernoffPy», а «Bridge 8 на этот другой проект», с собственной проверкой feasibility. Открытая научная задача (npj Sys Biol Appl 2025) остаётся реальной и VERIFIED-REAL — отклонён именно ЭТОТ мост, не сама задача.

**Status:** `rejected` в `registry/graph.yaml` (узлы `PROB-UDE-IDENTIFIABILITY-2025` остаётся `open`, `BRIDGE-8-UDE-IDENTIFIABILITY` → `rejected`). Feasibility-gate (пункт 1) выполнен и провалился в тот же день, до какого-либо scoping-вложения.

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
| 1 | RMT/Riemann/Hi-C (с исправлением GOE≠GUE) | READY (Phase 1a), Phase 1b BLOCKED | Phase 1b: Option A redesign в H-7 TAD (внешний проект, вне scope Y-17) |
| 2 | Chernoff/UDE stability bound (κ(V)→ω(A)→pseudospectral abscissa→теорема Крейса) | **CONFIRMED-WITH-CAVEATS, арка закрыта (H-B2-1k→1v)** | Открытый next-level вопрос: tighter predictor/bound для M1 (не запущен, требует новой теории) |
| 3 | TDA early-warning vs classical EWS | Phase 1 запущена, LEAD/weak_alive (см. `null_results/` и `pearl_registry/`) | Rows 2-3 Relaxation Map (change-point co-requirement, peak-tau) — не запущены |
| — | Frontier R&D / TOFT / RAF | BLOCKED — постоянный `unverified_source`, не переспрашивать без новой информации | — |

---

*Создан: 2026-09-06. Метод: skeptic-verified cross-referencing внешнего анализа против реального содержимого vault.*
