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

уверенность выросла (ADR-061).** Сиды увеличены 15→40 при N_DIM≥16 (граница из самих данных:
N=12 значим, N=16 первый незначимый). Результат: точечные оценки СДВИНУЛИСЬ К НУЛЮ, не к
значимости (N=16: -0.225→-0.012; N=50: 0.504→0.298) — сигнатура шума, регрессирующего к
истинному нулю, а не недодетектированного эффекта. Тренд затухания сам стал значим (p=0.042).
Свидетельство теперь склоняется к H1 (генуинный слом κ(V) как дескриптора при большом N), не к
H2 (просто мощность). Первичный вопрос моста B2 сместился со статистического на механистический:
что управляет M1, когда κ(V) уже недостаточно. 2 новых теста. **[WS: power follow-up] CLOSED.**

**[WS: H-B2-1n, «продолжай автономно» после power follow-up] WEAKENED + exploratory сигнал,
честно отгорожен (ADR-062).** Первый целевой тест альтернативы: numerical abscissa ω(A) на
идентичной популяции H-B2-1m. WEAKENED по критерию (1/5 значим), но ВСЕ 5 срезов положительны
(у κ(V) 2 были отрицательны) — материально консистентнее. Exploratory (вычислено после
незначимых срезов, по Anti-Overfitting Gate НЕ меняет вердикт): Fisher-комбинация p=0.013,
знаковая консистентность p=0.0625. Skeptic CONFIRMED-REAL: стена от вердикта алгоритмически
реальна (verdict вычисляется до combine_pvalues), но предупредил — «нарративно пориста»,
явный guardrail добавлен. Новый предрегистрированный подтверждающий тест (свежие сиды, Fisher
как первичный критерий) НЕ запущен автоматически — по собственной дисциплине сессии против
автоцепочки. **[WS: H-B2-1n] CLOSED.**

**[WS: H-B2-1o, прямая команда пользователя «запусти подтверждающий тест на свежих сидах итд
все по очереди автономно»] CONFIRMED по букве, но сужен skeptic'ом (ADR-063).** Предрегистрированный
подтверждающий тест: сиды 40-99 (0 пересечения с H-B2-1n), Fisher — первичный критерий с самого
начала. Fisher p=0.0019 → CONFIRMED. Skeptic `[WEAKENED]`: 99.4% сигнала — от 3/5 срезов
(N=16,24,32); N=40,50 дают ρ=0.007 дважды (не слабее — неотличимо от нуля). Post-hoc
partial-conjunction (k=3/5, отгорожен как и Fisher в H-B2-1n) даёт p=0.151 — НЕ проходит,
подтверждает возражение числом. Вырожденность m1/ω(A) на большом N проверена и исключена
(CV≈1.0/0.07). Честный вывод: сигнал реален и реплицирован, но сужен до N∈{16,24,32};
разрыв при N≥40 остаётся открытым. Новый тест N∈{64,80} назван (различил бы «невезучая пара»
от «генуинный потолок»), НЕ запущен — требует новых данных. **[WS: H-B2-1o] CLOSED.**

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
- [2026-09-07 18:41] `0f1039a` (local, branch `feature/h-b2-1o-confirmatory-fresh-seeds` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): chore: auto-log commit history entry (final)
- [2026-09-07 18:41] `4080998` (local, branch `feature/h-b2-1o-confirmatory-fresh-seeds` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): chore: auto-log commit history entry
- [2026-09-07 18:41] `af3125a` (local, branch `feature/h-b2-1o-confirmatory-fresh-seeds` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-B2-1o -- pre-registered confirmatory test of H-B2-1n's exploratory Fisher signal on fresh seeds, CONFIRMED but scoped by skeptic + partial-conjunction check
- [2026-09-07 14:10] `1a53d71` (local, branch `feature/h-b2-1n-numerical-abscissa` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): chore: auto-log commit history entry (final)
- [2026-09-07 14:10] `ad0cc76` (local, branch `feature/h-b2-1n-numerical-abscissa` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): chore: auto-log commit history entry
- [2026-09-07 14:10] `30cf4bc` (local, branch `feature/h-b2-1n-numerical-abscissa` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-B2-1n -- numerical abscissa omega(A) tested against M1 at large N_DIM, WEAKENED with a walled-off exploratory Fisher signal
- [2026-09-07 13:35] `82b5f25` (local, branch `feature/h-b2-1m-power-followup` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): chore: auto-log commit history entry (final)
- [2026-09-07 13:34] `c823896` (local, branch `feature/h-b2-1m-power-followup` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): chore: auto-log commit history entry
- [2026-09-07 13:34] `e115766` (local, branch `feature/h-b2-1m-power-followup` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): fix: H-B2-1m power follow-up -- more seeds at large N move point estimates toward zero, not toward significance
- [2026-09-07 12:54] `da584f8` (local, branch `feature/h-b2-1m-multiseed-multin` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): chore: auto-log commit history entry (final)
- [2026-09-07 12:54] `6974b5e` (local, branch `feature/h-b2-1m-multiseed-multin` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): chore: auto-log commit history entry
- [2026-09-07 12:54] `c09f7e1` (local, branch `feature/h-b2-1m-multiseed-multin` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-B2-1m -- genuinely independent multi-seed x multi-N_DIM test of kappa(V)->M1, first use of Step 0a gate
- [2026-09-07 11:53] `fed7f36` (local, branch `feature/meta-analysis-b1-b4b6-resolution` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): chore: auto-log commit history entry (final)
- [2026-09-07 11:53] `c45def5` (local, branch `feature/meta-analysis-b1-b4b6-resolution` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): chore: fix stale 'blocked pending user input' line + auto-log entry
- [2026-09-07 11:53] `be76b4b` (local, branch `feature/meta-analysis-b1-b4b6-resolution` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs: root-cause self-review's 7/7 blind spot; resolve B1 (Q-GOE-vs-GUE) and B4-B6 per user direction
