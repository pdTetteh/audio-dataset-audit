from pathlib import Path

from audiodatasetaudit.manifest import load_manifest


def test_load_manifest(sample_manifest_path: Path) -> None:
    df = load_manifest(sample_manifest_path)
    assert len(df) == 3
    assert set(["item_id", "path", "split", "label"]).issubset(df.columns)
