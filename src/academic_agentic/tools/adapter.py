from typing import Any
import httpx
from academic_agentic.config import Settings
from academic_agentic.tools.registry import ToolDefinition

class ToolGateway:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
    
    async def invoke(self, tool: ToolDefinition, arguments: dict[str, Any]) -> dict[str, Any]:
        if not self.settings.tool_gateway_url:
            return {"status": "unavailable", "detail": "No TOOL_GATEWAY_URL is configured for this registered tool."}
        headers = {"Authorization": f"Bearer {self.settings.tool_gateway_token}"} if self.settings.tool_gateway_token else {}
        url = f"{self.settings.tool_gateway_url.rstrip('/')}/tools/{tool.name}/invoke"
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(url, json={"arguments": arguments}, headers=headers)
                response.raise_for_status()
                return {"status": "ok", "data": response.json()}
        except httpx.HTTPError as exc:
            return {"status": "error", "detail": str(exc)}