# manifest.md — 20261014-syn-h1-rstat-memory-graph

## Воспроизведение
```
cd experiments/20261014-syn-h1-rstat-memory-graph
export SYNH1_CACHE=<dir outside repo>     # тексты частного vault (C3) остаются там, не в репозитории
python run.py prep      # корпуса C1-C3, чанки, эмбеддинги nomic-embed-text (локальный Ollama), яд/benign-пулы
python run.py s2        # контроли инструмента -> metrics/s2.json
python run.py s3        # посылка на чистых графах -> metrics/s3.json
python run.py e1        # exploratory: ещё более разреженные kNN (k=2,3) -> metrics/e1_exploratory.json
python run.py s4        # детекция + контроли + решающие правила -> metrics/s4.json, s4_raw.json
python -m pytest tests/test_syn_h1_rstat.py -q
```
Seed 20261014. Python 3.13.2, numpy 2.3.4, scipy 1.16.3, networkx 3.5, scikit-learn 1.7.2.

## Данные
- C1: заметки проекта Y-17 (md, без `.git`, `.claude`, `lit`, `papers`, `metrics` и без папки этого эксперимента, чтобы шаблонная фраза яда не попала в корпус); C2: `~/.claude/skills/**/*.md`; C3: `~/.claude/memory/**/*.md`, файлы 1–100 КБ.
- Чанки ≥400 симв. (≤1500), ≥60 слов, ≤8 на файл; эмбеддер `nomic-embed-text` через Ollama с префиксом `search_document: `.
- В репозиторий попадают только агрегаты (`metrics/*.json`) и код; тексты чанков и эмбеддинги — в кэше вне репозитория (приватность vault).

## Артефакты
`claim.md` (pre-registration + Addendum A1), `estimand.md`, `experiment.yaml`, `source_register.md`, `novelty_check.md`, `controls.md`, `substrate_gate.md`, `oracle_adequacy.md`, `rstat_lib.py`, `corpus.py`, `detect.py`, `run.py`, `metrics/`.

## Коммиты
`62660d1` pre-registration · `730b778` Addendum A1 (до S3/S4) · результатный коммит (S2–S4, decision, null_results) — следующий в ветке `research/syn-h1-rstat-memory`; кроме `run.py` команд: `pc`, `s4pc`, `s3decide`, `s4decide`, `e1`; аудит скептика — `audit/`.
