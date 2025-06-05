from flask import Blueprint
from app.controllers.user import get_users, get_user, update_user, delete_user
from app.middleware.verify_token import verify_token, admin_required

user_bp = Blueprint('user', __name__)

user_bp.route('/', methods=['GET'])(admin_required(get_users))
user_bp.route('/<user_id>', methods=['GET'])(verify_token(get_user))
user_bp.route('/<user_id>', methods=['PUT',
              'PATCH'])(verify_token(update_user))
user_bp.route('/<user_id>', methods=['DELETE'])(admin_required(delete_user))
