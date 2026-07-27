"""
VerificationReport: holds the results of a single verify() run.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class VerificationReport:
    reference: str
    candidate: str
    formal_verdict: str = "NOT_RUN"  # PASS / FAIL / TIMEOUT / NOT_RUN
    fuzz_verdict: str = "NOT_RUN"  # PASS / FAIL / NOT_RUN
    fuzz_trials: int = 0
    errors: list = field(default_factory=list)
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    tool_versions: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)
    # The reproducibility fingerprint for this run (set by verify()).
    fingerprint: object = None

    def passed(self):
        """True only if both checks passed."""
        return self.formal_verdict == "PASS" and self.fuzz_verdict == "PASS"

    def __str__(self):
        return (
            f"HDL-Verify Report\n"
            f"  Reference : {self.reference}\n"
            f"  Candidate : {self.candidate}\n"
            f"  Formal    : {self.formal_verdict}\n"
            f"  Fuzz      : {self.fuzz_verdict} ({self.fuzz_trials} trials)\n"
            f"  Overall   : {'PASS ✅' if self.passed() else 'FAIL ❌'}\n"
            f"  Timestamp : {self.timestamp}\n"
        )
