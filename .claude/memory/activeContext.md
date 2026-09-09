# activeContext.md — Y-17 100 gipotez

## Scope Fence
- **Goal:** [PLAN, не факт] Оценить и начать проверку cross-domain мостов между каталогом ~141 открытых научных задач и реальными проектами (H-7 chromatin, ChernoffPy, May 1972)
- **[2026-09-09, ADR-087] Scope расширен пользователем явно:** пятый источник гипотез — сам 100-item каталог напрямую, без требования тематической связи с исходными 4 якорями. Не отменяет исходные якоря, добавляет к ним.
- **Boundary:** Эта папка + чтение (не запись) в исходный vault `C:\Users\serge\.claude\memory\` при необходимости сверки
- **Done when:** Хотя бы один мост прошёл полный цикл kill-criterion → эксперимент → KILLED/CONFIRMED/LEAD
- **NOT NOW:** Frontier R&D / TOFT / RAF — постоянно `unverified_source` (пользователь подтвердил 2026-09-07: возможно на другой машине, доступа нет); полный Hypothesis Portfolio (128+ гипотез из ARCHCODE и др.) — отдельный, не связанный проект














## Current Focus
**[VERIFIED — 2026-09-10, ADR-113] H-B7-28 (первый цикл автономной «миссии», установленной по прямой просьбе пользователя): CONFIRMED, mechanism H-B7-27 распространён на полный домен H-B7-22 (k=1..40, 80 условий, 8x шире прежнего).** Compute-First на всех 80 условиях H-B7-22's исходного домена: инвариант `FGFR3=True&GRB2=False&EGFR=False` — **0 нарушений на 4516 состояниях**. Полный эксперимент переиспользует `check_isomorphism`/`check_invariant`/`build_phi` H-B7-27 и `solve_absorption` H-B7-26 БЕЗ ИЗМЕНЕНИЙ (Minimal Relaxation Rule — расширен только диапазон k): **80/80 OK, 0 BLOCKED-INFRASTRUCTURE**, изоморфизм подтверждён на всех 40 k, инвариант держится с 0 исключениями, корольарный пересчёт совпадает на каждом k и точно воспроизводит committed-числа H-B7-27 для k=1..5. Для k≥5 (SCHEDULE_ROBUST зона H-B7-22) — точно 1.0 на обеих ветках. FL Step 8a: независимый ревьюер, выборка k=1/20/40 (обе ветки) — CONFIRMED-REAL, точное совпадение, сам поднял и снял вопрос о «вырожденности» проверки на тривиальных графах (k=1's 956-состояний — не тривиальный случай, тоже держится). `graph.yaml`: 147 узлов, 188 рёбер, `H-B7-28` статус `confirmed`, ребро `grounds` от H-B7-27. **Push:** батчируется, спрашивается на естественных паузах, не после каждого коммита — H-B7-26/27 уже запушены пользователем явным «да».
**[VERIFIED — 2026-09-10, ADR-112] H-B7-27 (прямое продолжение H-B7-26 по инструкции пользователя — «держать сильный механизм, не отвлекаться на слабую регрессию»): CONFIRMED, branch_1/branch_2 равенство exact escape probability объяснено как настоящий graph automorphism.** Пользователь заметил, что в H-B7-26's committed данных совпадает АБСОЛЮТНО всё между ветками (не только escape probability, но `n_states_in_graph`, `n_transient`, `expected_steps_to_absorption` до 15 знака) — предложил искать structural reason (isomorphism/lumpability/bisimulation), не гнаться за H9-A regression. Compute-First нашёл точный ответ дешевле слепого VF2-поиска: `GROWTH_ARREST_STATE_1`/`_2` отличаются РОВНО в одном узле — `EGFR_stimulus`. Кандидат `φ=flip(EGFR_stimulus)` — прямая проверка: node-set bijection + рёбра сохраняются в обе стороны, при каждом k=1..4. **Механизм (не просто эмпирика):** `EGFR=!GRB2&!FGFR3&(SPRY|EGFR_stimulus)` — `EGFR_stimulus` влияет на `EGFR` только при `!GRB2&!FGFR3`. Исчерпывающая проверка ~4422 состояний (обе ветки, k=1..5): **0 исключений** — `FGFR3≡True`, `GRB2≡False`, `EGFR≡False` тождественно. `EGFR_stimulus`'s правило — замороженная самопетля. Значит `φ` изоморфен ПО ПОСТРОЕНИЮ: branch_2's граф буквально ЕСТЬ граф branch_1 при инертной координате. Полный прогон — 5/5 k подтвердили обе части независимо (изоморфизм + инвариант) плюс корольарный пересчёт совпал с H-B7-26 до `1e-9`. FL Step 8a: первая попытка ревьюера — `BLOCKED-INFRASTRUCTURE` (Write недоступен + heredoc заблокирован, честно отчитано, не как evidence против claim), повторная попытка с известным воркэраундом (`python -` stdin-pipe) — CONFIRMED-REAL, полностью независимо написанный код (не переиспользовал функции run.py), точное совпадение по всем полям. `graph.yaml`: 146 узлов, 187 рёбер, `H-B7-27` статус `confirmed`, ребро `grounds` от H-B7-26. **Явный запрос пользователя на «миссию»:** установлен self-pacing автономный цикл (через `/loop` dynamic mode + `ScheduleWakeup`) — Green/Yellow-tier работа (эксперименты, тесты, коммиты в feature-ветки, локальный merge, реестрация graph.yaml/ADR/LEDGER) продолжается без подтверждения; `git push` в публичный репо остаётся Red-tier (см. `~/.claude/rules/autonomy-budget.md` — намеренно неотключаемо формулировкой «работай автономно»), батчируется на естественных паузах, спрашивается явно перед каждым push, не после каждого коммита.
**[VERIFIED — 2026-09-10, ADR-111] H-B7-26 (прямой редирект пользователя после подробной критики cross-domain/sci-hypothesis отчёта): CONFIRMED, точная asynchronous escape probability через absorbing Markov chain, oracle gate 10/10.** Пользователь поймал две реальные слабости отчёта: (1) H9-A r²=0.89 опирался лишь на 3 различных значения PNR-шага с коррелированными ветками, не на 8 независимых точек — верный вердикт «LEAD, не PROMOTE»; (2) собственная литературная проверка показала, что async-BN-как-Markov-chain уже устоявшаяся техника — снижает новизну неформальной Kramers-рамки. Обе поправки приняты полностью, без возражений. Пользователь сам предложил объективно более сильную переформулировку: async reachability graph H-B7-22 с uniform-random-among-unstable переходами H-B7-23 ЯВЛЯЕТСЯ конечной absorbing Markov chain — точные вероятности через `(I-Q)q=b` (Kemeny & Snell 1960). Compute-First (branch_1/k=1): `q=0.068866`, попадает в собственный 95%-CI H-B7-23 `[0.0592,0.0772]`. Полный эксперимент — все 10 условий (8 fragile k=1..4×2 ветки + k=5×2 позитивный контроль): **oracle gate 10/10 пройден**, k=5 даёт точно 1.0 обе ветки. Побочный продукт — ожидаемое число шагов до поглощения (fundamental matrix). Незапланированное наблюдение (зафиксировано, не преследуется): точные вероятности branch_1/branch_2 численно ИДЕНТИЧНЫ на каждом k, несмотря на подтверждённо различные release-состояния — кандидат в Pearl Registry, декомпозиция путей отложена. FL Step 8a: независимый ревьюер реконструировал branch_1/k=2 с нуля. Явно НЕ решено (per приоритет пользователя): декомпозиция вероятности по путям (item 3), повторная оценка large-deviation/Kramers claim на точных числах (item 4) — обе задачи намеренно отложены. `graph.yaml`: 145 узлов, 186 рёбер, `H-B7-26` статус `confirmed`, рёбра `grounds` от H-B7-22 и H-B7-23 (ВАЛИДИРУЕТ, не инвалидирует, их методологию). **Открытый loose end: уже опубликованный Artifact "Rare-Event Divergence" (https://claude.ai/code/artifact/d50ad18a-97f5-4997-90b0-82f0e56f1e51) содержит H9-A раздел, представленный увереннее, чем оправдывают данные — не исправлен, не автономное действие, поднять как опцию при следующей паузе.**
**[VERIFIED — 2026-09-10, ADR-110] H-B2-4 (первая гипотеза после закрытия ВСЕЙ async B7-арки; выбор через Explore-агента, не наугад): REJECTED, чистый confident null.** Explore-агент систематически просканировал 20 узлов `lead`, `null_results/`, `parked/`, документы бриджей B1-B3 — отверг 2 казавшихся перспективными кандидата (B3 lake-TDA уже закрыт; B2 tighter-predictor уже закрыт как H-B2-3) прежде чем найти H-B2-1k — узел с собственным явно названным, никогда не выполненным fix'ом («multi-seed x permutation-test criterion»). H-B2-1k's исходный sign-change критерий проходился чистым шумом с вероятностью ~0.999994 (single-seed, 9 точек). H-B2-4: 30 seed × 9 N_DIM, permutation test (2000 перестановок). Результат: усреднённая M1(N_DIM) СТРОГО монотонна (0 смен знака), p=1.0 — крайняя противоположность немонотонности. Кажущаяся немонотонность H-B2-1k была ровно тем шумовым артефактом, который предсказал его собственный skeptic-проход. REJECTED для H-B2-1j's pearl-предсказания, но НЕ для основного подтверждённого claim'а H-B2-1j (Theorem 3.1 bound, другой вопрос — Gate 1 non-transfer применён явно). Пойман и исправлен ДО коммита неверный edge-type (`invalidates` вместо `grounds`, который бы неверно каскадировал статус H-B2-1j). `graph.yaml`: 144 узла, 184 ребра, `H-B2-4` статус `killed`, + `null_results/` запись (следуя паттерну H-B2-3).
**[VERIFIED — 2026-09-10, ADR-109] H-B7-25 (замыкает последний пункт Relaxation Map H-B7-22 — bounded-delay fairness): REJECTED для универсального claim'а, но честный частичный survival.** Compute-First на k=1: p21CIP нестабилен (готов сработать) на каждом шаге до точки невозврата, RBL2 пассивно стабилен весь этот период — гипотеза обобщена на все 8 fragile-состояний. Полный прогон: **p21CIP-нестабильность подтверждена 8/8 без исключений** (не структурно заблокирован, именно «оголожен» планированием), но **RBL2-пассивность НЕ генерализуется** — держится при k=1,2, но при k=3,4 (обе ветки) RBL2 ТОЖЕ становится нестабильным на последних 1-2 шагах (меньше запаса ближе к k*=5). Anti-Overfitting Gate применён честно: гипотеза с одной проверки протестирована на всех 8 и найдена ложной в 4 — отчитано REJECTED, не сглажено. Прямой ответ на bounded-fairness: `p21CIP_min_starvation_count` (=PNR-шаг H-B7-24) точно даёт минимум пропусков p21CIP для побега (5/4/4/2). FL Step 8a не запущен (REJECT, вне scope). `graph.yaml`: 143 узла, 182 ребра, `H-B7-25` статус `lead`. **Это замыкает ВСЕ пункты Relaxation Map H-B7-22** — frequency (H-B7-23), timing/mechanism (H-B7-24), bounded-fairness (здесь) — под-арка async B7 (H-B7-13→25) теперь полностью закрыта, следующий шаг не назначен.
**[VERIFIED — 2026-09-10, ADR-108] H-B7-24 (механистическое углубление H-B7-22): CONFIRMED, резкая точка невозврата вдоль async-побега, всегда триггер CyclinE1.** Compute-First на k=1/branch_1 (11-шаговый путь): исчерпывающая проверка достижимости H-B7-22 (без изменений) на КАЖДОМ промежуточном состоянии — GROWTH_ARREST достижим через шаг 4 (после срабатывания CyclinA!), недостижим начиная с шага 5 (срабатывание CyclinE1). Механизм: CyclinA и CyclinE1 имеют ИДЕНТИЧНОЕ правило (проверено по .bnet-файлу) — срабатывание CyclinA одного не коммитит (не монотонно, может откатиться), только CyclinE1 фиксирует. Полный эксперимент — все 8 fragile-состояний: **8/8 резкая одношаговая точка невозврата** (без отката), **8/8 триггер — CyclinE1** (никогда CyclinA). Длина пути и шаг PNR монотонно сокращаются к k=4 (11/10/6/3; PNR 5/4/4/2), идентично на обеих ветках. FL Step 8a: reviewer с нуля (собственный BFS, собственная reachability, собственная SCC-детекция) для k=1/branch_1 — CONFIRMED, идентичный путь, идентичный шаг 5, идентичный триггер, явно проверил отсутствие отката. `graph.yaml`: 142 узла, 181 ребро, `H-B7-24` статус `confirmed`.
**[VERIFIED — 2026-09-10, ADR-107] H-B7-23 (прямое продолжение H-B7-22's Relaxation Map — «quantify vulnerability, not just existence»): CONFIRMED, монотонный рост частоты побега 6.7%→33.8% по мере приближения к k*=5.** Новая random-schedule конвенция (выбор среди unstable-узлов, не всех 35) — сходимость за 5-15 шагов, не сотни. Позитивный контроль (k=5, обе ветки, 3000/3000 PROLIFERATION) прошёл точно. Обе ветки согласуются в пределах CI на каждом k — переподтверждает H-B7-12's эквивалентность на стохастической величине. Интерпретация: уязвимость H-B7-22 НЕ экзотика — уже при k=1 ~1/15 случайных траекторий убегает, при k=4 ~1/3. FL Step 8a: узкий reviewer с нуля независимо реконструировал самое нагруженное число (branch_1, k=4) — CONFIRMED, 34.2% точно в заявленном CI. Честная граница: связь с H-B7-16's accuracy-провалом ТОЛЬКО качественная (разные random-schedule конвенции), явно не претендует на количественное объяснение. `graph.yaml`: 141 узел, 180 рёбер, `H-B7-23` статус `confirmed`.
**[VERIFIED — 2026-09-10, ADR-106] H-B7-22 (следующая гипотеза по автономной инструкции, Route 5 из breakthrough-routes.md): синхронный k*=5-порог НЕ независим от расписания обновлений — реальная, механистически объяснённая находка, подтверждена reviewer'ом.** Compute-First на 3 точках (k=3,4,5) вскрыл: при k=3,4 (синхронно «безопасно») async-достижимы ОБА исхода. Полный эксперимент — весь домен H-B7-13 (k=1..40, обе ветки, 80 состояний), строгая SCC-детекция аттракторов (`networkx`): substrate чист (0 cap-нарушений, 0 циклических/неоднозначных аттракторов). Резкое разделение: k∈{1,2,3,4} обе ветки — SCHEDULE_FRAGILE (PROLIFERATION дополнительно достижим, включая k=1 — самый ранний и «безопасный»!); k∈{5..40} — SCHEDULE_ROBUST. Новая величина `k_adv=1`, намного меньше k*=5. Механизм (Mechanism Claim Gate, проверен ДО полного прогона): конкретный порядок обновлений позволяет CyclinA/CyclinE1 сработать на УСТАРЕВШИХ p21CIP=False/RBL2=False — race condition, невозможная синхронно; объясняет одностороннюю асимметрию напрямую. FL Step 8a (обязателен — переворачивает допущение всей под-арки B7-9..21): узкий reviewer независимо с нуля реконструировал k=1/branch_1 — собственная BFS, не вызов кода эксперимента — CONFIRMED, с точным совпадением 956 состояний при полностью независимой реализации. НЕ убивает синхронные находки H-B7-9..21 (все явно ограничили себя синхронным обновлением) и не противоречит H-B7-16 (другой вопрос — точность маркеров при RANDOM, не existence при adversarial). `graph.yaml`: 140 узлов, 178 рёбер, `H-B7-22` статус `confirmed`.
**[VERIFIED — 2026-09-10, ADR-105] Lean 4 formализация H-B7-21 (пилот, по запросу пользователя после обсуждения методологии OpenAI GPT-6 Astra): первое применение Strong-tier верификации в проекте.** `falsification-ladder.md`'s Independent Verification Strength Ladder называла Lean/Coq уровнем Strong с самого начала, но проект ни разу это не использовал — только цитировал. Установлен `elan`+Lean 4.33.1 (не было на машине), без mathlib (сознательно — Epoch AI's собственная цифра, независимо перепроверена фетчем страницы: 1.2М строк Lean на ОДНО 18-страничное доказательство — mathlib оправдан для открытых/асимптотических задач вроде Форсайта/Ловаса, не для конечных claim'ов вроде этого). Доказано в Lean (~115 строк, 0 sorry/admit/native_decide, `#print axioms` → только `[propext]`): (1) абстрактная core-теорема H-B7-21 — для ЛЮБОЙ таблицы и ЛЮБОГО типа Row, не только 2984 проверенных случая; (2) multi-node следствие для списка произвольной длины; (3) конкретная инстанциация на реальном правиле RBL2 и реальных значениях PROLIFERATION_STATE, независимо подтверждена `decide` (ядро Lean, другая реализация, не Python). Артефакт: `experiments/.../h21/lean/` (HB721Core.lean + README.md), decision.md addendum, graph.yaml evidence обновлён. Честная граница: полная 35-узловая сеть НЕ перекодирована в Lean — общность теоремы делает это ненужным именно для этого claim'а.
**[VERIFIED — 2026-09-10, ADR-104] H-CAT31-2 (следующая гипотеза после закрытия B7-арки, по инструкции «продолжай следующую гипотезу автономно»): REJECTED, честный null-результат, не hard-killed.** Выбор направления НЕ произвольный — по уже существующему `reports/2026-09-09-breakthrough-routes.md` (5 маршрутов, прошлая сессия): маршруты B3/B2 уже REJECTED, Форсайт заблокирован (многосессионная задача), Route 2 (Ловас: хвосты/арифметика) — единственный готовый. Переиспользована машинерия H-CAT31-1 (`theta_via_lp`) без изменений. Проверка: коррелирует ли простое/составное n (3 предрегистрированные пары из отчёта: 127/129, 251/255, 509/511) с ХВОСТОМ распределения `X=log(theta/sqrt(n))` (H-CAT31-1 сообщал только среднее). Позитивный контроль пройден чисто (6.4e-14 при пороге 1e-6, 3000 графов). Результат: дисперсия — согласованное направление, но не существенное (макс. 13.5% при пороге ≥50%); top-decile-вклад — направление НЕ согласовано; все CI пересекаются. **REJECTED** для узкого предрегистрированного вопроса, статус `lead` (weak_alive, не killed) — Relaxation Map называет 2 открытых направления (непрерывный признак делимости, бо́льшая выборка), ни одно не запущено. `graph.yaml`: 139 узлов, 176 рёбер.
**[VERIFIED — 2026-09-10, ADR-103] H-B7-21 (по прямой инструкции пользователя: синтез + минимальное условие, продолжать автономно до полного закрытия): CONFIRMED, замыкает всю observability/rule-perturbation под-арку B7 (H-B7-13→H-B7-21).** Часть A — общая теорема проверена ИСЧЕРПЫВАЮЩЕ по ВСЕМ 35 узлам сети (не только 3 ранее протестированных): возмущение множества single-bit правил сохраняет `PROLIFERATION_STATE`/`_2` неподвижной точкой ⟺ ни одна возмущённая строка не равна собственной входной конфигурации состояния для этого узла. 35 узлов × 2 ветки × 2984 проверки, 0 расхождений, 0 нарушений baseline fixed-point (впервые проверено сетевым образом, не только для 3 узлов вручную). Достаточность проверена и при ОДНОВРЕМЕННОМ возмущении нескольких узлов сразу (новое, за пределами H-B7-17/19/20). Часть B — синтез: RBL2 33.3% fragile, p21CIP 0%, CyclinE1 9.7% — НЕ монотонно по числу входов, явно НЕ подогнан тренд на n=3. Реальная методологическая находка: 2 reviewer-попытки подряд зависли на лимите ходов из-за заблокированного `python -c` в песочнице (не bundled-scope, как в прежних случаях) — третья попытка с явной инструкцией писать файл-скрипт прошла чисто. FL Step 8a: CONFIRMED на highest-risk узле (E2F1_high, 10 входов). `graph.yaml`: 138 узлов, 175 рёбер, `H-B7-21` статус `confirmed`. **Открытые нити (не пройдены, названы явно): расширение полной ROBUST/FRAGILE-машинерии за пределы 3 узлов; проверка асимметрии fragile-rate на бóльшем n; double-bit возмущения — вся исходная инструкция пользователя выполнена, следующий шаг не назначен, ждать нового направления.**
**[VERIFIED — 2026-09-10, ADR-102] H-B7-20 (третий и последний feedback-loop узел, CyclinE1, 32-строчное exhaustive возмущение, по явному запросу пользователя): PARTIALLY-ROBUST, замыкает тройное сравнение RBL2/p21CIP/CyclinE1 и общий принцип дестабилизации.** Реальное структурное отличие от H-B7-17/19: CyclinE1 НЕ клэмпится, орбита клэмп-фазы перестроена заново для каждого возмущения (новые функции). Substrate-проверка через ДРУГОЙ путь кода подтвердила орбиту H-B7-15 точно (7 состояний/ветвь). Результат: 28 ROBUST, 3 FRAGILE, 1 CRITERION_INVALID из 32. По прямому запросу пользователя добавлен систематический слой (не на одном отобранном случае): КАЖДАЯ fragile/invalid строка проверена H-B7-18's методологией на дестабилизацию самого аттрактора — единственная CRITERION_INVALID строка (`flip_FFTTT`) дестабилизирует аттрактор сам (обе ветви), все 3 FRAGILE строки — только-наблюдаемость. Общий принцип теперь подтверждён ТРИЖДЫ вычислительно (RBL2, p21CIP независимо перепроверен скретч-скриптом в рамках этого эксперимента, CyclinE1): дестабилизирующее возмущение узла всегда точно совпадает со строкой, соответствующей собственной входной конфигурации `PROLIFERATION_STATE` для этого узла. Отклонена (до фиксации в артефактах) ложная рабочая гипотеза «направление flip коррелирует с хрупкостью» — RBL2 добавленная строка, CyclinE1 удалённая, противоположные паттерны. Пойман и исправлен ДО запуска пробел дизайна: изначальная проверка дестабилизации не покрывала CRITERION_INVALID строки, хотя оригинальное расследование H-B7-18 было именно про CRITERION_INVALID случай RBL2 — расширено на все fragile-or-invalid строки. `graph.yaml`: 137 узлов, 172 ребра, `H-B7-20` статус `lead`, рёбра `grounds` от H-B7-15/17/18/19. **Следующий шаг (прямая инструкция пользователя): H-B7-21 — синтез sensitivity-профилей всех трёх узлов + попытка вывести минимальное необходимое/достаточное условие существования аттрактора Proliferation, продолжать автономно до полного закрытия темы.**
[summarized] **B1/B2/B3 arc (H-B3-1 through H-B3-1k, ADR-010–027) archived to `history/activeContext-archive-20260906-b1b2b3.md`**
[summarized] **[2026-09-09, продолжение] Bridge 8 (UDE identifiability ↔ PRJ-CHERNOFFPY) зарегистрирован proposed → в тот же день...
[summarized] **[VERIFIED — 2026-09-09, по прямому запросу пользователя «посмотри на 100-item каталог, какие ещё есть кандидаты»]...
[summarized] **[VERIFIED, побочно, честно зафиксировано]** 4 фоновых `pytest -q` прогона на весь репозиторий накопились за...
[summarized] **[VERIFIED — 2026-09-09] H-CAT37-1 (первый эксперимент под расширенным scope, ADR-087/088): Forsythe conjecture...
[summarized] **[VERIFIED — 2026-09-09] H-CAT31-1 (второй эксперимент под расширенным scope, ADR-089): Lovász theta случайных...
[summarized] **[VERIFIED — 2026-09-09] Оставшиеся 6 кластеров каталога реально проверены (не «паттерн предсказывает»), все...
[summarized] **[VERIFIED — 2026-09-10, ADR-101] H-B7-19 (второй клэмп-узел p21CIP, exhaustive 16-строчное возмущение через...
[summarized] **[VERIFIED — 2026-09-10, ADR-100] H-B7-18 (продолжение открытого вопроса из H-B7-17): почему flip_TF_drop_CyclinE1...
[summarized] **[VERIFIED — 2026-09-10, ADR-099] H-B7-17 (вторая половина option 2: rule perturbations на RBL2): PARTIALLY-ROBUST,...


[summarized] **[VERIFIED — 2026-09-10, ADR-091] Ретроскан H-CAT37-1: гипотеза Форсайта разрешена ИЗВНЕ**...
[summarized] **[VERIFIED — 2026-09-10, ADR-092] H-CAT37-2 (целенаправленный поиск того же дня): INFORMATIVE_NEGATIVE, с реальным...
[summarized] **[VERIFIED — 2026-09-10, ADR-093] H-B2-3 («начни B2», route 4 отчёта): transferability B2-предиктора — REJECTED,...
[summarized] **[VERIFIED — 2026-09-10, ADR-094] H-B3-2 («начни B3», route 3 отчёта): PH₀ chirality-excess (Baryshnikov 2022) —...
[summarized] **[VERIFIED — 2026-09-10, ADR-095] H-B7-13 (согласованный пользователем узкий следующий шаг после B2/B3):...
[summarized] **[VERIFIED — 2026-09-10, ADR-096] H-B7-14 (Minimal Relaxation Rule на H-B7-13, по прямой инструкции пользователя...
[summarized] **[VERIFIED — 2026-09-10, ADR-097] H-B7-15 (по прямой просьбе пользователя поднять H-B7-14 до «model-level...
[summarized] **[VERIFIED — 2026-09-10, ADR-097a] H-B7-15 addendum: минимальность j*=1 — бесплатное следствие уже собранных...
[summarized] **[VERIFIED — 2026-09-10, ADR-098] H-B7-16 (второй из двух вариантов пользователя после H-B7-15: robustness к...
[summarized] **[VERIFIED — 2026-09-09, завершение] Весь 100-item каталог просмотрен (100/100), не только 7 кандидатов.** Ключевая...

## Project State
- **Repo:** https://github.com/sergeeey/Y-17-100-gipotez — PUBLIC, created 2026-09-06, commit d50597f (initial import). [VERIFIED]
- **Excluded from public repo (.gitignore):** `H-7 GeoSpectra Lab (DIFFERENT project…).md` — third-party correspondence refs (Tom Lawrence). Local copy kept. User may override.
- **New meta-goal (2026-09-06, user):** make this an *exemplary experimental lab* — memory/structure/hypothesis-graph designed up front so a blind orchestrator can operate; use it to test the whole tool/agent/methodology stack. **Variant C chosen by user (AskUserQuestion) → ADR-002.** Every tool use → row in `tooling-eval/LEDGER.md` (25 rows after session 1: CAUGHT 6 / OK 8 / NOISE 5 / NOT-YET 6).
- **Graph validator:** `python scripts/lab_check.py` (SCHEMA invariants 1–3) + `pytest` (3 tests incl. negative control replicating the 2026-05-28 incident). Run both before every commit.
- **FL template source (reuse, don't reinvent):** `D:\Claude-cod-top-2026\experiments\_template\` (14 files) [VERIFIED]
- **Files transferred:** 15 (2026-09-06)
- **Bridges scoped:** 3, все терминальны (2026-09-09): RMT/Riemann — Phase 1a READY, 1b BLOCKED (external Option A); ChernoffPy/UDE — CONFIRMED-WITH-CAVEATS, арка H-B2-1→1v закрыта 2026-09-08; May1972/TDA — CLOSED 2026-09-09 как informative negative (0 confirmed / 8 killed / 1 parked из 15 под-гипотез), арка H-B3-1→1p. **[2026-09-10] H-B3-2** (новая статья, PH₀ chirality-excess, route 3 отчёта) добавлена к той же закрытой Bridge 3 — REJECT после bug-fix-and-rerun, не реоткрывает мост (по-прежнему 0 confirmed на этой линии); Mechanism Claim Gate внутри неё — единственный устоявший позитивный побочный результат.
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
- [2026-09-09 18:28] `564d8db` (local, branch `feature/h-b7-28-full-domain-isomorphism` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-B7-28 -- branch isomorphism mechanism extended to H-B7-22's full domain (k=1..40), CONFIRMED
- [2026-09-09 18:19] `365621c` (local, branch `feature/h-b7-27-branch-isomorphism` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-B7-27 -- branch_1/branch_2 exact-probability equality explained as graph automorphism, CONFIRMED
- [2026-09-09 17:51] `158831b` (local, branch `feature/h-b7-26-exact-absorption` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-B7-26 -- exact asynchronous escape probability via absorbing Markov chain, CONFIRMED
- [2026-09-09 17:10] `d0ecd80` (local, branch `feature/h-b2-4-multiseed-permutation` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-B2-4 -- multi-seed + permutation test finds M1(N_DIM) perfectly monotonic, closing H-B2-1k's own named CRITERION_INVALID gap
- [2026-09-09 16:00] `d06d21d` (local, branch `feature/h-b7-25-starvation-asymmetry` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-B7-25 -- p21CIP-specific starvation confirmed 8/8, RBL2-passive framing rejected at k=3,4 -- honest partial survival
- [2026-09-09 15:26] `54ec343` (local, branch `feature/h-b7-24-point-of-no-return` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-B7-24 -- sharp point of no return along async escape, always CyclinE1's own firing, confirmed by FL Step 8a reviewer
- [2026-09-09 14:48] `dd10fe7` (local, branch `feature/h-b7-23-random-async-vulnerability` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-B7-23 -- random-schedule escape frequency 6.7%->33.8% (k=1..4), confirms H-B7-22's vulnerability is substantial not rare
- [2026-09-09 13:28] `5b345a5` (local, branch `feature/h-b7-22-adversarial-async` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-B7-22 -- k*=5 release threshold is NOT schedule-independent, confirmed by adversarial async reachability + FL Step 8a reviewer
- [2026-09-09 12:44] `3630559` (local, branch `feature/h-b7-21-lean-pilot` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: Lean 4 formalization pilot for H-B7-21 -- first Strong-tier verification in this project
- [2026-09-09 12:26] `cbc885f` (local, branch `feature/h-cat31-2-lovasz-tail-arithmetic` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-CAT31-2 -- tail/arithmetic structure of Lovasz theta, near-prime vs composite n, REJECTED (honest null)
- [2026-09-09 12:10] `9aeb717` (local, branch `feature/h-b7-21-fixedpoint-condition` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-B7-21 -- minimal necessary/sufficient condition for Proliferation attractor, exhaustive network-wide, closes B7 observability sub-arc
- [2026-09-09 11:54] `3468d81` (local, branch `feature/h-b7-20-cycline1-ruleperturbation` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-B7-20 -- exhaustive CyclinE1 rule-perturbation robustness, PARTIALLY-ROBUST (28/32), closes three-way destabilization principle
- [2026-09-09 10:55] `97f95af`: Merge: H-B7-19 exhaustive p21CIP rule-perturbation robustness, ROBUST (15/16)
- [2026-09-09 10:55] `42a16d6` (local, branch `feature/h-b7-19-p21cip-ruleperturbation` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-B7-19 -- exhaustive p21CIP rule-perturbation robustness, ROBUST (15/16)
- [2026-09-09 10:06] `2e382b8`: Merge: H-B7-18 mechanistic explanation of H-B7-17's CRITERION_INVALID finding
