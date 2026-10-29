from fractions import Fraction
import itertools
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import check


class CaseFacts(unittest.TestCase):
    def test_original_and_changed_information_loss_are_exhaustive(self):
        for modulus, output in ((5, 2), (7, 5)):
            def process(x, y):
                if modulus == 5:
                    x, y = y, x
                    x, y = x, x
                    x, y = (x+y) % modulus, y
                    x, y = y, x
                else:
                    x, y = (x+y) % modulus, y
                    x, y = y, x
                    x, y = x, x
                return x, y
            target = (output, 2*output % modulus) if modulus == 5 else (output, output)
            actual = {(x,y) for x,y in itertools.product(range(modulus), repeat=2) if process(x,y) == target}
            self.assertEqual(actual, {(x,output) for x in range(modulus)})
        self.assertEqual(((2+3) % 7, 3)[::-1], (3,5))

    def test_root_set_and_valid_alternatives(self):
        self.assertEqual([x for x in range(-10,11) if x*(x-2)==0], [0,2])
        for x in (Fraction(2),Fraction(3)):
            self.assertEqual((x-Fraction(5,2))**2, Fraction(1,4))
            self.assertEqual(x*x-5*x+6, 0)
        self.assertEqual(Fraction(18,3)-Fraction(6,3), 4)

    def test_without_replacement_is_conditional_not_independent(self):
        draws=list(itertools.permutations(range(5),2))
        two_red=sum(a<3 and b<3 for a,b in draws)
        self.assertEqual(Fraction(two_red,len(draws)), Fraction(3,10))
        self.assertEqual(Fraction(3,5)*Fraction(2,4), Fraction(3,10))
        self.assertNotEqual(Fraction(2,4), Fraction(3,5))

    def test_audit_rejects_changed_capture_and_wrong_case_annotation(self):
        temp = Path(os.environ["LOCALAPPDATA"]) / "Temp/opencode"
        with tempfile.TemporaryDirectory(dir=temp) as directory, patch.object(check, "ROOT", Path(directory)):
            root = Path(directory)
            case = {"id": "fixture", "prompt": "Synthetic unit fixture, not a live learner.",
                    "expect": {"must": ["State the claim"], "must_not": []}}
            (root / "development.json").write_text(json.dumps({"cases": [case, {**case, "id": "other"}]}), encoding="utf-8")
            (root / "confirmation.json").write_text('{"cases":[]}', encoding="utf-8")
            (root / "frozen.json").write_text(json.dumps({"sha256": {name: check.digest(root / name) for name in ("development.json", "confirmation.json")}}), encoding="utf-8")
            folder = root / "runs/fixture-chat"
            folder.mkdir(parents=True)
            raw = "The claim is correct.\n"
            (folder / "reply.txt").write_text(raw, encoding="utf-8")
            (folder / "prompt.txt").write_text(check.prompt(case, "chat") + "\n", encoding="utf-8")
            (folder / "transcript.md").write_text("## Learner turn 1\n" + case["prompt"] + "\n\n## Assistant turn 1\n" + raw, encoding="utf-8")
            metadata = {"case_id": "fixture", "arm": "chat", "model": check.MODEL, "session": "unit-test-only",
                        "raw_sha256": check.digest(folder / "reply.txt"), "prompt_sha256": check.digest(folder / "prompt.txt")}
            (folder / "metadata.json").write_text(json.dumps(metadata), encoding="utf-8")
            annotation = {"format": "live-run-annotation", "version": 1, "case_id": "fixture", "run": 1,
                          "judge": "unit fixture, not a tutor", "transcript": "transcript.md",
                          "must": [{"index": 0, "observed": True, "turns": [1], "quote": "claim is correct"}], "must_not": []}
            (folder / "annotation.json").write_text(json.dumps(annotation), encoding="utf-8")
            self.assertEqual(check.audit()["rows"][0]["verdict"], "PASS")
            (folder / "reply.txt").write_text("changed", encoding="utf-8")
            with self.assertRaises(AssertionError):
                check.audit()
            (folder / "reply.txt").write_text(raw, encoding="utf-8")
            annotation["case_id"] = "other"
            (folder / "annotation.json").write_text(json.dumps(annotation), encoding="utf-8")
            with self.assertRaises(AssertionError):
                check.audit()


if __name__ == "__main__":
    unittest.main()
