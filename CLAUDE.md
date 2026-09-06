# Y-17 — 100 гипотез / Cross-Domain Bridge Lab

## PROJECT
- **Goal:** Каталог ~141 нерешённых научных задач среднего масштаба (100 внешних + 43 моих, verified) + проверка cross-domain мостов между ними и реальными проектами (H-7 chromatin/RMT, ChernoffPy, May 1972 stability-complexity)
- **Stack:** Python (numpy, requests для базовых экспериментов), Obsidian markdown для документации
- **Status:** Early exploration. Один мост (Riemann/RMT Phase 1a) готов к запуску, остальное требует scoping

## READ FIRST (в этом порядке)
0. `LAB.md` — точка входа для слепого оркестратора: что это, где мы, что связано, следующий шаг
0.5. `registry/graph.yaml` — единственный машиночитаемый граф связей; **статус меняется сначала здесь**, markdown вторичен
1. `README.md` — полная навигация по структуре папки
2. `00-catalog/Open Problems Catalog — Skeptic Assessment of the 100-item version (2026-09-06).md` — как относиться к каталогу 100 задач (реальные источники, но шаблонная аргументация)
3. `01-cross-domain-bridges/Cross-Domain Bridge Lab — Project.md` — полный разбор мостов, что verified/blocked

## ALWAYS DO
- Гипотеза не существует, пока нет узла в `registry/graph.yaml` (l0_type, kill_criterion, evidence, status) — см. `registry/SCHEMA.md`
- Каждый применённый агент/скилл/хук/правило → строка в `tooling-eval/LEDGER.md` в ту же сессию (мета-цель: тест стека = данные, не впечатление)
- Новый NULL/инвалидация → ретроскан по рёбрам `grounds`/`depends_on` в graph.yaml в ту же сессию
- Перед тем как строить на любом "мосте" из этой папки — проверить, не изменился ли статус upstream-проекта (см. прецедент: PARKED-файл про Riemann/RMT ссылался на результат, инвалидированный за 12 дней до написания заметки)
- Разделять Pipeline vs Experiment в любом коде (см. `03-methodology-rules/lesson-hypothesis-execution-rules.md`)
- Explicit kill-criterion ДО запуска эксперимента, не после
- Evidence labels: `VERIFIED-REAL` / `VERIFIED-SYNTHETIC` / `HYPOTHESIS` / `UNVERIFIED` / `CONFLICT`
- Три исхода эксперимента: KILLED / CONFIRMED / LEAD — никаких "почти"

## CRITICAL CONTEXT — не наступать на грабли снова
- **"H-7 GeoSpectra Lab" ≠ "H-7 TAD Spectral Diagnostic"** — два разных проекта (физика vs биология), случайно делят номер. См. файлы в `01-cross-domain-bridges/` с явными пометками.
- **Биологический r-statistic результат (AUC=0.99998) INVALIDATED** — label circularity, не биологический сигнал. Redesign Option A не завершён. Не сравнивать с Riemann zeros, пока это не исправлено.
- **Frontier R&D / TOFT / RAF Theory / CatlyNet — НЕ НАЙДЕНЫ нигде в исходном Obsidian vault** после grep-проверки. Если пользователь ссылается на них как на существующие проекты — уточнить, где физически лежат, прежде чем строить на них выводы.

## NEVER
- Не подавать/публиковать что-либо из этой папки без прогона через Submission Gate (`03-methodology-rules/Submission Gate Protocol (HARD RULE).md`) — 4 gate'а: skeptic run, checklist, consistency check, 24h cooling-off
- Не доверять числовым score'ам из raw-каталога (`00-catalog/100 Open Problems...`) как реальному ranking'у — это precision theater поверх сжатого 7-10 диапазона, не калиброванный инструмент
- Не путать "название задачи реально существует в источнике" с "объяснение задачи было реально исследовано" — 13 идентичных шаблонных фраз найдены grep'ом в raw-каталоге

## Origin
Перенесено из Obsidian vault (`C:\Users\serge\.claude\memory\`) 2026-09-06 в рамках сессии Claude Code. Vault остаётся source of truth для истории — при существенных изменениях синхронизировать оба места.
