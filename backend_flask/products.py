from flask import Blueprint, request, jsonify

products_bp = Blueprint('products', __name__)

@products_bp.route('/', methods=['GET'])
def get_products():
    # TODO: Implement get products logic
    return jsonify({'message': 'Get products endpoint'}), 200

@products_bp.route('/<product_id>', methods=['GET'])
def get_product(product_id):
    # TODO: Implement get product by id logic
    return jsonify({'message': f'Get product {product_id} endpoint'}), 200

@products_bp.route('/', methods=['POST'])
def create_product():
    # TODO: Implement create product logic
    return jsonify({'message': 'Create product endpoint'}), 201

@products_bp.route('/<product_id>', methods=['PATCH'])
def update_product(product_id):
    # TODO: Implement update product logic
    return jsonify({'message': f'Update product {product_id} endpoint'}), 200

@products_bp.route('/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    # TODO: Implement delete product logic
    return jsonify({'message': f'Delete product {product_id} endpoint'}), 200
