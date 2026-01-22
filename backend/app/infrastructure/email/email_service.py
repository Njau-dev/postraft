import requests
from flask import current_app
from typing import Optional, List, Dict
import logging
import json

logger = logging.getLogger(__name__)


class EmailService:
    """Service for sending emails via Brevo (Sendinblue) API"""

    # Brevo API endpoints
    BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"
    BREVO_SENDER_ENDPOINT = "https://api.brevo.com/v3/senders"

    @staticmethod
    def _get_headers() -> dict:
        """Get headers for Brevo API requests"""
        api_key = current_app.config.get('BREVO_API_KEY')
        if not api_key:
            logger.error("BREVO_API_KEY not configured")
            return {}

        return {
            'accept': 'application/json',
            'content-type': 'application/json',
            'api-key': api_key
        }

    @staticmethod
    def send_email(
        to_email: str,
        subject: str,
        html_body: str,
        text_body: Optional[str] = None,
        recipient_name: Optional[str] = None
    ) -> dict:
        """
        Send an email via Brevo API

        Args:
            to_email: Recipient email address
            subject: Email subject
            html_body: HTML content
            text_body: Plain text content (optional)
            recipient_name: Recipient name (optional)

        Returns:
            dict: Response containing message_id if successful, error if failed
        """
        try:
            # Get configuration
            api_key = current_app.config.get('BREVO_API_KEY')
            sender_email = current_app.config.get('BREVO_SENDER_EMAIL')
            sender_name = current_app.config.get('BREVO_SENDER_NAME')

            if not all([api_key, sender_email, sender_name]):
                logger.error("Missing Brevo configuration")
                return {'error': 'Email service not configured properly'}

            # Prepare recipients
            to = [{"email": to_email}]
            if recipient_name:
                to[0]["name"] = recipient_name

            # Prepare email data
            email_data = {
                "sender": {
                    "email": sender_email,
                    "name": sender_name
                },
                "to": to,
                "subject": subject,
                "htmlContent": html_body,
            }

            # Add text content if provided
            if text_body:
                email_data["textContent"] = text_body

            # Send email via Brevo API
            headers = EmailService._get_headers()
            if not headers:
                return {'error': 'API key not configured'}

            response = requests.post(
                EmailService.BREVO_API_URL,
                headers=headers,
                json=email_data
            )

            if response.status_code == 201:
                response_data = response.json()
                message_id = response_data.get('messageId')
                logger.info(
                    f"Email sent successfully to {to_email}, message ID: {message_id}")
                return {
                    'success': True,
                    'message_id': message_id
                }
            else:
                error_msg = f"Brevo API error: {response.status_code} - {response.text}"
                logger.error(error_msg)
                return {
                    'error': f"Failed to send email: {response.status_code}",
                    'details': response.text
                }

        except requests.exceptions.RequestException as e:
            error_msg = f"Network error while sending email: {str(e)}"
            logger.error(error_msg)
            return {'error': 'Network error occurred'}
        except Exception as e:
            error_msg = f"Unexpected error while sending email: {str(e)}"
            logger.error(error_msg)
            return {'error': 'Failed to send email'}

    @staticmethod
    def send_password_reset_email(to_email: str, reset_token: str, recipient_name: Optional[str] = None) -> dict:
        """
        Send password reset email via Brevo

        Args:
            to_email: Recipient email address
            reset_token: Password reset token
            recipient_name: Recipient name (optional)

        Returns:
            dict: Response from send_email
        """
        # Get frontend URL from config
        frontend_url = current_app.config.get(
            'FRONTEND_URL', 'http://localhost:3000')
        reset_url = current_app.config.get(
            'PASSWORD_RESET_URL', f'{frontend_url}/reset-password')
        reset_link = f"{reset_url}?token={reset_token}"

        subject = "Reset Your Password"

        # HTML email content
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Password Reset</title>
        </head>
        <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f7f9fc;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                <!-- Header -->
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px 20px; text-align: center;">
                    <h1 style="color: white; margin: 0; font-size: 28px; font-weight: 600;">Password Reset</h1>
                </div>
                
                <!-- Content -->
                <div style="padding: 40px 30px;">
                    <h2 style="color: #2c3e50; margin-top: 0; font-size: 24px;">Hello{', ' + recipient_name if recipient_name else ''},</h2>
                    
                    <p style="font-size: 16px; margin-bottom: 25px; color: #555;">
                        We received a request to reset your password. If you didn't make this request, please ignore this email.
                    </p>
                    
                    <p style="font-size: 16px; margin-bottom: 30px; color: #555;">
                        To reset your password, click the button below:
                    </p>
                    
                    <!-- Reset Button -->
                    <div style="text-align: center; margin: 40px 0;">
                        <a href="{reset_link}" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 16px 32px; text-decoration: none; border-radius: 6px; font-weight: 600; font-size: 16px; display: inline-block; box-shadow: 0 4px 6px rgba(102, 126, 234, 0.4);">
                            Reset Password
                        </a>
                    </div>
                    
                    <!-- Alternative Link -->
                    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 6px; margin-top: 30px; border-left: 4px solid #667eea;">
                        <p style="margin: 0 0 10px 0; font-size: 14px; color: #666; font-weight: 600;">Or copy and paste this link into your browser:</p>
                        <p style="margin: 0; word-break: break-all; color: #2980b9; font-size: 14px; padding: 10px; background-color: white; border-radius: 4px; border: 1px solid #e9ecef;">
                            {reset_link}
                        </p>
                    </div>
                    
                    <!-- Expiry Notice -->
                    <div style="margin-top: 30px; padding: 15px; background-color: #fff8e1; border-radius: 6px; border-left: 4px solid #ffc107;">
                        <p style="margin: 0; color: #856404; font-size: 14px;">
                            <strong>Important:</strong> This link will expire in 1 hour for security reasons.
                        </p>
                    </div>
                </div>
                
                <!-- Footer -->
                <div style="padding: 20px 30px; background-color: #f8f9fa; text-align: center; border-top: 1px solid #e9ecef;">
                    <p style="margin: 0 0 10px 0; font-size: 12px; color: #6c757d;">
                        If you're having trouble clicking the button, copy and paste the URL above into your web browser.
                    </p>
                    <p style="margin: 0; font-size: 12px; color: #6c757d;">
                        This is an automated message. Please do not reply to this email.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """

        # Plain text alternative
        text_body = f"""
        Password Reset Request
        
        Hello{', ' + recipient_name if recipient_name else ''},
        
        We received a request to reset your password. If you didn't make this request, please ignore this email.
        
        To reset your password, click the link below:
        {reset_link}
        
        This link will expire in 1 hour for security reasons.
        
        If you're having trouble clicking the link, copy and paste the URL into your web browser.
        
        This is an automated message. Please do not reply to this email.
        """

        return EmailService.send_email(
            to_email=to_email,
            subject=subject,
            html_body=html_body,
            text_body=text_body,
            recipient_name=recipient_name
        )

    @staticmethod
    def send_password_reset_confirmation(to_email: str, recipient_name: Optional[str] = None) -> dict:
        """
        Send password reset confirmation email via Brevo

        Args:
            to_email: Recipient email address
            recipient_name: Recipient name (optional)

        Returns:
            dict: Response from send_email
        """
        subject = "Password Reset Successful"

        # HTML email content
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Password Reset Successful</title>
        </head>
        <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f7f9fc;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                <!-- Header -->
                <div style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%); padding: 30px 20px; text-align: center;">
                    <h1 style="color: white; margin: 0; font-size: 28px; font-weight: 600;">✓ Password Updated</h1>
                </div>
                
                <!-- Content -->
                <div style="padding: 40px 30px;">
                    <h2 style="color: #2c3e50; margin-top: 0; font-size: 24px;">Hello{', ' + recipient_name if recipient_name else ''},</h2>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <div style="display: inline-block; background-color: #d4edda; border-radius: 50%; width: 80px; height: 80px; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px;">
                            <span style="font-size: 40px; color: #155724;">✓</span>
                        </div>
                    </div>
                    
                    <p style="font-size: 16px; margin-bottom: 20px; color: #555; text-align: center;">
                        Your password has been successfully reset.
                    </p>
                    
                    <p style="font-size: 16px; margin-bottom: 20px; color: #555;">
                        You can now log in to your account with your new password.
                    </p>
                    
                    <!-- Security Alert -->
                    <div style="margin-top: 30px; padding: 20px; background-color: #f8d7da; border-radius: 6px; border-left: 4px solid #dc3545;">
                        <h3 style="color: #721c24; margin-top: 0; font-size: 16px; margin-bottom: 10px;">Security Notice</h3>
                        <p style="margin: 0; color: #721c24; font-size: 14px;">
                            If you did not perform this action, please contact our support team immediately as your account may have been compromised.
                        </p>
                    </div>
                </div>
                
                <!-- Footer -->
                <div style="padding: 20px 30px; background-color: #f8f9fa; text-align: center; border-top: 1px solid #e9ecef;">
                    <p style="margin: 0; font-size: 12px; color: #6c757d;">
                        For security reasons, this is an automated message. Please do not reply to this email.
                    </p>
                    <p style="margin: 10px 0 0 0; font-size: 12px; color: #6c757d;">
                        If you have any questions, please visit our help center.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """

        # Plain text alternative
        text_body = f"""
        Password Reset Successful
        
        Hello{', ' + recipient_name if recipient_name else ''},
        
        Your password has been successfully reset.
        
        You can now log in to your account with your new password.
        
        Security Notice:
        If you did not perform this action, please contact our support team immediately as your account may have been compromised.
        
        For security reasons, this is an automated message. Please do not reply to this email.
        """

        return EmailService.send_email(
            to_email=to_email,
            subject=subject,
            html_body=html_body,
            text_body=text_body,
            recipient_name=recipient_name
        )

    @staticmethod
    def verify_sender() -> dict:
        """
        Verify if the sender email is properly configured in Brevo

        Returns:
            dict: Verification status and information
        """
        try:
            headers = EmailService._get_headers()
            if not headers:
                return {'error': 'API key not configured'}

            response = requests.get(
                EmailService.BREVO_SENDER_ENDPOINT,
                headers=headers
            )

            if response.status_code == 200:
                senders = response.json()
                sender_email = current_app.config.get('BREVO_SENDER_EMAIL')

                # Check if our sender email exists and is verified
                for sender in senders.get('senders', []):
                    if sender['email'] == sender_email:
                        return {
                            'success': True,
                            'verified': sender.get('verified', False),
                            'sender': sender
                        }

                return {
                    'error': f'Sender email {sender_email} not found in Brevo account'
                }
            else:
                return {
                    'error': f'Failed to fetch senders: {response.status_code}',
                    'details': response.text
                }

        except Exception as e:
            logger.error(f"Failed to verify sender: {str(e)}")
            return {'error': str(e)}
