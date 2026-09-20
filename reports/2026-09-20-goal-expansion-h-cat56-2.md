# Пространство решений цели: довести контрпример H-CAT56-2 до проверенного результата

Дата: 2026-09-20. Режим: `deep`. Цель взята из контекста разговора (пользователь вызвал скилл без аргументов).

**Честная сводка по количеству.** Внутренний пул содержал около 45 кандидатов до слияния; после удаления дублей по механизму
осталось **30 содержательно различных вариантов**, а не 100. Причина: цель узкая (один теоретико-численный результат),
и дополнительные варианты были бы переформулировками (например, «проверить другим кодом» и «проверить другой библиотекой»)
либо чистой внешней аналогией. Требование «не менее 25 междисциплинарных вариантов» **не выполнено**: их 5, и каждый
помечен как гипотеза с положительным штрафом за спекулятивность. Распределение по типам: {'computational_experiment': 7, 'extension': 9, 'established_method': 5, 'new_hypothesis': 3, 'cross_domain_transfer': 5, 'no_go': 1}.

## Раздел 1: Формализация цели

- **primary_goal:** установить, что для обобщённых quasi-pure состояний (Yang, Eq. 12) условие PCC не гарантирует
  насыщение матричной QCRB на одной копии, и довести это до результата, который выдерживает внешнюю проверку и проверку новизны.
- **success_criteria:** (а) точный сертификат (без плавающей арифметики) либо формальное доказательство; (б) необходимость
  Observation 2 доказана самодостаточно; (в) новизна подтверждена ответом специалистов либо полным обзором; (г) воспроизведение
  вне текущей модели и текущего стека; (д) заметка на arXiv.
- **current_state:** контрпример `d=22, r=2, s=16`, `dim V⊥=21<22` (второй: `d=23, r=3, s=12`); независимые пересчёты (мой код на полных
  матрицах, 4 из 4); доказана нижняя граница `dim V⊥ >= r^2+max(s,2kr-sr^2)+max(1,k^2-C(s,2)r^2)`; тест не срабатывает при
  `r=2, d<=21`. Статус в реестре: `INTERNALLY VERIFIED / NOVELTY UNRESOLVED`, публикация `BLOCKED-BY-NOVELTY-CHECK`.
- **known_constraints:** одна лаборатория, проверка одной семьёй моделей, нет точного сертификата над Q(i), новизна
  не установлена; ресурсы ограничены (машина перезагружалась при 12 параллельных LP).
- **excluded_approaches:** случайный поиск как «доказательство», согласие моделей как свидетельство, повторные
  оптимизации без сертификата.
- **evidence_standard:** сертификат или доказательство; поисковая неудача не считается свидетельством.

## Раздел 2: Что уже известно (с маркировкой)

- `<fact>` Observation 2 и класс quasi-pure определены в arXiv:2601.21801 и arXiv:2405.00405; в 2601.21801 вопрос достаточности
  PCC для обобщённых quasi-pure состояний прямо назван открытым (прочитано мной, с цитатой из текста).
- `<fact>` В обзоре arXiv:2602.12097 слова «quasi-pure» нет (проверено поиском по странице); он рассматривает иерархию условий
  коммутативности и утверждает, что для состояний неполного ранга задачи (A), (B) остаются открытыми.
- `<inference>` Необходимость `dim V⊥ >= d` следует из условия `(L_i - c_i)|w> в ker rho` (мой вывод).
- `<hypothesis>` Контрпример новый: поиск ключевыми словами и чтение трёх статей нового пример этого класса не нашли,
  но это слабое свидетельство.
- `<unknown>` Есть ли пример в Supplement или в работах, цитирующих 2601.21801.

## Раздел 3: Карта логических разрывов

1. Нет машинно-точного сертификата (рационально-точный экземпляр).
2. Необходимость Observation 2 не оформлена для внешнего читателя.
3. Новизна проверена только по ключевым словам.
4. Воспроизведение сделано одной моделью и одним стеком.
5. Не выписана точная формулировка «насыщения» (матричная против скалярной, одна копия).
6. Граница `dim V⊥ = d` (d=21) не решена; нет точного теста насыщаемости при `dim V⊥ >= d`.

## Раздел 4: Карта линз (12, каждая с связью с задачей)

Линейная алгебра (ранг-нулевость, границы); компьютерная алгебра (точные сертификаты); формальная верификация (Lean);
теория оценивания (насыщение QCRB); выпуклая геометрия (конус ранг-один операторов в подпространстве); полиномиальная
оптимизация (сертификаты через SOS); численная алгебраическая геометрия (конечные многообразия на границе); теория
матроидов и жёсткости (ранг в общем положении); квантовая коррекция ошибок (условия вида Π A†B Π); воспроизводимость и
научная коммуникация (обмен с авторами, архив); методология (пререгистрация критериев); вычислительный эксперимент
(состязательный поиск против собственной границы).

## 1. Точный контрпример над Q(i) и нижняя оценка ранга по модулю простого

Type: computational_experiment
Evidence: inference
Source domains: computer algebra, exact linear algebra
Target gap: нет машинно-точного сертификата dim V=463

Core mechanism:
PCC для блоков A_j линейно по A_j при фиксированных A_1..A_{j-1}; решать нулевое пространство точной рациональной арифметикой (действительные и мнимые части как рациональные неизвестные, 80 неизвестных), построить состояние над Q(i), затем посчитать ранг 544x484 матрицы порождающих по 2-3 простым модулям. Ранг по модулю p доказывает только rank_Q(i) >= 463 (при корректной редукции знаменателей по модулю p). Точное равенство требует верхней оценки rank <= 463: она следует из доказанной границы dim V⊥ >= 21 (dim V = 484 - dim V⊥ <= 463) и должна быть выписана в сертификате явно вместе с проверкой, что построенный экземпляр имеет блочную структуру, к которой граница применима. Вывод: rank <= 463 и rank(mod p) = 463 дают rank = 463.

Why it may work:
агент упёрся в LLL и целочисленное ядро, а прямое решение нулевого пространства над Q для 80 неизвестных мало; нужен только один точный экземпляр.

Required assumptions:
рациональное решение цепочки нулевых пространств существует с умеренным ростом чисел; PCC выполняется точно.

Main obstacle:
рост коэффициентов при 16 последовательных решениях.

Cheapest test:
python-flint/sympy DomainMatrix: построить A_1..A_16 над Q, проверить PCC точно (ноль), ранг по двум простым.

