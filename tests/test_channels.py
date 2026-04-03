from pathlib import Path

import pandas as pd

from audiodatasetaudit.checks.channel_consistency import ChannelConsistencyCheck
from audiodatasetaudit.io.audio_probe import probe_manifest_paths


def test_channel_check_warns_on_mixed_channel_counts(probe_manifest_path: Path) -> None:
    df = pd.read_csv(probe_manifest_path)
    probe_results = probe_manifest_paths(df, probe_manifest_path.parent.resolve())

    result = ChannelConsistencyCheck(probe_results).run(df)

    assert result.status == "warn"
    assert result.metrics["dominant_channels"] == 1
    assert result.metrics["mismatch_count"] == 1
