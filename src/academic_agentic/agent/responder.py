from academic_agentic.agent.state import AgentState

def respond(state: AgentState, runtime) -> dict:
    plan = state.get("plan", {})
    if plan.get("needs_clarification"):
        text = plan.get("clarification_question") or "What additional detail would help me complete this safely?"
    elif state.get("pending_approvals"):
        text = state.get("response") or "I have prepared the requested next action. Please review and approve it before I carry it out."
    else:
        text = state.get("response") or plan.get("summary") or "I could not find a supported action for that request."
    runtime.memory.append(state["session_id"], "user", state["request"])
    runtime.memory.append(state["session_id"], "assistant", text)
    return {"response": text}