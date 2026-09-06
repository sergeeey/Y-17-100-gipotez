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
  (var_ratio 0.297), не различает FP/TP. KILLED как объяснение именно этих двух рядов;
  `[HYPOTHESIS]` вероятно generic-свойство самого правила детекции, не проверено отдельно.
  Открытый вопрос (что отличает Loch Leven/Paul doSat от 3 других негативных рядов) не закрыт.
  См. `case_study_notes.md`.

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
- [2026-09-06 19:17] `4c9a795` (local, branch `feature/h-b3-1h-case-study` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): H-B3-1h Relaxation Map item 2: Loch Leven/Paul doSat case study — candidate mechanism KILLED by its own positive control
- [2026-09-06 19:10] `a236655`: chore: auto-log commit history entry (2)
- [2026-09-06 19:10] `a416670` (local, branch `feature/auto-log-7210aad` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): chore: auto-log commit history entry
- [2026-09-06 19:10] `7210aad` (local, branch `feature/h-b3-1h-conjunction` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): H-B3-1h: TDA invariant conjunction (entropy AND total-persistence) — best specificity in B3 arc
- [2026-09-06 19:02] `3751f69`: chore: auto-log commit history entry
- [2026-09-06 19:01] `6519e03` (local, branch `feature/h-b3-1g-result` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat(H-B3-1g): first non-identical-5/5 result in the entire B3 arc -> LEAD
- [2026-09-06 18:54] `98251ed`: chore: auto-log commit history entry
- [2026-09-06 18:54] `62ad1d4` (local, branch `feature/h-b3-1g-total-persistence` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat(H-B3-1g): add total-persistence TDA invariant, wire through V1's null pipeline; real run pending
- [2026-09-06 18:46] `372ef2a`: chore: auto-log commit history entry
- [2026-09-06 18:46] `afa3234` (local, branch `feature/h-b2-1g-strong-coupling` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat(H-B2-1g): 7th confirmation resolves the arc's most important finding -- bound validity != practical usefulness
- [2026-09-06 18:41] `104c300`: chore: auto-log commit history entry
- [2026-09-06 18:40] `817fb47` (local, branch `feature/h-b2-1f-nd-stiff` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat(H-B2-1f): sixth consecutive confirmation, N=8 scale-up, counterintuitive M1 finding
- [2026-09-06 18:29] `390e573`: chore: auto-log commit history entry
- [2026-09-06 18:29] `492eea1` (local, branch `feature/h-b2-1e-combined-stress` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat(H-B2-1e): combined non-normal + mixed-sign stress test closes the H-B2-1* arc at 5 confirmations
- [2026-09-06 18:23] `d65eba8`: chore: auto-log commit history entry
