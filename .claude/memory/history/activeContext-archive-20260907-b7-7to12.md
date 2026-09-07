# activeContext.md archive — H-B7-7 through H-B7-12 (2026-09-06/07)

Archived verbatim from `.claude/memory/activeContext.md` per Checkpoint Fidelity discipline
(`memory-protocol.md`): content fully superseded by `registry/graph.yaml` (nodes `H-B7-7`..`H-B7-12`,
bridge `B7-KAUFFMAN-ATTRACTORS`) and `.claude/memory/decisions.md` (ADR-034 through ADR-039).
Archived to keep `activeContext.md` under the 200-line ceiling ahead of the B3 thread's own entry.

---

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

**[WS: H-B7-11 remy_tumorigenesis cross-branch] CLOSED 2026-09-07 (ADR-038, прямой запрос
пользователя «проверь другую мультистабильную ветку итд продолжай выполнять все по очереди»).**
`[VERIFIED]`:
- Compute-First пересчёт всех 16 веток ДО дизайна → **побочно поймал ошибку счёта H-B7-4** (7, не
  8, мультистабильных веток; «2 фенотипически разных» — верно). Dated correction addendum, не
  тихая правка.
- `do(p21CIP=0, RBL2=0)` на ЕДИНСТВЕННОЙ другой фенотипически-дивергентной ветке (отличается на 1
  бит, EGFR_stimulus) → **CONFIRMED** — точный Proliferation attractor этой ветки, механизм
  структурно идентичен (те же escape-route узлы активны).
- **FL Step 8a skeptic pass выполнен и пройден** (шестой CONFIRMED подряд): CONFIRMED-REAL;
  исчерпывающее перечисление аттракторов второй ветки — ровно 3, все совпали.
- Граф: `H-B7-11 → confirmed`. Мост остаётся `evidence: CONFLICT`. **Pearl impact 8.** Первая
  кросс-ветка генерализация в серии B7. Следующий шаг: транзиентная версия на этой ветке.

**[WS: H-B7-12 remy_tumorigenesis cross-branch transient] CLOSED 2026-09-07 (ADR-039, продолжение
очереди по запросу пользователя «продолжай выполнять все по очереди»).** `[VERIFIED]`:
- Транзиентный `do(p21CIP=0, RBL2=0)` на второй ветке → k*=5 воспроизвёлся ТОЧНО (тот же
  one-step race, что H-B7-10).
- **НО skeptic отнёсся к «подозрительно удобному» совпадению как к сигналу для БОЛЬШЕЙ проверки** —
  нашёл, что обе ветки динамически ЭКВИВАЛЕНТНЫ: `EGFR` заблокирован `FGFR3=1` (правило требует
  `!FGFR3` в обоих дизъюнктах), `EGFR_stimulus` никогда не распространяется.
- **Дополнительно:** только 2 из 7 мультистабильных веток вообще имеют Proliferation attractor, обе
  требуют идентичной `(DNA=0,FGFR3=1,GI=1)` — пространство кросс-веточной генерализации для этой
  цели побега ИСЧЕРПАНО.
- **Вердикт: WEAKENED** (per Response Matrix, Accepted) — технический kill criterion выполнен, но
  рамка скорректирована. Dated addendum добавлен в H-B7-11's decision.md (не тихая правка,
  технический CONFIRMED H-B7-11 не изменён).
- Граф: `H-B7-12 → confirmed` (WEAKENED). Мост остаётся `evidence: CONFLICT`. **Pearl impact 8** —
  методологическая находка о ТОМ, как проверять claims о генерализации.

**Bridge B7-KAUFFMAN-ATTRACTORS net position after H-B7-1..12:** `evidence: CONFLICT` throughout.
Chain: Fauré model TASK_INFEASIBLE (H-B7-1..3) → Remy model single/two/three-hit all REJECTED but
mechanism traced with increasing precision (H-B7-4..6, ending in an explicit source-level OR gate
`Growth_arrest = p21CIP|RBL2|RB1`) → four-hit CONFIRMED, first successful escape (H-B7-7) →
necessity-minimized to two-hit (H-B7-8) → transient (strict Kauffman) CONFIRMED with exact k*=5
threshold, fully mechanistically traced to a one-synchronous-step race condition (H-B7-9/10) →
cross-branch generalization CONFIRMED then WEAKENED to "robustness to one inert input" once the
skeptic found the two tested branches are dynamically equivalent, closing the generalization
question by exhaustion rather than leaving it open (H-B7-11/12).
