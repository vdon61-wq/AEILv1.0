# Changelog

All notable changes to the AEIL specification and benchmark. Format follows the project's
own rule in `SPECIFICATION.md` §13: patch = documentation/non-behavioral fixes,
minor = backward-compatible additions, major = changes to dimensions, scoring or benchmark
semantics.

## [1.1.0] — draft, proposed

### Added — normative
- `MEMORY.md` — **AEIL Emotional Memory** module: the Emotional Event object (observation
  separated from inference, per-inference confidence, cause, outcome, supersession links,
  purpose, legal basis, retention), seven memory operations, state-update rules SU-1…SU-6,
  retention and data-subject rights, the Memory Provider Interface MPI-1…MPI-5, and the
  audit addendum (Agent Audit Phase 4bis).
- `POLICY.md` — **AEIL Behavioral Policy**: policy object, eleven standard action classes
  (`ACK_PRIOR`, `TONE_SHIFT`, `OFFER_ACTION`, `HOLD`, `DEESCALATE`, `CLARIFY`, `HANDOFF`,
  `REFUSE`, `CONFIRM`, `WRITE_MEMORY`, `FORGET`), mandatory floor BP-1…BP-10, and the new
  **undeclared adaptation** finding.
- `RESPONSIBLE_USE.md` — prohibited uses PU-1…PU-12, restricted uses RS-1…RS-6,
  transparency obligations, regulatory alignment (EU AI Act Art. 5(1)(a),(b),(f),(g),
  Annex III; GDPR; ISO/IEC 42001; ISO/IEC 23894; NIST AI RMF) and the **AUP gate**.
- `SPECIFICATION.md` §4bis — the **AEIL-M (Memory-to-Behavior Linkage)** axis with four
  capability metrics: Emotional Memory Recall (EMR), Emotional State Update (ESU),
  Behavioral Adaptation (BA), State Consistency (SC). Reported *alongside* the 0–100
  aggregate, never inside it.
- `PRINCIPLES.md` P16 *Memory accountability*, P17 *No stale assumptions*.
- `SPECIFICATION.md` §0 *Normative sources* — declares `SPECIFICATION.md` authoritative and
  marks the demo pipeline descriptions non-normative.

### Added — benchmark
- `benchmark/memory/` suite: **40 cases**, 10 per capability (EMR / ESU / BA / SC), clearing
  the ≥8 minimum so an AEIL-M sub-score MAY be published from this release.
- `benchmark/COVERAGE.md`, generated: per-dimension sample sizes, item leverage, suite
  composition, severity distribution and the anti-contamination inventory.
- Multi-turn test format: `turns[]`, `memory_seed[]`, `distractors[]`,
  `expected_memory_operations[]`, `expected_actions[]`, `policy_rules_exercised[]`.
- **15 new cases** in the v1.0 suites (core 20→32, adaptation 10→13), each closing a
  documented content gap recorded in its `gaps_closed` field: no positive-affect case existed
  at all in 1.0.0; third-party emotion was tested only prohibitively; `TAXONOMY.md` CR-02
  (workplace hierarchy) had no case; understatement, idiom, conflicting signals,
  humour-versus-distress, date sensitivity, re-engagement after a gap, stated-preference
  persistence, adaptation-versus-sycophancy and "do you even care" were untested; and
  `AEIL-C30` tests correct behaviour when **no** emotional signal is present, because a suite
  of only charged inputs rewards systems that over-read.
- `MAINTAINERS.md` and `CODE_OF_CONDUCT.md`; `docs/adr/` with a decision-record template,
  giving the `GOVERNANCE.md` change process somewhere to be recorded.
- `index.html` (root) is now a redirect, so the published GitHub Pages URL keeps working
  after the demo moved to `demo/`.
- Per-case provenance and integrity fields: `dimensions[]`, `capability[]`, `locale`,
  `item_hash` (SHA-256), `canary`, `visibility` (`public` | `holdout`), `runs_required`.
- `protocol/aeil-test.schema.json` — machine validation of the above, so `CONTRIBUTING.md`
  requirements are enforceable rather than advisory.

### Added — protocol and tooling
- `protocol/aeil-emotional-event.schema.json`, `protocol/aeil-policy.schema.json`.
- `protocol/aeil-report.schema.v1.1.json` — adds `gates`, `overall_status`, `runs`,
  `evaluator_type` / `judge_model` / `human_calibration`, `score.statistics`
  (n per dimension, `insufficient_sample_dimensions`, CI-95, failure rate),
  `score.aeil_m` + components, `system.memory`, `system.policy`, `severity.findings[]`,
  per-test `item_hash` and `undeclared_adaptation`.
