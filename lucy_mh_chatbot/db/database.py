from google.cloud import bigquery

# Replace the following with your project ID
project_id = 'your-project-id'

# Replace the following with the name of your BigQuery dataset
dataset_name = 'your-dataset-name'

# Replace the following with the name of your BigQuery table for user information
users_table_name = 'users'

# Replace the following with the name of your BigQuery table for mental health disorder information
mental_health_disorders_table_name = 'mental_health_disorders'

def get_database_connection():
    client = bigquery.Client(project=project_id)
    return client

def create_user(username, password, is_admin=False):
    client = get_database_connection()
    table_ref = client.dataset(dataset_name).table(users_table_name)
    table = client.get_table(table_ref)
    row = {"username": username, "password": password, "is_admin": is_admin}
    errors = client.insert_rows(table, [row])
    if errors:
        raise Exception("Error inserting row into users table")

def get_user_by_username(username):
    client = get_database_connection()
    query = f"""
        SELECT * FROM `{project_id}.{dataset_name}.{users_table_name}`
        WHERE username = @username
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("username", "STRING", username)
        ]
    )
    query_job = client.query(query, job_config=job_config)
    results = query_job.result()
    return [dict(row) for row in results]

def create_mental_health_disorder(name, description):
    client = get_database_connection()
    table_ref = client.dataset(dataset_name).table(mental_health_disorders_table_name)
    table = client.get_table(table_ref)
    row = {"name": name, "description": description}
    errors = client.insert_rows(table, [row])
    if errors:
        raise Exception("Error inserting row into mental_health_disorders table")

def get_mental_health_disorder_by_name(name):
    client = get_database_connection()
    query = f"""
        SELECT * FROM `{project_id}.{dataset_name}.{mental_health_disorders_table_name}`
        WHERE name = @name
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("name", "STRING", name)
        ]
    )
    query_job = client.query(query, job_config=job_config)
    results = query_job.result()
    return [dict(row) for row in results]
