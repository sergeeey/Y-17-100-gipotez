# parked/INDEX.md — реестр отложенных (валидных, но деприоритизированных)

_Запись здесь означает: утверждение валидно, но отложено. Вернуться, когда сработает revival condition._
_Перед новой гипотезой: `grep -i` по этому файлу — не дублировать отложенную работу._

## Как добавить запись

При вердикте ARCHIVE в `decision.md`:
1. Скопировать заполненный `decision.md` в `parked/<id>-<slug>.md`
2. Добавить строку: почему отложено + **измеримое** условие возврата (не «когда будет время»)
3. Статус узла в `registry/graph.yaml` → `parked`

**Второй допустимый класс записей — `blocked-not-parked`:** гипотеза, у которой в `graph.yaml` статус `blocked` (заблокирована зависимостью, не решением) и **нет** `decision.md` с вердиктом ARCHIVE. Такие строки допускаются здесь только для того, чтобы grep по одному файлу показывал всё отложенное; в колонке `graph node` обязательно явно указан реальный статус. Правило: `blocked` в графе ≠ `parked`; не менять статус графа ради строки в этом файле.

## Index

| id | date | slug | why parked | revival condition (measurable) | graph node |
|---|---|---|---|---|---|
| H-B1-1b | 2026-09-06 | riemann-vs-chromatin-r-stat | upstream artifact `ART-TAD-AUC-0.99998` invalidated; note `[PARKED] Riemann via RMT` is stale (written 12 days after invalidation) | H-7 TAD Option A redesign produces a **new** artifact with honest AUC and pre-registered kill-criterion; `Q-GOE-vs-GUE` resolved or explicitly bracketed | `H-B1-1b` (status: `blocked`, not `parked` — blocked by dependency, not by choice) |
| B4/B5/B6 | 2026-09-06 | frontier-toft-raf-unverified | source projects not found in vault (grep = 0) | user confirms projects exist and gives path, OR confirms they were LLM-generated → then move to `null_results` as `REFUSE(no_source)` | `B4-FRONTIER`, `B5-TOFT`, `B6-RAF` (status: `unverified_source`) |
