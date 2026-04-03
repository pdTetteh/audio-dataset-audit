from __future__ import annotations

from collections import defaultdict
from typing import Any

import pandas as pd

from audiodatasetaudit.checks.base import AuditCheck
from audiodatasetaudit.models import CheckResult

_SPLIT_NORMALIZATION = {
    "valid": "val",
    "validation": "val",
}


class LeakageCheck(AuditCheck):
    def __init__(self, field_name: str, display_name: str | None = None) -> None:
        self.field_name = field_name
        self.display_name = display_name or field_name
        self.name = f"{field_name}_leakage"
        self.description = (
            f"Detect overlap for {self.display_name} values across dataset splits."
        )

    def run(self, df: pd.DataFrame) -> CheckResult:
        if self.field_name not in df.columns:
            return CheckResult(
                name=self.name,
                status="warn",
                summary=(
                    f"Skipped {self.display_name} leakage detection because the "
                    f"'{self.field_name}' column is missing."
                ),
                metrics={
                    "field": self.field_name,
                    "skipped": True,
                    "reason": "missing_column",
                },
            )

        usable = df[[self.field_name, "split"]].copy()
        usable[self.field_name] = usable[self.field_name].astype("string").str.strip()
        usable["split"] = usable["split"].astype("string").str.strip().str.lower()
        usable["split"] = usable["split"].replace(_SPLIT_NORMALIZATION)
        usable = usable.dropna(subset=[self.field_name, "split"])
        usable = usable[(usable[self.field_name] != "") & (usable["split"] != "")]

        value_to_splits: dict[str, set[str]] = defaultdict(set)
        for value, split in usable[[self.field_name, "split"]].itertuples(index=False):
            value_to_splits[str(value)].add(str(split))

        overlaps: list[dict[str, Any]] = []
        for value, splits in value_to_splits.items():
            if len(splits) > 1:
                overlaps.append(
                    {
                        "value": value,
                        "splits": sorted(splits),
                        "num_splits": len(splits),
                    }
                )

        overlaps.sort(key=lambda item: (item["num_splits"] * -1, item["value"]))
        status = "fail" if overlaps else "pass"
        rows_with_field = int(usable.shape[0])
        unique_values = int(usable[self.field_name].nunique()) if rows_with_field else 0

        if overlaps:
            summary = (
                f"Detected {len(overlaps)} {self.display_name} value(s) present in more "
                "than one split."
            )
        else:
            summary = (
                f"No cross-split leakage detected for {self.display_name} values among "
                f"{unique_values} unique entries."
            )

        return CheckResult(
            name=self.name,
            status=status,
            summary=summary,
            metrics={
                "field": self.field_name,
                "rows_with_field": rows_with_field,
                "unique_values": unique_values,
                "overlap_count": len(overlaps),
            },
            details=overlaps,
        )
