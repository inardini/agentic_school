# Lesson 2: Enhancing an Agent with Tools

## Purpose of this Lesson

This lesson builds upon the basic agent by introducing **tools**. Tools are functions that an agent can call to interact with the outside world, access knowledge bases, or perform specific tasks. This example demonstrates how to create an agent that can use a variety of tools to answer more complex questions.

This agent is a "developer assistant" that can search ArXiv, scrape websites, search Reddit, and validate JSON.

## Technical Background

*   **Tools**: In the ADK, a tool is simply a Python function with type hints and a docstring. The agent's LLM uses the function signature and docstring to understand what the tool does and how to use it.
*   **`tools` parameter**: The `LlmAgent` constructor takes a `tools` parameter, which is a list of the tool functions that the agent can use.
*   **Tool Calling**: When a user asks a question that requires a tool, the LLM doesn't answer directly. Instead, it generates a special response called a "tool call," which specifies the tool to use and the arguments to pass to it. The ADK framework then executes the tool and returns the result to the agent, which uses it to formulate the final answer.

The agent is defined like this:

```python
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
```

## How to Run this Agent

1.  **Activate your virtual environment:**
    ```bash
    source .venv/bin/activate
    ```

2.  **Run the agent using the ADK CLI:**
    ```bash
    adk run /home/user/agentic_school/agent_workshop/single_agent_with_tools
    ```

3.  **Interact with the agent:**
    Try asking a question that requires a tool. For example: "Search for papers on ArXiv about reinforcement learning."

```