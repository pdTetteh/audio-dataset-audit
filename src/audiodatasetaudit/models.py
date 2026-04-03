from dataclasses import dataclass, field
from typing import Any


@dataclass
class CheckResult:
    name: str
    status: str
    summary: str
    metrics: dict[str, Any] = field(default_factory=dict)
    details: list[dict[str, Any]] = field(default_factory=list)
