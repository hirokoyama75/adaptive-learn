import json
import unittest

import benchmark as b


class BenchmarkTests(unittest.TestCase):
    def test_oracle_exhaustively_matches_independent_composition(self):
        for seed in b.SEEDS:
            world = b.make_world(seed)
            transforms = {
                world["glyphs"][0]: lambda n: (world["factor"] * n + world["shift"]) % 11,
                world["glyphs"][1]: lambda n: (n + world["shift"]) % 11,
                world["glyphs"][2]: lambda n: (2 * n + 1) % 11,
            }
            for n in range(11):
                for seal in world["seals"]:
                    for glyph in world["glyphs"]:
                        for flag in (0, 1):
                            item = dict(count=n, seal=seal, glyph=glyph, flag=flag)
                            if (n, flag) == (10, 1):
                                expected = dict(value=None, route=world["stop"], trace=[])
                            else:
                                first = {world["seals"][0]: n, world["seals"][1]: 10 - n}[seal]
                                second = transforms[glyph](first)
                                third = (second + {0: 0, 1: world["flag_shift"]}[flag]) % 11
                                expected = dict(value=third, route=world["routes"][third % 3], trace=[first, second, third])
                            self.assertEqual(b.evaluate(world, item), expected)

    def test_unknowns_and_boolean_inputs_are_not_defaulted(self):
        world = b.make_world(43)
        for bad in ({}, {**world["worked"], "count": True}, {**world["worked"], "flag": False},
                    {**world["worked"], "seal": "missing"}):
            self.assertEqual(b.evaluate(world, bad), dict(value=None, route="UNKNOWN", trace=[]))

    def test_posttest_disjoint_and_has_eight_known_two_unknown_items(self):
        for seed in b.SEEDS:
            world = b.make_world(seed)
            before = [world["worked"], *world["practice"], *world["pre"]]
            self.assertTrue(all(item not in before for item in world["post"]))
            self.assertEqual(len({b.canonical(item) for item in world["post"]}), 10)
            self.assertTrue(all(b.evaluate(world, item)["route"] != "UNKNOWN" for item in world["post"][:8]))
            self.assertTrue(all(b.evaluate(world, item)["route"] == "UNKNOWN" for item in world["post"][8:]))

    def test_perfect_answers_and_invalid_json_grade_without_guessing(self):
        world = b.make_world(107)
        raw = json.dumps({"answers": [{"id": f"Q{i}", **b.evaluate(world, item)}
                                      for i, item in enumerate(world["post"], 1)]})
        self.assertEqual(b.grade(world, "post", raw)["correct"], [True] * 10)
        self.assertEqual(b.grade(world, "post", "not json")["correct"], [False] * 10)
        parsed = json.loads(raw)
        parsed["answers"][0]["value"] = True
        self.assertFalse(b.grade(world, "post", json.dumps(parsed))["valid"])

    def test_feedback_is_bounded_and_control_gets_no_key(self):
        for seed in b.SEEDS:
            world = b.make_world(seed)
            for arm in b.ARMS:
                for number in (1, 2):
                    feedback = b.feedback(world, arm, number, "not json")
                    self.assertLessEqual(len(feedback.split()), 110)
                    if arm == "control":
                        self.assertNotIn(world["stop"], feedback)
                        self.assertNotIn("trace=", feedback)


if __name__ == "__main__":
    unittest.main()
