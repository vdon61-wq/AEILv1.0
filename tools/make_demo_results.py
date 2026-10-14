#!/usr/bin/env python3
"""Generates a synthetic v1.0 results file so the reference scorer can be
demonstrated against the *existing* 60-case benchmark (backward-compatibility check).

Usage: python3 tools/make_demo_results.py <repo_with_benchmark> <out.json>
"""
import json
import os
import sys

SUITES = ["core", "safety", "adaptation", "agents", "memory"]


def main() -> int:
    repo, out = sys.argv[1], sys.argv[2]
    ids = []
    for s in SUITES:
        p = os.path.join(repo, "benchmark", s, "tests.json")
        if not os.path.exists(p):
            continue
        data = json.load(open(p, encoding="utf-8"))
        ids += [(t["test_id"], t.get("default_severity_if_failed", "Medium"))
                for t in data.get("tests", [])]

    results = []
    for i, (tid, sev) in enumerate(ids):
        sc = 4 if i % 7 else (3 if i % 3 else 2)
        if tid.endswith("G01"):      # agent acts on emotional urgency -> Critical
            sc = 0
        elif tid.endswith("S01"):
            sc = 1
        elif tid.endswith("C01"):
            sc = 2
        failed = sc < 2
        results.append({
            "test_id": tid,
            "score": sc,
            "severity": sev if failed else ("Medium" if sc == 2 else "None"),
            "runs": [{"run_index": k + 1,
                      "score": max(0, min(4, sc + (-1 if k == 2 and sc > 0 else 0)))}
                     for k in range(3)],
            "notes": "synthetic demo - not a real evaluation",
        })

    payload = {
        "audit_id": "demo-v1compat-001",
        "audit_type": "model",
        "date": "2026-10-14T10:00:00Z",
        "evaluator_type": "human",
        "system": {"name": "LegacySystem", "version": "2.3"},
        "benchmark_version": "1.0.0",
        "aeil_version": "1.0.0",
        "results": results,
    }
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
    print(f"wrote {out}: {len(results)} results")
    return 0


if __name__ == "__main__":
    sys.exit(main())
