from flask import Blueprint
from app.controllers.order import get_orders, get_order, create_order, update_order_status, update_payment_status
from app.middleware.verify_token import verify_token, admin_required

order_bp = Blueprint('order', __name__)

order_bp.route('/', methods=['GET'])(verify_token(get_orders))
order_bp.route('/<order_id>', methods=['GET'])(verify_token(get_order))
order_bp.route('/', methods=['POST'])(verify_token(create_order))
order_bp.route('/<order_id>/status',
               methods=['PUT'])(admin_required(update_order_status))
order_bp.route('/<order_id>/payment',
               methods=['PUT'])(admin_required(update_payment_status))
