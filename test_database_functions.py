#!/usr/bin/env python3
"""
Direct database function testing for admin features
"""

import sys
sys.path.append('c:/Users/Marvel/python-e-commerce')

from webapp.dbaccess import *
from webapp.databaseConfig import database_connector

def test_admin_database_functions():
    """Test all admin database functions"""
    print("🔍 Testing Admin Database Functions")
    print("=" * 50)
    
    # Test admin stats
    try:
        stats = get_admin_stats()
        print(f"✅ get_admin_stats(): {stats}")
    except Exception as e:
        print(f"❌ get_admin_stats() failed: {e}")
        
    # Test get all users
    try:
        users = get_all_users()
        print(f"✅ get_all_users(): Found {len(users)} users")
    except Exception as e:
        print(f"❌ get_all_users() failed: {e}")
        
    # Test get all products for admin
    try:
        products = get_all_products_admin()
        print(f"✅ get_all_products_admin(): Found {len(products)} products")
    except Exception as e:
        print(f"❌ get_all_products_admin() failed: {e}")
        
    # Test get all categories
    try:
        categories = get_all_categories()
        print(f"✅ get_all_categories(): Found {len(categories)} categories")
    except Exception as e:
        print(f"❌ get_all_categories() failed: {e}")
        
    # Test categories with stats
    try:
        cat_stats = get_all_categories_with_stats()
        print(f"✅ get_all_categories_with_stats(): Found {len(cat_stats)} categories with stats")
    except Exception as e:
        print(f"❌ get_all_categories_with_stats() failed: {e}")
        
    # Test recent orders
    try:
        orders = get_recent_orders(limit=5)
        print(f"✅ get_recent_orders(): Found {len(orders)} recent orders")
    except Exception as e:
        print(f"❌ get_recent_orders() failed: {e}")
        
    # Test paginated orders
    try:
        orders_paginated = get_all_orders_paginated(page=1, per_page=10)
        print(f"✅ get_all_orders_paginated(): Found {len(orders_paginated)} orders")
    except Exception as e:
        print(f"❌ get_all_orders_paginated() failed: {e}")
        
    # Test inventory overview
    try:
        inventory = get_inventory_overview()
        print(f"✅ get_inventory_overview(): Found {len(inventory)} inventory items")
    except Exception as e:
        print(f"❌ get_inventory_overview() failed: {e}")
        
    # Test low stock items
    try:
        low_stock = get_low_stock_items(threshold=10)
        print(f"✅ get_low_stock_items(): Found {len(low_stock)} low stock items")
    except Exception as e:
        print(f"❌ get_low_stock_items() failed: {e}")
        
    # Test user profile functions
    try:
        user_profile = get_user_profile(10024)  # Admin user ID
        print(f"✅ get_user_profile(): Retrieved profile for admin user")
    except Exception as e:
        print(f"❌ get_user_profile() failed: {e}")
        
    # Test user role function
    try:
        role = get_user_role(10024)
        print(f"✅ get_user_role(): Admin user role is '{role}'")
    except Exception as e:
        print(f"❌ get_user_role() failed: {e}")
        
    print("=" * 50)
    print("✅ Database function testing complete!")

def test_sample_data():
    """Test if sample data is properly loaded"""
    print("\n🔍 Verifying Sample Data")
    print("=" * 30)
    
    # Check users
    users = get_all_users()
    print(f"Total users: {len(users)}")
    
    # Check categories
    categories = get_all_categories()
    print(f"Total categories: {len(categories)}")
    for cat in categories[:5]:  # Show first 5
        print(f"  - {cat}")
        
    # Check products
    products = get_all_products_admin()
    print(f"Total products: {len(products)}")
    
    # Check inventory
    inventory = get_inventory_overview()
    print(f"Total inventory entries: {len(inventory)}")

if __name__ == "__main__":
    database_connector()
    test_admin_database_functions()
    test_sample_data()
