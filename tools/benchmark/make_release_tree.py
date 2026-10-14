#!/usr/bin/env python3
"""Builds the complete AEIL v1.1.0 release tree from a pristine v1.0 checkout.

Order matters and is fixed:
  1. copy the pristine tree to the staging path
  2. apply the normative document edits (anchors are v1.0 text, so this must run before any
     other change touches those files)
  3. overlay the new normative documents, schemas and tooling
  4. assemble the benchmark (reads pristine v1.0 cases, writes v1.1.0 cases)
  5. repository hygiene: licences, placeholders, manifest, renames, demo separation
  6. release metadata: VERSION, CHANGELOG, README, MAINTAINERS

Usage: python3 build/make_release_tree.py <pristine_v1.0> <staging_dir>
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys

BUILD = os.path.dirname(os.path.abspath(__file__))
HOME = os.path.dirname(BUILD)
PROPOSALS = os.path.join(HOME, "AEIL_review", "proposals")

sys.path.insert(0, BUILD)
sys.path.insert(0, os.path.join(BUILD))

import doc_edits                                                      # noqa: E402

# tools/apply_proposals.py holds the demo banner, scoped licence reservation and ADR
# template. Resolve it from the repository this script lives in first (so a bare checkout
# works), falling back to the review workspace when bootstrapping a new tree.
for _candidate in (os.path.join(HOME, "aeil-fork", "tools"),
                   os.path.join(PROPOSALS, "tools")):
    if os.path.exists(os.path.join(_candidate, "apply_proposals.py")):
        sys.path.insert(0, _candidate)
        break
import apply_proposals as ap                                          # noqa: E402

RELEASE = "1.1.0"
BENCH_RELEASE = "1.1.0"
REPO_URL = "https://github.com/vdon61-wq/AEILv1.0"
PAGES_URL = "https://vdon61-wq.github.io/AEILv1.0/"


def run(cmd: list[str], **kw) -> str:
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        raise SystemExit(f"command failed: {' '.join(cmd)}\n{r.stdout}\n{r.stderr}")
    return r.stdout


# ------------------------------------------------------------------ new files
GITIGNORE = """# Python
__pycache__/
*.py[cod]
*.egg-info/
.venv/
venv/

# Tool caches
.pytest_cache/
.mypy_cache/
.ruff_cache/
.coverage
htmlcov/

# Build and validation output
build/
dist/
validation.json
demo-results.json
demo-report.json

# Editors and OS
.DS_Store
*.swp
.idea/
.vscode/

