# app/db_operations.py
import mysql.connector
from app.config import db_config
from app.constants import UserCodes

class DatabaseConnectionError(Exception):
    def __init__(self, message, error_code=UserCodes.DATABASE_CONNECTION_ERROR):
        super().__init__(message)
        self.error_code = error_code

def get_db_connection():
    try:
        # Use context manager for database connection
        return mysql.connector.connect(**db_config)

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        # Raise a custom exception for database connection errors
        raise DatabaseConnectionError("Failed to connect to the database.", error_code=UserCodes.DATABASE_CONNECTION_ERROR)