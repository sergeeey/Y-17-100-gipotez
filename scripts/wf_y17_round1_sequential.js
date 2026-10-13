export const meta = {
  name: 'y17-top5-round1-sequential',
  description: 'Round 1 resumed SEQUENTIALLY and throttled (one worker at a time, low CPU) after the 2026-10-03 overheating shutdown',
  phases: [
    { title: 'Research', detail: 'one worker per problem, each in its own experiments/ folder' },
    { title: 'Verify', detail: 'context-asymmetric adversarial check of each worker claim' },
  ],
}

const ROOT = 'E:/Проверка Гипотез/работаю над проверкой гипотез/Y-17 100 gipotez'
const PY = 'C:/Users/serge/miniconda3/envs/ape311/python3.exe'

const PREAMBLE = `
You are an autonomous research worker in the Y-17 cross-domain lab. Project root: ${ROOT}
Python: ${PY} (numpy/scipy/sympy available; check before assuming other packages). Today is 2026-10-03.
Background: a literature audit of five open problems is in ${ROOT}/00-catalog/ (file named "Список 50 задач — глубокий аудит ТОП-5, историческая справка (2026-10-03).md"). Read the section of YOUR problem first. NOTE: that audit already had one error corrected (continuous vs discontinuous piecewise-linear systems) - trust only what you verify yourself.

HARD RULES (non-negotiable):
1. Work ONLY inside your own experiment folder: ${ROOT}/experiments/<your-id>/ . Do NOT edit registry/graph.yaml, LAB.md, activeContext.md, CLAUDE.md, anything in ~/.claude, or any other experiment. No git commit, no git push, no pip/conda install (if a package is missing, report it as BLOCKED with the exact name instead of installing).
2. Lab discipline (falsification-ladder): write claim.md FIRST with an explicit kill criterion BEFORE running the main experiment; run a positive control (known-good case with a known answer) and a negative control BEFORE trusting any search result; write decision.md at the end (verdict PROMOTE/REPEAT/REJECT/ARCHIVE with a Kill Analysis if REJECT). A code path that cannot return a nonzero/positive answer on the control is not validated.
3. Evidence honesty: mark every claim [VERIFIED] (tool-confirmed by you), [DOCS], [INFERRED], [WEAK] or [UNKNOWN]. Never fabricate numbers, citations, file names or test results. Every literature fact you rely on must be traced to a primary source you actually opened (use firecrawl_search / firecrawl_scrape tools; arXiv abstracts are not enough for technical claims - read the relevant full text, long results are saved to a file, search them with Grep -o using bounded regex like .{80}keyword.{80}). A claim 'this is new' needs a documented novelty search; absence of evidence is not proof of novelty.
4. Environment gotchas: 'python -c' is blocked by a hook - write script files and run them. Foreground Bash calls time out at ~2 min: run anything longer with run_in_background and read the output file; use print(..., flush=True). Do not run the repo-wide pytest. Do not poll more than needed.
5. Bounded round: stop when your kill criterion is resolved or after about 25 substantial tool iterations, whichever first. A truthful REPEAT/REJECT/'already known' is a good outcome; a false LEAD is the worst outcome. Do not spin on the same approach more than 3 times (change strategy).
6. Prefer existing solutions over building from scratch (Using Wheels First) but verify they actually apply.

7. HARDWARE LIMITS (mandatory - the previous parallel run overheated the user's laptop and powered it off):
   a) NEVER run more than ONE heavy process at a time, and never any other research worker's job. No multiprocessing.Pool / ProcessPoolExecutor / joblib n_jobs>1 / concurrent workers / launching several background jobs at once. If existing scripts in your folder use a Pool or launch parallel jobs (e.g. launch*.sh with several simultaneous runs), change them to run SERIALLY first.
   b) Run EVERY heavy Python job through the throttle wrapper: ${PY} ${ROOT}/scripts/lowprio.py <script.py> [args]  (BLAS limited to 2 threads, BELOW_NORMAL priority). Foreground checks under ~30 s may run plain.
   c) Each single job must finish in at most ~10 minutes of wall time (use chunks / checkpoint files); wait at least 45 seconds (sleep 45) between two heavy jobs so the machine cools. Prefer cheaper methods (smaller grids, fewer random starts, early stopping) over brute force.
   d) Before starting, check that no earlier job of yours is still running (tasklist for python.exe whose command line is a research script; the MCP servers python.exe are normal and must not be touched).

Finish by returning the requested structured report. List in claims_for_independent_verification ONLY concrete, checkable claims (with exact parameters / file paths) that an independent verifier should try to break.
`

