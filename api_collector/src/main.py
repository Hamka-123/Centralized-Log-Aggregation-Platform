import logging
from common.logging_setup import setup_logging

from contextlib import asynccontextmanager
from fastapi import FastAPI

from .api.api_router import router
from .api.api_router_services import router_services
from .db_async import init_db_pool, close_db_pool 


# Initialize centralized logging for the API service
setup_logging("api")
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- START: Executed once at startup---
    await init_db_pool()
    logger.info("Database pool initialized.")
    
    yield # --- The application is working ---
    
    # --- STOP: Executed when stopped ---
    await close_db_pool()
    logger.info("Database pool closed.")

# Pass the lifespan to the FastAPI constructor
app = FastAPI(title="Log Collector API", lifespan=lifespan)

app.include_router(router)
app.include_router(router_services)

@app.get("/health")
def health():
    return {"status": "ok"}