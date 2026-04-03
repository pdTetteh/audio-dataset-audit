from __future__ import annotations

from typing import Any

import pandas as pd

from audiodatasetaudit.checks.base import AuditCheck
from audiodatasetaudit.io.audio_probe import AudioProbeResult
from audiodatasetaudit.models import CheckResult


class FileExistenceCheck(AuditCheck):
    name = "file_existence"
    description = "Detect missing audio files referenced by the manifest."

    def __init__(self, probe_results: dict[str, AudioProbeResult]) -> None:
        self.probe_results = probe_results

    def run(self, df: pd.DataFrame) -> CheckResult:
        details: list[dict[str, Any]] = []
        for row in df.itertuples(index=False):
            raw_path = str(getattr(row, "path", ""))
            probe = self.probe_results.get(raw_path)
            if probe is None or probe.exists:
                continue
            details.append(
                {
                    "item_id": str(getattr(row, "item_id", "")),
                    "path": raw_path,
                    "resolved_path": probe.resolved_path,
                }
            )

        missing_count = len(details)
        status = "fail" if missing_count else "pass"
        summary = (
            f"Detected {missing_count} manifest row(s) pointing to missing files."
            if missing_count
            else "All manifest paths resolved to existing files."
        )
        return CheckResult(
            name=self.name,
            status=status,
            summary=summary,
            metrics={
                "rows_checked": int(df.shape[0]),
                "unique_paths_checked": len(self.probe_results),
                "missing_file_count": missing_count,
            },
            details=details,
        )
