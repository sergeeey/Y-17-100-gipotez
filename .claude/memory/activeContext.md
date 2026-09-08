# activeContext.md — Y-17 100 gipotez

## Scope Fence
- **Goal:** [PLAN, не факт] Оценить и начать проверку cross-domain мостов между каталогом ~141 открытых научных задач и реальными проектами (H-7 chromatin, ChernoffPy, May 1972)
- **Boundary:** Эта папка + чтение (не запись) в исходный vault `C:\Users\serge\.claude\memory\` при необходимости сверки
- **Done when:** Хотя бы один мост прошёл полный цикл kill-criterion → эксперимент → KILLED/CONFIRMED/LEAD
- **NOT NOW:** Frontier R&D / TOFT / RAF — постоянно `unverified_source` (пользователь подтвердил 2026-09-07: возможно на другой машине, доступа нет); полный Hypothesis Portfolio (128+ гипотез из ARCHCODE и др.) — отдельный, не связанный проект









## Current Focus
[summarized] **B1/B2/B3 arc (H-B3-1 through H-B3-1k, ADR-010–027) archived to `history/activeContext-archive-20260906-b1b2b3.md`**
[summarized] репликацией — H-B2-1p был drawer-selection). ω(A), как и κ(V), имеет реальный потолок между
[summarized] **[Полный ход H-B2-1r→1s→1t (WEAKENED-фикс→CONFIRMED→CONFIRMED сильнее) archived to
[summarized] **[Итог: pseudospectral abscissa дважды независимо реплицирована, ADR-069]** CONFIRMED на

**[Полный ход H-B2-1u→1v→Step2→1w→1x→1y (MECHANISM_VERIFIED→cross-validated→docs closed→
K_MODEL_WINS→robustness→ARTIFACT_HYPOTHESIS_SUPPORTED) archived to
`history/activeContext-archive-20260908-kreiss-mechanism-and-predictor-arc.md`]**

**[VERIFIED] [Итог: пользовательский 3-priority план ПОЛНОСТЬЮ ВЫПОЛНЕН + Option B закрыт,
ADR-070…075]** Теорема Крейса верифицирована на 20 матрицах, дважды независимо cross-validated
через `pseudopy`, канонический документ моста B2 обновлён (`CONFIRMED-WITH-CAVEATS`). Первый
predictive-tier результат арки: K(A)-модель решительно предсказывает M1 точнее established
alpha_eps-корреляции и наивного теоретического потолка на held-out данных (H-B2-1w,
`K_MODEL_WINS`, устояло при расширении выборки — H-B2-1x). **Финал (H-B2-1y):** литературный
поиск для Option B (аналитический вывод «почему K²») не нашёл прямого совпадения — вместо
подгонки цитаты пользователь выбрал дешёвую проверку альтернативы: не артефакт ли это. Прямая
проверка на 16 матрицах подтвердила — **shallow K(A) недооценивает истинную константу СИЛЬНЕЕ для
матриц с уже большим K (bias~shallow_K^1.6, до 84×), и при глубокой переоценке показатель степени
M1~K(A) падает с 2.19 до 0.72** — «квадратичный масштаб» substantially объясняется этим смещением,
не новой физикой. Option B закрыт БЕЗ построения теории. Предиктивный результат H-B2-1w не
пострадал (RMSE-победа не зависит от чистоты физического закона).

**[VERIFIED] Продолжение (H-B2-1z, автономно, по стоящей авторизации, после reflective-сообщения
пользователя о том, что «нужна сходящаяся оценка K(A), иначе физическая интерпретация мутная»):**
закрытая форма kappa(lambda_1) (Trefethen-Embree eigenvalue condition number, один вызов
eig()+inv(), БЕЗ pseudopy) даёт ИМЕННО эту сходящуюся оценку. Проверено на 16 матрицах H-B2-1y:
kappa(lambda_1) >= deep_k в 16/16 случаях (медиана 0.989 от kappa). Mechanism Claim Gate на
отдельной малой тестовой матрице: сэмплированное отношение сходится к kappa(lambda_1) в пределах
0.02% на достижимом sweet spot (eps~5e-5), затем РАЗВОРАЧИВАЕТСЯ (численный floor, подтверждён
non-determinism между двумя идентичными прогонами на самых мелких eps). Переподгонка M1~K(A) с
kappa(lambda_1) на ПОЛНОЙ 80-точечной выборке H-B2-1x дала показатель 0.62-0.66 — ещё дальше от
квадратичного, усиливая H-B2-1y на впятеро большей выборке. Честная оговорка: kappa(lambda_1) —
худший held-out предиктор M1 (RMSE 0.522 vs 0.365 у смещённой shallow-оценки) — предиктивная
полезность и физическая корректность остаются разными осями. **Reviewer не дошёл до вердикта
(2 попытки, обе упёрлись в лимит ходов) — закрыто self-review: независимая hand-derived формула
+ второй независимый численный метод (SVD-bisection, без pseudopy) подтвердили формулу и
уточнили природу численного floor'а (артефакт pipeline'а pseudopy, не double-precision вообще).
Смержено в main.** Ничего не запущено дальше автоматически — ждёт направления пользователя.

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
- [2026-09-08 20:14] `79fce3d` (local, branch `feature/h-b2-1z-kreiss-eigval-condition-anchor` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs: update activeContext.md with H-B2-1z's closed gap and merge status
- [2026-09-08 20:12] `fcc1362` (local, branch `feature/h-b2-1z-kreiss-eigval-condition-anchor` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): fix: H-B2-1z -- close the reviewer-flagged gap with a second independent numerical method, since Agent(reviewer) never reached a verdict
- [2026-09-08 20:04] `866627e` (local, branch `feature/h-b2-1z-kreiss-eigval-condition-anchor` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-B2-1z -- closed-form eigenvalue condition number replaces non-converging pseudospectrum sampling as the convergent K(A) anchor
- [2026-09-08 19:18] `cdb6ed3` (local, branch `feature/h-b2-1y-kreiss-bias-check` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): fix: H-B2-1y -- close 2 reviewer-found gaps, verify deep_k boundary-hit pattern directly
- [2026-09-08 18:47] `98375d1` (local, branch `feature/h-b2-1y-kreiss-bias-check` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-B2-1y -- Chernoff/Kreiss node closes Option B: K^2 exponent traced to K(A) estimate bias, sharpened not weakened
- [2026-09-08 15:23] `4a7167a` (local, branch `feature/h-b2-1x-tighter-predictor-robustness` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-B2-1x -- robustness check on H-B2-1w's K(A) exponent, sharpened not weakened
- [2026-09-08 14:14] `505a1ef` (local, branch `feature/h-b2-1w-tighter-predictor-m1` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs: log LEDGER row for verifying H-B2-1w's cross-experiment data join
- [2026-09-08 14:12] `7f9727e` (local, branch `feature/h-b2-1w-tighter-predictor-m1` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-B2-1w -- K(A)-based model decisively beats naive ceiling and established alpha_eps correlation on held-out M1 prediction
- [2026-09-08 13:40] `d05f090` (local, branch `docs/close-bridge2-arc` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs: fix stale Bridge 2 status line in activeContext.md Project State summary
- [2026-09-08 13:40] `35c0f9d` (local, branch `docs/close-bridge2-arc` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs: close Bridge 2 (Chernoff/Kreiss) arc in the canonical bridge document
- [2026-09-08 13:37] `20d3d03`: feat: H-B2-1v -- independent cross-implementation check of H-B2-1u's small-eps Kreiss growth via pseudopy
- [2026-09-08 13:28] `20d3d03` (local, branch `feature/h-b2-1v-kreiss-crossimpl-smalleps` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-B2-1v -- independent cross-implementation check of H-B2-1u's small-eps Kreiss growth via pseudopy
- [2026-09-08 13:15] `e45cec6`: fix: H-B2-1u -- address mandatory reviewer's late-arriving P1 (unconverged Kreiss eps floor)
- [2026-09-08 13:15] `e45cec6`: fix: H-B2-1u -- address mandatory reviewer's late-arriving P1 (unconverged Kreiss eps floor)
- [2026-09-08 13:15] `e45cec6`: fix: H-B2-1u -- address mandatory reviewer's late-arriving P1 (unconverged Kreiss eps floor)
