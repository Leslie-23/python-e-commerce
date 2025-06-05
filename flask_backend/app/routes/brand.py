from flask import Blueprint
from app.controllers.brand import get_brands, get_brand, create_brand, update_brand, delete_brand
from app.middleware.verify_token import admin_required

brand_bp = Blueprint('brand', __name__)

brand_bp.route('/', methods=['GET'])(get_brands)
brand_bp.route('/<brand_id>', methods=['GET'])(get_brand)
brand_bp.route('/', methods=['POST'])(admin_required(create_brand))
brand_bp.route(
    '/<brand_id>', methods=['PUT', 'PATCH'])(admin_required(update_brand))
brand_bp.route('/<brand_id>', methods=['DELETE'])(admin_required(delete_brand))
