import pymysql

# Connection settings
db_config = {
    "host": "localhost",
    "port": 3306,
    "user": "app",
    "password": "qwerty123",
    "database": "logs_aggregation"
}

def check_db_connection():
    conn = None
    try:
        print("DEBUG: Connecting to MySQL...")
        conn = pymysql.connect(**db_config)
        
        # Using the context manager for the cursor
        with conn.cursor() as cursor:
            # 1. Try to insert data
            sql_insert = "INSERT INTO logs (message, level, service_id) VALUES (%s, %s, %s)"
            cursor.execute(sql_insert, ("DEBUG_TEST", "DEBUG", 1))
            
            # Confirming the transaction
            conn.commit()
            print("DEBUG: Insert successful!")
            
            # 2. Let's try to read
            sql_select = "SELECT * FROM logs WHERE message = %s"
            cursor.execute(sql_select, ("DEBUG_TEST",))
            result = cursor.fetchone()
            
            print(f"DEBUG: Found record: {result}")
            
    except Exception as e:
        print(f"DEBUG: ERROR occurred: {e}")
        # If there was an error, we try to roll back the transaction (if the connection is alive)
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()
            print("DEBUG: Connection closed.")

if __name__ == "__main__":
    check_db_connection()