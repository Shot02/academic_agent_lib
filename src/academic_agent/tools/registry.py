from typing import Any
from pydantic import BaseModel, Field
from academic_agent.safety.policy import SideEffect

class ToolDefinition(BaseModel):
    name: str = Field(pattern=r"^[a-zA-Z][a-zA-Z0-9_-]{1,80}$")
    description: str
    input_schema: dict[str, Any] = Field(default_factory=lambda: {"type": "object", "properties": {}})
    side_effect: SideEffect = SideEffect.READ
    tags: list[str] = Field(default_factory=list)

class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolDefinition] = {}
    
    def register(self, tool: ToolDefinition) -> ToolDefinition:
        self._tools[tool.name] = tool
        return tool
    
    def get(self, name: str) -> ToolDefinition | None:
        return self._tools.get(name)
    
    def catalog(self) -> list[dict[str, Any]]:
        return [tool.model_dump() for tool in self._tools.values()]