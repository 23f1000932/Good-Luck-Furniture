from flask import jsonify


def success_response(data=None, message=None, status_code=200, meta=None):
    """Return a standardized success JSON response."""
    payload = {'success': True}
    if data is not None:
        payload['data'] = data
    if message:
        payload['message'] = message
    if meta:
        payload['meta'] = meta
    return jsonify(payload), status_code


def error_response(code, message, status_code=400):
    """Return a standardized error JSON response."""
    return jsonify({
        'success': False,
        'error': {
            'code': code,
            'message': message,
        }
    }), status_code


def paginated_response(items, total, page, per_page):
    """Return a paginated success response."""
    return success_response(
        data=items,
        meta={
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page,
            'has_next': page * per_page < total,
            'has_prev': page > 1,
        }
    )
