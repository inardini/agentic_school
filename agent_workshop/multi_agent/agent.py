from google.adk.agents import Agent
from .subagents.search_agent.agent import search_agent
from .subagents.code_agent.agent import code_agent
from dotenv import load_dotenv

load_dotenv()


root_agent = Agent(
    name="developer_assistant",
    model="gemini-2.0-flash", 
    description="An advanced developer assistant that can search for information and generate code solutions",
    instruction="""You are an advanced developer assistant. You can help with:

1. Researching topics using ArXiv papers and Reddit discussions

When a user asks for research, delegate to the 'search_coordinator' agent.

When a user asks for code solutions, delegate to the 'code_coordinator' agent.

When a user asks for both research and code, coordinate between both agents as needed.

Always provide comprehensive and helpful responses based on the specialized agents' outputs.""",
    sub_agents=[
        search_agent,
        code_agent
    ]
)