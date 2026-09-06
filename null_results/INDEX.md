# null_results/INDEX.md — реестр фальсифицированных гипотез

_Запись здесь означает: утверждение проверено и **ОПРОВЕРГНУТО**. Не повторять без принципиально другого подхода._
_Перед любой новой гипотезой: `grep -i "<ключевое слово>"` по этому файлу._

## Как добавить запись

При вердикте REJECT в `decision.md`:
1. Скопировать заполненный `decision.md` в `null_results/<id>-<slug>.md` (Kill Analysis обязателен: что убито / что НЕ убито / Relaxation Map)
2. Добавить строку в таблицу
3. **Ретроскан:** в `registry/graph.yaml` найти все узлы, до которых от убитого ведут `grounds`/`depends_on`, пересмотреть их статус в ту же сессию
4. Обновить статус узла в `registry/graph.yaml` → `killed`

## Index

| id | date | slug | verdict | why falsified (≤10 words) | retroscan done |
|---|---|---|---|---|---|
| H-B3-1c | 2026-09-06 | lakes-tda-ews-surrogate-null-v1 | REJECT | AR(1) null too simple — real negative-control lakes have extra structure (5/5 still false-positive) | Да — нет узлов, зависящих от H-B3-1c; H-B3-1/H-B3-1b (родители) не затронуты, их CRITERION_INVALID вердикты остаются в силе |

> Историческая справка (не эксперимент этой лаборатории, но релевантный NULL upstream): `ART-TAD-AUC-0.99998` инвалидирован 2026-05-16 в проекте H-7 TAD — label circularity. Учтён в `registry/graph.yaml` как артефакт со статусом `invalidated`, ребро `invalidates` от `ART-TAD-R-HONEST`.
