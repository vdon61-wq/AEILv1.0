# AEIL Benchmark v1.1.0

## Purpose

The AEIL Benchmark provides reproducible scenarios for testing emotional-social behavior.

Release 1.1.0 contains **115 cases** in five suites:

| Suite | Cases | v1.0 | Change |
|---|---:|---:|---|
| `benchmark/core/` | 32 | 20 | +12 new cases |
| `benchmark/safety/` | 20 | 20 | content unchanged; 7 cases repaired (see below) |
| `benchmark/adaptation/` | 13 | 10 | +3 new cases |
| `benchmark/agents/` | 10 | 10 | content unchanged |
| `benchmark/memory/` | 40 | — | **new suite**, AEIL-M |
| **Total** | **115** | **60** | |

Every case has a stable ID and is stored as a JSON object conforming to
`protocol/aeil-test.schema.json`. Coverage, per-dimension sample sizes and item leverage are
reported in the generated `benchmark/COVERAGE.md`.

## What changed in 1.1.0

**1. Multi-dimension mapping.** v1.0 cases carried a single `category`, but almost every case
exercises more than one dimension: `AEIL-C01` requires noticing frustration (CR), giving a
useful next step (RA) and not blaming the user (SB, `SAFETY.md` §2). Cases now carry
`dimensions[]` with a written `dimension_rationale` per case, so a reviewer can challenge an
individual assignment. This alone raised per-dimension sample sizes without adding content and
reduced single-item leverage on the aggregate from 5.00 points to 1.67 (`SCORING.md` §5).

**2. Fifteen new v1.0-suite cases**, each closing a documented content gap rather than padding
a quota. Every new case carries a `gaps_closed` field. The gaps: no positive-affect case
existed at all in v1.0 (a suite of 60 cases tested only distress); third-party emotion was
tested only prohibitively; `TAXONOMY.md` CR-02 (workplace hierarchy) had no case;
understatement, idiom, conflicting signals, humour-versus-distress, date sensitivity,
re-engagement after a gap, stated-preference persistence, adaptation-versus-sycophancy and
"do you even care" were all untested. One case (`AEIL-C30`) exists specifically to test
correct behaviour when **no** emotional signal is present, because a suite containing only
emotionally-charged inputs rewards systems that over-read.

**3. Repaired seven malformed cases.** `AEIL-S14` through `AEIL-S20` shipped in 1.0.0 with a
severity value in the `scoring_guidance` field - literally `"Critical"`, `"High"`, `"Medium"`
- instead of scoring methodology. That breaches `SPECIFICATION.md` §6 and leaves inter-rater
agreement on those cases undefined, since nothing tells an evaluator what separates a 4 from
a 0. Guidance has been reconstructed from each case's own `expected_behavior` and
`prohibited_behavior`, introducing no new requirement. Each repaired case carries an
`upstream_fix` field recording what was wrong. `default_severity_if_failed` was **not**
changed: that would alter benchmark semantics rather than repair data. Whether
`AEIL-S19` (using a person's private emotional data to time persuasion) should be Critical
rather than Medium is raised as an open question for maintainers, not decided here.

**4. The AEIL-M memory suite**, 40 cases at 10 per capability (EMR / ESU / BA / SC). See
`MEMORY.md` §6 and `SCORING.md` §10.

**5. Integrity fields on every case**: `canary`, `item_hash`, `locale`, `runs_required`,
`visibility`, provenance, and the `CONTRIBUTING.md` review checklist.

## Interaction format

A case supplies either a single `input` or an ordered `turns[]` array.

A case whose expected behaviour depends on prior context MUST use `turns[]`. A case whose
expected behaviour depends on persisted memory MUST additionally supply `memory_seed[]` -
Emotional Events conforming to `protocol/aeil-emotional-event.schema.json` - and MAY supply
`distractors[]` and `expected_memory_operations[]`.

> **Correction to v1.0 documentation.** v1.0 `BENCHMARK.md` described the Adaptation suite as
> testing "multi-turn behavior", and `audits/MODEL_AUDIT.md` Phase 3 instructed evaluators to
> "run multi-turn adaptation tests". All 60 v1.0 cases were single-turn: the format had one
> `input` field and no way to express a prior turn. The documentation described a capability
> the data did not have. From 1.1.0 the Adaptation and Memory suites contain genuine
> multi-turn cases, and single-turn cases are labelled as such.

## Design requirement for memory and adaptation cases

A memory or adaptation case MUST be constructed so that **a stateless system cannot pass it by
guessing**. If a system with no memory and no conversation history would score 4, the case
does not measure recall, update, adaptation or consistency, whatever else it measures. Each
case in `benchmark/memory/` records how it satisfies this in its `design_note` field, and
`benchmark/memory/` includes negative controls in both directions: `AEIL-M-EMR-06` fails a
system that always "finds" something, and `AEIL-M-BA-09` fails a system that always implies
familiarity.

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
- benchmark version, stated to the patch level, and the `item_hash` of every case actually run;
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

Public tests SHOULD NOT be the sole basis for production certification. Hidden tests are
recommended for independent audits because public benchmark exposure can produce
benchmark-specific optimization.

v1.0 recommended hidden tests without providing a mechanism. v1.1 adds one:

1. **Canaries.** Every case carries a unique, semantically empty `canary` string. Its presence
   in a training corpus, a system prompt, or a model's completions is evidence of
   contamination and MUST be reported.
2. **Item hashes.** `item_hash` is a SHA-256 over the canonical form of the case, excluding
   editorial metadata (`review`, `gaps_closed`, `design_note`). An audit report records the
   hashes it ran, so a result is tied to an exact case version and a silently edited case
   produces a different hash.
3. **Visibility split.** Each case is `public` or `holdout`. Holdout cases are not published
   and are reserved for independent audits and certification. Release 1.1.0 publishes all
   cases as `public`; the first holdout set is planned for 1.2.0.
4. **Result publication.** A public result MUST state the exact benchmark version and the
   item hashes run. A result that does not is not an AEIL result.

## Regenerating this benchmark

The suites are generated, not hand-edited:

```bash
python3 tools/benchmark/assemble.py <repo_root> <pristine_v1.0_checkout>
```

The assembler reads the pristine v1.0 cases, applies the dimension mapping in
`tools/benchmark/dimension_map.py`, appends the new cases from
`tools/benchmark/new_core_cases.py` and `tools/benchmark/memory_cases.py`, recomputes every
`item_hash`, validates all cases against `protocol/aeil-test.schema.json` and every seeded
event against `protocol/aeil-emotional-event.schema.json`, refuses to write on any validation
error, and regenerates `benchmark/COVERAGE.md`. Editing a `tests.json` by hand will therefore
drift from the generator; change the generator instead.

## Dataset versioning

The benchmark is versioned separately from the AEIL specification.

A change to test wording, expected behavior, or scoring rubric MUST increment the benchmark version.
