from pathlib import Path

import pandas as pd

from audiodatasetaudit.checks.file_existence import FileExistenceCheck
from audiodatasetaudit.io.audio_probe import probe_manifest_paths


def test_file_existence_check_fails_on_missing_files(probe_manifest_path: Path) -> None:
    df = pd.read_csv(probe_manifest_path)
    probe_results = probe_manifest_paths(df, probe_manifest_path.parent.resolve())

    result = FileExistenceCheck(probe_results).run(df)

    assert result.status == "fail"
    assert result.metrics["missing_file_count"] == 1
    assert result.details[0]["path"] == "audio/missing.wav"
