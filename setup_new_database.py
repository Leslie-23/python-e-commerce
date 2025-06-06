#!/usr/bin/env python3
"""
Setup New Database Script
This script will seed your new MongoDB database with initial data
"""

import os
import sys
import time

# Add the flask_backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'flask_backend'))


def create_admin_user(db):
    """Create admin user in the new database"""

    users_collection = db['users']

    # Check if admin already exists
    existing_admin = users_collection.find_one({"email": "admin@example.com"})
    if existing_admin:
        print("✅ Admin user already exists")
        return existing_admin

    # Create admin user
    admin_password = "admin123"
    hashed_password = bcrypt.hashpw(
        admin_password.encode('utf-8'), bcrypt.gensalt())

    admin_user = {
        "email": "admin@example.com",
        "password": hashed_password.decode('utf-8'),
        "firstName": "Admin",
        "lastName": "User",
        "phone": "1234567890",
        "addresses": [],
        "role": "admin",
        "is_verified": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

    result = users_collection.insert_one(admin_user)
    print(f"✅ Admin user created with ID: {result.inserted_id}")
    return admin_user


def create_sample_products(db):
    """Create sample products in the new database"""

    products_collection = db['products']

    # Check if products already exist
    if products_collection.count_documents({}) > 0:
        print("✅ Products already exist")
        return

    sample_products = [
        {
            "title": "Wireless Bluetooth Headphones",
            "description": "High-quality wireless headphones with noise cancellation",
            "price": 99.99,
            "discountPercentage": 10,
            "discountedPrice": 89.99,
            "rating": 4.5,
            "stock": 50,
            "brand": "AudioTech",
            "category": "Electronics",
            "thumbnail": "https://via.placeholder.com/300x300?text=Headphones",
            "images": ["https://via.placeholder.com/300x300?text=Headphones"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "title": "Smart Fitness Watch",
            "description": "Advanced fitness tracking with heart rate monitor",
            "price": 199.99,
            "discountPercentage": 15,
            "discountedPrice": 169.99,
            "rating": 4.3,
            "stock": 30,
            "brand": "FitTech",
            "category": "Electronics",
            "thumbnail": "https://via.placeholder.com/300x300?text=Watch",
            "images": ["https://via.placeholder.com/300x300?text=Watch"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "title": "Organic Cotton T-Shirt",
            "description": "Comfortable organic cotton t-shirt in various colors",
            "price": 24.99,
            "discountPercentage": 0,
            "discountedPrice": 24.99,
            "rating": 4.1,
            "stock": 100,
            "brand": "EcoWear",
            "category": "Clothing",
            "thumbnail": "https://via.placeholder.com/300x300?text=T-Shirt",
            "images": ["https://via.placeholder.com/300x300?text=T-Shirt"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    ]

    result = products_collection.insert_many(sample_products)
    print(f"✅ {len(result.inserted_ids)} sample products created")


def create_sample_brands(db):
    """Create sample brands in the new database"""

    brands_collection = db['brands']

    # Check if brands already exist
    if brands_collection.count_documents({}) > 0:
        print("✅ Brands already exist")
        return

    sample_brands = [
        {"label": "AudioTech", "value": "audiotech"},
        {"label": "FitTech", "value": "fittech"},
        {"label": "EcoWear", "value": "ecowear"},
        {"label": "TechGear", "value": "techgear"},
        {"label": "StyleCo", "value": "styleco"}
    ]

    result = brands_collection.insert_many(sample_brands)
    print(f"✅ {len(result.inserted_ids)} sample brands created")


def create_sample_categories(db):
    """Create sample categories in the new database"""

    categories_collection = db['categories']

    # Check if categories already exist
    if categories_collection.count_documents({}) > 0:
        print("✅ Categories already exist")
        return

    sample_categories = [
        {"label": "Electronics", "value": "electronics"},
        {"label": "Clothing", "value": "clothing"},
        {"label": "Home & Garden", "value": "home-garden"},
        {"label": "Sports & Fitness", "value": "sports-fitness"},
        {"label": "Books", "value": "books"}
    ]

    result = categories_collection.insert_many(sample_categories)
    print(f"✅ {len(result.inserted_ids)} sample categories created")


def setup_new_database(mongo_uri, db_name="ecommerce"):
    """Set up your new MongoDB database with initial data"""

    print(f"🚀 Setting up new database: {db_name}")
    print("=" * 50)

    try:
        # Connect to MongoDB
        client = MongoClient(mongo_uri)
        db = client[db_name]

        print("🔌 Connected to MongoDB")

        # Create collections and initial data
        print("\n📚 Creating initial data...")

        create_admin_user(db)
        create_sample_products(db)
        create_sample_brands(db)
        create_sample_categories(db)

        # List all collections
        collections = db.list_collection_names()
        print(f"\n📋 Collections created: {collections}")

        # Show summary
        print(f"\n📊 Database Summary:")
        print(f"   Users: {db['users'].count_documents({})}")
        print(f"   Products: {db['products'].count_documents({})}")
        print(f"   Brands: {db['brands'].count_documents({})}")
        print(f"   Categories: {db['categories'].count_documents({})}")

        client.close()
        print("\n✅ Database setup completed successfully!")

        return True

    except Exception as e:
        print(f"❌ Database setup failed: {str(e)}")
        return False


def main():
    """Main function"""

    print("🗄️  Database Setup Tool")
    print("=" * 50)

    # Get MongoDB URI
    print("Please provide your MongoDB connection string:")
    mongo_uri = input("MongoDB URI: ").strip()

    if not mongo_uri:
        print("❌ MongoDB URI is required")
        return

    # Get database name
    db_name = input("Database name (default: ecommerce): ").strip()
    if not db_name:
        db_name = "ecommerce"

    # Setup database
    success = setup_new_database(mongo_uri, db_name)

    if success:
        print(f"\n🎉 Your new database '{db_name}' is ready!")
        print("\nNext steps:")
        print("1. Update your .env file with the new MONGO_URI")
        print("2. Restart your Flask backend")
        print("3. Test login with admin@example.com / admin123")
    else:
        print("\n❌ Database setup failed. Please check your MongoDB URI and try again.")


if __name__ == "__main__":
    main()
