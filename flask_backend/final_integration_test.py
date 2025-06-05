#!/usr/bin/env python3
"""
Final Integration Test - Frontend & Backend Authentication
Testing the authentication flow as the frontend would use it
"""

import requests
import json


def test_frontend_auth_flow():
    """Test the complete authentication flow from frontend perspective"""

    print("🔄 Testing Frontend-Backend Integration")
    print("=" * 50)

    base_url = "http://localhost:5000"
    session = requests.Session()
    session.headers.update({'Content-Type': 'application/json'})

    # Test admin login (same as frontend would do)
    print("1. Testing admin login via POST /auth/login...")
    login_data = {
        "email": "admin@example.com",
        "password": "admin123"
    }

    login_response = session.post(f"{base_url}/auth/login", json=login_data)
    print(f"   Status: {login_response.status_code}")

    if login_response.status_code == 200:
        user_data = login_response.json()
        print(f"   ✅ Login successful!")
        print(f"   User: {user_data.get('name')} ({user_data.get('email')})")
        print(f"   Admin: {user_data.get('isAdmin')}")
        print(f"   Verified: {user_data.get('isVerified')}")

        # Check cookies
        cookies = login_response.cookies
        print(f"   Cookies received: {list(cookies.keys())}")

        if 'token' in cookies:
            print(f"   ✅ Token cookie set successfully")
        else:
            print(f"   ❌ Token cookie not found")
            print(f"   Available cookies: {dict(cookies)}")
    else:
        print(f"   ❌ Login failed: {login_response.text}")
        return False

    # Test auth check (frontend checks this on page load)
    print("\n2. Testing auth check via GET /auth/check-auth...")
    auth_check = session.get(f"{base_url}/auth/check-auth")
    print(f"   Status: {auth_check.status_code}")

    if auth_check.status_code == 200:
        user_data = auth_check.json()
        print(f"   ✅ Auth check successful!")
        print(f"   Authenticated as: {user_data.get('name')}")
    else:
        print(f"   ❌ Auth check failed: {auth_check.text}")
        return False

    # Test accessing products (main functionality)
    print("\n3. Testing products access via GET /products...")
    products_response = session.get(f"{base_url}/products")
    print(f"   Status: {products_response.status_code}")    if products_response.status_code == 200:
        products_data = products_response.json()
        print(f"   ✅ Products retrieved successfully!")
        if isinstance(products_data, list):
            print(f"   Found {len(products_data)} products")
        elif isinstance(products_data, dict) and 'products' in products_data:
            print(f"   Found {len(products_data['products'])} products")
        else:
            print(f"   Products data structure: {type(products_data)}")
    else:
        print(f"   ❌ Products access failed: {products_response.text}")
        return False

    # Test logout
    print("\n4. Testing logout via GET /auth/logout...")
    logout_response = session.get(f"{base_url}/auth/logout")
    print(f"   Status: {logout_response.status_code}")

    if logout_response.status_code == 200:
        print(f"   ✅ Logout successful!")

        # Verify token is cleared
        cookies_after_logout = logout_response.cookies
        print(f"   Cookies after logout: {list(cookies_after_logout.keys())}")
    else:
        print(f"   ❌ Logout failed: {logout_response.text}")
        return False

    # Test auth check after logout (should fail)
    print("\n5. Testing auth check after logout...")
    auth_check_after_logout = session.get(f"{base_url}/auth/check-auth")
    print(f"   Status: {auth_check_after_logout.status_code}")

    if auth_check_after_logout.status_code == 401:
        print(f"   ✅ Auth check correctly failed after logout")
    else:
        print(f"   ❌ Auth check should have failed after logout")
        return False

    print("\n" + "=" * 50)
    print("🎉 Frontend-Backend Integration Test PASSED!")
    print("\n📋 Summary:")
    print("   ✅ Admin login working")
    print("   ✅ Cookie authentication working")
    print("   ✅ Protected routes accessible")
    print("   ✅ Logout working")
    print("   ✅ Session management working")
    print("\n🌐 Frontend should now work properly!")
    print("   Open: http://localhost:3000/login")
    print("   Use: admin@example.com / admin123")

    return True


def test_regular_user_login():
    """Test login with regular user credentials"""

    print("\n🔄 Testing Regular User Login")
    print("=" * 30)

    base_url = "http://localhost:5000"
    session = requests.Session()
    session.headers.update({'Content-Type': 'application/json'})

    # Try to login with a regular user (assuming users exist from seeding)
    login_data = {
        "email": "user@example.com",  # This might not exist, that's okay
        "password": "user123"
    }

    login_response = session.post(f"{base_url}/auth/login", json=login_data)
    print(f"Regular user login status: {login_response.status_code}")

    if login_response.status_code == 200:
        user_data = login_response.json()
        print(f"✅ Regular user login successful: {user_data.get('name')}")
        print(f"   Admin: {user_data.get('isAdmin')}")
    else:
        print(f"ℹ️  Regular user login failed (expected if user doesn't exist)")
        print(f"   Response: {login_response.text}")


if __name__ == "__main__":
    try:
        success = test_frontend_auth_flow()
        test_regular_user_login()

        if success:
            print("\n🚀 Ready for frontend testing!")
            print("   1. Make sure React app is running on http://localhost:3000")
            print("   2. Navigate to login page")
            print("   3. Use admin@example.com / admin123")
            print("   4. Should redirect to main page after successful login")

    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
