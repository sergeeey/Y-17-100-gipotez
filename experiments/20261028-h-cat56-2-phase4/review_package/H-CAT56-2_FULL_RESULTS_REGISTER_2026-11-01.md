# H-CAT56-2 — полный реестр результатов исследования

Дата фиксации: 2026-11-01. Основание: отчёты Claude Code, Codex и переписка в текущем диалоге. Это консолидированный реестр, а не новая независимая проверка исходного репозитория. Состояния после последнего отчёта не предполагаются.

## I. Предмет гипотезы и условия

Гипотеза: могут ли два различных набора из одинакового количества параметров одной квантовой модели иметь разные свойства одноэкземплярной достижимости **матричной** SLD quantum Cramér–Rao bound?

Базовое состояние: rho_0 = Q ⊕ 0 на C^22, Q=diag(1/3,2/3), rank=2, kernel dimension=20. 16 SLD L_a=[[0,A_a†],[A_a,0]], A_a in C^(20x2), построены из целочисленных данных. Каноническое аналитическое семейство постоянного ранга F_U. S+={0,...,11}; S-={4,...,15}, оба по 12 параметров, 8 общих. Неоцениваемые четыре параметра **известны и фиксированы**, а не являются неизвестными nuisance parameters. Сравнение в точке theta=0 и, для no-go, локально вокруг неё. Не смешивать матричную CFIM с направленной Hellinger/D2 метрикой.

## II. Положительные результаты

P01. Построена явная модель ранга 2 в 22 измерениях с 16 SLD и целочисленными A.

P02. Найдены два пересекающихся равномощных 12-параметрических подмножества S+ и S- с разной одноэкземплярной матричной достижимостью.

P03. S+ attainable: существует конечное rank-one POVM с CFIM=SLD QFIM (матрица 12x12) в theta=0. Сертификат точный, не только numeric.

P04. Положительный сертификат S+: 1764 регулярных исхода, вероятности положительны; 280 строго положительно определённых рациональных moment blocks; все 484/484 линейных уравнений полноты выполнены точно.

P05. `stage_e_v1/code/exact_cert.py` сам вычисляет рациональное решение y=G.solve(rI) и проверяет его. `verify_exact_integer_v3.py` независимо строит A из 22-мерных векторов, читает сохранённое y и проверяет 484 целочисленных ограничения и миноры 280 блоков. Это **не** две полностью независимые реконструкции исходных моментов: общие входы `exact_bases2.pkl`, `exact_sdp2_M.pkl`, `indep_rows.npy`.

P06. Численный positive control S+: относительный дефицит ~2.43e-12, матричная ошибка ~1.47e-10; численные результаты служат только контролем, не заменой точного сертификата.

P07. Частичная коммутативность `P[L_a,L_b]P=0` в theta=0 для всех 120 пар из 16 SLD, значит для 66 пар каждого из S+ и S-. По отчёту целочисленная проверка дала max defect 0. Для пары (14,15): A_14†A_15=[[136,144i],[-144i,-132]] — Hermitian.

P08. Слабая коммутативность `tr(rho[L_a,L_b])=0` выполнена в theta=0 для всех пар.

P09. Для S- получена аналитическая схема no-go через конусный разделитель, теорему N и интервал O3; проверено в классе конечных и естественных борелевских POVM с точными конвенциями Fisher-information.

P10. Сертифицированная эрмитова матрица: H_exact=(R_0+R_0†)/2, вычислена точно через Arb из сохранённых binary64 элементов. Re(y†R_0 y)=y†H_exact y. Исходная R_0 не побитово эрмитова; defect max ~5.2e-17. `tr H=Σ Re(R_0)_ii`; комплексный `tr R_0` отличается на ~2.3e-17. Не писать `R_sym == R_0` в точном смысле.

P11. Порог O3: последовательное binary64 `s*=fl(fl(0.9·tr H)/20) = 0x1.c057f53368882p-7 = 0.01368236038871751`. Это на один ulp выше результата округления точного 9/10 от trace. Дефиниция s* должна сохранять последовательность округлений.

P12. Положительный separator gap по отчёту gamma=tr(H)-20s* ~= 0.030405245308261095 >0. Допустимость оценки для всего геометрического множества зависит от математических интервальных лемм и полного покрытия.

P13. O3 v3: 7912 чанков, 3955841 лист, все записи ok; четыре запуски по диапазонам без пересечений, SHA журнала и leaf files по результатам аудита совпали; все найденные нижние границы slack положительны.

P14. Run A: 0..1710, 1711 chunks, 855500 leaves, min slack ~[3.1338e-8 ± 6.7e-13]; Run B: 1711..3420, 1710 chunks, 855000 leaves, min ~[2.9217e-8 ± 7.1e-13]; Run C: 3421..5600, 2180 chunks, 1090000 leaves, min ~[8.40e-9 ± 5.2e-12]; Run D: 5601..7911, 2311 chunks, 1155341 leaves, min ~[2.022e-8 ± 5.8e-12]. Worst lower bound ~8.3948e-9 >0. All four audits reported COMPLETE_STRICT scoped to run.

