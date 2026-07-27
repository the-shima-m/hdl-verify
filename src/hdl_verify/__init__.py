"""
HDL-Verify: Validation and Reproducibility Toolkit
for AI-Generated Hardware Description Code.

Quick start:
    from hdl_verify import verify
    report = verify("ref.v", "candidate.v")
    print(report)
"""

from hdl_verify.core import verify
from hdl_verify.report import VerificationReport

__version__ = "0.1.0"
__all__ = ["VerificationReport", "verify"]
