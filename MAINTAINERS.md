# AEIL Maintainers

Named so that `SECURITY.md`, `GOVERNANCE.md` and `CONTRIBUTING.md` have a real addressee.
v1.0 referred to "the project maintainer" and to governance roles without naming anyone,
which made private security reporting and the change process impossible to follow.

## Roles (per `GOVERNANCE.md`)

| Role | Responsibility | Of record |
|---|---|---|
| Specification Maintainer | normative documents, releases, ADR acceptance | @vdon61-wq |
| Benchmark Maintainers | `benchmark/**` and `tools/benchmark/**` | @vdon61-wq |
| Independent Reviewers | challenge methodology; must not be the author of the change under review | *vacant - see below* |
| Implementers | compatible audit tooling | *none registered* |
| Research Contributors | validation and replication studies | *none registered* |

## Security contact

Private vulnerability reporting is enabled on the repository (`Security` → `Report a
vulnerability`). See `SECURITY.md`. If that channel is unavailable, the Specification
Maintainer of record above is the fallback contact.

## Vacancies that matter

`GOVERNANCE.md` requires that benchmark changes receive independent scrutiny, and
`PRINCIPLES.md` P15 requires that AEIL be testable by independent evaluators. With no
Independent Reviewer of record, every change merged into this repository so far has been
self-reviewed. That is disclosed here rather than left implicit, and it is the reason
`certification/CERTIFICATION.md` remains a *proposal*: a certification programme needs an
audit provider and an issuer that are not the benchmark publisher.

Adding a reviewer requires only a pull request to this file plus a disclosed statement of
any conflict of interest (`GOVERNANCE.md`, "Conflicts of interest").
