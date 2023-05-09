import os
import json
from google.cloud import pubsub_v1

if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
    from .secrets import GOOGLE_APPLICATION_CREDENTIALS
else:
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GOOGLE_APPLICATION_CREDENTIALS

# Define publisher function
def publish_message(project_id, topic_name, message):
    """
    Publishes a message to a Pub/Sub topic.
    """
    # Initialize a Publisher client
    publisher = pubsub_v1.PublisherClient()

    # Create the fully qualified topic path
    topic_path = publisher.topic_path(project_id, topic_name)

    # Convert message to bytes
    message_bytes = message.encode('utf-8')

    # Publish the message
    response = publisher.publish(topic_path, data=message_bytes)

    print(f"Message published: {response.result()}")

# Set environment variables
project_id = os.getenv("PROJECT_ID")
topic_name = os.getenv("TOPIC_NAME")

# Define function to send message to Pub/Sub
def send_to_pubsub(user_message):
    """
    Sends a message to Pub/Sub topic.
    """
    # Convert message to JSON format
    message = json.dumps({'message': user_message})

    # Send message to Pub/Sub
    publish_message(project_id, topic_name, message)
