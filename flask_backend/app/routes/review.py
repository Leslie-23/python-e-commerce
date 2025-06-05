from flask import Blueprint
from app.controllers.review import get_product_reviews, get_user_reviews, create_review, update_review, delete_review
from app.middleware.verify_token import verify_token

review_bp = Blueprint('review', __name__)

review_bp.route('/product/<product_id>', methods=['GET'])(get_product_reviews)
review_bp.route('/user', methods=['GET'])(verify_token(get_user_reviews))
review_bp.route('/', methods=['POST'])(verify_token(create_review))
review_bp.route(
    '/<review_id>', methods=['PUT', 'PATCH'])(verify_token(update_review))
review_bp.route(
    '/<review_id>', methods=['DELETE'])(verify_token(delete_review))
