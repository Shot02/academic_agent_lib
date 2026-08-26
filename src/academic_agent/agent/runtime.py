from typing import Any, Optional
from langgraph.checkpoint.memory import MemorySaver
from academic_agent.agent.graph import build_graph
from academic_agent.config import Settings, get_settings
from academic_agent.llm.structured import build_llm
from academic_agent.memory.manager import MemoryManager
from academic_agent.tools.adapter import ToolGateway
from academic_agent.tools.registry import ToolRegistry, ToolDefinition

class AgentRuntime:
    """Main runtime for the academic agent."""
    
    def __init__(self, settings: Optional[Settings] = None) -> None:
        self.settings = settings or get_settings()
        self.llm = build_llm(self.settings)
        self.registry = ToolRegistry()
        self.gateway = ToolGateway(self.settings)
        self.memory = MemoryManager(self.settings.memory_window)
        self.graph = build_graph(self, MemorySaver())
    
    async def run(
        self,
        request: str,
        session_id: str = "default",
        actor_role: Optional[str] = None,
        approved_action_ids: Optional[list[str]] = None
    ) -> dict[str, Any]:
        """Run the agent with a user request."""
        state = {
            "request": request,
            "session_id": session_id,
            "actor_role": actor_role,
            "approved_action_ids": approved_action_ids or [],
            "observations": [],
            "pending_approvals": [],
            "loop_count": 0
        }
        result = await self.graph.ainvoke(
            state,
            {"configurable": {"thread_id": session_id}}
        )
        return {
            "response": result.get("response"),
            "observations": result.get("observations", []),
            "pending_approvals": result.get("pending_approvals", []),
            "proposed_follow_ups": result.get("proposed_follow_ups", [])
        }
    
    def register_tool(self, tool_definition: dict) -> dict:
        """Register a tool with the agent."""
        tool = ToolDefinition(**tool_definition)
        return self.registry.register(tool)
    
    def register_tools(self, tool_definitions: list[dict]) -> list[dict]:
        """Register multiple tools at once."""
        return [self.register_tool(td) for td in tool_definitions]
    
    def list_tools(self) -> list[dict]:
        """List all registered tools."""
        return self.registry.catalog()
    
    def get_tool(self, name: str) -> Optional[ToolDefinition]:
        """Get a specific tool by name."""
        return self.registry.get(name)
    
    def clear_memory(self, session_id: str) -> None:
        """Clear conversation history for a session."""
        self.memory._sessions.pop(session_id, None)