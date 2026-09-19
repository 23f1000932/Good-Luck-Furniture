from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from datetime import datetime, timezone

from ..extensions import db, limiter
from ..models.admin_user import AdminUser
from ..utils.responses import success_response, error_response

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
@limiter.limit("10 per minute")
def login():
    """Admin login — returns JWT access token."""
    data = request.get_json()
    if not data:
        return error_response('BAD_REQUEST', 'Request body is required', 400)

    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not email or not password:
        return error_response('VALIDATION_ERROR', 'Email and password are required', 400)

    user = AdminUser.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return error_response('INVALID_CREDENTIALS', 'Invalid email or password', 401)

    if not user.is_active:
        return error_response('ACCOUNT_DISABLED', 'This account has been disabled', 403)

    # Update last login
    user.touch_login()
    db.session.commit()

    access_token = create_access_token(identity=str(user.id))
    return success_response({
        'access_token': access_token,
        'user': user.to_dict()
    }, 'Login successful')


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    """Get the current authenticated admin user."""
    user_id = int(get_jwt_identity())
    user = AdminUser.query.get(user_id)
    if not user or not user.is_active:
        return error_response('UNAUTHORIZED', 'User not found or inactive', 401)
    return success_response(user.to_dict())


@auth_bp.route('/logout', methods=['POST'])
@jwt_required(optional=True)
def logout():
    """Logout (client should discard the token)."""
    # JWT is stateless; client clears the token
    return success_response(message='Logged out successfully')


@auth_bp.route('/change-password', methods=['PUT'])
@jwt_required()
def change_password():
    """Change the current admin user's password."""
    data = request.get_json()
    if not data:
        return error_response('BAD_REQUEST', 'Request body is required', 400)

    current_password = data.get('current_password', '')
    new_password = data.get('new_password', '')

    if not current_password or not new_password:
        return error_response('VALIDATION_ERROR', 'current_password and new_password are required', 400)

    if len(new_password) < 8:
        return error_response('VALIDATION_ERROR', 'New password must be at least 8 characters', 400)

    user_id = int(get_jwt_identity())
    user = AdminUser.query.get(user_id)
    if not user or not user.is_active:
        return error_response('UNAUTHORIZED', 'User not found', 401)

    if not user.check_password(current_password):
        return error_response('INVALID_CREDENTIALS', 'Current password is incorrect', 400)

    user.set_password(new_password)
    db.session.commit()
    return success_response(message='Password updated successfully')

