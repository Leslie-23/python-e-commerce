from flask import Blueprint
from app.controllers.product import get_products, get_product, create_product, update_product, delete_product
from app.middleware.verify_token import admin_required

product_bp = Blueprint('product', __name__)

product_bp.route('/', methods=['GET'])(get_products)
product_bp.route('/<product_id>', methods=['GET'])(get_product)
product_bp.route('/', methods=['POST'])(admin_required(create_product))
product_bp.route(
    '/<product_id>', methods=['PUT', 'PATCH'])(admin_required(update_product))
product_bp.route(
    '/<product_id>', methods=['DELETE'])(admin_required(delete_product))
