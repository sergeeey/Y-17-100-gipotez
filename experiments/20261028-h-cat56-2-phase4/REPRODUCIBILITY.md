# REPRODUCIBILITY — стадия C, S− (2026-10-29)

Корень: `experiments/20261028-h-cat56-2-phase4/` (пути Windows; запуск из корня репозитория `Y-17 100 gipotez`).
Хеши всех входов, кода и результатов: `PROOF_CERTIFICATES/SHA256SUMS.txt` (проверка: `sha256sum -c PROOF_CERTIFICATES/SHA256SUMS.txt`, файлы списком в `files.txt`).

Входы (не менялись): `instance_d22_r2_s16.jsonl` (A0), `s14_R_…_nx250.npz` (R), `s14_povm_prefix12.npz` (POVM S+, 280 элементов).

## Команды

Базовый float-сертификат S− (≈71 мин):
    python -I experiments/20261028-h-cat56-2-phase4/code/c3d_cell_certificate_adapted.py <instance> <R.npz> 0.9 16 32 14 experiments/20261028-h-cat56-2-phase4/metrics/c3d_S-_f090_v2.json S-

Запас 10⁻⁴ (переменная окружения MARGIN_REL=1e-4), порог b = 0.0145 (frac = 0.9537827998421272), контроль S+ — аналогично с другими аргументами.

Выгрузка листьев: `code/c3g_dump_leaves.py` (тот же аргумент-набор, даёт `*_leaves.npz`).
Интервальная проверка листьев: `python -I code/interval_cells.py <leaves.npz> <out.json> [--samples]`.
Лемма ячейки (выборка): `python -I code/lemma_audit.py 40 6000 <out.json>`.
Щели: `python -I code/sliver_check.py 20000 20261029`.
Аудитор независимого ядра: `python -I code/falsify_c3d.py` (путь к скрипту — абсолютный; сам скрипт и пути внутри него Windows).
mpmath 40 знаков: `python -I code/mp_check_constants.py`.
Прямая проверка 280 POVM: `python -I code/check_povm280_direct.py`; PCC-целочисленная: `python -I code/check_hermitian_qfim.py`.

## Зависимости
numpy 2.3.4, scipy 1.16.3, mpmath 1.3.0, python-flint 0.9.0 (arb, 192 бит). Python 3.11+.

## Полный строгий интервальный прогон (2026-10-29, C_NOTES 6f)

1. Выгрузка листьев: `python -I code/c3h_dump_all_leaves.py <аргументы как у c3d>` → `metrics/c3h_S-_f090_all_accepted_leaves.npy` (3 955 841 × 4).
2. Прогон 1 (12 воркеров; упал на `FLINT exception`, причина не установлена): `python -I code/interval_full_parallel.py 12` → `metrics/interval_full_progress.jsonl`, `logs/interval_full_parallel.log`.
3. Прогон 2 (8 воркеров, только недостающие чанки, исключения фиксируются на каждом листе): `python -I code/interval_resume_parallel.py 8` → `metrics/interval_resume_progress.jsonl`, `metrics/interval_resume_summary.json`, `logs/interval_resume_parallel.log`.
4. Независимая проверка покрытия: `python -I code/verify_interval_coverage.py` → `metrics/interval_coverage_check.json` (ожидаемый вердикт `COVERAGE_CONSISTENT`, код выхода 0).
5. Перепроверка 200 ячеек с наименьшим запасом после исправления правила λ_K: `python -I code/recheck_closest_leaves.py 200` → `metrics/recheck_closest_leaves.json`, `logs/recheck_closest_leaves.log` (ожидаемый вердикт `UNCHANGED`).
6. Точный тайлинг листов (O2): `python -I code/verify_tiling_exact.py` → `metrics/tiling_exact_check.json` (ожидаемый вердикт `TILING_EXACT`, ~25 с).
7. Итоговый документ стадии C: `STAGE_C_FINAL_PROOF.md` (вердикт CONDITIONAL; открытые пункты O1–O4 в §10).

Ожидаемое время: прогон 1 ≈ 7 ч на 12 процессах; прогон 2 ≈ 65 мин на 8 процессах для 722 чанков. Нагрузка на ПК: снижена (BELOW_NORMAL, BLAS = 1 на воркер).

## Полный прогон с исправленным правилом λ_K (O3, 2026-10-30, `o3_v2`)

Корень: `experiments/20261028-h-cat56-2-phase4/o3_v2/`.

1. Проверка манифеста: `cd experiments/20261028-h-cat56-2-phase4/o3_v2 && sha256sum -c SHA256SUMS_o3v2.txt`.
2. Предпроверка ядра и отрицательные тесты: `python -I code/preflight_v2.py` → `metrics/preflight_v2.json` (ожидаемый вердикт `PREFLIGHT_OK`).
3. Полный прогон: `python -I code/o3_run_v2.py 8` → `metrics/o3_progress.jsonl`, `metrics/o3_failures.jsonl`, `metrics/o3_summary.json`, `logs/o3_run_v2.log`. Возобновление: повторный запуск той же команды пропускает записанные чанки.
4. Ожидаемый результат: `all_chunks_covered_once`, `leaves_match_total`, `final_gap_positive` = true; `failed_this_run` = 0.

Прогон не воспроизводится побитово на другой машине без проверки SHA: все входы фиксированы по `SHA256SUMS_o3v2.txt`.

## Что не входит
- Математический аудит леммы и разделения (см. LEMMA_CELL_AUDIT.md §7; STAGE_C_FINAL_PROOF.md, вердикт CONDITIONAL). Закрыты O2 и O3; открыты O1 (независимость слабая–средняя) и O4 (соглашение D1 по первоисточникам).
- Причина `FLINT exception` первого прогона.
