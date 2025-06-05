import os
import sys
import bcrypt
from dotenv import load_dotenv
from app import create_app
from app.models.user import User
from app.models.brand import Brand
from app.models.category import Category
from app.models.product import Product

# Load environment variables
load_dotenv()

# Initialize Flask app
app = create_app()
app_context = app.app_context()
app_context.push()


def create_admin_user():
    """Create an admin user if it doesn't exist"""
    try:
        # Check if admin user exists
        admin = User.objects(email='admin@example.com').first()
        if not admin:
            # Hash password
            hashed_password = bcrypt.hashpw(
                'admin123'.encode('utf-8'), bcrypt.gensalt())

            # Create admin user
            admin = User(
                name='Admin User',
                email='admin@example.com',
                password=hashed_password.decode('utf-8'),
                is_verified=True,
                is_admin=True
            )
            admin.save()
            print("Admin user created successfully")
        else:
            print("Admin user already exists")
    except Exception as e:
        print(f"Error creating admin user: {e}")


def create_brands():
    """Create brands if they don't exist"""
    try:
        brands_data = [
            {"name": "Apple", "description": "American technology company"},
            {"name": "Samsung", "description": "South Korean electronics company"},
            {"name": "Nike", "description": "American sportswear company"},
            {"name": "Adidas", "description": "German sportswear company"},
            {"name": "Sony", "description": "Japanese electronics company"}
        ]

        for brand_data in brands_data:
            brand = Brand.objects(name=brand_data['name']).first()
            if not brand:
                Brand(**brand_data).save()
                print(f"Brand '{brand_data['name']}' created")
            else:
                print(f"Brand '{brand_data['name']}' already exists")
    except Exception as e:
        print(f"Error creating brands: {e}")


def create_categories():
    """Create categories if they don't exist"""
    try:
        categories_data = [
            {"name": "Electronics", "description": "Electronic devices and accessories"},
            {"name": "Clothing", "description": "Apparel and fashion items"},
            {"name": "Books", "description": "Books and literature"},
            {"name": "Home & Kitchen",
                "description": "Home and kitchen appliances and accessories"},
            {"name": "Sports", "description": "Sports equipment and accessories"}
        ]

        for category_data in categories_data:
            category = Category.objects(name=category_data['name']).first()
            if not category:
                Category(**category_data).save()
                print(f"Category '{category_data['name']}' created")
            else:
                print(f"Category '{category_data['name']}' already exists")
    except Exception as e:
        print(f"Error creating categories: {e}")


def create_products():
    """Create sample products if they don't exist"""
    try:
        # Get brands and categories
        apple = Brand.objects(name="Apple").first()
        samsung = Brand.objects(name="Samsung").first()
        electronics = Category.objects(name="Electronics").first()

        if not apple or not samsung or not electronics:
            print("Required brands or categories not found")
            return

        products_data = [
            {
                "title": "iPhone 13",
                "description": "Latest iPhone model with A15 Bionic chip",
                "price": 999.99,
                "discounted_price": 899.99,
                "stock": 50,
                "brand": apple,
                "category": electronics,
                "image_url": "https://example.com/iphone13.jpg"
            },
            {
                "title": "Samsung Galaxy S21",
                "description": "Flagship Samsung smartphone with 5G support",
                "price": 899.99,
                "discounted_price": 849.99,
                "stock": 40,
                "brand": samsung,
                "category": electronics,
                "image_url": "https://example.com/galaxys21.jpg"
            },
            {
                "title": "MacBook Pro",
                "description": "Powerful laptop for professionals",
                "price": 1499.99,
                "stock": 30,
                "brand": apple,
                "category": electronics,
                "image_url": "https://example.com/macbookpro.jpg"
            }
        ]

        for product_data in products_data:
            product = Product.objects(title=product_data['title']).first()
            if not product:
                Product(**product_data).save()
                print(f"Product '{product_data['title']}' created")
            else:
                print(f"Product '{product_data['title']}' already exists")
    except Exception as e:
        print(f"Error creating products: {e}")


if __name__ == "__main__":
    print("Starting database seed process...")
    create_admin_user()
    create_brands()
    create_categories()
    create_products()
    print("Database seed completed")

    # Clean up
    app_context.pop()
