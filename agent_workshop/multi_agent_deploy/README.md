# Lesson 3: Building a Multi-Agent System

## Purpose of this Lesson

This lesson introduces the concept of **multi-agent systems**. Instead of a single, monolithic agent, you can create a team of specialized agents that collaborate to solve complex problems. This approach promotes modularity, reusability, and can lead to more robust and capable AI systems.

This example features a "developer assistant" that acts as a coordinator, delegating tasks to two specialized sub-agents: a `search_agent` and a `code_agent`.

## Technical Background

*   **`sub_agents`**: The `LlmAgent` constructor has a `sub_agents` parameter, which is a list of other agent instances that the parent agent can delegate tasks to.
*   **Delegation**: The parent agent uses its LLM to decide which sub-agent is best suited to handle a particular request. It then delegates the task to that sub-agent. This is a powerful way to build complex systems from simpler components.
*   **`SequentialAgent`**: This is a type of workflow agent that executes a series of sub-agents in a specific order. It's useful for creating pipelines where the output of one agent becomes the input of the next.
*   **`LoopAgent`**: This is another workflow agent that repeatedly executes its sub-agents until a certain condition is met. This is useful for iterative processes like code generation and refinement.

The root agent in this example is a coordinator:

```python
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
```

## How to Run this Agent

1.  **Activate your virtual environment:**
    ```bash
    source .venv/bin/activate
    ```

2.  **Run the agent using the ADK CLI:**
    ```bash
    adk run /home/user/agentic_school/agent_workshop/multi_agent
    ```

3.  **Interact with the agent:**
    Try asking a question that requires delegation. For example: "Create a python script to print 'hello world'."
