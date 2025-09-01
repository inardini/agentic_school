from google.adk.agents import LlmAgent

root_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="single_agent",
    instruction="You are a helpful assistant.",
)
