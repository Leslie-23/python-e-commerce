from flask import Blueprint, request, jsonify

users_bp = Blueprint('users', __name__)

# Ensure both /users and /users/ work by setting strict_slashes=False

@users_bp.route('/', methods=['GET'], strict_slashes=False)
def get_users():
    # TODO: Implement get users logic
    return jsonify({'message': 'Get users endpoint'}), 200

@users_bp.route('/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    # TODO: Implement get user by id logic
    return jsonify({'message': f'Get user {user_id} endpoint'}), 200

@users_bp.route('/', methods=['POST'], strict_slashes=False)
def create_user():
    # TODO: Implement create user logic
    return jsonify({'message': 'Create user endpoint'}), 201

@users_bp.route('/<user_id>', methods=['PATCH'], strict_slashes=False)
def update_user(user_id):
    # TODO: Implement update user logic
    return jsonify({'message': f'Update user {user_id} endpoint'}), 200

@users_bp.route('/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    # TODO: Implement delete user logic
    return jsonify({'message': f'Delete user {user_id} endpoint'}), 200
