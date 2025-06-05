from flask import Blueprint
from app.controllers.wishlist import get_wishlist, add_to_wishlist, remove_from_wishlist, clear_wishlist
from app.middleware.verify_token import verify_token

wishlist_bp = Blueprint('wishlist', __name__)

wishlist_bp.route('/', methods=['GET'])(verify_token(get_wishlist))
wishlist_bp.route('/add', methods=['POST'])(verify_token(add_to_wishlist))
wishlist_bp.route('/item/<product_id>',
                  methods=['DELETE'])(verify_token(remove_from_wishlist))
wishlist_bp.route('/clear', methods=['DELETE'])(verify_token(clear_wishlist))
