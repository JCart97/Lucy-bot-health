import psycopg2
import logging.config
from config import DATABASE_CONFIG

# Load logging configuration
logging.config.fileConfig('logging.ini')
logger = logging.getLogger('db_setup')

def create_database():
    """
    Create database and tables
    """
    logger.info("Creating database and tables...")

    # Connect to default database
    conn = psycopg2.connect(
        dbname='postgres',
        user=DATABASE_CONFIG['user'],
        password=DATABASE_CONFIG['password'],
        host=DATABASE_CONFIG['host'],
        port=5432
    )

    # Create database
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE {DATABASE_CONFIG['dbname']};")
    cursor.close()
    conn.close()

    # Connect to database and create tables
    conn = psycopg2.connect(
        dbname=DATABASE_CONFIG['dbname'],
        user=DATABASE_CONFIG['user'],
        password=DATABASE_CONFIG['password'],
        host=DATABASE_CONFIG['host'],
        port=5432
    )

    conn.autocommit = True
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(100) NOT NULL,
            created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
    ''')

    # Create mental_health_disorders table
    cursor.execute('''
        CREATE TABLE mental_health_disorders (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) UNIQUE NOT NULL,
            description VARCHAR(500) NOT NULL
        );
    ''')

    # Create chat_history table
    cursor.execute('''
        CREATE TABLE chat_history (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            message TEXT NOT NULL,
            created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
    ''')

    cursor.close()
    conn.close()

    logger.info("Database and tables created successfully!")


if __name__ == '__main__':
    create_database()
