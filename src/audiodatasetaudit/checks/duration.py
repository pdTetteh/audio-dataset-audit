from __future__ import annotations

from statistics import median
from typing import Any

import pandas as pd

from audiodatasetaudit.checks.base import AuditCheck
from audiodatasetaudit.io.audio_probe import AudioProbeResult
from audiodatasetaudit.models import CheckResult


class DurationCheck(AuditCheck):
    name = "duration_sanity"
    description = "Summarize probed durations and flag zero-length or mismatched entries."

    def __init__(
        self,
        probe_results: dict[str, AudioProbeResult],
        *,
        manifest_tolerance: float = 0.1,
        short_duration_threshold: float = 0.05,
        long_duration_threshold: float = 60.0,
    ) -> None:
        self.probe_results = probe_results
        self.manifest_tolerance = manifest_tolerance
        self.short_duration_threshold = short_duration_threshold
        self.long_duration_threshold = long_duration_threshold

    def run(self, df: pd.DataFrame) -> CheckResult:
        readable = [
            probe
            for probe in self.probe_results.values()
            if probe.readable and probe.duration is not None
        ]
        if not readable:
            return CheckResult(
                name=self.name,
                status="warn",
                summary=(
                    "Skipped duration analysis because no readable audio files were "
                    "available."
                ),
                metrics={"skipped": True, "reason": "no_readable_audio"},
            )

        durations = [float(probe.duration) for probe in readable]
        details: list[dict[str, Any]] = []
        zero_duration_count = 0
        suspicious_short_count = 0
        suspicious_long_count = 0
        duration_mismatch_count = 0
        manifest_has_duration = "duration" in df.columns

        for row in df.itertuples(index=False):
            raw_path = str(getattr(row, "path", ""))
            probe = self.probe_results.get(raw_path)
            if probe is None or not probe.readable or probe.duration is None:
                continue

            item_id = str(getattr(row, "item_id", ""))
            duration = float(probe.duration)
            if duration <= 0.0:
                zero_duration_count += 1
                details.append(
                    {
                        "item_id": item_id,
                        "path": raw_path,
                        "issue": "zero_duration",
                        "duration": duration,
                    }
                )
            elif duration < self.short_duration_threshold:
                suspicious_short_count += 1
                details.append(
                    {
                        "item_id": item_id,
                        "path": raw_path,
                        "issue": "very_short",
                        "duration": duration,
                    }
                )
            elif duration > self.long_duration_threshold:
                suspicious_long_count += 1
                details.append(
                    {
                        "item_id": item_id,
                        "path": raw_path,
                        "issue": "very_long",
                        "duration": duration,
                    }
                )

            if manifest_has_duration:
                manifest_value = getattr(row, "duration", None)
                if manifest_value is not None and manifest_value == manifest_value:
                    manifest_duration = float(manifest_value)
                    delta = abs(manifest_duration - duration)
                    if delta > self.manifest_tolerance:
                        duration_mismatch_count += 1
                        details.append(
                            {
                                "item_id": item_id,
                                "path": raw_path,
                                "issue": "manifest_duration_mismatch",
                                "manifest_duration": manifest_duration,
                                "probed_duration": round(duration, 6),
                                "delta": round(delta, 6),
                            }
                        )

        status = "fail" if zero_duration_count else "warn" if details else "pass"
        summary = (
            "Duration analysis completed without flagged entries."
            if not details
            else "Duration analysis flagged zero-length, extreme, or manifest-mismatched files."
        )
        return CheckResult(
            name=self.name,
            status=status,
            summary=summary,
            metrics={
                "readable_file_count": len(readable),
                "min_duration": round(min(durations), 6),
                "median_duration": round(median(durations), 6),
                "max_duration": round(max(durations), 6),
                "zero_duration_count": zero_duration_count,
                "suspicious_short_count": suspicious_short_count,
                "suspicious_long_count": suspicious_long_count,
                "manifest_duration_mismatch_count": duration_mismatch_count,
                "manifest_has_duration": manifest_has_duration,
            },
            details=details,
        )
