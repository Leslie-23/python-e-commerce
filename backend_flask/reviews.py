from flask import Blueprint, request, jsonify

reviews_bp = Blueprint('reviews', __name__)

@reviews_bp.route('/', methods=['GET'])
def get_reviews():
    # TODO: Implement get reviews logic
    return jsonify({'message': 'Get reviews endpoint'}), 200

@reviews_bp.route('/', methods=['POST'])
def create_review():
    # TODO: Implement create review logic
    return jsonify({'message': 'Create review endpoint'}), 201
