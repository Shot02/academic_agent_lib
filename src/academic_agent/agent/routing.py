from typing import Literal
from academic_agent.agent.state import AgentState

def after_plan(state: AgentState) -> Literal["execute", "respond"]:
    if state.get("plan", {}).get("needs_clarification"):
        return "respond"
    return "execute" if state.get("plan", {}).get("tool_requests") else "respond"

def after_observe(state: AgentState) -> Literal["execute", "respond"]:
    follow_up = state.get("plan", {}).get("tool_requests", [])
    return "execute" if follow_up and state.get("loop_count", 0) < 2 else "respond"