from pydantic import BaseModel

class LogModel(BaseModel):
    message: str
    level: str
    service_id: int