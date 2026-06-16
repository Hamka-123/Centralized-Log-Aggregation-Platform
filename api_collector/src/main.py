from contextlib import asynccontextmanager
from fastapi import FastAPI
from .api.api_router import router
from .database import init_db_pool, close_db_pool 

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- СТАРТ: Выполняется один раз при запуске ---
    await init_db_pool()
    print("Database pool initialized.")
    
    yield # --- Приложение работает ---
    
    # --- СТОП: Выполняется при остановке ---
    await close_db_pool()
    print("Database pool closed.")

# Передаем lifespan в конструктор FastAPI
app = FastAPI(title="Log Collector API", lifespan=lifespan)

app.include_router(router)

@app.get("/health")
def health():
    return {"status": "ok"}