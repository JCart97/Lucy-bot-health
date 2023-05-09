from google.cloud import pubsub_v1
import os

PROJECT_ID = os.getenv("PROJECT_ID")
TOPIC_ID = os.getenv("TOPIC_ID")

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

def publish_message(message):
    future = publisher.publish(topic_path, message.encode('utf-8'))
    future.result()
