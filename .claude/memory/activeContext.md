# activeContext.md — Y-17 100 gipotez

## Scope Fence
- **Goal:** [PLAN, не факт] Оценить и начать проверку cross-domain мостов между каталогом ~141 открытых научных задач и реальными проектами (H-7 chromatin, ChernoffPy, May 1972)
- **Boundary:** Эта папка + чтение (не запись) в исходный vault `C:\Users\serge\.claude\memory\` при необходимости сверки
- **Done when:** Хотя бы один мост прошёл полный цикл kill-criterion → эксперимент → KILLED/CONFIRMED/LEAD
- **NOT NOW:** Frontier R&D / TOFT / RAF — заблокированы до подтверждения существования; полный Hypothesis Portfolio (128+ гипотез из ARCHCODE и др.) — отдельный, не связанный проект



## Current Focus
[summarized] **[WS: consistency-review] CLOSED 2026-09-06 (автономно, `reviewer` agent, read-only pass по паттерну сессии 1a).**...
[summarized] - Gate 1 ДО запуска: Mendota/Washington исключены — их дата перехода лежит ВНЕ скачанного ряда.
[summarized] **[WS: H-B3-1 unblocked] 2026-09-06 (ADR-010, пользователь передал файл `squealSondesMet_08to11_forOPUS.csv`).**...
[summarized] **[WS: H-B3-1c V1] 2026-09-06 (ADR-011, прямой запрос пользователя «реализуй V1 и перезапусти оба датасета»).**...
[summarized] **[WS: H-B3-1d V1'] CLOSED 2026-09-06 (ADR-012, прямой запрос пользователя «Реализуй V1'»).** `[VERIFIED]`:
[summarized] **[WS: H-B3-1e V2'] CLOSED 2026-09-06 (ADR-013, автономно во время отсутствия пользователя, по разрешению «продолжай...
[summarized] **[WS: H-B2-1 Chernoff-NeuralODE] CLOSED 2026-09-06 (ADR-014, автономно во время отсутствия пользователя, следующий...
[summarized] **[WS: H-B3-1f V3 descriptive] CLOSED 2026-09-06 (ADR-015, автономно, explicitly рекомендован в H-B3-1e...
[summarized] **[WS: H-B2-1 correction] CLOSED 2026-09-06 (ADR-016, автономно, `/loop`, продолжение установленной работы).**...
[summarized] **[WS: H-B2-1b matrix case] CLOSED 2026-09-06 (ADR-017, автономно, `/loop` продолжение установленной работы).**...
[summarized] **[WS: H-B2-1c non-normal] CLOSED 2026-09-06 (ADR-018, автономно, `/loop`, третья подряд генерализация одного...
[summarized] **[WS: H-B2-1d mixed spectrum + H-B2-1c formula fix] CLOSED 2026-09-06 (ADR-019, автономно, `/loop`, второе явное...
[summarized] **[WS: H-B2-1e combined stress + серия закрыта] CLOSED 2026-09-06 (ADR-020, автономно, `/loop`, пятое и финальное...
[summarized] **[WS: H-B2-1f N=8 scale-up] CLOSED 2026-09-06 (ADR-021, автономно, `/loop`, после явного «почему ты...


**[WS: H-B2-1g strong coupling — самая важная находка] CLOSED 2026-09-06 (ADR-022, автономно, `/loop`, без пауз).** `[VERIFIED]`:
- Усилил связь в 5 раз (3→15) на той же 8D конструкции H-B2-1f. 6 тестов ДО сравнения.
- **Результат: M1 взлетел до 158.93 (~60× больше, чем 2.665 при слабой связи)** — контринтуитивная находка H-B2-1f оказалась артефактом слабой связи. Граница всё равно держится (16/16), порядок точен (1.0026/2.0007), но эффективность упала до ~1.5×10⁻⁷ — формально верно, практически бесполезно.
- **Ключевой вывод серии:** валидность границы и практическая полезность — разные оси. Предыдущие числа эффективности (0.0002-0.37) были артефактом протестированных параметров, не общим свойством.
- Граф: `H-B2-1g → confirmed`. Pearl impact 9 (самый высокий за всю серию B2) — предостережение от чтения прошлых чисел как общего свойства метода.

**[WS: H-B3-1g total persistence] CLOSED 2026-09-06 (ADR-023, автономно, `/loop`, «hard branch» из H-B3-1f).** `[VERIFIED]`:
- Реализовал `betti1_total_persistence_series()` (сумма длин баров H1) в общем модуле, прокинул `tda_stat_fn` через всю цепочку V1. 2 существующих regression-теста сломались (моки не принимали новый параметр) — сразу пойманы и починены.
- **Результат: первое отклонение от идентичного 5/5 за всю серию B3.** n_false_positives=4/5 (Paul chl перестал быть ложным срабатыванием) → IMPROVED_NOT_PASS. Новая проблема: Peter pH теперь даёт TDA-сигнал с запозданием на 100 дней (раньше не срабатывал вообще).
- **Peter doSat's +13-дневный лид воспроизвёлся ИДЕНТИЧНО в 4-й раз подряд** под структурно разными методами (V1, V1', теперь V1g) — самый надёжный сигнал во всём мосте B3.
- Граф: `H-B3-1g → lead`. Pearl impact 8: ось «топологический инвариант» НЕ исчерпана (в отличие от оси «null-модель», давшей идентичный 5/5 трижды подряд) — переоткрывает мост B3 для небезосновательного дальнейшего исследования.

**[WS: H-B3-1h invariant conjunction] CLOSED 2026-09-06 (ADR-024, автономно, `/loop`, БЕЗ нового вычисления).** `[VERIFIED]`:
- Джойн уже посчитанных V1 (entropy) и V1g (total persistence) — конъюнкция «оба должны сработать». 5 тестов (поймал и исправил собственную ошибочную assumption — 3, не 5, для «entropy alone TDA-only»).
- **Результат: лучшая специфичность за всю серию B3.** 2/5 ложных срабатываний (< entropy 3/5, < total persistence 4/5). Peter doSat сохранился с идентичным лидом. Проблема Peter pH из H-B3-1g отфильтрована побочно.
- **Ключевая находка:** Loch Leven и Paul doSat теперь сопротивляются ВСЕМ методам сессии (3 null-модели + другой инвариант + конъюнкция) — самый концентрированный ложноположительный сигнал, сужает открытый вопрос до двух конкретных рядов.
- Граф: `H-B3-1h → lead`. Pearl impact 8.
- **[WS: H-B3-1h] Addendum (same day, read-only diagnostic, no new detection compute):** `[VERIFIED]`
  Relaxation Map item 2 (case study Loch Leven/Paul doSat raw data) → нашёл кандидат-механизм
  (локальный минимум дисперсии в окне crossing: var_ratio 0.259/0.151), Positive-Control
  Digitization (Gate 3) сразу опроверг — Peter doSat (доверенный TP) показывает тот же паттерн
  (var_ratio 0.297), не различает FP/TP. KILLED как объяснение именно этих двух рядов.
  Открытый вопрос (что отличает Loch Leven/Paul doSat от 3 других негативных рядов) не закрыт.
  См. `case_study_notes.md`.
- **[WS: H-B3-1h] Addendum 2 (same day):** `[VERIFIED]` проверил собственное `falsifiable_prediction`
  из pearl-записи на ВСЕХ 6 рядах серии B3, у которых вообще есть `tda_betti_crossing`
  (Windermere/Peter pH/Paul pH никогда не пересекают ни под каким методом — не из чего считать
  окно). **6/6 (100%) var_ratio < 0.5**, и у positive-роли (среднее 0.375), и у negative-роли
  (среднее 0.199) — предсказание подтверждено полностью: это структурное свойство самого правила
  expanding-Kendall-tau, не специфика Loch Leven/Paul doSat. Pearl обновлён на CONFIRMED. Заодно
  поймал и исправил собственную ошибку в `case_study_notes.md` (Paul chl ошибочно был отнесён к
  «никогда не пересекающим» — на самом деле пересекает под entropy, но не под total persistence).

**[WS: H-B3-1i IAAFT+total-persistence] CLOSED 2026-09-06 (ADR-025, автономно, `/loop`, последняя
клетка дизайна 2×2, настоящий новый compute ~25 мин).** `[VERIFIED]`:
- Заполнил четвёртую клетку {entropy,total persistence}×{AR(1),IAAFT}. 3 теста ДО запуска.
- **Формальный вердикт: REJECT** (FP=4/5, набор рядов идентичен V1g). Дисциплина: НЕ повысил до LEAD
  из-за интересной качественной находки (Anti-Overfitting Gate, verdict-shopping).
- **Главная находка (impact 9, самый высокий в серии B3):** лид Peter doSat, идентичный (+13d) в 4
  подряд структурно разных вариантах, здесь РАЗВОРАЧИВАЕТ ЗНАК на -74d (TDA теперь отстаёт). Первый
  провал самой устойчивой находки всего моста B3. Механизм FP тоже сдвинулся для 2/4 рядов (Loch
  Leven, Paul pH теперь через classical, не TDA).
- Урок: «устойчиво под N вариантами» ≠ «устойчиво» без оговорки границ протестированного пространства.
- Граф: `H-B3-1i → killed` (FL-вердикт REJECT). Pearl impact 9.
- **[WS: H-B3-1i] Addendum (same day, single-series diagnostic, дешевле полного 9-серийного прогона):**
  `[VERIFIED]` механизм разворота знака найден: реальная tau-кривая total persistence НЕ зависит
  от null-модели, зависит только ПОРОГ. При t=172d реальная tau=0.786 > AR1-порога (0.557), но <
  IAAFT-порога (0.948, локальный всплеск именно там). К t=259d tau упала до 0.564, IAAFT-порог
  просел до 0.558 — узкое позднее пересечение. IAAFT-порог не «строже в среднем» (ниже AR1 в 58%
  точек) — он зашумлённее в конкретной точке. Побочно поймал вводящую в заблуждение авто-строку
  `interpretation` в собственном скрипте (сравнивала только средние, противоречила
  `fraction_iaaft_higher<0.5`).

**[WS: B3-MAY-TDA consolidation] CLOSED 2026-09-06 (без нового compute, обновление устаревшего
узла моста).** `[VERIFIED]`:
- Узел `B3-MAY-TDA` в graph.yaml не обновлялся с изначального scoping (evidence: HYPOTHESIS) — ДО
  запуска любого из 10 экспериментов серии. Обновил на `evidence: CONFLICT` с полным консолидированным
  резюме по всем 10 экспериментам (H-B3-1…1i).
- Ось null-модели практически исчерпана для entropy (3/3 идентичны) и наполовину для total
  persistence (2/2 REJECT, но с содержательным взаимодействием — sign-flip). Оставшаяся клетка
  (detrend+IAAFT+total persistence) — низкий приоритет по CDT Protocol.
- Открытый вопрос с наивысшим приоритетом остаётся: Loch Leven/Paul doSat vs 3 других негативных
  рядов. Следующий по ценности шаг при продолжении B3: bottleneck/Wasserstein distance напрямую по
  диаграммам — принципиально другая FAMILY, не параметрический вариант.
- LAB.md обновлён (пункт L отмечен частично выполненным, добавлено консолидированное резюме).

**[WS: H-B3-1j diagram-distance] CLOSED 2026-09-06 (ADR-026, автономно, `/loop`, «hard branch»
полностью реализован, настоящий новый compute).** `[VERIFIED]`:
- Реализовал `betti1_diagram_distance_series()` (Wasserstein-2 от диаграммы окна до diagраммы-БАЗЫ,
  `persim` — уже транзитивная зависимость `ripser`, новых пакетов не нужно). 5 тестов ДО прогона.
- **Формальный вердикт: REJECT** (FP=4/5, набор рядов идентичен V1g/H-B3-1i). Дисциплина: НЕ повысил
  до LEAD (Anti-Overfitting Gate) несмотря на лучший `n_positive_cases_with_tda_lead` серии.
- **Находка (impact 8, продолжение находки H-B3-1i):** лид Peter doSat восстановлен до +11d под
  AR(1)-null'ом (близко к историческим +13d); Peter pH впервые дал интерпретируемый положительный
  лид (+2d). Разворот знака положителен под ОБЕИМИ статистиками при AR(1), отрицателен только под
  IAAFT — сужает находку H-B3-1i до вероятного эффекта NULL-МОДЕЛИ, не статистики. Предсказание для
  проверки: IAAFT+diagram-distance должен дать отрицательный лид.
- Граф: `H-B3-1j → killed` (FL-вердикт REJECT). Pearl impact 8.
- **Ревью (`reviewer` agent, т.к. правка общего модуля `obrienlakes/run.py`):** NEEDS_WORK, только
  P2, без P0/P1. Все числа в decision.md сверены с run.json — совпадают. 2 P2 устранены: (1) проверил
  reference-диаграмму на вырожденность на реальных данных всех 9 рядов — не вырождена (12-46 баров,
  Peter doSat: 46 баров); (2) добавил 6-й тест на реальных данных Peter doSat (reps=2, быстрый) —
  раньше только синтетика. 122 теста, вердикт REJECT не изменился.

**[WS: H-B3-1k IAAFT+diagram-distance] CLOSED 2026-09-06 (ADR-027, автономно, `/loop`, прямой тест
собственного предсказания из pearl-записи H-B3-1j).** `[VERIFIED]`:
- Последняя (4-я) клетка дизайна: IAAFT+diagram-distance. 3 теста ДО запуска.
- **Предсказание ОПРОВЕРГНУТО:** лид Peter doSat = +4.0d, ПОЛОЖИТЕЛЬНЫЙ (предсказывался отрицательный).
  Полная таблица 2×2: {AR1,IAAFT}×{total persistence,diagram-distance} = {+13, -74, +11, +4} —
  положителен в 3/4 клеток. Ни null-модель, ни статистика не объясняют знак в одиночку. -74d теперь
  выглядит как выброс конкретной ПАРЫ, не общий эффект.
- **Побочно:** зеркальный паттерн у Peter pH (отрицателен в 3/4 клеток) — независимое подтверждение.
- Что НЕ опровергнуто: само измерение H-B3-1i (зашумлённый IAAFT-порог в t=172d) остаётся верным как
  единичный факт — опровергнута только обобщённая гипотеза из него.
- **Методологическая ценность:** чистый цикл предсказание→тест→falsification. Усиливает
  `B3-MAY-TDA` → `evidence: CONFLICT`.
- Граф: `H-B3-1k → killed`. Pearl-запись H-B3-1j обновлена на FALSIFIED.

**[WS: H-B7-1 Kauffman cancer attractors] CLOSED 2026-09-06 (ADR-028, прямой запрос пользователя
«начинай скоупинг R6», первый выход за пределы B1/B2/B3).** `[VERIFIED]`:
- Новый мост `B7-KAUFFMAN-ATTRACTORS` — Boolean-GRN динамика, первый раз в проекте. Gate 1: нашёл
  реальную статью (Fauré et al. 2006) через WebSearch, точный `.bnet`-файл через GitHub API
  (hklarner/pyboolnet), скачал и захэшировал. Gate 3: тот же репозиторий даёт сторонний positive
  control (PyBoolNet's собственный отчёт об аттракторах).
- 7 тестов (4 на проверяемых руками синтетических сетях) ДО реального прогона.
- **Результат: CONFIRMED.** Brute-force с нуля (`boolean.py`, без `eval`) точно воспроизвёл: 2
  аттрактора, quiescent point (байт-в-байт), complex period-7, basin 512/512. Расследована и
  разрешена несостыковка в порядке переменных trapspace-строки PyBoolNet (алфавитный, не порядок
  объявления) — не списано на совпадение, проверено против биологии.
- **Важная оговорка:** это воспроизведение известного результата, НЕ проверка самой гипотезы
  Kauffman. Настоящий тест — perturbation-эксперимент (Rb=0 или p27=0 зафиксированы), следующий шаг.
- Граф: `H-B7-1 → confirmed`. Pearl impact 6.

**[WS: H-B7-2 perturbation] CLOSED 2026-09-06 (ADR-029, прямой запрос пользователя «начинай
perturbation-эксперимент», настоящий тест гипотезы Kauffman).** `[VERIFIED]`:
- Первый CAUSAL эксперимент в проекте (EstimandOps L0: do-оператор vs естественная динамика, 4
  допущения идентифицируемости тривиальны — детерминированный механизм). Переиспользовал
  верифицированные функции H-B7-1 без изменения. 6 тестов (5 на проверяемых сетях) ДО прогона.
- **do(Rb=0) → CONFIRMED [WEAKENED]:** CycD=0 сходится к НОВОМУ аттрактору периода 8 внутри CycD=0 —
  персистентное деление без фактора роста. Но это новый аттрактор, не один из 2 у невозмущённой сети
  — слабее строгой формулировки Kauffman.
- **do(p27=0) → REJECTED:** CycD=0 всё равно сходится к point attractor. Согласуется с биологией
  (Rb центральнее p27 в узле рестрикции).
- **Методологическая находка:** разграничил (a) «новый аттрактор от перманентной потери гена» vs
  (b) «патологическое состояние уже существует, достижимо временным возмущением» [строгий Kauffman,
  не проверено] — легко спутать при беглом изложении.
- Граф: `H-B7-2 → lead`. Мост `B7-KAUFFMAN-ATTRACTORS` → `evidence: CONFLICT`. Pearl impact 7.

**[WS: H-B7-3 transient perturbation] CLOSED 2026-09-06 (ADR-030, прямой запрос пользователя
«начинай transient-perturbation эксперимент», Compute-First дедукция).** `[VERIFIED]`:
- ДО новой симуляции проверил: H-B7-1 уже доказал, что у ВСЕХ 512 состояний CycD=0 РОВНО ОДИН
  аттрактор. Логический вывод: временное (отпускаемое) возмущение Rb/p27 не может дать другой
  исход — гарантировано заранее, без нового compute-дизайна.
- 6 тестов + 6 реальных симуляций (разные узлы/длительности/старты) подтвердили: **6/6 (100%)**
  вернулись к quiescent point attractor, ровно как предсказано.
- **Классификация: TASK_INFEASIBLE для строгой формулировки Kauffman в ЭТОЙ модели**, не улика
  против гипотезы — модели не хватает мультистабильности внутри одной ветки CycD.
- Сужает H-B7-2: эффект do(Rb=0) требует ПЕРМАНЕНТНОЙ фиксации, временная версия не даёт ничего.
- Граф: `H-B7-3 → confirmed` (дедукция). Мост остаётся `evidence: CONFLICT`. Pearl impact 8.

Phase 1b (H-B1-1b, хроматин) — BLOCKED: upstream `ART-TAD-AUC-0.99998` invalidated; ждёт Option A в H-7 TAD + решение `Q-GOE-vs-GUE`.

## Project State
- **Repo:** https://github.com/sergeeey/Y-17-100-gipotez — PUBLIC, created 2026-09-06, commit d50597f (initial import). [VERIFIED]
- **Excluded from public repo (.gitignore):** `H-7 GeoSpectra Lab (DIFFERENT project…).md` — third-party correspondence refs (Tom Lawrence). Local copy kept. User may override.
- **New meta-goal (2026-09-06, user):** make this an *exemplary experimental lab* — memory/structure/hypothesis-graph designed up front so a blind orchestrator can operate; use it to test the whole tool/agent/methodology stack. **Variant C chosen by user (AskUserQuestion) → ADR-002.** Every tool use → row in `tooling-eval/LEDGER.md` (25 rows after session 1: CAUGHT 6 / OK 8 / NOISE 5 / NOT-YET 6).
- **Graph validator:** `python scripts/lab_check.py` (SCHEMA invariants 1–3) + `pytest` (3 tests incl. negative control replicating the 2026-05-28 incident). Run both before every commit.
- **FL template source (reuse, don't reinvent):** `D:\Claude-cod-top-2026\experiments\_template\` (14 files) [VERIFIED]
- **Files transferred:** 15 (2026-09-06)
- **Bridges scoped:** 3 (RMT/Riemann — READY/BLOCKED split; ChernoffPy/UDE — needs formalization; May1972/TDA — ready to scope)
- **Bridges blocked pending user input:** 3 (Frontier R&D, TOFT/SMT, RAF Theory)



## Architecture (файлы этой папки)
- `00-catalog/` — источники задач (raw + verified subset + skeptic assessment)
- `01-cross-domain-bridges/` — главный рабочий файл + H-7 контекст (два разных проекта!)
- `02-related-projects-context/` — ChernoffPy, May 1972
- `03-methodology-rules/` — переиспользуемые правила (execution rules, submission gate, ESV scoring)



## Quick Commands
```bash
pip install -r requirements.txt
python scripts/lab_check.py          # graph invariants (must be OK before commit)
python -m pytest -q                  # 3 tests
python -m ruff check scripts/ tests/ # lint (line-length=100 pinned in pyproject.toml)
# LEDGER summary — count by grep, never by hand:
grep -E '^\| (2026-[0-9-]+|—) \|' tooling-eval/LEDGER.md | awk -F'|' '{gsub(/ /,"",$6); print $6}' | sort | uniq -c
```



## Open Questions (для пользователя)
1. Frontier R&D / TOFT / RAF Theory — реальны на другом компьютере, или нет?
2. Доступен ли этот E:\ путь с других ПК (тот же физический диск / сетевая шара / нет)?

---
*Создан: 2026-09-06 при переносе из Obsidian vault.*



## Auto-commit log
- [2026-09-06 22:19] `7422132`: chore: auto-log commit history entry
- [2026-09-06 22:18] `db14a3f` (local, branch `feature/h-b7-2-perturbation` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): H-B7-2: perturbation (do-operator) test of Kauffman's Cancer Attractor hypothesis -- differentiated result
- [2026-09-06 22:05] `e45a14e`: chore: auto-log commit history entry
- [2026-09-06 22:04] `242345a` (local, branch `feature/h-b7-1-kauffman-cellcycle` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): H-B7-1: first Boolean-GRN experiment (Kauffman cancer attractors) -- CONFIRMED as a reproduction
- [2026-09-06 21:05] `1a90d82`: chore: auto-log commit history entry
- [2026-09-06 21:05] `c238353` (local, branch `feature/h-b3-1k-null-model-falsified` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): H-B3-1k: null-model-effect hypothesis FALSIFIED by its own pre-registered prediction
- [2026-09-06 20:33] `5c61761`: chore: auto-log commit history entry
- [2026-09-06 20:33] `b12c6d8`: chore: record reviewer-agent verdict for H-B3-1j in activeContext.md
- [2026-09-06 20:31] `dcecb68` (local, branch `feature/h-b3-1j-review-response` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): H-B3-1j: address reviewer's two P2 findings (reference-diagram degeneracy, missing real-data regression test)
- [2026-09-06 20:24] `dedf213` (local, branch `feature/h-b3-1j-diagram-distance` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): H-B3-1j: the "hard branch" fully implemented (Wasserstein diagram-distance) -- REJECT again, but narrows H-B3-1i's finding to a null-model effect
- [2026-09-06 20:09] `00a6637`: chore: auto-log commit history entry
- [2026-09-06 20:08] `610ac08` (local, branch `feature/b3-may-tda-consolidation` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): B3-MAY-TDA: update stale bridge node with consolidated evidence from 10 experiments
- [2026-09-06 20:05] `045f082`: chore: auto-log commit history entry
- [2026-09-06 20:04] `31bf217` (local, branch `feature/h-b3-1i-sign-flip-mechanism` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): H-B3-1i: mechanism of Peter doSat's sign flip found via cheap single-series diagnostic
- [2026-09-06 19:39] `442931f`: chore: auto-log commit history entry
