#!/usr/bin/env python3
"""
Quick Login Test - Just test the essential login functionality
"""

import requests
import json


def test_login():
    """Test basic login functionality"""

    print("🔄 Testing Login Functionality")
    print("=" * 30)

    base_url = "http://localhost:5000"
    session = requests.Session()
    session.headers.update({'Content-Type': 'application/json'})

    # Test admin login
    print("1. Testing admin login...")
    login_data = {
        "email": "admin@example.com",
        "password": "admin123"
    }

    try:
        login_response = session.post(
            f"{base_url}/auth/login", json=login_data)
        print(f"   Status: {login_response.status_code}")

        if login_response.status_code == 200:
            user_data = login_response.json()
            print(f"   ✅ Login successful!")
            print(
                f"   User: {user_data.get('name')} ({user_data.get('email')})")
            print(f"   Admin: {user_data.get('isAdmin')}")
            print(f"   Verified: {user_data.get('isVerified')}")

            # Check cookies
            cookies = login_response.cookies
            if 'token' in cookies:
                print(f"   ✅ Token cookie set successfully")
            else:
                print(f"   ❌ Token cookie not found")

            # Test auth check
            print("\n2. Testing auth check...")
            auth_check = session.get(f"{base_url}/auth/check-auth")
            if auth_check.status_code == 200:
                print(f"   ✅ Auth check successful!")
            else:
                print(f"   ❌ Auth check failed")

            # Test products access
            print("\n3. Testing products access...")
            products_response = session.get(f"{base_url}/products")
            if products_response.status_code == 200:
                products_data = products_response.json()
                if isinstance(products_data, list):
                    print(
                        f"   ✅ Products retrieved: {len(products_data)} items")
                else:
                    print(f"   ✅ Products retrieved: {type(products_data)}")
            else:
                print(f"   ❌ Products access failed")

            print("\n🎉 Authentication is working!")
            print("Frontend should be able to login successfully now.")
            return True

        else:
            print(f"   ❌ Login failed: {login_response.text}")
            return False

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


if __name__ == "__main__":
    test_login()
