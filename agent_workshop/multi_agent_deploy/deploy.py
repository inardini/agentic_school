import os
import vertexai
from vertexai import agent_engines
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Vertex AI
vertexai.init(
    project=os.getenv("GOOGLE_CLOUD_PROJECT"),
    location=os.getenv("GOOGLE_CLOUD_LOCATION"),
    staging_bucket=os.getenv("GOOGLE_CLOUD_BUCKET"),
)

print("Deploying multi-agent system to Vertex AI Agent Engine...")

# Create and deploy the agent engine
remote_app = agent_engines.create(
    display_name="hello_agent",
    description="A simple hello world agent.",
    agent_engine=agent_engines.ModuleAgent(
        module_name="root_agent",
        agent_name="agent_app",
        register_operations={
            "": ["get_session", "list_sessions", "create_session", "delete_session"],
            "async": [
                "async_get_session",
                "async_list_sessions",
                "async_create_session",
                "async_delete_session",
            ],
            "stream": ["stream_query", "streaming_agent_run_with_events"],
            "async_stream": ["async_stream_query"],
        },
    ),
    requirements=[
        "google-cloud-aiplatform[adk,agent_engines]",
        "langchain-community",
        "arxiv",
        "python-dotenv"
    ],
    extra_packages=[
        "root_agent.py",
    ],
    env_vars={
        "PROJECT_ID": os.getenv("GOOGLE_CLOUD_PROJECT"),
        "LOCATION": os.getenv("GOOGLE_CLOUD_LOCATION"),
    },
)

print(f"Agent deployed successfully!")
print(f"App ID: {remote_app.resource_name}")
print(f"Display Name: {remote_app.display_name}")
