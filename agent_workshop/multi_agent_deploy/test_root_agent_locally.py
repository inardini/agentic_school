import asyncio
import aiofiles
import uuid
from typing import Any, Iterator, Optional

from root_agent import create_root_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from vertexai.preview.reasoning_engines import AdkApp
from vertexai import agent_engines

def chat_loop(
    app, user_id: Optional[str] = None, session_id: Optional[str] = None
) -> None:
    """Interactive chat loop for AI applications."""

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
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if not user_input or user_input.lower() in {"quit", "exit", "bye"}:
                break

            print("\nAssistant: ", end="", flush=True)

            response = _get_response_text(query_fn(user_input))
            print(response or "(No response generated)")

        except (KeyboardInterrupt, EOFError):
            print("\n\n🗑 Chat interrupted.")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            continue

    print("\n👋 Goodbye!")


def _print_startup_info(user_id: str, session_id: str) -> None:
    """Print startup information."""
    print("\n🚀 Starting chat...")
    print(f"👤 User ID: {user_id}")
    print(f"📁 Session ID: {session_id}")
    print("💬 Type 'exit' or 'quit' to end.")
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

async def main():
    session_service = InMemorySessionService()
    user_id = "test_user"
    session = await session_service.create_session(app_name="test_app", user_id=user_id)
    
    errlog = await aiofiles.open("error.log", "w+")
    
    root_agent = create_root_agent(errlog)

    runner = Runner(
        agent=root_agent, app_name="test_app", session_service=session_service
    )
    
    try:
        chat_loop(runner, user_id, session.id)
    finally:
        await errlog.close()

if __name__ == "__main__":
    asyncio.run(main())