P15. `phi_rows` соответствует real-linear условиям A_i†y ∈ R x; phase reduction Y(e^{iα}x)=e^{iα}Y(x) and phase-invariant separator. Path bound du=hth/2+sin(theta_c/2)hph checked. Sparse numerical sampling 1000 tightest cells 5x5 and 9x9 found no sampled violation, but it is not a proof. Coarse grid sup ~0.0021–0.00218 vs s* ~0.01368; not exhaustive.

P16. Theorem N v8 corrected after Codex criticism: support-projector/Riesz estimates, Łojasiewicz/Hölder continuity, Borel approximation, and distinction between D1/D2; reports say hand proof conditional on O3. At theta≈0 the separator leads to a **uniform positive trace CFIM deficit** for S- with stated assumptions, not necessarily explicit optimized constant.

P17. `Y_S= ⋃_x {y:A_i†y=λ_i x, λ_i ∈ R}` and rank<=1 real-line reformulation are equivalent; invertible Q^(1/2) sends real lines to real lines without preserving each individual line.

P18. Codex cross-model audits identified and helped localize actual faults; latest O3 v3 was reported PASS (internal) after D1–D4 corrections. The review is not external independent mathematical refereeing. Earlier v2 O3 remained conditional due float decisions and leaf evidence gap, which v3 was designed to resolve.

P19. Preserved code/doc milestone with Git commit f0c6df5ccef9a5c7612f7436b4e64eed7f8c4a32 on research/h-cat56-2-cfim-convention, 306 files, normal hooks. 258 non-Chernoff tests passed; remaining Chernoff suite not entirely completed. Git history local only, no push.

P20. Archive `H-CAT56-2_large_artifacts_2026-10-31.tar.gz` ~1.79GB outside Git with 7938 entries and `ARCHIVE_SHA256SUMS.txt`; `gzip -t` and per-file archive hash comparison reported successful. Archive SHA256 `411d9721ff2ec2221eae0cd7c252e6b55d5c40702d0522a33fd8748524543e30`. Restoration test was launched but no final result reported; no remote redundancy confirmed.

## III. Negative, impossibility and refutation results

N01. S- does not admit single-copy POVM saturating complete 12x12 matrix CFIM=QFIM at theta=0 under proved definitions, for arbitrary finite POVMs and specified Borel class. Not limited to separated/projective POVMs.

N02. No-go is about the matrix, not *every directional scalar*. In fact directional measurement can saturate a chosen h-direction; do not say all estimation is impossible.

N03. Near theta=0, no one-copy measurement in stated class can eliminate positive **trace** deficit, within the constant-rank orbit. This is stronger than excluding one candidate measurement but weaker than an arbitrary path/rank-jump statement.

N04. Partial commutativity is NOT sufficient to guarantee one-copy matrix attainability in this model (conditional on validity of full S- no-go), even though it holds for full 16-parameter system.

N05. Pair/composite-rank criterion: reported thresholds 399, full-model count 120*4=480, subset 66*4=264. A count alone does not establish actual matrix rank; needs explicit theorem hypotheses and computation. The 12-parameter subset is not excluded by this criterion as presently applied.

N06. Original Nurdin iff conditions are restricted in the 2024 published corrigendum to *separated* POVMs, not arbitrary ones; cannot use them as universal necessary/sufficient conditions without extra argument.

N07. Counterexample under rank jumps defeats broad assertions of QFIM continuity and unrestricted existence of D2 along every curve. Theorem N revised to claims on rays and curve limsup as appropriate.

N08. Null-probability outcomes cannot automatically be discarded from auxiliary QFIM decomposition: two-outcome POVM `{I_2⊕0,0⊕I_20}` has all N_E contribution at p=0 kernel effect even though ordinary CFIM there is zero. Sum N_E=F^Q is exact.

N09. Earlier Theorem N v8 assertions were actually flawed: omega defined through full N_v (rank jump), explicit s1 without L, blanket D2 along any curve, and Lemma 5 normalization. Corrections were made; preserve both original faults and errata provenance.

N10. Earlier O3 v2 was not a rigorous full interval certificate: float-based branching/estimates and incomplete leaf provenance; O3 v3 replaced it, but v2 remains historical evidence.

N11. Stored R_0 is not exactly Hermitian; `np.array_equal(R_sym,R_0)` false with defect ~5.2e-17. Historical `STAGE_C_FINAL_PROOF.md` lines 71–73 contradicted line 103; recorded in ERRATA; original unaltered.

