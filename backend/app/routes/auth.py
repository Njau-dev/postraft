from flask import Blueprint, request, current_app
from app.core.auth.authentication import AuthenticationService
from app.utils.decorators import auth_required
from app.utils.responses import success_response, error_response, created_response

bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user

    Request body:
        {
            "email": "user@example.com",
            "password": "password123"
        }

    Response:
        {
            "success": true,
            "data": {
                "user": {...},
                "token": "eyJ..."
            }
        }
    """
    try:
        data = request.get_json()

        if not data:
            return error_response('Request body is required', 400)

        email = data.get('email')
        password = data.get('password')
        user_name = data.get('user_name')

        if not email or not password or not user_name:
            return error_response('Email, password, and user name are required', 400)

        result = AuthenticationService.register_user(
            email, password, user_name)

        return created_response(result, 'User registered successfully')

    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        # log error
        current_app.logger.error(f"Registration error: {str(e)}")
        return error_response('Registration failed', 500)


@bp.route('/login', methods=['POST'])
def login():
    """
    Login user

    Request body:
        {
            "email": "user@example.com",
            "password": "password123"
        }

    Response:
        {
            "success": true,
            "data": {
                "user": {...},
                "token": "eyJ..."
            }
        }
    """
    try:
        data = request.get_json()

        if not data:
            return error_response('Request body is required', 400)

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return error_response('Email and password are required', 400)

        result = AuthenticationService.login_user(email, password)

        return success_response(result, 'Login successful')

    except ValueError as e:
        return error_response(str(e), 401)
    except Exception as e:
        return error_response('Login failed', 500)


@bp.route('/me', methods=['GET'])
@auth_required
def get_current_user(current_user):
    """
    Get current authenticated user

    Headers:
        Authorization: Bearer {token}

    Response:
        {
            "success": true,
            "data": {
                "user": {...},
                "plan": {...}
            }
        }
    """
    print(f'Current user: {current_user}')
    try:
        return success_response({
            'user': current_user.to_dict(),
            'plan': current_user.plan.to_dict()
        })
    except Exception as e:
        return error_response('Failed to fetch user', 500)


@bp.route('/logout', methods=['POST'])
@auth_required
def logout(current_user):
    """
    Logout user (client-side token removal)

    Note: JWT tokens are stateless, so logout is handled client-side
    """
    return success_response(message='Logged out successfully')


@bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    """
    Request password reset

    Request body:
        {
            "email": "user@example.com"
        }

    Response:
        {
            "success": true,
            "message": "Password reset email sent"
        }
    """
    try:
        data = request.get_json()

        if not data:
            return error_response('Request body is required', 400)

        email = data.get('email')

        if not email:
            return error_response('Email is required', 400)

        result = AuthenticationService.forgot_password(email)

        return success_response(result, result['message'])

    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        current_app.logger.error(f"Forgot password error: {str(e)}")
        return error_response('Failed to send password reset email', 500)


@bp.route('/reset-password', methods=['POST'])
def reset_password():
    """
    Reset password using token

    Request body:
        {
            "token": "reset_token_string",
            "password": "new_password_123"
        }

    Response:
        {
            "success": true,
            "data": {
                "user": {...},
                "token": "eyJ..."
            },
            "message": "Password reset successfully"
        }
    """
    try:
        data = request.get_json()

        if not data:
            return error_response('Request body is required', 400)

        token = data.get('token')
        password = data.get('password')

        if not token:
            return error_response('Reset token is required', 400)
        if not password:
            return error_response('New password is required', 400)

        result = AuthenticationService.reset_password(token, password)

        return success_response(result, result['message'])

    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        current_app.logger.error(f"Reset password error: {str(e)}")
        return error_response('Failed to reset password', 500)


@bp.route('/validate-reset-token/<token>', methods=['GET'])
def validate_reset_token(token):
    """
    Validate password reset token

    URL parameter:
        token: Reset token from email link

    Response:
        {
            "success": true,
            "data": {
                "valid": true,
                "email": "user@example.com",
                "expires_at": "2023-12-01T12:00:00"
            }
        }
    """
    try:
        if not token:
            return error_response('Token is required', 400)

        result = AuthenticationService.validate_reset_token(token)

        return success_response(result, 'Token is valid')

    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        current_app.logger.error(f"Validate token error: {str(e)}")
        return error_response('Failed to validate token', 500)
