"""Stdlib generator, oracle, prompts, and grader for a synthetic rule benchmark.

This module makes no model/network calls. Actual subagent replies are recorded
separately by the orchestrator, never synthesized by this program.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import random

MODEL = "opencode-go/deepseek-v4.1-flash#low"
SEEDS = (43, 107, 211, 509)
ARMS = ("tutor", "selfstudy", "control")
ROOT = Path(__file__).resolve().parent


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value):
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def evaluate(world, item):
    required = {"count", "seal", "glyph", "flag"}
    if (set(item) != required or type(item.get("count")) is not int or not 0 <= item["count"] <= 10
            or item["seal"] not in world["seals"] or item["glyph"] not in world["glyphs"]
            or type(item["flag"]) is not int or item["flag"] not in (0, 1)):
        return {"value": None, "route": "UNKNOWN", "trace": []}
    n = item["count"]
    if n == 10 and item["flag"] == 1:
        return {"value": None, "route": world["stop"], "trace": []}
    if item["seal"] == world["seals"][1]:
        n = 10 - n
    trace = [n]
    index = world["glyphs"].index(item["glyph"])
    if index == 0:
        n = (world["factor"] * n + world["shift"]) % 11
    elif index == 1:
        n = (n + world["shift"]) % 11
    else:
        n = (2 * n + 1) % 11
    trace.append(n)
    n = (n + world["flag_shift"]) % 11 if item["flag"] else n
    trace.append(n)
    return {"value": n, "route": world["routes"][n % 3], "trace": trace}


def make_world(seed):
    rng = random.Random(seed)
    words = ["fep", "lun", "vek", "sor", "dap", "nib", "kel", "zun", "pir", "bov", "teg"]
    rng.shuffle(words)
    world = {"seed": seed, "seals": words[:2], "glyphs": words[2:5],
             "routes": words[5:8], "stop": words[8], "factor": rng.choice((2, 3, 4)),
             "shift": rng.randint(1, 10), "flag_shift": rng.randint(1, 10)}
    pool = [{"count": n, "seal": seal, "glyph": glyph, "flag": flag}
            for n in range(11) for seal in world["seals"] for glyph in world["glyphs"] for flag in (0, 1)]
    practice = [{"count": rng.randint(1, 8), "seal": world["seals"][1], "glyph": world["glyphs"][0], "flag": 1},
                {"count": 10, "seal": world["seals"][0], "glyph": world["glyphs"][1], "flag": 1}]
    worked = {"count": 2, "seal": world["seals"][0], "glyph": world["glyphs"][2], "flag": 1}
    available = [item for item in pool if item not in practice and item != worked]
    rng.shuffle(available)
    pre = available[:4]
    post = available[4:12]
    # Pin one unseen priority exception and one ordinary upper boundary.
    post[0] = {"count": 10, "seal": world["seals"][1], "glyph": world["glyphs"][2], "flag": 1}
    post[1] = {"count": 10, "seal": world["seals"][1], "glyph": world["glyphs"][0], "flag": 0}
    used = [worked, *practice, *pre]
    unique = []
    for item in post + available[12:]:
        if item not in used and item not in unique:
            unique.append(item)
        if len(unique) == 8:
            break
    unknown_seal = {**unique[2], "seal": "unlisted-seal"}
    missing_flag = {key: value for key, value in unique[3].items() if key != "flag"}
    world.update(worked=worked, practice=practice, pre=pre, post=unique + [unknown_seal, missing_flag])
    return world


def worked_text(world, item):
    answer = evaluate(world, item)
    if answer["route"] == "UNKNOWN":
        return "A required field is missing or invalid: value=null, route=UNKNOWN, trace=[]."
    if answer["route"] == world["stop"]:
        return f"Original count=10 and flag=1 trigger the priority stop: value=null, route={world['stop']}, trace=[]. No transforms run."
    return (f"After seal, glyph, then flag the trace is {answer['trace']}; final value={answer['value']}, "
            f"route={answer['route']}. Choose the route only from the final value's remainder on division by 3.")


def handout(world):
    a, b, c = world["glyphs"]
    normal, flip = world["seals"]
    r0, r1, r2 = world["routes"]
    return (f"Fictional Neral sorting world {world['seed']}. Each parcel has count (an integer 0..10), "
            f"seal ({normal} or {flip}), glyph ({a}, {b}, or {c}), and flag (integer 0 or 1). "
            "Validate all four fields first: missing/unlisted/invalid fields mean value=null, route=UNKNOWN, trace=[]. "
            f"Next, if ORIGINAL count=10 and flag=1, stop immediately: value=null, route={world['stop']}, trace=[]. "
            f"Otherwise apply these steps IN ORDER: (1) seal {flip} changes count n to 10-n; seal {normal} leaves n alone. "
            f"(2) glyph {a}: n=({world['factor']}*n+{world['shift']}) mod 11; glyph {b}: n=(n+{world['shift']}) mod 11; "
            f"glyph {c}: n=(2*n+1) mod 11. (3) flag=1 adds {world['flag_shift']} mod 11; flag=0 leaves n alone. "
            f"The final n is value. Remainder n mod 3 chooses route: 0->{r0}, 1->{r1}, 2->{r2}. "
            "mod means the nonnegative remainder (12 mod 11 is 1). trace lists n after seal, glyph, flag. "
            f"Worked example {canonical(world['worked'])}: {worked_text(world, world['worked'])}")


def task_text(world, stage):
    items = world["pre"] if stage == "pre" else world["post"] if stage == "post" else [world["practice"][int(stage[-1]) - 1]]
    prefix = {"pre": "B", "post": "Q", "practice1": "P1-", "practice2": "P2-"}[stage]
    lines = []
    for index, item in enumerate(items, 1):
        question_id = f"{prefix}{index}"
        if stage == "post" and index in (7, 8):
            lines.append(f"{question_id}: A parcel starts at count {item['count']}; its outer seal is {item['seal']}, "
                         f"its glyph is {item['glyph']}, and its flag is {item['flag']}. Give the final value/route.")
        else:
            lines.append(f"{question_id}: {canonical(item)}")
    return "\n".join(lines)


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate key: {key}")
        result[key] = value
    return result


def parse_reply(raw, ids):
    text = raw.strip()
    if text.startswith("```json\n") and text.endswith("```"):
        text = text[8:-3].strip()
    reply = json.loads(text, object_pairs_hook=_pairs)
    if not isinstance(reply, dict) or set(reply) - {"answers", "question", "summary"}:
        raise ValueError("Expected an answers object with only optional question/summary")
    answers = reply.get("answers")
    if not isinstance(answers, list) or len(answers) != len(ids):
        raise ValueError("Every requested ID must be answered exactly once")
    indexed = {}
    for answer in answers:
        if not isinstance(answer, dict) or set(answer) != {"id", "value", "route", "trace"}:
            raise ValueError("Each answer needs id, value, route, trace")
        if answer["id"] not in ids or answer["id"] in indexed:
            raise ValueError("Unknown or repeated answer ID")
        if answer["value"] is not None and (type(answer["value"]) is not int or not 0 <= answer["value"] <= 10):
            raise ValueError("Value must be null or an integer 0..10")
        if not isinstance(answer["route"], str) or not isinstance(answer["trace"], list):
            raise ValueError("Route/trace types are invalid")
        if len(answer["trace"]) not in (0, 3) or any(type(n) is not int or not 0 <= n <= 10 for n in answer["trace"]):
            raise ValueError("Trace must contain zero or three intermediate integers")
        indexed[answer["id"]] = answer
    return indexed


def grade(world, stage, raw):
    items = world["pre"] if stage == "pre" else world["post"] if stage == "post" else [world["practice"][int(stage[-1]) - 1]]
    prefix = {"pre": "B", "post": "Q", "practice1": "P1-", "practice2": "P2-"}[stage]
    ids = [f"{prefix}{i}" for i in range(1, len(items) + 1)]
    try:
        answers = parse_reply(raw, ids)
    except (ValueError, TypeError, KeyError) as error:
        return {"valid": False, "error": str(error), "correct": [False] * len(items), "trace_correct": [False] * len(items)}
    expected = [evaluate(world, item) for item in items]
    return {"valid": True,
            "correct": [answers[key]["value"] == target["value"] and answers[key]["route"] == target["route"]
                        for key, target in zip(ids, expected)],
            "trace_correct": [answers[key]["trace"] == target["trace"] for key, target in zip(ids, expected)]}


def feedback(world, arm, number, raw):
    if arm == "control":
        return "Your response was recorded. This condition supplies no rulebook or answer feedback. Continue using only information actually provided; do not invent missing rules."
    item = world["practice"][number - 1]
    checked = worked_text(world, item)
    if arm == "selfstudy":
        return "Worked solution for your self-check: " + checked
    result = grade(world, f"practice{number}", raw)
    if not result["valid"]:
        return "The response format could not be assessed. Here is the checked task solution, not a claim of learner error: " + checked
    if result["correct"][0] and result["trace_correct"][0]:
        return "Your result and intermediate values match this item. That is open-context execution, not checked retention. " + checked
    if number == 2:
        return "Check the original count before any transformation: the priority stop outranks the seal/glyph/flag steps. " + checked
    answer = parse_reply(raw, [f"P{number}-1"])[f"P{number}-1"]
    expected = evaluate(world, item)
    if len(answer["trace"]) != 3:
        focus = "Without intermediate values I cannot locate the blocking step; compare the checked sequence. "
    elif answer["trace"] == expected["trace"]:
        focus = f"Your transformations match; check the final route lookup using {expected['value']} mod 3, not an earlier value. "
    else:
        index = next(i for i in range(3) if answer["trace"][i] != expected["trace"][i])
        focus = (f"The first mismatch is after {('seal', 'glyph', 'flag')[index]}: your trace has {answer['trace'][index]}, "
                 f"but that step gives {expected['trace'][index]}. Apply that step to the preceding value. ")
    return focus + checked


RESPONSE_RULE = ('Reply only JSON: {"answers":[{"id":"ID","value":null,"route":"UNKNOWN","trace":[]}],'
                 '"question":null}. Include every requested ID exactly once. Use computed integers/routes when justified; '
                 'UNKNOWN/null/[] means the required rules or fields are unavailable. Do not pretend to be human, '
                 'deliberately fail, or invent rules. No tools, files, browser, other agents, or external sources. '
                 'Show only the three task intermediate values, not hidden reasoning. question may be a brief clarification request.')


def prompt(world, arm, stage, previous=""):
    if stage == "pre":
        body = f"Synthetic rule-application study, fictional world {world['seed']}. No rulebook has been provided yet. This is a pretest without feedback.\n"
    elif stage == "practice1":
        body = (handout(world) if arm != "control" else "No rulebook is supplied in this condition.") + "\nPractice item 1:\n"
    elif stage == "practice2":
        body = feedback(world, arm, 1, previous) + "\nPractice item 2:\n"
    else:
        body = feedback(world, arm, 2, previous) + "\nPosttest: no new help. Prior conversation remains available; this is not a retention test.\n"
    return body + task_text(world, stage) + "\n" + RESPONSE_RULE


def freeze(out):
    if out.exists():
        raise ValueError("Refusing to overwrite a frozen benchmark")
    worlds = [make_world(seed) for seed in SEEDS]
    rng = random.Random(20261029)
    runs = []
    for world in worlds:
        arms = list(ARMS)
        rng.shuffle(arms)
        runs.extend({"id": f"w{world['seed']}-{arm}", "seed": world["seed"], "arm": arm,
                     "phase": "development" if world["seed"] in SEEDS[:2] else "confirmation"} for arm in arms)
    document = {"format": "synthetic-rule-benchmark", "version": 1, "model": MODEL,
                "worlds": worlds, "runs": runs,
                "protocol_sha256": hashlib.sha256((ROOT / "PROTOCOL.md").read_bytes()).hexdigest(),
                "generator_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    document["data_sha256"] = digest({"worlds": worlds, "runs": runs})
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return document


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("freeze", "prompt", "grade"))
    parser.add_argument("--data", type=Path, default=ROOT / "frozen.json")
    parser.add_argument("--run")
    parser.add_argument("--stage", choices=("pre", "practice1", "practice2", "post"))
    parser.add_argument("--reply", type=Path)
    args = parser.parse_args()
    if args.command == "freeze":
        data = freeze(args.data)
        print(json.dumps({"runs": data["runs"], "data_sha256": data["data_sha256"]}, indent=2))
        return
    data = json.loads(args.data.read_text(encoding="utf-8"))
    assert digest({"worlds": data["worlds"], "runs": data["runs"]}) == data["data_sha256"], "Frozen data changed"
    run = next(row for row in data["runs"] if row["id"] == args.run)
    world = next(world for world in data["worlds"] if world["seed"] == run["seed"])
    raw = args.reply.read_text(encoding="utf-8") if args.reply else ""
    if args.command == "prompt":
        print(prompt(world, run["arm"], args.stage, raw))
    else:
        print(json.dumps(grade(world, args.stage, raw), indent=2))


if __name__ == "__main__":
    main()
