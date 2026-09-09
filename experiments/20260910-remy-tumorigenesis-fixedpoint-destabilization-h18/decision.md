# H-B7-18 — decision.md

## Result

**Hand-derivation confirmed exactly, computationally, before and after review.** At
`PROLIFERATION_STATE` (branch 1) and `PROLIFERATION_STATE_2` (branch 2): `CyclinD1=False`,
`CyclinE1=True`. The state's own `RBL2=False` is consistent with the ORIGINAL rule
(`!CyclinE1 & !CyclinD1 = False`), but NOT with the perturbed rule
(`RBL2 := !CyclinD1 = !False = True`). Applying one synchronous step under the perturbed rules to
either known Proliferation state changes exactly ONE node — `RBL2`, `False → True` — nothing else.
Both states are confirmed fixed points under the ORIGINAL (unperturbed) rules first, as a
sanity/positive-control check, before checking the perturbed case.

**The destabilized trajectory converges cleanly to a NEW `GROWTH_ARREST`-phenotype point
attractor on both branches** — period 1, `fate_label == GROWTH_ARREST` — but this attractor does
NOT string-match either previously-known `GROWTH_ARREST_STATE_1` or `_2` (the ones established in
H-B7-4/9/10/11). This is a genuinely THIRD Growth_arrest-phenotype fixed point, not previously
characterized anywhere in this arc — an honest, more precise finding than "it just goes back to
the known safe state."

## Verdict

**CONFIRMED-SELF-DESTABILIZING.** This directly explains, at the algebraic/mechanistic level, WHY
H-B7-17's `flip_TF_drop_CyclinE1` perturbation abolishes the transient escape entirely (every
`k=1..6` on both branches relapses to `GROWTH_ARREST`) rather than merely shifting the threshold
or hiding it from a 2-marker observation: **the Proliferation attractor itself stops existing as
a stable resting point under this specific rule change.** It is not that the transient clamp fails
to reach `Proliferation` under this perturbation — there is no longer a `Proliferation` state for
it to reach (at least not the two previously-known ones; a structurally different one elsewhere in
the ~2^31-state space is not ruled out, and not claimed to be).

**Sharpest defensible statement:**

> `RBL2 := !CyclinD1` destabilizes both known Proliferation fixed points of this network directly
> — the state's own `RBL2=False` becomes self-inconsistent under the new rule (which evaluates to
> `True` at the exact `CyclinD1=False` value both Proliferation states share), and the resulting
> one-node perturbation cascades to a new, previously-uncharacterized Growth_arrest-phenotype
> point attractor on both bistable branches. This is the mechanistic root of H-B7-17's
> `CRITERION_INVALID` finding: the perturbation does not merely make the escape unobservable or
> shift its timing — it removes the escape's own destination from the dynamical landscape.

## FL Step 8a — Independent Reviewer

Narrowly-scoped, context-asymmetric reviewer pass (single combined script, one invocation):
**`[CONFIRMED-REAL]`** on both sub-claims. Independently reconstructed the full pipeline from
scratch (own `.bnet` parse, own perturbed-rules dict), confirmed the SAME single-node change
(`RBL2`) on one synchronous step for both branches, and confirmed both trajectories converge to a
`GROWTH_ARREST`-phenotype point attractor matching neither named prior state — flagging this
explicitly as "worth stating clearly, not a discrepancy" (matches this document's own framing).

**A genuine incidental verification the reviewer performed, worth recording:** this experiment's
pipeline crosses THREE separately-instantiated `boolean.BooleanAlgebra()` objects (one in H-B7-17's
own module, used to build the perturbation expression; one in H-B7-13's `h1`, used to compile the
base network; one more inside H-B7-3's `run_until_attractor`'s own `h1` reference) — the reviewer
independently confirmed `evaluate_expression`'s symbol substitution works correctly across these
separate instances (name-based equality, not object identity), rather than assuming this was safe.

## Kill Analysis (Anti-Overfitting Gate)

**What was killed:** the possibility that H-B7-17's `CRITERION_INVALID` finding was some artifact
of the transient-clamp protocol specifically (e.g. the clamp simply never manages to reach the
right region of state space under this perturbation) rather than a structural fact about the
perturbed network's own attractor landscape.

**What was NOT killed / established:** the underlying `j*=1` minimal-observability result
(H-B7-14/15) and its partial robustness to the OTHER 3 rule perturbations (H-B7-17) are unaffected
— this experiment traces exactly the one perturbation already flagged as qualitatively different.

**Relaxation Map:**
- **Remove** the "only these 2 known states" restriction: a full or targeted search for OTHER
  Proliferation-phenotype attractors under the perturbed rules (not just checking whether the 2
  known ones survive) was not attempted — the ~2^31 free-node space is too large for brute force,
  but a `pyboolnet`-style targeted search from other candidate starting points is a named, cheap
  next step.
- **Weaken:** characterize the newly-found Growth_arrest attractors themselves (which nodes
  differ from the previously-known `GROWTH_ARREST_STATE_1`/`_2`?) — not done here, a natural,
  cheap follow-up given the states are already in hand.

## Revival Condition

Not applicable (not a REJECT). Forward-looking: the two newly-found Growth_arrest attractors are
themselves worth a one-line characterization (diff against the known states) as a cheap addendum,
not attempted here to keep this experiment scoped to its one pre-registered question.

## Scope note

Direct follow-up to H-B7-17's own explicitly-named open question (decision.md Revival Condition):
"WHY does dropping CyclinE1's input from RBL2's rule abolish the escape entirely, rather than just
shift the threshold?" Answered mechanistically, not just observationally, closing that thread for
the arc's current scope.
