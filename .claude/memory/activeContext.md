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
**[VERIFIED — 2026-09-12] H-CAT31-3 §§18-26: sharpened Poincaré ladder fully analytic through
l=5, Exam 2 PROMOTE, Exam 3 structural theorem obtained, l_eff boundedness left open.**
SESSION STOPPED HERE by explicit user instruction ("остановись здесь, зафиксируй итог").

- **§18 (l=1,2 analytic, Exam 1 PASSED):** three-term ladder bound fully layer-wise-verified,
  0 violations all 7 n. Root cause of earlier `pinv`-noise resolved via exact double-centered
  projection (`check_l2_analytic_projection.py`).
- **§19-21 (Exam 2, l=3, PROMOTE verdict):** general interior-layer `E_3(q)` formula derived
  (reuses `P_1,P_2` as generic operators applied to the raw triple indicator as target — the
  key simplification that made every later level tractable). Scaled to all 7 n via an
  algebraic reduction avoiding `(v,C(N,3))` matrices. **Four-term ladder computed and verified:
  excess growth `91.2→69.3→32.7→11.2 pp` (n=23→47) — user's own kill-or-promote threshold
  cleared. Verdict: PROMOTE, not a plateau.**
- **§22-24 (Exam 3 stages 1-3, tail concentration):** reformulated from "does `E_l` decay
  geometrically" to "`t_r:=R_r/(D_r/gamma_r)` tail-tightness". Honest finding: `t_4` INCREASES
  with `r` (expected) but DECREASES with `n` at FIXED `r=4` (`1.0000→0.8810`, n=23→47) — the
  opposite of what a naive fixed-`r` uniform bound needs. User-derived reformulation
  (independently re-verified): `l_eff(N)` via `l_eff(N+1-l_eff)=r(N+1-r)/t_r`; for fixed r=4,
  **`t_4≥c>0` uniformly REQUIRES `l_eff=O(1)`, not just `O(N)`** (any `l_eff→∞`, even
  `log log N`, forces `t_4→0`). 7-point data (`N=10..22`) cannot distinguish a finite limit
  from slow divergence — **question left explicitly OPEN, not resolved either way.**
- **§25-26 (Exam 3 stage 4-6, general E_l construction):** recursive construction generalizes
  cleanly — each level's "pure V_k basis" is built ONCE and reused as operator `P_k[g]` for
  ANY target `g` (no fresh derivation per level). Verified numerically at l=4 (0/6 boundary,
  0/16 diagonalization violations) and l=5 (0/5, 0/10) at n=23,29,31 — both first-try successes.
  **General theorem (point 26):** tight-frame identity `sum_A Z_A⊗Z_A=lambda_k·P_k` via Schur's
  lemma, valid for arbitrary k — but rests on a CITED (not independently re-derived in-session)
  representation-theory fact (irreducibility of `V_k` under the Gelfand pair `(S_N,S_q×S_{N-q})`)
  and the exact `lambda_k` constant is not symbolically derived from first principles, only
  empirically confirmed 5-for-5. Honestly scoped as structural progress, not a from-scratch
  closed-form proof.
- **What remains open, explicitly, for a future session:** (1) is `l_eff(N)` bounded for fixed
  r — the actual kill-or-promote question for the whole Johnson-ladder mechanism reaching
  `O(1/n)`; (2) independent derivation of `lambda_k` from the trace identity; (3) scaling `E_l`
  computation to `n=37-47` at `l≥4` (currently small-N-only, brute-force `(v,C(N,l))` matrices).
