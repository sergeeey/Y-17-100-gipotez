# SENT — Channel A, 2026-09-23

Sent by the owner from their own account (sergeikuch80@gmail.com), outside this session's tools.
This file records the exact text as sent, for provenance. It is not a draft; do not re-send from it.

**Date/time:** 2026-09-23, 10:38 (owner's local time, as shown by the mail client)
**From:** Sergey Boyko <sergeikuch80@gmail.com>
**To:** jing.yang.quantum@zju.edu.cn
**Cc:** satoyaimai@yahoo.co.jp, luca.pezze@ino.cnr.it
**Subject:** Question about an exact PCC-compatible generic quasi-pure instance

---

Dear Dr. Yang, Dr. Imai, and Dr. Pezzè,

My name is Sergey Boyko, and I am a researcher affiliated with the Ronin Institute for Independent Scholarship.

I have been studying your work on the geometric criterion for optimal measurements in multiparameter quantum metrology, together with the quasi-pure-state framework from the earlier work.

I am writing about the question of whether the partial commutativity condition (PCC) is sufficient for single-copy saturation of the SLD quantum Cramer-Rao bound for generic quasi-pure states.

In a targeted exact search, I found an instance in the generic quasi-pure class defined by Eq. (12), with

d = 22, r = 2, s = 16.

For this instance, the PCC holds exactly,

Π_r [L_i, L_j] Π_r = 0

for all parameter pairs, and the QFIM is nonsingular, with

rank F^Q = 16.

Using the operator-space construction in your paper, I obtain

dim_R V = 463,
dim_R V_perp = 21,

so

dim V_perp = 21 < 22 = d.

If I understand Observation 2 and the simultaneous hollowization criterion correctly, this would imply that no single-copy POVM can saturate the SLD-QCRB for this model despite the PCC being satisfied.

For the null-outcome part of the optimality conditions, I rely on Ref. [29] as cited in your paper and on the corresponding regular/null-outcome conditions.

The local state family can be realized by unitary conjugation of a rank-2 reference state,

ρ(θ) = exp(-i Σ_i θ_i G_i) ρ_0 exp(+i Σ_i θ_i G_i),

so positivity is preserved by construction. In the exact verification I use an integer-scaled representative of the reference state; it can of course be normalized to unit trace.

I have not proved that this instance is structurally excluded from the special block-classical ancilla subclass of Eq. (16), for which you give a constructive LMCC saturation result. The construction was not designed to belong to that subclass. If it can in fact be represented in the form of Eq. (16), that would be important for me to know, since it would point to a problem in my interpretation.

The computation uses exact arithmetic rather than floating-point numerics. I implemented the verification in two separate ways in the same local research environment. The second implementation was written from scratch and does not import code from the first one. Both implementations use the same mathematical specification and the same input instance, so I regard this as an internal cross-check rather than an external independent reproduction. Both give

dim_R V = 463,
dim_R V_perp = 21.

As a positive control for the construction of V and V_perp, I also applied the same machinery to the LMCC example from your paper and obtained the expected inclusion of the saturating measurement in V_perp.

I also ran simple negative controls. Perturbing one coefficient breaks the PCC condition, while duplicating one block makes the QFIM singular. These are only sensitivity checks of the verification procedure, not independent validation of the main claim.

The instance was selected by search, and I am not claiming that it is typical or generic in a measure-theoretic sense.

Before making any claim of novelty, I would be very grateful for your view on two questions.

1. Is my application of Observation 2 and the hollowization criterion to this generic quasi-pure instance correct? In particular, am I using the full 22-dimensional Hilbert space and the corresponding 484-dimensional real Hermitian operator space correctly, or is there an additional assumption that I may have missed?

2. Are you aware of an explicit PCC-compatible but non-saturable example already known within the generic quasi-pure class?

I am not claiming a new general theorem. If my reading of Observation 2 is correct, the potentially new point is only an explicit exact, search-selected instance within the generic quasi-pure class for which PCC sufficiency was left open.

If useful, I would be happy to send the exact instance together with a small reproducibility package.

Thank you very much for your time.

Best regards,

Sergey Boyko
Researcher
Ronin Institute for Independent Scholarship

---

## Diff against the frozen v4 (`2026-09-23-authors-email-DRAFT-v4.md`, commit `a21a1b5`)

The owner rewrote parts of v4 in their own final pass. Substance of every required skeptic fix (F2, F3, F4, F7, F8, F9, F12, F13, F16) is preserved, in some
places phrased more precisely than v4:

- **Eq.(16) hedge (F2):** rephrased — now explicitly separates "not proved structurally excluded" from "not designed to belong to", and adds a consequence
  ("that would point to a problem in my interpretation") that v4 did not have. Strictly stronger disclosure than v4.
- **Second-implementation disclosure (F3):** rephrased to "I regard this as an internal cross-check rather than an external independent reproduction" —
  same substance as v4, arguably clearer.
- **Positive control (F4):** present, described in prose without naming the internal filename `gate4b_lmcc_in_vperp.py` (correctly — that's an internal
  artifact reference, not something an external reader needs).
- **Question 1 detail (F7):** present (484-dim ambient space, full 22×22 vs support blocks).
- **Parametric family (F8):** present, and additionally states the normalization point explicitly in the email body (`Tr ρ` not stated as 1, "it can of
  course be normalized to unit trace") — this covers F9 in the email itself, where v4 had deferred that fix to `FORMAT.md` only.
- **I/we (F12), search-selection (F13), softened subject (F16):** all present; subject went further than v4's fix, dropping "counterexample" entirely.

Two things v4 had that the sent version does not:
- **F11 (paper identification):** the sent version does not spell out the arXiv numbers of the two source papers in the opening paragraph. Low-risk
  omission — the recipients are the papers' own authors.
- **F14 (cost acknowledgment / low-cost opt-out):** the sent version drops the "I realise this is a request for your time... no obligation to look at it
  at all" paragraph. A stylistic choice, not a correctness issue.

No mathematical claim, number, or hedge was weakened relative to v4. The email is materially at least as careful as the reviewed draft.
