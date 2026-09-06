# substrate_gate.md — 20260906-may1972-tda-ews-peterlake

_Step 2a. Attempted 2026-09-06 before any control could run. Resolved to BLOCKED-INFRASTRUCTURE —
this is a finding about the environment's current network access, NOT about the claim._

## Data access attempts (in order tried)

| # | Path | Result | Detail |
|---|---|---|---|
| 1 | EDI PASTA legacy REST API, `pasta.lternet.edu/package/search/eml` | `403` | `User 'EDI-...(Public Access)' is not authorized to execute service method 'searchDataPackages'` |
| 2 | Same host, `listDataPackageRevisions` on 12 candidate package IDs | `403` (all 12) | Same "not authorized" message — every public/anonymous method on this host is gated now, not just search |
| 3 | `pasta.edirepository.org` (newer host guess) | DNS failure | `ENOTFOUND` — host does not resolve |
| 4 | Resolved the actual DOI (`10.6073/pasta/f618d3b51a53d08021563701a211304f`) → package `knb-lter-ntl.360.2`, confirmed as the exact 2008–2011 Cascade Food Web Resilience Experiment dataset | Package identified `[VERIFIED]` | This IS the right package — the blocker is download, not identification |
| 5 | `pasta.lternet.edu/package/metadata/eml/knb-lter-ntl/360/2` | `403` | `not authorized to execute service method 'readMetadata'` |
| 6 | `portal.edirepository.org/nis/metadataviewer?packageid=knb-lter-ntl.360.2` | `200`, but body is a **Cloudflare Turnstile login page** | EDI's web portal now requires a bot-detection challenge even for metadata viewing. **Not attempted to bypass** — prohibited (CAPTCHA/bot-detection bypass is a hard-blocked action category). |
| 7 | NSF Public Access Repository (PAR) mirror search | Not found | Other NTL-LTER packages (temperature chain 2009–2019, Mendota buoy) ARE mirrored on PAR; this specific 2008–2011 package predates PAR's typical coverage window and has no mirror found |
| 8 | R package `lterdatasampler` (bundles teaching copies of some LTER datasets, public GitHub) | Checked, does not include Cascade/Peter/Paul Lake data | Confirmed via package documentation |
| 9 | Science.org supplementary materials for Carpenter et al. 2011 | `403 Forbidden` | Paywalled/bot-blocked; not attempted to circumvent |

## Verdict

- [ ] `READY`
- [x] `BLOCKED-INFRASTRUCTURE` — the substrate (this session's network access to EDI) cannot honestly
      test the claim right now. **This is not evidence against H-B3-1.** The package exists, is correctly
      identified, and is described as publicly available by EDI's own policy — it is unreachable from here
      today via legitimate (non-CAPTCHA-bypassing) means.
- [ ] `UNTRUSTED-ENVIRONMENT`

## What would resolve this (any one of)

1. **User downloads the package manually** (a human passing EDI's Turnstile challenge is not a bypass)
   from `https://portal.edirepository.org/nis/mapbrowse?packageid=knb-lter-ntl.360.2` and provides the
   CSV file(s) — then this experiment resumes from Step 3 (controls) with real data.
2. **An EDI API token** (if the user has an EDI account) may restore programmatic access to the legacy
   PASTA methods — untested, EDI's current auth model for the REST API was not otherwise discoverable
   from public documentation pages in this session.
3. **A different, already-openly-mirrored dataset** for the same claim — e.g. a lake-manipulation dataset
   already present in `lterdatasampler` or another R-package/Zenodo-hosted teaching corpus — would require
   re-scoping `claim.md`'s Population section, not just swapping a file.

## Fix log

| Attempt | Problem found | Fix applied | Re-run result |
|---|---|---|---|
| 1 | Legacy PASTA REST API returns 403 on every public method tested (search, list, metadata) | None available without credentials | Still blocked |
| 2 | Portal web UI requires Cloudflare Turnstile | None attempted (prohibited to bypass) | Still blocked |

**No further attempts made after (9).** Continuing to probe would mean either guessing at entity IDs
against a server that has already declined every related method (not a legitimate path — indistinguishable
from trying to work around the access control), or attempting the CAPTCHA (explicitly prohibited). Stopped
here per the hard rule: an infrastructure block is reported, not routed around.
