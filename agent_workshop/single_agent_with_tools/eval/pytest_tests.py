"""
Pytest-based tests for developer assistant agent.
Tests the 4 available tools: ArXiv search, web scraping, Reddit search, and JSON validation.
"""
import pytest
from google.adk.evaluation.agent_evaluator import AgentEvaluator


@pytest.mark.asyncio
async def test_json_validation_tool():
    """Test the JSON validation functionality."""
    await AgentEvaluator.evaluate(
        agent_module="single_agent_with_tools",
        eval_dataset_file_path_or_dir="single_agent_with_tools/eval/test_dev_agent.test.json",
    )


@pytest.mark.asyncio
async def test_arxiv_search_tool():
    """Test the ArXiv search functionality."""
    await AgentEvaluator.evaluate(
        agent_module="single_agent_with_tools",
        eval_dataset_file_path_or_dir="single_agent_with_tools/eval/test_dev_agent.test.json",
    )


@pytest.mark.asyncio
async def test_web_scraping_tool():
    """Test the web scraping functionality."""
    await AgentEvaluator.evaluate(
        agent_module="single_agent_with_tools",
        eval_dataset_file_path_or_dir="single_agent_with_tools/eval/test_dev_agent.test.json",
    )


@pytest.mark.asyncio
async def test_reddit_search_tool():
    """Test the Reddit search functionality."""
    await AgentEvaluator.evaluate(
        agent_module="single_agent_with_tools",
        eval_dataset_file_path_or_dir="single_agent_with_tools/eval/test_dev_agent.test.json",
    )


@pytest.mark.asyncio
async def test_integration_workflow():
    """Test complex multi-tool workflows."""
    await AgentEvaluator.evaluate(
        agent_module="single_agent_with_tools",
        eval_dataset_file_path_or_dir="single_agent_with_tools/eval/integration_tests_evalset.json",
    )


class TestDeveloperAssistant:
    """Test class for developer assistant agent with 4 tools."""
    
    @pytest.mark.asyncio
    async def test_individual_tools(self):
        """Test each tool individually."""
        await AgentEvaluator.evaluate(
            agent_module="single_agent_with_tools",
            eval_dataset_file_path_or_dir="single_agent_with_tools/eval/test_dev_agent.test.json",
        )
    
    @pytest.mark.asyncio
    async def test_research_workflows(self):
        """Test research-focused multi-turn conversations."""
        await AgentEvaluator.evaluate(
            agent_module="single_agent_with_tools",
            eval_dataset_file_path_or_dir="single_agent_with_tools/eval/integration_tests_evalset.json",
        )
    
    @pytest.mark.asyncio
    async def test_tool_trajectory_accuracy(self):
        """Test that tools are called in the expected sequence."""
        await AgentEvaluator.evaluate(
            agent_module="single_agent_with_tools",
            eval_dataset_file_path_or_dir="single_agent_with_tools/eval/integration_tests_evalset.json",
        )