N12. Two S+ checkers are NOT completely independent: one resolves y, one loads checkpoint y; share bases/moment input. This does not negate explicit final certificate but limits independence of provenance.

N13. Absence of sampled bound failures does NOT prove interval formulas; grid check only corroborates. O3 v3 source audit is the more relevant review.

N14. Full 16-param rank condition and pair counts do NOT automatically prove the same implication for 12-param S- (264<399).

N15. Same-subset-size dependence is not known to be novel as a *general principle*: Suzuki–Yang–Hayashi study parameters of interest and D-invariance, especially with nuisance parameters. Our excluded params are **known** and fixed, not nuisance unknown; direct theorem applicability still requires checking.

## IV. Scientifically important boundaries and unknowns

U01. No independent human referee has checked the entire mathematical argument. Codex is a cross-model internal audit.

U02. Full prior-art equivalence/non-equivalence remains UNKNOWN. Nurdin published correction, quantum exponential family, Suzuki–Yang–Hayashi §5.4, YPZJ, Nurdin projective-measurement work must be compared claim-by-claim. The corrigendum has been provided in the conversation even if not in Claude's local project.

U03. D-invariance itself has not been checked for S+ and S-, and full-rank assumptions may fail for rho_0. Partial/weak commutativity do not automatically establish any specific asymptotic theorem under rank deficiency. Avoid categorical assertion 'both asymptotically attain the same bound'.

U04. Whole-paper reproducibility requires binding to all primary inputs and code, audit of tiling/interval lemmas and final state; full external formal verification still absent.

U05. Exact S+ POVM 1764 outcomes is mathematically certified by moments, but the full independent construction of moment inputs/search provenance is not established.

U06. No experimental physical quantum sensor / implementation / improved sensor precision demonstrated. Application remains prospective.

U07. Local commit and archive are on one machine, no reported remote backup. Restoration test has no completion result. Scientific work is not disaster-proof.

U08. Repo ruff exemption spans phase4 frozen research scripts, including potential F821 defects. Lint pass via exclusion is not equivalent to semantic correctness. Tests: 258 non-Chernoff pass; full suite not established.

U09. The draft reply to Professor Hendra Nurdin is not sent; maintain distinction between scientific outreach and expert validation.

## V. Evidence locations / handoff references

- Git commit: `f0c6df5ccef9a5c7612f7436b4e64eed7f8c4a32`, branch `research/h-cat56-2-cfim-convention`.
- `experiments/20261028-h-cat56-2-phase4/review_package/EVIDENCE_LEDGER.md`
- `review_package/PROOF_OBLIGATIONS.md`; `REVIEW_BRIEF.md`; `O3_AUDIT_RECORD.md`; `O3_V3_INDEPENDENT_AUDIT.md`; `NOVELTY_MATRIX.md`; `ERRATA_STAGE_C_FINAL_PROOF.md`; `FINAL_CONSISTENCY_2026-11-01.md`; `SHA256SUMS.txt`; `RESEARCH_MILESTONE.md` (exact paths relative to phase4 where applicable).
- O3 code `o3_v3/code/interval_cells_v3.py`, `o3_run_v3.py`, `audit_v3_coverage.py`; O3 evidence `o3_v3/records/*.gz` and common `o3v3_progress.jsonl`, per-run summary and manifests.
- S+ code `stage_e_v1/code/exact_cert.py`, `verify_exact_integer_v3.py`; shared exact inputs `exact_bases2.pkl`, `exact_sdp2_M.pkl`, `indep_rows.npy`.
- Novelty test `novelty_checks/partial_commutativity_check.py` and `.out`; review Codex logs.
- Archive `H-CAT56-2_large_artifacts_2026-10-31.tar.gz`, SHA256 `411d9721ff2ec2221eae0cd7c252e6b55d5c40702d0522a33fd8748524543e30`, archival manifest `ARCHIVE_SHA256SUMS.txt`.
- Published references: Nurdin arxiv 2402.11567 with 2024 IEEE CSL corrigendum DOI 10.1109/LCSYS.2024.3451468; Suzuki–Yang–Hayashi arxiv 1911.02790; Yang–Pang–Zhou–Jordan arxiv 1806.07337; Nurdin arxiv 2405.01471.

## VI. Priority without scope creep

1. Make off-machine backup of both repository commit and large archive; verify restore and hashes. Keep archive separate from ordinary Git history if needed.
2. Verify applicability of asymptotic criteria and pair-rank claims without treating a zero necessary condition as sufficiency.
3. Finalize concise technical note and scientifically precise correspondence with Prof. Nurdin; seek external mathematician/referee check.
4. Preserve corrections and negative results; don't rewrite old versions as though they never existed.

Status convention: "verified exact" / "verified interval" refers to reported internal certificates; "published/refereed" is not claimed. A new result requires append-only update with source hashes and scope.
