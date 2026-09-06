# activeContext.md archive — H-B7-1 through H-B7-6 (2026-09-06/07)

Archived verbatim from `.claude/memory/activeContext.md` per Checkpoint Fidelity discipline
(`memory-protocol.md`): content fully superseded by `registry/graph.yaml` (nodes `H-B7-1`..`H-B7-6`,
bridge `B7-KAUFFMAN-ATTRACTORS`) and `.claude/memory/decisions.md` (ADR-028 through ADR-033), not
lost. Archived to keep `activeContext.md` under the 200-line ceiling ahead of adding H-B7-10.

---

**[WS: H-B7-1 Kauffman cancer attractors] CLOSED 2026-09-06 (ADR-028, прямой запрос пользователя
«начинай скоупинг R6»).** Независимое brute-force воспроизведение аттракторов Fauré et al. 2006
(Boolean cell-cycle network) — точное совпадение с PyBoolNet positive control. CONFIRMED как
воспроизведение, гипотеза Kauffman сама по себе не проверена этим шагом.

**[WS: H-B7-2 perturbation] CLOSED 2026-09-06 (ADR-029, прямой запрос пользователя «начинай
perturbation-эксперимент»).** `do(Rb=0)` → CycD=0 область сходится к НОВОМУ period-8 аттрактору —
CONFIRMED-WEAKENED (не строгая формулировка Kauffman, новый аттрактор, не раскрытие существующего).
`do(p27=0)` → REJECTED, quiescence сохраняется.

**[WS: H-B7-3 transient perturbation] CLOSED 2026-09-06 (ADR-030, прямой запрос пользователя
«начинай transient-perturbation эксперимент»).** Compute-First дедукция из H-B7-1's exhaustive
результата: у области CycD=0 РОВНО ОДИН аттрактор под истинными правилами → транзиентное возмущение
Rb/p27 логически ГАРАНТИРОВАННО возвращается к quiescence. Проверено на 6 конкретных траекториях —
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

**[WS: H-B7-6 remy_tumorigenesis three-hit] CLOSED 2026-09-06 (ADR-033, автономно, продолжение
Relaxation Map H-B7-5).** `[VERIFIED]`:
- `do(RAS=1, TP53=0, p21CIP=0)` → **REJECTED снова** — bit-string-новое состояние, но фенотипически
  всё ещё Growth_arrest (собственный phenotype-узел сети: Growth_arrest=1, Proliferation=0).
- Полный механизм найден И ПОДТВЕРЖДЁН ДВУМЯ независимыми способами: (1) алгебра на `.bnet` правилах
  — `Growth_arrest = p21CIP | RBL2 | RB1`, явный тройной OR в исходнике; `CyclinD1` доказуемо не
  может быть 1 ни в одной неподвижной точке этой ветки; (2) независимо подтверждено `pyboolnet` на
  ВСЕХ 3 реальных аттракторах ветки — `CyclinD1=0` включая настоящий Proliferation.
- Собственный kill criterion оказался двусмысленным (bit-string vs фенотипическая новизна) —
  разрешено по намерению, зафиксировано как Hindsight Distortion Gap correction.
- Граф: `H-B7-6 → killed`. Мост остаётся `evidence: CONFLICT`. **Pearl impact 9.** Следующий шаг:
  четырёхударный `do(RAS=1, TP53=0, p21CIP=0, RBL2=0)` или транзиентный толчок RBL2/CyclinE1.
