# 100 перспективных нерешённых научных задач среднего масштаба

**Проверено по состоянию на:** 6 сентября 2026  
**Цель:** не знаменитые мегапроблемы, а конкретные входы, где один исследователь или малая группа может немедленно поставить вычислительный/математический эксперимент.

<fact>В каталоге ровно 100 задач. Старые open-problem списки не принимались на веру: выполнялась проверка последующих решений и прогресса.</fact>

<fact>В ходе фильтрации исключены как минимум два показательных уже закрытых случая: noisy-query problem из COLT-2025, решённый в COLT-2026, и двухкопийный Werner-state Problem 5 из PRX Quantum, для которого в июле 2026 заявлено решение.</fact>

<inference>Каталог намеренно смещён к задачам с точным verifier, воспроизводимым benchmark или дешёвым генератором instances. Именно там AI даёт реальный рычаг, а не презентационный дым.</inference>

**<feasibility>9/10</feasibility>** для первых экспериментов; полное решение отдельных задач варьирует примерно от 3/10 до 7/10.

---

## #1 — Локальная регуляризация, способная учить все мультиклассовые классы

**Field:** Computer Science / Learning Theory  
**Status:** Partially Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Локальная регуляризация, способная учить все мультиклассовые классы» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Главный барьер обычно в разрыве между worst-case lower bounds и конструктивными алгоритмами; локально хорошие эвристики не дают tight общей гарантии.

### What Is Already Known
<fact>Есть существенные частичные результаты, но исходная tight/общая постановка не закрыта. Основная свежая точка опоры: COLT 2024 Open Problems, PMLR 247 (2024).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Локальная регуляризация, способная учить все мультиклассовые классы → структурная характеристика → более сильный алгоритм → перенос в scientific computing / data analysis.</hypothesis>

### AI / Computational Attack Surface
simulation; optimization; symbolic search; model comparison; counterexample generation; uncertainty-aware AI assistance.

### First Research Experiment
**Проверяемый старт:** Перебрать малые конечные multiclass classes и автоматически искать минимальный контрпример к известным достаточным условиям.

### Scores
```text
Scientific Importance: 8/10
Tractability: 6/10
Computational Accessibility: 9/10
AI Leverage: 10/10
Bridge Potential: 8/10
Underexploredness: 8/10
Verification Clarity: 9/10
```

### Evidence
- Primary/current source: COLT 2024 Open Problems, PMLR 247 (2024).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #2 — Оптимальная сложность joint differential privacy в линейных contextual bandits

**Field:** Computer Science / Private Bandits  
**Status:** Partially Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Оптимальная сложность joint differential privacy в линейных contextual bandits» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Главный барьер обычно в разрыве между worst-case lower bounds и конструктивными алгоритмами; локально хорошие эвристики не дают tight общей гарантии.

### What Is Already Known
<fact>Есть существенные частичные результаты, но исходная tight/общая постановка не закрыта. Основная свежая точка опоры: COLT 2024 Open Problems, PMLR 247 (2024).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Оптимальная сложность joint differential privacy в линейных contextual bandits → структурная характеристика → более сильный алгоритм → перенос в scientific computing / data analysis.</hypothesis>

### AI / Computational Attack Surface
simulation; optimization; symbolic search; model comparison; counterexample generation; uncertainty-aware AI assistance.

### First Research Experiment
**Проверяемый старт:** Сравнить privatized confidence-set algorithms на синтетических контекстах с контролируемым спектром.

### Scores
```text
Scientific Importance: 8/10
Tractability: 7/10
Computational Accessibility: 10/10
AI Leverage: 8/10
Bridge Potential: 9/10
Underexploredness: 9/10
Verification Clarity: 9/10
```

### Evidence
- Primary/current source: COLT 2024 Open Problems, PMLR 247 (2024).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #3 — Tight instance-optimal identity testing

**Field:** Computer Science / Property Testing  
**Status:** Partially Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Tight instance-optimal identity testing» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Главный барьер обычно в разрыве между worst-case lower bounds и конструктивными алгоритмами; локально хорошие эвристики не дают tight общей гарантии.

### What Is Already Known
<fact>Есть существенные частичные результаты, но исходная tight/общая постановка не закрыта. Основная свежая точка опоры: COLT 2024 Open Problems, PMLR 247 (2024).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Tight instance-optimal identity testing → структурная характеристика → более сильный алгоритм → перенос в scientific computing / data analysis.</hypothesis>

### AI / Computational Attack Surface
simulation; optimization; symbolic search; model comparison; counterexample generation; uncertainty-aware AI assistance.

### First Research Experiment
**Проверяемый старт:** Для алфавитов n≤12 численно решить minimax testing game и сопоставить с кандидатными complexity functionals.

### Scores
```text
Scientific Importance: 8/10
Tractability: 8/10
Computational Accessibility: 8/10
AI Leverage: 9/10
Bridge Potential: 10/10
Underexploredness: 7/10
Verification Clarity: 9/10
```

### Evidence
- Primary/current source: COLT 2024 Open Problems, PMLR 247 (2024).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #4 — Black-box reductions для adaptive gradient methods в nonconvex optimization

**Field:** Computer Science / Optimization  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Black-box reductions для adaptive gradient methods в nonconvex optimization» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Главный барьер обычно в разрыве между worst-case lower bounds и конструктивными алгоритмами; локально хорошие эвристики не дают tight общей гарантии.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: COLT 2024 Open Problems, PMLR 247 (2024).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Black-box reductions для adaptive gradient methods в nonconvex optimization → структурная характеристика → более сильный алгоритм → перенос в scientific computing / data analysis.</hypothesis>

### AI / Computational Attack Surface
simulation; optimization; symbolic search; model comparison; counterexample generation; uncertainty-aware AI assistance.

### First Research Experiment
**Проверяемый старт:** Задать DSL преобразований оптимизаторов и выполнить program synthesis reduction на benchmark nonconvex functions.

### Scores
```text
Scientific Importance: 8/10
Tractability: 5/10
Computational Accessibility: 9/10
AI Leverage: 10/10
Bridge Potential: 8/10
Underexploredness: 8/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: COLT 2024 Open Problems, PMLR 247 (2024).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #5 — Direct-sum теоремы в learning theory

**Field:** Computer Science / Complexity of Learning  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Direct-sum теоремы в learning theory» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Главный барьер обычно в разрыве между worst-case lower bounds и конструктивными алгоритмами; локально хорошие эвристики не дают tight общей гарантии.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: COLT 2024 Open Problems, PMLR 247 (2024).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Direct-sum теоремы в learning theory → структурная характеристика → более сильный алгоритм → перенос в scientific computing / data analysis.</hypothesis>

### AI / Computational Attack Surface
simulation; optimization; symbolic search; model comparison; counterexample generation; uncertainty-aware AI assistance.

### First Research Experiment
**Проверяемый старт:** Вычислить exact complexity одной и двух копий малых concept classes и искать нарушения аддитивности.

### Scores
```text
Scientific Importance: 8/10
Tractability: 6/10
Computational Accessibility: 10/10
AI Leverage: 8/10
Bridge Potential: 9/10
Underexploredness: 9/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: COLT 2024 Open Problems, PMLR 247 (2024).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #6 — Оптимальный regret в stochastic decision-theoretic online learning под DP

**Field:** Computer Science / Online Learning  
**Status:** Partially Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Оптимальный regret в stochastic decision-theoretic online learning под DP» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Главный барьер обычно в разрыве между worst-case lower bounds и конструктивными алгоритмами; локально хорошие эвристики не дают tight общей гарантии.

### What Is Already Known
<fact>Есть существенные частичные результаты, но исходная tight/общая постановка не закрыта. Основная свежая точка опоры: COLT 2024 Open Problems, PMLR 247 (2024).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Оптимальный regret в stochastic decision-theoretic online learning под DP → структурная характеристика → более сильный алгоритм → перенос в scientific computing / data analysis.</hypothesis>

### AI / Computational Attack Surface
simulation; optimization; symbolic search; model comparison; counterexample generation; uncertainty-aware AI assistance.

### First Research Experiment
**Проверяемый старт:** Решить finite-horizon minimax DP на малых пространствах действий и извлечь scaling law.

### Scores
```text
Scientific Importance: 8/10
Tractability: 7/10
Computational Accessibility: 8/10
AI Leverage: 9/10
Bridge Potential: 10/10
Underexploredness: 7/10
Verification Clarity: 9/10
```

### Evidence
- Primary/current source: COLT 2024 Open Problems, PMLR 247 (2024).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #7 — Оптимальная anytime convergence rate gradient descent

**Field:** Computer Science / Optimization  
**Status:** Partially Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Оптимальная anytime convergence rate gradient descent» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Главный барьер обычно в разрыве между worst-case lower bounds и конструктивными алгоритмами; локально хорошие эвристики не дают tight общей гарантии.

### What Is Already Known
<fact>Есть существенные частичные результаты, но исходная tight/общая постановка не закрыта. Основная свежая точка опоры: COLT 2024 Open Problems, PMLR 247 (2024).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Оптимальная anytime convergence rate gradient descent → структурная характеристика → более сильный алгоритм → перенос в scientific computing / data analysis.</hypothesis>

### AI / Computational Attack Surface
simulation; optimization; symbolic search; model comparison; counterexample generation; uncertainty-aware AI assistance.

### First Research Experiment
**Проверяемый старт:** Через Performance Estimation Problems найти оптимальные единые префиксы step-size schedules для горизонтов 1…50.

### Scores
```text
Scientific Importance: 8/10
Tractability: 8/10
Computational Accessibility: 9/10
AI Leverage: 10/10
Bridge Potential: 8/10
Underexploredness: 8/10
Verification Clarity: 9/10
```

### Evidence
- Primary/current source: COLT 2024 Open Problems, PMLR 247 (2024).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #8 — Оптимальный regret в kernel-based reinforcement learning

**Field:** Computer Science / RL Theory  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Оптимальный regret в kernel-based reinforcement learning» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Главный барьер обычно в разрыве между worst-case lower bounds и конструктивными алгоритмами; локально хорошие эвристики не дают tight общей гарантии.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: COLT 2024 Open Problems, PMLR 247 (2024).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Оптимальный regret в kernel-based reinforcement learning → структурная характеристика → более сильный алгоритм → перенос в scientific computing / data analysis.</hypothesis>

### AI / Computational Attack Surface
simulation; optimization; symbolic search; model comparison; counterexample generation; uncertainty-aware AI assistance.

### First Research Experiment
**Проверяемый старт:** Построить continuous-state MDP family с управляемым kernel eigenvalue decay и измерить regret scaling.

### Scores
```text
Scientific Importance: 8/10
Tractability: 5/10
Computational Accessibility: 10/10
AI Leverage: 8/10
Bridge Potential: 9/10
Underexploredness: 9/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: COLT 2024 Open Problems, PMLR 247 (2024).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #9 — Сходимость single-timescale mean-field Langevin descent-ascent в zero-sum games

**Field:** Computer Science / Game Dynamics  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Сходимость single-timescale mean-field Langevin descent-ascent в zero-sum games» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Главный барьер обычно в разрыве между worst-case lower bounds и конструктивными алгоритмами; локально хорошие эвристики не дают tight общей гарантии.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: COLT 2024 Open Problems, PMLR 247 (2024).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Сходимость single-timescale mean-field Langevin descent-ascent в zero-sum games → структурная характеристика → более сильный алгоритм → перенос в scientific computing / data analysis.</hypothesis>

### AI / Computational Attack Surface
simulation; optimization; symbolic search; model comparison; counterexample generation; uncertainty-aware AI assistance.

### First Research Experiment
**Проверяемый старт:** Искать polynomial Lyapunov functions через SOS для малых toy-games и проверять Langevin simulations.

### Scores
```text
Scientific Importance: 8/10
Tractability: 6/10
Computational Accessibility: 8/10
AI Leverage: 9/10
Bridge Potential: 10/10
Underexploredness: 7/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: COLT 2024 Open Problems, PMLR 247 (2024).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #10 — FPT зонотопных задач по геометрической размерности

**Field:** Computer Science / Parameterized Geometry  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «FPT зонотопных задач по геометрической размерности» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Главный барьер обычно в разрыве между worst-case lower bounds и конструктивными алгоритмами; локально хорошие эвристики не дают tight общей гарантии.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: COLT 2025 Open Problems, PMLR 291 (2025; page current in 2026).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>FPT зонотопных задач по геометрической размерности → структурная характеристика → более сильный алгоритм → перенос в scientific computing / data analysis.</hypothesis>

### AI / Computational Attack Surface
simulation; optimization; symbolic search; model comparison; counterexample generation; uncertainty-aware AI assistance.

### First Research Experiment
**Проверяемый старт:** Для d=2…6 вычислить exact instances и искать kernelization rule, уменьшающий число generators.

### Scores
```text
Scientific Importance: 8/10
Tractability: 7/10
Computational Accessibility: 9/10
AI Leverage: 10/10
Bridge Potential: 8/10
Underexploredness: 8/10
Verification Clarity: 10/10
```

### Evidence
- Primary/current source: COLT 2025 Open Problems, PMLR 291 (2025; page current in 2026).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #11 — Structure-agnostic minimax risk для partial linear model

**Field:** Statistics / Semiparametric Learning  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Structure-agnostic minimax risk для partial linear model» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Существующие частичные результаты не дают одновременно общности, tight-гарантий и конструктивного алгоритма.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: COLT 2025 Open Problems, PMLR 291 (2025; page current in 2026).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Structure-agnostic minimax risk для partial linear model → структурная характеристика → более сильный алгоритм → перенос в scientific computing / data analysis.</hypothesis>

### AI / Computational Attack Surface
simulation; optimization; symbolic search; model comparison; counterexample generation; uncertainty-aware AI assistance.

### First Research Experiment
**Проверяемый старт:** В конечномерной дискретизации численно решить convex-concave minimax estimator game.

### Scores
```text
Scientific Importance: 8/10
Tractability: 8/10
Computational Accessibility: 10/10
AI Leverage: 8/10
Bridge Potential: 9/10
Underexploredness: 9/10
Verification Clarity: 10/10
```

### Evidence
- Primary/current source: COLT 2025 Open Problems, PMLR 291 (2025; page current in 2026).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #12 — Оптимальный data selection для regression tasks

**Field:** Computer Science / Experimental Design  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Оптимальный data selection для regression tasks» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Главный барьер обычно в разрыве между worst-case lower bounds и конструктивными алгоритмами; локально хорошие эвристики не дают tight общей гарантии.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: COLT 2025 Open Problems, PMLR 291 (2025; page current in 2026).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Оптимальный data selection для regression tasks → структурная характеристика → более сильный алгоритм → перенос в scientific computing / data analysis.</hypothesis>

### AI / Computational Attack Surface
simulation; optimization; symbolic search; model comparison; counterexample generation; uncertainty-aware AI assistance.

### First Research Experiment
**Проверяемый старт:** Для n≤40 решить subset-selection oracle через MIP и найти случаи провала leverage sampling.

### Scores
```text
Scientific Importance: 8/10
Tractability: 5/10
Computational Accessibility: 8/10
AI Leverage: 9/10
Bridge Potential: 10/10
Underexploredness: 7/10
Verification Clarity: 10/10
```

### Evidence
- Primary/current source: COLT 2025 Open Problems, PMLR 291 (2025; page current in 2026).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #13 — Instance-dependent sample complexity поиска Nash equilibrium в zero-sum matrix games

**Field:** Computer Science / Game Theory  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Instance-dependent sample complexity поиска Nash equilibrium в zero-sum matrix games» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Главный барьер обычно в разрыве между worst-case lower bounds и конструктивными алгоритмами; локально хорошие эвристики не дают tight общей гарантии.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: COLT 2025 Open Problems, PMLR 291 (2025; page current in 2026).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Instance-dependent sample complexity поиска Nash equilibrium в zero-sum matrix games → структурная характеристика → более сильный алгоритм → перенос в scientific computing / data analysis.</hypothesis>

### AI / Computational Attack Surface
simulation; optimization; symbolic search; model comparison; counterexample generation; uncertainty-aware AI assistance.

### First Research Experiment
**Проверяемый старт:** Перебрать 3×3…6×6 игры и эмпирически связать stopping complexity с support/gap structure.

### Scores
```text
Scientific Importance: 8/10
Tractability: 6/10
Computational Accessibility: 9/10
AI Leverage: 10/10
Bridge Potential: 8/10
Underexploredness: 8/10
Verification Clarity: 10/10
```

### Evidence
- Primary/current source: COLT 2025 Open Problems, PMLR 291 (2025; page current in 2026).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #14 — Heavy-tailed bandits с неизвестными tail parameters

**Field:** Computer Science / Robust Bandits  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Heavy-tailed bandits с неизвестными tail parameters» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Главный барьер обычно в разрыве между worst-case lower bounds и конструктивными алгоритмами; локально хорошие эвристики не дают tight общей гарантии.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: COLT 2025 Open Problems, PMLR 291 (2025; page current in 2026).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Heavy-tailed bandits с неизвестными tail parameters → структурная характеристика → более сильный алгоритм → перенос в scientific computing / data analysis.</hypothesis>

### AI / Computational Attack Surface
simulation; optimization; symbolic search; model comparison; counterexample generation; uncertainty-aware AI assistance.

### First Research Experiment
**Проверяемый старт:** Сравнить adaptive truncation policies на Pareto/mixture rewards при неизвестном α.

### Scores
```text
Scientific Importance: 8/10
Tractability: 7/10
Computational Accessibility: 10/10
AI Leverage: 8/10
Bridge Potential: 9/10
Underexploredness: 9/10
Verification Clarity: 10/10
```

