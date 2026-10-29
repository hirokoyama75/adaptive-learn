import itertools
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import pilot as p


def independent_matrix(world, program):
    k, m = world["k"], world["mod"]
    matrices = {"W": ((0, 1), (1, k)), "N": ((1, 1), (0, 1)), "C": ((1, 0), (1, 0)), "S": ((0, 1), (1, 0))}
    result = ((1, 0), (0, 1))
    for op in program:
        a = matrices[op]
        result = tuple(tuple(sum(a[i][n] * result[n][j] for n in range(2)) % m for j in range(2)) for i in range(2))
    return result


class PilotTests(unittest.TestCase):
    def worlds(self):
        return [p.make_world(617, 5, 2), p.make_world(1291, 7, 3)]

    def test_all_short_programs_match_independent_matrix_oracle(self):
        for world in self.worlds():
            for n in range(5):
                for program in itertools.product(p.OPS, repeat=n):
                    coefficients = independent_matrix(world, program)
                    for state in p.states(world):
                        self.assertEqual(p.execute(world, program, state), p.mapping(world, coefficients, state))

    def test_every_packet_has_unique_reverse_ambiguous_loss_and_solvable_construction(self):
        for world in self.worlds():
            seen = set()
            for index, packet in enumerate(world["packets"]):
                keys = {p.canonical({key: value}) for key, value in packet.items()}
                self.assertFalse(seen.intersection(keys))
                seen.update(keys)
                for key, count in (("R", 1), ("L", world["mod"])):
                    preimages = [s for s in p.states(world) if p.execute(world, packet[key]["program"], s) == packet[key]["observed"]]
                    self.assertEqual(len(preimages), count)
                for key in ("R", "L"):
                    coefficients = independent_matrix(world, packet[key]["program"])
                    for state in p.states(world):
                        self.assertEqual(p.execute(world, packet[key]["program"], state), p.mapping(world, coefficients, state))
                for program in (packet["Q"]["left"], packet["Q"]["right"]):
                    for state in p.states(world):
                        self.assertEqual(p.execute(world, program, state), p.mapping(world, independent_matrix(world, program), state))
                solution = p.solutions(world, index)
                raw = json.dumps({**solution, "explanation": "synthetic unit fixture, not a learner", "question": None})
                self.assertEqual(p.grade(world, index, raw)["correct"], dict.fromkeys(p.IDS, True))
                self.assertEqual(p.signature(world, packet["Q"]["left"]) == p.signature(world, packet["Q"]["right"]), bool(index % 2))

    def test_parser_and_certificates_reject_bad_types_and_accept_alternatives(self):
        world = self.worlds()[0]
        raw = {**p.solutions(world, 0), "explanation": "test fixture", "question": None}
        raw["answers"][0]["result"] = [True, 0]
        raw["answers"][1]["result"] *= 2
        raw["answers"][2]["result"] = {"equivalent": 0, "witness": [1, 0]}
        raw["answers"][3]["result"] = ["invented"]
        self.assertFalse(any(p.grade(world, 0, json.dumps(raw))["correct"].values()))
        self.assertFalse(p.grade(world, 0, "not json")["valid"])
        duplicate = '{"answers":[],"answers":[],"explanation":"","question":null}'
        self.assertFalse(p.grade(world, 0, duplicate)["valid"])
        raw = {**p.solutions(world, 0), "explanation": "test fixture", "question": None}
        raw["answers"][1]["result"].reverse()
        self.assertTrue(all(p.grade(world, 0, json.dumps(raw))["correct"].values()))

    def test_capture_is_immutable_and_separates_human_workload_from_runtime(self):
        temp_root = Path(os.environ["LOCALAPPDATA"]) / "Temp/opencode"
        with tempfile.TemporaryDirectory(dir=temp_root) as directory, patch.object(p, "ROOT", Path(directory)):
            world = self.worlds()[0]
            data = {"worlds": [world], "runs": [{"id": "test-tutor", "seed": 617, "arm": "tutor"}], "data_sha256": "unit fixture"}
            with patch.object(p, "load", return_value=data):
                p.prepare("test-tutor", 0)
                raw_path = Path(directory) / "raw.txt"
                raw_path.write_text(json.dumps({**p.solutions(world, 0), "explanation": "undo loss equivalence", "question": None}), encoding="utf-8")
                review = {key: {"ok": True, "quote": word} for key, word in zip(p.CHECKS, ("undo", "loss", "equivalence"))}
                saved = p.capture("test-tutor", 0, "test-session", raw_path, review)
                self.assertTrue(saved["qualifies"])
                with self.assertRaises(FileExistsError):
                    p.capture("test-tutor", 0, "test-session", raw_path, review)
                result = p.report()
                self.assertFalse(result["human_learning_time_measured"])
                self.assertFalse(result["rows"][0]["confirmed_criterion"])
                self.assertGreater(result["rows"][0]["human_facing_words"], 0)
                row = result["rows"][0]
                reference = row["human_workload_scenarios_not_measurements"]["reference"]
                self.assertEqual(reference["assumed_active_seconds"], round(60 * row["human_facing_words"] / 180 + 4 * 45 + 30, 1))
                record_path = Path(directory) / "sessions/test-tutor/0.record.json"
                original = record_path.read_text(encoding="utf-8")
                changed = json.loads(original)
                changed["qualifies"] = False
                record_path.write_text(json.dumps(changed), encoding="utf-8")
                with self.assertRaises(AssertionError):
                    p.report()
                changed = json.loads(original)
                changed["explanation_review"]["loss"]["quote"] = "fabricated quote"
                record_path.write_text(json.dumps(changed), encoding="utf-8")
                with self.assertRaises(AssertionError):
                    p.report()
                record_path.write_text(original, encoding="utf-8")
                p.prepare("test-tutor", 3)
                with self.assertRaises(AssertionError):
                    p.capture("test-tutor", 3, "replacement-session", raw_path, review)
                (Path(directory) / "sessions/test-tutor/0.prompt.txt").write_text("tampered", encoding="utf-8")
                with self.assertRaises(AssertionError):
                    p.report()

    def test_human_lesson_keys_track_original_information_and_accept_all_witnesses(self):
        world = {"mod": 5, "k": 2}
        for program, start, result in ((["W", "N"], [2, 1], [0, 4]),
                                       (["N", "W"], [2, 3], [3, 1]),
                                       (["W", "S"], [3, 2], [2, 2])):
            self.assertEqual(p.execute(world, program, start), result)
            self.assertEqual([s for s in p.states(world) if p.execute(world, program, s) == result], [tuple(start)])
        for program, observation, expected in ((["S", "C"], [3, 3], {(a, 3) for a in range(5)}),
                                               (["N", "S", "C"], [4, 4], {(a, 4) for a in range(5)}),
                                               (["S", "N", "C"], [1, 1], {(a, (1-a) % 5) for a in range(5)})):
            self.assertEqual({s for s in p.states(world) if p.execute(world, program, s) == observation}, expected)
        for state in p.states(world):
            self.assertEqual(p.execute(world, ["S", "C"], state), [state[1], state[1]])
            self.assertEqual(p.execute(world, ["W", "C"], state), [state[1], state[1]])


if __name__ == "__main__":
    unittest.main()
