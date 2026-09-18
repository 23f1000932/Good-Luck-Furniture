from functools import wraps
from flask import current_app
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from ..utils.responses import error_response
from ..models.admin_user import AdminUser


def require_admin(f):
    """
    Decorator that verifies a valid JWT token exists and the user
    is an active admin. Blocks all unauthenticated/unauthorized requests.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = AdminUser.query.get(user_id)
            if not user or not user.is_active:
                return error_response('UNAUTHORIZED', 'Access denied', 401)
            return f(*args, **kwargs)
        except Exception as e:
            return error_response('UNAUTHORIZED', 'Authentication required', 401)
    return decorated
