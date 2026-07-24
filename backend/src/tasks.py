from pathlib import Path

from celery import Celery
from pypdf import PdfReader

from src.config import settings
from src.database_sync import sync_session_maker
from src.logger import logger
from src.models import Alert, StoredFile
from src.storage import storage_provider

celery_app = Celery("file_tasks", broker=settings.REDIS_URL, backend=settings.REDIS_URL)


@celery_app.task
def scan_file_for_threats(file_id: str) -> None:
    with sync_session_maker() as session:
        file_item = session.get(StoredFile, file_id)
        if not file_item:
            return

        file_item.processing_status = "processing"
        reasons: list[str] = []
        extension = Path(file_item.original_name).suffix.lower()

        if extension in {".exe", ".bat", ".cmd", ".sh", ".js"}:
            reasons.append(f"suspicious extension {extension}")

        if file_item.size > settings.MAX_FILE_SIZE_BYTES:
            reasons.append("file is larger than 10 MB")

        if extension == ".pdf" and file_item.mime_type not in {"application/pdf", "application/octet-stream"}:
            reasons.append("pdf extension does not match mime type")

        file_item.scan_status = "suspicious" if reasons else "clean"
        file_item.scan_details = ", ".join(reasons) if reasons else "no threats found"
        file_item.requires_attention = bool(reasons)
        session.commit()
        logger.info(f"Threat scan completed for {file_id}: status={file_item.scan_status}")

    extract_file_metadata.delay(file_id)


@celery_app.task
def extract_file_metadata(file_id: str) -> None:
    with sync_session_maker() as session:
        file_item = session.get(StoredFile, file_id)
        if not file_item:
            return

        stored_path = storage_provider.get_path(file_item.stored_name)
        if not stored_path.exists():
            file_item.processing_status = "failed"
            file_item.scan_status = file_item.scan_status or "failed"
            file_item.scan_details = "stored file not found during metadata extraction"
            session.commit()
            send_file_alert.delay(file_id)
            return

        metadata = {
            "extension": Path(file_item.original_name).suffix.lower(),
            "size_bytes": file_item.size,
            "mime_type": file_item.mime_type,
        }

        if file_item.mime_type.startswith("text/"):
            line_count = 0
            char_count = 0
            with open(stored_path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    line_count += 1
                    char_count += len(line)
            metadata["line_count"] = line_count
            metadata["char_count"] = char_count
        elif file_item.mime_type == "application/pdf":
            try:
                reader = PdfReader(str(stored_path))
                metadata["approx_page_count"] = len(reader.pages)
            except Exception as e:
                logger.exception(f"Failed to read PDF {file_id}: {e}")
                metadata["approx_page_count"] = 0

        file_item.metadata_json = metadata
        file_item.processing_status = "processed"
        session.commit()

    send_file_alert.delay(file_id)


@celery_app.task
def send_file_alert(file_id: str) -> None:
    with sync_session_maker() as session:
        file_item = session.get(StoredFile, file_id)
        if not file_item:
            return

        if file_item.processing_status == "failed":
            alert = Alert(file_id=file_id, level="critical", message="File processing failed")
        elif file_item.requires_attention:
            alert = Alert(
                file_id=file_id,
                level="warning",
                message=f"File requires attention: {file_item.scan_details}",
            )
        else:
            alert = Alert(file_id=file_id, level="info", message="File processed successfully")

        session.add(alert)
        session.commit()
