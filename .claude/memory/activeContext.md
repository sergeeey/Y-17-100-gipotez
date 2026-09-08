# activeContext.md — Y-17 100 gipotez

## Scope Fence
- **Goal:** [PLAN, не факт] Оценить и начать проверку cross-domain мостов между каталогом ~141 открытых научных задач и реальными проектами (H-7 chromatin, ChernoffPy, May 1972)
- **[2026-09-09, ADR-087] Scope расширен пользователем явно:** пятый источник гипотез — сам 100-item каталог напрямую, без требования тематической связи с исходными 4 якорями. Не отменяет исходные якоря, добавляет к ним.
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

**[VERIFIED — 2026-09-09, по прямому запросу пользователя «посмотри на 100-item каталог, какие ещё есть кандидаты»] Полный обзор каталога по кластерам, сопоставленным с реальной инфраструктурой.** Топ-кандидат — Numerical Linear Algebra (#36-47, Amsel et al. arXiv:2602.05394, Simons Workshop, 36 авторов, реальность подтверждена WebSearch) — прямое совпадение с рабочим псевдоспектральным кодом Bridge 2. На этот раз применена дисциплина, которой не хватило Bridge 8: **полный текст первичного источника прочитан через `mcp__arxiv__*` ДО регистрации в graph.yaml, не после.** Оба проверенных под-кандидата отклонены БЕЗ единой записи в graph.yaml: #39 (Deterministic Pseudospectral Shattering, Problem 3.1) — вопрос СУЩЕСТВОВАНИЯ универсального детерминированного алгоритма, не эмпирически тестируем конечным числом матриц; #43 (injections vs OSE, Problems 5.1/5.2) — статья САМА (v3, апдейт 20 августа 2026, РАНЬШЕ заявленной даты каталога 6 сентября) уже документирует ОТРИЦАТЕЛЬНЫЙ ответ (Townsend & Wang, arXiv:2604.10215v2) — конкретное подтверждение staleness каталога. ADR-084 + pearl_registry: theoretical-CS/чистая-математика кластеры каталога (COLT, numerical LA, вероятно RIMS topology) структурно не подходят под FL-эмпирический формат этого проекта — «Prove or disprove универсальную границу» ≠ «измерь число против порога». **[VERIFIED — 2026-09-09, автономное продолжение по Stop-hook feedback «не откладывай на пользователя»]** Отчёт закончился фразой «жду направления» — hook корректно поймал это как отложенное решение при активном /goal-условии. Продолжил без ожидания: проверил ещё 4 кандидата (#65 materials — нужна MD-симуляция, тот же разрыв что Bridge 8; #92 evolutionary population structures — источник БЕЗ авторов/журнала/DOI, проваливает Source Trace на входе; #83 single-cell embedding — реальный источник, но живой конкурентный community-бенчмарк OpenProblems.bio, непропорционален одной сессии; #96-98 neuroscience attractor landscapes — требует обучения RNN, тот же ML-разрыв). **Итог 7 кандидатов из 6 кластеров этой сессии (Bridge 8 + Numerical LA #39/#43 + эти 4): все отклонены по РАЗНЫМ, конкретно проверенным причинам** (ADR-085): 4/7 инфраструктурный разрыв (ML/симуляция), 1/7 непроверяемый источник, 1/7 proof-theoretic, 1/7 устарел, 1/7 непропорционален масштабу. Ни один узел не записан в graph.yaml впустую — feasibility проверялась ДО регистрации во всех 7 случаях. Оставшиеся непроверенные кластеры каталога (pure math, topology, quantum info, geoscience, chemistry, synthetic bio) — не исключены явно, но паттерн (математика→proof-theoretic, естественные науки→нужны реальные данные) предсказывает похожий результат.

**[VERIFIED, побочно, честно зафиксировано]** 4 фоновых `pytest -q` прогона на весь репозиторий накопились за несколько тиков без проверки, что предыдущие ещё живы (~53 мин простоя по таймстампу goal check-in, LEDGER `MISSED`) — пользователь заметил через goal check-in раньше меня. Все 4 остановлены `TaskStop` (подтверждено ответом инструмента); частичный лог (`/tmp/pytest_full.log`) показал 0 падений на ~22% прогона — содержательных потерь нет, но урок процесса записан.

**[VERIFIED — 2026-09-09] H-CAT37-1 (первый эксперимент под расширенным scope, ADR-087/088): Forsythe conjecture (restarted CG), CONFIRMED на выборке.** 2 реальных методологических бага пойманы Mechanism Claim Gate ДО claim'а: (1) жёсткий порог 1e-8 в фикс. бюджете 500 restarts ложно классифицировал 48/144 медленно-но-реально сходящихся пар как контрпримеры — исправлено log-linear decay-slope тестом; (2) сырой power-basis Крылова численно вырожден (cond(V)~1e19 при s=7) на плохо обусловленных матрицах — исправлено ортонормальным базисом Ланцоша. После обоих фиксов: 0/171 протестированных (n,mode,s,seed) пар показывают настоящий контрпример (extended-restart follow-up до 8000 restarts на оставшихся 6 кандидатах, регресс-тест `test_no_genuine_counterexample_survives_extended_restart_budget`). 12/12 тестов проходят, ruff clean. `registry/graph.yaml`: 124 узла, 145 рёбер.

**[VERIFIED — 2026-09-09] H-CAT31-1 (второй эксперимент под расширенным scope, ADR-089): Lovász theta случайных circulant graphs — CONFIRMED, содержательно, не «ожидаемо».** Снова Mechanism Claim Gate поймал реальный баг: формула θ(G)=n·(-λ_min)/(d-λ_min) для vertex-transitive графов (вспомнена по памяти, уверенно) точно совпала с известным θ(C_5)=√5 на разреженных циклах, но оказалась НЕВЕРНОЙ на плотных circulant-графах (n≥9) — подтверждено третьей независимой проверкой (дополнение графа изоморфно C_9, закрытая формула нечётного цикла + тождество θ(G)θ(Ḡ)=n совпадают с LP-реализацией, не с формулой из памяти). LP взята напрямую из Table 1 источника (arXiv:2603.29571), доверена. Отдельно: первая LP-реализация строила DFT-матрицу Python-циклом — при n=2560 не завершилась за 3+ минуты, `TaskStop`нута, векторизована. **Результат:** θ(G)/√n держится в 0.97–1.02 для n от 40 до 2560 (log-log наклон -0.035, практически плоско) — прямая численная поддержка ТОЧНОЙ гипотезы (Conjecture 18) против более слабой опубликованной верхней границы источника, реальный вклад в открытый разрыв. 6/6 тестов, ruff clean. `registry/graph.yaml`: 126 узлов, 146 рёбер.

**[VERIFIED — 2026-09-09, завершение] Весь 100-item каталог просмотрен (100/100), не только 7 кандидатов.** Ключевая переоценка scope: мандат проекта — мост именно к 4 якорям (H-7/RMT, ChernoffPy, May1972, built-инфраструктура Bridge3/7), НЕ любая дёшево вычислимая задача. Классификация: 9 пунктов (#36-47, #75-79, #88-89, #92) тематически связаны с якорем, все проверены и отклонены (ADR-083/084/085); #90-91 уже покрыты закрытием Bridge 3; **83 пункта не имеют тематической связи ни с одним якорем** — дёшевы вычислительно (#1-29, #37, #41, #44, #54, #59-60 честно), но были бы отдельной несвязанной исследовательской линией, не мостом под текущим определением. ADR-086 + pearl_registry: «дёшево ли» и «связано ли с якорем» — два раздельных обязательных условия. **Поиск моста из этого каталога под текущим scope — завершён.** Расширение scope (принять несвязанные-но-дешёвые задачи как отдельное направление) — реальный открытый вопрос, оставлен пользователю явно, не решается автономно (redefinition проекта — другой класс решения, чем выбор среди кандидатов-мостов).

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
- [2026-09-09 01:51] `6b6e8af` (local, branch `feature/h-cat37-1-forsythe-conjecture` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-CAT37-1 -- Forsythe conjecture (restarted CG) CONFIRMED on tested sample, 2 real bugs caught first
- [2026-09-09 01:32] `c60a986` (local, branch `docs/full-catalog-scan-complete` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs: activeContext -- full 100/100 catalog classification, bridge search under current scope complete
- [2026-09-09 01:32] `cd45eec` (local, branch `docs/full-catalog-scan-complete` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs: complete full 100-item catalog scan -- no remaining item fits the project's bridge definition
- [2026-09-09 01:29] `96027e2` (local, branch `docs/catalog-exhaustion-survey-part2` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs: activeContext -- 7-candidate catalog survey tally, autonomous continuation per Stop-hook
- [2026-09-09 01:28] `c285ce4` (local, branch `docs/catalog-exhaustion-survey-part2` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs: continue catalog survey autonomously per Stop-hook feedback -- 4 more candidates checked and ruled out, none registered
- [2026-09-09 01:24] `de1f095` (local, branch `docs/catalog-survey-bridge9-numerical-la-ruled-out` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): chore: auto-log commit history entries
- [2026-09-09 01:24] `77a8916` (local, branch `docs/catalog-survey-bridge9-numerical-la-ruled-out` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs: activeContext -- catalog survey findings, both Bridge 9 candidates ruled out pre-registration, background task hygiene note
- [2026-09-09 01:23] `579f727` (local, branch `docs/catalog-survey-bridge9-numerical-la-ruled-out` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs: survey 100-item catalog for Bridge 9 candidates -- Numerical LA cluster ruled out via primary source
- [2026-09-09 00:31] `fec787b` (local, branch `docs/reject-bridge8-scoping-gate` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs: activeContext -- Bridge 8 registered then rejected same day by its own feasibility gate
- [2026-09-09 00:30] `b317b72` (local, branch `docs/reject-bridge8-scoping-gate` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): fix: Bridge 8's own feasibility gate rejects Bridge 8 -- proposed to rejected same day
- [2026-09-09 00:23] `bca21f4` (local, branch `chore/auto-log-20260909` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): chore: auto-log commit history entries
- [2026-09-09 00:23] `eed2648` (local, branch `docs/propose-bridge8-ude-identifiability` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs: ADR-082 + LEDGER rows for Bridge 3 closure / Bridge 8 proposal decisions
- [2026-09-09 00:22] `9d46370` (local, branch `docs/propose-bridge8-ude-identifiability` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: register Bridge 8 (UDE identifiability) as proposed, novelty/transfer gate defined upfront
- [2026-09-09 00:17] `b037322`: Merge: close Bridge 3 (May1972/TDA) arc in canonical docs
- [2026-09-09 00:17] `846a4a3` (local, branch `docs/close-bridge3-arc` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs: close Bridge 3 (May1972/TDA) arc in the canonical bridge document
