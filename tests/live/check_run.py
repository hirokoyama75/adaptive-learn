"""Derive PASS/FAIL for a judge-annotated live run, mechanically.

This check validates that a judge annotated every `must` and `must_not` item of
one case and that every claimed observation, violation, automatic fail, or
severe violation cites an assistant turn number and a verbatim quote that
appears in that turn of the transcript. It does not judge tutoring quality,
verify tool actions, or measure learning. Nothing is written.

Annotation JSON (version 1, one file per case/run/judge):

    {
      "format": "live-run-annotation",
      "version": 1,
      "case_id": "L-01",
      "run": 1,
      "judge": "independent judge label (never the tutor session)",
      "transcript": "run-1.md",
      "must": [{"index": 0, "observed": true, "turns": [1], "quote": "..."}],
      "must_not": [{"index": 0, "violation": false}],
      "automatic_fails": [{"dimension": "D3", "turns": [1], "quote": "..."}],
      "severe": [{"rule": "...", "turns": [1], "quote": "..."}],
      "dimensions": {"D1": 2, "D6": "N/A"},
      "notes": "..."
    }

Transcripts are markdown with one `## Assistant turn N` or `## Learner turn N`
header per message. Quotes are matched verbatim (whitespace-normalized) against
the cited assistant turns. `transcript` resolves relative to the annotation file.

Usage:

    python -B tests/live/check_run.py --cases tests/live/cases.json \
        --annotation tests/live/fixtures/l08-correction/annotation.json

Exit codes: 0 = PASS, 1 = FAIL, 2 = invalid usage or invalid annotation.
A missing judgment, an unverifiable quote, or a malformed annotation is
INVALID (exit 2) and can never pass.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from check_cases import validate

EXIT_PASS, EXIT_FAIL, EXIT_INVALID = 0, 1, 2
DIMENSIONS = ("D1", "D2", "D3", "D4", "D5", "D6")
FORMAT_NAME = "live-run-annotation"
SECTION_RE = re.compile(r"^##\s*(Assistant|Learner)\s+turn\s+(\d+)\s*$")
ANNOTATION_KEYS = {
    "format", "version", "case_id", "run", "judge", "transcript",
    "must", "must_not", "automatic_fails", "severe", "dimensions", "notes",
}
MUST_KEYS = {"index", "observed", "turns", "quote", "note"}
MUST_NOT_KEYS = {"index", "violation", "turns", "quote", "note"}
AUTOFAIL_KEYS = {"dimension", "turns", "quote", "reason"}
SEVERE_KEYS = {"rule", "turns", "quote"}
SCOPE_NOTE = (
    "note: derived mechanically from judge annotations and quote references; "
    "this check does not judge tutoring or measure learning."
)


class CheckError(ValueError):
    """Invalid usage or invalid annotation; the run cannot pass on this input."""


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise CheckError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"), object_pairs_hook=_pairs)
    except FileNotFoundError:
        raise CheckError(f"file not found: {path}")
    except (OSError, UnicodeError, json.JSONDecodeError, RecursionError) as error:
        raise CheckError(f"malformed JSON in {path}: {error}")


def _normalize(text):
    return " ".join(str(text).split())


def _parse_transcript(text):
    """Return (assistant, learner) turn-numbered section maps."""
    assistant, learner = {}, {}
    current = None
    for line in text.splitlines():
        match = SECTION_RE.match(line.strip())
        if match:
            role, number = match.group(1), int(match.group(2))
            if number < 1:
                raise CheckError("turn numbers start at 1")
            target = assistant if role == "Assistant" else learner
            if number in target:
                raise CheckError(f"duplicate {role} turn {number} in transcript")
            target[number] = []
            current = (target, number)
            continue
        if current is not None:
            current[0][current[1]].append(line)
    return ({key: "\n".join(value) for key, value in assistant.items()},
            {key: "\n".join(value) for key, value in learner.items()})


def _require_quote(entry, label):
    quote = entry.get("quote")
    if not isinstance(quote, str) or not quote.strip():
        raise CheckError(f"{label}: a claimed positive needs a non-empty verbatim quote")
    return quote


def _verify_evidence(assistant, learner, turns, quote, label):
    if not isinstance(turns, list) or not turns:
        raise CheckError(f"{label}: turns must be a non-empty list of integers")
    if not all(type(turn) is int and turn >= 1 for turn in turns):
        raise CheckError(f"{label}: turns must be positive integers")
    normalized_quote = _normalize(quote)
    for turn in turns:
        if turn in assistant:
            if normalized_quote in _normalize(assistant[turn]):
                continue
            if turn in learner and normalized_quote in _normalize(learner[turn]):
                raise CheckError(
                    f"{label}: quote found in learner turn {turn}, not an assistant message"
                )
            raise CheckError(f"{label}: quote not found verbatim in assistant turn {turn}")
        if turn in learner:
            raise CheckError(f"{label}: turn {turn} is a learner turn; evidence must reference assistant messages")
        raise CheckError(f"{label}: turn {turn} does not exist in the transcript")


def _check_items(entries, item_texts, entry_keys, flag_key, case_id, what):
    if not isinstance(entries, list):
        raise CheckError(f"{case_id}: {what} must be a list")
    if len(entries) != len(item_texts):
        raise CheckError(
            f"{case_id}: {len(entries)} of {len(item_texts)} {what} items annotated; "
            f"every item needs a judgment and missing judgments never pass"
        )
    flags = []
    for expected, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise CheckError(f"{case_id}: {what} entries must be objects")
        unknown = set(entry) - entry_keys
        if unknown:
            raise CheckError(f"{case_id}: unknown entry fields in {what} {expected}: {sorted(unknown)}")
        index = entry.get("index")
        if type(index) is not int:
            raise CheckError(f"{case_id}: {what} entries need an integer index")
        if index != expected:
            raise CheckError(
                f"{case_id}: missing judgment for {what} {expected}: entries must cover "
                f"indexes 0..{len(item_texts) - 1} in order; found index {index}"
            )
        flag = entry.get(flag_key)
        if not isinstance(flag, bool):
            raise CheckError(f"{case_id}: {what} {index} needs a boolean {flag_key}")
        flags.append(flag)
    return flags


def check_annotation(annotation_path, cases):
    """Return (verdict, summary, failures) or raise CheckError."""
    annotation = _load_json(annotation_path)
    if not isinstance(annotation, dict):
        raise CheckError("annotation must be a JSON object")
    unknown = set(annotation) - ANNOTATION_KEYS
    if unknown:
        raise CheckError(f"unknown annotation fields: {sorted(unknown)}")
    if annotation.get("format") != FORMAT_NAME:
        raise CheckError(f"annotation format must be {FORMAT_NAME!r}")
    if type(annotation.get("version")) is not int or annotation["version"] != 1:
        raise CheckError("annotation version must be 1")
    case_id = annotation.get("case_id")
    if not isinstance(case_id, str) or not case_id.strip():
        raise CheckError("case_id must be a non-empty string")
    case = cases.get(case_id)
    if case is None:
        raise CheckError(f"unknown case_id {case_id!r}")
    run = annotation.get("run")
    if type(run) is not int or run < 1:
        raise CheckError("run must be a positive integer")
    judge = annotation.get("judge")
    if not isinstance(judge, str) or not judge.strip():
        raise CheckError("judge must be a non-empty string")
    transcript_ref = annotation.get("transcript")
    if not isinstance(transcript_ref, str) or not transcript_ref.strip():
        raise CheckError("transcript must be a non-empty path")
    transcript_path = Path(transcript_ref)
    if not transcript_path.is_absolute():
        transcript_path = Path(annotation_path).resolve().parent / transcript_path
    try:
        transcript_text = transcript_path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as error:
        raise CheckError(f"transcript unavailable: {transcript_path}: {error}") from error
    assistant, learner = _parse_transcript(transcript_text)

    must_texts = case["expect"]["must"]
    must_not_texts = case["expect"]["must_not"]
    failures = []
    observed_count = 0
    observed_flags = _check_items(annotation.get("must"), must_texts, MUST_KEYS, "observed", case_id, "must")
    for index, observed in enumerate(observed_flags):
        if observed:
            quote = _require_quote(annotation["must"][index], f"{case_id} must {index}")
            _verify_evidence(assistant, learner, annotation["must"][index].get("turns"),
                             quote, f"{case_id} must {index}")
            observed_count += 1
        else:
            failures.append(f"must {index} not observed: {must_texts[index]}")

    violation_count = 0
    violation_flags = _check_items(annotation.get("must_not"), must_not_texts, MUST_NOT_KEYS, "violation", case_id, "must_not")
    for index, violation in enumerate(violation_flags):
        if violation:
            quote = _require_quote(annotation["must_not"][index], f"{case_id} must_not {index}")
            _verify_evidence(assistant, learner, annotation["must_not"][index].get("turns"),
                             quote, f"{case_id} must_not {index}")
            violation_count += 1
            failures.append(f"must_not {index} violated: {must_not_texts[index]}")

    auto_fails = annotation.get("automatic_fails", [])
    if not isinstance(auto_fails, list):
        raise CheckError("automatic_fails must be a list")
    for entry in auto_fails:
        if not isinstance(entry, dict):
            raise CheckError("automatic_fails entries must be objects")
        unknown = set(entry) - AUTOFAIL_KEYS
        if unknown:
            raise CheckError(f"unknown automatic_fails fields: {sorted(unknown)}")
        dimension = entry.get("dimension")
        if dimension not in DIMENSIONS:
            raise CheckError(f"automatic fail needs a dimension in {DIMENSIONS}; found {dimension!r}")
        quote = _require_quote(entry, f"{case_id} automatic fail {dimension}")
        _verify_evidence(assistant, learner, entry.get("turns"), quote,
                         f"{case_id} automatic fail {dimension}")
        failures.append(f"automatic fail {dimension}: {quote}")
    severe_entries = annotation.get("severe", [])
    if not isinstance(severe_entries, list):
        raise CheckError("severe must be a list")
    for entry in severe_entries:
        if not isinstance(entry, dict):
            raise CheckError("severe entries must be objects")
        unknown = set(entry) - SEVERE_KEYS
        if unknown:
            raise CheckError(f"unknown severe fields: {sorted(unknown)}")
        rule = entry.get("rule")
        if not isinstance(rule, str) or not rule.strip():
            raise CheckError("severe entries need a non-empty rule")
        quote = _require_quote(entry, f"{case_id} severe: {rule}")
        _verify_evidence(assistant, learner, entry.get("turns"), quote,
                         f"{case_id} severe: {rule}")
        failures.append(f"severe: {rule}")

    dimensions = annotation.get("dimensions", {})
    if not isinstance(dimensions, dict):
        raise CheckError("dimensions must be an object")
    dimension_report = []
    for key, value in dimensions.items():
        if key not in DIMENSIONS:
            raise CheckError(f"unknown dimension {key!r}; expected one of {DIMENSIONS}")
        if value in ("N/A", "n/a"):
            dimension_report.append(f"{key}=N/A")
        elif type(value) is int and 0 <= value <= 2:
            dimension_report.append(f"{key}={value}")
        else:
            raise CheckError(f"dimension {key} must be 0, 1, 2, or N/A; found {value!r}")

    verdict = "FAIL" if failures else "PASS"
    summary = {
        "case": case_id,
        "run": run,
        "judge": judge,
        "must": f"{observed_count}/{len(must_texts)} observed",
        "must_not": f"{violation_count} violations",
        "automatic_fails": len(auto_fails),
        "severe": len(severe_entries),
        "dimensions": dimension_report,
        "notes": annotation.get("notes", ""),
    }
    return verdict, summary, failures


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--cases", type=Path, default=Path(__file__).with_name("cases.json"),
        help="path to cases.json (default: next to this script)",
    )
    parser.add_argument("--annotation", type=Path, required=True, help="annotation JSON to check")
    args = parser.parse_args(argv)

    try:
        cases_doc = _load_json(args.cases)
        case_list, errors = validate(cases_doc)
        if errors:
            raise CheckError("invalid cases: " + "; ".join(errors))
        cases = {case["id"]: case for case in case_list}
        verdict, summary, failures = check_annotation(args.annotation, cases)
    except CheckError as error:
        print(f"INVALID: {error}")
        print("verdict: INVALID (this annotation cannot pass)")
        print(SCOPE_NOTE)
        return EXIT_INVALID

    print(f"case {summary['case']}, run {summary['run']}, judge: {summary['judge']}")
    print(f"must: {summary['must']}")
    print(f"must_not: {summary['must_not']}")
    print(f"automatic fails: {summary['automatic_fails']}")
    print(f"severe: {summary['severe']}")
    print("dimensions: " + (" ".join(summary["dimensions"]) if summary["dimensions"] else "none recorded"))
    if summary["notes"]:
        print(f"notes: {summary['notes']}")
    for failure in failures:
        print(f"  - {failure}")
    print(f"verdict: {verdict}")
    print(SCOPE_NOTE)
    return EXIT_PASS if verdict == "PASS" else EXIT_FAIL


if __name__ == "__main__":
    raise SystemExit(main())
