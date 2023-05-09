import os

PROJECT_ID = os.getenv("PROJECT_ID")
JSON_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

client = bigquery.Client()

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

LOGGING_CONFIG = "config/logging.ini"

SECRET_KEY = os.getenv("SECRET_KEY")