import os
from google.adk.tools.langchain_tool import LangchainTool
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from langchain_community.utilities import ArxivAPIWrapper


# ArXiv search tool using LangChain
arxiv_wrapper = ArxivAPIWrapper()
arxiv_tool = LangchainTool(
    name="arxiv_search",
    description="Search ArXiv for academic papers and research",
    tool=arxiv_wrapper
)

# Reddit MCP tool
reddit_mcp_tool = MCPToolset(
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
