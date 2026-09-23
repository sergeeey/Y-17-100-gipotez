# DRAFT v4, NOT SENT. Channel A: email to authors of arXiv:2601.21801

Status: draft assembled 2026-09-23, after a context-blind skeptic pass on v3 (packet: `outreach/2026-09-23-authors-email-DRAFT-v3-skeptic-packet.md`,
verdict SEND-WITH-EDITS, 7 required fixes). Sending remains the human owner's action (Submission Gate 24h cooling-off, fresh from this edit). Agent does not send.

Contact addresses cross-checked twice: arXiv:2601.21801v1's own footnotes, and independently, Imai/Yang/Pezzè's later PRL 136, 150801 (2026) lists
the same three corresponding-author addresses — two sources, three months apart, same emails.

**To:** jing.yang.quantum@zju.edu.cn
**Cc:** satoyaimai@yahoo.co.jp, luca.pezze@ino.cnr.it
**Subject:** Possible exact counterexample to PCC sufficiency for generic quasi-pure states — request for a correctness check

---

Dear Dr. Yang, Dr. Imai, and Dr. Pezzè,

My name is Sergey Boyko, and I am a researcher affiliated with the Ronin Institute for Independent Scholarship.

I have been studying your recent work on the geometric criterion for optimal measurements in multiparameter quantum metrology, together with the quasi-pure-state framework introduced in the earlier work (arXiv:2601.21801 and arXiv:2405.00405; equation numbers below refer to arXiv:2601.21801).

I am writing because I believe I may have found an exact example relevant to the question left open for generic quasi-pure states: whether the partial commutativity condition (PCC) is sufficient for single-copy saturation of the SLD quantum Cramér-Rao bound.

The instance was found by a search over Gaussian-integer SLD blocks and then verified in exact arithmetic; it is not claimed to be typical. It belongs, as I read it, to the generic quasi-pure class defined by Eq. (12), with

d = 22, r = 2, s = 16.

For this exact instance, the PCC holds exactly,

Π_r[L_i,L_j]Π_r = 0

for all parameter pairs, and the QFIM is nonsingular,

rank F^Q = 16.

Using the operator-space construction of your Eq. (11), I obtain

dim_R V = 463, dim_R V_perp = 21,

so that

dim V_perp = 21 < 22 = d.

If I understand Observation 2 and the simultaneous hollowization criterion correctly, this implies that no single-copy POVM can saturate the SLD-QCRB for this model, despite the PCC being satisfied. The pair (ρ, {L_i}) extends to a genuine parametric family, not just a single point: ρ(θ) = exp(-i Σθ_i G_i) ρ_0 exp(+i Σθ_i G_i) with G_i = [[0, B_i^†],[B_i, 0]], whose first derivative at θ=0 reproduces the stated SLDs, and unitary conjugation preserves positivity at every order, not only to first order.

The construction was not designed to lie in the block-classical ancilla subclass of Eq. (16), for which you provide a constructive LMCC saturation result. I want to be explicit that I have no proof of exclusion: I have not verified that the instance falls outside that subclass, and I would welcome a correction if it does. For the null-outcome part of the optimality conditions, I rely on Ref. [29] as cited in your paper.

The computational part uses exact arithmetic rather than floating-point numerics. I wrote a second implementation from the same written specification, and it returns the same numbers. This only guards against coding mistakes on my side: both implementations are mine, ran on the same machine, and share the same reading of your definitions, so a misreading of Eq. (11) or Observation 2 would be reproduced by both. There has been no external or independent verification of this result.

I also ran simple controls on the PCC and QFIM gates: perturbing one coefficient destroys the PCC condition, and duplicating one block makes the QFIM singular. As a check on the rank computation itself, I ran the same pipeline on your own published saturating example (the two-qubit-plus-ancilla case in your End Matter) and confirmed that its measurement projectors lie in the orthogonal complement V_perp, exactly as your theorem requires — i.e. the same code correctly reports a case where the bound is not violated.

Before making any claim of novelty, I would be very grateful for your view on two questions:

1. Is my application of Observation 2 / the hollowization criterion to this generic quasi-pure instance correct? Concretely: I build the Eq. (11) operators from the full 22×22 SLDs (not their support blocks), and I take V_perp inside the 484-dimensional real space of Hermitian 22×22 matrices. Is that the intended reading, or is there an additional assumption I may have overlooked?
2. Are you aware of an explicit PCC-compatible but non-saturable example already known within the generic quasi-pure class?

