from fastapi import APIRouter, Depends, HTTPException, status
from ..models.log_model import LogModel
from ..database import get_db
from ..services.log_service import LogService
from ..repositories.log_repository import MariaDBRepository

router_services = APIRouter(prefix="/api", tags=["TestController"])

def get_log_service(conn = Depends(get_db)):
    repo = MariaDBRepository(conn)
    return LogService(repo)


@router_services.get("/services/{service_id}")
async def get_service_name(
    service_id: int, 
    service: LogService = Depends(get_log_service)
):
    name = await service.get_service_name(service_id)
    
    if not name:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Service with id {service_id} not found"
        )
        
    return {"service_id": service_id, "service_name": name}