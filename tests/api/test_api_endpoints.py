import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
# Assuming 'app' is the FastAPI instance import
from api_collector.src.main import app 
# Import the dependency functions you want to override
from api_collector.src.api.api_router import get_log_service
from api_collector.src.api.api_router_services import get_service

# Create a mock service instance
mock_log_service = AsyncMock()

# Override dependencies
app.dependency_overrides[get_log_service] = lambda: mock_log_service
app.dependency_overrides[get_service] = lambda: mock_log_service

client = TestClient(app)

@pytest.mark.asyncio
async def test_create_log_success():
    """Test POST /api/logs returns 201 on success."""
    payload = {
        "service_id": 1,
        "level": "INFO",
        "message": "Test log"
    }
    
    response = client.post("/api/logs", json=payload)
    
    assert response.status_code == 201
    assert response.json()["status"] == "success"
    mock_log_service.process_log.assert_awaited_once()

@pytest.mark.asyncio
async def test_get_logs_success():
    """Test GET /api/logs returns list of logs."""
    mock_logs = [{"id": 1, "message": "hello"}]
    mock_log_service.get_logs.return_value = mock_logs
    
    response = client.get("/api/logs?service_name=test&limit=10")
    
    assert response.status_code == 200
    assert response.json()["data"] == mock_logs

@pytest.mark.asyncio
async def test_register_service_success():
    """Test POST /api/services/register returns 201."""
    mock_log_service.create_service.return_value = 1
    payload = {"service_name": "auth-service", "description": "Auth module"}
    
    response = client.post("/api/services/register", json=payload)
    
    assert response.status_code == 201
    assert response.json()["id"] == 1
    assert response.json()["service_name"] == "auth-service"

@pytest.mark.asyncio
async def test_get_service_name_found():
    """Test GET /api/services/{id} returns 200 when found."""
    mock_log_service.get_service_name.return_value = "auth-service"
    
    response = client.get("/api/services/1")
    
    assert response.status_code == 200
    assert response.json()["service_name"] == "auth-service"

@pytest.mark.asyncio
async def test_get_service_name_not_found():
    """Test GET /api/services/{id} returns 404 when service missing."""
    mock_log_service.get_service_name.return_value = None
    
    response = client.get("/api/services/999")
    
    assert response.status_code == 404