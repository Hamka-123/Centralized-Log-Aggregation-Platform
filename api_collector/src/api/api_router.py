from fastapi import APIRouter, Depends, HTTPException, status
from ..models.log_model import LogModel
from ..db_async import get_db
from ..services.log_service import LogService
from ..repositories.log_repository import MariaDBRepository

# Class LogController
# NOTE: We use a functional approach with APIRouter and dependency injection 
# instead of class-based controllers to follow FastAPI idiomatic patterns, 
# keep services decoupled, and ensure optimal framework performance.
router = APIRouter(prefix="/api", tags=["LogController"])

def get_log_service(conn = Depends(get_db)):
    repo = MariaDBRepository(conn)
    return LogService(repo)

@router.post("/logs", status_code=status.HTTP_201_CREATED)
async def create_log(
    log_data: LogModel, 
    service: LogService = Depends(get_log_service)
):
    try:
        # 2. Be sure to add await!
        await service.process_log(log_data)
        return {"status": "success", "message": "Log received"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=str(e)
        )
        
@router.get("/logs")
async def get_logs(
    service_name: str = None,
    level: str = None,
    limit: int = 100,
    service: LogService = Depends(get_log_service)
):
    try:
        logs = await service.get_logs(service_name, level, limit)
        return {"status": "success", "data": logs}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=str(e)
        )
