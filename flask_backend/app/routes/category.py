from flask import Blueprint
from app.controllers.category import get_categories, get_category, create_category, update_category, delete_category
from app.middleware.verify_token import admin_required

category_bp = Blueprint('category', __name__)

category_bp.route('/', methods=['GET'])(get_categories)
category_bp.route('/<category_id>', methods=['GET'])(get_category)
category_bp.route('/', methods=['POST'])(admin_required(create_category))
category_bp.route('/<category_id>',
                  methods=['PUT', 'PATCH'])(admin_required(update_category))
category_bp.route('/<category_id>',
                  methods=['DELETE'])(admin_required(delete_category))
