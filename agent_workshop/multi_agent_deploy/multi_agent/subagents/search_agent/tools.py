import os
from google.adk.tools.langchain_tool import LangchainTool
from langchain_community.utilities import ArxivAPIWrapper


# ArXiv search tool using LangChain
arxiv_wrapper = ArxivAPIWrapper()
arxiv_tool = LangchainTool(
    name="arxiv_search",
    description="Search ArXiv for academic papers and research",
    tool=arxiv_wrapper
)
