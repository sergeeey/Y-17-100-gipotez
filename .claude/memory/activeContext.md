# activeContext.md — Y-17 100 gipotez

## Scope Fence
- **Goal:** [PLAN, не факт] Оценить и начать проверку cross-domain мостов между каталогом ~141 открытых научных задач и реальными проектами (H-7 chromatin, ChernoffPy, May 1972)
- **[2026-09-09, ADR-087] Scope расширен пользователем явно:** пятый источник гипотез — сам 100-item каталог напрямую, без требования тематической связи с исходными 4 якорями. Не отменяет исходные якоря, добавляет к ним.
- **Boundary:** Эта папка + чтение (не запись) в исходный vault `C:\Users\serge\.claude\memory\` при необходимости сверки
- **Done when:** Хотя бы один мост прошёл полный цикл kill-criterion → эксперимент → KILLED/CONFIRMED/LEAD
- **NOT NOW:** Frontier R&D / TOFT / RAF — постоянно `unverified_source` (пользователь подтвердил 2026-09-07: возможно на другой машине, доступа нет); полный Hypothesis Portfolio (128+ гипотез из ARCHCODE и др.) — отдельный, не связанный проект












## Current Focus
[summarized] **B1/B2/B3 arc (H-B3-1 through H-B3-1k, ADR-010–027) archived to `history/activeContext-archive-20260906-b1b2b3.md`**
[summarized] `killed` — вопрос о механизме lag'а НЕ опровергнут, отложен только этот дешёвый метод; revival
[summarized] **[VERIFIED] H-B3-1p (автономно, третья итерация «следующая гипотеза по очереди» — H-B3-1l's
[summarized] Phase 1b (H-B1-1b, хроматин) — BLOCKED: единственный оставшийся блокер — Option A в H-7 TAD (внешняя работа, вне...
[summarized] **[2026-09-09] Все 3 моста достигли терминального состояния — graph.yaml не содержит ни одного узла со статусом...


**[2026-09-09, продолжение] Bridge 8 (UDE identifiability ↔ PRJ-CHERNOFFPY) зарегистрирован proposed → в тот же день REJECTED собственным feasibility-gate.** Прямой grep реального кода (внутренний `experiments/`, внешний `E:/MarkovChains/ChernoffPy`) на torch/nn.Module/.backward()/neural/UDE/identifiab дал 0 совпадений — вся инфраструктура Bridge 2 «Neural-ODE/UDE» оказалась теоретической аналогией (Chernoff на линейном операторе), не обученной сетью. Посылка ADR-082 «общая инфраструктура — переносится код» была непроверенным [INFERRED], поданным как факт — ADR-083 фиксирует это честно как процессный урок, не заметает. Открытая задача (npj Sys Biol Appl 2025) остаётся open, отклонён только перенос через ChernoffPy; revival condition назван.

**[VERIFIED — 2026-09-09, по прямому запросу пользователя «посмотри на 100-item каталог, какие ещё есть кандидаты»] Полный обзор каталога по кластерам, сопоставленным с реальной инфраструктурой.** Топ-кандидат — Numerical Linear Algebra (#36-47, Amsel et al. arXiv:2602.05394, Simons Workshop, 36 авторов, реальность подтверждена WebSearch) — прямое совпадение с рабочим псевдоспектральным кодом Bridge 2. На этот раз применена дисциплина, которой не хватило Bridge 8: **полный текст первичного источника прочитан через `mcp__arxiv__*` ДО регистрации в graph.yaml, не после.** Оба проверенных под-кандидата отклонены БЕЗ единой записи в graph.yaml: #39 (Deterministic Pseudospectral Shattering, Problem 3.1) — вопрос СУЩЕСТВОВАНИЯ универсального детерминированного алгоритма, не эмпирически тестируем конечным числом матриц; #43 (injections vs OSE, Problems 5.1/5.2) — статья САМА (v3, апдейт 20 августа 2026, РАНЬШЕ заявленной даты каталога 6 сентября) уже документирует ОТРИЦАТЕЛЬНЫЙ ответ (Townsend & Wang, arXiv:2604.10215v2) — конкретное подтверждение staleness каталога. ADR-084 + pearl_registry: theoretical-CS/чистая-математика кластеры каталога (COLT, numerical LA, вероятно RIMS topology) структурно не подходят под FL-эмпирический формат этого проекта — «Prove or disprove универсальную границу» ≠ «измерь число против порога». **[VERIFIED — 2026-09-09, автономное продолжение по Stop-hook feedback «не откладывай на пользователя»]** Отчёт закончился фразой «жду направления» — hook корректно поймал это как отложенное решение при активном /goal-условии. Продолжил без ожидания: проверил ещё 4 кандидата (#65 materials — нужна MD-симуляция, тот же разрыв что Bridge 8; #92 evolutionary population structures — источник БЕЗ авторов/журнала/DOI, проваливает Source Trace на входе; #83 single-cell embedding — реальный источник, но живой конкурентный community-бенчмарк OpenProblems.bio, непропорционален одной сессии; #96-98 neuroscience attractor landscapes — требует обучения RNN, тот же ML-разрыв). **Итог 7 кандидатов из 6 кластеров этой сессии (Bridge 8 + Numerical LA #39/#43 + эти 4): все отклонены по РАЗНЫМ, конкретно проверенным причинам** (ADR-085): 4/7 инфраструктурный разрыв (ML/симуляция), 1/7 непроверяемый источник, 1/7 proof-theoretic, 1/7 устарел, 1/7 непропорционален масштабу. Ни один узел не записан в graph.yaml впустую — feasibility проверялась ДО регистрации во всех 7 случаях. Оставшиеся непроверенные кластеры каталога (pure math, topology, quantum info, geoscience, chemistry, synthetic bio) — не исключены явно, но паттерн (математика→proof-theoretic, естественные науки→нужны реальные данные) предсказывает похожий результат.

**[VERIFIED, побочно, честно зафиксировано]** 4 фоновых `pytest -q` прогона на весь репозиторий накопились за несколько тиков без проверки, что предыдущие ещё живы (~53 мин простоя по таймстампу goal check-in, LEDGER `MISSED`) — пользователь заметил через goal check-in раньше меня. Все 4 остановлены `TaskStop` (подтверждено ответом инструмента); частичный лог (`/tmp/pytest_full.log`) показал 0 падений на ~22% прогона — содержательных потерь нет, но урок процесса записан.

**[VERIFIED — 2026-09-09] H-CAT37-1 (первый эксперимент под расширенным scope, ADR-087/088): Forsythe conjecture (restarted CG), CONFIRMED на выборке.** 2 реальных методологических бага пойманы Mechanism Claim Gate ДО claim'а: (1) жёсткий порог 1e-8 в фикс. бюджете 500 restarts ложно классифицировал 48/144 медленно-но-реально сходящихся пар как контрпримеры — исправлено log-linear decay-slope тестом; (2) сырой power-basis Крылова численно вырожден (cond(V)~1e19 при s=7) на плохо обусловленных матрицах — исправлено ортонормальным базисом Ланцоша. После обоих фиксов: 0/171 протестированных (n,mode,s,seed) пар показывают настоящий контрпример (extended-restart follow-up до 8000 restarts на оставшихся 6 кандидатах, регресс-тест `test_no_genuine_counterexample_survives_extended_restart_budget`). 12/12 тестов проходят, ruff clean. `registry/graph.yaml`: 124 узла, 145 рёбер.

**[VERIFIED — 2026-09-09] H-CAT31-1 (второй эксперимент под расширенным scope, ADR-089): Lovász theta случайных circulant graphs — CONFIRMED, содержательно, не «ожидаемо».** Снова Mechanism Claim Gate поймал реальный баг: формула θ(G)=n·(-λ_min)/(d-λ_min) для vertex-transitive графов (вспомнена по памяти, уверенно) точно совпала с известным θ(C_5)=√5 на разреженных циклах, но оказалась НЕВЕРНОЙ на плотных circulant-графах (n≥9) — подтверждено третьей независимой проверкой (дополнение графа изоморфно C_9, закрытая формула нечётного цикла + тождество θ(G)θ(Ḡ)=n совпадают с LP-реализацией, не с формулой из памяти). LP взята напрямую из Table 1 источника (arXiv:2603.29571), доверена. Отдельно: первая LP-реализация строила DFT-матрицу Python-циклом — при n=2560 не завершилась за 3+ минуты, `TaskStop`нута, векторизована. **Результат:** θ(G)/√n держится в 0.97–1.02 для n от 40 до 2560 (log-log наклон -0.035, практически плоско) — прямая численная поддержка ТОЧНОЙ гипотезы (Conjecture 18) против более слабой опубликованной верхней границы источника, реальный вклад в открытый разрыв. 6/6 тестов, ruff clean. `registry/graph.yaml`: 126 узлов, 146 рёбер.

**[VERIFIED — 2026-09-09] Оставшиеся 6 кластеров каталога реально проверены (не «паттерн предсказывает»), все отклонены на scoping с конкретной, source-verified причиной для каждого — 100/100 каталог закрыт.** #54 (MUB в C^6) и #55 (SIC-POVM): WebSearch подтвердил — desятилетия сложного специализированного численного поиска (Brierley-Weigert, Butterley-Hall, Bell-inequality методы; SDP; алгебраическое построение Hadamard-матриц) УЖЕ дали сильные отрицательные/частичные результаты — любая Python-попытка в одну сессию чисто дублировала бы худшим инструментом уже сделанное специалистами, не добавляя информации. #27 (топология, minimal growth rate поверхностных групп, RIMS 2025, реальная формулировка через WebSearch — Problem 4.1, K. Fujiwara): формально чёткая постановка, но требует automatic-group-theory инфраструктуры (Cannon's algorithm/KBMAG), которой нет и которую дёшево не построить — тот же разрыв, что убил Bridge 8. #51 (nonsmooth dynamics, шум и grazing bifurcations): реальный источник (Chaos 33, 2023), но формулировка — открытое НАПРАВЛЕНИЕ, не конкретная проверяемая гипотеза; нужна существенная новая формализация прежде тестирования. #61 (geoscience, subsurface imaging latent models) и #93 (synthetic bio, open-endedness criterion): оба требуют либо обучения новых нейросетей (тот же ML-разрыв, что и UDE), либо реальных специализированных датасетов. #89 (ecology, genetic-vs-ecological divergence у микробов): требует реальных геномных+экологических баз данных, не сгенерировать честно синтетически. **Итог полного каталога (100/100 просмотрено, каждый непроверенный кластер этой сессией индивидуально source-verified, не экстраполирован):** 2 CONFIRMED (H-CAT37-1, H-CAT31-1), ~12+ кандидатов отклонены на scoping с конкретными причинами (инфраструктурный ML/симуляционный разрыв — большинство; уже исчерпывающе исследовано специалистами — quantum info; устарел/неверная посылка — Bridge 8, #43; недостаточно формализовано — nonsmooth dynamics). Дешёвый поиск по каталогу исчерпан добросовестно, не деклараторно.

**[VERIFIED — 2026-09-10, ADR-099] H-B7-17 (вторая половина option 2: rule perturbations на RBL2): PARTIALLY-ROBUST, находка через skeptic-discrepancy, не баг.** 4 single-bit truth-table flip'а правила RBL2 (2 входа, исчерпывающе), все выражения перепроверены computationally. Первый проход наивно дал «3 из 4 robust»; независимый reviewer, проверяя baseline-vs-fragile асимметрию, отметил расхождение в числе из моего prompt'а (моя опечатка, не баг кода) — но разбор ЭТОГО расхождения вскрыл: flip_TF_drop_CyclinE1's floor-маркер ТОЖЕ показывал 0 коллизий, т.е. переход вообще отсутствует под этим возмущением (все k=1..6 релапсируют в GROWTH_ARREST, проверено напрямую). Исправлено через FL Step 4a Floor-Ceiling дисциплину per-perturbation: floor's собственное число = сигнал «существует ли переход». Итог: 2/3 содержательно проверяемых возмущения ROBUST, 1/3 FRAGILE (механистически осмысленно — именно то возмущение, что убирает единственную строку таблицы истинности, дающую RBL2 снова стать True), 1/4 исключён как CRITERION_INVALID. `graph.yaml`: 134 узла, 164 ребра, статус `lead`. Обе половины option 2 пользователя (async H-B7-16, rule perturbation H-B7-17) теперь закрыты.

**[VERIFIED — 2026-09-10, ADR-091] Ретроскан H-CAT37-1: гипотеза Форсайта разрешена ИЗВНЕ** (Colbrook/Stepaniants/Townsend, arXiv:2609.04659, 4 сент. 2026, через 5 дней после эксперимента) — общая гипотеза ЛОЖНА для КАЖДОГО s≥4 (Lean-формализовано, контрпример размерности s+4 через transverse-Hopf-shadowing). Собственная находка H-CAT37-1 (0/171 при случайном поиске n≤12,s≤11) НЕ опровергнута — авторский контрпример не простая явная матрица (рациональная арифметика до ~2^500000, даже сами авторы не свели это к одному числовому примеру вне формализованного объёма доказательства). `graph.yaml`: `PROB-CAT-37→solved`, `H-CAT37-1` текст скорректирован (различает «эта выборка» от «общая гипотеза»). Проверена и честно отклонена оптимистичная рамка пользователя «воспроизвести сертификат = дешёвый первый тест» — клонирован репозиторий авторов, подтверждено: многосессионная задача, не быстрая проверка. Найден реальный open follow-up: контрпример при n=5,6,7 для s=4 не исключён теоремой (опора на 5-8 собственных значений, авторы использовали верхнюю границу 8) — pearl_registry запись, целенаправленный поиск следующим шагом.

**[VERIFIED — 2026-09-10, ADR-092] H-CAT37-2 (целенаправленный поиск того же дня): INFORMATIVE_NEGATIVE, с реальным пойманным багом по пути.** `differential_evolution` объектив изначально давал ПЛОСКИЙ штраф -1.0 для любого exact_solve_hit — пилот за 3 сек дал eval_slope=-1.0 на всех n, сырые данные показали 100% случайной популяции сходится точно за 7-16 restarts из 800 — ноль градиента. Исправлено непрерывной наградой за медленную сходимость; после фикса задержка выросла в 10-40x (39-314 restarts вместо 7-16). Тем не менее **при n=5,6,7 КАЖДЫЙ лучший найденный кандидат всё равно сходится точно** (extended-check 5000 restarts, 5 свежих seed) — контрпример не найден, но поиск доказанно нетривиален (не провален из-за отсутствия сигнала). Реальное, не доказательное свидетельство, что размерность 8 авторов не произвольна. `graph.yaml`: 127 узлов, 148 рёбер, `H-CAT37-2` статус `lead`.

**[VERIFIED — 2026-09-10, ADR-093] H-B2-3 («начни B2», route 4 отчёта): transferability B2-предиктора — REJECTED, реальный баг конструкции пойман до вердикта.** Mechanism Claim Gate доказал точно (не приближённо): M_T,W(B)=M_1,0(T(B-WI)), проверено численно 1e-6. Первая версия нового семейства матриц (2×2 rotation-блоки) использовала поэлементную upper-triangular маску — резала ЧЕРЕЗ собственный off-diagonal блока, искажая заявленные собственные значения (max_re_eig 0.5-5.98 вместо {0.5,≤-0.5}), давая `k_ref=inf`. Исправлено block-aware маской. **Честный результат:** compute cost — предиктор в 19× быстрее (держится); точность — экстраполяция на малый T деградирует резко (~7-30×, асимметрично), новое семейство+новый T (двойная экстраполяция) — ~22-200×, превышает предрегистрированный порог «на порядок». REJECTED — не безразмерная редукция (точная алгебра), а конкретная ОДНА подогнанная зависимость без переобучения. `null_results/H-B2-3-...md` создан, `graph.yaml`: 128 узлов, 149 рёбер, статус `killed`.

**[VERIFIED — 2026-09-10, ADR-094] H-B3-2 («начни B3», route 3 отчёта): PH₀ chirality-excess (Baryshnikov 2022) — REJECT после bug-fix-and-rerun; Mechanism Claim Gate устоял отдельно.** Mechanism Claim Gate: H1-VR-статистика Bridge 3 доказуемо слепа к развороту времени окна (5/5, побайтовая идентичность) — HOLDS, не затронут дальнейшим. Первая реализация `merge_tree_bars` прошла 6/6 hand-verified тестов, дала чистый CONFIRMED (chirality V1-crossing уникально на позитивном контроле Lower Zurich, лид 2.25 года, молчание на обоих негативных). По стандартной для сессии практике отправлен независимому `Agent(reviewer)` (2 проверяемых утверждения) ДО доверия — reviewer нашёл РЕАЛЬНЫЙ баг через ручной 7-точечный контрпример `[2,8,0,9,1,7,3]`: алгоритм молча терял глобальный минимум окна при нечётном числе экстремумов (~55% реальных окон Lower Zurich затронуто). Исправлено напрямую по Baryshnikov §2.2.1 (глобальный min/max сначала, рекурсия по остатку), **полный эксперимент перезапущен** — результат изменился материально: chirality-excess теперь ложно срабатывает на Windermere (негативный контроль), floor false-positive rate инвертировался с наименьшего из трёх статистик на наибольший. **REJECT** — прямая механическая фальсификация bug-fix-and-rerun'ом на идентичных данных. `null_results/H-B3-2-...md` создан, `graph.yaml`: 129 узлов, 151 ребро, статус `killed`. Revival condition: другой позитивный-контрольный датасет (Peter/Paul lakes) или менее шумочувствительная order-sensitive конструкция.

**[VERIFIED — 2026-09-10, ADR-095] H-B7-13 (согласованный пользователем узкий следующий шаг после B2/B3): наблюдаемость release-решения — REJECTED чисто для обоих маркерных наборов.** Точный (не выборочный) collision search по 80 release-состояниям (2 ветки × k=1..40) новой функцией, захватывающей состояние ИМЕННО в момент снятия transient-клэмпа (не финальное). Floor/ceiling санитарные контроли оба прошли. M1={Growth_arrest,Proliferation} и M2=M1+{p21CIP,RBL2} — ОБА REJECTED: один и тот же коллизионный кластер на обеих ветках (k=3,4 безопасно vs k=5 побег, все 4 маркера идентичны в момент решения — RBL2/CyclinE1-петля ещё не разошлась видимо ровно на пороге). Честная оговорка: H-B7-12 уже показал ветки динамически эквивалентными для этого вмешательства — домен фактически ~40 независимых состояний, не 80; не меняет вердикт. `graph.yaml`: 130 узлов, 154 ребра, статус `killed`. Revival condition: наблюдать маркеры через j шагов ПОСЛЕ снятия клэмпа вместо точного момента — самый вероятный fix, не запущен.

**[VERIFIED — 2026-09-10, ADR-096] H-B7-14 (Minimal Relaxation Rule на H-B7-13, по прямой инструкции пользователя «наблюдай маркеры через j шагов после снятия клэмпа»): CONFIRMED, j*=1, независимо перепроверено.** Одно изменённое допущение — момент наблюдения. Регрессия j=0 точно воспроизвела H-B7-13 (обязательная проверка перед доверием). Свип j=0..10: оба M1={Growth_arrest,Proliferation} и M2=M1+{p21CIP,RBL2} стали полностью достаточными на j*=1 — меньший набор M1 разрешился на том же j*, что и дополненный M2 (augmentация не была недостающим звеном, ожидание одного шага — было). Прямая проверка raw-данных: Proliferation True↔False переключается именно на k=5, j=1. FL Step 8a — независимый reviewer, 2 узких проверяемых чека (регрессия + полный домен 80 состояний на j=1, не выборка), оба CONFIRMED. `graph.yaml`: 131 узел, 156 рёбер, статус `confirmed`, остаётся в `experiments/` (PROMOTE, не REJECT).

**[VERIFIED — 2026-09-10, ADR-097] H-B7-15 (по прямой просьбе пользователя поднять H-B7-14 до «model-level theorem»): exhaustive-верификация j*=1 — theorem-level CONFIRMED.** Ключевой факт: клэмп-фаза — детерминированный walk под фиксированным rule-set, обязана зациклиться (тот же pigeonhole, что у find_attractors/run_until_attractor из H-B7-1/H-B7-3, впервые применённый к клэмп-фазе). Удивительная находка: орбита — всего 7 состояний на ветку (немедленная неподвижная точка на k=6) — k=1..40 (протестированный H-B7-13/14 диапазон) уже был строгим надмножеством ВСЕХ достижимых состояний. Регрессия точно совпала. Theorem-level: n_collisions=0 для ОБОИХ M1 и M2 на j=1 по ПОЛНОМУ домену (12 состояний, не выборка). FL Step 8a reviewer пошёл дальше запрошенного — перебрал все C(7,2)=21 пар состояний, исключив false-positive от бага. Побочно: собственный hand-verified тест дважды содержал ошибку в булевой алгебре (синхронное vs асинхронное обновление) — поймано запуском теста, не перечитыванием математики, оба раза исправлено. `graph.yaml`: 132 узла, 159 рёбер, статус `confirmed`.

**[VERIFIED — 2026-09-10, ADR-097a] H-B7-15 addendum: минимальность j*=1 — бесплатное следствие уже собранных данных.** Пользователь назвал минимальность как один из двух содержательных следующих шагов; проверка показала, что она УЖЕ полностью доказана: закоммиченное поле H-B7-15's `results_at_release_j0` показывает M1 исчерпывающе недостаточным (n_collisions=1) на том же 12-состоянном домене, где j=1 исчерпывающе достаточен — j=0 единственное меньшее значение → j*=1 минимален, не просто достаточен. Уже независимо проверено тем же reviewer-проходом (Check 2 тестировал оба j). Никакого нового эксперимента — только явная формулировка в decision.md/graph.yaml.

**[VERIFIED — 2026-09-10, ADR-098] H-B7-16 (второй из двух вариантов пользователя после H-B7-15: robustness к asynchronous update): DEGRADED-BUT-INFORMATIVE, честная частичная верификация.** Mechanism Claim Gate: single-point readout нестабилен под async (реальный флип в spot-check), windowed-majority-vote (30 checkpoint'ов, purity 0.97-1.00) принят как оценщик. Ключевая находка: чёткий синхронный порог k*=5 размывается в вероятностную S-кривую (P(Proliferation) 7%→84% на k=1..6). M1 accuracy: 79.4%→88.3% (+8.92пп, z=8.45 значимо), но **узко НЕ дотягивает** до предрегистрированного MCID 10пп — честно отмечено borderline. M2 (+p21CIP,+RBL2): 79.4%→95.0% (+15.58пп), уверенно проходит оба порога, значимо превосходит M1 — материальное отличие от синхронного случая (там augmentация не давала разницы вообще). Ceiling не 100% под async (91.9%/98.6%) — честно отражённая стохастичность, не замаскирована. FL Step 8a: reviewer дважды упёрся в лимит ходов на 3 связанных чеках — сужен до 1 чека (главная числовая находка M1 vs M2), CONFIRMED; остальные 2 чека честно названы как self-checked/непроверенные, не скрыты. Вердикт: `lead`, не `confirmed`. `graph.yaml`: 133 узла, 161 ребро.

**[VERIFIED — 2026-09-09, завершение] Весь 100-item каталог просмотрен (100/100), не только 7 кандидатов.** Ключевая переоценка scope: мандат проекта — мост именно к 4 якорям (H-7/RMT, ChernoffPy, May1972, built-инфраструктура Bridge3/7), НЕ любая дёшево вычислимая задача. Классификация: 9 пунктов (#36-47, #75-79, #88-89, #92) тематически связаны с якорем, все проверены и отклонены (ADR-083/084/085); #90-91 уже покрыты закрытием Bridge 3; **83 пункта не имеют тематической связи ни с одним якорем** — дёшевы вычислительно (#1-29, #37, #41, #44, #54, #59-60 честно), но были бы отдельной несвязанной исследовательской линией, не мостом под текущим определением. ADR-086 + pearl_registry: «дёшево ли» и «связано ли с якорем» — два раздельных обязательных условия. **Поиск моста из этого каталога под текущим scope — завершён.** Расширение scope (принять несвязанные-но-дешёвые задачи как отдельное направление) — реальный открытый вопрос, оставлен пользователю явно, не решается автономно (redefinition проекта — другой класс решения, чем выбор среди кандидатов-мостов).

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
- [2026-09-09 09:41] `4786056`: Merge: H-B7-16 async-update robustness, DEGRADED-BUT-INFORMATIVE, honest partial verification
- [2026-09-09 09:40] `e215955` (local, branch `feature/h-b7-16-async-robustness` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-B7-16 -- async-update robustness, DEGRADED-BUT-INFORMATIVE, honest partial verification
- [2026-09-09 09:13] `75fac57`: Merge: H-B7-15 minimality addendum -- free consequence of already-committed exhaustive data
- [2026-09-09 09:13] `d847b44` (local, branch `docs/h-b7-15-minimality-addendum` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs: H-B7-15 -- minimality of j*=1 is a free consequence of already-committed exhaustive data
- [2026-09-09 07:58] `9b3b663` (local, branch `feature/h-b7-15-exhaustive-orbit` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-B7-15 -- exhaustive verification of j*=1 over the complete orbit, theorem-level CONFIRMED
- [2026-09-09 07:27] `b015224` (local, branch `feature/h-b7-14-delayed-observation` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-B7-14 -- delayed-observation restores release-decision observability, j*=1, CONFIRMED
- [2026-09-09 07:14] `270f113` (local, branch `feature/h-b7-13-observability-collision` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-B7-13 -- release-decision observability, REJECTED for both candidate marker sets
- [2026-09-09 06:51] `d58b79e` (local, branch `feature/h-b3-2-ph0-chirality-directed` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-B3-2 -- PH0 chirality-excess, REJECT after bug-fix-and-rerun (Mechanism Claim Gate holds)
- [2026-09-09 06:14] `7bbb4ad` (local, branch `feature/h-b2-3-transferable-dimensionless-predictor` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-B2-3 -- transferable dimensionless predictor test, REJECTED, real bug caught first
- [2026-09-09 05:46] `883cbc6` (local, branch `feature/h-cat37-2-forsythe-s4-minimal-dimension` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-CAT37-2 -- targeted search for s=4 Forsythe counterexample below dim 8, INFORMATIVE_NEGATIVE
- [2026-09-09 05:34] `bdc00d6` (local, branch `docs/retroscan-h-cat37-1-forsythe-resolved` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs: activeContext -- H-CAT37-1 retroscan summary (Forsythe resolved externally, own finding intact)
- [2026-09-09 05:33] `50e4794` (local, branch `docs/retroscan-h-cat37-1-forsythe-resolved` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): fix: retroscan H-CAT37-1 -- Forsythe conjecture proven FALSE for s>=4 (external, arXiv:2609.04659)
- [2026-09-09 05:03] `1debe23` (local, branch `docs/close-100-item-catalog` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs: close full 100-item catalog -- 6 remaining clusters source-verified, not extrapolated
- [2026-09-09 04:58] `f8b2e9a` (local, branch `feature/h-cat31-1-lovasz-theta-circulant` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-CAT31-1 -- Lovasz theta of random circulant graphs CONFIRMED, ratio ~1.0 across n=40..2560
- [2026-09-09 01:51] `6b6e8af` (local, branch `feature/h-cat37-1-forsythe-conjecture` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-CAT37-1 -- Forsythe conjecture (restarted CG) CONFIRMED on tested sample, 2 real bugs caught first
