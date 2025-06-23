# Developer Assistant Agent Evaluation

This directory contains evaluation tests for the developer assistant agent using Google ADK's evaluation framework.

## Available Tools

The agent has 4 tools available for testing:

1. **ArXiv Search** (`langchain_tool`) - Search academic papers by topic, author, or paper ID
2. **Web Scraper** (`crewai_tool`) - Scrape content from websites, documentation, and tutorials  
3. **Reddit Search** (`mcp_reddit_tool`) - Search Reddit for developer discussions and solutions
4. **JSON Validator** (`json_tool`) - Validate and parse JSON strings

## Test Structure

### Unit Tests (`test_developer_assistant.test.json`)
- **JSON Validation**: Tests the custom JSON validator tool with developer-focused data
- **ArXiv Search**: Tests academic paper search for machine learning topics
- **Web Scraping**: Tests scraping Python tutorials and documentation
- **Reddit Search**: Tests searching for Python best practices discussions

### Integration Tests (`integration_tests.evalset.json`)
- **Research Workflow**: Multi-step research combining ArXiv → Reddit → JSON validation
- **Full Stack Research**: Complex workflow using all 4 tools in sequence

## Running Tests

### 1. Using ADK CLI (Recommended)
```bash
# Run unit tests
adk eval single_agent_with_tools single_agent_with_tools/eval/test_developer_assistant.test.json

# Run integration tests  
adk eval single_agent_with_tools single_agent_with_tools/eval/integration_tests.evalset.json

# Run with custom config
adk eval single_agent_with_tools single_agent_with_tools/eval/test_developer_assistant.test.json --config_file_path=single_agent_with_tools/eval/test_config.json

# Print detailed results
adk eval single_agent_with_tools single_agent_with_tools/eval/test_developer_assistant.test.json --print_detailed_results
```

### 2. Using Pytest
```bash
# Run all pytest tests
pytest single_agent_with_tools/eval/pytest_tests.py -v

# Run specific tool test
pytest single_agent_with_tools/eval/pytest_tests.py::test_json_validation_tool -v

# Run integration tests only
pytest single_agent_with_tools/eval/pytest_tests.py::TestDeveloperAssistant::test_research_workflows -v
```

### 3. Using Python Test Runner
```bash
python single_agent_with_tools/eval/test_runner.py
```

### 4. Using ADK Web UI
```bash
# Start web interface
adk web single_agent_with_tools

# Navigate to Eval tab to run tests interactively
```

## Evaluation Criteria

The tests use the following evaluation metrics:

- **Tool Trajectory Average Score**: 1.0 (requires 100% match in tool usage)
- **Response Match Score**: 0.7 (allows reasonable variation in natural language responses)

## Test Cases Overview

### Unit Test Cases
1. **JSON Validation**: Validates developer configuration JSON with skills array
2. **ArXiv Search**: Searches for transformer architecture papers  
3. **Web Scraping**: Scrapes Python tutorials from Real Python
4. **Reddit Search**: Finds Python best practices discussions

### Integration Test Cases
1. **Research Workflow**: Neural network research using ArXiv → Reddit → JSON validation
2. **Full Stack Research**: Web framework research using Web Scraper → ArXiv → Reddit → JSON validation

## Example Commands

```bash
# Quick unit test run
adk eval single_agent_with_tools single_agent_with_tools/eval/test_developer_assistant.test.json

# Run specific test from evalset
adk eval single_agent_with_tools single_agent_with_tools/eval/integration_tests.evalset.json:research_workflow

# Run with verbose output
adk eval single_agent_with_tools single_agent_with_tools/eval/test_developer_assistant.test.json --print_detailed_results
```

## File Structure
eval/
├── init.py # Package initialization
├── test_developer_assistant.test.json # Unit tests for 4 tools
├── integration_tests.evalset.json # Multi-tool integration tests
├── test_config.json # Evaluation criteria config
├── test_runner.py # Python async test runner
├── pytest_tests.py # Pytest-based tests
└── README.md # This documentation

## Debugging Failed Tests

Use the ADK web UI's Trace tab to debug test failures:

1. Run `adk web single_agent_with_tools`
2. Navigate to the Eval tab
3. Run the failing test case
4. Click on the Trace tab to see step-by-step execution
5. Look for tool call mismatches or response quality issues

## Adding New Tests

To add new test cases:

1. **For Unit Tests**: Add new `eval_cases` to `test_developer_assistant.test.json`
2. **For Integration Tests**: Add new `eval_cases` to `integration_tests.evalset.json`
3. **For Pytest**: Add new test functions to `pytest_tests.py`

Each test case should include:
- Unique `eval_id`
- User query in `user_content`
- Expected final response
- Expected tool usage in `intermediate_data.tool_uses`
- Proper tool names matching the actual tool implementations

## Tool Name Reference

When creating tests, use these exact tool names:
- `arxiv_search` - for ArXiv paper search
- `WebScraper` - for web scraping  
- `mcp_reddit_tool` - for Reddit search
- `json_validator` - for JSON validation