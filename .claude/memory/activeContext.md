# activeContext.md — Y-17 100 gipotez

## Scope Fence
- **Goal:** [PLAN, не факт] Оценить и начать проверку cross-domain мостов между каталогом ~141 открытых научных задач и реальными проектами (H-7 chromatin, ChernoffPy, May 1972)
- **Boundary:** Эта папка + чтение (не запись) в исходный vault `C:\Users\serge\.claude\memory\` при необходимости сверки
- **Done when:** Хотя бы один мост прошёл полный цикл kill-criterion → эксперимент → KILLED/CONFIRMED/LEAD
- **NOT NOW:** Frontier R&D / TOFT / RAF — постоянно `unverified_source` (пользователь подтвердил 2026-09-07: возможно на другой машине, доступа нет); полный Hypothesis Portfolio (128+ гипотез из ARCHCODE и др.) — отдельный, не связанный проект








## Current Focus
[summarized] **B1/B2/B3 arc (H-B3-1 through H-B3-1k, ADR-010–027) archived to `history/activeContext-archive-20260906-b1b2b3.md`**
[summarized] уверенность выросла (ADR-061).** Полный ход H-B2-1n→1o→1p→1q (WEAKENED→CONFIRMED-сужен→MIXED→
[summarized] **[Итог всей под-арки H-B2-1m→1q, ЗАВЕРШЕНА, ADR-065]** ω(A) твёрдо коррелирует с M1 при

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
статус H-B2-1q.

**[H-B2-1u, ADR-070, «Го Priority 3, механистический анализ» — ЗАВЕРШЁН]** Прямая проверка
теоремы Крейса `K(A) <= sup_t||exp(tA)|| <= e*n*K(A)` на 20 матрицах (N=40,50, сиды 300-309).
Первый черновик дал 1/20 кажущихся нарушений ДОКАЗАННОЙ границы (seed=301,N=50) —
per kill criterion расследовано, не отчитано как есть: причина — `EPS_VALUES` черновика
никогда не пробовал малые eps, где живёт истинный супремум K(A) для этого (почти нильпотентного)
семейства матриц (11-кратный скачок ratio при eps=0.02 против 0.5-3.0). Не баг в дважды
верифицированной pseudospectral_abscissa. Исправлено (расширенный EPS_VALUES + локальная сетка) →
**MECHANISM_VERIFIED, 0/20 нарушений.** Efficiency ratio низкий по всей выборке (медиана 3.7-6.3%,
макс 31%) — граница держится, но рыхлая (известное ограничение множителя `e*n`, не дефект).
Contextualизирует, не подрывает H-B2-1r/1s/1t. Статус `lead` (теорема не «подтверждается»
данными). **Последний названный шаг текущего плана пользователя — новый эксперимент НЕ запущен,
ждёт направления.**

**[ADR-071, коррекция ПОСЛЕ мержа]** Широкий reviewer дважды упёрся в лимит ходов → смержено по
узкому reviewer'у (LGTM) → запоздавшее уведомление: широкий досчитал, `NEEDS_WORK (P1)`.
Проверено напрямую: k_estimate уперт в наименьший eps=0.02 на 20/20 матриц, без плато (скан до
eps=0.001 подтвердил — ratio растёт геометрически, не сходится). Структурный потолок grid-search,
не баг. MECHANISM_VERIFIED устоял (недооценка K только ужесточает проверку), но efficiency-числа
(включая «выброс 31%») — верхняя граница, не точные значения; «выброс» — скорее артефакт. Второй
коммит (не amend): убран мёртвый code, исправлена тестовая формула, честный caveat в decision.md.

**[Полный ход H-B2-1u→1v→Step2→1w (MECHANISM_VERIFIED→cross-validated→docs closed→K_MODEL_WINS)
archived to `history/activeContext-archive-20260908-kreiss-mechanism-and-predictor-arc.md`]**

**[VERIFIED] [Итог: пользовательский 3-priority план (cross-check → close B2 → tighter predictor)
ПОЛНОСТЬЮ ВЫПОЛНЕН, ADR-070…073]** Теорема Крейса верифицирована на 20 матрицах, дважды
независимо cross-validated через `pseudopy` (eps~1 в H-B2-1s, малые eps в H-B2-1v), канонический
документ моста B2 обновлён (`CONFIRMED-WITH-CAVEATS`), и — главный итог — **первый predictive-tier
результат арки**: K(A)-модель решительно предсказывает M1 точнее established alpha_eps-корреляции
(RMSE в 2.6× лучше) и наивного теоретического потолка (в 12.2× лучше) на генуинно held-out данных
(30 свежих сидов, pre-registered split). Подобранная эмпирическая закономерность M1~K(A)^1.94 —
конкретный кандидат для future аналитической работы (Option B), честно помечена как наблюдение,
не теорема.

**[H-B2-1x, ADR-074, «продолжай» — robustness-проверка K(A)-показателя, ЗАВЕРШЁН]** TRAIN
расширен до 80 точек, TEST — 30 новых свежих сидов (420-434). Показатель K(A) устоял и сузился:
1.943→**2.354, 95% CI [2.19,2.52]** — полностью исключает 1.0, устойчиво superlinear (механический
label `EXPONENT_SHIFTED_AWAY_FROM_2` снова вводит в заблуждение, тот же класс проблемы что в
H-B2-1v). Две честные новые находки: (1) показатель N_DIM НЕ разделим (CI включает почти ноль) —
collinearity с K(A) (corr=0.45) + всего 2 значения N_DIM; (2) больше TRAIN-данных НЕ улучшило
RMSE на свежем тесте (0.3652 vs оригинальные 0.3058) — зафиксировано как есть, не объяснено
задним числом. **Ничего не запущено дальше автоматически — ждёт направления пользователя.**

Phase 1b (H-B1-1b, хроматин) — BLOCKED: единственный оставшийся блокер — Option A в H-7 TAD (внешняя работа, вне scope Y-17). `Q-GOE-vs-GUE` разрешён 2026-09-07 (см. ADR-059).

## Project State
- **Repo:** https://github.com/sergeeey/Y-17-100-gipotez — PUBLIC, created 2026-09-06, commit d50597f (initial import). [VERIFIED]
- **Excluded from public repo (.gitignore):** `H-7 GeoSpectra Lab (DIFFERENT project…).md` — third-party correspondence refs (Tom Lawrence). Local copy kept. User may override.
- **New meta-goal (2026-09-06, user):** make this an *exemplary experimental lab* — memory/structure/hypothesis-graph designed up front so a blind orchestrator can operate; use it to test the whole tool/agent/methodology stack. **Variant C chosen by user (AskUserQuestion) → ADR-002.** Every tool use → row in `tooling-eval/LEDGER.md` (25 rows after session 1: CAUGHT 6 / OK 8 / NOISE 5 / NOT-YET 6).
- **Graph validator:** `python scripts/lab_check.py` (SCHEMA invariants 1–3) + `pytest` (3 tests incl. negative control replicating the 2026-05-28 incident). Run both before every commit.
- **FL template source (reuse, don't reinvent):** `D:\Claude-cod-top-2026\experiments\_template\` (14 files) [VERIFIED]
- **Files transferred:** 15 (2026-09-06)
- **Bridges scoped:** 3 (RMT/Riemann — READY/BLOCKED split; ChernoffPy/UDE — CONFIRMED-WITH-CAVEATS, арка H-B2-1→1v закрыта 2026-09-08; May1972/TDA — Phase 1 запущена, LEAD)
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
- [2026-09-08 14:14] `505a1ef` (local, branch `feature/h-b2-1w-tighter-predictor-m1` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs: log LEDGER row for verifying H-B2-1w's cross-experiment data join
- [2026-09-08 14:12] `7f9727e` (local, branch `feature/h-b2-1w-tighter-predictor-m1` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-B2-1w -- K(A)-based model decisively beats naive ceiling and established alpha_eps correlation on held-out M1 prediction
- [2026-09-08 13:40] `d05f090` (local, branch `docs/close-bridge2-arc` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs: fix stale Bridge 2 status line in activeContext.md Project State summary
- [2026-09-08 13:40] `35c0f9d` (local, branch `docs/close-bridge2-arc` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs: close Bridge 2 (Chernoff/Kreiss) arc in the canonical bridge document
- [2026-09-08 13:37] `20d3d03`: feat: H-B2-1v -- independent cross-implementation check of H-B2-1u's small-eps Kreiss growth via pseudopy
- [2026-09-08 13:28] `20d3d03` (local, branch `feature/h-b2-1v-kreiss-crossimpl-smalleps` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-B2-1v -- independent cross-implementation check of H-B2-1u's small-eps Kreiss growth via pseudopy
- [2026-09-08 13:15] `e45cec6`: fix: H-B2-1u -- address mandatory reviewer's late-arriving P1 (unconverged Kreiss eps floor)
- [2026-09-08 13:15] `e45cec6`: fix: H-B2-1u -- address mandatory reviewer's late-arriving P1 (unconverged Kreiss eps floor)
- [2026-09-08 13:15] `e45cec6`: fix: H-B2-1u -- address mandatory reviewer's late-arriving P1 (unconverged Kreiss eps floor)
- [2026-09-08 13:15] `e45cec6`: fix: H-B2-1u -- address mandatory reviewer's late-arriving P1 (unconverged Kreiss eps floor)
- [2026-09-08 13:15] `e45cec6`: fix: H-B2-1u -- address mandatory reviewer's late-arriving P1 (unconverged Kreiss eps floor)
- [2026-09-08 13:15] `e45cec6`: fix: H-B2-1u -- address mandatory reviewer's late-arriving P1 (unconverged Kreiss eps floor)
- [2026-09-08 12:59] `e45cec6`: fix: H-B2-1u -- address mandatory reviewer's late-arriving P1 (unconverged Kreiss eps floor)
- [2026-09-08 12:59] `e45cec6`: fix: H-B2-1u -- address mandatory reviewer's late-arriving P1 (unconverged Kreiss eps floor)
- [2026-09-08 12:59] `e45cec6`: fix: H-B2-1u -- address mandatory reviewer's late-arriving P1 (unconverged Kreiss eps floor)
