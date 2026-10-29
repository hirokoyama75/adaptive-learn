"""Behavior tests at the user-confirmed public helper interface."""

import os
import json
from pathlib import Path
import sys
import tempfile
import unittest
import subprocess
import shutil
from datetime import datetime, timezone
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import learn_state
from learn_state import LearningError, initialize, resume, save


class StateTests(unittest.TestCase):
    def setUp(self):
        clock = learn_state._clock
        fixed_clock = patch("learn_state._clock", side_effect=lambda now=None:
                            clock(now if now is not None else datetime(2028, 1, 1, tzinfo=timezone.utc)))
        fixed_clock.start()
        self.addCleanup(fixed_clock.stop)
        preferred = Path(os.environ.get("LOCALAPPDATA", "")) / "Temp" / "opencode"
        self.temp = tempfile.TemporaryDirectory(
            prefix="adaptive-learn-", dir=preferred if preferred.is_dir() else None
        )
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "learning"

    def test_setup_creates_an_explicit_private_subject(self):
        result = initialize(self.root, "algebra")
        self.assertEqual(result["revision"], 0)
        self.assertTrue((self.root / "LEARNER.md").read_text(encoding="utf-8").startswith("<!-- adaptive-learn:1 -->"))
        rules = (self.root / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("/LEARNER.md\n", rules)
        self.assertIn("/algebra/.learning/\n", rules)
        self.assertTrue((self.root / "algebra/.learning/state.json").is_file())
        packet = resume(self.root, "algebra")
        self.assertEqual(packet["mode"], "class")
        self.assertIsNone(packet["constraints"]["deadline"])
        self.assertIsNone(packet["checkpoint"])

    def checkpoint(self, target="equations"):
        return {"task_id": "equation-1", "targets": [target], "prompt": "Solve 3x + 2 = 14.",
                "assessment": {"kind": "objective", "solution": "x = 4", "criteria": ["Preserve equality"]},
                "attempt": "3x = 12", "support": ["Subtract 2 from both sides."], "allowed_aids": [],
                "bottleneck": "Which operation reverses multiplication?", "plan_position": "First equation",
                "next_action": "Wait for the final step", "context": "One hint already supplied.", "source_ref": None}

    def test_task_handoff_survives_a_new_chat(self):
        initialize(self.root, "algebra")
        result = save(self.root, "algebra", {
            "expected_revision": 0, "goal": "Solve linear equations", "mode": "depth",
            "nodes": {"equations": {"kind": "skill", "label": "Solve equations"}},
            "checkpoint": self.checkpoint(),
            "plan": [{"target": "equations", "action": "Solve without help", "status": "current"}]
        })
        self.assertTrue(result["saved"])
        self.assertEqual(result["revision"], 1)
        packet = resume(self.root, "algebra")
        self.assertEqual(packet["checkpoint"], self.checkpoint())
        self.assertEqual(packet["goal"], "Solve linear equations")
        self.assertEqual(packet["mode"], "depth")
        self.assertEqual(packet["graph"]["nodes"]["equations"]["kind"], "skill")

    def event(self, event_id="e1", **changes):
        result = {"id": event_id, "target": "provisional:equations", "at": "2026-10-27T10:00:00+00:00",
                  "kind": "performance", "task_type": "solve", "context": "No method named",
                  "outcome": "correct", "independence": "independent", "assistance": [], "cues": [],
                  "allowed_aids": [], "summary": "Solved correctly with equal operations on both sides.",
                  "confidence": None, "importance": "normal", "after_gap": False}
        result.update(changes)
        return result

    def test_successes_are_reviewed_and_later_independent_retrieval_extends_spacing(self):
        initialize(self.root, "algebra")
        save(self.root, "algebra", {"expected_revision": 0, "evidence": [self.event()]})
        future = datetime(2026, 11, 10, tzinfo=timezone.utc)
        review = resume(self.root, "algebra", now=future)["reviews"][0]
        self.assertEqual(review["due_at"], "2026-10-28T10:00:00+00:00")
        self.assertEqual(review["last_evidence"], "e1")
        save(self.root, "algebra", {"expected_revision": 1, "evidence": [self.event(
            "e2", at="2026-10-28T10:00:00+00:00", kind="retrieval", after_gap=True)]})
        review = resume(self.root, "algebra", now=future)["reviews"][0]
        self.assertEqual(review["due_at"], "2026-10-30T10:00:00+00:00")
        self.assertEqual(review["interval_days"], 2)
        save(self.root, "algebra", {"expected_revision": 2, "evidence": [self.event(
            "e3", at="2026-10-30T10:00:00+00:00", independence="assisted", assistance=["Tutor named the next operation"])]})
        review = resume(self.root, "algebra", now=future)["reviews"][0]
        self.assertEqual(review["interval_days"], 1)
        self.assertEqual(review["last_evidence"], "e3")

    def test_independent_practice_extends_spacing_only_after_a_gap_and_when_due(self):
        initialize(self.root, "algebra")
        future = datetime(2027, 2, 1, tzinfo=timezone.utc)
        for revision, (at, after_gap, interval, due) in enumerate([
            ("2026-10-27T10:00:00Z", False, 1, "2026-10-28T10:00:00+00:00"),
            ("2026-10-27T11:00:00Z", True, 1, "2026-10-28T11:00:00+00:00"),
            ("2026-10-28T11:00:00Z", False, 1, "2026-10-29T11:00:00+00:00"),
            ("2026-10-29T11:00:00Z", True, 2, "2026-10-31T11:00:00+00:00"),
            ("2026-11-01T11:00:00Z", True, 4, "2026-11-05T11:00:00+00:00"),
            ("2026-11-05T11:00:00Z", True, 8, "2026-11-13T11:00:00+00:00"),
            ("2026-11-13T11:00:00Z", True, 16, "2026-11-29T11:00:00+00:00"),
            ("2026-11-29T11:00:00Z", True, 30, "2026-12-29T11:00:00+00:00"),
            ("2026-12-29T11:00:00Z", True, 30, "2027-01-28T11:00:00+00:00"),
        ]):
            with self.subTest(revision=revision):
                save(self.root, "algebra", {"expected_revision": revision, "evidence": [self.event(
                    f"practice{revision}", at=at, after_gap=after_gap)]})
                review = resume(self.root, "algebra", now=future)["reviews"][0]
                self.assertEqual(review["interval_days"], interval)
                self.assertEqual(review["due_at"], due)

    def test_low_importance_successes_preserve_prior_repairs_and_important_successes(self):
        future = datetime(2026, 11, 10, tzinfo=timezone.utc)
        for outcome in ("incorrect", "correct"):
            with self.subTest(outcome=outcome):
                root = self.root / outcome
                initialize(root, "algebra")
                save(root, "algebra", {"expected_revision": 0, "evidence": [self.event(outcome=outcome)]})
                original = resume(root, "algebra", now=future)["reviews"]
                self.assertEqual(len(original), 1)
                for revision in (1, 2):
                    save(root, "algebra", {"expected_revision": revision, "evidence": [self.event(
                        f"low{revision}", at=f"2026-10-{27 + revision}T10:00:00Z", importance="low", after_gap=True)]})
                    packet = resume(root, "algebra", now=future)
                    self.assertEqual(packet["reviews"], original)
                    self.assertEqual(len(packet["evidence"]), revision + 1)

    def test_low_importance_success_alone_creates_no_review(self):
        initialize(self.root, "algebra")
        save(self.root, "algebra", {"expected_revision": 0, "evidence": [self.event(importance="low")]})
        self.assertEqual(resume(self.root, "algebra", now=datetime(2026, 11, 10, tzinfo=timezone.utc))["reviews"], [])

    def test_false_tutor_error_is_invalidated_without_rewriting_old_evidence(self):
        initialize(self.root, "algebra")
        save(self.root, "algebra", {"expected_revision": 0, "evidence": [self.event(outcome="incorrect")]})
        reason = "Tutor misgraded an equivalent valid expression."
        save(self.root, "algebra", {"expected_revision": 1,
                                    "invalidations": [{"evidence_id": "e1", "reason": reason}]})
        packet = resume(self.root, "algebra", now=datetime(2026, 11, 10, tzinfo=timezone.utc))
        self.assertEqual(packet["reviews"], [])
        self.assertEqual(packet["evidence"][0]["invalidated"], reason)
        self.assertEqual(packet["evidence"][0]["outcome"], "incorrect")
        self.assertEqual(packet["evidence"][0]["summary"], self.event()["summary"])

    def test_cram_review_waits_for_intervening_work_and_can_be_suspended(self):
        initialize(self.root, "algebra")
        now = datetime(2026, 10, 27, 12, tzinfo=timezone.utc)
        save(self.root, "algebra", {"expected_revision": 0, "mode": "cram", "evidence": [self.event()]})
        self.assertEqual(resume(self.root, "algebra", now=now)["reviews"], [])
        save(self.root, "algebra", {"expected_revision": 1, "evidence": [self.event(
            "e2", target="provisional:units", at="2026-10-27T11:00:00+00:00")]})
        self.assertEqual([item["target"] for item in resume(self.root, "algebra", now=now)["reviews"]], ["provisional:equations"])
        save(self.root, "algebra", {"expected_revision": 2, "review_actions": [
            {"target": "provisional:equations", "action": "pause", "reason": "Learner is focusing on units today"}]})
        self.assertEqual(resume(self.root, "algebra", now=now)["reviews"], [])
        save(self.root, "algebra", {"expected_revision": 3, "evidence": [self.event(
            "e3", at="2026-10-27T11:30:00+00:00")]})
        later = datetime(2026, 11, 1, tzinfo=timezone.utc)
        self.assertNotIn("provisional:equations", [item["target"] for item in resume(self.root, "algebra", now=later)["reviews"]])
        save(self.root, "algebra", {"expected_revision": 4, "review_actions": [
            {"target": "provisional:equations", "action": "resume", "reason": "Return to equations"}]})
        self.assertIn("provisional:equations", [item["target"] for item in resume(self.root, "algebra", now=later)["reviews"]])

    def test_joint_arguments_are_preserved_and_prerequisite_cycles_are_rejected_before_writes(self):
        initialize(self.root, "logic")
        save(self.root, "logic", {"expected_revision": 0,
            "nodes": {key: {"kind": "concept", "label": key} for key in ("A", "B", "C", "D", "E")},
            "arguments": {"arg-one": {"premises": ["A", "B"], "conclusion": "E", "kind": "deductive"},
                          "arg-two": {"premises": ["C", "D"], "conclusion": "E", "kind": "empirical"},
                          "arg-back": {"premises": ["E"], "conclusion": "A", "kind": "empirical"}},
            "prerequisites": [{"target": "E", "requires": "A"}, {"target": "A", "requires": "B"}]})
        packet = resume(self.root, "logic", targets=["A", "B", "C", "D", "E"])
        self.assertEqual(packet["graph"]["arguments"]["arg-one"]["premises"], ["A", "B"])
        self.assertEqual(packet["graph"]["arguments"]["arg-two"]["premises"], ["C", "D"])
        folder = self.root / "logic/.learning"
        before = {name: (folder / name).read_bytes() for name in ("state.json", "graph.json")}
        with self.assertRaises(LearningError):
            save(self.root, "logic", {"expected_revision": 1,
                "nodes": {"unused": {"kind": "concept", "label": "Must not be written"}},
                "prerequisites": [{"target": "B", "requires": "E"}]})
        for name, value in before.items():
            self.assertEqual((folder / name).read_bytes(), value)

    def test_resume_is_bounded_but_never_truncates_the_active_task(self):
        initialize(self.root, "history")
        nodes = {f"topic{i}": {"kind": "concept", "label": f"Topic {i}"} for i in range(30)}
        events = [self.event(f"e{i}", target=f"topic{i}", summary="Detailed relevant evidence. " * 40) for i in range(30)]
        checkpoint = self.checkpoint("topic0")
        save(self.root, "history", {"expected_revision": 0, "nodes": nodes,
                                    "evidence": events, "checkpoint": checkpoint})
        packet = resume(self.root, "history", max_chars=6000, now=datetime(2026, 11, 10, tzinfo=timezone.utc))
        self.assertLessEqual(len(json.dumps(packet, ensure_ascii=False, indent=2) + "\n"), 6000)
        self.assertEqual(packet["checkpoint"], checkpoint)
        self.assertLessEqual(len(packet["graph"]["nodes"]), 8)
        self.assertGreater(packet["omitted"]["evidence"], 0)
        self.assertGreater(packet["omitted"]["due_reviews"], 0)
        large = self.checkpoint("topic0")
        large["prompt"] = "An essential long problem. " * 300
        save(self.root, "history", {"expected_revision": 1, "checkpoint": large})
        with self.assertRaisesRegex(LearningError, "checkpoint|budget"):
            resume(self.root, "history", max_chars=2048)
        self.assertEqual(resume(self.root, "history")["checkpoint"], large)

    def test_interrupted_state_replacement_preserves_old_checkpoint_and_allows_retry(self):
        initialize(self.root, "algebra")
        folder = self.root / "algebra/.learning"
        old_state = (folder / "state.json").read_bytes()
        request = {"expected_revision": 0, "nodes": {"equations": {"kind": "skill", "label": "Equations"}},
                   "checkpoint": self.checkpoint()}
        real_replace = os.replace

        def interrupted(source, destination):
            if Path(destination).name == "state.json":
                raise OSError("Simulated interruption at canonical state replacement")
            return real_replace(source, destination)

        with patch("os.replace", side_effect=interrupted):
            with self.assertRaises(LearningError):
                save(self.root, "algebra", request)
        self.assertEqual((folder / "state.json").read_bytes(), old_state)
        packet = resume(self.root, "algebra", targets=["equations"])
        self.assertEqual(packet["revision"], 0)
        self.assertIsNone(packet["checkpoint"])
        self.assertIn("equations", packet["graph"]["nodes"])
        self.assertEqual(list(self.root.rglob(".adaptive-*.tmp")), [])
        self.assertEqual(save(self.root, "algebra", request)["revision"], 1)
        self.assertEqual(resume(self.root, "algebra")["checkpoint"], self.checkpoint())

    def test_interrupted_withdrawal_warns_about_graph_changes_and_allows_retry(self):
        initialize(self.root, "algebra")
        save(self.root, "algebra", {"expected_revision": 0,
            "nodes": {"equations": {"kind": "skill", "label": "Equations"}},
            "evidence": [self.event(target="equations", outcome="incorrect")]})
        folder = self.root / "algebra/.learning"
        before = (folder / "state.json").read_bytes()
        request = {"expected_revision": 1,
            "withdrawals": [{"id": "equations", "reason": "Tutor's rule was wrong", "replacement": None}],
            "invalidations": [{"evidence_id": "e1", "reason": "Task used the wrong rule"}]}
        real_replace = os.replace

        def interrupted(source, destination):
            if Path(destination).name == "state.json":
                raise OSError("Simulated state replacement failure")
            return real_replace(source, destination)

        with patch("os.replace", side_effect=interrupted):
            with self.assertRaisesRegex(LearningError, "Graph changes were written.*state save is unconfirmed"):
                save(self.root, "algebra", request)
        self.assertEqual((folder / "state.json").read_bytes(), before)
        packet = resume(self.root, "algebra", targets=["equations"], now=datetime(2026, 11, 10, tzinfo=timezone.utc))
        self.assertEqual(packet["graph"]["nodes"]["equations"]["withdrawn"], "Tutor's rule was wrong")
        self.assertIsNone(packet["evidence"][0]["invalidated"])
        self.assertEqual(packet["reviews"], [])
        self.assertEqual(list(self.root.rglob(".adaptive-*.tmp")), [])
        self.assertEqual(save(self.root, "algebra", request)["revision"], 2)
        self.assertEqual(resume(self.root, "algebra", targets=["equations"])["evidence"][0]["invalidated"],
                         "Task used the wrong rule")

    def test_command_line_setup_save_resume_and_errors(self):
        helper = Path(__file__).resolve().parents[1] / "scripts/learn_state.py"
        common = ["--root", str(self.root / "course folder"), "--subject", "algebra"]

        def run(command, extra=(), data=None):
            return subprocess.run([sys.executable, "-B", str(helper), command, *common, *extra],
                                  input=data, capture_output=True, text=True, encoding="utf-8", check=False,
                                  env={**os.environ, "PYTHONIOENCODING": "utf-8"})

        result = run("init")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["revision"], 0)
        request = json.dumps({"expected_revision": 0, "goal": "理解 equations", "mode": "depth"}, ensure_ascii=False)
        result = run("save", ["--input", "-"], request)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout)["saved"])
        result = run("resume", ["--review-limit", "0"])
        self.assertEqual(json.loads(result.stdout)["goal"], "理解 equations")
        result = run("save", ["--input", "-"], request)
        self.assertEqual(result.returncode, 2)
        self.assertIn("Stale revision", json.loads(result.stderr)["error"])
        self.assertEqual(result.stdout, "")

    def test_repeated_setup_preserves_profile_progress_and_existing_ignore_rules(self):
        self.root.mkdir()
        rules = b"# User rules\r\n/private-data\r\n"
        (self.root / ".gitignore").write_bytes(rules)
        initialize(self.root, "algebra")
        profile = self.root / "LEARNER.md"
        profile.write_text(profile.read_text(encoding="utf-8") + "\nPrefer concrete examples.\n", encoding="utf-8")
        before_profile = profile.read_bytes()
        save(self.root, "algebra", {"expected_revision": 0, "goal": "Keep this goal"})
        state_path = self.root / "algebra/.learning/state.json"
        before_state = state_path.read_bytes()
        self.assertFalse(initialize(self.root, "algebra")["initialized"])
        initialize(self.root, "physics")
        self.assertEqual(profile.read_bytes(), before_profile)
        self.assertEqual(state_path.read_bytes(), before_state)
        current_rules = (self.root / ".gitignore").read_bytes()
        self.assertTrue(current_rules.startswith(rules))
        self.assertEqual(current_rules.count(b"/algebra/.learning/"), 1)
        self.assertIn(b"/physics/.learning/", current_rules)

    def test_unfamiliar_profile_is_not_overwritten_or_adopted(self):
        self.root.mkdir()
        profile = self.root / "LEARNER.md"
        profile.write_text("Personal document, not a learning marker", encoding="utf-8")
        with self.assertRaises(LearningError):
            initialize(self.root, "algebra")
        self.assertEqual(profile.read_text(encoding="utf-8"), "Personal document, not a learning marker")
        self.assertFalse((self.root / ".gitignore").exists())

    def test_invalid_existing_formats_fail_without_resetting_them(self):
        initialize(self.root, "algebra")
        path = self.root / "algebra/.learning/state.json"
        original = path.read_text(encoding="utf-8")
        future = json.loads(original)
        future["format_version"] = 99
        extra = json.loads(original)
        extra["future_field"] = "must not be discarded"
        damaged = [json.dumps(future), json.dumps(extra), '{"format_version":1,',
                   original.replace('"revision": 0', '"revision": 0, "revision": 1'),
                   original.replace('"revision": 0', '"revision": NaN')]
        for contents in damaged:
            with self.subTest(contents=contents[:60]):
                path.write_text(contents, encoding="utf-8")
                with self.assertRaises(LearningError):
                    initialize(self.root, "algebra")
                with self.assertRaises(LearningError):
                    save(self.root, "algebra", {"expected_revision": 0})
                self.assertEqual(path.read_text(encoding="utf-8"), contents)
        path.write_text(original, encoding="utf-8")

    def test_invalid_updates_never_write_graph_additions_or_state(self):
        initialize(self.root, "algebra")
        folder = self.root / "algebra/.learning"
        before = {name: (folder / name).read_bytes() for name in ("state.json", "graph.json")}
        bad_updates = [
            {"expected_revision": True},
            {"checkpoint": self.checkpoint("missing")},
            {"evidence": [self.event(assistance=["A hint"], independence="independent")]},
            {"evidence": [self.event(kind="self_report")]},
            {"evidence": [self.event(kind="retrieval", after_gap=False)]},
            {"evidence": [self.event(), self.event()]},
            {"prerequisites": [{"target": "new", "requires": "missing"}]},
            {"arguments": {"bad": {"premises": ["new"], "conclusion": "missing", "kind": "deductive"}}},
            {"constraints": {"deadline": "tomorrow", "study_minutes": None, "scope": [], "scope_status": "unknown", "scope_source": None}},
            {"constraints": []},
            {"mode": "mastered"},
            {"invalidations": [{"evidence_id": "missing", "reason": "No such event"}]},
            {"unknown_field": "do not discard"},
        ]
        for bad in bad_updates:
            with self.subTest(update=bad):
                request = {"expected_revision": 0, "nodes": {"new": {"kind": "skill", "label": "New target"}}, **bad}
                with self.assertRaises(LearningError):
                    save(self.root, "algebra", request)
                for name, value in before.items():
                    self.assertEqual((folder / name).read_bytes(), value)

    def test_revision_changed_after_load_refuses_before_writing_a_withdrawal(self):
        initialize(self.root, "algebra")
        save(self.root, "algebra", {"expected_revision": 0,
            "nodes": {"equations": {"kind": "skill", "label": "Equations"}}})
        stale = learn_state._load(self.root, "algebra")
        save(self.root, "algebra", {"expected_revision": 1, "goal": "Another writer's update"})
        folder = self.root / "algebra/.learning"
        before = {name: (folder / name).read_bytes() for name in ("graph.json", "state.json")}
        with patch("learn_state._load", return_value=stale):
            with self.assertRaisesRegex(LearningError, "State changed during save"):
                save(self.root, "algebra", {"expected_revision": 1, "withdrawals": [
                    {"id": "equations", "reason": "Stale proposed correction", "replacement": None}]})
        for name, value in before.items():
            self.assertEqual((folder / name).read_bytes(), value)

    def test_revision_change_after_graph_write_is_still_refused(self):
        initialize(self.root, "algebra")
        real_write = learn_state._atomic_write

        def concurrent_save(root, path, text):
            real_write(root, path, text)
            if path.name == "graph.json":
                save(root, "algebra", {"expected_revision": 0, "goal": "Another writer's update"})

        with patch("learn_state._atomic_write", side_effect=concurrent_save):
            with self.assertRaisesRegex(LearningError, "Graph changes were written.*State changed during save"):
                save(self.root, "algebra", {"expected_revision": 0,
                    "nodes": {"equations": {"kind": "skill", "label": "Equations"}}})
        packet = resume(self.root, "algebra", targets=["equations"])
        self.assertEqual(packet["revision"], 1)
        self.assertEqual(packet["goal"], "Another writer's update")
        self.assertIn("equations", packet["graph"]["nodes"])

    def test_visited_plan_exposure_and_self_report_are_not_performance(self):
        initialize(self.root, "algebra")
        save(self.root, "algebra", {"expected_revision": 0,
            "plan": [{"target": "provisional:equations", "action": "Read an explanation", "status": "visited"}],
            "evidence": [self.event("e1", kind="exposure", outcome="unassessed", independence="unknown"),
                         self.event("e2", kind="self_report", outcome="unassessed", independence="unknown")]})
        packet = resume(self.root, "algebra")
        self.assertEqual(packet["reviews"], [])
        self.assertTrue(all(event["independence"] == "unknown" for event in packet["evidence"]))

    def test_node_withdrawal_retains_ids_and_removes_review_recommendations(self):
        initialize(self.root, "logic")
        save(self.root, "logic", {"expected_revision": 0,
            "nodes": {"old": {"kind": "proposition", "label": "Wrong rule", "statement": "An explicitly erroneous example rule."}},
            "evidence": [self.event(target="old", outcome="incorrect")]})
        save(self.root, "logic", {"expected_revision": 1,
            "nodes": {"new": {"kind": "proposition", "label": "Corrected rule", "statement": "The replacement qualified rule.", "qualifications": ["Under the stated model"]}},
            "withdrawals": [{"id": "old", "reason": "Tutor's rule was wrong", "replacement": "new"}],
            "invalidations": [{"evidence_id": "e1", "reason": "Task relied on the withdrawn rule"}]})
        packet = resume(self.root, "logic", targets=["old", "new"])
        self.assertEqual(packet["reviews"], [])
        self.assertEqual(packet["graph"]["nodes"]["old"]["replacement"], "new")
        self.assertEqual(packet["graph"]["nodes"]["old"]["statement"], "An explicitly erroneous example rule.")
        self.assertTrue(packet["warnings"])
        with self.assertRaises(LearningError):
            save(self.root, "logic", {"expected_revision": 2, "nodes": {"old": {"kind": "concept", "label": "Reuse old ID"}}})

    def test_cross_subject_links_resolve_without_copying_evidence(self):
        initialize(self.root, "math")
        initialize(self.root, "physics")
        save(self.root, "math", {"expected_revision": 0, "nodes": {"units": {"kind": "concept", "label": "Units"}},
                                "evidence": [self.event(target="units")]})
        save(self.root, "physics", {"expected_revision": 0, "nodes": {"dimensions": {"kind": "skill", "label": "Check dimensions"}},
            "links": [{"target": "dimensions", "subject": "math", "target_id": "units"}]})
        packet = resume(self.root, "physics", targets=["dimensions"])
        self.assertEqual(packet["evidence"], [])
        self.assertEqual(packet["graph"]["links"][0]["subject"], "math")
        for subject, target in (("../outside", "units"), ("math", "absent")):
            with self.subTest(subject=subject):
                with self.assertRaises(LearningError):
                    save(self.root, "physics", {"expected_revision": 1,
                        "links": [{"target": "dimensions", "subject": subject, "target_id": target}]})

    def test_unsafe_subjects_and_the_skill_directory_are_rejected(self):
        for subject in ("../escape", "C:\\escape", "two/parts", "CON", "nul", "", "a b", ".."):
            with self.subTest(subject=subject):
                with self.assertRaises(LearningError):
                    initialize(self.root, subject)
        skill_root = Path(__file__).resolve().parents[1]
        with self.assertRaises(LearningError):
            initialize(skill_root, "learner")
        self.assertFalse(self.root.exists())

    def test_linked_subject_cannot_escape_the_selected_root(self):
        self.root.mkdir()
        outside = Path(self.temp.name) / "outside"
        outside.mkdir()
        link = self.root / "linked"
        try:
            link.symlink_to(outside, target_is_directory=True)
        except OSError:
            if os.name != "nt":
                self.skipTest("Directory links are not permitted on this host")
            result = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(outside)], capture_output=True, check=False)
            if result.returncode:
                self.skipTest("Neither symlink nor junction creation is permitted")
        with self.assertRaises(LearningError):
            initialize(self.root, "linked")
        self.assertEqual(list(outside.iterdir()), [])
        self.assertFalse((self.root / "LEARNER.md").exists())

    def test_unfamiliar_derived_plan_is_left_alone_after_a_successful_save(self):
        initialize(self.root, "algebra")
        path = self.root / "algebra/.learning/plan.md"
        path.write_text("User-owned plan. Do not replace.", encoding="utf-8")
        result = save(self.root, "algebra", {"expected_revision": 0, "goal": "Persist this"})
        self.assertTrue(result["saved"])
        self.assertTrue(result["warnings"])
        self.assertEqual(path.read_text(encoding="utf-8"), "User-owned plan. Do not replace.")
        self.assertEqual(resume(self.root, "algebra")["goal"], "Persist this")

    def test_session_summary_records_learning_evidence_without_replaying_the_task(self):
        initialize(self.root, "algebra")
        save(self.root, "algebra", {"expected_revision": 0, "checkpoint": self.checkpoint("provisional:equations"),
                                    "evidence": [self.event()]})
        notes = list((self.root / "algebra/.learning/sessions").glob("*.md"))
        self.assertEqual(len(notes), 1)
        text = notes[0].read_text(encoding="utf-8")
        self.assertIn("e1", text)
        self.assertIn("independent", text)
        self.assertIn(self.event()["summary"], text)
        self.assertNotIn(self.checkpoint()["prompt"], text)
        self.assertNotIn(self.checkpoint()["assessment"]["solution"], text)

    def test_suspension_survives_a_low_importance_success_and_new_error(self):
        initialize(self.root, "algebra")
        save(self.root, "algebra", {"expected_revision": 0, "evidence": [self.event(outcome="incorrect")]})
        save(self.root, "algebra", {"expected_revision": 1, "review_actions": [
            {"target": "provisional:equations", "action": "pause", "reason": "Not a current priority"}]})
        save(self.root, "algebra", {"expected_revision": 2, "evidence": [self.event(
            "e2", at="2026-10-28T10:00:00+00:00", importance="low")]})
        save(self.root, "algebra", {"expected_revision": 3, "evidence": [self.event(
            "e3", at="2026-10-29T10:00:00+00:00", outcome="incorrect")]})
        self.assertEqual(resume(self.root, "algebra", now=datetime(2026, 11, 10, tzinfo=timezone.utc))["reviews"], [])

    def test_excessively_nested_json_fails_clearly_without_reinitializing(self):
        initialize(self.root, "algebra")
        path = self.root / "algebra/.learning/state.json"
        contents = "[" * 2000 + "0" + "]" * 2000
        path.write_text(contents, encoding="utf-8")
        with self.assertRaises(LearningError):
            resume(self.root, "algebra")
        self.assertEqual(path.read_text(encoding="utf-8"), contents)

    def git(self, *arguments):
        executable = shutil.which("git")
        if not executable:
            self.skipTest("Git is not available; no installation attempted")
        return subprocess.run([executable, "-C", str(self.root), *arguments], capture_output=True,
                              text=True, encoding="utf-8", check=False)

    def test_git_privacy_rules_work_and_existing_tracking_is_only_reported(self):
        self.root.mkdir()
        self.assertEqual(self.git("init", "--quiet").returncode, 0)
        initialize(self.root, "algebra")
        for path in ("LEARNER.md", "algebra/.learning/state.json"):
            self.assertEqual(self.git("check-ignore", "--quiet", "--", path).returncode, 0)
        self.assertEqual(self.git("add", "-f", "--", "LEARNER.md").returncode, 0)
        result = initialize(self.root, "algebra")
        self.assertTrue(any("already tracked" in warning for warning in result["warnings"]))
        self.assertIn("LEARNER.md", self.git("ls-files", "--", "LEARNER.md").stdout)

    def test_overriding_git_rules_trigger_a_privacy_warning_without_overwriting_user_rules(self):
        self.root.mkdir()
        self.assertEqual(self.git("init", "--quiet").returncode, 0)
        subject = self.root / "algebra"
        subject.mkdir()
        rules = subject / ".gitignore"
        rules.write_text("!.learning/\n", encoding="utf-8")
        result = initialize(self.root, "algebra")
        self.assertEqual(self.git("check-ignore", "--quiet", "--", "algebra/.learning/state.json").returncode, 1)
        self.assertTrue(any("unignored" in warning for warning in result["warnings"]))
        self.assertEqual(rules.read_text(encoding="utf-8"), "!.learning/\n")

    def test_early_same_day_retrieval_does_not_inflate_later_spacing(self):
        initialize(self.root, "algebra")
        save(self.root, "algebra", {"expected_revision": 0, "evidence": [self.event()]})
        save(self.root, "algebra", {"expected_revision": 1, "evidence": [self.event(
            "e2", at="2026-10-27T11:00:00+00:00", kind="retrieval", after_gap=True)]})
        review = resume(self.root, "algebra", now=datetime(2026, 11, 10, tzinfo=timezone.utc))["reviews"][0]
        self.assertEqual(review["interval_days"], 1)
        self.assertEqual(review["due_at"], "2026-10-28T11:00:00+00:00")

    def test_a_save_cannot_exceed_the_documented_readable_file_size(self):
        initialize(self.root, "algebra")
        events = [self.event(f"e{i}", context="c" * 4000, summary="s" * 4000, importance="low") for i in range(1100)]
        save(self.root, "algebra", {"expected_revision": 0, "evidence": events})
        path = self.root / "algebra/.learning/state.json"
        before = path.read_bytes()
        extra = [self.event(f"f{i}", context="c" * 4000, summary="s" * 4000, importance="low") for i in range(1100)]
        with self.assertRaisesRegex(LearningError, "16 MiB"):
            save(self.root, "algebra", {"expected_revision": 1, "evidence": extra})
        self.assertEqual(path.read_bytes(), before)
        self.assertEqual(resume(self.root, "algebra", evidence_limit=0)["revision"], 1)

    def test_cli_character_budget_includes_the_actual_serialized_output(self):
        initialize(self.root, "algebra")
        save(self.root, "algebra", {"expected_revision": 0, "goal": "g" * 1000})
        packet = resume(self.root, "algebra", review_limit=0)
        budget = len(json.dumps(packet, ensure_ascii=False, indent=2) + "\n")
        helper = Path(__file__).resolve().parents[1] / "scripts/learn_state.py"
        result = subprocess.run([sys.executable, "-B", str(helper), "resume", "--root", str(self.root),
                                 "--subject", "algebra", "--review-limit", "0", "--max-chars", str(budget)],
                                capture_output=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertLessEqual(len(result.stdout.decode("utf-8")), budget)

    def test_far_exam_keeps_class_spacing_and_near_exam_changes_urgency_not_mode(self):
        initialize(self.root, "algebra")
        constraints = {"deadline": "2027-01-27", "study_minutes": 60, "scope": ["Equations", "Units"],
                       "scope_status": "provisional", "scope_source": "Supplied practice paper"}
        save(self.root, "algebra", {"expected_revision": 0, "constraints": constraints, "evidence": [self.event()]})
        future = datetime(2026, 10, 29, tzinfo=timezone.utc)
        packet = resume(self.root, "algebra", now=future)
        self.assertEqual(packet["mode"], "class")
        self.assertIsNone(packet["reviews"][0]["after_evidence_id"])
        constraints["deadline"] = "2026-10-27"
        save(self.root, "algebra", {"expected_revision": 1, "constraints": constraints,
            "evidence": [self.event("e2", target="provisional:units", at="2026-10-27T11:00:00+00:00")]})
        packet = resume(self.root, "algebra", now=datetime(2026, 10, 27, 12, tzinfo=timezone.utc))
        self.assertEqual(packet["mode"], "class")
        self.assertEqual(packet["reviews"][0]["after_evidence_id"], "e1")
        save(self.root, "algebra", {"expected_revision": 2, "evidence": [self.event("e3", at="2026-10-28T10:00:00+00:00")]})
        reviews = resume(self.root, "algebra", now=datetime(2026, 11, 10, tzinfo=timezone.utc))["reviews"]
        equation_review = next(item for item in reviews if item["target"] == "provisional:equations")
        self.assertEqual(equation_review["due_at"], "2026-10-29T10:00:00+00:00")

    def test_derived_view_io_failure_does_not_hide_a_successful_canonical_save(self):
        initialize(self.root, "algebra")
        real_replace = os.replace

        def fail_plan(source, destination):
            if Path(destination).name == "plan.md":
                raise OSError("Simulated derived-plan failure")
            return real_replace(source, destination)

        with patch("os.replace", side_effect=fail_plan):
            result = save(self.root, "algebra", {"expected_revision": 0, "goal": "This was saved"})
        self.assertTrue(result["saved"])
        self.assertTrue(any("derived" in warning for warning in result["warnings"]))
        self.assertEqual(resume(self.root, "algebra")["goal"], "This was saved")

    def test_reliability_pause_survives_invalidation_and_can_resume_without_a_review(self):
        initialize(self.root, "algebra")
        save(self.root, "algebra", {"expected_revision": 0, "evidence": [self.event(outcome="incorrect")]})
        save(self.root, "algebra", {"expected_revision": 1, "review_actions": [
            {"target": "provisional:equations", "action": "pause", "reason": "Learner's choice"}]})
        save(self.root, "algebra", {"expected_revision": 2, "invalidations": [
            {"evidence_id": "e1", "reason": "Tutor correction"}]})
        packet = resume(self.root, "algebra")
        self.assertEqual(packet["reviews"], [])
        self.assertEqual(packet["suspensions"], {"provisional:equations": "Learner's choice"})
        save(self.root, "algebra", {"expected_revision": 3, "mode": "cram", "evidence": [self.event(
            "e2", at="2026-10-28T10:00:00Z", outcome="incorrect")]})
        self.assertEqual(resume(self.root, "algebra")["reviews"], [])
        save(self.root, "algebra", {"expected_revision": 4, "invalidations": [
            {"evidence_id": "e2", "reason": "Another correction"}], "review_actions": [
            {"target": "provisional:equations", "action": "resume", "reason": "Return to this target"}]})
        self.assertEqual(resume(self.root, "algebra")["suspensions"], {})
        save(self.root, "algebra", {"expected_revision": 5, "evidence": [self.event(
            "e3", at="2026-10-29T10:00:00Z", outcome="incorrect")]})
        self.assertFalse(resume(self.root, "algebra")["reviews"][0]["paused"])

    def test_reliability_v1_migrates_in_memory_and_preserves_original_on_upgrade(self):
        initialize(self.root, "algebra")
        save(self.root, "algebra", {"expected_revision": 0, "evidence": [self.event(outcome="incorrect")]})
        save(self.root, "algebra", {"expected_revision": 1, "review_actions": [
            {"target": "provisional:equations", "action": "pause", "reason": "Keep this pause"}]})
        folder = self.root / "algebra/.learning"
        path = folder / "state.json"
        legacy = json.loads(path.read_text(encoding="utf-8"))
        legacy["format_version"] = 1
        legacy.pop("suspensions", None)
        legacy_bytes = (json.dumps(legacy, indent=2) + "\n").encode("utf-8")
        path.write_bytes(legacy_bytes)
        graph_bytes = (folder / "graph.json").read_bytes()
        packet = resume(self.root, "algebra")
        self.assertEqual(packet["format_version"], 2)
        self.assertEqual(packet["suspensions"], {"provisional:equations": "Keep this pause"})
        self.assertEqual(path.read_bytes(), legacy_bytes)
        self.assertFalse((folder / "state.v1.json").exists())
        save(self.root, "algebra", {"expected_revision": 2})
        upgraded = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(upgraded["format_version"], 2)
        self.assertEqual(upgraded["evidence"], legacy["evidence"])
        self.assertEqual((folder / "state.v1.json").read_bytes(), legacy_bytes)
        self.assertEqual((folder / "graph.json").read_bytes(), graph_bytes)
        with self.assertRaises(LearningError):
            learn_state._version(upgraded, set(legacy))
        for bad in ({**upgraded, "format_version": 99}, {key: value for key, value in upgraded.items() if key != "suspensions"}):
            contents = json.dumps(bad)
            path.write_text(contents, encoding="utf-8")
            with self.assertRaises(LearningError):
                resume(self.root, "algebra")
            self.assertEqual(path.read_text(encoding="utf-8"), contents)

    def test_reliability_due_reviews_never_escape_the_selected_target_slice(self):
        initialize(self.root, "algebra")
        checkpoint = self.checkpoint("n0")
        checkpoint["targets"] = [f"n{i}" for i in range(8)]
        save(self.root, "algebra", {"expected_revision": 0,
            "nodes": {f"n{i}": {"kind": "skill", "label": f"Target {i}"} for i in range(9)},
            "checkpoint": checkpoint, "evidence": [self.event(target="n8", outcome="incorrect")]})
        for targets, expected in ((None, []), (["n0"], []), (["n8"], ["n8"])):
            with self.subTest(targets=targets):
                packet = resume(self.root, "algebra", targets=targets)
                self.assertEqual([review["target"] for review in packet["reviews"]], expected)
                self.assertEqual(packet["omitted"]["due_reviews"], 1 - len(expected))
                self.assertEqual(packet["checkpoint"], checkpoint)
                self.assertTrue(all(target in packet["graph"]["nodes"] for target in expected))

    def test_reliability_cram_due_set_is_independent_of_insertion_order(self):
        due_sets = []
        events = [self.event("a10"), self.event("b12", target="provisional:units", at="2026-10-27T12:00:00Z"),
                  self.event("a11", at="2026-10-27T11:00:00Z")]
        for index, order in enumerate((events, [events[0], events[2], events[1]])):
            root = self.root / str(index)
            initialize(root, "algebra")
            save(root, "algebra", {"expected_revision": 0, "mode": "cram", "evidence": order})
            packet = resume(root, "algebra", now=datetime(2026, 10, 27, 13, tzinfo=timezone.utc))
            due_sets.append([review["target"] for review in packet["reviews"]])
            self.assertEqual(len(resume(root, "algebra")["reviews"]), 2)
        self.assertEqual(due_sets, [["provisional:equations"], ["provisional:equations"]])

    def test_reliability_future_evidence_is_refused_before_writes(self):
        initialize(self.root, "algebra")
        folder = self.root / "algebra/.learning"
        before = {name: (folder / name).read_bytes() for name in ("graph.json", "state.json")}
        now = datetime(2026, 10, 27, 10, tzinfo=timezone.utc)
        with self.assertRaisesRegex(LearningError, "future|ahead"):
            save(self.root, "algebra", {"expected_revision": 0,
                "nodes": {"new": {"kind": "skill", "label": "Must not be written"}},
                "evidence": [self.event(at="2026-10-27T10:06:00Z")]}, now=now)
        for name, contents in before.items():
            self.assertEqual((folder / name).read_bytes(), contents)
        save(self.root, "algebra", {"expected_revision": 0, "evidence": [self.event(at="2026-10-27T10:05:00Z")]}, now=now)

    def test_reliability_reviews_are_recomputed_on_read_without_writing(self):
        initialize(self.root, "algebra")
        save(self.root, "algebra", {"expected_revision": 0, "evidence": [self.event(outcome="incorrect")]})
        path = self.root / "algebra/.learning/state.json"
        stored = json.loads(path.read_text(encoding="utf-8"))
        stored["reviews"][0].update(due_at="2099-01-01T00:00:00Z", interval_days=30, reason="Forged cache")
        contents = json.dumps(stored)
        path.write_text(contents, encoding="utf-8")
        packet = resume(self.root, "algebra")
        self.assertEqual(packet["reviews"][0]["due_at"], "2026-10-28T10:00:00+00:00")
        self.assertEqual(packet["reviews"][0]["interval_days"], 1)
        self.assertNotEqual(packet["reviews"][0]["reason"], "Forged cache")
        self.assertEqual(path.read_text(encoding="utf-8"), contents)

    def test_reliability_stdin_limit_counts_utf8_bytes(self):
        initialize(self.root, "algebra")
        helper = Path(__file__).resolve().parents[1] / "scripts/learn_state.py"
        payload = json.dumps({"expected_revision": 0, "goal": "é" * 9_000_000}, ensure_ascii=False).encode("utf-8")
        result = subprocess.run([sys.executable, "-B", str(helper), "save", "--root", str(self.root),
                                 "--subject", "algebra", "--input", "-"], input=payload, capture_output=True, check=False)
        self.assertEqual(result.returncode, 2)
        self.assertIn("16 MiB", json.loads(result.stderr.decode("utf-8"))["error"])

    def test_reliability_oversized_profiles_are_refused_without_overwriting(self):
        initialize(self.root, "algebra")
        path = self.root / "LEARNER.md"
        with path.open("wb") as stream:
            stream.write(b"<!-- adaptive-learn:1 -->\n")
            stream.truncate(16 * 1024 * 1024 + 1)
        for operation in (initialize, resume):
            with self.assertRaisesRegex(LearningError, "16 MiB"):
                operation(self.root, "algebra")
        self.assertEqual(path.stat().st_size, 16 * 1024 * 1024 + 1)

    def test_reliability_missing_ignore_rules_are_reported_without_restoring(self):
        initialize(self.root, "algebra")
        path = self.root / ".gitignore"
        path.unlink()
        saved = save(self.root, "algebra", {"expected_revision": 0})
        packet = resume(self.root, "algebra")
        self.assertTrue(any("ignore" in warning.lower() for warning in saved["warnings"]))
        self.assertTrue(any("ignore" in warning.lower() for warning in packet["warnings"]))
        self.assertFalse(path.exists())

    def legacy_state(self):
        initialize(self.root, "algebra")
        path = self.root / "algebra/.learning/state.json"
        state = json.loads(path.read_text(encoding="utf-8"))
        state["format_version"] = 1
        state.pop("suspensions")
        contents = ("\ufeff" + json.dumps(state, indent=2).replace("\n", "\r\n") + "\r\n").encode("utf-8")
        path.write_bytes(contents)
        return path, contents

    def test_reliability_interrupted_upgrade_preserves_v1_backup_and_retries(self):
        path, original = self.legacy_state()
        real_replace = os.replace

        def interrupted(source, destination):
            if Path(destination).name == "state.json":
                raise OSError("Interrupted migration")
            return real_replace(source, destination)

        with patch("os.replace", side_effect=interrupted):
            with self.assertRaisesRegex(LearningError, "state.v1.json.*unconfirmed"):
                save(self.root, "algebra", {"expected_revision": 0})
        self.assertEqual(path.read_bytes(), original)
        self.assertEqual((path.parent / "state.v1.json").read_bytes(), original)
        self.assertEqual(resume(self.root, "algebra")["revision"], 0)
        self.assertEqual(save(self.root, "algebra", {"expected_revision": 0})["revision"], 1)
        self.assertEqual(json.loads(path.read_text(encoding="utf-8"))["format_version"], 2)

    def test_reliability_conflicting_migration_backup_is_not_overwritten(self):
        path, original = self.legacy_state()
        backup = path.parent / "state.v1.json"
        backup.write_bytes(b"Unfamiliar operator backup")
        graph = path.parent / "graph.json"
        before_graph = graph.read_bytes()
        with self.assertRaisesRegex(LearningError, "backup"):
            save(self.root, "algebra", {"expected_revision": 0,
                "nodes": {"new": {"kind": "skill", "label": "Not committed"}}})
        self.assertEqual(path.read_bytes(), original)
        self.assertEqual(graph.read_bytes(), before_graph)
        self.assertEqual(backup.read_bytes(), b"Unfamiliar operator backup")

    def test_reliability_invalid_suspensions_are_rejected_without_writes(self):
        initialize(self.root, "algebra")
        path = self.root / "algebra/.learning/state.json"
        original = json.loads(path.read_text(encoding="utf-8"))
        for suspensions in ({"ghost": "Dangling target"}, {"provisional:equations": None}, []):
            contents = json.dumps({**original, "suspensions": suspensions})
            path.write_text(contents, encoding="utf-8")
            with self.assertRaises(LearningError):
                resume(self.root, "algebra")
            self.assertEqual(path.read_text(encoding="utf-8"), contents)

    def test_reliability_withdrawal_keeps_pause_until_explicitly_resumed(self):
        initialize(self.root, "algebra")
        save(self.root, "algebra", {"expected_revision": 0,
            "nodes": {"old": {"kind": "skill", "label": "Withdrawn target"}},
            "evidence": [self.event(target="old", outcome="incorrect")]})
        save(self.root, "algebra", {"expected_revision": 1, "review_actions": [
            {"target": "old", "action": "pause", "reason": "Preserve this decision"}]})
        save(self.root, "algebra", {"expected_revision": 2, "withdrawals": [
            {"id": "old", "reason": "Tutor correction", "replacement": None}]})
        packet = resume(self.root, "algebra", targets=["old"])
        self.assertEqual(packet["reviews"], [])
        self.assertEqual(packet["suspensions"], {"old": "Preserve this decision"})
        save(self.root, "algebra", {"expected_revision": 3, "review_actions": [
            {"target": "old", "action": "resume", "reason": "Clear the standing pause"}]})
        self.assertEqual(resume(self.root, "algebra", targets=["old"])["suspensions"], {})

    def test_reliability_future_clock_slack_does_not_count_as_intervening_work_yet(self):
        initialize(self.root, "algebra")
        now = datetime(2026, 10, 27, 10, tzinfo=timezone.utc)
        save(self.root, "algebra", {"expected_revision": 0, "mode": "cram", "evidence": [self.event()]}, now=now)
        save(self.root, "algebra", {"expected_revision": 1, "evidence": [self.event(
            "later", target="provisional:units", at="2026-10-27T10:04:00Z")]}, now=now)
        self.assertEqual(resume(self.root, "algebra", now=now)["reviews"], [])
        packet = resume(self.root, "algebra", now=datetime(2026, 10, 27, 10, 5, tzinfo=timezone.utc))
        self.assertEqual([review["target"] for review in packet["reviews"]], ["provisional:equations"])

    def test_reliability_suspension_slices_stay_bounded_and_keep_checkpoint(self):
        initialize(self.root, "algebra")
        checkpoint = self.checkpoint("n0")
        targets = [f"n{i}" for i in range(12)]
        save(self.root, "algebra", {"expected_revision": 0, "checkpoint": checkpoint,
            "nodes": {target: {"kind": "skill", "label": target,
                               "qualifications": [] if target == "n0" else ["Optional context. " * 40]}
                      for target in targets},
            "plan": [{"target": target, "action": "Later work", "status": "upcoming"} for target in targets],
            "evidence": [self.event(f"e{i}", target=target, outcome="incorrect") for i, target in enumerate(targets)]})
        save(self.root, "algebra", {"expected_revision": 1, "review_actions": [
            {"target": target, "action": "pause", "reason": "Learner's standing choice. " * 30} for target in targets]})
        path = self.root / "algebra/.learning/state.json"
        original = path.read_bytes()
        for budget in (2048, 4096, 8192):
            packet = resume(self.root, "algebra", targets=targets, max_chars=budget)
            self.assertLessEqual(len(json.dumps(packet, ensure_ascii=False, indent=2) + "\n"), budget)
            self.assertEqual(packet["checkpoint"], checkpoint)
            self.assertTrue(set(packet["suspensions"]) <= set(packet["selected_targets"]))
            self.assertTrue(all(item["target"] in packet["selected_targets"] for item in packet["plan"] + packet["reviews"]))
            self.assertTrue(all(count >= 0 for count in packet["omitted"].values()))
            self.assertEqual(packet["omitted"]["suspensions"] + len(packet["suspensions"]), len(targets))
        self.assertEqual(path.read_bytes(), original)

    def test_active_task_does_not_pull_in_unrelated_recent_targets_by_default(self):
        initialize(self.root, "algebra")
        save(self.root, "algebra", {"expected_revision": 0,
            "checkpoint": self.checkpoint("provisional:equations"),
            "evidence": [self.event("old", target="provisional:unrelated", importance="low")]})
        packet = resume(self.root, "algebra")
        self.assertEqual(packet["selected_targets"], ["provisional:equations"])
        self.assertEqual(packet["evidence"], [])
        self.assertEqual(packet["omitted"]["evidence"], 1)


if __name__ == "__main__":
    unittest.main()
