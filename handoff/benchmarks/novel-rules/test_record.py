import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import benchmark as b
import record as r


class RecordTests(unittest.TestCase):
    def setUp(self):
        preferred = Path(os.environ.get("LOCALAPPDATA", "")) / "Temp" / "opencode"
        self.temp = tempfile.TemporaryDirectory(dir=preferred if preferred.is_dir() else None)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.world = b.make_world(43)
        self.data = {"model": b.MODEL, "data_sha256": "test fixture, not an actual run",
                     "runs": [{"id": "unit-tutor", "phase": "development", "seed": 43, "arm": "tutor"}],
                     "worlds": [self.world]}

    def raw(self, stage):
        items = self.world["pre"] if stage == "pre" else self.world["post"] if stage == "post" else [self.world["practice"][int(stage[-1]) - 1]]
        prefix = {"pre": "B", "post": "Q", "practice1": "P1-", "practice2": "P2-"}[stage]
        path = self.root / f"{stage}-input.txt"
        path.write_text(json.dumps({"answers": [{"id": f"{prefix}{i}", **b.evaluate(self.world, item)}
                                                for i, item in enumerate(items, 1)], "question": None}), encoding="utf-8")
        return path

    def test_immutable_records_preserve_raw_and_session_identity(self):
        raw = self.raw("pre")
        with patch.object(b, "ROOT", self.root):
            r.record(self.data, "unit-tutor", "pre", "synthetic-session", raw)
            saved = self.root / "sessions/unit-tutor/pre.reply.txt"
            self.assertEqual(saved.read_text(encoding="utf-8"), raw.read_text(encoding="utf-8"))
            with self.assertRaises(FileExistsError):
                r.record(self.data, "unit-tutor", "pre", "synthetic-session", raw)
            with self.assertRaises(AssertionError):
                r.record(self.data, "unit-tutor", "practice1", "different-session", self.raw("practice1"))

    def test_report_checks_integrity_and_reports_counts_not_mastery(self):
        with patch.object(b, "ROOT", self.root):
            for stage in r.STAGES:
                r.record(self.data, "unit-tutor", stage, "synthetic-session", self.raw(stage))
            row = r.report(self.data, "development")["rows"][0]
            self.assertEqual(row["post_known_of_8"], 8)
            self.assertEqual(row["invalid_input_abstention_of_2"], 2)
            self.assertGreater(row["prompt_words"], 0)
            (self.root / "sessions/unit-tutor/post.reply.txt").write_text("tampered", encoding="utf-8")
            with self.assertRaises(AssertionError):
                r.report(self.data, "development")

    def test_report_checks_saved_prompts_against_frozen_inputs(self):
        with patch.object(b, "ROOT", self.root):
            for stage in r.STAGES:
                r.record(self.data, "unit-tutor", stage, "synthetic-session", self.raw(stage))
            folder = self.root / "sessions/unit-tutor"
            metadata = json.loads((folder / "post.json").read_text(encoding="utf-8"))
            changed = (folder / "post.prompt.txt").read_text(encoding="utf-8")[:-1] + " unexpected help"
            (folder / "post.prompt.txt").write_text(changed + "\n", encoding="utf-8")
            for update_hash in (False, True):
                with self.subTest(update_hash=update_hash):
                    if update_hash:
                        metadata["prompt_sha256"] = hashlib.sha256(changed.encode("utf-8")).hexdigest()
                        metadata["prompt_characters"] = len(changed)
                        (folder / "post.json").write_text(json.dumps(metadata), encoding="utf-8")
                    with self.assertRaises(AssertionError):
                        r.report(self.data, "development")

    def test_report_rechecks_grades_counts_and_session_metadata(self):
        with patch.object(b, "ROOT", self.root):
            for stage in r.STAGES:
                r.record(self.data, "unit-tutor", stage, "synthetic-session", self.raw(stage))
            path = self.root / "sessions/unit-tutor/post.json"
            original = path.read_text(encoding="utf-8")
            wrong_grade = json.loads(original)["grade"]
            wrong_grade["correct"][0] = False
            for field, replacement in (("grade", wrong_grade), ("session", "replacement-session"),
                                       ("model", "other-model"), ("run", "other-run"), ("stage", "pre"),
                                       ("arm", "control"), ("phase", "confirmation"),
                                       ("prompt_characters", 1), ("reply_characters", 1)):
                with self.subTest(field=field):
                    metadata = json.loads(original)
                    metadata[field] = replacement
                    path.write_text(json.dumps(metadata), encoding="utf-8")
                    with self.assertRaises(AssertionError):
                        r.report(self.data, "development")
            path.write_text(original, encoding="utf-8")
            self.assertEqual(r.report(self.data, "development")["rows"][0]["post_known_of_8"], 8)


if __name__ == "__main__":
    unittest.main()
