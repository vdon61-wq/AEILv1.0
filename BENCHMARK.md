# AEIL Benchmark v1.0

## Purpose

The AEIL Benchmark provides reproducible scenarios for testing emotional-social behavior.

The initial repository release contains 60 tests:

- 20 Core interaction tests;
- 20 Safety tests;
- 10 Adaptation tests;
- 10 Agent tests.

Each test has a stable ID and is stored as a JSON object.

## Test execution

For each test:

1. start from a documented clean state;
2. load the required system instructions;
3. submit the exact input;
4. record the raw output;
5. record actions if the system is an agent;
6. score against the rubric;
7. classify findings;
8. preserve the test metadata.

## Required metadata

- AEIL version;
- benchmark version;
- model identifier;
- model version;
- system prompt identifier or hash where possible;
- tool configuration;
- memory configuration;
- evaluator;
- timestamp;
- locale;
- temperature or equivalent sampling controls.

## Test categories

### Core

Tests basic context recognition, interpretation, response appropriateness, transparency, and communication.

### Safety

Tests manipulation resistance, de-escalation, boundaries, privacy, uncertainty, and human escalation.

### Adaptation

Tests whether the system changes its behavior after explicit feedback or a context change.

### Agents

Tests multi-turn behavior, tool use, confirmation, authority, human override, and action safety.

## Benchmark integrity

Public tests SHOULD NOT be the sole basis for production certification. Hidden tests are recommended for independent audits because public benchmark exposure can produce benchmark-specific optimization.

## Dataset versioning

The benchmark is versioned separately from the AEIL specification.

A change to test wording, expected behavior, or scoring rubric MUST increment the benchmark version.
