import os
import vertexai
from vertexai import agent_engines
from dotenv import load_dotenv
from multi_agent.agent import root_agent
from uuid import uuid4

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
    display_name="my_agent",
    agent_engine=root_agent,
    requirements=[
        "google-cloud-aiplatform[adk,agent_engines]",
        "langchain-community",
        "arxiv",
        "python-dotenv"
    ],
    extra_packages=[
        "./multi_agent"
    ]
)

print(f"Agent deployed successfully!")
print(f"App ID: {remote_app.resource_name}")
print(f"Display Name: {remote_app.display_name}")