import pandas as pd

from audiodatasetaudit.checks.duplicates import DuplicateCheck


def test_duplicate_check_fails_on_duplicate_ids() -> None:
    df = pd.DataFrame(
        {
            "item_id": ["1", "1", "2"],
            "path": ["a.wav", "b.wav", "c.wav"],
            "split": ["train", "val", "test"],
            "label": ["x", "y", "z"],
        }
    )
    result = DuplicateCheck().run(df)
    assert result.status == "fail"
    assert result.metrics["duplicate_item_id_count"] == 2
