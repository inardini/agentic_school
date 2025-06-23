from google.adk.agents import ParallelAgent, LlmAgent
from .tools import arxiv_tool, reddit_mcp_tool

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
