import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration"""

    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 'postgresql://localhost/postraft')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv(
        'JWT_ACCESS_TOKEN_EXPIRES', 3600)))  # 1 hour

    # Redis
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

    # AWS S3
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
    S3_BUCKET = os.getenv('S3_BUCKET', 'postraft-media')

    # Cloudinary (alternative)
    CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME')
    CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY')
    CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET')

    # CORS
    FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000')

    # Storage Provider
    STORAGE_PROVIDER = os.getenv('STORAGE_PROVIDER', 'cloudinary')

    # Brevo Configuration (API Key)
    BREVO_API_KEY = os.getenv('BREVO_API_KEY')
    BREVO_SENDER_EMAIL = os.getenv('BREVO_SENDER_EMAIL')
    BREVO_SENDER_NAME = os.getenv('BREVO_SENDER_NAME', 'PostRaft Support')

    # Password Reset Configuration
    PASSWORD_RESET_URL = os.getenv(
        'PASSWORD_RESET_URL', 'http://localhost:3000/reset-password')
    PASSWORD_RESET_TOKEN_EXPIRY = timedelta(hours=1)


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
