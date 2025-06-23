# Building Your First Agent: A Hands-On Workshop

This repository contains the code and resources for the "Building Your First Agent: Hands-On with the Agent Development Kit" talk (Level: 300, Advanced).

This session is your practical guide to bringing your agent ideas to life\! Dive into building your very own intelligent agent. Get a deep dive into the Agent Development Kit (ADK) and see its core components in action. Join our step-by-step hands-on lab and create a simple yet powerful research assistant.

In this workshop, you will:

  * Learn how to evaluate your agents effectively, ensuring you choose the right agent for your specific use case.
  * Master the process of testing, debugging, and refining your agents to achieve optimal performance.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

  * Python 3.12 or higher

## Project Setup

You can set up the project using one of the two methods detailed below. Both will install the necessary dependencies to run the agent and its tests.

### Method 1: Using `pyproject.toml` (Recommended)

This approach uses the `pyproject.toml` file to install the project dependencies. This is the modern and recommended way to manage Python projects.

1.  **Clone the repository:**

    ```bash
    git clone <your-repository-url>
    cd <your-repository-name>
    ```

2.  **Create and activate a virtual environment:**

      * **On macOS and Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
      * **On Windows:**
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

3.  **Install the project and its dependencies:**

    ```bash
    pip install .
    ```

    This command reads the `pyproject.toml` file and installs all the packages listed under `[project.dependencies]`.

### Method 2: Using `requirements.txt`

This method uses a `requirements.txt` file, which is a common way to specify a list of Python packages to be installed.

1.  **Clone the repository:**

    ```bash
    git clone <your-repository-url>
    cd <your-repository-name>
    ```

2.  **Create and activate a virtual environment:**

      * **On macOS and Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
      * **On Windows:**
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

3.  **Install the dependencies using `requirements.txt`:**

    ```bash
    pip install -r requirements.txt
    ```