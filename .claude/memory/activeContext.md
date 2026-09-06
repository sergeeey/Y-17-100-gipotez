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
- Follow-up: `H-B1-1c` — CONFIRMED, см. ниже.
- Skeptic concern про SE (соседние r делят спейсинг) — верен по направлению (ρ₁=0.28), не меняет вывод (`metrics/diag_se.json`).

**[WS: pilot-pains-automation] CLOSED 2026-09-06 — вариант C выполнен (ADR-005).** `[VERIFIED]`:
- D-репо `D:\Claude-cod-top-2026`, ветка `y17/pilot-pains`, коммит `8c76a73` (10 файлов, только мои; чужая незакоммиченная работа на main не тронута). 72 теста зелёные. **НЕ запушено** — решение владельца.
- Задеплоено копированием в `~/.claude/hooks` (lib/runtime.py + 3 хука, 0 diff). Live smoke: notification → 0 байт; реальный research-запрос → RESEARCH.
- Шаблон: `ceiling.md` (новый, поле Population) + `escape_route.md` per-sign — в D: и здесь.
- **Находка для владельца стека:** 10 хуков (`ceiling_gate_guard`, `claim_scope_gate`, …) существуют только в `~/.claude/hooks` со своей git-историей — две git-истины; `docs/ceiling-gate-structured-block.md` отсутствует. Не разруливал.

**[WS: scoping-H-B3-1] CLOSED 2026-09-06 (ADR-006, commit `d06942a`, автономная очередь по запросу пользователя "давай A ... итд по очереди").** Найдено ДО построения плана: Mangal/GloBI непригодны (та же болезнь, что Frontier R&D/TOFT/RAF). Исправлено на Carpenter 2011 Peter/Paul Lake (EDI/NTL-LTER). Wang 2023 → kill-критерий честно сужен до Phase 1 N=1. `registry/graph.yaml`: H-B3-1 `ready_to_scope→ready`. `experiments/20260906-may1972-tda-ews-peterlake/` — design-complete (claim/estimand/experiment.yaml/ceiling/escape_route), **расчёт НЕ запущен** (загрузка EDI + Ripser — отдельный крупный шаг). 2 pearls.

**[WS: H-B1-1c] CLOSED 2026-09-06 (ADR-007, автономная очередь, пункт B).** `[VERIFIED]`:
- Формула N_eff/потолок взята из первоисточника (PDF `arXiv:2507.10193`, прочитан постранично через `Read`), не из WebSearch-пересказа — WebFetch на abstract и на сырой PDF честно отказались (не могли прочитать), это и заставило пойти к первоисточнику.
- **Опровергло** число «N_eff ≈ 1.446·ρ̄(γ_N)», записанное ранее в pearl_registry во время H-B1-1a — его нет в первоисточнике, было бы фабрикацией. Реальная формула: N_e(T)=(1/√(12Λ))log(T/2π), Λ=1.573151071 (Eq.42); точный sine-kernel предел 0.5997504209; эмпирическая подгонка 0.1896·N_eff^-3.081 (Fig.6).
- Результат: ratio observed/predicted = **1.054** (кумулятивно) / **0.884** (окно последних 50k) — оба далеко внутри пре-регистрированного [1/3,3], несмотря на экстраполяцию на 3+ порядка ниже откалиброванного диапазона (n=10⁸-10²³ → применено на n≈10⁵). `experiments/20260906-riemann-cue-neff-ceiling/decision.md`.
- Закрыл CEILING_MISSPECIFIED из H-B1-1a. Граф: `H-B1-1c → confirmed`.

