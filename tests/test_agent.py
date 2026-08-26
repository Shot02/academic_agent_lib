import pytest
import asyncio
from academic_agentic import AgentRuntime

@pytest.fixture
def runtime():
    return AgentRuntime()

@pytest.mark.asyncio
async def test_basic_response(runtime):
    """Test that the agent responds to a basic message."""
    response = await runtime.run("Hello", session_id="test1")
    assert response["response"] is not None
    assert isinstance(response["observations"], list)
    assert isinstance(response["pending_approvals"], list)

@pytest.mark.asyncio
async def test_tool_registration(runtime):
    """Test tool registration."""
    runtime.register_tool({
        "name": "test_tool",
        "description": "Test tool",
        "input_schema": {"type": "object", "properties": {}},
        "side_effect": "read"
    })
    tools = runtime.list_tools()
    assert any(t["name"] == "test_tool" for t in tools)

@pytest.mark.asyncio
async def test_write_requires_approval(runtime):
    """Test that write operations require approval."""
    runtime.register_tool({
        "name": "update_grade",
        "description": "Update grade",
        "input_schema": {"type": "object", "properties": {}},
        "side_effect": "write"
    })
    
    response = await runtime.run(
        "Update grade for student 123 to A+",
        session_id="test3",
        actor_role="teacher"
    )
    
    # Should have pending approvals
    assert len(response["pending_approvals"]) > 0