### Evidence
- Primary/current source: COLT 2025 Open Problems, PMLR 291 (2025; page current in 2026).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #15 — Точная hardness/tractability граница Hamiltonian Cycle на структурно ограниченных классах графов

**Field:** Mathematics / Graph Algorithms  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Точная hardness/tractability граница Hamiltonian Cycle на структурно ограниченных классах графов» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Трудность в том, что малые примеры дают сильные закономерности, но переход к произвольному размеру требует нового invariant, extremal argument или decomposition.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Agrawal et al., Solving Problems on Graphs: From Structure to Algorithms, Dagstuhl Reports 15(1), 2025, DOI 10.4230/DagRep.15.1.105.</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Точная hardness/tractability граница Hamiltonian Cycle на структурно ограниченных классах графов → новый invariant/decomposition → алгоритмы и формальная верификация → перенос в соседние вычислительные области.</hypothesis>

### AI / Computational Attack Surface
exhaustive search на малых размерах; SAT/SMT/MIP; symbolic algebra; counterexample generation; automated theorem proving; exact/interval verification.

### First Research Experiment
**Проверяемый старт:** Сгенерировать минимальные графы и искать структурные признаки границы tractable/hard.

### Scores
```text
Scientific Importance: 8/10
Tractability: 8/10
Computational Accessibility: 8/10
AI Leverage: 9/10
Bridge Potential: 10/10
Underexploredness: 7/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Agrawal et al., Solving Problems on Graphs: From Structure to Algorithms, Dagstuhl Reports 15(1), 2025, DOI 10.4230/DagRep.15.1.105.
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #16 — Polylogarithmic bounds на treewidth в целевых graph classes

**Field:** Mathematics / Graph Algorithms  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Polylogarithmic bounds на treewidth в целевых graph classes» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Трудность в том, что малые примеры дают сильные закономерности, но переход к произвольному размеру требует нового invariant, extremal argument или decomposition.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Agrawal et al., Solving Problems on Graphs: From Structure to Algorithms, Dagstuhl Reports 15(1), 2025, DOI 10.4230/DagRep.15.1.105.</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Polylogarithmic bounds на treewidth в целевых graph classes → новый invariant/decomposition → алгоритмы и формальная верификация → перенос в соседние вычислительные области.</hypothesis>

### AI / Computational Attack Surface
exhaustive search на малых размерах; SAT/SMT/MIP; symbolic algebra; counterexample generation; automated theorem proving; exact/interval verification.

### First Research Experiment
**Проверяемый старт:** Вычислить exact treewidth extremal families и различить competing log^k growth hypotheses.

### Scores
```text
Scientific Importance: 8/10
Tractability: 5/10
Computational Accessibility: 9/10
AI Leverage: 10/10
Bridge Potential: 8/10
Underexploredness: 8/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Agrawal et al., Solving Problems on Graphs: From Structure to Algorithms, Dagstuhl Reports 15(1), 2025, DOI 10.4230/DagRep.15.1.105.
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #17 — Atoms vs. avoiding simplicial vertices

**Field:** Mathematics / Graph Algorithms  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Atoms vs. avoiding simplicial vertices» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Трудность в том, что малые примеры дают сильные закономерности, но переход к произвольному размеру требует нового invariant, extremal argument или decomposition.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Agrawal et al., Solving Problems on Graphs: From Structure to Algorithms, Dagstuhl Reports 15(1), 2025, DOI 10.4230/DagRep.15.1.105.</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Atoms vs. avoiding simplicial vertices → новый invariant/decomposition → алгоритмы и формальная верификация → перенос в соседние вычислительные области.</hypothesis>

### AI / Computational Attack Surface
exhaustive search на малых размерах; SAT/SMT/MIP; symbolic algebra; counterexample generation; automated theorem proving; exact/interval verification.

### First Research Experiment
**Проверяемый старт:** Перебрать графы до 11 вершин, сделать clique-cutset decomposition и найти minimal forbidden patterns.

### Scores
```text
Scientific Importance: 8/10
Tractability: 6/10
Computational Accessibility: 10/10
AI Leverage: 8/10
Bridge Potential: 9/10
Underexploredness: 9/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Agrawal et al., Solving Problems on Graphs: From Structure to Algorithms, Dagstuhl Reports 15(1), 2025, DOI 10.4230/DagRep.15.1.105.
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #18 — Подсчёт графов с vertex cover размера k

**Field:** Mathematics / Graph Algorithms  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Подсчёт графов с vertex cover размера k» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Трудность в том, что малые примеры дают сильные закономерности, но переход к произвольному размеру требует нового invariant, extremal argument или decomposition.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Agrawal et al., Solving Problems on Graphs: From Structure to Algorithms, Dagstuhl Reports 15(1), 2025, DOI 10.4230/DagRep.15.1.105.</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Подсчёт графов с vertex cover размера k → новый invariant/decomposition → алгоритмы и формальная верификация → перенос в соседние вычислительные области.</hypothesis>

### AI / Computational Attack Surface
exhaustive search на малых размерах; SAT/SMT/MIP; symbolic algebra; counterexample generation; automated theorem proving; exact/interval verification.

### First Research Experiment
**Проверяемый старт:** Вычислить последовательности для k≤6 и применить integer-relation/conjecture discovery.

### Scores
```text
Scientific Importance: 8/10
Tractability: 7/10
Computational Accessibility: 8/10
AI Leverage: 9/10
Bridge Potential: 10/10
Underexploredness: 7/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Agrawal et al., Solving Problems on Graphs: From Structure to Algorithms, Dagstuhl Reports 15(1), 2025, DOI 10.4230/DagRep.15.1.105.
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #19 — Longest Cycle parameterized above combinatorial bounds

**Field:** Mathematics / Graph Algorithms  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Longest Cycle parameterized above combinatorial bounds» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Трудность в том, что малые примеры дают сильные закономерности, но переход к произвольному размеру требует нового invariant, extremal argument или decomposition.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Agrawal et al., Solving Problems on Graphs: From Structure to Algorithms, Dagstuhl Reports 15(1), 2025, DOI 10.4230/DagRep.15.1.105.</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Longest Cycle parameterized above combinatorial bounds → новый invariant/decomposition → алгоритмы и формальная верификация → перенос в соседние вычислительные области.</hypothesis>

### AI / Computational Attack Surface
exhaustive search на малых размерах; SAT/SMT/MIP; symbolic algebra; counterexample generation; automated theorem proving; exact/interval verification.

### First Research Experiment
**Проверяемый старт:** Автоматически искать sound kernelization rules на малых instances.

### Scores
```text
Scientific Importance: 8/10
Tractability: 8/10
Computational Accessibility: 9/10
AI Leverage: 10/10
Bridge Potential: 8/10
Underexploredness: 8/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Agrawal et al., Solving Problems on Graphs: From Structure to Algorithms, Dagstuhl Reports 15(1), 2025, DOI 10.4230/DagRep.15.1.105.
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #20 — Single-exponential clique-width algorithms без данного k-expression

**Field:** Mathematics / Graph Algorithms  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Single-exponential clique-width algorithms без данного k-expression» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Трудность в том, что малые примеры дают сильные закономерности, но переход к произвольному размеру требует нового invariant, extremal argument или decomposition.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Agrawal et al., Solving Problems on Graphs: From Structure to Algorithms, Dagstuhl Reports 15(1), 2025, DOI 10.4230/DagRep.15.1.105.</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Single-exponential clique-width algorithms без данного k-expression → новый invariant/decomposition → алгоритмы и формальная верификация → перенос в соседние вычислительные области.</hypothesis>

### AI / Computational Attack Surface
exhaustive search на малых размерах; SAT/SMT/MIP; symbolic algebra; counterexample generation; automated theorem proving; exact/interval verification.

### First Research Experiment
**Проверяемый старт:** Использовать approximate rank-width decompositions и измерить фактическую exponential base.

### Scores
```text
Scientific Importance: 8/10
Tractability: 5/10
Computational Accessibility: 10/10
AI Leverage: 8/10
Bridge Potential: 9/10
Underexploredness: 9/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Agrawal et al., Solving Problems on Graphs: From Structure to Algorithms, Dagstuhl Reports 15(1), 2025, DOI 10.4230/DagRep.15.1.105.
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #21 — k-Induced Disjoint Paths на H3-subgraph-free graphs

**Field:** Mathematics / Graph Algorithms  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «k-Induced Disjoint Paths на H3-subgraph-free graphs» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Трудность в том, что малые примеры дают сильные закономерности, но переход к произвольному размеру требует нового invariant, extremal argument или decomposition.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Agrawal et al., Solving Problems on Graphs: From Structure to Algorithms, Dagstuhl Reports 15(1), 2025, DOI 10.4230/DagRep.15.1.105.</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>k-Induced Disjoint Paths на H3-subgraph-free graphs → новый invariant/decomposition → алгоритмы и формальная верификация → перенос в соседние вычислительные области.</hypothesis>

### AI / Computational Attack Surface
exhaustive search на малых размерах; SAT/SMT/MIP; symbolic algebra; counterexample generation; automated theorem proving; exact/interval verification.

### First Research Experiment
**Проверяемый старт:** Перебрать H3-free graphs и искать минимальные obstructions для candidate decompositions.

### Scores
```text
Scientific Importance: 8/10
Tractability: 6/10
Computational Accessibility: 8/10
AI Leverage: 9/10
Bridge Potential: 10/10
Underexploredness: 7/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Agrawal et al., Solving Problems on Graphs: From Structure to Algorithms, Dagstuhl Reports 15(1), 2025, DOI 10.4230/DagRep.15.1.105.
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #22 — Feedback Vertex Set в P_t-free bipartite graphs

**Field:** Mathematics / Graph Algorithms  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Feedback Vertex Set в P_t-free bipartite graphs» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Трудность в том, что малые примеры дают сильные закономерности, но переход к произвольному размеру требует нового invariant, extremal argument или decomposition.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Agrawal et al., Solving Problems on Graphs: From Structure to Algorithms, Dagstuhl Reports 15(1), 2025, DOI 10.4230/DagRep.15.1.105.</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Feedback Vertex Set в P_t-free bipartite graphs → новый invariant/decomposition → алгоритмы и формальная верификация → перенос в соседние вычислительные области.</hypothesis>

### AI / Computational Attack Surface
exhaustive search на малых размерах; SAT/SMT/MIP; symbolic algebra; counterexample generation; automated theorem proving; exact/interval verification.

### First Research Experiment
**Проверяемый старт:** Для t=5…9 получить exact branching signatures и вывести candidate recurrence.

### Scores
```text
Scientific Importance: 8/10
Tractability: 7/10
Computational Accessibility: 9/10
AI Leverage: 10/10
Bridge Potential: 8/10
Underexploredness: 8/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Agrawal et al., Solving Problems on Graphs: From Structure to Algorithms, Dagstuhl Reports 15(1), 2025, DOI 10.4230/DagRep.15.1.105.
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #23 — Detecting almost-complete induced minors

**Field:** Mathematics / Graph Algorithms  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Detecting almost-complete induced minors» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Трудность в том, что малые примеры дают сильные закономерности, но переход к произвольному размеру требует нового invariant, extremal argument или decomposition.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Agrawal et al., Solving Problems on Graphs: From Structure to Algorithms, Dagstuhl Reports 15(1), 2025, DOI 10.4230/DagRep.15.1.105.</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Detecting almost-complete induced minors → новый invariant/decomposition → алгоритмы и формальная верификация → перенос в соседние вычислительные области.</hypothesis>

### AI / Computational Attack Surface
exhaustive search на малых размерах; SAT/SMT/MIP; symbolic algebra; counterexample generation; automated theorem proving; exact/interval verification.

### First Research Experiment
**Проверяемый старт:** Вычислить induced-minor obstructions до 12 вершин и искать параметризуемое описание.

### Scores
```text
Scientific Importance: 8/10
Tractability: 8/10
Computational Accessibility: 10/10
AI Leverage: 8/10
Bridge Potential: 9/10
Underexploredness: 9/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Agrawal et al., Solving Problems on Graphs: From Structure to Algorithms, Dagstuhl Reports 15(1), 2025, DOI 10.4230/DagRep.15.1.105.
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #24 — Перенос свойств curve complex в framework Artin groups

**Field:** Mathematics / Low-dimensional Topology  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Перенос свойств curve complex в framework Artin groups» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Трудность в том, что малые примеры дают сильные закономерности, но переход к произвольному размеру требует нового invariant, extremal argument или decomposition.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Ohtsuki (ed.), Problems on Low-dimensional Topology, 2025, RIMS Kyoto University.</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Перенос свойств curve complex в framework Artin groups → новый invariant/decomposition → алгоритмы и формальная верификация → перенос в соседние вычислительные области.</hypothesis>

### AI / Computational Attack Surface
exhaustive search на малых размерах; SAT/SMT/MIP; symbolic algebra; counterexample generation; automated theorem proving; exact/interval verification.

### First Research Experiment
**Проверяемый старт:** Построить complexes для малых Artin groups и вычислить hyperbolicity/connectivity invariants.

### Scores
```text
Scientific Importance: 8/10
Tractability: 5/10
Computational Accessibility: 8/10
AI Leverage: 9/10
Bridge Potential: 10/10
Underexploredness: 7/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Ohtsuki (ed.), Problems on Low-dimensional Topology, 2025, RIMS Kyoto University.
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #25 — Структурные открытые вопросы о (pure) cactus groups

**Field:** Mathematics / Low-dimensional Topology  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Структурные открытые вопросы о (pure) cactus groups» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Трудность в том, что малые примеры дают сильные закономерности, но переход к произвольному размеру требует нового invariant, extremal argument или decomposition.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Ohtsuki (ed.), Problems on Low-dimensional Topology, 2025, RIMS Kyoto University.</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Структурные открытые вопросы о (pure) cactus groups → новый invariant/decomposition → алгоритмы и формальная верификация → перенос в соседние вычислительные области.</hypothesis>

### AI / Computational Attack Surface
exhaustive search на малых размерах; SAT/SMT/MIP; symbolic algebra; counterexample generation; automated theorem proving; exact/interval verification.

### First Research Experiment
**Проверяемый старт:** Вычислить low-dimensional homology и growth data для n≤10.

### Scores
```text
Scientific Importance: 8/10
Tractability: 6/10
Computational Accessibility: 9/10
AI Leverage: 10/10
Bridge Potential: 8/10
Underexploredness: 8/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Ohtsuki (ed.), Problems on Low-dimensional Topology, 2025, RIMS Kyoto University.
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #26 — Расширение skein modules до TQFT и skein modules mapping tori

**Field:** Mathematics / Low-dimensional Topology  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Расширение skein modules до TQFT и skein modules mapping tori» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Трудность в том, что малые примеры дают сильные закономерности, но переход к произвольному размеру требует нового invariant, extremal argument или decomposition.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Ohtsuki (ed.), Problems on Low-dimensional Topology, 2025, RIMS Kyoto University.</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Расширение skein modules до TQFT и skein modules mapping tori → новый invariant/decomposition → алгоритмы и формальная верификация → перенос в соседние вычислительные области.</hypothesis>

### AI / Computational Attack Surface
exhaustive search на малых размерах; SAT/SMT/MIP; symbolic algebra; counterexample generation; automated theorem proving; exact/interval verification.

### First Research Experiment
**Проверяемый старт:** Реализовать symbolic skein rewriting для малых mapping tori и сравнить dimensions.

### Scores
```text
Scientific Importance: 8/10
Tractability: 7/10
Computational Accessibility: 10/10
AI Leverage: 8/10
Bridge Potential: 9/10
Underexploredness: 9/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Ohtsuki (ed.), Problems on Low-dimensional Topology, 2025, RIMS Kyoto University.
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #27 — Конечный generating set, достигающий minimal growth rate

**Field:** Mathematics / Low-dimensional Topology  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Конечный generating set, достигающий minimal growth rate» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Трудность в том, что малые примеры дают сильные закономерности, но переход к произвольному размеру требует нового invariant, extremal argument или decomposition.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Ohtsuki (ed.), Problems on Low-dimensional Topology, 2025, RIMS Kyoto University.</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Конечный generating set, достигающий minimal growth rate → новый invariant/decomposition → алгоритмы и формальная верификация → перенос в соседние вычислительные области.</hypothesis>

### AI / Computational Attack Surface
exhaustive search на малых размерах; SAT/SMT/MIP; symbolic algebra; counterexample generation; automated theorem proving; exact/interval verification.

### First Research Experiment
**Проверяемый старт:** Перебрать Nielsen-equivalent generating sets для малых presentations.

### Scores
```text
Scientific Importance: 8/10
Tractability: 8/10
Computational Accessibility: 8/10
AI Leverage: 9/10
Bridge Potential: 10/10
Underexploredness: 7/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Ohtsuki (ed.), Problems on Low-dimensional Topology, 2025, RIMS Kyoto University.
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #28 — Полная chart description knitted surfaces

**Field:** Mathematics / Low-dimensional Topology  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Полная chart description knitted surfaces» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Трудность в том, что малые примеры дают сильные закономерности, но переход к произвольному размеру требует нового invariant, extremal argument или decomposition.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Ohtsuki (ed.), Problems on Low-dimensional Topology, 2025, RIMS Kyoto University.</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Полная chart description knitted surfaces → новый invariant/decomposition → алгоритмы и формальная верификация → перенос в соседние вычислительные области.</hypothesis>

### AI / Computational Attack Surface
exhaustive search на малых размерах; SAT/SMT/MIP; symbolic algebra; counterexample generation; automated theorem proving; exact/interval verification.

### First Research Experiment
**Проверяемый старт:** Перечислить chart move-equivalence classes ограниченной сложности.

### Scores
```text
Scientific Importance: 8/10
Tractability: 5/10
Computational Accessibility: 9/10
AI Leverage: 10/10
Bridge Potential: 8/10
Underexploredness: 8/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Ohtsuki (ed.), Problems on Low-dimensional Topology, 2025, RIMS Kyoto University.
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #29 — Plat presentations для surface-links

