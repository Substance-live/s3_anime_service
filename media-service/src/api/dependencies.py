from fastapi import Request
from src.s3.service import AsyncS3SignedURLService

def get_s3_service(request: Request) -> AsyncS3SignedURLService:
    return request.app.state.s3_service