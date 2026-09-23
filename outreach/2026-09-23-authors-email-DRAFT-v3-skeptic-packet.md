# DRAFT v3 for skeptic review, NOT SENT. Context-blind packet: email text + FORMAT.md only.

**To:** jing.yang.quantum@zju.edu.cn
**Cc:** satoyaimai@yahoo.co.jp, luca.pezze@ino.cnr.it
**Subject:** Possible exact counterexample to PCC sufficiency for generic quasi-pure states

---

Dear Dr. Yang, Dr. Imai, and Dr. Pezzè,

My name is Sergey Boyko, and I am a researcher affiliated with the Ronin Institute for Independent Scholarship.

I have been studying your recent work on the geometric criterion for optimal measurements in multiparameter quantum metrology, together with the quasi-pure-state framework introduced in the earlier work.

I am writing because I believe I may have found an exact example relevant to the question left open for generic quasi-pure states: whether the partial commutativity condition (PCC) is sufficient for single-copy saturation of the SLD quantum Cramér-Rao bound.

The construction belongs to the generic quasi-pure class defined by Eq. (12), and has

d=22, r=2, s=16.

For this exact instance, the PCC holds exactly,

Π_r[L_i,L_j]Π_r=0

for all parameter pairs, and the QFIM is nonsingular,

rank F^Q=16.

Using the operator-space construction in your paper, I obtain

dim_R V=463, dim_R V_perp=21,

so that

dim V_perp=21<22=d.

If I understand Observation 2 and the simultaneous hollowization criterion correctly, this implies that no single-copy POVM can saturate the SLD-QCRB for this model, despite the PCC being satisfied.

I have also checked that the construction is not intended to belong to the special block-classical ancilla subclass of Eq. (16), for which you provide a constructive LMCC saturation result. For the null-outcome part of the optimality conditions, I rely on Ref. [29] as cited in your paper, together with the corresponding regular/null-outcome framework.

The computational part uses exact arithmetic rather than floating-point numerics. The same instance has also been reproduced by a second implementation written independently from the first one within our local environment, sharing only the specification and the input instance. Both implementations give the same values

dim V=463, dim V_perp=21.

We also ran simple negative controls: perturbing one coefficient destroys the PCC condition, while duplicating one block makes the QFIM singular. These controls show that the verification gates are sensitive to changes in the instance rather than merely reproducing a fixed expected output.

Before making any claim of novelty, I would be very grateful for your view on two questions:

1. Is my application of Observation 2 / the hollowization criterion to this generic quasi-pure instance correct, or is there an additional assumption that I may have overlooked?
2. Are you aware of an explicit PCC-compatible but non-saturable example already known within the generic quasi-pure class?

I am not claiming a new general theorem. If my reading of Observation 2 is correct, PCC alone need not guarantee single-copy saturation once

dim V_perp<d.

What may be new here is only an explicit exact instance within the generic quasi-pure class for which PCC sufficiency was left open.

If useful, I would be happy to send the exact instance together with a minimal reproducibility package.

Thank you very much for your time and for your work.

Best regards,
Sergey Boyko
Researcher
Ronin Institute for Independent Scholarship
[email]

---

# FORMAT.md — mathematical specification of the referenced instance (seed 701082)

## State

- `d = 22`, `r = 2`, `k = 20`, `s = 16`
- In the eigenbasis: `ρ = diag(1, 2, 0, …, 0)` (support = first `r` coordinates)
- Generic quasi-pure: SLD has the block form
  `L_i = [[0, A_i^†], [A_i, 0]]` with `A_i` a complex `k × r` matrix
- Construction: `A_i = -2i B_i`, where `B_i = Re_i + i Im_i` are stored Gaussian-integer blocks, every entry `|value| <= 78`

## Checks (exact integer arithmetic)

1. PCC: for all `i < j`, the support-support block of `[L_i, L_j]` is the zero `2 x 2` (equivalently `A_i^† A_j` Hermitian for all pairs).
2. QFIM: `F_ij = Re sum_{a=0}^{1} q_a (A_i^† A_j)_{aa}`, weights `q = (1, 2)`. `det F != 0` over Z.
3. `V = span_R{iM, iW}` from the paper's Eq. (11) operators, built from the FULL `22 x 22` `L_i`. `dim_R V` computed as exact integer rank over Q of the `[Re, Im]` stack (FLINT).

## What this does NOT assert (recorded separately, not part of the letter)

- Novelty as settled fact.
- Independence from Observation 2 / Hollowization Theorem 1 / Ref. [29] null-outcome iff (the letter explicitly names this dependency).
- That the found instance is typical (it was search-selected, not sampled at random).
- Anything about the Eq. (16) ancilla subclass, collective measurements, or scalar weighted bounds.