**Field:** Mathematics / Low-dimensional Topology  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Plat presentations для surface-links» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Трудность в том, что малые примеры дают сильные закономерности, но переход к произвольному размеру требует нового invariant, extremal argument или decomposition.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Ohtsuki (ed.), Problems on Low-dimensional Topology, 2025, RIMS Kyoto University.</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Plat presentations для surface-links → новый invariant/decomposition → алгоритмы и формальная верификация → перенос в соседние вычислительные области.</hypothesis>

### AI / Computational Attack Surface
exhaustive search на малых размерах; SAT/SMT/MIP; symbolic algebra; counterexample generation; automated theorem proving; exact/interval verification.

### First Research Experiment
**Проверяемый старт:** Искать минимальные plat presentations малых surface-link diagrams exhaustive search.

### Scores
```text
Scientific Importance: 8/10
Tractability: 6/10
Computational Accessibility: 10/10
AI Leverage: 8/10
Bridge Potential: 9/10
Underexploredness: 9/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Ohtsuki (ed.), Problems on Low-dimensional Topology, 2025, RIMS Kyoto University.
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #30 — Sharp tensor concentration inequalities, не сводящиеся к грубой matricization

**Field:** Mathematics / Probability  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Sharp tensor concentration inequalities, не сводящиеся к грубой matricization» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Трудность в том, что малые примеры дают сильные закономерности, но переход к произвольному размеру требует нового invariant, extremal argument или decomposition.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Bandeira et al., Randomstrasse101: Open Problems of 2025, arXiv:2603.29571 (2026).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Sharp tensor concentration inequalities, не сводящиеся к грубой matricization → новый invariant/decomposition → алгоритмы и формальная верификация → перенос в соседние вычислительные области.</hypothesis>

### AI / Computational Attack Surface
exhaustive search на малых размерах; SAT/SMT/MIP; symbolic algebra; counterexample generation; automated theorem proving; exact/interval verification.

### First Research Experiment
**Проверяемый старт:** Искать случайные 3-тензоры, максимизирующие отношение empirical tail к candidate bound.

### Scores
```text
Scientific Importance: 8/10
Tractability: 7/10
Computational Accessibility: 8/10
AI Leverage: 9/10
Bridge Potential: 10/10
Underexploredness: 7/10
Verification Clarity: 10/10
```

### Evidence
- Primary/current source: Bandeira et al., Randomstrasse101: Open Problems of 2025, arXiv:2603.29571 (2026).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #31 — Типичный Lovász theta number случайных circulant graphs

**Field:** Mathematics / Probabilistic Combinatorics  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Типичный Lovász theta number случайных circulant graphs» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Трудность в том, что малые примеры дают сильные закономерности, но переход к произвольному размеру требует нового invariant, extremal argument или decomposition.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Bandeira et al., Randomstrasse101: Open Problems of 2025, arXiv:2603.29571 (2026).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Типичный Lovász theta number случайных circulant graphs → новый invariant/decomposition → алгоритмы и формальная верификация → перенос в соседние вычислительные области.</hypothesis>

### AI / Computational Attack Surface
exhaustive search на малых размерах; SAT/SMT/MIP; symbolic algebra; counterexample generation; automated theorem proving; exact/interval verification.

### First Research Experiment
**Проверяемый старт:** Вычислить symmetry-reduced SDP для тысяч circulants и оценить scaling.

### Scores
```text
Scientific Importance: 8/10
Tractability: 8/10
Computational Accessibility: 9/10
AI Leverage: 10/10
Bridge Potential: 8/10
Underexploredness: 8/10
Verification Clarity: 10/10
```

### Evidence
- Primary/current source: Bandeira et al., Randomstrasse101: Open Problems of 2025, arXiv:2603.29571 (2026).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #32 — Injectivity и stability phase retrieval для structured measurements

**Field:** Applied Mathematics / Inverse Problems  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Injectivity и stability phase retrieval для structured measurements» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Трудность в том, что малые примеры дают сильные закономерности, но переход к произвольному размеру требует нового invariant, extremal argument или decomposition.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Melnyk et al., Phasebook: a survey of selected open problems in phase retrieval, 2025.</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Injectivity и stability phase retrieval для structured measurements → новый invariant/decomposition → алгоритмы и формальная верификация → перенос в соседние вычислительные области.</hypothesis>

### AI / Computational Attack Surface
exhaustive search на малых размерах; SAT/SMT/MIP; symbolic algebra; counterexample generation; automated theorem proving; exact/interval verification.

### First Research Experiment
**Проверяемый старт:** Искать certified ambiguous signal pairs для candidate structured ensembles.

### Scores
```text
Scientific Importance: 9/10
Tractability: 5/10
Computational Accessibility: 10/10
AI Leverage: 8/10
Bridge Potential: 9/10
Underexploredness: 9/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Melnyk et al., Phasebook: a survey of selected open problems in phase retrieval, 2025.
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #33 — Правильный порядок констант quantitative Helly/Steinitz

**Field:** Mathematics / Convex Geometry  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Правильный порядок констант quantitative Helly/Steinitz» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Трудность в том, что малые примеры дают сильные закономерности, но переход к произвольному размеру требует нового invariant, extremal argument или decomposition.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Naszódi, Quantitative Helly-type problems, Analysis Mathematica 51 (2025), DOI 10.1007/s10476-025-00127-z.</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Правильный порядок констант quantitative Helly/Steinitz → новый invariant/decomposition → алгоритмы и формальная верификация → перенос в соседние вычислительные области.</hypothesis>

### AI / Computational Attack Surface
exhaustive search на малых размерах; SAT/SMT/MIP; symbolic algebra; counterexample generation; automated theorem proving; exact/interval verification.

### First Research Experiment
**Проверяемый старт:** Оптимизировать extremal configurations в d=2…8 и вывести asymptotic hypothesis.

### Scores
```text
Scientific Importance: 8/10
Tractability: 6/10
Computational Accessibility: 8/10
AI Leverage: 9/10
Bridge Potential: 10/10
Underexploredness: 7/10
Verification Clarity: 10/10
```

### Evidence
- Primary/current source: Naszódi, Quantitative Helly-type problems, Analysis Mathematica 51 (2025), DOI 10.1007/s10476-025-00127-z.
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #34 — Завершение классификации групп порядка 1024 на умеренных ресурсах

**Field:** Mathematics / Computational Group Theory  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Завершение классификации групп порядка 1024 на умеренных ресурсах» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Трудность в том, что малые примеры дают сильные закономерности, но переход к произвольному размеру требует нового invariant, extremal argument или decomposition.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Eick, Classification of Finite Groups: Recent Developements and Open Problems, Foundations of Computational Mathematics 25 (2025), DOI 10.1007/s10208-024-09688-1.</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Завершение классификации групп порядка 1024 на умеренных ресурсах → новый invariant/decomposition → алгоритмы и формальная верификация → перенос в соседние вычислительные области.</hypothesis>

### AI / Computational Attack Surface
exhaustive search на малых размерах; SAT/SMT/MIP; symbolic algebra; counterexample generation; automated theorem proving; exact/interval verification.

### First Research Experiment
**Проверяемый старт:** Профилировать extension/isomorphism pipeline и искать exact-preserving pruning rules.

### Scores
```text
Scientific Importance: 8/10
Tractability: 7/10
Computational Accessibility: 9/10
AI Leverage: 10/10
Bridge Potential: 8/10
Underexploredness: 8/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Eick, Classification of Finite Groups: Recent Developements and Open Problems, Foundations of Computational Mathematics 25 (2025), DOI 10.1007/s10208-024-09688-1.
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #35 — Классификация групп порядка p^n q для n≤7

**Field:** Mathematics / Computational Algebra  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Классификация групп порядка p^n q для n≤7» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Трудность в том, что малые примеры дают сильные закономерности, но переход к произвольному размеру требует нового invariant, extremal argument или decomposition.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Eick, Classification of Finite Groups: Recent Developements and Open Problems, Foundations of Computational Mathematics 25 (2025), DOI 10.1007/s10208-024-09688-1.</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Классификация групп порядка p^n q для n≤7 → новый invariant/decomposition → алгоритмы и формальная верификация → перенос в соседние вычислительные области.</hypothesis>

### AI / Computational Attack Surface
exhaustive search на малых размерах; SAT/SMT/MIP; symbolic algebra; counterexample generation; automated theorem proving; exact/interval verification.

### First Research Experiment
**Проверяемый старт:** Закрыть один новый congruence slice при n=6 с machine-checkable case log.

### Scores
```text
Scientific Importance: 8/10
Tractability: 8/10
Computational Accessibility: 10/10
AI Leverage: 8/10
Bridge Potential: 9/10
Underexploredness: 9/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Eick, Classification of Finite Groups: Recent Developements and Open Problems, Foundations of Computational Mathematics 25 (2025), DOI 10.1007/s10208-024-09688-1.
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #36 — Robust scalable iterative solvers для high-frequency Helmholtz/convection-dominated PDE

**Field:** Applied Mathematics / Numerical Linear Algebra  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Robust scalable iterative solvers для high-frequency Helmholtz/convection-dominated PDE» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Трудность в том, что малые примеры дают сильные закономерности, но переход к произвольному размеру требует нового invariant, extremal argument или decomposition.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Amsel et al., Linear Systems and Eigenvalue Problems: Open Questions from a Simons Workshop, arXiv:2602.05394 (2026; updated Aug. 2026).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Robust scalable iterative solvers для high-frequency Helmholtz/convection-dominated PDE → новый invariant/decomposition → алгоритмы и формальная верификация → перенос в соседние вычислительные области.</hypothesis>

### AI / Computational Attack Surface
exhaustive search на малых размерах; SAT/SMT/MIP; symbolic algebra; counterexample generation; automated theorem proving; exact/interval verification.

### First Research Experiment
**Проверяемый старт:** Создать parameter grid и автоматически искать композиции classical preconditioners.

### Scores
```text
Scientific Importance: 9/10
Tractability: 5/10
Computational Accessibility: 8/10
AI Leverage: 9/10
Bridge Potential: 10/10
Underexploredness: 7/10
Verification Clarity: 10/10
```

### Evidence
- Primary/current source: Amsel et al., Linear Systems and Eigenvalue Problems: Open Questions from a Simons Workshop, arXiv:2602.05394 (2026; updated Aug. 2026).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #37 — Forsythe conjecture для restarted conjugate gradient

**Field:** Applied Mathematics / Numerical Linear Algebra  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Forsythe conjecture для restarted conjugate gradient» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Трудность в том, что малые примеры дают сильные закономерности, но переход к произвольному размеру требует нового invariant, extremal argument или decomposition.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Amsel et al., Linear Systems and Eigenvalue Problems: Open Questions from a Simons Workshop, arXiv:2602.05394 (2026; updated Aug. 2026).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Forsythe conjecture для restarted conjugate gradient → новый invariant/decomposition → алгоритмы и формальная верификация → перенос в соседние вычислительные области.</hypothesis>

### AI / Computational Attack Surface
exhaustive search на малых размерах; SAT/SMT/MIP; symbolic algebra; counterexample generation; automated theorem proving; exact/interval verification.

### First Research Experiment
**Проверяемый старт:** В exact rational arithmetic искать минимальный counterexample на малых SPD matrices.

### Scores
```text
Scientific Importance: 9/10
Tractability: 6/10
Computational Accessibility: 9/10
AI Leverage: 10/10
Bridge Potential: 8/10
Underexploredness: 8/10
Verification Clarity: 10/10
```

### Evidence
- Primary/current source: Amsel et al., Linear Systems and Eigenvalue Problems: Open Questions from a Simons Workshop, arXiv:2602.05394 (2026; updated Aug. 2026).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #38 — O(n^3) backward-stable полная diagonalization общей матрицы

**Field:** Applied Mathematics / Numerical Linear Algebra  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «O(n^3) backward-stable полная diagonalization общей матрицы» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Трудность в том, что малые примеры дают сильные закономерности, но переход к произвольному размеру требует нового invariant, extremal argument или decomposition.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Amsel et al., Linear Systems and Eigenvalue Problems: Open Questions from a Simons Workshop, arXiv:2602.05394 (2026; updated Aug. 2026).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>O(n^3) backward-stable полная diagonalization общей матрицы → новый invariant/decomposition → алгоритмы и формальная верификация → перенос в соседние вычислительные области.</hypothesis>

### AI / Computational Attack Surface
exhaustive search на малых размерах; SAT/SMT/MIP; symbolic algebra; counterexample generation; automated theorem proving; exact/interval verification.

### First Research Experiment
**Проверяемый старт:** Тестировать candidate factorization pipelines на adversarial nonnormal matrices с high-precision oracle.

### Scores
```text
Scientific Importance: 9/10
Tractability: 7/10
Computational Accessibility: 10/10
AI Leverage: 8/10
Bridge Potential: 9/10
Underexploredness: 9/10
Verification Clarity: 10/10
```

### Evidence
- Primary/current source: Amsel et al., Linear Systems and Eigenvalue Problems: Open Questions from a Simons Workshop, arXiv:2602.05394 (2026; updated Aug. 2026).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #39 — Детерминированное pseudospectral shattering

**Field:** Applied Mathematics / Numerical Linear Algebra  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Детерминированное pseudospectral shattering» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Трудность в том, что малые примеры дают сильные закономерности, но переход к произвольному размеру требует нового invariant, extremal argument или decomposition.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Amsel et al., Linear Systems and Eigenvalue Problems: Open Questions from a Simons Workshop, arXiv:2602.05394 (2026; updated Aug. 2026).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Детерминированное pseudospectral shattering → новый invariant/decomposition → алгоритмы и формальная верификация → перенос в соседние вычислительные области.</hypothesis>

### AI / Computational Attack Surface
exhaustive search на малых размерах; SAT/SMT/MIP; symbolic algebra; counterexample generation; automated theorem proving; exact/interval verification.

### First Research Experiment
**Проверяемый старт:** Оптимизировать deterministic perturbation directions на малых nonnormal matrices.

### Scores
```text
Scientific Importance: 9/10
Tractability: 8/10
Computational Accessibility: 8/10
AI Leverage: 9/10
Bridge Potential: 10/10
Underexploredness: 7/10
Verification Clarity: 10/10
```

### Evidence
- Primary/current source: Amsel et al., Linear Systems and Eigenvalue Problems: Open Questions from a Simons Workshop, arXiv:2602.05394 (2026; updated Aug. 2026).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #40 — Полная характеризация сходимости Ritz values для non-Hermitian matrices

**Field:** Applied Mathematics / Numerical Linear Algebra  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Полная характеризация сходимости Ritz values для non-Hermitian matrices» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Трудность в том, что малые примеры дают сильные закономерности, но переход к произвольному размеру требует нового invariant, extremal argument или decomposition.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Amsel et al., Linear Systems and Eigenvalue Problems: Open Questions from a Simons Workshop, arXiv:2602.05394 (2026; updated Aug. 2026).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Полная характеризация сходимости Ritz values для non-Hermitian matrices → новый invariant/decomposition → алгоритмы и формальная верификация → перенос в соседние вычислительные области.</hypothesis>

### AI / Computational Attack Surface
exhaustive search на малых размерах; SAT/SMT/MIP; symbolic algebra; counterexample generation; automated theorem proving; exact/interval verification.

### First Research Experiment
**Проверяемый старт:** Сэмплировать Jordan/pseudospectral families и искать минимальный predictive invariant set.

### Scores
```text
Scientific Importance: 9/10
Tractability: 5/10
Computational Accessibility: 9/10
AI Leverage: 10/10
Bridge Potential: 8/10
Underexploredness: 8/10
Verification Clarity: 10/10
```

### Evidence
- Primary/current source: Amsel et al., Linear Systems and Eigenvalue Problems: Open Questions from a Simons Workshop, arXiv:2602.05394 (2026; updated Aug. 2026).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #41 — Quasi-optimal greedy row/column subset selection

**Field:** Applied Mathematics / Numerical Linear Algebra  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Quasi-optimal greedy row/column subset selection» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Трудность в том, что малые примеры дают сильные закономерности, но переход к произвольному размеру требует нового invariant, extremal argument или decomposition.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Amsel et al., Linear Systems and Eigenvalue Problems: Open Questions from a Simons Workshop, arXiv:2602.05394 (2026; updated Aug. 2026).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Quasi-optimal greedy row/column subset selection → новый invariant/decomposition → алгоритмы и формальная верификация → перенос в соседние вычислительные области.</hypothesis>

### AI / Computational Attack Surface
exhaustive search на малых размерах; SAT/SMT/MIP; symbolic algebra; counterexample generation; automated theorem proving; exact/interval verification.

### First Research Experiment
**Проверяемый старт:** Дифференцируемо искать worst-case matrices для CPQR/greedy против global optimum.

### Scores
```text
Scientific Importance: 9/10
Tractability: 6/10
Computational Accessibility: 10/10
AI Leverage: 8/10
Bridge Potential: 9/10
Underexploredness: 9/10
Verification Clarity: 10/10
```

### Evidence
- Primary/current source: Amsel et al., Linear Systems and Eigenvalue Problems: Open Questions from a Simons Workshop, arXiv:2602.05394 (2026; updated Aug. 2026).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #42 — Tight error bounds для DLR / complete pivoting

