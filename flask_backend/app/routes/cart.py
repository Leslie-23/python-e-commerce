from flask import Blueprint
from app.controllers.cart import get_cart, add_to_cart, update_cart_item, remove_from_cart, clear_cart
from app.middleware.verify_token import verify_token

cart_bp = Blueprint('cart', __name__)

cart_bp.route('/', methods=['GET'])(verify_token(get_cart))
cart_bp.route('/add', methods=['POST'])(verify_token(add_to_cart))
cart_bp.route('/item/<item_id>',
              methods=['PUT', 'PATCH'])(verify_token(update_cart_item))
cart_bp.route('/item/<item_id>',
              methods=['DELETE'])(verify_token(remove_from_cart))
cart_bp.route('/clear', methods=['DELETE'])(verify_token(clear_cart))
