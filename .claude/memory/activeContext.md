# activeContext.md — Y-17 100 gipotez

## Scope Fence
- **Goal:** [PLAN, не факт] Оценить и начать проверку cross-domain мостов между каталогом ~141 открытых научных задач и реальными проектами (H-7 chromatin, ChernoffPy, May 1972)
- **Boundary:** Эта папка + чтение (не запись) в исходный vault `C:\Users\serge\.claude\memory\` при необходимости сверки
- **Done when:** Хотя бы один мост прошёл полный цикл kill-criterion → эксперимент → KILLED/CONFIRMED/LEAD
- **NOT NOW:** Frontier R&D / TOFT / RAF — заблокированы до подтверждения существования; полный Hypothesis Portfolio (128+ гипотез из ARCHCODE и др.) — отдельный, не связанный проект


## Current Focus
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
- [2026-09-06 14:30] `b408879` (local, branch `feature/h-b3-1e-v2prime` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat(H-B3-1e): V2' (detrend-then-IAAFT surrogate) implemented and run -> REJECT, identical false-positive set to V1/V1'
- [2026-09-06 14:07] `3e75d01` (local, branch `feature/auto-log-c8f5e5f` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): chore: auto-log commit history entry
- [2026-09-06 14:06] `c8f5e5f` (local, branch `feature/h-b3-1d-v1prime` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat(H-B3-1d): V1' (IAAFT surrogate-null) implemented and run -> REJECT, sharper diagnosis than V1
- [2026-09-06 13:34] `bbd1496`: chore: auto-log commit history entry
- [2026-09-06 13:33] `34304c3`: feat(H-B3-1c): V1 surrogate-null implemented and re-run on both datasets -> REJECT (first real one)
- [2026-09-06 13:12] `ea27a8a`: chore: auto-log commit history entry
- [2026-09-06 13:12] `acd8184`: feat(H-B3-1): unblocked by user-provided data -> CRITERION_INVALID, 2nd independent confirmation
- [2026-09-06 12:57] `c166b46`: feat(H-B3-1b): re-scoped to a reachable dataset, ran end-to-end -> CRITERION_INVALID (LEAD)
- [2026-09-06 12:32] `3d011c2`: chore(D:)+feat(H-B3-1): merge/push pilot-pains fix; H-B3-1 substrate gate BLOCKED-INFRASTRUCTURE
- [2026-09-06 12:21] `1a5cd82`: feat(H-B1-1c): known-answer test #2 CONFIRMED — closes CEILING_MISSPECIFIED from H-B1-1a
- [2026-09-06 12:13] `d06942a`: feat(scoping): H-B3-1 — replace Mangal/GloBI with Carpenter 2011 Peter/Paul Lake; honest N=1 kill-criterion
- [2026-09-06 12:00] `7baa088`: feat(lab): automate the 3 pilot pains — ceiling.md template, per-sign escape rows, ADR-005
- [2026-09-06 11:57] `ff6246c`: fix: gitignore inline comments broke hook-scratch patterns; LEDGER +1
- [2026-09-06 11:47] `ff6246c`: fix: gitignore inline comments broke hook-scratch patterns; LEDGER +1
- [2026-09-06 11:46] `c912d70`: chore: untrack hook scratch files, ignore **/.claude/state/