**Field:** Applied Mathematics / Numerical Linear Algebra  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Tight error bounds для DLR / complete pivoting» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Трудность в том, что малые примеры дают сильные закономерности, но переход к произвольному размеру требует нового invariant, extremal argument или decomposition.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Amsel et al., Linear Systems and Eigenvalue Problems: Open Questions from a Simons Workshop, arXiv:2602.05394 (2026; updated Aug. 2026).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Tight error bounds для DLR / complete pivoting → новый invariant/decomposition → алгоритмы и формальная верификация → перенос в соседние вычислительные области.</hypothesis>

### AI / Computational Attack Surface
exhaustive search на малых размерах; SAT/SMT/MIP; symbolic algebra; counterexample generation; automated theorem proving; exact/interval verification.

### First Research Experiment
**Проверяемый старт:** Сканировать structured kernel matrices и находить worst-case pivot growth.

### Scores
```text
Scientific Importance: 9/10
Tractability: 7/10
Computational Accessibility: 8/10
AI Leverage: 9/10
Bridge Potential: 10/10
Underexploredness: 7/10
Verification Clarity: 10/10
```

### Evidence
- Primary/current source: Amsel et al., Linear Systems and Eigenvalue Problems: Open Questions from a Simons Workshop, arXiv:2602.05394 (2026; updated Aug. 2026).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #43 — Достаточна ли injection вместо OSE для least squares/SVD

**Field:** Applied Mathematics / Numerical Linear Algebra  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Достаточна ли injection вместо OSE для least squares/SVD» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Трудность в том, что малые примеры дают сильные закономерности, но переход к произвольному размеру требует нового invariant, extremal argument или decomposition.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Amsel et al., Linear Systems and Eigenvalue Problems: Open Questions from a Simons Workshop, arXiv:2602.05394 (2026; updated Aug. 2026).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Достаточна ли injection вместо OSE для least squares/SVD → новый invariant/decomposition → алгоритмы и формальная верификация → перенос в соседние вычислительные области.</hypothesis>

### AI / Computational Attack Surface
exhaustive search на малых размерах; SAT/SMT/MIP; symbolic algebra; counterexample generation; automated theorem proving; exact/interval verification.

### First Research Experiment
**Проверяемый старт:** Искать sketch distributions, injective w.h.p., но нарушающие OSE, и тестировать LS error.

### Scores
```text
Scientific Importance: 9/10
Tractability: 8/10
Computational Accessibility: 9/10
AI Leverage: 10/10
Bridge Potential: 8/10
Underexploredness: 8/10
Verification Clarity: 10/10
```

### Evidence
- Primary/current source: Amsel et al., Linear Systems and Eigenvalue Problems: Open Questions from a Simons Workshop, arXiv:2602.05394 (2026; updated Aug. 2026).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #44 — Nelson–Nguyen sparse dimensionality-reduction conjecture

**Field:** Applied Mathematics / Numerical Linear Algebra  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Nelson–Nguyen sparse dimensionality-reduction conjecture» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Трудность в том, что малые примеры дают сильные закономерности, но переход к произвольному размеру требует нового invariant, extremal argument или decomposition.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Amsel et al., Linear Systems and Eigenvalue Problems: Open Questions from a Simons Workshop, arXiv:2602.05394 (2026; updated Aug. 2026).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Nelson–Nguyen sparse dimensionality-reduction conjecture → новый invariant/decomposition → алгоритмы и формальная верификация → перенос в соседние вычислительные области.</hypothesis>

### AI / Computational Attack Surface
exhaustive search на малых размерах; SAT/SMT/MIP; symbolic algebra; counterexample generation; automated theorem proving; exact/interval verification.

### First Research Experiment
**Проверяемый старт:** Решить exact feasibility малых parameter tuples через SAT/MIP.

### Scores
```text
Scientific Importance: 9/10
Tractability: 5/10
Computational Accessibility: 10/10
AI Leverage: 8/10
Bridge Potential: 9/10
Underexploredness: 9/10
Verification Clarity: 10/10
```

### Evidence
- Primary/current source: Amsel et al., Linear Systems and Eigenvalue Problems: Open Questions from a Simons Workshop, arXiv:2602.05394 (2026; updated Aug. 2026).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #45 — Polynomial-time Tensor Train approximation лучше m−1 factor

**Field:** Applied Mathematics / Numerical Linear Algebra  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Polynomial-time Tensor Train approximation лучше m−1 factor» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Трудность в том, что малые примеры дают сильные закономерности, но переход к произвольному размеру требует нового invariant, extremal argument или decomposition.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Amsel et al., Linear Systems and Eigenvalue Problems: Open Questions from a Simons Workshop, arXiv:2602.05394 (2026; updated Aug. 2026).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Polynomial-time Tensor Train approximation лучше m−1 factor → новый invariant/decomposition → алгоритмы и формальная верификация → перенос в соседние вычислительные области.</hypothesis>

### AI / Computational Attack Surface
exhaustive search на малых размерах; SAT/SMT/MIP; symbolic algebra; counterexample generation; automated theorem proving; exact/interval verification.

### First Research Experiment
**Проверяемый старт:** Искать small-tensor extremizers ratio TT-SVD/global optimum.

### Scores
```text
Scientific Importance: 9/10
Tractability: 6/10
Computational Accessibility: 8/10
AI Leverage: 9/10
Bridge Potential: 10/10
Underexploredness: 7/10
Verification Clarity: 10/10
```

### Evidence
- Primary/current source: Amsel et al., Linear Systems and Eigenvalue Problems: Open Questions from a Simons Workshop, arXiv:2602.05394 (2026; updated Aug. 2026).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #46 — NEPv solver с superlinear convergence и линейной стоимостью итерации

**Field:** Applied Mathematics / Numerical Linear Algebra  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «NEPv solver с superlinear convergence и линейной стоимостью итерации» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Трудность в том, что малые примеры дают сильные закономерности, но переход к произвольному размеру требует нового invariant, extremal argument или decomposition.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Amsel et al., Linear Systems and Eigenvalue Problems: Open Questions from a Simons Workshop, arXiv:2602.05394 (2026; updated Aug. 2026).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>NEPv solver с superlinear convergence и линейной стоимостью итерации → новый invariant/decomposition → алгоритмы и формальная верификация → перенос в соседние вычислительные области.</hypothesis>

### AI / Computational Attack Surface
exhaustive search на малых размерах; SAT/SMT/MIP; symbolic algebra; counterexample generation; automated theorem proving; exact/interval verification.

### First Research Experiment
**Проверяемый старт:** Тестировать low-rank Jacobian updates на parameterized nonlinear eigenproblems.

### Scores
```text
Scientific Importance: 9/10
Tractability: 7/10
Computational Accessibility: 9/10
AI Leverage: 10/10
Bridge Potential: 8/10
Underexploredness: 8/10
Verification Clarity: 10/10
```

### Evidence
- Primary/current source: Amsel et al., Linear Systems and Eigenvalue Problems: Open Questions from a Simons Workshop, arXiv:2602.05394 (2026; updated Aug. 2026).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #47 — Оптимальная product complexity аппроксимации matrix sign

**Field:** Applied Mathematics / Numerical Linear Algebra  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Оптимальная product complexity аппроксимации matrix sign» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Трудность в том, что малые примеры дают сильные закономерности, но переход к произвольному размеру требует нового invariant, extremal argument или decomposition.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Amsel et al., Linear Systems and Eigenvalue Problems: Open Questions from a Simons Workshop, arXiv:2602.05394 (2026; updated Aug. 2026).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Оптимальная product complexity аппроксимации matrix sign → новый invariant/decomposition → алгоритмы и формальная верификация → перенос в соседние вычислительные области.</hypothesis>

### AI / Computational Attack Surface
exhaustive search на малых размерах; SAT/SMT/MIP; symbolic algebra; counterexample generation; automated theorem proving; exact/interval verification.

### First Research Experiment
**Проверяемый старт:** Синтезировать multiplication circuits глубины 3–6 и оптимизировать coefficients.

### Scores
```text
Scientific Importance: 9/10
Tractability: 8/10
Computational Accessibility: 10/10
AI Leverage: 8/10
Bridge Potential: 9/10
Underexploredness: 9/10
Verification Clarity: 10/10
```

### Evidence
- Primary/current source: Amsel et al., Linear Systems and Eigenvalue Problems: Open Questions from a Simons Workshop, arXiv:2602.05394 (2026; updated Aug. 2026).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #48 — Unified global nonsmooth dynamics при uncertainty/stochasticity

**Field:** Mathematics / Nonsmooth Dynamical Systems  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Unified global nonsmooth dynamics при uncertainty/stochasticity» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Трудность в том, что малые примеры дают сильные закономерности, но переход к произвольному размеру требует нового invariant, extremal argument или decomposition.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Beyond the Bristol book: Advances and perspectives in non-smooth dynamics and applications, Chaos 33 (2023), section XIII Open Problems and Challenges.</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Unified global nonsmooth dynamics при uncertainty/stochasticity → новый invariant/decomposition → алгоритмы и формальная верификация → перенос в соседние вычислительные области.</hypothesis>

### AI / Computational Attack Surface
exhaustive search на малых размерах; SAT/SMT/MIP; symbolic algebra; counterexample generation; automated theorem proving; exact/interval verification.

### First Research Experiment
**Проверяемый старт:** Собрать benchmark impact/switching models и сравнить invariant descriptors.

### Scores
```text
Scientific Importance: 8/10
Tractability: 5/10
Computational Accessibility: 8/10
AI Leverage: 9/10
Bridge Potential: 10/10
Underexploredness: 7/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Beyond the Bristol book: Advances and perspectives in non-smooth dynamics and applications, Chaos 33 (2023), section XIII Open Problems and Challenges.
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #49 — Аналитическая теория конструктивной роли nonsmoothness в stabilization/control

**Field:** Mathematics / Nonsmooth Dynamical Systems  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Аналитическая теория конструктивной роли nonsmoothness в stabilization/control» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Трудность в том, что малые примеры дают сильные закономерности, но переход к произвольному размеру требует нового invariant, extremal argument или decomposition.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Beyond the Bristol book: Advances and perspectives in non-smooth dynamics and applications, Chaos 33 (2023), section XIII Open Problems and Challenges.</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Аналитическая теория конструктивной роли nonsmoothness в stabilization/control → новый invariant/decomposition → алгоритмы и формальная верификация → перенос в соседние вычислительные области.</hypothesis>

### AI / Computational Attack Surface
exhaustive search на малых размерах; SAT/SMT/MIP; symbolic algebra; counterexample generation; automated theorem proving; exact/interval verification.

### First Research Experiment
**Проверяемый старт:** Искать кусочно-гладкие Lyapunov certificates через SMT/SOS.

### Scores
```text
Scientific Importance: 8/10
Tractability: 6/10
Computational Accessibility: 9/10
AI Leverage: 10/10
Bridge Potential: 8/10
Underexploredness: 8/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Beyond the Bristol book: Advances and perspectives in non-smooth dynamics and applications, Chaos 33 (2023), section XIII Open Problems and Challenges.
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #50 — Rigorous theory Markov-switching nonlinear networks

**Field:** Mathematics / Nonsmooth Dynamical Systems  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Rigorous theory Markov-switching nonlinear networks» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Трудность в том, что малые примеры дают сильные закономерности, но переход к произвольному размеру требует нового invariant, extremal argument или decomposition.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Beyond the Bristol book: Advances and perspectives in non-smooth dynamics and applications, Chaos 33 (2023), section XIII Open Problems and Challenges.</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Rigorous theory Markov-switching nonlinear networks → новый invariant/decomposition → алгоритмы и формальная верификация → перенос в соседние вычислительные области.</hypothesis>

### AI / Computational Attack Surface
exhaustive search на малых размерах; SAT/SMT/MIP; symbolic algebra; counterexample generation; automated theorem proving; exact/interval verification.

### First Research Experiment
**Проверяемый старт:** Точно вычислить stability boundaries малых network motifs по switching rates.

### Scores
```text
Scientific Importance: 8/10
Tractability: 7/10
Computational Accessibility: 10/10
AI Leverage: 8/10
Bridge Potential: 9/10
Underexploredness: 9/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Beyond the Bristol book: Advances and perspectives in non-smooth dynamics and applications, Chaos 33 (2023), section XIII Open Problems and Challenges.
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #51 — Критерий: когда шум regularizes или усиливает grazing bifurcations

**Field:** Mathematics / Nonsmooth Dynamical Systems  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Критерий: когда шум regularizes или усиливает grazing bifurcations» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Трудность в том, что малые примеры дают сильные закономерности, но переход к произвольному размеру требует нового invariant, extremal argument или decomposition.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Beyond the Bristol book: Advances and perspectives in non-smooth dynamics and applications, Chaos 33 (2023), section XIII Open Problems and Challenges.</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Критерий: когда шум regularizes или усиливает grazing bifurcations → новый invariant/decomposition → алгоритмы и формальная верификация → перенос в соседние вычислительные области.</hypothesis>

### AI / Computational Attack Surface
exhaustive search на малых размерах; SAT/SMT/MIP; symbolic algebra; counterexample generation; automated theorem proving; exact/interval verification.

### First Research Experiment
**Проверяемый старт:** Построить phase diagram canonical grazing map по noise amplitude/color.

### Scores
```text
Scientific Importance: 8/10
Tractability: 8/10
Computational Accessibility: 8/10
AI Leverage: 9/10
Bridge Potential: 10/10
Underexploredness: 7/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Beyond the Bristol book: Advances and perspectives in non-smooth dynamics and applications, Chaos 33 (2023), section XIII Open Problems and Challenges.
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #52 — Probabilistic basins of attraction в stochastic nonsmooth systems

**Field:** Mathematics / Nonsmooth Dynamical Systems  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Probabilistic basins of attraction в stochastic nonsmooth systems» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Трудность в том, что малые примеры дают сильные закономерности, но переход к произвольному размеру требует нового invariant, extremal argument или decomposition.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Beyond the Bristol book: Advances and perspectives in non-smooth dynamics and applications, Chaos 33 (2023), section XIII Open Problems and Challenges.</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Probabilistic basins of attraction в stochastic nonsmooth systems → новый invariant/decomposition → алгоритмы и формальная верификация → перенос в соседние вычислительные области.</hypothesis>

### AI / Computational Attack Surface
exhaustive search на малых размерах; SAT/SMT/MIP; symbolic algebra; counterexample generation; automated theorem proving; exact/interval verification.

### First Research Experiment
**Проверяемый старт:** Сравнить set-oriented numerics, reachability и Monte Carlo oracle на 2D systems.

### Scores
```text
Scientific Importance: 8/10
Tractability: 5/10
Computational Accessibility: 9/10
AI Leverage: 10/10
Bridge Potential: 8/10
Underexploredness: 8/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Beyond the Bristol book: Advances and perspectives in non-smooth dynamics and applications, Chaos 33 (2023), section XIII Open Problems and Challenges.
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #53 — Универсальность sausage-string mode-locking structure

**Field:** Mathematics / Nonsmooth Dynamical Systems  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Универсальность sausage-string mode-locking structure» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Трудность в том, что малые примеры дают сильные закономерности, но переход к произвольному размеру требует нового invariant, extremal argument или decomposition.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Beyond the Bristol book: Advances and perspectives in non-smooth dynamics and applications, Chaos 33 (2023), section XIII Open Problems and Challenges.</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Универсальность sausage-string mode-locking structure → новый invariant/decomposition → алгоритмы и формальная верификация → перенос в соседние вычислительные области.</hypothesis>

### AI / Computational Attack Surface
exhaustive search на малых размерах; SAT/SMT/MIP; symbolic algebra; counterexample generation; automated theorem proving; exact/interval verification.

### First Research Experiment
**Проверяемый старт:** Сравнить pinch-point symbolic transitions в нескольких классах nonsmooth/delay systems.

### Scores
```text
Scientific Importance: 8/10
Tractability: 6/10
Computational Accessibility: 10/10
AI Leverage: 8/10
Bridge Potential: 9/10
Underexploredness: 9/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Beyond the Bristol book: Advances and perspectives in non-smooth dynamics and applications, Chaos 33 (2023), section XIII Open Problems and Challenges.
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #54 — Полный набор mutually unbiased bases в C^6

**Field:** Physics / Quantum Information  
**Status:** Open  
**Difficulty:** Very High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Полный набор mutually unbiased bases в C^6» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Нужно отделить универсальную структуру от model-specific эффектов и получить вычислимый критерий, выдерживающий предельные/шумовые режимы.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: McNulty & Weigert, Mutually Unbiased Bases in Composite Dimensions – A Review, Quantum 10, 2051 (2026).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Полный набор mutually unbiased bases в C^6 → новый coarse-grained принцип → optimization / statistical mechanics → predictive design или control.</hypothesis>

### AI / Computational Attack Surface
simulation; optimization; symbolic search; model comparison; counterexample generation; uncertainty-aware AI assistance.

### First Research Experiment
**Проверяемый старт:** Certified branch-and-bound поиск четвёртой MUB в классифицированных Hadamard families.

### Scores
```text
Scientific Importance: 9/10
Tractability: 7/10
Computational Accessibility: 8/10
AI Leverage: 9/10
Bridge Potential: 10/10
Underexploredness: 7/10
Verification Clarity: 10/10
```

### Evidence
- Primary/current source: McNulty & Weigert, Mutually Unbiased Bases in Composite Dimensions – A Review, Quantum 10, 2051 (2026).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #55 — SIC-POVM: существование хотя бы в бесконечной последовательности новых размерностей

**Field:** Physics / Quantum Information  
**Status:** Open  
**Difficulty:** Very High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «SIC-POVM: существование хотя бы в бесконечной последовательности новых размерностей» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Нужно отделить универсальную структуру от model-specific эффектов и получить вычислимый критерий, выдерживающий предельные/шумовые режимы.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: 2026 SIC-POVM literature including Journal of Algebraic Combinatorics, explicitly stating all-dimension existence remains open.</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>SIC-POVM: существование хотя бы в бесконечной последовательности новых размерностей → новый coarse-grained принцип → optimization / statistical mechanics → predictive design или control.</hypothesis>

