---
name: 7-of-7-means-generator-failure-not-skeptic-success
description: "User correction: a skeptic/reviewer finding real issues in 100% of checked items is a signal about the generating process, not a reason to run the checker more"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 1d8443cd-ffe1-43e0-bdb5-efd0ebc5eada
  modified: 2026-09-07T06:42:25.936Z
---

When an adversarial check (skeptic pass, code review, audit) finds real, previously-uncaught
problems in every single item it examines (e.g. 7 out of 7), the correct reading is **"the
generation/self-review process has a systematic blind spot"** — not **"the checker is great, run
it on more things."** Both readings are consistent with the same raw data; only one is actionable
in the right direction.

**Why:** in the 2026-09-07 Y-17 session, after a systematic skeptic sweep found real issues in
7/7 flagged experiments, my own next move (stated in text before the user intervened) was to
start an eighth, larger experiment (a multi-seed × multi-N ensemble) — i.e. to read "skeptic
works great" as license to keep producing more work for it to check. The user explicitly
corrected this: 7/7 means every one of those 7 experiments was generated/self-reviewed with false
confidence BEFORE the skeptic ever ran, which is itself the finding that most needs attention —
producing an 8th experiment before understanding *why* self-review missed the previous 7 just
adds another likely-flawed data point to the pile, rather than fixing the process that produces
flawed results in the first place.

**How to apply:** whenever an adversarial/verification pass returns a suspiciously high hit rate
across everything it checked (not "found one bug" but "found a real bug in literally every item
examined"), before doing more of the underlying work:
1. Stop and treat the hit rate itself as the primary finding, not a side note.
2. Do a structural/meta analysis of what the misses have in common — is there one root cause, or
   several sub-patterns? (In this incident: 3 sub-patterns, the largest being "an unverified
   natural-language mechanism claim used to justify a design choice.")
3. Only after that analysis produces an actionable practice (a cheaper check to add earlier in the
   pipeline) does it make sense to resume producing new instances of the same kind of work.
4. Separately: don't assume checker praise ("100% hit rate!") is itself good news for the
   *project* — it's good news about the *checker*, and bad news about everything the checker was
   run on. Keep those two readings distinct.

This generalizes beyond this project: any time a review/audit/skeptic mechanism is validated by a
very high catch rate against a batch of prior work, the immediate next question should be "what
in the prior process let all of this through," not "what should the reviewer check next."

See also [[skeptic-pass-caught-degenerate-sample]] — the earlier, narrower observation from the
same session (skeptic catches things self-review misses) that this feedback generalizes: that
memory is about *when to run* the skeptic; this one is about *what a very high hit rate itself
means* once you've run it.