const PROBLEMS = [
  {
    key: 'lum-chua-30',
    id: '20261003-lum-chua-continuation',
    brief: `PROBLEM #30: number of limit cycles of planar piecewise linear systems with two zones separated by a straight line, DISCONTINUOUS (Filippov) class. Known (verified): continuous class has at most 1 cycle (Freire et al 1998); discontinuous class: 3 nested cycles constructed (Freire-Ponce-Torres 2014; Llibre-Ponce), uniform upper bound L*<=8 proven (Carmona-Fernandez-Sanchez-Novaes arXiv:2210.12125). Open: exact maximum between 3 and 8.
Existing round-1 work: ${ROOT}/experiments/20261003-lum-chua-discontinuous-pwl-limit-cycles/ (read claim.md, decision.md, run.py). Round 1: 40 random draws found at most 1 cycle -> REPEAT. Code was validated (positive control: TL=-2.0,DL=5.0,aL=aR=0.5,TR=0.5,DR=1.0 has exactly 1 cycle near y=2.8877; never >1 in 35 continuous configs).
YOUR TASK (new folder experiments/20261003-lum-chua-continuation): (a) FIRST make the half-return map fast and reliable (e.g. closed-form solution of each linear zone via eigen/matrix-exponential, or vectorised integration; the existing version costs 1-14 s per 60-point grid and has grid-edge artifacts), and validate it against the slow solve_ivp version on several parameter sets; (b) run the planned continuation: start from the known 1-cycle continuous example and move aL away from aR (also vary other parameters), tracking how the number of sign changes of G(y0)=R(L(y0))-y0 changes, including tangency/birth events and a wider y range; (c) try to reproduce the published THREE nested cycles mechanism (two linear foci, discontinuous matching, Freire-Ponce-Torres 2014 / Llibre-Ponce) - find the paper full text if possible (open versions: arXiv, authors' UAB preprints) - as the real positive control for the discontinuous case; (d) only after (c) works, search for >=4 cycles with structured search near the mechanism. NOTE the Lienard-form half-return map assumes both zones are foci and the switching line x=0; check the sliding-region/ Filippov issue (count only crossing limit cycles). Any claimed >=4 cycles must come with exact parameters and a second independent computation (different method/tolerance) - otherwise report REPEAT.`,
  },
  {
    key: 'yang-baxter-11',
    id: '20261003-ybe-dim3-beyond-acc',
    brief: `PROBLEM #11: classification of solutions of the constant Yang-Baxter equation R12 R13 R23 = R23 R13 R12 for R acting on C^3 (x) C^3. Verified: strict charge-conserving solutions classified in all dimensions; additive charge conservation (ACC) ansatz solved in dim 3 by Hietarinta-Martin-Rowell (arXiv:2310.03816, Proc. R. Soc. A 480 (2024)); general classification without any ansatz is open. Also see arXiv:1806.08400 and arXiv:2609.38290 (notions of equivalence among constant YB operators).
YOUR TASK (folder experiments/20261003-ybe-dim3-beyond-acc): (a) read the full text of arXiv:2310.03816 and extract the explicit solution families; implement the YBE residual (9x9 matrices, tensor-product placement) in numpy and verify (positive control) that their families satisfy YBE to machine precision, and that random matrices do not (negative control); (b) validate a numerical solver on dimension 2 where the classification is known (Hietarinta 1992) - it must rediscover the known families; (c) then search dimension 3 numerically (many random starts, least-squares/Newton on the residual, possibly with a relaxed ansatz such as a weaker charge-conservation or sparsity pattern) for solution families NOT covered by strict-charge or ACC ansatz, and classify what you find (permutation solutions, known deformations, genuinely unexplained). A solution only counts as interesting after you have checked it is not equivalent (by the standard symmetries: basis change P(x)P conjugation, transposition, scaling, etc., see arXiv:2609.38290) to a known family. Report honestly if everything found is already known. Do not claim a classification.`,
  },
  {
    key: 'coxeter-1',
    id: '20261003-coxeter-n3-completeness',
    brief: `PROBLEM #1: hyperbolic Coxeter polytopes of finite volume with n = dim+3 facets. Verified (Felikson-Tumarkin survey page https://www.maths.dur.ac.uk/users/anna.felikson/Polytopes/polytopes.html): none exist for dim>=17 (Tumarkin 2004), unique one in dim 16; compact ones only in dim 2..6 and 8; pyramids over products of three simplices (dim 4..9,13); one-non-simple-vertex case classified by Roberts (arXiv:1511.08451, dim 4..10); full classification across all dims 2..16 is incomplete.
YOUR TASK (folder experiments/20261003-coxeter-n3-completeness): build a small trustworthy toolkit first, then use it. (a) Check whether the tool CoxIter is available locally (do NOT install anything; just look); otherwise implement in Python: Gram matrix of a Coxeter diagram, signature test (n,1), Vinberg's criterion for finite volume / compactness (elliptic and parabolic subdiagrams, each elliptic subdiagram of rank n-1 extends in exactly two ways), f-vector if feasible. (b) Positive controls: validate on polytopes with known answers: Lanner simplices, the simplicial prisms, Esselmann polytopes, Roberts' lists (arXiv:1511.08451) and, if you can obtain the diagram, Tumarkin's unique dim-16 polytope (PDF links on the survey page, e.g. .../poly/16.pdf and .../poly/f3.pdf). Negative control: diagrams known NOT to give finite-volume polytopes. (c) Then run a bounded exhaustive or structured enumeration of Coxeter diagrams with n=dim+3 nodes in a dimension/subfamily where the published classification is incomplete (e.g. only angles pi/2, pi/3, pi/4, pi/5 or pi/6 in dim 5..10; state precisely what family you enumerate) and compare with published lists. Success = either a validated reproduction (useful and honest) or a concrete discrepancy (a diagram your tool says is a finite-volume polytope that is absent from the literature lists) - the latter must be triple-checked (independent implementation of the criterion) before you call it anything. Be explicit about what the enumeration does NOT cover.`,
  },
  {
    key: 'sierpinski-carpet-5',
    id: '20261003-carpet-spectrum',
    brief: `PROBLEM #5 (replacement version): spectrum of the graph Laplacian on Sierpinski CARPET graph approximations. Verified: for the Sierpinski GASKET the spectrum is completely described by spectral decimation (Fukushima-Shima 1992: eigenvalue recursion with the map R(z)=z(5-z) for the standard gasket graph Laplacian up to normalisation); for the CARPET the survey arXiv:1902.03408 (discrete magic carpets) states they see no evidence of the spectral decimation property. Also useful: arXiv:1302.4007 (decimation method survey) and arXiv:2308.00185.
YOUR TASK (folder experiments/20261003-carpet-spectrum): (a) positive control FIRST: build gasket graphs levels 1..7, compute Laplacian spectra (scipy.sparse.linalg / dense eigvalsh up to a few thousand vertices) and reproduce spectral decimation numerically (verify that level n+1 eigenvalues are preimages of level n eigenvalues under the known polynomial map, with the correct multiplicities, and that spectral dimension estimated from the counting function is near ln9/ln5=1.365); (b) then build Sierpinski carpet graphs (vertex graph on the lattice points of the carpet, levels 1..4 or 5 as far as memory allows; define the graph precisely and state your choice) and compute spectra; (c) test the decimation question as a falsifiable claim with a pre-registered kill criterion: is there a low-degree polynomial or rational map R (degree<=6) such that spec(level n+1) is contained in R^{-1}(spec(level n)) up to tolerance 1e-8 (try: search for relations via the gasket-validated test, e.g. test whether sets of eigenvalue sums/products are algebraically related; compare multiplicity patterns; plot-free numeric tests only)? Estimate also the spectral dimension from Weyl counting and compare with literature values (state the source you found; walk dimension of the carpet ~2.097 numerically, verify via a source). Report honestly: most likely outcome is 'no decimation found at tested degrees' (a REJECT of that narrow claim with a clear Kill Analysis), which is a legitimate result. Do not claim anything about analytic non-existence.`,
  },
  {
    key: 'diff-difference-17',
    id: '20261003-ddeq-lax-verification',
    brief: `PROBLEM #17: integrable (1+1)-dimensional evolutionary differential-difference equations with matrix/vector variables. Verified: S. Igonin, arXiv:2604.26870 (April 2026) 'On matrix Lax representations for (1+1)-dimensional evolutionary differential-difference equations' and the earlier arXiv:2410.01474; scalar five-point classification arXiv:1708.02456; symmetry approach Mikhailov-Shabat-Yamilov.
YOUR TASK (folder experiments/20261003-ddeq-lax-verification): this is verification-first, not discovery-first. (a) Read the full text of arXiv:2604.26870 (HTML version works; long files are saved to a file, use Grep -o with bounded regex) and extract concretely: the definition of a matrix Lax representation (zero-curvature condition for u_t = F(u_{k..m}), shift operators), gauge equivalence, the 'fake MLR' notion, and at least two explicit new two-component equations with their Lax representations and Miura-type transformations; (b) implement in sympy a checker for the differential-difference zero-curvature condition D_t(L_n) = M_{n+1} L_n - L_n M_n (with u_{n+j} as independent symbols, shift operator acting on symbols) and validate it on a textbook positive control (Volterra/Toda lattice with the known Lax pair) and a negative control (the same equation with a perturbed Lax matrix); (c) verify the paper's explicit examples (Lax pair satisfies the condition identically; Miura transformation maps solutions to solutions: check by substitution); (d) additionally test numerically/symbolically whether the symmetry-approach necessary condition (existence of a higher symmetry of order 3 or 5, solve for coefficients via linear algebra over a polynomial ansatz) holds for one of the two-component equations. Report any equation that FAILS a claim of the paper as a concrete discrepancy (triple-check your own implementation before reporting). Honest expected outcome: reproduction of published results; a discrepancy is possible but must be proven.`,
  },
]

