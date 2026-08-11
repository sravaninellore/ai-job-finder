import os
import uuid
from fastapi import UploadFile, HTTPException
from app.config import settings

ALLOWED_EXTENSIONS = {".pdf", ".docx"}
MAX_FILE_SIZE_MB = 10
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

class FileStorageService:
    def __init__(self, upload_dir: str = settings.UPLOAD_DIR):
        self.upload_dir = upload_dir
        os.makedirs(self.upload_dir, exist_ok=True)

    def save_file(self, file: UploadFile) -> tuple[str, str, int]:
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file format '{ext}'. Allowed formats: {', '.join(ALLOWED_EXTENSIONS)}"
            )

        # Read content to check file size
        file.file.seek(0, os.SEEK_END)
        file_size = file.file.tell()
        file.file.seek(0)

        if file_size > MAX_FILE_SIZE_BYTES:
            raise HTTPException(
                status_code=400,
                detail=f"File size exceeds maximum allowed size of {MAX_FILE_SIZE_MB}MB."
            )

        unique_filename = f"{uuid.uuid4()}{ext}"
        saved_path = os.path.join(self.upload_dir, unique_filename)

        with open(saved_path, "wb") as f:
            f.write(file.file.read())

        return saved_path, ext, file_size

file_storage_service = FileStorageService()
