# activeContext.md — Y-17 100 gipotez

## Scope Fence
- **Goal:** [PLAN, не факт] Оценить и начать проверку cross-domain мостов между каталогом ~141 открытых научных задач и реальными проектами (H-7 chromatin, ChernoffPy, May 1972)
- **Boundary:** Эта папка + чтение (не запись) в исходный vault `C:\Users\serge\.claude\memory\` при необходимости сверки
- **Done when:** Хотя бы один мост прошёл полный цикл kill-criterion → эксперимент → KILLED/CONFIRMED/LEAD
- **NOT NOW:** Frontier R&D / TOFT / RAF — заблокированы до подтверждения существования; полный Hypothesis Portfolio (128+ гипотез из ARCHCODE и др.) — отдельный, не связанный проект



## Current Focus
**B1/B2/B3 arc (H-B3-1 through H-B3-1k, ADR-010–027) archived to
`.claude/memory/history/activeContext-archive-20260906-b1b2b3.md`** — fully superseded by
`registry/graph.yaml` node/bridge statuses (source of truth) and `decisions.md` ADRs. Summary: B2
(Chernoff↔Neural-ODE) closed with 7 confirmations; B3 (May1972↔TDA) closed with 5 LEAD / 6 killed
across 11 experiments, bridge `B3-MAY-TDA → evidence: CONFLICT`. Active thread below (B7,
Kauffman cancer attractors) continues from there.

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
- [2026-09-06 20:09] `00a6637`: chore: auto-log commit history entry
- [2026-09-06 20:08] `610ac08` (local, branch `feature/b3-may-tda-consolidation` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): B3-MAY-TDA: update stale bridge node with consolidated evidence from 10 experiments
