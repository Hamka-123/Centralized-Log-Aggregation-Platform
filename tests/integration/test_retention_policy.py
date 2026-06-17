import pytest
from datetime import datetime

def test_event_scheduler_configuration(db_connection):
    """
    Checks that the event scheduler is enabled and the purge event exists.
    """
    cursor = db_connection.cursor()
    
    # 1. Check if scheduler is ON
    cursor.execute("SHOW VARIABLES LIKE 'event_scheduler'")
    result = cursor.fetchone()
    assert result[1] == 'ON', "Event scheduler is OFF! Database won't run the cleanup."

    # 2. Check the event details
    cursor.execute("SHOW EVENTS LIKE 'purge_old_logs'")
    event = cursor.fetchone()
    
    # event[0] - Db, event[1] - Name, event[5] - Execution time/Schedule info
    # event[6] - Starts, event[7] - Ends (usually None), event[8] - Status
    assert event is not None, "Retention event 'purge_old_logs' not found!"
    
    # Print schedule info to console so you can see it
    print(f"\n--- Retention Policy Schedule ---")
    print(f"Event Name: {event[1]}")
    print(f"Starts at: {event[6]}") # Время первого запуска
    print(f"Status: {event[8]}")    # ENABLED или DISABLED
    print(f"---------------------------------")
    
def test_retention_procedure_execution(db_connection, test_service_id):
    """
    Verify that the stored procedure correctly deletes old logs 
    and keeps fresh ones.
    """
    cursor = db_connection.cursor()
    
    # 1. Insert an old log (31 days ago)
    cursor.execute(
        "INSERT INTO logs (service_id, level, message, created_at) "
        "VALUES (%s, %s, %s, DATE_SUB(NOW(), INTERVAL 31 DAY))",
        (test_service_id, 'INFO', 'Old log')
    )
    old_log_id = cursor.lastrowid
    
    # 2. Insert a fresh log (now)
    cursor.execute(
        "INSERT INTO logs (service_id, level, message, created_at) "
        "VALUES (%s, %s, %s, NOW())",
        (test_service_id, 'INFO', 'Fresh log')
    )
    fresh_log_id = cursor.lastrowid
    
    # 3. CALL the procedure instead of writing raw SQL
    cursor.execute("CALL sp_cleanup_logs()")
    
    # 4. Verify results
    cursor.execute("SELECT id FROM logs WHERE id = %s", (old_log_id,))
    assert cursor.fetchone() is None, "Procedure failed to delete old log!"
    
    cursor.execute("SELECT id FROM logs WHERE id = %s", (fresh_log_id,))
    assert cursor.fetchone() is not None, "Procedure incorrectly deleted fresh log!"
    
    # Cleanup
    cursor.execute("DELETE FROM logs WHERE id = %s", (fresh_log_id,))
    cursor.close()