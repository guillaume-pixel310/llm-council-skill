#!/usr/bin/env python3
"""
Eval runner for the llm-council skill (v2 — MetaGPT role-based architecture).

Usage:
  python3 scripts/run_evals.py                     # run all cases
  python3 scripts/run_evals.py --category trigger-recognition
  python3 scripts/run_evals.py --id trigger-01
  python3 scripts/run_evals.py --benchmark 5       # run N times, report variance

Each case exercises query_llms.py directly and validates:
  1. Script exits cleanly (or with expected error)
  2. JSON output has the required keys: prompt, council, messages
  3. council.productmanager.response and council.architect.response are non-empty
  4. messages list has the expected roles in sequence
"""

import json
import os
import sys
import argparse
import statistics
import time
from pathlib import Path
from typing import Optional

EVALS_FILE = Path(__file__).parent.parent / "evals" / "eval_prompts.json"
QUERY_SCRIPT = Path(__file__).parent / "query_llms.py"


def load_cases(category: Optional[str] = None, case_id: Optional[str] = None):
    with open(EVALS_FILE) as f:
        data = json.load(f)
    cases = data["cases"]
    if category:
        cases = [c for c in cases if c["category"] == category]
    if case_id:
        cases = [c for c in cases if c["id"] == case_id]
    return cases


def run_case(case: dict, env_override: Optional[dict] = None) -> dict:
    """Run query_llms.py for a single eval case. Returns a result dict."""
    import subprocess

    env = os.environ.copy()
    if env_override:
        env.update(env_override)

    simulated_error = case.get("simulated_error", "")
    if "OPENAI_API_KEY not set" in simulated_error:
        env.pop("OPENAI_API_KEY", None)
    elif "Both API keys missing" in simulated_error:
        env.pop("OPENAI_API_KEY", None)
        env.pop("GEMINI_API_KEY", None)

    start = time.monotonic()
    proc = subprocess.run(
        [sys.executable, str(QUERY_SCRIPT), case["prompt"]],
        capture_output=True,
        text=True,
        timeout=90,
        env=env,
    )
    elapsed = time.monotonic() - start

    result = {
        "id": case["id"],
        "elapsed_s": round(elapsed, 2),
        "returncode": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
        "checks": [],
        "passed": False,
    }

    # Parse JSON output
    try:
        output = json.loads(proc.stdout)
    except json.JSONDecodeError:
        result["checks"].append({"name": "json-parseable", "passed": False, "note": "stdout is not valid JSON"})
        return result

    result["checks"].append({"name": "json-parseable", "passed": True})

    # Required top-level keys
    for key in ("prompt", "council", "messages"):
        present = key in output
        result["checks"].append({"name": f"key-{key}", "passed": present})

    # council must be a dict with both role keys
    council = output.get("council") or {}
    for role_key in ("productmanager", "architect"):
        present = role_key in council
        result["checks"].append({"name": f"council-role-{role_key}", "passed": present})

    # Each role must have a non-empty response
    for role_key in ("productmanager", "architect"):
        role_data = council.get(role_key)
        if isinstance(role_data, dict):
            has_response = bool(role_data.get("response"))
            result["checks"].append({"name": f"{role_key}-response-present", "passed": has_response})
            has_source = bool(role_data.get("source"))
            result["checks"].append({"name": f"{role_key}-source-tracked", "passed": has_source})

    # messages list must contain at least 3 entries (User + PM + Architect)
    messages = output.get("messages", [])
    result["checks"].append({"name": "messages-min-length", "passed": len(messages) >= 3})

    # messages must appear in correct role sequence
    if len(messages) >= 3:
        roles_in_order = [m.get("role") for m in messages[:3]]
        expected = ["User", "ProductManager", "Architect"]
        result["checks"].append({
            "name": "messages-role-sequence",
            "passed": roles_in_order == expected,
            "note": f"got {roles_in_order}" if roles_in_order != expected else "",
        })

    result["parsed_output"] = output
    result["passed"] = all(c["passed"] for c in result["checks"])
    return result


def print_result(result: dict, verbose: bool = False):
    status = "PASS" if result["passed"] else "FAIL"
    print(f"  [{status}] {result['id']}  ({result['elapsed_s']}s)")
    if not result["passed"] or verbose:
        for check in result["checks"]:
            mark = "+" if check["passed"] else "x"
            note = f"  — {check.get('note', '')}" if check.get("note") else ""
            print(f"         {mark} {check['name']}{note}")


def run_benchmark(cases: list, runs: int):
    """Run each case N times and report timing variance."""
    print(f"\nBenchmark: {runs} runs per case\n")
    for case in cases:
        times = []
        pass_count = 0
        for i in range(runs):
            try:
                result = run_case(case)
                times.append(result["elapsed_s"])
                if result["passed"]:
                    pass_count += 1
            except Exception as e:
                print(f"  Error on run {i+1} for {case['id']}: {e}")

        if times:
            mean = statistics.mean(times)
            stdev = statistics.stdev(times) if len(times) > 1 else 0.0
            print(
                f"  {case['id']}: pass={pass_count}/{runs}  "
                f"mean={mean:.2f}s  stdev={stdev:.2f}s  "
                f"min={min(times):.2f}s  max={max(times):.2f}s"
            )
        else:
            print(f"  {case['id']}: all runs failed")


def main():
    parser = argparse.ArgumentParser(description="Run llm-council skill evals")
    parser.add_argument("--category", help="Filter by category")
    parser.add_argument("--id", dest="case_id", help="Run a single case by ID")
    parser.add_argument("--benchmark", type=int, metavar="N", help="Benchmark: run N times per case")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    cases = load_cases(category=args.category, case_id=args.case_id)
    if not cases:
        print("No matching eval cases found.")
        sys.exit(1)

    # Skip cases that test the skill-layer trigger logic (require a live Claude session)
    runnable = [c for c in cases if c.get("should_trigger", True)]
    skipped = [c for c in cases if not c.get("should_trigger", True)]

    if skipped:
        print(f"Skipping {len(skipped)} no-trigger case(s) (require skill-layer testing, not script-level):")
        for c in skipped:
            print(f"  - {c['id']}: {c['prompt'][:60]}")
        print()

    if args.benchmark:
        run_benchmark(runnable, args.benchmark)
        return

    print(f"Running {len(runnable)} eval case(s)...\n")
    passed = 0
    failed = 0
    for case in runnable:
        try:
            result = run_case(case)
            print_result(result, verbose=args.verbose)
            if result["passed"]:
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  [ERROR] {case['id']}: {e}")
            failed += 1

    print(f"\nResults: {passed} passed, {failed} failed out of {len(runnable)} cases")
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
