"""
Test runner for developer assistant agent using ADK evaluation framework.
Tests the 4 available tools: ArXiv search, web scraping, Reddit search, and JSON validation.
"""
import asyncio
from google.adk.evaluation.agent_evaluator import AgentEvaluator


async def test_basic_functionality():
    """Test the agent's basic functionality via test files."""
    print("Running basic functionality tests...")
    print("Testing: ArXiv search, Web scraping, Reddit search, JSON validation")
    
    await AgentEvaluator.evaluate(
        agent_module="single_agent_with_tools",
        eval_dataset_file_path_or_dir="single_agent_with_tools/eval/test_dev_agent.test.json",
        eval_config_file_path_or_dir="single_agent_with_tools/eval/test_config.json",
    )
    print("✅ Basic functionality tests completed")


async def test_integration_scenarios():
    """Test complex integration scenarios via evalset."""
    print("Running integration tests...")
    print("Testing: Multi-tool workflows and research scenarios")
    
    await AgentEvaluator.evaluate(
        agent_module="single_agent_with_tools",
        eval_dataset_file_path_or_dir="single_agent_with_tools/eval/integration_tests_evalset.json",
    )
    print("✅ Integration tests completed")


async def run_all_tests():
    """Run all evaluation tests."""
    print("🚀 Starting Developer Assistant Agent Evaluation")
    print("Available Tools: ArXiv Search, Web Scraping, Reddit Search, JSON Validation")
    print("=" * 70)
    
    try:
        # Run basic unit tests
        await test_basic_functionality()
        
        # Run integration tests
        await test_integration_scenarios()
        
        print("=" * 70)
        print("🎉 All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(run_all_tests())