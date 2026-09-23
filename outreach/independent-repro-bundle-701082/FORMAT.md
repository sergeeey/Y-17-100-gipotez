# FORMAT — seed 701082 exact instance

## State

- `d = 22`, `r = 2`, `k = 20`, `s = 16` (`s` = number of parameters / SLD blocks)
- In the eigenbasis: `ρ = diag(1, 2, 0, …, 0)` (support = first `r` coordinates).
  Unnormalised representative (`Tr ρ = 3`): all checks below (PCC, `det F ≠ 0`, `rank V`)
  are invariant under `ρ → ρ / Tr ρ`, since the weights `q` and `ρ` enter only through
  positive scalar factors that do not change Hermiticity, nonsingularity, or rank.
- Generic quasi-pure: SLD has the block form
  `L_i = [[0, A_i^†], [A_i, 0]]` with `A_i` a complex `k × r` matrix
- Construction: `A_i = -2i B_i`, where `B_i = Re_i + i Im_i` are the stored Gaussian-integer blocks

## Block layout

Each of the 16 blocks is a `20 × 2` complex matrix.

### Flat form (`blocks_flat[j]`, length 80)

```text
indices 0..39  : Re, row-major, shape (20, 2)
indices 40..79 : Im, row-major, shape (20, 2)
```

Decode:

```python
x = blocks_flat[j]  # 80 ints
Re[c, a] = x[c * 2 + a]           # c=0..19, a=0..1
Im[c, a] = x[40 + c * 2 + a]
```

### Structured form (`blocks_Re_Im[j]`)

```json
{ "Re": [[...],[...], ...], "Im": [[...],[...], ...] }
```

each `20 × 2` integer matrices.

## Checks a second verifier should implement

### 1. PCC (exact)

Build full `22 × 22` complex matrices `L_i` as above.
For all `i < j`, the **support–support** block of `[L_i, L_j]` must be the zero `2 × 2`
(equivalently: `A_i^† A_j` Hermitian for all pairs — same constraint).

### 2. QFIM nonsingular

With weights `q = (1, 2)` on the support eigenvalues (`q` is `ρ`'s support diagonal, unnormalised same as `ρ` above):

```text
F_ij = Re sum_{a=0}^{1} q_a (A_i^† A_j)_{aa}      i, j = 1..s
```

`F` is the `s × s = 16 × 16` SLD QFIM. Require `det F ≠ 0` over ℤ (or FLINT / exact det).

### 3. Real dimension of V

`V` is the **real** span of the generators `iM` and `iW` from the paper
(Yang–Imai–Pezzé arXiv:2601.21801 Eq. (11) / our construction):

Support projectors / Pauli-like σ on the `r`-support (4 real generators for `r=2`):
diagonal projectors + off-diagonal hermitean + antihermitean pairs.

For each σ and each `i`: append real/imag vectorisation of `i[σ, L_i]`.
For each σ and each `i < j`: append real/imag vectorisation of
`i (L_i σ L_j − L_j σ L_i)`.

Stack → integer matrix with `544` rows × `2·d² = 968` columns
(project verifier). Rank over ℚ should be **463**, hence

```text
dim V⊥ = d² − rank(V) = 484 − 463 = 21 < 22 = d
```

(Your row count may differ if you use a different but spanning set of σ;
the **rank** must match, not the redundant generator count.)

### 4. Observation 2 (theorem, not arithmetic)

If dim V⊥ < d, then under Obs.2 / Hollowization no single-copy measurement
saturates `F^C = F^Q`. That step is logical, not part of the numeric verifier.

## Dependencies of Path A only

`numpy`, `python-flint` (`flint.fmpz_mat`). No project-local imports.
