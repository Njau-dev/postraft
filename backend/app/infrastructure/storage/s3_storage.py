import boto3
from botocore.exceptions import ClientError
from flask import current_app
import os
import uuid
from typing import Optional

class S3Storage:
    """Handles S3 file uploads"""
    
    def __init__(self):
        self.s3_client = None
        self.bucket = None
    
    def _get_client(self):
        """Lazy initialization of S3 client"""
        if not self.s3_client:
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
                aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY'],
                region_name=current_app.config['AWS_REGION']
            )
            self.bucket = current_app.config['S3_BUCKET']
        return self.s3_client
    
    def upload_file(self, file, folder: str = 'products') -> Optional[str]:
        """
        Upload file to S3
        
        Args:
            file: File object from request
            folder: S3 folder (products, templates, posters, etc.)
            
        Returns:
            str: Public URL of uploaded file or None if failed
        """
        try:
            # Generate unique filename
            ext = os.path.splitext(file.filename)[1]
            filename = f"{uuid.uuid4()}{ext}"
            key = f"{folder}/{filename}"
            
            # Upload file
            client = self._get_client()
            client.upload_fileobj(
                file,
                self.bucket,
                key,
                ExtraArgs={
                    'ContentType': file.content_type,
                    'ACL': 'public-read'
                }
            )
            
            # Return public URL
            url = f"https://{self.bucket}.s3.{current_app.config['AWS_REGION']}.amazonaws.com/{key}"
            return url
            
        except ClientError as e:
            current_app.logger.error(f"S3 upload error: {e}")
            return None
        except Exception as e:
            current_app.logger.error(f"Upload error: {e}")
            return None
    
    def delete_file(self, url: str) -> bool:
        """
        Delete file from S3
        
        Args:
            url: Full S3 URL
            
        Returns:
            bool: True if deleted, False otherwise
        """
        try:
            # Extract key from URL
            key = url.split(f"{self.bucket}.s3.{current_app.config['AWS_REGION']}.amazonaws.com/")[1]
            
            client = self._get_client()
            client.delete_object(Bucket=self.bucket, Key=key)
            return True
            
        except Exception as e:
            current_app.logger.error(f"S3 delete error: {e}")
            return False

storage = S3Storage()
