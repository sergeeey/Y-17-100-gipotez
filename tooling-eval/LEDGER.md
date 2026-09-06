# tooling-eval/LEDGER.md — реестр применения инструментов стека

> Мета-цель лаборатории №1: **протестировать все агенты, скиллы, правила, хуки на реальных задачах.**
> Без этого файла результат теста — впечатление. С ним — данные.
> Одна строка на одно применение. Заполнять в ту же сессию, не по памяти.
> **Сводку считать grep'ом, не в голове** — первая же ручная сводка (2026-09-06) содержала off-by-one, пойманный reviewer'ом.

## Словарь исхода

| Исход | Смысл |
|---|---|
| `CAUGHT` | Инструмент нашёл реальную проблему/риск, который иначе прошёл бы |
| `OK` | Сработал штатно, нашёл ожидаемое, ничего не пропустил |
| `MISSED` | Должен был поймать, но не поймал (известно из другого источника) |
| `NOISE` | Сработал ложно / не по делу / отвлёк |
| `BLOCKED` | Не смог применить (нет доступа, нет данных, не подключён) |
| `NOT-YET` | Запланирован, ещё не применялся |

Правило: **одна строка = один исход.** Если инструмент сделал две разные вещи (штатно отработал И поймал побочное) — две строки.

## Реестр

