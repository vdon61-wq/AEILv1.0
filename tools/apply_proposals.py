#!/usr/bin/env python3
"""Builds a candidate v1.1.0 repository tree by overlaying these proposals onto a clone
of the current AEILv1.0 repo, then applies the purely mechanical Sprint-0 fixes.

This exists so the effect of the proposals is measurable: run
`tools/validate_repo.py` before and after and diff the findings.

Usage:
  python3 tools/apply_proposals.py <clone_of_AEILv1.0> <output_dir>

Deliberately NOT done here (they need an owner decision, see gap analysis appendix 3):
  * embedding the full Apache-2.0 / CC-BY-4.0 texts;
  * deciding which assets are proprietary vs open (the demo is moved, not relicensed);
  * rewriting SPECIFICATION.md / PRINCIPLES.md / SCORING.md / SEVERITY.md / SAFETY.md prose;
  * rebalancing the existing 60 benchmark cases.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROPOSALS = os.path.dirname(HERE)

# proposal path -> destination path inside the candidate repo
COPY_MAP = {
    "MEMORY.md": "MEMORY.md",
    "POLICY.md": "POLICY.md",
    "RESPONSIBLE_USE.md": "RESPONSIBLE_USE.md",
    "ROADMAP.md": "ROADMAP.md",
    "CHANGELOG-1.1.0-draft.md": "docs/CHANGELOG-1.1.0-draft.md",
    "protocol/aeil-test.schema.json": "protocol/aeil-test.schema.json",
    "protocol/aeil-emotional-event.schema.json": "protocol/aeil-emotional-event.schema.json",
    "protocol/aeil-policy.schema.json": "protocol/aeil-policy.schema.json",
    "protocol/aeil-report.schema.v1.1.json": "protocol/aeil-report.schema.v1.1.json",
    "benchmark/memory/tests.json": "benchmark/memory/tests.json",
    "ci/aeil-validate.yml": ".github/workflows/aeil-validate.yml",
    "tools/aeil_score.py": "tools/aeil_score.py",
    "tools/validate_repo.py": "tools/validate_repo.py",
    "tools/make_demo_results.py": "tools/make_demo_results.py",
    "tools/apply_proposals.py": "tools/apply_proposals.py",
}

ROOT_LICENCE = """# AEIL — Licensing

AEIL uses a multi-licence structure. The authoritative description is
[`AEIL_v1.0_licenses/LICENSE.md`](AEIL_v1.0_licenses/LICENSE.md) and
[`AEIL_v1.0_licenses/LICENSE-MAP.md`](AEIL_v1.0_licenses/LICENSE-MAP.md).

| Material | Licence |
|---|---|
| Specification, documentation, public benchmark | CC-BY-4.0 |
| Code, JSON schemas, tooling (`tools/`, `protocol/`, `benchmark/`) | Apache-2.0 |
| AEIL name, logos, certification marks | see `AEIL_v1.0_licenses/TRADEMARK.md` |
| Demo platform (`demo/`) | proprietary — all rights reserved, **not** part of the open specification |

SPDX-License-Identifier: CC-BY-4.0 OR Apache-2.0

Full licence texts: `AEIL_v1.0_licenses/LICENSES/`.
"""

DEMO_README = """# AEIL demo platform — proprietary, non-normative

Everything in this folder is a **demonstration**, not part of the AEIL specification.

* The normative source is [`/SPECIFICATION.md`](../SPECIFICATION.md). Where this demo and
  the specification differ, the specification wins.
* The pipeline shown here ("Universal AEIL Pipeline") is **non-normative** and is not the
  six-dimension model of `SPECIFICATION.md` §4.
* All `confidence` values displayed are **synthetic simulation output**, produced by a
  deterministic seeded generator. They are not measured uncertainties.
* The data is fictional. No real person's emotional data appears here.

## Regulatory notice

This demo depicts emotion inference in a **workplace** setting (Team Manager) and an
**education** setting (Education Manager). In the European Union, inferring the emotions of a
natural person in the workplace or in education institutions is a **prohibited AI practice**
under Article 5(1)(f) of Regulation (EU) 2024/1689 (AI Act), applicable since 2 February 2025.
The only exception is a system genuinely intended for medical or safety reasons.

**These two demo scenarios must not be deployed in the EU as depicted.** See
[`/RESPONSIBLE_USE.md`](../RESPONSIBLE_USE.md) (PU-1, PU-2) and §6 of that document for the
required re-scoping (aggregated, non-attributable signals only).

## Licence

