from __future__ import annotations

from pathlib import Path
from typing import Any

from audiodatasetaudit.models import CheckResult


def _format_value(value: Any) -> str:
    if isinstance(value, dict):
        pieces = ", ".join(f"{k}={v}" for k, v in value.items())
        return f"{{{pieces}}}"
    if isinstance(value, list):
        preview = ", ".join(_format_value(item) for item in value[:5])
        suffix = ", ..." if len(value) > 5 else ""
        return f"[{preview}{suffix}]"
    return str(value)


def write_markdown_report(results: list[CheckResult], output_path: str) -> None:
    lines = ["# AudioDatasetAudit Report", ""]
    for result in results:
        lines.append(f"## {result.name}")
        lines.append(f"- Status: **{result.status}**")
        lines.append(f"- Summary: {result.summary}")
        if result.metrics:
            lines.append("- Metrics:")
            for key, value in result.metrics.items():
                lines.append(f"  - {key}: {_format_value(value)}")
        if result.details:
            lines.append("- Details:")
            for detail in result.details[:10]:
                lines.append(f"  - {_format_value(detail)}")
            if len(result.details) > 10:
                lines.append(f"  - ... ({len(result.details) - 10} more)")
        lines.append("")
    Path(output_path).write_text("\n".join(lines), encoding="utf-8")
