# Урок: операционные правила запуска гипотез (из Codex H6 session)

## Контекст

2026-05-10. Параллельная Codex сессия после H6 PBDB execution выработала операционные правила, которые применимы ко всему портфелю 128 гипотез. Они уже зашиты в [[Hypothesis Execution Queue (2026-05-10)]] но заслуживают повышения в raw/ как универсальный паттерн.

## 6 операционных правил для каждой гипотезы

Каждый запуск гипотезы должен иметь:

1. **Разделение Pipeline vs Experiment** — отдельные секции в коде/доке
   - Pipeline = что делает код (data flow, инструменты)
   - Experiment = какая научная идея проверяется (claim, метрика, controls)
   - Без этого через неделю не вспомнишь почему такие bins/bootstrap/thresholds

2. **Kill criterion ДО execution** — explicit, не post-hoc
   - "Если X — гипотеза умерла"
   - Записать в код / комментарий ДО запуска
   - Иначе post-hoc rationalization

3. **Sensitivity matrix, не один run** — минимум 6 вариантов
   - Baseline + bin sizes + filters + alternative methods
   - Один run = noise; 6 runs = signal vs robustness
   - H6 sensitivity 6/6 KILLED = robust verdict
   - H8 3/6 MARGINAL = lead не confirmation

4. **Top-N side-signal capture** — не только target metric
   - H6 искал 26 Myr, нашёл 62 Myr (Melott 2008 vicinity)
   - Если бы выводили только target → 62 Myr lead был бы пропущен
   - Pipeline должен report top peaks вне target window

5. **Evidence label обязателен:**
   - `VERIFIED-REAL` — real-world data, sources cited
   - `VERIFIED-SYNTHETIC` — mock/synthetic (валиден для unit tests, INVALID для validation claims)
   - `HYPOTHESIS` — agent заявил, но не tool-confirmed
   - `UNVERIFIED` — нет независимой проверки
   - `CONFLICT` — sources contradict

6. **Same-day vault update** — не "позже"
   - Result generated → hypothesis card обновлён в тот же день
   - Иначе vault drift и context loss

## Три исхода гипотезы (no "почти"!)

Каждая гипотеза должна резолвиться в одно из:
- **KILLED** — не выдержала kill-criterion
- **CONFIRMED** — peer-review-ready результат (редкий)
- **LEAD** — interesting signal, но не paper-grade (например H8)

**Не разрешено:** "почти", "вероятно", "интересно но не уверен" — это эвфемизмы для "не закрыто". Лучше KILLED с честным null-result чем lingering в "in progress".

## Killed hypothesis = success pattern (новый стандарт)

H6 PBDB изменил портфельный стандарт. Killed hypothesis с:
- Clean code на GitHub
- Cached data
- Bootstrap N=1000
- Sensitivity runs
- null_result.md report

— это **success**, не failure. Solo researcher accumulates assets независимо от научного результата.

## Antipattern (что НЕ делать)

❌ Один run без sensitivity matrix
❌ Только target metric, без top-N peaks
❌ Verdict "почти KILLED" / "почти CONFIRMED"
❌ Mixed pipeline и experiment в одном blob кода
❌ Post-hoc kill criterion (после результата)
❌ Updated vault через неделю после execution
❌ `[VERIFIED]` без указания REAL/SYNTHETIC

## Связь с другими правилами

- Audit-verification-gate.md — VERIFIED-REAL vs VERIFIED-SYNTHETIC distinction
- Skeptic-triggers.md — round numbers и synthetic data flags
- Submission Gate Protocol — не подавать без kill criterion явного

## Пример применения (H6 vs H8)

**H6 (правильно):**
- Pipeline: PBDB API → bins → Lomb-Scargle → bootstrap (отдельная секция)
- Experiment: 26 Myr periodicity claim Raup-Sepkoski (отдельная секция)
- Kill criterion ДО run: "FAP > 0.05 при baseline → KILLED"
- Sensitivity: 6 runs (bin sizes, taxonomy levels, filters)
- Top-N capture: top_period_Myr выведен → нашли 62 Myr серендипно
- Same-day vault update: ✅
- Verdict: KILLED 6/6 → null-result publishable

**H8 (правильно):**
- Same pipeline, разные experiment
- Kill criterion: "если 0/6 CONFIRMED → KILLED, иначе LEAD"
- Result: 3/6 MARGINAL → status LEAD (не "почти CONFIRMED")
- Need: biodiversity metric для true Melott 2008 replication

#operational-rules #hypothesis-execution #pipeline-vs-experiment #sensitivity-matrix #side-signals #lessons-learned