**[WS: merge-D-and-run-H-B3-1] 2026-09-06 (ADR-008, по подтверждению пользователя).**
- **Merge/push D: DONE.** `y17/pilot-pains` (8c76a73) → `origin/main` через fast-forward push БЕЗ checkout (на рабочем дереве D: обнаружены чужие незакоммиченные файлы — не тронуты, Unclaimed Work Ownership). Local `main` тоже обновлён (`update-ref`, без переключения).
- **H-B3-1 реальный запуск → BLOCKED-INFRASTRUCTURE.** Пакет `knb-lter-ntl.360.2` точно идентифицирован (DOI resolve), но EDI закрыл публичный доступ: PASTA API 403 на все методы (12/12 ID), портал → Cloudflare Turnstile. 9 путей проверено, CAPTCHA не обходил (запрещено). `experiments/20260906-may1972-tda-ews-peterlake/substrate_gate.md`. Граф: `H-B3-1 → blocked`, evidence не понижен — это НЕ REJECT.
- **Требуется решение пользователя (если хочешь закрыть именно Peter Lake):** (a) вручную скачать пакет с `portal.edirepository.org/nis/mapbrowse?packageid=knb-lter-ntl.360.2`; (b) EDI API-токен; (c) — **сделано ниже через H-B3-1b, отдельный узел, Peter Lake не тронут.**

**[WS: H-B3-1b] 2026-09-06 (ADR-009, автономно по запросу «действуй максимально автономно»).** `[VERIFIED]`:
- Нашёл реально доступную альтернативу (O'Brien et al. 2023, тот же bridge B3): GitHub `duncanobrien/ews-assessments`, без CAPTCHA. Новый узел `H-B3-1b` (Peter Lake `H-B3-1` не тронут, остаётся `blocked`).
- Gate 1 ДО запуска: Mendota/Washington исключены — их дата перехода лежит ВНЕ скачанного ряда.
- **Результат:** Lower Zurich — TDA опередил classical EWS на **+24 месяца**, верное направление. Оба негативных контроля (Windermere, Loch Leven) — ложное срабатывание. `ceiling-gate` хук поймал пропущенный Step 4a → добавил AR(1)-суррогатную floor-проверку: **floor = 80–83%** ложных срабатываний БЕЗ всякого механизма → вердикт **CRITERION_INVALID** (не REJECT — жёсткое правило FL, не в null_results).
- Граф: `H-B3-1b → lead` (трёхисходная конвенция KILLED/CONFIRMED/LEAD). Rescue Review: `weak_alive`, 3 конкретных дешёвых next steps в decision.md (новый experiment ID нужен для любого — Minimal Relaxation Rule).
- Pearl (impact 8): фиксированный tau≥0.5 порог сидит на floor для экологических рядов такой длины — общий методологический паттерн.

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
- [2026-09-06 12:32] `3d011c2`: chore(D:)+feat(H-B3-1): merge/push pilot-pains fix; H-B3-1 substrate gate BLOCKED-INFRASTRUCTURE
- [2026-09-06 12:21] `1a5cd82`: feat(H-B1-1c): known-answer test #2 CONFIRMED — closes CEILING_MISSPECIFIED from H-B1-1a
- [2026-09-06 12:13] `d06942a`: feat(scoping): H-B3-1 — replace Mangal/GloBI with Carpenter 2011 Peter/Paul Lake; honest N=1 kill-criterion
- [2026-09-06 12:00] `7baa088`: feat(lab): automate the 3 pilot pains — ceiling.md template, per-sign escape rows, ADR-005
- [2026-09-06 11:57] `ff6246c`: fix: gitignore inline comments broke hook-scratch patterns; LEDGER +1
- [2026-09-06 11:47] `ff6246c`: fix: gitignore inline comments broke hook-scratch patterns; LEDGER +1
- [2026-09-06 11:46] `c912d70`: chore: untrack hook scratch files, ignore **/.claude/state/
- [2026-09-06 11:45] `f8057d0`: feat(pilot): H-B1-1a through FL Full-Ladder — PROMOTE [WEAKENED]
- [2026-09-06 11:18] `f021de1`: feat: lab core — LAB.md entry point, registry graph, FL template, ledgers, lab_check
- [2026-09-06 10:58] `d50597f`: chore: initial import of Y-17 Cross-Domain Bridge Lab from Obsidian vault
