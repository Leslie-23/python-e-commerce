from flask import Blueprint
from app.controllers.address import get_addresses, get_address, create_address, update_address, delete_address
from app.middleware.verify_token import verify_token

address_bp = Blueprint('address', __name__)

address_bp.route('/', methods=['GET'])(verify_token(get_addresses))
address_bp.route('/<address_id>', methods=['GET'])(verify_token(get_address))
address_bp.route('/', methods=['POST'])(verify_token(create_address))
address_bp.route(
    '/<address_id>', methods=['PUT', 'PATCH'])(verify_token(update_address))
address_bp.route(
    '/<address_id>', methods=['DELETE'])(verify_token(delete_address))
