# Lesson 1: Your First Basic Agent

## Purpose of this Lesson

This lesson introduces the most fundamental concept in the Agent Development Kit (ADK): creating a simple, conversational AI agent. The goal is to understand the minimal components required to build and run an agent that can respond to user input based on a set of instructions.

This agent is a simple "developer assistant" that has a predefined persona but no external capabilities (tools).

## Technical Background

*   **`LlmAgent`**: This is the core class for creating an agent powered by a Large Language Model (LLM). It handles the interaction with the model, including sending the prompt and receiving the response.
*   **`name`**: A unique identifier for your agent.
*   **`model`**: Specifies which LLM to use (e.g., `"gemini-2.0-flash"`). The ADK can connect to various models, including Google's Gemini family and others through LiteLLM.
*   **`instruction`**: This is the most critical part of a basic agent. It's a string that defines the agent's persona, its capabilities, and the rules it must follow. The quality of your instructions directly impacts the agent's performance and behavior.

The code for this agent is straightforward:

```python
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
```

## How to Run this Agent

1.  **Activate your virtual environment:**
    Make sure you have followed the setup instructions in the main `README.md` of this repository.
    ```bash
    source .venv/bin/activate
    ```

2.  **Run the agent using the ADK CLI:**
    The `adk run` command starts an interactive chat session with your agent in the terminal.
    ```bash
    adk run /home/user/agentic_school/agent_workshop/single_agent
    ```

3.  **Interact with the agent:**
    Once the agent is running, you can type your questions and see its responses. For example, try asking: "What is the best way to learn Python?"
