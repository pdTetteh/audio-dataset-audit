from pathlib import Path

import pandas as pd

from audiodatasetaudit.checks.duration import DurationCheck
from audiodatasetaudit.io.audio_probe import probe_manifest_paths


def test_duration_check_warns_on_short_and_mismatched_files(probe_manifest_path: Path) -> None:
    df = pd.read_csv(probe_manifest_path)
    probe_results = probe_manifest_paths(df, probe_manifest_path.parent.resolve())

    result = DurationCheck(probe_results).run(df)

    assert result.status == "warn"
    assert result.metrics["suspicious_short_count"] == 1
    assert result.metrics["manifest_duration_mismatch_count"] == 1
