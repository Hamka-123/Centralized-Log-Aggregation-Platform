import pytest
import pymysql 
import os
import requests

def test_log_flow_api_to_db(db_connection, test_service_id):
    # 1. Prepare data
    test_log = {
        "message": "Integration test log",
        "level": "INFO",
        "service_id": test_service_id
    }
    
    # 2. Act
    response = requests.post("http://localhost:8000/api/logs", json=test_log)
    
    # DEBUG: Если 500, то выведет ошибку в консоль
    if response.status_code != 201:
        print(f"\nAPI Error: {response.text}")
    
    assert response.status_code == 201
    
    # 3. Assert: Check Database 
    # Use DictCursor so the result is returned as a dictionary with column names as keys
    with db_connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT message, level, service_id FROM logs WHERE message = %s", (test_log["message"],))
        result = cursor.fetchone()
    
    assert result is not None, "Log record not found in the database"
    assert result["message"] == test_log["message"]
    assert result["level"] == test_log["level"]
    assert result["service_id"] == test_log["service_id"]