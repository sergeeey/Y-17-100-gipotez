# activeContext.md — Y-17 100 gipotez

## Scope Fence
- **Goal:** [PLAN, не факт] Оценить и начать проверку cross-domain мостов между каталогом ~141 открытых научных задач и реальными проектами (H-7 chromatin, ChernoffPy, May 1972)
- **Boundary:** Эта папка + чтение (не запись) в исходный vault `C:\Users\serge\.claude\memory\` при необходимости сверки
- **Done when:** Хотя бы один мост прошёл полный цикл kill-criterion → эксперимент → KILLED/CONFIRMED/LEAD
- **NOT NOW:** Frontier R&D / TOFT / RAF — заблокированы до подтверждения существования; полный Hypothesis Portfolio (128+ гипотез из ARCHCODE и др.) — отдельный, не связанный проект




## Current Focus
[summarized] **B1/B2/B3 arc (H-B3-1 through H-B3-1k, ADR-010–027) archived to
[summarized] **[WS: H-B7-1 Kauffman cancer attractors] CLOSED 2026-09-06 (ADR-028, прямой запрос пользователя
[summarized] **[WS: H-B7-2 perturbation] CLOSED 2026-09-06 (ADR-029, прямой запрос пользователя «начинай
[summarized] **[WS: H-B7-3 transient perturbation] CLOSED 2026-09-06 (ADR-030, прямой запрос пользователя

  вернулись к quiescent point attractor, ровно как предсказано.
- **Классификация: TASK_INFEASIBLE для строгой формулировки Kauffman в ЭТОЙ модели**, не улика
  против гипотезы — модели не хватает мультистабильности внутри одной ветки CycD.
- Сужает H-B7-2: эффект do(Rb=0) требует ПЕРМАНЕНТНОЙ фиксации, временная версия не даёт ничего.
- Граф: `H-B7-3 → confirmed` (дедукция). Мост остаётся `evidence: CONFLICT`. Pearl impact 8.

**[WS: H-B7-4 remy_tumorigenesis] CLOSED 2026-09-06 (ADR-031, автономно, `/loop`, продолжение
Relaxation Map H-B7-3).** `[VERIFIED]`:
- Установил `pyboolnet` как активный инструмент (не только .bnet-файлы). Живой прогон на Fauré-сети
  → точное совпадение с H-B7-1 — апгрейд верификации до «different tool, same task» (addendum в
  H-B7-1's decision.md).
- Нашёл через `pyboolnet` реальную модель (Remy et al. 2015, рак мочевого пузыря, 35 узлов) с
  ГЕНУИННОЙ мультистабильностью — 2 ветки дают РАЗНЫЕ ФЕНОТИПЫ (Growth_arrest vs Proliferation) при
  одинаковых внешних сигналах — структура, которой не хватало Fauré-модели.
- **do(RAS=1) → REJECTED**, но ГЕНУИННО информативно (структурная предпосылка успеха существовала,
  в отличие от H-B7-3) — согласуется с multi-hit теорией канцерогенеза.
- Граф: `H-B7-4 → killed`. Мост остаётся `evidence: CONFLICT`. Pearl impact 8. Следующий шаг:
  комбинированное do(RAS=1, TP53=0).
**[WS: H-B7-4 remy_tumorigenesis] CLOSED.**

**[WS: H-B7-5 remy_tumorigenesis two-hit] CLOSED 2026-09-06 (ADR-032, прямой запрос пользователя
«начинай двухударный эксперимент»).** `[VERIFIED]`:
- `do(RAS=1, TP53=0)` на той же bistable-ветке → **REJECTED снова** (вернулось в Growth_arrest).
- Но механизм провала ПРОСЛЕЖЕН прямо против правил `.bnet`: `p21CIP=1` держится ДАЖЕ при TP53=0
  через второй, TP53-независимый дизъюнкт своего правила (`Growth_inhibitors&!CyclinE1&!AKT`),
  блокируя CyclinD1 несмотря на RAS=1.
- Структурно: ВСЕ 8 мультистабильных веток модели имеют `Growth_inhibitors=1` — резервный чекпоинт
  не специфичен одной ветке.
- Граф: `H-B7-5 → killed`. Мост остаётся `evidence: CONFLICT`. **Pearl impact 9** (самый высокий в
  серии B7). Следующий шаг: трёхударный `do(RAS=1, TP53=0, p21CIP=0)`, мотивированный найденным
  механизмом, не произвольным выбором.
**[WS: H-B7-5 remy_tumorigenesis two-hit] CLOSED.**

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
- [2026-09-06 22:54] `8fbb6a3`: chore: auto-log commit history entry
- [2026-09-06 22:54] `962403a` (local, branch `feature/active-context-archive-trim` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): chore: archive B1/B2/B3 arc from activeContext.md, trim to under the 200-line ceiling
- [2026-09-06 22:49] `167605b` (local, branch `feature/h-b7-4-remy-tumorigenesis` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): H-B7-4: installed pyboolnet, found a genuinely bistable cancer model, first structurally-capable test of Kauffman's hypothesis
- [2026-09-06 22:30] `0f92f1c`: chore: auto-log commit history entry
- [2026-09-06 22:30] `52fcdb6` (local, branch `feature/h-b7-3-transient-perturbation` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): H-B7-3: Compute-First deduction predicts the outcome before simulation -- strict Kauffman test is untestable in this model
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
