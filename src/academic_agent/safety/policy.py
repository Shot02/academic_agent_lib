from enum import StrEnum

class SideEffect(StrEnum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    COMMUNICATE = "communicate"

APPROVAL_REQUIRED = {SideEffect.WRITE, SideEffect.DELETE, SideEffect.COMMUNICATE}
POLICY_SUMMARY = "Read-only retrieval can run automatically. Writing records, deleting data, and external communication require explicit staff approval."