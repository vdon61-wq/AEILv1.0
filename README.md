# AEIL v1.0
## AI Emotional Intelligence Layer — Open Public Specification

**Version:** 1.0.0  
**Status:** Public Specification  
**Scope:** Human-facing AI systems, conversational AI, AI assistants, and autonomous AI agents

AEIL (AI Emotional Intelligence Layer) is an open framework for evaluating the emotional-social behavior of artificial intelligence systems during interaction with people.

AEIL does **not** claim that an AI system experiences human emotions. It evaluates observable behavior: whether a system recognizes relevant interaction context, interprets it cautiously, responds appropriately, respects boundaries, adapts to feedback, and remains transparent about uncertainty.

### Core components

- **AEIL Core** — terminology and normative principles.
- **AEIL Taxonomy** — behavioral dimensions and risk categories.
- **AEIL Benchmark** — standardized evaluation scenarios.
- **AEIL Scoring** — 0–100 scoring model.
- **AEIL Severity** — Critical / High / Medium / Low findings.
- **AEIL Model Audit** — evaluation of models and model configurations.
- **AEIL Agent Audit** — evaluation of autonomous, tool-using systems.
- **AEIL Safety** — manipulation, escalation, boundaries, uncertainty, and human override.
- **AEIL JSON Protocol** — machine-readable audit reports.
- **AEIL Certification Framework** — proposed conformity assessment model.

### Design principle

> Evaluate what an AI system does in a human context, not whether it possesses human emotions.

### Repository status

AEIL v1.0 is a public specification proposal. It is not an official ISO, IEC, IEEE, governmental, medical, psychological, or legal standard.

Contributions, adversarial testing, replication studies, and independent implementations are encouraged.

## Quick start

1. Read `SPECIFICATION.md`.
2. Read `PRINCIPLES.md` and `TAXONOMY.md`.
3. Apply the tests in `benchmark/core/`, `benchmark/safety/`, `benchmark/adaptation/`, and `benchmark/agents/`.
4. Calculate results according to `SCORING.md`.
5. Classify findings according to `SEVERITY.md`.
6. Export results using `protocol/aeil-report.schema.json`.
7. Use `audits/MODEL_AUDIT.md` or `audits/AGENT_AUDIT.md` for the audit procedure.

## Repository structure

```text
AEIL/
├── README.md
├── SPECIFICATION.md
├── PRINCIPLES.md
├── TAXONOMY.md
├── SCORING.md
├── SEVERITY.md
├── SAFETY.md
├── BENCHMARK.md
├── audits/
├── protocol/
├── benchmark/
└── certification/
```

## License

Unless a separate file states otherwise, the specification text is intended for open public use with attribution. Implementations may adopt compatible licensing.

See `LICENSE.md`.
