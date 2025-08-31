import os
import functools
from typing import Any

import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path='../.env')

# Database connection details from environment variables
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = "postgresdb"  # This is the service name in docker-compose
DB_PORT = "5432"


def db_connector(func):
    """
    Decorator to handle database connection and cursor management.
    It opens a connection, creates a cursor, passes it to the decorated function,
    commits the transaction, and closes the connection.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            # Establish the connection
            conn = psycopg2.connect(
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT
            )
            # Create a cursor and pass it to the function
            with conn.cursor() as cur:
                result = func(cur, *args, **kwargs)
                conn.commit()
                return result
        finally:
            # Ensure the connection is closed
            if conn:
                conn.close()
    return wrapper


def handle_errors(func):
    """
    Decorator to catch exceptions during function execution and return a
    standardized JSON error response.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            # Attempt to execute the function
            return func(*args, **kwargs)
        except Exception as e:
            # Return a dictionary with error information
            return {
                "status": "failure",
                "error_type": type(e).__name__,
                "error_message": str(e)
            }
    return wrapper


def parse_output(cursor, one=False):
    """
    Parses the output of a psycopg2 cursor into a dictionary or a list of dictionaries.

    Args:
        cursor: The psycopg2 cursor after a fetch operation.
        one (bool): If True, returns a single dictionary, otherwise a list.

    Returns:
        A dictionary or a list of dictionaries representing the query result.
    """
    # Get column names from the cursor description
    desc = cursor.description
    if not desc:
        return {} if one else []

    # Create a list of column names
    column_names = [col[0] for col in desc]

    if one:
        # Fetch one record and convert it to a dictionary
        record = cursor.fetchone()
        return dict(zip(column_names, record)) if record else {}
    else:
        # Fetch all records and convert them to a list of dictionaries
        return [dict(zip(column_names, row)) for row in cursor.fetchall()]