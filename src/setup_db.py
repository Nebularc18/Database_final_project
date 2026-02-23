import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from db import get_connection_no_db, DB_NAME

def split_sql_statements(sql_content: str) -> list:
    statements = []
    current_statement = []
    in_delimiter_block = False
    custom_delimiter = ';'
    
    lines = sql_content.split('\n')
    
    for line in lines:
        stripped = line.strip()
        
        delimiter_match = re.match(r'DELIMITER\s+(\S+)', stripped, re.IGNORECASE)
        if delimiter_match:
            if current_statement and ''.join(current_statement).strip():
                statements.append(''.join(current_statement).strip())
                current_statement = []
            custom_delimiter = delimiter_match.group(1)
            in_delimiter_block = (custom_delimiter != ';')
            continue
        
        if in_delimiter_block:
            if custom_delimiter in stripped:
                parts = line.split(custom_delimiter)
                current_statement.append(parts[0])
                if ''.join(current_statement).strip():
                    statements.append(''.join(current_statement).strip())
                current_statement = []
                if len(parts) > 1 and parts[1].strip():
                    current_statement.append(parts[1])
            else:
                current_statement.append(line + '\n')
        else:
            if ';' in stripped:
                semi_idx = line.find(';')
                current_statement.append(line[:semi_idx + 1])
                if ''.join(current_statement).strip():
                    statements.append(''.join(current_statement).strip())
                current_statement = []
                if semi_idx + 1 < len(line) and line[semi_idx + 1:].strip():
                    current_statement.append(line[semi_idx + 1:])
            else:
                current_statement.append(line + '\n')
    
    if current_statement:
        stmt = ''.join(current_statement).strip()
        if stmt:
            statements.append(stmt)
    
    return statements

def run_sql_file(filepath: str, connection):
    cursor = connection.cursor()
    
    with open(filepath, 'r', encoding='utf-8') as f:
        sql_script = f.read()
    
    statements = split_sql_statements(sql_script)
    
    for statement in statements:
        if statement.strip():
            try:
                cursor.execute(statement)
                while cursor.nextset():
                    pass
            except Exception as e:
                print(f"Error executing statement: {e}")
                print(f"Statement: {statement[:100]}...")
                raise
    
    connection.commit()
    cursor.close()

def setup_database():
    print("Setting up database...")
    
    connection = get_connection_no_db()
    if not connection:
        print("Failed to connect to MySQL server")
        return False
    
    try:
        schema_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sql', 'schema.sql')
        seed_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sql', 'seed.sql')
        
        print("Running schema.sql...")
        run_sql_file(schema_path, connection)
        print("Schema created successfully!")
        
        print("Running seed.sql...")
        run_sql_file(seed_path, connection)
        print("Seed data inserted successfully!")
        
        print(f"\nDatabase '{DB_NAME}' setup complete!")
        return True
        
    except Exception as e:
        print(f"Error setting up database: {e}")
        connection.rollback()
        return False
    finally:
        if connection and connection.is_connected():
            connection.close()

if __name__ == "__main__":
    setup_database()
