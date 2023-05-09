from flask import Flask, jsonify, request
from google.cloud import bigquery

app = Flask(__name__)

# Create a BigQuery client
client = bigquery.Client()

# Define BigQuery dataset and table names
dataset_name = "chat_history"
table_name = "chat_data"

# Define the schema for the BigQuery table
schema = [
    bigquery.SchemaField("user_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("timestamp", "TIMESTAMP", mode="REQUIRED"),
    bigquery.SchemaField("message", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("topic", "STRING", mode="REQUIRED"),
]

# Create the BigQuery dataset if it does not exist
try:
    client.get_dataset(dataset_name)
except Exception:
    dataset_ref = client.create_dataset(dataset_name)

# Create the BigQuery table if it does not exist
try:
    client.get_table(f"{dataset_name}.{table_name}")
except Exception:
    table_ref = bigquery.Table(f"{dataset_name}.{table_name}", schema=schema)
    table = client.create_table(table_ref)

# Define an API endpoint to receive messages from users
@app.route("/message", methods=["POST"])
def receive_message():
    # Get the message data from the request body
    data = request.json
    user_id = data.get("user_id")
    message = data.get("message")
    topic = data.get("topic")

    # Insert the message data into the BigQuery table
    row = {"user_id": user_id, "message": message, "topic": topic}
    errors = client.insert_rows_json(table, [row])
    if errors:
        return jsonify({"success": False}), 500

    return jsonify({"success": True})


if __name__ == "__main__":
    app.run()
