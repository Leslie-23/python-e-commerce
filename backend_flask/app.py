from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask import jsonify, render_template
from auth import auth_bp
from users import users_bp
from products import products_bp
from orders import orders_bp
from cart import cart_bp
from brands import brands_bp
from categories import categories_bp
from address import address_bp
from reviews import reviews_bp
from wishlist import wishlist_bp
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

app = Flask(__name__)

# Config
MONGO_URI = os.environ.get('MONGO_URI')
if not MONGO_URI:
    print("WARNING: MONGO_URI not found in environment. Falling back to localhost.")
    MONGO_URI = 'mongodb://localhost:27017/ecommerce'
app.config['MONGO_URI'] = MONGO_URI
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key')

# Extensions
mongo = PyMongo(app)
CORS(app, supports_credentials=True, expose_headers=["X-Total-Count"])

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(products_bp, url_prefix='/products')
app.register_blueprint(orders_bp, url_prefix='/orders')
app.register_blueprint(cart_bp, url_prefix='/cart')
app.register_blueprint(brands_bp, url_prefix='/brands')
app.register_blueprint(categories_bp, url_prefix='/categories')
app.register_blueprint(address_bp, url_prefix='/address')
app.register_blueprint(reviews_bp, url_prefix='/reviews')
app.register_blueprint(wishlist_bp, url_prefix='/wishlist')

@app.route('/')
def index():
    try:
        users = list(mongo.db.users.find())
    except Exception as e:
        print(f"MongoDB connection failed: {e}\nUsing dummy data.")
        users = [
            {'name': 'Demo User', 'email': 'demo@example.com'},
            {'name': 'Test User', 'email': 'test@example.com'}
        ]
    return render_template('index.html', users=users)

if __name__ == '__main__':
    app.run(port=int(os.environ.get('PORT', 8000)), debug=True)
