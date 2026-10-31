# Evidence Ledger v2 — H-CAT56-2, 2026-10-31 (заменяет EVIDENCE_LEDGER_2026-10-31.md)

Статусы: PROVED-hand (логика на бумаге, проверена перевыводом) · PROVED (логика, формальная) · VERIFIED-exact · VERIFIED-interval · VERIFIED-float (не доказательство) · CONDITIONAL · OPEN · NOT-USED.
Коммитов, push, внешних отправок не было; A0, R, исторические сертификаты, registry не менялись.

| # | Утверждение | Статус | Доказательство / файл | SHA-256 (префикс) |
|---|---|---|---|---|
| L1 | Конвенция A_i = −2iB_i; Q = diag(1/3,2/3) | CONDITIONAL (принято владельцем; соответствие FORMAT.md и загрузчику проверено) | `outreach/…/FORMAT.md`; `ys_space.py` | — |
| L2 | SLD L_a и ρ(θ) = e^Xρe^{−X}: уравнение SLD точно, производная ~4·10⁻¹⁰ | VERIFIED-float | `stage_e_v1/code/check_sld_convention.py` | d39a31ef… |
| L3 | QFIM F = Re Tr(QAᴴA) точно, F ≻ 0 на S+ | VERIFIED-float | то же | — |
| L4 | Y_S(x_j) точно, 1484 × 12 | VERIFIED-exact | `audit_ys_exact.py` → `logs/audit_ys_exact.json` | 34e59fff… |
| L5 | A из определения лифта = сохранённая A | VERIFIED-float (3.3·10⁻¹⁶) | `audit_lift_rows.py` → `logs/audit_lift_rows.log` | b4d45b32… |
| L6 | 484 координаты = Herm(22); ΣE = I ⇔ A·M = b | PROVED-hand | `THEOREM_S_PLUS_EXISTENCE_v6.md` §3 | 0a685a4f… |
| L7 | Лемма D: M = ω Σĉĉᵀ, (ĉ)_N = 1 | PROVED-hand; численно 200/200 | `check_decomposition_v5.py` | f0f78a12… |
| L8 | Насыщение ⇔ A_iᴴy = ξα, ξ ∈ R, для любого Q ≻ 0 | PROVED-hand по тексту YPZJ thm:reg | v6 §2 | arXiv:1806.07337 §4.1 |
| L9 | A·M* = b точно над Q (484 строки) | VERIFIED-exact (исходный прогон) | `exact_cert.py` → `logs/exact_cert_result.json` | 53a1f6d7… |
| L10 | M_j* ≻ 0 точно над Q | VERIFIED-exact (Sylvester, исходный прогон) | тот же вывод | — |
| L11 | Независимая перепроверка L9, L10 по checkpoint y, fmpq, без пересчёта решения | **в процессе (фон)**; результат: `logs/verify_exact_rational_v1.json` | `stage_e_v1/code/verify_exact_rational_v1.py` | — |
| L12 | Цепочка входов instance → exact_kernel → exact_bases → exact_bases2 → exact_sdp2_M → exact_cert | прочитана по коду, хеши записаны | `logs/SHA256SUMS_inputs_stageE_v5_2026-10-31.txt` | — |
| L13 | Направления Ξ (280) — upstream `s14_povm_prefix12.npz` | не перепроверено | SHA 8ab6f458… | — |
| L14 | Теорема S+ (1764 исхода, регулярность, ΣE=I, CFIM=QFIM) | PROVED-hand при L6, L8, L9, L10 | `S_PLUS_FINAL_v1.md` | 97f92f8e… |
| L15 | mod-p и Decimal | NOT-USED | `verify_cert_compact.py` | — |
| S1 | Теорема C (D1) | PROVED-hand + VERIFIED-interval | `STAGE_C_FINAL_PROOF.md`, O3 | — |
| S2 | O3 v2: 7912 чанков, 3 955 841 лист, 0 отказов, gap 0.0304 | VERIFIED-interval; журнал AUDIT_PASS | `o3_v2/metrics/o3_journal_audit_2026-10-31.json` | c72a47a8… |
| S3 | Входы O3: R.npz (55b898d6…), leaves.npy (29ab7b14…) совпадают с записанными | VERIFIED-exact (хеши) | `o3_v2/SHA256SUMS_o3v2.txt` | — |
| S4 | Арифметика arb: округление, покрытие | VERIFIED-interval; код прочитан (`interval_cells_v2.py`): верхние границы, Gershgorin для любого V, сертификат ядра на каждой ячейке | — | — |
| S5 | Лемма 1 и лемма 4 | PROVED-hand; перевыведено агентом; S1–S6 PASS | `D2_CONE_TRANSFER_v3.md` (корень phase4); `d2_v3_S_checks.log` | 97b8f56d… |
| S6 | Предел null-исходов (Nh)(Nh)ᵀ/(hᵀNh); ошибка ∝ t² | PROVED-hand; численно S5 | то же | — |
| S7 | Счётный случай (лемма 5) с соглашением F_k := 0 при p_k = 0 | PROVED-hand (агент-аудит: пробел в определении закрыт) | `S_MINUS_FINAL_v2.md` §4 | — |
| S8 | Шаг в конус: tr(R D_k) ≤ s·tr D_k поэлементно | PROVED-hand | `S_MINUS_FINAL_v2.md` §3 | — |
| S9 | Теорема A (D2, конечные и счётные POVM, F_U, одно h) | PROVED-hand; агент weak-medium; гипотезы H1–H5 явно | `S_MINUS_FINAL_v2.md` §2 | — |
| S10 | Численные g-проверки (G1–G4) | VERIFIED-float на конечном усечении (НЕ проверка хвоста) | `d2_v3/metrics/g5_countable_check.log` | 30069211… |
| S11 | Борелевский CFIM (D2) | OPEN; препятствие — робастная лемма (R); пересечение с D2_G5_TAIL §5 (Пратт) не разрешено | `S_MINUS_BOREL_AND_NURDIN_v1.md` | — |
| S12 | D2 для семей вне F_U | OPEN | — | — |
| S13 | Nurdin: составная матрица c_lm для 16 параметров (Prop 2 техноты) | PROVED-hand (проверен текст доказательства) + ранг 399 | `TECHNICAL_NOTE_A0_EN_v1.2.md` §4 | — |
| S14 | Nurdin c_lm для S− | **не применим**: 4·C(12,2) = 264 < 399 | `S_MINUS_BOREL_AND_NURDIN_v1.md` §C3 | — |
| S15 | Новизна | PARTIAL (см. memo) | `RESEARCH_MEMO_DRAFT_2026-10-31.md` | — |

## Итоговые статусы

- **S+ = {0..11}:** PROVED-hand на Ξ (1764 исхода) при L6, L8, L9, L10. Воспроизводимость: входы захешированы; перепроверка L9/L10 (L11) — в процессе.
- **S−, D1:** PROVED-hand + VERIFIED-interval.
- **S−, D2, конечные и счётные POVM в F_U, одно h:** PROVED-hand при явных гипотезах H1–H5 и соглашении D2; аудит — weak-medium.
- **S−, борелевский случай и семьи вне F_U:** OPEN.
- **Новизна:** PARTIAL.
