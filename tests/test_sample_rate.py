from pathlib import Path

import pandas as pd

from audiodatasetaudit.checks.sample_rate import SampleRateConsistencyCheck
from audiodatasetaudit.io.audio_probe import probe_manifest_paths


def test_sample_rate_check_warns_on_mixed_rates(probe_manifest_path: Path) -> None:
    df = pd.read_csv(probe_manifest_path)
    probe_results = probe_manifest_paths(df, probe_manifest_path.parent.resolve())

    result = SampleRateConsistencyCheck(probe_results).run(df)

    assert result.status == "warn"
    assert result.metrics["dominant_sample_rate"] == 16000
    assert result.metrics["mismatch_count"] == 1
