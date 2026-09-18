import os
import uuid
from datetime import datetime, timezone
from flask import current_app
from werkzeug.utils import secure_filename
from ..extensions import db
from ..models.product_image import ProductImage


def save_image_local(file, product_id):
    """
    Save an uploaded image to the local filesystem.
    Returns (image_url, storage_path) tuple.
    """
    original_filename = secure_filename(file.filename)
    ext = original_filename.rsplit('.', 1)[-1].lower()
    unique_name = f"{product_id}_{uuid.uuid4().hex}.{ext}"

    upload_folder = current_app.config['UPLOAD_FOLDER_PATH']
    product_folder = os.path.join(upload_folder, str(product_id))
    os.makedirs(product_folder, exist_ok=True)

    file_path = os.path.join(product_folder, unique_name)
    file.save(file_path)

    # Relative storage path
    storage_path = f"{product_id}/{unique_name}"
    # URL served by Flask static route
    image_url = f"/uploads/{storage_path}"

    return image_url, storage_path


def save_image_supabase(file, product_id):
    """
    Upload an image to Supabase Storage.
    Returns (image_url, storage_path) tuple.
    """
    from supabase import create_client

    url = current_app.config['SUPABASE_URL']
    key = current_app.config['SUPABASE_SERVICE_ROLE_KEY']
    bucket = current_app.config['SUPABASE_STORAGE_BUCKET']

    supabase = create_client(url, key)

    original_filename = secure_filename(file.filename)
    ext = original_filename.rsplit('.', 1)[-1].lower()
    unique_name = f"{product_id}/{uuid.uuid4().hex}.{ext}"

    file_data = file.read()
    content_type = _get_content_type(ext)

    supabase.storage.from_(bucket).upload(
        unique_name,
        file_data,
        {'content-type': content_type}
    )

    public_url = supabase.storage.from_(bucket).get_public_url(unique_name)
    return public_url, unique_name


def delete_image_local(storage_path):
    """Delete a local image file."""
    try:
        upload_folder = current_app.config['UPLOAD_FOLDER_PATH']
        file_path = os.path.join(upload_folder, storage_path)
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        current_app.logger.error(f"Failed to delete local image {storage_path}: {e}")


def delete_image_supabase(storage_path):
    """Delete an image from Supabase Storage."""
    try:
        from supabase import create_client
        url = current_app.config['SUPABASE_URL']
        key = current_app.config['SUPABASE_SERVICE_ROLE_KEY']
        bucket = current_app.config['SUPABASE_STORAGE_BUCKET']
        supabase = create_client(url, key)
        supabase.storage.from_(bucket).remove([storage_path])
    except Exception as e:
        current_app.logger.error(f"Failed to delete Supabase image {storage_path}: {e}")


def save_image(file, product_id):
    """
    Environment-aware image save. Routes to local or Supabase based on config.
    Returns (image_url, storage_path).
    """
    backend = current_app.config.get('STORAGE_BACKEND', 'local')
    if backend == 'supabase':
        return save_image_supabase(file, product_id)
    return save_image_local(file, product_id)


def delete_image(storage_path):
    """Environment-aware image deletion."""
    backend = current_app.config.get('STORAGE_BACKEND', 'local')
    if backend == 'supabase':
        delete_image_supabase(storage_path)
    else:
        delete_image_local(storage_path)


def _get_content_type(ext):
    types = {
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'webp': 'image/webp',
    }
    return types.get(ext, 'image/jpeg')
