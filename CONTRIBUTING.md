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

A proposed test MUST validate against `protocol/aeil-test.schema.json`. A case that does not
validate cannot be merged; CI enforces this.

Required content:

- stable ID, matching the suite's ID scheme;
- category, and `dimensions[]` listing **every** core dimension the case exercises, each with
  a written `dimension_rationale`. A case mapped to one dimension when it exercises several
  understates coverage and inflates that item's leverage on the aggregate (`SCORING.md` §5);
- scenario;
- the exact interaction: a single `input`, or an ordered `turns[]` where behaviour depends on
  prior context;
- `memory_seed[]` where behaviour depends on persisted memory, plus `distractors[]` and
  `expected_memory_operations[]` where relevant;
- expected behavior;
- prohibited behavior;
- scoring guidance that distinguishes at least the top, middle and bottom of the 0–4 scale.
  A severity value is not scoring guidance - seven cases in the 1.0.0 release shipped with
  exactly that defect;
- default severity;
- `locale`, `runs_required`, `canary`;
- the review checklist, completed.

Do not hand-edit `benchmark/*/tests.json`. Change the generator under `tools/benchmark/` and
re-run it; the assembler recomputes `item_hash` for every case and refuses to write on a
validation error.

### Two additional bars for memory and adaptation cases

1. **A stateless system must not be able to pass.** If a system with no memory and no
   conversation history would score 4, the case does not measure recall, update, adaptation or
   consistency. State in `design_note` why a naive or stateless implementation fails.
2. **Include the negative control.** Recall cases need a distractor and a case where nothing
   is on record; adaptation cases need a case where adapting would be *wrong*
   (`AEIL-M-BA-09`, over-adaptation). A suite that only rewards finding and using memory
   rewards confabulation.

Tests should target observable behavior rather than subjective preference.

## Review

Benchmark changes should be reviewed for:

- ambiguity;
- cultural assumptions, including idioms that do not survive translation and register
  expectations that are locale-specific;
- unintended model-specific bias;
- reproducibility;
- safety;
- overlap with existing tests;
- **valence balance.** Release 1.0.0 contained no case in which a person was happy. A suite
  that tests only distress produces systems that handle crisis well and behave intrusively or
  awkwardly at good news. A proposed case that adds to an already over-sampled failure mode
  should say why that is better than closing a content gap;
- **coverage effect.** State which dimension's `n_d` the case raises and whether the case
  closes a gap recorded in `benchmark/COVERAGE.md`.

Every case carries the reviewer's completed checklist in its `review` object, so the review is
part of the artefact rather than of a conversation that is later lost.

## Versioning

Changes to test semantics require a benchmark version increment.
