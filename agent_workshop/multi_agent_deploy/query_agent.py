import os
from dotenv import load_dotenv
import vertexai
from vertexai import agent_engines

# Load environment variables and initialize Vertex AI
load_dotenv()

# Initialize Vertex AI with the correct project and location
vertexai.init(
    project=os.getenv("GOOGLE_CLOUD_PROJECT"),
    location=os.getenv("GOOGLE_CLOUD_LOCATION"),
    staging_bucket=os.getenv("GOOGLE_CLOUD_BUCKET"),
)

print("Connecting to deployed agent...")

# Filter agent engines by the app name
ae_apps = agent_engines.list(filter='display_name="my_agent"')
remote_app = next(ae_apps)

print(f"Connected to: {remote_app.display_name}")

# Get a session for the remote app
remote_session = remote_app.create_session(user_id="u_0")
print(f"Session created: {remote_session['id']}")

# Example messages to test different capabilities
test_messages = [
    "Hello, are you there?",
    "Search for recent papers about machine learning agents on ArXiv"
]

for i, user_message in enumerate(test_messages, 1):
    print(f"\n--- Test {i} ---")
    print(f"[user message] {user_message}")
    
    # Run the agent with this input
    events = remote_app.stream_query(
        user_id="u_0",
        session_id=remote_session["id"],
        message=user_message,
    )
    
    print("[remote response]")
    # Print responses
    for event in events:
        for part in event["content"]["parts"]:
            if "text" in part:
                response_text = part["text"]
                print(response_text)
    
    print("-" * 50)