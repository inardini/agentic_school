from google.adk.agents import  LoopAgent, LlmAgent, SequentialAgent
from google.adk.code_executors import BuiltInCodeExecutor
from google.adk.tools.tool_context import ToolContext

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

initial_code_generator = LlmAgent(
    name="InitialCodeGenerator",
    model="gemini-2.0-flash",
    instruction=f"Generate a Python code solution based on the user request: {{{STATE_USER_REQUEST}}}",
    description="Generates initial Python code.",
    output_key=STATE_CURRENT_CODE
)

code_executor_agent = LlmAgent(
    name="CodeExecutorAgent",
    model="gemini-2.0-flash",
    instruction=f"Execute the code in {{{STATE_CURRENT_CODE}}}. If it runs successfully, respond with the exact phrase '{SUCCESS_PHRASE}'. Otherwise, provide a clear error analysis.",
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
    sub_agents=[initial_code_generator, code_refinement_loop]
)

# # Define initial code generator
# initial_code_generator = LlmAgent(
#     name="InitialCodeGenerator",
#     model="gemini-2.0-flash",
#     include_contents='none',
#     instruction=f"""You are a Python Code Generator. 
#     Create a complete, runnable Python code solution based on the user request.
    
#     User Request: {{{STATE_USER_REQUEST}}}
    
#     **Guidelines:**
#     - Write clean, well-documented Python code
#     - Include necessary imports
#     - Add comments for clarity
#     - Make sure the code is complete and executable
#     - Focus on functionality over optimization in the first draft
    
#     Output *only* the Python code. Do not add explanations or markdown formatting.
#     """,
#     description="Generates initial Python code based on user requirements.",
#     output_key=STATE_CURRENT_CODE
# )

# # Define code executor agent
# code_executor_agent = LlmAgent(
#     name="CodeExecutorAgent",
#     model="gemini-2.0-flash",
#     include_contents='none',
#     instruction=f"""You are a Code Execution Agent that tests Python code.
    
#     **Code to Execute:**
#     ```python
#     {{current_code}}
#     ```
    
#     **Task:**
#     Execute the provided code using the code execution capabilities.
#     Analyze the execution results and provide feedback.
    
#     IF the code executes successfully without any errors:
#     Output *exactly* the phrase "{SUCCESS_PHRASE}" and nothing else.
    
#     ELSE IF there are errors or issues:
#     Provide a clear, concise error analysis explaining what went wrong.
#     Focus on actionable feedback that can help fix the code.
    
#     Output only the success phrase OR the error analysis.
#     """,
#     description="Executes code and reports success or provides error analysis.",
#     code_executor=BuiltInCodeExecutor(),
#     output_key=STATE_EXECUTION_RESULT
# )

# # Define code refiner agent
# code_refiner_agent = LlmAgent(
#     name="CodeRefinerAgent",
#     model="gemini-2.0-flash",
#     include_contents='none',
#     instruction=f"""You are a Code Refiner that improves Python code based on execution results.
    
#     **Current Code:**
#     ```python
#     {{current_code}}
#     ```
    
#     **Execution Result:**
#     {{execution_result}}
    
#     **Original User Request:**
#     {{user_request}}
    
#     **Task:**
#     Analyze the execution result.
    
#     IF the execution result is *exactly* "{SUCCESS_PHRASE}":
#     You MUST call the 'exit_code_loop' function. Do not output any text.
    
#     ELSE (there are errors to fix):
#     Carefully analyze the error and fix the code. Apply the necessary changes to resolve the issues.
#     Output *only* the corrected Python code.
    
#     Do not add explanations. Either output the fixed code OR call the exit_code_loop function.
#     """,
#     description="Refines code based on execution results, or calls exit_code_loop if execution is successful.",
#     tools=[exit_code_loop],
#     output_key=STATE_CURRENT_CODE
# )

# # Define code refinement loop
# code_refinement_loop = LoopAgent(
#     name="CodeRefinementLoop",
#     sub_agents=[
#         code_executor_agent,  
#         code_refiner_agent,   
#     ],
#     max_iterations=3  
# )


# # Define the code agent
# code_agent = SequentialAgent(
#             name="code_coordinator",
#             description="Generates initial code and then iteratively refines it through execution testing",
#             sub_agents=[
#                 initial_code_generator,  
#                 code_refinement_loop     
#             ]
#         )