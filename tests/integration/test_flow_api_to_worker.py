import pytest
import uuid
import requests
from unittest.mock import MagicMock
from alerting_worker.src.services.alert_engine import AlertEngine
from alerting_worker.src.repositories.data_fetcher import DataFetcher
from alerting_worker.src.db_sync import get_db_connection

def test_log_flow_api_to_worker(db_connection, test_service_id):
    # 1. Prepare data (IMPORTANT: Use ERROR so worker picks it up)
    unique_msg = f"Integration test error log {uuid.uuid4()}"
    
    test_log = {
        "message": unique_msg,
        "level": "ERROR", 
        "service_id": test_service_id
    }
    
    # 2. ACT: Create log via API
    response = requests.post("http://localhost:8000/api/logs", json=test_log)
    assert response.status_code == 201
    
    # 3. ACT: Run the worker logic manually
    # Use the factory function that creates a NEW connection.
    # This prevents the DataFetcher from closing your shared test connection.
    mock_mailer = MagicMock()
    fetcher = DataFetcher(get_db_connection)
    engine = AlertEngine(fetcher, mock_mailer)
    
    engine.process_alerts()
    
    # 4. ASSERT: Check Database for Worker result
    # Now db_connection is still open because the worker used its own connection
    cursor = db_connection.cursor()
    
    # Verify that the log is marked as processed (processed = 1)
    cursor.execute("SELECT processed FROM logs WHERE message = %s", (unique_msg,))
    result = cursor.fetchone()
    assert result is not None, f"Log with message '{unique_msg}' not found in DB!"
    assert result[0] == 1, "Log should be marked as processed (1)"
    
    # Verify that a record was created in the alerts table
    cursor.execute("""
        SELECT status FROM alerts 
        WHERE log_id = (SELECT id FROM logs WHERE message = %s)
    """, (test_log["message"],))
    
    alert = cursor.fetchone()
    assert alert is not None, "Alert record should exist in DB"
    assert alert[0] == 'SENT', "Alert status should be 'SENT'"
    
    # Verify that the mailer mock was called
    mock_mailer.send.assert_called_once()
    
    cursor.close()