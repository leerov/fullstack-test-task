import mimetypes
import shutil
import tempfile
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status
from sqlalchemy import select

from src.database import async_session_maker
from src.logger import logger
from src.models import StoredFile
from src.storage import storage_provider
from src.validators import validate_file


async def list_files(skip: int = 0, limit: int = 100) -> list[StoredFile]:
    async with async_session_maker() as session:
        result = await session.execute(
            select(StoredFile)
            .order_by(StoredFile.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())


async def get_file(file_id: str) -> StoredFile:
    async with async_session_maker() as session:
        file_item = await session.get(StoredFile, file_id)
        if not file_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
        return file_item


async def create_file(title: str, upload_file: UploadFile) -> StoredFile:
    filename = upload_file.filename or ""
    file_id = str(uuid4())
    suffix = Path(filename).suffix
    stored_name = f"{file_id}{suffix}"

    # Non-obvious optimization: Validate file type from the header (first 261 bytes)
    # before performing any disk I/O, preventing malicious files from being written to disk.
    header = await upload_file.file.read(261)
    await upload_file.file.seek(0)

    validate_file(filename, upload_file.content_type, header)

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(upload_file.file, tmp)
        tmp_path = Path(tmp.name)

    try:
        storage_provider.save_file(stored_name, tmp_path)
        logger.info(f"Successfully saved file to storage: {stored_name}")

        file_size = tmp_path.stat().st_size
        mime_type = upload_file.content_type or mimetypes.guess_type(stored_name)[0] or "application/octet-stream"

        file_item = StoredFile(
            id=file_id,
            title=title,
            original_name=filename,
            stored_name=stored_name,
            mime_type=mime_type,
            size=file_size,
            processing_status="uploaded",
        )
        async with async_session_maker() as session:
            session.add(file_item)
            await session.commit()
            await session.refresh(file_item)
        return file_item
    finally:
        tmp_path.unlink(missing_ok=True)


async def update_file(file_id: str, title: str) -> StoredFile:
    async with async_session_maker() as session:
        file_item = await session.get(StoredFile, file_id)
        if not file_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
        file_item.title = title
        await session.commit()
        await session.refresh(file_item)
        return file_item


async def delete_file(file_id: str) -> None:
    async with async_session_maker() as session:
        file_item = await session.get(StoredFile, file_id)
        if not file_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
        storage_provider.delete(file_item.stored_name)
        await session.delete(file_item)
        await session.commit()
        logger.info(f"Deleted file {file_id} from database and storage")


async def get_file_path(file_id: str) -> tuple[StoredFile, Path]:
    file_item = await get_file(file_id)
    stored_path = storage_provider.get_path(file_item.stored_name)
    if not stored_path.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stored file not found")
    return file_item, stored_path