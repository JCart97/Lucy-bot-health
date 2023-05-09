import re
import logging
import random

from . import mental_health_disorders
from .pubsub.publisher import publish_message
from .pubsub.subscriber import listen_for_messages

logger = logging.getLogger(__name__)

greeting_keywords = ['hi', 'hello', 'hey', 'greetings', 'sup', 'what\'s up']
farewell_keywords = ['bye', 'goodbye', 'see you', 'see ya']
fallback_responses = ['Sorry, I didn\'t understand that.', 'Can you rephrase that?', 'I\'m not sure what you mean.']

disorder_keywords = []
for disorder in mental_health_disorders.disorders:
    disorder_keywords.extend(disorder['keywords'])

def check_for_greeting(text):
    """
    Check if the user's message contains a greeting keyword.

    Args:
        text (str): The user's message.

    Returns:
        bool: True if the message contains a greeting keyword, False otherwise.
    """
    for word in text.split():
        if word.lower() in greeting_keywords:
            return True
    return False

def check_for_farewell(text):
    """
    Check if the user's message contains a farewell keyword.

    Args:
        text (str): The user's message.

    Returns:
        bool: True if the message contains a farewell keyword, False otherwise.
    """
    for word in text.split():
        if word.lower() in farewell_keywords:
            return True
    return False

def get_disorder_from_message(text):
    """
    Find the mental health disorder that matches the user's message.

    Args:
        text (str): The user's message.

    Returns:
        dict: The mental health disorder that matches the message, or None if no match is found.
    """
    for disorder in mental_health_disorders.disorders:
        for keyword in disorder['keywords']:
            if re.search(fr'\b{keyword}\b', text, flags=re.IGNORECASE):
                return disorder
    return None

def generate_response(text):
    """
    Generate a response based on the user's message.

    Args:
        text (str): The user's message.

    Returns:
        str: The chatbot's response.
    """
    if check_for_greeting(text):
        return random.choice(['Hello!', 'Hi there!', 'Hey!'])

    if check_for_farewell(text):
        return random.choice(['Goodbye!', 'See you later!', 'Take care!'])

    disorder = get_disorder_from_message(text)
    if disorder:
        publish_message(text, 'chatbot-commands')
        response = f'You may be experiencing {disorder["name"]}. Please seek professional help.'
        return response

    return random.choice(fallback_responses)

def chat():
    """
    Start the chatbot.
    """
    logger.info('Chatbot started')
    listen_for_messages('user-messages', generate_response)
