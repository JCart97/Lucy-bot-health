from google.cloud import bigquery

# set up environment variables
PROJECT_ID = os.getenv("PROJECT_ID")
JSON_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

#create BigQuery client object
client = bigquery.Client(project=PROJECT_ID, credentials=JSON_PATH)

#Define BigQuery Table Name

TABLE_NAME = "chat_history"

def insert_chat(chat_history):
    #Define BigQuery dataset name
    dataset_ref = client.dataset("chatbot_dataset")

    #Get BigQuery table object
    table_ref = dataset_ref.table(TABLE_NAME)
    table = client.get_table(table_ref)

    #Insert new row into BigQuery
    insert_row = [(chat_history['user'], chat_history['bot'], chat_history['timestamp'])]

    if errors:
        raise ValueError(errors)