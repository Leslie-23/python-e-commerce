import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from app.database.db import init_db

load_dotenv()


def create_app():
    app = Flask(__name__)

    # Configure app    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_key')
    app.config['JWT_SECRET_KEY'] = os.environ.get(
        'JWT_SECRET_KEY', 'dev_jwt_key')
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_COOKIE_SECURE'] = os.environ.get(
        'PRODUCTION', 'false').lower() == 'true'
    # Disable CSRF for compatibility
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False
    app.config['JWT_ACCESS_COOKIE_NAME'] = 'token'  # Match Node.js cookie name
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(
        os.environ.get('COOKIE_EXPIRATION_DAYS', 30)) * 24 * 60 * 60

    # Initialize extensions
    # Collect all available origins from environment variables
    origins = []
    for i in range(1, 10):  # Support up to ORIGIN_9
        origin_key = f'ORIGIN_{i}'
        origin = os.environ.get(origin_key)
        if origin:
            # Remove trailing slash if present
            if origin.endswith('/'):
                origin = origin[:-1]
            origins.append(origin)

    # Also check for simple ORIGIN environment variable
    simple_origin = os.environ.get('ORIGIN')
    if simple_origin:
        origins.append(simple_origin)

    # If no origins were found, default to allow all
    if not origins:
        origins = ['*']

    print(f"CORS configured with origins: {origins}")

    CORS(app,
         origins=origins,
         supports_credentials=True,
         expose_headers=["X-Total-Count"],
         methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
    JWTManager(app)

    # Initialize database
    init_db(app)

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.user import user_bp
    from app.routes.product import product_bp
    from app.routes.order import order_bp
    from app.routes.cart import cart_bp
    from app.routes.brand import brand_bp
    from app.routes.category import category_bp
    from app.routes.address import address_bp
    from app.routes.review import review_bp
    from app.routes.wishlist import wishlist_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(product_bp, url_prefix='/products')
    app.register_blueprint(order_bp, url_prefix='/orders')
    app.register_blueprint(cart_bp, url_prefix='/cart')
    app.register_blueprint(brand_bp, url_prefix='/brands')
    app.register_blueprint(category_bp, url_prefix='/categories')
    app.register_blueprint(address_bp, url_prefix='/address')
    app.register_blueprint(review_bp, url_prefix='/reviews')
    app.register_blueprint(wishlist_bp, url_prefix='/wishlist')

    @app.route('/')
    def index():
        return {'message': 'running'}, 200

    return app