### AI / Computational Attack Surface
simulation; optimization; symbolic search; model comparison; counterexample generation; uncertainty-aware AI assistance.

### First Research Experiment
**Проверяемый старт:** Из high-precision numerical SIC автоматически реконструировать number fields и Galois patterns.

### Scores
```text
Scientific Importance: 9/10
Tractability: 8/10
Computational Accessibility: 9/10
AI Leverage: 10/10
Bridge Potential: 8/10
Underexploredness: 8/10
Verification Clarity: 10/10
```

### Evidence
- Primary/current source: 2026 SIC-POVM literature including Journal of Algebraic Combinatorics, explicitly stating all-dimension existence remains open.
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #56 — Практичная полная характеристика single-copy saturability multiparameter QCRB

**Field:** Physics / Quantum Metrology  
**Status:** Partially Open  
**Difficulty:** Very High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Практичная полная характеристика single-copy saturability multiparameter QCRB» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Нужно отделить универсальную структуру от model-specific эффектов и получить вычислимый критерий, выдерживающий предельные/шумовые режимы.

### What Is Already Known
<fact>Есть существенные частичные результаты, но исходная tight/общая постановка не закрыта. Основная свежая точка опоры: Yang, Imai & Pezzè, A geometric criterion for optimal measurements in multiparameter quantum metrology, arXiv:2601.21801 (2026).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Практичная полная характеристика single-copy saturability multiparameter QCRB → новый coarse-grained принцип → optimization / statistical mechanics → predictive design или control.</hypothesis>

### AI / Computational Attack Surface
simulation; optimization; symbolic search; model comparison; counterexample generation; uncertainty-aware AI assistance.

### First Research Experiment
**Проверяемый старт:** Решать optimal POVM SDP на random qutrit/ququart models и классифицировать cases по geometric invariants.

### Scores
```text
Scientific Importance: 9/10
Tractability: 5/10
Computational Accessibility: 10/10
AI Leverage: 8/10
Bridge Potential: 9/10
Underexploredness: 9/10
Verification Clarity: 10/10
```

### Evidence
- Primary/current source: Yang, Imai & Pezzè, A geometric criterion for optimal measurements in multiparameter quantum metrology, arXiv:2601.21801 (2026).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #57 — Существование NPPT bound entangled states

**Field:** Physics / Quantum Entanglement  
**Status:** Open  
**Difficulty:** Very High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Существование NPPT bound entangled states» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Нужно отделить универсальную структуру от model-specific эффектов и получить вычислимый критерий, выдерживающий предельные/шумовые режимы.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Horodecki, Rudnicki & Życzkowski, Five Open Problems in Quantum Information Theory, PRX Quantum 3, 010101 (2022).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Существование NPPT bound entangled states → новый coarse-grained принцип → optimization / statistical mechanics → predictive design или control.</hypothesis>

### AI / Computational Attack Surface
simulation; optimization; symbolic search; model comparison; counterexample generation; uncertainty-aware AI assistance.

### First Research Experiment
**Проверяемый старт:** Строить certified SDP hierarchies для k-copy distillability на малых families.

### Scores
```text
Scientific Importance: 9/10
Tractability: 6/10
Computational Accessibility: 8/10
AI Leverage: 9/10
Bridge Potential: 10/10
Underexploredness: 7/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Horodecki, Rudnicki & Życzkowski, Five Open Problems in Quantum Information Theory, PRX Quantum 3, 010101 (2022).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #58 — Физическая интерпретация q в nonextensive statistics

**Field:** Physics / Information Theory  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Физическая интерпретация q в nonextensive statistics» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Нужно отделить универсальную структуру от model-specific эффектов и получить вычислимый критерий, выдерживающий предельные/шумовые режимы.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Nelson, Open Problems within Nonextensive Statistical Mechanics, Entropy 26, 118 (2024).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Физическая интерпретация q в nonextensive statistics → новый coarse-grained принцип → optimization / statistical mechanics → predictive design или control.</hypothesis>

### AI / Computational Attack Surface
simulation; optimization; symbolic search; model comparison; counterexample generation; uncertainty-aware AI assistance.

### First Research Experiment
**Проверяемый старт:** Проверить, предсказывается ли fitted q независимыми dynamical invariants в моделях с известной микродинамикой.

### Scores
```text
Scientific Importance: 9/10
Tractability: 7/10
Computational Accessibility: 9/10
AI Leverage: 10/10
Bridge Potential: 8/10
Underexploredness: 8/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Nelson, Open Problems within Nonextensive Statistical Mechanics, Entropy 26, 118 (2024).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #59 — Обобщённое Fourier-преобразование для q-statistics, пригодное в signal processing

**Field:** Mathematics / Signal Processing  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Обобщённое Fourier-преобразование для q-statistics, пригодное в signal processing» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Трудность в том, что малые примеры дают сильные закономерности, но переход к произвольному размеру требует нового invariant, extremal argument или decomposition.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Nelson, Open Problems within Nonextensive Statistical Mechanics, Entropy 26, 118 (2024).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Обобщённое Fourier-преобразование для q-statistics, пригодное в signal processing → новый invariant/decomposition → алгоритмы и формальная верификация → перенос в соседние вычислительные области.</hypothesis>

### AI / Computational Attack Surface
exhaustive search на малых размерах; SAT/SMT/MIP; symbolic algebra; counterexample generation; automated theorem proving; exact/interval verification.

### First Research Experiment
**Проверяемый старт:** Задать axioms и автоматически искать low-order transform kernels с проверкой invertibility.

### Scores
```text
Scientific Importance: 8/10
Tractability: 8/10
Computational Accessibility: 10/10
AI Leverage: 8/10
Bridge Potential: 9/10
Underexploredness: 9/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Nelson, Open Problems within Nonextensive Statistical Mechanics, Entropy 26, 118 (2024).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #60 — Согласованная normalization nonextensive entropy и generalized product

**Field:** Physics / Mathematical Information Theory  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Согласованная normalization nonextensive entropy и generalized product» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Нужно отделить универсальную структуру от model-specific эффектов и получить вычислимый критерий, выдерживающий предельные/шумовые режимы.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Nelson, Open Problems within Nonextensive Statistical Mechanics, Entropy 26, 118 (2024).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Согласованная normalization nonextensive entropy и generalized product → новый coarse-grained принцип → optimization / statistical mechanics → predictive design или control.</hypothesis>

### AI / Computational Attack Surface
simulation; optimization; symbolic search; model comparison; counterexample generation; uncertainty-aware AI assistance.

### First Research Experiment
**Проверяемый старт:** Формализовать axioms в theorem prover и проверить definitions на finite probability simplices.

### Scores
```text
Scientific Importance: 9/10
Tractability: 5/10
Computational Accessibility: 8/10
AI Leverage: 9/10
Bridge Potential: 10/10
Underexploredness: 7/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Nelson, Open Problems within Nonextensive Statistical Mechanics, Entropy 26, 118 (2024).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #61 — Когда joint forward+inverse latent model действительно улучшает subsurface imaging

**Field:** Geoscience / Inverse Problems  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Когда joint forward+inverse latent model действительно улучшает subsurface imaging» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Inverse/rare-event характер задачи делает ground truth дорогим, а distribution shift сильным; это ломает обычную validation схему.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Gupta et al., A Unified Framework for Forward and Inverse Problems in Subsurface Imaging using Latent Space Translations, ICLR 2025.</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Когда joint forward+inverse latent model действительно улучшает subsurface imaging → структурная характеристика → более сильный алгоритм → перенос в scientific computing / data analysis.</hypothesis>

### AI / Computational Attack Surface
simulation; optimization; symbolic search; model comparison; counterexample generation; uncertainty-aware AI assistance.

### First Research Experiment
**Проверяемый старт:** На OpenFWI-like data варьировать latent dimension и joint loss, проверяя zero-shot geological shift.

### Scores
```text
Scientific Importance: 8/10
Tractability: 6/10
Computational Accessibility: 9/10
AI Leverage: 10/10
Bridge Potential: 8/10
Underexploredness: 8/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Gupta et al., A Unified Framework for Forward and Inverse Problems in Subsurface Imaging using Latent Space Translations, ICLR 2025.
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #62 — Репрезентативность ensemble-boosted климатических экстремумов

**Field:** Geoscience / Rare-event Sampling  
**Status:** Partially Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Репрезентативность ensemble-boosted климатических экстремумов» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Inverse/rare-event характер задачи делает ground truth дорогим, а distribution shift сильным; это ломает обычную validation схему.

### What Is Already Known
<fact>Есть существенные частичные результаты, но исходная tight/общая постановка не закрыта. Основная свежая точка опоры: Finkel & O’Gorman, Boosting Ensembles for Statistics of Tails at Conditionally Optimal Advance Split Times, arXiv:2507.22310 (2025).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Репрезентативность ensemble-boosted климатических экстремумов → структурная характеристика → более сильный алгоритм → перенос в scientific computing / data analysis.</hypothesis>

### AI / Computational Attack Surface
simulation; optimization; symbolic search; model comparison; counterexample generation; uncertainty-aware AI assistance.

### First Research Experiment
**Проверяемый старт:** Сравнить boosted tail law с brute-force long-run oracle и измерить bias.

### Scores
```text
Scientific Importance: 8/10
Tractability: 7/10
Computational Accessibility: 10/10
AI Leverage: 8/10
Bridge Potential: 9/10
Underexploredness: 9/10
Verification Clarity: 9/10
```

### Evidence
- Primary/current source: Finkel & O’Gorman, Boosting Ensembles for Statistics of Tails at Conditionally Optimal Advance Split Times, arXiv:2507.22310 (2025).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #63 — Онлайн-выбор advance split time в rare-event sampling

**Field:** Applied Mathematics / Climate Algorithms  
**Status:** Partially Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Онлайн-выбор advance split time в rare-event sampling» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Трудность в том, что малые примеры дают сильные закономерности, но переход к произвольному размеру требует нового invariant, extremal argument или decomposition.

### What Is Already Known
<fact>Есть существенные частичные результаты, но исходная tight/общая постановка не закрыта. Основная свежая точка опоры: Finkel & O’Gorman, Boosting Ensembles for Statistics of Tails at Conditionally Optimal Advance Split Times, arXiv:2507.22310 (2025).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Онлайн-выбор advance split time в rare-event sampling → новый invariant/decomposition → алгоритмы и формальная верификация → перенос в соседние вычислительные области.</hypothesis>

### AI / Computational Attack Surface
exhaustive search на малых размерах; SAT/SMT/MIP; symbolic algebra; counterexample generation; automated theorem proving; exact/interval verification.

### First Research Experiment
**Проверяемый старт:** Сравнить online split policies на трёх chaotic systems с known rare-event probabilities.

### Scores
```text
Scientific Importance: 9/10
Tractability: 8/10
Computational Accessibility: 8/10
AI Leverage: 9/10
Bridge Potential: 10/10
Underexploredness: 7/10
Verification Clarity: 9/10
```

### Evidence
- Primary/current source: Finkel & O’Gorman, Boosting Ensembles for Statistics of Tails at Conditionally Optimal Advance Split Times, arXiv:2507.22310 (2025).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #64 — Weak-wind problem массивных звёзд

**Field:** Astronomy / Stellar Physics  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Hybrid  

### Problem
<fact>Закрыть конкретную постановку «Weak-wind problem массивных звёзд» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Нужно отделить универсальную структуру от model-specific эффектов и получить вычислимый критерий, выдерживающий предельные/шумовые режимы.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Sander, Open Questions in Massive Star Research across Cosmic Scales, arXiv:2601.00373 (2026).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Weak-wind problem массивных звёзд → новый coarse-grained принцип → optimization / statistical mechanics → predictive design или control.</hypothesis>

### AI / Computational Attack Surface
simulation; optimization; symbolic search; model comparison; counterexample generation; uncertainty-aware AI assistance.

### First Research Experiment
**Проверяемый старт:** Hierarchical fit competing wind prescriptions на homogeneous spectral sample.

### Scores
```text
Scientific Importance: 9/10
Tractability: 5/10
Computational Accessibility: 9/10
AI Leverage: 10/10
Bridge Potential: 8/10
Underexploredness: 8/10
Verification Clarity: 10/10
```

### Evidence
- Primary/current source: Sander, Open Questions in Massive Star Research across Cosmic Scales, arXiv:2601.00373 (2026).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #65 — Микроструктурный предиктор ductile-to-brittle transition

**Field:** Physics / Soft Amorphous Materials  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Микроструктурный предиктор ductile-to-brittle transition» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Нужно отделить универсальную структуру от model-specific эффектов и получить вычислимый критерий, выдерживающий предельные/шумовые режимы.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Divoux et al., Ductile-to-brittle transition and yielding in soft amorphous materials: perspectives and open questions, Soft Matter 20 (2024).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Микроструктурный предиктор ductile-to-brittle transition → новый coarse-grained принцип → optimization / statistical mechanics → predictive design или control.</hypothesis>

### AI / Computational Attack Surface
simulation; optimization; symbolic search; model comparison; counterexample generation; uncertainty-aware AI assistance.

### First Research Experiment
**Проверяемый старт:** Обучить sparse symbolic classifier на particle simulations и проверить transfer между potentials.

### Scores
```text
Scientific Importance: 9/10
Tractability: 6/10
Computational Accessibility: 10/10
AI Leverage: 8/10
Bridge Potential: 9/10
Underexploredness: 9/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Divoux et al., Ductile-to-brittle transition and yielding in soft amorphous materials: perspectives and open questions, Soft Matter 20 (2024).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #66 — Связь локальных rearrangements с macroscopic yielding

**Field:** Physics / Soft Amorphous Materials  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Связь локальных rearrangements с macroscopic yielding» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Нужно отделить универсальную структуру от model-specific эффектов и получить вычислимый критерий, выдерживающий предельные/шумовые режимы.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Divoux et al., Ductile-to-brittle transition and yielding in soft amorphous materials: perspectives and open questions, Soft Matter 20 (2024).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Связь локальных rearrangements с macroscopic yielding → новый coarse-grained принцип → optimization / statistical mechanics → predictive design или control.</hypothesis>

### AI / Computational Attack Surface
simulation; optimization; symbolic search; model comparison; counterexample generation; uncertainty-aware AI assistance.

### First Research Experiment
**Проверяемый старт:** Измерить predictive information soft spots о future yield на ensembles одинакового macro-state.

### Scores
```text
Scientific Importance: 9/10
Tractability: 7/10
Computational Accessibility: 8/10
AI Leverage: 9/10
Bridge Potential: 10/10
Underexploredness: 7/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Divoux et al., Ductile-to-brittle transition and yielding in soft amorphous materials: perspectives and open questions, Soft Matter 20 (2024).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #67 — Предсказание nucleation/location shear bands до разрушения

**Field:** Physics / Soft Amorphous Materials  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Предсказание nucleation/location shear bands до разрушения» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Нужно отделить универсальную структуру от model-specific эффектов и получить вычислимый критерий, выдерживающий предельные/шумовые режимы.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Divoux et al., Ductile-to-brittle transition and yielding in soft amorphous materials: perspectives and open questions, Soft Matter 20 (2024).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Предсказание nucleation/location shear bands до разрушения → новый coarse-grained принцип → optimization / statistical mechanics → predictive design или control.</hypothesis>

### AI / Computational Attack Surface
simulation; optimization; symbolic search; model comparison; counterexample generation; uncertainty-aware AI assistance.

### First Research Experiment
**Проверяемый старт:** Сравнить leading nonaffine modes до yield с фактическим band location.

### Scores
```text
Scientific Importance: 9/10
Tractability: 8/10
Computational Accessibility: 9/10
AI Leverage: 10/10
Bridge Potential: 8/10
Underexploredness: 8/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Divoux et al., Ductile-to-brittle transition and yielding in soft amorphous materials: perspectives and open questions, Soft Matter 20 (2024).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #68 — Минимальный state description preparation/aging history для failure

**Field:** Physics / Soft Amorphous Materials  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Минимальный state description preparation/aging history для failure» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Нужно отделить универсальную структуру от model-specific эффектов и получить вычислимый критерий, выдерживающий предельные/шумовые режимы.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Divoux et al., Ductile-to-brittle transition and yielding in soft amorphous materials: perspectives and open questions, Soft Matter 20 (2024).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Минимальный state description preparation/aging history для failure → новый coarse-grained принцип → optimization / statistical mechanics → predictive design или control.</hypothesis>

### AI / Computational Attack Surface
simulation; optimization; symbolic search; model comparison; counterexample generation; uncertainty-aware AI assistance.

### First Research Experiment
**Проверяемый старт:** Создать одинаковые final-energy states разными protocols и искать различающие observables.

### Scores
```text
Scientific Importance: 9/10
Tractability: 5/10
Computational Accessibility: 10/10
AI Leverage: 8/10
Bridge Potential: 9/10
Underexploredness: 9/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Divoux et al., Ductile-to-brittle transition and yielding in soft amorphous materials: perspectives and open questions, Soft Matter 20 (2024).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #69 — Количественный coarse-graining particle→elastoplastic→continuum

**Field:** Physics / Soft Amorphous Materials  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Количественный coarse-graining particle→elastoplastic→continuum» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Нужно отделить универсальную структуру от model-specific эффектов и получить вычислимый критерий, выдерживающий предельные/шумовые режимы.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Divoux et al., Ductile-to-brittle transition and yielding in soft amorphous materials: perspectives and open questions, Soft Matter 20 (2024).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Количественный coarse-graining particle→elastoplastic→continuum → новый coarse-grained принцип → optimization / statistical mechanics → predictive design или control.</hypothesis>

### AI / Computational Attack Surface
simulation; optimization; symbolic search; model comparison; counterexample generation; uncertainty-aware AI assistance.

### First Research Experiment
**Проверяемый старт:** Из particle simulation вывести mesoscopic transition kernel и проверить без re-fit на другом size.

### Scores
```text
Scientific Importance: 9/10
Tractability: 6/10
Computational Accessibility: 8/10
AI Leverage: 9/10
Bridge Potential: 10/10
Underexploredness: 7/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Divoux et al., Ductile-to-brittle transition and yielding in soft amorphous materials: perspectives and open questions, Soft Matter 20 (2024).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #70 — Отличение equilibrium от kinetic trapping в nanocrystal assemblies

