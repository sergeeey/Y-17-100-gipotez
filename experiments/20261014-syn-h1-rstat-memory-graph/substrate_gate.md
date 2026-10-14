# substrate_gate.md — FL Step 2a (Verification Substrate Gate)

Дата: 2026-10-14. Вопрос: можно ли честно прогнать тест на этой инфраструктуре? (не вопрос об истинности claim'а)

| Проверка | Результат | Доказательство |
|---|---|---|
| Environment | pinned в записи, воспроизводимо | Python 3.13.2, numpy 2.3.4, scipy 1.16.3, networkx 3.5, scikit-learn 1.7.2, pytest 8.4.2; seed 20261014; повторный `python run.py s2` дал идентичный `metrics/s2.json` |
| Code provenance | известна | `rstat_lib.py` (написан в сессии, 11 тестов `tests/test_syn_h1_rstat.py`); константы Poisson/GOE/GUE сверены симуляцией (S2 A) и с Atas et al. arXiv:1212.5611 по аннотации |
| Dependencies | lockfile проекта нет; версии записаны выше | `[WEAK]`: pin без lockfile |
| Exactness | вердикт не зависит от округления | вырожденные зазоры: TOL 1e-9 vs 1e-12 дают идентичные доли на решётках |
| Test-harness sanity | smoke-тесты пройдены | 11/11 passed; ruff clean |
| Artifacts | пишутся в файл | `metrics/s2.json` (и далее `s3.json`, `s4.json`) |
| Security/integrity | хуки не искажают прогон | известный шум: PreToolUse блокирует `python -c` (обход: скрипты-файлы); `commit_test_gate`/`post_commit_memory` — не влияют на вычисления |
| Clean state | scope известен | в рабочем дереве >80 чужих незакоммиченных путей (другие сессии: LAB.md, activeContext.md, эксперименты Lovasz/Chernoff…); внутри `experiments/20261014-syn-h1-rstat-memory-graph/` и своих `tests/test_syn_h1_rstat.py` изменения только мои; коммиты — только по явным путям |

**Verdict: `READY`** (с пометкой: pin без lockfile → `[WEAK]` воспроизводимость на другой машине).
Данные S3/S4 берутся из локальных корпусов и локального Ollama (`nomic-embed-text`); внешней сети не требуют.