| Дата | Инструмент | Тип | Задача | Исход | Что именно / комментарий |
|---|---|---|---|---|---|
| 2026-09-06 | `project_classifier` hook | hook | классификация проекта при старте | `OK` | research, margin=6 — верно |
| 2026-09-06 | `project_classifier` hook | hook | побочно: проверка наличия `.git` | `CAUGHT` | папка оказалась архивом без `.git` → инициировали репо |
| 2026-09-06 | `routing-floor` hook | hook | детект research-задачи по ключевому слову | `NOISE` | сработал на слово «эксперимент» в запросе про scaffolding репо; L0 gate к созданию репо неприменим |
| 2026-09-06 | `resource-router` hook | hook | рекомендация role chain / модели | `NOISE` | предложил builder→tester для задачи «предложи варианты архитектуры» (design, не implement) |
| 2026-09-06 | `memory-guard` hook | hook | напоминание обновить activeContext после коммита | `OK` | сработал, activeContext обновлён |
| 2026-09-06 | `Grep` (secrets scan) | tool | скан папки на секреты/PII перед публикацией | `OK` | 0 секретов; 1 ложный хит на слово «token» в тексте |
| 2026-09-06 | `Grep` (third-party names) | tool | поиск имён третьих лиц перед публикацией | `CAUGHT` | нашёл ссылки на неотправленную переписку и Discord-транскрипт в файле GeoSpectra → файл исключён из публичного репо |
| 2026-09-06 | `gh` CLI | tool | создание публичного репо + push | `OK` | `gh repo create --public --source --push` с первого раза |
| 2026-09-06 | `AskUserQuestion` | tool | выбор варианта структуры + решение о приватности | `OK` | 2 вопроса, 2 ответа, без переспросов |
| 2026-09-06 | `artifact-provenance-gates` (Gate 1) | rule | идентичность артефактов при построении графа | `CAUGHT` | заставил разделить `ART-TAD-AUC-0.99998` (fit) и `ART-TAD-R-HONEST` (measurement) как разные узлы вместо одного «результата H-7» |
| 2026-09-06 | FL `experiments/_template` (Claude-cod-top-2026) | template | переиспользование вместо написания своего | `OK` | 14 файлов скопированы; `dependency_graph.yaml` внутри шаблона — independence-профиль, не граф проекта; дублирования с `registry/graph.yaml` нет |
| 2026-09-06 | `plan-mode-guard` hook | hook | milestones 3/5/10 файлов | `NOISE` | план был утверждён через `AskUserQuestion` (вариант C + таблица компонентов); хук видит только `EnterPlanMode` как канал утверждения |
| 2026-09-06 | `reviewer` agent (sonnet, read-only) | agent | pre-commit консистентность LAB.md↔SCHEMA↔graph.yaml↔INDEX↔ADR, 8 проверок | `CAUGHT` | 4 находки (2 MEDIUM: off-by-one в сводке LEDGER, обход протокола в parked/INDEX; 2 LOW: неполный блокер H-B1-1b в LAB.md, двусмысленное «3 моста» в ADR-003). Ядро graph.yaml — чистое. MEDIUM перепроверен grep'ом до правки |
| 2026-09-06 | `commit-test-gate` hook (Stop) | hook | блок завершения хода: `.py` изменён, pytest не запускался | `CAUGHT` | вынудил написать тесты, включая негативный контроль — реплику инцидента 2026-05-28; валидатор доказанно умеет падать |
| 2026-09-06 | `scripts/lab_check.py` + pytest | tool | валидация graph.yaml, 3 теста (1 позитивный + 2 негативных контроля) | `OK` | 23 узла / 19 рёбер, инварианты 1–3; 3/3 passed |
| 2026-09-06 | `ruff` format/check + PostToolUse formatter hook | tool | линт/формат `scripts/`, `tests/` | `CAUGHT` | ping-pong 88↔100 символов между `ruff format` (default) и хуком → закреплено `line-length=100` в `pyproject.toml`; затем flip RUF100↔E402 при включении правила `E` — 2 лишних круга |
| 2026-09-06 | `submission-gate` hook | hook | сработал на текст уведомления reviewer'а | `NOISE` | «external-facing artifact» — коммит scaffolding'а в публичный репо ≠ submission; триггер по слову «ready» |
| 2026-09-06 | `routing-floor` hook (2-й раз) | hook | сработал на слово «hypothesis» в уведомлении reviewer'а | `NOISE` | тот же режим отказа, что и в 1-й раз → счётчик pearl №1: 2/3 |
| 2026-09-06 | `resource-router` hook (2-й раз) | hook | рекомендация explorer→builder→reviewer для fix-прохода | `OK` | на этот раз по делу |
| — | `skeptic` agent (asymmetric context) | agent | Step 8a пилота H-B1-1a | `NOT-YET` | |
| — | EstimandOps L0 gate | rule | классификация H-B1-1a | `NOT-YET` | |
| — | Floor–Ceiling (FL Step 4a) | rule | пилот H-B1-1a | `NOT-YET` | ожидание: floor = r̄ Poisson ≈ 0.386, ceiling = GUE 0.6027; проверить, что метрика вообще различает |
| — | `analyst` / `hypothesis-arbiter` / `cross-domain` skills | skill | мосты B2, B3 | `NOT-YET` | |
| — | `verifier` agent | agent | source trace (FL Step -4) для каталога | `NOT-YET` | |
| — | `graphify` meta-graph query | tool | «уже есть в моих репо?» перед расширением `lab_check` | `NOT-YET` | |

## Сводка (считать командой ниже, не вручную)

```bash
grep -E '^\| (2026-[0-9-]+|—) \|' tooling-eval/LEDGER.md | awk -F'|' '{gsub(/ /,"",$6); print $6}' | sort | uniq -c
```

| Исход | Кол-во |
|---|---|
| CAUGHT | 6 |
| OK | 8 |
| MISSED | 0 |
| NOISE | 5 |
| BLOCKED | 0 |
| NOT-YET | 6 |

**Наблюдение после первой сессии:** все 5 `NOISE` — хуки с keyword-эвристикой, не различающие тип задачи (scaffolding vs research) и источник текста (запрос пользователя vs уведомление агента). `routing-floor` — 2/3 до порога действия (pearl №1). Все 6 `CAUGHT` — либо инструменты с реальным входом (grep, reviewer, pytest), либо хуки, проверяющие **состояние** (нет `.git`, `.py` изменён без тестов), а не **слова**. Гипотеза для pearl: state-based хуки ловят, keyword-based шумят — проверять на следующих 20 строках.
