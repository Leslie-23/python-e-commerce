from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity


def verify_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({"message": "Authentication failed"}), 401
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            from app.models.user import User
            user_id = get_jwt_identity()
            user = User.objects.get(id=user_id)
            if not user.is_admin:
                return jsonify({"message": "Admin access required"}), 403
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({"message": "Authentication failed"}), 401
    return decorated
