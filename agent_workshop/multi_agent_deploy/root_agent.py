import os
from google.adk.agents import Agent, LlmAgent, SequentialAgent, ParallelAgent, LoopAgent, BaseAgent
from google.adk.code_executors import BuiltInCodeExecutor
from google.adk.tools.tool_context import ToolContext
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from typing import AsyncGenerator
from google.adk.tools.langchain_tool import LangchainTool
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from google.adk.tools.mcp_tool import StdioConnectionParams
from langchain_community.utilities import ArxivAPIWrapper
from vertexai.preview.reasoning_engines import AdkApp

# Search Agent Tools
arxiv_wrapper = ArxivAPIWrapper()
arxiv_tool = LangchainTool(
    name="arxiv_search",
    description="Search ArXiv for academic papers and research",
    tool=arxiv_wrapper
)

reddit_mcp_tool = MCPToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command='uvx',
            args=[
                "--from",
                "git+https://github.com/adhikasp/mcp-reddit.git",
                "mcp-reddit"
            ],
            env={
                "MCP_SERVER_REQUEST_TIMEOUT": os.getenv(
                    "MCP_SERVER_REQUEST_TIMEOUT", "500"
                ),
            },
        ),
    )
)

# Search Agent
arxiv_researcher = LlmAgent(
                    name="arxiv_researcher",
                    model="gemini-2.0-flash", 
                    description="Searches ArXiv for academic papers and research",
                    instruction="Search ArXiv for relevant academic papers and research. Provide summaries of key findings.",
                    tools=[arxiv_tool],
                    output_key="arxiv_results"
                )

reddit_researcher = LlmAgent(
                    name="reddit_researcher",
                    model="gemini-2.0-flash", 
                    description="Searches Reddit for community discussions and experiences",
                    instruction="Search Reddit for relevant community discussions and experiences. Provide summaries of key findings.",
                    tools=[reddit_mcp_tool],
                    output_key="reddit_results"
                )

search_agent = ParallelAgent(
            name="search_coordinator",
            description="Coordinates parallel search across ArXiv and Reddit",
            sub_agents=[arxiv_researcher, reddit_researcher]
)

# Code Agent
STATE_USER_REQUEST = "user_request"
STATE_CURRENT_CODE = "current_code"
STATE_EXECUTION_RESULT = "execution_result"
SUCCESS_PHRASE = "Code executed successfully without errors."

def exit_code_loop(tool_context: ToolContext):
    """Call this function ONLY when code execution is successful, signaling the iterative process should end."""
    tool_context.actions.escalate = True
    return {}

class UserRequestSetter(BaseAgent):
    """A custom agent to extract the user's request from the conversation history
    and save it to the session state."""
    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        user_message = ""
        for event in reversed(ctx.session.events):
            if event.author == "user" and event.content and event.content.parts:
                user_message = event.content.parts[0].text
                break
        
        if user_message:
            ctx.session.state[STATE_USER_REQUEST] = user_message
        
        yield Event(author=self.name)

initial_code_generator = LlmAgent(
    name="InitialCodeGenerator",
    model="gemini-2.0-flash",
    instruction=f"Generate a Python code solution based on the user request: {{{STATE_USER_REQUEST}}}. Use the built-in urllib.request module instead of requests.",
    description="Generates initial Python code.",
    output_key=STATE_CURRENT_CODE
)

code_executor_agent = LlmAgent(
    name="CodeExecutorAgent",
    model="gemini-2.0-flash",
    instruction=f"Execute the following code: {{{STATE_CURRENT_CODE}}}. If it runs successfully, respond with the exact phrase '{SUCCESS_PHRASE}'. Otherwise, provide a clear error analysis.",
    description="Executes code and reports success or provides error analysis.",
    code_executor=BuiltInCodeExecutor(),
    output_key=STATE_EXECUTION_RESULT
)

code_refiner_agent = LlmAgent(
    name="CodeRefinerAgent",
    model="gemini-2.0-flash",
    instruction=f"Analyze the execution result in {{{STATE_EXECUTION_RESULT}}}. If the result is '{SUCCESS_PHRASE}', you MUST call the 'exit_code_loop' function. Otherwise, fix the code in {{{STATE_CURRENT_CODE}}} based on the error.",
    description="Refines code based on execution results, or exits the loop.",
    tools=[exit_code_loop],
    output_key=STATE_CURRENT_CODE
)

code_refinement_loop = LoopAgent(
    name="CodeRefinementLoop",
    sub_agents=[code_executor_agent, code_refiner_agent],
    max_iterations=3
)

code_agent = SequentialAgent(
    name="code_coordinator",
    description="Generates and iteratively refines code.",
    sub_agents=[UserRequestSetter(name="UserRequestSetter"), initial_code_generator, code_refinement_loop]
)


# Root Agent
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

# AdkApp
def session_service_builder():
  from google.adk.sessions import VertexAiSessionService
  return VertexAiSessionService(project=os.getenv("GOOGLE_CLOUD_PROJECT"), location=os.getenv("GOOGLE_CLOUD_LOCATION"))

agent_app = AdkApp(
    agent=root_agent,
    session_service_builder=session_service_builder
)
