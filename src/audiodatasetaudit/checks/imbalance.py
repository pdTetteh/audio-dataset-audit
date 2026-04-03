import pandas as pd

from audiodatasetaudit.checks.base import AuditCheck
from audiodatasetaudit.models import CheckResult


class ImbalanceCheck(AuditCheck):
    name = "imbalance"
    description = "Report class distribution and imbalance severity."

    def run(self, df: pd.DataFrame) -> CheckResult:
        counts = df["label"].value_counts(dropna=False).to_dict()
        values = list(counts.values())
        ratio = (max(values) / min(values)) if values and min(values) > 0 else None
        status = "warn" if ratio and ratio > 10 else "pass"
        return CheckResult(
            name=self.name,
            status=status,
            summary="Computed class distribution from the label column.",
            metrics={
                "class_counts": counts,
                "max_to_min_ratio": ratio,
                "num_classes": len(counts),
            },
        )
