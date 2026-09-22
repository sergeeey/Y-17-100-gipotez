# Ref. [29] read note — null-outcome saturation iff (2026-09-22)

Source: Yang, Pang, Zhou, Jordan, *Optimal measurements for quantum multiparameter
estimation with general states*, Phys. Rev. A **100**, 032104 (2019)
= arXiv:1806.07337v3. This is Ref. [29] of Yang–Imai–Pezzé arXiv:2601.21801.

Read via ar5iv HTML, 2026-09-22. Marker: `[DOCS, read]`.

## What we needed

Whether the **iff** between saturating the per-outcome matrix bound for a **null**
POVM operator and the paper's Eq. (3) / W-orthogonality is actually in Ref. [29],
or only asserted by 2601.21801.

## What Ref. [29] states (verified against HTML)

- Sec. II: defines regular vs null POVM operators (`Tr(ρ Π_k)=0` ⇒ null); notes
  CFIM contributions of type `0/0` need a multivariate limit.
- Sec. III.2: proves the per-operator matrix inequality (their Eq. 9) **for null
  operators**, with an explicit regularization of the CFIM.
- Sec. IV (Theorems on null operators): **necessary and sufficient** saturation
  condition for a null operator — real coefficients `η_{ij}^k` independent of the
  support index `n`, of the form
  `Π_k (L_i − η_{ij}^k L_j) ρ = 0`
  (and equivalent support/kernel projections on the null vectors). Quote frame from
  HTML: *"The matrix bound of the CFIM due to a null operator Π_k is saturated at λ,
  if and only if …"*.
- Also: for **positive-definite** weight matrices, saturation of the **matrix**
  Helstrom bound ⇔ saturation of the **scalar** bound (Lemma 2 / Sec. III.3) —
  independently re-derived in our `proof_and_scope.md` correction 2026-09-20;
  consistent.

## Mapping to 2601.21801

| 2601.21801 | Ref. [29] |
|---|---|
| Eq. (3) null: `⟨ψ_a\|L_i\|π⟩ = η ⟨ψ_a\|L_j\|π⟩`, η real, independent of `a` | null-operator saturation iff above |
| SM S1.A: Eq. (3) ⇔ `⟨π\|W_{ij,ab}\|π⟩=0` | geometric rewrite in 2601; not re-proven here |
| SM S1.B: M-condition automatic for null | local one-line `[PROOF]` already in `proof_and_scope.md` |

## Effect on U1

Previous status: **HOLD-WITH-DOCUMENTED-DEPENDENCY** because null iff was
`[DOCS, unread]` on Ref. [29].

After this read: null-outcome **iff is grounded in a published N&S theorem we have
now read**. Remaining external packaging is Hollowization Theorem 1 of 2601 as a
unified statement (regular + null → every saturating rank-one outcome ∈ V⊥), whose
null half is now traced to Ref. [29] Theorems rather than an unread black box.

**Upgrade:** U1 → **`HOLD`** for the implication
`dim V⊥ < d ⇒ single-copy matrix non-saturation`, with residual note:
Hollowization Thm 1 itself is still `[DOCS]` as a named theorem of 2601 (we re-derived
counting + regular outcomes + now verified null N&S in Ref. [29]; we did not re-typeset
Hollowization as a standalone paper).

Not a novelty claim. Does not authorize sending without owner action / cooling-off.
