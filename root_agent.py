import os
from google.adk.agents import LlmAgent
from vertexai.preview.reasoning_engines import AdkApp

def create_root_agent(errlog):
    return LlmAgent(
        model="gemini-2.0-flash",
        name="hello_agent",
        instruction="Just say hello world.",
    )

def session_service_builder():
  from google.adk.sessions import VertexAiSessionService
  return VertexAiSessionService(project=os.getenv("GOOGLE_CLOUD_PROJECT"), location=os.getenv("GOOGLE_CLOUD_LOCATION"))

agent_app = AdkApp(
    agent=create_root_agent(None),
    session_service_builder=session_service_builder
)