#!/usr/bin/env python3

import requests
import json
import sys


def test_auth_endpoints():
    """Test authentication endpoints to identify issues"""
    base_url = "http://localhost:5000"

    print("🔍 Testing Flask Authentication Endpoints")
    print("=" * 50)

    # Test 1: Check if Flask server is responding
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ Flask server is responding: {response.status_code}")
    except Exception as e:
        print(f"❌ Flask server is not responding: {e}")
        return

    # Test 2: Test registration endpoint
    print("\n📝 Testing Registration Endpoint")
    test_user = {
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "testpass123"
    }

    try:
        response = requests.post(f"{base_url}/auth/signup",
                                 json=test_user,
                                 headers={'Content-Type': 'application/json'})
        print(f"Registration Response Status: {response.status_code}")
        print(f"Registration Response Headers: {dict(response.headers)}")
        print(f"Registration Response Body: {response.text}")

        if response.status_code == 201:
            print("✅ Registration successful")
        else:
            print("❌ Registration failed")
    except Exception as e:
        print(f"❌ Registration request failed: {e}")

    # Test 3: Test login endpoint
    print("\n🔐 Testing Login Endpoint")
    login_creds = {
        "email": "admin@example.com",
        "password": "admin123"
    }

    try:
        response = requests.post(f"{base_url}/auth/login",
                                 json=login_creds,
                                 headers={'Content-Type': 'application/json'})
        print(f"Login Response Status: {response.status_code}")
        print(f"Login Response Headers: {dict(response.headers)}")
        print(f"Login Response Body: {response.text}")

        if response.status_code == 200:
            print("✅ Login successful")

            # Test check-auth with cookies
            print("\n🔍 Testing Check Auth with Cookies")
            cookies = response.cookies
            auth_response = requests.get(
                f"{base_url}/auth/check-auth", cookies=cookies)
            print(f"Check Auth Status: {auth_response.status_code}")
            print(f"Check Auth Body: {auth_response.text}")
        else:
            print("❌ Login failed")
    except Exception as e:
        print(f"❌ Login request failed: {e}")

    # Test 4: Test CORS headers
    print("\n🌐 Testing CORS Headers")
    try:
        response = requests.options(f"{base_url}/auth/login",
                                    headers={
                                        'Origin': 'http://localhost:3000',
                                        'Access-Control-Request-Method': 'POST',
                                        'Access-Control-Request-Headers': 'Content-Type'
                                    })
        print(f"CORS Preflight Status: {response.status_code}")
        print(f"CORS Headers: {dict(response.headers)}")
    except Exception as e:
        print(f"❌ CORS request failed: {e}")


if __name__ == "__main__":
    test_auth_endpoints()
