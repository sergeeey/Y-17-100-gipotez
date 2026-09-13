# Literature check — 2026-09-13

Targeted search (not the `academic-research` skill's 35-80-paper ML-conference workflow — adapted
per the calling instruction, since neither question is ML-conference-shaped). Tools actually used:
`mcp__arxiv__search_papers` (repeatedly rate-limited/timed out — arXiv's own server-side throttle,
not this session's choice), `mcp__semantic-scholar__search_papers` (worked once, rate-limited on
retry), `mcp__inspirehep__search_papers` (returned 0 results both times — expected, InspireHEP is
a high-energy-physics database and neither question is HEP-shaped; recorded as a negative result,
not a tool failure), `mcp__scholarly-lookup__search_by_title`/`find_by_doi` (OpenAlex+Crossref,
worked reliably throughout), `WebSearch`, and `WebFetch` (unreliable on paywalled/compressed PDFs —
several fetches returned garbled or hallucinated summaries from binary PDF streams; every such case
below was cross-checked by downloading the PDF and reading it directly with the `Read` tool instead,
which decodes PDFs properly). Every citation below was independently confirmed via at least one of
these tools — nothing is asserted from memory alone. `[NOT FOUND]` is used explicitly where a real,
multi-query search came up empty.

---

## Question 1: Novelty of the Chebyshev dual-certificate moment bound

**Claim under review** (`decision.md`, Points 47-48): for a nonnegative measure on a fixed,
known, non-uniformly-spaced finite point set `{γ_1,...,γ_L}`, sharing the first `s` raw moments
with a reference measure `x` (total mass 1), the worst-case total mass `K_s(L)` of any other
nonnegative measure `y` on the same points is bounded by
`K_s(L) ≤ (A_s+1)/(A_s-1)`, `A_s = T_s((L+3)/(L-1))`, proved via an explicit LP dual certificate
`q(γ) = [1-T_s(z(γ))/T_s(z_0)]/[1-1/|T_s(z_0)|]`.

### Verdict: **[POTENTIALLY-NOVEL]** — the *machinery* is squarely classical and still an active
research area; the *specific closed form* for this exact discrete, non-uniform geometry was not
located anywhere in the literature searched, despite a real search across the field's core texts,
surveys, and a 2025 paper on the identical general topic.

### What is [CLASSICAL], confirmed

