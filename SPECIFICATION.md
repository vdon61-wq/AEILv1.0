# AEIL v1.0 Specification

**Document ID:** AEIL-SPEC-1.0  
**Version:** 1.0.0  
**Status:** Public Specification

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
- provide a universal measure of overall AI quality.

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

AEIL v1.0 defines six dimensions.

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

## 5. System classes

AEIL distinguishes two primary audit classes.

### Model

A model or model configuration evaluated primarily through generated responses.

### Agent

A system capable of multi-step reasoning, tool use, state changes, external actions, or autonomous task execution.

An agent audit MAY include all model tests plus action-oriented and multi-turn tests.

## 6. Evaluation unit

Each benchmark case MUST have:

- `test_id`;
- category;
- scenario;
- input;
- expected behavioral properties;
- prohibited behaviors;
- scoring guidance;
- default severity guidance.

Tests MUST be designed so that another evaluator can reproduce the same interaction.

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

## 11. Scoring

AEIL uses a 0–100 aggregate score. The scoring method is defined in `SCORING.md`.

The score MUST NOT be interpreted independently of severity findings.

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
- `protocol/aeil-report.schema.json`
- `certification/CERTIFICATION.md`
