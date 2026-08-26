import uuid
from langgraph.graph import END, START, StateGraph
from academic_agent.agent.observer import observe_results
from academic_agent.agent.planner import plan_request
from academic_agent.agent.responder import respond
from academic_agent.agent.routing import after_observe, after_plan
from academic_agent.agent.state import AgentState
from academic_agent.safety.permissions import evaluate_tool_permission

async def execute_tools(state: AgentState, runtime) -> dict:
    observations = list(state.get("observations", []))
    approvals = list(state.get("pending_approvals", []))
    approved = set(state.get("approved_action_ids", []))
    for call in state.get("plan", {}).get("tool_requests", []):
        tool = runtime.registry.get(call["tool_name"])
        if not tool:
            observations.append({"tool": call["tool_name"], "status": "unavailable", "detail": "Tool is not registered."})
            continue
        action_id = f"act_{uuid.uuid5(uuid.NAMESPACE_URL, call['tool_name'] + str(call.get('arguments', {}))).hex[:12]}"
        decision = evaluate_tool_permission(tool.side_effect, action_id in approved, state.get("actor_role"))
        if not decision.allowed:
            approvals.append({"id": action_id, "tool_name": tool.name, "arguments": call.get("arguments", {}), "purpose": call.get("purpose"), "side_effect": tool.side_effect.value, "reason": decision.reason})
            continue
        result = await runtime.gateway.invoke(tool, call.get("arguments", {}))
        observations.append({"tool": tool.name, "purpose": call.get("purpose"), **result})
    return {"observations": observations, "pending_approvals": approvals, "plan": {**state.get("plan", {}), "tool_requests": []}}

# IMPORTANT: Define async node functions that take the runtime from closure
def build_graph(runtime, checkpointer):
    graph = StateGraph(AgentState)
    
    # Define async functions inside build_graph so they have access to runtime
    async def plan_node(state):
        return await plan_request(state, runtime)
    
    async def execute_node(state):
        return await execute_tools(state, runtime)
    
    async def observe_node(state):
        return await observe_results(state, runtime)
    
    def respond_node(state):
        return respond(state, runtime)
    
    # Add nodes with async functions directly
    graph.add_node("plan", plan_node)
    graph.add_node("execute", execute_node)
    graph.add_node("observe", observe_node)
    graph.add_node("respond", respond_node)
    
    graph.add_edge(START, "plan")
    graph.add_conditional_edges("plan", after_plan, {"execute": "execute", "respond": "respond"})
    graph.add_edge("execute", "observe")
    graph.add_conditional_edges("observe", after_observe, {"execute": "execute", "respond": "respond"})
    graph.add_edge("respond", END)
    
    return graph.compile(checkpointer=checkpointer)