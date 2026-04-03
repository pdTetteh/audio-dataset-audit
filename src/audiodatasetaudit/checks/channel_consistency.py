from __future__ import annotations

from collections import Counter
from typing import Any

import pandas as pd

from audiodatasetaudit.checks.base import AuditCheck
from audiodatasetaudit.io.audio_probe import AudioProbeResult
from audiodatasetaudit.models import CheckResult


class ChannelConsistencyCheck(AuditCheck):
    name = "channel_consistency"
    description = (
        "Summarize audio channel counts and flag files that deviate from the dominant "
        "count."
    )

    def __init__(self, probe_results: dict[str, AudioProbeResult]) -> None:
        self.probe_results = probe_results

    def run(self, df: pd.DataFrame) -> CheckResult:
        readable = [probe for probe in self.probe_results.values() if probe.readable]
        counts = Counter(probe.channels for probe in readable if probe.channels is not None)
        if not counts:
            return CheckResult(
                name=self.name,
                status="warn",
                summary=(
                    "Skipped channel analysis because no readable audio files were "
                    "available."
                ),
                metrics={"skipped": True, "reason": "no_readable_audio"},
            )

        dominant_channels, dominant_count = max(
            counts.items(),
            key=lambda item: (item[1], -item[0]),
        )
        details: list[dict[str, Any]] = []
        for row in df.itertuples(index=False):
            raw_path = str(getattr(row, "path", ""))
            probe = self.probe_results.get(raw_path)
            if probe is None or not probe.readable or probe.channels == dominant_channels:
                continue
            details.append(
                {
                    "item_id": str(getattr(row, "item_id", "")),
                    "path": raw_path,
                    "channels": probe.channels,
                    "dominant_channels": dominant_channels,
                }
            )

        mismatch_count = len(details)
        status = "warn" if len(counts) > 1 else "pass"
        summary = (
            f"Observed {len(counts)} channel layouts; dominant layout uses "
            f"{dominant_channels} channel(s)."
            if len(counts) > 1
            else f"All readable files share a consistent channel count of {dominant_channels}."
        )
        return CheckResult(
            name=self.name,
            status=status,
            summary=summary,
            metrics={
                "readable_file_count": len(readable),
                "dominant_channels": dominant_channels,
                "dominant_count": dominant_count,
                "channel_count_distribution": dict(sorted(counts.items())),
                "mismatch_count": mismatch_count,
            },
            details=details,
        )
