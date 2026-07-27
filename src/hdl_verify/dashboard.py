"""
dashboard.py — turn batch results into a self-contained HTML dashboard.

Reads a results CSV (as produced by `hdl-verify-batch --csv results.csv`)
and writes a single standalone HTML file: a sortable, color-coded table with
a pass-rate summary. No server, no dependencies — open it in any browser or
commit it to the repo.

Run
---
    hdl-verify-dashboard results.csv -o dashboard.html
"""

from __future__ import annotations

import argparse
import csv
import datetime
import html
import sys


def _verdict_class(v: str) -> str:
    v = (v or "").upper()
    if v == "PASS":
        return "pass"
    if v == "FAIL":
        return "fail"
    if v in ("SKIP", "NOT_RUN"):
        return "skip"
    return "other"


def build_html(rows: list[dict], title: str = "HDL-Verify Results") -> str:
    total = len(rows)
    passed = sum(1 for r in rows if (r.get("overall", "").upper() == "PASS"))
    failed = sum(1 for r in rows if (r.get("overall", "").upper() == "FAIL"))
    skipped = total - passed - failed
    rate = (100 * passed / total) if total else 0
    generated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    headers = (
        list(rows[0].keys())
        if rows
        else ["candidate", "reference", "formal", "fuzz", "overall"]
    )

    body_rows = []
    for r in rows:
        cells = []
        for h in headers:
            val = html.escape(str(r.get(h, "")))
            if h in ("formal", "fuzz", "overall"):
                cells.append(f'<td class="v {_verdict_class(r.get(h,""))}">{val}</td>')
            else:
                cells.append(f"<td>{val}</td>")
        body_rows.append("<tr>" + "".join(cells) + "</tr>")

    header_html = "".join(f"<th>{html.escape(h)}</th>" for h in headers)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<style>
  body {{ font-family: -apple-system, Segoe UI, Roboto, sans-serif;
          margin: 2rem; color: #1a1a2e; background: #f7f7fb; }}
  h1 {{ margin-bottom: 0.25rem; }}
  .sub {{ color: #666; margin-top: 0; font-size: 0.9rem; }}
  .cards {{ display: flex; gap: 1rem; margin: 1.5rem 0; flex-wrap: wrap; }}
  .card {{ background: #fff; border-radius: 10px; padding: 1rem 1.5rem;
           box-shadow: 0 1px 4px rgba(0,0,0,0.08); min-width: 90px; }}
  .card .n {{ font-size: 1.8rem; font-weight: 700; }}
  .card .l {{ font-size: 0.8rem; color: #666; text-transform: uppercase;
              letter-spacing: 0.05em; }}
  .rate .n {{ color: #2563eb; }}
  table {{ border-collapse: collapse; width: 100%; background: #fff;
           border-radius: 10px; overflow: hidden;
           box-shadow: 0 1px 4px rgba(0,0,0,0.08); }}
  th, td {{ text-align: left; padding: 0.6rem 0.9rem;
            border-bottom: 1px solid #eee; font-size: 0.9rem; }}
  th {{ background: #1a1a2e; color: #fff; font-weight: 600; }}
  td.v {{ font-weight: 700; text-align: center; }}
  .pass {{ color: #16a34a; }}
  .fail {{ color: #dc2626; }}
  .skip {{ color: #9ca3af; }}
  tr:hover td {{ background: #fafaff; }}
</style>
</head>
<body>
  <h1>{html.escape(title)}</h1>
  <p class="sub">Generated {generated} — HDL-Verify</p>

  <div class="cards">
    <div class="card"><div class="n">{total}</div><div class="l">Total</div></div>
    <div class="card"><div class="n pass">{passed}</div><div class="l">Passed</div></div>
    <div class="card"><div class="n fail">{failed}</div><div class="l">Failed</div></div>
    <div class="card"><div class="n skip">{skipped}</div><div class="l">Skipped</div></div>
    <div class="card rate"><div class="n">{rate:.0f}%</div><div class="l">Pass rate</div></div>
  </div>

  <table>
    <thead><tr>{header_html}</tr></thead>
    <tbody>
      {chr(10).join(body_rows)}
    </tbody>
  </table>
</body>
</html>
"""


def load_rows(csv_path: str) -> list[dict]:
    with open(csv_path, "r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="hdl-verify-dashboard",
        description="Generate a standalone HTML dashboard from a results CSV.",
    )
    p.add_argument("csv_file", help="Results CSV from hdl-verify-batch.")
    p.add_argument(
        "-o",
        "--output",
        default="dashboard.html",
        help="Output HTML file (default: dashboard.html).",
    )
    p.add_argument(
        "--title",
        default="HDL-Verify Results",
        help="Dashboard title.",
    )
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    rows = load_rows(args.csv_file)
    out = build_html(rows, title=args.title)
    with open(args.output, "w", encoding="utf-8") as fh:
        fh.write(out)
    print(f"Dashboard written to {args.output} ({len(rows)} rows)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
