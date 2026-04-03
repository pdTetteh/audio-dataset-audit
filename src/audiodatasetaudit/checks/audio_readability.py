from __future__ import annotations

from typing import Any

import pandas as pd

from audiodatasetaudit.checks.base import AuditCheck
from audiodatasetaudit.io.audio_probe import AudioProbeResult
from audiodatasetaudit.models import CheckResult


class AudioReadabilityCheck(AuditCheck):
    name = "audio_readability"
    description = "Detect files that exist but cannot be probed as valid audio."

    def __init__(self, probe_results: dict[str, AudioProbeResult]) -> None:
        self.probe_results = probe_results

    def run(self, df: pd.DataFrame) -> CheckResult:
        details: list[dict[str, Any]] = []
        for row in df.itertuples(index=False):
            raw_path = str(getattr(row, "path", ""))
            probe = self.probe_results.get(raw_path)
            if probe is None or not probe.exists or probe.readable:
                continue
            details.append(
                {
                    "item_id": str(getattr(row, "item_id", "")),
                    "path": raw_path,
                    "resolved_path": probe.resolved_path,
                    "error": probe.error or "unknown_error",
                }
            )

        unreadable_count = len(details)
        status = "fail" if unreadable_count else "pass"
        summary = (
            f"Detected {unreadable_count} existing file(s) that could not be read as audio."
            if unreadable_count
            else "All existing files were readable as audio."
        )
        return CheckResult(
            name=self.name,
            status=status,
            summary=summary,
            metrics={
                "rows_checked": int(df.shape[0]),
                "unique_paths_checked": len(self.probe_results),
                "unreadable_file_count": unreadable_count,
            },
            details=details,
        )
