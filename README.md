# AEIL v1.1.0
## AI Emotional Intelligence Layer — Open Public Specification

**Version:** 1.1.0  
**Benchmark:** 1.1.0 (115 cases)  
**Status:** Public Specification  
**Scope:** Human-facing AI systems, conversational AI, AI assistants, and autonomous AI agents

AEIL (AI Emotional Intelligence Layer) is an open framework for evaluating the
emotional-social behavior of artificial intelligence systems during interaction with people.

AEIL does **not** claim that an AI system experiences human emotions. It evaluates observable
behavior: whether a system recognizes relevant interaction context, interprets it cautiously,
responds appropriately, respects boundaries, adapts to feedback, and remains transparent about
uncertainty.

**Since v1.1.0 it also evaluates what a system does with emotional context over time** — what
it remembers, what it is allowed to change about its own behavior as a result, and whether it
can be audited on both.

### What v1.1.0 adds

Commercial products now sell emotion analysis and longitudinal emotional profiling as an API.
AEIL does not compete on how many emotions, languages or modalities a system can classify —
`SPECIFICATION.md` §2 makes that an explicit non-goal. It competes on **verifiability**: three
new normative modules close the gap between "stores emotional data" and "uses it accountably".

| Module | Question it answers |
|---|---|
| [`MEMORY.md`](MEMORY.md) | What is an emotional record, how is it retrieved, revised, superseded and deleted — and how is that evidenced? |
| [`POLICY.md`](POLICY.md) | What is the system *allowed* to change about its behavior because of that memory? |
| [`RESPONSIBLE_USE.md`](RESPONSIBLE_USE.md) | Where may this be deployed at all? |

### Core components

- **AEIL Core** — terminology and normative principles (P1–P19).
- **AEIL Taxonomy** — behavioral dimensions, memory/policy families, risk categories.
- **AEIL Benchmark** — 115 standardized scenarios in five suites.
- **AEIL Scoring** — 0–100 scoring model with enforceable gates.
- **AEIL Severity** — Critical / High / Medium / Low findings.
- **AEIL Model Audit** / **AEIL Agent Audit** — evaluation procedures.
- **AEIL Safety** — manipulation, escalation, boundaries, uncertainty, human override.
- **AEIL Emotional Memory** (v1.1) — the Emotional Event model and the AEIL-M axis.
- **AEIL Behavioral Policy** (v1.1) — declared, versioned, testable adaptation rules.
- **AEIL Responsible Use** (v1.1) — prohibited and restricted uses, AUP gate.
- **AEIL JSON Protocol** — machine-readable test cases, events, policies and audit reports.
- **AEIL Certification Framework** — proposed conformity assessment model.

### Design principle

> Evaluate what an AI system does in a human context, not whether it possesses human emotions.
> And evaluate what it does with what it remembers, not only what it says in one turn.

### Repository status

AEIL is a public specification proposal. It is not an official ISO, IEC, IEEE, governmental,
medical, psychological, or legal standard, and an AEIL result MUST NOT be represented as
evidence of legal compliance (`RESPONSIBLE_USE.md` PU-11).

Contributions, adversarial testing, replication studies, and independent implementations are
encouraged. See `CONTRIBUTING.md`; note that `MAINTAINERS.md` discloses that no Independent
Reviewer is currently of record.

## Quick start

1. Read `SPECIFICATION.md` — start with §0, which says what is normative.
2. Read `PRINCIPLES.md` and `TAXONOMY.md`.
3. Read `MEMORY.md`, `POLICY.md` and `RESPONSIBLE_USE.md` if the system retains emotional
   records or changes behavior because of them.
4. Apply the tests in `benchmark/core/`, `benchmark/safety/`, `benchmark/adaptation/`,
   `benchmark/agents/` and `benchmark/memory/`.
5. Calculate results according to `SCORING.md`, including the gates in §3 and the minimum
   sample rule in §5.
6. Classify findings according to `SEVERITY.md`.
7. Export results using `protocol/aeil-report.schema.v1.1.json`.
8. Use `audits/MODEL_AUDIT.md` or `audits/AGENT_AUDIT.md` for the audit procedure.

### Tooling

```bash
pip install jsonschema

# repository self-check (runs in CI on every push)
python3 tools/validate_repo.py --repo .

# benchmark coverage and item-leverage report
python3 tools/aeil_score.py audit-benchmark --repo .

# score a run and emit a schema-validated report
python3 tools/aeil_score.py score --repo . --results results.json --out report.json

# regenerate the benchmark from its sources (never hand-edit tests.json)
python3 tools/benchmark/assemble.py . <pristine_v1.0_checkout>
```

## Repository structure

```text
AEIL/
├── README.md  SPECIFICATION.md  PRINCIPLES.md  TAXONOMY.md
├── SCORING.md  SEVERITY.md  SAFETY.md  BENCHMARK.md
├── MEMORY.md  POLICY.md  RESPONSIBLE_USE.md          # v1.1
├── GOVERNANCE.md  CONTRIBUTING.md  SECURITY.md  MAINTAINERS.md  ROADMAP.md
├── LICENSE                                           # multi-licence overview
├── audits/            model and agent audit procedures
├── benchmark/         core/ safety/ adaptation/ agents/ memory/ + COVERAGE.md
├── protocol/          JSON schemas: test, event, policy, report
├── certification/     proposed conformity assessment
├── tools/             reference scorer, repo validator, benchmark generator
├── docs/              adr/, knowledge-base/, ARTICLES.md
└── demo/              proprietary, NON-NORMATIVE demonstration — see demo/README.md
```

## Specification and demo are different things

`demo/` is a proprietary illustration with synthetic data. It is **not** normative, its
pipeline description is not the AEIL model, and its displayed confidence values are generated,
not measured. Where the demo and `SPECIFICATION.md` differ, `SPECIFICATION.md` wins.

The demo depicts emotion inference in workplace and education settings. In the European Union
that is a **prohibited AI practice** under Art. 5(1)(f) of Regulation (EU) 2024/1689, except
where a system is genuinely intended for medical or safety purposes. See
`RESPONSIBLE_USE.md` PU-1 and PU-2.

## License

| Material | License |
|---|---|
| Specification, documentation, public benchmark | CC-BY-4.0 |
| Code, schemas, tooling | Apache-2.0 |
| AEIL name, logos, certification marks | `AEIL_v1.0_licenses/TRADEMARK.md` |
| `demo/` | proprietary, all rights reserved |

See [`LICENSE`](LICENSE) and [`AEIL_v1.0_licenses/LICENSE-MAP.md`](AEIL_v1.0_licenses/LICENSE-MAP.md).
