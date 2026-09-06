---
title: "Submission Gate Protocol — HARD RULE против validation theater"
type: hard-rule
status: active
priority: maximum
domain: Scientific Integrity, Quality Assurance
created: 2026-05-10
related:
  - "[[Pre-Submission Checklist Template]]"
  - "[[Submission Diary]]"
  - "[[Hypothesis Portfolio MOC]]"
tags:
  - hard-rule
  - submission-gate
  - validation-theater
  - guardrail
  - integrity
---

# 🛑 SUBMISSION GATE PROTOCOL — HARD RULE

> **Это не рекомендация. Это hard barrier.**
> Любая попытка submission (preprint, grant, public post, paper, code release) ОБЯЗАНА пройти этот gate.

---

## Контекст возникновения правила

**Прецеденты "почти подал ложные данные":**

1. **2026-05-01:** ТОП-10 ниш ArgosArb — F1=1.000 на synthetic data, чуть не объявлен "VERIFIED". Postmortem → создан `~/.claude/rules/skeptic-triggers.md`
2. **bioRxiv "жемчужины" (раньше):** ARCHCODE pearls — skeptic опроверг → submission saved
3. **2026-05-10:** ARCHCODE manuscript v2 объявлен "READY" → skeptic нашёл text↔figures mismatch (AUC 0.98 vs 0.79)

**Паттерн:** excitement of completion + commitment bias → пропуск verification → almost submission.

**Это решает hard barrier, не willpower.**

---

## ПРАВИЛО: 4 GATES (нельзя пропустить ни один)

### Gate 1: TRIGGER DETECTION

**Когда срабатывает:**

Любой из этих сигналов = mandatory ENTER protocol:

| Trigger | Пример |
|---------|--------|
| Keyword в user message | "подаём", "submit", "send", "publish", "ready", "готово к отправке" |
| File modification | `manuscript*.md`, `*.docx`, `paper*`, `cover_letter*`, `submission*` |
| Round numbers в claims | "AUC=0.98", "100% accuracy", "F1=1.000" |
| Synthetic data в validation | `np.random.seed`, `mock_data`, `create_synthetic` |
| External destination | bioRxiv, arXiv, Manifold, Twitter, GitHub release, email to editor |
| External claim | "ready for review", "production-ready", "publication-ready" |

**Mandatory action when triggered:**
```
[SUBMISSION GATE TRIGGERED]
Reason: <which trigger>
STOP all "submit"/"upload"/"send" suggestions until 4 gates passed.
```

### Gate 2: SKEPTIC AGENT RUN

**Mandatory:** Spawn skeptic agent (subagent_type: "skeptic") with prompt:

```
Skeptic mode: pre-submission red team analysis.

Material to review: <manuscript / preprint / grant / post>
Source files: <list>
Claimed result: <main claim>

Specific tasks:
1. Spot-check 3 random numerical claims against actual source data
2. Compare text claims vs figure outputs side-by-side  
3. Identify any synthetic data without [VERIFIED-SYNTHETIC] label
4. Flag round numbers (AUC=0.98, F1=1.000, etc.) for false-precision check
5. Verify references section exists and matches inline citations
6. Apply skeptic-triggers.md 5 triggers explicitly

Output: PASS / FAIL with specific evidence.
If FAIL: list each kill criterion triggered.
```

**Cannot proceed без skeptic verdict.**

### Gate 3: PRE-SUBMISSION CHECKLIST

**Заполнить template:** [[Pre-Submission Checklist Template]]

Минимум 9 проверок (см. template). Каждая — `[VERIFIED]` или `[FAILED]` с evidence.

**Если хоть одна `[FAILED]` → STOP. Не submit.**

### Gate 4: 24-HOUR COOLING OFF

**Между объявлением "READY" и actual submission:** ≥ 24 часа.

**Why:** Excitement of completion затмевает критическое мышление. 24 часа дают:
- Skeptic findings settle
- Fresh eyes на следующий день
- Новый skeptic re-run на финальной версии
- Возможность поймать что было пропущено

