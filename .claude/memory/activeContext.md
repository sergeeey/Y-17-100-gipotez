# activeContext.md — Y-17 100 gipotez

## Scope Fence
- **Goal:** [PLAN, не факт] Оценить и начать проверку cross-domain мостов между каталогом ~141 открытых научных задач и реальными проектами (H-7 chromatin, ChernoffPy, May 1972)
- **Boundary:** Эта папка + чтение (не запись) в исходный vault `C:\Users\serge\.claude\memory\` при необходимости сверки
- **Done when:** Хотя бы один мост прошёл полный цикл kill-criterion → эксперимент → KILLED/CONFIRMED/LEAD
- **NOT NOW:** Frontier R&D / TOFT / RAF — заблокированы до подтверждения существования; полный Hypothesis Portfolio (128+ гипотез из ARCHCODE и др.) — отдельный, не связанный проект





## Current Focus
[summarized] **B1/B2/B3 arc (H-B3-1 through H-B3-1k, ADR-010–027) archived to
[summarized] **H-B7-7 through H-B7-12 (ADR-034–039) archived to
[summarized] **[WS: B3 case-study thread continued] CLOSED 2026-09-07 (ADR-040, прямой запрос пользователя

  Windermere пересекает 6/7 (как позитивы); настоящие выбросы — Paul_doSat (7/7) и Paul_chl/
  Paul_pH (3/7 каждый). Частота НЕ коррелирует с ролью positive/negative.
- Тест тренда (Paul lake, 3 переменные) → **REJECTED, развёрнут наоборот**: pH — сильнейший тренд
  (ρ=-0.579, p≈3e-31), но наименьшая частота; doSat — тренда нет (p=0.42), но частота максимальна.
- Тест автокорреляции lag-1 → **WEAK**: направление совпадает с предсказанием дважды (n=9 и
  n=6 контролируемых по частоте), но не значимо ни разу.
- Граф: `B3-MAY-TDA` session_summary_2026-09-07 добавлен (correction, не тихая правка). Вердикт
  `H-B3-1h` не изменён (остаётся `lead`). 5 новых тестов, все прошли.
- **Post-commit reviewer catch (per собственный 3+-файлов чек-лист):** нашёл реальный P1 —
  `approx_n_seasons` всегда возвращал 1 (диффил намеренно сжатую `season_time`). Не был load-bearing
  ни в одном выводе. Исправлен независимым пересчётом границ сезона из сырой decimal-year оси
  (`count_seasons`), даёт корректные `n_seasons=3`. Regression test добавлен, 185 тестов проходят.
- **Addendum 5 (продолжение автономно, `/loop`):** Peter lake replicate — направление тренд-инверсии
  реплицировалось НЕЗАВИСИМО на второй, качественно другой по форме ветке (pH — сильнейший тренд И
  наименьшая частота на ОБОИХ озёрах, несмотря на разную форму спектра частот). Формальный
  объединённый тест (n=6) остаётся незначимым — тот же набор данных, не новая мощность. Побочно:
  |trend| и AC1 сами ранг-коррелированы — возможно, одна ось нестационарности, не два кандидата.
**[WS: B3 case-study thread continued] CLOSED.**

**[WS: B2 coupling sweep, `/loop` continued] H-B2-1h (ADR-042):** 10-точечный скан
`coupling_magnitude ∈ {3..30}` для M1 (H-B2-1g's own named next step). Provenance побитово
проверен против H-B2-1f (M1=2.665) и H-B2-1g (M1=158.93). **CONFIRMED** экспоненциальный рост
(raw-NLS R²=0.9994 vs квадратичная 0.951 vs линейная 0.680) — но только после самопойманной
ошибки: первая версия сравнивала log-space R² экспоненты с raw-space R² альтернатив (разные
loss), исправлено переподбором через `scipy.optimize.curve_fit`. Caveat задокументирован, не
подавлен: consecutive ratios M1[i+1]/M1[i] монотонно убывают (3.76→1.80) — рост замедляется,
хотя экспонента всё равно лучшая из трёх форм. Pearl impact 7 (общий паттерн: R² на широком
динамическом диапазоне слабо ловит систематическое отклонение). 5 новых тестов, 195 всего проходят.
**[WS: B2 coupling sweep] CLOSED.**

**[WS: B2 multi-seed, `/loop` continued] H-B2-1i (ADR-043):** закрывает второй открытый вопрос
H-B2-1g's Relaxation Map — типичен ли M1=158.93 (seed=0, coupling=15) или это неудачный draw.
Ансамбль 30 сидов, Tukey-fence критерий пре-регистрирован до запуска. **MODERATE**: выше Q3
(143.97, медиана 68.97), но внутри Tukey fence (371.36 — максимум на другом сиде). Распределение
право-скошено (mean 109.14 > median 68.97, диапазон 15.00–371.36 при фиксированных eigenvalues/
coupling). Честный вердикт сохранён (не округлён до TYPICAL/OUTLIER). 4 новых теста, 199 всего.
**[WS: B2 multi-seed] CLOSED.**

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
- [2026-09-07 07:55] `782ae01` (local, branch `feature/h-b2-1i-multiseed` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): H-B2-1i: 30-seed ensemble at coupling=15 closes H-B2-1g's open question -- M1=158.93 is MODERATE
- [2026-09-07 07:48] `9d5a9bc` (local, branch `feature/auto-log-5b1c9b8` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): chore: auto-log commit history entry
- [2026-09-07 07:48] `5b1c9b8` (local, branch `feature/h-b2-1h-coupling-sweep` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): H-B2-1h: coupling-magnitude sweep CONFIRMS exponential M1 growth, self-caught R^2 loss-mismatch first
- [2026-09-07 07:32] `b31db36`: chore: auto-log commit history entry
- [2026-09-07 07:32] `e826359` (local, branch `feature/b3-peter-lake-replicate` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): B3 Addendum 5: Peter lake replicate confirms trend-inversion direction independently
- [2026-09-07 07:14] `c49c0a2`: chore: auto-log commit history entry
- [2026-09-07 07:13] `cf68944` (local, branch `feature/b3-crosstab-correction-and-paul-lake-analysis` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs: note reviewer-caught fix in activeContext.md
- [2026-09-07 07:13] `7ed5ea3` (local, branch `feature/b3-crosstab-correction-and-paul-lake-analysis` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): fix: approx_n_seasons always returned 1, reviewer-caught before push
- [2026-09-07 07:05] `b44f9b2` (local, branch `feature/b3-crosstab-correction-and-paul-lake-analysis` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): B3: fix provenance drift, correct a wrong crossing-rate claim, test 2 new candidates
- [2026-09-07 01:52] `fbb382b`: chore: auto-log commit history entry
- [2026-09-07 01:51] `da0e337` (local, branch `feature/h-b7-12-crossbranch-transient` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): H-B7-12: transient sweep on second branch WEAKENED -- exact k*=5 match was branch equivalence
- [2026-09-07 01:33] `8ce0ff7`: chore: auto-log commit history entry
- [2026-09-07 01:32] `6343a11` (local, branch `feature/h-b7-11-crossbranch` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): H-B7-11: cross-branch generalization CONFIRMED, incidentally caught H-B7-4's branch-count error
- [2026-09-07 01:01] `6788722`: chore: auto-log commit history entry
- [2026-09-07 01:00] `c24b243` (local, branch `feature/h-b7-10-transient-sweep` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): H-B7-10: fine duration sweep pins exact threshold k*=5, fully traced to a 1-step race condition
