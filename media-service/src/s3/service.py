import asyncio
import uuid
import boto3
from contextlib import asynccontextmanager

from aiobotocore.session import get_session



class AsyncS3SignedURLService:
    expire_time = 900

    def __init__(self, access_key, secret_key, endpoint_url, bucket_name):
        self.bucket = bucket_name
        self.session = get_session()
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
            "region_name": "ru-central-1"
        }

    @asynccontextmanager
    async def _get_client(self):
        async with self.session.create_client('s3', **self.config) as client:
            yield client

    def generate_upload_url(self, key: str, content_type: str):

        client = boto3.client(
            "s3",
            aws_access_key_id=self.config["aws_access_key_id"],
            aws_secret_access_key=self.config["aws_secret_access_key"],
            endpoint_url=self.config["endpoint_url"],
            region_name=self.config["region_name"],
        )
        return client.generate_presigned_url(
            "put_object",
            Params={"Bucket": self.bucket, "Key": key, "ContentType": content_type},
            ExpiresIn=self.expire_time
        )

    def generate_download_url(self, key: str):
        client = boto3.client(
            "s3",
            aws_access_key_id=self.config["aws_access_key_id"],
            aws_secret_access_key=self.config["aws_secret_access_key"],
            endpoint_url=self.config["endpoint_url"],
            region_name=self.config["region_name"],
        )
        return client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket, "Key": key},
            ExpiresIn=self.expire_time
        )

    async def is_uploaded(self, key: str) -> bool:
        async with self._get_client() as client:
            try:
                await client.head_object(Bucket=self.bucket, Key=key)
                return True
            except client.exceptions.ClientError as e:
                if e.response["ResponseMetadata"]["HTTPStatusCode"] == 404:
                    return False
                raise

    async def delete_media_by_uid(self, prefix_url: str, uid: str) -> int:
        prefix = f"{prefix_url}{uid}/"
        async with self._get_client() as client:
            response = await client.list_objects_v2(Bucket=self.bucket, Prefix=prefix)
            if "Contents" not in response:
                return 0
            keys_to_delete = [{"Key": obj["Key"]} for obj in response["Contents"]]
            await client.delete_objects(Bucket=self.bucket, Delete={"Objects": keys_to_delete})
            return len(keys_to_delete)

    async def check_upload_status(self, s3_path_prefix: str, expected_files: list[str]) -> dict:
        async with self._get_client() as client:
            response = await client.list_objects_v2(Bucket=self.bucket, Prefix=s3_path_prefix)
            uploaded_files = [obj["Key"].replace(s3_path_prefix, "") for obj in response.get("Contents", [])]
            return {
                "uploaded": uploaded_files,
                "missing": list(set(expected_files) - set(uploaded_files)),
                "complete": set(expected_files).issubset(uploaded_files),
            }

# Пример использования
async def main():
    s3_client = AsyncS3SignedURLService(
        access_key="d3138e43-5985-47a4-9640-e02138e93aa6:af193c714d6701ccf79ac408572315ef",
        secret_key="c381d3494cbe1514184035405d7dc168",
        endpoint_url="https://s3.cloud.ru",
        bucket_name="bucket-a5e689",
    )

    uid = str(uuid.uuid4())
    content_type = "image/jpeg"
    file_name = "../../../other/mag_bitva.jpg"
    key = f"anime/{uid}/{file_name}"

    print("\n📤 Генерация signed URL для загрузки:")
    upload_url = s3_client.generate_upload_url(key, content_type)
    print(upload_url)

    # ----------------------------
    import requests

    with open(file_name, "rb") as f:
        response = requests.put(upload_url, data=f, headers={"Content-Type": content_type})

    print("Status:", response.status_code)

    # ----------------------------

    print("\n✅ Проверка, загружен ли файл:")
    uploaded = await s3_client.is_uploaded(key)
    print(f"Загружен: {uploaded}")

    print("\n🔗 Генерация signed URL для скачивания (если загружен):")
    if uploaded:
        download_url = s3_client.generate_download_url(key)
        print(download_url)

    print("\n📊 Проверка статуса загрузки всех файлов:")
    expected_files = [file_name]
    status = await s3_client.check_upload_status(f"anime/{uid}/", expected_files)
    print(status)

    input("Ready ?")

    # ⚠️ Будь осторожен, это удаляет файлы!
    print("\n🗑️ Удаление всех файлов по uid:")
    deleted_count = await s3_client.delete_media_by_uid("anime/", uid)
    print(f"Удалено файлов: {deleted_count}")


if __name__ == "__main__":
    asyncio.run(main())