**Field:** Chemistry / Materials Science  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Отличение equilibrium от kinetic trapping в nanocrystal assemblies» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Масштабы от атомистики до мезоскопики связаны many-body эффектами, а дешёвые coarse models теряют transferability.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Bassani et al., Nanocrystal Assemblies: Current Advances and Open Problems, ACS Nano 18 (2024).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Отличение equilibrium от kinetic trapping в nanocrystal assemblies → новый coarse-grained принцип → optimization / statistical mechanics → predictive design или control.</hypothesis>

### AI / Computational Attack Surface
simulation; optimization; symbolic search; model comparison; counterexample generation; uncertainty-aware AI assistance.

### First Research Experiment
**Проверяемый старт:** Сопоставить unbiased MD, enhanced sampling и experimental structure statistics.

### Scores
```text
Scientific Importance: 8/10
Tractability: 7/10
Computational Accessibility: 9/10
AI Leverage: 10/10
Bridge Potential: 8/10
Underexploredness: 8/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Bassani et al., Nanocrystal Assemblies: Current Advances and Open Problems, ACS Nano 18 (2024).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #71 — Inverse design assembly protocol для target nanocrystal superlattice

**Field:** Chemistry / Materials Science  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Inverse design assembly protocol для target nanocrystal superlattice» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Масштабы от атомистики до мезоскопики связаны many-body эффектами, а дешёвые coarse models теряют transferability.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Bassani et al., Nanocrystal Assemblies: Current Advances and Open Problems, ACS Nano 18 (2024).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Inverse design assembly protocol для target nanocrystal superlattice → новый coarse-grained принцип → optimization / statistical mechanics → predictive design или control.</hypothesis>

### AI / Computational Attack Surface
simulation; optimization; symbolic search; model comparison; counterexample generation; uncertainty-aware AI assistance.

### First Research Experiment
**Проверяемый старт:** Bayesian/RL search protocol и stress-test ±10% parameter perturbations.

### Scores
```text
Scientific Importance: 8/10
Tractability: 8/10
Computational Accessibility: 10/10
AI Leverage: 8/10
Bridge Potential: 9/10
Underexploredness: 9/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Bassani et al., Nanocrystal Assemblies: Current Advances and Open Problems, ACS Nano 18 (2024).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #72 — Transferable ligand-mediated effective interaction model

**Field:** Chemistry / Materials Science  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Transferable ligand-mediated effective interaction model» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Масштабы от атомистики до мезоскопики связаны many-body эффектами, а дешёвые coarse models теряют transferability.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Bassani et al., Nanocrystal Assemblies: Current Advances and Open Problems, ACS Nano 18 (2024).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Transferable ligand-mediated effective interaction model → новый coarse-grained принцип → optimization / statistical mechanics → predictive design или control.</hypothesis>

### AI / Computational Attack Surface
simulation; optimization; symbolic search; model comparison; counterexample generation; uncertainty-aware AI assistance.

### First Research Experiment
**Проверяемый старт:** Обучить pair+three-body coarse model на atomistic trajectories и проверить concentration transfer.

### Scores
```text
Scientific Importance: 8/10
Tractability: 5/10
Computational Accessibility: 8/10
AI Leverage: 9/10
Bridge Potential: 10/10
Underexploredness: 7/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Bassani et al., Nanocrystal Assemblies: Current Advances and Open Problems, ACS Nano 18 (2024).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #73 — Predictive structure→quantum-function map для nanocrystal superstructures

**Field:** Chemistry / Materials Science  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Predictive structure→quantum-function map для nanocrystal superstructures» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Масштабы от атомистики до мезоскопики связаны many-body эффектами, а дешёвые coarse models теряют transferability.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Bassani et al., Nanocrystal Assemblies: Current Advances and Open Problems, ACS Nano 18 (2024).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Predictive structure→quantum-function map для nanocrystal superstructures → новый coarse-grained принцип → optimization / statistical mechanics → predictive design или control.</hypothesis>

### AI / Computational Attack Surface
simulation; optimization; symbolic search; model comparison; counterexample generation; uncertainty-aware AI assistance.

### First Research Experiment
**Проверяемый старт:** Сочетать ab-initio anchors и large graph Hamiltonian, тестируя defects.

### Scores
```text
Scientific Importance: 8/10
Tractability: 6/10
Computational Accessibility: 9/10
AI Leverage: 10/10
Bridge Potential: 8/10
Underexploredness: 8/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Bassani et al., Nanocrystal Assemblies: Current Advances and Open Problems, ACS Nano 18 (2024).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #74 — OOD-safe transferable interatomic ML potentials

**Field:** Chemistry / Materials Science  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «OOD-safe transferable interatomic ML potentials» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Масштабы от атомистики до мезоскопики связаны many-body эффектами, а дешёвые coarse models теряют transferability.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Bassani et al., Nanocrystal Assemblies: Current Advances and Open Problems, ACS Nano 18 (2024).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>OOD-safe transferable interatomic ML potentials → новый coarse-grained принцип → optimization / statistical mechanics → predictive design или control.</hypothesis>

### AI / Computational Attack Surface
simulation; optimization; symbolic search; model comparison; counterexample generation; uncertainty-aware AI assistance.

### First Research Experiment
**Проверяемый старт:** Adversarial/high-temperature MD: проверить, предсказывает ли uncertainty true force error до drift.

### Scores
```text
Scientific Importance: 8/10
Tractability: 7/10
Computational Accessibility: 10/10
AI Leverage: 8/10
Bridge Potential: 9/10
Underexploredness: 9/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Bassani et al., Nanocrystal Assemblies: Current Advances and Open Problems, ACS Nano 18 (2024).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #75 — Identifiability mechanistic parameters в Universal Differential Equations

**Field:** Computational Biology / Systems Biology  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Identifiability mechanistic parameters в Universal Differential Equations» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Система частично наблюдаема, неоднородна и исторически зависима; predictive fit не равен mechanistic identification.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Philipps, Schmid & Hasenauer, Current state and open problems in universal differential equations for systems biology, npj Systems Biology and Applications 11, 101 (2025).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Identifiability mechanistic parameters в Universal Differential Equations → более идентифицируемая модель → dynamical systems / information theory → проверяемые биологические предсказания.</hypothesis>

### AI / Computational Attack Surface
simulation generation; causal/model comparison; active learning; equation discovery; uncertainty calibration; literature synthesis с точным verifier.

### First Research Experiment
**Проверяемый старт:** Synthetic ODE с hidden term: варьировать ANN capacity и измерять parameter bias.

### Scores
```text
Scientific Importance: 9/10
Tractability: 8/10
Computational Accessibility: 8/10
AI Leverage: 9/10
Bridge Potential: 10/10
Underexploredness: 7/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Philipps, Schmid & Hasenauer, Current state and open problems in universal differential equations for systems biology, npj Systems Biology and Applications 11, 101 (2025).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #76 — Robust training UDE на stiff biological dynamics

**Field:** Computational Biology / Systems Biology  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Robust training UDE на stiff biological dynamics» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Система частично наблюдаема, неоднородна и исторически зависима; predictive fit не равен mechanistic identification.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Philipps, Schmid & Hasenauer, Current state and open problems in universal differential equations for systems biology, npj Systems Biology and Applications 11, 101 (2025).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Robust training UDE на stiff biological dynamics → более идентифицируемая модель → dynamical systems / information theory → проверяемые биологические предсказания.</hypothesis>

### AI / Computational Attack Surface
simulation generation; causal/model comparison; active learning; equation discovery; uncertainty calibration; literature synthesis с точным verifier.

### First Research Experiment
**Проверяемый старт:** Сравнить implicit differentiable solvers и gradients с high-precision oracle.

### Scores
```text
Scientific Importance: 9/10
Tractability: 5/10
Computational Accessibility: 9/10
AI Leverage: 10/10
Bridge Potential: 8/10
Underexploredness: 8/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Philipps, Schmid & Hasenauer, Current state and open problems in universal differential equations for systems biology, npj Systems Biology and Applications 11, 101 (2025).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #77 — UDE inference при sparse/noisy observations

**Field:** Computational Biology / Systems Biology  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «UDE inference при sparse/noisy observations» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Система частично наблюдаема, неоднородна и исторически зависима; predictive fit не равен mechanistic identification.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Philipps, Schmid & Hasenauer, Current state and open problems in universal differential equations for systems biology, npj Systems Biology and Applications 11, 101 (2025).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>UDE inference при sparse/noisy observations → более идентифицируемая модель → dynamical systems / information theory → проверяемые биологические предсказания.</hypothesis>

### AI / Computational Attack Surface
simulation generation; causal/model comparison; active learning; equation discovery; uncertainty calibration; literature synthesis с точным verifier.

### First Research Experiment
**Проверяемый старт:** Оценивать recovery hidden vector field, а не только forecast RMSE, по noise/missingness grid.

### Scores
```text
Scientific Importance: 9/10
Tractability: 6/10
Computational Accessibility: 10/10
AI Leverage: 8/10
Bridge Potential: 9/10
Underexploredness: 9/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Philipps, Schmid & Hasenauer, Current state and open problems in universal differential equations for systems biology, npj Systems Biology and Applications 11, 101 (2025).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #78 — Автоматический выбор mechanistic vs neural structure UDE

**Field:** Computational Biology / Systems Biology  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Автоматический выбор mechanistic vs neural structure UDE» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Система частично наблюдаема, неоднородна и исторически зависима; predictive fit не равен mechanistic identification.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Philipps, Schmid & Hasenauer, Current state and open problems in universal differential equations for systems biology, npj Systems Biology and Applications 11, 101 (2025).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Автоматический выбор mechanistic vs neural structure UDE → более идентифицируемая модель → dynamical systems / information theory → проверяемые биологические предсказания.</hypothesis>

### AI / Computational Attack Surface
simulation generation; causal/model comparison; active learning; equation discovery; uncertainty calibration; literature synthesis с точным verifier.

### First Research Experiment
**Проверяемый старт:** Program synthesis на reaction networks с искусственно удалёнными reactions.

### Scores
```text
Scientific Importance: 9/10
Tractability: 7/10
Computational Accessibility: 8/10
AI Leverage: 9/10
Bridge Potential: 10/10
Underexploredness: 7/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Philipps, Schmid & Hasenauer, Current state and open problems in universal differential equations for systems biology, npj Systems Biology and Applications 11, 101 (2025).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #79 — Calibrated uncertainty и OOD detection для UDE

**Field:** Computational Biology / Systems Biology  
**Status:** Partially Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Calibrated uncertainty и OOD detection для UDE» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Система частично наблюдаема, неоднородна и исторически зависима; predictive fit не равен mechanistic identification.

### What Is Already Known
<fact>Есть существенные частичные результаты, но исходная tight/общая постановка не закрыта. Основная свежая точка опоры: Philipps, Schmid & Hasenauer, Current state and open problems in universal differential equations for systems biology, npj Systems Biology and Applications 11, 101 (2025).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Calibrated uncertainty и OOD detection для UDE → более идентифицируемая модель → dynamical systems / information theory → проверяемые биологические предсказания.</hypothesis>

### AI / Computational Attack Surface
simulation generation; causal/model comparison; active learning; equation discovery; uncertainty calibration; literature synthesis с точным verifier.

### First Research Experiment
**Проверяемый старт:** Проверить interval coverage на progressively out-of-range interventions.

### Scores
```text
Scientific Importance: 9/10
Tractability: 8/10
Computational Accessibility: 9/10
AI Leverage: 10/10
Bridge Potential: 8/10
Underexploredness: 8/10
Verification Clarity: 9/10
```

### Evidence
- Primary/current source: Philipps, Schmid & Hasenauer, Current state and open problems in universal differential equations for systems biology, npj Systems Biology and Applications 11, 101 (2025).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #80 — Batch integration без удаления biological variation

**Field:** Computational Biology / Single-cell  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Batch integration без удаления biological variation» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Система частично наблюдаема, неоднородна и исторически зависима; predictive fit не равен mechanistic identification.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Luecken et al., Defining and benchmarking open problems in single-cell analysis, Nature Biotechnology 43 (2025).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Batch integration без удаления biological variation → более идентифицируемая модель → dynamical systems / information theory → проверяемые биологические предсказания.</hypothesis>

### AI / Computational Attack Surface
simulation generation; causal/model comparison; active learning; equation discovery; uncertainty calibration; literature synthesis с точным verifier.

### First Research Experiment
**Проверяемый старт:** Semi-synthetic batches с known signal: построить Pareto frontier mixing vs conservation.

### Scores
```text
Scientific Importance: 9/10
Tractability: 5/10
Computational Accessibility: 10/10
AI Leverage: 8/10
Bridge Potential: 9/10
Underexploredness: 9/10
Verification Clarity: 10/10
```

### Evidence
- Primary/current source: Luecken et al., Defining and benchmarking open problems in single-cell analysis, Nature Biotechnology 43 (2025).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #81 — Надёжный cell–cell communication inference

**Field:** Computational Biology / Single-cell  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Надёжный cell–cell communication inference» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Система частично наблюдаема, неоднородна и исторически зависима; predictive fit не равен mechanistic identification.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Luecken et al., Defining and benchmarking open problems in single-cell analysis, Nature Biotechnology 43 (2025).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Надёжный cell–cell communication inference → более идентифицируемая модель → dynamical systems / information theory → проверяемые биологические предсказания.</hypothesis>

### AI / Computational Attack Surface
simulation generation; causal/model comparison; active learning; equation discovery; uncertainty calibration; literature synthesis с точным verifier.

### First Research Experiment
**Проверяемый старт:** На perturbational validation data оценить prediction downstream targets, а не co-expression.

### Scores
```text
Scientific Importance: 9/10
Tractability: 6/10
Computational Accessibility: 8/10
AI Leverage: 9/10
Bridge Potential: 10/10
Underexploredness: 7/10
Verification Clarity: 10/10
```

### Evidence
- Primary/current source: Luecken et al., Defining and benchmarking open problems in single-cell analysis, Nature Biotechnology 43 (2025).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #82 — Denoising scRNA-seq без hallucinated expression

**Field:** Computational Biology / Single-cell  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Denoising scRNA-seq без hallucinated expression» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Система частично наблюдаема, неоднородна и исторически зависима; predictive fit не равен mechanistic identification.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Luecken et al., Defining and benchmarking open problems in single-cell analysis, Nature Biotechnology 43 (2025).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Denoising scRNA-seq без hallucinated expression → более идентифицируемая модель → dynamical systems / information theory → проверяемые биологические предсказания.</hypothesis>

### AI / Computational Attack Surface
simulation generation; causal/model comparison; active learning; equation discovery; uncertainty calibration; literature synthesis с точным verifier.

### First Research Experiment
**Проверяемый старт:** Molecule downsampling: измерить calibration и false structure creation.

### Scores
```text
Scientific Importance: 9/10
Tractability: 7/10
Computational Accessibility: 9/10
AI Leverage: 10/10
Bridge Potential: 8/10
Underexploredness: 8/10
Verification Clarity: 10/10
```

### Evidence
- Primary/current source: Luecken et al., Defining and benchmarking open problems in single-cell analysis, Nature Biotechnology 43 (2025).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #83 — 2D embedding, сохраняющий local и global biological structure

**Field:** Computational Biology / Single-cell  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «2D embedding, сохраняющий local и global biological structure» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Система частично наблюдаема, неоднородна и исторически зависима; predictive fit не равен mechanistic identification.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Luecken et al., Defining and benchmarking open problems in single-cell analysis, Nature Biotechnology 43 (2025).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>2D embedding, сохраняющий local и global biological structure → более идентифицируемая модель → dynamical systems / information theory → проверяемые биологические предсказания.</hypothesis>

### AI / Computational Attack Surface
simulation generation; causal/model comparison; active learning; equation discovery; uncertainty calibration; literature synthesis с точным verifier.

### First Research Experiment
**Проверяемый старт:** Multi-objective embedding + bootstrap stability biological conclusions.

### Scores
```text
Scientific Importance: 9/10
Tractability: 8/10
Computational Accessibility: 10/10
AI Leverage: 8/10
Bridge Potential: 9/10
Underexploredness: 9/10
Verification Clarity: 10/10
```

### Evidence
- Primary/current source: Luecken et al., Defining and benchmarking open problems in single-cell analysis, Nature Biotechnology 43 (2025).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #84 — Open-set label projection при domain shift

**Field:** Computational Biology / Single-cell  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Open-set label projection при domain shift» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Система частично наблюдаема, неоднородна и исторически зависима; predictive fit не равен mechanistic identification.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Luecken et al., Defining and benchmarking open problems in single-cell analysis, Nature Biotechnology 43 (2025).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Open-set label projection при domain shift → более идентифицируемая модель → dynamical systems / information theory → проверяемые биологические предсказания.</hypothesis>

### AI / Computational Attack Surface
simulation generation; causal/model comparison; active learning; equation discovery; uncertainty calibration; literature synthesis с точным verifier.

### First Research Experiment
**Проверяемый старт:** Скрыть один cell type из reference и измерить unknown-detection vs known accuracy.

### Scores
```text
Scientific Importance: 9/10
Tractability: 5/10
Computational Accessibility: 8/10
AI Leverage: 9/10
Bridge Potential: 10/10
Underexploredness: 7/10
Verification Clarity: 10/10
```

### Evidence
- Primary/current source: Luecken et al., Defining and benchmarking open problems in single-cell analysis, Nature Biotechnology 43 (2025).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #85 — Match modalities без paired cells

**Field:** Computational Biology / Single-cell  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Match modalities без paired cells» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Система частично наблюдаема, неоднородна и исторически зависима; predictive fit не равен mechanistic identification.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Luecken et al., Defining and benchmarking open problems in single-cell analysis, Nature Biotechnology 43 (2025).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Match modalities без paired cells → более идентифицируемая модель → dynamical systems / information theory → проверяемые биологические предсказания.</hypothesis>

### AI / Computational Attack Surface
simulation generation; causal/model comparison; active learning; equation discovery; uncertainty calibration; literature synthesis с точным verifier.

### First Research Experiment
**Проверяемый старт:** Удалить pairing из paired ground truth и оценить posterior match calibration.

### Scores
```text
Scientific Importance: 9/10
Tractability: 6/10
Computational Accessibility: 9/10
AI Leverage: 10/10
Bridge Potential: 8/10
Underexploredness: 8/10
Verification Clarity: 10/10
```

### Evidence
- Primary/current source: Luecken et al., Defining and benchmarking open problems in single-cell analysis, Nature Biotechnology 43 (2025).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #86 — Perturbation prediction на unseen drug×cell-type combinations

**Field:** Computational Biology / Single-cell  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Perturbation prediction на unseen drug×cell-type combinations» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Система частично наблюдаема, неоднородна и исторически зависима; predictive fit не равен mechanistic identification.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Luecken et al., Defining and benchmarking open problems in single-cell analysis, Nature Biotechnology 43 (2025).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Perturbation prediction на unseen drug×cell-type combinations → более идентифицируемая модель → dynamical systems / information theory → проверяемые биологические предсказания.</hypothesis>

### AI / Computational Attack Surface
simulation generation; causal/model comparison; active learning; equation discovery; uncertainty calibration; literature synthesis с точным verifier.

### First Research Experiment
**Проверяемый старт:** Hold out целые drug classes/cell types и тестировать compositional extrapolation.

### Scores
```text
Scientific Importance: 9/10
Tractability: 7/10
Computational Accessibility: 10/10
AI Leverage: 8/10
Bridge Potential: 9/10
Underexploredness: 9/10
Verification Clarity: 10/10
```

### Evidence
- Primary/current source: Luecken et al., Defining and benchmarking open problems in single-cell analysis, Nature Biotechnology 43 (2025).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #87 — Predict modality с оценкой irreducible information loss

**Field:** Computational Biology / Single-cell  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Predict modality с оценкой irreducible information loss» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Система частично наблюдаема, неоднородна и исторически зависима; predictive fit не равен mechanistic identification.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Luecken et al., Defining and benchmarking open problems in single-cell analysis, Nature Biotechnology 43 (2025).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Predict modality с оценкой irreducible information loss → более идентифицируемая модель → dynamical systems / information theory → проверяемые биологические предсказания.</hypothesis>

### AI / Computational Attack Surface
simulation generation; causal/model comparison; active learning; equation discovery; uncertainty calibration; literature synthesis с точным verifier.

### First Research Experiment
**Проверяемый старт:** Оценить conditional entropy floor и сравнить модели с ним.

### Scores
```text
Scientific Importance: 9/10
Tractability: 8/10
Computational Accessibility: 8/10
AI Leverage: 9/10
Bridge Potential: 10/10
Underexploredness: 7/10
Verification Clarity: 10/10
```

### Evidence
- Primary/current source: Luecken et al., Defining and benchmarking open problems in single-cell analysis, Nature Biotechnology 43 (2025).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #88 — Самосогласованная теория strain-level microbial diversity

**Field:** Biology / Ecology & Evolution  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Самосогласованная теория strain-level microbial diversity» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Система частично наблюдаема, неоднородна и исторически зависима; predictive fit не равен mechanistic identification.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Goyal & Chure, Paradox of the Sub-Plankton, Environmental Microbiology 27 (2025).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Самосогласованная теория strain-level microbial diversity → более идентифицируемая модель → dynamical systems / information theory → проверяемые биологические предсказания.</hypothesis>

### AI / Computational Attack Surface
simulation generation; causal/model comparison; active learning; equation discovery; uncertainty calibration; literature synthesis с точным verifier.

### First Research Experiment
**Проверяемый старт:** Сравнить niche/neutral/HGT mechanistic models на longitudinal metagenomics.

### Scores
```text
Scientific Importance: 9/10
Tractability: 5/10
Computational Accessibility: 9/10
AI Leverage: 10/10
Bridge Potential: 8/10
Underexploredness: 8/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Goyal & Chure, Paradox of the Sub-Plankton, Environmental Microbiology 27 (2025).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #89 — Связь genetic similarity с ecological divergence у microbes

