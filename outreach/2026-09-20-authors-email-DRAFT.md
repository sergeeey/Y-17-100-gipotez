# DRAFT, NOT SENT. Channel A: email to the authors of arXiv:2601.21801

Status: draft prepared 2026-09-20. Sending is the human owner's action, after the 24 h cooling-off required by the project's Submission Gate.
Frozen package: commit `1fdb5fa` of https://github.com/sergeeey/Y-17-100-gipotez (anything committed later is a new version).

**To:** jing.yang.quantum@zju.edu.cn, satoyaimai@yahoo.co.jp, luca.pezze@ino.cnr.it  (addresses as printed on arXiv:2601.21801v1)
**From:** Sergey Boyko (project owner)
**Subject:** Possible counterexample to PCC sufficiency for generic quasi-pure states: is it known?

---

Dear Dr. Yang, Dr. Imai, Dr. Pezzè,

I have been working through arXiv:2601.21801 and the conjecture about generic quasi-pure states from Ref. [38] (arXiv:2405.00405). I have a numerically found candidate counterexample and one question. I am not claiming a theorem.

**Candidate.** Generic quasi-pure state in the sense of Eq. (12) (Π_r ∂_iρ Π_r = 0), Hilbert dimension d = 22, rank r = 2, s = 16 parameters. The partial commutativity condition holds (full-commutator residual ~1e-14), the QFIM is nonsingular, and with V built exactly as in your Eq. (11) I get dim V = 463 of 484, i.e. dim V⊥ = 21 < d = 22. By your Observation 2 the QCRB is then not saturable. A second configuration is d = 23, r = 3, s = 12 (dim V⊥ = 22). By a rank-nullity count the test provably cannot fire for r = 2 with d ≤ 21, so d = 22 is the first size where it can.

**How well it is checked.** Reproduced with independently written full-matrix code (different sampler, random unitary basis change, several seeds), stable for the spectrum p_2 from 0.4 to 1e-6; an exact modular-arithmetic certificate over F_p exists. I do not have an explicit rational instance, and my argument that a Gaussian-rational instance exists (a lifting from F_p) has not been independently checked.

**Question.** Is such an example already known to you, or is there prior work I missed? Or is there a condition implicit in "generic quasi-pure" (for instance on the support–kernel blocks of the SLDs) that this construction violates?

**Reproduction (about 2 seconds, numpy only):** commit `1fdb5fa`, file `experiments/20260919-pcc-generic-quasipure-cat56-2/orchestrator_independent_check.py`, run `python orchestrator_independent_check.py`. Expected first lines: `d=22 r=2 s=16 ... dimV=463 dimVperp=21 fires=True`; the control `d=21, s=16` prints `dimVperp=21 fires=False`. Notes and the write-up of the checks: `experiments/20260920-h-cat56-2-verification-gates/decision.md`.

[OPTIONAL, owner's choice: The computations were done with AI-assisted tooling; I have reviewed the results and the write-up but I am not a specialist in this area, so I would value a quick sanity check most of all.]

Thank you for your time. A one-line "known / not known" would already help a lot.

Best regards,
Sergey Boyko
GitHub: sergeeey