Falsifier:
точное построение невозможно за разумное время или ранг по модулю p оказывается меньше 463 при точном PCC.

Expected output:
файл с точными A_i и скрипт-сертификат, воспроизводимый за минуты; в сертификате две строки: нижняя оценка по модулю p и верхняя оценка из границы.

Scores:
  relevance: 10
  feasibility: 8
  novelty: 3
  expected_impact: 9
  evidence_strength: 8
  confidence: 0.70
  falsifiability: 10
  speculation_penalty: 0
  priority_score: 8.40
  adjusted_score: 8.40

Sources:
experiments/20260919-pcc-generic-quasipure-cat56-2/decision.md (раздел Exactness); arXiv:2601.21801 (Yang, Imai, Pezze), https://arxiv.org/html/2601.21801

## 2. Машинно-проверенный вывод нижней границы dim V⊥ в Lean 4

Type: extension
Evidence: inference
Source domains: formal verification
Target gap: граница доказана рукой и проверена численно, но не формально

Core mechanism:
формализовать ранг-нулевость: dim V⊥ = r^2 + dim P + dim Q, dim P >= max(s, 2kr - s r^2), dim Q >= max(1, k^2 - C(s,2) r^2) из линейной алгебры Mathlib; вывести, что тест не срабатывает при r=2, d<=21.

Why it may work:
это чистая линейная алгебра над C, Lean на машине установлен (по записи в pearl registry, не проверял версию).

Required assumptions:
Mathlib содержит ранг-нулевость для конечномерных вещественных пространств и работу с эрмитовыми матрицами.

Main obstacle:
перевод эрмитовой структуры и вещественной размерности в Lean трудоёмок.

Cheapest test:
формализовать одну лемму (dim P >= 2kr - s r^2) и оценить время.

Falsifier:
лемма не формализуется за неделю или найден пробел в бумажном доказательстве.

Expected output:
Lean-артефакт, повышающий verification_strength до strong для части утверждений.

Scores:
  relevance: 7
  feasibility: 5
  novelty: 5
  expected_impact: 6
  evidence_strength: 7
  confidence: 0.50
  falsifiability: 9
  speculation_penalty: 1
  priority_score: 6.40
  adjusted_score: 5.40

Sources:
experiments/20260919-pcc-generic-quasipure-cat56-2/decision.md (What was proven)

## 3. Элементарное доказательство необходимости Observation 2 как приложение

Type: established_method
Evidence: inference
Source domains: quantum estimation theory
Target gap: необходимость dim V⊥ >= d выведена в чате, но не оформлена и не проверена экспертом

Core mechanism:
оформить: F=Q iff (L_i - c_i)|w> лежит в ker rho с вещественными c_i; отсюда каждый насыщающий ранг-один элемент лежит в V⊥. POVM, разрешающий единицу, имеет векторы носителей, которые порождают всё C^d, поэтому среди них есть не менее d линейно независимых; их проекторы линейно независимы в пространстве эрмитовых матриц и лежат в V⊥, значит dim V⊥ >= d. Число элементов POVM при этом может быть больше d; измельчение до ранг-один сохраняет насыщение.

Why it may work:
аргумент замкнут и не зависит от препринта, устраняет главный риск (опора на неподтверждённый Observation 2).

Required assumptions:
определения W и M из статьи; насыщение понимается как F_C = F_Q (матричное).

Main obstacle:
лёгкие пробелы в измельчении неранг-один POVM.

Cheapest test:
написать 1-2 страницы и отдать на проверку независимому читателю.

Falsifier:
читатель находит шаг, не следующий из предыдущих.

Expected output:
самодостаточное приложение к заметке.

Scores:
  relevance: 9
  feasibility: 9
  novelty: 2
  expected_impact: 8
  evidence_strength: 9
  confidence: 0.90
  falsifiability: 8
  speculation_penalty: 0
  priority_score: 8.00
  adjusted_score: 8.00

