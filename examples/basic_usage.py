import asyncio
from academic_agent import AgentRuntime

async def main():
    # Initialize the agent
    runtime = AgentRuntime()
    
    # Register tools
    tools = [
        {
            "name": "get_attendance",
            "description": "Get attendance records for a class",
            "input_schema": {
                "type": "object",
                "properties": {
                    "class_name": {"type": "string"}
                }
            },
            "side_effect": "read"
        },
        {
            "name": "update_grade",
            "description": "Update a student's grade",
            "input_schema": {
                "type": "object",
                "properties": {
                    "student_id": {"type": "string"},
                    "grade": {"type": "string"}
                }
            },
            "side_effect": "write"
        }
    ]
    
    # Register all tools
    runtime.register_tools(tools)
    
    # Print available tools
    print("Available tools:", runtime.list_tools())
    
    # Run the agent
    response = await runtime.run(
        "Get attendance for 5th grade",
        session_id="example1",
        actor_role="teacher"
    )
    
    print("\nResponse:", response["response"])
    print("Observations:", response["observations"])
    print("Pending approvals:", response["pending_approvals"])
    print("Follow-ups:", response["proposed_follow_ups"])
    
    # Test write operation
    response = await runtime.run(
        "Update grade for student 123 to A+",
        session_id="example2",
        actor_role="teacher"
    )
    
    print("\nWrite Response:", response["response"])
    print("Pending approvals:", response["pending_approvals"])

if __name__ == "__main__":
    asyncio.run(main())