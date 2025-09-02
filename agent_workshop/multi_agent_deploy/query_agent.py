import os
import uuid
import vertexai
from vertexai import agent_engines
from typing import Any, Iterator, Optional
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools.mcp_tool import StdioConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import (
    MCPToolset,
    StdioServerParameters,
)
from google.genai import types
from vertexai.preview.reasoning_engines import AdkApp

def run_queries(
    app, queries: list[str], user_id: Optional[str] = None, session_id: Optional[str] = None
) -> None:
    """Run a list of queries against an AI application."""

    # Simple setup
    user_id = user_id or f"u_{uuid.uuid4().hex[:8]}"

    # Handle session based on app type
    if isinstance(app, (AdkApp, agent_engines.AgentEngine)):
        # Only create session if session_id is not provided
        if not session_id:
            session = app.create_session(user_id=user_id)
            # Handle both dict and object session responses
            if isinstance(session, dict):
                session_id = session["id"]
            else:
                session_id = session.id

        def query_fn(msg: str):
            return app.stream_query(user_id=user_id, session_id=session_id, message=msg)

    elif isinstance(app, Runner):
        session_id = session_id or f"s_{uuid.uuid4().hex[:8]}"

        def query_fn(msg: str):
            return app.run(
                user_id=user_id,
                session_id=session_id,
                new_message=types.Content(role="user", parts=[types.Part(text=msg)]),
            )

    else:
        raise TypeError(
            f"Unsupported app type: {type(app)}. Expected AdkApp, AgentEngine, or Runner."
        )

    _print_startup_info(user_id, session_id)

    # Main loop
    for query in queries:
        try:
            print(f"\nYou: {query}")
            print("\nAssistant: ", end="", flush=True)

            response = _get_response_text(query_fn(query))
            print(response or "(No response generated)")

        except Exception as e:
            print(f"\nError: {e}")
            continue

    print("\nGoodbye!")


def _print_startup_info(user_id: str, session_id: str) -> None:
    """Print startup information."""
    print("\nStarting chat...")
    print(f"User ID: {user_id}")
    print(f"Session ID: {session_id}")
    print("-" * 50)


def _get_response_text(events: Iterator[Any]) -> str:
    """Extract response text from event stream."""
    responses = []

    for event in events:
        # Handle dict-like events (AgentEngine format)
        if isinstance(event, dict):
            text = _extract_from_dict_event(event)
        # Handle object-like events
        else:
            text = _extract_from_object_event(event)

        if text:
            responses.append(text)
            # Print streaming text in real-time
            print(text, end="", flush=True)

    return "".join(responses)


def _extract_from_dict_event(event: dict) -> Optional[str]:
    """Extract text from dictionary-style events (AgentEngine format)."""
    # Handle AgentEngine response format
    if "parts" in event and "role" in event:
        # Only extract text from model responses, skip function calls/responses
        if event.get("role") == "model":
            parts = event.get("parts", [])
            text_parts = []

            for part in parts:
                # Extract text content, skip function calls
                if isinstance(part, dict) and "text" in part:
                    text_parts.append(part["text"])

            return "".join(text_parts) if text_parts else None
        return None

    # Handle other dict formats
    content = event.get("content", {})
    if isinstance(content, str):
        return content

    parts = content.get("parts", [])
    if not parts:
        return None

    text_parts = []
    for part in parts:
        if isinstance(part, dict) and "text" in part:
            text_parts.append(part["text"])

    return "".join(text_parts) if text_parts else None


def _extract_from_object_event(event: Any) -> Optional[str]:
    """Extract text from object-style events."""
    # Handle string content directly
    content = getattr(event, "content", None)
    if isinstance(content, str):
        return content

    # Handle content with parts
    if content and hasattr(content, "parts"):
        text_parts = []
        for part in content.parts:
            if hasattr(part, "text") and part.text:
                text_parts.append(part.text)
        return "".join(text_parts) if text_parts else None

    # Handle direct text attribute
    return getattr(event, "text", None)

if __name__ == "__main__":
    vertexai.init(
        project=os.getenv("GOOGLE_CLOUD_PROJECT"),
        location=os.getenv("GOOGLE_CLOUD_LOCATION"),
    )
    agent_engine = agent_engines.get("projects/974417049733/locations/us-central1/reasoningEngines/4739550424644714496")
    queries = [
        "What are the latest advancements in Large Language Models?",
        "What are the best subreddits for learning about prompt engineering?",
        "Write a python function to reverse a string."
    ]
    run_queries(agent_engine, queries)
