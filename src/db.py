import os
from pathlib import Path
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = int(os.getenv('DB_PORT', 3306))
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', 'final_project')

def get_connection(database: str = None):
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=database or DB_NAME,
            autocommit=False
        )
        return connection
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

def get_connection_no_db():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            autocommit=False
        )
        return connection
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

def test_connection():
    connection = get_connection()
    if connection and connection.is_connected():
        print(f"Connected to database: {DB_NAME}")
        connection.close()
        return True
    return False
