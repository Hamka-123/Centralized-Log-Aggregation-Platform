import pytest
from unittest.mock import AsyncMock
from api_collector.src.services.log_service import LogService
from api_collector.src.repositories.interfaces import IRepository
from api_collector.src.models.log_model import LogModel

# Test suite for LogService
@pytest.mark.asyncio
async def test_save_log_success():
    """
    Scenario: Successfully saving a log entry.
    Ensure that the service correctly delegates the call to the repository.
    """
    # Mock the repository dependency
    mock_repo = AsyncMock(spec=IRepository)
    service = LogService(repository=mock_repo)
    
    # Test payload
    test_log = LogModel(
        service_id=1,
        level="INFO",
        message="System heartbeat"
    )
    
    # Execution
    await service.process_log(test_log)
    
    # Verification
    mock_repo.save.assert_called_once_with(test_log.model_dump())

@pytest.mark.asyncio
async def test_save_log_repository_failure():
    """
    Scenario: The database/repository raises an exception.
    The service should propagate the error (or handle it, depending on implementation).
    Here we verify that the service attempts to call the repository and fails as expected.
    """
    mock_repo = AsyncMock(spec=IRepository)
    # Simulate a database connection error
    mock_repo.save.side_effect = Exception("Database connection failed")
    
    service = LogService(repository=mock_repo)
    test_log = LogModel(
        service_id=1,
        level="ERROR",
        message="Critical failure"
    )
    
    # Verify that the exception propagates
    with pytest.raises(Exception, match="Database connection failed"):
        await service.process_log(test_log)