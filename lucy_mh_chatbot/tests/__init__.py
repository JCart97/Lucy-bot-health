import unittest
from google.cloud import bigquery
from app import app

# Create a BigQuery client for testing
client = bigquery.Client(project="your-project-id")

class TestChatHistory(unittest.TestCase):
    def test_receive_message(self):
        # Send a test message to the API
        with app.test_client() as c:
            data = {"user_id": "test_user", "message": "test_message", "topic": "test_topic"}
            response = c.post("/message", json=data)
            self.assertEqual(response.status_code, 200)

        # Check that the message was inserted into the BigQuery table
        query = f"SELECT * FROM chat_history.chat_data WHERE user_id='test_user' AND message='test_message' AND topic='test_topic'"
        result = client.query(query).result()
        self.assertTrue(len(list(result)) > 0)


if __name__ == "__main__":
    unittest.main()
