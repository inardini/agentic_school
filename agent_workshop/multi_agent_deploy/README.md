# Lesson 3: Building a Multi-Agent System

## Purpose of this Lesson

This lesson introduces the concept of **multi-agent systems**. Instead of a single, monolithic agent, you can create a team of specialized agents that collaborate to solve complex problems. This approach promotes modularity, reusability, and can lead to more robust and capable AI systems.

This example features a "developer assistant" that acts as a coordinator, delegating tasks to two specialized sub-agents: a `search_agent` and a `code_agent`.

## How to Deploy and Run this Agent

### 1. Prerequisites

- You have a Google Cloud project with the Vertex AI API enabled.
- You have a Google Cloud Storage bucket.
- You have Python 3.12 or later installed.
- You have authenticated your local environment with Google Cloud using `gcloud auth application-default login`.

### 2. Setup your Environment

- **Create a virtual environment:**
  ```bash
  python3 -m venv .venv
  ```
- **Activate the virtual environment:**
  ```bash
  source .venv/bin/activate
  ```
- **Install the required packages:**
  ```bash
  pip install "google-cloud-aiplatform[adk,agent_engines]" langchain-community arxiv python-dotenv
  ```
- **Set environment variables:**
  Create a `.env` file in this directory with the following content:
  ```
  GOOGLE_CLOUD_PROJECT="your-project-id"
  GOOGLE_CLOUD_LOCATION="your-location"
  GOOGLE_CLOUD_BUCKET="your-bucket-name"
  ```
  Replace the placeholder values with your actual project ID, location, and bucket name.

### 3. Deploy the Agent

- **Run the deployment script:**
  ```bash
  python deploy.py
  ```
- **Copy the resource name:**
  The script will output the resource name of the deployed agent. It will look something like this:
  `projects/your-project-number/locations/your-location/reasoningEngines/your-reasoning-engine-id`
  Copy this resource name for the next step.

### 4. Test the Agent

- **Update the query script:**
  Open the `query_agent.py` file and replace the placeholder resource name in the following line with the resource name you copied in the previous step:
  ```python
  agent_engine = agent_engines.get("projects/your-project-number/locations/your-location/reasoningEngines/your-reasoning-engine-id")
  ```
- **Run the query script:**
  ```bash
  python query_agent.py
  ```
  The script will run the queries defined in the `queries` list and print the agent's responses.