I am not claiming a new general theorem. If my reading of Observation 2 is correct, PCC alone need not guarantee single-copy saturation once dim V_perp < d. What may be new here is only an explicit exact instance within the generic quasi-pure class for which PCC sufficiency was left open.

I realise this is a request for your time. Even a one-line reply — "this is already known" or "the criterion does not apply as you read it" — would be extremely valuable, and of course there is no obligation to look at it at all. If useful, I would be happy to send the exact instance together with a minimal reproducibility package.

Thank you very much for your time and for your work.

Best regards,
Sergey Boyko
Researcher
Ronin Institute for Independent Scholarship
[your email]

---

## Changelog vs v3 (skeptic-reviewed, 2026-09-23)

Required fixes applied (skeptic packet verdict: SEND-WITH-EDITS):

- **F2** — "I have also checked that the construction is not intended to belong to..." (claimed a check that was never run, and directly contradicted the packet's own "does NOT assert" list) → replaced with an explicit "no proof of exclusion" hedge.
- **F3** — "written independently... sharing only the specification and the input instance" (reads as independent replication) → replaced with an explicit same-author, same-machine, same-reading-of-definitions disclosure. Matches this project's own internal label (`medium`, same-lab, NOT external U3) instead of overstating it.
- **F4 (partial)** — the two negative controls (PCC, QFIM) don't touch the load-bearing rank computation. Added: the paper's own published LMCC saturating example, run through the same rank/V pipeline, correctly lands in V_perp (`experiments/20260920-h-cat56-2-verification-gates/gate4b_lmcc_in_vperp.py`, verified 2026-09-20 and re-run 2026-09-22) — a real positive control on the step the conclusion actually rests on. The instance/gate4b files themselves are still not attached (see below).
- **F7** — added the full-22×22-vs-support-block and the 484-dimensional ambient space explicitly to question 1, so it is answerable in one line.
- **F8** — added the parametric-family sentence (unitary conjugation, all-order positivity), pre-empting the most likely first technical question. Derivation: `experiments/20260920-h-cat56-2-verification-gates/lifting_lemma.md` § "Things a checker should attack" (last bullet).
- **F11** — both source papers now named with arXiv numbers; equation numbers pinned to 2601.21801.
- **F12** — "we/our" → "I/my" throughout (single-author disclosure).
- **F13** — added: the instance was search-found, not claimed typical.
- **F14** — added an explicit acknowledgment of the time cost and a cheap one-line-reply opt-out.
- **F16** — subject softened from a bare "counterexample" to "...— request for a correctness check", matching the hedged body text.
- **F19** — dropped "rather than merely reproducing a fixed expected output" (defensive, in-project jargon, adds nothing for this audience).

Left as-is, deliberately:

- **ZIP / instance not attached** — the owner's explicit prior choice ("не прикладывал бы ZIP к первому письму"); offered on request only, per F14's advice this is now paired with an explicit low-cost opt-out so the request doesn't read as demanding a second round.
- **F9 (Tr ρ = 3, unnormalised)** — the email body never states ρ's numeric entries; this affects `FORMAT.md`/the instance package, not this letter, and should be fixed there before anything is actually sent to the authors on request.
- **F10 (Eq. 12 "genericity" not independently checked)** and **F15 (`s`, size of `F` not spelled out)** — same: these are `FORMAT.md`-level fixes, not email-level, deferred until the package itself is prepared for sending.
- **F20 (titles/affiliation unverified)** — owner's own information; not mine to verify or change.
- **F1, F5, F6, F17, F18, F21** — artifacts of the skeptic packet's condensed FORMAT.md excerpt, not real gaps in the actual bundle `FORMAT.md` (re-checked directly: it already defines the ambient space, `dim V_perp = 484 - 463 = 21`, the index ranges for the generators, and row/column counts). No email-text action needed.

## Still open before actual send (not part of this edit)

- `outreach/independent-repro-bundle-701082/FORMAT.md`: fix `Tr ρ = 3` (F9) and spell out `s` / size of `F` (F15) before the bundle is offered on request.
- Titles/affiliation line (F20) — owner to verify.
- 24h cooling-off from this edit.
