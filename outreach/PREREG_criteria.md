# Pre-registration of outcome criteria for the two outreach channels (written BEFORE anything is sent)

Date: 2026-09-20. Frozen result: commit `1fdb5fa`. Status of the claim at freeze: `INTERNALLY VERIFIED / NOVELTY UNRESOLVED`.
Rules: the claim text is not rewritten after answers arrive. Any change caused by an answer is a NEW registered version (new commit, new note), and this file is not edited.

## Channel B: lemma review (`lemma_blind_packet.md`)

- **PASS:** the checker identifies no gap, and can restate the key rank/lifting argument in their own words.
- **FAIL:** the checker names a concrete step that does not follow from the stated hypotheses, or gives a counterexample to it.
- **INCONCLUSIVE:** no answer in 30 days, or the answer is "cannot tell". This does NOT count as PASS.
- Strength ladder for the checker (falsification-ladder.md): another instance of the same model = weak; a different model = medium; independent human = strong. The internal blind pass run on 2026-09-20 is weak and is recorded as such.

## Channel A: authors

- **Active draft (2026-09-23):** `outreach/2026-09-23-authors-email-DRAFT-v4.md` (PASS-SMALL instance seed 701082; Obs2 caveat; context-blind skeptic pass on v3 with verdict SEND-WITH-EDITS, edits applied; NOT SENT). No further text edits planned; the 24h Submission Gate cooling-off is counted from this freeze.
- Superseded: `outreach/2026-09-22-authors-email-DRAFT-v2.md`, `outreach/2026-09-20-authors-email-DRAFT.md`, `outreach/2026-09-23-authors-email-DRAFT-v3-skeptic-packet.md` (skeptic-review packet only, not a send candidate itself).
- **Superseded draft:** `outreach/2026-09-20-authors-email-DRAFT.md` (pre-exact-instance).
- **Send checklist:** `outreach/SEND_CHECKLIST_channel_A.md`.
- Outcome criteria (unchanged by draft v2):
  - **Novelty support:** the authors say they do not know such an example and name no hidden condition that this construction violates.
  - **Novelty FAIL:** the authors cite a publication with the same generic quasi-pure counterexample, or show that the example is outside the class (for instance a violated condition on the SLD support-kernel blocks).
  - **No answer / vague answer:** status stays `NOVELTY UNRESOLVED`. Silence is not support.
- Even a "novelty support" reply is additional evidence only. The literature audit (`experiments/20260920-h-cat56-2-verification-gates/novelty_audit.md`) remains a separate gate.

## Independence

The two channels are run separately. The email does not mention the lemma review, and the reviewer is not told the authors' answer.
