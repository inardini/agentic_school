import os
import asyncio
from multi_agent_deploy.root_agent import code_agent
from multi_agent_deploy.query_agent import run_queries
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

async def main():
    session_service = InMemorySessionService()
    user_id = "test_user"
    session = await session_service.create_session(app_name="test_app", user_id=user_id)
    runner = Runner(
        agent=code_agent, app_name="test_app", session_service=session_service
    )
    queries = [
        "Write a python script to parse a CSV file and print the first 5 rows."
    ]
    run_queries(runner, queries, user_id=user_id, session_id=session.id)

if __name__ == "__main__":
    asyncio.run(main())