**Field:** Biology / Ecology & Evolution  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Связь genetic similarity с ecological divergence у microbes» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Система частично наблюдаема, неоднородна и исторически зависима; predictive fit не равен mechanistic identification.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Goyal & Chure, Paradox of the Sub-Plankton, Environmental Microbiology 27 (2025).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Связь genetic similarity с ecological divergence у microbes → более идентифицируемая модель → dynamical systems / information theory → проверяемые биологические предсказания.</hypothesis>

### AI / Computational Attack Surface
simulation generation; causal/model comparison; active learning; equation discovery; uncertainty calibration; literature synthesis с точным verifier.

### First Research Experiment
**Проверяемый старт:** Сравнить genetic и ecological distance matrices и nonlinear threshold models.

### Scores
```text
Scientific Importance: 9/10
Tractability: 6/10
Computational Accessibility: 10/10
AI Leverage: 8/10
Bridge Potential: 9/10
Underexploredness: 9/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Goyal & Chure, Paradox of the Sub-Plankton, Environmental Microbiology 27 (2025).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #90 — Early-warning signals для long ecological transients

**Field:** Biology / Ecology & Evolution  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Early-warning signals для long ecological transients» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Система частично наблюдаема, неоднородна и исторически зависима; predictive fit не равен mechanistic identification.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Morozov et al., Long-living transients in ecological models, Physics of Life Reviews 51 (2024).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Early-warning signals для long ecological transients → более идентифицируемая модель → dynamical systems / information theory → проверяемые биологические предсказания.</hypothesis>

### AI / Computational Attack Surface
simulation generation; causal/model comparison; active learning; equation discovery; uncertainty calibration; literature synthesis с точным verifier.

### First Research Experiment
**Проверяемый старт:** На моделях с известным transient clock сравнить classical EWS и spectral indicators.

### Scores
```text
Scientific Importance: 9/10
Tractability: 7/10
Computational Accessibility: 8/10
AI Leverage: 9/10
Bridge Potential: 10/10
Underexploredness: 7/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Morozov et al., Long-living transients in ecological models, Physics of Life Reviews 51 (2024).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #91 — Long transients при stochasticity + multiple timescales

**Field:** Biology / Ecology & Evolution  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Long transients при stochasticity + multiple timescales» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Система частично наблюдаема, неоднородна и исторически зависима; predictive fit не равен mechanistic identification.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Morozov et al., Long-living transients in ecological models, Physics of Life Reviews 51 (2024).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Long transients при stochasticity + multiple timescales → более идентифицируемая модель → dynamical systems / information theory → проверяемые биологические предсказания.</hypothesis>

### AI / Computational Attack Surface
simulation generation; causal/model comparison; active learning; equation discovery; uncertainty calibration; literature synthesis с точным verifier.

### First Research Experiment
**Проверяемый старт:** Построить scaling residence time по noise и timescale separation.

### Scores
```text
Scientific Importance: 9/10
Tractability: 8/10
Computational Accessibility: 9/10
AI Leverage: 10/10
Bridge Potential: 8/10
Underexploredness: 8/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Morozov et al., Long-living transients in ecological models, Physics of Life Reviews 51 (2024).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #92 — Dynamic population structures и active linking в evolutionary search

**Field:** Biology / Ecology & Evolution  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Dynamic population structures и active linking в evolutionary search» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Система частично наблюдаема, неоднородна и исторически зависима; predictive fit не равен mechanistic identification.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Recent synthesis on complex and dynamic population structures in evolutionary optimization, 2024–2025.</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Dynamic population structures и active linking в evolutionary search → более идентифицируемая модель → dynamical systems / information theory → проверяемые биологические предсказания.</hypothesis>

### AI / Computational Attack Surface
simulation generation; causal/model comparison; active learning; equation discovery; uncertainty calibration; literature synthesis с точным verifier.

### First Research Experiment
**Проверяемый старт:** Для Moran-like process с rewiring оценить fixation probabilities и low-order closures.

### Scores
```text
Scientific Importance: 9/10
Tractability: 5/10
Computational Accessibility: 10/10
AI Leverage: 8/10
Bridge Potential: 9/10
Underexploredness: 9/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Recent synthesis on complex and dynamic population structures in evolutionary optimization, 2024–2025.
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #93 — Измеримый критерий sustained open-endedness в synthetic biology

**Field:** Biology / Synthetic Biology  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Измеримый критерий sustained open-endedness в synthetic biology» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Система частично наблюдаема, неоднородна и исторически зависима; predictive fit не равен mechanistic identification.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Stock & Gorochowski, Open-endedness in synthetic biology, Science Advances 10 (2024).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Измеримый критерий sustained open-endedness в synthetic biology → более идентифицируемая модель → dynamical systems / information theory → проверяемые биологические предсказания.</hypothesis>

### AI / Computational Attack Surface
simulation generation; causal/model comparison; active learning; equation discovery; uncertainty calibration; literature synthesis с точным verifier.

### First Research Experiment
**Проверяемый старт:** Сравнить novelty metrics по способности предсказывать будущие functional classes.

### Scores
```text
Scientific Importance: 9/10
Tractability: 6/10
Computational Accessibility: 8/10
AI Leverage: 9/10
Bridge Potential: 10/10
Underexploredness: 7/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Stock & Gorochowski, Open-endedness in synthetic biology, Science Advances 10 (2024).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #94 — Снижение reality gap в evolutionary/synthetic bio search

**Field:** Biology / Synthetic Biology  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Снижение reality gap в evolutionary/synthetic bio search» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Система частично наблюдаема, неоднородна и исторически зависима; predictive fit не равен mechanistic identification.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Stock & Gorochowski, Open-endedness in synthetic biology, Science Advances 10 (2024).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Снижение reality gap в evolutionary/synthetic bio search → более идентифицируемая модель → dynamical systems / information theory → проверяемые биологические предсказания.</hypothesis>

### AI / Computational Attack Surface
simulation generation; causal/model comparison; active learning; equation discovery; uncertainty calibration; literature synthesis с точным verifier.

### First Research Experiment
**Проверяемый старт:** Эволюционировать circuits под ensemble simulators и проверить transfer.

### Scores
```text
Scientific Importance: 9/10
Tractability: 7/10
Computational Accessibility: 9/10
AI Leverage: 10/10
Bridge Potential: 8/10
Underexploredness: 8/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Stock & Gorochowski, Open-endedness in synthetic biology, Science Advances 10 (2024).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #95 — Минимальные условия возникновения higher-level evolutionary entities

**Field:** Biology / Synthetic Biology  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Минимальные условия возникновения higher-level evolutionary entities» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Система частично наблюдаема, неоднородна и исторически зависима; predictive fit не равен mechanistic identification.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Stock & Gorochowski, Open-endedness in synthetic biology, Science Advances 10 (2024).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Минимальные условия возникновения higher-level evolutionary entities → более идентифицируемая модель → dynamical systems / information theory → проверяемые биологические предсказания.</hypothesis>

### AI / Computational Attack Surface
simulation generation; causal/model comparison; active learning; equation discovery; uncertainty calibration; literature synthesis с точным verifier.

### First Research Experiment
**Проверяемый старт:** Построить phase diagram communication/cost/heritability в минимальной agent model.

### Scores
```text
Scientific Importance: 9/10
Tractability: 8/10
Computational Accessibility: 10/10
AI Leverage: 8/10
Bridge Potential: 9/10
Underexploredness: 9/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Stock & Gorochowski, Open-endedness in synthetic biology, Science Advances 10 (2024).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #96 — Аналитическая теория преобразования neural manifolds по глубине

**Field:** Neuroscience / Theory of Intelligence  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Аналитическая теория преобразования neural manifolds по глубине» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Высокоразмерная динамика допускает много эквивалентных описаний; нужна теория, связывающая microscopic updates с macroscopic computation.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Huang, Eight challenges in developing theory of intelligence, Frontiers in Computational Neuroscience 18 (2024).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Аналитическая теория преобразования neural manifolds по глубине → более идентифицируемая модель → dynamical systems / information theory → проверяемые биологические предсказания.</hypothesis>

### AI / Computational Attack Surface
simulation generation; causal/model comparison; active learning; equation discovery; uncertainty calibration; literature synthesis с точным verifier.

### First Research Experiment
**Проверяемый старт:** Измерить manifold invariants layer-by-layer и проверить candidate recursions.

### Scores
```text
Scientific Importance: 8/10
Tractability: 5/10
Computational Accessibility: 8/10
AI Leverage: 9/10
Bridge Potential: 10/10
Underexploredness: 7/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Huang, Eight challenges in developing theory of intelligence, Frontiers in Computational Neuroscience 18 (2024).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #97 — Как activity+plasticity порождают low-dimensional internal representations

**Field:** Neuroscience / Theory of Intelligence  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Как activity+plasticity порождают low-dimensional internal representations» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Высокоразмерная динамика допускает много эквивалентных описаний; нужна теория, связывающая microscopic updates с macroscopic computation.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Huang, Eight challenges in developing theory of intelligence, Frontiers in Computational Neuroscience 18 (2024).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Как activity+plasticity порождают low-dimensional internal representations → более идентифицируемая модель → dynamical systems / information theory → проверяемые биологические предсказания.</hypothesis>

### AI / Computational Attack Surface
simulation generation; causal/model comparison; active learning; equation discovery; uncertainty calibration; literature synthesis с точным verifier.

### First Research Experiment
**Проверяемый старт:** Искать простые plasticity rules, минимизирующие latent dimension при сохранении task info.

### Scores
```text
Scientific Importance: 8/10
Tractability: 6/10
Computational Accessibility: 9/10
AI Leverage: 10/10
Bridge Potential: 8/10
Underexploredness: 8/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Huang, Eight challenges in developing theory of intelligence, Frontiers in Computational Neuroscience 18 (2024).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #98 — Как обучение перестраивает attractor landscape recurrent neural systems

**Field:** Neuroscience / Theory of Intelligence  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Как обучение перестраивает attractor landscape recurrent neural systems» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Высокоразмерная динамика допускает много эквивалентных описаний; нужна теория, связывающая microscopic updates с macroscopic computation.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Huang, Eight challenges in developing theory of intelligence, Frontiers in Computational Neuroscience 18 (2024).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Как обучение перестраивает attractor landscape recurrent neural systems → более идентифицируемая модель → dynamical systems / information theory → проверяемые биологические предсказания.</hypothesis>

### AI / Computational Attack Surface
simulation generation; causal/model comparison; active learning; equation discovery; uncertainty calibration; literature synthesis с точным verifier.

### First Research Experiment
**Проверяемый старт:** До/после обучения построить metastable transition graph и связать изменения с weight modes.

### Scores
```text
Scientific Importance: 8/10
Tractability: 7/10
Computational Accessibility: 10/10
AI Leverage: 8/10
Bridge Potential: 9/10
Underexploredness: 9/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Huang, Eight challenges in developing theory of intelligence, Frontiers in Computational Neuroscience 18 (2024).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #99 — Quantitative theory continual learning без catastrophic forgetting

**Field:** Neuroscience / Theory of Intelligence  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Quantitative theory continual learning без catastrophic forgetting» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Высокоразмерная динамика допускает много эквивалентных описаний; нужна теория, связывающая microscopic updates с macroscopic computation.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Huang, Eight challenges in developing theory of intelligence, Frontiers in Computational Neuroscience 18 (2024).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Quantitative theory continual learning без catastrophic forgetting → более идентифицируемая модель → dynamical systems / information theory → проверяемые биологические предсказания.</hypothesis>

### AI / Computational Attack Surface
simulation generation; causal/model comparison; active learning; equation discovery; uncertainty calibration; literature synthesis с точным verifier.

### First Research Experiment
**Проверяемый старт:** На solvable teacher–student model вывести exact forgetting frontier.

