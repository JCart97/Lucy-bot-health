import os

from .db_setup import create_tables
from .user_setup import create_users

# Create tables in the database
create_tables()

# Create users in the database
create_users()
