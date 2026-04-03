import pandas as pd

from audiodatasetaudit.checks.split_integrity import SplitIntegrityCheck


def test_split_integrity_warns_when_test_missing() -> None:
    df = pd.DataFrame(
        {
            "item_id": ["1", "2"],
            "path": ["a.wav", "b.wav"],
            "split": ["train", "val"],
            "label": ["x", "y"],
        }
    )
    result = SplitIntegrityCheck().run(df)
    assert result.status == "warn"
    assert "test" in result.metrics["missing_core_splits"]


def test_split_integrity_fails_on_invalid_split() -> None:
    df = pd.DataFrame(
        {
            "item_id": ["1", "2"],
            "path": ["a.wav", "b.wav"],
            "split": ["train", "holdout"],
            "label": ["x", "y"],
        }
    )
    result = SplitIntegrityCheck().run(df)
    assert result.status == "fail"
    assert "holdout" in result.metrics["invalid_split_values"]
