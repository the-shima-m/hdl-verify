"""
experiment.py — batch verification for manual LLM experiments.

Workflow this supports:
  1. You ask an LLM (by hand, in its web chat) to write a circuit.
  2. You save its answer as a .v file under an experiment folder, named to
     match the reference circuit it should be equivalent to.
  3. You run this to verify ALL of them at once and get a results table.

Naming convention
-----------------
A candidate file must share the stem of its reference. For a reference
`arithbench/adders/adder_8bit.v`, name the candidate `adder_8bit.v` (or
`adder_8bit__anything.v`) inside the experiment folder. The part before a
double underscore is used to find the matching reference.

Example layout
--------------
    experiments/
      qwen2.5-coder/
        adder_8bit.v          -> checked against arithbench/adders/adder_8bit.v
        mult_4bit__try2.v     -> checked against arithbench/.../mult_4bit.v
      prompts.log             -> your record of what you asked

Run
---
    hdl-verify-batch experiments/qwen2.5-coder --model Qwen2.5-Coder
"""

from __future__ import annotations

import argparse
import csv
import os
import sys

from hdl_verify import verify


def _index_references(arithbench_dir: str) -> dict:
    """Map every reference circuit's stem -> its full path."""
    index = {}
    for root, _dirs, files in os.walk(arithbench_dir):
        for fn in files:
            if fn.endswith(".v") and not fn.endswith("_broken.v"):
                stem = fn[:-2]  # drop ".v"
                index[stem] = os.path.join(root, fn)
    return index


def _reference_for(candidate_file: str, ref_index: dict) -> str | None:
    """Find the reference whose stem matches this candidate's stem."""
    base = os.path.basename(candidate_file)[:-2]  # drop ".v"
    stem = base.split("__")[0]  # allow candidate__note.v
    return ref_index.get(stem)


def run_experiment(
    experiment_dir: str,
    arithbench_dir: str = "arithbench",
    model_name: str = "",
    fingerprint_dir: str = "",
):
    """Verify every candidate .v in experiment_dir against its reference."""
    ref_index = _index_references(arithbench_dir)

    candidates = sorted(
        os.path.join(experiment_dir, f)
        for f in os.listdir(experiment_dir)
        if f.endswith(".v")
    )
    if not candidates:
        print(f"No .v candidate files found in {experiment_dir}")
        return []

    rows = []
    for cand in candidates:
        ref = _reference_for(cand, ref_index)
        name = os.path.basename(cand)
        if ref is None:
            rows.append(
                {
                    "candidate": name,
                    "reference": "(no match)",
                    "formal": "SKIP",
                    "fuzz": "SKIP",
                    "overall": "SKIP",
                }
            )
            continue

        fp_path = ""
        if fingerprint_dir:
            os.makedirs(fingerprint_dir, exist_ok=True)
            fp_path = os.path.join(fingerprint_dir, name + ".fingerprint.json")

        report = verify(ref, cand, model_name=model_name, fingerprint_path=fp_path)
        rows.append(
            {
                "candidate": name,
                "reference": os.path.relpath(ref, arithbench_dir),
                "formal": report.formal_verdict,
                "fuzz": report.fuzz_verdict,
                "overall": "PASS" if report.passed() else "FAIL",
            }
        )
    return rows


def _print_table(rows):
    if not rows:
        return
    headers = ["candidate", "reference", "formal", "fuzz", "overall"]
    widths = {h: max(len(h), *(len(str(r[h])) for r in rows)) for h in headers}
    line = "  ".join(h.ljust(widths[h]) for h in headers)
    print(line)
    print("-" * len(line))
    for r in rows:
        print("  ".join(str(r[h]).ljust(widths[h]) for h in headers))

    total = len(rows)
    passed = sum(1 for r in rows if r["overall"] == "PASS")
    failed = sum(1 for r in rows if r["overall"] == "FAIL")
    print(
        f"\nSummary: {passed}/{total} passed, {failed} failed "
        f"(pass rate {100*passed/total:.0f}%)"
    )


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="hdl-verify-batch",
        description="Verify a folder of (LLM-generated) candidate circuits "
        "against their matching ArithBench references.",
    )
    p.add_argument("experiment_dir", help="Folder of candidate .v files.")
    p.add_argument(
        "--arithbench",
        default="arithbench",
        help="Path to the reference benchmark (default: arithbench).",
    )
    p.add_argument("--model", default="", help="LLM name (recorded in fingerprints).")
    p.add_argument(
        "--fingerprints",
        default="",
        metavar="DIR",
        help="If given, save a fingerprint per candidate into this folder.",
    )
    p.add_argument(
        "--csv",
        default="",
        metavar="PATH",
        help="Also write the results table to this CSV file.",
    )
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    rows = run_experiment(
        args.experiment_dir,
        arithbench_dir=args.arithbench,
        model_name=args.model,
        fingerprint_dir=args.fingerprints,
    )
    _print_table(rows)

    if args.csv and rows:
        with open(args.csv, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        print(f"\nResults written to {args.csv}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
