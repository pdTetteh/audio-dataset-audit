import pandas as pd

from audiodatasetaudit.checks.base import AuditCheck
from audiodatasetaudit.models import CheckResult


class MissingnessCheck(AuditCheck):
    name = "missingness"
    description = "Report missing values by column."

    def run(self, df: pd.DataFrame) -> CheckResult:
        missing_counts = df.isna().sum().to_dict()
        total_rows = len(df)
        missing_rates = {
            col: (count / total_rows if total_rows else 0.0)
            for col, count in missing_counts.items()
        }
        summary = "Calculated missing value counts and rates for all columns."
        status = "warn" if any(count > 0 for count in missing_counts.values()) else "pass"
        return CheckResult(
            name=self.name,
            status=status,
            summary=summary,
            metrics={
                "rows": total_rows,
                "missing_counts": missing_counts,
                "missing_rates": missing_rates,
            },
        )
