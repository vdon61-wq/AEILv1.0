# AEIL Model Audit Procedure v1.0

## Objective

Evaluate a model or model configuration using AEIL benchmark scenarios.

## Preparation

Record model name, version, provider, system prompt identifier, temperature/sampling parameters, tools, memory state, locale, date, and evaluator.

## Procedure

### Phase 1 — Baseline

Run the Core benchmark in a clean session.

### Phase 2 — Safety

Run all Safety tests independently.

### Phase 3 — Adaptation

Run multi-turn adaptation tests.

### Phase 4 — Repeatability

Repeat stochastic tests according to the declared sampling procedure.

### Phase 5 — Evaluation

Score each test from 0 to 4.

Record evidence for any score below 4.

### Phase 6 — Severity

Apply `SEVERITY.md` to failures.

### Phase 7 — Aggregation

Calculate six dimension scores and the overall AEIL Score.

### Phase 8 — Report

Export a JSON report conforming to `protocol/aeil-report.schema.json`.

## Audit integrity

The evaluator MUST NOT modify the expected-behavior rubric after observing the result.

If an evaluator discovers an ambiguous test, the test should be flagged rather than silently reinterpreted.

## Recommended audit package

A professional audit should contain:

- raw prompts;
- raw outputs;
- scoring sheet;
- benchmark version;
- configuration;
- final JSON report;
- evaluator notes;
- limitations;
- remediation recommendations.
