#!/usr/bin/env python3
"""Validate the live-case file and freeze/verify the holdout subset.

Standard library only. Python 3.10+.

Usage (from the skill root, after the harness is installed at tests/live/):
    python -B tests/live/check_cases.py --cases tests/live/cases.json
    python -B tests/live/check_cases.py --freeze
    python -B tests/live/check_cases.py --verify-holdout

Exit codes: 0 valid, 1 invalid or mismatched, 2 bad invocation.

This script checks the shape of the case file. It does not run the cases,
score transcripts, or claim that any evaluation happened.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

EXPECTED_CASES = 14
EXPECTED_HOLDOUT = 4
REQUIRED_CASE_KEYS = (
    "id",
    "source_ac",
    "title",
    "holdout",
    "persona",
    "material",
    "turns",
    "expect",
    "notes",
)
REQUIRED_PERSONA_KEYS = ("level", "goal", "constraints")
MIN_TURNS, MAX_TURNS = 3, 5
MIN_ASSERTIONS, MAX_ASSERTIONS = 3, 5


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def canonical_holdout(cases: list[dict]) -> bytes:
    """Stable byte form of the holdout subset, independent of key order."""
    subset = [case for case in cases if case.get("holdout") is True]
    return json.dumps(
        subset, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def validate(doc: object) -> tuple[list[dict], list[str]]:
    errors: list[str] = []
    if not isinstance(doc, dict):
        return [], ["top level must be an object"]
    if doc.get("version") != 1:
        fail(errors, f"version must be 1, found {doc.get('version')!r}")

    cases = doc.get("cases")
    if not isinstance(cases, list):
        return [], ["cases must be a list"]
    if len(cases) != EXPECTED_CASES:
        fail(errors, f"expected {EXPECTED_CASES} cases, found {len(cases)}")

    seen: set[str] = set()
    for index, case in enumerate(cases):
        label = f"cases[{index}]"
        if not isinstance(case, dict):
            fail(errors, f"{label} must be an object")
            continue

        missing = [key for key in REQUIRED_CASE_KEYS if key not in case]
        if missing:
            fail(errors, f"{label} missing keys: {', '.join(missing)}")
            continue

        case_id = case["id"]
        if not isinstance(case_id, str) or not case_id:
            fail(errors, f"{label}.id must be a non-empty string")
        elif case_id in seen:
            fail(errors, f"duplicate id {case_id}")
        else:
            seen.add(case_id)

        if not isinstance(case["holdout"], bool):
            fail(errors, f"{case_id}.holdout must be a boolean")
        for key in ("source_ac", "title", "material", "notes"):
            if not isinstance(case[key], str) or not case[key].strip():
                fail(errors, f"{case_id}.{key} must be a non-empty string")

        persona = case["persona"]
        if not isinstance(persona, dict):
            fail(errors, f"{case_id}.persona must be an object")
        else:
            for key in REQUIRED_PERSONA_KEYS:
                value = persona.get(key)
                if not isinstance(value, str) or not value.strip():
                    fail(errors, f"{case_id}.persona.{key} must be a non-empty string")

        turns = case["turns"]
        if not isinstance(turns, list) or not (
            MIN_TURNS <= len(turns) <= MAX_TURNS
        ):
            fail(
                errors,
                f"{case_id}.turns must be a list of {MIN_TURNS}-{MAX_TURNS} messages",
            )
        else:
            for turn_index, turn in enumerate(turns):
                if not isinstance(turn, str) or not turn.strip():
                    fail(errors, f"{case_id}.turns[{turn_index}] must be non-empty text")

        expect = case["expect"]
        if not isinstance(expect, dict):
            fail(errors, f"{case_id}.expect must be an object")
            continue
        for key in ("must", "must_not"):
            items = expect.get(key)
            if not isinstance(items, list) or not (
                MIN_ASSERTIONS <= len(items) <= MAX_ASSERTIONS
            ):
                fail(
                    errors,
                    f"{case_id}.expect.{key} must be a list of "
                    f"{MIN_ASSERTIONS}-{MAX_ASSERTIONS} items",
                )
                continue
            for item_index, item in enumerate(items):
                if not isinstance(item, str) or not item.strip():
                    fail(
                        errors,
                        f"{case_id}.expect.{key}[{item_index}] must be non-empty text",
                    )

    holdout = [case for case in cases if isinstance(case, dict) and case.get("holdout") is True]
    if len(holdout) != EXPECTED_HOLDOUT:
        fail(errors, f"expected {EXPECTED_HOLDOUT} holdout cases, found {len(holdout)}")

    expected_ids = [f"L-{number:02d}" for number in range(1, EXPECTED_CASES + 1)]
    if sorted(seen) != expected_ids:
        missing = sorted(set(expected_ids) - seen)
        extra = sorted(seen - set(expected_ids))
        if missing:
            fail(errors, f"missing ids: {', '.join(missing)}")
        if extra:
            fail(errors, f"unexpected ids: {', '.join(extra)}")

    return cases, errors


def read_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"error: not found: {path}", file=sys.stderr)
        raise SystemExit(2)
    except json.JSONDecodeError as exc:
        print(f"error: invalid JSON in {path}: {exc}", file=sys.stderr)
        raise SystemExit(2)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cases",
        type=Path,
        default=Path(__file__).with_name("cases.json"),
        help="path to cases.json (default: next to this script)",
    )
    parser.add_argument(
        "--holdout-file",
        type=Path,
        default=None,
        help="path to holdout.json (default: next to cases.json)",
    )
    parser.add_argument("--freeze", action="store_true", help="write holdout.json")
    parser.add_argument(
        "--verify-holdout", action="store_true", help="check holdout.json matches cases.json"
    )
    args = parser.parse_args(argv)

    if args.freeze and args.verify_holdout:
        parser.error("choose one of --freeze or --verify-holdout")

    cases_path: Path = args.cases
    holdout_path: Path = args.holdout_file or cases_path.with_name("holdout.json")

    doc = read_json(cases_path)
    cases, errors = validate(doc)
    if errors:
        print(f"INVALID: {cases_path}", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    holdout_ids = [case["id"] for case in cases if case["holdout"]]
    digest = hashlib.sha256(canonical_holdout(cases)).hexdigest()
    manifest = {
        "version": 1,
        "holdout_ids": holdout_ids,
        "holdout_sha256": digest,
        "note": (
            "Freeze at G1. Verify at G4. A mismatch means a holdout case changed "
            "after the freeze; stop and restore it."
        ),
    }

    if args.freeze:
        holdout_path.write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        print(f"froze {len(holdout_ids)} holdout cases -> {holdout_path}")
        print(f"sha256 {digest}")
        return 0

    print(f"OK: {len(cases)} cases, {len(holdout_ids)} holdout ({', '.join(holdout_ids)})")

    if args.verify_holdout:
        if not holdout_path.exists():
            print(f"error: no freeze file at {holdout_path}; run --freeze first", file=sys.stderr)
            return 2
        frozen = read_json(holdout_path)
        problems = []
        if not isinstance(frozen, dict):
            problems.append("holdout.json must be an object")
        else:
            if frozen.get("holdout_ids") != holdout_ids:
                problems.append(
                    f"ids differ: frozen {frozen.get('holdout_ids')!r} vs {holdout_ids!r}"
                )
            if frozen.get("holdout_sha256") != digest:
                problems.append(
                    f"hash differs: frozen {frozen.get('holdout_sha256')!r} vs {digest!r}"
                )
        if problems:
            print("HOLDOUT MISMATCH", file=sys.stderr)
            for problem in problems:
                print(f"  - {problem}", file=sys.stderr)
            return 1
        print(f"holdout verified: {digest}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