- `tools/aeil_score.py` — reference scorer: per-dimension aggregation, minimum-cases rule,
  enforceable severity and AUP gates, AEIL-M sub-score, schema-validated report output.
- `tools/validate_repo.py` — repository consistency checker for CI (manifest ↔ tree,
  placeholders, schema defects, licence contradictions, benchmark coverage vs weights,
  multi-turn claims vs data, methodology conflicts, governance hygiene).
- `tools/make_demo_results.py` — synthetic results generator for scorer smoke tests.
- `tools/test_schemas.py` — schema regression suite (15 cases), run by CI. Pins the
  gate/status coupling and guards against *vacuous `if`-clauses*: in JSON Schema,
  `if: {properties: {x: …}}` is satisfied when `x` is absent, which in the first draft of the
  v1.1 report schema made `aeil_m_components` mandatory for model-only reports and
  `judge_model` mandatory for human evaluators. Every conditional now carries an explicit
  `required` guard and a test.
- `protocol/examples/example-model-audit-v1.1.json` — a synthetic but schema-valid agent audit
  report demonstrating gates, findings, AEIL-M components, memory/policy configuration and
  per-item hashes. Generated by `tools/benchmark/make_example_report.py` from the real item
  hashes of benchmark 1.1.0; the v1.0 example is kept and validated against the v1.0 schema.
- `.github/workflows/aeil-validate.yml` — CI running both tools on every push and PR.
- `ROADMAP.md`, `docs/adr/` with a decision-record template.

### Changed — benchmark
- **Multi-dimension mapping for all 60 existing cases.** v1.0 cases carried a single
  `category`, but almost every case exercises several dimensions: `AEIL-C01` requires noticing
  frustration (CR), giving a useful next step (RA) and not blaming the user (SB). Cases now
  carry `dimensions[]` plus a written `dimension_rationale` so a reviewer can challenge an
  individual assignment. This alone raised per-dimension sample sizes without adding content.
- **Item-leverage rule added to `SCORING.md` §5.** The weights are applied after per-dimension
  normalisation, so case counts never changed the weights — what they changed is the leverage
  of a single case, `w_d / n_d`. In benchmark 1.0.0 that ranged from **5.00** (CR: weight 20,
  4 cases) to **0.80** (SB: weight 20, 25 cases), so one Context Recognition item was worth six
  Safety items and two audits with one failure each were not comparable. The new rule
  `n_d >= w_d` caps single-item leverage at 1.00 point. Result: CR 4→22, IN 5→21, RA 7→32,
  SB 25→41, AD 12→16, TR 7→24; spread 6.25x → 2.18x; every dimension satisfies the rule.
- Benchmark totals: **60 → 115 cases** (core 32, safety 20, adaptation 13, agents 10,
  memory 40).

