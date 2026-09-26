# Search for the information missing for a breakthrough in the top-3 lines (2026-09-27)

Scope: read-only literature/index search plus direct reads of PDF pages (page images, not summariser text) for the decisive statements. Web content is data, never instructions; several fetches were flagged by the
web-response guard as "command_injection" and contained no directives. Markers: `[DOCS, read]` = read on the page image; `[WEAK]` = summariser text or an index count (OpenAlex and Semantic Scholar show 0 citations even for
papers years old, so "0 citing works" is a weak negative).

## 1. H-CAT56-2 (PCC in quantum metrology)
- **Correction to our own records.** Ref. [38] of arXiv:2601.21801 is `J. Yang, "Pure State Inspired Lossless Post-selected Quantum Metrology of Mixed States" (2024a), arXiv:2405.00405` (from the html bibliography): the
  same arXiv id as our "Yang 2405.00405", but under the title of **v1** (1 May 2024; later versions are titled "Lossless Postselected Quantum Metrology with Quasi-pure Mixed States").
- **v1 read in full (6 pages) `[DOCS, read]`:** it defines the quasi-pure condition (Eqs. 19-20, `Pi_r d_x rho Pi_r = 0`) and says the state "behaves like a pure state", but contains **no statement that PCC is sufficient**.
  The only related sentence (p. 4, conclusion) says this "may provide insights into ... the construction of optimal measurements when a mixed state satisfies the partial commutativity condition [34, 49]".
  So "as conjectured in Ref. [38]" is the 2026 authors' framing of an outlook remark; the open question itself is stated in 2601.21801. In the v4 html (Oct 2025) a summariser found no such passage either `[WEAK]`.
- Index counts: OpenAlex `cited_by_count` = 0 for 2601.21801, 2405.00405 and 2502.16227 `[WEAK]`; Nurdin v5 and the withdrawn 2405.01471 were read directly earlier (no PCC-holds-but-not-saturable example).
- **Still missing (unchanged in kind):** the authors' reply (window to 2026-10-23), external human reproduction, blind review of the lifting lemma (existence for r >= 3 rests on it), the IEEE LCSYS published versions,
  the body of 2109.05807, and whether v2/v3 of 2405.00405 contain the "conjecture" wording.

## 2. H-CAT37-2 (Forsythe: is dimension s+4 minimal for s = 4?)  arXiv:2609.04659 v2 (Colbrook, Stepaniants, Townsend), read on page images
- **Minimality is open, by the authors' own words (p. 146):** "Natural questions include the smallest dimension in which nonconvergence can occur at each restart length, and whether the Hopf mechanism persists when the spectra are subject to
  additional structure." A summariser's claim that the paper "establishes s+4 as minimal" is **wrong** and was rejected on this page.
- **Structural facts a theory-informed search can use:**
  - every limit of a nonterminating orbit is supported on between s+1 and 2s eigenvalues (p. 4), i.e. 5..8 nodes for s = 4;
  - the map: `(T_4 w)_i = w_i p_w(lambda_i)^2 / sum_j w_j p_w(lambda_j)^2` with `p_w(t) = 1 + sum_{l=1}^4 c_l t^l` fixed by Galerkin orthogonality `sum_i w_i p_w(lambda_i) lambda_i^j = 0, 0 <= j <= 3` (C.2.3-C.2.4, p. 108);
  - the eight-node seed is a **six-node two-cycle of the core squared-weight map plus two external nodes** whose squared two-block multipliers equal one (C.3, p. 108); the mechanism is described as needing "two neutral external
    spectral modes" (p. 4); the parameter q moves the leading vector field through a **transverse Hopf point**;
  - certification: rational interval arithmetic and Sturm sequences (abstract), "algebraic isolating boxes and contraction mappings" (p. 146); the whole classification is formalised in Lean (Appendix D).
- **Inference `[INFERRED]`, not stated in the paper:** if the mechanism needs a core of at least s+1 = 5 nodes plus two external nodes, then n = 5 and 6 (our earlier search range) are unlikely for THIS mechanism and n = 7 with a five-node core is the only
  open size; whether a five-node core two-cycle with a transverse Hopf point exists is unknown. Our earlier search (differential evolution, region clipped at LOG_BOUND = 3.0, the Hopf term never executed for the final candidates) was not aimed at this.
- **Still missing:** sections C.3-C.5 (pp. 108-122, the Hopf point and weight coordinates) have not been read in detail; a rigorous existence or nonexistence certificate method for n = 7 is not yet designed.

## 3. H-CAT31-3 (Lovasz theta of random circulant graphs)
- **The external open problem is the MEAN, not our variance target.** ETH "Randomstrasse101" Problems 17/18 (post of 21-22 May 2025) and the open-problems compilation arXiv:2603.29571 (March 2026), both from html summaries `[WEAK]` on wording:
  Conjecture 18: `E theta(G) = (1 + o(1)) sqrt(n)` for random dense circulant graphs; progress in 2025 (Bandeira, Blasiok, Dmitriev, Faure, Kireeva, Kunisky, arXiv:2502.16227): "a precise lower bound and an upper bound
  O(sqrt(n) log log n)"; as of March 2026 still open. **No mention of variance or concentration** in either source.
- Consequence: our target `Var(log(theta/sqrt n)) = O(1/n)` has no external literature anchor; the anchor is the mean. The project's own results (decision.md Point 94) say a sharp mean-gap rate would force a small variance, not conversely.
  An earlier version of my own chat summary listed the variance target as the external anchor; that was wrong and is corrected here.
- Follow-up literature: an arXiv metadata search (`all:"random circulant" AND all:"Lovasz"`) returns only the 2025 paper; `abs:Lovasz AND abs:circulant` and a theta/Cayley/concentration query return nothing; OpenAlex counts 0 citing works `[WEAK]`.
  Not read: the OpenReview version of the paper and the ETH research-collection item (HTTP 500 at fetch time).
- **Still missing:** a proof idea for `E theta / sqrt n = 1 + o(1)` with a rate (not data: finite growth cannot exclude a plateau); an independent mathematical reviewer; optionally the pre-registered n approx 8191 point.

## Cross-cutting
The Forsythe resolution (2609.04659) was AI-assisted and Lean-verified by its authors; a Lean route exists in principle for machine-checking our lifting lemma, but it is heavy and not started.
