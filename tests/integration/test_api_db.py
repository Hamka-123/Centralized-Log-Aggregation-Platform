import pytest
import requests
from sqlalchemy import text

def test_log_flow_api_to_db(db_session):
    """
    Integration Test:
    1. Send a POST request to API.
    2. Query Database to verify data was saved.
    """
    # 1. Prepare data
    test_log = {
        "message": "Integration test log",
        "level": "INFO"
    }
    
    # 2. Act: Send request to API
    response = requests.post("http://localhost:8000/logs", json=test_log)
    assert response.status_code == 201 # Or 200, depending on your API
    
    # 3. Assert: Check Database using the db_session fixture
    # Adjust the table name to your actual table name
    query = text("SELECT message, level FROM logs WHERE message = :msg")
    result = db_session.execute(query, {"msg": test_log["message"]}).fetchone()
    
    assert result is not None
    assert result[0] == test_log["message"]
    assert result[1] == test_log["level"]