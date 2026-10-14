# AEIL Governance Proposal

## Goal

Develop AEIL through transparent, documented review rather than unilateral changes.

## Proposed roles

**Specification Maintainer** — manages releases and normative documents.

**Benchmark Maintainers** — curate test suites.

**Independent Reviewers** — challenge methodology and identify weaknesses.

**Implementers** — build compatible audit tools.

**Research Contributors** — conduct validation studies.

## Change process

Material changes should include:

1. rationale;
2. proposed text or test;
3. compatibility impact;
4. evidence;
5. review period;
6. release note.

Each material change is recorded as an Architecture Decision Record in `docs/adr/`, using
`docs/adr/0000-template.md`. The ADR is where the six items above live, so that the reasoning
survives independently of the pull request that carried it. An accepted ADR is referenced from
`CHANGELOG.md`.

> v1.0 defined this process but provided no place to record it, so no change in the v1.0
> history has a documented rationale, compatibility assessment or review period. The ADR
> directory exists from v1.1.0.

Changes are classified by the rule already in `SPECIFICATION.md` §13: patch for documentation
and non-behavioral fixes, minor for backward-compatible additions, major for changes to
dimensions, scoring or benchmark semantics. A change that weakens any of BP-1…BP-10
(`POLICY.md` §4), removes a Prohibited use (`RESPONSIBLE_USE.md` §2.1), or alters a dimension
weight is **major** by definition and requires the full review period.

## Independence

Benchmark governance should avoid allowing a single vendor or model provider to define the result of its own evaluation without independent scrutiny.

## Conflicts of interest

Contributors should disclose material conflicts when proposing or reviewing benchmark changes.
