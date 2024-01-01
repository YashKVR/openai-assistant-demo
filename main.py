from dotenv import load_dotenv
import os
import time
from openai import OpenAI

# Load the .env file (optionally specify a path if it's not in the root directory)
load_dotenv()

openai_key = os.environ['OPENAI_API_KEY']
asst_id = os.environ['ASSISTANT_ID']

client = OpenAI()

# Create a thread with a message
thread = client.beta.threads.create(
    messages=[
        {
            'role': 'user',
            "content": "What's the most livable city in the world?"
            }
    ]
)

# Submit the thread to assistant (as a new run)
run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=asst_id)
print(f"Run Created: {run.id}")

# Wait for the run to complete. run is async function
while run.status != "completed":
    run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    print(f"🏃🏻‍♂️Run Status: {run.status}")
    time.sleep(1)
else:
    print("🏁Run Completed!")

# Get the latest message from the thread
message_response = client.beta.threads.messages.list(thread_id=thread.id)
messages = message_response.data

# Print the messages, the messages are received in reverse order, message at 0 index is latest message
latest_message = messages[0]
print(f"Response: {latest_message.content[0].text.value}")