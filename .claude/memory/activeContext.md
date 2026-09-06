# activeContext.md — Y-17 100 gipotez

## Scope Fence
- **Goal:** [PLAN, не факт] Оценить и начать проверку cross-domain мостов между каталогом ~141 открытых научных задач и реальными проектами (H-7 chromatin, ChernoffPy, May 1972)
- **Boundary:** Эта папка + чтение (не запись) в исходный vault `C:\Users\serge\.claude\memory\` при необходимости сверки
- **Done when:** Хотя бы один мост прошёл полный цикл kill-criterion → эксперимент → KILLED/CONFIRMED/LEAD
- **NOT NOW:** Frontier R&D / TOFT / RAF — заблокированы до подтверждения существования; полный Hypothesis Portfolio (128+ гипотез из ARCHCODE и др.) — отдельный, не связанный проект

## Current Focus
**[WS: lab-core] Ядро лаборатории построено (2026-09-06), вариант C (ADR-002).** Файлы: `LAB.md`, `registry/{SCHEMA.md,graph.yaml}`, `experiments/_template/` (14 файлов из Claude-cod-top-2026), `null_results/parked/pearl_registry INDEX.md`, `tooling-eval/LEDGER.md`, `.claude/memory/decisions.md` (ADR-001..004). **CLOSED 2026-09-06 — commit `f021de1` pushed** после чеклиста: lab_check OK, ruff OK, pytest 3/3, reviewer 4 находки исправлены. `[VERIFIED]`

**[WS: pilot-H-B1-1a] CLOSED 2026-09-06 — PROMOTE [WEAKENED].** Полный FL Full-Ladder пройден: ZSG → L0 (descriptive) → estimand → source trace (Atas 2013 констант ы web-verified) → substrate gate (поймал округление 0.60266 vs точное 0.6026578 — до прогона) → controls (GUE 0.6006 ✓, GOE 0.5310 ✓, Poisson 0.3867 kill fired ✓) → floor/ceiling → run → 7 no-collapse → 3 stress → skeptic asymmetric (WEAKENED, 3 concerns) → decision. `[VERIFIED]` из metrics/*.json:
- ⟨r⟩(zeros1) = **0.61092**, SE 0.00054–0.00086 (i.i.d./Bartlett/block-bootstrap); в полосе ±0.01 вокруг surmise 0.602658 с запасом 0.0017; **+0.0103 (z≥10) выше эмпирического GUE 0.6006** → efficiency 1.038 → CEILING_MISSPECIFIED (потолок для N→∞, популяция конечной высоты).
- Тренд по высоте 0.617 → 0.6119 → 0.6100 → 0.6006: **известная** конечно-высотная поправка ∝ (log T/2π)⁻³ — Forrester–Mays 2015 (arXiv:1506.06531), Nishigaki PTEP 2026 (arXiv:2507.10193). Novelty check убил псевдо-новизну до статуса гипотезы.
- Follow-up: `H-B1-1c` (known-answer тест №2 с потолком CUE(N_eff), допуск ~0.002) — `ready_to_scope`.
- Skeptic concern про SE (соседние r делят спейсинг) — верен по направлению (ρ₁=0.28), не меняет вывод (`metrics/diag_se.json`).

**[WS: pilot-pains-automation] CLOSED 2026-09-06 — вариант C выполнен (ADR-005).** `[VERIFIED]`:
- D-репо `D:\Claude-cod-top-2026`, ветка `y17/pilot-pains`, коммит `8c76a73` (10 файлов, только мои; чужая незакоммиченная работа на main не тронута). 72 теста зелёные. **НЕ запушено** — решение владельца.
- Задеплоено копированием в `~/.claude/hooks` (lib/runtime.py + 3 хука, 0 diff). Live smoke: notification → 0 байт; реальный research-запрос → RESEARCH.
- Шаблон: `ceiling.md` (новый, поле Population) + `escape_route.md` per-sign — в D: и здесь.
- **Находка для владельца стека:** 10 хуков (`ceiling_gate_guard`, `claim_scope_gate`, …) существуют только в `~/.claude/hooks` со своей git-историей — две git-истины; `docs/ceiling-gate-structured-block.md` отсутствует. Не разруливал.

**СЛЕДУЮЩИЙ ШАГ — решение пользователя** (LAB.md § 6): A) scoping `H-B3-1` (первая убиваемая гипотеза), B) `H-B1-1c` (первый эксперимент с настоящим `ceiling.md`). Плюс: merge/push ветки D: и дрейф хуков.

Phase 1b (H-B1-1b, хроматин) — BLOCKED: upstream `ART-TAD-AUC-0.99998` invalidated; ждёт Option A в H-7 TAD + решение `Q-GOE-vs-GUE`.

## Project State
- **Repo:** https://github.com/sergeeey/Y-17-100-gipotez — PUBLIC, created 2026-09-06, commit d50597f (initial import). [VERIFIED]
- **Excluded from public repo (.gitignore):** `H-7 GeoSpectra Lab (DIFFERENT project…).md` — third-party correspondence refs (Tom Lawrence). Local copy kept. User may override.
- **New meta-goal (2026-09-06, user):** make this an *exemplary experimental lab* — memory/structure/hypothesis-graph designed up front so a blind orchestrator can operate; use it to test the whole tool/agent/methodology stack. **Variant C chosen by user (AskUserQuestion) → ADR-002.** Every tool use → row in `tooling-eval/LEDGER.md` (25 rows after session 1: CAUGHT 6 / OK 8 / NOISE 5 / NOT-YET 6).
- **Graph validator:** `python scripts/lab_check.py` (SCHEMA invariants 1–3) + `pytest` (3 tests incl. negative control replicating the 2026-05-28 incident). Run both before every commit.
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
pip install -r requirements.txt
python scripts/lab_check.py          # graph invariants (must be OK before commit)
python -m pytest -q                  # 3 tests
python -m ruff check scripts/ tests/ # lint (line-length=100 pinned in pyproject.toml)
# LEDGER summary — count by grep, never by hand:
grep -E '^\| (2026-[0-9-]+|—) \|' tooling-eval/LEDGER.md | awk -F'|' '{gsub(/ /,"",$6); print $6}' | sort | uniq -c
```

## Open Questions (для пользователя)
1. Frontier R&D / TOFT / RAF Theory — реальны на другом компьютере, или нет?
2. Доступен ли этот E:\ путь с других ПК (тот же физический диск / сетевая шара / нет)?

---
*Создан: 2026-09-06 при переносе из Obsidian vault.*

## Auto-commit log
- [2026-09-06 11:57] `ff6246c`: fix: gitignore inline comments broke hook-scratch patterns; LEDGER +1
- [2026-09-06 11:47] `ff6246c`: fix: gitignore inline comments broke hook-scratch patterns; LEDGER +1
- [2026-09-06 11:46] `c912d70`: chore: untrack hook scratch files, ignore **/.claude/state/
- [2026-09-06 11:45] `f8057d0`: feat(pilot): H-B1-1a through FL Full-Ladder — PROMOTE [WEAKENED]
- [2026-09-06 11:18] `f021de1`: feat: lab core — LAB.md entry point, registry graph, FL template, ledgers, lab_check
- [2026-09-06 10:58] `d50597f`: chore: initial import of Y-17 Cross-Domain Bridge Lab from Obsidian vault
