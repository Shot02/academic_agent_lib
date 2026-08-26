from typing import Any, TypedDict

class AgentState(TypedDict, total=False):
    session_id: str
    actor_role: str | None
    request: str
    plan: dict[str, Any]
    observations: list[dict[str, Any]]
    pending_approvals: list[dict[str, Any]]
    approved_action_ids: list[str]
    response: str
    proposed_follow_ups: list[str]
    loop_count: int