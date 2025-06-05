#!/usr/bin/env python3
"""
Simple Flask route testing
"""

import requests
import sys

BASE_URL = "http://127.0.0.1:5007"

def test_routes():
    """Test Flask routes accessibility"""
    print("🔍 Testing Flask Routes")
    print("=" * 40)
    
    # Test main routes
    routes_to_test = [
        ("/", "Home page"),
        ("/products", "Products page"),
        ("/electronics", "Electronics page"),
        ("/toys", "Toys page"),
        ("/login/", "Login page"),
        ("/signup/", "Signup page"),
        ("/contact", "Contact page"),
        ("/analytics", "Analytics page"),
    ]
    
    session = requests.Session()
    
    for route, description in routes_to_test:
        try:
            response = session.get(f"{BASE_URL}{route}")
            if response.status_code == 200:
                print(f"✅ {description}: Status {response.status_code}")
            else:
                print(f"❌ {description}: Status {response.status_code}")
        except Exception as e:
            print(f"❌ {description}: Error - {e}")
    
    print("\n🔐 Testing Login Functionality")
    print("=" * 40)
    
    # Test admin login
    login_data = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    try:
        login_response = session.post(f"{BASE_URL}/login/", data=login_data, allow_redirects=False)
        if login_response.status_code in [200, 302]:  # 302 is redirect after successful login
            print("✅ Admin login successful")
            
            # Now test admin routes
            admin_routes = [
                ("/admin", "Admin Dashboard"),
                ("/admin/users", "Admin Users"),
                ("/admin/products", "Admin Products"),
                ("/admin/categories", "Admin Categories"),
                ("/admin/orders", "Admin Orders"),
                ("/admin/inventory", "Admin Inventory"),
                ("/admin/analytics", "Admin Analytics"),
                ("/admin/settings", "Admin Settings"),
                ("/admin/products/add", "Add Product"),
                ("/admin/categories/add", "Add Category"),
            ]
            
            print("\n🛠️ Testing Admin Routes")
            print("=" * 40)
            
            for route, description in admin_routes:
                try:
                    response = session.get(f"{BASE_URL}{route}")
                    if response.status_code == 200:
                        print(f"✅ {description}: Status {response.status_code}")
                    else:
                        print(f"❌ {description}: Status {response.status_code}")
                except Exception as e:
                    print(f"❌ {description}: Error - {e}")
                    
            # Test API routes
            print("\n🔌 Testing API Routes")
            print("=" * 40)
            
            api_routes = [
                ("/api/admin/stats", "Admin Stats API"),
                ("/api/cart/count", "Cart Count API"),
            ]
            
            for route, description in api_routes:
                try:
                    response = session.get(f"{BASE_URL}{route}")
                    if response.status_code == 200:
                        print(f"✅ {description}: Status {response.status_code}")
                        if "json" in response.headers.get('content-type', ''):
                            print(f"    Data: {response.json()}")
                    else:
                        print(f"❌ {description}: Status {response.status_code}")
                except Exception as e:
                    print(f"❌ {description}: Error - {e}")
                    
        else:
            print(f"❌ Admin login failed: Status {login_response.status_code}")
            
    except Exception as e:
        print(f"❌ Admin login error: {e}")

if __name__ == "__main__":
    test_routes()
