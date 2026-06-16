from fastapi import APIRouter, Depends, HTTPException, status
from ..models.log_model import LogModel
from ..database import get_db
from ..services.log_service import LogService
from ..repositories.log_repository import MariaDBRepository

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
        # 2. Обязательно добавляем await!
        await service.process_log(log_data)
        
        # 3. Внимание: new_log.id больше нет. 
        # Если нужно вернуть ID, его нужно передать из репозитория/сервиса.
        return {"status": "success", "message": "Log received"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=str(e)
        )