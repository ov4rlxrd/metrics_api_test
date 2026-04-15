from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.routers.metrics import metrics_router
from app.database import engine



app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

    await engine.dispose()


app = FastAPI(lifespan=lifespan)


app.include_router(metrics_router)