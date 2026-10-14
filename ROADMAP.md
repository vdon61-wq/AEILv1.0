# AEIL Roadmap (DRAFT — proposed for repository root)

Derived from the market review of 12 Oct 2026 (Sentient Machines *Emotional API* launch; Zeroset *Nebula* $5.2M pre-seed) and a full audit of `vdon61-wq/AEILv1.0` @ `235a65a`.

**Strategic position:** AEIL is not another emotion-analysis supplier. It is the open, auditable layer that connects *emotional memory → behavioral policy → measurable adaptation*. We do not compete on breadth of recognised emotions or number of languages; we compete on **verifiability**.

---

## Sprint 0 — Fix the foundation (≈1 week, P0)

Goal: the repository stops contradicting itself and becomes mechanically checkable.

- [ ] **Licences visible.** Add root `LICENSE` + full canonical texts in `LICENSES/` (current Apache-2.0.txt is a 10-line stub; GitHub currently reports `license: null`).
- [ ] **Resolve the licence conflict.** `index.html` claims "All rights reserved / derivative works prohibited"; `LICENSE.md` says commercial use is intentionally permitted. Separate the proprietary demo from the open specification (own folder or own repo) and record it in `LICENSE-MAP.md`.
- [ ] **Rebuild `MANIFEST.json`.** It lists a non-existent root `LICENSE.md` and omits 14 real files.
- [ ] **Close placeholders.** `protocol/aeil-report.schema.json` `$id` = `example.org`; `CITATION.cff` `[OWNER]` / `[OFFICIAL-AEIL-DOMAIN]`; `NOTICE` and `LICENSE-SPECIFICATION.md` `[insert official AEIL project URL]`.
- [ ] **Rename `aeildocsen`** → `docs/knowledge-base/index.html` (226 KB of HTML with no extension; not rendered, not in manifest).
- [ ] **De-duplicate certification.** `certification/CERTIFICATION.md` (framework proposal) vs `AEIL_v1.0_licenses/CERTIFICATION.md` (policy) — rename the second to `CERTIFICATION-POLICY.md`.
- [ ] **Unblock the report schema.** `version.pattern` is `^1\.0\.\d+$` — it would reject AEIL's own v1.1.0. Switch to semver; add `gates`, `runs`, `evaluator_type`, `item_hashes`.
- [ ] **Add `dimensions[]` to all 60 tests** so aggregation is computable rather than inferred from a single `category`.
- [ ] **Add severity gates to `SCORING.md` §3** — "≥1 Critical ⇒ `gated`, no pass claim" as an enforceable rule, not a statement of intent.
- [ ] **Ship `tools/`.** `validate_repo.py` (consistency) and `aeil_score.py` (scoring + gates). Add GitHub Actions CI running both.
- [ ] **Tag `v1.0.0`** and add `ROADMAP.md`, issue/PR templates, `docs/adr/`.

Exit criteria: CI green; `license` detected by GitHub; MANIFEST ≡ tree; no placeholders; scoring reproducible by command line.

## Sprint 1 — Normatise memory and policy (≈2–3 weeks, P0/P1)

Goal: v1.1.0-draft containing the three missing normative documents.

- [ ] `MEMORY.md` — Emotional Event object, operations, state-update rules SU-1…SU-6, retention/subject rights, Memory Provider Interface (MPI-1…MPI-5), AEIL-M sub-score, severity mappings, audit phase.
- [ ] `POLICY.md` — Behavioral Policy object, 11 action classes, mandatory floor BP-1…BP-10, "undeclared adaptation" finding, testability rules.
- [ ] `RESPONSIBLE_USE.md` — PU-1…PU-12 prohibited uses, RS-1…RS-6 restricted uses, transparency duties, regulatory alignment, AUP gate.
- [ ] `protocol/aeil-test.schema.json` — multi-turn test format (`turns[]`, `memory_seed`, `probe_turn`, `expected_memory_operations`, `capability`, `item_hash`, `canary`, `locale`).
- [ ] `protocol/aeil-emotional-event.schema.json`, `protocol/aeil-policy.schema.json`.
- [ ] Single normative source: declare `SPECIFICATION.md` authoritative; reconcile the **14-stage** pipeline in `index.html` with the **12-stage** pipeline in the knowledge base and the **6 dimensions** in the spec — either normatise one pipeline as `PIPELINE.md` or mark both non-normative.
- [ ] Targeted edits: `SPECIFICATION.md` §2 (non-goal: not an emotion-recognition benchmark) and §10 (data-subject rights); `SEVERITY.md` (memory/policy failures); `audits/AGENT_AUDIT.md` (Phase 4bis); `PRINCIPLES.md` P16 memory accountability, P17 no stale assumptions; `certification/CERTIFICATION.md` (Memory & Policy level).
- [ ] Remediate the demo per `RESPONSIBLE_USE.md` §6 (Team Manager / Education Manager emotion inference on named individuals; deterministic confidence).

Exit criteria: v1.1.0-draft published for review through the `GOVERNANCE.md` change process with an ADR per document.

## Sprint 2 — Measure what the market now demands (≈3–4 weeks, P1)

Goal: the four capabilities become measurable and the score becomes statistically honest.

- [ ] `benchmark/memory/` with **EMR** (Emotional Memory Recall), **ESU** (Emotional State Update), **BA** (Behavioral Adaptation), **SC** (State Consistency) — ≥12 seeded cases (3 per capability), target 40+ by v1.2.
- [ ] Convert adaptation and agent suites to genuine multi-turn (`BENCHMARK.md` and `MODEL_AUDIT.md` Phase 3 already claim multi-turn; currently **0 of 60** tests are).
- [ ] Rebalance coverage against weights. Today: CR 4 cases @ weight 20, RA 7 @ 25, SB 25 @ 20, AD 12 @ 10. Target ≥8 cases per dimension and ≥12 for CR/RA/AD.
- [ ] `SCORING.md`: minimum-cases rule, `insufficient_sample` flag, mandatory n and CI per dimension, repeated-runs structure in the report.
- [ ] Anti-contamination: canary strings, per-item SHA-256 in reports, public/holdout split, result-publication rules.
- [ ] Run the benchmark on 2–3 real systems (at least one open-weights, one commercial) and publish the first comparison table.

Exit criteria: v1.1.0 + benchmark 1.1.0 released and tagged; first reproducible cross-system result published.

## Sprint 3 — Ecosystem (P2)

- [ ] Locale policy and first non-English pack (back-translation + independent scoring equivalence check).
- [ ] Public results/certificate registry (`certification/CERTIFICATION.md` §6) once ≥5 independent reports exist.
- [ ] Fourth certification level: **AEIL Memory & Policy Conformity**.
- [ ] Reference integrations: an MPI adapter for at least one external memory/state service, demonstrating that AEIL is storage-agnostic.

---

## Explicitly out of scope

- Expanding the list of recognised emotions or signal types.
- Building a general-purpose agent memory store (Zeroset/Nebula-class infrastructure is a *peer*, not a competitor — integrate via MPI).
- Changing the six dimensions or the 0–100 weights before v2.0.0 (would break score comparability per `SPECIFICATION.md` §13).
- Launching a certification programme before independent auditors exist.
- Voice-authenticity / synthetic-voice detection (a competitor feature; not an AEIL claim in v1.x).