### Scores
```text
Scientific Importance: 8/10
Tractability: 8/10
Computational Accessibility: 8/10
AI Leverage: 9/10
Bridge Potential: 10/10
Underexploredness: 7/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Huang, Eight challenges in developing theory of intelligence, Frontiers in Computational Neuroscience 18 (2024).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

## #100 — Causal learning из internal representations

**Field:** Neuroscience / Theory of Intelligence  
**Status:** Open  
**Difficulty:** High  
**Research Mode:** Theoretical / Computational  

### Problem
<fact>Закрыть конкретную постановку «Causal learning из internal representations» в форме tight characterization, доказательства/контрпримера либо алгоритма с проверяемой гарантией, соответствующей формулировке первичного open-problem источника.</fact>

### Why It Is Still Open
Высокоразмерная динамика допускает много эквивалентных описаний; нужна теория, связывающая microscopic updates с macroscopic computation.

### What Is Already Known
<fact>Проблема явно сформулирована как открытая в указанном источнике или актуальном benchmark; полного общепринятого решения при status-check не найдено. Основная точка опоры: Huang, Eight challenges in developing theory of intelligence, Frontiers in Computational Neuroscience 18 (2024).</fact>

### Why This Problem Matters
<inference>Даже частичное решение, которое вводит правильный invariant, lower bound, certified algorithm или переносимый benchmark, имеет самостоятельную научную ценность и может сузить более широкий класс задач.</inference>

### Interdisciplinary Bridge
<hypothesis>Causal learning из internal representations → более идентифицируемая модель → dynamical systems / information theory → проверяемые биологические предсказания.</hypothesis>

### AI / Computational Attack Surface
simulation generation; causal/model comparison; active learning; equation discovery; uncertainty calibration; literature synthesis с точным verifier.

### First Research Experiment
**Проверяемый старт:** На families SCM с одинаковой observational distribution тестировать interventional generalization.

### Scores
```text
Scientific Importance: 8/10
Tractability: 5/10
Computational Accessibility: 9/10
AI Leverage: 10/10
Bridge Potential: 8/10
Underexploredness: 8/10
Verification Clarity: 8/10
```

### Evidence
- Primary/current source: Huang, Eight challenges in developing theory of intelligence, Frontiers in Computational Neuroscience 18 (2024).
- Current-status check: Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

---

# Финальные рейтинги

## A. Top-20 Most Promising

1. **#39 Детерминированное pseudospectral shattering** — composite=8.97, AI=9, bridge=10, tractability=8.
2. **#87 Predict modality с оценкой irreducible information loss** — composite=8.97, AI=9, bridge=10, tractability=8.
3. **#63 Онлайн-выбор advance split time в rare-event sampling** — composite=8.97, AI=9, bridge=10, tractability=8.
4. **#75 Identifiability mechanistic parameters в Universal Differential Equations** — composite=8.97, AI=9, bridge=10, tractability=8.
5. **#43 Достаточна ли injection вместо OSE для least squares/SVD** — composite=8.71, AI=10, bridge=8, tractability=8.
6. **#55 SIC-POVM: существование хотя бы в бесконечной последовательности новых размерностей** — composite=8.71, AI=10, bridge=8, tractability=8.
7. **#79 Calibrated uncertainty и OOD detection для UDE** — composite=8.71, AI=10, bridge=8, tractability=8.
8. **#67 Предсказание nucleation/location shear bands до разрушения** — composite=8.71, AI=10, bridge=8, tractability=8.
9. **#91 Long transients при stochasticity + multiple timescales** — composite=8.71, AI=10, bridge=8, tractability=8.
10. **#3 Tight instance-optimal identity testing** — composite=8.71, AI=9, bridge=10, tractability=8.
11. **#15 Точная hardness/tractability граница Hamiltonian Cycle на структурно ограниченных классах графов** — composite=8.71, AI=9, bridge=10, tractability=8.
12. **#27 Конечный generating set, достигающий minimal growth rate** — composite=8.71, AI=9, bridge=10, tractability=8.
13. **#51 Критерий: когда шум regularizes или усиливает grazing bifurcations** — composite=8.71, AI=9, bridge=10, tractability=8.
14. **#99 Quantitative theory continual learning без catastrophic forgetting** — composite=8.71, AI=9, bridge=10, tractability=8.
15. **#42 Tight error bounds для DLR / complete pivoting** — composite=8.68, AI=9, bridge=10, tractability=7.
16. **#54 Полный набор mutually unbiased bases в C^6** — composite=8.68, AI=9, bridge=10, tractability=7.
17. **#66 Связь локальных rearrangements с macroscopic yielding** — composite=8.68, AI=9, bridge=10, tractability=7.
18. **#78 Автоматический выбор mechanistic vs neural structure UDE** — composite=8.68, AI=9, bridge=10, tractability=7.
19. **#90 Early-warning signals для long ecological transients** — composite=8.68, AI=9, bridge=10, tractability=7.
20. **#47 Оптимальная product complexity аппроксимации matrix sign** — composite=8.49, AI=8, bridge=9, tractability=8.

## B. Top-20 AI-Attackable

1. **#7 Оптимальная anytime convergence rate gradient descent** — composite=8.46, AI=10, bridge=8, tractability=8.
2. **#19 Longest Cycle parameterized above combinatorial bounds** — composite=8.46, AI=10, bridge=8, tractability=8.
3. **#31 Типичный Lovász theta number случайных circulant graphs** — composite=8.46, AI=10, bridge=8, tractability=8.
4. **#43 Достаточна ли injection вместо OSE для least squares/SVD** — composite=8.71, AI=10, bridge=8, tractability=8.
5. **#55 SIC-POVM: существование хотя бы в бесконечной последовательности новых размерностей** — composite=8.71, AI=10, bridge=8, tractability=8.
6. **#67 Предсказание nucleation/location shear bands до разрушения** — composite=8.71, AI=10, bridge=8, tractability=8.
7. **#79 Calibrated uncertainty и OOD detection для UDE** — composite=8.71, AI=10, bridge=8, tractability=8.
8. **#91 Long transients при stochasticity + multiple timescales** — composite=8.71, AI=10, bridge=8, tractability=8.
9. **#10 FPT зонотопных задач по геометрической размерности** — composite=8.18, AI=10, bridge=8, tractability=7.
10. **#22 Feedback Vertex Set в P_t-free bipartite graphs** — composite=8.18, AI=10, bridge=8, tractability=7.
11. **#34 Завершение классификации групп порядка 1024 на умеренных ресурсах** — composite=8.18, AI=10, bridge=8, tractability=7.
12. **#46 NEPv solver с superlinear convergence и линейной стоимостью итерации** — composite=8.43, AI=10, bridge=8, tractability=7.
13. **#58 Физическая интерпретация q в nonextensive statistics** — composite=8.43, AI=10, bridge=8, tractability=7.
14. **#70 Отличение equilibrium от kinetic trapping в nanocrystal assemblies** — composite=8.18, AI=10, bridge=8, tractability=7.
15. **#82 Denoising scRNA-seq без hallucinated expression** — composite=8.43, AI=10, bridge=8, tractability=7.
16. **#94 Снижение reality gap в evolutionary/synthetic bio search** — composite=8.43, AI=10, bridge=8, tractability=7.
17. **#1 Локальная регуляризация, способная учить все мультиклассовые классы** — composite=7.87, AI=10, bridge=8, tractability=6.
18. **#13 Instance-dependent sample complexity поиска Nash equilibrium в zero-sum matrix games** — composite=7.87, AI=10, bridge=8, tractability=6.
19. **#25 Структурные открытые вопросы о (pure) cactus groups** — composite=7.87, AI=10, bridge=8, tractability=6.
20. **#37 Forsythe conjecture для restarted conjugate gradient** — composite=8.11, AI=10, bridge=8, tractability=6.

## C. Top-20 Hidden Gems

1. **#11 Structure-agnostic minimax risk для partial linear model** — composite=8.24, AI=8, bridge=9, tractability=8.
2. **#47 Оптимальная product complexity аппроксимации matrix sign** — composite=8.49, AI=8, bridge=9, tractability=8.
3. **#83 2D embedding, сохраняющий local и global biological structure** — composite=8.49, AI=8, bridge=9, tractability=8.
4. **#23 Detecting almost-complete induced minors** — composite=8.24, AI=8, bridge=9, tractability=8.
5. **#35 Классификация групп порядка p^n q для n≤7** — composite=8.24, AI=8, bridge=9, tractability=8.
6. **#59 Обобщённое Fourier-преобразование для q-statistics, пригодное в signal processing** — composite=8.24, AI=8, bridge=9, tractability=8.
7. **#71 Inverse design assembly protocol для target nanocrystal superlattice** — composite=8.24, AI=8, bridge=9, tractability=8.
8. **#95 Минимальные условия возникновения higher-level evolutionary entities** — composite=8.49, AI=8, bridge=9, tractability=8.
9. **#14 Heavy-tailed bandits с неизвестными tail parameters** — composite=7.97, AI=8, bridge=9, tractability=7.
10. **#38 O(n^3) backward-stable полная diagonalization общей матрицы** — composite=8.21, AI=8, bridge=9, tractability=7.
11. **#86 Perturbation prediction на unseen drug×cell-type combinations** — composite=8.21, AI=8, bridge=9, tractability=7.
12. **#2 Оптимальная сложность joint differential privacy в линейных contextual bandits** — composite=7.97, AI=8, bridge=9, tractability=7.
13. **#62 Репрезентативность ensemble-boosted климатических экстремумов** — composite=7.97, AI=8, bridge=9, tractability=7.
14. **#26 Расширение skein modules до TQFT и skein modules mapping tori** — composite=7.97, AI=8, bridge=9, tractability=7.
15. **#50 Rigorous theory Markov-switching nonlinear networks** — composite=7.97, AI=8, bridge=9, tractability=7.
16. **#74 OOD-safe transferable interatomic ML potentials** — composite=7.97, AI=8, bridge=9, tractability=7.
17. **#98 Как обучение перестраивает attractor landscape recurrent neural systems** — composite=7.97, AI=8, bridge=9, tractability=7.
18. **#39 Детерминированное pseudospectral shattering** — composite=8.97, AI=9, bridge=10, tractability=8.
19. **#87 Predict modality с оценкой irreducible information loss** — composite=8.97, AI=9, bridge=10, tractability=8.
20. **#3 Tight instance-optimal identity testing** — composite=8.71, AI=9, bridge=10, tractability=8.

## D. Top-10 Bridge Problems

1. **#36 Robust scalable iterative solvers для high-frequency Helmholtz/convection-dominated PDE** — composite=7.98, AI=9, bridge=10, tractability=5.
2. **#39 Детерминированное pseudospectral shattering** — composite=8.97, AI=9, bridge=10, tractability=8.
3. **#42 Tight error bounds для DLR / complete pivoting** — composite=8.68, AI=9, bridge=10, tractability=7.
4. **#45 Polynomial-time Tensor Train approximation лучше m−1 factor** — composite=8.35, AI=9, bridge=10, tractability=6.
5. **#54 Полный набор mutually unbiased bases в C^6** — composite=8.68, AI=9, bridge=10, tractability=7.
6. **#57 Существование NPPT bound entangled states** — composite=8.35, AI=9, bridge=10, tractability=6.
7. **#60 Согласованная normalization nonextensive entropy и generalized product** — composite=7.98, AI=9, bridge=10, tractability=5.
8. **#63 Онлайн-выбор advance split time в rare-event sampling** — composite=8.97, AI=9, bridge=10, tractability=8.
9. **#66 Связь локальных rearrangements с macroscopic yielding** — composite=8.68, AI=9, bridge=10, tractability=7.
10. **#69 Количественный coarse-graining particle→elastoplastic→continuum** — composite=8.35, AI=9, bridge=10, tractability=6.

# Meta-analysis

## Повторяющиеся структуры

1. **Identifiability:** phase retrieval, UDE, causal representations, inverse imaging, quantum metrology.
2. **Local-to-global:** yielding, nonsmooth bifurcations, ecological transients, plasticity, graph decompositions.
3. **Rare events / tails:** heavy-tailed bandits, climate extremes, brittle failure, rare reactive configurations.
4. **Compression without losing semantics:** sketching, TT, data selection, single-cell embeddings, neural manifolds.
5. **Symmetry-constrained search:** MUB/SIC, finite groups, topology, phase retrieval, graph obstructions.

## Где вычислительный ресурс уже опережает исследовательскую методику

<inference>Самый большой разрыв виден в задачах, где миллионы малых точных экспериментов уже дешевы, но conjectures и counterexamples по-прежнему ищутся вручную: graph obstructions, matrix/tensor extremizers, finite-group case splits, UDE identifiability maps и bifurcation atlases.</inference>

## 10 методов, применимых сразу к множеству задач

1. SAT/SMT/MIP counterexample search.
2. Exact arithmetic + interval certification.
3. Exhaustive small-n enumeration.
4. SDP/SOS для bounds и Lyapunov functions.
5. Differentiable adversarial instance search.
6. Symbolic regression / equation discovery.
7. Automated theorem proving / proof assistants.
8. Rare-event sampling / importance splitting.
9. Active learning / Bayesian experimental design.
10. Symmetry reduction + canonical forms.

## OPEN PROBLEM MAP

```text
MUB / SIC ─────┐
Phase retrieval ├── symmetry + algebraic geometry ──→ certified search
Finite groups ──┘                                  │
                                                   ├──→ reusable exact verifiers
Graph problems ─── structure/decomposition ────────┘

Climate extremes ─┐
Ecological transients ├── metastability / rare transitions ─→ rare-event methods
Yielding ──────────┤
Neural attractors ─┘

UDE ───────────────┐
Subsurface inversion ├── hybrid mechanistic + learned models ─→ identifiability/UQ
ML potentials ─────┤
Single-cell ───────┘
```

## Практический Top-10 для старта одним исследователем

1. #12 Data selection for regression.
2. #10 Zonotope FPT.
3. #30 Tensor concentration.
4. #32 Phase retrieval.
5. #36 Hard-PDE iterative solvers.
6. #43 Injection vs OSE.
7. #61 Joint forward/inverse subsurface imaging.
8. #75 UDE identifiability.
9. #86 Perturbation prediction.
10. #92 Dynamic population structures / active linking.

# Источники

- **COLT24:** COLT 2024 Open Problems, PMLR 247 (2024).
- **COLT25:** COLT 2025 Open Problems, PMLR 291 (2025; page current in 2026).
- **DAG:** Agrawal et al., Solving Problems on Graphs: From Structure to Algorithms, Dagstuhl Reports 15(1), 2025, DOI 10.4230/DagRep.15.1.105.
- **TOPO:** Ohtsuki (ed.), Problems on Low-dimensional Topology, 2025, RIMS Kyoto University.
- **RAND:** Bandeira et al., Randomstrasse101: Open Problems of 2025, arXiv:2603.29571 (2026).
- **HELLY:** Naszódi, Quantitative Helly-type problems, Analysis Mathematica 51 (2025), DOI 10.1007/s10476-025-00127-z.
- **GROUP:** Eick, Classification of Finite Groups: Recent Developements and Open Problems, Foundations of Computational Mathematics 25 (2025), DOI 10.1007/s10208-024-09688-1.
- **PHASE:** Melnyk et al., Phasebook: a survey of selected open problems in phase retrieval, 2025.
- **NLA:** Amsel et al., Linear Systems and Eigenvalue Problems: Open Questions from a Simons Workshop, arXiv:2602.05394 (2026; updated Aug. 2026).
- **NSM:** Beyond the Bristol book: Advances and perspectives in non-smooth dynamics and applications, Chaos 33 (2023), section XIII Open Problems and Challenges.
- **SIM:** Simpson, The necessity of the sausage-string structure for mode-locking regions of piecewise-linear maps, arXiv:2312.03887.
- **QIT:** Horodecki, Rudnicki & Życzkowski, Five Open Problems in Quantum Information Theory, PRX Quantum 3, 010101 (2022).
- **MUB:** McNulty & Weigert, Mutually Unbiased Bases in Composite Dimensions – A Review, Quantum 10, 2051 (2026).
- **QCRB:** Yang, Imai & Pezzè, A geometric criterion for optimal measurements in multiparameter quantum metrology, arXiv:2601.21801 (2026).
- **SIC:** 2026 SIC-POVM literature including Journal of Algebraic Combinatorics, explicitly stating all-dimension existence remains open.
- **NENT:** Nelson, Open Problems within Nonextensive Statistical Mechanics, Entropy 26, 118 (2024).
- **GEO:** Gupta et al., A Unified Framework for Forward and Inverse Problems in Subsurface Imaging using Latent Space Translations, ICLR 2025.
- **CLIM:** Finkel & O’Gorman, Boosting Ensembles for Statistics of Tails at Conditionally Optimal Advance Split Times, arXiv:2507.22310 (2025).
- **STAR:** Sander, Open Questions in Massive Star Research across Cosmic Scales, arXiv:2601.00373 (2026).
- **SOFT:** Divoux et al., Ductile-to-brittle transition and yielding in soft amorphous materials: perspectives and open questions, Soft Matter 20 (2024).
- **NANO:** Bassani et al., Nanocrystal Assemblies: Current Advances and Open Problems, ACS Nano 18 (2024).
- **UDE:** Philipps, Schmid & Hasenauer, Current state and open problems in universal differential equations for systems biology, npj Systems Biology and Applications 11, 101 (2025).
- **SC:** Luecken et al., Defining and benchmarking open problems in single-cell analysis, Nature Biotechnology 43 (2025).
- **SCWEB:** OpenProblems.bio living benchmark, checked 2026-09-06.
- **MICRO:** Goyal & Chure, Paradox of the Sub-Plankton, Environmental Microbiology 27 (2025).
- **ECO:** Morozov et al., Long-living transients in ecological models, Physics of Life Reviews 51 (2024).
- **EVOL:** Recent synthesis on complex and dynamic population structures in evolutionary optimization, 2024–2025.
- **SYN:** Stock & Gorochowski, Open-endedness in synthetic biology, Science Advances 10 (2024).
- **NEURO:** Huang, Eight challenges in developing theory of intelligence, Frontiers in Computational Neuroscience 18 (2024).
- **STATUS:** Targeted status searches through 2026-09-06 for the exact problem plus solved/proof/counterexample/progress; entries with known complete resolution were excluded.

## Ограничение

<unknown>Поиск «не найдено решения» не эквивалентен математическому доказательству отсутствия свежей статьи. Поэтому для выбора одной конкретной задачи перед серьёзной работой следует повторить точечную status-verification именно по ней, включая preprints последних недель.</unknown>

<confidence>0.86</confidence>