from pathlib import Path

from audiodatasetaudit.models import CheckResult


def write_markdown_report(results: list[CheckResult], output_path: str) -> None:
    lines = ["# AudioDatasetAudit Report", ""]
    for result in results:
        lines.append(f"## {result.name}")
        lines.append(f"- Status: **{result.status}**")
        lines.append(f"- Summary: {result.summary}")
        if result.metrics:
            lines.append("- Metrics:")
            for key, value in result.metrics.items():
                lines.append(f"  - {key}: {value}")
        lines.append("")
    Path(output_path).write_text("\n".join(lines), encoding="utf-8")
