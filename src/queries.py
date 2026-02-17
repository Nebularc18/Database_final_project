# ============================================================================
# queries.py
# ============================================================================
"""
This module contains all SQL queries used by the application.
Each function should execute a specific query and return the results.

What to include here:
    1. SELECT queries for retrieving data
    2. INSERT queries for adding new records
    3. UPDATE queries for modifying existing records
    4. DELETE queries for removing records
    5. CALL statements for stored procedures
    6. Function calls for database functions
    7. Complex queries with JOINs, GROUP BY, HAVING, etc.
    8. Parameterized queries to prevent SQL injection

Example structure:
    from db import get_connection

    def get_all_users():
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return results

    def get_user_by_id(user_id):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result

    def create_user(username, email):
        connection = get_connection()
        cursor = connection.cursor()
        query = "INSERT INTO users (username, email) VALUES (%s, %s)"
        cursor.execute(query, (username, email))
        connection.commit()
        user_id = cursor.lastrowid
        cursor.close()
        connection.close()
        return user_id

    def call_stored_procedure(param1, param2):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.callproc('procedure_name', [param1, param2])
        results = cursor.stored_results()
        cursor.close()
        connection.close()
        return list(results)[0].fetchall()

Tips:
    - ALWAYS use parameterized queries (%s placeholders) to prevent SQL injection
    - Use dictionary=True cursor for readable column names in results
    - Close connections properly (consider using context managers)
    - Group related queries together (e.g., all user queries in one section)
    - Add docstrings explaining what each function does
    - Return meaningful data types (list of dicts, single dict, or affected row count)
"""