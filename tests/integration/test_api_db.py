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
    
    if response.status_code != 201:
        print(f"\nAPI Error: {response.text}")
    
    assert response.status_code == 201
    
    response = requests.get(f"http://localhost:8000/api/services/{test_service_id}")
    response_data = response.json()
    params = {
        "service_name": response_data["service_name"],
        "level": test_log["level"],
        "limit": 5
    }
    
    # 3. Assert: Check Database 
    response = requests.get("http://localhost:8000/api/logs", params=params)
    
    assert response.status_code == 200
    data = response.json()
    
    assert "status" in data
    assert data["status"] == "success"
    assert "data" in data
    assert isinstance(data["data"], list)
    
    assert len(data["data"]) > 0
    
    first_log = data["data"][0]
    assert first_log["level"] == test_log["level"]
    assert first_log["service_name"] == response_data["service_name"]