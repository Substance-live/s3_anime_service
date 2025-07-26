from fastapi import APIRouter

from .anime_media import router as media_router

main_router = APIRouter()
main_router.include_router(media_router)
