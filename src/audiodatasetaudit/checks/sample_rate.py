from __future__ import annotations

from collections import Counter
from typing import Any

import pandas as pd

from audiodatasetaudit.checks.base import AuditCheck
from audiodatasetaudit.io.audio_probe import AudioProbeResult
from audiodatasetaudit.models import CheckResult


class SampleRateConsistencyCheck(AuditCheck):
    name = "sample_rate_consistency"
    description = (
        "Summarize sample rates and flag files that deviate from the dominant rate."
    )

    def __init__(self, probe_results: dict[str, AudioProbeResult]) -> None:
        self.probe_results = probe_results

    def run(self, df: pd.DataFrame) -> CheckResult:
        readable = [probe for probe in self.probe_results.values() if probe.readable]
        counts = Counter(probe.sample_rate for probe in readable if probe.sample_rate is not None)
        if not counts:
            return CheckResult(
                name=self.name,
                status="warn",
                summary=(
                    "Skipped sample-rate analysis because no readable audio files were "
                    "available."
                ),
                metrics={"skipped": True, "reason": "no_readable_audio"},
            )

        dominant_rate, dominant_count = max(counts.items(), key=lambda item: (item[1], item[0]))
        details: list[dict[str, Any]] = []
        for row in df.itertuples(index=False):
            raw_path = str(getattr(row, "path", ""))
            probe = self.probe_results.get(raw_path)
            if probe is None or not probe.readable or probe.sample_rate == dominant_rate:
                continue
            details.append(
                {
                    "item_id": str(getattr(row, "item_id", "")),
                    "path": raw_path,
                    "sample_rate": probe.sample_rate,
                    "dominant_sample_rate": dominant_rate,
                }
            )

        mismatch_count = len(details)
        status = "warn" if len(counts) > 1 else "pass"
        summary = (
            f"Observed {len(counts)} sample rates; dominant rate is {dominant_rate} Hz."
            if len(counts) > 1
            else f"All readable files share a consistent sample rate of {dominant_rate} Hz."
        )
        return CheckResult(
            name=self.name,
            status=status,
            summary=summary,
            metrics={
                "readable_file_count": len(readable),
                "dominant_sample_rate": dominant_rate,
                "dominant_count": dominant_count,
                "sample_rate_counts": dict(sorted(counts.items())),
                "mismatch_count": mismatch_count,
            },
            details=details,
        )
