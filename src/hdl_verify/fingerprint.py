"""
fingerprint.py — the reproducibility record for a verify() run.

A Fingerprint captures everything needed to reproduce a verification later:
the exact content of both input circuits (by hash), the versions of every
tool used, the platform, the timestamp, and any AI-model / prompt metadata
the user chooses to record. It can be written to disk as JSON and compared
against a later run to detect drift.

This is the piece that answers the proposal's core problem: existing
benchmarks have "no way to reproduce their own results." A Fingerprint makes
a run replayable and makes drift measurable.
"""

from __future__ import annotations

import hashlib
import json
import platform
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone


def _file_sha256(path: str) -> str:
    """Return the SHA-256 hex digest of a file's contents, or '' if unreadable."""
    try:
        h = hashlib.sha256()
        with open(path, "rb") as fh:
            for chunk in iter(lambda: fh.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()
    except OSError:
        return ""


def _tool_version(tool: str) -> str:
    """Return a one-line version string for a tool, or 'not found'."""
    if not shutil.which(tool):
        return "not found"
    flag = "-V" if tool == "iverilog" else "--version"
    try:
        result = subprocess.run(
            [tool, flag], capture_output=True, text=True, timeout=15
        )
        text = (result.stdout or result.stderr or "").strip()
        return text.splitlines()[0] if text else "unknown"
    except Exception:  # noqa: BLE001
        return "unknown"


def _git_commit() -> str:
    """Return the current git commit hash of the working tree, or 'unknown'."""
    if not shutil.which("git"):
        return "unknown"
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return result.stdout.strip() or "unknown"
    except Exception:  # noqa: BLE001
        return "unknown"


@dataclass
class Fingerprint:
    """A complete, replayable record of the conditions of one verify() run."""

    reference: str
    candidate: str
    reference_sha256: str = ""
    candidate_sha256: str = ""
    tool_versions: dict = field(default_factory=dict)
    platform_info: dict = field(default_factory=dict)
    git_commit: str = "unknown"
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    # Optional: filled in by the user when the candidate came from an LLM.
    model_name: str = ""
    prompt: str = ""

    @classmethod
    def capture(
        cls,
        reference: str,
        candidate: str,
        model_name: str = "",
        prompt: str = "",
    ) -> "Fingerprint":
        """Build a Fingerprint by inspecting the files, tools, and platform now."""
        return cls(
            reference=reference,
            candidate=candidate,
            reference_sha256=_file_sha256(reference),
            candidate_sha256=_file_sha256(candidate),
            tool_versions={
                "yosys": _tool_version("yosys"),
                "iverilog": _tool_version("iverilog"),
            },
            platform_info={
                "system": platform.system(),
                "release": platform.release(),
                "machine": platform.machine(),
                "python": sys.version.split()[0],
            },
            git_commit=_git_commit(),
            model_name=model_name,
            prompt=prompt,
        )

    def to_dict(self) -> dict:
        return asdict(self)

    def save(self, path: str) -> None:
        """Write the fingerprint to disk as pretty-printed JSON."""
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(self.to_dict(), fh, indent=2, sort_keys=True)

    @classmethod
    def load(cls, path: str) -> "Fingerprint":
        """Load a fingerprint previously written with save()."""
        with open(path, "r", encoding="utf-8") as fh:
            return cls(**json.load(fh))

    def diff(self, other: "Fingerprint") -> dict:
        """
        Compare this fingerprint against another and return what changed.

        Used by the drift study: capture a fingerprint today, capture another
        30 days later, and diff() shows exactly what moved — a tool version,
        a file hash, the platform. An empty dict means nothing changed.
        """
        changes = {}
        a, b = self.to_dict(), other.to_dict()
        for key in a:
            if a[key] != b.get(key):
                changes[key] = {"before": a[key], "after": b.get(key)}
        return changes
