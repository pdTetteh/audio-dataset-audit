from pathlib import Path

import pandas as pd

from audiodatasetaudit.io.audio_probe import probe_audio_file, probe_manifest_paths


def test_probe_audio_file_reads_wave_metadata() -> None:
    result = probe_audio_file("tests/fixtures/audio/mono_16k.wav")

    assert result.exists is True
    assert result.readable is True
    assert result.sample_rate == 16000
    assert result.channels == 1
    assert result.duration is not None and round(result.duration, 2) == 1.0


def test_probe_audio_file_flags_missing_file() -> None:
    result = probe_audio_file("tests/fixtures/audio/does_not_exist.wav")

    assert result.exists is False
    assert result.error == "file_not_found"


def test_probe_manifest_paths_uses_base_dir(probe_manifest_path: Path) -> None:
    df = pd.read_csv(probe_manifest_path)

    results = probe_manifest_paths(df, probe_manifest_path.parent.resolve())

    assert "audio/mono_16k.wav" in results
    assert results["audio/mono_16k.wav"].resolved_path.endswith("tests/fixtures/audio/mono_16k.wav")