const WORKER_SCHEMA = {
  type: 'object',
  properties: {
    problem: { type: 'string' },
    experiment_dir: { type: 'string' },
    status: { type: 'string', enum: ['LEAD', 'REPEAT', 'REJECT', 'BLOCKED', 'ALREADY_KNOWN'] },
    summary: { type: 'string' },
    positive_control: { type: 'string' },
    negative_control: { type: 'string' },
    findings: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          claim: { type: 'string' },
          evidence_marker: { type: 'string' },
          how_verified: { type: 'string' },
          artifact_path: { type: 'string' },
        },
        required: ['claim', 'evidence_marker', 'how_verified'],
      },
    },
    claims_for_independent_verification: { type: 'array', items: { type: 'string' } },
    literature_checked: { type: 'array', items: { type: 'string' } },
    caveats: { type: 'array', items: { type: 'string' } },
    next_round: { type: 'string' },
  },
  required: ['problem', 'experiment_dir', 'status', 'summary', 'positive_control', 'negative_control', 'findings', 'claims_for_independent_verification', 'caveats', 'next_round'],
}

const VERDICT_SCHEMA = {
  type: 'object',
  properties: {
    problem: { type: 'string' },
    verdicts: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          claim: { type: 'string' },
          verdict: { type: 'string', enum: ['CONFIRMED', 'WEAKENED', 'REFUTED', 'UNVERIFIABLE'] },
          reason: { type: 'string' },
          method: { type: 'string' },
        },
        required: ['claim', 'verdict', 'reason', 'method'],
      },
    },
    process_issues: { type: 'array', items: { type: 'string' } },
    overall: { type: 'string' },
  },
  required: ['problem', 'verdicts', 'process_issues', 'overall'],
}

