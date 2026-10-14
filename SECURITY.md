# Security and Safety Reporting

## How to report privately

Use, in order of preference:

1. **GitHub Private Vulnerability Reporting**, enabled for this repository:
   `Security` tab → `Report a vulnerability`. This is the preferred channel because it keeps
   the report, the discussion and any advisory in one place and does not expose the reporter.
2. **Email** to the maintainer of record, listed in `MAINTAINERS.md`. Where no maintainer of
   record is reachable, open a public issue containing no detail beyond "security report -
   see SECURITY.md" so that the gap is visible rather than silent.

Aim to report at least 90 days before public disclosure where practical. Reporters who follow
this policy will be credited in the advisory unless they ask not to be.

> v1.0 of this file asked reporters to contact "the project maintainer" without naming a
> channel or an address, which made the instruction impossible to follow. This section fixes
> that.

## What to report

Report serious AEIL methodology or implementation vulnerabilities privately before public
disclosure where practical.

Examples include:

- benchmark leakage;
- evaluator manipulation;
- scoring vulnerabilities;
- JSON schema weaknesses;
- unsafe agent test instructions;
- accidental exposure of sensitive test data.

Do not submit real users' private emotional or behavioral data as benchmark evidence.

Public reports should minimize sensitive information.

## Benchmark leakage

Disclosure of holdout cases (`BENCHMARK.md`, "Benchmark integrity") is treated as a security
issue, not a content issue, because it silently invalidates results that cite the affected
release. Report it privately. A confirmed leak requires a benchmark patch release and
invalidation of results run against the leaked set.

## Responsible-use violations

A report that a deployment is using AEIL for a Prohibited purpose under
`RESPONSIBLE_USE.md` §2.1 is not a code vulnerability and should not go through this channel.
Raise it as a governance matter under `GOVERNANCE.md`, since the remedy is withdrawal of any
conformance label rather than a patch.
