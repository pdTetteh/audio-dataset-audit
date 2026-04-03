import pandas as pd

from audiodatasetaudit.checks.imbalance import ImbalanceCheck


def test_imbalance_warns_for_large_ratio() -> None:
    df = pd.DataFrame(
        {
            "item_id": [str(i) for i in range(12)],
            "path": [f"{i}.wav" for i in range(12)],
            "split": ["train"] * 12,
            "label": ["major"] * 11 + ["minor"],
        }
    )
    result = ImbalanceCheck().run(df)
    assert result.status == "warn"
    assert result.metrics["max_to_min_ratio"] == 11
