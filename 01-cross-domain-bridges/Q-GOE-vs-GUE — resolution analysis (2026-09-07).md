# Q-GOE-vs-GUE — resolution analysis (2026-09-07)

**Status:** graph.yaml `Q-GOE-vs-GUE` — `open` → `bracketed` (a reasoned default position with a
named burden of proof, not a hard proof either way).

**Why this document exists:** user, reviewing the session log, said the B1 blocker ("Option A /
Q-GOE-vs-GUE") could not be resolved by them from the log as written, and explicitly delegated the
call to the agent ("сам принимай оптимальные смелые решения"). Reading the actual argument behind
each of the two named items shows they are not symmetric: Option A is unfinished implementation
work in a different, external project (genuinely out of this project's write-scope — see
`CLAUDE.md` Scope Fence); Q-GOE-vs-GUE is a theoretical claim made *by* the upstream H-7 TAD
project, evaluable in scope here from RMT/symmetry-class reasoning alone, without needing that
project's code or data. This document does the latter.

## The claim under examination

`01-cross-domain-bridges/H-7 TAD Spectral Diagnostic.md` (lines 130-151), added 2026-05-17 with
its own dated note **"усиление для рукописи"** ("strengthening for the manuscript"):

> До деплеции: матрица блочно-диагональная → класс Пуассон (нет уровневого отталкивания)
> После деплеции: матрица полносвязная → класс A (GUE) = Wigner-Dyson

i.e.: block-diagonal contact matrix → Poisson statistics; fully-connected contact matrix →
Altland-Zirnbauer class A (GUE).

## Why this argument does not establish GUE [INFERRED, standard RMT classification]

The Poisson↔Wigner-Dyson axis and the GOE↔GUE axis are **two different, independent properties**
of a random matrix ensemble, not one sliding scale:

- **Poisson vs. Wigner-Dyson** (level repulsion vs. none) is driven by whether the underlying
  dynamics/coupling is integrable (block-diagonal, uncoupled subsystems → no level repulsion →
  Poisson) or chaotic (fully coupled → level repulsion → Wigner-Dyson of SOME class). This is the
  Bohigas-Giannoni-Schmit-type transition, and it is a real, standard RMT phenomenon — the
  block-diagonal-to-fully-connected argument correctly predicts a Poisson→Wigner-Dyson shift.
- **GOE vs. GUE** (which Wigner-Dyson class) is set by whether the matrix has time-reversal
  symmetry. A **real, symmetric** matrix — which is exactly what a Hi-C contact matrix is, since
  contact frequency between loci `i` and `j` has no direction (`C_ij = C_ji` by construction) —
  falls in class **AI (GOE)** by default. Reaching class **A (GUE)** requires an *additional*,
  physically distinct broken-time-reversal-symmetry mechanism (e.g. a complex Hermitian
  construction, a synthetic gauge flux through cycles of the contact graph) — becoming
  "fully-connected" does not, by itself, break time-reversal symmetry or complexify the matrix.

The cited argument conflates these two axes: it correctly predicts the Poisson→Wigner-Dyson
transition (connectivity-driven, real) but asserts the wrong Wigner-Dyson sub-class (GUE instead
of GOE) without ever specifying a mechanism for the symmetry-breaking that GUE specifically
requires. No such mechanism is named anywhere in the cited section — the table (line 136-139)
correctly *states* that class A requires "no symmetry" and class AI requires "time-reversal
symmetry," but the application section never checks which one a real, symmetric Hi-C matrix
actually has.

**Scientism Detection flag (per `~/.claude/rules/artifact-provenance-gates.md` Gate 4):** the
section's own header timestamp — "Добавлено 2026-05-17 — усиление для рукописи" — names the
motivation as strengthening a manuscript's authority ("Переводит статью из 'мы нашли дескриптор' →
'мы идентифицировали смену AZ-класса'... Связывает с 50-летней теоретической физикой (авторитет
фреймворка)", lines 153-156), not as an independently-derived prediction checked before the
manuscript motivation existed. Invoking a named, authoritative 50-year-old classification scheme
without checking which of its sub-classes actually applies is structurally the same move Gate 4
flags for words like "well-established" or "best practice" — a citation standing in for a computed
or argued number.

## What survives, and what does not

**Survives:** the underlying empirical prediction — CTCF depletion drives chromatin from Poisson
to *some* Wigner-Dyson class — is plausible RMT reasoning and does not depend on which sub-class.

**Does not survive as argued:** the specific claim that the resulting class is A/GUE rather than
AI/GOE. No mechanism for broken time-reversal symmetry is given.

## Resolution (bracketed, not proven)

**Default/null expectation, until a specific symmetry-breaking mechanism is proposed and
checked:** a fused (fully-connected) Hi-C contact matrix should be compared against **GOE**, not
GUE. This project's own `experiments/20260906-riemann-rstat-gue/` already has both reference
values on hand (`result_summary.md`): `⟨r⟩_GOE = 0.535898` (theoretical), separated from
`⟨r⟩_GUE = 0.602658` by 0.070 — a large, easily-resolved gap, so this choice is not a close call
numerically once real chromatin data is available.

**Falsifiable, forward-looking statement (for whenever Option A produces an honest AUC):** when
the H-7 TAD project's Option A redesign yields real post-fusion r-statistics, compare them against
`⟨r⟩_GOE ≈ 0.536` as the primary null, not `⟨r⟩_GUE ≈ 0.603`. If the honest r-statistic instead
sits near 0.60, that would be a genuinely interesting, falsifying-the-default result — worth
re-opening the symmetry-breaking-mechanism question in earnest, not worth assuming in advance.

**Evidence marker:** [INFERRED] — standard RMT/AZ classification reasoning applied to a specific
claim in this project's own upstream document; not independently verified against a primary AZ
tenfold-way source line-by-line, and not tool-computed (no code was run for this analysis — it is
a theoretical argument, appropriately marked as such, not overclaimed as [VERIFIED]).

## What this does NOT resolve

1. Does **not** unblock `H-B1-1b` — Option A's implementation is still unfinished, external, and
   out of this project's write-scope regardless of which ensemble is the right comparison target.
2. Does **not** prove GOE is correct — it names the default/null position and the burden of proof
   for anyone wanting to argue GUE instead (name the symmetry-breaking mechanism).
3. Does **not** revise `H-B1-1a`'s own CONFIRMED[WEAKENED] Riemann-zeros result — that experiment
   never depended on the chromatin side of the comparison.
