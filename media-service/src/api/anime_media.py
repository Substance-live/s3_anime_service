import uuid
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException

from src.api.dependencies import get_s3_service
from src.api.schemas import Response1, UploadUrls, Input1
from src.file.schemas import FileCreateSchema
from src.file.service import FileService
from src.media.enum.media_status import MediaStatus
from src.media.schemas import MediaCreateSchema
from src.media.service import MediaService
from src.s3.service import AsyncS3SignedURLService

router = APIRouter(
    prefix="/api/media/anime",
    tags=["Медиа"]
)

@router.post("/init-upload")
async def init_upload_anime(files_list: Input1, s3_service: AsyncS3SignedURLService = Depends(get_s3_service)) -> Response1:
    new_uid = uuid.uuid4()
    media_model = MediaCreateSchema(
        s3_key=f"anime/{new_uid}/",
        status=MediaStatus.pending,
    )
    new_media = await MediaService.add(media_model)

    upload_urls = UploadUrls()
    for file in files_list.files:
        file_model = FileCreateSchema(
            media_id=new_media.id,
            file_name=file.file_name,
            s3_key=f"{media_model.s3_key}{file.file_name}",
            content_type=file.content_type,
            created_at=datetime.now(),
        )

        url = s3_service.generate_upload_url(
            key=file_model.s3_key,
            content_type=file_model.content_type
        )
        if file.content_type.split('/')[-2] == "image":
            upload_urls.images.append(url)
        elif file.content_type.split('/')[-2] == "video":
            upload_urls.video.append(url)
        else:
            raise TypeError("Неизвестный content_type", file.content_type)


        await FileService.add(file_model)

    return Response1(media_id=new_media.id, upload_urls=upload_urls)


@router.post("/{media_id}/confirm")
async def confirm_upload_anime(media_id: int, s3_service: AsyncS3SignedURLService = Depends(get_s3_service)):
    expected_files = [file.file_name for file in await FileService.get_files_from_media(media_id)]
    try:
        s3_path_prefix = (await MediaService.get(media_id)).s3_key
    except IndexError as e:
        return HTTPException(status_code=404, detail=e.args)

    result = await s3_service.check_upload_status(s3_path_prefix, expected_files)
    if result["complete"]:
        await MediaService.update_state(media_id, MediaStatus.uploaded)

    return result

@router.get("/{media_id}")
async def get_media_anime(media_id: int, s3_service: AsyncS3SignedURLService = Depends(get_s3_service)):
    try:
        media_status = (await MediaService.get(media_id)).status
    except IndexError as e:
        return HTTPException(status_code=404, detail=e.args)

    if media_status == MediaStatus.pending:
        return HTTPException(status_code=404, detail="Files upload doesn't confirmed")

    files_list = await FileService.get_files_from_media(media_id)
    upload_urls = UploadUrls()

    for file in files_list:

        url = s3_service.generate_download_url(file.s3_key)

        if file.content_type.split('/')[-2] == "image":
            upload_urls.images.append(url)
        elif file.content_type.split('/')[-2] == "video":
            upload_urls.video.append(url)
        else:
            raise TypeError("Неизвестный content_type")

    await MediaService.update_expire_time(media_id, datetime.now() + timedelta(seconds=s3_service.expire_time))

    return Response1(media_id=media_id, upload_urls=upload_urls)
