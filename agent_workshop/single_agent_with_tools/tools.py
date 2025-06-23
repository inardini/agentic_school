import os
import json
from google.adk.tools.langchain_tool import LangchainTool
from google.adk.tools.crewai_tool import CrewaiTool
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from crewai_tools import ScrapeWebsiteTool
from langchain_community.utilities import ArxivAPIWrapper

def json_validator(json_string: str) -> dict:
    """
    Validate JSON strings for developers.
    
    Args:
        json_string (str): JSON string to validate
        
    Returns:
        dict: Validation result with status and data
    """
    try:
        parsed = json.loads(json_string.strip())
        return {"status": "success", "data": parsed}
    except Exception as e:
        print(f"TOOL ERROR: {e}")
        return {"status": "error", "error_message": f"Tool failed: {type(e).__name__}"}

arxiv_wrapper = ArxivAPIWrapper(
        top_k_results=3,
        doc_content_chars_max=4000
    )
langchain_tool = LangchainTool(
        name="arxiv_search",
        description="Search academic papers on ArXiv by topic, author, or paper ID",
        tool=arxiv_wrapper
    )

crewai_tool = CrewaiTool(
    name="WebScraper",
    description="Scrape content from websites, documentation, GitHub repos, and tutorials",
    tool=ScrapeWebsiteTool()
)

mcp_reddit_tool = MCPToolset(
    connection_params=StdioServerParameters(
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


json_tool = json_validator

all_tools = [
    langchain_tool,         
    crewai_tool, 
    mcp_reddit_tool,       
    json_tool,             
]