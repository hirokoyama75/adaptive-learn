"""Checked concept tasks and immutable capture for a small time-focused pilot."""

from datetime import datetime, timezone
import hashlib
import itertools
import json
from pathlib import Path
import random
import sys
import time

ROOT = Path(__file__).resolve().parent
MODEL = "opencode-go/deepseek-v4.1-flash#low"
OPS = ("W", "N", "C", "S")
IDS = ("R", "L", "Q", "B")
CHECKS = ("reverse", "loss", "equivalence")


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_once(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(text)


def states(world):
    return list(itertools.product(range(world["mod"]), repeat=2))


def execute(world, program, state):
    x, y = state
    m, k = world["mod"], world["k"]
    for op in program:
        if op == "W":
            x, y = y, (x + k * y) % m
        elif op == "N":
            x, y = (x + y) % m, y
        elif op == "C":
            x, y = x, x
        elif op == "S":
            x, y = y, x
        else:
            raise ValueError("Unknown operation")
    return [x, y]


def matrix(world, program):
    a, c = execute(world, program, (1, 0))
    b, d = execute(world, program, (0, 1))
    return [[a, b], [c, d]]


def mapping(world, coefficients, state):
    return [sum(a * b for a, b in zip(row, state)) % world["mod"] for row in coefficients]


def signature(world, program):
    return [execute(world, program, state) for state in states(world)]


def make_world(seed, modulus, k):
    world = {"seed": seed, "mod": modulus, "k": k}
    rng = random.Random(seed)
    packets = []
    used = set()
    for index in range(4):
        while True:
            reverse = [rng.choice(("W", "N", "S")) for _ in range(5)]
            start = rng.choice(states(world))
            observation = execute(world, reverse, start)
            loss = [rng.choice(("W", "N", "S")), "C", rng.choice(("W", "N")), "S"]
            lost_observation = execute(world, loss, rng.choice(states(world)))
            tail = [rng.choice(("W", "N", "S"))]
            left = ["W", "S"] + tail
            right = (["N"] * k if index % 2 else ["S"] + ["N"] * k + ["S"]) + tail
            target_program = (["N", "W", "C"] if index == 3 else rng.choice(
                (["N", "W", "N"], ["W", "N", "S"], ["N", "S", "W"], ["W", "W", "N"])))
            packet = {"R": {"program": reverse, "observed": observation},
                      "L": {"program": loss, "observed": lost_observation},
                      "Q": {"left": left, "right": right},
                      "B": {"target": matrix(world, target_program), "max_length": 3}}
            keys = {canonical({key: value}) for key, value in packet.items()}
            if not used.intersection(keys):
                used.update(keys)
                packets.append(packet)
                break
    world["packets"] = packets
    return world


def handout(world):
    m, k = world["mod"], world["k"]
    example = execute(world, ["W"], (1, 2))
    return (f"Goal: explain which changes preserve information, undo a chain, and test a claim on new cases. "
            f"A machine holds two numbers (x,y), each 0..{m-1}. Wrap arithmetic mod {m}: take the remainder; "
            f"for example {m+1} becomes 1 and -1 becomes {m-1}. "
            f"Operations use BOTH OLD values simultaneously: W makes (y, x+{k}*y); "
            "N makes (x+y, y); C makes (x,x); S makes (y,x). Wrap each result. "
            f"Example: W on (1,2) gives {example}. Run a list left to right. "
            "Recover means find a starting pair that would produce the observation. "
            "Two different starts with the same result show the result does not identify a unique start. "
            "Two programs are equivalent only if their results agree for EVERY possible starting pair. "
            "A construction must work for every pair, not just the examples. Ask a brief clarification if blocked.")


def task_text(world, index):
    p = world["packets"][index]
    return (f"R: After {p['R']['program']}, the pair is {p['R']['observed']}. Recover the unique starting pair.\n"
            f"L: After {p['L']['program']}, the pair is {p['L']['observed']}. Give TWO DISTINCT starting pairs that produce it.\n"
            f"Q: Are {p['Q']['left']} and {p['Q']['right']} equivalent for every pair? "
            "If not, give one starting pair on which they differ. If equivalent, witness=null.\n"
            f"B: Build a program of at most {p['B']['max_length']} operations. Its output must be "
            f"({p['B']['target'][0][0]}*x+{p['B']['target'][0][1]}*y, "
            f"{p['B']['target'][1][0]}*x+{p['B']['target'][1][1]}*y), mod {world['mod']}, for every starting pair.\n"
            "Briefly explain how to undo a chain, why L has no unique start, and your general justification or counterexample for Q.")


RESPONSE = ('Reply only JSON: {"answers":[{"id":"R","result":[0,0]},'
            '{"id":"L","result":[[0,0],[0,1]]},'
            '{"id":"Q","result":{"equivalent":false,"witness":[0,0]}},'
            '{"id":"B","result":["W","S"]}],"explanation":"brief explanation",'
            '"question":null}. Those are format examples, not task answers. Include each ID exactly once. '
            'Use result=null if you cannot answer. Do not deliberately fail or pretend to be human. '
            'No tools, files, browser, other agents, or external sources. Show only task answers and a short explanation, not hidden reasoning.')


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON key")
        result[key] = value
    return result


def parse(raw):
    text = raw.strip()
    if text.startswith("```json\n") and text.endswith("```"):
        text = text[8:-3].strip()
    payload = json.loads(text, object_pairs_hook=unique_pairs)
    if not isinstance(payload, dict) or set(payload) != {"answers", "explanation", "question"}:
        raise ValueError("Expected answers, explanation, question")
    if not isinstance(payload["explanation"], str) or (payload["question"] is not None and not isinstance(payload["question"], str)):
        raise ValueError("Invalid explanation/question")
    answers = payload["answers"]
    if not isinstance(answers, list) or len(answers) != 4:
        raise ValueError("Four answers required")
    indexed = {}
    for answer in answers:
        if not isinstance(answer, dict) or set(answer) != {"id", "result"} or not isinstance(answer["id"], str):
            raise ValueError("Invalid answer object")
        if answer["id"] not in IDS or answer["id"] in indexed:
            raise ValueError("Missing/duplicate/unknown ID")
        indexed[answer["id"]] = answer["result"]
    return payload, indexed


def grade(world, index, raw):
    try:
        _, a = parse(raw)
    except (ValueError, TypeError) as error:
        return {"valid": False, "error": str(error), "correct": {key: False for key in IDS}}
    p = world["packets"][index]
    def pair(value):
        return isinstance(value, list) and len(value) == 2 and all(type(n) is int and 0 <= n < world["mod"] for n in value)
    r = pair(a["R"]) and execute(world, p["R"]["program"], a["R"]) == p["R"]["observed"]
    l = (isinstance(a["L"], list) and len(a["L"]) == 2 and all(pair(v) for v in a["L"])
         and a["L"][0] != a["L"][1] and all(execute(world, p["L"]["program"], v) == p["L"]["observed"] for v in a["L"]))
    equivalent = signature(world, p["Q"]["left"]) == signature(world, p["Q"]["right"])
    q = a["Q"]
    q = (isinstance(q, dict) and set(q) == {"equivalent", "witness"} and type(q["equivalent"]) is bool
         and q["equivalent"] == equivalent and ((equivalent and q["witness"] is None) or
         (not equivalent and pair(q["witness"]) and execute(world, p["Q"]["left"], q["witness"]) != execute(world, p["Q"]["right"], q["witness"]))))
    build = a["B"]
    good_build = (isinstance(build, list) and len(build) <= 3 and all(isinstance(op, str) and op in OPS for op in build)
                  and all(execute(world, build, state) == mapping(world, p["B"]["target"], state) for state in states(world)))
    return {"valid": True, "correct": dict(zip(IDS, map(bool, (r, l, q, good_build))))}


def solutions(world, index):
    p = world["packets"][index]
    reverse = next(list(s) for s in states(world) if execute(world, p["R"]["program"], s) == p["R"]["observed"])
    lost = [list(s) for s in states(world) if execute(world, p["L"]["program"], s) == p["L"]["observed"]][:2]
    witness = next((list(s) for s in states(world) if execute(world, p["Q"]["left"], s) != execute(world, p["Q"]["right"], s)), None)
    build = next(list(program) for n in range(4) for program in itertools.product(OPS, repeat=n)
                 if matrix(world, program) == p["B"]["target"])
    return {"answers": [{"id": "R", "result": reverse}, {"id": "L", "result": lost},
                        {"id": "Q", "result": {"equivalent": witness is None, "witness": witness}},
                        {"id": "B", "result": build}]}


def worked_feedback(world, index):
    key = solutions(world, index)
    values = {row["id"]: row["result"] for row in key["answers"]}
    return (f"Checked self-study solutions: R starts at {values['R']}. Undo the last operation first: "
            f"W inverse on (u,v) is ((v-{world['k']}*u) mod {world['mod']},u); N inverse is (u-v,v), wrapped; S undoes itself. "
            f"L: starts {values['L']} both give the observation; C erased a distinction, and later reversible moves cannot restore it. "
            f"Q: {values['Q']}. W then S adds {world['k']} copies of y to x, so it equals {world['k']} N operations; "
            "S before/after moves the addition to the other slot instead. A differing witness refutes a universal claim; a sample match is insufficient proof. "
            f"B: {values['B']}; substitute generic x,y through its operations to verify the target, not only one input.")


def freeze():
    worlds = [make_world(617, 5, 2), make_world(1291, 7, 3)]
    runs = [{"id": f"w{seed}-{arm}", "seed": seed, "arm": arm}
            for seed, arms in ((617, ("tutor", "selfstudy")), (1291, ("selfstudy", "tutor"))) for arm in arms]
    data = {"model": MODEL, "worlds": worlds, "runs": runs,
            "source_sha256": sha(Path(__file__).read_text(encoding="utf-8")),
            "protocol_sha256": sha((ROOT / "PROTOCOL.md").read_text(encoding="utf-8")),
            "skill_sha256": hashlib.sha256((ROOT.parents[2] / "adaptive-learn/SKILL.md").read_bytes()).hexdigest()}
    data["data_sha256"] = sha(canonical({"worlds": worlds, "runs": runs}))
    write_once(ROOT / "frozen.json", json.dumps(data, indent=2) + "\n")
    return data


def load():
    data = json.loads((ROOT / "frozen.json").read_text(encoding="utf-8"))
    assert data["data_sha256"] == sha(canonical({"worlds": data["worlds"], "runs": data["runs"]}))
    assert data["source_sha256"] == sha(Path(__file__).read_text(encoding="utf-8"))
    assert data["protocol_sha256"] == sha((ROOT / "PROTOCOL.md").read_text(encoding="utf-8"))
    return data


def prepare(run_id, index, feedback=""):
    data = load()
    run = next(run for run in data["runs"] if run["id"] == run_id)
    world = next(w for w in data["worlds"] if w["seed"] == run["seed"])
    material = (handout(world) if index == 0 else feedback) + "\n" + task_text(world, index)
    if index == 3:
        material = "Final transfer: no new help. Prior context remains available.\n" + material
    folder = ROOT / "sessions" / run_id
    declared = material + "\n" + RESPONSE
    write_once(folder / f"{index}.material.txt", material + "\n")
    write_once(folder / f"{index}.prompt.txt", declared + "\n")
    write_once(folder / f"{index}.launch.json", json.dumps({"utc": datetime.now(timezone.utc).isoformat(), "monotonic_ns": time.monotonic_ns(),
               "run": run_id, "index": index, "model": MODEL, "prompt_sha256": sha(declared), "material_sha256": sha(material)}, indent=2) + "\n")
    return declared


def qualifies(result, raw, review):
    assert set(review) == set(CHECKS)
    explanation = parse(raw)[0]["explanation"] if result["valid"] else ""
    for assessment in review.values():
        assert set(assessment) == {"ok", "quote"} and type(assessment["ok"]) is bool
        assert isinstance(assessment["quote"], str) and assessment["quote"] in explanation
        assert not assessment["ok"] or bool(assessment["quote"])
    return result["valid"] and all(result["correct"].values()) and all(v["ok"] for v in review.values())


def capture(run_id, index, session, raw_path, review):
    data = load()
    run = next(run for run in data["runs"] if run["id"] == run_id)
    world = next(w for w in data["worlds"] if w["seed"] == run["seed"])
    folder = ROOT / "sessions" / run_id
    launch = json.loads((folder / f"{index}.launch.json").read_text(encoding="utf-8"))
    prior = sorted(folder.glob("*.record.json"))
    if prior:
        assert json.loads(prior[-1].read_text(encoding="utf-8"))["session"] == session
    raw = raw_path.read_text(encoding="utf-8")
    result = grade(world, index, raw)
    qualified = qualifies(result, raw, review)
    record = {**launch, "session": session, "capture_utc": datetime.now(timezone.utc).isoformat(),
              "launch_to_capture_seconds": (time.monotonic_ns() - launch["monotonic_ns"]) / 1e9,
              "raw_sha256": sha(raw), "grade": result, "explanation_review": review,
              "qualifies": qualified}
    write_once(folder / f"{index}.reply.txt", raw)
    write_once(folder / f"{index}.record.json", json.dumps(record, indent=2) + "\n")
    return record


def report():
    data = load()
    rows = []
    for run in data["runs"]:
        world = next(w for w in data["worlds"] if w["seed"] == run["seed"])
        folder = ROOT / "sessions" / run["id"]
        turns = []
        words = protocol_words = 0
        for path in sorted(folder.glob("*.record.json")):
            saved = json.loads(path.read_text(encoding="utf-8"))
            index = saved["index"]
            raw = (folder / f"{index}.reply.txt").read_text(encoding="utf-8")
            prompt = (folder / f"{index}.prompt.txt").read_text(encoding="utf-8")
            material = (folder / f"{index}.material.txt").read_text(encoding="utf-8")
            launch = json.loads((folder / f"{index}.launch.json").read_text(encoding="utf-8"))
            for key, value in launch.items():
                assert saved[key] == value
            assert saved["model"] == MODEL and saved["run"] == run["id"] and index in range(4)
            assert sha(raw) == saved["raw_sha256"] and sha(prompt[:-1]) == saved["prompt_sha256"]
            assert sha(material[:-1]) == saved["material_sha256"] and prompt == material[:-1] + "\n" + RESPONSE + "\n"
            assert saved["grade"] == grade(world, index, raw)
            assert saved["qualifies"] == qualifies(saved["grade"], raw, saved["explanation_review"])
            assert saved["launch_to_capture_seconds"] >= 0
            assert not turns or saved["session"] == turns[0]["session"]
            words += len(material.split())
            protocol_words += len(RESPONSE.split())
            turns.append(saved)
        scenarios = {name: {"assumed_active_seconds": round(60 * words / speed + len(turns) * (4 * attempt + explain), 1)}
                     for name, speed, attempt, explain in (("fast", 240, 30, 20), ("reference", 180, 45, 30), ("slower", 120, 60, 60))}
        for value in scenarios.values():
            value["remaining_of_600_seconds_for_live_waiting"] = round(600 - value["assumed_active_seconds"], 1)
        rows.append({**run, "turns": [{"index": t["index"], "correct": t["grade"]["correct"], "qualifies": t["qualifies"],
                                     "launch_to_capture_seconds": t["launch_to_capture_seconds"]} for t in turns],
                     "confirmed_criterion": bool(turns and turns[-1]["index"] == 3 and turns[-1]["qualifies"] and any(t["qualifies"] for t in turns[:-1])),
                     "human_facing_words": words, "agent_protocol_words": protocol_words, "human_workload_scenarios_not_measurements": scenarios})
    return {"model": MODEL, "human_learning_time_measured": False, "data_sha256": data["data_sha256"], "rows": rows}


if __name__ == "__main__":
    if sys.argv[1:] == ["freeze"]:
        frozen = freeze()
        print(json.dumps({key: frozen[key] for key in ("model", "runs", "data_sha256", "source_sha256", "protocol_sha256", "skill_sha256")}, indent=2))
    else:
        print(json.dumps(report(), indent=2))
