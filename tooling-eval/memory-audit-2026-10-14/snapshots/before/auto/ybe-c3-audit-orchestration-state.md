---
name: ybe-c3-audit-orchestration-state
description: "State of the C3 constant-QYBE completeness audit (E0/E1) as of 2026-10-05 and the orchestrator/executor protocol (Claude verifies, Cursor executes, other LLMs untrusted)"
metadata:
  node_type: memory
  type: project
  originSessionId: 9e1180dc-26dc-4ec8-a457-75a2b7087b55
  modified: 2026-10-05T07:42:19.194Z
---

**Task:** audit whether the 9 known components through D=diag(omega^(i-j)) (R0=S⊗S^-1) in constant quantum YBE on C^3 are all (H9 = "exactly 9" is only a HYPOTHESIS; >=9 is established). Data in `experiments/20261004-c3-obstruction-cas/` (trusted: `C3_STAGE1_INPUT`, `C3_STAGE1_SLICE`; Singular at /home/serge/cas/bin/Singular, WSL).

**Verified facts (2026-10-05):**
- rank dF=48, ker=33, 26-slice after 6 gauge + 1 scale; Qbar (coker-projected quadrics) rank 170, full Q rank 218 (218-170=48). I2 = the 170 Qbar forms.
- T4 (`qybe_tangent_cone_generator.py:171-177`): Q(Xp)!=0 but in im dF => phi_2 != 0 => F|_{D+ker} is NOT the Kuranishi germ; cubic parts need phi_2 correction.
- The 243-equation I_actual with cubic parts (rank 216) and the 38 primes are NOT in the repo; radical/std runs timed out (exit 124 = no result). `obstruction26.sing` is outside the trusted package and has linear monomials.
- coker dim = 729-48 = 681 (not 243): the 243 count needs explanation.

**Plan (E0/E1 only, no claims about total number of components):**
- E0: audit how I_actual was built (phi_2/phi_3 included?).
- E1: per prime P_k: Jacobian rank of Qbar forms at a rational generic point; rank=codim => generically reduced => class A (no same-dimension twins); else exact local length (class B). Group by orbits (T connected fixes primes; only discrete sigma etc. acts).
- E1': vertices of the 6 rank-3 quadric cones (P15,P22,P36,P18,P26,P31); correct 3-jet test is `pi_coker(2Q(X,Y0)+C(X)) ∈ Im J2(X)` with Y_h ranging over ALL ker dF (not ker J2(X)).
- Rigorous sandwich for twins: L_P <= length_P(gr A) <= U_P=length_P(S/I2); blind to thin components inside intersections/Sing/rank-drop loci (search locus B = Crit(P_k)=P_k+I_r(J2)).

**Orchestration protocol (agreed with user):** Claude = orchestrator/verifier, Cursor = executor, user = courier. Channel: `experiments/20261004-c3-obstruction-cas/handoff/` (`TASK_NNN.md`, `REPORT_NNN.md`, SHA256SUMS, `summary.json` <=2KB). Reports must start with `TASK_ID` and `repo@commit`. Task packets follow delegation-contract fields (objective, owned paths, context refs, acceptance criteria, stop condition, forbidden: floats as proof, edits to trusted package, claims on component count, push). Files NOT yet created: user must say "go" for TASK_001 (E1) / TASK_002 (quadric vertices, 3-jet).

**Other LLMs (Gemini, ChatGPT, Kimi): outputs are untrusted until recomputed.** Gemini's "QUADRATIC_CRITICAL_STRATA_AUDIT" was fabricated: SHA256 e3b0c442...b855 is the empty-input hash, witness X15 had 27 entries not 26, vertex dim wrong, assumed rank=codim for all 38 primes (circular with E1), M3 built from ker J2(X) is identically zero. Usable ideas only: Crit(P_k) definition, suspicion on Sing of the 6 quadrics, 3-jet test shape (after fixing).

**Why:** user has few usage limits until Tuesday; wants cheap verification (read hashes/summaries, recompute a sample) not long reads.
**How to apply:** when user says "give Cursor a task", produce TASK_NNN.md from the plan above; treat any pasted report (Cursor/ChatGPT/Kimi/Gemini) by first checking TASK_ID/repo@commit/hashes against what was issued; a mismatched project report (once an audio-capture report was pasted by mistake) is flagged, not accepted. The commit_test_gate stop-hook fires on foreign untracked .py files; answer briefly that no tests were run.

**Update 2026-10-05 (Cursor E0 report, `experiments/20261005-e0-kuranishi/`):** archive sha256 35b70e1a... verified, all 12 SHA256SUMS OK, trusted C3_STAGE1_INPUT unchanged (10/10 OK; note its SHA256SUMS has CRLF -> use `tr -d '\r'`). Report had no TASK_ID/repo@commit (no task was issued).
- Cursor claim "qbar_170.json matches kappa2 only after doubling squares / file ideal != pi_coker(Q)" is REFUTED by my independent mod-p check (p=32003, 700 sample points, own Q verified against Taylor coefficient of F(R0+eps X)): json as-is has span == true kappa2 (rank 170 both); doubling or halving squares gives rank 196. So qbar_170.json and cone_Qbar_170_correct.sing are correct; Cursor's own `kappa2_170.json` has a square-monomial convention differing from the file -> do not use it. My script: scratchpad/check_qbar.py.
- Cursor claims NOT yet verified: kappa3 span rank 651, phi2 formulas, Kuranishi cubic. Consistent with mine: old 216 cubics missing, phi2(Xp)!=0.
