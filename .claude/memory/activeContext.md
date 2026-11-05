# activeContext.md — Y-17 100 gipotez

## Current Focus

- **[2026-11-03] H-CAT56-2 phase4: independent audit of V5.1 finished, verdict VERIFIED-CONDITIONAL** (not human-refereed; no registry status changed). Record: `experiments/20261028-h-cat56-2-phase4/audit_v51/AUDIT_REPORT_V51.md`, ledger row 2026-11-03. Next step is an external human reader for lemma A1 (`A1_CHECK.md`) and PROOF_MAP rows 3-4, not a V5.2. Owner decisions open: freeze D as a rational file (would be V5.2), commit/push of the 24 modified + untracked files in this tree, whether to register phase4 as its own node. Push/commit status: use `digest.py`, not this line.

- **[2026-10-14] Memory audit review state:** reviewer iteration 1 NEEDS_WORK (fixed), iteration 2 NEEDS_WORK (P1 N1 dated cap-pointer flipped newest-first detection; fixed in `2176d37`, regression test added), iteration 3 (final, cap 3) LGTM (P2 residual: pointer count includes old pointers; nothing lost). Full results: `tooling-eval/memory-audit-2026-10-14/REPORT.md`.
- **[2026-10-14 RECONCILIATION — generated state beats written state.]** Push/publish/commit status and registry counts are no longer kept here as hand-written claims: 3 of them were false within 17 days (push status of `25776d4`, MathOverflow publication, the hooks-fix commit) and one superseded not-sent line survived next to the newer sent line. Current state = `python tooling-eval/memory-audit-2026-10-14/digest.py` (derived from git/gh/files). Work since 2026-09-27 (git log): `edc14e7` round 1 of the sequential autonomous run on five audited open problems (#30, #11, #1, #5, #17); `84950a6` round 2 on #30, #1, #11 (no LEAD); `1453996` protocol H-YBE-C3-TWIN-001. Evidence: `tooling-eval/memory-audit-2026-10-14/REPORT.md`.
- **[2026-10-14] OPEN owner decisions from the memory audit** (nothing global was changed): apply `tooling-eval/memory-audit-2026-10-14/proposed/pre_compact.diff` (+ the same patch in `claude-cod-top-2026-src`), digest-first in `session_start.py` (opt-in), fix the two lost underscores in the live MO post, commit the canonical untracked `outreach/` files, push. Details and evidence: `tooling-eval/memory-audit-2026-10-14/REPORT.md`, `tooling-eval/memory-audit-2026-10-14/proposed/README.md`.
- **[2026-10-13]** Round 1 of the sequential autonomous run on five audited open problems (#30, #11, #1, #5, #17) is finished, no LEAD. REJECT: polynomial decimation on carpet graphs (H-CARPET-1). Reproductions: H-COXETER-1 (56 classes, dims 4,5,6,7,11), H-DDEQ-1. REPEAT: H-LUMCHUA-1 (Huan-Yang 3 cycles reproduced, no 4), H-YBE-1 (two weak-charge candidates, novelty unknown). Open: Q-ROBERTS-D4-DISCREPANCY. Details: `experiments/20261003-*/decision.md` + `skeptic_verdict.md`, `00-catalog/Список 50 задач — глубокий аудит ТОП-5...md`, graph nodes `H-*`, ledger section "Автономный раунд 1". Round 2 (2026-10-13, folders `experiments/20261013-*`, committed separately) finished, no LEAD. #30: REPEAT, cycle counter fixed (3 cycles on HY/FPTT21/GRS), none with 4, counts are lower bounds only (verifier found k stratification wrong in 38%). #1: Q-ROBERTS-D4-DISCREPANCY RESOLVED, PA/PB equal P_{7,1}/P_{7,2} of Ma-Zheng 2401.13698, Roberts list is incomplete; survey `4..9,13` vs primary `<=11` still open (Tumarkin Tables 4/5 unread). #11: candidate idx 88 ALREADY_KNOWN (Hietarinta 1993 Sec 2.1.1), idx 101 = exact family F(e,u,v), not in the H-CYBE-002 shift family nor in Hietarinta 1993, novelty vs wider literature unverifiable.
- **[2026-10-04]** H-CYBE-003 jet check, status unchanged: at `21 R_0` the order-2 and order-3 obstruction ideals on the 11-dimensional kernel are zero. Naive `Y=0` cubic leaves the image (augmented rank 71). One linear component. `experiments/20261003-c-ybe-001/research/obstruction_orders.md`.
- **[2026-10-03]** H-CYBE-001 KILLED: four-ansatz search found no new invertible vertex-QYBE matrix. Exact certificates for I, P, diagonals, HMR vertex images, Jimbo q=2, and the non-SCC Gaussian in Q(ω). `experiments/20261003-c-ybe-001/research/decision.md`.
- **[2026-10-03]** H-CYBE-002 CONFIRMED on the narrow claim only: the 5-parameter monomial shift solves the vertex equation, witness commutant rank 8, no product eigenvector. World novelty UNKNOWN. Census 73 / 29 / 19. `experiments/20261003-c-ybe-001/research/decision_monomial.md`.
- **[2026-10-03]** H-CYBE-003 CONFIRMED: at the witness, dim ker of the 729×81 linearization is 11 and equals family+GL_3. Coboundary invariants (C, AE, AD/B), scale-free pair (AE/C^2, AD/(BC)). `experiments/20261003-c-ybe-001/research/decision_moduli.md`.
- **[2026-10-03]** TOP-1: ZIP re-verified, not handed (`U3_OWNER_ACTION.md` receipt; sha256 `2b425b7d…c57a`, 12839 bytes). TOP-2: Nurdin Condition 3 is not dim V⊥. Exact on seed 701082: Condition 2 holds, common kernel rank 0. Alignment search numerical only (floor ≈ 0.093), not a second certificate. Note: `experiments/20260920-h-cat56-2-verification-gates/NURDIN_COND3_2026-10-03.md`. H-CAT56-2 status unchanged. No resend.
- **[2026-09-27 CURRENT PLAN — READ THIS FIRST.]** Canonical: `outreach/CURRENT_PLAN_2026-09-27.md`. Wait U2 (email SENT 2026-09-23, no resend, classify via `PREREG_criteria.md`, log `U2_WAIT_LOG.md`). Optional U3: owner hands ZIP per `U3_OWNER_ACTION.md` — not done. No new H-id, no 463/21 recompute, no H-CAT31-3 active-search revival (node stays `lead`; POL subtree parked). Silence until ~2026-10-23 ≠ novelty. LAB.md §6 updated to this, not the 2026-09-06 archive.
- **[2026-09-27] `outreach/lemma_blind_packet.md` v3 — real gap fixed, ready for a genuinely independent reviewer, not yet sent.** Untrusted external review (independently re-derived before accepting) caught a real formal gap in v2 step 5: separate nonvanishing of N and each m_l does not give one common witness point — fixed with a product argument (see `lemma_blind_review_record.md` addendum). Same 2026-09-20 same-model pass had said `NO-GAP-FOUND` and missed it — second in-project case (after H-CAT31-3 Point 47→48) of the review layer itself failing, not the claim. Packet also renamed away from "lifting" (Hensel-lifting connotation is wrong; the real structure is a finite-field non-vanishing witness). Committed `25776d4`, pushed (and `de046fb`; verified 2026-10-14 with `git branch -r --contains 25776d4` -> origin/feature/small-exact-instance). MathOverflow question PUBLISHED by the owner 2026-09-27 (https://mathoverflow.net/questions/515586; 0 answers, 56 views on 2026-10-14). Record and one OPEN defect (underscores lost in `Q_{ij}` and `\sum_{a=1}^{2}` in the live source) are in `outreach/MO_QUESTION.md`.
- **[2026-09-25, H-CAT56-2, waiting on U2/U3]** While waiting for the authors: (a) Nurdin arXiv:2402.11567 v5 and withdrawn 2405.01471 read directly (page images); a wrong line in our own novelty_audit.md ("Nurdin says PCC not sufficient") withdrawn, no prior PCC-holds/not-saturable example found, still WEAK; (b) `experiments/20260925-h-cat56-2-rank-family`: F_p certificates for r=4 (d=31,s=13 -> dimV_perp 30) and r=5 (d=41,s=14 -> 40), 7 of 10 registered configs matched; the 3 above-s* controls failed as registered (my pre-registration error: QFIM singular by counting, amended in writing, the amended match is forced not independent); independent reviewer NEEDS_WORK P2 addressed, status PARTIALLY_SUPPORTED not PROMOTE; closed form min_s LB = r^2+ceil(2kr/(r^2+1))+1 exact for k>=r (computation); local note draft only. Existence-level breadth, same lab, lifting lemma unreviewed. No status change, no push of this work yet, no resend.
- **[2026-09-22 evening CHECKPOINT — H-CAT56-2; demoted 2026-10-14: superseded by the 2026-09-27 CURRENT PLAN.]** Frozen status: *exact counterexample package internally certified; portability passed via independent local reimplementation; theorem-chain read and consistent; novelty and external reproduction unresolved.* (`outreach/CHECKPOINT_FREEZE_2026-09-22.md`). **Full multi-day handoff for next agent:** `outreach/HANDOFF_2026-09-20_to_2026-09-22.md`. Three gates stay separate — object math ≠ portability ≠ novelty. Primary residual risk = theorem-context / prior art, not “is 463 wrong?”. Ordered next: (1) hand ZIP + `THIRD_PARTY_BRIEF.md` (discrepancy-first, no expected 463/21); (2) 24h cooling-off → send DRAFT-v2 per checklist (user prose needs must-fix on “general insufficiency” attribution); (3) **no new internal experiments** until U2/U3 signal. Email NOT SENT. [SUPERSEDED 2026-09-23: email SENT, see the 2026-09-23 entry below] Do not revive H-CAT31-3.
- **[2026-09-23 later, Tracy Critical Path executed: infra fixes pushed + two scoping ADRs, no science touched.]** External audit (see the SENT-email row below) also found two real lab-infrastructure bugs (`caps.py` uncaught `ValueError` on machines with <24 CPUs; `lab_check.py` INV1 silently accepting `kill_criterion: null` via `str(None)="None"`), both fixed + regression-tested (`1dcde4c`, 19/19 tests) and pushed. Two larger findings scoped, not yet executed (`ADR-124`/`ADR-125` in `decisions.md`, commit `8aef394`): rechecked the test-isolation gap's real size directly (`grep -rln "cmd_run()" tests/*.py` = 35 files, not the 3 the audit named; 1 already has the working donor pattern, 34 are candidates, spot-checked 10 more with zero isolation guards) and decided to split the `grounds` edge type (evidential dependency vs. design provenance) before any `INV3` widening. Explicitly NOT done: the 34-file rollout itself, the edge retyping, `testpaths` inclusion of `experiments/**` (reason for its original exclusion not yet established). H-CAT56-2 outreach state (U1/U2/U3, cooling-off, SENT) untouched by any of this.
- **[2026-09-23, EMAIL SENT — H-CAT56-2 Channel A closed as an owner action, U2 clock started.]** Owner sent the author email themselves ([owner-email-redacted] → Jing Yang, Cc Imai/Pezzè, 10:38), outside this session's tools. Exact text + diff against the reviewed v4: `outreach/2026-09-23-authors-email-SENT.md`. Before send: v3 got a context-blind skeptic pass (verdict SEND-WITH-EDITS, 7 required fixes: Eq.(16) hedge, local-vs-external-implementation disclosure, a genuine positive control on the load-bearing rank step via the paper's own LMCC example, question 1 spelled out, unitary-conjugation parametric-family sentence, I/we cleanup, search-selection disclosed, softened subject), applied as v4 and committed as an outreach freeze (`a21a1b5`). The owner's final sent text rewrites v4's wording but preserves every required fix, in places more precisely than v4 (e.g. the Eq.(16) hedge and the normalization note). 30-day clock for U2 outcomes (`outreach/PREREG_criteria.md`) starts 2026-09-23. Status: `SCIENCE: READY FOR AUTHOR INQUIRY (unchanged)`, `NOVELTY (U2): UNRESOLVED, awaiting reply`, `EXTERNAL HUMAN REPRODUCTION (U3): OPEN`, `EMAIL: SENT`. No resend, no new recomputation of 463/21 — next action only on an actual reply or via U3's third-party brief.
- **[2026-09-22 later, trajectory-lab decision — staged parallelism, stop condition reached.]** Deep-mode-with-early-stop run in the Cursor session (not this session's skill catalog) formalized the same freeze as a branching decision (hand-ZIP / send-email / staged-parallelism / more-compute, against WORLD RESPONSEs) and named the Minimum Distinguishing Future explicitly: a material discrepancy from a third party BEFORE the send gate (not "no reply yet", not "recomputed 463 again"). Decision: staged parallelism — hand the ZIP now, let the existing 24h cooling-off run in parallel, send only if no material blocker surfaces by the gate; then stop, since the next state depends on an external observation. This session's own addition: re-verified `outreach/independent-repro-bundle-701082.zip` byte-for-byte against the unpacked folder after the two 2026-09-22 commits — no drift, 9/9 shared files identical. No science changed. `tooling-eval/LEDGER.md` row appended.
- **[2026-09-17, H-CAT31-3 Points 77-89 — long proof-attempt + measurement window on `(POL)`/`F4rel` for `CV²(y*)`; PARKED active search — do not restart without revival condition.]** Context: `(POL): sup_n E‖x*‖²<∞`, reduced (Point 85, exact KKT identity `s=2Q+1` non-degenerate-vertex support size) to `E[CV²(y)]=O(1)`. Four proof ROUTES attempted this window, all genuinely tried (not just cited) and all KILLED with a precise, quantified reason, not vague failure: (1) direct Talagrand transfer from Arora-Bhaskara's i.i.d.-edge technique — killed Point 81, circulant graphs lack the `Θ(n²)`-independent-bits structure the technique needs (re-confirmed independently Point 87§4A by two research agents); (2) uncertainty-principle-on-supports — killed Point 85, saturated with zero slack; (3) Young's/sup-norm convolution bounds on `F4rel` — killed Point 86, one reproduces the trivial bound exactly, the other's gap widens with `n`; (4) KKT/argmin-stability via LP non-degeneracy margins (`boyko-specialist`'s suggestion) — killed Point 88 after finding its cited source (Escande arXiv:2304.00809) was misattributed (real paper, wrong technique) and finding zero correlation between vertex margins and `CV²`, a result that itself SURVIVED a real adversarial skeptic pass testing 3 alternative explanations.
- **[VERIFIED-COMPUTATION, Point 87, the load-bearing measurement chain this window] `CV²(y*)` measured across 6 points, `n=127→8009`, up to 300 reps each (fewer at largest `n` — LP solve cost grew from `~0.07s`/instance at `n=509` to `~15-18min`/instance at `n=8009`, a canonical-code `45s` time-limit had to be worked around with a local no-timelimit wrapper, never touching Codex's read-only `CertificateLP`).** Two separable findings, corrected TWICE by real skeptic passes before reaching their final form (see `decision.md` Point 87 §4E-4I for the full, honest before/after): (a) **dispersion of `CV²` across independent instances shrinks as the ORDINARY, trivial `n^{-1/2}` CLT-type rate** — not a mysterious `-0.53` law as a first draft claimed; that apparent deviation from `-0.5` is entirely `mean(CV²)`'s own separate drift, confirmed via an exact algebraic decomposition (`slope(std)-slope(mean)=slope(CV_of_CV2)`, verified to 4 decimals); this dispersion law holds cleanly over about one decade (`n≈500-4000`) but is REJECTED (`p=0.0017`) across the full `127-8009` range once the endpoints are included. (b) **`mean(CV²)` is genuinely, significantly increasing with `n`** (`0.987→1.050` from `n=127→8009`, `9σ`+ from `1` at the largest `n`'s) — real, not noise — but whether it converges to a constant (`≥~1.09-1.13` at 1-2σ, no upper bound established) or grows without bound is **UNRESOLVED and likely UNRESOLVABLE within this `n`-range**: a 5-model comparison (Point 87§4I) found the candidate functional forms (log-linear, log-log, `n^{-1/4}`, `1/ln n`, `n^{-1/2}`) are nearly collinear over `n∈[127,8009]` (`|corr|` up to `0.996`), so model selection there is close to uninformative, and — critically — whichever model "wins" flips entirely depending on whether the single point `n=127` (already independently flagged, twice now, as the one point driving nearly all discrimination and a likely pre-asymptotic outlier) is included or excluded.
- **[VERIFIED-COMPUTATION, Point 89] A second, independent attempt at explaining `mean(CV²)`'s drift — the "D2" pair-weight `Dirichlet(2,...,2)` heuristic (imported from an earlier, different project branch; the user explicitly disclosed the provenance gap mid-session per Gate 1 discipline, closed here) — does NOT explain it either, but MORE importantly turned out to be algebraically CIRCULAR with the already-open `mean(CV²)` question: `R=(2-μ_D2)+(CV²-1)` exactly, so this residual test is the SAME open question in different notation, not independent evidence. A first-draft "33σ, residual converges to ≈0.085" headline was WITHDRAWN (not merely caveated) after a real skeptic pass found the specific functional form fit (`1/Q`) actively contradicts D2's own algebra (`y0·√Q≈0.5` is empirically constant, meaning the model's own leading correction is `Q^{-1/2}`, not `Q^{-1}`) and that alternate, equally-natural forms give an asymptote CONSISTENT WITH ZERO. What survives: `R>0` significantly at every tested `n` (D2 alone doesn't fully explain the energy) — a real but narrow qualitative finding.

[summarized] - **[METHODOLOGY LESSON, `[REPEAT]`-worthy — happened ~9 times this window, not once]: every substantive numeric...

## Scope Fence
- **[archived 2026-10-14]** 11 verbose H-CAT31-3 entries (Points 57-64, 2026-09-14/15; status of that node unchanged) moved VERBATIM to `.claude/memory/history/activeContext-archive-2026-10-14.md`; full record also in `experiments/20260910-lovasz-theta-variance-scaling-cat31-3/decision.md`.
- **Goal:** [PLAN, не факт] Оценить и начать проверку cross-domain мостов между каталогом ~141 открытых научных задач и реальными проектами (H-7 chromatin, ChernoffPy, May 1972)
- **[2026-09-09, ADR-087] Scope расширен пользователем явно:** пятый источник гипотез — сам 100-item каталог напрямую, без требования тематической связи с исходными 4 якорями. Не отменяет исходные якоря, добавляет к ним.
- **[VERIFIED — 2026-09-10] Deep external novelty audit — читать вторым (после ADR-121, перед ADR-122).** По прямому запросу пользователя запущены 6 параллельных `Agent(analyst)` по кластерам (Boolean network dynamics/control, Boolean structural/canalization, Forsythe, transient growth/Kreiss, TDA lakes, Lovász theta), каждый проверял ~33 сильных claim'а на 10 возможных отношений к внешней литературе (special case/counterexample/known-by-theorem/etc). **Критическая находка: все 6 агентов не имели WebFetch/arXiv** (agent-каталог снова соврал про tools — повтор `[AVOID×1]` из июля, теперь в 6× масштабе), поэтому внешняя половина `BLOCKED-INFRASTRUCTURE`. Вместо этого — дедуктивный реанализ: 9 claims оказались тавтологиями (H-B7-21/24 — буквально Lean-теорема/forward-closure; H1-VR time-reversal invariance — 5 строк из определения VR), 2 новых факта найдены в уже собранных данных (`Var(log θ/√n)∝n^-0.96` у Lovász; `K_ref` точно однородна степени 0 у Kreiss). Полный отчёт: `reports/2026-09-10-deep-external-novelty-audit.md`. **Track 1 (7 decisive-проверок, все локальные, сделаны в ту же сессию):** пересчитан Lovász slope (n≥40: ≈0, не −0.035) + явное неравенство E[θ]≥√n; K_ref-инвариантность подтверждена алгебраически и её численный разрыв на экстремальных T найден и задокументирован; исправлена «1-2 orders of magnitude» → точные 1.6-4.2 в H-B7-29; найден почти вакуумный floor-check в H-B7-31 (ROBUST-условия — 2-состояния графы); найдено и Pearl-зарегистрировано точное рациональное P(k=2)=2·P(k=1) в H-B7-26 (119/864=2×119/1728); гипотеза «chirality_excess просто переоткрывает baseline» ОПРОВЕРГНУТА корреляционной проверкой (H-B3-2); branch automorphism (H-B7-27) независимо подтверждён `pyboolnet`'s trap-space solver — verification_strength повышен medium→strong. **Track 2 (внешняя литературная проверка через WebFetch/arXiv/Semantic Scholar напрямую в основной сессии, не через агента — ЗАВЕРШЁН, 4/6 проверок).** Решающие находки: (1) arXiv:2609.04659 (Forsythe) — авторы САМИ прямой цитатой называют «smallest dimension» открытым вопросом, H-CAT37-2 бил в реальную открытую задачу; (2) arXiv:2502.16227 (Bandeira et al., companion work, найден и открыт) — Theorem 1 даёт ТОЧНО `√n ≤ E[θ] ≤ C√(n log log n)`, той же техникой (θθ̄=n + Jensen/AM-GM), опубликовано в феврале 2025 — `E[θ]≥√n` `KNOWN-BY-GENERAL-THEOREM`, НЕ собственная находка; но `Var(log θ/√n)∝n^-0.96` в этой статье не обсуждается вообще — остаётся сильнейшим живым кандидатом на новизну всего аудита; (3) DNB (PMID 22461973, открыт через PMC) — 3 критерия отслеживаются ВНУТРИ одной системы во времени, structural mismatch с H-B3-1q (сравнение MEЖДУ Peter/Paul) — НЕ переоткрытие DNB; (4) Baryshnikov 2022 (arXiv:1909.09846) — Definition 2.6 реализована в проекте корректно, Remark 2.7's предсказанный знак совпал на 2/3 озёр. Не завершены (низкий приоритет): Trefethen&Embree Ch.16 цитата, Kreiss-constant certified-accuracy алгоритмы. **[VERIFIED] §9/H-CAT31-3 (углубление главного кандидата, по прямому запросу пользователя, ЗАВЕРШЕНО):** новый Standard-Ladder эксперимент, n=32..3000 (9 точек, 40-300 реплик), pre-registered kill-criterion (CI должен содержать −1 И исключать −0.5/−2). **Результат: REJECTED для точного exponent=−1** — weighted-OLS slope=−0.9126, 95% CI=[−0.9751,−0.8501], чисто исключает −1 (не широкий неинформативный интервал). Stability-check (первая половина диапазона −0.900 vs вторая −0.897) исключает простое объяснение «finite-size коррекция к −1». Явление survives (дисперсия реально убывает степенным законом), но статус понижен с `POSSIBLE-NOVEL-SPECIAL-CASE` до `BENCHMARK-SPECIFIC-NUMERIC-RESULT` — точное число без структурного объяснения. `graph.yaml`: H-CAT31-3, статус `lead`, ребро `grounds` от H-CAT31-1 + `tested_on` к SUB-RANDOM-CIRCULANT-GRAPHS. **Честный итог всего аудита: среди ~34 проверенных claims нет ни одного подтверждённого внешне нового вклада — единственный серьёзный кандидат был испытан со всей строгостью и не выжил в чистом виде.** **CALIBRATION FIX (пользователь поймал overclaim):** формулировка «stability-check исключает finite-size correction» была сильнее данных — исправлено на «нет видимого дрейфа к −1 в диапазоне n=32..3000; простое finite-range объяснение disfavored, но асимптотика −1 за пределами диапазона НЕ исключена» (возможен `Var=C·n⁻¹·L(n)` с медленно меняющимся L(n), напр. логарифмическим). Следующий дешёвый шаг — НЕ больший sweep, а сравнение структурно-мотивированных correction-моделей на уже собранных 9 точках (не beauty contest кривых). Финальная формулировка: «robust unexplained empirical concentration law... natural n⁻¹ law falsified over the tested range».
- **[VERIFIED — 2026-09-10, ADR-122] Schema upgrade — читать вторым.** По итогам независимого аудита (context-asymmetric `Agent(analyst)`, заказан пользователем) добавлены 3 ортогональных атрибута поверх `status`: `evidence_mode` (empirical/exhaustive/deductive/formal/simulation), `verification_strength` (none/weak/medium/strong — честно снижает вес «reviewer confirmed», где это была та же модель в изолированном контексте, не другая модель/инструмент), новый тип узла `substrate` + ребро `tested_on` (делает видимой substrate-diversity: 153 узла графа концентрируются на 6 реальных субстратах). `lab_check.py` печатает substrate-diversity отчёт при каждом запуске. Retrofit ЧАСТИЧНЫЙ (15 flagship-гипотез из ~128 hypothesis/artifact узлов, честно так и помечено — см. отчёт). ADR-121's stop-rule НЕ ослаблен этим — это инфраструктура для следующего цикла, не повод его начать.
- **[2026-09-10, ADR-118 → ADR-121] CONSOLIDATION PHASE ЗАВЕРШЕНА, STOP-RULE АКТИВЕН [demoted 2026-10-14: порядок чтения теперь задаёт CURRENT PLAN 2026-09-27].** Пункты 1-2 ADR-118 выполнены: (1) B7 external novelty audit — методы вокруг H-B7-26…31 в основном устоявшиеся в литературе (не новая теория, хорошо проверенный case-study); (2) B3-1q external-data search — per-season разрез (H-B3-1r) ослабил интерпретацию H-B3-1q, красивый LEAD не выдержал робастность-проверки. Пользователь явно остановил пункт 3 (снова cross-domain/sci-hypothesis) — ADR-121. **Текущий правильный статус: НЕ «у нас ничего нет», а «есть несколько хорошо проверенных результатов, пока нет убедительно подтверждённого внешне нового открытия».** Новый цикл гипотез запускать ТОЛЬКО при появлении: (1) новой независимой модели (не Remy 2015, не Peter/Paul Lakes); (2) нового датасета (генуинно другая манипулированная/контрольная система); (3) новой теоремы/литературной щели, которую B7/B3-аудиты не нашли устоявшейся; (4) внешнего open problem с чётким structural foothold. НЕ валидное основание: «граф умеет родить ещё один H-номер». Не начинать новый `H-B*-N` без явного запроса пользователя и без одного из этих 4 условий.
- **Boundary:** Эта папка + чтение (не запись) в исходный vault `C:\Users\serge\.claude\memory\` при необходимости сверки
- **Done when:** Хотя бы один мост прошёл полный цикл kill-criterion → эксперимент → KILLED/CONFIRMED/LEAD
- **NOT NOW:** Frontier R&D / TOFT / RAF — постоянно `unverified_source` (пользователь подтвердил 2026-09-07: возможно на другой машине, доступа нет); полный Hypothesis Portfolio (128+ гипотез из ARCHCODE и др.) — отдельный, не связанный проект






























































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
[summarized] - [2026-11-01 19:58] `ff8d01f` (local, branch `research/h-cat56-2-cfim-convention` -- may be replaced if this branch...

- [2026-10-14 20:28] `ad0598c` (local, branch `research/syn-h1-rstat-memory` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs(syn-h1): state scope of inference and mark secondary findings as INFERRED
- [2026-10-14 20:26] `b3b5c1d` (local, branch `research/syn-h1-rstat-memory` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): research(syn-h1): S1-S4 result for r-statistic memory-graph poisoning detector -> REJECT (C1 failed)
- [2026-10-14 19:52] `730b778` (local, branch `research/syn-h1-rstat-memory` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs(syn-h1): addendum A1 to pre-registration (after S2 + review, before any S3/S4 run)
- [2026-10-14 19:37] `62660d1` (local, branch `research/syn-h1-rstat-memory` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs(syn-h1): pre-register r-statistic memory-graph poisoning detector (S0, before any real-data run)
- [2026-10-14 14:13] `854a257` (local, branch `feature/small-exact-instance` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): docs(memory-audit): record review iteration 3 (LGTM) in report and activeContext
- [2026-10-14 14:06] `b69d318` (local, branch `feature/small-exact-instance` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): research(memory-audit): patch E1-E7, remediation, digest, final report (before/after)
- [2026-10-14 13:27] `c703c93` (local, branch `feature/small-exact-instance` -- may be replaced if this branch is later merged via squash or rebase; check that branch's PR/merge for the surviving hash if this one becomes unresolvable): research(memory-audit): measurement harness + BEFORE results (compaction replay, state claims, integrity, mutation control)

- 2026-10-14 [WS: ybe-c3-twin] Коммит 1453996: протокол `experiments/20261014-ybe-c3-twin-exclusion/PROTOCOL.md` + пилот P12 (ранг 18,18,18,18, класс A) + узел H-YBE-C3-TWIN-001 в graph.yaml + строки LEDGER. Блокер: нет списка 38 простых с подтверждённым происхождением; девять компонент в репозитории не подтверждены (LAB.md: шесть = нижняя оценка). Не закоммичено: этот файл.

- 2026-11-01 [WS: h-cat56-2-phase4] Веха сохранена: коммиты f0c6df5, 7711489 (локально, без push). Не закоммичено: NOVELTY_MATRIX, FINAL_CONSISTENCY, review_package/SHA256SUMS, FULL_RESULTS_AUDIT/REGISTER_VERIFIED, composite_rank_check, письмо v3. Аудит 64 пунктов: 33/20/6/5, исходный реестр ChatGPT не найден (OB-1). Сводка: vault projects/Y-17/H-CAT56-2 — веха phase4 2026-11-01. Письмо Нурдину v3 не отправлено.

- 2026-11-01 [WS: h-cat56-2-phase4] Коммит b7ed3a9 (локально, без push): OB-1 закрыт (сверка 44 пунктов реестра ChatGPT: 28/12/3/1/0), FULL_RESULTS_AUDIT и REGISTER_VERIFIED, поправки NOVELTY_MATRIX (2405.01471 отозвана; у Suzuki проверено только уравнение (104), лемма 4.4 и D-инвариантность нет, OB-8). Проверки: ruff чист, 258 тестов без Chernoff, ревьюер LGTM 3/3. Не вошло: черновики письма Нурдину v2/v3 (не отправлены), *.bak-*, o3_v3/records, pkl.

- 2026-11-01 [WS: h-cat56-2-phase4] Владелец ОТПРАВИЛ Нурдину ответ (контраст S+/S-, 120 пар, ранги 261/264/399, признание, что недостаточность PCC известна). Текст дословно в vault correspondence/nurdin-2026-11-01-email-SENT.md. Обещана обновлённая записка (с оговорками: матричная CFIM, D1, F_U, θ=0, computer-assisted). Ждём ответа; контрольная дата 2026-11-08 [ПРЕДЛОЖЕНИЕ]. Открыто: OB-2 (PDF поправки), OB-3 (его условия (1),(2prime) к S+/S-). Черновики v2/v3 заменены отправленным текстом.

- 2026-11-01 [WS: h-cat56-2-phase4] Черновик обновлённой записки Нурдину: review_package/TECHNICAL_NOTE_SUBSET_CONTRAST_DRAFT_2026-11-01.md (не отправлен, не в git; скептик без контекста: P1 нет, P2 исправлены). Новое: резюме поправки Нурдина прочитано (OpenAlex), dim V-perp для подмножеств 175 (S+) и 172 (S-), ранги 261/264 по модулю двух простых (нижняя оценка) и через SVD (novelty_checks/obs2_subset_dims.py). Не закоммичено: OB1 addendum, SHA256SUMS, obs2_subset_dims.*, черновик записки.

- 2026-11-01 [WS: h-cat56-2-phase4] Коммит 995d03e (локально, без push): obs2_subset_dims (21/175/172), дополнение к OB1 (поправка Нурдина прочитана), черновик записки TECHNICAL_NOTE_SUBSET_CONTRAST_DRAFT (не отправлен). 258 тестов, ревьюер LGTM. В git теперь и черновик записки: при будущем push репозиторий публичный, решение владельца.
- **[2026-11-01] Private material untracked** (commit d7722c8, local, no push): 10 letter/draft files removed from git index (files kept on disk), private patterns added to .gitignore. Old copies still in history and on origin/feature/small-exact-instance and origin/feature/outreach-drafts (owner decision pending on history rewrite). Rule: ~/.claude/rules/private-material-never-in-repo.md. No .py changed in this commit; commit-test-gate warning is generic.
