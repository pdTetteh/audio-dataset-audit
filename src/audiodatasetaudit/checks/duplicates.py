import pandas as pd

from audiodatasetaudit.checks.base import AuditCheck
from audiodatasetaudit.models import CheckResult


class DuplicateCheck(AuditCheck):
    name = "duplicates"
    description = "Detect duplicate item IDs and duplicate file paths."

    def run(self, df: pd.DataFrame) -> CheckResult:
        dup_ids = df[df.duplicated(subset=["item_id"], keep=False)]
        dup_paths = df[df.duplicated(subset=["path"], keep=False)]
        status = "fail" if not dup_ids.empty or not dup_paths.empty else "pass"
        return CheckResult(
            name=self.name,
            status=status,
            summary="Checked for duplicate item IDs and duplicate file paths.",
            metrics={
                "duplicate_item_id_count": int(dup_ids.shape[0]),
                "duplicate_path_count": int(dup_paths.shape[0]),
            },
            details=[
                {
                    "duplicate_item_ids": dup_ids[["item_id", "path"]].to_dict(orient="records"),
                    "duplicate_paths": dup_paths[["item_id", "path"]].to_dict(orient="records"),
                }
            ],
        )
