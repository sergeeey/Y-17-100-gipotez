# Урок: text↔figures consistency check before "READY" claim

## Что произошло (2026-05-10)

ARCHCODE manuscript v2 был объявлен "READY for bioRxiv submission" без text↔figures verification. Skeptic agent в parallel session сравнил claims в тексте с output figures generation script — нашёл 4 critical mismatches:

1. AUC: text 0.982 vs figures 0.791 (Δ=0.191, 19.1pp)
2. n: text 32,201 vs figures 25,850 (Δ=6,351, 19.8%)
3. ρ: text 0.077 vs figures 0.014
4. Figure 3 synthetic data без `[VERIFIED-SYNTHETIC]` label

Submission saved before embarrassment.

## Root cause

Manuscript text написан на одном dataset (April HBB-only, n=1,103), figures на другом (2026-05-10 9-loci pooled, n=25,850). Между этим — 10+ часов и смена data scope.

## Lesson

Любое утверждение "manuscript READY for submission" требует **обязательную** проверку:

1. **Text↔figures consistency** — каждое числовое claim в тексте должно матчить figure values
2. **Sample size verification** — n из text == n из data load output  
3. **Synthetic data labeling** — любой `np.random.seed(...)` или mock data в validation figure → `[VERIFIED-SYNTHETIC]` явно
4. **References completeness** — bibliography section существует, не только inline citations

## How to apply

Перед claim "READY":
- Открой manuscript + figures side-by-side
- Spot-check 3 random claims (AUC, n, ρ, kill criteria)
- Если хоть один не матчит → STOP, fix data pipeline first

Это **тот же урок** что 2026-05-01 ТОП-10 disaster postmortem — validation claims требуют [VERIFIED-REAL] markers, не интуитивную уверенность.

## Triggered guardrails (что сработало)

- `~/.claude/rules/skeptic-triggers.md` Trigger 4 (round numbers AUC=0.98)
- `~/.claude/rules/skeptic-triggers.md` Trigger 5 (synthetic evidence)
- `~/.claude/rules/audit-verification-gate.md` spot-check rule

## Внешнее подтверждение (arXiv 2608.27424, Aug 2026)

"Beyond F1" paper независимо показал ту же ловушку в ML security scanners:
ModelScan сообщал precision/recall/F1 = **100%** — но только на 67/135 families
где вообще выдавал решение (ModelAudit: 135/135). **Высокий F1 маскировал
scanner который не анализирует половину входов.**

→ Урок обобщается: любой eval должен мерить **coverage / decision-availability**
ОТДЕЛЬНО от accuracy. "F1=100% на решённых случаях" ≠ "работает". Это ровно
ARCHCODE AUC=0.98 (маскировал data mismatch) в другом домене.
См. [[Weekly arXiv Digest — 2026-08-22-28 (software-wedge)]] #3.

#postmortem #validation-theater #archcode #manuscript #scientific-integrity #lessons-learned #coverage-metric
