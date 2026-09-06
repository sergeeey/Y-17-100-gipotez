# Y-17 — 100 гипотез / Open Problems Bridge Lab

**Перенесено из Obsidian vault:** 2026-09-06
**Статус:** активная рабочая папка, vault остаётся source of truth для истории решений — сюда копии для локальной работы

---

## Структура папки

```
00-catalog/                  ← сами каталоги задач (100 + 44 + skeptic-разбор)
01-cross-domain-bridges/     ← проект мостов + связанные H-7 файлы (физика vs биология!)
02-related-projects-context/ ← ChernoffPy, May 1972, конкретные смежные проекты
03-methodology-rules/        ← правила которые применялись при аудите (переиспользуй их)
```

---

## 00-catalog/ — три слоя одного каталога

| Файл | Что это | Доверие |
|------|---------|---------|
| `100 Open Problems — raw catalog` | Исходный список 100 задач от внешнего LLM | ⚠️ Названия+источники реальны, но "Why open"/"Why matters" — **шаблонный текст**, повторяется дословно по кластерам источников (проверено grep'ом — 13 идентичных фраз) |
| `Open Problems Catalog — Phase 1 (44 of 100)` | Мой собственный набор — 4 параллельных агента с **живым web/arXiv поиском** статуса каждой задачи | ✅ Более глубокий, но 4x меньше (43 уникальные, не 100) |
| `Open Problems Catalog — Skeptic Assessment` | Разбор внешнего каталога — что реально, что theater | Читай ПЕРВЫМ — объясняет, как использовать остальные два файла |

**Пересечение между Phase 1 (43) и внешним каталогом (100): почти нулевое.** Комбинированный уникальный пул — **~141 задача**. Разные домены (мой: number theory/physics/CS/bio-classic; внешний: COLT learning theory, quantum info, finite groups, UDE systems biology, single-cell benchmarking).

**Как использовать внешний каталог честно:** это индекс "100 названий + 27 реальных источников", не готовый анализ. Перед тем как брать конкретную задачу — читай оригинальный цитируемый источник (COLT proceedings, Dagstuhl Report, RIMS Kyoto list и т.д.), не шаблонное резюме.

---

## 01-cross-domain-bridges/ — ⚠️ ВАЖНО прочитать перед стартом

### Naming collision (уже пойман, не наступай снова)

**"H-7 GeoSpectra Lab"** и **"H-7 TAD Spectral Diagnostic"** — ДВА РАЗНЫХ ПРОЕКТА, случайно делящих номер:

| | H-7 GeoSpectra Lab | H-7 TAD Spectral Diagnostic |
|---|---|---|
| Домен | Физика частиц, S³×S⁶ compactification | Биология, Hi-C хроматин |
| Путь | `E:\...\N-7-GeoSpectra-Lab` | `E:\Проверка Гипотез\работаю над проверкой гипотез\H-7 test dhk\` |
| Статус | ACTIVE, external collaboration (details local-only) | HOLD, redesign in progress |

`[PARKED] Riemann via RMT — H7 Bridge.md` **ошибочно линкует на GeoSpectra Lab**, хотя реально должен ссылаться на TAD Spectral Diagnostic. Файл включён в папку с этой пометкой — не путай их дальше.

### Критическая находка: биологический результат инвалидирован

`H-7 TAD Spectral Diagnostic.md` показывает:
- Заявленный AUC=0.99998 (16.05.2026) → **INVALIDATED в тот же день** — label circularity (классификатор предсказывал WT vs auxin через саму разницу как feature, математическая тавтология)
- Реальные числа: **WT r=0.5113±0.061, Auxin r=0.5130±0.060**, delta=+0.0018 — крошечная, никакого чистого перехода Poisson(0.39)→Wigner-Dyson(0.53)
- Redesign "Option A" в процессе, ожидаемый честный AUC 0.70-0.85, **не завершён**

`[PARKED] Riemann via RMT` написан на 12 дней позже инвалидации, но описывает результат как готовый к сравнению. **Не строй на этом, пока Option A не даст честный результат.**

### Что можно делать прямо сейчас (Phase 1a, независимо от биологии)

```python
# pip install numpy requests

import numpy as np
import requests

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

# Kill-критерий: |r_mean - 0.6027| < 0.01, иначе методология сломана
# (это replication известного факта Montgomery-Odlyzko 1972/1987, не открытие)
```

**Phase 1b (сравнение с хроматином) — BLOCKED** до завершения Option A в TAD-проекте.

### Открытый теоретический вопрос (не решён, зафиксирован)

TAD-проект утверждает через Altland-Zirnbauer tenfold way, что fused-хроматин → класс **A (GUE)**, не GOE, вопреки моей изначальной интуиции "вещественная симметричная матрица = GOE". Это внутренний аргумент проекта про нарушение симметрии — открытый вопрос, требует отдельного разбора прежде чем сравнивать ансамбли напрямую.

---

## 02-related-projects-context/

- **ChernoffPy** — реальный активный проект (predictions log), предложенный мост: теорема Чернова (полугруппы операторов) ↔ Neural ODE/UDE stability bounds. Статус: **[HYPOTHESIS]**, не доказано что Neural-ODE слой формально удовлетворяет условиям теоремы Чернова — это первый шаг, не эксперимент.
- **Hypothesis Revival Targets** — содержит R1 (May 1972 stability-complexity paradox), реальную основу для моста #3 (TDA early-warning ↔ May's paradox). Данные для проверки открыты: Mangal, GloBI (ecological network databases).

---

## 03-methodology-rules/ — переиспользуй, не изобретай заново

- **`lesson-hypothesis-execution-rules.md`** — 6 обязательных правил для любого запуска: разделение pipeline/experiment, kill-criterion до запуска, sensitivity matrix (не один run), top-N side-signal capture, evidence labels (VERIFIED-REAL/SYNTHETIC/HYPOTHESIS/UNVERIFIED/CONFLICT), same-day update. Три исхода: KILLED/CONFIRMED/LEAD — никаких "почти".
- **`lesson-text-figures-consistency-check.md`** — почему нужно сверять текст с фигурами/данными перед любым claim "готово". Тот же паттерн, что мы поймали в TAD-проекте.
- **`Submission Gate Protocol (HARD RULE).md`** — 4 gate'а перед любой внешней публикацией (skeptic run + checklist + consistency check + 24h cooling off). Применяй если что-то из этой папки дойдёт до preprint.
- **`Portfolio Intelligence Audit v2 — Bayesian PPV Edition.md`** — формула ESV (Expected Scientific Value) через Ioannidis PPV с empirical reproducibility base rates по доменам. **Полезно переиспользовать для честного скоринга** вместо "compressed 7-10 scores" из внешнего каталога — там ranking был precision theater (composite-числа с 3 знаками после запятой поверх нерасличимых входов).

---

## ❌ Не найдено в vault (нужен твой ответ)

Три моста из исходного cross-domain анализа **не существуют нигде** в Obsidian vault после grep-проверки:

- **Frontier R&D** (Sentinel-2 OOD detection, Гипотеза H1)
- **TOFT vs SMT** (Soto & Sonnenschein kill-test)
- **RAF Theory / CatlyNet / iRAF / Wood-Ljungdahl pathway**

Если они реальны — либо на другом компьютере (D:\ДНК?), либо обсуждались устно и не сохранены. Скажи где искать, или подтверди что это были красиво звучащие, но не имеющие основы связки от внешнего LLM (тот же паттерн, что в 100-problem каталоге — реальные источники, шаблонные bridge-claims).

---

## Рекомендуемый порядок работы

1. Прочитать `00-catalog/Open Problems Catalog — Skeptic Assessment` — как вообще относиться к каталогу
2. Прочитать `01-cross-domain-bridges/Cross-Domain Bridge Lab — Project.md` целиком — полный разбор мостов
3. Запустить Phase 1a код (2 минуты) — sanity-check RMT-инфраструктуры
4. Определиться по Frontier R&D / TOFT / RAF — реальны или нет
5. Переиспользовать `03-methodology-rules/` при каждом новом эксперименте — не изобретать заново

---

*README создан: 2026-09-06. Vault остаётся source of truth — обновляй оба места при существенных изменениях.*
