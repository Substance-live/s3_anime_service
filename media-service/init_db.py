import asyncio

from src.db import create_tables
from src.file.models import FileOrm
from src.media.models import MediaOrm

async def main():
    await create_tables()

if __name__ == '__main__':
    asyncio.run(main())