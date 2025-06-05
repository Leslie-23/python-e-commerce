from app.seed.seed import create_admin_user, create_brands, create_categories, create_products
import os
import sys

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '.')))

# Import and run the seed script

if __name__ == "__main__":
    print("Starting database seed process...")
    create_admin_user()
    create_brands()
    create_categories()
    create_products()
    print("Database seed completed")
