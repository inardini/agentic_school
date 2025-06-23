from google.adk.agents import Agent
from dotenv import load_dotenv

load_dotenv()

# Create a simple conversational agent without tools
root_agent = Agent(
    name="developer_assistant",
    model="gemini-2.0-flash",
    description="A helpful AI assistant for developers.",
    instruction=(
        "You are an expert developer assistant to support developers with their coding problems."
   ),
)