- Real bugs found and fixed THIS session (not hidden): single-index-vs-pair-product correlation
  bug in the first `E_3` interior-layer attempt (caught via Gram-matrix diagnostic, not just
  diagonalization agreement); an overclaim ("converges faster than geometric decay" — retracted
  after user caught that 3 ratio points starting at 0 can't establish an asymptotic rate);
  reporting habit "0/0 violations" (looks like an absent test) corrected to real denominators.
- Full writeup: `decision.md` points 18-26 (each with its own verification artifacts in
  `metrics/`), `pearl_registry/INDEX.md`.

[summarized] **B7 autonomous-mission arc (ADR-102 through ADR-116: H-B7-20..31 + Lean 4 formalization of H-B7-21) archived to...
[summarized] **[VERIFIED — 2026-09-09, по прямому запросу пользователя «посмотри на 100-item каталог, какие ещё есть кандидаты»]...

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
- [2026-09-12 20:31] `0bd89c3` (local, branch `feature/h-cat31-3-general-tight-frame-theorem` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-CAT31-3 -- general tight-frame theorem for E_l, plus l=5 numerical confirmation
- [2026-09-12 20:20] `4b33956` (local, branch `feature/h-cat31-3-general-l-recursive-e4` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): fix: H-CAT31-3 -- closest-match eigenvalue + explicit assert (reviewer P2 findings)
- [2026-09-12 20:12] `de54c35` (local, branch `feature/h-cat31-3-general-l-recursive-e4` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-CAT31-3 -- general recursive E_l construction, verified at l=4, 0 violations
- [2026-09-12 20:04] `12c90e3` (local, branch `feature/h-cat31-3-leff-boundedness-attempt` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): fix: H-CAT31-3 -- attempt to prove l_eff(N) boundedness analytically, not resolved
- [2026-09-12 19:58] `0b776cd` (local, branch `feature/h-cat31-3-effective-spectral-level` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): fix: H-CAT31-3 -- guard None-l_eff print path (reviewer P2 findings)
- [2026-09-12 19:56] `be61f21` (local, branch `feature/h-cat31-3-effective-spectral-level` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): fix: H-CAT31-3 -- correct point 23's asymptotic target before merge (user math corrections)
- [2026-09-12 19:53] `6ef84a4` (local, branch `feature/h-cat31-3-effective-spectral-level` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-CAT31-3 -- Exam 3 stage 2, effective spectral level l_eff, mixed growth-rate signal
- [2026-09-12 19:38] `db07090` (local, branch `feature/h-cat31-3-tail-concentration-exam3` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): fix: H-CAT31-3 -- structural existence check for tail_tightness (reviewer P1 finding)
- [2026-09-12 19:34] `790a67a` (local, branch `feature/h-cat31-3-tail-concentration-exam3` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): fix: H-CAT31-3 -- correct overclaim on excess-growth decay; Exam 3 stage 1
- [2026-09-12 19:11] `cca5343` (local, branch `feature/h-cat31-3-four-term-ladder` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-CAT31-3 -- four-term ladder kill-or-promote test, PROMOTE
- [2026-09-12 18:05] `9caa1f0` (local, branch `feature/h-cat31-3-exam2-e3-boundary` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): fix: H-CAT31-3 -- center z_abc explicitly (reviewer P2 finding)
- [2026-09-12 18:00] `a716009` (local, branch `feature/h-cat31-3-exam2-e3-boundary` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-CAT31-3 -- Exam 2 stage C, general interior-layer E3(q) formula verified
- [2026-09-12 17:37] `573f54d` (local, branch `feature/h-cat31-3-exam2-e3-boundary` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-CAT31-3 -- Exam 2 stage A+B, rigorous P1+P2 functions, exact E3 at boundary
- [2026-09-12 14:42] `1e2fc86` (local, branch `feature/h-cat31-3-l2-l3-ladder-analytic-fix` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): fix: H-CAT31-3 -- persist re-runnable verification for E1/E2 analytic docstring claim
- [2026-09-12 14:32] `1b1902a` (local, branch `feature/h-cat31-3-l2-l3-ladder-analytic-fix` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): feat: H-CAT31-3 -- analytic l=2/l=3 Johnson ladder, 0 numerical violations
