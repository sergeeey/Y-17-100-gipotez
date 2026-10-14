# oracle_adequacy.md — FL Step 2b (Oracle Adequacy Gate)

Оракул = связка «детектор → graph-level AUROC → bootstrap-CI по графам → ΔAUC против бейзлайнов» (`rstat_lib.py`). Вопрос: умеет ли он отличить истинный исход от правдоподобного ложного?

## Каноническая шкала (6 проверок)
| Проверка | Ответ | Основание |
|---|---|---|
| Gameable? | нет в рамках S2/S4: порог alarm задаётся по чистым репликам, знаки детекторов фиксированы заранее | claim.md, раздел «Детекторы» |
| Real vs theater? | S3 — реальные локальные тексты и реальные эмбеддинги; S4 — реальные чанки + шаблонный яд (честно синтетический, ограничение заявлено) | claim.md Constraints |
| Negative control (B)? | чистый против чистого: AUROC 0.575, 95 % CI [0.465, 0.688] ∋ 0.5; метка-шаффл 0.539 | `metrics/s2.json` oracle_adequacy |
| Positive control (G)? | ER против несвязных блоков: AUROC = 1.000; мутация «знак детектора» → 0.000 | там же |
| Reproducible? | да, seed 20261014, идентичный повторный прогон | substrate_gate.md |
| Measures the intent? | **частично** (`WEAK`): AUROC на графах измеряет предсказательную силу статистики; не измеряет защиту реального RAG | claim.md «What this does NOT mean» |

`Q = B AND G = yes` → **ADEQUATE с пометкой WEAK по последнему пункту**; все downstream-claim'ы наследуют слепое пятно «яд шаблонный, не оптимизированный под retriever».

## FL-addendum
| Проверка | Ответ |
|---|---|
| Independence | оракул (AUROC/bootstrap) независим от генерации гипотезы по построению; независимое ревью кода — `Agent(reviewer)` + скептик Step 8a в конце |
| Injected-error catch | да: мутация знака → AUROC 0.0; метки перемешаны → ≈0.5 |
| No data leakage | яд и benign-пулы строятся из чанков, не входящих в проверяемую подвыборку; held-out часть пула используется для B-growth (проверяется в S4, пишется в `metrics/s4.json`) |

**Verdict: `ADEQUATE` (WEAK по «measures the intent»).**
