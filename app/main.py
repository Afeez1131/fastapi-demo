from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import AsyncSessionLocal, Base, engine
from app.routers.product import router as product_router
from app.seed import run_seeds


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSessionLocal() as session:
        await run_seeds(session)
    yield


app = FastAPI(title="FastAPI Demo", lifespan=lifespan)

app.include_router(product_router)


@app.get("/health")
async def health():
    return {"status": "ok"}