Copyright (c) the AEIL rights holder. All rights reserved for the contents of this folder.
This notice does not affect the CC-BY-4.0 / Apache-2.0 licensing of the specification,
benchmark, schemas and tooling elsewhere in this repository.
"""

ADR_TEMPLATE = """# ADR-{number}: {title}

- **Status:** proposed | accepted | superseded by ADR-{n}
- **Date:** YYYY-MM-DD
- **Deciders:** {roles per GOVERNANCE.md}
- **AEIL version affected:** {e.g. 1.1.0}
- **Conflicts of interest disclosed:** yes / no

## Context

What is the issue that we're seeing that is motivating this decision or change?

## Decision

The change that we're proposing or have made.

## Rationale (GOVERNANCE.md requires: rationale, proposed text, compatibility impact,
## evidence, review period, release note)

* **Proposed text or test:** link to the diff / file.
* **Compatibility impact:** does this change dimensions, scoring or benchmark semantics
  (⇒ major), add backward-compatible content (⇒ minor), or fix documentation (⇒ patch)?
* **Evidence:** benchmark results, replication studies, evaluator-agreement data.
* **Review period:** from YYYY-MM-DD to YYYY-MM-DD.
* **Release note:** text to appear in CHANGELOG.md.

## Consequences

What becomes easier or harder as a result.
"""


def sh_copy(src: str, dst: str) -> None:
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)


DEMO_PLACEHOLDER_ORIGIN = "https://aeil-demo.example.com/"
DEMO_PUBLIC_URL = "https://vdon61-wq.github.io/AEILv1.0/demo/"

BANNER_CSS = """
<style id="aeil-non-normative-banner-style">
#aeil-banner{position:sticky;top:0;z-index:99999;background:#7a1220;color:#fff;
font:600 13px/1.5 system-ui,sans-serif;padding:10px 16px;border-bottom:2px solid #ff5a6e}
#aeil-banner b{color:#ffd7dc}#aeil-banner a{color:#ffd7dc}
</style>
"""

BANNER_HTML = """
<div id="aeil-banner" role="note">
<b>Non-normative demonstration.</b> The authoritative AEIL methodology is
<a href="../SPECIFICATION.md">SPECIFICATION.md</a>. All confidence values shown are
<b>synthetic simulation output</b> from a deterministic seeded generator, not measured
uncertainty. This demo depicts emotion inference in workplace and education settings, which is a
<b>prohibited AI practice in the EU</b> under Art.&nbsp;5(1)(f) of Regulation (EU) 2024/1689
(AI Act) except for medical or safety purposes &mdash; it must not be deployed as depicted.
See <a href="README.md">demo/README.md</a> and <a href="../RESPONSIBLE_USE.md">RESPONSIBLE_USE.md</a>.
</div>
"""

# Deterministic replacement for Math.random (PRINCIPLES P10 reproducibility).
# Injected before any application script so the 7 call sites become reproducible.
SEEDED_PRNG = """
<script id="aeil-deterministic-prng">
/* AEIL demo determinism shim: replaces Math.random with a seeded mulberry32 PRNG so that
   displayed "confidence" values are reproducible (PRINCIPLES.md P10). Values remain synthetic. */
