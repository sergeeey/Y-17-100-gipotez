# activeContext.md — Y-17 100 gipotez

## Scope Fence
- **Goal:** [PLAN, не факт] Оценить и начать проверку cross-domain мостов между каталогом ~141 открытых научных задач и реальными проектами (H-7 chromatin, ChernoffPy, May 1972)
- **Boundary:** Эта папка + чтение (не запись) в исходный vault `C:\Users\serge\.claude\memory\` при необходимости сверки
- **Done when:** Хотя бы один мост прошёл полный цикл kill-criterion → эксперимент → KILLED/CONFIRMED/LEAD
- **NOT NOW:** Frontier R&D / TOFT / RAF — постоянно `unverified_source` (пользователь подтвердил 2026-09-07: возможно на другой машине, доступа нет); полный Hypothesis Portfolio (128+ гипотез из ARCHCODE и др.) — отдельный, не связанный проект






## Current Focus
[summarized] **B1/B2/B3 arc (H-B3-1 through H-B3-1k, ADR-010–027) archived to `history/activeContext-archive-20260906-b1b2b3.md`**
[summarized] **[WS: B3 change-point, `/loop` continued] H-B3-1m (ADR-046):** закрывает ПОСЛЕДНИЙ пункт
[summarized] **H-B2-1j/1k/1l scale sweep + первые 4 skeptic-прохода (ADR-047–053) archived to
[summarized] **[WS: пятый skeptic-проход подряд, самый строгий] H-B2-1h REJECTED (ADR-054):** skeptic на

**математический факт**: для нильпотентного N (N⁸=0), M1(c) ДОКАЗУЕМО полином степени ≤7 —
истинная экспонента алгебраически НЕВОЗМОЖНА. Уже задокументированное замедление отношений
(3.76→1.80) оказалось эмпирической сигнатурой именно этого факта, не второстепенной оговоркой.
Вердикт CONFIRMED→REJECTED, статус confirmed→killed. Практически важный вопрос pearl impact 9
переоткрыт — этот скан тестировал другой, более узкий вопрос. Итог 5 подряд skeptic-проходов:
5/5 нашли реальные проблемы, разброс от мягкого до математически безапелляционного.
**[WS: fifth skeptic pass] CLOSED.**

**[WS: шестой skeptic-проход, первый на мосте B3] H-B3-1l дальше WEAKENED (ADR-055):** skeptic
на H-B3-1l (peak-tau TDA vs classical). Нашёл 2: (1) правдоподобный механизм для конфаунда
негативных контролей (argmax структурно смещён к раннему индексу, РАЗНО для гладких classical и
«дёрганых» TDA-статистик) — не подтверждён эмпирически; (2) **независимо проверено против
committed data**: `classical_ac1_peak_date=1999.25` — ДО `tda_betti_peak_date=2000.5` — AC1
САМ ПО СЕБЕ уже обходит TDA, скрыто асимметричным правилом выбора classical-статистики
(oracle-informed для позитивного случая, «раньше из двух» для негативных). Вердикт WEAKENED
сильнее, чем оригинальный самопойманный конфаунд подразумевал. 2 новых pearl-записи. Итог 6
подряд skeptic-проходов: 6/6 нашли реальные проблемы на ДВУХ разных мостах (B2 и B3) — не
специфично одному стилю эксперимента. **[WS: sixth skeptic pass] CLOSED.**

**[WS: седьмой, ПОСЛЕДНИЙ skeptic-проход] H-B3-1m CRITERION_INVALID → UNRESOLVED AT CURRENT
POWER (ADR-056):** skeptic на H-B3-1m (two-part tau+Pettitt rule). Самая серьёзная находка всего
скана, независимо перепроверена вычислением: claim.md's механизм-обоснование («Pettitt ловит
level-shift, не тренд») ЛОЖНО — K=n²/4 точно для чистого монотонного тренда без шума (n=30 →
K=225.0=предсказание, p≈3.7e-5), AND-gate не даёт заявленной специфичности. Плюс: reps=30 даёт
95%-CI±18пп, порог 50% внутри шума — Loch Leven (53.3%) vs Windermere (33.3%) неразличимы;
общий seed=0 коррелирует суррогаты трёх озёр. graph.yaml evidence→CONFLICT, kill_criterion
переписан. **Итог СЕМИ подряд skeptic-проходов: 7/7 нашли реальные проблемы**, диапазон от
мягкого до математически/вычислительно безапелляционного, на ОБОИХ мостах (B2, B3). Систематический
skeptic-скан флагованных экспериментов ЗАВЕРШЁН. **[WS: seventh and final skeptic pass] CLOSED.**

**[WS: H-B3-1m power-фикс, прямое следствие ADR-056] REJECT финально (ADR-057):** установлен
`pyhomogeneity`, `pettitt_test` сверена — K/U совпадает точно на 7 случаях, реализация без ошибок
(Finding 5 DISMISSED); побочно — ВТОРОЕ независимое подтверждение Finding 1 (сторонний пакет тоже
помечает чистый тренд как значимый). `run.py`: reps 30→500, раздельный seed на озеро. Floor
резолвится чисто: Lower Zurich 44.0%, Windermere 42.8%, Loch Leven 41.6% (все CI<50%) — но именно
это открыло Step 2 критерия впервые: Loch Leven реально two-part-crosses на СВОИХ данных (не
только AR(1)-нуле) — истинный false positive. Вердикт UNRESOLVED→**REJECT**. Kill Analysis,
`null_results/H-B3-1m-…md`, graph.yaml status killed/evidence VERIFIED-REAL. **ЗАКРЫВАЕТ ВСЕ 3
пункта Relaxation Map H-B3-1b окончательно** (Row1 REJECT, Row2 REJECT, Row3 CONFIRMED-с-
конфаундом) — ни один чистый PROMOTE. **[WS: H-B3-1m power fix] CLOSED.**

**[WS: пользователь — 3 приоритета после 7/7 skeptic-скана] Мета-анализ (ADR-058) + B1/B4-B6
(ADR-059).** Пользователь явно остановил автозапуск H-B2-1l (был бы 8-м экспериментом без анализа
7/7): читать «skeptic 7/7» как провал generation process, не как повод запускать больше. Приоритет:
анализ → B1 (делегирован агенту) → B4-B6 (пользователь ответил) → H-B2-1l (припаркован).
**Мета-анализ:** прямое чтение всех 7 CORRECTION ADDENDUM → 3 под-паттерна, большинство (4/7) —
неверифицированное механистическое предложение (естественноязыковой claim о поведении
статистики использован как обоснование без прямой проверки). `03-methodology-rules/lesson-self-review-blind-spot-7of7.md`.
**B1 (Q-GOE-vs-GUE) разрешён:** цитируемый аргумент H-7 TAD путает Poisson-vs-Wigner-Dyson
(связность, верно) с GOE-vs-GUE (нарушение симметрии, не установлено) — реальная симметричная
Hi-C-матрица по умолчанию GOE, не GUE. Gate 4 Scientism flag: датированная пометка «усиление для
рукописи». H-B1-1b остаётся blocked, но сужен до ОДНОГО блокера (Option A, внешний, вне scope).
**B4-B6:** пользователь ответил напрямую — доступа к другой машине сейчас нет, постоянное
`unverified_source`, не переспрашивать. **[WS: user 3-priority redirect] CLOSED.**

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
- [2026-09-07 11:53] `c45def5` (local, branch `feature/meta-analysis-b1-b4b6-resolution` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): chore: fix stale 'blocked pending user input' line + auto-log entry
- [2026-09-07 11:53] `be76b4b` (local, branch `feature/meta-analysis-b1-b4b6-resolution` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs: root-cause self-review's 7/7 blind spot; resolve B1 (Q-GOE-vs-GUE) and B4-B6 per user direction
- [2026-09-07 11:27] `96b5b93` (local, branch `feature/h-b3-1m-power-fix-reject` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): chore: auto-log commit history entry (round 2, final)
- [2026-09-07 11:27] `8f81fe8` (local, branch `feature/h-b3-1m-power-fix-reject` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): chore: auto-log commit history entry
- [2026-09-07 11:27] `22cec95` (local, branch `feature/h-b3-1m-power-fix-reject` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): fix: H-B3-1m REJECT, finally -- power fix + independent Pettitt cross-check resolve the skeptic's open findings
- [2026-09-07 11:04] `435a7f2` (local, branch `feature/h-b3-1m-skeptic-final-sweep-close` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): chore: auto-log commit history entry (round 2, final)
- [2026-09-07 11:04] `7d0a417` (local, branch `feature/h-b3-1m-skeptic-final-sweep-close` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): chore: auto-log commit history entry
- [2026-09-07 11:04] `f0ddb5c` (local, branch `feature/h-b3-1m-skeptic-final-sweep-close` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): fix: H-B3-1m verdict downgraded to UNRESOLVED AT CURRENT POWER by seventh and final skeptic pass -- AND-gate mechanism disproven by direct computation
- [2026-09-07 10:51] `3ae216d` (local, branch `feature/h-b3-1l-skeptic-argmax-bias` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): chore: auto-log commit history entry (round 4, folding in)
- [2026-09-07 10:51] `36ad740` (local, branch `feature/h-b3-1l-skeptic-argmax-bias` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): chore: auto-log commit history entry (round 3, final)
- [2026-09-07 10:51] `0dd1337` (local, branch `feature/h-b3-1l-skeptic-argmax-bias` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): chore: auto-log commit history entry (round 2)
- [2026-09-07 10:51] `5fd8565` (local, branch `feature/h-b3-1l-skeptic-argmax-bias` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): chore: auto-log commit history entry
- [2026-09-07 10:50] `3e72176` (local, branch `feature/h-b3-1l-skeptic-argmax-bias` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): fix: H-B3-1l WEAKENED by sixth skeptic pass -- AC1 quietly beats TDA via asymmetric selection rule
- [2026-09-07 10:38] `8a7aef4` (local, branch `feature/h-b2-1h-skeptic-rejected` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): fix: H-B2-1h REJECTED by fifth skeptic pass -- proven mathematically, not just re-argued
- [2026-09-07 10:22] `9475623` (local, branch `feature/h-b2-1i-skeptic-weakened` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): fix: H-B2-1i WEAKENED by fourth skeptic pass -- mildest of four, core measurement confirmed intact
