from flask import current_app

_storage = None

def _get_storage():
    global _storage
    if _storage is None:
        if current_app.config['STORAGE_PROVIDER'] == 's3':
            from app.infrastructure.storage.s3_storage import storage
            _storage = storage
        elif current_app.config['STORAGE_PROVIDER'] == 'cloudinary':
            from app.infrastructure.storage.cloudinary_storage import storage
            _storage = storage
        else:
            raise ValueError("Invalid STORAGE_PROVIDER. Must be 's3' or 'cloudinary'")
    return _storage


def upload_image(file, folder='products'):
    """Upload image file"""
    return _get_storage().upload_file(file, folder)


def delete_image(url):
    """Delete image file"""
    return _get_storage().delete_file(url)
