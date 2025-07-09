from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import Base, engine, AsyncSessionLocal
from app.auth.routes import router as auth_router
from app.datasets.routes import router as dataset_router
from app.file.routes import router as file_router
import app.auth.models
import app.datasets.models

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(dataset_router, prefix="/dataset", tags=["Dataset"])
app.include_router(file_router,prefix="/files",tags=["file"])



# Create tables on startup
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Dependency for DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@app.get("/")
async def root():
    return {"message": "Connected to PostgreSQL!"}

