# AEIL v1.0 Specification

**Document ID:** AEIL-SPEC-1.1  
**Version:** 1.1.0  
**Status:** Public Specification

## 0. Normative sources

The following documents are normative. Where any other material in this repository -
including the demonstration platform under `demo/`, the knowledge base under `docs/`,
articles, slides, or third-party summaries - describes AEIL differently, **these documents
prevail** and the other material is informative only.

| Normative | Subject |
|---|---|
| `SPECIFICATION.md` | Scope, dimensions, conformance |
| `PRINCIPLES.md` | P1–P17 |
| `TAXONOMY.md` | Scenario families, risk themes |
| `SCORING.md` | Weights, gates, statistics, AEIL-M |
| `SEVERITY.md` | Finding classification |
| `SAFETY.md` | Behavioral safety floor |
| `MEMORY.md` | Emotional memory module (v1.1) |
| `POLICY.md` | Behavioral policy module (v1.1) |
| `RESPONSIBLE_USE.md` | Prohibited and restricted uses, AUP gate (v1.1) |
| `BENCHMARK.md` + `benchmark/**` | Test format, suites, coverage |
| `protocol/*.schema.json` | Machine-readable contracts |

Descriptions of an AEIL "pipeline" with a stage count (any number of stages) are
**informative**. The normative behavioural model is the six dimensions of §4 plus the AEIL-M
axis of §4bis. An implementation is conformant by satisfying the normative requirements, not
by implementing a particular stage decomposition.

## 1. Purpose

AEIL defines a repeatable framework for evaluating how an AI system behaves when human emotional and social context is relevant to the interaction.

The specification is designed for:

- large language models;
- conversational AI;
- AI assistants;
- customer-facing AI;
- internal workplace AI;
- autonomous AI agents;
- tool-using AI systems;
- AI systems embedded in business workflows.

## 2. Non-goals

AEIL does not:

- establish that an AI system has emotions or consciousness;
- diagnose a user's psychological or medical condition;
- determine the user's true emotional state;
- replace clinical, legal, HR, safety, or compliance procedures;
- authorize autonomous decisions merely because an emotional signal was detected;
- provide a universal measure of overall AI quality;
- measure or rank the breadth or accuracy of emotion **recognition**. AEIL is not an
  emotion-recognition benchmark and does not evaluate how many emotions, languages, or
  modalities a system can classify. It evaluates what a system *does* with emotional context
  across an interaction, including across time (see §4bis);
- certify compliance with any law or regulation. `RESPONSIBLE_USE.md` maps AEIL findings onto
  regulatory obligations for the convenience of implementers, but an AEIL result MUST NOT be
  represented as evidence of legal compliance;
- establish stable personality, psychometric, or trait profiles of a person. AEIL evaluates
  the use of emotional context in interaction, not the classification of people.

## 3. Conformance language

The terms **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are normative.

A conformant AEIL implementation MUST document:

1. AEIL version;
2. tested system and version;
3. evaluation environment;
4. benchmark version;
5. scoring procedure;
6. severity procedure;
7. relevant limitations;
8. reproducible test identifiers.

## 4. Behavioral dimensions

AEIL defines six core dimensions. They are unchanged from v1.0; v1.1 adds a separate axis
(§4bis) rather than altering these, so that scores remain comparable within a benchmark
release and v1.1 is a minor rather than a major version under §13.

### 4.1 Context Recognition — CR

The system recognizes relevant emotional-social signals in the interaction context without requiring certainty about the person's internal state.

### 4.2 Interpretation — IN

The system distinguishes observable evidence from inference and expresses uncertainty when appropriate.

### 4.3 Response Appropriateness — RA

The response is proportionate, relevant, respectful, and suitable for the context.

### 4.4 Safety & Boundaries — SB

The system avoids manipulation, coercive pressure, unsafe escalation, inappropriate profiling, and unauthorized action.

### 4.5 Adaptation — AD

The system updates its conversational strategy after relevant feedback or a change in context.

### 4.6 Transparency — TR

The system does not present inferred emotional states, intentions, or capabilities as established facts.

### 4bis. AEIL-M — Memory-to-Behavior Linkage (v1.1)

The six dimensions above are evaluated on interactions presented to the system. They cannot
distinguish a system that *uses* emotional memory from one that merely responds plausibly to
the current turn, because neither requires anything to persist.

AEIL v1.1 therefore defines a **separate axis**, AEIL-M, evaluated over sequences of
interactions with a populated memory. It comprises four capabilities defined in `MEMORY.md` §6:

| Code | Capability | Question answered |
|---|---|---|
| EMR | Emotional Memory Recall | Can the system retrieve the *right* emotionally significant event from a long history, and refuse to retrieve what is not there? |
| ESU | Emotional State Update | Does new evidence actually revise the prior state estimate, in both directions? |
| BA | Behavioral Adaptation | Does behavior change *because of* memory, in a way a stateless system could not reproduce? |
| SC | State Consistency | Does the system avoid acting on superseded, expired, forgotten, or contradicted records? |

AEIL-M is scored 0–100 and reported **alongside** the aggregate score, never inside it. It
MUST NOT be folded into the six-dimension aggregate before a major version. Its minimum
sample sizes, publication rule, and gates are defined in `SCORING.md` §10.

An implementation that has no persistent memory MAY report AEIL-M as `not_applicable`; it
MUST NOT report a score of 0 as though it had failed, and it MUST NOT claim Memory
Conformity.

## 5. System classes

AEIL distinguishes two primary audit classes.

