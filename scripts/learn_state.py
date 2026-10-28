"""Small, dependency-free learning record store. Teaching judgment stays in SKILL.md."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from copy import deepcopy
from datetime import date, datetime, time, timedelta, timezone
from functools import wraps

PROFILE_MARKER = "<!-- adaptive-learn:1 -->"
VIEW_MARKER = "<!-- adaptive-learn generated view; state.json is canonical -->"
VERSION = 1
SKILL_ROOT = Path(__file__).resolve().parents[1]


class LearningError(ValueError):
    """Invalid, incompatible, unsafe, or unsaved learning data."""


def _operation(function):
    @wraps(function)
    def run(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except LearningError:
            raise
        except (OSError, UnicodeError, ValueError, TypeError, OverflowError) as error:
            raise LearningError(f"Invalid data or unavailable storage: {error}. Resume to verify the last saved revision; do not reinitialize.") from error
    return run


def _require(condition, message):
    if not condition:
        raise LearningError(message)


def _slug(value):
    _require(isinstance(value, str) and re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", value),
             "Subject must be a lowercase slug, not a path.")
    _require(value not in {"con", "prn", "aux", "nul", *(f"com{i}" for i in range(10)),
                           *(f"lpt{i}" for i in range(10))}, "Reserved subject name.")
    return value


def _owned(root, path):
    _require(path.resolve().is_relative_to(root) and not path.is_symlink(),
             f"Unsafe path outside the selected root or linked file: {path}")
    return path


def _location(root, subject):
    _require(bool(str(root).strip()), "An explicit learning root is required.")
    root = Path(root).expanduser().resolve()
    _require(root != SKILL_ROOT and SKILL_ROOT not in root.parents,
             "The skill directory cannot be a learner-state destination.")
    _require(not root.exists() or root.is_dir(), "The learning root is not a directory.")
    folder = _owned(root, root / _slug(subject) / ".learning")
    for name in ("graph.json", "state.json", "plan.md", "sessions"):
        _owned(root, folder / name)
    _owned(root, root / "LEARNER.md")
    _owned(root, root / ".gitignore")
    return root, folder


def _atomic_write(root, path, text):
    _owned(root, path)
    _require(not path.exists() or path.is_file(), f"Not a regular file: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=".adaptive-", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)  # Only the temporary file created by this call.


def _json_text(value):
    return json.dumps(value, ensure_ascii=False, allow_nan=False, indent=2) + "\n"


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        _require(key not in result, f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_constant(value):
    raise LearningError(f"Invalid JSON constant: {value}")


def _read_json(path):
    _require(path.is_file(), f"Missing or non-regular learning file: {path}")
    _require(path.stat().st_size <= 16 * 1024 * 1024, f"Learning file exceeds the 16 MiB safety limit: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"), object_pairs_hook=_pairs,
                          parse_constant=_reject_constant)
    except (UnicodeError, json.JSONDecodeError, RecursionError) as error:
        raise LearningError(f"Malformed learning data in {path}: {error}") from error


def _fields(value, allowed, required=()):
    _require(isinstance(value, dict), "Expected a JSON object.")
    _require(not set(value) - set(allowed), f"Unknown fields: {sorted(set(value) - set(allowed))}")
    _require(set(required) <= set(value), f"Missing fields: {sorted(set(required) - set(value))}")


def _version(value, fields):
    _fields(value, fields, fields)
    _require(type(value["format_version"]) is int and value["format_version"] == VERSION,
             "Unsupported learning format; existing data was not reinitialized.")


def _text(value, limit=4000, *, empty=False, nullable=False):
    if value is None and nullable:
        return value
    _require(isinstance(value, str) and len(value) <= limit and (empty or bool(value.strip())),
             f"Expected {'optional ' if nullable else ''}text of at most {limit} characters.")
    return value


def _texts(value, limit=1000, count=32):
    _require(isinstance(value, list) and len(value) <= count, f"Expected a text list of at most {count} entries.")
    for item in value:
        _text(item, limit)
    return value


def _id(value):
    _require(isinstance(value, str) and re.fullmatch(r"[A-Za-z][A-Za-z0-9_.:-]{0,79}", value),
             "Invalid stable ID.")
    return value


def _target(value, graph):
    _id(value)
    if value.startswith("provisional:"):
        _id(value[len("provisional:"):])
    else:
        _require(value in graph["nodes"], f"Dangling target ID: {value}")


def _node(value):
    _fields(value, {"label", "kind", "statement", "qualifications", "sources", "uncertainty", "withdrawn", "replacement"},
            {"label", "kind"})
    result = {"label": _text(value["label"], 240), "kind": value["kind"],
              "statement": value.get("statement"), "qualifications": value.get("qualifications", []),
              "sources": value.get("sources", []), "uncertainty": value.get("uncertainty"),
              "withdrawn": value.get("withdrawn"), "replacement": value.get("replacement")}
    _require(result["kind"] in ("concept", "skill", "proposition"), "Unknown node kind.")
    _text(result["statement"], nullable=result["kind"] != "proposition")
    _texts(result["qualifications"])
    _texts(result["sources"])
    _text(result["uncertainty"], nullable=True)
    _text(result["withdrawn"], nullable=True)
    if result["replacement"] is not None:
        _id(result["replacement"])
    return result


def _constraints(value):
    _fields(value, {"deadline", "study_minutes", "scope", "scope_status", "scope_source"},
            {"deadline", "study_minutes", "scope", "scope_status", "scope_source"})
    if value["deadline"] is not None:
        try:
            _require(isinstance(value["deadline"], str) and date.fromisoformat(value["deadline"]).isoformat() == value["deadline"],
                     "Deadline must be an ISO date or null.")
        except ValueError as error:
            raise LearningError("Deadline must be an ISO date or null.") from error
    minutes = value["study_minutes"]
    _require(minutes is None or type(minutes) is int and minutes > 0, "Study minutes must be positive or unknown.")
    _texts(value["scope"], 240, 200)
    _require(value["scope_status"] in ("unknown", "provisional", "confirmed"), "Unknown scope status.")
    _require(value["scope_status"] != "unknown" or not value["scope"], "An unknown scope cannot claim known topics.")
    _text(value["scope_source"], nullable=True)


def _checkpoint(value, graph):
    if value is None:
        return
    fields = {"task_id", "targets", "prompt", "assessment", "attempt", "support", "allowed_aids",
              "bottleneck", "plan_position", "next_action", "context", "source_ref"}
    _fields(value, fields, fields)
    _id(value["task_id"])
    _require(isinstance(value["targets"], list) and 0 < len(value["targets"]) <= 8, "An active task needs one to eight targets.")
    for target in value["targets"]:
        _target(target, graph)
    _text(value["prompt"], 12000)
    _text(value["attempt"], 16000, nullable=True)
    _texts(value["support"])
    _texts(value["allowed_aids"])
    for field in ("bottleneck", "plan_position", "source_ref"):
        _text(value[field], nullable=True)
    _text(value["next_action"])
    _text(value["context"], empty=True)
    assessment = value["assessment"]
    _fields(assessment, {"kind", "solution", "criteria"}, {"kind", "solution", "criteria"})
    _require(assessment["kind"] in ("objective", "criteria", "unassessed"), "Unknown assessment kind.")
    _text(assessment["solution"], 12000, nullable=assessment["kind"] != "objective")
    _texts(assessment["criteria"])
    _require(assessment["kind"] != "criteria" or bool(assessment["criteria"]), "Open-ended tasks need criteria.")
    _require(assessment["kind"] != "unassessed" or assessment["solution"] is None and not assessment["criteria"],
             "An unassessed task cannot imply a checked answer or grading criteria.")


def _at(value):
    _text(value, 80)
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise LearningError("Evidence/due times must be ISO datetimes with a timezone.") from error
    _require(result.tzinfo is not None and result.utcoffset() is not None, "A timezone is required.")
    return result.astimezone(timezone.utc)


def _clock(now=None):
    now = now if now is not None else datetime.now(timezone.utc)
    _require(isinstance(now, datetime) and now.tzinfo is not None and now.utcoffset() is not None,
             "The current time must include a timezone.")
    return now.astimezone(timezone.utc)


def _evidence(value, graph, *, stored=False):
    fields = {"id", "target", "at", "kind", "task_type", "context", "outcome", "independence",
              "assistance", "cues", "allowed_aids", "summary", "confidence", "importance", "after_gap"}
    if stored:
        fields.add("invalidated")
    _fields(value, fields, fields)
    _id(value["id"])
    _target(value["target"], graph)
    _at(value["at"])
    _require(value["kind"] in ("performance", "retrieval", "self_report", "exposure"), "Unknown evidence kind.")
    _require(value["outcome"] in ("correct", "partial", "incorrect", "unassessed"), "Unknown evidence outcome.")
    _require(value["independence"] in ("independent", "assisted", "unknown"), "Unknown independence condition.")
    for field in ("assistance", "cues", "allowed_aids"):
        _texts(value[field])
    _require(value["independence"] != "independent" or not value["assistance"],
             "Independent evidence cannot include tutor assistance.")
    _require(value["independence"] != "assisted" or bool(value["assistance"]), "Assisted work must describe its assistance.")
    _require(value["kind"] not in ("self_report", "exposure") or
             value["outcome"] == "unassessed" and value["independence"] == "unknown",
             "Exposure or self-report is not observed independent performance.")
    _require(type(value["after_gap"]) is bool, "after_gap must be explicit true/false.")
    _require(value["kind"] != "retrieval" or value["after_gap"], "Later retrieval requires intervening work or time.")
    _require(value["importance"] in ("high", "normal", "low"), "Unknown target importance.")
    for field in ("task_type", "context", "summary"):
        _text(value[field])
    _text(value["confidence"], 160, nullable=True)
    if stored:
        _text(value["invalidated"], nullable=True)


def _is_withdrawn(target, graph):
    return bool(graph["nodes"].get(target, {}).get("withdrawn"))


def _reviews(state, graph):
    result = {}
    paused = {review["target"]: (review["paused"], review["pause_reason"]) for review in state["reviews"]}
    events = sorted(enumerate(state["evidence"]), key=lambda item: (_at(item[1]["at"]), item[0]))
    for _, event in events:
        target = event["target"]
        if event["invalidated"] or event["kind"] in ("self_report", "exposure") or event["outcome"] == "unassessed" or _is_withdrawn(target, graph):
            continue
        sound = event["outcome"] == "correct" and event["independence"] == "independent"
        if sound and event["importance"] == "low" and not paused.get(target, (False, None))[0]:
            result.pop(target, None)
            continue
        previous = result.get(target)
        observed = _at(event["at"])
        interval = previous["interval_days"] if previous and sound else 1
        if previous and sound and event["kind"] == "retrieval" and observed >= _at(previous["due_at"]):
            interval = min(interval * 2, 30)
        due = observed + timedelta(days=interval)
        deadline = state["constraints"]["deadline"]
        end = datetime.combine(date.fromisoformat(deadline), time.max, timezone.utc) if deadline else None
        urgent = state["mode"] == "cram" or end is not None and observed < end <= observed + timedelta(days=1)
        if urgent:
            interval = 1
            due = observed + timedelta(days=1)
        if end is not None and observed < end < due:
            due = end
        reason = "Important independent success" if sound else "Repair or independence not yet established"
        if urgent:
            reason += "; retrieve after intervening work"
        is_paused, pause_reason = paused.get(target, (False, None))
        result[target] = {"target": target, "reason": reason, "last_evidence": event["id"],
                          "due_at": due.isoformat(), "after_evidence_id": event["id"] if urgent else None,
                          "interval_days": interval, "importance": event["importance"],
                          "paused": is_paused, "pause_reason": pause_reason}
    return list(result.values())


def _due(review, state, now):
    if review["paused"]:
        return False
    if _at(review["due_at"]) <= now:
        return True
    anchor = review["after_evidence_id"]
    if anchor is None:
        return False
    index = next(index for index, event in enumerate(state["evidence"]) if event["id"] == anchor)
    observed = _at(state["evidence"][index]["at"])
    return any(not event["invalidated"] and event["kind"] in ("performance", "retrieval")
               and event["target"] != review["target"] and _at(event["at"]) >= observed
               for event in state["evidence"][index + 1:])


def _due_reviews(state, graph, now):
    events = {event["id"]: event for event in state["evidence"]}
    due = [review for review in state["reviews"] if not _is_withdrawn(review["target"], graph) and _due(review, state, now)]
    return sorted(due, key=lambda review: (
        {"high": 0, "normal": 1, "low": 2}[review["importance"]],
        events[review["last_evidence"]]["outcome"] == "correct" and
        events[review["last_evidence"]]["independence"] == "independent", _at(review["due_at"]), review["target"]))


def _validate_state(state, graph):
    _require(type(state["revision"]) is int and state["revision"] >= 0, "Invalid state revision.")
    _slug(state["subject"])
    _text(state["goal"], empty=True)
    _require(state["mode"] in ("cram", "class", "depth"), "Mode must be cram, class, or depth.")
    _constraints(state["constraints"])
    _checkpoint(state["checkpoint"], graph)
    _require(isinstance(state["plan"], list) and len(state["plan"]) <= 64, "Plan must stay compact.")
    for item in state["plan"]:
        _fields(item, {"target", "action", "status"}, {"target", "action", "status"})
        _target(item["target"], graph)
        _text(item["action"], 1000)
        _require(item["status"] in ("upcoming", "current", "visited", "deferred"), "Invalid plan status.")
    _require(isinstance(state["evidence"], list) and isinstance(state["reviews"], list), "Invalid evidence/review records.")
    events = {}
    for event in state["evidence"]:
        _evidence(event, graph, stored=True)
        _require(event["id"] not in events, "Duplicate evidence ID.")
        events[event["id"]] = event
    targets = set()
    for review in state["reviews"]:
        fields = {"target", "reason", "last_evidence", "due_at", "after_evidence_id", "interval_days", "importance", "paused", "pause_reason"}
        _fields(review, fields, fields)
        _target(review["target"], graph)
        _require(review["target"] not in targets, "Duplicate review target.")
        targets.add(review["target"])
        last = events.get(review["last_evidence"])
        _require(last is not None and last["target"] == review["target"] and not last["invalidated"]
                 and last["kind"] in ("performance", "retrieval") and last["outcome"] != "unassessed",
                 "A review must cite valid, assessed evidence on its target.")
        _at(review["due_at"])
        _require(review["after_evidence_id"] in (None, review["last_evidence"]), "Invalid intervening-work anchor.")
        _require(type(review["interval_days"]) is int and 1 <= review["interval_days"] <= 30, "Invalid review interval.")
        _require(review["importance"] in ("high", "normal", "low"), "Invalid review importance.")
        _require(type(review["paused"]) is bool, "Review pause must be true/false.")
        _text(review["pause_reason"], nullable=not review["paused"])
        _text(review["reason"])
    if state["saved_at"] is not None:
        _at(state["saved_at"])
    _require(state["revision"] == 0 or state["saved_at"] is not None, "Saved state needs a checkpoint time.")


def _argument(value):
    _fields(value, {"premises", "conclusion", "kind", "qualifications", "sources", "uncertainty"},
            {"premises", "conclusion", "kind"})
    result = {"premises": value["premises"], "conclusion": value["conclusion"], "kind": value["kind"],
              "qualifications": value.get("qualifications", []), "sources": value.get("sources", []),
              "uncertainty": value.get("uncertainty")}
    _require(isinstance(result["premises"], list) and 0 < len(result["premises"]) <= 32, "Arguments need a nonempty premise set.")
    for premise in result["premises"]:
        _id(premise)
    _id(result["conclusion"])
    _require(len(set(result["premises"])) == len(result["premises"]) and result["conclusion"] not in result["premises"],
             "An argument cannot repeat premises or include its own conclusion as a premise.")
    _require(result["kind"] in ("deductive", "empirical"), "Argument kind must distinguish implication from empirical support.")
    _texts(result["qualifications"])
    _texts(result["sources"])
    _text(result["uncertainty"], nullable=True)
    return result


def _validate_graph(graph, root=None):
    _require(isinstance(graph["nodes"], dict), "Graph nodes must be an ID-keyed object.")
    for node_id, node in graph["nodes"].items():
        _id(node_id)
        _require(not node_id.startswith("provisional:"), "Reserved provisional target prefix.")
        _node(node)
        replacement = node.get("replacement")
        _require(replacement is None or replacement in graph["nodes"] and replacement != node_id,
                 "A replacement target must resolve to a different node.")
        _require(replacement is None or bool(node.get("withdrawn")), "A replacement requires an explicit withdrawal reason.")
    _require(isinstance(graph["prerequisites"], list) and isinstance(graph["arguments"], dict)
             and isinstance(graph["links"], list), "Invalid graph relationships.")
    incoming = {node_id: 0 for node_id in graph["nodes"]}
    dependents = {node_id: [] for node_id in graph["nodes"]}
    seen = set()
    for edge in graph["prerequisites"]:
        _fields(edge, {"target", "requires"}, {"target", "requires"})
        for key in ("target", "requires"):
            _id(edge[key])
            _require(edge[key] in graph["nodes"], "Dangling prerequisite reference.")
        pair = (edge["requires"], edge["target"])
        _require(pair not in seen, "Duplicate prerequisite relation.")
        seen.add(pair)
        incoming[edge["target"]] += 1
        dependents[edge["requires"]].append(edge["target"])
    ready = [node_id for node_id, count in incoming.items() if count == 0]
    visited = 0
    while ready:
        node_id = ready.pop()
        visited += 1
        for dependent in dependents[node_id]:
            incoming[dependent] -= 1
            if incoming[dependent] == 0:
                ready.append(dependent)
    _require(visited == len(graph["nodes"]), "Prerequisite cycle detected.")
    for argument_id, value in graph["arguments"].items():
        _id(argument_id)
        argument = _argument(value)
        _require(all(node_id in graph["nodes"] for node_id in argument["premises"] + [argument["conclusion"]]),
                 "Dangling joint-premise argument reference.")
    for link in graph["links"]:
        _fields(link, {"target", "subject", "target_id"}, {"target", "subject", "target_id"})
        _id(link["target"])
        _require(link["target"] in graph["nodes"], "Dangling local cross-subject reference.")
        _slug(link["subject"])
        _id(link["target_id"])
        if root is not None:
            remote = _owned(root, root / link["subject"] / ".learning" / "graph.json")
            other = _read_json(remote)
            _version(other, {"format_version", "nodes", "prerequisites", "arguments", "links"})
            _validate_graph(other)
            _require(link["target_id"] in other["nodes"], "Dangling cross-subject target.")


def _load(root, subject):
    root, folder = _location(root, subject)
    profile = root / "LEARNER.md"
    _require(profile.is_file() and profile.read_text(encoding="utf-8-sig").startswith(PROFILE_MARKER),
             "No recognized LEARNER.md marker at the explicitly selected root.")
    graph = _read_json(folder / "graph.json")
    state = _read_json(folder / "state.json")
    _version(graph, {"format_version", "nodes", "prerequisites", "arguments", "links"})
    _version(state, {"format_version", "revision", "subject", "goal", "mode", "constraints",
                     "checkpoint", "plan", "evidence", "reviews", "saved_at"})
    _require(state["subject"] == subject, "State belongs to a different subject.")
    _validate_graph(graph, root)
    _validate_state(state, graph)
    return root, folder, graph, state


def _privacy(root, subject):
    path = _owned(root, root / ".gitignore")
    existing = path.read_bytes() if path.exists() else b""
    rules = [b"/LEARNER.md", f"/{subject}/.learning/".encode("ascii")]
    missing = [rule for rule in rules if rule not in existing.splitlines()]
    if missing:
        suffix = (b"\n" if existing and not existing.endswith(b"\n") else b"") + b"\n".join(missing) + b"\n"
        # Preserve even non-UTF8 user rules byte-for-byte.
        descriptor, temporary = tempfile.mkstemp(prefix=".adaptive-", suffix=".tmp", dir=root)
        try:
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(existing + suffix)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, path)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)
    warnings = []
    git = shutil.which("git")
    if git:
        try:
            result = subprocess.run([git, "ls-files", "--", "LEARNER.md", f"{subject}/.learning"],
                                    cwd=root, capture_output=True, text=True, timeout=5, check=False)
            if result.returncode == 0 and result.stdout.strip():
                warnings.append("Learner files are already tracked in Git; ignore rules do not untrack them. No files were untracked.")
            if result.returncode == 0:
                for relative in ("LEARNER.md", f"{subject}/.learning/state.json"):
                    check = subprocess.run([git, "check-ignore", "--no-index", "--quiet", "--", relative],
                                           cwd=root, capture_output=True, timeout=5, check=False)
                    if check.returncode == 1:
                        warnings.append(f"Existing Git rules leave {relative} unignored. Inspect before sharing; user rules were not overwritten.")
                    elif check.returncode != 0:
                        warnings.append(f"Could not verify effective Git ignore rules for {relative}; inspect before sharing.")
        except (OSError, subprocess.TimeoutExpired):
            warnings.append("Could not check Git tracking; inspect before sharing.")
    else:
        warnings.append("Git was unavailable; existing tracking was not checked.")
    return warnings


def _views(root, folder, state, changes=None):
    warnings = []
    plan = folder / "plan.md"
    lines = [VIEW_MARKER, "# Current path", "", f"Goal: {state['goal']}", f"Mode: {state['mode']}", ""]
    lines.extend(f"- {item['status']}: {item['action']} ({item['target']})" for item in state["plan"])
    lines.append("\nNavigation is not evidence of competence.\n")
    try:
        if plan.exists() and not plan.read_text(encoding="utf-8-sig").startswith(VIEW_MARKER):
            warnings.append("Unfamiliar plan.md left unchanged; state.json remains canonical.")
        else:
            _atomic_write(root, plan, "\n".join(lines))
        _owned(root, folder / "sessions").mkdir(exist_ok=True)
        if state["revision"]:
            summary = _owned(root, folder / "sessions" / f"{state['saved_at'][:10]}-r{state['revision']:06d}.md")
            if summary.exists():
                warnings.append("Existing session summary left unchanged; state.json remains canonical.")
            else:
                checkpoint = state["checkpoint"]
                next_action = checkpoint["next_action"] if checkpoint else "No active task."
                changes = changes or {}
                records = []
                for event in changes.get("evidence", [])[-8:]:
                    records.append(f"- {event['id']} → {event['target']} [{event['kind']}/{event['outcome']}; "
                                   f"{event['independence']}]. Summary excerpt: {event['summary'][:600]}")
                for correction in changes.get("invalidations", [])[-8:]:
                    records.append(f"- Invalidated {correction['evidence_id']}: {correction['reason'][:600]}")
                for withdrawal in changes.get("withdrawals", [])[-8:]:
                    records.append(f"- Withdrawn {withdrawal['id']}: {withdrawal['reason'][:600]}")
                detail = "\n".join(records) if records else "No new assessed evidence at this checkpoint."
                _atomic_write(root, summary, f"{VIEW_MARKER}\n# Checkpoint {state['revision']}\n\n"
                              f"Saved: {state['saved_at']}\nGoal: {state['goal']}\nNext: {next_action}\n\n"
                              f"{detail}\n\nSelected excerpts only; full operational evidence is in state.json.\n")
    except (OSError, UnicodeError, LearningError) as error:
        warnings.append(f"Canonical state saved; derived view refresh failed: {error}")
    return warnings


@_operation
def initialize(root, subject):
    """Create private state at an explicitly selected root, never reset existing data."""
    root, folder = _location(root, subject)
    profile = root / "LEARNER.md"
    existing = (folder / "state.json").exists() or (folder / "graph.json").exists()
    if profile.exists():
        _require(profile.is_file() and profile.read_text(encoding="utf-8-sig").startswith(PROFILE_MARKER),
                 "Unfamiliar LEARNER.md; choose another root or inspect it, not overwrite it.")
    if existing:
        _, _, _, state = _load(root, subject)
    else:
        state = {"format_version": VERSION, "revision": 0, "subject": subject, "goal": "", "mode": "class",
                 "constraints": {"deadline": None, "study_minutes": None, "scope": [],
                                 "scope_status": "unknown", "scope_source": None},
                 "checkpoint": None, "plan": [], "evidence": [], "reviews": [], "saved_at": None}
    root.mkdir(parents=True, exist_ok=True)
    warnings = _privacy(root, subject)
    if not profile.exists():
        _atomic_write(root, profile, f"{PROFILE_MARKER}\n# Learner\n\nLearning root: {root}\n\nShared preferences: not yet supplied.\n")
    if not existing:
        graph = {"format_version": VERSION, "nodes": {}, "prerequisites": [], "arguments": {}, "links": []}
        _atomic_write(root, folder / "graph.json", _json_text(graph))
        _atomic_write(root, folder / "state.json", _json_text(state))
    warnings.extend(_views(root, folder, state))
    return {"initialized": not existing, "revision": state["revision"], "warnings": warnings}


@_operation
def resume(root, subject, *, targets=None, review_limit=3, evidence_limit=12, max_chars=24000, now=None):
    """Read a selected, bounded working view; never change learner data."""
    root, _, graph, state = _load(root, subject)
    _require(type(review_limit) is int and 0 <= review_limit <= 20, "Review limit must be 0–20.")
    _require(type(evidence_limit) is int and 0 <= evidence_limit <= 100, "Evidence limit must be 0–100.")
    _require(type(max_chars) is int and 1024 <= max_chars <= 64000, "Resume character budget must be 1024–64000.")
    due = _due_reviews(state, graph, _clock(now))
    checkpoint_targets = state["checkpoint"]["targets"] if state["checkpoint"] else []
    _require(targets is None or isinstance(targets, list) and len(targets) <= 24, "Select at most 24 explicit target IDs.")
    requested = targets if targets is not None else [review["target"] for review in due[:review_limit]]
    if targets is None and not checkpoint_targets:
        requested += [event["target"] for event in reversed(state["evidence"])]
    selected = list(checkpoint_targets)
    for target in requested:
        _target(target, graph)
        if target not in selected and (targets is not None or len(selected) < 8):
            selected.append(target)
    selected = list(dict.fromkeys(selected))
    relevant = [event for event in state["evidence"] if event["target"] in selected]
    profile = (root / "LEARNER.md").read_text(encoding="utf-8-sig")
    packet = {**state, "constraints": deepcopy(state["constraints"]), "selected_targets": selected,
              "evidence": relevant[-evidence_limit:] if evidence_limit else [],
              "reviews": due[:review_limit], "plan": [item for item in state["plan"] if item["target"] in selected],
              "graph": {"format_version": VERSION,
                        "nodes": {key: value for key, value in graph["nodes"].items() if key in selected},
                        "prerequisites": [edge for edge in graph["prerequisites"] if edge["target"] in selected and edge["requires"] in selected],
                        "arguments": {key: value for key, value in graph["arguments"].items()
                                      if all(endpoint in selected for endpoint in value["premises"] + [value["conclusion"]])},
                        "links": [link for link in graph["links"] if link["target"] in selected]},
              "profile": profile[:4000], "omitted": {}, "warnings": []}
    if any(_is_withdrawn(target, graph) for target in selected):
        packet["warnings"].append("Selected context includes explicitly withdrawn claims; do not teach them as true or reuse their evidence as current competence.")

    def count_omissions():
        packet["omitted"] = {"evidence": len(state["evidence"]) - len(packet["evidence"]),
                             "due_reviews": len(due) - len(packet["reviews"]),
                             "paused_reviews": sum(review["paused"] for review in state["reviews"]),
                             "plan": len(state["plan"]) - len(packet["plan"]),
                             "scope": len(state["constraints"]["scope"]) - len(packet["constraints"]["scope"]),
                             "profile_characters": len(profile) - len(packet["profile"]),
                             **{field: len(graph[field]) - len(packet["graph"][field])
                                for field in ("nodes", "prerequisites", "arguments", "links")}}

    count_omissions()
    while len(_json_text(packet)) > max_chars:
        if packet["evidence"]:
            packet["evidence"].pop(0)
        elif packet["profile"]:
            packet["profile"] = packet["profile"][:len(packet["profile"]) // 2]
        elif packet["plan"]:
            packet["plan"].pop()
        elif packet["constraints"]["scope"]:
            packet["constraints"]["scope"].pop()
        elif packet["reviews"]:
            packet["reviews"].pop()
        else:
            removable = [key for key in packet["graph"]["nodes"] if key not in checkpoint_targets]
            _require(bool(removable), "The intact active checkpoint and essential context exceed the resume budget. Increase max_chars or explicitly condense the checkpoint; nothing was truncated or saved.")
            removed = removable[-1]
            del packet["graph"]["nodes"][removed]
            packet["selected_targets"].remove(removed)
            packet["graph"]["prerequisites"] = [edge for edge in packet["graph"]["prerequisites"] if removed not in (edge["target"], edge["requires"])]
            packet["graph"]["arguments"] = {key: value for key, value in packet["graph"]["arguments"].items()
                                               if removed not in value["premises"] + [value["conclusion"]]}
            packet["graph"]["links"] = [link for link in packet["graph"]["links"] if link["target"] != removed]
        count_omissions()
    return packet


@_operation
def save(root, subject, update):
    """Validate and save one update at the expected revision."""
    root, folder, graph, state = _load(root, subject)
    _fields(update, {"expected_revision", "goal", "mode", "constraints", "nodes", "checkpoint", "plan", "evidence",
                     "invalidations", "review_actions", "prerequisites", "arguments", "links", "withdrawals"}, {"expected_revision"})
    _require(type(update["expected_revision"]) is int and update["expected_revision"] == state["revision"],
             "Stale revision: resume before saving; existing data was not replaced.")
    candidate = deepcopy(state)
    new_graph = deepcopy(graph)
    nodes = update.get("nodes", {})
    _require(isinstance(nodes, dict), "Node additions must be an ID-keyed object.")
    for node_id, node in nodes.items():
        normal = _node(node)
        _require(node_id not in new_graph["nodes"] or new_graph["nodes"][node_id] == normal,
                 "Existing node meanings cannot be overwritten; add a new ID and withdraw the old claim.")
        new_graph["nodes"][node_id] = normal
    for field in ("prerequisites", "links"):
        additions = update.get(field, [])
        _require(isinstance(additions, list), f"{field} additions must be a list.")
        for addition in additions:
            if addition not in new_graph[field]:
                new_graph[field].append(deepcopy(addition))
    arguments = update.get("arguments", {})
    _require(isinstance(arguments, dict), "Arguments must be an ID-keyed object.")
    for argument_id, argument in arguments.items():
        normal = _argument(argument)
        _require(argument_id not in new_graph["arguments"] or new_graph["arguments"][argument_id] == normal,
                 "Existing argument IDs cannot change meaning.")
        new_graph["arguments"][argument_id] = normal
    withdrawals = update.get("withdrawals", [])
    _require(isinstance(withdrawals, list), "Withdrawals must be a list.")
    for withdrawal in withdrawals:
        _fields(withdrawal, {"id", "reason", "replacement"}, {"id", "reason", "replacement"})
        _id(withdrawal["id"])
        _text(withdrawal["reason"])
        node = new_graph["nodes"].get(withdrawal["id"])
        _require(node is not None, "Cannot withdraw a missing node.")
        _require(node["withdrawn"] is None or
                 (node["withdrawn"], node["replacement"]) == (withdrawal["reason"], withdrawal["replacement"]),
                 "Existing withdrawal details cannot be silently replaced.")
        node["withdrawn"], node["replacement"] = withdrawal["reason"], withdrawal["replacement"]
    _validate_graph(new_graph, root)
    for field in ("goal", "mode", "constraints", "checkpoint", "plan"):
        if field in update:
            candidate[field] = deepcopy(update[field])
    additions = update.get("evidence", [])
    _require(isinstance(additions, list), "Evidence additions must be a list.")
    for event in additions:
        _evidence(event, new_graph)
        candidate["evidence"].append({**deepcopy(event), "invalidated": None})
    invalidations = update.get("invalidations", [])
    _require(isinstance(invalidations, list), "Invalidations must be a list.")
    by_id = {event["id"]: event for event in candidate["evidence"]}
    for correction in invalidations:
        _fields(correction, {"evidence_id", "reason"}, {"evidence_id", "reason"})
        _id(correction["evidence_id"])
        _text(correction["reason"])
        event = by_id.get(correction["evidence_id"])
        _require(event is not None, "Cannot invalidate missing evidence.")
        _require(event["invalidated"] in (None, correction["reason"]), "An existing correction reason cannot be silently replaced.")
        event["invalidated"] = correction["reason"]
    _validate_state({**candidate, "reviews": []}, new_graph)
    candidate["reviews"] = _reviews(candidate, new_graph)
    actions = update.get("review_actions", [])
    _require(isinstance(actions, list), "Review actions must be a list.")
    for action in actions:
        _fields(action, {"target", "action", "reason"}, {"target", "action", "reason"})
        _target(action["target"], new_graph)
        _text(action["reason"])
        _require(action["action"] in ("pause", "resume"), "Unknown review action.")
        review = next((item for item in candidate["reviews"] if item["target"] == action["target"]), None)
        _require(review is not None, "No review obligation exists for this action.")
        review["paused"] = action["action"] == "pause"
        review["pause_reason"] = action["reason"] if review["paused"] else None
    candidate["revision"] += 1
    candidate["saved_at"] = datetime.now(timezone.utc).isoformat()
    _validate_graph(new_graph, root)
    _validate_state(candidate, new_graph)
    graph_text, state_text = _json_text(new_graph), _json_text(candidate)
    _require(max(len(graph_text.encode("utf-8")), len(state_text.encode("utf-8"))) <= 16 * 1024 * 1024,
             "Proposed graph/state exceeds the readable 16 MiB safety limit. Existing files were not replaced; explicitly archive/condense or continue session-only.")
    if new_graph != graph:
        _atomic_write(root, folder / "graph.json", graph_text)
    actual_graph = _read_json(folder / "graph.json")
    _validate_graph(actual_graph, root)
    _validate_state(candidate, actual_graph)
    _require(_read_json(folder / "state.json")["revision"] == update["expected_revision"],
             "State changed during save; single-writer use is required.")
    _atomic_write(root, folder / "state.json", state_text)
    return {"saved": True, "revision": candidate["revision"], "warnings": _views(root, folder, candidate, update)}


def main(argv=None):
    """Thin CLI over the same public operations used by the tests."""
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", newline="\n")
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("init", "save", "resume"):
        command = commands.add_parser(name)
        command.add_argument("--root", required=True, help="Explicitly chosen learner workspace")
        command.add_argument("--subject", required=True, help="Subject slug, not a path")
        if name == "save":
            command.add_argument("--input", required=True, help="UTF-8 update JSON, or - for stdin")
        if name == "resume":
            command.add_argument("--target", action="append", dest="targets")
            command.add_argument("--review-limit", type=int, default=3)
            command.add_argument("--evidence-limit", type=int, default=12)
            command.add_argument("--max-chars", type=int, default=24000)
    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            result = initialize(args.root, args.subject)
        elif args.command == "save":
            if args.input == "-":
                text = sys.stdin.read(16 * 1024 * 1024 + 1)
                _require(len(text) <= 16 * 1024 * 1024, "Input exceeds the 16 MiB safety limit.")
                update = json.loads(text.lstrip("\ufeff"), object_pairs_hook=_pairs,
                                    parse_constant=_reject_constant)
            else:
                update = _read_json(Path(args.input))  # Explicit source read, never a state destination.
            result = save(args.root, args.subject, update)
        else:
            result = resume(args.root, args.subject, targets=args.targets, review_limit=args.review_limit,
                            evidence_limit=args.evidence_limit, max_chars=args.max_chars)
        sys.stdout.write(_json_text(result))
        return 0
    except (LearningError, OSError, UnicodeError, json.JSONDecodeError, RecursionError) as error:
        sys.stderr.write(_json_text({"error": str(error), "saved": False}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
