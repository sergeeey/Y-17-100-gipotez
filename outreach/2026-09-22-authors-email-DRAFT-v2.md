# DRAFT v2, NOT SENT. Channel A: email to authors of arXiv:2601.21801

Status: draft updated 2026-09-22 after PASS-SMALL exact instance + Obs2/Ref.[29] deep-read.
Sending remains the **human owner's** action (Submission Gate 24h cooling-off).
Agent does **not** send.

Frozen reproduce package (local paths; commit hash to be filled by owner at send time):
- `experiments/20260920-small-exact-qi-instance/PACKAGE_FREEZE_2026-09-22.md`
- instance seed **701082**, `verify_exact_Q.py`

**To:** jing.yang.quantum@zju.edu.cn, satoyaimai@yahoo.co.jp, luca.pezze@ino.cnr.it
(addresses as printed on arXiv:2601.21801v1)
**From:** Sergey Boyko (project owner)
**Subject:** Explicit Gaussian-integer candidate counterexample to PCC sufficiency for generic quasi-pure states — is it known?

---

Dear Dr. Yang, Dr. Imai, Dr. Pezzè,

I have been working through arXiv:2601.21801 and the open question on PCC sufficiency for generic quasi-pure states (your citation of Ref. [38] / arXiv:2405.00405). I am writing with one concrete object and two narrow questions. I am **not** claiming an independent theorem that replaces yours.

**Exact candidate.** Generic quasi-pure state in the sense of your Eq. (12) (Π_r ∂_i ρ Π_r = 0), Hilbert dimension d = 22, rank r = 2, s = 16 parameters. All SLD blocks A_i = −2i B_i are given by 16 explicit 20×2 **Gaussian-integer** matrices B_j (every real/imaginary entry has absolute value ≤ 78). Exact integer checks give: PCC on the full 22×22 commutators; nonsingular QFIM (Bareiss / FLINT det ≠ 0); and exact rank over ℚ of the real [Re, Im] stack of the iW/iM generators equal to **463**, hence dim V⊥ = **21 < 22**. By your **Observation 2** (and Simultaneous Hollowization Theorem 1), this implies the single-copy matrix QCRB is not saturable. A second floating-point / modular family exists at d = 23, r = 3, s = 12 (dim V⊥ = 22). By a rank-nullity lower bound on dim V⊥ the certified test cannot fire for r = 2 with d ≤ 21, so d = 22 is the first size where it can.

**Dependence (stated explicitly).** The non-saturation step uses your Observation 2 / Hollowization Theorem 1. I re-derived the counting argument (every saturating rank-one outcome in V⊥ ⇒ dim V⊥ ≥ d) and the regular-outcome necessity; for null outcomes I checked your Supplemental S1 against Ref. [29] (Yang–Pang–Zhou–Jordan, PRA 100, 032104 / arXiv:1806.07337) and treat the null N&S saturation condition as theirs. I have **not** rewritten Hollowization as a standalone proof independent of your paper.

**Separately ours (elementary).** For PCC quasi-pure states, dim V⊥ = r² + dim P + dim Q with explicit P, Q; a rank-nullity lower bound; and the first dimensions where the bound can drop below d (22 for r=2, 23 for r=3, …).

**Questions.**
1. Is a PCC-satisfying, non-saturable **generic** quasi-pure example (Eq. 12, not only Eq. 16) already known to you, or did I miss prior work?
2. Is there an implicit condition in “generic quasi-pure” (e.g. on support–kernel blocks of the SLDs) that this construction violates?

**Reproduction (~seconds; needs numpy + python-flint):**

```text
python experiments/20260920-small-exact-qi-instance/verify_exact_Q.py \
  experiments/20260920-small-exact-qi-instance/instance_d22_r2_s16.jsonl \
  701082
```

Expected JSON fields include: `dimV_over_Q_exact: 463`, `dimVperp_exact: 21`,
`fires_dimVperp_lt_d: True`, `pcc_exact_full_commutators: True`.
Package note: `PACKAGE_FREEZE_2026-09-22.md`. Earlier float/modular checks:
`experiments/20260920-h-cat56-2-verification-gates/`.

[OPTIONAL, owner's choice: Computations used AI-assisted tooling; I reviewed the
artifacts but I am not a specialist in this area, so a short sanity check would
help most.]

A one-line “known / not known / condition violated” would already help a lot.

Best regards,
Sergey Boyko
GitHub: sergeeey

---

## Changelog vs v1 (2026-09-20)

- Added PASS-SMALL exact instance (seed 701082); removed “no rational instance”.
- Softened claim language; explicit Obs2/Hollowization/Ref.[29] dependence.
- Pointed reproduce command to `verify_exact_Q.py` instead of float orchestrator only.
- Still NOT SENT.
