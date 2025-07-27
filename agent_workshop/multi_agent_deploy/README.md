# Lesson 4: Deploying a Multi-Agent System

## Purpose of this Lesson

This lesson demonstrates how to take a multi-agent system, like the one in the previous lesson, and prepare it for deployment as a standalone application. This involves creating a queryable endpoint that can be used to interact with the agent.

This example is very similar to the `multi_agent` example, but it includes a `query_agent.py` script that shows how to programmatically interact with the agent.

## Technical Background

*   **`Runner`**: The `Runner` class is the main entry point for interacting with an agent programmatically. It manages the agent's lifecycle, the event loop, and coordinates with the various services (like the session service).
*   **`SessionService`**: This service is responsible for creating, retrieving, and managing conversation sessions. The `InMemorySessionService` is a simple implementation that stores session data in memory.
*   **`run_async`**: This is the main method of the `Runner` class. It takes a user's message and returns an asynchronous generator that yields events as the agent processes the request.

The `query_agent.py` script shows how to use these components to interact with the agent:

```python
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
```

## How to Run this Agent

1.  **Activate your virtual environment:**
    ```bash
    source .venv/bin/activate
    ```

2.  **Run the `query_agent.py` script:**
    ```bash
    python /home/user/agentic_school/agent_workshop/multi_agent_deploy/query_agent.py
    ```

This will run the agent with the hardcoded query and print the final generated code to the console.

