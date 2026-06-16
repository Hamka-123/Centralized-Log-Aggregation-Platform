from contextlib import asynccontextmanager
from fastapi import FastAPI
from .api.api_router import router
from .api.api_router_services import router_services
from .database import init_db_pool, close_db_pool 

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- START: Executed once at startup---
    await init_db_pool()
    print("Database pool initialized.")
    
    yield # --- The application is working ---
    
    # --- STOP: Executed when stopped ---
    await close_db_pool()
    print("Database pool closed.")

# Pass the lifespan to the FastAPI constructor
app = FastAPI(title="Log Collector API", lifespan=lifespan)

app.include_router(router)
app.include_router(router_services)

@app.get("/health")
def health():
    return {"status": "ok"}