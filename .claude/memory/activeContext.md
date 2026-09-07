# activeContext.md — Y-17 100 gipotez

## Scope Fence
- **Goal:** [PLAN, не факт] Оценить и начать проверку cross-domain мостов между каталогом ~141 открытых научных задач и реальными проектами (H-7 chromatin, ChernoffPy, May 1972)
- **Boundary:** Эта папка + чтение (не запись) в исходный vault `C:\Users\serge\.claude\memory\` при необходимости сверки
- **Done when:** Хотя бы один мост прошёл полный цикл kill-criterion → эксперимент → KILLED/CONFIRMED/LEAD
- **NOT NOW:** Frontier R&D / TOFT / RAF — заблокированы до подтверждения существования; полный Hypothesis Portfolio (128+ гипотез из ARCHCODE и др.) — отдельный, не связанный проект





## Current Focus
[summarized] **B1/B2/B3 arc (H-B3-1 through H-B3-1k, ADR-010–027) archived to `history/activeContext-archive-20260906-b1b2b3.md`**
[summarized] **H-B7-7 through H-B7-12 (ADR-034–039) archived to `history/activeContext-archive-20260907-b7-7to12.md`**
[summarized] **B3 case-study (ADR-040) + B2 coupling/seed (ADR-042/043) + B3 peak-tau self-catch (ADR-044/045) archived to `history/activeContext-archive-20260907-b2-b3-part2.md`**

**[WS: B3 change-point, `/loop` continued] H-B3-1m (ADR-046):** закрывает ПОСЛЕДНИЙ пункт
H-B3-1b's Relaxation Map — Row 2 (two-part правило: tau≥0.5 И Pettitt level-shift test).
Pettitt's test реализован с нуля (не установлен ни один пакет), провалидирован 4 тестами
(позитив/негатив/калибровка/вырожденный случай) ДО реального прогона. **CRITERION_INVALID
снова** (max floor FP = 53.3% на Loch Leven, ≥ порога 50%) — НЕ доказательство против гипотезы
(FL Step 4a). НО floor упал ПРИМЕРНО ВДВОЕ на 2 из 3 озёр (83.3%→40.0%, 80.0%→33.3%) — механизм
работает, недостаточно именно на Loch Leven. Все 3 пункта исходной Relaxation Map `H-B3-1b`
теперь закрыты (Row 1 REJECT, Row 2 CRITERION_INVALID-с-улучшением, Row 3 CONFIRMED-с-конфаундом).
8 новых тестов, 212 всего. **[WS: B3 change-point] CLOSED.**

**[WS: B2 scale N=50, продолжение по «продолжай автономно»] H-B2-1j (ADR-047):** закрывает
ПОСЛЕДНИЙ открытый пункт LAB.md для всей арки H-B2-1* (coupling sweep + multi-seed уже закрыты).
Идентичная конструкция H-B2-1f/g, N_DIM 8→50, coupling=15/seed=0 зафиксированы. **CONFIRMED**:
граница держится 16/16, порядок точен (0.9983, 2.0081). Находка: M1 ВЫРОС 158.93→675.40 (~4.25×)
— опровергает наивную экстраполяцию «M1 продолжает уменьшаться с N» из H-B2-1f. Эффективность
упала ЕЩЁ на 3-5 порядков (1.3e-10, 4.3e-12). Новый механизм: `‖A^(m+1)x0‖` растёт с N независимо
от M1 — минимум два члена управляют коллапсом эффективности. 5 новых тестов, 217 всего.
**[WS: B2 scale N=50] CLOSED.**

**[WS: M1 non-monotonicity, выбор пользователя «углубиться в новые механизмы»] H-B2-1k
(ADR-048):** прямая проверка pearl-предсказания H-B2-1j. Фиксированный спектральный диапазон
[-50,-1] (изолирует размерность от диапазона, в отличие от H-B2-1j's confounded конвенции).
Найден и исправлен edge case ДО прогона: N=2 даёт вырожденный linspace(num=1) — исключён из
скана. **CONFIRMED немонотонность**: 8 смен знака в 8 разностях M1(N=3..50), крупные скачки
(12× рост, >6× падение). Однозначно подтверждает собственное предсказание H-B2-1j. Ограничение:
один сид, конкретная форма кривой не установлена как типичная. 8 новых тестов, 225 всего.
**[WS: M1 non-monotonicity] CLOSED.**

**[WS: eigenvector conditioning, продолжение «углубиться в новые механизмы»] H-B2-1l
(ADR-049):** заостряет неформальную гипотезу «кластеризация собственных значений» (общую для
H-B2-1i и H-B2-1k) до κ(V) — числа обусловленности матрицы собственных векторов, классически
связанного с M1. Переиспользованы ОБЕ уже построенные популяции (30 seed-матриц H-B2-1i + 9
N-матриц H-B2-1k) без новых draw'ов. **CONFIRMED**: положительная корреляция в ОБЕИХ популяциях
(seed: ρ=0.453 p=0.012 n=30; N: ρ=0.917 p=0.0005 n=9) — объединяет две ранее необъяснённые
находки одним механизмом. N-скан намного сильнее seed-ансамбля, причина не диагностирована.
6 новых тестов, 231 всего. **[WS: eigenvector conditioning] CLOSED.**

**[WS: первый реальный skeptic-проход, после отчёта пользователю] H-B2-1l WEAKENED (ADR-050):**
запущен `Agent(skeptic)` на H-B2-1l с полной асимметрией контекста (первый раз за всю сессию,
после того как сама пометила это HIGH-приоритетной дырой в отчёте). Найдено реально: N-скан
популяция (fixed seed=0) — одна детерминированная кривая на 9 точках сетки, НЕ 9 независимых
наблюдений; эффективный n≈1. «Согласованность в обеих популяциях» не выдержала проверки —
переоткрыта немонотонность H-B2-1k по N. Seed-ансамбль (ρ=0.453, n=30) выжил как частичный
механизм (~20% вариации). Побочно исправлен реальный баг verdict-логики (принимала любой
положительный ρ, мягче собственного порога claim.md). 1 новый regression-тест, 232 всего.
Обе связанные pearl-записи исправлены. **[WS: first skeptic pass] CLOSED.**

**[WS: второй skeptic-проход подряд] H-B2-1j confound найден (ADR-051):** сразу за H-B2-1l —
skeptic на H-B2-1j (граница Чернова при N=50). Нашёл: конструкция меняет N_DIM, спектральный
диапазон И размер блока связи ОДНОВРЕМЕННО — минимум 3 переменные вместо заявленной одной.
**Ирония:** этот же confound я сам распознал и избежал при построении H-B2-1k, но не
распространил осознание назад на H-B2-1j. Находка «M1 выросло с размерностью» опровергнута как
изолированный эффект — H-B2-1k's правильно изолированный скан заменяет её. Граница
(валидность+порядок) выжила, проверена дополнительно вручную (локальный порядок по парам n).
Обе pearl-записи и graph.yaml исправлены. **[WS: second skeptic pass] CLOSED.**

**[WS: третий skeptic-проход подряд, самая серьёзная находка] H-B2-1k FALSIFIED (ADR-052):**
skeptic на H-B2-1k (немонотонность M1 по N). Нашёл: пре-регистрированный критерий «≥1 смена
знака» проходится ЧИСТЫМ ШУМОМ с вероятностью ≈0.999994 (2 из 9! упорядочиваний монотонны) —
тот же класс floor-дефекта, что H-B3-1/1b's tau≥0.5, просто не пойманный из-за ярлыка
«descriptive → floor not applicable». Плюс: 9 точек скана — структурно независимые draw'ы
(seed пересоздаётся заново на каждый вызов). Моя собственная заранее предвиденная защита
(«смягчено масштабом скачков») логически несостоятельна. Статус понижен confirmed→lead
(CRITERION_INVALID precedent). Аудит: паттерн больше нигде в сессии не повторяется. Pearl
impact 8: FL Step 4a floor-проверка нужна для ЛЮБОГО бинарного критерия, не только detection
rules. **[WS: third skeptic pass] CLOSED.**

**[WS: четвёртый skeptic-проход, самый мягкий] H-B2-1i WEAKENED (ADR-053):** skeptic на
H-B2-1i (seed-ансамбль M1) — единственном основании уцелевшей части H-B2-1l. **Ядро измерения
явно подтверждено целым** (30 значений — реальные независимые draw'ы, ссылка H-B2-1l безопасна).
Найдено мягче: self-inclusion референсного сида (не меняет вердикт), Tukey-на-скошенном-
распределении (на лог-шкале 158.93 — «заурядно», ≈0.87σ, а не «выше Q3» как на сырой шкале).
Статус узла НЕ понижен (в отличие от H-B2-1k) — ослаблена метка, не данные. Итог 4 подряд
skeptic-проходов: 4/4 нашли реальные, но по-разному серьёзные проблемы — не монотонная
эскалация, честный разброс. **[WS: fourth skeptic pass] CLOSED.**

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
- [2026-09-07 10:12] `5aa54d5` (local, branch `feature/h-b2-1k-skeptic-falsified` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): fix: H-B2-1k FALSIFIED by third skeptic pass -- monotonicity criterion passed by pure noise ~always
- [2026-09-07 10:02] `d198c40` (local, branch `feature/h-b2-1j-skeptic-confound` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): fix: H-B2-1j's M1-growth claim falsified by a confound the SAME session already knew to avoid
- [2026-09-07 09:51] `cc4932d` (local, branch `feature/h-b2-1l-skeptic-weakened` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): fix: H-B2-1l WEAKENED by the session's first real skeptic pass -- N-sweep was one curve, not 9
- [2026-09-07 09:07] `5b1ab1e` (local, branch `feature/h-b2-1l-eigenvector-conditioning` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): H-B2-1l: eigenvector conditioning kappa(V) explains M1 in both independent H-B2-1* populations
- [2026-09-07 08:56] `31daa9a` (local, branch `feature/h-b2-1k-dimension-sweep` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): H-B2-1k: M1(N) is non-monotonic at a fixed spectral range -- confirms H-B2-1j's own prediction
- [2026-09-07 08:39] `f263ce1` (local, branch `feature/h-b2-1j-scale-n50` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): H-B2-1j: Theorem 3.1 bound CONFIRMED at N=50, efficiency collapses 3-5 more orders of magnitude
- [2026-09-07 08:30] `2434dfe` (local, branch `feature/h-b3-1m-changepoint` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): H-B3-1m: two-part rule (tau AND Pettitt) closes the last H-B3-1b Relaxation Map row
- [2026-09-07 08:10] `aaa6c04` (local, branch `feature/h-b3-1l-peaktau` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): H-B3-1l: peak-tau reporting closes H-B3-1b's Relaxation Map Row 3 -- CONFIRMED with a confound
- [2026-09-07 08:00] `8b85c83` (local, branch `feature/h-b3-1b-stale-annotation-fix` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): fix: H-B3-1b graph.yaml annotation was stale -- Type-4 status-lag self-catch
- [2026-09-07 07:55] `782ae01` (local, branch `feature/h-b2-1i-multiseed` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): H-B2-1i: 30-seed ensemble at coupling=15 closes H-B2-1g's open question -- M1=158.93 is MODERATE
- [2026-09-07 07:48] `9d5a9bc` (local, branch `feature/auto-log-5b1c9b8` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): chore: auto-log commit history entry
- [2026-09-07 07:48] `5b1c9b8` (local, branch `feature/h-b2-1h-coupling-sweep` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): H-B2-1h: coupling-magnitude sweep CONFIRMS exponential M1 growth, self-caught R^2 loss-mismatch first
- [2026-09-07 07:32] `b31db36`: chore: auto-log commit history entry
- [2026-09-07 07:32] `e826359` (local, branch `feature/b3-peter-lake-replicate` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): B3 Addendum 5: Peter lake replicate confirms trend-inversion direction independently
- [2026-09-07 07:14] `c49c0a2`: chore: auto-log commit history entry
