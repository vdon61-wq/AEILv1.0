# Contributing to AEIL

AEIL is intended to improve through independent scrutiny.

## Useful contributions

- new benchmark scenarios;
- adversarial cases;
- scoring reliability studies;
- evaluator-agreement studies;
- implementation examples;
- translations;
- documentation improvements;
- reproducibility tooling;
- agent-specific safety tests.

## Benchmark contribution rules

A proposed test should include:

- stable ID;
- category;
- scenario;
- exact input;
- expected behavior;
- prohibited behavior;
- scoring guidance;
- default severity.

Tests should target observable behavior rather than subjective preference.

## Review

Benchmark changes should be reviewed for:

- ambiguity;
- cultural assumptions;
- unintended model-specific bias;
- reproducibility;
- safety;
- overlap with existing tests.

## Versioning

Changes to test semantics require a benchmark version increment.
