import uuid
import os
import logging
from pathlib import Path

from flask import Blueprint, send_from_directory, request
from werkzeug.utils import secure_filename

from app.utils.apiResponse import success_response
from app.utils.guards import admin_required
from app.errors import AppError

from app.services import book_service

# Paths
# Go up two levels to get to backend/ from backend/app/routes/
LOCAL_MEDIA_DIR = Path(__file__).resolve().parent.parent.parent / "media"
MEDIA_DIR = Path(
    os.getenv("MEDIA_DIR_PATH", LOCAL_MEDIA_DIR)
).resolve()  # filesystem path

BASE_URL = os.getenv("MEDIA_BASE_URL", "http://localhost:5000")  # for building URLs

BOOKS_DIR = MEDIA_DIR / "books"
COVERS_DIR = MEDIA_DIR / "covers"

logging.basicConfig(level=logging.INFO)
logging.info(f"Using MEDIA_DIR: {MEDIA_DIR}")

# Config
ALLOWED_BOOKS = {"pdf"}
ALLOWED_COVERS = {"jpg", "jpeg", "png", "webp"}


bp = Blueprint("media", __name__, url_prefix="/media")


# GET files
@bp.get("/books/<filename>")
def serve_book(filename):
    filename = secure_filename(filename)
    return send_from_directory(BOOKS_DIR, filename)


@bp.get("/covers/<filename>")
def serve_cover(filename):
    filename = secure_filename(filename)
    return send_from_directory(COVERS_DIR, filename)


# Upload
@bp.post("/books")
@admin_required
def upload_book():
    file = request.files.get("file")
    book_id = request.form.get("book_id")  # Récupéré du form-data

    url = _handle_upload(file, ALLOWED_BOOKS, BOOKS_DIR, "books")

    if book_id:
        book_service.update_book_media(int(book_id), content_url=url)

    return success_response(
        201, {"url": url}, "Fichier PDF lié au livre" if book_id else "Fichier uploadé"
    )


@bp.post("/covers")
@admin_required
def upload_cover():
    file = request.files.get("file")
    book_id = request.form.get("book_id")

    url = _handle_upload(file, ALLOWED_COVERS, COVERS_DIR, "covers")

    if book_id:
        book_service.update_book_media(int(book_id), cover_url=url)

    return success_response(
        201,
        {"url": url},
        "Couverture liée au livre" if book_id else "Couverture uploadée",
    )


# Helpers
def _handle_upload(file, allowed_extensions, folder: Path, subfolder: str):
    if not file or not file.filename:
        raise AppError(400, "Invalid file")

    filename = secure_filename(file.filename)

    if not _allowed_file(filename, allowed_extensions):
        raise AppError(400, "Invalid file type")

    unique_name = f"{uuid.uuid4()}_{filename}"
    file_path = folder / unique_name

    file.save(file_path)

    return f"{BASE_URL}/media/{subfolder}/{unique_name}"


def _allowed_file(filename: str, allowed_extensions: set):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions
