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
**[VERIFIED — 2026-09-11, cont.] H-CAT31-3 § 14 — density-vs-shape localization, sharpest
finding of the whole investigation (sobering, not comforting).** Decomposed
`E[delta^2] = sum_q w_q*A_q^2 + sum_q w_q*C_q` using ACTUAL Hamming-layer probability
`w_q=C(m-1,q)/2^(m-1)` across prime n=11..37 (necklace-orbit method, validated). **Density
part (`n^2*sum w_q A_q^2`) nearly flat (19.2→21.5, +12%) — genuinely `O(1)`-consistent,
matching point 5's own `A_q~4-5/n` finding. Shape part is NOT flat — grows ~6x over the same
range and essentially CATCHES UP to the density part by n=37 (21.36 vs 21.46). Shape fraction
of `E[delta^2]` rises monotonically 16%→50%, no sign of leveling off.** Precisely localizes
the `O(1/n)` obstruction to WITHIN-Hamming-layer LP-optimum heterogeneity (shape/bulk LP
geometry), not the mean single-generator response (density, well-behaved). Honest
calibration: 8 points still small for distinguishing `L(n)=O(1)` from slow growth — localizes
WHERE the question lives, doesn't resolve it. Full writeup: `experiments/20260910-lovasz-
theta-variance-scaling-cat31-3/decision.md` § Addendum point 14.
[summarized] **H-CAT31-3 §§10-13 (exact small-n enumeration, vanishing-even-levels theorem, 7th-angle verification, necklace-orbit extension) archived to `history/activeContext-archive-20260911-b7-mission.md`.** Superseded by §14 (kept above, sharpest finding: density-vs-shape localization). One-line-each: §10 exact enumeration n=9-25 (n*Var(X) initially read as stabilizing, later corrected); §11 PROVED theorem -- all even Fourier-Walsh levels vanish exactly (from antisymmetry); §12 3 external claims independently verified to machine precision (sharpened ES bound, exact prime W1=Mn(1/2)^2/4m identity, self-correction: prime-only sequence still rising not stabilizing); §13 necklace-orbit method implemented (a real bug caught by positive control, fixed, re-validated to 8.88e-14), extended exact data to n=29,31,37 -- n*Var(X) and kappa_n keep rising, no plateau.
[summarized] **H-CAT31-3 §§7-9 (exact Cauchy-Schwarz lower bound, calibration fix, LP-sensitivity/Delta_g upper-bound attempts, fourth check) archived to `history/activeContext-archive-20260911-b7-mission.md`.** Superseded by §10 (kept above, cleanest evidence: exact enumeration, no proof yet). One-line-each: §7 Var(X_n)>=M_n(1/2)^2/(4m) proved unconditionally (Cauchy-Schwarz + score-function identity), Omega(1/n) only CONDITIONAL on unproven liminf|M_n(1/2)|>0; §8 third upper-bound attempt (Delta_g_k=4cos(2pi ki/n) exact bound found+verified, still only gives O(sqrt(n)polylog(n)) not O(1/n) -- same LP-vertex-movement wall as §6); calibration fix (user caught "established" overclaim, fixed to explicitly conditional throughout); §9 fourth check (time-domain LP reformulation ruled out as an escape; own data reframed as n*(ES bound) empirical signal).
[summarized] **H-CAT31-3 mechanism investigation §§1-6 (2026-09-11: cosh bound, Q-proxy, single-generator sensitivity, prime-n homogeneity theorem, density-response, LP-sensitivity attempt) archived to `history/activeContext-archive-20260911-b7-mission.md`.** Superseded by §7 (real Omega(1/n) result, kept above) and §8 (final honest verdict, kept above); full text remains in decision.md. One-line-each: §1 mechanism addendum (cosh bound holds 7/9, Q-proxy explains 66-86% variance, ES bound tightens 2.57->1.27 at n=128/512/1536 then inconclusive at n=3000); §4 prime-n homogeneity theorem (proved+exhaustively verified, not just heuristic); §5 density-response (exact symmetry confirmed, sign-corrected cross-check with Q-proxy agrees to 0.3-1.5%); §6 LP-concavity attempt at O(1/n) upper bound (real mechanism found, verified numerically, but only gives O(1) per generator not O(1/n) -- first of 3 attempts that all hit the same wall, see §8).
[summarized] **[VERIFIED — 2026-09-10, ADR-120] H-B3-1r (consolidation phase, приоритет 2 — B3-1q external-data search): REJECT —...

[summarized] **B7 autonomous-mission arc (ADR-102 through ADR-116: H-B7-20..31 + Lean 4 formalization of H-B7-21) archived to `history/activeContext-archive-20260911-b7-mission.md`.** One-line each: H-B7-20 PARTIALLY-ROBUST (CyclinE1 triple-comparison closure); H-B7-21 CONFIRMED (exhaustive 35-node perturbation theorem, see Lean 4 pilot below); H-B7-22 CONFIRMED (async k*=5 threshold schedule-dependent, SCHEDULE_FRAGILE k=1..4); H-B7-23 CONFIRMED (escape frequency 6.7%->33.8%); H-B7-24 CONFIRMED (sharp point-of-no-return, CyclinE1 trigger); H-B7-25 REJECTED-partial (p21CIP 8/8, RBL2 does NOT generalize past k=2); H-B2-4 REJECTED (clean confident null, sign-change criterion was pure noise); H-B7-26 CONFIRMED (exact absorbing Markov chain escape probability, oracle 10/10); H-B7-27 CONFIRMED (branch equality = real graph automorphism via frozen EGFR_stimulus); H-B7-28 CONFIRMED (mechanism extended to full 80-condition domain); H-B7-29 CONFIRMED (FGFR3_stimulus NOT inert, contrast test); H-B7-30 CONFIRMED (exact probabilities dont rescue the large-deviation fit); H-B7-31 CONFIRMED (early-exit BFS, 84-90% savings on FRAGILE only) -- closes the ENTIRE original H-B7-26 priority list (5/5 items).
[summarized] **Lean 4 pilot (H-B7-21 formalization, ADR-105) + H-CAT31-2 (composite/prime-tail REJECTED, ADR-104) archived to `history/activeContext-archive-20260911-b7-mission.md`.**
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
- [2026-09-11 13:41] `c3331ea` (local, branch `feature/h-cat31-3-density-shape-localization` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs: activeContext.md -- record density-vs-shape localization, consolidate §§10-13
- [2026-09-11 13:40] `43b0f44` (local, branch `feature/h-cat31-3-density-shape-localization` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-CAT31-3 -- density-vs-shape localization, sharpest finding yet, sobering not comforting
- [2026-09-11 13:33] `931983d` (local, branch `feature/h-cat31-3-necklace-orbit-extension` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs: activeContext.md -- record necklace-orbit extension and the bug it caught
- [2026-09-11 13:33] `8a8058c` (local, branch `feature/h-cat31-3-necklace-orbit-extension` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-CAT31-3 -- Hamming-layer decomposition + necklace-orbit extension to n=29,31,37
- [2026-09-11 13:21] `393f855` (local, branch `feature/h-cat31-3-seventh-angle-verified` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs: activeContext.md -- record verified 7th angle, self-correction to §10
- [2026-09-11 13:21] `c51bccd` (local, branch `feature/h-cat31-3-seventh-angle-verified` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-CAT31-3 -- verified 3 external claims: sharpened ES bound, exact prime W1 identity, calibration correction
- [2026-09-11 12:59] `28c555c` (local, branch `feature/h-cat31-3-exact-walsh-decomposition` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs: activeContext.md -- record the vanishing-even-Fourier-levels theorem
- [2026-09-11 12:59] `44473ab` (local, branch `feature/h-cat31-3-exact-walsh-decomposition` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-CAT31-3 -- PROVED theorem: all even-degree Fourier-Walsh weights of X_n vanish
- [2026-09-11 12:46] `3122f0f` (local, branch `feature/h-cat31-3-exact-enumeration-small-n` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs: activeContext.md -- record exact enumeration finding, consolidate H-CAT31-3 §§7-9
- [2026-09-11 12:45] `c8230eb` (local, branch `feature/h-cat31-3-exact-enumeration-small-n` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-CAT31-3 -- exact (noise-free) enumeration at small n, 5th angle on O(1/n)
- [2026-09-11 12:36] `ae0ff4d` (local, branch `feature/h-cat31-3-fourth-upper-bound-check` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs: activeContext.md -- record fourth upper-bound check (empirical support, still not proven)
- [2026-09-11 12:36] `b281288` (local, branch `feature/h-cat31-3-fourth-upper-bound-check` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs: H-CAT31-3 -- fourth upper-bound check, per user request to keep trying
- [2026-09-11 12:31] `d29baa7` (local, branch `docs/h-cat31-3-conditional-calibration-fix` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs: activeContext.md -- record the Omega(1/n)-is-conditional calibration fix
- [2026-09-11 12:31] `5bf591d` (local, branch `docs/h-cat31-3-conditional-calibration-fix` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs: H-CAT31-3 -- calibration fix, Omega(1/n) is conditional not established
- [2026-09-11 12:24] `aefb1ea` (local, branch `feature/h-cat31-3-delta-g-final-attempt` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs: activeContext.md -- record final upper-bound verdict, consolidate H-CAT31-3 §§1-6
