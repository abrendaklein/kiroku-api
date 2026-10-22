from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from sqlalchemy import text

from app import models  # noqa: F401  (needed so create_all sees the tables)
from app.database import Base, SessionLocal, engine
from app.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # runs once when the app starts
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="kiroku API", lifespan=lifespan)

app.include_router(router)


@app.get("/health")
def health_check():
    # SELECT 1 is the cheapest way to check the db is answering
    try:
        with SessionLocal() as db:
            db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Database connection failed"
        )