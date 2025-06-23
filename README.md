# Building Your First Agent: A Hands-On Workshop

This repository contains the code and resources for the "Building Your First Agent: Hands-On with the Agent Development Kit" talk (Level: 300, Advanced).

This session is your practical guide to bringing your agent ideas to life\! Dive into building your very own intelligent agent. Get a deep dive into the Agent Development Kit (ADK) and see its core components in action. Join our step-by-step hands-on lab and create a simple yet powerful research assistant.

In this workshop, you will:

  * Learn how to evaluate your agents effectively, ensuring you choose the right agent for your specific use case.
  * Master the process of testing, debugging, and refining your agents to achieve optimal performance.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

  * **Python 3.12 or higher**
  * **uv**: An extremely fast Python package installer. It is the recommended way to set up this project.
      * Install it by following the official instructions at the [Astral `uv` documentation](https://www.google.com/search?q=%5Bhttps://astral.sh/guide/uv%5D\(https://astral.sh/guide/uv\)).

## Project Setup

### Recommended Setup (using `uv`)

This method is **highly recommended** as it is significantly faster and more reliable. It uses the `uv.lock` file to install the exact versions of the packages required for this project, skipping the slow dependency resolution step.

1.  **Clone the repository:**

    ```bash
    git clone <your-repository-url>
    cd <your-repository-name>
    ```

2.  **Create and activate a virtual environment with `uv`:**

    ```bash
    # Create a virtual environment in a .venv directory
    uv venv

    # Activate the environment
    # On macOS and Linux:
    source .venv/bin/activate
    # On Windows:
    .\.venv\Scripts\activate
    ```

3.  **Install dependencies using `uv pip sync`:**
    This command reads the `uv.lock` file and installs the dependencies at maximum speed.

    ```bash
    uv pip sync uv.lock
    ```

You are now ready to go\!

\<br\>

\<details\>
\<summary\>\<b\>Alternative Setup (using pip)\</b\>\</summary\>

These methods use `pip` and do not require `uv`. They are noticeably slower than the recommended `uv` setup but will still work.

### Method A: Using `pyproject.toml`

This approach uses the `pyproject.toml` file to install the project dependencies.

1.  **Clone and enter the repository.**
2.  **Create and activate a virtual environment:**
      * On macOS/Linux: `python3 -m venv venv` and `source venv/bin/activate`
      * On Windows: `python -m venv venv` and `.\venv\Scripts\activate`
3.  **Install the project:**
    ```bash
    pip install .
    ```

### Method B: Using `requirements.txt`

This method uses a `requirements.txt` file, which avoids the local project build step.

1.  **Clone and enter the repository.**
2.  **Create and activate a virtual environment.**
3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

\</details\>

## For Developers: Managing Dependencies

If you need to add, remove, or update a package, you should not edit the `uv.lock` file directly. Instead, follow this process:

1.  **Modify `pyproject.toml`**: Add or remove your desired package from the `dependencies` list in the `pyproject.toml` file.

2.  **Re-generate the lock file**: Run the `uv pip compile` command. This will perform the slow dependency resolution step once and create an updated `uv.lock` file.

    ```bash
    uv pip compile pyproject.toml --output-file uv.lock
    ```

3.  **Commit your changes**: Add both the modified `pyproject.toml` and the newly generated `uv.lock` file to your git commit. This ensures everyone on the team can get the new dependencies by just running `uv pip sync uv.lock`.

## Configuration and Authentication

Before running the agent, you must configure your environment and authenticate with Google Cloud.

### 1\. Authenticate with gcloud

This command will open a browser window for you to log in with your Google account. This provides your local application with the credentials it needs to access Google Cloud services.

```bash
gcloud auth application-default login
```

### 2\. Create the .env File

The application uses a `.env` file to load necessary environment variables. Create a file named `.env` in the root directory of this project.

Copy and paste the following content into the `.env` file and fill in your specific values.

```env
# Your Google Cloud Project ID
GOOGLE_CLOUD_PROJECT="your-gcp-project-id"

# The location for your GCP resources
GOOGLE_CLOUD_LOCATION="us-central1"

# A Google Cloud Storage bucket for the agent to use
GOOGLE_CLOUD_BUCKET="your-gcs-bucket-name"

# Tells the GenAI libraries to use the Vertex AI backend
GOOGLE_GENAI_USE_VERTEXAI=TRUE
```

