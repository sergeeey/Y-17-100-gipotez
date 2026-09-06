# activeContext.md — Y-17 100 gipotez

## Scope Fence
- **Goal:** [PLAN, не факт] Оценить и начать проверку cross-domain мостов между каталогом ~141 открытых научных задач и реальными проектами (H-7 chromatin, ChernoffPy, May 1972)
- **Boundary:** Эта папка + чтение (не запись) в исходный vault `C:\Users\serge\.claude\memory\` при необходимости сверки
- **Done when:** Хотя бы один мост прошёл полный цикл kill-criterion → эксперимент → KILLED/CONFIRMED/LEAD
- **NOT NOW:** Frontier R&D / TOFT / RAF — заблокированы до подтверждения существования; полный Hypothesis Portfolio (128+ гипотез из ARCHCODE и др.) — отдельный, не связанный проект

## Current Focus
**[WS: lab-core] Ядро лаборатории построено (2026-09-06), вариант C (ADR-002).** Файлы: `LAB.md`, `registry/{SCHEMA.md,graph.yaml}`, `experiments/_template/` (14 файлов из Claude-cod-top-2026), `null_results/parked/pearl_registry INDEX.md`, `tooling-eval/LEDGER.md`, `.claude/memory/decisions.md` (ADR-001..004). Статус: pre-commit review (yaml validation + reviewer agent) → commit → push.

**[WS: pilot-H-B1-1a] СЛЕДУЮЩИЙ ШАГ:** пилот `H-B1-1a` (Riemann zeros r-stat, известный ответ r̄≈0.6027 GUE) через ПОЛНЫЙ FL стек как позитивный контроль лаборатории: L0 → claim.md → estimand → controls → floor/ceiling (Step 4a: floor=Poisson 0.386, ceiling=GUE 0.6027) → run → skeptic (asymmetric) → decision → graph.yaml + LEDGER. Kill: |r̄−0.6027| ≥ 0.01 → pipeline broken.

Phase 1b (H-B1-1b, хроматин) — BLOCKED: upstream `ART-TAD-AUC-0.99998` invalidated; ждёт Option A в H-7 TAD + решение `Q-GOE-vs-GUE`.

## Project State
- **Repo:** https://github.com/sergeeey/Y-17-100-gipotez — PUBLIC, created 2026-09-06, commit d50597f (initial import). [VERIFIED]
- **Excluded from public repo (.gitignore):** `H-7 GeoSpectra Lab (DIFFERENT project…).md` — third-party correspondence refs (Tom Lawrence). Local copy kept. User may override.
- **New meta-goal (2026-09-06, user):** make this an *exemplary experimental lab* — memory/structure/hypothesis-graph designed up front so a blind orchestrator can operate; use it to test the whole tool/agent/methodology stack. Structure variant NOT yet chosen — options presented to user.
- **FL template source (reuse, don't reinvent):** `D:\Claude-cod-top-2026\experiments\_template\` (14 files) [VERIFIED]
- **Files transferred:** 15 (2026-09-06)
- **Bridges scoped:** 3 (RMT/Riemann — READY/BLOCKED split; ChernoffPy/UDE — needs formalization; May1972/TDA — ready to scope)
- **Bridges blocked pending user input:** 3 (Frontier R&D, TOFT/SMT, RAF Theory)

## Architecture (файлы этой папки)
- `00-catalog/` — источники задач (raw + verified subset + skeptic assessment)
- `01-cross-domain-bridges/` — главный рабочий файл + H-7 контекст (два разных проекта!)
- `02-related-projects-context/` — ChernoffPy, May 1972
- `03-methodology-rules/` — переиспользуемые правила (execution rules, submission gate, ESV scoring)

## Quick Commands
```bash
# Phase 1a — Riemann zeros sanity check
pip install numpy requests
python phase1a_riemann_check.py  # код в Cross-Domain Bridge Lab — Project.md
```

## Open Questions (для пользователя)
1. Frontier R&D / TOFT / RAF Theory — реальны на другом компьютере, или нет?
2. Доступен ли этот E:\ путь с других ПК (тот же физический диск / сетевая шара / нет)?

---
*Создан: 2026-09-06 при переносе из Obsidian vault.*

## Auto-commit log
- [2026-09-06 10:58] `d50597f`: chore: initial import of Y-17 Cross-Domain Bridge Lab from Obsidian vault