# Local audit working data - never commit real people's emotional or behavioural
# data as benchmark evidence (SECURITY.md).
audits/local/
results/*.json
!protocol/examples/*.json
"""

MAINTAINERS = """# AEIL Maintainers

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
"""

CODE_OF_CONDUCT = """# AEIL Code of Conduct

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
"""

ADR_TEMPLATE_PATH = "docs/adr/0000-template.md"


def build(pristine: str, staging: str) -> int:
    for label, root in (("pristine", pristine),):
        if not os.path.isdir(os.path.join(root, "benchmark")):
            raise SystemExit(f"not an AEIL repository ({label}): {root}")
    if os.path.abspath(pristine) == os.path.abspath(staging):
        raise SystemExit("pristine and staging must differ")

    # ---- 1. clean copy ---------------------------------------------------
    if os.path.exists(staging):
        shutil.rmtree(staging)
    shutil.copytree(pristine, staging, symlinks=True,
                    ignore=shutil.ignore_patterns(".git", "__pycache__"))
    print(f"[1/6] copied pristine tree -> {staging}")

    # ---- 2. normative document edits ------------------------------------
    print("[2/6] applying normative document edits")
    if doc_edits.apply(staging) != 0:
        raise SystemExit("document edits failed - aborting, nothing written")

    # ---- 3. overlay new documents, schemas, tooling ----------------------
    print("[3/6] overlaying new documents, schemas and tooling")
    overlay = {
        "MEMORY.md": "MEMORY.md",
        "POLICY.md": "POLICY.md",
        "RESPONSIBLE_USE.md": "RESPONSIBLE_USE.md",
        "ROADMAP.md": "ROADMAP.md",
        "protocol/aeil-test.schema.json": "protocol/aeil-test.schema.json",
        "protocol/aeil-emotional-event.schema.json": "protocol/aeil-emotional-event.schema.json",
        "protocol/aeil-policy.schema.json": "protocol/aeil-policy.schema.json",
        "protocol/aeil-report.schema.v1.1.json": "protocol/aeil-report.schema.v1.1.json",
        "ci/aeil-validate.yml": ".github/workflows/aeil-validate.yml",
        "tools/aeil_score.py": "tools/aeil_score.py",
        "tools/validate_repo.py": "tools/validate_repo.py",
        "tools/make_demo_results.py": "tools/make_demo_results.py",
        "tools/apply_proposals.py": "tools/apply_proposals.py",
        "tools/test_schemas.py": "tools/test_schemas.py",
    }
    for src, dst in overlay.items():
        s = os.path.join(PROPOSALS, src)
        if not os.path.exists(s):
            raise SystemExit(f"missing proposal artefact: {src}")
        d = os.path.join(staging, dst)
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copy2(s, d)
        print(f"   + {dst}")

    for src in ("dimension_map.py", "new_core_cases.py", "memory_cases.py",
                "assemble.py", "doc_edits.py", "make_release_tree.py",
                "make_selfcontained.py", "make_example_report.py"):
        s = os.path.join(BUILD, src)
        if os.path.exists(s):
            d = os.path.join(staging, "tools", "benchmark", src)
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copy2(s, d)
            print(f"   + tools/benchmark/{src}")

    with open(os.path.join(staging, "MAINTAINERS.md"), "w", encoding="utf-8") as fh:
        fh.write(MAINTAINERS)
    with open(os.path.join(staging, "CODE_OF_CONDUCT.md"), "w", encoding="utf-8") as fh:
        fh.write(CODE_OF_CONDUCT)
    os.makedirs(os.path.join(staging, "docs", "adr"), exist_ok=True)
    # ADR template is defined in tools/apply_proposals.py; write it out
    with open(os.path.join(staging, ADR_TEMPLATE_PATH), "w", encoding="utf-8") as fh:
        fh.write(ap.ADR_TEMPLATE)
    print("   + MAINTAINERS.md, CODE_OF_CONDUCT.md, docs/adr/0000-template.md")

    # ---- 4. benchmark ----------------------------------------------------
    print("[4/6] assembling benchmark v1.1.0")
    env = dict(os.environ, AEIL_REPO=staging)
    out = run([sys.executable, os.path.join(staging, "tools", "benchmark", "assemble.py"),
               staging, pristine], env=env)
    print("   " + out.strip().replace("\n", "\n   "))

    # ---- 4b. generated example report (needs benchmark 1.1.0 + schemas in place)
    print("[4b/6] generating protocol/examples/example-model-audit-v1.1.json")
    out4b = run([sys.executable, os.path.join(BUILD, "make_example_report.py"),
                 staging, os.path.join(staging, "protocol", "examples",
                                       "example-model-audit-v1.1.json")])
    print("   " + out4b.strip())
    print("[4c/6] schema regression tests")
    out4c = run([sys.executable, os.path.join(staging, "tools", "test_schemas.py"), staging])
    print("   " + out4c.strip().replace("\n", "\n   "))

    # ---- 5. repository hygiene ------------------------------------------
    print("[5/6] repository hygiene")
    hygiene(staging, pristine)

    # never ship build artefacts; v1.0 had no .gitignore at all
    with open(os.path.join(staging, ".gitignore"), "w", encoding="utf-8") as fh:
        fh.write(GITIGNORE)
    removed = 0
    for root, dirs, _files in os.walk(staging):
        for d in list(dirs):
            if d in ("__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"):
                shutil.rmtree(os.path.join(root, d), ignore_errors=True)
                dirs.remove(d)
                removed += 1
    print(f"   + .gitignore; removed {removed} cache dir(s) from the tree")

    # ---- 6. release metadata --------------------------------------------
    print("[6/6] release metadata")
    release_metadata(staging)

    print(f"\nrelease tree ready at {staging}")
    return 0


# ------------------------------------------------------------------- hygiene
def hygiene(staging: str, pristine: str) -> None:
    # 5a. full canonical licence texts
    licences_dir = os.path.join(staging, "AEIL_v1.0_licenses", "LICENSES")
    os.makedirs(licences_dir, exist_ok=True)
    for name, url in (("Apache-2.0.txt", "https://www.apache.org/licenses/LICENSE-2.0.txt"),
                      ("CC-BY-4.0.txt",
                       "https://creativecommons.org/licenses/by/4.0/legalcode.txt")):
        cached = os.path.join("/tmp", name)
        dest = os.path.join(licences_dir, name)
        if os.path.exists(cached) and os.path.getsize(cached) > 5000:
            shutil.copy2(cached, dest)
        else:
            import urllib.request
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            data = urllib.request.urlopen(req, timeout=60).read()
            with open(dest, "wb") as fh:
                fh.write(data)
        lines = len(open(dest, encoding="utf-8", errors="replace").read().splitlines())
        print(f"   = AEIL_v1.0_licenses/LICENSES/{name}: {lines} lines (was a 10-12 line stub)")

    # 5b. root licence so GitHub detects it
    with open(os.path.join(staging, "LICENSE"), "w", encoding="utf-8") as fh:
        fh.write(ROOT_LICENCE)
    print("   + LICENSE (root) - GitHub previously reported 'license: null'")

    # 5c. close placeholders
    subs = {
        "AEIL_v1.0_licenses/CITATION.cff": [
            ("https://github.com/[OWNER]/AEIL", REPO_URL),
            ("https://[OFFICIAL-AEIL-DOMAIN]/", PAGES_URL),
            ('version: "1.0"', f'version: "{RELEASE}"'),
            ('title: "AI Emotional Intelligence Layer (AEIL) v1.0"',
             f'title: "AI Emotional Intelligence Layer (AEIL) v{RELEASE}"'),
        ],
        "AEIL_v1.0_licenses/NOTICE": [
            ("[insert official AEIL project URL]", REPO_URL),
        ],
        "AEIL_v1.0_licenses/LICENSE-SPECIFICATION.md": [
            ("**[insert official AEIL project URL]**", f"**{REPO_URL}**"),
        ],
        "protocol/aeil-report.schema.json": [
            ("https://example.org/aeil/v1.0/aeil-report.schema.json",
             f"{PAGES_URL}protocol/aeil-report.schema.json"),
            ('"pattern": "^1\\\\.0\\\\.\\\\d+$"', '"pattern": "^\\\\d+\\\\.\\\\d+\\\\.\\\\d+$"'),
        ],
    }
    for rel, pairs in subs.items():
        p = os.path.join(staging, rel)
        if not os.path.exists(p):
            print(f"   ! {rel} not found, placeholder fixes skipped")
            continue
        body = open(p, encoding="utf-8").read()
        hit = 0
        for a, b in pairs:
            if a in body:
                body = body.replace(a, b)
                hit += 1
        open(p, "w", encoding="utf-8").write(body)
        print(f"   = {rel}: {hit}/{len(pairs)} placeholder(s) closed")

    # 5c2. disambiguate the bare `README.md` reference in the licence map: four different
    #      README.md files now exist, so an unqualified reference is ambiguous.
    lm = os.path.join(staging, "AEIL_v1.0_licenses", "LICENSE-MAP.md")
    if os.path.exists(lm):
        body = open(lm, encoding="utf-8").read()
        before = body
        body = body.replace("- `README.md`\n", "- `/README.md` (root)\n", 1)
        if body != before:
            open(lm, "w", encoding="utf-8").write(body)
            print("   = AEIL_v1.0_licenses/LICENSE-MAP.md: bare `README.md` reference "
                  "qualified as `/README.md` (root)")

    # 5d. duplicate CERTIFICATION.md
    dup = os.path.join(staging, "AEIL_v1.0_licenses", "CERTIFICATION.md")
    if os.path.exists(dup):
        shutil.move(dup, os.path.join(staging, "AEIL_v1.0_licenses",
                                      "CERTIFICATION-POLICY.md"))
        print("   = AEIL_v1.0_licenses/CERTIFICATION.md -> CERTIFICATION-POLICY.md "
              "(two different files shared one name)")

    # 5e. extension-less knowledge base
    kb = os.path.join(staging, "aeildocsen")
    if os.path.exists(kb):
        dest = os.path.join(staging, "docs", "knowledge-base", "index.html")
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.move(kb, dest)
        with open(os.path.join(staging, "docs", "knowledge-base", "README.md"), "w",
                  encoding="utf-8") as fh:
            fh.write(KB_README)
        print("   = aeildocsen -> docs/knowledge-base/index.html (221 KB, no extension, "
              "unrendered by GitHub)")

    # 5f. demo separation + mechanical demo fixes
    demo = os.path.join(staging, "demo")
    os.makedirs(demo, exist_ok=True)
    idx = os.path.join(staging, "index.html")
    if os.path.exists(idx):
        shutil.move(idx, os.path.join(demo, "index.html"))
        with open(os.path.join(demo, "README.md"), "w", encoding="utf-8") as fh:
            fh.write(ap.DEMO_README)
        ap._patch_demo(os.path.join(demo, "index.html"))
        print("   = index.html -> demo/index.html (proprietary, non-normative, "
              "deterministic, regulatory banner)")
    # keep GitHub Pages working from the repository root
    with open(os.path.join(staging, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(PAGES_REDIRECT)
    print("   + index.html (root) - redirect so the existing Pages URL keeps working")


ROOT_LICENCE = """# AEIL — Licensing

AEIL uses a multi-licence structure because the specification, benchmark, software, branding
and certification programme have different legal and operational roles. The authoritative
description is [`AEIL_v1.0_licenses/LICENSE.md`](AEIL_v1.0_licenses/LICENSE.md) and the
file-by-file mapping is
[`AEIL_v1.0_licenses/LICENSE-MAP.md`](AEIL_v1.0_licenses/LICENSE-MAP.md).

| Material | Licence |
|---|---|
| Specification and prose documentation (`*.md`, `docs/`) | CC-BY-4.0 |
| Public benchmark (`benchmark/`) | CC-BY-4.0 |
| Code, JSON schemas and tooling (`tools/`, `protocol/`, `.github/`) | Apache-2.0 |
| AEIL name, logos, certification marks | see `AEIL_v1.0_licenses/TRADEMARK.md` |
| Demonstration platform (`demo/`) | **proprietary, all rights reserved** — not part of the open specification |

SPDX-License-Identifier: CC-BY-4.0 OR Apache-2.0

Full canonical licence texts: [`AEIL_v1.0_licenses/LICENSES/`](AEIL_v1.0_licenses/LICENSES/).

## Why this file is at the root

Until v1.1.0 the licence files lived only under `AEIL_v1.0_licenses/`, so GitHub reported
`license: null` for the repository and an adopter cloning it received no machine-readable
grant. This file exists so the licence is detectable; it does not replace the detailed map.

## Boundary that v1.0 left ambiguous

`index.html` (now `demo/index.html`) carried an all-rights-reserved notice claiming exclusive
rights over "the code, design, **methodology**, texts and graphics", while
`AEIL_v1.0_licenses/LICENSE.md` states that "commercial use is intentionally permitted" and
the licence map assigns `docs/*` to CC-BY-4.0. Both cannot be true of the methodology.

v1.1.0 resolves it by separation rather than by choosing a winner: the **methodology is open**
(CC-BY-4.0 / Apache-2.0) and the **demo is proprietary**. The demo's notice is scoped to the
`demo/` folder and says so explicitly. If the maintainers intend the opposite - a proprietary
methodology with an open-looking repository - that is a legitimate choice, but it must be made
deliberately and the CC-BY-4.0 files withdrawn, because as published the repository grants
rights it elsewhere disclaims.
"""

KB_README = """# AEIL knowledge base — informative, NON-NORMATIVE

`index.html` in this folder was published in v1.0 as the extension-less file `aeildocsen`
(221 KB), which GitHub neither renders nor lists. It is renamed here so it is reachable.

**This document is non-normative.** It describes a "12-stage AEIL Core Engine pipeline", while
`demo/index.html` describes a 14-stage "Universal AEIL Pipeline" and `SPECIFICATION.md` defines
six behavioural dimensions plus the AEIL-M axis. Those three descriptions are not equivalent,
and in v1.0 nothing said which one governed.

## Regulatory notice — read before relying on the product descriptions below

The knowledge base describes the same seven applied products as the demo, including
**AI Team Manager** and **AI Education Manager**. Both infer the emotional state of identified
individuals in, respectively, the workplace and an education institution.

In the European Union that is a **prohibited AI practice** under Article 5(1)(f) of Regulation
(EU) 2024/1689 (the AI Act), applicable since 2 February 2025. The only exception is a system
genuinely intended for **medical or safety** reasons. The prohibition has been in force since
before v1.0 of this repository was published.

These descriptions must therefore be read as illustrative of what an emotional-intelligence
layer *could* compute, not as deployable products. See
[`/RESPONSIBLE_USE.md`](../../RESPONSIBLE_USE.md) — in particular PU-1 (workplace), PU-2
(education), PU-5 (employment decisions) and §6 (remediation guidance) — and
[`/demo/README.md`](../../demo/README.md).

Nothing in this folder is a compliance instrument, and no AEIL score or label is evidence of
legal compliance (PU-11).

`SPECIFICATION.md` §0 now settles it: the normative behavioural model is the six dimensions
plus AEIL-M. Any stage-count pipeline is an implementation or presentation choice. Where this
knowledge base conflicts with a normative document, the normative document prevails and this
text should be corrected.

See `benchmark/COVERAGE.md` for the generated coverage report and `ROADMAP.md` for what is
planned next.
"""

PAGES_REDIRECT = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>AEIL — AI Emotional Intelligence Layer</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="refresh" content="0; url=demo/index.html">
<link rel="canonical" href="https://vdon61-wq.github.io/AEILv1.0/">
<style>
body{margin:0;background:#070b13;color:#e6edf7;
font:16px/1.6 ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
display:grid;place-items:center;min-height:100vh;padding:24px}
main{max-width:640px;text-align:center}
a{color:#7dd3fc}h1{font-size:26px;margin:0 0 12px}
code{background:#111827;padding:2px 6px;border-radius:5px;font-size:13px}
.box{background:#0d1420;border:1px solid #1f2a3a;border-radius:12px;padding:20px 22px;
margin-top:22px;text-align:left;font-size:14px}
</style>
</head>
<body>
<main>
<h1>AEIL — AI Emotional Intelligence Layer</h1>
<p>Redirecting to the demonstration platform. If nothing happens,
<a href="demo/index.html">open the demo</a>.</p>

<div class="box">
<strong>The demo is not the specification.</strong>
<p style="margin:8px 0 0">The normative documents are Markdown files at the repository root:
<a href="https://github.com/vdon61-wq/AEILv1.0/blob/main/SPECIFICATION.md"><code>SPECIFICATION.md</code></a>,
<a href="https://github.com/vdon61-wq/AEILv1.0/blob/main/MEMORY.md"><code>MEMORY.md</code></a>,
<a href="https://github.com/vdon61-wq/AEILv1.0/blob/main/POLICY.md"><code>POLICY.md</code></a>,
<a href="https://github.com/vdon61-wq/AEILv1.0/blob/main/RESPONSIBLE_USE.md"><code>RESPONSIBLE_USE.md</code></a>,
<a href="https://github.com/vdon61-wq/AEILv1.0/blob/main/SCORING.md"><code>SCORING.md</code></a>
and <a href="https://github.com/vdon61-wq/AEILv1.0/blob/main/BENCHMARK.md"><code>BENCHMARK.md</code></a>.</p>
<p style="margin:8px 0 0">The demo is a proprietary, non-normative illustration with synthetic
data. It depicts emotion inference in workplace and education settings, which is a prohibited
AI practice in the EU under Art.&nbsp;5(1)(f) of Regulation (EU) 2024/1689 except for medical
or safety purposes; see
<a href="https://github.com/vdon61-wq/AEILv1.0/blob/main/RESPONSIBLE_USE.md"><code>RESPONSIBLE_USE.md</code></a>.</p>
</div>
</main>
</body>
</html>
"""


README_V11 = """# AEIL v1.1.0
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
"""


# --------------------------------------------------------- release metadata
def release_metadata(staging: str) -> None:
    with open(os.path.join(staging, "VERSION"), "w", encoding="utf-8") as fh:
        fh.write(RELEASE + "\n")

    draft = open(os.path.join(PROPOSALS, "CHANGELOG-1.1.0-draft.md"),
                 encoding="utf-8").read()
    # the draft already ends with a normalised 1.0.0 entry; use it verbatim
    with open(os.path.join(staging, "CHANGELOG.md"), "w", encoding="utf-8") as fh:
        fh.write(draft if draft.endswith("\n") else draft + "\n")
    with open(os.path.join(staging, "README.md"), "w", encoding="utf-8") as fh:
        fh.write(README_V11)
    print("   = VERSION -> 1.1.0, CHANGELOG.md -> 1.1.0 entry, README.md rewritten")

    # MANIFEST regenerated from the finished tree
    files = []
    for root, dirs, names in os.walk(staging):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        for n in names:
            rel = os.path.relpath(os.path.join(root, n), staging).replace("\\", "/")
            if rel != "MANIFEST.json":
                files.append(rel)
    files.sort()

    suites = {}
    for s in ("core", "safety", "adaptation", "agents", "memory"):
        p = os.path.join(staging, "benchmark", s, "tests.json")
        if os.path.exists(p):
            suites[s] = len(json.load(open(p, encoding="utf-8")).get("tests", []))

    manifest = {
        "project": "AEIL",
        "version": RELEASE,
        "benchmark_version": BENCH_RELEASE,
        "status": "Public Specification",
        "generated_by": "tools/benchmark/make_release_tree.py; verify with "
                        "tools/validate_repo.py in CI. Do not edit by hand.",
        "repository": REPO_URL,
        "normative_sources": [
            "SPECIFICATION.md", "PRINCIPLES.md", "TAXONOMY.md", "SCORING.md", "SEVERITY.md",
            "SAFETY.md", "MEMORY.md", "POLICY.md", "RESPONSIBLE_USE.md", "BENCHMARK.md",
        ],
        "informative": ["demo/", "docs/knowledge-base/", "docs/ARTICLES.md", "ROADMAP.md"],
        "files": files,
        "benchmark_tests": sum(suites.values()),
        "benchmark_suites": suites,
    }
    with open(os.path.join(staging, "MANIFEST.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(f"   = MANIFEST.json regenerated: {len(files)} files, "
          f"{sum(suites.values())} benchmark cases")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    sys.exit(build(sys.argv[1], sys.argv[2]))
