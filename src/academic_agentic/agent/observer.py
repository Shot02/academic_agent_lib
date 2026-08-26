from academic_agentic.agent.state import AgentState
from academic_agentic.llm.structured import ObservationAssessment, observer_prompt

async def observe_results(state: AgentState, runtime) -> dict:
    assessment = await runtime.llm.with_structured_output(
        ObservationAssessment, method="function_calling"
    ).ainvoke(
        observer_prompt(state["request"], state.get("observations", []), runtime.registry.catalog())
    )
    plan = state.get("plan", {})
    plan["tool_requests"] = [x.model_dump() for x in assessment.follow_up_tool_requests]
    return {"plan": plan, "proposed_follow_ups": assessment.anomalies_or_opportunities, "response": assessment.final_response, "loop_count": state.get("loop_count", 0) + 1}
