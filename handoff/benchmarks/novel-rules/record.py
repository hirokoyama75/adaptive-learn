"""Record actual subagent replies and summarize frozen synthetic-benchmark runs.

The orchestrator supplies raw returned text and the actual session ID. This
script cannot authenticate the provider, inspect hidden tool calls, or run a
model. Generated prompts are the declared inputs, not a provider trace.
"""

import argparse
import hashlib
import json
from pathlib import Path

import benchmark as b

STAGES = ("pre", "practice1", "practice2", "post")


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_frozen():
    path = b.ROOT / "frozen.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert b.digest({"worlds": data["worlds"], "runs": data["runs"]}) == data["data_sha256"]
    assert file_hash(b.ROOT / "benchmark.py") == data["generator_sha256"], "Generator/grader changed after freeze"
    assert file_hash(b.ROOT / "PROTOCOL.md") == data["protocol_sha256"], "Protocol changed after freeze"
    return data


def write_once(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(text)


def record(data, run_id, stage, session, raw_path):
    run = next(row for row in data["runs"] if row["id"] == run_id)
    world = next(world for world in data["worlds"] if world["seed"] == run["seed"])
    folder = b.ROOT / "sessions" / run_id
    previous = ""
    if stage != "pre":
        index = STAGES.index(stage)
        prior = folder / f"{STAGES[index - 1]}.json"
        saved = json.loads(prior.read_text(encoding="utf-8"))
        assert saved["session"] == session, "A learner session cannot be silently replaced"
        previous = (folder / f"{STAGES[index - 1]}.reply.txt").read_text(encoding="utf-8")
    raw = raw_path.read_text(encoding="utf-8")
    intended = b.prompt(world, run["arm"], stage, previous)
    grade = b.grade(world, stage, raw)
    metadata = {"run": run_id, "phase": run["phase"], "stage": stage,
                "session": session, "model": data["model"], "arm": run["arm"],
                "raw_sha256": hashlib.sha256(raw.encode("utf-8")).hexdigest(),
                "prompt_sha256": hashlib.sha256(intended.encode("utf-8")).hexdigest(),
                "prompt_characters": len(intended), "reply_characters": len(raw), "grade": grade,
                "capture": "actual tool-returned reply, manually preserved by orchestrator; internal tool traces unavailable"}
    write_once(folder / f"{stage}.reply.txt", raw)
    write_once(folder / f"{stage}.prompt.txt", intended + "\n")
    write_once(folder / f"{stage}.json", json.dumps(metadata, indent=2) + "\n")
    return {"run": run_id, "stage": stage, "valid": grade["valid"], "correct": sum(grade["correct"])}


def report(data, phase):
    rows = []
    for run in data["runs"]:
        if phase != "all" and run["phase"] != phase:
            continue
        folder = b.ROOT / "sessions" / run["id"]
        world = next(world for world in data["worlds"] if world["seed"] == run["seed"])
        stages = {}
        previous = ""
        session = None
        prompt_words = reply_words = questions = 0
        for stage in STAGES:
            saved = json.loads((folder / f"{stage}.json").read_text(encoding="utf-8"))
            raw = (folder / f"{stage}.reply.txt").read_text(encoding="utf-8")
            assert hashlib.sha256(raw.encode("utf-8")).hexdigest() == saved["raw_sha256"]
            intended = (folder / f"{stage}.prompt.txt").read_text(encoding="utf-8")
            expected = b.prompt(world, run["arm"], stage, previous)
            assert intended == expected + "\n", "Saved prompt differs from frozen inputs and actual prior reply"
            assert saved["prompt_sha256"] == hashlib.sha256(expected.encode("utf-8")).hexdigest(), "Prompt hash mismatch"
            assert saved["grade"] == b.grade(world, stage, raw), "Saved grade differs from regrading the raw reply"
            if session is None:
                session = saved["session"]
            expected_metadata = {"run": run["id"], "phase": run["phase"], "stage": stage,
                                 "arm": run["arm"], "model": data["model"], "session": session,
                                 "prompt_characters": len(expected), "reply_characters": len(raw)}
            for field, value in expected_metadata.items():
                assert saved[field] == value, f"Inconsistent {field} metadata"
            previous = raw
            prompt_words += len(intended.split())
            reply_words += len(raw.split())
            if saved["grade"]["valid"]:
                text = raw.strip()
                payload = json.loads(text[8:-3] if text.startswith("```json\n") and text.endswith("```") else text)
                questions += isinstance(payload.get("question"), str) and bool(payload["question"].strip())
            stages[stage] = saved
        post = stages["post"]["grade"]
        rows.append({**run, "pre_correct_of_4": sum(stages["pre"]["grade"]["correct"]),
                     "practice1_correct": sum(stages["practice1"]["grade"]["correct"]),
                     "practice2_correct": sum(stages["practice2"]["grade"]["correct"]),
                     "post_known_of_8": sum(post["correct"][:8]),
                     "surface_transfer_of_2": sum(post["correct"][6:8]),
                     "invalid_input_abstention_of_2": sum(post["correct"][8:]),
                     "known_traces_of_8": sum(post["trace_correct"][:8]),
                     "invalid_replies": sum(not stage["grade"]["valid"] for stage in stages.values()),
                     "clarification_questions": questions, "prompt_words": prompt_words, "reply_words": reply_words,
                     "prompt_characters": sum(stage["prompt_characters"] for stage in stages.values()),
                     "reply_characters": sum(stage["reply_characters"] for stage in stages.values())})
    return {"kind": "synthetic open-context benchmark; not human learning", "model": data["model"],
            "frozen_data_sha256": data["data_sha256"], "phase": phase, "rows": rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("record", "report"))
    parser.add_argument("--run")
    parser.add_argument("--stage", choices=STAGES)
    parser.add_argument("--session")
    parser.add_argument("--raw", type=Path)
    parser.add_argument("--phase", choices=("development", "confirmation", "all"), default="all")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    data = load_frozen()
    result = record(data, args.run, args.stage, args.session, args.raw) if args.command == "record" else report(data, args.phase)
    text = json.dumps(result, indent=2) + "\n"
    if args.out:
        write_once(args.out, text)
    print(text, end="")


if __name__ == "__main__":
    main()
