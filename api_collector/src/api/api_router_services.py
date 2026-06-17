from fastapi import APIRouter, Depends, HTTPException, status
from ..models.services import ServiceCreate
from ..db_async import get_db
from ..services.log_service import LogService
from ..repositories.log_repository import MariaDBRepository

# ServiceController
router_services = APIRouter(prefix="/api/services", tags=["ServiceController"])

def get_service(conn = Depends(get_db)):
    repo = MariaDBRepository(conn)
    return LogService(repo)

@router_services.post("/register", status_code=201)
async def register_service(
    payload: ServiceCreate, 
    service: LogService = Depends(get_service)
):
    service_id = await service.create_service(payload.service_name, payload.description)
    return {"id": service_id, "service_name": payload.service_name, "description": payload.description}


@router_services.get("/{service_id}")
async def get_service_name(
    service_id: int, 
    service: LogService = Depends(get_service)
):
    name = await service.get_service_name(service_id)
    
    if not name:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Service with id {service_id} not found"
        )
        
    return {"service_id": service_id, "service_name": name}
