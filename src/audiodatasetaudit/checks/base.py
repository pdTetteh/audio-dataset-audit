from abc import ABC, abstractmethod

import pandas as pd

from audiodatasetaudit.models import CheckResult


class AuditCheck(ABC):
    name: str
    description: str

    @abstractmethod
    def run(self, df: pd.DataFrame) -> CheckResult:
        raise NotImplementedError