**Exception:** только если есть hard external deadline (grant call closes сегодня) — но ДАЖЕ тогда mandatory skeptic + checklist, just shorter cooling.

---

## ENFORCEMENT — кто следит

### Меня (Claude Sonnet 4.6)

**HARD COMMITMENT:**

1. **NEVER** объявляю что-то "READY for submission" без явного прохождения 4 gates
2. **ALWAYS** spawn skeptic agent перед суггестией submit/upload/send
3. **ALWAYS** перечисляю в response какой gate triggered и какой пройден
4. **NEVER** говорю "всё готово, подавай" если не прошли все 4 gates

**Если я нарушаю это правило — это критическая ошибка.** Пользователь имеет право указать на это.

### User (Sergey)

1. **Право вето:** в любой момент сказать "skeptic check" → mandatory pause
2. **Запись:** каждое прохождение gate в [[Submission Diary]]
3. **Calibration:** через год — Brier score на собственных "ready" claims

---

## КОНКРЕТНЫЕ EDGE CASES

### Edge case 1: "Это маленький fix, не нужен полный gate"

**Ответ:** ВСЕГДА полный gate. "Маленькие fixes" — главный источник validation theater (одна цифра меняется, остальное не пересчитывается).

### Edge case 2: "Это re-submission, не новая submission"

**Ответ:** Re-submission = new submission. Все 4 gates обязательны. Если данные изменились между submissions — skeptic может найти inconsistency.

### Edge case 3: "Я уверен на 100%"

**Ответ:** Калибровка показывает что "100% уверен" люди ошибаются в 15-30% случаев (Tetlock 2015). Уверенность ≠ correctness. Gate всё равно обязателен.

### Edge case 4: "Hard deadline сегодня"

**Ответ:** Минимальный gate (skeptic + checklist) обязателен. Cooling off можно сократить до 2 часов, но НЕ убрать. Лучше пропустить deadline чем подать с ошибкой.

### Edge case 5: "Это просто preprint, можно update"

**Ответ:** Preprint update требует объяснения почему было неправильно. Updates оставляют trail в Wayback Machine. Лучше не подавать ошибку чем потом её explain.

---

## METRIC: успех protocol

| Metric | Target | Текущий |
|--------|--------|---------|
| Submissions с post-publication corrections | 0 | TBD |
| Skeptic catches before submission | track all | 3 (ТОП-10, pearls, ARCHCODE v2) |
| Average gate completion time | 1-2 часа | TBD |
| User confidence in submitted material | "I'd bet $1000 on this" | TBD |

---

## АНТИ-ПАТТЕРНЫ (запрещены)

❌ "Submission package READY" без явного gate prove
❌ "All checklist items complete" без actual file references
❌ "Skeptic не нужен, я проверил" — skeptic agent ОТДЕЛЬНЫЙ context, видит то что я не вижу
❌ "Время поджимает" — это сигнал что нужна ещё одна проверка
❌ Сразу после написания manuscript объявлять "ready" — обязательно 24h cooling
❌ Доверять чужому LLM-output (Codex/GPT-5) без re-verification

---

## INTEGRATION с другими rules

- `~/.claude/rules/integrity.md` — Verify-Before-Claim принцип
- `~/.claude/rules/skeptic-triggers.md` — 5 triggers для skeptic auto-invoke
- `~/.claude/rules/audit-verification-gate.md` — spot-check rule
- `[[Pre-Submission Checklist Template]]` — конкретный template
- `[[Submission Diary]]` — log каждой submission attempt

---

## КОМАНДЫ user'а для quick-trigger

Если пользователь хочет быстро запустить gate, может написать:

- **`/skeptic`** — manual trigger skeptic skill
- **"submission gate"** — full 4-gate protocol
- **"проверь перед отправкой"** — same in Russian
- **"red team this"** — adversarial review

Я distinguish между casual "ну отправляй" (требует gate) и technical request "тестово отправь dry-run" (не требует gate).

---

*Created: 2026-05-10 после ARCHCODE v2 skeptic catch. Status: ACTIVE HARD RULE.*
