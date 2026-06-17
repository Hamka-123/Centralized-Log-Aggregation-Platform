import time
import pytest

def test_containers_are_running(docker_client):
    """Wait for containers to be ready and verify they become healthy."""
    target_containers = ["centralized_log_db", "centralized_log_api", "centralized_log_worker"]
    max_retries = 40  # Increased to 40 seconds to account for start_period
    
    for i in range(max_retries):
        containers = docker_client.containers.list()
        container_names = [c.name for c in containers]
        
        # Check if all containers are running
        all_running = all(name in container_names for name in target_containers)
        
        if all_running:
            all_healthy = True
            for name in target_containers:
                container = docker_client.containers.get(name)
                health = container.attrs.get("State", {}).get("Health", {}).get("Status")
                
                # If healthcheck exists but is not 'healthy', we aren't ready yet
                if health and health != "healthy":
                    all_healthy = False
                    break
            
            if all_healthy:
                return # Success!

        time.sleep(1) 

    pytest.fail("Containers failed to reach 'healthy' state within timeout (40s)")

def test_api_health_endpoint():
    """Verify the API responds with 200 OK."""
    import requests
    # Add a small delay to allow the API to start the web server
    time.sleep(2)
    response = requests.get("http://localhost:8000/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}