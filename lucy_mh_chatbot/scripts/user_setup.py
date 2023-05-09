import csv
import logging
from pathlib import Path

from .database import get_database_connection

logger = logging.getLogger(__name__)


def create_users_table():
    """
    Create the users table in the database.
    """
    create_users_table_query = '''
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            is_admin BOOLEAN NOT NULL DEFAULT FALSE
        );
    '''

    conn = get_database_connection()
    with conn.cursor() as cursor:
        cursor.execute(create_users_table_query)
    conn.commit()
    logger.info('Created users table')


def insert_user_data():
    """
    Insert user data from a CSV file into the database.
    """
    csv_path = Path(__file__).parent.parent / 'users.csv'
    with open(csv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        next(reader)  # skip header row
        data = [(row[0], row[1], row[2], row[3], row[4] == 'True') for row in reader]

    insert_user_query = '''
        INSERT INTO users (username, password, email, is_admin)
        VALUES (%s, %s, %s, %s)
    '''

    conn = get_database_connection()
    with conn.cursor() as cursor:
        cursor.executemany(insert_user_query, data)
    conn.commit()
    logger.info('Inserted user data')
