from academic_agent.agent.state import AgentState
from academic_agent.llm.structured import AgentPlan, planner_prompt

async def plan_request(state: AgentState, runtime) -> dict:
    history = runtime.memory.recent(state["session_id"])
    # Dynamic tool arguments are valid function-call parameters but are not
    # permitted in OpenAI's strict JSON-schema response-format mode.
    plan = await runtime.llm.with_structured_output(
        AgentPlan, method="function_calling"
    ).ainvoke(
        planner_prompt(state["request"], runtime.registry.catalog(), history)
    )
    return {"plan": plan.model_dump(), "proposed_follow_ups": plan.proposed_follow_ups}