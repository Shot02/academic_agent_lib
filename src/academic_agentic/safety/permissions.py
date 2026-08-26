from dataclasses import dataclass
from academic_agent.safety.policy import APPROVAL_REQUIRED, SideEffect

@dataclass(frozen=True)
class PermissionDecision:
    allowed: bool
    needs_approval: bool
    reason: str

def evaluate_tool_permission(side_effect: SideEffect, approved: bool, actor_role: str | None) -> PermissionDecision:
    if side_effect not in APPROVAL_REQUIRED:
        return PermissionDecision(True, False, "Read-only tool")
    if not actor_role:
        return PermissionDecision(False, True, "An identified staff role is required before approval")
    if approved:
        return PermissionDecision(True, False, "Explicit staff approval recorded")
    return PermissionDecision(False, True, f"{side_effect.value.capitalize()} action requires explicit approval")