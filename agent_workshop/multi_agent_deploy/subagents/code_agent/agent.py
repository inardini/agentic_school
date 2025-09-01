from google.adk.agents import LoopAgent, LlmAgent, SequentialAgent, BaseAgent
from google.adk.code_executors import BuiltInCodeExecutor
from google.adk.tools.tool_context import ToolContext
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from typing import AsyncGenerator

# State keys
STATE_USER_REQUEST = "user_request"
STATE_CURRENT_CODE = "current_code"
STATE_EXECUTION_RESULT = "execution_result"
STATE_ERROR_MESSAGE = "error_message"
STATE_ITERATION_COUNT = "iteration_count"
SUCCESS_PHRASE = "Code executed successfully without errors."

# Tool Definition
def exit_code_loop(tool_context: ToolContext):
    """Call this function ONLY when code execution is successful, signaling the iterative process should end."""
    print(f"  [Tool Call] exit_code_loop triggered by {tool_context.agent_name}")
    tool_context.actions.escalate = True
    return {}

def set_state(tool_context: ToolContext, key: str, value: str) -> dict:
    """Sets a value in the session state."""
    tool_context.state[key] = value
    print(f"  [Tool Call] set_state: Set '{key}' to '{value}'")
    return {"status": "success"}

class UserRequestSetter(BaseAgent):
    """A custom agent to extract the user's request from the conversation history
    and save it to the session state."""
    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        user_message = ""
        # Iterate backwards through events to find the last user message
        for event in reversed(ctx.session.events):
            if event.author == "user" and event.content and event.content.parts:
                # Extract text from the first part of the content
                user_message = event.content.parts[0].text
                break
        
        if user_message:
            ctx.session.state[STATE_USER_REQUEST] = user_message
        
        # Yield a simple event to signal completion without generating output
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