Sources:
experiments/20260919-pcc-generic-quasipure-cat56-2/decision.md (Orchestrator's independent verification); arXiv:2601.21801 (Yang, Imai, Pezze), https://arxiv.org/html/2601.21801

## 4. Воспроизвести числа из самой статьи (пример с двумя кубитами и ancilla)

Type: computational_experiment
Evidence: hypothesis
Source domains: reproducibility
Target gap: наш конвейер не сверен с опубликованными числами W, M, dim V

Core mechanism:
взять пример магнитометрии из End Matter статьи 2601.21801, посчитать dim V и dim V⊥ нашим кодом и сравнить с написанным авторами.

Why it may work:
положительный контроль против первоисточника закрывает риск неверных определений W и M (Gate 1 артефактной идентичности).

Required assumptions:
в статье приведены числа для проверки; определения совпадают.

Main obstacle:
числа в статье могут быть не выписаны явно.

Cheapest test:
прочитать End Matter, выписать ожидаемое dim V и сравнить.

Falsifier:
расхождение с опубликованным числом при тех же входных данных.

Expected output:
строка в decision.md о сверке с опубликованным примером.

Scores:
  relevance: 9
  feasibility: 7
  novelty: 1
  expected_impact: 8
  evidence_strength: 8
  confidence: 0.70
  falsifiability: 9
  speculation_penalty: 0
  priority_score: 7.45
  adjusted_score: 7.45

Sources:
arXiv:2601.21801 (Yang, Imai, Pezze), https://arxiv.org/html/2601.21801

## 5. Независимая реализация в другом пакете (SageMath или Julia)

Type: computational_experiment
Evidence: hypothesis
Source domains: reproducibility
Target gap: все проверки написаны одной моделью на одном стеке numpy

Core mechanism:
переписать построение rho, dRho, SLD, W, M и ранга на другой системе без просмотра прежнего кода, сравнить dim V для d=22, r=2, s=16.

Why it may work:
разные библиотеки и авторство разрывают общие ошибки индексации и точности.

Required assumptions:
определения из статьи достаточны для независимого переписывания.

Main obstacle:
реализовать нужно только по описанию; трудоёмко без Sage/Julia на машине.

Cheapest test:
выбрать доступный пакет, реализовать для d=8, затем d=22.

Falsifier:
другая реализация даёт dim V отличный от 463 при тех же определениях.

Expected output:
второй независимый код и таблица сравнения.

Scores:
  relevance: 8
  feasibility: 6
  novelty: 1
  expected_impact: 7
  evidence_strength: 8
  confidence: 0.70
  falsifiability: 9
  speculation_penalty: 0
  priority_score: 6.80
  adjusted_score: 6.80

Sources:
experiments/20260919-pcc-generic-quasipure-cat56-2/decision.md; scripts/orchestrator_independent_check.py

## 6. Отправить пакет авторам с вопросом «известно ли это»

Type: established_method
Evidence: hypothesis
Source domains: scientific communication
Target gap: проверка новизны идёт только по литературе, без ответа специалистов

Core mechanism:
короткое письмо авторам 2601.21801 и 2405.00405 с точной формулировкой контрпримера, файлом воспроизведения и одним вопросом: известен ли такой пример для обобщённых quasi-pure состояний.

Why it may work:
авторы сами назвали вопрос открытым; их ответ решает вопрос новизны быстрее любого поиска.

Required assumptions:
авторы отвечают; контакт доступен.

Main obstacle:
нет ответа; риск, что идею присвоят без соавторства.

Cheapest test:
составить письмо с приложением и после проверки ответить на вопросы.

Falsifier:
авторы указывают опубликованный пример этого класса.

Expected output:
подтверждение новизны либо ссылка на предшественника.

Scores:
  relevance: 10
  feasibility: 7
  novelty: 1
  expected_impact: 10
  evidence_strength: 7
  confidence: 0.60
  falsifiability: 7
  speculation_penalty: 0
  priority_score: 7.75
  adjusted_score: 7.75

Sources:
arXiv:2601.21801 (Yang, Imai, Pezze), https://arxiv.org/html/2601.21801; arXiv:2405.00405 (Yang), https://arxiv.org/html/2405.00405v4

## 7. Оптимизация измерения на контрпримере: насколько далёк FIM от QFIM

Type: computational_experiment
Evidence: hypothesis
Source domains: numerical optimization
Target gap: неизвестно, насколько сильно нарушено насыщение

Core mechanism:
итеративная оптимизация POVM (в духе QestOptPOVM) для максимизации Tr(F_Q^{-1} F_C); оценить лучший достижимый зазор.

Why it may work:
теорема запрещает нулевой зазор; ненулевой зазор — количественная иллюстрация, а не сертификат.

Required assumptions:
оптимизация достаточно надёжна для d=22.

Main obstacle:
поиск не даёт сертификата ни в какую сторону; дорого при d=22.

Cheapest test:
запустить на уменьшенном аналоге, где Observation 2 не даёт запрета, и на d=22.

Falsifier:
оптимизатор находит FIM=QFIM на d=22 (противоречит теореме, значит ошибка).

Expected output:
число зазора и график сходимости.

Scores:
  relevance: 6
  feasibility: 4
  novelty: 4
  expected_impact: 5
  evidence_strength: 6
  confidence: 0.40
  falsifiability: 5
  speculation_penalty: 1
  priority_score: 5.10
  adjusted_score: 4.10

Sources:
QestOptPOVM arXiv:2403.20131 (наличие подтверждено выдачей поиска)

## 8. Точно зафиксировать понятие «насыщение» и проверить скалярные веса

Type: computational_experiment
Evidence: hypothesis
Source domains: estimation theory
Target gap: результат относится к матричному F_C=F_Q; для скалярной границы Tr[W F^{-1}] вывод может меняться

Core mechanism:
определить уровень утверждения (матричное, одна копия), затем на состоянии контрпримера проверить, достижима ли скалярная граница для конкретных весов W.

Why it may work:
иначе критик скажет, что мы опровергли не то понятие насыщения.

Required assumptions:
скалярная оптимизация решаема на d=22.

Main obstacle:
скалярный случай может быть отдельной трудной задачей.

Cheapest test:
выписать формулировку и найти литературное определение насыщения QCRB.

Falsifier:
по литературе стандартное определение скалярное, а не матричное, и наш результат его не затрагивает.

Expected output:
точная формулировка результата и оговорка в заметке.

Scores:
  relevance: 8
  feasibility: 6
  novelty: 6
  expected_impact: 7
  evidence_strength: 5
  confidence: 0.50
  falsifiability: 7
  speculation_penalty: 1
  priority_score: 6.65
  adjusted_score: 5.65

Sources:
arXiv:2601.21801 (Yang, Imai, Pezze), https://arxiv.org/html/2601.21801

## 9. Явная физическая модель контрпримера с целочисленными Гамильтонианами

Type: computational_experiment
Evidence: hypothesis
Source domains: quantum physics modelling
Target gap: контрпример задан блоками SLD, а не Гамильтонианами

Core mechanism:
построить rho_lambda = U(lambda) rho_0 U(lambda)^dag с 16 эрмитовыми генераторами, дающими нужные блоки B_i, целочисленные или гауссово-рациональные.

Why it may work:
читателю проще проверить явную модель; заодно проверяется реализуемость семьи.

Required assumptions:
блоки B_i выражаются через генераторы вне поддержки.

Main obstacle:
нужно проверить интегрируемость до второго порядка.

Cheapest test:
построить для малого d с той же структурой, затем для d=22.

Falsifier:
получившаяся семья не квази-чистая или PCC нарушается на построенных генераторах.

Expected output:
файл с явной моделью и проверкой.

Scores:
  relevance: 7
  feasibility: 6
  novelty: 5
  expected_impact: 7
  evidence_strength: 6
  confidence: 0.50
  falsifiability: 8
  speculation_penalty: 1
  priority_score: 6.55
  adjusted_score: 5.55

Sources:
experiments/20260919-pcc-generic-quasipure-cat56-2/decision.md; arXiv:2405.00405 (Yang), https://arxiv.org/html/2405.00405v4

## 10. Регрессионные тесты для независимой проверки контрпримера

Type: extension
Evidence: fact
Source domains: software engineering
Target gap: проверка существует только как одноразовый скрипт без теста

Core mechanism:
pytest, фиксирующий dim V=463 и dim V⊥ для d=20, 21, 22, 23 и контрольные случаи; запуск за секунды.

Why it may work:
не даёт молча испортиться результату при рефакторинге.

Required assumptions:
числа стабильны на разных сидах.

Main obstacle:
тест зависит от случайного сэмплера.

Cheapest test:
оформить два-три теста на существующем скрипте.

Falsifier:
тест падает без изменения кода (нестабильность).

Expected output:
tests/test_pcc_counterexample.py.

Scores:
  relevance: 5
  feasibility: 9
  novelty: 1
  expected_impact: 4
  evidence_strength: 8
  confidence: 0.90
  falsifiability: 9
  speculation_penalty: 0
  priority_score: 6.05
  adjusted_score: 6.05

Sources:
scripts/orchestrator_independent_check.py

## 11. Полный обзор предшественников: цитирующие работы, Supplement, определение Eq.12 и «generic»

Type: established_method
Evidence: hypothesis
Source domains: literature search
Target gap: поиск ключевыми словами слабое свидетельство; нет проверки Supplement и цитирований

Core mechanism:
Semantic Scholar/INSPIRE: работы, цитирующие 2601.21801 и 2405.00405; прочитать Supplement, точную формулировку гипотезы в Ref. [38], пример E из Ref. [59]; проверить, что в Eq.12 нет скрытых предположений (постоянный ранг, независимость ядра) и смысл слова «generic».

Why it may work:
закрывает главный блокер публикации (BLOCKED-BY-NOVELTY-CHECK) и риск скрытых допущений.

Required assumptions:
нужные тексты доступны.

Main obstacle:
часть источников платная или без открытого текста.

Cheapest test:
выгрузить список цитирований и просмотреть 20-30 работ.

Falsifier:
найден опубликованный пример PCC без насыщения для класса Eq.12 или явное дополнительное допущение, которое наши состояния нарушают.

Expected output:
таблица предшественников и решение о новизне.

Scores:
  relevance: 10
  feasibility: 8
  novelty: 1
  expected_impact: 9
  evidence_strength: 6
  confidence: 0.80
  falsifiability: 8
  speculation_penalty: 0
  priority_score: 7.70
  adjusted_score: 7.70

Sources:
arXiv:2601.21801 (Yang, Imai, Pezze), https://arxiv.org/html/2601.21801; arXiv:2405.00405 (Yang), https://arxiv.org/html/2405.00405v4; arXiv:2602.12097, https://arxiv.org/html/2602.12097

## 12. Доказать точность нижней границы: dim V⊥ = r^2 + s* + 1 при k >= 5

Type: extension
Evidence: hypothesis
Source domains: linear algebra, matroid theory
Target gap: точность границы измерена, а не доказана

Core mechanism:
показать, что при s* = ceil(2kr/(r^2+1)) генерики достигают равенства, предъявив один экземпляр над Q(i) и используя полунепрерывность ранга.

Why it may work:
один точный пример даёт равенство для общего положения (верхняя оценка через ранг).

Required assumptions:
существует экземпляр с нужным рангом; равенство не нарушается арифметикой.

Main obstacle:
нужно решить систему для каждого k.

Cheapest test:
проверить равенство точной арифметикой для r=2, k=5..12.

Falsifier:
экземпляр с dim V⊥ выше формулы при том же (d, r, s).

Expected output:
теорема о точности и формула первого срабатывания d*(r).

Scores:
  relevance: 8
  feasibility: 5
  novelty: 7
  expected_impact: 7
  evidence_strength: 5
  confidence: 0.50
  falsifiability: 8
  speculation_penalty: 1
  priority_score: 6.65
  adjusted_score: 5.65

Sources:
experiments/20260919-pcc-generic-quasipure-cat56-2/decision.md

## 13. Замкнутая формула минимального d для срабатывания при всех r

Type: extension
Evidence: inference
Source domains: combinatorics
Target gap: первые размеры срабатывания 22, 23, 31, 41 найдены перебором r=2..5, общей формулы нет

Core mechanism:
минимизировать по s правую часть границы; получить d*(r) и доказать, что при d < d*(r) тест не срабатывает.

Why it may work:
перебор уже сделан, нужна только замкнутая форма.

Required assumptions:
граница верна.

Main obstacle:
минимум по s может не иметь простой формы.

Cheapest test:
посчитать d*(r) для r до 12 и подобрать формулу.

Falsifier:
формула не сходится с перебором хотя бы в одной точке.

Expected output:
утверждение о минимальном размере контрпримера.

Scores:
  relevance: 7
  feasibility: 6
  novelty: 6
  expected_impact: 6
  evidence_strength: 6
  confidence: 0.60
  falsifiability: 9
  speculation_penalty: 1
  priority_score: 6.55
  adjusted_score: 5.55

Sources:
experiments/20260919-pcc-generic-quasipure-cat56-2/metrics/theory.json

## 14. Гипотеза: Observation 2 — единственное препятствие для quasi-pure (dim V⊥ >= d достаточно)

Type: new_hypothesis
Evidence: hypothesis
Source domains: quantum estimation theory
Target gap: не известно, есть ли второе препятствие сверх счёта размерности

Core mechanism:
предположить, что для обобщённых quasi-pure состояний PCC и dim V⊥ >= d гарантируют насыщение; искать контрпримеры около границы.

Why it may work:
все 36 из 36 проверенных состояний при d<=6 насыщаемы (расчёт сегодня), ни одного нарушения.

Required assumptions:
тест Observation 2 полон в классе quasi-pure.

Main obstacle:
нужен точный тест насыщаемости, поиск без сертификата.

Cheapest test:
сканировать состояния с dim V⊥ = d и d+1 при d=20, 21 (эти есть в нашем классе).

Falsifier:
состояние с dim V⊥ >= d и доказанной ненасыщаемостью (второй механизм).

Expected output:
утверждение (гипотеза) или второй контрпример.

Scores:
  relevance: 8
  feasibility: 4
  novelty: 8
  expected_impact: 9
  evidence_strength: 3
  confidence: 0.30
  falsifiability: 8
  speculation_penalty: 2
  priority_score: 6.65
  adjusted_score: 4.65

Sources:
experiments/20260919-pcc-generic-quasipure-cat56-2/decision.md; reports/2026-09-19-prior-result-gate-h-cat56-3.md

## 15. Граничный случай dim V⊥ = d (d=21, r=2, s=16) через конечное многообразие

Type: cross_domain_transfer
Evidence: hypothesis
Source domains: numerical algebraic geometry
Target gap: при n=d-1 допустимые векторы образуют конечное многообразие, точного решения нет

Core mechanism:
система условий гололизации на 21-мерном V⊥ с 20 вещественными параметрами; решить непрерывной гомотопией (Bertini/HomotopyContinuation.jl) и проверить существование ортонормированного базиса из ранг-один элементов.

Why it may work:
конечное число решений даёт точный ответ, а не поиск.

Required assumptions:
система полиномиальная и достаточно малая для гомотопий.

Main obstacle:
20 переменных и высокая степень; инструменты не установлены.

Cheapest test:
решить сначала на аналоге малой размерности с dim V⊥ = d.

Falsifier:
решатель не сходится или число решений превышает вычислимое.

Expected output:
ответ «насыщаемо / нет» на границе.

Scores:
  relevance: 8
  feasibility: 3
  novelty: 8
  expected_impact: 9
  evidence_strength: 3
  confidence: 0.30
  falsifiability: 9
  speculation_penalty: 2
  priority_score: 6.55
  adjusted_score: 4.55

Sources:
метод — [MEMORY], источник не читался; см. reports/2026-09-19-prior-result-gate-h-cat56-3.md

## 16. Сертификат ненасыщаемости через моментные релаксации Ласерра

Type: cross_domain_transfer
Evidence: hypothesis
Source domains: polynomial optimization
Target gap: V3 из Relaxation Map: нужен сертификат отсутствия ранг-один разложения единицы в V⊥

Core mechanism:
по Фаркашу: искать эрмитов Y с <u|Y|u> >= 0 на допустимых u и Tr Y < 0; проверять через суммы квадратов уровня 2.

Why it may work:
даёт сертификат отрицательного ответа, чего не даёт поиск.

Required assumptions:
уровень релаксации достаточно мал для d <= 8.

Main obstacle:
размер релаксации растёт как d^4; может быть неплотной.

Cheapest test:
реализовать на d=4 с известным ответом.

Falsifier:
релаксация не сертифицирует даже заведомо ненасыщаемое состояние (d=22 через сокращение).

Expected output:
инструмент точной проверки насыщаемости для малых d.

Scores:
  relevance: 8
  feasibility: 4
  novelty: 7
  expected_impact: 8
  evidence_strength: 4
  confidence: 0.35
  falsifiability: 9
  speculation_penalty: 2
  priority_score: 6.60
  adjusted_score: 4.60

Sources:
метод — [MEMORY]; H-CAT56-1 Relaxation Map V3

## 17. Доказать общий ранг через матроидный или жёсткостной счёт

Type: cross_domain_transfer
Evidence: hypothesis
Source domains: matroid theory, rigidity theory
Target gap: нет доказательства, что общий ранг равен формуле

Core mechanism:
как в теории жёсткости: generic rank на алгебраическом семействе есть максимальный ранг на открытом плотном множестве, а в специальных точках ранг может быть ниже. Один точный экземпляр максимального ранга (идея 1) даёт нижнюю оценку для generic claim, а матроидный счёт даёт верхнюю; утверждать равенство в любой точке нельзя.

Why it may work:
структура «порождающие через билинейные условия» похожа на жёсткостные матрицы.

Required assumptions:
ранг нижне-полунепрерывен по Зарисскому; формула для верхней оценки известна.

Main obstacle:
аналогия структурная, но не формально доказана.

Cheapest test:
проверить полунепрерывность на малом примере.

Falsifier:
ранг в некоторой точке многообразия PCC превышает найденную верхнюю оценку.

Expected output:
доказательство общего положения без выбора точки.

Scores:
  relevance: 6
  feasibility: 5
  novelty: 7
  expected_impact: 6
  evidence_strength: 5
  confidence: 0.35
  falsifiability: 8
  speculation_penalty: 2
  priority_score: 5.95
  adjusted_score: 3.95

Sources:
методы — [MEMORY]

## 18. Размерность многообразия PCC и допустимое число параметров

Type: cross_domain_transfer
Evidence: hypothesis
Source domains: algebraic geometry
Target gap: неизвестно, при каких s многообразие PCC непусто и невырождено

Core mechanism:
посчитать размерность пространства решений A_i^dag A_j эрмитово (детерминантальная структура): 2kr - 4(j-1) вещественных степеней свободы на шаг j.

Why it may work:
объясняет, почему s ограничено и где QFIM становится вырожденной.

Required assumptions:
условия независимы в общем положении.

Main obstacle:
условия зависимы при специальных A_i.

Cheapest test:
проверить размерности ядер по шагам на d=22 (они есть в метриках агента).

Falsifier:
фактическая размерность ядра не совпадает с подсчётом.

Expected output:
формула для s_max(d, r).

Scores:
  relevance: 5
  feasibility: 5
  novelty: 6
  expected_impact: 5
  evidence_strength: 5
  confidence: 0.30
  falsifiability: 7
  speculation_penalty: 2
  priority_score: 5.30
  adjusted_score: 3.30

Sources:
experiments/20260919-pcc-generic-quasipure-cat56-2/decision.md

## 19. Обобщить границу на не-quasi-pure состояния с ненулевыми блоками ядра

Type: extension
Evidence: hypothesis
Source domains: quantum estimation theory
Target gap: граница выведена только при Π_r ∂ρ Π_r = 0

Core mechanism:
разложить V на блоки с ненулевыми kernel-kernel вкладами и вывести аналогичную нижнюю оценку через ранг-нулевость.

Why it may work:
снимает ограничение на класс и связывается с общим утверждением Observation 2.

Required assumptions:
блочная структура по-прежнему сохраняется.

Main obstacle:
блоки перестают быть ортогональными, счёт усложняется.

Cheapest test:
разобрать случай r=2, малое ненулевое kernel-kernel возмущение.

Falsifier:
получена граница, слабее известной.

Expected output:
теорема для более широкого класса.

Scores:
  relevance: 6
  feasibility: 5
  novelty: 7
  expected_impact: 7
  evidence_strength: 4
  confidence: 0.35
  falsifiability: 7
  speculation_penalty: 2
  priority_score: 5.90
  adjusted_score: 3.90

Sources:
experiments/20260919-pcc-generic-quasipure-cat56-2/decision.md

## 20. Порог по числу параметров: при каких s достаточность PCC для quasi-pure гарантирована

Type: new_hypothesis
Evidence: hypothesis
Source domains: quantum estimation theory
Target gap: теорема статьи даёт порог по размерности, но не по числу параметров

Core mechanism:
вывести из счёта, что при s <= s0(d, r) выполняется dim V⊥ >= d плюс что-то и PCC достаточно.

Why it may work:
комплементарно к контрпримеру: где достаточность верна.

Required assumptions:
второго препятствия нет (см. гипотезу о единственности).

Main obstacle:
зависит от результата этой гипотезы.

Cheapest test:
сравнить порог по d из Eq.(15) с нашим счётом.

Falsifier:
порог противоречит контрпримеру или статье.

Expected output:
уточнение порога достаточности.

Scores:
  relevance: 6
  feasibility: 4
  novelty: 7
  expected_impact: 6
  evidence_strength: 3
  confidence: 0.25
  falsifiability: 6
  speculation_penalty: 2
  priority_score: 5.25
  adjusted_score: 3.25

Sources:
arXiv:2601.21801 (Yang, Imai, Pezze), https://arxiv.org/html/2601.21801

## 21. Численная устойчивость dim V при малом положительном p2

Type: computational_experiment
Evidence: hypothesis
Source domains: sanity check
Target gap: ранги в определении V не должны зависеть от конкретных положительных p

Core mechanism:
пересчитать независимым кодом для p2 = 0.4, 0.1, 1e-3, 1e-6 и убедиться, что dim V=463. Это проверка устойчивости при строго положительном спектре. Она НЕ говорит о переходе к чистому состоянию: при p2 = 0 ранг состояния падает и структура SLD может измениться скачком.

Why it may work:
быстро (минуты), проверяет допущение «ранги не зависят от p при положительном спектре».

Required assumptions:
SLD блоки в положительном спектре зависят от p гладко и не меняют ранги.

Main obstacle:
при малых p2 численная точность падает.

Cheapest test:
запустить orchestrator_independent_check.py с разными p.

Falsifier:
dim V меняется с p при положительном спектре (тогда вывод о независимости от p неверен).

Expected output:
строка проверки в decision.md.

Scores:
  relevance: 7
  feasibility: 9
  novelty: 5
  expected_impact: 6
  evidence_strength: 7
  confidence: 0.80
  falsifiability: 10
  speculation_penalty: 0
  priority_score: 7.30
  adjusted_score: 7.30

Sources:
scripts/orchestrator_independent_check.py

## 22. Мост с квантовой коррекцией ошибок: условия Книлла–Лафламма и PCC

Type: cross_domain_transfer
Evidence: hypothesis
Source domains: quantum error correction
Target gap: условие вида Π A_i^dag A_j Π = λ_ij Π похоже на PCC; связь метрологии и коррекции ошибок известна

Core mechanism:
сопоставить PCC блокам A_i^dag A_j и искать, даёт ли код-теоретический счёт (число операторов ошибки против размерности кода) ту же границу.

Why it may work:
обе стороны — счёт ограничений против размерности.

Required assumptions:
сопоставление вида «Эрмитов A^dag A» ↔ «пропорционален единице» корректно.

Main obstacle:
аналогия может быть чисто внешней; у нас уже был такой мост (Bridge 10).

Cheapest test:
выписать оба условия рядом и проверить, следует ли одно из другого.

Falsifier:
условия не сводятся друг к другу ни в одном предельном случае.

Expected output:
либо новая связь, либо отрицательный результат.

Scores:
  relevance: 5
  feasibility: 4
  novelty: 8
  expected_impact: 6
  evidence_strength: 2
  confidence: 0.15
  falsifiability: 6
  speculation_penalty: 3
  priority_score: 4.95
  adjusted_score: 1.95

Sources:
Knill–Laflamme, [MEMORY]; связь метрологии и QEC — [MEMORY]

## 23. Короткая заметка на arXiv: теорема, точный пример, доказательство необходимости

Type: established_method
Evidence: hypothesis
Source domains: scientific publication
Target gap: результата пока нет в статье; путь к публикации не описан

Core mechanism:
структура: постановка (Eq.12, PCC), теорема о границе, точный контрпример (идея 1), приложение с доказательством необходимости (идея 3), сверка с опубликованным примером (идея 4).

Why it may work:
короткая заметка — естественный формат для узкого результата; собирается из уже готовых частей.

Required assumptions:
идеи 1, 3, 4, 6, 11 дали положительный результат.

Main obstacle:
зависит от ответа авторов и проверки новизны.

Cheapest test:
собрать черновик из готовых разделов decision.md.

Falsifier:
результат оказывается известным или содержит ошибку.

Expected output:
препринт.

Scores:
  relevance: 10
  feasibility: 6
  novelty: 1
  expected_impact: 10
  evidence_strength: 6
  confidence: 0.60
  falsifiability: 6
  speculation_penalty: 0
  priority_score: 7.30
  adjusted_score: 7.30

Sources:
experiments/20260919-pcc-generic-quasipure-cat56-2/decision.md

## 24. Архив воспроизведения на Zenodo с запуском одной командой

Type: established_method
Evidence: fact
Source domains: reproducibility
Target gap: код и метрики лежат в репозитории, но без цитируемого архива и единой команды

Core mechanism:
собрать код (h2_core, fp_certify, orchestrator_independent_check), метрики и README с одной командой, дать DOI.

Why it may work:
повышает проверяемость для внешних читателей.

Required assumptions:
репозиторий публичный, лицензия ясна.

Main obstacle:
поддержка зависимостей.

Cheapest test:
написать make/скрипт и прогнать с чистого клона.

Falsifier:
результат не воспроизводится на чистой машине.

Expected output:
DOI и README.

Scores:
  relevance: 7
  feasibility: 9
  novelty: 1
  expected_impact: 6
  evidence_strength: 9
  confidence: 0.90
  falsifiability: 9
  speculation_penalty: 0
  priority_score: 7.10
  adjusted_score: 7.10

Sources:
experiments/20260919-pcc-generic-quasipure-cat56-2

## 25. Формализовать необходимость Observation 2 в Lean

Type: extension
Evidence: hypothesis
Source domains: formal verification
Target gap: необходимость выведена бумажно, формально не проверена

Core mechanism:
формализовать: базис из d ранг-один элементов с суммой I линейно независим и лежит в V⊥, значит dim V⊥ >= d.

Why it may work:
убирает опору на доверие к тексту.

Required assumptions:
теория PSD-матриц в Mathlib достаточна.

Main obstacle:
трудоёмко: эрмитовы матрицы и ранг-один проекторы.

Cheapest test:
формализовать только линейную независимость d проекторов.

Falsifier:
лемма не проходит формализацию.

Expected output:
формальный артефакт.

Scores:
  relevance: 6
  feasibility: 4
  novelty: 5
  expected_impact: 6
  evidence_strength: 6
  confidence: 0.40
  falsifiability: 9
  speculation_penalty: 1
  priority_score: 5.80
  adjusted_score: 4.80

Sources:
Lean 4 — установка машины по записи в pearl registry, не проверял

## 26. Калькулятор диагностики: таблица размеров, где тест Observation 2 может сработать

Type: extension
Evidence: fact
Source domains: software tools
Target gap: нет инструмента, дающего первое d срабатывания для заданных (r, s)

Core mechanism:
маленькая функция и таблица по формуле границы, включая r до 8 и s до 2kr; выдавать d*(r).

Why it may work:
полезно другим исследователям; побочный продукт идеи 13.

Required assumptions:
граница верна.

Main obstacle:
нужно убедиться, что граница применима вне протестированных диапазонов.

Cheapest test:
реализовать и сверить с theory.json.

Falsifier:
таблица расходится с перебором.

Expected output:
функция и таблица в заметке.

Scores:
  relevance: 5
  feasibility: 8
  novelty: 3
  expected_impact: 4
  evidence_strength: 7
  confidence: 0.70
  falsifiability: 8
  speculation_penalty: 0
  priority_score: 5.80
  adjusted_score: 5.80

Sources:
experiments/20260919-pcc-generic-quasipure-cat56-2/metrics/theory.json

## 27. Попытаться опровергнуть собственную границу состязательным поиском

Type: no_go
Evidence: hypothesis
Source domains: adversarial testing
Target gap: граница проверена на 234 образцах, но это не попытка её сломать

Core mechanism:
оптимизировать по A_i так, чтобы dim V⊥ оказалось ниже нижней границы; любой успех опровергает теорему.

Why it may work:
если граница верна, поиск не находит; если находит, нашли ошибку до публикации.

Required assumptions:
оптимизатор способен исследовать многообразие PCC.

Main obstacle:
поиск без сертификата: неудача слаба как доказательство.

Cheapest test:
запустить адаптивный поиск с целевой функцией «ранг минус граница».

Falsifier:
найден экземпляр с dim V⊥ ниже границы (граница неверна).

Expected output:
подтверждённая или опровергнутая граница.

Scores:
  relevance: 8
  feasibility: 7
  novelty: 3
  expected_impact: 7
  evidence_strength: 6
  confidence: 0.70
  falsifiability: 10
  speculation_penalty: 0
  priority_score: 7.00
  adjusted_score: 7.00

Sources:
experiments/20260919-pcc-generic-quasipure-cat56-2/decision.md

## 28. Две копии и коллективные измерения: остаётся ли состояние ненасыщаемым

Type: new_hypothesis
Evidence: hypothesis
Source domains: quantum estimation theory
Target gap: результат — про одну копию; для N копий насыщение возможно асимптотически

Core mechanism:
проверить, снимает ли двухкопийное коллективное измерение запрет; условие переходит в размерность d^2=484.

Why it may work:
поясняет границу применимости результата.

Required assumptions:
PCC для двух копий переформулируется корректно.

Main obstacle:
d=484 делает расчёт неподъёмным.

Cheapest test:
оценить размерности и только сформулировать оговорку.

Falsifier:
оценка показывает, что вопрос решается тривиально формулой Nagaoka/Holevo.

Expected output:
оговорка в заметке.

Scores:
  relevance: 4
  feasibility: 2
  novelty: 7
  expected_impact: 5
  evidence_strength: 2
  confidence: 0.10
  falsifiability: 5
  speculation_penalty: 3
  priority_score: 3.90
  adjusted_score: 0.90

Sources:
Holevo-QCR gap обсуждается в arXiv:2602.12097 (прочитано частично)

## 29. Расширить Prior Result Gate: обязательная проверка отзыва источника

Type: extension
Evidence: fact
Source domains: research methodology
Target gap: сегодня поиск выдал отозванную статью как релевантную

Core mechanism:
в шаблон гейта добавить шаг: для каждого источника открыть страницу и проверить статус withdrawn/retracted.

Why it may work:
дешёвая защита от ложной опоры; сработала сегодня.

Required assumptions:
страницы источника доступны.

Main obstacle:
не для всех издателей статус виден.

Cheapest test:
добавить строку в шаблон и в чеклист отчёта.

Falsifier:
шаг не находит ничего на 10 следующих проверках (стоит ли держать).

Expected output:
изменение шаблона.

Scores:
  relevance: 4
  feasibility: 9
  novelty: 1
  expected_impact: 5
  evidence_strength: 8
  confidence: 0.90
  falsifiability: 8
  speculation_penalty: 0
  priority_score: 5.90
  adjusted_score: 5.90

Sources:
reports/2026-09-19-prior-result-gate-h-cat56-3.md

## 30. Заранее зафиксировать критерии повышения verification_strength

Type: extension
Evidence: fact
Source domains: research methodology
Target gap: сейчас H-CAT56-2 medium без формального перехода в strong

Core mechanism:
прописать: strong только при внешнем воспроизведении (идея 6 или 5) либо машинном доказательстве (идея 2) плюс проверенной новизне (идея 11).

Why it may work:
не даёт самообману повысить статус по настроению.

Required assumptions:
критерии принимаются.

Main obstacle:
формальность без пользы.

Cheapest test:
дописать строку в graph.yaml комментарий узла.

Falsifier:
ни один критерий не выполним в разумный срок.

Expected output:
правило в записи узла.

Scores:
  relevance: 6
  feasibility: 9
  novelty: 1
  expected_impact: 6
  evidence_strength: 8
  confidence: 0.90
  falsifiability: 8
  speculation_penalty: 0
  priority_score: 6.60
  adjusted_score: 6.60

Sources:
registry/graph.yaml (узел H-CAT56-2)

## Приоритеты: уровни и порядок исполнения

Числовые оценки в карточках (`priority_score`, `adjusted_score`, `confidence`) субъективны и **порядковые**: разница вроде 7.70 против 7.75 ничего не значит, а `confidence` не является вероятностью. Для решений используются уровни ниже, они устойчивы к небольшому сдвигу весов.

| Уровень | Идеи | Смысл |
|---|---|---|
| A, блокирующие | 1, 3, 4, 11 | точность сертификата, логика запрета, воспроизведение опубликованного примера, новизна |
| B, внешняя проверка и публикация | 5, 6, 23, 24 | независимая реализация, вопрос авторам, заметка, архив |
| C, усиление результата | 8, 12, 13, 21, 27 | формулировка насыщения, точность границы, формула d*(r), устойчивость, состязательный поиск |
| D, исследовательские | 14-20, 22, 28 | второй механизм, граница dim V⊥=d, обобщения, мосты |
| Процесс | 10, 25, 26, 29, 30 | тесты, Lean, калькулятор, шаг про отзыв источника, критерии статуса |

**Порядок исполнения (по зависимостям, не по оценке):** 4 → 3 → 1 → 11 → 6 → 5 и 24 → 23.

1. **4** первой: если код не воспроизводит пример самой статьи, точная арифметика бессмысленна (проверка идентичности артефакта).
2. **3**: зафиксировать логический мост от дефекта ранга к ненасыщаемости.
3. **1**: точный экземпляр над Q(i) с двусторонним сертификатом ранга.
4. **11**: серьёзный поиск предшественников.
5. **6**: письмо авторам только после сертификата: короткий проверяемый пакет сильнее фразы «нашли численно».
6. **5 и 24**, затем **23**.

Из 1+3+11 публикация автоматически не следует: нужны ещё корректная область утверждения (идея 8: насыщение матричной QCRB на одной копии, а не скалярные веса или коллективные измерения) и независимое воспроизведение.

### Скрытые допущения финалистов (Circularity Scan)

| # | Идея | Скрытое допущение |
|---|---|---|
| 1 | Точный контрпример над Q(i) и нижняя оценка ранга по модулю простого | точное решение существует с приемлемым ростом чисел (LOW) |
| 3 | Элементарное доказательство необходимости Observation 2 как приложение | определение насыщения совпадает с матричным F_C=F_Q (MEDIUM) |
| 4 | Воспроизвести числа из самой статьи (пример с двумя кубитами и ancilla) | числа в статье выписаны явно (MEDIUM) |
| 5 | Независимая реализация в другом пакете (SageMath или Julia) | определения из статьи достаточны для независимого переписывания (MEDIUM) |
| 6 | Отправить пакет авторам с вопросом «известно ли это» | авторы отвечают и не присваивают идею (MEDIUM) |
| 10 | Регрессионные тесты для независимой проверки контрпримера | числа стабильны на разных сидах (LOW) |
| 11 | Полный обзор предшественников: цитирующие работы, Supplement, определение Eq.12 и «generic» | источники открыты и найдены; Supplement доступен (MEDIUM) |
| 21 | Численная устойчивость dim V при малом положительном p2 | блочная структура не зависит от спектра p (LOW) |
| 23 | Короткая заметка на arXiv: теорема, точный пример, доказательство необходимости | идеи 1, 3, 4, 6, 11 дали положительный результат (HIGH) |
| 24 | Архив воспроизведения на Zenodo с запуском одной командой | чистый клон воспроизводит без скрытых зависимостей (LOW) |
| 27 | Попытаться опровергнуть собственную границу состязательным поиском | оптимизатор способен исследовать многообразие PCC (MEDIUM) |
| 30 | Заранее зафиксировать критерии повышения verification_strength | критерии принимаются без пересмотра задним числом (LOW) |

## Три портфеля

- **Conservative (проверка и путь к публикации):** идеи 1, 3, 4, 6, 10, 11, 21, 23, 24, 27, 29, 30. Цель: превратить внутренне проверенный результат
  во внешне проверенный, не расширяя его.
- **Balanced:** Conservative плюс 2, 5, 8, 9, 12, 13, 25, 26. Цель: строже доказать границу и определить точную формулировку.
- **Moonshot:** 14, 15, 16, 17, 19, 22. Цель: выяснить, есть ли второй механизм контрпримера у границы `dim V⊥ = d` и шире класса.
  Низкая вероятность успеха (уверенность 0,25-0,35), высокая цена, поиск без сертификата не считается ответом.

## Матрица зависимостей (кратко)

1 (точный экземпляр) → 12 (точность границы), 2 (Lean), 23 (заметка). 3 (необходимость) → 25 (Lean), 23. 11 (обзор) → 6 (авторы) →
23. 21 и 27 (проверки собственных допущений) → 23. 14-16 (граница и второй механизм) зависят от 3 и от того, найдётся ли точный тест насыщаемости (16).

## План прототипирования

- **День:** идеи 21 (предел p2), 4 (сверка с примером статьи), 10 (тесты), 30 (критерии), 29 (шаг про отзыв источника).
- **Неделя:** идея 1 (точный экземпляр), 3 (оформление доказательства), 11 (обзор и определение Eq.12), письмо авторам (6), состязательный поиск против границы (27).
- **Месяц:** 5 (независимая реализация), 12-13 (точность и d*(r)), 2 и 25 (Lean), 24 (архив), черновик заметки (23).
- **Год:** 14-16 (второй механизм, граница dim V⊥=d, сертификат Ласерра), 19 (обобщение), возможно совместная работа с авторами.

## Отрицательные результаты и запреты, найденные при исследовании

- Тест Observation 2 **не может** сработать при `r=2, d<=21` и `r=3, d<=22` (доказано); вопрос достаточности в этих размерах остаётся открытым.
- Исходный H-CAT56-1 искал контрпример в классе Eq.(16), где достаточность доказана теоремой (REPEAT).
- Мост «LP-вершина Ловаса ↔ размер POVM» тривиален (Мост 10).
- Минимальный размер POVM в проверенной области равен `d` (H-CAT56-3, тривиально).
- Статья arXiv:2405.01471 отозвана автором и не используется.
- Закон разброса числа Ловаса на простых `n` не подтвердил заранее заявленное «исключает −1» (H-CAT31-4).

## Неизвестное

- Есть ли в Supplement 2601.21801 или в работах, цитирующих её, явный пример PCC без насыщения для класса Eq.12.
- Достаточен ли `dim V⊥ >= d` для насыщения quasi-pure состояний (идея 14; проверена лишь до `d<=6`).
- Как изменится вывод при скалярной формулировке границы (идея 8).

## Источники (реально просмотренные)

- arXiv:2601.21801 (Yang, Imai, Pezze), https://arxiv.org/html/2601.21801
- arXiv:2405.00405 (Yang), https://arxiv.org/html/2405.00405v4
- arXiv:2602.12097, https://arxiv.org/html/2602.12097
- Yamagata, arXiv:2604.21323, https://arxiv.org/abs/2604.21323
- Im, Wolkowicz, «A strengthened Barvinok–Pataki bound on SDP rank», https://optimization-online.org/2021/04/8346/ (наличие подтверждено выдачей поиска)
- Локальные: `experiments/20260919-pcc-generic-quasipure-cat56-2/decision.md`, `scripts/orchestrator_independent_check.py`, `reports/2026-09-19-prior-result-gate-h-cat56-3.md`

Методы Ласерра, матроидные счёты жёсткости, гомотопии и условия Книлла–Лафламма приведены по памяти (`[MEMORY]`), их источники не открывались.
