from flask import Blueprint
from app.controllers.auth import signup, login, logout, check_auth, verify_otp, resend_otp, forgot_password, reset_password
from app.middleware.verify_token import verify_token

auth_bp = Blueprint('auth', __name__)

auth_bp.route('/signup', methods=['POST'])(signup)
auth_bp.route('/login', methods=['POST'])(login)
auth_bp.route('/logout', methods=['GET'])(logout)
auth_bp.route('/check-auth', methods=['GET'])(verify_token(check_auth))
auth_bp.route('/verify-otp', methods=['POST'])(verify_otp)
auth_bp.route('/resend-otp', methods=['POST'])(resend_otp)
auth_bp.route('/forgot-password', methods=['POST'])(forgot_password)
auth_bp.route('/reset-password', methods=['POST'])(reset_password)