(function () {
  var seed = 0x4145494C; /* "AEIL" */
  Math.random = function () {
    seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
    var t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
})();
</script>
"""

SCOPED_RESERVATION = """<!-- ===============================================================
     AEIL DEMO PLATFORM - proprietary, NON-NORMATIVE.
     Copyright (c) the AEIL rights holder. All rights reserved for the
     contents of this demo/ folder only: its HTML, CSS, JavaScript, layout,
     copy and graphics.

     This reservation is scoped to the demo. It does NOT apply to the AEIL
     specification, benchmark, JSON schemas or tooling elsewhere in this
     repository, which are licensed CC-BY-4.0 (documentation, benchmark) and
     Apache-2.0 (code, schemas) - see /LICENSE and
     /AEIL_v1.0_licenses/LICENSE-MAP.md.

     The methodology demonstrated here is non-normative; /SPECIFICATION.md is
     authoritative. Contact / licensing: see demo/README.md.
     =============================================================== -->"""


def _patch_demo(path: str) -> None:
    """Mechanical, reversible fixes to the demo asset (gap analysis section D5, R3, R5)."""
    body = open(path, encoding="utf-8", errors="replace").read()
    original_len = len(body)
    changes = []

    # (a) scope the all-rights-reserved claim to the demo folder
    m = re.search(r"<!--[^>]*?©\s*20\d\d[^>]*?All rights reserved.*?-->", body, re.S)
    if m:
        body = body[:m.start()] + SCOPED_RESERVATION + body[m.end():]
        changes.append("copyright reservation scoped to demo/")
    elif re.search(r"All rights reserved", body, re.I):
        changes.append("WARN: reservation present but header block not matched - fix manually")

    # (b) replace the placeholder legal URL with a real, relative target
    n = body.count("https://aeil-demo.example.com/legal/license")
    if n:
        body = body.replace("https://aeil-demo.example.com/legal/license", "README.md")
        changes.append(f"placeholder legal URL -> README.md ({n}x)")

    # (b2) replace the remaining placeholder demo domain (canonical / og:url / JSON-LD)
    #      with the repository's real GitHub Pages location, now that the demo moved to demo/
    n = body.count(DEMO_PLACEHOLDER_ORIGIN)
    if n:
        body = body.replace(DEMO_PLACEHOLDER_ORIGIN, DEMO_PUBLIC_URL)
        changes.append(f"{DEMO_PLACEHOLDER_ORIGIN} -> {DEMO_PUBLIC_URL} ({n}x)")

    # (b3) fix the in-page copyright notice string: stale year + placeholder domain
    m = re.search(r"var NOTICE='([^']*)';", body)
    if m:
        body = body.replace(m.group(0),
                            "var NOTICE='\\n\\n\u00a9 2026 AEIL Demo Platform \u00b7 "
                            "non-normative demonstration \u00b7 see demo/README.md\\n"
                            "Proprietary demo assets. The AEIL specification, benchmark and "
                            "schemas are openly licensed (CC-BY-4.0 / Apache-2.0).';")
        changes.append("in-page NOTICE string: year 2025 -> 2026, placeholder domain removed, "
                       "open/proprietary boundary stated")

    # (c) deterministic PRNG + inline banner, injected before the first script/head end
    if "aeil-deterministic-prng" not in body:
        if re.search(r"<head[^>]*>", body, re.I):
            body = re.sub(r"(<head[^>]*>)", r"\1" + BANNER_CSS + SEEDED_PRNG, body, count=1,
                          flags=re.I)
            changes.append("seeded PRNG shim + banner CSS injected after <head>")
        if re.search(r"<body[^>]*>", body, re.I):
            body = re.sub(r"(<body[^>]*>)", r"\1" + BANNER_HTML, body, count=1, flags=re.I)
            changes.append("inline non-normative + Art. 5(1)(f) banner injected after <body>")

    if body != open(path, encoding="utf-8", errors="replace").read():
        open(path, "w", encoding="utf-8").write(body)
        print(f"  patched demo/index.html ({original_len} -> {len(body)} bytes)")
        for c in changes:
            print(f"    - {c}")


def build(src_repo: str, out: str) -> int:
    if os.path.abspath(src_repo) == os.path.abspath(out):
        print("source and destination must differ")
        return 2
    if os.path.exists(out):
        shutil.rmtree(out)
    shutil.copytree(src_repo, out, symlinks=True,
                    ignore=shutil.ignore_patterns(".git", "__pycache__", "node_modules"))

    # 1. overlay proposals
    for rel, dst in COPY_MAP.items():
        s = os.path.join(PROPOSALS, rel)
        if os.path.exists(s):
            sh_copy(s, os.path.join(out, dst))
        else:
            print(f"  skip (missing): {rel}")

    # 2. move the proprietary demo out of the specification surface
    demo = os.path.join(out, "demo")
    os.makedirs(demo, exist_ok=True)
    for name in ("index.html", "aeildocsen"):
        p = os.path.join(out, name)
        if os.path.exists(p):
            target = os.path.join(demo, "index.html" if name == "index.html"
                                  else "knowledge-base.html")
            shutil.move(p, target)
            print(f"  moved {name} -> demo/{os.path.basename(target)}")
    with open(os.path.join(demo, "README.md"), "w", encoding="utf-8") as fh:
        fh.write(DEMO_README)

    # 2b. mechanical demo fixes: scope the copyright claim, kill the placeholder legal URL,
    #     make the simulation deterministic (P10), and add the inline non-normative banner.
    demo_index = os.path.join(demo, "index.html")
    if os.path.exists(demo_index):
        _patch_demo(demo_index)

    # 3. root licence so GitHub detects it
    with open(os.path.join(out, "LICENSE"), "w", encoding="utf-8") as fh:
        fh.write(ROOT_LICENCE)

    # 4. ADR directory (GOVERNANCE.md change process needs somewhere to record decisions)
    adr = os.path.join(out, "docs", "adr")
    os.makedirs(adr, exist_ok=True)
    with open(os.path.join(adr, "0000-template.md"), "w", encoding="utf-8") as fh:
        fh.write(ADR_TEMPLATE)

    # 5. fix the report schema: placeholder $id and the 1.0.x-only version pattern
    schema_rel = os.path.join(out, "protocol", "aeil-report.schema.json")
    if os.path.exists(schema_rel):
        body = open(schema_rel, encoding="utf-8").read()
        body = body.replace("https://example.org/aeil/v1.0/aeil-report.schema.json",
                            "https://vdon61-wq.github.io/AEILv1.0/protocol/aeil-report.schema.json")
        body = body.replace(r'"pattern": "^1\\.0\\.\\d+$"', r'"pattern": "^\\d+\\.\\d+\\.\\d+$"')
        body = re.sub(r'"\$id":\s*"https://example\.org[^"]*"',
                      '"$id": "https://vdon61-wq.github.io/AEILv1.0/protocol/aeil-report.schema.json"',
                      body)
        body = body.replace('"pattern": "^1\\\\.0\\\\.\\\\d+$"', '"pattern": "^\\\\d+\\\\.\\\\d+\\\\.\\\\d+$"')
        open(schema_rel, "w", encoding="utf-8").write(body)
        json.loads(body)  # must stay valid
        print("  patched protocol/aeil-report.schema.json ($id, version pattern)")

    # 6. rename the ambiguous duplicate certification policy
    dup = os.path.join(out, "AEIL_v1.0_licenses", "CERTIFICATION.md")
    if os.path.exists(dup):
        shutil.move(dup, os.path.join(out, "AEIL_v1.0_licenses", "CERTIFICATION-POLICY.md"))
        print("  renamed AEIL_v1.0_licenses/CERTIFICATION.md -> CERTIFICATION-POLICY.md")

    # 7. close the citation / notice placeholders
    for rel, pairs in {
        "AEIL_v1.0_licenses/CITATION.cff": [
            ("https://github.com/[OWNER]/AEIL", "https://github.com/vdon61-wq/AEILv1.0"),
            ("https://[OFFICIAL-AEIL-DOMAIN]/", "https://vdon61-wq.github.io/AEILv1.0/"),
        ],
        "AEIL_v1.0_licenses/NOTICE": [
            ("[insert official AEIL project URL]", "https://github.com/vdon61-wq/AEILv1.0"),
        ],
        "AEIL_v1.0_licenses/LICENSE-SPECIFICATION.md": [
            ("**[insert official AEIL project URL]**",
             "**https://github.com/vdon61-wq/AEILv1.0**"),
        ],
    }.items():
        p = os.path.join(out, rel)
        if not os.path.exists(p):
            continue
        body = open(p, encoding="utf-8").read()
        for a, b in pairs:
            body = body.replace(a, b)
        open(p, "w", encoding="utf-8").write(body)
        print(f"  closed placeholders in {rel}")

    # 8. regenerate MANIFEST.json from the tree
    files = []
    for root, dirs, names in os.walk(out):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        for n in names:
            rel = os.path.relpath(os.path.join(root, n), out).replace("\\", "/")
            if rel == "MANIFEST.json":
                continue
            files.append(rel)
    files.sort()
    total_tests = 0
    for suite in ("core", "safety", "adaptation", "agents", "memory"):
        p = os.path.join(out, "benchmark", suite, "tests.json")
        if os.path.exists(p):
            data = json.load(open(p, encoding="utf-8"))
            total_tests += len(data.get("tests", []))
    manifest = {
        "project": "AEIL",
        "version": "1.1.0-draft",
        "status": "Public Specification (draft)",
        "generated_by": "tools/apply_proposals.py - regenerate on every change and verify in CI",
        "files": files,
        "benchmark_tests": total_tests,
        "benchmark_suites": {
            s: len(json.load(open(os.path.join(out, "benchmark", s, "tests.json"),
                                  encoding="utf-8")).get("tests", []))
            for s in ("core", "safety", "adaptation", "agents", "memory")
            if os.path.exists(os.path.join(out, "benchmark", s, "tests.json"))
        },
    }
    with open(os.path.join(out, "MANIFEST.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(f"  regenerated MANIFEST.json ({len(files)} files, {total_tests} benchmark cases)")

    # 9. version bump marker
    with open(os.path.join(out, "VERSION"), "w", encoding="utf-8") as fh:
        fh.write("1.1.0-draft\n")

    print(f"\ncandidate tree written to {out}")
    return 0


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    return build(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    sys.exit(main())
