# activeContext.md — Y-17 100 gipotez

## Scope Fence
- **Goal:** [PLAN, не факт] Оценить и начать проверку cross-domain мостов между каталогом ~141 открытых научных задач и реальными проектами (H-7 chromatin, ChernoffPy, May 1972)
- **Boundary:** Эта папка + чтение (не запись) в исходный vault `C:\Users\serge\.claude\memory\` при необходимости сверки
- **Done when:** Хотя бы один мост прошёл полный цикл kill-criterion → эксперимент → KILLED/CONFIRMED/LEAD
- **NOT NOW:** Frontier R&D / TOFT / RAF — постоянно `unverified_source` (пользователь подтвердил 2026-09-07: возможно на другой машине, доступа нет); полный Hypothesis Portfolio (128+ гипотез из ARCHCODE и др.) — отдельный, не связанный проект







## Current Focus
[summarized] **B1/B2/B3 arc (H-B3-1 through H-B3-1k, ADR-010–027) archived to `history/activeContext-archive-20260906-b1b2b3.md`**
[summarized] **5-й/6-й/7-й skeptic-проходы + H-B3-1m power-фикс (ADR-054–057) archived to
[summarized] **[WS: пользователь — 3 приоритета после 7/7 skeptic-скана] Мета-анализ (ADR-058) + B1/B4-B6
[summarized] **[WS: H-B2-1m, прямая команда пользователя «Запусти H-B2-1l итд»] WEAKENED, не CONFIRMED
[summarized] **[WS: H-B2-1m power follow-up, прямая команда пользователя] H1>H2, вердикт WEAKENED остаётся,

уверенность выросла (ADR-061).** Полный ход H-B2-1n→1o→1p→1q (WEAKENED→CONFIRMED-сужен→MIXED→
NOT_REPLICATED) archived to `history/activeContext-archive-20260907-b2-omega-abscissa-arc.md`.

**[Итог всей под-арки H-B2-1m→1q, ЗАВЕРШЕНА, ADR-065]** ω(A) твёрдо коррелирует с M1 при
N∈{16,32} (p<0.01); генуинный ноль на 6 значениях N от 40 до 80 на 2 независимых диапазонах
сидов (последний спорный случай, N=64, напрямую опровергнут предрегистрированной fixed-grid
репликацией — H-B2-1p был drawer-selection). ω(A), как и κ(V), имеет реальный потолок между
N=32 и N=40. Первая в сессии REJECT-запись → `null_results/INDEX.md`. Revival Condition: нужен
ДРУГОЙ дескриптор (pseudospectral abscissa названа, не протестирована) — не вариация текущей
пары.

**[Полный ход H-B2-1r→1s→1t (WEAKENED-фикс→CONFIRMED→CONFIRMED сильнее) archived to
`history/activeContext-archive-20260908-pseudospectral-verification-arc.md`]**

**[Итог: pseudospectral abscissa дважды независимо реплицирована, ADR-069]** CONFIRMED на
N=40,50 на ТРЁХ разных наборах данных подряд (H-B2-1r: сиды 0-14; H-B2-1s: та же популяция,
независимая реализация pseudopy; H-B2-1t: полностью свежие сиды 300-339) — с усилением эффекта
на каждом шаге (N=40: ρ 0.82→0.73 у своей реализации, но 0.731 на свежих данных против
исходных ρ; значимость p=8.69e-8). Comparator-аномалия (κ(V) маргинально значим при N=40 на
третьем диапазоне сидов) честно исследована через partial correlation: ω(A)-сигнал — spillover
(исчезает), κ(V)-сигнал выживает — единичное наблюдение в pearl_registry, не меняет hard_killed
статус H-B2-1q. **Priority 3 пользователя (механистический анализ: resolvent amplification →
Kreiss constant → transient growth → M1) теперь на прочной двукратно-независимой доказательной
базе, НЕ запущен — ждёт подтверждения.**

Phase 1b (H-B1-1b, хроматин) — BLOCKED: единственный оставшийся блокер — Option A в H-7 TAD (внешняя работа, вне scope Y-17). `Q-GOE-vs-GUE` разрешён 2026-09-07 (см. ADR-059).

## Project State
- **Repo:** https://github.com/sergeeey/Y-17-100-gipotez — PUBLIC, created 2026-09-06, commit d50597f (initial import). [VERIFIED]
- **Excluded from public repo (.gitignore):** `H-7 GeoSpectra Lab (DIFFERENT project…).md` — third-party correspondence refs (Tom Lawrence). Local copy kept. User may override.
- **New meta-goal (2026-09-06, user):** make this an *exemplary experimental lab* — memory/structure/hypothesis-graph designed up front so a blind orchestrator can operate; use it to test the whole tool/agent/methodology stack. **Variant C chosen by user (AskUserQuestion) → ADR-002.** Every tool use → row in `tooling-eval/LEDGER.md` (25 rows after session 1: CAUGHT 6 / OK 8 / NOISE 5 / NOT-YET 6).
- **Graph validator:** `python scripts/lab_check.py` (SCHEMA invariants 1–3) + `pytest` (3 tests incl. negative control replicating the 2026-05-28 incident). Run both before every commit.
- **FL template source (reuse, don't reinvent):** `D:\Claude-cod-top-2026\experiments\_template\` (14 files) [VERIFIED]
- **Files transferred:** 15 (2026-09-06)
- **Bridges scoped:** 3 (RMT/Riemann — READY/BLOCKED split; ChernoffPy/UDE — needs formalization; May1972/TDA — ready to scope)
- **Bridges permanently `unverified_source`** (answered 2026-09-07, not pending): 3 (Frontier R&D, TOFT/SMT, RAF Theory)







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
1. ~~Frontier R&D / TOFT / RAF Theory — реальны на другом компьютере, или нет?~~ **[VERIFIED —
   прямая цитата пользователя, 2026-09-07, эта сессия]:** "на другой машине может и раньше были
   но сейчас у меня нет доступа к этой машине". Это ПОСТОЯННОЕ, не временное состояние — B4-B6
   остаются `unverified_source` в graph.yaml без дальнейшего перефлагирования как открытого
   вопроса каждую сессию. Не строить на них выводы, но и не переспрашивать снова без новой
   информации от пользователя.
2. Доступен ли этот E:\ путь с других ПК (тот же физический диск / сетевая шара / нет)?

---
*Создан: 2026-09-06 при переносе из Obsidian vault.*







## Auto-commit log
- [2026-09-07 22:05] `53081a1` (local, branch `feature/h-b2-1s-pseudospectral-crossimpl` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): chore: auto-log commit history + verdict entries
- [2026-09-07 22:04] `92618a8` (local, branch `feature/h-b2-1s-pseudospectral-crossimpl` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): fix: H-B2-1s -- verdict logic now compares against H-B2-1r's own result, not pseudopy in isolation (reviewer P2)
- [2026-09-07 21:58] `74155cf` (local, branch `feature/h-b2-1s-pseudospectral-crossimpl` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-B2-1s -- cross-implementation check of H-B2-1r's pseudospectral abscissa via pseudopy, CONFIRMED cleanly
- [2026-09-07 21:31] `6956804` (local, branch `feature/h-b2-1r-pseudospectral-abscissa` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs: ADR-067 -- resolve Evaluator-Optimizer iteration-guard deadlock by documented manual counter reset
- [2026-09-07 21:19] `9f56f2e` (local, branch `feature/h-b2-1r-pseudospectral-abscissa` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs: downgrade stale P1 finding in approx_n_seasons to P2, by user decision
- [2026-09-07 20:48] `e00608a` (local, branch `feature/h-b2-1r-pseudospectral-abscissa` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-B2-1r -- pseudospectral abscissa CONFIRMED at N=40,50, closing the descriptor gap kappa(V)/omega(A) left open, after a self-caught bug and independent verification
- [2026-09-07 20:05] `15cf345` (local, branch `feature/h-b2-1q-fixedgrid-replication` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-B2-1q -- pre-registered fixed-grid replication resolves the H-B2-1p N=64 dispute: NOT_REPLICATED, omega(A) sub-arc closed
- [2026-09-07 19:00] `68f1371` (local, branch `feature/h-b2-1p-boundary-test` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-B2-1p -- discriminating test at N_DIM in {64,80}, MIXED, and a self-caught methodological error (retrospective FDR over adaptively-selected N) corrected in place
- [2026-09-07 18:42] `d05b5bf` (local, branch `feature/h-b2-1o-confirmatory-fresh-seeds` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): chore: auto-log commit history entry (round 5, final)
- [2026-09-07 18:41] `09a74c2` (local, branch `feature/h-b2-1o-confirmatory-fresh-seeds` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): chore: auto-log commit history entry (round 4, final)
- [2026-09-07 18:41] `757312c` (local, branch `feature/h-b2-1o-confirmatory-fresh-seeds` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): chore: auto-log commit history entry (round 3, final)
- [2026-09-07 18:41] `67efdaa` (local, branch `feature/h-b2-1o-confirmatory-fresh-seeds` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): chore: auto-log commit history entry (round 2, final)
- [2026-09-07 18:41] `0f1039a` (local, branch `feature/h-b2-1o-confirmatory-fresh-seeds` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): chore: auto-log commit history entry (final)
- [2026-09-07 18:41] `4080998` (local, branch `feature/h-b2-1o-confirmatory-fresh-seeds` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): chore: auto-log commit history entry
- [2026-09-07 18:41] `af3125a` (local, branch `feature/h-b2-1o-confirmatory-fresh-seeds` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-B2-1o -- pre-registered confirmatory test of H-B2-1n's exploratory Fisher signal on fresh seeds, CONFIRMED but scoped by skeptic + partial-conjunction check
