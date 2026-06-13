from fastapi import FastAPI
from src.api.api_router import router

app = FastAPI(title="Log Aggregator API")

app.include_router(router)