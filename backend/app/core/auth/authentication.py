from app.extensions import db
from app.models import User, Plan, PasswordResetToken
from flask_jwt_extended import create_access_token
from datetime import datetime, timedelta
import secrets
import logging
from app.infrastructure.email.email_service import EmailService

logger = logging.getLogger(__name__)


class AuthenticationService:
    """Handles user authentication logic"""

    @staticmethod
    def register_user(email: str, password: str, user_name: str) -> dict:
        """
        Register a new user

        Args:
            user_name: User first name
            email: User email
            password: Plain text password

        Returns:
            dict: User data and token

        Raises:
            ValueError: If email already exists or validation fails
        """
        # Validate email
        if not email or '@' not in email:
            raise ValueError('Invalid email address')

        # Validate password
        if not password or len(password) < 8:
            raise ValueError('Password must be at least 8 characters')

        if not user_name or len(user_name) < 2:
            raise ValueError('User name must be at least 2 characters')

        # Check if user exists
        existing_user = User.query.filter_by(email=email.lower()).first()
        if existing_user:
            raise ValueError('Email already registered')

        # Get Free plan (default)
        free_plan = Plan.query.filter_by(name='Free').first()
        if not free_plan:
            raise ValueError('Default plan not found')

        # Create user
        user = User(
            email=email.lower(),
            plan_id=free_plan.id,
            user_name=user_name
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        # Generate token
        token = create_access_token(identity=str(user.id))

        return {
            'user': user.to_dict(),
            'token': token
        }

    @staticmethod
    def login_user(email: str, password: str) -> dict:
        """
        Login user

        Args:
            email: User email
            password: Plain text password

        Returns:
            dict: User data and token

        Raises:
            ValueError: If credentials are invalid
        """
        # Find user
        user = User.query.filter_by(email=email.lower()).first()

        if not user or not user.check_password(password):
            raise ValueError('Invalid email or password')

        # Generate token
        token = create_access_token(identity=str(user.id))

        return {
            'user': user.to_dict(),
            'token': token
        }

    @staticmethod
    def get_current_user(user_id: int) -> User:
        """
        Get current authenticated user

        Args:
            user_id: User ID from JWT token

        Returns:
            User: User object

        Raises:
            ValueError: If user not found
        """
        user = User.query.get(user_id)
        if not user:
            raise ValueError('User not found')
        return user

    @staticmethod
    def forgot_password(email: str) -> dict:
        """
        Initiate password reset process

        Args:
            email: User email

        Returns:
            dict: Success message

        Raises:
            ValueError: If email not found
        """
        # Find user
        user = User.query.filter_by(email=email.lower()).first()

        if not user:
            # For security, don't reveal that email doesn't exist
            logger.info(
                f"Password reset requested for non-existent email: {email}")
            return {
                'message': 'If an account exists with this email, you will receive a password reset link shortly.'
            }

        # Generate a secure token
        reset_token = secrets.token_urlsafe(32)

        # Set expiry time (1 hour from now)
        expiry_time = datetime.utcnow() + timedelta(hours=1)

        # Create or update reset token
        existing_token = PasswordResetToken.query.filter_by(
            user_id=user.id).first()

        if existing_token:
            existing_token.token = reset_token
            existing_token.expires_at = expiry_time
            existing_token.used = False
        else:
            reset_token_record = PasswordResetToken(
                user_id=user.id,
                token=reset_token,
                expires_at=expiry_time
            )
            db.session.add(reset_token_record)

        db.session.commit()

        # Send password reset email via Brevo API
        try:
            email_response = EmailService.send_password_reset_email(
                to_email=user.email,
                reset_token=reset_token,
                recipient_name=user.user_name
            )

            if email_response.get('success'):
                logger.info(f"Password reset email sent to {user.email}")
            else:
                logger.warning(
                    f"Email sending issue: {email_response.get('error')}")
                # Don't raise error to user, just log it

        except Exception as e:
            logger.error(f"Failed to send password reset email: {str(e)}")
            # Don't raise error to user, just log it

        return {
            'message': 'If an account exists with this email, you will receive a password reset link shortly.'
        }

    @staticmethod
    def reset_password(token: str, new_password: str) -> dict:
        """
        Reset password using token

        Args:
            token: Password reset token
            new_password: New password

        Returns:
            dict: Success message and user data

        Raises:
            ValueError: If token invalid, expired, or password invalid
        """
        # Validate new password
        if not new_password or len(new_password) < 8:
            raise ValueError('Password must be at least 8 characters')

        # Find valid token
        reset_token_record = PasswordResetToken.query.filter_by(
            token=token,
            used=False
        ).first()

        if not reset_token_record:
            raise ValueError('Invalid or expired reset token')

        # Check if token is expired
        if reset_token_record.expires_at < datetime.utcnow():
            raise ValueError('Reset token has expired')

        # Get user
        user = User.query.get(reset_token_record.user_id)
        if not user:
            raise ValueError('User not found')

        # Update password
        user.set_password(new_password)

        # Mark token as used
        reset_token_record.used = True
        reset_token_record.used_at = datetime.utcnow()

        db.session.commit()

        # Send confirmation email via Brevo API
        try:
            email_response = EmailService.send_password_reset_confirmation(
                to_email=user.email,
                recipient_name=user.user_name
            )

            if email_response.get('success'):
                logger.info(
                    f"Password reset confirmation sent to {user.email}")
            else:
                logger.warning(
                    f"Confirmation email issue: {email_response.get('error')}")

        except Exception as e:
            logger.error(f"Failed to send confirmation email: {str(e)}")
            # Don't raise error to user

        # Generate new access token
        access_token = create_access_token(identity=str(user.id))

        return {
            'message': 'Password reset successfully',
            'user': user.to_dict(),
            'token': access_token
        }

    @staticmethod
    def validate_reset_token(token: str) -> dict:
        """
        Validate reset token without using it

        Args:
            token: Password reset token

        Returns:
            dict: Token validity and user info if valid

        Raises:
            ValueError: If token invalid
        """
        # Find valid token
        reset_token_record = PasswordResetToken.query.filter_by(
            token=token,
            used=False
        ).first()

        if not reset_token_record:
            raise ValueError('Invalid reset token')

        # Check if token is expired
        if reset_token_record.expires_at < datetime.utcnow():
            raise ValueError('Reset token has expired')

        # Get user
        user = User.query.get(reset_token_record.user_id)
        if not user:
            raise ValueError('User not found')

        return {
            'valid': True,
            'email': user.email,
            'expires_at': reset_token_record.expires_at.isoformat()
        }
