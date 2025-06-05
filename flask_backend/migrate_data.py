import os
import sys
import json
import bcrypt
from dotenv import load_dotenv
from pymongo import MongoClient

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

# Load environment variables
load_dotenv()

# MongoDB connection
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017')
NODE_DB_NAME = 'ecommerce'  # Node.js database name
FLASK_DB_NAME = 'ecommerce'  # Flask database name (could be the same)

# Connect to MongoDB
client = MongoClient(MONGO_URI)
node_db = client[NODE_DB_NAME]
flask_db = client[FLASK_DB_NAME]


def migrate_users():
    """Migrate users from Node.js to Flask"""
    print("Migrating users...")

    # Get users from Node.js database
    node_users = list(node_db.users.find())

    # Clear existing users in Flask database
    flask_db.users.delete_many({})

    # Migrate each user
    for user in node_users:
        # Keep the same password hash as it's already BCrypt
        flask_db.users.insert_one(user)

    print(f"Migrated {len(node_users)} users")


def migrate_brands():
    """Migrate brands from Node.js to Flask"""
    print("Migrating brands...")

    # Get brands from Node.js database
    node_brands = list(node_db.brands.find())

    # Clear existing brands in Flask database
    flask_db.brands.delete_many({})

    # Migrate each brand
    for brand in node_brands:
        flask_db.brands.insert_one(brand)

    print(f"Migrated {len(node_brands)} brands")


def migrate_categories():
    """Migrate categories from Node.js to Flask"""
    print("Migrating categories...")

    # Get categories from Node.js database
    node_categories = list(node_db.categories.find())

    # Clear existing categories in Flask database
    flask_db.categories.delete_many({})

    # Migrate each category
    for category in node_categories:
        flask_db.categories.insert_one(category)

    print(f"Migrated {len(node_categories)} categories")


def migrate_products():
    """Migrate products from Node.js to Flask"""
    print("Migrating products...")

    # Get products from Node.js database
    node_products = list(node_db.products.find())

    # Clear existing products in Flask database
    flask_db.products.delete_many({})

    # Migrate each product
    for product in node_products:
        flask_db.products.insert_one(product)

    print(f"Migrated {len(node_products)} products")


def migrate_addresses():
    """Migrate addresses from Node.js to Flask"""
    print("Migrating addresses...")

    # Get addresses from Node.js database
    node_addresses = list(node_db.addresses.find())

    # Clear existing addresses in Flask database
    flask_db.addresses.delete_many({})

    # Migrate each address
    for address in node_addresses:
        flask_db.addresses.insert_one(address)

    print(f"Migrated {len(node_addresses)} addresses")


def migrate_carts():
    """Migrate carts from Node.js to Flask"""
    print("Migrating carts...")

    # Get carts from Node.js database
    node_carts = list(node_db.carts.find())

    # Clear existing carts in Flask database
    flask_db.carts.delete_many({})

    # Migrate each cart
    for cart in node_carts:
        flask_db.carts.insert_one(cart)

    print(f"Migrated {len(node_carts)} carts")


def migrate_orders():
    """Migrate orders from Node.js to Flask"""
    print("Migrating orders...")

    # Get orders from Node.js database
    node_orders = list(node_db.orders.find())

    # Clear existing orders in Flask database
    flask_db.orders.delete_many({})

    # Migrate each order
    for order in node_orders:
        flask_db.orders.insert_one(order)

    print(f"Migrated {len(node_orders)} orders")


def migrate_reviews():
    """Migrate reviews from Node.js to Flask"""
    print("Migrating reviews...")

    # Get reviews from Node.js database
    node_reviews = list(node_db.reviews.find())

    # Clear existing reviews in Flask database
    flask_db.reviews.delete_many({})

    # Migrate each review
    for review in node_reviews:
        flask_db.reviews.insert_one(review)

    print(f"Migrated {len(node_reviews)} reviews")


def migrate_wishlists():
    """Migrate wishlists from Node.js to Flask"""
    print("Migrating wishlists...")

    # Get wishlists from Node.js database
    node_wishlists = list(node_db.wishlists.find())

    # Clear existing wishlists in Flask database
    flask_db.wishlists.delete_many({})

    # Migrate each wishlist
    for wishlist in node_wishlists:
        flask_db.wishlists.insert_one(wishlist)

    print(f"Migrated {len(node_wishlists)} wishlists")


if __name__ == "__main__":
    print("Starting data migration from Node.js to Flask...")

    # Confirm before proceeding
    confirm = input(
        "This will delete all existing data in the Flask database. Continue? (y/n): ")
    if confirm.lower() != 'y':
        print("Migration cancelled")
        sys.exit(0)

    # Perform migrations
    migrate_users()
    migrate_brands()
    migrate_categories()
    migrate_products()
    migrate_addresses()
    migrate_carts()
    migrate_orders()
    migrate_reviews()
    migrate_wishlists()

    print("Migration completed successfully!")
