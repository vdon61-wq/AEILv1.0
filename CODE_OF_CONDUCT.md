# AEIL Code of Conduct

## Scope

Applies to all spaces associated with AEIL: the repository, issues, pull requests, benchmark
contributions, audits, and any chat or forum where AEIL is being developed.

## Why this project needs one

AEIL exists to make emotionally-adaptive AI accountable. A project whose own conduct is
unaccountable cannot credibly ask that of others. Two behaviours are specifically corrosive
here and are called out explicitly:

- **Benchmark gaming presented as progress.** Editing a case, its scoring guidance or its
  severity to make a system look better is data falsification, not contribution. So is
  training on public cases and reporting the result as an independent AEIL score
  (`BENCHMARK.md`, "Benchmark integrity").
- **Appeal to authority over evidence.** "This is how our product works" is not an argument
  about what AEIL should require. `PRINCIPLES.md` P15 makes AEIL testable by independent
  evaluators precisely so that the maintainer can be wrong and be shown it.

## Expected behaviour

- Argue about the case, not the person. Benchmark review is adversarial by design
  (`CONTRIBUTING.md`); a challenged case is a working process, not a personal criticism.
- Disclose conflicts of interest when proposing or reviewing changes, especially where you
  are employed by, hold equity in, or sell against a system that AEIL evaluates
  (`GOVERNANCE.md`).
- Treat benchmark cases about distress, vulnerability, grief and coercion with care. They
  exist to protect real people and should not be rewritten for shock value or amusement.
- Assume good faith, correct in private first, escalate in public only when needed.

## Unacceptable behaviour

Harassment, personal or political attacks, trolling, inflammatory or derogatory language,
public or private harassment, publishing others' private data, and conduct that would be
unlawful in the applicable jurisdiction.

Specific to this project: submitting real people's emotional or behavioural data as benchmark
evidence (`SECURITY.md`), or proposing a case whose purpose is to make a system manipulate
more effectively rather than to detect manipulation.

## Enforcement

Report to the Specification Maintainer of record in `MAINTAINERS.md`, or via GitHub's private
reporting. Reports are handled confidentially. Where the maintainer is the subject of a
report, the report goes to any Independent Reviewer of record; where none exists, that fact is
stated publicly in the issue so the gap is visible rather than silently absorbing the report.

Consequences escalate from a private warning, through a public warning and temporary
ban, to permanent exclusion. Falsified benchmark data results in revert of the change and a
public note in `CHANGELOG.md`, because a silently reverted case leaves the next contributor
to make the same mistake.

## Attribution

Adapted from the Contributor Covenant, version 2.1, with project-specific additions above.
