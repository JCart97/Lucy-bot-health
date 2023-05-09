import os
import time
import json
from google.cloud import pubsub_v1

# Set up pubsub client
subscriber_client = pubsub_v1.SubscriberClient()

# Get topic name from environment variable
topic_name = os.getenv('TOPIC_NAME')

# Define callback function to handle incoming messages
def callback(message):
    message_data = json.loads(message.data.decode('utf-8'))
    print(f'Received message: {message_data}')
    message.ack()

# Create subscription to listen for messages
def subscribe(subscription_id):
    subscription_path = subscriber_client.subscription_path(
        os.getenv('PROJECT_ID'), subscription_id)
    subscriber_client.subscribe(subscription_path, callback=callback)

    print(f'Starting subscriber {subscription_id}...')
    while True:
        time.sleep(60)
