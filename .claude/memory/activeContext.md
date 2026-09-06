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

**[WS: H-B7-7 remy_tumorigenesis four-hit] CLOSED 2026-09-06 (ADR-034, прямой запрос пользователя
«начинай четырёхударный тест»).** `[VERIFIED]`:
- `do(RAS=1, TP53=0, p21CIP=0, RBL2=0)` → **CONFIRMED** — первый успешный перманентный побег из
  Growth_arrest в Proliferation во всей серии B7. Побитовое совпадение с pyboolnet-верифицированным
  PROLIFERATION_STATE.
- Независимо переподтверждено СВЕЖИМ прогоном `pyboolnet.compute_attractors()` на построенной с
  нуля сети (ноль переиспользования своего кода) — ровно 1 аттрактор, is_steady/is_univocal/
  is_faithful все yes.
- **FL Step 8a skeptic pass выполнен и пройден** (обязателен для CONFIRMED, не только REJECT):
  вердикт CONFIRMED-REAL, 5 проверок фальсификации, включая реально ЗАПУЩЕННЫЙ (не только
  предложенный) скрипт независимой проверки.
- Skeptic нашёл реальное WEAKENING: RAS/TP53 уже истинны в стартовом состоянии — реально нагруженный
  минимум — только `do(p21CIP=0, RBL2=0)`.
- Граф: `H-B7-7 → confirmed`. Мост остаётся `evidence: CONFLICT`. **Pearl impact 9.** Следующий шаг:
  тест необходимости `do(p21CIP=0, RBL2=0)` без RAS/TP53.
**[WS: H-B7-7 remy_tumorigenesis four-hit] CLOSED.**

**[WS: H-B7-8 remy_tumorigenesis necessity test] CLOSED 2026-09-07 (ADR-035, прямой запрос
пользователя «начинай тест необходимости do(p21CIP=0, RBL2=0) итд действуй автономно»).**
`[VERIFIED]`:
- `do(p21CIP=0, RBL2=0)` БЕЗ клампа RAS/TP53 → **CONFIRMED** — reaches точный Proliferation
  attractor; RAS/TP53 сами динамически осели в значения H-B7-7's клампа.
- Независимо переподтверждено СВЕЖИМ `pyboolnet.compute_attractors()` с ПОЛНОСТЬЮ нетронутыми
  правилами RAS/TP53 — ровно 1 аттрактор, побитовое совпадение. Bit-identical воспроизводимость
  тоже проверена (2 свежих прогона).
- **FL Step 8a skeptic pass снова выполнен и пройден:** CONFIRMED-REAL. Skeptic нашёл реальный,
  включённый (не отклонённый) нюанс: самоподдерживающиеся сигнальные петли ветки делают RAS=1/
  TP53=0 «естественным состоянием покоя» — смягчает, но не отменяет новизну (ни одно правило не
  тавтология входов ветки).
- Минимальный достаточный набор для этой точки установлен: `do(p21CIP=0, RBL2=0)`.
- Граф: `H-B7-8 → confirmed`. Мост остаётся `evidence: CONFLICT`. **Pearl impact 8.** Следующий
  шаг: транзиентная версия — открыта для ВСЕЙ серии B7, не только этого эксперимента.
**[WS: H-B7-8 remy_tumorigenesis necessity test] CLOSED.**

**[WS: H-B7-9 remy_tumorigenesis transient necessity] CLOSED 2026-09-07 (ADR-036, прямой запрос
пользователя «начинай транзиентную версию»).** `[VERIFIED]`:
- Транзиентный `do(p21CIP=0, RBL2=0)` для k=1,3,10,30, затем ПОЛНОЕ освобождение к невозмущённым
  правилам → **CONFIRMED для k=10,30** — точный Proliferation attractor, персистентен после release.
- **Первое подтверждение строгой формулировки Kauffman во всей серии B7** — закрывает различие,
  названное ещё в H-B7-2's decision.md (слабое перманентное чтение vs строгое транзиентное).
- Чистый порог длительности: k=1,3 → релапс во ВТОРОЙ (не исходный) Growth_arrest fixed point.
- Независимо переподтверждено СВЕЖИМ `pyboolnet.compute_attractors()` на ПОЛНОСТЬЮ невозмущённой
  ветке (ноль клампов) — ровно 3 аттрактора, совпадают один-в-один со всеми тремя сообщёнными
  состояниями.
- **FL Step 8a skeptic pass выполнен и пройден** (третий CONFIRMED подряд, каждый со своим pass):
  CONFIRMED-REAL; skeptic предсказал k=0 → period-2 осцилляцию БЕЗ возможности запустить —
  подтверждено точно основной сессией.
