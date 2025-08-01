from typing import List

from pydantic import BaseModel


class UploadUrls(BaseModel):
    logo: List[str] = []
    images: List[str] = []
    trailers: List[str] = []
    preview: List[str] = []

class Response1(BaseModel):
    media_id: int
    upload_urls: UploadUrls

class File(BaseModel):
    content_type: str
    file_name: str

class Input1(BaseModel):
    files: List[File]
