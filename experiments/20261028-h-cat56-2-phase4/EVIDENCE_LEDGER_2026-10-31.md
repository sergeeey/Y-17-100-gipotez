# Evidence Ledger — H-CAT56-2, S+ и S−, 2026-10-31

Статусы: PROVED (логика) · VERIFIED-exact (точная арифметика, воспроизведено в этом проходе) · VERIFIED-interval (arb) · VERIFIED-float (численно, не доказательство) · CONDITIONAL · OPEN · NOT-USED (отвергнуто как доказательство).
Не коммитилось, не отправлялось, исторические сертификаты A0, R, registry/graph.yaml не менялись.

| # | Утверждение | Статус | Основание / воспроизведение | SHA / файл |
|---|---|---|---|---|
| L1 | Конвенция: A_i = −2iB_i = 2 Im − 2i Re; состояние diag(1,2) ~ Q = diag(1/3,2/3) | CONDITIONAL (принято владельцем как рабочее) | FORMAT.md + loader ys_space/qfi_pcc_check сходятся | `outreach/…/FORMAT.md` |
| L2 | SLD L_a = [[0,Aᴴ],[A,0]] и ρ(θ) = e^{X}ρe^{−X}, X = [[0,−Aᴴ/2],[A/2,0]] | VERIFIED-float (SLD exact 0, производная 4·10⁻¹⁰ конечными разностями) | `check_sld_convention.py` | `stage_e_v1/code/check_sld_convention.py` |
| L3 | QFIM F_ij = Re Tr(QAᴴA) = Tr(ρ(LL+LL)/2) для S+ | VERIFIED-float (ошибка 0) | то же | то же |
| L4 | Y_S(x_j) точно: 1484 вектора × 12 условий | VERIFIED-exact (Fraction) | `audit_ys_exact.py` | `logs/audit_ys_exact.json` (SHA 34e59fff…) |
| L5 | Линеаризация A из определения лифта = сохранённая A (float) | VERIFIED-float (3.3·10⁻¹⁶) | `audit_lift_rows.py` | `logs/audit_lift_rows.log` (SHA b4d45b32…) |
| L6 | 484 координаты = Herm(22); ΣE = I ⇔ A·M = b | PROVED | v6 §3 | `THEOREM_S_PLUS_EXISTENCE_v6.md` (SHA 0a685a4f…) |
| L7 | Лемма D: M = ω Σ ĉĉᵀ, (ĉ)_N = 1, N исходов | PROVED; numeric 200/200 (10⁻¹⁵) | v6 §4 | `check_decomposition_v5.py` (SHA f0f78a12…) |
| L8 | Насыщение ⇔ A_iᴴy = ξα, ξ ∈ R, для любого Q ≻ 0 | PROVED по тексту YPZJ thm:reg | v6 §2 | arXiv:1806.07337 §4.1 |
| L9 | A·M* = b точно над Q (все 484) | VERIFIED-exact (исходный прогон; перезапуска нет) | `exact_cert.py`: `rows_violated_exactly: 0` | `logs/exact_cert_result.json` (SHA 53a1f6d7…), `logs/exact_cert.log` (SHA 3f59a0b6…) |
| L10 | M_j* ≻ 0 точно над Q | VERIFIED-exact (Sylvester, исходный прогон) | `exact_cert.py` блок LDL, `all_M_positive_definite_exact: true` | то же |
| L11 | Цепочка входов: instance → exact_kernel → exact_bases → exact_bases2 → exact_sdp2_M → exact_cert | прочитана по коду; хеши входов записаны | `logs/SHA256SUMS_inputs_stageE_v5_2026-10-31.txt` | — |
| L12 | Направления Ξ (280) — upstream-файл `s14_povm_prefix12.npz` | не перепроверено (генерация вне этого проекта) | SHA 8ab6f458… | `20261027-h-cat56-2-discovery/metrics/` |
| L13 | Теорема S+ (1764 исхода, регулярность, ΣE=I, CFIM=QFIM) | PROVED при L6, L8, L9, L10 | `S_PLUS_FINAL_v1.md` | SHA 97f92f8e… |
| L14 | mod-p остатки (3 простых модуля) | NOT-USED как доказательство (нет границы реконструкции) | `logs/verify_cert_compact.log` | — |
| L15 | Decimal-проверка PD | NOT-USED (не завершилась, без контроля округления) | — | — |
| S1 | Теорема C (D1, отрицательная) | PROVED-hand + VERIFIED-interval | `STAGE_C_FINAL_PROOF.md`, O3 | — |
| S2 | O3 v2: 7912 чанков, 3 955 841 лист, 0 отказов, final gap 0.0304 > 0 | VERIFIED-interval | `o3_v2/metrics/o3_summary.json`; журнал `audit_o3_journal_2026-10-31.py` → AUDIT_PASS | `o3_v2/metrics/o3_journal_audit_2026-10-31.json` (SHA c72a47a8…) |
| S3 | Входы O3: R.npz и leaves.npy совпадают с исходными (SHA) | VERIFIED-exact (сравнение хешей) | `o3_v2/SHA256SUMS_o3v2.txt`, аудит журнала | — |
| S4 | Лемма 1 (блочная формула) и Лемма 4 (ранг-1 ⇔ 𝒴_S) | PROVED-hand; S1–S6 PASS | `d2_v3_S_checks.py` | `d2_v3/metrics/d2_v3_S_checks.log` (SHA 97b8f56d…) |
| S5 | Предел F_D2 для null-исходов (Nh)(Nh)ᵀ/(hᵀNh) | PROVED-hand; численно (ошибка ∝ t) | v3 §3b; S5 | то же |
| S6 | Счётный POVM: тугость хвостов через F_k ⪯ N_k и полноту | PROVED-hand (новое, `S_MINUS_FINAL_v1.md` §4) | `g5_countable_check.py`: G1–G4 PASS (численно) | `d2_v3/metrics/g5_countable_check.log` (SHA 30069211…), `d2_v3/code/g5_countable_check.py` (SHA e7fa800b…) |
| S7 | Теорема A (D2, конечные/счётные POVM, семья F_U, одно h) | CONDITIONAL: аналитика полна, нет независимого аудита v3 + S6 (G4 PARTIAL) | `S_MINUS_FINAL_v1.md` §2, §6 | — |
| S8 | Борелевский (несчётный) CFIM в D2 | OPEN | нужна робастная версия Теоремы A | — |
| S9 | D2 для общих C¹-семей (вне F_U) | OPEN | E_AUDIT T4(ii) | — |
| S10 | Nurdin, составная матрица c_lm — вывод формулировки | OPEN (текст не найден в репозитории) | HANDOFF_2026-10-30 | — |
| S11 | Новизна | PARTIAL (YPZJ, YIP, Nurdin v5 + корригендум, Conlon 2404.01520/2609.35975, Imai–Yang–Pezzè 2602.12097; «Theorem 6» есть только в v1) | `arxiv` метаданные, `REPORT_SOURCE_CHECK_2026-10-31.md` | — |

## Замечания по воспроизводимости

- Точный сертификат `exact_cert.py` (3.2 ч) не перезапускался в этом проходе; его корректность опирается на захешированный выход и на код, прочитанный построчно.
- Mod-p и Decimal-проверки не используются как доказательство (L14, L15).
- O3 журнал: per-leaf B_up для чанков 0–3420 не записан; вердикт опирается на ok-флаги arb на каждом листе.
- Коммит и внешние отправки не делались; папка phase4 — не отслеживается git.

## Итоговые статусы

- **S+ = {0..11}: PROVED на сетке Ξ (1764 исхода) логически при L6, L8, L9, L10; воспроизводимость сертификата частичная (хеши + нет перезапуска).**
- **S− = {4..15}: Теорема C (D1) PROVED; Теорема A (D2, конечные и счётные POVM, семья F_U, одно направление) CONDITIONAL (нужен независимый аудит); борелевский случай и общие семьи OPEN.**
- **Новизна: PARTIAL.**
