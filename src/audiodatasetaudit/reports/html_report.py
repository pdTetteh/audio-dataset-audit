from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Any

from audiodatasetaudit.models import CheckResult

_STATUS_CLASS = {
    "pass": "status-pass",
    "warn": "status-warn",
    "fail": "status-fail",
}


def _stringify(value: Any) -> str:
    if isinstance(value, dict):
        items = ", ".join(f"{k}={_stringify(v)}" for k, v in value.items())
        return f"{{{items}}}"
    if isinstance(value, list):
        items = ", ".join(_stringify(item) for item in value)
        return f"[{items}]"
    return str(value)


def _table(headers: list[str], rows: list[list[str]], empty_message: str) -> str:
    if not rows:
        return f'<p class="empty">{escape(empty_message)}</p>'

    header_html = "".join(f"<th>{escape(header)}</th>" for header in headers)
    row_html = []
    for row in rows:
        row_html.append(
            "<tr>"
            + "".join(f"<td>{escape(cell)}</td>" for cell in row)
            + "</tr>"
        )
    return (
        '<div class="table-wrap">'
        "<table>"
        f"<thead><tr>{header_html}</tr></thead>"
        f"<tbody>{''.join(row_html)}</tbody>"
        "</table>"
        "</div>"
    )


def _metrics_table(result: CheckResult) -> str:
    rows = [[key, _stringify(value)] for key, value in result.metrics.items()]
    return _table(["Metric", "Value"], rows, "No metrics available.")


def _details_table(result: CheckResult) -> str:
    if not result.details:
        return '<p class="empty">No detail rows.</p>'

    headers: list[str] = []
    seen = set()
    for detail in result.details:
        for key in detail.keys():
            if key not in seen:
                seen.add(key)
                headers.append(key)

    rows: list[list[str]] = []
    for detail in result.details:
        rows.append([_stringify(detail.get(header, "")) for header in headers])
    return _table(headers, rows, "No detail rows.")


def _summary_cards(results: list[CheckResult]) -> str:
    counts = {"pass": 0, "warn": 0, "fail": 0}
    for result in results:
        if result.status in counts:
            counts[result.status] += 1

    total = len(results)
    cards = [
        ("Checks", str(total), "status-neutral"),
        ("Pass", str(counts["pass"]), "status-pass"),
        ("Warn", str(counts["warn"]), "status-warn"),
        ("Fail", str(counts["fail"]), "status-fail"),
    ]
    pieces = []
    for label, value, css_class in cards:
        pieces.append(
            f'<div class="summary-card {css_class}">'
            f'<div class="summary-label">{escape(label)}</div>'
            f'<div class="summary-value">{escape(value)}</div>'
            "</div>"
        )
    return "".join(pieces)


def write_html_report(results: list[CheckResult], output_path: str) -> None:
    sections: list[str] = []
    for result in results:
        status_class = _STATUS_CLASS.get(result.status, "status-neutral")
        sections.append(
            '<section class="check-card">'
            '<div class="check-header">'
            f'<h2>{escape(result.name)}</h2>'
            f'<span class="status-pill {status_class}">{escape(result.status.upper())}</span>'
            "</div>"
            f'<p class="summary">{escape(result.summary)}</p>'
            '<div class="grid">'
            '<div class="panel">'
            '<h3>Metrics</h3>'
            f'{_metrics_table(result)}'
            "</div>"
            '<div class="panel">'
            '<h3>Details</h3>'
            f'{_details_table(result)}'
            "</div>"
            "</div>"
            "</section>"
        )

    html = f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>AudioDatasetAudit Report</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f5f7fb;
      --surface: #ffffff;
      --border: #d9e2f1;
      --text: #172033;
      --muted: #5a6780;
      --pass-bg: #e7f7ee;
      --pass-text: #156c3e;
      --warn-bg: #fff4db;
      --warn-text: #8a5a00;
      --fail-bg: #fde8e8;
      --fail-text: #a11b1b;
      --neutral-bg: #eef2ff;
      --neutral-text: #3f4d67;
      --shadow: 0 12px 30px rgba(22, 32, 51, 0.08);
    }}

    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system,
        BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.5;
    }}
    .container {{
      max-width: 1180px;
      margin: 0 auto;
      padding: 40px 20px 64px;
    }}
    .hero {{
      margin-bottom: 28px;
    }}
    .hero h1 {{
      margin: 0 0 8px;
      font-size: 2.25rem;
      line-height: 1.1;
    }}
    .hero p {{
      margin: 0;
      color: var(--muted);
      max-width: 760px;
    }}
    .summary-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
      gap: 14px;
      margin: 24px 0 30px;
    }}
    .summary-card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 18px;
      padding: 18px;
      box-shadow: var(--shadow);
    }}
    .summary-label {{
      font-size: 0.92rem;
      color: var(--muted);
      margin-bottom: 8px;
    }}
    .summary-value {{
      font-size: 2rem;
      font-weight: 700;
    }}
    .check-card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 22px;
      padding: 22px;
      box-shadow: var(--shadow);
      margin-bottom: 18px;
    }}
    .check-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 10px;
    }}
    .check-header h2 {{
      margin: 0;
      font-size: 1.2rem;
      line-height: 1.25;
    }}
    .summary {{
      margin: 0 0 18px;
      color: var(--muted);
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 16px;
    }}
    .panel {{
      border: 1px solid var(--border);
      border-radius: 18px;
      padding: 16px;
      background: #fcfdff;
    }}
    .panel h3 {{
      margin: 0 0 12px;
      font-size: 1rem;
    }}
    .status-pill {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 0.38rem 0.72rem;
      border-radius: 999px;
      font-size: 0.78rem;
      font-weight: 700;
      letter-spacing: 0.03em;
    }}
    .status-pass {{ background: var(--pass-bg); color: var(--pass-text); }}
    .status-warn {{ background: var(--warn-bg); color: var(--warn-text); }}
    .status-fail {{ background: var(--fail-bg); color: var(--fail-text); }}
    .status-neutral {{ background: var(--neutral-bg); color: var(--neutral-text); }}
    .table-wrap {{ overflow-x: auto; }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.94rem;
    }}
    th, td {{
      padding: 0.72rem 0.8rem;
      border-bottom: 1px solid var(--border);
      text-align: left;
      vertical-align: top;
    }}
    th {{
      font-size: 0.84rem;
      text-transform: uppercase;
      letter-spacing: 0.02em;
      color: var(--muted);
      background: #f8faff;
    }}
    tr:last-child td {{ border-bottom: none; }}
    .empty {{ margin: 0; color: var(--muted); }}
    .footer {{
      margin-top: 32px;
      color: var(--muted);
      font-size: 0.92rem;
    }}
    @media (max-width: 640px) {{
      .container {{ padding: 24px 14px 40px; }}
      .hero h1 {{ font-size: 1.7rem; }}
      .check-card {{ padding: 18px; }}
      .check-header {{ align-items: flex-start; flex-direction: column; }}
    }}
  </style>
</head>
<body>
  <main class=\"container\">
    <header class=\"hero\">
      <h1>AudioDatasetAudit Report</h1>
      <p>Structured quality checks for speech and audio datasets,
        including split hygiene, leakage detection, metadata coverage, and
        class balance.</p>
    </header>

    <section class=\"summary-grid\">
      {_summary_cards(results)}
    </section>

    {''.join(sections)}

    <p class=\"footer\">Generated by AudioDatasetAudit.</p>
  </main>
</body>
</html>
"""
    Path(output_path).write_text(html, encoding="utf-8")
