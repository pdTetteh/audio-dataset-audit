import json
from pathlib import Path

from audiodatasetaudit.models import CheckResult


def write_json_report(results: list[CheckResult], output_path: str) -> None:
    path = Path(output_path)
    payload = [
        {
            "name": r.name,
            "status": r.status,
            "summary": r.summary,
            "metrics": r.metrics,
            "details": r.details,
        }
        for r in results
    ]
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