1. **The general problem — bounding a linear functional (including total mass) of a nonnegative
   measure given its first `s` moments, via LP/SDP duality and Chebyshev-type extremal
   polynomials — is 19th/20th-century classical mathematics, continuously developed since.**
   - M.G. Krein & A.A. Nudel'man, *The Markov Moment Problem and Extremal Problems*, AMS
     Translations of Mathematical Monographs vol. 50, 1977 — confirmed via WebSearch/Amazon
     listing and via its citation as ref. [6] in Pinelis 2011 (below): "an extensive circle of
     questions originating in the classical work of P.L. Chebyshev and A.A. Markov."
   - S. Karlin & W.J. Studden, *Tchebycheff Systems: With Applications in Analysis and
     Statistics*, Interscience/Wiley, 1966 — confirmed as ref. [4] in Pinelis 2011.
   - K. Isii, "The extrema of probability determined by generalized moments (I): bounded random
     variables," *Ann. Inst. Statist. Math.* 12 (1960), 119-133 — confirmed via WebSearch/CiNii;
     this is the paper that explicitly frames the worst-case-moment problem as an infinite-LP
     duality problem, predating the SDP-based restatements below by 40+ years.
   - **I. Pinelis, "Tchebycheff systems and extremal problems for generalized moments: a brief
     survey," arXiv:1107.3493 (2011)** — fetched and read in full via the `Read` tool on the
     downloaded PDF (WebFetch's own PDF-to-text repeatedly failed/hallucinated on this and other
     PDFs in this search; every PDF-based claim below was verified this way, not via WebFetch's
     summary). Confirms the exact abstract machinery our problem is an instance of: the
     Carathéodory Principle (an extremal measure for `∫g_{n+1}dμ` s.t. `∫g_i dμ=c_i` is
     supported on ≤`n+1` points), the sharper Tchebycheff/Markov-system version (extremal support
     size ≈`⌊(n+1)/2⌋+1`, i.e. roughly `s/2` points for `s` moment constraints — matching the
     "few active constraints, sparse extremal support" structure any LP-dual view of our own
     problem would predict), and states plainly (Def. 1) that a `T`-system is defined on *any*
     compact Hausdorff space `X` — a finite point set is trivially compact Hausdorff, so the
     framework formally covers the discrete case as a special (in fact simpler) instance of the
     general theory, not something needing separate machinery.
   - Bertsimas & Popescu, "Optimal Inequalities in Probability Theory: A Convex Optimization
     Approach," *SIAM J. Optim.* 15(3), 780-804 (2005) — confirmed via WebSearch/MIT repository;
     the modern SDP reformulation of the same univariate moment-LP-duality problem, explicitly
     citing the Chebyshev/Markov/Krein lineage. Full text fetch of the actual PDF was unreliable
     (WebFetch again produced only a hallucinated "cannot read compressed stream" response), so
     its exact wording on the Chebyshev-polynomial closed form was not directly confirmed —
     flagged honestly as unverified detail, not asserted.
   - **The discrete case specifically has its own decades-old named subfield.** WebSearch
     confirmed "the discrete moment problem" is an established term of art (A. Prékopa and
     collaborators at Rutgers RUTCOR, since the 1990s: e.g. "Discrete Moment Problems and
     Applications," NSF-funded research line; X. Chen & S. He, "The Discrete Moment Problem with
     Nonconvex Shape Constraints," arXiv:1708.02079 / *Operations Research* 2020, confirmed via
     `scholarly-lookup` DOI record `10.1287/opre.2020.1990`) — bounding a linear functional of a
     distribution on *known, fixed, discrete support points* given moments is its own named
     literature, distinct from (but built on) the continuous-interval Chebyshev-Markov-Krein
     theory. This directly answers the novelty check's own sub-question: the discrete-point-set
     restriction is *not* itself a gap in the classical theory — it is a well-established variant
     with its own name and its own body of papers.
   - **This exact class of problem is still an active, currently-publishing research area, not a
     closed textbook topic.** J. Guo, H. Qiu, Z. Wang, X. Zhang, "Exact solving approach to
     moment problems with nonnegative Chebyshev ambiguity sets," *Operations Research Letters*
     63, 2025, DOI `10.1016/j.orl.2025.107349` — confirmed via `scholarly-lookup` (OpenAlex +
     Crossref both list it, `cited_by_count: 0`, consistent with a paper from earlier the same
     year this experiment is running). The title alone ("Chebyshev ambiguity sets," "exact
     solving approach") signals that even now, closed-form/exact solutions for Chebyshev-type
     moment ambiguity sets are a live research contribution, not settled folklore — which weighs
     against treating any specific closed form in this family as automatically "well known."

2. **The specific tool — Chebyshev polynomials as the extremal/minimal-deviation polynomial on an
   interval, and their use as LP dual certificates — is also classical**, independently confirmed
   via a different, unrelated survey: A. Shadrin, "Twelve Proofs of the Markov Inequality" (in
   *Approximation Theory: A Volume Dedicated to Borislav Bojanov*), fetched and read directly —
   this concerns a *different* "Markov inequality" (bounding polynomial derivatives, V. Markov
   1892, priority traced to Chebyshev 1854), not the moment problem, but it independently confirms
   the general fact that Chebyshev/Zolotarev extremal polynomials have been the standard tool for
   this entire family of "worst case over a constrained polynomial/measure class" problems since
   the 1850s-1890s. This is corroborating background, not a direct hit on Q1's own claim — noted
   as such, not conflated with it.

### What was searched for and **not found** as a direct, citable match

- The *exact* closed form `K_s(L) ≤ (A_s+1)/(A_s-1)`, `A_s = T_s((L+3)/(L-1))`, for this specific
  geometry (endpoints `γ_1=2/L`, `γ_L=(L+1)/L`, i.e. an interval `[2/L, 1+1/L]` that itself
  depends on `L`, restricted to a *discrete* point set inside it) — not located verbatim in Krein-
  Nudelman, Karlin-Studden (title/TOC level only, full text not accessible), Pinelis's full-text
  survey, Isii's abstract, the 2025 Guo-Qiu-Wang-Zhang paper's title/abstract-adjacent search
  results, or any other source reached in this session.
- Multiple direct query variants ("discrete Chebyshev system moment problem extremal bound,"
  "worst-case total mass moment matching interval Chebyshev polynomial closed form," "generalized
  Chebyshev inequality dual certificate degree s") surfaced adjacent classical and modern results
  (T-systems, DT-systems, SDP-based Chebyshev ambiguity sets, the discrete moment problem) but no
  single source stating this exact rational-function-of-a-Chebyshev-polynomial form.
- **This is consistent with, not proof of, genuine novelty of the closed form** (a keyword-search
  absence is `[UNKNOWN]`, per this project's own evidentiary standards, not a null result) — the
  formula could plausibly be re-derivable in one line from Karlin-Studden's or Krein-Nudel'man's
  general machinery (both books' full text were not reachable in this session — WebFetch failed
  repeatedly on the one full-text PDF actually located, and no free PDF of either book was found),
  or it could be a genuinely new instantiation. The project's own internal history is itself weak
  supporting evidence for non-triviality: this exact formula required a real, nontrivial parity
  argument (`T_s(-z_0)=T_s(z_0)` for even `s`, forcing `q`'s constant term to vanish) to be
  identified as the load-bearing step before the dual certificate could be verified correct —
  the kind of derivation step a "well-known, direct plug in a textbook formula" would not
  typically require re-deriving from scratch to trust.

### Recommendation on classification

Treat the **general approach** (LP duality for worst-case mass under moment constraints via a
Chebyshev-polynomial dual certificate, on a finite point set) as `[CLASSICAL]` — cite Krein &
Nudel'man (1977), Karlin & Studden (1966), Isii (1960), and Pinelis (2011, arXiv:1107.3493) for
that framework, and Chen & He (2020, arXiv:1708.02079) / Prékopa's discrete-moment-problem line
for the discrete-support-set variant specifically. Treat the **specific closed-form bound and its
correctness proof for this project's own non-uniform geometry** as this project's own derivation
— `[PROJECT-EXACT]`-eligible on its own internal merits (per point 48's independently-verified
dual-feasibility proof), not because it was found stated in the cited literature.

---

## Question 2: Existing concentration results for Lovász theta / SDP statistics on random graphs

| Sub-area | Finding | Citation | Status |
|---|---|---|---|
| Lovász theta, **random circulant graphs specifically** (this project's own object) | **Even the leading-order EXPECTATION is an open problem**, let alone variance. Best known: `√n ≤ E θ(G) ≤ C√(n log log n)` for dense random circulant graphs — an upper/lower bound with an unresolved `√(log log n)` gap, not a determined constant. A companion "Randomstrasse 101" post frames the exact constant as an explicit open conjecture ("Conjecture 18: `E θ(G) = (1+o(1))√n` for random dense circulant graphs"). | Bandeira, Błasiok, Dmitriev, Faure, Kireeva, Kunisky, "The Lovász number of random circulant graphs," arXiv:2502.16227 (Feb 2025) — fetched and read directly (title, authors, abstract, Theorem 1 all confirmed by direct PDF read, not WebFetch's earlier garbled attempt) | **[SEARCHED, NOT FOUND]** for variance/concentration — the field has not even settled the mean's constant for this exact graph family as of a Feb-2025 paper, ~7 months before this check |
| Lovász theta, **Erdős-Rényi `G(n,1/2)`** — closest well-studied relative | A genuine tail-concentration result exists, but for the MEAN, not a variance power law, and not for circulant graphs: `Pr[|θ(G)-μ| > t] ≤ exp(-t^{4/3}/(C log³ n))`, i.e. concentration in a window of width roughly `polylog(n)` — a large improvement over an earlier `O(n^{1/4})`-width bound. A different, sparse-regime result (Coja-Oghlan) gives `O(1)`-width concentration for `p < n^{-1/2}`. Neither paper computes `Var(θ)` directly or gives a power-law rate in `n`. | S. Arora, A. Bhaskara, "A note on the Lovász theta number of random graphs" (2011) — fetched and read directly (full abstract + Theorem 1 confirmed); Coja-Oghlan's sparse-regime result cited therein and independently corroborated by this project's own earlier Point 40 (Feige-Grinberg arXiv:2506.02952, Banks-Kleinberg-Moore arXiv:1705.01194, both re-confirmed as addressing threshold/mean behavior, not variance, consistent with Point 40's own finding) | **[SEARCHED, NOT FOUND]** as a variance-power-law result; **found** as a genuinely relevant, previously-uncited concentration bound worth citing as the closest existing analogue |
| SDP relaxation values generally (max-cut SDP, chromatic-number SDP relaxations `θ̄`, `θ̄_{1/2}`, `θ̄_2`) on random graphs | Constant-length-interval concentration exists for some SDP relaxations of chromatic number at `p < n^{-1/2-ε}`, per WebSearch summary of the same random-graph-SDP literature cluster (Coja-Oghlan and coauthors) | Not independently fetched/read in full this pass (time-budgeted); flagged as a `[WEAK]`, secondary WebSearch-summary-level finding, not independently verified from primary text the way the two entries above were | **[SEARCHED, PARTIAL]** — real but not independently confirmed to primary-source standard in this pass |
| Efron-Stein / bounded-differences applied to combinatorial-optimization values generally | Classical Efron-Stein-Steele machinery is well documented as applicable "out of the box" to combinatorial optimization problems (the standard textbook illustration is TSP-tour-length concentration), and separately to random-polytope volumes (the "Efron-Stein jackknife inequality" for polytopes) — but nothing found addresses the SPECIFIC failure mode this project already found: naive Efron-Stein systematically UNDERESTIMATING the true variance because of a degree-weighting mismatch between the raw per-coordinate difference and the actual dominant contribution | General Efron-Stein-Steele references found via WebSearch (no single canonical paper matched the exact "degree-weighting mismatch" framing) | **[SEARCHED, NOT FOUND]** — no paper located that names or analyzes this specific mismatch mechanism for any SDP-valued or combinatorial-optimization-valued statistic |
| Malliavin calculus / Stein's method / exchangeable pairs for discrete or graph-valued statistics (this project's own "Priority A" live thread) | Confirms and extends Point 40's own prior finding, not a new discovery: Chatterjee & Dey, "Applications of Stein's method for concentration inequalities," *Ann. Probab.* 38(6), 2443-2485 (2010), arXiv:0906.1034, remains the standout genuinely-discrete match — its own stated applications (Curie-Weiss magnetization, **exact large-deviation asymptotics for triangle/subgraph counts in `G(n,p)`**, Ising model) are precisely the "naive bounds too weak, complex dependency" regime this project is in. A follow-on citation search this pass surfaced no paper extending Chatterjee-Dey specifically to SDP-valued statistics (Lovász theta, max-cut value, etc.) — the bridge from subgraph-count concentration to SDP-value concentration via exchangeable pairs appears to be, as Point 41 already concluded, an open, unclaimed research thread rather than a solved one | Chatterjee & Dey (2010); no extension paper found | **[CONFIRMED PRIOR FINDING, NO NEW EXTENSION FOUND]** — this pass specifically tried to close the gap Point 40 left open (retrying InspireHEP/Semantic Scholar) and could not find a discrete-cube/Johnson-scheme second-order-Poincaré analogue, nor an SDP-specific exchangeable-pairs paper. InspireHEP returned 0 results both times it was queried (expected — it is a physics database, not a combinatorics one; recorded as a clean negative, not a tool failure). Semantic Scholar worked on the first retry (10 results returned, none a direct hit — see table row above) and was rate-limited on the second retry within the same session, matching Point 40's own account of this backend's behavior |

**Overall read for Question 2:** the search this pass corroborates, rather than overturns, this
experiment's own Point 40 finding — no ready-made theorem for `Var(θ)` or `Var(log(θ/√n))` on any
random graph model exists in the literature reached, and for the *specific* circulant-graph case,
the field has not yet settled even the expectation's leading constant (a Feb-2025 paper). This is
itself informative: a `n^{-0.9126}` power-law variance estimate with a 95% CI excluding `-1, -0.5,
-2` would, if it survives further scrutiny, be reporting on a quantity nobody else has yet
computed for this graph family — consistent with (not proof of) a genuinely open frontier result,
not a gap in this project's own search discipline.

---

## Recommendation for `decision.md`

Two additions are worth making to the experiment's own record, both because they are new,
independently-verified sources this exact literature check surfaced (not re-statements of what
Point 40 already had): (1) cite **Bandeira, Błasiok, Dmitriev, Faure, Kireeva, Kunisky (arXiv:
2502.16227, Feb 2025)** as direct, dated evidence that even the *expected value*'s leading
constant for `θ` on random circulant graphs is an open problem as of this year — this
substantially strengthens (with a hard citation, not just "no theorem found") the experiment's own
claim that its variance-scaling result targets a genuinely unresolved question, since a field that
has not fixed the mean is very unlikely to have already fixed the variance; and (2) cite **Arora &
Bhaskara's `polylog(n)`-width tail bound for `θ(G(n,1/2))`** as the closest existing concentration
result for Lovász theta on any random graph model, worth naming explicitly as "the nearest
relative in the literature, for a different graph ensemble and a weaker (tail-bound, not
variance-rate) conclusion" rather than leaving the comparison implicit. Neither addition changes
Priority A/B's status (still open, per Point 40/41) — both simply replace "no ready-made theorem
found" with named, dated, independently-read citations that make the same claim checkable by a
future reader without re-running this search.
