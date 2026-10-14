#!/usr/bin/env python3
"""AEIL repository consistency checker (proposal for tools/validate_repo.py).

Stdlib only. Designed to run in CI on every push. Every check prints a finding with a
severity and a rule id so results are diffable across releases.

Checks
------
MANIFEST   manifest <-> actual tree, both directions
PLACEHOLDER unresolved template placeholders in any tracked text file
SCHEMA     report-schema version pattern, $id host, additionalProperties
LICENCE    root licence detectable by GitHub; full licence texts present; contradictions
BENCH      required test fields, dimension coverage, multi-turn claims vs data
STRUCT     duplicate basenames with different content, extension-less large files
DEMO       non-determinism in demo assets; regulatory disclaimers
GOV        tags/releases, CI presence, ADR directory, security contact

Usage: python3 tools/validate_repo.py [--repo PATH] [--json out.json]
Exit code 0 = clean, 1 = findings, 2 = could not run.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from collections import defaultdict

TEXT_EXT = {".md", ".json", ".txt", ".html", ".yml", ".yaml", ".cff", ""}
PLACEHOLDER_PATTERNS = [
    (r"example\.(org|com)", "placeholder domain"),
    (r"\[insert [^\]]+\]", "unfilled placeholder"),
    (r"\[OWNER\]|\[OFFICIAL[^\]]*\]|\[TBD\]|\bTODO:\s", "unfilled placeholder"),
    (r"github\.com/\[", "unfilled URL"),
]
MIN_FULL_LICENCE_LINES = 50
# Documents that *describe* defects and fixes legitimately quote placeholders and
# conflicting numbers; scanning them produces self-referential false positives.
META_DOC_RE = re.compile(
    r"(^|/)(ROADMAP\.md|CHANGELOG[^/]*\.md|CONTRIBUTING\.md|SECURITY\.md"
    r"|docs/adr/|docs/CHANGELOG[^/]*\.md|AEIL_gap_analysis\.md)", re.I)
WEIGHTS = {"CR": 20, "IN": 15, "RA": 25, "SB": 20, "AD": 10, "TR": 10}
REQUIRED_TEST_FIELDS = ["test_id", "category", "title", "scenario", "expected_behavior",
                        "prohibited_behavior", "scoring_guidance", "default_severity_if_failed"]
SEVERITIES_OK = {"Critical", "High", "Medium", "Low"}


def _strip_json_prose(body: str) -> str:
    """Drop JSON Schema description/$comment/title prose before scanning for placeholders."""
    try:
        doc = json.loads(body)
    except json.JSONDecodeError:
        return body

    def clean(node):
        if isinstance(node, dict):
            return {k: clean(v) for k, v in node.items()
                    if k not in ("description", "$comment", "title")}
        if isinstance(node, list):
            return [clean(x) for x in node]
        return node

    return json.dumps(clean(doc))


class Report:
    def __init__(self) -> None:
        self.findings: list[dict] = []

    def add(self, severity: str, rule: str, message: str, path: str = "") -> None:
        self.findings.append({"severity": severity, "rule": rule, "message": message, "path": path})

    def emit(self) -> None:
        order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3, "Info": 4}
        grouped = defaultdict(list)
        for f in sorted(self.findings, key=lambda x: (order.get(x["severity"], 9), x["rule"])):
            grouped[f["severity"]].append(f)
        for sev in ["Critical", "High", "Medium", "Low", "Info"]:
            if not grouped[sev]:
                continue
            print(f"\n=== {sev} ({len(grouped[sev])}) ===")
            for f in grouped[sev]:
                loc = f" [{f['path']}]" if f["path"] else ""
                print(f"  {f['rule']}: {f['message']}{loc}")
        counts = {k: len(v) for k, v in grouped.items()}
        print(f"\ntotal findings: {sum(counts.values())} {counts}")


ARTIFACT_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "build", "dist",
                 ".pytest_cache", ".mypy_cache", ".ruff_cache", "coverage", ".next", "out",
                 "target", ".cache"}


def tracked_files(repo: str) -> list[str]:
    """Files that constitute the release: git-tracked (plus untracked-but-not-ignored) when
    this is a git checkout, so CI artefacts like build/validation.json are never mistaken for
    repository content. Falls back to a directory walk for exported trees."""
    gitdir = os.path.join(repo, ".git")
    if os.path.exists(gitdir):
        try:
            r = subprocess.run(
                ["git", "-C", repo, "ls-files", "--cached", "--others", "--exclude-standard"],
                capture_output=True, text=True, timeout=60)
            if r.returncode == 0 and r.stdout.strip():
                return sorted(r.stdout.splitlines())
        except (OSError, subprocess.SubprocessError):
            pass
    out = []
    for root, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in ARTIFACT_DIRS]
        for name in files:
            # a git worktree has `.git` as a *file* pointing at the real gitdir
            if name == ".git":
                continue
            out.append(os.path.relpath(os.path.join(root, name), repo).replace("\\", "/"))
    return sorted(out)


def read(repo: str, rel: str) -> str:
    try:
        with open(os.path.join(repo, rel), encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return ""


# ------------------------------------------------------------------- checks
def check_manifest(repo: str, files: list[str], rep: Report) -> None:
    if not os.path.exists(os.path.join(repo, "MANIFEST.json")):
        rep.add("Medium", "MANIFEST", "MANIFEST.json missing")
        return
    try:
        manifest = json.loads(read(repo, "MANIFEST.json"))
    except json.JSONDecodeError as exc:
        rep.add("High", "MANIFEST", f"MANIFEST.json is not valid JSON: {exc}")
        return
    listed = set(manifest.get("files", []))
    actual = set(files)
    for missing in sorted(listed - actual):
        rep.add("High", "MANIFEST", f"listed but not present in tree: {missing}")
    for extra in sorted(actual - listed):
        if extra in ("MANIFEST.json",):
            continue
        rep.add("Medium", "MANIFEST", f"present in tree but not listed: {extra}")
    claimed = manifest.get("benchmark_tests")
    if claimed is not None:
        real = 0
        for name in ("core", "safety", "adaptation", "agents", "memory"):
            p = f"benchmark/{name}/tests.json"
            if p in actual:
                try:
                    data = json.loads(read(repo, p))
                    real += len(data.get("tests", data if isinstance(data, list) else []))
                except json.JSONDecodeError:
                    pass
        if real != claimed:
            rep.add("High", "MANIFEST", f"benchmark_tests={claimed} but {real} cases found")
    if manifest.get("version") and os.path.exists(os.path.join(repo, "VERSION")):
        v = read(repo, "VERSION").strip()
        if v != manifest["version"]:
            rep.add("Medium", "MANIFEST", f"VERSION file '{v}' != MANIFEST version '{manifest['version']}'")


def check_placeholders(repo: str, files: list[str], rep: Report) -> None:
    for rel in files:
        if os.path.splitext(rel)[1].lower() not in TEXT_EXT:
            continue
        if META_DOC_RE.search(rel.replace("\\", "/")):
            continue  # changelogs/roadmaps quote the placeholders they are closing
        body = read(repo, rel)
        if rel.endswith(".json"):
            body = _strip_json_prose(body)
        for pattern, label in PLACEHOLDER_PATTERNS:
            for m in re.finditer(pattern, body):
                snippet = body[max(0, m.start() - 30):m.end() + 30].replace("\n", " ")
                rep.add("High" if "example." in m.group(0) or "[OWNER]" in m.group(0) else "Medium",
                        "PLACEHOLDER", f"{label}: ...{snippet.strip()}...", rel)
                break


def _report_schemas(files: list[str]) -> list[str]:
    found = [f for f in files if re.match(r"protocol/aeil-report\.schema(\.v[\d.]+)?\.json$", f)]

    def rank(rel: str) -> tuple:
        m = re.search(r"\.v(\d+)\.(\d+)", rel)
        return tuple(int(x) for x in m.groups()) if m else (1, 0)

    return sorted(found, key=rank)


def check_schemas(repo: str, files: list[str], rep: Report) -> None:
    all_report_schemas = _report_schemas(files)
    newest = all_report_schemas[-1] if all_report_schemas else None
    schema_rel = newest or "protocol/aeil-report.schema.json"
    path = os.path.join(repo, schema_rel)
    if not os.path.exists(path):
        rep.add("Medium", "SCHEMA", "no report schema found", schema_rel)
        return
    superseded = [s for s in all_report_schemas if s != newest]
    try:
        schema = json.loads(read(repo, schema_rel))
    except json.JSONDecodeError as exc:
        rep.add("High", "SCHEMA", f"invalid JSON: {exc}", schema_rel)
        return
    # when a newer report schema exists, defects of the older one are informational
    legacy = bool(superseded) and schema_rel != "protocol/aeil-report.schema.json"
    sid = schema.get("$id", "")
    if "example.org" in sid or not sid:
        rep.add("Low" if legacy else "High", "SCHEMA", f"$id is a placeholder/absent: '{sid}' - external $ref cannot resolve",
                schema_rel)
    pattern = schema.get("properties", {}).get("version", {}).get("pattern", "")
    if pattern and re.search(r"\\\.\d", pattern) and pattern.startswith("^1\\.0"):
        rep.add("Low" if legacy else "High", "SCHEMA",
                f"version pattern '{pattern}' is pinned to 1.0.x and would reject the project's own "
                "next minor release (SPECIFICATION.md section 13)", schema_rel)
    for obj in ("score", "severity"):
        if schema.get("properties", {}).get(obj, {}).get("additionalProperties") is not False:
            rep.add("Info" if legacy else "Low", "SCHEMA", f"'{obj}' allows additionalProperties - typos pass validation silently",
                    schema_rel)
    required_top = set(schema.get("required", []))
    for want, why in [("gates", "SCORING.md section 3 needs an enforceable gate"),
                      ("benchmark_version", "BENCHMARK.md: benchmark is versioned separately")]:
        if want not in required_top and want not in schema.get("properties", {}):
            rep.add("Info" if legacy else "Medium", "SCHEMA", f"'{want}' absent from report schema - {why}", schema_rel)
    audit_props = schema.get("properties", {}).get("audit", {}).get("properties", {})
    if "evaluator_type" not in audit_props:
        rep.add("Info" if legacy else "Medium", "SCHEMA",
                "'audit.evaluator_type' absent though SCORING.md sections 7-8 require identifying and "
                "calibrating evaluators", schema_rel)
    for old in superseded:
        rep.add("Info", "SCHEMA",
                f"kept for backward compatibility; superseded by {schema_rel}", old)

    if not os.path.exists(os.path.join(repo, "protocol", "aeil-test.schema.json")):
        rep.add("Medium", "SCHEMA",
                "no protocol/aeil-test.schema.json - CONTRIBUTING.md requires 8 fields per test but "
                "nothing validates them")


def check_licences(repo: str, files: list[str], rep: Report) -> None:
    root_licence = [f for f in files if os.path.dirname(f) == "" and f.upper().startswith("LICENSE")]
    if not root_licence:
        rep.add("High", "LICENCE",
                "no licence file at repository root - GitHub reports 'license: null' and adopters get no "
                "machine-readable grant")
    for rel in files:
        if re.search(r"LICENSES?/(Apache-2\.0|CC-BY-4\.0)\.txt$", rel):
            lines = len(read(repo, rel).strip().splitlines())
            if lines < MIN_FULL_LICENCE_LINES:
                rep.add("High", "LICENCE",
                        f"{lines}-line stub instead of the full licence text (Apache-2.0 section 4(a) "
                        "requires distributing the licence text)", rel)
    reserved, permissive = [], []
    scoped_words = re.compile(r"this folder|this directory|demo/|except|does not affect|"
                              r"elsewhere in this repository|for the contents of", re.I)
    for rel in files:
        if os.path.splitext(rel)[1].lower() not in {".html", ".md", ""}:
            continue
        if META_DOC_RE.search(rel.replace("\\", "/")):
            continue  # roadmaps/changelogs quote the reservations they are resolving
        body = read(repo, rel)
        claim = re.search(r"All rights reserved|without written permission .*prohibited|"
                          r"will be prosecuted", body, re.I)
        if claim:
            # A reservation explicitly scoped to one folder is the *fix*, not the defect - but the
            # scoping language must sit next to the claim, not merely somewhere in the file.
            window = body[max(0, claim.start() - 300):claim.end() + 300]
            if not scoped_words.search(window):
                reserved.append(rel)
        if re.search(r"Commercial use is intentionally permitted|CC[- ]BY[- ]4\.0", body):
            permissive.append(rel)
    if reserved and permissive:
        rep.add("Critical", "LICENCE",
                "contradictory licence statements in the same repository: "
                f"all-rights-reserved in {reserved[:3]} vs permissive/commercial-allowed in "
                f"{permissive[:3]}. Must be legally separated (open specification vs proprietary demo).")


def check_benchmarks(repo: str, files: list[str], rep: Report) -> None:
    per_dim = defaultdict(list)
    total = 0
    multi = 0
    field_missing = defaultdict(int)
    bad_sev = []
    suite_files = [f for f in files if re.match(r"benchmark/[^/]+/tests\.json$", f)]
    for rel in suite_files:
        try:
            data = json.loads(read(repo, rel))
        except json.JSONDecodeError as exc:
            rep.add("High", "BENCH", f"invalid JSON: {exc}", rel)
            continue
        tests = data.get("tests", data if isinstance(data, list) else [])
        declared = data.get("count")
        if declared is not None and declared != len(tests):
            rep.add("Medium", "BENCH", f"count={declared} but {len(tests)} tests present", rel)
        for t in tests:
            total += 1
            for field in REQUIRED_TEST_FIELDS:
                if field not in t:
                    field_missing[field] += 1
            if t.get("turns"):
                multi += 1
            dims = t.get("dimensions") or ([t["category"]] if t.get("category") in WEIGHTS else [])
            for d in dims:
                per_dim[d].append(t.get("test_id"))
            if t.get("default_severity_if_failed") not in SEVERITIES_OK:
                bad_sev.append(t.get("test_id"))
    for field, n in field_missing.items():
        rep.add("High", "BENCH", f"{n} test(s) missing required field '{field}'")
    if bad_sev:
        rep.add("Medium", "BENCH", f"invalid default_severity_if_failed in {bad_sev[:5]}")
    for d, weight in WEIGHTS.items():
        n = len(per_dim.get(d, []))
        if n and n < 8:
            rep.add("High", "BENCH",
                    f"dimension {d} carries weight {weight}% but has only {n} case(s) - below the "
                    "proposed minimum of 8; SCORING.md section 5 statistics are not meaningful")
    if total and multi == 0:
        rep.add("High", "BENCH",
                f"0 of {total} cases are multi-turn, yet BENCHMARK.md and audits/MODEL_AUDIT.md Phase 3 "
                "describe adaptation tests as multi-turn")
        for doc in ("BENCHMARK.md", "audits/MODEL_AUDIT.md"):
            if "multi-turn" in read(repo, doc).lower():
                rep.add("Medium", "BENCH", f"claims multi-turn testing that the data cannot support", doc)


def check_structure(repo: str, files: list[str], rep: Report) -> None:
    by_base = defaultdict(list)
    for rel in files:
        by_base[os.path.basename(rel).lower()].append(rel)

    # Collect *bare* (path-less) references made by documentation, e.g. `CERTIFICATION.md`.
    # A bare reference resolves unambiguously when the referring document has a sibling of the
    # same name; it is only ambiguous when no such sibling exists and several candidates live
    # elsewhere in the tree.
    lowered = {f.lower() for f in files}
    bare_refs = defaultdict(set)
    for rel in files:
        if os.path.splitext(rel)[1].lower() != ".md":
            continue
        base_self = os.path.basename(rel).lower()
        own_dir = os.path.dirname(rel)
        for m in re.finditer(r"(?<![\w./-])([A-Za-z0-9_.-]+\.md)(?![\w./-])", read(repo, rel)):
            target = m.group(1).lower()
            if target == base_self:
                continue
            if os.path.join(own_dir, target).replace("\\", "/").lower() in lowered:
                continue  # resolves to a sibling - unambiguous
            bare_refs[target].add(rel)

    # suite files legitimately share a basename (benchmark/<suite>/tests.json)
    suite_re = re.compile(r"^benchmark/[^/]+/tests\.json$")
    for base, paths in by_base.items():
        if len(paths) < 2 or all(suite_re.match(p) for p in paths):
            continue
        contents = {p: read(repo, p) for p in paths}
        if len(set(contents.values())) < 2:
            continue
        referring = sorted(bare_refs.get(base, []))
        if referring:
            rep.add("Medium", "STRUCT",
                    f"{len(paths)} different files named '{base}' ({paths}) and the name is "
                    f"referenced without a path from {referring[:3]} - the reference is ambiguous")
        else:
            rep.add("Low", "STRUCT",
                    f"{len(paths)} different files share the basename '{base}' ({paths}) - "
                    "always cite them with a full path")
    for rel in files:
        stem, ext = os.path.splitext(rel)
        size = os.path.getsize(os.path.join(repo, rel))
        if not ext and size > 20_000:
            head = read(repo, rel)[:200].lower()
            kind = "HTML" if head.lstrip().startswith("<!doctype html") or "<html" in head else "unknown"
            rep.add("Medium", "STRUCT",
                    f"{size/1024:.0f} KB extension-less {kind} file - not rendered by GitHub, not "
                    "referenced in MANIFEST; give it a real path and extension", rel)


def check_demo(repo: str, files: list[str], rep: Report) -> None:
    html_files = [f for f in files if os.path.splitext(f)[1].lower() in (".html", "") and
                  os.path.getsize(os.path.join(repo, f)) > 20_000]
    for rel in html_files:
        body = read(repo, rel)
        if "<html" not in body.lower():
            continue
        # a sibling README carrying the regulatory + non-normative notice mitigates,
        # but does not remove, the need for an inline banner
        sibling = os.path.join(os.path.dirname(rel), "README.md")
        disclaimer = read(repo, sibling) if os.path.exists(os.path.join(repo, sibling)) else ""
        has_notice = bool(re.search(r"(Art\.?|Article)\s*5\s*\(1\)\s*\(f\)|EU AI Act|AI Act|"
                                    r"prohibited AI practice", disclaimer, re.I))
        has_nonnorm = bool(re.search(r"non-normative", disclaimer + body, re.I))
        rnd = len(re.findall(r"Math\.random\s*\(", body))
        shimmed = bool(re.search(r"Math\.random\s*=", body)) or "deterministic-prng" in body
        if rnd and not shimmed:
            rep.add("High", "DEMO",
                    f"{rnd} Math.random() call(s) used to generate values shown as 'confidence' - "
                    "contradicts PRINCIPLES P3/P10 (uncertainty must be real and reproducible)", rel)
        elif rnd and shimmed:
            rep.add("Info", "DEMO",
                    f"{rnd} Math.random() call(s) remain but a deterministic override is installed; "
                    "label the displayed values as synthetic simulation output", rel)
        combined = body.lower()
        if not any(k in combined for k in ("eu ai act", "ai act", "gdpr", "article 5")) and not has_notice:
            if re.search(r"workplace|team .*emotional|learner|education|employee", combined):
                rep.add("Medium" if has_notice else "Critical", "DEMO",
                        "presents workplace/education emotion inference"
                        + (" with only a folder-level notice - add an inline banner"
                           if has_notice else " with no regulatory notice")
                        + ". EU AI Act Art. 5(1)(f) prohibits inferring emotions in the workplace and "
                          "in education institutions (applicable since 2025-02-02, medical/safety "
                          "exception only)", rel)
        if not has_nonnorm:
            rep.add("Low", "DEMO",
                    "not marked non-normative; SPECIFICATION.md should be named as the authoritative "
                    "source to avoid a second, conflicting methodology", rel)


def check_methodology_conflicts(repo: str, files: list[str], rep: Report) -> None:
    stages = defaultdict(set)
    for rel in files:
        if os.path.splitext(rel)[1].lower() not in {".html", ".md", ""}:
            continue
        if META_DOC_RE.search(rel.replace("\\", "/")):
            continue
        body = read(repo, rel)
        for m in re.finditer(r"(\d{1,2})[\s-]*(?:stage|этап)", body, re.I):
            stages[int(m.group(1))].add(rel)
        for m in re.finditer(r"(?:Pipeline|Core Engine)[^\n]{0,40}?(\d{1,2})\s*stage", body, re.I):
            stages[int(m.group(1))].add(rel)
    if len(stages) > 1:
        involved = sorted({f for v in stages.values() for f in v})
        marked = all(
            re.search(r"non-normative", read(repo, os.path.join(os.path.dirname(f), "README.md")), re.I)
            for f in involved
            if os.path.exists(os.path.join(repo, os.path.dirname(f), "README.md")))
        detail = "; ".join(f"{n}-stage in {sorted(v)[:2]}" for n, v in sorted(stages.items()))
        rep.add("Low" if marked else "High", "DOCTRINE",
                f"conflicting pipeline definitions in one repository: {detail}. Declare a single "
                "normative source (SPECIFICATION.md) or mark the others non-normative"
                + (" (all occurrences are inside a folder already marked non-normative)" if marked else ""))


def check_governance(repo: str, files: list[str], rep: Report) -> None:
    if not os.path.isdir(os.path.join(repo, ".github")):
        rep.add("Medium", "GOV", "no .github/ - no CI, no issue/PR templates, no CODEOWNERS")
    try:
        if not os.path.isdir(os.path.join(repo, ".git")):
            raise subprocess.SubprocessError("not a git checkout")
        tags = subprocess.run(["git", "-C", repo, "tag"], capture_output=True, text=True,
                              timeout=20).stdout.split()
        if not tags:
            rep.add("Medium", "GOV", "no git tags - no immutable release to cite "
                                     "(SPECIFICATION.md section 13 requires results to state an exact version)")
    except (OSError, subprocess.SubprocessError):
        pass  # no git metadata available (e.g. exported tree) - skip the tag check
    if not any(f.startswith("docs/adr") for f in files):
        rep.add("Low", "GOV", "GOVERNANCE.md defines a change process but there is no docs/adr/ to record decisions")
    sec = read(repo, "SECURITY.md").lower()
    if sec and not re.search(r"@|mailto:|private vulnerability reporting", sec):
        rep.add("Medium", "GOV", "SECURITY.md asks for private reports but names no channel or address",
                "SECURITY.md")
    for want in ("ROADMAP.md", "CODE_OF_CONDUCT.md"):
        if want not in files:
            rep.add("Low", "GOV", f"{want} absent")
    body = read(repo, "SAFETY.md") + read(repo, "SPECIFICATION.md") + read(repo, "RESPONSIBLE_USE.md")
    if not re.search(r"EU AI Act|GDPR|employment|credit|insurance", body):
        rep.add("High", "GOV",
                "no prohibited-use domains and no regulatory references anywhere in the normative "
                "documents - a responsible-use policy is required (see RESPONSIBLE_USE.md proposal)")


CHECKS = [check_manifest, check_placeholders, check_schemas, check_licences,
          check_benchmarks, check_structure, check_demo, check_methodology_conflicts,
          check_governance]


def main() -> int:
    ap = argparse.ArgumentParser(description="AEIL repository consistency checker")
    ap.add_argument("--repo", default=".")
    ap.add_argument("--json", help="also write findings as JSON")
    args = ap.parse_args()

    repo = os.path.abspath(args.repo)
    if not os.path.isdir(repo):
        print(f"not a directory: {repo}")
        return 2
    files = tracked_files(repo)
    print(f"AEIL repo validation - {repo}\nfiles: {len(files)}")

    rep = Report()
    for check in CHECKS:
        try:
            check(repo, files, rep)
        except Exception as exc:  # noqa: BLE001 - a broken check must not hide the others
            rep.add("Info", "TOOL", f"{check.__name__} raised {type(exc).__name__}: {exc}")
    rep.emit()

    if args.json:
        parent = os.path.dirname(os.path.abspath(args.json))
        os.makedirs(parent, exist_ok=True)
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(rep.findings, fh, ensure_ascii=False, indent=2)
        print(f"wrote {args.json}")
    blocking = [f for f in rep.findings if f["severity"] in ("Critical", "High")]
    return 1 if blocking else 0


if __name__ == "__main__":
    sys.exit(main())
