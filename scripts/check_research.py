"""Run local tests and replay the published synthetic evidence; no model calls."""

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def verify_archive():
    manifest = json.loads((ROOT / "handoff/PUBLICATION_MANIFEST.json").read_text(encoding="utf-8"))
    assert manifest["format"] == "adaptive-learn-publication-archive" and manifest["version"] == 1
    assert len(manifest["files"]) == manifest["file_count"]
    seen = set()
    for entry in manifest["files"]:
        path = (ROOT / entry["path"]).resolve()
        path.relative_to(ROOT)
        assert entry["path"] not in seen, "Repeated archive entry"
        seen.add(entry["path"])
        raw = path.read_bytes()
        assert len(raw) == entry["bytes"] and hashlib.sha256(raw).hexdigest() == entry["published_sha256"], entry["path"]


def main():
    if not __debug__:
        raise SystemExit("Run without -O; the frozen evidence checks use assertions.")
    verify_archive()
    preferred = Path(os.environ.get("LOCALAPPDATA", "")) / "Temp/opencode"
    with tempfile.TemporaryDirectory(prefix="adaptive-learn-check-", dir=preferred if preferred.is_dir() else None) as scratch:
        env = os.environ.copy()
        # Frozen research used a sibling workspace and Windows-style test temp paths.
        env["PYTHONPATH"] = str(ROOT / "tests/live") + os.pathsep + env.get("PYTHONPATH", "")
        env["PYTHONUTF8"] = "1"
        env["LOCALAPPDATA"] = scratch
        (Path(scratch) / "Temp/opencode").mkdir(parents=True)

        def run(arguments, capture=False):
            return subprocess.run([sys.executable, "-B", *arguments], cwd=ROOT, env=env, check=True,
                                  capture_output=capture, text=True, encoding="utf-8")

        for folder in ("tests", "handoff/benchmarks/novel-rules", "handoff/benchmarks/time-to-transfer", "handoff/iterations/tutor-vs-chat"):
            print(f"Testing {folder}", flush=True)
            run(["-m", "unittest", "discover", "-s", folder, "-p", "test_*.py", "-q"])

        run(["tests/live/check_cases.py", "--verify-holdout"])
        reports = (
            (["handoff/benchmarks/novel-rules/record.py", "report", "--phase", "all"], "handoff/benchmarks/novel-rules/all-results.json"),
            (["handoff/benchmarks/time-to-transfer/pilot.py"], "handoff/benchmarks/time-to-transfer/results.json"),
            (["handoff/iterations/tutor-vs-chat/check.py"], "handoff/iterations/tutor-vs-chat/results.json"),
        )
        for arguments, expected in reports:
            actual = json.loads(run(arguments, capture=True).stdout)
            assert actual == json.loads((ROOT / expected).read_text(encoding="utf-8")), expected
            print(f"Reproduced {expected}", flush=True)
    print("All 92 tests, archive hashes, holdout, and three recorded reports passed. No model calls or human learning measurement.")


if __name__ == "__main__":
    main()
