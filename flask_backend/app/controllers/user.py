from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
import bcrypt

from app.models.user import User
from app.utils.sanitize_user import sanitize_user
from app.middleware.verify_token import admin_required


def get_users():
    try:
        users = User.objects.all()
        return jsonify([sanitize_user(user) for user in users]), 200
    except Exception as e:
        print(f"Error in get_users: {e}")
        return jsonify({"message": "Error occurred while fetching users"}), 500


def get_user(user_id):
    try:
        user = User.objects.get(id=user_id)
        return jsonify(sanitize_user(user)), 200
    except User.DoesNotExist:
        return jsonify({"message": "User not found"}), 404
    except Exception as e:
        print(f"Error in get_user: {e}")
        return jsonify({"message": "Error occurred while fetching user"}), 500


def update_user(user_id):
    try:
        # Ensure user can only update their own profile or admin can update any
        current_user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)

        if str(user.id) != current_user_id:
            current_user = User.objects.get(id=current_user_id)
            if not current_user.is_admin:
                return jsonify({"message": "Unauthorized"}), 403

        data = request.get_json()

        # Don't allow updating email or admin status directly
        if 'email' in data:
            del data['email']

        # Only admins can update admin status
        if 'is_admin' in data:
            current_user = User.objects.get(id=current_user_id)
            if not current_user.is_admin:
                del data['is_admin']

        # Hash password if it's being updated
        if 'password' in data and data['password']:
            data['password'] = bcrypt.hashpw(data['password'].encode(
                'utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Update user
        for key, value in data.items():
            setattr(user, key, value)

        user.save()

        return jsonify(sanitize_user(user)), 200
    except User.DoesNotExist:
        return jsonify({"message": "User not found"}), 404
    except Exception as e:
        print(f"Error in update_user: {e}")
        return jsonify({"message": "Error occurred while updating user"}), 500


@admin_required
def delete_user(user_id):
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return jsonify({"message": "User deleted successfully"}), 200
    except User.DoesNotExist:
        return jsonify({"message": "User not found"}), 404
    except Exception as e:
        print(f"Error in delete_user: {e}")
        return jsonify({"message": "Error occurred while deleting user"}), 500