phase('Research')
const ORDER = ['sierpinski-carpet-5', 'diff-difference-17', 'lum-chua-30', 'coxeter-1', 'yang-baxter-11']
log('SEQUENTIAL throttled run, order: ' + ORDER.join(' -> '))

const RESUME =
  'RESUME NOTICE: earlier attempts at this exact task were interrupted by infrastructure failures (session limit, then a machine shutdown from overheating), NOT by a scientific outcome. The folder experiments/<ID>/ already contains partial work (claim.md, scripts, logs, possibly result files, no decision.md). Do NOT start from scratch and do NOT delete it: read claim.md, list the folder, re-read the logs, treat earlier outputs as UNVERIFIED (re-run what you rely on, treat files named *bug* as known-bad), then continue and finish the round (decision.md + structured report). Apply rule 7 (hardware limits) to everything you run, including anything you re-run.\n\n'

const out = []
let failures = 0
for (let i = 0; i < ORDER.length; i++) {
  const p = PROBLEMS.find((x) => x.key === ORDER[i])
  log('[' + (i + 1) + '/' + ORDER.length + '] ' + p.key)
  let worker = null
  let claimsText = ''
  if (p.key === 'diff-difference-17') {
    // worker already finished earlier (ALREADY_KNOWN); only the independent verification is missing
    worker = { experiment_dir: ROOT + '/experiments/' + p.id, done: true }
    claimsText = 'Attack the pre-registered claims C1-C5 exactly as written in claim.md of the audited folder (and the printed identities of arXiv:2604.26870 they refer to). Do not rely on the author\'s decision.md.'
  } else {
    worker = await agent(
      PREAMBLE + '\nYOUR EXPERIMENT FOLDER ID: ' + p.id + '\n\n' + RESUME.replace('<ID>', p.id) + p.brief,
      { label: 'research:' + p.key, phase: 'Research', schema: WORKER_SCHEMA },
    )
    if (worker) {
      claimsText = (worker.claims_for_independent_verification || []).map((c, k) => (k + 1) + '. ' + c).join('\n')
    }
  }
  if (!worker) {
    failures++
    log('worker for ' + p.key + ' returned nothing (failed/skipped); failures in a row: ' + failures)
    out.push({ problem: p.key, worker: null, verifier: null, note: 'worker failed' })
    if (failures >= 2) { log('two failures in a row - stopping the queue to avoid burning budget'); break }
    continue
  }
  failures = 0
  let verifier = null
  if (claimsText.length > 0) {
    verifier = await agent(
      'You are an independent adversarial verifier (falsification agent). Your job is NOT to confirm but to break. Another agent produced research in a folder.\n' +
      'Project root: ' + ROOT + '\nPython: ' + PY + ". 'python -c' is blocked by a hook: write script files. HARDWARE LIMITS (the machine overheated before): one heavy process at a time, run every heavy Python job as " + PY + ' ' + ROOT + '/scripts/lowprio.py <script.py>, no multiprocessing, jobs under ~10 minutes, sleep 45 between heavy jobs, do not run repo-wide pytest. No git, no installs.\n' +
      'Folder to audit: ' + worker.experiment_dir + '\nRead claim.md, the code and the controls there. Claims to attack:\n' + claimsText +
      '\n\nFor EACH claim: (1) re-derive or re-compute it by an INDEPENDENT method (different implementation / integrator / tolerance / library or a symbolic check) - do not just rerun their script; (2) try at least one attack designed to make it fail; (3) check cited literature facts against a primary source you open yourself; (4) check process issues: was a positive control that can return a positive answer actually exercised, are controls meaningful, is anything marked [VERIFIED] that was not. Write your verdict as skeptic_verdict.md in the audited folder (the only file you may create/edit there). Default to REFUTED/UNVERIFIABLE when evidence is thin. Return the structured verdict.',
      { label: 'verify:' + p.key, phase: 'Verify', schema: VERDICT_SCHEMA },
    )
  }
  out.push({ problem: p.key, worker, verifier })
  log('done ' + p.key + ': worker=' + (worker.status || 'prior') + ', verifier=' + (verifier ? 'ok' : 'none'))
}

log('Sequential round finished: ' + out.length + ' problems processed')
return out
