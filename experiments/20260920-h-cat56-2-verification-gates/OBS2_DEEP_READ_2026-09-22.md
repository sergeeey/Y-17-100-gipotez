# Observation 2 / Hollowization — bounded deep-read (2026-09-22)

Part of Trajectory Lab next step **B → conditional A**.
Not a new hypothesis. No author email sent.

## L0 (EstimandOps)

| Field | Value |
|---|---|
| Question type | **Descriptive / logical entailment** |
| Entity | Observation 2 + Hollowization Thm 1 of arXiv:2601.21801v1, as used by H-CAT56-2 |
| Predicate | Does `dim V⊥ < d` (as certified on our exact instance) entail non-saturation of single-copy matrix QCRB under the paper's definitions? |
| What a HOLD does NOT mean | Novelty settled; Ref. [29] re-proven; external verification of our code |

## Sources checked this session

| Source | Marker |
|---|---|
| ar5iv HTML of arXiv:2601.21801 (fetched 2026-09-22) | `[DOCS, read]` |
| `proof_and_scope.md` (2026-09-20) | `[PROOF]` + `[DOCS, read]` prior session |
| H-CAT56-2 orchestrator re-derivation in `decision.md` §Orchestrator | `[PROOF]` prior session |
| Re-run `verify_exact_Q.py` seed 701082 | `[VERIFIED]` this session |
| `gate4b_lmcc_in_vperp.py` (paper's saturating LMCC ∈ V⊥) | `[VERIFIED]` prior; not re-run this session |

## Chain split (ACTION ≠ WORLD: here, premise ≠ conclusion)

Our package proves internally:

```text
[VERIFIED] exact instance ⇒ dim V⊥ = 21 < 22 = d
```

The scientific conclusion needs an extra implication:

```text
dim V⊥ < d  ⇒  no single-copy POVM with F^C = F^Q
```

That implication is Observation 2 (paper). Equivalent form in the paper:
`n = dim V⊥ − 1 < d − 1` ⇒ incompleteness of rank-one POVM in V⊥.

## Verdict on sub-steps

### (a) Regular outcomes → projector ∈ V⊥

**HOLD `[PROOF]`.** Re-derived in-project (Cauchy–Schwarz equality conditions for F^C ≤ F^Q
force orthogonality to the W/M generators). Consistent with Hollowization Thm 1 for
positive-probability outcomes.

### (b) Null outcomes → projector ∈ V⊥

**HOLD-WITH-DEPENDENCY.**

- Source Supplemental S1.A/S1.B: null operators automatically satisfy M-conditions;
  W-conditions ≡ paper Eq. (3); hence null projectors also sit in V⊥. `[DOCS, read]`
- Local one-line re-derivation of automatic M for null vectors: **HOLD `[PROOF]`.**
- Remaining: the **iff** between saturation and Eq. (3) for null outcomes is attributed
  by the paper to **Ref. [29]** (Yang, Pang, Zhou, Jordan, PRA 100, 032104) — **not read
  in this project**. `[DOCS, unread]`

So null outcomes are not a silent gap anymore (closed against SM), but the iff still
inherits Ref. [29].

### (c) Counting: all outcomes in V⊥ + Σ E_w = I ⇒ dim V⊥ ≥ d

**HOLD `[PROOF]`.** Dual-basis argument on d linearly independent rank-one projectors;
no need for “reduce POVM to size d” step.

### Observation 2 as a published lemma

**HOLD as application, not as fully independent re-proof of Hollowization Thm 1.**

We independently re-derived the *necessity counting* that makes Obs2 work once every
saturating rank-one outcome lies in V⊥. We did **not** fully re-prove Simultaneous
Hollowization Theorem 1 from first principles for all outcome types without the paper /
Ref. [29].

### Positive control sanity

Paper's own saturating LMCC example: projectors lie in V⊥ (`gate4b`). This checks the
V-builder direction that *can* fail (unlike dim V⊥ ≥ d on that example). `[VERIFIED]` prior.

## Overall U1 status

### Addendum 2026-09-22 (same day) — Ref. [29] read

See `REF29_NULL_IFF_READ_2026-09-22.md`. Null-operator N&S saturation (Theorem 2 of
arXiv:1806.07337 / PRA 100, 032104) was read; maps to 2601 Eq. (3) for null outcomes.

```text
┌─────────────────────────────────────────────────────────────┐
│  HOLD                                                       │
│  (null iff no longer unread; send still needs Obs2 caveat   │
│   naming Hollowization Thm 1 as theirs)                     │
└─────────────────────────────────────────────────────────────┘
```

Prior label was HOLD-WITH-DOCUMENTED-DEPENDENCY (unread Ref. [29]).
Not **GAP**. Residual `[DOCS]`: Hollowization as named theorem of 2601 (counting +
regular + Ref.[29] null N&S now in hand).

## What must appear in any author email (if A proceeds)

1. Exact instance + `verify_exact_Q.py` command.
2. Explicit sentence: non-saturation conclusion **uses Observation 2 / Hollowization
   Theorem 1 of your paper**; null-outcome saturation iff cites Ref. [29], which we did
   not re-prove.
3. Separately: C-ID / C-LB / C-CEIL are ours (elementary), independent of Obs2.
4. Ask: (i) is Obs2/Hollowization correctly applied? (ii) is a generic quasi-pure
   counterexample at d=22,r=2 already known to you?

## Optional pre-send upgrade (not required by HOLD-WITH-DEPENDENCY)

Read Ref. [29] § on null-outcome Fisher convention. If that closes the iff locally →
upgrade label to **HOLD**. If it reveals a scope mismatch for our quasi-pure class →
**GAP** → narrow claim before send.

## U2 / U3 (not closed here)

| ID | Status after this session |
|---|---|
| U2 novelty | still `[WEAK]` / UNRESOLVED — author reply is the discriminating observation |
| U3 third-party reproduce | package frozen; not yet handed to an independent human/system |

## Conditional send rule (locked)

```text
IF Obs2 deep-read == HOLD:   # current outcome after Ref[29] read
    A_allowed := True
    email MUST still name Obs2/Hollowization as theirs (draft v2 does)
ELIF GAP:
    A_allowed := False until claim narrowed
ELIF full BLOCKED:
    A_allowed := False; request authors clarify Obs2 first OR park
```

Agent does **not** send. Owner action + Submission Gate cooling-off.
Draft: `outreach/2026-09-22-authors-email-DRAFT-v2.md`

**H-CAT31-3:** still do not revive in this cycle (attention cost > VoI vs closing U2).
