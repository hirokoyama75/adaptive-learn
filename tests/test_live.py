"""Tests for tests/live/check_run.py — the mechanical run checker.

The checker derives PASS/FAIL from a judge's annotation of one live run. These
tests use the authored synthetic fixtures in tests/live/fixtures/ (never model
runs, never calibrated judges) plus temporary programmatic annotations written
outside this repository. No learner data, names, or root paths appear anywhere.

Nothing here judges tutoring or measures learning: it only proves that the
checker requires complete judgments and verifiable quotes, and that legitimate
corrections can pass while premature answers fail.
"""

import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

HERE = Path(__file__).resolve().parent
LIVE = HERE / "live"
CASES = LIVE / "cases.json"
FIXTURES = LIVE / "fixtures"

sys.path.insert(0, str(LIVE))
import check_run  # noqa: E402


def run_annotation(path):
    """Run check_run against one annotation; return (exit_code, stdout)."""
    output = io.StringIO()
    errors = io.StringIO()
    with redirect_stdout(output), redirect_stderr(errors):
        code = check_run.main(["--cases", str(CASES), "--annotation", str(path)])
    return code, output.getvalue()


class CheckRunTests(unittest.TestCase):
    def setUp(self):
        preferred = Path(os.environ.get("LOCALAPPDATA", "")) / "Temp" / "opencode"
        self.temp_base = preferred if preferred.is_dir() else None

    def test_usage_error_without_annotation(self):
        with self.assertRaises(SystemExit) as raised:
            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                check_run.main(["--cases", str(CASES)])
        self.assertEqual(raised.exception.code, 2)

    def test_refusal_only_run_fails(self):
        code, output = run_annotation(FIXTURES / "l01-refusal" / "annotation.json")
        self.assertEqual(code, 1)
        self.assertIn("verdict: FAIL", output)
        self.assertIn("not observed", output)

    def test_post_surrender_reveal_can_pass(self):
        code, output = run_annotation(FIXTURES / "l01-surrender" / "annotation.json")
        self.assertEqual(code, 0)
        self.assertIn("verdict: PASS", output)

    def test_tutor_correction_of_own_error_can_pass(self):
        code, output = run_annotation(FIXTURES / "l08-correction" / "annotation.json")
        self.assertEqual(code, 0)
        self.assertIn("verdict: PASS", output)

    def test_premature_answer_automatic_fail_fails_even_with_an_observed_must(self):
        code, output = run_annotation(FIXTURES / "l01-premature" / "annotation.json")
        self.assertEqual(code, 1)
        self.assertIn("verdict: FAIL", output)
        self.assertIn("automatic fail", output)

    def test_fabricated_quote_is_rejected(self):
        code, output = run_annotation(FIXTURES / "l01-fabricated" / "annotation.json")
        self.assertEqual(code, 2)
        self.assertIn("INVALID", output)
        self.assertIn("quote", output)

    def test_evidence_on_a_learner_turn_is_rejected(self):
        code, output = run_annotation(FIXTURES / "l01-learner-turn" / "annotation.json")
        self.assertEqual(code, 2)
        self.assertIn("INVALID", output)
        self.assertIn("learner turn", output)

    def test_missing_must_judgment_is_rejected(self):
        code, output = run_annotation(FIXTURES / "l01-missing-must" / "annotation.json")
        self.assertEqual(code, 2)
        self.assertIn("INVALID", output)
        self.assertIn("missing judgment", output)

    def test_na_dimensions_are_recorded_and_do_not_block_a_pass(self):
        code, output = run_annotation(FIXTURES / "l09-na" / "annotation.json")
        self.assertEqual(code, 0)
        self.assertIn("verdict: PASS", output)
        self.assertIn("D3=N/A", output)
        self.assertIn("D6=N/A", output)

    # Programmatic structural-invalidity checks over temporary data.

    def temp_annotation(self, mutate):
        with tempfile.TemporaryDirectory(dir=self.temp_base) as td:
            root = Path(td)
            (root / "transcript.md").write_text(
                "# temporary fixture\n"
                "## Assistant turn 1\n"
                "Some tutor message text here.\n"
                "## Learner turn 1\n"
                "Some learner text.\n",
                encoding="utf-8",
            )
            base = {
                "format": "live-run-annotation",
                "version": 1,
                "case_id": "L-01",
                "run": 1,
                "judge": "synthetic temporary judge",
                "transcript": "transcript.md",
                "must": [
                    {"index": i, "observed": True, "turns": [1], "quote": "Some tutor message text here."}
                    for i in range(4)
                ],
                "must_not": [{"index": i, "violation": False} for i in range(4)],
                "automatic_fails": [],
                "severe": [],
                "dimensions": {},
            }
            mutate(base)
            path = root / "annotation.json"
            path.write_text(json.dumps(base), encoding="utf-8")
            return run_annotation(path)

    def assert_invalid(self, code, output, fragment):
        self.assertEqual(code, 2)
        self.assertIn("INVALID", output)
        self.assertIn(fragment, output)

    def test_unknown_annotation_field_rejected(self):
        code, output = self.temp_annotation(lambda base: base.update(extra=1))
        self.assert_invalid(code, output, "unknown annotation fields")

    def test_unknown_entry_field_rejected(self):
        code, output = self.temp_annotation(lambda base: base["must"][0].update(made_up=1))
        self.assert_invalid(code, output, "unknown entry fields")

    def test_malformed_json_rejected(self):
        with tempfile.TemporaryDirectory(dir=self.temp_base) as td:
            path = Path(td) / "annotation.json"
            path.write_text("{not json", encoding="utf-8")
            code, output = run_annotation(path)
        self.assert_invalid(code, output, "malformed JSON")

    def test_missing_transcript_rejected(self):
        code, output = self.temp_annotation(lambda base: base.update(transcript="absent.md"))
        self.assert_invalid(code, output, "transcript")

    def test_observed_without_quote_rejected(self):
        code, output = self.temp_annotation(lambda base: base["must"][0].pop("quote"))
        self.assert_invalid(code, output, "quote")

    def test_turn_out_of_range_rejected(self):
        code, output = self.temp_annotation(lambda base: base["must"][0].update(turns=[7]))
        self.assert_invalid(code, output, "does not exist")

    def test_missing_must_not_judgment_rejected(self):
        code, output = self.temp_annotation(lambda base: base.update(must_not=base["must_not"][:3]))
        self.assert_invalid(code, output, "must_not")

    def test_invalid_dimension_value_rejected(self):
        code, output = self.temp_annotation(lambda base: base.update(dimensions={"D1": 5}))
        self.assert_invalid(code, output, "dimension D1")

    def test_unknown_dimension_rejected(self):
        code, output = self.temp_annotation(lambda base: base.update(dimensions={"D9": 2}))
        self.assert_invalid(code, output, "unknown dimension")

    def test_wrong_case_id_rejected(self):
        code, output = self.temp_annotation(lambda base: base.update(case_id="L-99"))
        self.assert_invalid(code, output, "unknown case_id")

    def test_boolean_numbers_and_nonstring_case_ids_are_rejected(self):
        for mutate, fragment in (
            (lambda base: base.update(version=True), "version"),
            (lambda base: base.update(run=True), "run"),
            (lambda base: base["must"][0].update(index=False), "index"),
            (lambda base: base["must"][0].update(turns=[True]), "integers"),
            (lambda base: base.update(dimensions={"D1": True}), "dimension"),
            (lambda base: base.update(case_id=[]), "case_id"),
        ):
            with self.subTest(fragment=fragment):
                code, output = self.temp_annotation(mutate)
                self.assert_invalid(code, output, fragment)

    def test_directory_is_not_a_transcript(self):
        code, output = self.temp_annotation(lambda base: base.update(transcript="."))
        self.assert_invalid(code, output, "transcript")

    def test_malformed_case_shape_is_invalid_not_a_traceback(self):
        with tempfile.TemporaryDirectory(dir=self.temp_base) as td:
            path = Path(td) / "cases.json"
            path.write_text(json.dumps({"version": 1, "cases": [None]}), encoding="utf-8")
            output = io.StringIO()
            with redirect_stdout(output), redirect_stderr(io.StringIO()):
                code = check_run.main(["--cases", str(path), "--annotation", str(FIXTURES / "l08-correction/annotation.json")])
            self.assert_invalid(code, output.getvalue(), "cases")

    def test_copied_harness_cases_and_holdout_still_validate(self):
        script = LIVE / "check_cases.py"
        result = subprocess.run(
            [sys.executable, "-B", str(script), "--cases", str(CASES), "--verify-holdout"],
            cwd=str(HERE), capture_output=True, text=True, encoding="utf-8", check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("holdout verified", result.stdout)


if __name__ == "__main__":
    unittest.main()
