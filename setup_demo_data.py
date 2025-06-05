#!/usr/bin/env python3
"""
Demo Data Setup Script for E-commerce Website
This script populates the database with sample data for testing
"""

import sys
import os
import hashlib
from datetime import date, datetime, timedelta

# Add the parent directory to the path so we can import from webapp
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from webapp.dbaccess import (
    get_mysql_connection, 
    add_user, 
    add_category, 
    add_new_product
)
from werkzeug.security import generate_password_hash

def create_demo_admin_user():
    """Create a demo admin user"""
    try:
        conn = get_mysql_connection()
        cur = conn.cursor()
        
        # Check if admin already exists
        cur.execute("SELECT user_id FROM registered_user WHERE email = %s", ('admin@ecommerce.com',))
        if cur.fetchone():
            print("Admin user already exists")
            return
        
        # Create admin user with existing schema
        admin_data = {
            'email': 'admin@ecommerce.com',
            'username': 'admin',
            'password': 'admin123'
        }
        
        hashed_password = generate_password_hash(admin_data['password'])
        
        # Get a new user ID
        from webapp.dbaccess import gen_custID
        user_id = gen_custID()
        
        query = """
        INSERT INTO registered_user (user_id, email, password, username)
        VALUES (%s, %s, %s, %s)
        """
        
        cur.execute(query, (
            user_id,
            admin_data['email'],
            hashed_password,
            admin_data['username']
        ))
        
        conn.commit()
        print("✅ Admin user created successfully!")
        print("   Username: admin")
        print("   Password: admin123")
        print("   Email: admin@ecommerce.com")
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        conn.rollback()
    finally:
        conn.close()

def create_demo_categories():
    """Create demo categories"""
    categories = [
        {'category_name': 'Electronics', 'parent_category_id': None},
        {'category_name': 'Toys', 'parent_category_id': None},
        {'category_name': 'Books', 'parent_category_id': None},
        {'category_name': 'Clothing', 'parent_category_id': None},
        {'category_name': 'Home & Garden', 'parent_category_id': None}
    ]
    
    try:
        conn = get_mysql_connection()
        cur = conn.cursor()
        
        for category in categories:
            # Check if category exists
            cur.execute("SELECT category_id FROM category WHERE category_name = %s", (category['category_name'],))
            if not cur.fetchone():
                # Get next category ID
                cur.execute("SELECT MAX(category_id) FROM category")
                max_id = cur.fetchone()[0]
                new_id = (max_id + 1) if max_id else 1
                
                query = """
                INSERT INTO category (category_id, category_name, parent_category_id)
                VALUES (%s, %s, %s)
                """
                cur.execute(query, (new_id, category['category_name'], category['parent_category_id']))
                print(f"✅ Created category: {category['category_name']}")
        
        conn.commit()
        
    except Exception as e:
        print(f"❌ Error creating categories: {e}")
        conn.rollback()
    finally:
        conn.close()