- Граф: `H-B7-9 → confirmed`. Мост остаётся `evidence: CONFLICT`. **Pearl impact 9.** Следующий
  шаг: тонкий скан k=4..9; кросс-ветка проверка на другой мультистабильной ветке.
**[WS: H-B7-9 remy_tumorigenesis transient necessity] CLOSED.**

**[WS: H-B7-10 remy_tumorigenesis transient sweep] CLOSED 2026-09-07 (ADR-037, прямой запрос
пользователя «запусти скан k=4..9»).** `[VERIFIED]`:
- Точный скан k=4..9 → **CONFIRMED, k*=5 ТОЧНО**: k=4 релапс во второй Growth_arrest fixed point,
  k=5..9 все достигают точного Proliferation attractor.
- **Полная пошаговая трассировка объясняет порог ДО ОТДЕЛЬНОГО синхронного шага**: гонка между
  освобождением клампа и самоподдерживающейся активацией CyclinE1 — при k=4 CyclinE1 включается В
  ТОТ ЖЕ шаг, когда p21CIP/RBL2 возвращаются к True при освобождении; при k=5 CyclinE1 включается
  на шаг раньше, p21CIP/RBL2 на шаге освобождения уже видят CyclinE1=True.
- **FL Step 8a skeptic pass выполнен и пройден** (пятый CONFIRMED подряд, каждый со своим pass):
  CONFIRMED-REAL; hand-verified оба граничных состояния против всех 35 правил `.bnet`.
- Граф: `H-B7-10 → confirmed`. Мост остаётся `evidence: CONFLICT`. **Pearl impact 8.** Следующий
  шаг: тот же скан с другой стартовой точки; кросс-ветка проверка.
**[WS: H-B7-10 remy_tumorigenesis transient sweep] CLOSED.**

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
- [2026-09-07 01:00] `c24b243` (local, branch `feature/h-b7-10-transient-sweep` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): H-B7-10: fine duration sweep pins exact threshold k*=5, fully traced to a 1-step race condition
- [2026-09-07 00:44] `b1d13a6`: chore: auto-log commit history entry
- [2026-09-07 00:43] `a9a159a` (local, branch `feature/h-b7-9-transient-necessity` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): H-B7-9: transient do(p21CIP=0, RBL2=0) CONFIRMED for k=10,30, first strict-Kauffman confirmation
- [2026-09-07 00:09] `f2460d2`: chore: auto-log commit history entry
- [2026-09-07 00:08] `5636812` (local, branch `feature/h-b7-8-necessity-test` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): H-B7-8: necessity test do(p21CIP=0, RBL2=0) without RAS/TP53 CONFIRMED, skeptic pass passed
- [2026-09-06 23:54] `a8c76a4`: chore: auto-log commit history entry
- [2026-09-06 23:53] `fd6c1e9` (local, branch `feature/h-b7-7-fourhit-perturbation` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): H-B7-7: four-hit do(RAS=1, TP53=0, p21CIP=0, RBL2=0) CONFIRMED, skeptic pass (Step 8a) passed
- [2026-09-06 23:26] `f8c36d2`: chore: auto-log commit history entry
- [2026-09-06 23:25] `e2e6779` (local, branch `feature/h-b7-6-threehit-perturbation` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): H-B7-6: three-hit do(RAS=1, TP53=0, p21CIP=0) REJECTED, full mechanism found and verified two ways
- [2026-09-06 23:12] `23fd3a2`: chore: auto-log commit history entry (2)
- [2026-09-06 23:12] `5fbe68f` (local, branch `feature/auto-log-e9ce2d2` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): chore: auto-log commit history entry
- [2026-09-06 23:11] `e9ce2d2` (local, branch `feature/h-b7-5-twohit-perturbation` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): H-B7-5: two-hit do(RAS=1, TP53=0) REJECTED again, but the failure mechanism is traced and named
- [2026-09-06 22:54] `8fbb6a3`: chore: auto-log commit history entry
- [2026-09-06 22:54] `962403a` (local, branch `feature/active-context-archive-trim` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): chore: archive B1/B2/B3 arc from activeContext.md, trim to under the 200-line ceiling
- [2026-09-06 22:49] `167605b` (local, branch `feature/h-b7-4-remy-tumorigenesis` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): H-B7-4: installed pyboolnet, found a genuinely bistable cancer model, first structurally-capable test of Kauffman's hypothesis
