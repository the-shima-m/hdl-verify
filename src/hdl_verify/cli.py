"""
cli.py — command-line interface for HDL-Verify.

After installing the package, this is available as the `hdl-verify` command:

    hdl-verify reference.v candidate.v
    hdl-verify ref.v cand.v --model Qwen2.5-Coder --prompt "8-bit adder"
    hdl-verify ref.v cand.v --fingerprint out.json --json

It exits with code 0 if the overall verdict is PASS, 1 otherwise, so it can
be used in scripts and CI.
"""

from __future__ import annotations

import argparse
import json
import sys

from hdl_verify import __version__, verify


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="hdl-verify",
        description="Verify that two Verilog circuits are equivalent "
        "(formal proof + random fuzz test) and record a reproducibility "
        "fingerprint.",
    )
    p.add_argument("reference", help="Path to the known-correct Verilog file.")
    p.add_argument("candidate", help="Path to the candidate Verilog file.")
    p.add_argument(
        "--model",
        default="",
        help="Name of the LLM that produced the candidate (recorded in the "
        "fingerprint).",
    )
    p.add_argument(
        "--prompt",
        default="",
        help="Prompt given to the LLM (recorded in the fingerprint).",
    )
    p.add_argument(
        "--fingerprint",
        default="",
        metavar="PATH",
        help="Also write the run's reproducibility fingerprint to this JSON file.",
    )
    p.add_argument(
        "--timeout",
        type=int,
        default=600,
        help="Seconds allowed for the formal checker (default: 600).",
    )
    p.add_argument(
        "--json",
        action="store_true",
        help="Print the result as JSON instead of a human-readable report.",
    )
    p.add_argument(
        "--version",
        action="version",
        version=f"hdl-verify {__version__}",
    )
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)

    report = verify(
        args.reference,
        args.candidate,
        timeout=args.timeout,
        model_name=args.model,
        prompt=args.prompt,
        fingerprint_path=args.fingerprint,
    )

    if args.json:
        out = {
            "reference": report.reference,
            "candidate": report.candidate,
            "formal": report.formal_verdict,
            "fuzz": report.fuzz_verdict,
            "fuzz_trials": report.fuzz_trials,
            "overall": "PASS" if report.passed() else "FAIL",
            "errors": report.errors,
        }
        print(json.dumps(out, indent=2))
    else:
        print(report)
        if report.errors:
            print("Notes:")
            for e in report.errors:
                # Keep it short in the CLI; full detail is in the fingerprint.
                first_line = e.splitlines()[0] if e else e
                print(f"  - {first_line}")

    return 0 if report.passed() else 1


if __name__ == "__main__":
    sys.exit(main())
