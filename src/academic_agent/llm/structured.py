from typing import Any
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from academic_agent.config import Settings
from academic_agent.llm.prompts import SYSTEM_PROMPT

class ToolRequest(BaseModel):
    tool_name: str
    arguments: dict[str, Any] = Field(default_factory=dict)
    purpose: str

class AgentPlan(BaseModel):
    summary: str
    needs_clarification: bool = False
    clarification_question: str | None = None
    tool_requests: list[ToolRequest] = Field(default_factory=list)
    proposed_follow_ups: list[str] = Field(default_factory=list)

class ObservationAssessment(BaseModel):
    findings: list[str] = Field(default_factory=list)
    anomalies_or_opportunities: list[str] = Field(default_factory=list)
    follow_up_tool_requests: list[ToolRequest] = Field(default_factory=list)
    final_response: str

def build_llm(settings: Settings) -> ChatOpenAI:
    return ChatOpenAI(model=settings.openai_model, api_key=settings.openai_api_key, temperature=0)

def planner_prompt(request: str, tools: list[dict[str, Any]], history: list[str]) -> str:
    return f"""{SYSTEM_PROMPT}\n\nStaff request: {request}\n\nAvailable tools (use only these exact names): {tools}\n\nRecent context: {history}\n\nProduce a concise plan. For actions with a non-read side effect, include the requested tool but make clear it requires approval. Never invent tool parameters."""

def observer_prompt(request: str, observations: list[dict[str, Any]], tools: list[dict[str, Any]]) -> str:
    return f"""{SYSTEM_PROMPT}\n\nOriginal staff request: {request}\n\nTool observations: {observations}\n\nAvailable tools: {tools}\n\nAssess findings, including any meaningful anomaly or opportunity. Request follow-up read tools only when necessary. Give a helpful final response grounded in the observations."""