from google.adk.agents import Agent
from .tools import all_tools
from dotenv import load_dotenv

load_dotenv()

# Create the developer assistant with exactly 5 tools
root_agent = Agent(
    name="developer_assistant",
    model="gemini-2.0-flash",
    description="A helpful AI assistant for developers with access to academic papers, web scraping, code execution, Reddit discussions, and JSON validation.",
    instruction=(
        "You are an expert developer assistant with access to multiple tools. "
        "You can help with:\n"
        "- Searching academic papers on ArXiv for research\n"
        "- Scraping websites for information\n"
        "- Searching Reddit for developer discussions and solutions\n"
        "- Validating and formatting JSON data\n\n"
        "Always be helpful, accurate, and provide detailed explanations. "
        "Use the appropriate tools to gather information and solve problems effectively."
    ),
    tools=all_tools,
)