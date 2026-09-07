# activeContext.md — Y-17 100 gipotez

## Scope Fence
- **Goal:** [PLAN, не факт] Оценить и начать проверку cross-domain мостов между каталогом ~141 открытых научных задач и реальными проектами (H-7 chromatin, ChernoffPy, May 1972)
- **Boundary:** Эта папка + чтение (не запись) в исходный vault `C:\Users\serge\.claude\memory\` при необходимости сверки
- **Done when:** Хотя бы один мост прошёл полный цикл kill-criterion → эксперимент → KILLED/CONFIRMED/LEAD
- **NOT NOW:** Frontier R&D / TOFT / RAF — заблокированы до подтверждения существования; полный Hypothesis Portfolio (128+ гипотез из ARCHCODE и др.) — отдельный, не связанный проект




## Current Focus
[summarized] **B1/B2/B3 arc (H-B3-1 through H-B3-1k, ADR-010–027) archived to
[summarized] **H-B7-1 through H-B7-6 (ADR-028–033) archived to
`.claude/memory/history/activeContext-archive-20260907-b7-1to6.md`** — Fauré cell-cycle
reproduction/perturbation/transient (H-B7-1..3, TASK_INFEASIBLE for the strict claim in that small
model) → moved to Remy tumorigenesis model (H-B7-4..6, single/two/three-hit, all REJECTED but each
tracing the next mechanism precisely, ending with `Growth_arrest = p21CIP|RBL2|RB1` found as an
explicit source-level OR gate).

[summarized] **H-B7-7 through H-B7-12 (ADR-034–039) archived to
`.claude/memory/history/activeContext-archive-20260907-b7-7to12.md`** — four-hit CONFIRMED (first
escape) → necessity-minimized to two-hit → transient CONFIRMED with exact k*=5 threshold, fully
traced to a one-step race condition → cross-branch generalization CONFIRMED then WEAKENED once the
skeptic found the two branches dynamically equivalent, closing the question by exhaustion. Bridge
`B7-KAUFFMAN-ATTRACTORS` net position: `evidence: CONFLICT` throughout.

**[WS: B3 case-study thread continued] CLOSED 2026-09-07 (ADR-040, прямой запрос пользователя
«займись B3»).** `[VERIFIED]`:
- Нашёл provenance drift: pearl-запись про case-study Loch Leven/Paul doSat помечена «pending»,
  хотя фактически завершена в прошлой сессии — исправлено немедленно.
- **Более серьёзное:** сама формулировка decision.md «3 ряда никогда не пересекают» — ФАКТИЧЕСКИ
  НЕВЕРНА. Полная cross-tab (7 методов × 9 рядов, из реальных committed metrics) показывает:
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
**[WS: B3 case-study thread continued] CLOSED.**

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
- [2026-09-07 07:13] `cf68944` (local, branch `feature/b3-crosstab-correction-and-paul-lake-analysis` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs: note reviewer-caught fix in activeContext.md
- [2026-09-07 07:13] `7ed5ea3` (local, branch `feature/b3-crosstab-correction-and-paul-lake-analysis` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): fix: approx_n_seasons always returned 1, reviewer-caught before push
- [2026-09-07 07:05] `b44f9b2` (local, branch `feature/b3-crosstab-correction-and-paul-lake-analysis` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): B3: fix provenance drift, correct a wrong crossing-rate claim, test 2 new candidates
- [2026-09-07 01:52] `fbb382b`: chore: auto-log commit history entry
- [2026-09-07 01:51] `da0e337` (local, branch `feature/h-b7-12-crossbranch-transient` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): H-B7-12: transient sweep on second branch WEAKENED -- exact k*=5 match was branch equivalence
- [2026-09-07 01:33] `8ce0ff7`: chore: auto-log commit history entry
- [2026-09-07 01:32] `6343a11` (local, branch `feature/h-b7-11-crossbranch` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): H-B7-11: cross-branch generalization CONFIRMED, incidentally caught H-B7-4's branch-count error
- [2026-09-07 01:01] `6788722`: chore: auto-log commit history entry
- [2026-09-07 01:00] `c24b243` (local, branch `feature/h-b7-10-transient-sweep` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): H-B7-10: fine duration sweep pins exact threshold k*=5, fully traced to a 1-step race condition
- [2026-09-07 00:44] `b1d13a6`: chore: auto-log commit history entry
- [2026-09-07 00:43] `a9a159a` (local, branch `feature/h-b7-9-transient-necessity` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): H-B7-9: transient do(p21CIP=0, RBL2=0) CONFIRMED for k=10,30, first strict-Kauffman confirmation
- [2026-09-07 00:09] `f2460d2`: chore: auto-log commit history entry
- [2026-09-07 00:08] `5636812` (local, branch `feature/h-b7-8-necessity-test` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): H-B7-8: necessity test do(p21CIP=0, RBL2=0) without RAS/TP53 CONFIRMED, skeptic pass passed
- [2026-09-06 23:54] `a8c76a4`: chore: auto-log commit history entry
- [2026-09-06 23:53] `fd6c1e9` (local, branch `feature/h-b7-7-fourhit-perturbation` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): H-B7-7: four-hit do(RAS=1, TP53=0, p21CIP=0, RBL2=0) CONFIRMED, skeptic pass (Step 8a) passed
