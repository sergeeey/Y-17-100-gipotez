# activeContext.md — Y-17 100 gipotez

## Scope Fence
- **Goal:** [PLAN, не факт] Оценить и начать проверку cross-domain мостов между каталогом ~141 открытых научных задач и реальными проектами (H-7 chromatin, ChernoffPy, May 1972)
- **Boundary:** Эта папка + чтение (не запись) в исходный vault `C:\Users\serge\.claude\memory\` при необходимости сверки
- **Done when:** Хотя бы один мост прошёл полный цикл kill-criterion → эксперимент → KILLED/CONFIRMED/LEAD
- **NOT NOW:** Frontier R&D / TOFT / RAF — постоянно `unverified_source` (пользователь подтвердил 2026-09-07: возможно на другой машине, доступа нет); полный Hypothesis Portfolio (128+ гипотез из ARCHCODE и др.) — отдельный, не связанный проект











## Current Focus
[summarized] **B1/B2/B3 arc (H-B3-1 through H-B3-1k, ADR-010–027) archived to `history/activeContext-archive-20260906-b1b2b3.md`**

`killed` — вопрос о механизме lag'а НЕ опровергнут, отложен только этот дешёвый метод; revival
condition назван (сравнить траекторию expanding-tau напрямую) и не выполнен. Reviewer, снова
узко скоупнутый, дал LGTM с первой попытки (уже 3-й раз подряд с этим подходом). Мост B3: 15
под-гипотез, 0 confirmed.

**[VERIFIED] H-B3-1p (автономно, третья итерация «следующая гипотеза по очереди» — H-B3-1l's
ВТОРАЯ pending-строка в pearl_registry, отдельная от H-B3-1n): симметричное правило отбора
classical-статистики ИНВЕРТИРУЕТ вердикт H-B3-1l.** 6-й skeptic-проход (2026-09-07) нашёл: код
выбирает classical-статистику РАЗНЫМИ правилами — oracle-informed («ближе к переходу») для
Lower Zurich, симметричное («раньше из двух») для негативных контролей. Пересчёт Lower Zurich
ТЕМ ЖЕ честным правилом: classical_peak стал AC1=1999.25 (точно как предсказал pearl), TDA
(2000.5) оказался ПОЗЖЕ (lead=-15.0 мес, было +50.0) — **вердикт CONFIRMED→REJECTED**.
Consistency check: негативные контроли воспроизведены ТОЧНО под пересчётом. H-B3-1l downgrade
`lead`→`killed` в графе; создана запись в `null_results/INDEX.md` с полным ретросканом (оба
потомка — H-B3-1n, H-B3-1p — уже корректно учитывают коррекцию). **НЕ затронуто:** Peter doSat's
независимый +13-месячный лид (4× реплицирован) — единственный настоящий выживший позитивный
сигнал моста B3 теперь. Мост B3: 15 под-гипотез, 0 confirmed, 8 killed. Ничего не запущено
дальше автоматически — ждёт направления пользователя.

Phase 1b (H-B1-1b, хроматин) — BLOCKED: единственный оставшийся блокер — Option A в H-7 TAD (внешняя работа, вне scope Y-17). `Q-GOE-vs-GUE` разрешён 2026-09-07 (см. ADR-059).

**[2026-09-09] Все 3 моста достигли терминального состояния — graph.yaml не содержит ни одного узла со статусом proposed/ready/needs_formalization.** Bridge 3 арка формально закрыта в `01-cross-domain-bridges/Cross-Domain Bridge Lab — Project.md` (см. правку 2026-09-09). Проверено grep'ом по `registry/graph.yaml`: 39 valid / 29 confirmed / 14 lead / 14 killed / 6 unverified_source / 6 active / 1 blocked / 1 parked / 1 hold / 1 invalidated — ни одной "готовой к запуску" гипотезы. Внешний (Codex-style) лог этой же сессии предлагал новый multi-seed×multi-N эксперимент H-B2-1l — **сознательно НЕ запущен**: пользователь сам предостерёг от немедленного 8-го эксперимента сразу после skeptic-sweep 7/7 (сильный сигнал сначала стабилизировать методологию, не производить ещё один результат), и H-B2-1l переоткрывал бы уже закрытую 2026-09-08 арку Bridge 2 без новой мотивации. B1 (Option A) и B4-B6 (unverified_source) — оба фактических вопроса пользователю, оба уже отвечены ранее и не переспрашиваются (см. `CLAUDE.md` § CRITICAL CONTEXT).

**[2026-09-09, продолжение] Bridge 8 (UDE identifiability ↔ PRJ-CHERNOFFPY) зарегистрирован proposed → в тот же день REJECTED собственным feasibility-gate.** Прямой grep реального кода (внутренний `experiments/`, внешний `E:/MarkovChains/ChernoffPy`) на torch/nn.Module/.backward()/neural/UDE/identifiab дал 0 совпадений — вся инфраструктура Bridge 2 «Neural-ODE/UDE» оказалась теоретической аналогией (Chernoff на линейном операторе), не обученной сетью. Посылка ADR-082 «общая инфраструктура — переносится код» была непроверенным [INFERRED], поданным как факт — ADR-083 фиксирует это честно как процессный урок, не заметает. Открытая задача (npj Sys Biol Appl 2025) остаётся open, отклонён только перенос через ChernoffPy; revival condition назван.

**[VERIFIED — 2026-09-09, по прямому запросу пользователя «посмотри на 100-item каталог, какие ещё есть кандидаты»] Полный обзор каталога по кластерам, сопоставленным с реальной инфраструктурой.** Топ-кандидат — Numerical Linear Algebra (#36-47, Amsel et al. arXiv:2602.05394, Simons Workshop, 36 авторов, реальность подтверждена WebSearch) — прямое совпадение с рабочим псевдоспектральным кодом Bridge 2. На этот раз применена дисциплина, которой не хватило Bridge 8: **полный текст первичного источника прочитан через `mcp__arxiv__*` ДО регистрации в graph.yaml, не после.** Оба проверенных под-кандидата отклонены БЕЗ единой записи в graph.yaml: #39 (Deterministic Pseudospectral Shattering, Problem 3.1) — вопрос СУЩЕСТВОВАНИЯ универсального детерминированного алгоритма, не эмпирически тестируем конечным числом матриц; #43 (injections vs OSE, Problems 5.1/5.2) — статья САМА (v3, апдейт 20 августа 2026, РАНЬШЕ заявленной даты каталога 6 сентября) уже документирует ОТРИЦАТЕЛЬНЫЙ ответ (Townsend & Wang, arXiv:2604.10215v2) — конкретное подтверждение staleness каталога. ADR-084 + pearl_registry: theoretical-CS/чистая-математика кластеры каталога (COLT, numerical LA, вероятно RIMS topology) структурно не подходят под FL-эмпирический формат этого проекта — «Prove or disprove универсальную границу» ≠ «измерь число против порога». **Итог двух циклов поиска моста: 2 кандидата (Bridge 8, Numerical LA) проверены и отклонены с полной документацией, 0 экспериментов потрачено впустую, 0 узлов записано впустую в graph.yaml.** Домены biology/ecology/materials каталога не исследованы — открыто для будущего направления.

**[VERIFIED, побочно, честно зафиксировано]** 4 фоновых `pytest -q` прогона на весь репозиторий накопились за несколько тиков без проверки, что предыдущие ещё живы (~53 мин простоя по таймстампу goal check-in, LEDGER `MISSED`) — пользователь заметил через goal check-in раньше меня. Все 4 остановлены `TaskStop` (подтверждено ответом инструмента); частичный лог (`/tmp/pytest_full.log`) показал 0 падений на ~22% прогона — содержательных потерь нет, но урок процесса записан.

## Project State
- **Repo:** https://github.com/sergeeey/Y-17-100-gipotez — PUBLIC, created 2026-09-06, commit d50597f (initial import). [VERIFIED]
- **Excluded from public repo (.gitignore):** `H-7 GeoSpectra Lab (DIFFERENT project…).md` — third-party correspondence refs (Tom Lawrence). Local copy kept. User may override.
- **New meta-goal (2026-09-06, user):** make this an *exemplary experimental lab* — memory/structure/hypothesis-graph designed up front so a blind orchestrator can operate; use it to test the whole tool/agent/methodology stack. **Variant C chosen by user (AskUserQuestion) → ADR-002.** Every tool use → row in `tooling-eval/LEDGER.md` (25 rows after session 1: CAUGHT 6 / OK 8 / NOISE 5 / NOT-YET 6).
- **Graph validator:** `python scripts/lab_check.py` (SCHEMA invariants 1–3) + `pytest` (3 tests incl. negative control replicating the 2026-05-28 incident). Run both before every commit.
- **FL template source (reuse, don't reinvent):** `D:\Claude-cod-top-2026\experiments\_template\` (14 files) [VERIFIED]
- **Files transferred:** 15 (2026-09-06)
- **Bridges scoped:** 3, все терминальны (2026-09-09): RMT/Riemann — Phase 1a READY, 1b BLOCKED (external Option A); ChernoffPy/UDE — CONFIRMED-WITH-CAVEATS, арка H-B2-1→1v закрыта 2026-09-08; May1972/TDA — CLOSED 2026-09-09 как informative negative (0 confirmed / 8 killed / 1 parked из 15 под-гипотез), арка H-B3-1→1p
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
- [2026-09-09 01:23] `579f727` (local, branch `docs/catalog-survey-bridge9-numerical-la-ruled-out` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs: survey 100-item catalog for Bridge 9 candidates -- Numerical LA cluster ruled out via primary source
- [2026-09-09 00:31] `fec787b` (local, branch `docs/reject-bridge8-scoping-gate` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs: activeContext -- Bridge 8 registered then rejected same day by its own feasibility gate
- [2026-09-09 00:30] `b317b72` (local, branch `docs/reject-bridge8-scoping-gate` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): fix: Bridge 8's own feasibility gate rejects Bridge 8 -- proposed to rejected same day
- [2026-09-09 00:23] `bca21f4` (local, branch `chore/auto-log-20260909` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): chore: auto-log commit history entries
- [2026-09-09 00:23] `eed2648` (local, branch `docs/propose-bridge8-ude-identifiability` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs: ADR-082 + LEDGER rows for Bridge 3 closure / Bridge 8 proposal decisions
- [2026-09-09 00:22] `9d46370` (local, branch `docs/propose-bridge8-ude-identifiability` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: register Bridge 8 (UDE identifiability) as proposed, novelty/transfer gate defined upfront
- [2026-09-09 00:17] `b037322`: Merge: close Bridge 3 (May1972/TDA) arc in canonical docs
- [2026-09-09 00:17] `846a4a3` (local, branch `docs/close-bridge3-arc` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs: close Bridge 3 (May1972/TDA) arc in the canonical bridge document
- [2026-09-08 22:46] `568b4b4` (local, branch `feature/h-b2-2-resolvent-reference` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): fix: H-B2-2 -- self-review after third consecutive reviewer-agent timeout this session
- [2026-09-08 22:43] `785856e` (local, branch `feature/h-b2-2-resolvent-reference` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): fix: H-B2-2 -- move the x_floor safety check from an uncommitted scratchpad script into the committed test suite
- [2026-09-08 22:42] `dc6eac6` (local, branch `feature/h-b2-2-resolvent-reference` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-B2-2 -- direct resolvent-norm reference K_ref replaces pseudopy; ADR-077's open question closed at population scale
- [2026-09-08 22:26] `b5766d7` (local, branch `fix/h-b2-1z-correction-external-audit` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): fix: H-B2-1z correction -- external audit + independent reconfirmation falsify "convergent K(A) found"
- [2026-09-08 20:14] `ac6b74b` (local, branch `feature/h-b2-1z-kreiss-eigval-condition-anchor` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs: auto-log commit history entry
- [2026-09-08 20:14] `79fce3d` (local, branch `feature/h-b2-1z-kreiss-eigval-condition-anchor` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs: update activeContext.md with H-B2-1z's closed gap and merge status
- [2026-09-08 20:12] `fcc1362` (local, branch `feature/h-b2-1z-kreiss-eigval-condition-anchor` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): fix: H-B2-1z -- close the reviewer-flagged gap with a second independent numerical method, since Agent(reviewer) never reached a verdict
