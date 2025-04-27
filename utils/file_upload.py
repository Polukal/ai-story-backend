import os
import uuid
from werkzeug.utils import secure_filename
from PIL import Image

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
MAX_FILE_SIZE_MB = 5  # Max 5 MB
MAX_IMAGE_DIMENSION = 1024  # Max width/height 1024px

def allowed_file(filename: str) -> bool:
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_unique_filename(filename: str) -> str:
    """Generate a secure unique filename preserving extension."""
    ext = filename.rsplit('.', 1)[1].lower()
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    return secure_filename(unique_name)

def delete_old_file(filepath: str):
    """Delete old file from disk if it exists."""
    if filepath and os.path.exists(filepath[1:]):
        try:
            os.remove(filepath[1:])
            print(f"[FILE] Deleted old file: {filepath}")
        except Exception as e:
            print(f"[FILE] Failed to delete file {filepath}: {e}")

def validate_file_size(file) -> bool:
    """Validate that the uploaded file is under max size."""
    file.seek(0, os.SEEK_END)
    size_mb = file.tell() / (1024 * 1024)
    file.seek(0)
    return size_mb <= MAX_FILE_SIZE_MB

def resize_image(filepath: str):
    """Resize the saved image to max dimensions (in-place)."""
    try:
        img = Image.open(filepath)
        img.thumbnail((MAX_IMAGE_DIMENSION, MAX_IMAGE_DIMENSION))
        img.save(filepath)
        print(f"[IMAGE] Resized image: {filepath}")
    except Exception as e:
        print(f"[IMAGE] Failed to resize image {filepath}: {e}")
