#!/usr/bin/env python3
"""
Test script to verify Flask backend API endpoints
"""
import requests
import json

BASE_URL = "http://localhost:5000"


def test_api():
    print("🧪 Testing Flask Backend API Endpoints")
    print("=" * 50)

    # Test 1: Server Status
    print("\n1. Testing server status...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✅ Server status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Server status test failed: {e}")
        return

    # Test 2: Get Products
    print("\n2. Testing products endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/products/")
        print(f"✅ Products endpoint: {response.status_code}")
        products = response.json()
        print(f"   Found {len(products)} products")
        if products:
            print(f"   Sample product: {products[0]['title']}")
    except Exception as e:
        print(f"❌ Products test failed: {e}")

    # Test 3: Get Brands
    print("\n3. Testing brands endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/brands/")
        print(f"✅ Brands endpoint: {response.status_code}")
        brands = response.json()
        print(f"   Found {len(brands)} brands")
        if brands:
            print(f"   Sample brand: {brands[0]['name']}")
    except Exception as e:
        print(f"❌ Brands test failed: {e}")

    # Test 4: Get Categories
    print("\n4. Testing categories endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/categories/")
        print(f"✅ Categories endpoint: {response.status_code}")
        categories = response.json()
        print(f"   Found {len(categories)} categories")
        if categories:
            print(f"   Sample category: {categories[0]['name']}")
    except Exception as e:
        print(f"❌ Categories test failed: {e}")

    # Test 5: Admin Login
    print("\n5. Testing admin login...")
    try:
        login_data = {
            "email": "admin@example.com",
            "password": "admin123"
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        print(f"✅ Admin login: {response.status_code}")
        if response.status_code == 200:
            admin_data = response.json()
            print(
                f"   Admin user: {admin_data['name']} ({admin_data['email']})")
            print(f"   Is admin: {admin_data['is_admin']}")
        else:
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Admin login test failed: {e}")

    # Test 6: User Registration
    print("\n6. Testing user registration...")
    try:
        user_data = {
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "testpass123"
        }
        response = requests.post(f"{BASE_URL}/auth/signup", json=user_data)
        print(f"✅ User registration: {response.status_code}")
        if response.status_code in [200, 201]:
            print("   User registered successfully")
        else:
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ User registration test failed: {e}")

    print("\n" + "=" * 50)
    print("🎉 API testing completed!")
    print("\n💡 You can now test the frontend at: http://localhost:3000")
    print("💡 Admin credentials: admin@example.com / admin123")


if __name__ == "__main__":
    test_api()