def create_demo_products():
    """Create demo products"""
    try:
        conn = get_mysql_connection()
        cur = conn.cursor()
          # Get category IDs
        cur.execute("SELECT category_id, category_name FROM category")
        categories = dict(cur.fetchall())
        category_lookup = {v: k for k, v in categories.items()}
        
        products = [
            {
                'title': 'iPhone 14 Pro',
                'description': 'Latest iPhone with advanced camera system',
                'category': 'Electronics',
                'weight': 0.2,
                'product_image': 'product-images/iphone_14.png'
            },
            {
                'title': 'Samsung Galaxy S23',
                'description': 'Premium Android smartphone',
                'category': 'Electronics',
                'weight': 0.19,
                'product_image': 'product-images/galaxy_s23.png'
            },
            {
                'title': 'LEGO Creator Set',
                'description': 'Build amazing creations with this LEGO set',
                'category': 'Toys',
                'weight': 1.2,
                'product_image': 'product-images/lego_creator.png'
            },
            {
                'title': 'Python Programming Book',
                'description': 'Learn Python programming from scratch',
                'category': 'Books',
                'weight': 0.8,
                'product_image': 'product-images/python_book.png'
            },
            {
                'title': 'Cotton T-Shirt',
                'description': 'Comfortable cotton t-shirt in various colors',
                'category': 'Clothing',
                'weight': 0.3,
                'product_image': 'product-images/tshirt.png'
            }
        ]
        
        for product in products:
            # Check if product exists
            cur.execute("SELECT product_id FROM product WHERE title = %s", (product['title'],))
            if not cur.fetchone():
                category_id = category_lookup.get(product['category'])
                if category_id:
                    # Get next product ID
                    cur.execute("SELECT MAX(product_id) FROM product")
                    max_id = cur.fetchone()[0]
                    new_id = (max_id + 1) if max_id else 1
                    
                    query = """
                    INSERT INTO product (product_id, title, description, weight, category_id, product_image)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    cur.execute(query, (
                        new_id,
                        product['title'],
                        product['description'],
                        product['weight'],
                        category_id,
                        product['product_image']
                    ))                    
                    # Add a default variant
                    cur.execute("SELECT MAX(variant_id) FROM variant")
                    max_variant_id = cur.fetchone()[0]
                    new_variant_id = (max_variant_id + 1) if max_variant_id else 1
                    
                    variant_query = """
                    INSERT INTO variant (variant_id, product_id, name, price, variant_image)
                    VALUES (%s, %s, %s, %s, %s)
                    """
                    cur.execute(variant_query, (
                        new_variant_id,
                        new_id,
                        'Default',
                        99.99,
                        product['product_image']
                    ))
                    
                    # Add inventory
                    inventory_query = """
                    INSERT INTO inventory (variant_id, stock_count)
                    VALUES (%s, %s)
                    """
                    cur.execute(inventory_query, (new_variant_id, 50))
                    
                    print(f"✅ Created product: {product['title']}")
        
        conn.commit()
        
    except Exception as e:
        print(f"❌ Error creating products: {e}")
        conn.rollback()
    finally:
        conn.close()

def create_demo_user():
    """Create a demo regular user"""
    try:
        conn = get_mysql_connection()
        cur = conn.cursor()
        
        # Check if user already exists
        cur.execute("SELECT user_id FROM registered_user WHERE email = %s", ('user@example.com',))
        if cur.fetchone():
            print("Demo user already exists")
            return
        
        # Create demo user with existing schema
        user_data = {
            'email': 'user@example.com',
            'username': 'johndoe',
            'password': 'user123'
        }
        
        hashed_password = generate_password_hash(user_data['password'])
        
        # Get a new user ID
        from webapp.dbaccess import gen_custID
        user_id = gen_custID()
        
        query = """
        INSERT INTO registered_user (user_id, email, password, username)
        VALUES (%s, %s, %s, %s)
        """
        
        cur.execute(query, (
            user_id,
            user_data['email'],
            hashed_password,
            user_data['username']
        ))
        
        conn.commit()
        print("✅ Demo user created successfully!")
        print("   Username: johndoe")
        print("   Password: user123")
        print("   Email: user@example.com")
        
    except Exception as e:
        print(f"❌ Error creating demo user: {e}")
        conn.rollback()
    finally:
        conn.close()

def main():
    """Main function to set up demo data"""
    print("🚀 Setting up demo data for E-commerce Website...")
    print("=" * 50)
    
    create_demo_admin_user()
    create_demo_user()
    create_demo_categories()
    create_demo_products()
    
    print("\n" + "=" * 50)
    print("✅ Demo data setup completed!")
    print("\n📋 Login Credentials:")
    print("   👨‍💼 Admin:")
    print("      Username: admin")
    print("      Password: admin123")
    print("   👤 User:")
    print("      Username: johndoe")
    print("      Password: user123")
    print("\n🌐 Visit: http://127.0.0.1:5007")

if __name__ == "__main__":
    main()
