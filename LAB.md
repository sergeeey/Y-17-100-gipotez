# LAB.md — точка входа для слепого оркестратора

> Ты открыл этот репозиторий и ничего не помнишь. Начни здесь. Этот файл отвечает на четыре вопроса:
> **что это · где мы · что связано с чем · какой следующий шаг.** Всё остальное — по ссылкам.

**Репо:** https://github.com/sergeeey/Y-17-100-gipotez · **Методология:** research → FL Full-Ladder + EstimandOps L0 + skeptic-triggers
**Source of truth для истории:** Obsidian vault (`C:\Users\serge\.claude\memory\`); этот репо — рабочая копия + всё новое.

---

## 1. Что это (30 секунд)

Экспериментальная **лаборатория cross-domain мостов**: каталог ~141 нерешённой научной задачи → поиск структурных мостов между задачами и реальными проектами → один дешёвый фальсифицирующий эксперимент на каждый мост **до** инвестиций.

Второй, мета-уровень (2026-09-06): лаборатория — **образцовый полигон** для всего стека инструментов (агенты, скиллы, правила, хуки). Каждый инструмент, применённый к реальной задаче, получает строку в [`tooling-eval/LEDGER.md`](tooling-eval/LEDGER.md): поймал / пропустил / шум.

---

## 2. Карта репозитория

| Путь | Что там | Когда открывать |
|---|---|---|
| **`registry/graph.yaml`** | **Единственный машиночитаемый граф**: задачи, проекты, мосты, гипотезы, артефакты, открытые вопросы + типизированные рёбра | Всегда первым после этого файла. Любое изменение статуса — сначала сюда |
| `registry/SCHEMA.md` | Словарь типов узлов/рёбер/статусов | Перед добавлением узла |
| `experiments/<id>/` | По одному FL-эксперименту на гипотезу (шаблон — `experiments/_template/`, 14 файлов) | При запуске гипотезы |
| `null_results/` · `parked/` · `pearl_registry/` | REJECT · ARCHIVE · побочные testable-находки. Каждый с `INDEX.md` | Перед любой новой гипотезой — grep по всем трём |
| `tooling-eval/LEDGER.md` | Реестр применения инструментов: что использовали, что поймало, что пропустило | После каждого применения агента/скилла/хука |
| `00-catalog/` | Три слоя каталога задач (raw 100 · verified 43 · skeptic-разбор) | Когда нужен источник задачи. **Skeptic-разбор читать первым** |
| `01-cross-domain-bridges/` | Развёрнутые описания мостов + H-7 контекст | Детали моста, не статус (статус — в graph.yaml) |
| `02-related-projects-context/` | ChernoffPy, May 1972, Revival Targets | Grounding мостов 2 и 3 |
| `03-methodology-rules/` | Execution rules, Submission Gate, ESV-скоринг, text↔figures check | Перед запуском и перед любой внешней публикацией |
| `.claude/memory/activeContext.md` | Текущий фокус, состояние, открытые вопросы (Checkpoint Fidelity) | Каждую сессию |
| `.claude/memory/decisions.md` | ADR: почему решили так | Перед тем как «улучшить» архитектуру |

---

## 3. Текущее состояние (сверять с `registry/graph.yaml`, он главнее)

| Мост | Гипотеза | Статус | Блокер / следующий шаг |
|---|---|---|---|
| B1 RMT ↔ Riemann ↔ Hi-C | H-B1-1a репликация r-stat на нулях Римана | **READY** | Запустить как пилот всего стека (позитивный контроль *лаборатории*, не науки) |
| B1 | H-B1-1b хроматин vs GUE | **BLOCKED** | Два независимых блокера: (1) upstream `ART-TAD-AUC` инвалидирован — ждёт Option A в H-7 TAD; (2) `Q-GOE-vs-GUE` не решён. Снятие одного не разблокирует |
| B2 Chernoff ↔ Neural ODE/UDE | H-B2-1 слой Neural-ODE удовлетворяет условиям теоремы Чернова | **NEEDS_FORMALIZATION** | Сначала доказательство применимости, потом тест |
| B3 May 1972 ↔ TDA EWS | H-B3-1 TDA опережает classical EWS на известных коллапсах | **READY_TO_SCOPE** | Найти датасет Mangal/GloBI с известной датой коллапса |
| B4–B6 Frontier R&D / TOFT / RAF | — | **UNVERIFIED_SOURCE** | Пользователь: реальны ли проекты? До ответа — не в очереди |

**Открытый теоретический вопрос:** `Q-GOE-vs-GUE` — TAD-проект утверждает класс A (GUE) для fused-хроматина через Altland-Zirnbauer; не решён.

---

## 4. Инварианты лаборатории (нарушение = стоп)

1. **Гипотеза не существует, пока нет узла в `graph.yaml`** с `l0_type`, `kill_criterion`, `evidence`, `status`.
2. **L0 gate первым**: Descriptive / Predictive / Causal — до выбора tier FL. Causal → `estimand.md` с DAG.
3. **Kill-criterion до запуска**, три исхода: KILLED / CONFIRMED / LEAD. «Почти» не бывает.
4. **Новый NULL → ретроскан**: найти все узлы, до которых от него ведёт `depends_on`/`grounds`, и пересмотреть их статус *в той же сессии*. (Прецедент: PARKED-файл 12 дней ссылался на инвалидированный результат.)
5. **Верификация не переносится**: вердикт для артефакта A не действует для B из-за общего названия/автора (Gate 1, `artifact-provenance-gates`). H-7 GeoSpectra ≠ H-7 TAD.
6. **Evidence labels** на каждом числе: `VERIFIED-REAL` / `VERIFIED-SYNTHETIC` / `HYPOTHESIS` / `UNVERIFIED` / `CONFLICT`.
7. **Skeptic — с асимметрией контекста**: только `claim.md` + код, без истории рассуждений.
8. **Ничего наружу без Submission Gate** (`03-methodology-rules/Submission Gate Protocol (HARD RULE).md`).
9. **Каждый применённый инструмент → строка в LEDGER.** Без этого мета-цель «протестировать стек» — не данные, а впечатление.

---

## 5. Как добавить гипотезу (протокол, 6 шагов)

```
1. grep -i "<ключевое слово>" null_results/INDEX.md parked/INDEX.md pearl_registry/INDEX.md
2. Узел в registry/graph.yaml: id, l0_type, kill_criterion, evidence: HYPOTHESIS, status: proposed, рёбра grounds/depends_on
3. mkdir experiments/<YYYYMMDD-slug> && cp experiments/_template/* туда
4. claim.md: Zero-Signal Gate → L0 → Natural Language Statement → «что это НЕ значит» — ДО данных
5. Запуск: controls → floor/ceiling (Step 4a) → run → skeptic (asymmetric) → decision.md
6. Вердикт → обновить graph.yaml status + INDEX нужной папки + activeContext + LEDGER — в ту же сессию
```

---

## 6. Следующий шаг (одно действие)

**Пилот:** провести `H-B1-1a` через весь стек (шаги 3–6 выше). Ожидаемый ответ известен (r̄ ≈ 0.6027, GUE), поэтому это позитивный контроль самой лаборатории: если стек не воспроизводит известный факт — автоматизировать его рано.

---

*Создан 2026-09-06. При расхождении между этим файлом и `registry/graph.yaml` — прав граф; исправь этот файл.*
