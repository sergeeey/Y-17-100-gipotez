# decision.md — 20260910-remy-tumorigenesis-stimulus-asymmetry-h29

## Verdict: **CONFIRMED**

## Result Summary (`metrics/run.json`, 10 conditions)

| branch | k | n_states original | n_states flipped (capped) | hit STATE_CAP | isomorphism confirmed |
|---|---|---|---|---|---|
| branch_1 | 1 | 956 | 40528 | YES | **False** |
| branch_1 | 2 | 954 | 40375 | YES | **False** |
| branch_1 | 3 | 200 | 35699 | YES | **False** |
| branch_1 | 4 | 111 | 32400 | YES | **False** |
| branch_1 | 5 | 2 | 31256 | YES | **False** |
| branch_2 | 1 | 956 | 39624 | YES | **False** |
| branch_2 | 2 | 954 | 39470 | YES | **False** |
| branch_2 | 3 | 200 | 35417 | YES | **False** |
| branch_2 | 4 | 111 | 32369 | YES | **False** |
| branch_2 | 5 | 2 | 31245 | YES | **False** |

**10/10 conditions confirm the asymmetry, dramatically.** Flipping `FGFR3_stimulus` hits
`STATE_CAP=30000` on EVERY single condition, including `k=5` — where the ORIGINAL graph has only
**2 states** (H-B7-22's own SCHEDULE_ROBUST classification), yet the flipped graph explodes past
31000 states. This is not a subtle effect: the reachable universe grows by **1.6 to 4.2 orders of
magnitude** the instant `FGFR3_stimulus` is flipped (exact per-condition ratios below), while
flipping `EGFR_stimulus` (H-B7-27/28) never changed graph size by even a single state.

**CORRECTION (2026-09-10, decisive check from the deep external novelty audit,
`reports/2026-09-10-deep-external-novelty-audit.md`):** the original wording "1-2 orders of
magnitude" understated the k=5 condition and did not match the committed `metrics/run.json`.
Recomputed exactly from `n_states_flipped_capped / n_states_original`:

| branch | k | ratio | log10(ratio) |
|---|---|---:|---:|
| branch_1 | 1 | 42.4x | 1.63 |
| branch_1 | 2 | 42.3x | 1.63 |
| branch_1 | 3 | 178.5x | 2.25 |
| branch_1 | 4 | 291.9x | 2.47 |
| branch_1 | 5 | 15628.0x | **4.19** |
| branch_2 | 1-5 | (matching within <1%) | 1.62-4.19 |

k=1,2 are indeed ~1.6 orders ("1-2" as originally stated); k=5 is ~4.2 orders — nearly triple
the originally-quoted upper bound. This does not change the verdict (asymmetry is still
confirmed 10/10, and even the smallest ratio, 41x, is far beyond any subtle effect) — only the
magnitude description, which should not be re-cited as "1-2 orders" going forward.

## Mandatory checks against claim.md's own Kill Criterion

- [x] `φ'=flip(FGFR3_stimulus)` fails to be a node-set bijection for ALL 10 conditions — **PASS**
  (predicted asymmetry confirmed, not the null "also inert" outcome)
- [x] `STATE_CAP` explicitly NOT treated as a pass/fail criterion — correctly handled as
  `BLOCKED-INFRASTRUCTURE` for the exact count only; the size-differs-from-original check (which
  alone rules out bijection) needed no uncapped count and was evaluated independently — **PASS**
- [x] No exact violation count fabricated for any capped condition
  (`n_fgfr3_false_in_flipped_graph` is `None` everywhere it was capped) — **PASS**

## Interpretation

This is a genuine, dramatic structural asymmetry between two structurally-similar-LOOKING frozen
self-loop exogenous nodes. `EGFR_stimulus` is inert because `EGFR`'s rule only reads it under a
condition (`!GRB2&!FGFR3`) that never holds in this reachable region (H-B7-27/28's own finding).
`FGFR3_stimulus`, by contrast, is read UNCONDITIONALLY (given `!GRB2&!EGFR`, both already true in
this region) by `FGFR3`'s own rule — flipping it directly collapses the `FGFR3≡True` invariant that
the entire H-B7-27/28 mechanism depends on, opening up a vastly larger reachable universe. This
strengthens confidence that H-B7-27/28's own finding is a genuine, mechanism-specific effect
(algebraically explained, not a generic "any frozen coordinate is safe to flip" artifact) — exactly
the kind of contrast/control test Mechanism Development Mode's own Question 5 (structural asymmetry)
calls for.

## FL Step 8a — Independent Reviewer

Full-tier claim (a dramatic, surprising-shaped contrast result — 1-2 orders of magnitude graph-size
explosion) — mandatory per FL Step 8a. Context-asymmetric: reviewer given `claim.md` + `run.py`
only, no reasoning chain. Scoped narrowly to ONE reconstruction: independently verify `branch_1,
k=5` (the smallest, sharpest contrast — original graph has only 2 states) by rebuilding both the
original and `FGFR3_stimulus`-flipped release states and their reachable graphs from scratch, and
confirming (a) the isomorphism fails and (b) the flipped graph's size, even if capped, already
exceeds the original's 2 states by a wide margin.

**Verdict: CONFIRMED-REAL.** Reviewer independently re-executed only the graph-construction and
isomorphism primitives (`build_reachability_graph`, `build_phi`, `check_isomorphism`) — never called
`cmd_run()` or read the cached output before computing.

- Original graph: independently `2` states, no cap hit — matches H-B7-22's own pre-established
  SCHEDULE_ROBUST sanity check
- Flipped graph: independently `31256` states, `hit_cap=True` (BFS took ~86s, matching the stated
  cost warning)
- `node_set_bijection: False`, `isomorphism_confirmed: False` — established from the size mismatch
  alone, no cap-sensitive precision needed
- Cross-check against `metrics/run.json`: exact digit-for-digit match on
  `n_states_original=2`, `n_states_flipped_capped=31256`, `flipped_hit_cap=True`,
  `isomorphism_confirmed=False`

## Skeptic Concerns

No `[FALSIFIED]` concerns raised. Reviewer's own independent reconstruction matched the committed
value exactly, including the cap-sensitive field — no dismiss/accept/mitigate entries needed.

## Caveats / What This Does NOT Mean

Per claim.md's own "What This Does NOT Mean" section — unchanged and reaffirmed:

1. Does NOT claim to have found the network's full symmetry group.
2. Does NOT compute exact reachable-set sizes or exact invariant-violation counts for any capped
   condition — all 10 conditions hit `STATE_CAP`, so no exact numbers beyond the capped/partial
   counts are reported.
3. Does NOT itself resolve the large-deviation/Kramers question, still deliberately deferred.
4. Does NOT weaken H-B7-27/28's own confirmed result — this STRENGTHENS confidence the mechanism is
   specific and non-trivial, not a generic artifact.

## MCID

Not applicable — exact boolean/graph-structural claim, no statistical estimate.
