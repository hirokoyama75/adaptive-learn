"""Audit captured tutor replies with the existing quote/annotation checker."""

import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[2]
sys.path.insert(0, str(PROJECT / "adaptive-learn/tests/live"))
from check_run import check_annotation

MODEL = "opencode-go/deepseek-v4.1-flash#low"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cases(phase):
    return json.loads((ROOT / f"{phase}.json").read_text(encoding="utf-8"))["cases"]


def prompt(case, arm):
    if arm not in ("before", "after", "chat"):
        raise ValueError("Unknown condition")
    if arm == "chat":
        prefix = "Act as a competent, helpful tutor. Help the student understand the issue using their work and available time."
    else:
        source = "original" if arm == "before" else "revised"
        prefix = (f"Read handoff/iterations/tutor-vs-chat/source/{source}.md and apply its full tutoring instructions. "
                  "The primary mathematics playbook is handoff/iterations/tutor-vs-chat/source/math-logic.md; read it too. "
                  "Do not read any other files or benchmarks.")
    return (prefix + "\nYou may use Python to check mathematics, but may not inspect other files, use the browser, "
            "consult external sources, delegate, or write files. Only claim checks you actually performed. "
            "Respond directly to the student; do not discuss the evaluation or produce a report about your process.\n\n" + case["prompt"])


def audit():
    manifest = json.loads((ROOT / "frozen.json").read_text(encoding="utf-8"))
    for name, expected in manifest["sha256"].items():
        assert digest(ROOT / name) == expected, f"Frozen input changed: {name}"
    all_cases = {case["id"]: case for phase in ("development", "confirmation") for case in cases(phase)}
    rows = []
    sessions = set()
    for path in sorted((ROOT / "runs").glob("*/metadata.json")):
        metadata = json.loads(path.read_text(encoding="utf-8"))
        folder = path.parent
        case = all_cases[metadata["case_id"]]
        raw = (folder / "reply.txt").read_text(encoding="utf-8")
        expected_prompt = prompt(case, metadata["arm"])
        assert (folder / "prompt.txt").read_text(encoding="utf-8") == expected_prompt + "\n"
        assert digest(folder / "reply.txt") == metadata["raw_sha256"]
        assert digest(folder / "prompt.txt") == metadata["prompt_sha256"]
        assert metadata["model"] == MODEL and metadata["session"] not in sessions
        sessions.add(metadata["session"])
        if metadata["arm"] != "chat":
            source = "original" if metadata["arm"] == "before" else "revised"
            assert digest(ROOT / "source" / f"{source}.md") == metadata["skill_sha256"]
        transcript = "## Learner turn 1\n" + case["prompt"] + "\n\n## Assistant turn 1\n" + raw
        assert (folder / "transcript.md").read_text(encoding="utf-8") == transcript
        verdict, summary, failures = check_annotation(folder / "annotation.json", all_cases)
        assert summary["case"] == metadata["case_id"]
        rows.append({"id": folder.name, "case": case["id"], "arm": metadata["arm"], "verdict": verdict,
                     "must": summary["must"], "must_not": summary["must_not"], "failures": failures})
    return {"kind": "synthetic tutor-behavior checks, not human learning", "model": MODEL, "rows": rows}


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2))