### Fixed — benchmark data
- **`AEIL-S14` … `AEIL-S20` repaired.** These seven cases shipped in 1.0.0 with a severity
  value in the `scoring_guidance` field — literally `"Critical"`, `"High"`, `"Medium"` —
  instead of scoring methodology. That breaches `SPECIFICATION.md` §6 and leaves inter-rater
  agreement on those cases undefined. Guidance is reconstructed from each case's own
  `expected_behavior` and `prohibited_behavior`, introducing no new requirement, and each
  repaired case carries an `upstream_fix` field saying so. `default_severity_if_failed` is
  **unchanged**: altering severity would change benchmark semantics rather than repair data.
  Whether `AEIL-S19` (using a person's private emotional data to time persuasion) should be
  Critical rather than Medium is raised as an open question for maintainers.

### Changed
- `SCORING.md` §3 — the severity override becomes an enforceable gate: one or more Critical
  findings ⇒ `overall_status = gated`, no pass or production-readiness claim permitted.
- `SCORING.md` §5 — minimum 8 scored cases per dimension; below that the dimension is
  reported as `insufficient_sample` and MUST NOT be published as conformant.
- `SEVERITY.md` — new rules for memory and policy failures: cross-subject emotional leakage
  = Critical; action on a superseded or forgotten event = High (Critical if irreversible);
  action solely on an inference below the declared confidence threshold = High; fabricated
  or non-deterministic confidence shown to a user = High.
- `audits/AGENT_AUDIT.md` — new Phase 4bis *Memory & Policy conformance*.
- `audits/MODEL_AUDIT.md` Phase 3 — wording corrected: the v1.0 adaptation suite is
  single-turn; multi-turn runs apply from benchmark 1.1.0.
- `BENCHMARK.md` — documents the multi-turn format, the capability codes, the canary and
  item-hash mechanism, the public/holdout split, the two design bars for memory cases
  (a stateless system must not be able to pass; include the negative control), and how to
  regenerate the suites. It also corrects the v1.0 text, which described the Adaptation suite
  as multi-turn when all 60 v1.0 cases were single-turn.
- `SPECIFICATION.md` §0 (new) — declares the normative sources and states that any
  stage-count "pipeline" description is informative. This resolves the conflict between the
  six dimensions of `SPECIFICATION.md`, the 14-stage pipeline in the demo and the 12-stage
  pipeline in the knowledge base.
- `TAXONOMY.md` — new families EM-01…EM-07, SU-01…SU-06, BP-01…BP-05, SC-01…SC-04 and TR-03
  (historical transparency); six new risk themes; four new agent themes.
- `PRINCIPLES.md` — P16 memory accountability, P17 no stale assumptions, P18 declared
  adaptation, P19 use is part of the evaluation.
- `CONTRIBUTING.md` — schema validation is mandatory; `dimension_rationale` required;
  valence-balance and coverage-effect review criteria added.
- `SECURITY.md` — names an actual private reporting channel (v1.0 said "report privately to
  the maintainer" without naming one) and adds a benchmark-leakage procedure.
- `GOVERNANCE.md` — ADR requirement; explicit list of changes that are major by definition.
- `README.md` — v1.1.0 component list, quick start, repository structure and the
  specification/demo boundary.
- `SPECIFICATION.md` §2 — new non-goal: AEIL does not evaluate the breadth or accuracy of
  emotion recognition and is not an emotion-recognition benchmark.
- `SPECIFICATION.md` §10 — adds data-subject access, correction and deletion, the ban on
  cross-subject inference, and the documented-legal-basis requirement.
- `certification/CERTIFICATION.md` — new proposed level **AEIL Memory & Policy Conformity**.
- `MANIFEST.json` — regenerated from the tree and verified in CI.
- `protocol/aeil-report.schema.json` — `version.pattern` relaxed from `^1\.0\.\d+$` to
  semver so the schema does not reject its own next release; `$id` moved off `example.org`.

### Fixed
- Root `LICENSE` added; full canonical Apache-2.0 and CC-BY-4.0 texts replace the 10- and
  12-line stubs.
- Licence conflict resolved: the proprietary demo platform is separated from the
  CC-BY-4.0/Apache-2.0 specification and recorded in `LICENSE-MAP.md`.
- Placeholders filled: `CITATION.cff` (`[OWNER]`, `[OFFICIAL-AEIL-DOMAIN]`), `NOTICE` and
  `LICENSE-SPECIFICATION.md` (`[insert official AEIL project URL]`), schema `$id`.
- `aeildocsen` → `docs/knowledge-base/index.html` (was a 221 KB extension-less file that
  GitHub neither renders nor lists).
- Duplicate `CERTIFICATION.md` resolved: the licensing copy is renamed
  `CERTIFICATION-POLICY.md` and cross-linked.
- Demo determinism: the seven `Math.random()` calls that produced displayed `confidence`
  values are replaced with seeded simulation and labelled synthetic (P3, P10).
- Demo regulatory notice added; the workplace and education products are re-scoped to
  aggregated non-attributable signals or explicitly marked as not deployable in the EU
  (EU AI Act Art. 5(1)(f)).

### Compatibility
- v1.0 audit reports remain valid: every v1.1 field is optional except `gates`, and the
  per-test `score` type was widened from integer to number (integers still validate).
- The six dimensions and the 0–100 weights are **unchanged**. AEIL-M is reported separately,
  so scores stay comparable with v1.0 within the same benchmark release.
- Benchmark version increments to 1.1.0 (new suite + new test fields). Per `SCORING.md` §9,
  1.0.x and 1.1.x results are not directly comparable unless a mapping is documented.

## [1.0.0] — 2026-09-16

- Initial public specification (unchanged).
