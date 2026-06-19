import time
import requests
import os
import socket

# Service knows its own 'type' (e.g., 'auth', 'collector')
SERVICE_TYPE = os.getenv("SERVICE_TYPE", "unknown-service")
# Retrieve replica index provided by Docker Compose (e.g., 1, 2, 3...)
# Defaults to 1 if not running in a scaled environment
REPLICA_INDEX = os.getenv("REPLICA_INDEX", "1")
HOSTNAME = socket.gethostname() 

API_BASE_URL = "http://api_collector:8000"

def register_service():
    """Register self with a unique name including a counter/index."""
    url = f"{API_BASE_URL}/api/services/register"
    
    # Constructing the unique name: auth-1-hostname
    service_full_name = f"{SERVICE_TYPE}-{REPLICA_INDEX}-{HOSTNAME}"
    
    payload = {
        "service_name": service_full_name,
        "description": f"Auto-registered microservice instance {REPLICA_INDEX}"
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 201:
            # The DB returns the unique ID that this service will use from now on
            return response.json().get("id")
    except requests.exceptions.RequestException as e:
        print(f"Registration request failed: {e}")
        
    return None

def send_logs():
    """Continuously send logs to the API collector."""
    url = f"{API_BASE_URL}/api/logs"
    # Service ID is expected as an integer per OpenAPI specification
    service_id = 1 
    
    while True:
        try:
            data = {
                "service_id": service_id,
                "message": "Load test log entry",
                "level": "ERROR"
            }
            requests.post(url, json=data)
        except Exception as e:
            print(f"Log send error: {e}")
        # Send 10 logs per second
        time.sleep(0.1) 

if __name__ == "__main__":
    # Wait for the API to become available before starting
    max_retries = 5
    for i in range(max_retries):
        if register_service():
            send_logs()
            break
        print(f"Retrying registration in 5 seconds... ({i+1}/{max_retries})")
        time.sleep(5)