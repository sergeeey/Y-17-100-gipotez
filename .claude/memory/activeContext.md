# activeContext.md — Y-17 100 gipotez

## Scope Fence
- **Goal:** [PLAN, не факт] Оценить и начать проверку cross-domain мостов между каталогом ~141 открытых научных задач и реальными проектами (H-7 chromatin, ChernoffPy, May 1972)
- **[2026-09-09, ADR-087] Scope расширен пользователем явно:** пятый источник гипотез — сам 100-item каталог напрямую, без требования тематической связи с исходными 4 якорями. Не отменяет исходные якоря, добавляет к ним.
- **[VERIFIED — 2026-09-10] Deep external novelty audit — читать вторым (после ADR-121, перед ADR-122).** По прямому запросу пользователя запущены 6 параллельных `Agent(analyst)` по кластерам (Boolean network dynamics/control, Boolean structural/canalization, Forsythe, transient growth/Kreiss, TDA lakes, Lovász theta), каждый проверял ~33 сильных claim'а на 10 возможных отношений к внешней литературе (special case/counterexample/known-by-theorem/etc). **Критическая находка: все 6 агентов не имели WebFetch/arXiv** (agent-каталог снова соврал про tools — повтор `[AVOID×1]` из июля, теперь в 6× масштабе), поэтому внешняя половина `BLOCKED-INFRASTRUCTURE`. Вместо этого — дедуктивный реанализ: 9 claims оказались тавтологиями (H-B7-21/24 — буквально Lean-теорема/forward-closure; H1-VR time-reversal invariance — 5 строк из определения VR), 2 новых факта найдены в уже собранных данных (`Var(log θ/√n)∝n^-0.96` у Lovász; `K_ref` точно однородна степени 0 у Kreiss). Полный отчёт: `reports/2026-09-10-deep-external-novelty-audit.md`. **Track 1 (7 decisive-проверок, все локальные, сделаны в ту же сессию):** пересчитан Lovász slope (n≥40: ≈0, не −0.035) + явное неравенство E[θ]≥√n; K_ref-инвариантность подтверждена алгебраически и её численный разрыв на экстремальных T найден и задокументирован; исправлена «1-2 orders of magnitude» → точные 1.6-4.2 в H-B7-29; найден почти вакуумный floor-check в H-B7-31 (ROBUST-условия — 2-состояния графы); найдено и Pearl-зарегистрировано точное рациональное P(k=2)=2·P(k=1) в H-B7-26 (119/864=2×119/1728); гипотеза «chirality_excess просто переоткрывает baseline» ОПРОВЕРГНУТА корреляционной проверкой (H-B3-2); branch automorphism (H-B7-27) независимо подтверждён `pyboolnet`'s trap-space solver — verification_strength повышен medium→strong. **Track 2 (внешняя литературная проверка через WebFetch/arXiv/Semantic Scholar напрямую в основной сессии, не через агента — ЗАВЕРШЁН, 4/6 проверок).** Решающие находки: (1) arXiv:2609.04659 (Forsythe) — авторы САМИ прямой цитатой называют «smallest dimension» открытым вопросом, H-CAT37-2 бил в реальную открытую задачу; (2) arXiv:2502.16227 (Bandeira et al., companion work, найден и открыт) — Theorem 1 даёт ТОЧНО `√n ≤ E[θ] ≤ C√(n log log n)`, той же техникой (θθ̄=n + Jensen/AM-GM), опубликовано в феврале 2025 — `E[θ]≥√n` `KNOWN-BY-GENERAL-THEOREM`, НЕ собственная находка; но `Var(log θ/√n)∝n^-0.96` в этой статье не обсуждается вообще — остаётся сильнейшим живым кандидатом на новизну всего аудита; (3) DNB (PMID 22461973, открыт через PMC) — 3 критерия отслеживаются ВНУТРИ одной системы во времени, structural mismatch с H-B3-1q (сравнение MEЖДУ Peter/Paul) — НЕ переоткрытие DNB; (4) Baryshnikov 2022 (arXiv:1909.09846) — Definition 2.6 реализована в проекте корректно, Remark 2.7's предсказанный знак совпал на 2/3 озёр. Не завершены (низкий приоритет): Trefethen&Embree Ch.16 цитата, Kreiss-constant certified-accuracy алгоритмы. **[VERIFIED] §9/H-CAT31-3 (углубление главного кандидата, по прямому запросу пользователя, ЗАВЕРШЕНО):** новый Standard-Ladder эксперимент, n=32..3000 (9 точек, 40-300 реплик), pre-registered kill-criterion (CI должен содержать −1 И исключать −0.5/−2). **Результат: REJECTED для точного exponent=−1** — weighted-OLS slope=−0.9126, 95% CI=[−0.9751,−0.8501], чисто исключает −1 (не широкий неинформативный интервал). Stability-check (первая половина диапазона −0.900 vs вторая −0.897) исключает простое объяснение «finite-size коррекция к −1». Явление survives (дисперсия реально убывает степенным законом), но статус понижен с `POSSIBLE-NOVEL-SPECIAL-CASE` до `BENCHMARK-SPECIFIC-NUMERIC-RESULT` — точное число без структурного объяснения. `graph.yaml`: H-CAT31-3, статус `lead`, ребро `grounds` от H-CAT31-1 + `tested_on` к SUB-RANDOM-CIRCULANT-GRAPHS. **Честный итог всего аудита: среди ~34 проверенных claims нет ни одного подтверждённого внешне нового вклада — единственный серьёзный кандидат был испытан со всей строгостью и не выжил в чистом виде.** **CALIBRATION FIX (пользователь поймал overclaim):** формулировка «stability-check исключает finite-size correction» была сильнее данных — исправлено на «нет видимого дрейфа к −1 в диапазоне n=32..3000; простое finite-range объяснение disfavored, но асимптотика −1 за пределами диапазона НЕ исключена» (возможен `Var=C·n⁻¹·L(n)` с медленно меняющимся L(n), напр. логарифмическим). Следующий дешёвый шаг — НЕ больший sweep, а сравнение структурно-мотивированных correction-моделей на уже собранных 9 точках (не beauty contest кривых). Финальная формулировка: «robust unexplained empirical concentration law... natural n⁻¹ law falsified over the tested range».
- **[VERIFIED — 2026-09-10, ADR-122] Schema upgrade — читать вторым.** По итогам независимого аудита (context-asymmetric `Agent(analyst)`, заказан пользователем) добавлены 3 ортогональных атрибута поверх `status`: `evidence_mode` (empirical/exhaustive/deductive/formal/simulation), `verification_strength` (none/weak/medium/strong — честно снижает вес «reviewer confirmed», где это была та же модель в изолированном контексте, не другая модель/инструмент), новый тип узла `substrate` + ребро `tested_on` (делает видимой substrate-diversity: 153 узла графа концентрируются на 6 реальных субстратах). `lab_check.py` печатает substrate-diversity отчёт при каждом запуске. Retrofit ЧАСТИЧНЫЙ (15 flagship-гипотез из ~128 hypothesis/artifact узлов, честно так и помечено — см. отчёт). ADR-121's stop-rule НЕ ослаблен этим — это инфраструктура для следующего цикла, не повод его начать.
- **[2026-09-10, ADR-118 → ADR-121] CONSOLIDATION PHASE ЗАВЕРШЕНА, STOP-RULE АКТИВЕН — читать первым.** Пункты 1-2 ADR-118 выполнены: (1) B7 external novelty audit — методы вокруг H-B7-26…31 в основном устоявшиеся в литературе (не новая теория, хорошо проверенный case-study); (2) B3-1q external-data search — per-season разрез (H-B3-1r) ослабил интерпретацию H-B3-1q, красивый LEAD не выдержал робастность-проверки. Пользователь явно остановил пункт 3 (снова cross-domain/sci-hypothesis) — ADR-121. **Текущий правильный статус: НЕ «у нас ничего нет», а «есть несколько хорошо проверенных результатов, пока нет убедительно подтверждённого внешне нового открытия».** Новый цикл гипотез запускать ТОЛЬКО при появлении: (1) новой независимой модели (не Remy 2015, не Peter/Paul Lakes); (2) нового датасета (генуинно другая манипулированная/контрольная система); (3) новой теоремы/литературной щели, которую B7/B3-аудиты не нашли устоявшейся; (4) внешнего open problem с чётким structural foothold. НЕ валидное основание: «граф умеет родить ещё один H-номер». Не начинать новый `H-B*-N` без явного запроса пользователя и без одного из этих 4 условий.
- **Boundary:** Эта папка + чтение (не запись) в исходный vault `C:\Users\serge\.claude\memory\` при необходимости сверки
- **Done when:** Хотя бы один мост прошёл полный цикл kill-criterion → эксперимент → KILLED/CONFIRMED/LEAD
- **NOT NOW:** Frontier R&D / TOFT / RAF — постоянно `unverified_source` (пользователь подтвердил 2026-09-07: возможно на другой машине, доступа нет); полный Hypothesis Portfolio (128+ гипотез из ARCHCODE и др.) — отдельный, не связанный проект
















## Current Focus
**[VERIFIED — 2026-09-11, cont.] H-CAT31-3 § 6 — attempted formal proof of Efron-Stein
`O(1/n)` bound, per direct user request. HONEST OUTCOME: full proof NOT achieved.** Real
partial progress instead: derived + numerically verified (n=11 toy, `verify_lp_sensitivity_
concavity.py`) that the LP value function `V(t)` under RHS-relaxation of one generator's
constraint is concave/piecewise-linear (standard parametric-LP duality), connecting
`Delta_i theta` to LP dual variables via a tangent-line argument — confirmed real (not just
asserted): piecewise-linearity to `~1e-15`, genuine kink, `max_t V(t)` matches an
independently-computed `theta_via_lp` value to grid resolution. **Gap explicitly NOT closed:**
crude magnitude bounds only give `O(1)` per generator, not the needed `O(1/n)` — closing it
requires a concentration/RIP-type argument on the dual solution specific to the random
ensemble, not established in the primary source (arXiv:2502.16227) and equivalent to new
research, not a routine continuation. Documented as precise incomplete progress (names the
exact missing lemma), not a disguised negative result or a fabricated proof. Full writeup:
`experiments/20260910-lovasz-theta-variance-scaling-cat31-3/decision.md` § Addendum point 6.
**[VERIFIED — 2026-09-11, cont.] H-CAT31-3 mechanism addendum § 5 — density-response experiment,
independent cross-check of sensitivity, by directly varying `p` (not a within-sample
regression).** Exact symmetry `M_n(1-p)=-M_n(p)` re-derived from `theta(G)*theta(Gbar)=n`
(Lovász, pathwise) + `Gbar~G(n,1-p)`, confirmed on data (4/4 symmetry pairs within 2 SE at
n=128/512). Direct finite-difference `λ̂=(M_n(0.5+h)-M_n(0.5-h))/(2h)` came out NEGATIVE
(-2.2 to -3.3) — caught and resolved a sign confusion myself before reporting it as a
contradiction: `dD_n/dp≈-2` (the Q-proxy `D_n` decreases with density), so
`dM_n/dp≈-2·b` (b = Q-proxy regression slope) is negative too. **Magnitude cross-check: at
n=512, predicted `-2.901` vs directly measured `-2.892` (0.3% agreement); at n=128, predicted
`-2.471` vs measured `-2.433` (1.5% agreement).** Two structurally independent measurements
(within-sample proxy regression vs. direct response to varying p) now agree closely — real,
non-circular consistency evidence for the density-driven mechanism. Full writeup:
`experiments/20260910-lovasz-theta-variance-scaling-cat31-3/decision.md` § Addendum point 5.
**[VERIFIED — 2026-09-11, cont.] H-CAT31-3 mechanism addendum § 4 — prime-n generator
homogeneity, a small theorem PROVED here (not cited from external text).** Derived and
exhaustively verified (`verify_prime_isomorphism_exhaustive.py`, n=7 prime, all 8 subsets,
diff~5e-15): for prime `n`, `theta(G_S)=theta(G_{aS})` exactly for any unit `a` (graph
automorphism via vertex relabeling), and since `S -> aS` is measure-preserving under i.i.d.
Bernoulli(1/2) generator bits, `E[(Delta_i theta)^2]` is EXACTLY equal across all generator
indices `i` for prime `n` — not a heuristic. Empirical check at n=127 (prime) vs n=128
(composite), 150 reps × 7 indices, gave CV=0.231 vs 0.132 — OPPOSITE direction from the naive
prediction, but NOT a refutation: per-index SE (~15-25%) at this rep count is fully consistent
with a true CV of 0. Honest reading: the diagnostic lacks power to detect the proven identity,
neither confirms nor refutes it. Practical upshot for future work: prime n + single-index
measurement (not averaging over 3) would both remove the composite-n heterogeneity confound
and roughly halve per-replicate cost for any future Efron-Stein sensitivity sweep.
**[VERIFIED — 2026-09-11] H-CAT31-3 mechanism-level addendum (Mechanism Development Mode,
triggered by user-supplied external AI analyses, independently re-checked, NOT trusted at face
value).** Three diagnostics, all reusing the experiment's own verified substrate, none reopening
the REJECTED verdict for exponent=-1: (1) exact inequality `V_n<=2(E[theta]/sqrt(n)-1)` derived
independently from the Lovász identity + `cosh(x)>=1+x^2/2`, holds on 7/9 sweep points, 2
"violations" explained by sampling noise; (2) Q-proxy diagnostic (density-only proxy `D_n`
explains 66-86% of `Var(X_n)` across n=32..3000, not the ~100% a stronger externally-suggested
hypothesis implied); (3) single-generator sensitivity / Efron-Stein bound — the striking result:
`n^2*E[(Delta_i X)^2]` nearly IDENTICAL at n=512/1536 (60.7, 60.7) after a finite-size drop from
n=128 (84.5), and bound/measured-V_n ratio shrinks 2.57→1.67→1.27 (tightening toward 1) —
suggestive that the true asymptotic could be exponent=-1 with `-0.91` a finite-size transient,
consistent with the CORRECTED CALIBRATION's un-excluded `L(n)` alternative. **NOT confirmed at
n=3000** — extension used only 8 reps (cost-limited), SE on the key statistic is ~49% relative,
point estimate (121.4) statistically indistinguishable from continuing OR breaking the trend.
**Verdict: genuinely open, sharpened not resolved.** Concrete next decisive step named but not
run: a well-powered (not 8-replicate) single-generator sensitivity measurement at n>=3000, or a
formal proof of `E[(Delta_i theta)^2]=O(1/n)`. Literature calibration: arXiv:2502.16227's
theorem/conjecture reverified directly from LaTeX source (exact match); the "Faure sensitivity
already attempted" claim from the pasted analyses is `[WEAK]` (ResearchGate 403'd, only a search
engine's paraphrase available), explicitly not required for the math above to hold. Full writeup:
`experiments/20260910-lovasz-theta-variance-scaling-cat31-3/decision.md` § Addendum (2026-09-11).
[summarized] **[VERIFIED — 2026-09-10, ADR-120] H-B3-1r (consolidation phase, приоритет 2 — B3-1q external-data search): REJECT —...

[summarized] **B7 autonomous-mission arc (ADR-102 through ADR-116: H-B7-20..31 + Lean 4 formalization of H-B7-21) archived to `history/activeContext-archive-20260911-b7-mission.md`.** One-line each: H-B7-20 PARTIALLY-ROBUST (CyclinE1 triple-comparison closure); H-B7-21 CONFIRMED (exhaustive 35-node perturbation theorem, see Lean 4 pilot below); H-B7-22 CONFIRMED (async k*=5 threshold schedule-dependent, SCHEDULE_FRAGILE k=1..4); H-B7-23 CONFIRMED (escape frequency 6.7%->33.8%); H-B7-24 CONFIRMED (sharp point-of-no-return, CyclinE1 trigger); H-B7-25 REJECTED-partial (p21CIP 8/8, RBL2 does NOT generalize past k=2); H-B2-4 REJECTED (clean confident null, sign-change criterion was pure noise); H-B7-26 CONFIRMED (exact absorbing Markov chain escape probability, oracle 10/10); H-B7-27 CONFIRMED (branch equality = real graph automorphism via frozen EGFR_stimulus); H-B7-28 CONFIRMED (mechanism extended to full 80-condition domain); H-B7-29 CONFIRMED (FGFR3_stimulus NOT inert, contrast test); H-B7-30 CONFIRMED (exact probabilities dont rescue the large-deviation fit); H-B7-31 CONFIRMED (early-exit BFS, 84-90% savings on FRAGILE only) -- closes the ENTIRE original H-B7-26 priority list (5/5 items).
[summarized] **Lean 4 pilot (H-B7-21 formalization, ADR-105) + H-CAT31-2 (composite/prime-tail REJECTED, ADR-104) archived to `history/activeContext-archive-20260911-b7-mission.md`.**
**[VERIFIED — 2026-09-10, ADR-103] H-B7-21 (по прямой инструкции пользователя: синтез + минимальное условие, продолжать автономно до полного закрытия): CONFIRMED, замыкает всю observability/rule-perturbation под-арку B7 (H-B7-13→H-B7-21).** Часть A — общая теорема проверена ИСЧЕРПЫВАЮЩЕ по ВСЕМ 35 узлам сети (не только 3 ранее протестированных): возмущение множества single-bit правил сохраняет `PROLIFERATION_STATE`/`_2` неподвижной точкой ⟺ ни одна возмущённая строка не равна собственной входной конфигурации состояния для этого узла. 35 узлов × 2 ветки × 2984 проверки, 0 расхождений, 0 нарушений baseline fixed-point (впервые проверено сетевым образом, не только для 3 узлов вручную). Достаточность проверена и при ОДНОВРЕМЕННОМ возмущении нескольких узлов сразу (новое, за пределами H-B7-17/19/20). Часть B — синтез: RBL2 33.3% fragile, p21CIP 0%, CyclinE1 9.7% — НЕ монотонно по числу входов, явно НЕ подогнан тренд на n=3. Реальная методологическая находка: 2 reviewer-попытки подряд зависли на лимите ходов из-за заблокированного `python -c` в песочнице (не bundled-scope, как в прежних случаях) — третья попытка с явной инструкцией писать файл-скрипт прошла чисто. FL Step 8a: CONFIRMED на highest-risk узле (E2F1_high, 10 входов). `graph.yaml`: 138 узлов, 175 рёбер, `H-B7-21` статус `confirmed`. **Открытые нити (не пройдены, названы явно): расширение полной ROBUST/FRAGILE-машинерии за пределы 3 узлов; проверка асимметрии fragile-rate на бóльшем n; double-bit возмущения — вся исходная инструкция пользователя выполнена, следующий шаг не назначен, ждать нового направления.**
**[VERIFIED — 2026-09-10, ADR-102] H-B7-20 (третий и последний feedback-loop узел, CyclinE1, 32-строчное exhaustive возмущение, по явному запросу пользователя): PARTIALLY-ROBUST, замыкает тройное сравнение RBL2/p21CIP/CyclinE1 и общий принцип дестабилизации.** Реальное структурное отличие от H-B7-17/19: CyclinE1 НЕ клэмпится, орбита клэмп-фазы перестроена заново для каждого возмущения (новые функции). Substrate-проверка через ДРУГОЙ путь кода подтвердила орбиту H-B7-15 точно (7 состояний/ветвь). Результат: 28 ROBUST, 3 FRAGILE, 1 CRITERION_INVALID из 32. По прямому запросу пользователя добавлен систематический слой (не на одном отобранном случае): КАЖДАЯ fragile/invalid строка проверена H-B7-18's методологией на дестабилизацию самого аттрактора — единственная CRITERION_INVALID строка (`flip_FFTTT`) дестабилизирует аттрактор сам (обе ветви), все 3 FRAGILE строки — только-наблюдаемость. Общий принцип теперь подтверждён ТРИЖДЫ вычислительно (RBL2, p21CIP независимо перепроверен скретч-скриптом в рамках этого эксперимента, CyclinE1): дестабилизирующее возмущение узла всегда точно совпадает со строкой, соответствующей собственной входной конфигурации `PROLIFERATION_STATE` для этого узла. Отклонена (до фиксации в артефактах) ложная рабочая гипотеза «направление flip коррелирует с хрупкостью» — RBL2 добавленная строка, CyclinE1 удалённая, противоположные паттерны. Пойман и исправлен ДО запуска пробел дизайна: изначальная проверка дестабилизации не покрывала CRITERION_INVALID строки, хотя оригинальное расследование H-B7-18 было именно про CRITERION_INVALID случай RBL2 — расширено на все fragile-or-invalid строки. `graph.yaml`: 137 узлов, 172 ребра, `H-B7-20` статус `lead`, рёбра `grounds` от H-B7-15/17/18/19. **Следующий шаг (прямая инструкция пользователя): H-B7-21 — синтез sensitivity-профилей всех трёх узлов + попытка вывести минимальное необходимое/достаточное условие существования аттрактора Proliferation, продолжать автономно до полного закрытия темы.**
[summarized] **B1/B2/B3 arc (H-B3-1 through H-B3-1k, ADR-010–027) archived to `history/activeContext-archive-20260906-b1b2b3.md`**
[summarized] **[2026-09-09, продолжение] Bridge 8 (UDE identifiability ↔ PRJ-CHERNOFFPY) зарегистрирован proposed → в тот же день...

[summarized] **[VERIFIED — 2026-09-09, по прямому запросу пользователя «посмотри на 100-item каталог, какие ещё есть кандидаты»]...
[summarized] **[VERIFIED — 2026-09-10, ADR-091] Ретроскан H-CAT37-1: гипотеза Форсайта разрешена ИЗВНЕ**...

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
- [2026-09-11 11:40] `72a5afa` (local, branch `feature/h-cat31-3-lp-sensitivity-attempt` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs: activeContext.md -- record LP-sensitivity attempt, archive Lean4/H-CAT31-2 entries
- [2026-09-11 11:40] `917cf03` (local, branch `feature/h-cat31-3-lp-sensitivity-attempt` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs: H-CAT31-3 -- LP-sensitivity attempt at formal O(1/n) proof, gap explicitly named
- [2026-09-11 11:33] `5ef1e0f` (local, branch `feature/h-cat31-3-density-response` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs: activeContext.md -- record density-response addendum, archive B7 mission arc
- [2026-09-11 11:30] `1aa3393` (local, branch `feature/h-cat31-3-density-response` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-CAT31-3 -- density-response experiment, independent cross-check of sensitivity
- [2026-09-11 11:15] `2ee15a6` (local, branch `feature/h-cat31-3-prime-symmetry-theorem` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-CAT31-3 -- prime-n generator homogeneity theorem, proved and exhaustively verified
- [2026-09-11 11:02] `a572df5` (local, branch `feature/h-cat31-3-mechanism-addendum` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs: fix dangling docstring reference in check_q_proxy_diagnostic_n3000.py
- [2026-09-11 10:59] `14312da` (local, branch `feature/h-cat31-3-mechanism-addendum` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-CAT31-3 -- mechanism-level addendum (Efron-Stein sensitivity, Q-proxy, cosh bound)
- [2026-09-11 10:01] `23914c0` (local, branch `docs/h-cat31-3-calibration-fix` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): chore: activeContext.md -- record the H-CAT31-3 calibration fix
- [2026-09-11 10:00] `30dc754` (local, branch `docs/h-cat31-3-calibration-fix` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs: calibration fix -- H-CAT31-3 stability-check overclaim, user-caught
- [2026-09-10 23:27] `be1f280` (local, branch `feature/h-cat31-3-variance-scaling-deepened` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-CAT31-3 -- deepened Var(log theta/sqrt(n)) exponent check, REJECTED for -1
- [2026-09-10 22:25] `679d850` (local, branch `docs/deep-novelty-audit-track2-external-verification` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): chore: activeContext.md update -- Track 2 external verification complete
- [2026-09-10 22:24] `460b31e` (local, branch `docs/deep-novelty-audit-track2-external-verification` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs: Track 2 -- primary-source external novelty verification
- [2026-09-10 22:16] `0f55ec9` (local, branch `docs/deep-novelty-audit-track1-decisive-checks` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): chore: activeContext.md update -- deep novelty audit + Track 1 summary
- [2026-09-10 22:15] `acfe738` (local, branch `docs/deep-novelty-audit-track1-decisive-checks` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs: deep external novelty audit + 7 decisive checks (Track 1)
- [2026-09-10 18:50] `009aab2` (local, branch `docs/adr-122-evidence-mode-verification-strength-substrate` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: ADR-122 -- evidence_mode/verification_strength/substrate schema package