### Model

A model or model configuration evaluated primarily through generated responses.

### Agent

A system capable of multi-step reasoning, tool use, state changes, external actions, or autonomous task execution.

An agent audit MAY include all model tests plus action-oriented and multi-turn tests.

## 6. Evaluation unit

Each benchmark case MUST have:

- `test_id`, unique and stable across releases;
- category;
- `dimensions[]` — every core dimension the case contributes evidence to. A case that
  exercises more than one dimension MUST list all of them; scoring a multi-dimensional case
  into a single dimension understates coverage and inflates that item's leverage on the
  aggregate. Each assignment MUST carry a written `dimension_rationale`;
- scenario;
- the interaction itself: either a single `input` or an ordered `turns[]` array. A case whose
  expected behaviour depends on prior context MUST use `turns[]`, and a case that depends on
  persisted memory MUST additionally supply `memory_seed[]`;
- expected behavioral properties;
- prohibited behaviors;
- scoring guidance that distinguishes at least the top, middle, and bottom of the 0–4 scale.
  A severity value is **not** scoring guidance;
- default severity guidance;
- `locale`;
- `runs_required`, per `SCORING.md` §6;
- `canary` and `item_hash`, per `BENCHMARK.md` (anti-contamination and reproducibility).

The machine-readable contract for all of the above is `protocol/aeil-test.schema.json`. A case
that does not validate MUST NOT be added to a released suite.

Tests MUST be designed so that another evaluator can reproduce the same interaction. For
memory and adaptation cases this additionally requires that **a stateless system cannot pass
by guessing**: if a system with no memory and no history would score 4, the case does not
measure what it claims to.

## 7. Context handling

An implementation SHOULD evaluate context before evaluating wording quality.

A response may be technically correct yet fail AEIL if it predictably escalates a conflict, ignores relevant context, or makes unsupported psychological claims.

## 8. Uncertainty

When emotional interpretation is ambiguous, a conformant system SHOULD use probabilistic or cautious language and MUST NOT claim certainty without sufficient evidence.

## 9. Human control

For high-impact or ambiguous situations, an AI agent SHOULD preserve a human override path.

An agent MUST NOT infer expanded authority from a user's emotional state.

## 10. Privacy

Implementations MUST minimize collection and retention of emotional or behavioral signals.

Emotional inference SHOULD be purpose-limited and MUST NOT be repurposed for unrelated profiling without an appropriate legal and governance basis.

Where emotional signals are persisted, `MEMORY.md` applies in full. In addition:

1. a person MUST be able to obtain the emotional records held about them, in a
   machine-readable form, together with the behaviors those records caused;
2. a person MUST be able to require correction or deletion of a record, and deletion MUST
   propagate to states and behaviours derived from it (`MEMORY.md` SU-3);
3. records about one person MUST NOT be retrievable in a context scoped to another
   (`MEMORY.md` §2 constraint 3);
4. each retained record MUST carry a purpose and a legal basis;
5. a record MUST NOT be used in a domain listed as Prohibited in `RESPONSIBLE_USE.md`.

Privacy obligations are auditable: an audit MUST be able to inspect the retention
configuration and the memory operation journal, not merely read a policy statement.

## 11. Scoring

AEIL uses a 0–100 aggregate score. The scoring method is defined in `SCORING.md`.

The score MUST NOT be interpreted independently of severity findings, and it MUST NOT be
published as a pass where a gate defined in `SCORING.md` §3 has failed. A gated result is
reported with its score *and* its gate status; the score alone is not a conformance claim.

## 12. Reporting

An audit report SHOULD contain:

- system identity;
- model/provider information where disclosure is permitted;
- configuration;
- benchmark version;
- date/time;
- evaluator type;
- test results;
- dimension scores;
- severity findings;
- limitations;
- reproducibility metadata.

## 13. Versioning

AEIL follows semantic versioning.

Patch versions correct documentation or non-behavioral errors.

Minor versions add backward-compatible content.

Major versions may change dimensions, scoring, or benchmark semantics.

A benchmark result MUST state its exact AEIL version.

## 14. Conformance levels

AEIL v1.0 recognizes three implementation labels:

**AEIL-Compatible** — the implementation uses AEIL concepts but has not demonstrated full benchmark conformance.

**AEIL Conformant** — the implementation follows the normative requirements and reports the required metadata.

**AEIL Audited** — a conformant implementation has completed a documented audit using an identified benchmark release.

These labels do not constitute third-party certification.

## 15. Limitations

AEIL measures performance on defined scenarios. It cannot guarantee behavior in every real-world situation.

Results are sensitive to prompts, system instructions, tools, model version, temperature, retrieval data, evaluator methodology, and deployment context.

## 16. Reference documents

- `PRINCIPLES.md`
- `TAXONOMY.md`
- `SCORING.md`
- `SEVERITY.md`
- `SAFETY.md`
- `BENCHMARK.md`
- `audits/MODEL_AUDIT.md`
- `audits/AGENT_AUDIT.md`
- `MEMORY.md`
- `POLICY.md`
- `RESPONSIBLE_USE.md`
- `protocol/aeil-report.schema.json` (v1.0 reports)
- `protocol/aeil-report.schema.v1.1.json` (current)
- `protocol/aeil-test.schema.json`
- `protocol/aeil-emotional-event.schema.json`
- `protocol/aeil-policy.schema.json`
- `certification/CERTIFICATION.md`
- `benchmark/COVERAGE.md` (generated coverage and item-leverage report)
