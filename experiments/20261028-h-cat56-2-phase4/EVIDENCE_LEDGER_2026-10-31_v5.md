# Evidence Ledger v5 — H-CAT56-2, 2026-10-31 (публикационная версия; дополняет v4)

Статусы: PROVED-hand (логика, внутренний аудит, та же модель) · PROVED · VERIFIED-exact (точная арифметика) · VERIFIED-interval (arb) · VERIFIED-NUMERIC (не доказательство) · CONDITIONAL · OPEN · FALSIFIED · UNKNOWN. Внешнее рецензирование не проводилось ни по одному пункту.

| # | Утверждение | Статус | Доказательство | Хеш/файл |
|---|---|---|---|---|
| S+.1 | Логика Теоремы S+ (1764 регулярных исхода на Ξ, ΣE=I, CFIM=QFIM при θ=0) | PROVED (логика) | `THEOREM_S_PLUS_EXISTENCE_v6.md`, `S_PLUS_CERTIFICATE_FINAL_v2.md` §1 | — |
| S+.2 | 484 равенства над ℤ, независимое построение A | VERIFIED-exact | `verify_exact_integer_v3.json` (rows_violated_exactly 0) | f255dec4… |
| S+.3 | 280 блоков положительно определены над ℤ | VERIFIED-exact | `verify_exact_integer_v3.json` (all_blocks_positive_definite_exact true) | f255dec4… |
| S+.4 | 484 равенства над ℚ, исходный прогон | VERIFIED-exact | `exact_cert_result.json` | 53a1f6d7… |
| S+.5 | 280 блоков над ℚ, исходный прогон | VERIFIED-exact | `exact_cert_result.json` | 53a1f6d7… |
| S+.6 | Общие входы двух прогонов (bases2, I, checkpoint y) | документировано; регенерации нет → CONDITIONAL на корректность входов | `S_PLUS_CERTIFICATE_FINAL_v2.md` §4; `SHA256SUMS_S+_chain_2026-10-31.txt` | fbca57fa… (bases2), 1d6cdf94… (y), 0b0f3a4f… (I) |
| S+.7 | Цепочка направления → базисы → моменты → POVM | прочитана по коду; хеши записаны | `SHA256SUMS_S+_chain_2026-10-31.txt` | — |
| S+.8 | Эталон численного контроля (относительный дефицит 2.4e-12) | VERIFIED-NUMERIC | `stage_e_v1/logs/control_differential.json` | a8f71199… |
| S+.9 | Точные элементы POVM не выписаны (не требуется для существования) | OPEN (не препятствие) | — | — |
| S−.1 | Теорема N v8 (матрица/след, конечный и борелевский POVM, F_U, |θ|≤s₁) | PROVED-hand | `THEOREM_NATURAL_D2_NOGO_v8.md`; `S_MINUS_LOGIC_CHECK_v8.md` | db75a412… (v8) |
| S−.2 | Предложение 7 (сеть = интеграл, μ = tr M) | PROVED-hand (поправки записи внесены) | `THEOREM_NATURAL_D2_NOGO_v8.md` §2 | — |
| S−.3 | Контрпример: направленная квадратичная форма насыщаема (I₂⊕0, 0⊕e_ke_kᴴ) | PROVED-hand (аналитически) + VERIFIED-NUMERIC | `S_MINUS_LOGIC_CHECK_v8.md` §3 | — |
| S−.4 | Łojasiewicz (раздел BCR §2.6) | PROVED (стандарт); номер Cor. 2.6.7 не используется | оглавление BCR (Google Books excerpt) | — |
| S−.5 | Теорема N на C¹-семьях при условиях 1–3 **и** разделителе R* с γ > 0; модуль ω вместо L. Условие 3 — блок (∂ρ₀)_{ss} = 0 | PROVED-hand для F_U (разделитель от O3). Для общей семьи **CONDITIONAL** на разделитель. Независимая реконструкция: `PROOF_RECONSTRUCTION_THEOREM_N_2026-10-31.md`, шаги 1–8 |
| S−.5g | Проектор Рисса: N_v(θ) ⪰ Gram(P(θ)w_a(θ)), f_θ ≥ f₀ − ω(|θ|) без постоянного ранга | PROVED-hand (реконструкция шагов 2–5; использует C2) | `PROOF_RECONSTRUCTION…` шаги 2–5 | — |
| S−.5h | Łojasiewicz для f₀ на C¹-семье: f₀ полуалгебраична при любых фиксированных L(0), θ₀ ≤ 1 | PROVED-hand (ссылка BCR §2.6, уровень раздела) | `PROOF_RECONSTRUCTION…` шаг 6 | — |
| S−.5i | Нуль f₀ = ℂ²×𝒴 при C3; 𝒴 совпадает с YPZJ-насыщением ∪_x Y_S(x) для F_U | PROVED-hand | `PROOF_RECONSTRUCTION…` шаг 7 | — |
| S−.5j | Лемма 6 (цепочка Гёльдера, константа 22C₁C₀) | PROVED-hand (реконструкция с нуля) | `PROOF_RECONSTRUCTION…` шаг 8 | — |
| S−.5k | Аналитический скачок lim F^Q(sh) − F^Q(0) = 4(trτ)hhᵀ для toy-семьи | PROVED-hand (первый порядок) + VERIFIED-NUMERIC (3.9976 при s = 0.003) | `PROOF_RECONSTRUCTION…` приложение; `toy_rank_jump/` | — | `THEOREM_NATURAL_D2_NOGO_v8.md` §0, §4; `S_MINUS_LOGIC_CHECK_v8.md` §4–5 | db75a412… (v8, до правки; пересчитан в манифесте) |
| S−.5a | Одностороннее неравенство f_s ≥ f_0 − ω(s) без постоянного ранга (проектор Рисса) | PROVED-hand; численно на игрушке 5×3 (синтетика) | `THEOREM_NATURAL_D2_NOGO_v8.md` §0 | — |
| S−.5b | Контрпример: без непрерывности ∂ρ в нуле tr(F^Q − F_E) = 0 при θ_k → 0 | FALSIFIED-условие (контрпример проверен аудитом аналитически) | `THEOREM_NATURAL_D2_NOGO_v8.md` §0 | — |
| S−.5c | Предельная форма N₁ (tr F^C_M(sh) → ≤ tr F^Q(0) − c) для C¹-семей при условиях 1–3 | **FALSIFIED** (контрпример `toy_rank_jump/`: tr F^Q(s) → 65.51 ≠ 61.51 = tr F^Q(0); численно, синтетика 5×3) | `THEOREM_NATURAL_D2_NOGO_v8.md` §2, §4 | rank_jump_check.out (SHA в манифесте) |
| S−.5c′ | N₁ предельная форма при постоянном ранге 2 | PROVED-hand (проектор поддержки и L непрерывны; tr F^Q непрерывна) | `THEOREM_NATURAL_D2_NOGO_v8.md` §2 | — |
| S−.5d | Предложение 8 для C¹-семей | **FALSIFIED** в общем случае (16.40 против 12.40 на скачке ранга); верно для F_U | `THEOREM_NATURAL_D2_NOGO_v8.md` §3, §4; `toy_rank_jump/povm8_jump.out` | — |
| S−.5e | Условие нулевого блока относится к ∂ρ₀ (эквивалентно L(0)_ss = 0), не к ρ₀ (ss-блок ρ₀ = Q) | PROVED-hand (уравнение Сильвестра, Q > 0); роль: продуктовая структура 𝒱₀ = ℂ² × 𝒴 | `THEOREM_NATURAL_D2_NOGO_v8.md` §0 | — |
| S−.5l | O4 (D1 против D2): след ≤ tr F^Q(0) − c вдоль каждого луча (D2 существует); для произвольной кривой только limsup ≤ tr F^Q(0) − c (существование D2 вдоль кривых ложно, аудит Codex) | PROVED-hand (предел конечной суммы; непрерывность tr F^Q для постоянного ранга) | `PROOF_RECONSTRUCTION…` вторая проверка, п. 7; ARTICLE §2 | — |
| S−.5m | Теорема N не использует O1 (редукцию насыщения) | PROVED-hand (проверкой зависимостей шагов 1–8) | `PROOF_RECONSTRUCTION…` вторая проверка, п. 6 | — |
| S−.5f | Łojasevich для f_0 на C¹-семье | PROVED-hand (f_0 полуалгебраична при любых фиксированных L(0)) | `THEOREM_NATURAL_D2_NOGO_v8.md` §0 | — |
| S−.6 | Теорема Q (конечный POVM, направленный D2 в нуле) | PROVED-hand | `THEOREM_NOGO_S_MINUS_v4.md` | 74a201c7… (v4) |
| S−.7 | O3 интервальный сертификат (γ ≥ 0.0304) | VERIFIED-interval (с оговорками: per-leaf для чанков 0–3420 не записан; прогон 6.1 ч > лимита 4 ч) | `o3_v2/metrics/o3_journal_audit_2026-10-31.json` | — |
| S−.8 | Постоянство ранга dim Y_S = 4 на CP¹ | PROVED + VERIFIED-interval | `THEOREM_NOGO_S_MINUS_v3.md` §6 | — |
| S−.9 | D1-запрет (нулевые исходы 0) | PROVED-hand + VERIFIED-interval | `STAGE_C_FINAL_PROOF.md` | — |
| S−.10 | Nurdin c_lm для 16 параметров (ранг 399) | PROVED-hand | `TECHNICAL_NOTE_A0_EN_v1.2.md` §4 | — |
| S−.11 | Nurdin c_lm для S− | не применимо (264 < 399) | `S_MINUS_LOGIC_CHECK_v8.md` / статья Prop. 5 | — |
| S−.12 | Семьи вне C¹ | OPEN | — | — |
| S−.13 | Явные константы c, s₁, C₂, θ₀ | OPEN (существуют, не вычислены) | — | — |
| N.1 | Новизна | PARTIAL | `ARTICLE_DRAFT_v4_2026-10-31.md` §7 | полный поиск не проведён |
| N.2 | Внешнее рецензирование | **не проводилось** | — | — |
| N.3 | Hayashi–Ouyang: критерии насыщения | UNKNOWN (только метаданные) | — | — |
| N.4 | Nurdin: композитная матрица c_lm — вывод из переписки | UNKNOWN (в репозитории не найден) | — | — |
| N.9 | Литература по single-copy насыщению (2402.11567; 1806.07337; 2602.12097) найдена поисковыми сниппетами; полный текст 2602.12097 и 2601.21801 не прочитан | UNKNOWN (полнота поиска) | поиск 2026-10-31; `SCIENTIFIC_READINESS_REPORT_2026-10-31.md` §4 | — |
| N.10 | Новизна: инстанс-уровневые результаты S+ и S− (F_U, след, D2-предел, Borel) — новые; известные критерии (YPZJ thm:reg, Nurdin) не выдаются за новые | PARTIAL (полный поиск не проводился; «впервые» не используется) | `SCIENTIFIC_READINESS_REPORT_2026-10-31.md` §4 | — |
| N.5 | Нормировка ΣN_k = F^Q для полного POVM (N_E,ab = Re tr(E L_a ρ L_b), F^Q = Re tr(ρ L_a L_b)): Σ_k tr(E_k L_aρL_b) = tr(L_aρL_b), и Re tr(ρL_bL_a) = Re tr(ρL_aL_b) через сопряжение | PROVED-hand; численно: два исхода {I₂⊕0, 0⊕I₂₀} дают ΣN − F^Q ≈ 7·10⁻¹² (FQ0 из замкнутой формы), случайный POVM на 40 исходах — относительно 1.6·10⁻¹⁵ | `checks/fu_normalization_and_Y_2026-10-31.py` → `.out` (part1) | — |
| N.6 | Ядерный исход (p_k(0) = 0) даёт N_k ≠ 0: для {I₂⊕0, 0⊕I₂₀} след N_ker = 60005.33 = tr F^Q(0), F_k := 0 (D1) | PROVED-hand (p_k = 0 ⇒ a_j = 0, но b_j = ρ^{1/2}L v_j ≠ 0 в общем случае) + VERIFIED-NUMERIC | `checks/…out` (two_outcome_N_kernel_outcome_trace) | — |
| N.7 | Y_S(x) ⊂ 𝒴 и 𝒴 = ∪_x Y_S(x): w_a = Q^{1/2}A_aᴴy, rank_ℝ Gram(w) ≤ 1 ⇔ w_a = ξ_a w с ξ_a ∈ ℝ; x ↦ Q^{1/2}x — биекция ℂ² | PROVED-hand (ℝ-линейное обратимое отображение переводит вещественные прямые в вещественные прямые, а не сохраняет каждую; множество «все векторы на одной вещественной прямой» сохраняется) + VERIFIED-NUMERIC (120 базисных векторов Y_S(x) по 30 случайным x: max rank 1; 200 случайных y: rank 4) | `checks/…out` (part2) | — |
| N.8 | Конечные разности SLD: невязка ‖∂ρ − (ρL+Lρ)/2‖ ≈ 4·10⁻⁷ при ε = 10⁻⁶ — ограничение конечных разностей, аналитическое тождество L_ss = 0 точное | VERIFIED-NUMERIC (ограничено FD) | `checks/…out` (sld_equation_max_residual_at_0) | — |

## Итоговые статусы

- **S+:** существование POVM из 1764 регулярных исходов — PROVED (логика); точные равенства и положительность — VERIFIED-exact в двух арифметиках на общих входах; регенерация входов не выполнена → CONDITIONAL на входы.
- **S−:** матричный/следовой запрет для конечных и борелевских POVM (F_U, |θ| ≤ s₁) — PROVED-hand; направленная квадратичная форма не запрещена; Теорема N переносится на C¹-семьи при условиях 1–3 (PROVED-hand); предельная форма N₁ и Предложение 8 для общих C¹-семей ложны при условиях 1–3 (контрпример со скачком ранга); верны при постоянном ранге 2 (N₁) и для F_U.
- **Численные контроли:** реализационные эталоны, не доказательство.
- **Внешняя проверка:** отсутствует.
