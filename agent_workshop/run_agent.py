import asyncio

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from multi_agent.agent import root_agent
from google.genai import types as genai_types


async def main():
    """Runs the agent with a sample query."""
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name="app", user_id="test_user", session_id="test_session"
    )
    runner = Runner(
        agent=root_agent, app_name="app", session_service=session_service
    )
    query = "Create a python script to print 'hello world'."
    async for event in runner.run_async(
        user_id="test_user",
        session_id=session.id,
        new_message=genai_types.Content(
            role="user", 
            parts=[genai_types.Part.from_text(text=query)]
        ),
    ):
        if event.is_final_response():
            pass

    # Get the session again to get the updated state
    updated_session = await session_service.get_session(app_name="app", user_id="test_user", session_id=session.id)
    # Print the final generated code from the session state
    final_code = updated_session.state.get("current_code")
    if final_code:
        cleaned_code = final_code.replace("```python", "").replace("```", "").strip()
        print(f"```python\n{cleaned_code}\n```")


if __name__ == "__main__":
    asyncio.run(main())
