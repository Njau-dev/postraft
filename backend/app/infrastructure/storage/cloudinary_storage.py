import cloudinary
import cloudinary.uploader
import cloudinary.api
from flask import current_app
import os
import uuid
from typing import Optional


class CloudinaryStorage:
    """Handles Cloudinary file uploads"""

    def __init__(self):
        self.configured = False

    def _configure(self):
        """Configure Cloudinary if not already done"""
        if not self.configured:
            cloudinary.config(
                cloud_name=current_app.config['CLOUDINARY_CLOUD_NAME'],
                api_key=current_app.config['CLOUDINARY_API_KEY'],
                api_secret=current_app.config['CLOUDINARY_API_SECRET']
            )
            self.configured = True

    def upload_file(self, file, folder: str = 'products') -> Optional[str]:
        """
        Upload file to Cloudinary

        Args:
            file: File object from request
            folder: Cloudinary folder (products, templates, posters, etc.)

        Returns:
            str: Public URL of uploaded file or None if failed
        """
        try:
            self._configure()

            # Generate unique public_id
            ext = os.path.splitext(file.filename)[1]
            public_id = f"{folder}/{uuid.uuid4()}"

            # Upload file
            upload_result = cloudinary.uploader.upload(
                file,
                public_id=public_id,
                folder=folder,
                resource_type='auto'  # Auto-detect image/video
            )

            # Return secure URL
            return upload_result.get('secure_url')

        except Exception as e:
            current_app.logger.error(f"Cloudinary upload error: {e}")
            return None

    def delete_file(self, url: str) -> bool:
        """
        Delete file from Cloudinary

        Args:
            url: Full Cloudinary URL

        Returns:
            bool: True if deleted, False otherwise
        """
        try:
            self._configure()

            # Extract public_id from URL
            # URL format: https://res.cloudinary.com/{cloud_name}/image/upload/v{version}/{public_id}.{format}
            parts = url.split('/')
            # Find the part after 'upload/'
            upload_index = parts.index('upload')
            public_id_with_version = '/'.join(parts[upload_index + 1:])
            # Remove version (v1234567890/) and extension
            if public_id_with_version.startswith('v'):
                public_id_parts = public_id_with_version.split('/')
                public_id = '/'.join(public_id_parts[1:])  # Skip version
                public_id = os.path.splitext(public_id)[0]  # Remove extension
            else:
                public_id = os.path.splitext(public_id_with_version)[0]

            # Delete
            result = cloudinary.uploader.destroy(public_id)
            return result.get('result') == 'ok'

        except Exception as e:
            current_app.logger.error(f"Cloudinary delete error: {e}")
            return False


storage = CloudinaryStorage()
