import pymysql

# Настройки подключения (укажи свои данные)
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
        
        # Используем контекстный менеджер для курсора
        with conn.cursor() as cursor:
            # 1. Пробуем вставить данные
            sql_insert = "INSERT INTO logs (message, level, service_id) VALUES (%s, %s, %s)"
            cursor.execute(sql_insert, ("DEBUG_TEST", "DEBUG", 1))
            
            # Подтверждаем транзакцию
            conn.commit()
            print("DEBUG: Insert successful!")
            
            # 2. Пробуем прочитать
            sql_select = "SELECT * FROM logs WHERE message = %s"
            cursor.execute(sql_select, ("DEBUG_TEST",))
            result = cursor.fetchone()
            
            print(f"DEBUG: Found record: {result}")
            
    except Exception as e:
        print(f"DEBUG: ERROR occurred: {e}")
        # Если была ошибка, пробуем откатить транзакцию (если соединение живо)
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()
            print("DEBUG: Connection closed.")

if __name__ == "__main__":
    check_db_connection()