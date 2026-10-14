#!/usr/bin/env python3
"""Schema regression tests for AEIL v1.1 (proposal for tools/test_schemas.py).

Why this file exists: the first draft of `aeil-report.schema.v1.1.json` contained
*vacuous if-clauses*. In JSON Schema, `if: {properties: {x: {...}}}` is satisfied when `x`
is ABSENT - properties constrains only present keys. The result: a model-only report with no
`aeil_m` was rejected for missing `aeil_m_components`, and any report lacking
`evaluator_type` was rejected for missing `judge_model`. Both are legal v1.1 reports.

Every conditional in every AEIL schema now carries an explicit `required` guard, and these
tests pin the behaviour. CI runs this file on every push.

Usage: python3 tools/test_schemas.py [repo_root]     (default: repository root)
Exit:  0 all pass, 1 any failure.
"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(HERE)


def load(*parts: str):
    with open(os.path.join(REPO, *parts), encoding="utf-8") as fh:
        return json.load(fh)


def registry():
    from referencing import Registry, Resource
    res = []
    proto = os.path.join(REPO, "protocol")
    for fn in sorted(os.listdir(proto)):
        if fn.endswith(".json") and "schema" in fn:
            doc = load("protocol", fn)
            if "$id" in doc:
                res.append((doc["$id"], Resource.from_contents(doc)))
            res.append((fn, Resource.from_contents(doc)))
    return Registry().with_resources(res)


def base_report(**kw):
    d = {
        "standard": "AEIL", "version": "1.1.0", "benchmark_version": "1.1.0",
        "audit": {"audit_id": "t1", "type": "model",
                  "date": "2026-10-14T00:00:00Z", "evaluator_type": "human"},
        "system": {"name": "S", "version": "1"},
        "benchmark": {"name": "AEIL Benchmark", "version": "1.1.0"},
        "score": {"overall": 80, "context_recognition": 80, "interpretation": 80,
                  "response_appropriateness": 80, "safety_boundaries": 80,
                  "adaptation": 80, "transparency": 80},
        "severity": {"critical": 0, "high": 0, "medium": 0, "low": 0},
        "gates": {"critical_findings": {"passed": True, "rule": "severity.critical == 0"},
                  "aup": {"passed": True}},
        "overall_status": "conformant",
        "tests": [{"test_id": "AEIL-C01", "score": 4}],
    }
    d.update(kw)
    return d


GATE_OK = {"critical_findings": {"passed": True, "rule": "severity.critical == 0"},
           "aup": {"passed": True}}
GATE_CRIT_FAIL = {"critical_findings": {"passed": False, "rule": "severity.critical == 0"},
                  "aup": {"passed": True}}
GATE_AUP_FAIL = {"critical_findings": {"passed": True, "rule": "severity.critical == 0"},
                 "aup": {"passed": False}}
CRIT = {"critical": 1, "high": 0, "medium": 0, "low": 0}
CLEAN = {"critical": 0, "high": 0, "medium": 0, "low": 0}
M_COMPONENTS = {"emotional_memory_recall": 70, "emotional_state_update": 70,
                "behavioral_adaptation": 70, "state_consistency": 70}


def report_cases():
    S = base_report()["score"]
    A = base_report()["audit"]
    return [
        # --- vacuous-if regressions (the bug class this file exists for) ---
        ("model-only report without aeil_m is valid", base_report(), True),
        ("aeil_m null (memory suite not run) is valid",
         base_report(score={**S, "aeil_m": None}), True),
        ("human evaluator without judge_model is valid", base_report(), True),
        # --- aeil_m coupling ---
        ("aeil_m published WITHOUT components is invalid",
         base_report(score={**S, "aeil_m": 70}), False),
        ("aeil_m published WITH components is valid",
         base_report(score={**S, "aeil_m": 70, "aeil_m_components": M_COMPONENTS}), True),
        # --- llm judge identification ---
        ("llm_judge without judge_model is invalid",
         base_report(audit={**A, "evaluator_type": "llm_judge"}), False),
        ("llm_judge with judge_model+rubric is valid",
         base_report(audit={**A, "evaluator_type": "llm_judge",
                            "judge_model": "j", "judge_rubric_version": "1"}), True),
        # --- gate/status coupling (SCORING.md s.3, P11) ---
        ("critical finding with status=conformant is invalid (gate bypass)",
         base_report(severity=CRIT, gates=GATE_CRIT_FAIL,
                     overall_status="conformant"), False),
        ("critical finding with status=gated is valid",
         base_report(severity=CRIT, gates=GATE_CRIT_FAIL, overall_status="gated"), True),
        ("aup failure with status=conformant is invalid",
         base_report(gates=GATE_AUP_FAIL, overall_status="conformant"), False),
        ("aup failure with status=not_conformant is valid",
         base_report(gates=GATE_AUP_FAIL, overall_status="not_conformant"), True),
        # --- basic hygiene ---
        ("missing gates is invalid", {k: v for k, v in base_report().items()
                                      if k != "gates"}, False),
        ("score out of range is invalid",
         base_report(score={**S, "overall": 140}), False),
        ("test score 5 is invalid",
         base_report(tests=[{"test_id": "X", "score": 5}]), False),
        ("fractional test score from averaged runs is valid",
         base_report(tests=[{"test_id": "X", "score": 3.67,
                             "runs": [{"run_index": 1, "score": 4},
                                      {"run_index": 2, "score": 3},
                                      {"run_index": 3, "score": 4}]}]), True),
    ]


def example_files():
    """Each shipped example must validate against the schema of its OWN version."""
    out = []
    exdir = os.path.join(REPO, "protocol", "examples")
    if not os.path.isdir(exdir):
        return out
    for fn in sorted(os.listdir(exdir)):
        if not fn.endswith(".json"):
            continue
        doc = load("protocol", "examples", fn)
        mm = ".".join(str(doc.get("version", "")).split(".")[:2])
        schema_fn = (f"aeil-report.schema.v{mm}.json"
                     if os.path.exists(os.path.join(REPO, "protocol",
                                                    f"aeil-report.schema.v{mm}.json"))
                     else "aeil-report.schema.json")
        out.append((f"examples/{fn} vs {schema_fn}", doc, schema_fn))
    return out


def main() -> int:
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        print("jsonschema not installed: pip install jsonschema")
        return 2

    reg = registry()
    v11 = Draft202012Validator(load("protocol", "aeil-report.schema.v1.1.json"), registry=reg)
    Draft202012Validator.check_schema(load("protocol", "aeil-report.schema.v1.1.json"))
    Draft202012Validator.check_schema(load("protocol", "aeil-report.schema.json"))
    Draft202012Validator.check_schema(load("protocol", "aeil-test.schema.json"))
    Draft202012Validator.check_schema(load("protocol", "aeil-emotional-event.schema.json"))
    Draft202012Validator.check_schema(load("protocol", "aeil-policy.schema.json"))
    print("all five schemas are valid draft 2020-12 schemas")

    failures = 0
    print("\nreport-schema regression cases:")
    for name, doc, want in report_cases():
        errs = list(v11.iter_errors(doc))
        got = not errs
        ok = got == want
        failures += 0 if ok else 1
        mark = "PASS" if ok else "FAIL"
        extra = f"  first error: {errs[0].message[:70]}" if errs and not ok else ""
        print(f"  {mark}  {name} (valid={got}, expected={want}){extra}")

    print("\nshipped examples:")
    for name, doc, schema_fn in example_files():
        validator = Draft202012Validator(load("protocol", schema_fn), registry=reg)
        errs = list(validator.iter_errors(doc))
        ok = not errs
        failures += 0 if ok else 1
        print(f"  {'PASS' if ok else 'FAIL'}  {name}"
              + (f"  first error: {errs[0].message[:70]}" if errs else ""))

    print(f"\n{'ALL PASS' if failures == 0 else str(failures) + ' FAILURES'}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
