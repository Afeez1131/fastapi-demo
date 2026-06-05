from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine
from app.routers.product import router as product_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="FastAPI Demo", lifespan=lifespan)

app.include_router(product_router)


@app.get("/health")
async def health():
    return {"status": "ok"}
