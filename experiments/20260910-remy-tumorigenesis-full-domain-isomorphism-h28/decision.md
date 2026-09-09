# decision.md — 20260910-remy-tumorigenesis-full-domain-isomorphism-h28

## Verdict: **CONFIRMED**

## Result Summary (`metrics/run.json`, 40 k values, 80 conditions)

- **80/80 conditions OK, 0 BLOCKED-INFRASTRUCTURE** (`STATE_CAP=30000` never hit)
- **4516 total reachable states scanned** (both branches, k=1..40)
- **Invariant (`FGFR3=True & GRB2=False & EGFR=False`): 0 violations across all 4516 states**
- **Isomorphism (`φ=flip(EGFR_stimulus)`): confirmed at all 40 k values** — node-set bijection +
  bidirectional edge preservation, both directions
- **Corollary (`exact_escape_probability` independently re-derived on both graphs): matches at all
  40 k values**, and for `k=1..5` matches H-B7-27's own already-committed values (regression test)
- For `k>=5` (H-B7-22's own SCHEDULE_ROBUST region): exact escape probability is `1.0` for both
  branches at every tested k, as expected from H-B7-22's own classification

## Mandatory checks against claim.md's own Kill Criterion

- [x] Invariant holds with 0 exceptions across ALL 80 conditions — **PASS**
- [x] Isomorphism confirmed for ALL 40 k values — **PASS**
- [x] No condition hit `STATE_CAP` — **PASS**

## What this generalizes, precisely

H-B7-27 established the branch isomorphism for the 10 conditions H-B7-26 tested (`k=1..5`). This
experiment extends the SAME mechanism (unchanged: `EGFR`'s rule gates `EGFR_stimulus`'s relevance
behind `!GRB2&!FGFR3`, which never holds anywhere checked) across the ENTIRE originally-tested
domain of H-B7-22 (`k=1..40`, both branches) — the widest domain this specific mechanism has been
checked against so far in this project. `branch_2`'s reachable graph is `branch_1`'s own graph at
an inert `EGFR_stimulus` coordinate offset, across the full tested range, not just a narrow window.

## FL Step 8a — Independent Reviewer

Full-tier claim generalizing a prior CONFIRMED result (H-B7-27) to a much larger domain (8x the
number of conditions) — mandatory per FL Step 8a. Context-asymmetric: reviewer given `claim.md` +
`run.py` only, no reasoning chain. Scoped narrowly (per this session's own established
reviewer-turn-budget lesson) to a SAMPLE-based spot check rather than a full 80-condition
re-derivation: independently verify the invariant AND isomorphism for exactly 3 representative
conditions spanning the domain — `k=1` (largest graph, 956 states), `k=20` (middle of the
SCHEDULE_ROBUST region), `k=40` (boundary of the tested domain) — both branches each.

**Verdict: CONFIRMED-REAL.** Reviewer loaded `run.py` independently, rebuilt `phi` from scratch,
and for k=1/20/40 (both branches) independently: simulated the release state, built the reachable
graph, counted invariant violations at every node, and checked the isomorphism (release mapping,
node-set bijection, bidirectional edge preservation).

| k | n1 mine/expected | n2 mine/expected | violations | φ(release) match | bijection | edges fwd/bwd |
|---|---|---|---|---|---|---|
| 1 | 956/956 | 956/956 | 0/0 | True | True | True/True |
| 20 | 1/1 | 1/1 | 0/0 | True | True | True/True |
| 40 | 1/1 | 1/1 | 0/0 | True | True | True/True |

Reviewer's own adversarial pass explicitly checked (and dismissed) whether the invariant only holds
trivially at large k where graphs collapse to a single state (`k=20/40`, `n=1`) — noted that `k=1`
(956 states) is the substantive, non-trivial case and the invariant holds there too, so the claim
does not rest only on the trivial cases. Also independently re-derived `node_names`/indices from
`h1.parse_bnet` rather than importing pre-computed indices from `run.py`, ruling out an index-mismatch
false-positive.

## Skeptic Concerns

No `[FALSIFIED]` concerns raised. Reviewer's own adversarial challenge #2 ("does the invariant only
hold vacuously at large k where the graph is trivial") is **Dismissed** (reasoning: `k=1`'s own
956-state graph is the substantive non-trivial case and the invariant holds there with 0 exceptions
too — the claim is not resting on the trivial `k>=20` cases alone).

## Caveats / What This Does NOT Mean

Per claim.md's own "What This Does NOT Mean" section — unchanged and reaffirmed:

1. Does NOT claim this invariant holds for any clamp scheme, base-state pair, or k beyond 40 not
   already covered by H-B7-22's own originally-tested domain.
2. Does NOT re-derive escape probabilities as a new finding for k=6..40 — already known to be 1.0
   from H-B7-22's own SCHEDULE_ROBUST classification; this experiment's corollary is a
   construction-consistency regression, not a new result.
3. Does NOT itself resolve the large-deviation/Kramers question, still deliberately deferred.
4. Does NOT claim to have found the network's full symmetry group — only that this one bijection is
   confirmed an automorphism across this specific tested domain.

## MCID

Not applicable — exact boolean/graph-structural claim, no statistical estimate.
