from pathlib import Path

import pandas as pd

from audiodatasetaudit.checks.leakage import LeakageCheck


LEAKY_MANIFEST = Path("tests/fixtures/leaky_manifest.csv")


def test_speaker_leakage_check_detects_overlap() -> None:
    df = pd.read_csv(LEAKY_MANIFEST)

    result = LeakageCheck("speaker_id", "speaker").run(df)

    assert result.status == "fail"
    assert result.metrics["overlap_count"] == 1
    assert result.details[0]["value"] == "spk01"
    assert result.details[0]["splits"] == ["train", "val"]


def test_device_leakage_check_normalizes_validation_split() -> None:
    df = pd.read_csv(LEAKY_MANIFEST)

    result = LeakageCheck("device_id", "device").run(df)

    assert result.status == "fail"
    assert result.metrics["overlap_count"] == 1
    assert result.details[0]["value"] == "phoneA"
    assert result.details[0]["splits"] == ["train", "val"]


def test_date_leakage_check_detects_overlap() -> None:
    df = pd.read_csv(LEAKY_MANIFEST)

    result = LeakageCheck("date", "recording date").run(df)

    assert result.status == "fail"
    assert result.metrics["overlap_count"] == 1
    assert result.details[0]["value"] == "2026-01-10"


def test_leakage_check_skips_missing_column(sample_manifest_path: Path) -> None:
    df = pd.read_csv(sample_manifest_path)

    result = LeakageCheck("collector_id", "collector").run(df)

    assert result.status == "warn"
    assert result.metrics["skipped"] is True
    assert result.metrics["reason"] == "missing_column"
