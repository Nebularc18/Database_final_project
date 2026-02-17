# ============================================================================
# setup_db.py
# ============================================================================
"""
This script initializes the database by running schema.sql and seed.sql.
Use this to set up a fresh database for testing or development.

What to include here:
    1. Read and execute schema.sql (creates tables, constraints, triggers, etc.)
    2. Read and execute seed.sql (inserts test/demo data)
    3. Error handling for SQL execution failures
    4. Success/error messages to inform the user
    5. Option to run only schema or only seed (optional)

Example structure:
    import os
    from db import get_connection

    def run_sql_file(filepath):
        connection = get_connection()
        cursor = connection.cursor()
        
        with open(filepath, 'r') as f:
            sql_script = f.read()
        
        # Split and execute statements
        for statement in sql_script.split(';'):
            if statement.strip():
                cursor.execute(statement)
        
        connection.commit()
        cursor.close()
        connection.close()

    def setup_database():
        print("Running schema.sql...")
        run_sql_file('sql/schema.sql')
        print("Running seed.sql...")
        run_sql_file('sql/seed.sql')
        print("Database setup complete!")

    if __name__ == "__main__":
        setup_database()

Tips:
    - Handle multi-statement SQL files properly
    - Use transactions for atomic operations
    - Provide clear output about what's being executed
    - Consider adding a --reset flag to drop existing tables first
    - Handle DELIMITER changes in stored procedures/triggers
"""