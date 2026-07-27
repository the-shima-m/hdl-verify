"""
Basic tests for hdl_verify.
"""

import shutil

import pytest

from hdl_verify import verify
from hdl_verify.report import VerificationReport


def test_report_fail_by_default():
    """A fresh report should not be passing."""
    report = VerificationReport(reference="ref.v", candidate="cand.v")
    assert not report.passed()


def test_report_pass_when_both_pass():
    """Report should pass only when both verdicts are PASS."""
    report = VerificationReport(reference="ref.v", candidate="cand.v")
    report.formal_verdict = "PASS"
    report.fuzz_verdict = "PASS"
    assert report.passed()


def test_report_str_contains_filenames():
    """String output should mention both files."""
    report = VerificationReport(reference="ref.v", candidate="cand.v")
    output = str(report)
    assert "ref.v" in output
    assert "cand.v" in output


# Skip these if Yosys isn't installed (e.g. on a machine without the tools).
yosys_missing = shutil.which("yosys") is None
requires_yosys = pytest.mark.skipif(yosys_missing, reason="yosys not installed")

REF = "arithbench/adders/adder_4bit.v"
BROKEN = "arithbench/adders/adder_4bit_broken.v"


@requires_yosys
def test_formal_pass_on_identical_circuit():
    """A circuit is always equivalent to itself, so formal must PASS."""
    report = verify(REF, REF)
    assert report.formal_verdict == "PASS"


@requires_yosys
def test_formal_fail_on_broken_circuit():
    """The broken adder ignores carry_in, so formal must FAIL."""
    report = verify(REF, BROKEN)
    assert report.formal_verdict == "FAIL"


@requires_yosys
def test_fuzz_pass_on_identical_circuit():
    """Fuzzing a circuit against itself must PASS."""
    report = verify(REF, REF)
    assert report.fuzz_verdict == "PASS"


@requires_yosys
def test_fuzz_fail_on_broken_circuit():
    """Fuzzing against the broken adder must FAIL."""
    report = verify(REF, BROKEN)
    assert report.fuzz_verdict == "FAIL"


def test_fingerprint_captures_file_hashes():
    """Every run must produce a fingerprint with content hashes."""
    report = verify(REF, REF)
    assert report.fingerprint is not None
    assert report.fingerprint.reference_sha256 != ""
    assert report.fingerprint.candidate_sha256 != ""
