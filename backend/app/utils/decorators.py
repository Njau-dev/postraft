from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.core.auth.authentication import AuthenticationService
from app.core.auth.authorization import AuthorizationService


def auth_required(f):
    """
    Decorator to protect routes with JWT authentication

    Usage:
        @bp.route('/protected')
        @auth_required
        def protected_route(current_user):
            return {'message': f'Hello {current_user.email}'}
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()

            user_id = int(get_jwt_identity())
            current_user = AuthenticationService.get_current_user(user_id)

            return f(current_user=current_user, *args, **kwargs)
        except Exception as e:
            return jsonify({'error': str(e)}), 401
    return decorated


def plan_limit(resource_type: str):
    """
    Decorator to check plan limits before executing action

    Args:
        resource_type: Type of resource ('product', 'template', 'generation')

    Usage:
        @bp.route('/products', methods=['POST'])
        @auth_required
        @plan_limit('product')
        def create_product(current_user):
            # Create product logic
    """
    def decorator(f):
        @wraps(f)
        def decorated(current_user, *args, **kwargs):
            # Check limits based on resource type
            if resource_type == 'product':
                can_create, error = AuthorizationService.can_create_product(
                    current_user)
            elif resource_type == 'template':
                can_create, error = AuthorizationService.can_create_template(
                    current_user)
            elif resource_type == 'generation':
                can_create, error = AuthorizationService.can_generate_poster(
                    current_user)
            else:
                can_create, error = False, "Invalid resource type"

            if not can_create:
                return jsonify({'error': error}), 403

            return f(current_user=current_user, *args, **kwargs)
        return decorated
    return decorator


def requires_feature(feature_name: str):
    """
    Decorator to check if user's plan includes a feature

    Usage:
        @bp.route('/auto-post', methods=['POST'])
        @auth_required
        @requires_feature('auto_post')
        def auto_post(current_user):
            # Auto post logic
    """
    def decorator(f):
        @wraps(f)
        def decorated(current_user, *args, **kwargs):
            if not AuthorizationService.has_feature(current_user, feature_name):
                return jsonify({
                    'error': f'This feature requires a plan upgrade',
                    'feature': feature_name
                }), 403
            return f(current_user=current_user, *args, **kwargs)
        return decorated
    return decorator


def admin_required(f):
    """
    Decorator to restrict access to admin users only

    Usage:
        @bp.route('/admin/dashboard')
        @auth_required
        @admin_required
        def admin_dashboard(current_user):
            # Admin dashboard logic
    """
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if not current_user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        return f(current_user=current_user, *args, **kwargs)
    return decorated
