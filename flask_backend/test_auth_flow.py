#!/usr/bin/env python3
"""
Test script to verify frontend-backend authentication integration
"""
import requests
import json

BASE_URL = "http://localhost:5000"


def test_authentication_flow():
    print("🔐 Testing Authentication Flow")
    print("=" * 50)

    # Create a session to maintain cookies
    session = requests.Session()

    # Test 1: Login
    print("\n1. Testing login...")
    try:
        login_data = {
            "email": "admin@example.com",
            "password": "admin123"
        }
        response = session.post(f"{BASE_URL}/auth/login", json=login_data)
        print(f"✅ Login status: {response.status_code}")

        if response.status_code == 200:
            user_data = response.json()
            print(f"   User: {user_data['name']} ({user_data['email']})")
            print(f"   Admin: {user_data['is_admin']}")

            # Check if cookie was set
            cookies = session.cookies.get_dict()
            if 'token' in cookies:
                print(f"   ✅ Token cookie set successfully")
            else:
                print(f"   ❌ No token cookie found")
                print(f"   Available cookies: {list(cookies.keys())}")
        else:
            print(f"   ❌ Login failed: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Login test failed: {e}")
        return False

    # Test 2: Check Auth (using the session with cookies)
    print("\n2. Testing auth check...")
    try:
        response = session.get(f"{BASE_URL}/auth/check-auth")
        print(f"✅ Auth check status: {response.status_code}")

        if response.status_code == 200:
            user_data = response.json()
            print(f"   Authenticated as: {user_data['name']}")
        else:
            print(f"   ❌ Auth check failed: {response.text}")

    except Exception as e:
        print(f"❌ Auth check test failed: {e}")

    # Test 3: Access Protected Resource
    print("\n3. Testing protected resource access...")
    try:
        response = session.get(f"{BASE_URL}/products/")
        print(f"✅ Products access status: {response.status_code}")

        if response.status_code == 200:
            products = response.json()
            print(f"   Retrieved {len(products)} products while authenticated")
        else:
            print(f"   ❌ Failed to access products: {response.text}")

    except Exception as e:
        print(f"❌ Protected resource test failed: {e}")

    # Test 4: Logout
    print("\n4. Testing logout...")
    try:
        response = session.get(f"{BASE_URL}/auth/logout")
        print(f"✅ Logout status: {response.status_code}")

        if response.status_code == 200:
            print(f"   Logout successful")

            # Check if cookie was cleared
            cookies = session.cookies.get_dict()
            print(f"   Remaining cookies: {list(cookies.keys())}")
        else:
            print(f"   ❌ Logout failed: {response.text}")

    except Exception as e:
        print(f"❌ Logout test failed: {e}")

    print("\n" + "=" * 50)
    print("🎉 Authentication flow testing completed!")
    return True


def test_frontend_compatible_endpoints():
    print("\n🌐 Testing Frontend-Compatible Endpoints")
    print("=" * 50)

    endpoints = [
        ("GET", "/", "Root endpoint"),
        ("GET", "/products/", "Products list"),
        ("GET", "/brands/", "Brands list"),
        ("GET", "/categories/", "Categories list"),
    ]

    for method, endpoint, description in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}")
            status = "✅" if response.status_code == 200 else "❌"
            print(f"{status} {description}: {response.status_code}")
        except Exception as e:
            print(f"❌ {description}: {e}")


if __name__ == "__main__":
    test_authentication_flow()
    test_frontend_compatible_endpoints()
    print("\n💡 Now test the login form at: http://localhost:3000/login")
    print("💡 Admin credentials: admin@example.com / admin123")
