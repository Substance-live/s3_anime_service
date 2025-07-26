from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.api import main_router
from src.config import settings
from src.db import create_tables, delete_tables
from src.s3.service import AsyncS3SignedURLService


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.s3_service = AsyncS3SignedURLService(
        access_key=settings.S3_ACCESS_KEY,
        secret_key=settings.S3_SECRET_KEY,
        endpoint_url=settings.S3_ENDPOINT_URL,
        bucket_name=settings.S3_BUCKET_NAME,
    )

    await create_tables()
    yield
    await delete_tables()

app = FastAPI(lifespan=lifespan)

app.include_router(main_router)



@app.get("/root")
def root():
    return "root"

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000)