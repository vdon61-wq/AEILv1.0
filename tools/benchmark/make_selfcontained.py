#!/usr/bin/env python3
"""Makes tools/benchmark/ self-contained inside the repository.

1. Inlines the 12 seed AEIL-M cases into memory_cases.py (they previously lived outside the
   repo, in the review workspace), so the whole 40-case suite is regenerable from a bare
   checkout.
2. Rewrites assemble.py to resolve the JSON schemas from the repository it is writing into,
   instead of from the review workspace.
"""
import json
import os
import pprint
import sys

BUILD = os.path.join(os.path.dirname(os.path.abspath(__file__)))
SEED_PATH = os.path.join(os.path.dirname(BUILD), "AEIL_review", "proposals",
                         "benchmark", "memory", "tests.json")


def inline_seeds() -> None:
    with open(SEED_PATH, encoding="utf-8") as fh:
        seeds = json.load(fh)["tests"]
    target = os.path.join(BUILD, "memory_cases.py")
    body = open(target, encoding="utf-8").read()
    if "SEED_MEMORY_CASES" in body:
        print("memory_cases.py already contains SEED_MEMORY_CASES - skipping inline")
        return
    lines = [
        "",
        "",
        "# " + "=" * 74,
        "# The 12 seed AEIL-M cases, inlined so this module is self-contained inside the",
        "# repository and the 40-case suite is regenerable from a bare checkout with no",
        "# dependency on any path outside it. item_hash is recomputed by assemble.py.",
        "# " + "=" * 74,
        "SEED_MEMORY_CASES = [",
    ]
    for c in seeds:
        c = {k: v for k, v in c.items() if k != "item_hash"}
        rendered = pprint.pformat(c, sort_dicts=False, width=96).replace("\n", "\n    ")
        lines.append("    " + rendered + ",")
    lines.append("]")
    with open(target, "a", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"inlined {len(seeds)} seed cases into memory_cases.py")


def patch_assemble() -> None:
    target = os.path.join(BUILD, "assemble.py")
    s = open(target, encoding="utf-8").read()

    old_import = ("from memory_cases import NEW_MEMORY_CASES                 # noqa: E402\n"
                  "\n"
                  "REVIEW_ROOT = os.path.join(os.path.dirname(BUILD), \"AEIL_review\", \"proposals\")\n"
                  "SEED_MEMORY = os.path.join(REVIEW_ROOT, \"benchmark\", \"memory\", \"tests.json\")\n"
                  "SCHEMA_DIR = os.path.join(REVIEW_ROOT, \"protocol\")")
    new_import = ("from memory_cases import NEW_MEMORY_CASES, SEED_MEMORY_CASES  # noqa: E402\n"
                  "\n"
                  "# The assembler lives at tools/benchmark/assemble.py inside the repository, so\n"
                  "# the schemas are two levels up. AEIL_REPO overrides this when the assembler is\n"
                  "# run against a different checkout from the one it lives in.\n"
                  "REPO_ROOT = os.environ.get(\"AEIL_REPO\") or os.path.dirname(os.path.dirname(BUILD))\n"
                  "SCHEMA_DIR = os.path.join(REPO_ROOT, \"protocol\")")
    if old_import not in s:
        print("WARN: import block already patched or not found")
    else:
        s = s.replace(old_import, new_import)

    old_seed = ('    with open(SEED_MEMORY, encoding="utf-8") as fh:\n'
                '        seed = json.load(fh)["tests"]\n'
                '    merged = list(seed) + [dict(c) for c in NEW_MEMORY_CASES]')
    new_seed = '    merged = [dict(c) for c in SEED_MEMORY_CASES] + [dict(c) for c in NEW_MEMORY_CASES]'
    if old_seed not in s:
        print("WARN: seed-loading block already patched or not found")
    else:
        s = s.replace(old_seed, new_seed)

    # validate() must fail loudly rather than silently skip when schemas are absent
    old_v = ('    resources = []\n'
             '    for fn in os.listdir(SCHEMA_DIR):')
    new_v = ('    if not os.path.isdir(SCHEMA_DIR):\n'
             '        raise SystemExit(f"schemas not found at {SCHEMA_DIR}; set AEIL_REPO to the "\n'
             '                         "repository root you are assembling into")\n'
             '    resources = []\n'
             '    for fn in sorted(os.listdir(SCHEMA_DIR)):')
    if old_v in s:
        s = s.replace(old_v, new_v)

    with open(target, "w", encoding="utf-8") as fh:
        fh.write(s)
    print("patched assemble.py: schemas now resolved from the repository")


if __name__ == "__main__":
    inline_seeds()
    patch_assemble()
    sys.exit(0)
