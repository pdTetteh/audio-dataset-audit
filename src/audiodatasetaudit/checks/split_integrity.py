import pandas as pd

from audiodatasetaudit.checks.base import AuditCheck
from audiodatasetaudit.models import CheckResult

ALLOWED_SPLITS = {"train", "val", "valid", "validation", "test"}


class SplitIntegrityCheck(AuditCheck):
    name = "split_integrity"
    description = "Validate split values and summarize split counts."

    def run(self, df: pd.DataFrame) -> CheckResult:
        split_counts = df["split"].value_counts(dropna=False).to_dict()
        observed = set(df["split"].dropna().astype(str).str.lower().unique())
        invalid = sorted(observed - ALLOWED_SPLITS)
        missing_core = sorted({"train", "test"} - observed)
        status = "fail" if invalid else "warn" if missing_core else "pass"
        return CheckResult(
            name=self.name,
            status=status,
            summary="Checked split labels and summarized split distribution.",
            metrics={
                "split_counts": split_counts,
                "invalid_split_values": invalid,
                "missing_core_splits": missing_core,
            },
        )
