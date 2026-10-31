# Evidence Ledger v4 — H-CAT56-2, 2026-10-31 (дополняет v2, v3; статусы по типу доказательства)

Статусы: PROVED-hand (логика, внутренний аудит, та же модель) · PROVED (формально) · VERIFIED-exact (точная арифметика) · VERIFIED-interval (arb) · VERIFIED-NUMERIC (численно; не доказательство) · CONDITIONAL · OPEN · FALSIFIED · UNKNOWN · NOT-USED.

| # | Утверждение | Статус | Доказательство / файл | Примечание |
|---|---|---|---|---|
| S+1 | 484 равенства A·M* = b над ℚ, исходный прогон | VERIFIED-exact | `stage_e_v1/logs/exact_cert_result.json` (SHA 53a1f6d7…) | исходный прогон ≈3.2 ч, не перезапускался |
| S+2 | 484 равенства, независимая целочисленная перепроверка (A из определения лифта) | VERIFIED-exact (violated = 0 при 2941 с) | `stage_e_v1/logs/verify_exact_integer_v3.log` | инпуты: checkpoint y, exact_bases2; статус финальный после записи JSON |
| S+3 | Положительность 280 блоков, исходный прогон (Sylvester) | VERIFIED-exact | `exact_cert_result.json` | — |
| S+4 | Положительность 280 блоков, целочисленная перепроверка (главные миноры) | в процессе (40 блоков при 3264 с) | `verify_exact_integer_v3.log` | при завершении — запись в `verify_exact_integer_v3.json` |
| S+5 | Построение POVM из 1764 исходов (лемма D, лемма 2, лемма 3) | PROVED-hand; численная проверка лемм D, линеаризации и SLD | `THEOREM_S_PLUS_EXISTENCE_v6.md`; `check_decomposition_v5.py`; `audit_lift_rows.py` | — |
| S+6 | Harness-эталон: POVM S+ на S+, θ=0, относительный дефицит 2.4·10⁻¹² | VERIFIED-NUMERIC (эталон реализации) | `stage_e_v1/logs/control_differential.json`; `control_differential.py` | не доказательство |
| S+7 | Перенормировка возмущённых POVM: S^{−1/2}ES^{−1/2} сохраняет полноту (ошибка 4.7·10⁻¹⁵) и положительность | PROVED (по построению) + VERIFIED-NUMERIC | `control_differential.py` (функция recomplete) | — |
| S−1 | Теорема C (D1, нулевые исходы 0): нет POVM с CFIM_D1 = F^Q | PROVED-hand + VERIFIED-interval | `STAGE_C_FINAL_PROOF.md`; O3 | — |
| S−2 | O3 журнал: 7 912 чанков, 3 955 841 лист, 0 отказов | VERIFIED-interval | `o3_v2/metrics/o3_journal_audit_2026-10-31.json` | per-leaf B_up чанков 0–3420 не записан |
| S−3 | Покрытие листами прямоугольника | VERIFIED-exact (точная сверка дерева O2) + согласованность площади | `o3_v2/metrics/leaves_coverage_2026-10-31.json` | — |
| S−4 | Постоянство ранга dim Y_S(x) = 4 на CP¹ | PROVED-hand + VERIFIED-interval | `THEOREM_NOGO_S_MINUS_v3.md` §6 | — |
| S−5 | Теорема Q (конечный POVM, D2 в нуле, количественно) | PROVED-hand (аудит CONFIRMED) | `THEOREM_NOGO_S_MINUS_v4.md` | — |
| S−6 | Теорема N v8 (матрица/след, |θ| ≤ s₁, любой h, конечный и борелевский POVM) | PROVED-hand (аудит ae2a07af: CONFIRMED с поправками записи) | `THEOREM_NATURAL_D2_NOGO_v8.md` | область: матричная/следовая CFIM |
| S−7 | Предложение 7: сеть разбиений = интегральная CFIM при θ-независимой μ = tr M | PROVED-hand (исправлено обоснование: без мартингала) | `THEOREM_NATURAL_D2_NOGO_v8.md` §2 | ссылки Dmitriev–Levit не нужны |
| S−8 | Квадратичная форма по направлению (Hellinger-тип) saturable: Proposition 6 | PROVED-hand (аналитически) + VERIFIED-NUMERIC | `ARTICLE_DRAFT_v3_2026-10-31.md` Prop. 6 | определение CFIM обязательно указывать |
| S−9 | Łojasiewicz: f_0 полуалгебраична на сфере C²², нули = 𝒱₀ ∩ S | PROVED (стандарт) | — | ссылка: BCR §2.6 (уровень раздела, оглавление подтверждено) |
| S−10 | Номер Corollary 2.6.7 BCR | не используется в статье; номер UNKNOWN по первоисточнику | — | заменён ссылкой на раздел |
| S−11 | Численный оптимум дефицита по K (аудит): зазор убывает к положительному плато (~15) | VERIFIED-NUMERIC (верхние оценки инфимума) | отчёт аудитора; scratchpad | не доказательство; c не вычислена |
| S−12 | Выборочная оценка s* ≈ 0.00284 ≤ s_target (сертификат) | VERIFIED-NUMERIC (согласованность) | отчёт аудитора | — |
| S−13 | Nurdin c_lm: 16 параметров (ранг 399) | PROVED-hand | `TECHNICAL_NOTE_A0_EN_v1.2.md` §4 | — |
| S−14 | Nurdin c_lm для S− | не применимо: 264 < 399 | — | — |
| S−15 | Семьи вне F_U | OPEN | — | — |
| N-1 | Новизна | PARTIAL | `ARTICLE_DRAFT_v3_2026-10-31.md` §7 | полный поиск не проведён |
| N-2 | Контрольный тест S− минимальным дефицитом (полный) | OPEN | `CONTROL_RESULTS_2026-10-31.md` (старый K=24 — неразличающий) | новый дизайн: S+ эталон (done) → S− поиск; нижняя граница не получена |

## Сводка

- **S+:** существование POVM из 1764 регулярных исходов — PROVED (логика). Точные равенства 484 — VERIFIED-exact по двум независимым прогонам (исходный; целочисленный). Положительность 280 блоков — VERIFIED-exact по исходному прогону; целочисленная перепроверка в процессе.
- **S−:** матричный/следовой запрет для конечных и борелевских POVM в F_U при |θ| ≤ s₁ — PROVED-hand (внутренний аудит). Квадратичная форма по направлению — не запрещена (Proposition 6). Семьи вне F_U — OPEN.
- **Численные контроли:** эталон S+ пройден; дефицит S− по численному поиску — верхняя граница; нижняя оценка не получена.
- **Внешние зависимости:** BCR §2.6 (раздел подтверждён); внешнее рецензирование отсутствует.
