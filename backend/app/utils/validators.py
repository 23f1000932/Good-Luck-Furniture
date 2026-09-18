import os
from flask import current_app
from werkzeug.utils import secure_filename


ALLOWED_MIME_TYPES = {
    'image/jpeg', 'image/jpg', 'image/png', 'image/webp'
}

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


def allowed_file(filename):
    """Check if the file extension is allowed."""
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in ALLOWED_EXTENSIONS


def validate_image_file(file):
    """
    Validate an uploaded image file.
    Returns (is_valid: bool, error_message: str | None)
    """
    if not file:
        return False, 'No file provided'

    filename = file.filename
    if not filename or filename == '':
        return False, 'No filename provided'

    if not allowed_file(filename):
        return False, f'File type not allowed. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}'

    # Read a small portion to check magic bytes
    file.seek(0)
    header = file.read(12)
    file.seek(0)

    # Check magic bytes for common image formats
    if not _is_valid_image_header(header):
        return False, 'File does not appear to be a valid image'

    return True, None


def _is_valid_image_header(header):
    """Check image magic bytes."""
    # JPEG
    if header[:2] == b'\xff\xd8':
        return True
    # PNG
    if header[:8] == b'\x89PNG\r\n\x1a\n':
        return True
    # WebP
    if header[:4] == b'RIFF' and header[8:12] == b'WEBP':
        return True
    return False


def safe_filename(filename):
    """Return a secure filename."""
    return secure_filename(filename)


def validate_required_fields(data, required_fields):
    """
    Validate that all required fields are present and non-empty.
    Returns list of missing field names.
    """
    missing = []
    for field in required_fields:
        value = data.get(field)
        if value is None or (isinstance(value, str) and not value.strip()):
            missing.append(field)
    return missing


VALID_PRICE_VISIBILITY = {'visible', 'contact_for_price', 'hidden'}


def validate_price_visibility(value):
    """Validate price_visibility field."""
    if value and value not in VALID_PRICE_VISIBILITY:
        return False, f'price_visibility must be one of: {", ".join(VALID_PRICE_VISIBILITY)}'
    return True, None
