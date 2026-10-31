# Инструкция воспроизведения — H-CAT56-2 (2026-10-31)

Все пути — относительно `experiments/20261028-h-cat56-2-phase4/`. Окружение: Python 3, numpy, scipy, python-flint (fmpz/fmpq/arb). Коммитов и внешних отправок нет. Исходные данные (инстанс, `s14_povm_prefix12.npz`) не изменяются.

## 1. Целостность артефактов

```
sha256sum -c SHA256SUMS_S+_chain_2026-10-31.txt
sha256sum -c SHA256SUMS_S+_integer_check_2026-10-31.txt
sha256sum -c SHA256SUMS_v6_2026-10-31.txt
sha256sum -c SHA256SUMS_v5_2026-10-31.txt
```

## 2. S+ — точная проверка

| Шаг | Команда | Ожидаемый результат | Время |
|---|---|---|---|
| Точная Y_S-принадлежность | `python stage_e_v1/code/audit_ys_exact.py` | `membership_exact_pass: true`, 1484 вектора | минуты |
| Линеаризация A | `python stage_e_v1/code/audit_lift_rows.py` | `LIFT_ROWS_AGREE` | минуты |
| Лемма D (численно) | `python stage_e_v1/code/check_decomposition_v5.py` | ошибка ≤ 1e-14 | секунды |
| Модель SLD/QFIM | `python stage_e_v1/code/check_sld_convention.py` | SLD ≈ 0, QFIM ≈ 0 | секунды |
| Целочисленная проверка 484 + 280 | `python stage_e_v1/code/verify_exact_integer_v3.py` | `rows_violated_exactly: 0`, `all_blocks_positive_definite_exact: true` | ≈ 81 мин, один процесс, ≈17 ГБ |
| Рациональный исходный прогон | `python stage_e_v1/code/exact_cert.py` | `rows_violated_exactly: 0` | ≈ 3.2 ч, не перезапускать без причины |

Сравнить выводы с `stage_e_v1/logs/verify_exact_integer_v3.json` и `exact_cert_result.json`.

## 3. Численные контроли (не доказательство)

```
python stage_e_v1/code/control_differential.py
```
Ожидаемо: POS относительный дефицит ~1e-12; NEG ~0.44; SENS квадратичный рост. Файл: `stage_e_v1/logs/control_differential.json`.

## 4. O3 (интервальный сертификат)

```
python o3_v2/code/audit_o3_journal_2026-10-31.py      # AUDIT_PASS
python o3_v2/code/audit_leaves_coverage_2026-10-31.py
```
Полный перезапуск O3 (≈6.1 ч) не выполнялся; см. `O3_CLOSURE_2026-10-31.md`.

## 5. S− — логика

Документы: `THEOREM_NATURAL_D2_NOGO_v8.md` (теорема), `S_MINUS_LOGIC_CHECK_v8.md` (таблица определений, кванторов, контрпример), `THEOREM_NOGO_S_MINUS_v4.md` (Теорема Q для D2 в нуле). Логическая проверка — ручная; численных шагов для доказательства нет.

## 6. Что проверить внешне (не выполнено)

1. Полное рецензирование доказательств Теоремы N и Предложения 7.
2. Расширение на C¹-семьи (аудит adc79edf; статус CONDITIONAL).
3. Номера теорем: только раздел BCR §2.6 подтверждён.
4. Hayashi–Ouyang — тексты о критериях насыщения.

## 7. Игрушечный контрпример со скачком ранга (synthetic, не модель C²²)

```
cd toy_rank_jump
python rank_jump_check.py > rank_jump_check.out
python povm8_jump.py > povm8_jump.out
```
Ожидаемо: при s = 0.003 `trFQ(s)-trFQ(0) ≈ +3.998` (аналитически 4·trτ = 4), `hFEh` с прыжком `≈ 16.40` против `hFQ0h = 12.40`, без прыжка (jump=False) — совпадение `12.399`. Аналитический вывод: `PROOF_RECONSTRUCTION_THEOREM_N_2026-10-31.md`, раздел «Аналитическое объяснение скачка ранга».

## 8. Независимая реконструкция Теоремы N

`PROOF_RECONSTRUCTION_THEOREM_N_2026-10-31.md`: шаги 1–12, со статусами PROVED-hand / CONDITIONAL / FALSIFIED / UNKNOWN. Самопроверка — только по тексту шагов; внешний аудитор не привлекался.

## 9. Нормировка ΣN_k = F^Q и соответствие Y ↔ Y_S для F_U (S− = {4..15})

```
python checks/fu_normalization_and_Y_2026-10-31.py > checks/fu_normalization_and_Y_2026-10-31.out
```
Ожидаемо: `two_outcome_sum_N_minus_FQ0_max_abs ≈ 7e-12`, `random_povm_sum_N_minus_FQ0_relative ≈ 1.6e-15`, `max_rank_real_gram_Qh_A^H_y_over_Y_S_basis = 1`, `generic_y_rank_distribution = {"4": 200}`. Конечно-разностная невязка SLD (≈4e-7) ограничена шагом ε = 10⁻⁶; аналитическое тождество L_ss = 0 точное.
