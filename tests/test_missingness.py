import pandas as pd

from audiodatasetaudit.checks.missingness import MissingnessCheck


def test_missingness_warns_when_missing_values_present() -> None:
    df = pd.DataFrame(
        {
            "item_id": ["1", "2"],
            "path": ["a.wav", "b.wav"],
            "split": ["train", "test"],
            "label": ["car_horn", None],
        }
    )
    result = MissingnessCheck().run(df)
    assert result.status == "warn"
    assert result.metrics["missing_counts"]["label"] == 1
