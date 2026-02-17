# ============================================================================
# db.py
# ============================================================================
"""
This module handles database connection management.
It reads environment variables and provides a way to get MySQL connections.

What to include here:
    1. Import required modules (mysql.connector, dotenv, os)
    2. Load environment variables from .env file
    3. Define database configuration constants from environment variables
    4. Create a function to establish and return a database connection
    5. Optional: Connection pooling for better performance
    6. Optional: Context manager for automatic connection cleanup

Example structure:
    import os
    from dotenv import load_dotenv
    import mysql.connector
    from mysql.connector import Error

    load_dotenv()

    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')

    def get_connection():
        try:
            connection = mysql.connector.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            return connection
        except Error as e:
            print(f"Error connecting to database: {e}")
            return None

Tips:
    - Never hardcode credentials in this file
    - Always read from environment variables
    - Handle connection errors gracefully
    - Consider using connection pooling for production apps
    - Return None or raise exception on connection failure
"""