import asyncio
import datetime

from src.file.schemas import FileCreateSchema
from src.file.service import FileService
from src.media.enum.media_status import MediaStatus
from src.media.schemas import MediaCreateSchema
from src.media.service import MediaService

media_list = [
    MediaCreateSchema(s3_key="anime/Naruto/", status=MediaStatus.uploaded),
    MediaCreateSchema(s3_key="anime/Onepiece/", status=MediaStatus.uploaded),
    MediaCreateSchema(s3_key="anime/Death note/", status=MediaStatus.uploaded),
    MediaCreateSchema(s3_key="anime/Demon slayer final/", status=MediaStatus.uploaded),
]

files_list = [
    FileCreateSchema(media_id=1, file_name="logo1.jpg", s3_key="anime/Naruto/logo1.jpg", content_type="image/jpeg", created_at=datetime.datetime.now()),
    FileCreateSchema(media_id=1, file_name="image1.jpg", s3_key="anime/Naruto/image1.jpg", content_type="image/jpeg", created_at=datetime.datetime.now()),
    FileCreateSchema(media_id=1, file_name="image2.jpg", s3_key="anime/Naruto/image2.jpg", content_type="image/jpeg", created_at=datetime.datetime.now()),
    FileCreateSchema(media_id=1, file_name="image3.jpg", s3_key="anime/Naruto/image3.jpg", content_type="image/jpeg", created_at=datetime.datetime.now()),
    FileCreateSchema(media_id=1, file_name="image4.jpg", s3_key="anime/Naruto/image4.jpg", content_type="image/jpeg", created_at=datetime.datetime.now()),
    FileCreateSchema(media_id=1, file_name="trailer1.mp4", s3_key="anime/Naruto/trailer1.mp4", content_type="video/mp4", created_at=datetime.datetime.now()),
    FileCreateSchema(media_id=1, file_name="trailer1_preview.avif", s3_key="anime/Naruto/trailer1_preview.avif", content_type="image/avif", created_at=datetime.datetime.now()),

    FileCreateSchema(media_id=2, file_name="logo1.jpg", s3_key="anime/Onepiece/logo1.jpg", content_type="image/jpeg", created_at=datetime.datetime.now()),
    FileCreateSchema(media_id=2, file_name="image1.jpg", s3_key="anime/Onepiece/image1.jpg", content_type="image/jpeg", created_at=datetime.datetime.now()),
    FileCreateSchema(media_id=2, file_name="image2.jpg", s3_key="anime/Onepiece/image2.jpg", content_type="image/jpeg", created_at=datetime.datetime.now()),
    FileCreateSchema(media_id=2, file_name="trailer1.mp4", s3_key="anime/Onepiece/trailer1.mp4", content_type="video/mp4", created_at=datetime.datetime.now()),
    FileCreateSchema(media_id=2, file_name="trailer1_preview.avif", s3_key="anime/Onepiece/trailer1_preview.avif", content_type="image/avif", created_at=datetime.datetime.now()),

    FileCreateSchema(media_id=3, file_name="image1.jpg", s3_key="anime/Death note/image1.jpg", content_type="image/jpeg", created_at=datetime.datetime.now()),
    FileCreateSchema(media_id=3, file_name="logo1.jpg", s3_key="anime/Death note/logo1.jpg", content_type="image/jpeg", created_at=datetime.datetime.now()),
    FileCreateSchema(media_id=3, file_name="trailer1.mp4", s3_key="anime/Death note/trailer1.mp4", content_type="video/mp4", created_at=datetime.datetime.now()),
    FileCreateSchema(media_id=3, file_name="trailer1_preview.avif", s3_key="anime/Death note/trailer1_preview.avif", content_type="image/avif", created_at=datetime.datetime.now()),

    FileCreateSchema(media_id=4, file_name="logo1.jpg", s3_key="anime/Demon slayer final/logo1.jpg", content_type="image/jpeg", created_at=datetime.datetime.now()),
    FileCreateSchema(media_id=4, file_name="image1.jpg", s3_key="anime/Demon slayer final/image1.jpg", content_type="image/jpeg", created_at=datetime.datetime.now()),
    FileCreateSchema(media_id=4, file_name="image2.jpg", s3_key="anime/Demon slayer final/image2.jpg", content_type="image/jpeg", created_at=datetime.datetime.now()),
    FileCreateSchema(media_id=4, file_name="trailer1.mp4", s3_key="anime/Demon slayer final/trailer1.mp4", content_type="video/mp4", created_at=datetime.datetime.now()),
    FileCreateSchema(media_id=4, file_name="trailer2.mp4", s3_key="anime/Demon slayer final/trailer2.mp4", content_type="video/mp4", created_at=datetime.datetime.now()),
    FileCreateSchema(media_id=4, file_name="trailer1_preview.avif", s3_key="anime/Demon slayer final/trailer1_preview.avif", content_type="image/avif", created_at=datetime.datetime.now()),
    FileCreateSchema(media_id=4, file_name="trailer2_preview.avif", s3_key="anime/Demon slayer final/trailer2_preview.avif", content_type="image/avif", created_at=datetime.datetime.now()),

]


async def main():
    for media in media_list:
        await MediaService.add(media)

    for file in files_list:
        await FileService.add(file)


if __name__ == '__main__':
    asyncio.run(main())