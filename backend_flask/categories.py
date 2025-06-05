from flask import Blueprint, request, jsonify

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/', methods=['GET'])
def get_categories():
    # TODO: Implement get categories logic
    return jsonify({'message': 'Get categories endpoint'}), 200

@categories_bp.route('/', methods=['POST'])
def create_category():
    # TODO: Implement create category logic
    return jsonify({'message': 'Create category endpoint'}), 201
