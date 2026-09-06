# activeContext.md — Y-17 100 gipotez

## Scope Fence
- **Goal:** [PLAN, не факт] Оценить и начать проверку cross-domain мостов между каталогом ~141 открытых научных задач и реальными проектами (H-7 chromatin, ChernoffPy, May 1972)
- **Boundary:** Эта папка + чтение (не запись) в исходный vault `C:\Users\serge\.claude\memory\` при необходимости сверки
- **Done when:** Хотя бы один мост прошёл полный цикл kill-criterion → эксперимент → KILLED/CONFIRMED/LEAD
- **NOT NOW:** Frontier R&D / TOFT / RAF — заблокированы до подтверждения существования; полный Hypothesis Portfolio (128+ гипотез из ARCHCODE и др.) — отдельный, не связанный проект


## Current Focus

**[WS: consistency-review] CLOSED 2026-09-06 (автономно, `reviewer` agent, read-only pass по паттерну сессии 1a).** Аудит всех 4 гипотез, добавленных сегодня (H-B3-1d/1e/1f, H-B2-1) на предмет расхождений между graph.yaml/LAB.md/null_results/pearl_registry/decisions.md: **найдена 1 находка LOW-severity** — колонка «retroscan done» в `null_results/INDEX.md` для H-B3-1c/H-B3-1d утверждала «нет зависимых узлов», но позже в ту же сессию H-B3-1d/1e/1f сослались на них как на предков (Relaxation Map/descriptive join — ожидаемо, REJECT не отменён). Исправлено: добавлена временная пометка + явное объяснение, что это не откат вердикта. Всё остальное (валидность графа, provenance 4 новых узлов, числовая консистентность между файлами, арифметика LEDGER, честность цепочки Minimal Relaxation Rule) — без замечаний.
[summarized] **[WS: lab-core] Ядро лаборатории построено (2026-09-06), вариант C (ADR-002).** Файлы: `LAB.md`,...
[summarized] **[WS: pilot-H-B1-1a] CLOSED 2026-09-06 — PROMOTE [WEAKENED].** Полный FL Full-Ladder пройден: ZSG → L0...
[summarized] **[WS: pilot-pains-automation] CLOSED 2026-09-06 — вариант C выполнен (ADR-005).** `[VERIFIED]`:
[summarized] **[WS: scoping-H-B3-1] CLOSED 2026-09-06 (ADR-006, commit `d06942a`, автономная очередь по запросу пользователя...
[summarized] **[WS: H-B1-1c] CLOSED 2026-09-06 (ADR-007, автономная очередь, пункт B).** `[VERIFIED]`:
[summarized] **[WS: merge-D-and-run-H-B3-1] 2026-09-06 (ADR-008, по подтверждению пользователя).**
[summarized] **[WS: H-B3-1b] 2026-09-06 (ADR-009, автономно по запросу «действуй максимально автономно»).** `[VERIFIED]`:

- Gate 1 ДО запуска: Mendota/Washington исключены — их дата перехода лежит ВНЕ скачанного ряда.
- **Результат:** Lower Zurich — TDA опередил classical EWS на **+24 месяца**, верное направление. Оба негативных контроля (Windermere, Loch Leven) — ложное срабатывание. `ceiling-gate` хук поймал пропущенный Step 4a → добавил AR(1)-суррогатную floor-проверку: **floor = 80–83%** ложных срабатываний БЕЗ всякого механизма → вердикт **CRITERION_INVALID** (не REJECT — жёсткое правило FL, не в null_results).
- Граф: `H-B3-1b → lead` (трёхисходная конвенция KILLED/CONFIRMED/LEAD). Rescue Review: `weak_alive`, 3 конкретных дешёвых next steps в decision.md (новый experiment ID нужен для любого — Minimal Relaxation Rule).
- Pearl (impact 8): фиксированный tau≥0.5 порог сидит на floor для экологических рядов такой длины — общий методологический паттерн.

**[WS: H-B3-1 unblocked] 2026-09-06 (ADR-010, пользователь передал файл `squealSondesMet_08to11_forOPUS.csv`).** `[VERIFIED]`:
- Gate 1 ДО запуска: идеальный баланс Peter/Paul, 5-мин шаг, минимум разрывов. Точная дата перехода — из первоисточника (PDF Carpenter 2011, day230/2010), не по памяти.
- **Сам поймал баг до decision.md:** первый прогон переиспользовал ICE-правило соседа и молча оставил только сезон 2009 (114/450 дней), пропустив переход 2010. Исправлено склейкой сезонов 2008–2010 на «сезонном» индексе времени; закреплено 5 тестами.
- **Результат:** AR(1)-пол = 45–85% на всех 6 рядов → **CRITERION_INVALID**, ВТОРОЕ независимое подтверждение находки H-B3-1b на совершенно другом датасете (контролируемый эксперимент, высокая частота vs наблюдательные данные, месячные). Peter doSat: TDA +1 день (тривиально); chl/pH — TDA не сработал вовсе; Paul (контроль) — ложное срабатывание на всех 3 переменных.
- Граф: `H-B3-1 → lead`. Pearl impact 8→**9** (кросс-датасетное подтверждение).

**[WS: H-B3-1c V1] 2026-09-06 (ADR-011, прямой запрос пользователя «реализуй V1 и перезапусти оба датасета»).** `[VERIFIED]`:
- Реализовал per-series per-timepoint AR(1)-суррогатный null (95-й перцентиль, α=0.05) взамен фиксированного tau≥0.5 — единственное изменённое допущение (Minimal Relaxation Rule). Новый узел `H-B3-1c`, родители `H-B3-1`/`H-B3-1b` не тронуты.
- **Перед полным прогоном** написал self-consistency тест (`tests/test_surrogate_null_v1.py`) — подтвердил, что правило само по себе корректно (срабатывает <50% на настоящем AR(1)-шуме, далеко от floor 45-90%).
- **Результат прогона на всех 9 рядах: 5/5 негативных контролей всё равно ложно сработали.** НЕ CRITERION_INVALID (правило работает) — **настоящий REJECT**: AR(1) слишком бедная нулевая модель для реальных «тихих» экологических рядов (внутрисезонные тренды, гетероскедастичность). Первый настоящий REJECT в проекте — записан в `null_results/H-B3-1c-lakes-tda-ews-surrogate-null-v1.md` с полным Kill Analysis.
- `ceiling-gate` хук дал ложное срабатывание (искал строку «CRITERION_INVALID» без понимания отрицания в моей же формулировке) — задокументировано как ещё один keyword-шум.
- Rescue Review: `weak_alive`, следующий кандидат — V1' (IAAFT phase-randomized surrogate), не запущен.
- Pearl (impact 7): реальные негативные контроли не описываются AR(1) — общий методологический урок для будущих surrogate-based тестов.

**[WS: H-B3-1d V1'] CLOSED 2026-09-06 (ADR-012, прямой запрос пользователя «Реализуй V1'»).** `[VERIFIED]`:
- Реализовал IAAFT (Schreiber & Schmitz 1996) как замену AR(1) — единственное изменённое допущение (Minimal Relaxation Rule). Тонкая обёртка вокруг `v1.cmd_run()`, никакой логики не продублировано.
- **Сам поймал баг ДО первого прогона:** прямой вызов `v1.cmd_run()` из V1' молча перезаписал бы уже закоммиченный `metrics/run.json` V1. Добавлен `write_output: bool` guard, закреплён 2 регресс-тестами.
- **Перед полным прогоном:** 6 юнит-тестов (`tests/test_iaaft_v1prime.py`) независимо подтвердили корректность IAAFT (точное распределение амплитуд, ошибка спектра <10% vs AR(1)'s ~50%).
- **Результат: 5/5 негативных контролей ВСЁ РАВНО ложно сработали** — идентичный набор рядов V1, идентичный +13-дневный лид Peter doSat. НЕ «ничего не узнали»: IAAFT строго богаче AR(1) (полный спектр + точное распределение амплитуд) и всё равно не помогла → убивает «AR(1) слишком прост» как ДОСТАТОЧНОЕ объяснение, сужает диагноз к нестационарности/детерминированному внутрисезонному тренду — допущению, общему для ОБЕИХ моделей. Второй настоящий REJECT в проекте — `null_results/H-B3-1d-lakes-tda-ews-iaaft-null-v1prime.md`.
- Rescue Review: `weak_alive`, следующий кандидат V2' (detrend-then-surrogate) — теперь мотивирован ДВУМЯ независимо провалившимися стационарными нулями, не запущен.
- Pearl impact 7→**8** (сузил методологический паттерн: не просто «AR(1) недостаточен», а «любая стационарная линейная модель недостаточна»).

**[WS: H-B3-1e V2'] CLOSED 2026-09-06 (ADR-013, автономно во время отсутствия пользователя, по разрешению «продолжай автономно… ухожу на 5-6 часов»).** `[VERIFIED]`:
- Реализовал `smooth_trend()` + `detrend_surrogate()` (детренд скользящим средним, окно=25% длины ряда, → IAAFT на остатке → ретренд). Единственное изменённое допущение от V1' (Minimal Relaxation Rule).
- **Escape-point гейт ДО дорогого прогона** (по собственной рекомендации `H-B3-1d`): синтетический негативный контроль (гладкий сезонный тренд + AR(1)-шум) — чистый IAAFT даёт 87.5% ложных срабатываний, detrend+IAAFT снижает до 37.5% на ТОЙ ЖЕ синтетике. Только после подтверждения механизма запустил реальный прогон.
- **Результат: 5/5 негативных контролей всё равно ложно сработали — БАЙТ-В-БАЙТ те же 5 рядов**, что у V1 и V1' (Windermere, Loch Leven, Paul chl/pH/doSat). Три структурно разные null-модели (AR(1)/IAAFT/detrend+IAAFT) дали идентичный провал — сильнее любого отдельного REJECT: устойчиво к смене допущений о временной структуре.
- **Качественный сдвиг:** Peter doSat потерял TDA-лид (был +13 дней), Lower Zurich приобрёл (+23 месяца, близко к исходной находке H-B3-1b +24 месяца до любой null-коррекции).
- **Синтетика прошла, реальность — нет:** отдельный методологический pearl (impact 7) — пройденный escape-point на синтетике подтверждает фикс только для СМОДЕЛИРОВАННОГО механизма, не гарантирует совпадение с реальным. Третий REJECT в проекте — `null_results/H-B3-1e-lakes-tda-ews-detrend-surrogate-v2prime.md`.
- Rescue Review: `weak_alive`. Рекомендация decision.md: переходить к V3 (descriptive-only, без нового вычисления) вместо 4-й попытки null-модели — три подряд REJECT с идентичным набором ложных срабатываний указывают на проблему самой бинарной рамки, не конкретной null-модели.

**[WS: H-B2-1 Chernoff-NeuralODE] CLOSED 2026-09-06 (ADR-014, автономно во время отсутствия пользователя, следующий незаблокированный пункт очереди).** `[VERIFIED]`:
- **Сам поймал фабрикат цитаты ДО начала работы:** предыдущая врезка «⚡ Урок» этой же сессии утверждала несуществующую работу Chevyrev & Friz 2022. `WebSearch` (4 запроса) не нашёл. Третий случай фабрикации в проекте, первый — в неформальном тексте, не в FL-артефакте. Pearl impact 6: gate на атрибуцию должен покрывать ЛЮБОЙ текст, не только claim.md/decision.md.
- Нашёл и прочитал ПЕРВОИСТОЧНИК вместо фабриката: Galkin & Remizov 2021 (arXiv:2104.01249) — реальная теорема о скорости сходимости формулы Чернова. `WebFetch` не смог декомпрессировать PDF (та же проблема, что дважды раньше) → `Read` постранично сработал.
- Дизайн: 1D `dx/dt=-x` (точное аналитическое решение), два блока (order-1 Euler, order-2 Taylor). Формально проверил гипотезы теоремы Чернова — выполнены (kill-критерий (a) НЕ сработал). 7 тестов (позитив/негатив/self-consistency) ДО сравнения.
- **Результат: оба блока дали эмпирический порядок сходимости на 1 больше, чем гарантирует сама теорема** (1.00/2.00 против гарантии 0/1), на 2 горизонтах T — подтверждено символьно И численно, совпадение <1%. Kill-критерий (b) сработал: теорема формально верна, но её количественная оценка систематически на порядок n слабее элементарного расчёта Тейлора.
- Floor-Ceiling (Step 4a) явно НЕ применён — обосновано как дедуктивная, не популяционная проверка (Structure-Bias Guard).
- Pearl impact 6: паттерн «гарантия m-1 против истины m» для полиномиально-усечённых функций Чернова — портативен на будущие проверки в этом и родственных (ChernoffPy) проектах.
- Граф: `H-B2-1 → killed`. Первый КИЛЛ дедуктивного (не empirical-data) эксперимента в проекте — `null_results/H-B2-1-chernoff-neuralode-1d-decay.md`.

**[WS: H-B3-1f V3 descriptive] CLOSED 2026-09-06 (ADR-015, автономно, explicitly рекомендован в H-B3-1e decision.md).** `[VERIFIED]`:
- Джойн БЕЗ нового вычисления: 4 уже посчитанных `metrics/run.json` (raw, V1, V1', V2') → одна таблица 9×4. 4 регресс-теста подтвердили дословное воспроизведение родительских чисел.
- **Находка: ранжирование по устойчивости сигнала показывает, что самый согласованный «TDA опережает classical» сигнал во ВСЁМ исследовании принадлежит НЕГАТИВНОМУ контролю** (Paul doSat, 4 из 4 методов согласны) — устойчивее, чем у 2 из 3 настоящих позитивных случаев (Peter chl/pH: 0 из 4 методов вообще находят TDA-сигнал). Это НЕ видно ни из одного отдельного REJECT — их агрегатный «5/5» не показывает, что самая уверенная ложная тревога сильнее большинства настоящих.
- Побочно: pH-переменная (оба озера) никогда не даёт TDA-сигнал ни под одним методом.
- Pearl impact 7: агрегатный счётчик ложных срабатываний может скрывать более резкую картину; такое ранжирование стоит строить РАНЬШЕ в цепочке (после 2-го REJECT, не 3-го).
- Граф: `H-B3-1f → lead`, L0 переклассифицирован в descriptive. Рекомендация: текущий пайплайн детекции исчерпан для этой популяции — нужен принципиально новый подход, не очередной параметрический вариант.

**[WS: H-B2-1 correction] CLOSED 2026-09-06 (ADR-016, автономно, `/loop`, продолжение установленной работы).** `[VERIFIED]`:
- После `/loop` вернулся к самому свежему открытому треду и продолжил читать ТОТ ЖЕ первоисточник (arXiv:2104.01249) дальше — нашёл Theorem 3.1 (главный результат, стр.15-21), из которого Theorem 1.2 (использованная изначально) — explicitly названное автором упрощение.
- Применил Theorem 3.1 к тем же полиномиальным блокам: K_j=0 легитимен (блоки ТОЧНО совпадают с усечённым рядом Тейлора), даёт `bound_m(t,n)=t^{m+1}/((m+1)!·n^m)` — порядок m, совпадающий с истинной эмпирической ошибкой (не m-1).
- **Проверено на всех 32 уже посчитанных комбинациях без нового дорогого вычисления**: граница выполняется всегда, КПД ПОСТОЯНЕН при росте n (0.368/0.050) — сигнатура точного совпадения порядка.
- Коррекция оформлена честно: старый вердикт не переписан, помечен SUPERSEDED с датированным addendum (Hindsight Distortion Gap discipline). Та же дисциплина применена к `null_results/`.
- Граф: `H-B2-1 → confirmed` (было `killed`). Pearl impact 8: новый методологический гейт «Strongest-Available-Formalization Check» — не убивать вывод об аппарате целиком, если протестировано только explicitly упрощённое следствие теоремы.
- B2 Relaxation Map row 2 (многомерный случай) — приоритет повышен.

**[WS: H-B2-1b matrix case] CLOSED 2026-09-06 (ADR-017, автономно, `/loop` продолжение установленной работы).** `[VERIFIED]`:
- Реализовал 2D симметричную матрицу A (собственные значения -1,-2, ортогональный поворот — генуинно внедиагональная). Те же полиномиальные блоки и легитимный K_j=0, что в коррекции H-B2-1. 8 тестов ДО реального сравнения.
- **Ключевая нетривиальность:** быстрое собственное значение (-2) требует вдвое мельче шага для условия M2, чем медленное — риск, который 1D-тест принципиально не мог показать.
- **Результат: механизм устоял полностью.** Порядок совпал с теорией (1.0014/2.0032), граница выполнилась во всех 16 случаях, эффективность постоянна, условие M2 выполнилось для ОБОИХ собственных значений на всех 8 n — не гарантировано заранее.
- Граф: `H-B2-1b → confirmed` (новый узел, Minimal Relaxation Rule: 1D→2D). Pearl impact 7: коррекция H-B2-1 не артефакт игрушки, переносится на базовый многомерный случай.

**[WS: H-B2-1c non-normal] CLOSED 2026-09-06 (ADR-018, автономно, `/loop`, третья подряд генерализация одного механизма).** `[VERIFIED]`:
- A=[[-1,10],[0,-2]] (несимметричная, подтверждено). M1/M2 ЧЕСТНО измерены численно (не предположены =1, как в симметричном H-B2-1b) — этот трюк был легитимен только благодаря симметрии. 8 тестов ДО сравнения.
- **Результат: механизм устоял.** Измерен реальный transient growth (M1≈2.563, M2≈2.56-2.60). Эмпирический порядок точно совпал с теорией (1.0004/2.0068). Граница выполнилась во всех 16 случаях. Эффективность постоянна (0.0076/0.0151) — сигнатура точного совпадения порядка, но константа слабее в 16-40 раз (transient growth + большая норма степеней A).
- Граф: `H-B2-1c → confirmed` (новый узел). Pearl impact 7: третья подряд успешная генерализация в одной сессии (1D→2D-симметрия→2D-несимметрия) — сильный сигнал реальности коррекции H-B2-1, не артефакта игрушки.

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
- [2026-09-06 16:24] `9da2cdc` (local, branch `feature/h-b2-1c-nonnormal` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat(H-B2-1c): Theorem-3.1/K_j=0 mechanism survives a non-normal matrix with honestly measured M1/M2
- [2026-09-06 15:53] `71cb476`: chore: auto-log commit history entry
- [2026-09-06 15:52] `51c1c3f` (local, branch `feature/h-b2-1b-matrix-case` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat(H-B2-1b): Theorem-3.1/K_j=0 mechanism confirmed in a genuine 2D matrix case
- [2026-09-06 15:20] `db77901`: chore: auto-log commit history entry
- [2026-09-06 15:19] `01d6d9d` (local, branch `feature/h-b2-1-theorem31-correction` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): fix(H-B2-1): correct KILLED -> CONFIRMED after reading the paper's actual main theorem (3.1), not just its simplified 1D corollary
- [2026-09-06 14:58] `f428e99`: chore: auto-log commit history entry
- [2026-09-06 14:57] `09269f1` (local, branch `feature/consistency-review-fix` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): fix(null_results): timestamp the stale retroscan claim for H-B3-1c/1d
- [2026-09-06 14:51] `6e1bc7a`: chore: auto-log commit history entry
- [2026-09-06 14:50] `0ec53c5`: chore: auto-log commit history entry
- [2026-09-06 14:49] `30a0e63` (local, branch `feature/h-b3-1f-descriptive-v3` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat(H-B3-1f): V3 descriptive-only join reveals the sharpest finding in bridge B3 -- with zero new compute
- [2026-09-06 14:43] `5a8b00b`: chore: auto-log commit history entry
- [2026-09-06 14:42] `4e7f269` (local, branch `feature/h-b2-1-chernoff-neuralode` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat(H-B2-1): Chernoff <-> Neural-ODE bridge formalized and tested -> KILLED (practically useless, formally valid)
- [2026-09-06 14:30] `527f6e1` (local, branch `feature/auto-log-b408879` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): chore: auto-log commit history entry
- [2026-09-06 14:30] `b408879` (local, branch `feature/h-b3-1e-v2prime` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat(H-B3-1e): V2' (detrend-then-IAAFT surrogate) implemented and run -> REJECT, identical false-positive set to V1/V1'
- [2026-09-06 14:07] `3e75d01` (local, branch `feature/auto-log-c8f5e5f` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): chore: auto-log commit history entry
