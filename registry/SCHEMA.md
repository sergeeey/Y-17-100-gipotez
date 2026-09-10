# registry/SCHEMA.md — словарь графа лаборатории

Один файл `graph.yaml`: список `nodes` и список `edges`. Никаких других реестров. Если что-то нельзя выразить узлом или ребром — сначала расширь этот словарь, потом добавляй.

## Узлы (`nodes[]`)

Обязательные поля для всех: `id`, `type`, `title`, `status`, `evidence`, `source` (файл/URL, где это описано), `updated` (YYYY-MM-DD).

| `type` | Что это | Дополнительные обязательные поля |
|---|---|---|
| `problem` | Нерешённая задача из каталога | `catalog` (raw-100 / phase1-43), `catalog_ref` (номер/ID в каталоге) |
| `project` | Реальный внешний проект (свой или чужой), к которому строится мост | `path` (локальный путь или `null`), `owner` |
| `bridge` | Предполагаемый структурный изоморфизм между problem и project | `mechanism` (одно предложение: какой механизм переносится) |
| `hypothesis` | Фальсифицируемое утверждение внутри моста | `l0_type` (descriptive / predictive / causal), `kill_criterion`, `experiment_dir` (или `null`), `fl_tier` (micro / standard / full) |
| `artifact` | Конкретный результат/число/файл с датой и происхождением (Gate 1: artifact identity) | `date_created`, `provenance` (prediction / fit / illustration / measurement / replication) |
| `question` | Открытый теоретический вопрос без гипотезы (пока) | `blocks` (список id, которым мешает нерешённость) — дублируется ребром `blocks` для машиночитаемости |
| `substrate` | Независимая базовая система/датасет/модель/семейство теорем, на которой проверяется гипотеза — делает graph-inflation видимым (независимый аудит 2026-09-10: 153 узла могут скрывать всего 4-6 реальных субстратов) | `category` (model / dataset / theorem_family / open_problem) |

### `evidence_mode` (опционально, только `hypothesis`/`artifact` — ортогонально `status`)

Не вердикт — описывает, КАКОЙ ТИП проверки дал результат, потому что одно слово `confirmed`
смешивает структурно разные заявления (находка независимого аудита, 2026-09-10):

- `empirical` — реальные/полевые/наблюдательные данные (включая канонический вычисленный
  математический датасет вроде нулей дзета-функции), статистическое сравнение, подвержено шуму
- `exhaustive` — исчерпывающая проверка КАЖДОГО случая в конечном, полностью заданном
  пространстве (без выборки)
- `deductive` — следует из доказательства/алгебраического тождества/определения, не из
  прогона данных (проверенная теорема — не то же самое, что подтверждённая данными гипотеза)
- `formal` — машинно-проверенное доказательство (Lean/Coq) или символьный вывод
- `simulation` — синтетические/симулированные данные вместо реальной системы (не путать с
  `VERIFIED-SYNTHETIC` в `evidence` — то поле про тестовые данные, это поле про предмет claim'а)

### `verification_strength` (опционально, только `hypothesis`/`artifact` — ортогонально `status`)

Называет, насколько независимой была реальная проверка FL Step 8a, по собственной шкале
проекта (`falsification-ladder.md` § Independent Verification Strength Ladder) — сведе́ние
этого к одному слову «reviewer confirmed» прячет реальную силу проверки:

- `none` — независимая проверка не запускалась
- `weak` — та же модель, тот же контекст, либо та же модель + изолированный контекст без
  смены кода/метода
- `medium` — та же модель, изолированный контекст, но ГЕНУИННО независимо написанный
  код/метод (другая реализация того же вычисления)
- `strong` — другая модель, другой инструмент (Lean/Coq/символьный солвер), независимо
  построенная cross-implementation (напр. другая библиотека), либо внешняя человеческая
  репликация

### `status` (по типу)

- `problem`: `open` / `partially_solved` / `solved` / `disputed`
- `project`: `active` / `hold` / `archived` / `unverified_source`
- `bridge`: `proposed` / `verified_grounding` / `unverified_source` / `rejected`
- `hypothesis`: `proposed` / `ready` / `ready_to_scope` / `needs_formalization` / `blocked` / `running` / `killed` / `confirmed` / `lead` / `parked`
- `artifact`: `valid` / `invalidated` / `stale` / `superseded`
- `question`: `open` / `resolved`
- `substrate`: `active` / `exhausted` / `blocked` / `archived`

### `evidence` (единый набор из CLAUDE.md)

`VERIFIED-REAL` · `VERIFIED-SYNTHETIC` · `HYPOTHESIS` · `UNVERIFIED` · `CONFLICT`

## Рёбра (`edges[]`)

Поля: `from`, `to`, `type`, `note` (опционально), `since` (YYYY-MM-DD).

| `type` | Смысл | Правило ретроскана |
|---|---|---|
| `grounds` | A является основанием для B (файл/проект → мост/гипотеза) | Если A → `invalidated`/`stale`, все B → пересмотр статуса в ту же сессию |
| `depends_on` | B не может быть выполнен без результата A | Если A `killed`/`invalidated` → B ≥ `blocked` |
| `invalidates` | A показал, что B неверен | Обязательно поставить B.status = `invalidated`; проверить всё, что `grounds`/`depends_on` B |
| `supersedes` | A заменяет B (новая версия) | B.status = `superseded` |
| `blocks` | Нерешённый A мешает B | Снятие блока = A.status `resolved` |
| `links_to` | Слабая тематическая связь без зависимости | Не участвует в ретроскане |
| `collides_with` | Именной конфликт: два разных объекта под одним названием | Никогда не сливать; статусы не переносятся (Gate 1) |
| `tested_on` | `hypothesis`/`artifact` A проверялась на субстрате B | Не участвует в ретроскане; участвует в substrate-diversity отчёте `lab_check.py` |

## Инварианты (проверяются вручную до появления `lab check`)

1. Каждый `hypothesis` имеет ≥1 ребро `grounds` входящее и непустой `kill_criterion`.
2. Каждый `artifact` с `status: invalidated` имеет ≥1 входящее ребро `invalidates`.
3. Нет `hypothesis` со `status: ready`, у которой какой-либо `depends_on`-предок `invalidated`/`killed`/`stale`.
4. Каждый id уникален; рёбра ссылаются только на существующие id.
5. У каждого узла `updated` не старше даты последнего изменения его статуса.

Нарушение 3 — ровно тот класс ошибки, что уже случился (PARKED Riemann → инвалидированный AUC). Проверять первым.
