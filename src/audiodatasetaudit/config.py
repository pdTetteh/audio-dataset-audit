from dataclasses import dataclass


@dataclass
class AuditConfig:
    fail_on_warn: bool = False
