from pathlib import Path

import pandas as pd

from audiodatasetaudit.checks.audio_readability import AudioReadabilityCheck
from audiodatasetaudit.io.audio_probe import probe_manifest_paths


def test_audio_readability_check_flags_corrupt_audio(probe_manifest_path: Path) -> None:
    df = pd.read_csv(probe_manifest_path)
    probe_results = probe_manifest_paths(df, probe_manifest_path.parent.resolve())

    result = AudioReadabilityCheck(probe_results).run(df)

    assert result.status == "fail"
    assert result.metrics["unreadable_file_count"] == 1
    assert result.details[0]["path"] == "audio/broken.wav"
