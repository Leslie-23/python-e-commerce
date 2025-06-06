#!/usr/bin/env python3

import requests
import json
import time


def test_complete_flow():
    """Test the complete authentication flow end-to-end"""
    base_url = "http://localhost:5000"
    frontend_url = "http://localhost:3000"

    print("🧪 Testing Complete Frontend-Backend Integration")
    print("=" * 60)

    # Test 1: Check if both servers are running
    print("\n🔍 Step 1: Checking Server Status")
    try:
        flask_response = requests.get(base_url, timeout=5)
        print(f"✅ Flask server responding: {flask_response.status_code}")
    except Exception as e:
        print(f"❌ Flask server not responding: {e}")
        return

    try:
        frontend_response = requests.get(frontend_url, timeout=5)
        print(f"✅ Frontend server responding: {frontend_response.status_code}")
    except Exception as e:
        print(f"❌ Frontend server not responding: {e}")
        return

    # Test 2: Test CORS configuration
    print("\n🌐 Step 2: Testing CORS Configuration")
    cors_headers = {
        'Origin': frontend_url,
        'Access-Control-Request-Method': 'POST',
        'Access-Control-Request-Headers': 'Content-Type'
    }

    try:
        cors_response = requests.options(
            f"{base_url}/auth/login", headers=cors_headers, timeout=5)
        print(f"CORS Preflight Status: {cors_response.status_code}")

        cors_response_headers = dict(cors_response.headers)
        print(
            f"CORS Origin: {cors_response_headers.get('Access-Control-Allow-Origin', 'NOT SET')}")
        print(
            f"CORS Credentials: {cors_response_headers.get('Access-Control-Allow-Credentials', 'NOT SET')}")
        print(
            f"CORS Methods: {cors_response_headers.get('Access-Control-Allow-Methods', 'NOT SET')}")

        if cors_response_headers.get('Access-Control-Allow-Origin') == frontend_url:
            print("✅ CORS configured correctly")
        else:
            print("❌ CORS not configured for frontend URL")
    except Exception as e:
        print(f"❌ CORS test failed: {e}")

    # Test 3: Test registration with new user
    print("\n📝 Step 3: Testing User Registration")
    test_user = {
        "name": f"Test User {int(time.time())}",
        "email": f"testuser{int(time.time())}@example.com",
        "password": "TestPass123"
    }

    try:
        headers = {
            'Content-Type': 'application/json',
            'Origin': frontend_url
        }

        signup_response = requests.post(
            f"{base_url}/auth/signup",
            json=test_user,
            headers=headers,
            timeout=10
        )

        print(f"Registration Status: {signup_response.status_code}")
        print(f"Registration Response: {signup_response.text}")

        if signup_response.status_code == 201:
            print("✅ Registration successful")
            user_data = signup_response.json()
            user_id = user_data.get('id')

            # Test OTP flow
            print("\n📧 Step 4: Testing OTP Flow")
            otp_data = {"user": user_id}

            otp_response = requests.post(
                f"{base_url}/auth/resend-otp",
                json=otp_data,
                headers=headers,
                timeout=10
            )

            print(f"OTP Request Status: {otp_response.status_code}")
            print(f"OTP Response: {otp_response.text}")

            if otp_response.status_code == 200:
                print("✅ OTP generation successful")
            else:
                print("❌ OTP generation failed")

        else:
            print("❌ Registration failed")

    except Exception as e:
        print(f"❌ Registration test failed: {e}")

    # Test 4: Test admin login
    print("\n🔐 Step 5: Testing Admin Login")
    admin_creds = {
        "email": "admin@example.com",
        "password": "admin123"
    }

    try:
        login_response = requests.post(
            f"{base_url}/auth/login",
            json=admin_creds,
            headers=headers,
            timeout=10
        )

        print(f"Login Status: {login_response.status_code}")
        print(f"Login Response: {login_response.text}")

        if login_response.status_code == 200:
            print("✅ Admin login successful")

            # Check cookies
            cookies = login_response.cookies
            print(f"Cookies received: {dict(cookies)}")

            # Test protected route
            print("\n🔒 Step 6: Testing Protected Route")
            auth_response = requests.get(
                f"{base_url}/auth/check-auth",
                cookies=cookies,
                headers={'Origin': frontend_url},
                timeout=10
            )

            print(f"Auth Check Status: {auth_response.status_code}")
            print(f"Auth Check Response: {auth_response.text}")

            if auth_response.status_code == 200:
                print("✅ Authentication check successful")
            else:
                print("❌ Authentication check failed")

        else:
            print("❌ Admin login failed")

    except Exception as e:
        print(f"❌ Login test failed: {e}")

    # Test 5: Error handling
    print("\n🚨 Step 7: Testing Error Handling")
    try:
        error_response = requests.post(
            f"{base_url}/auth/login",
            json={"email": "nonexistent@example.com", "password": "wrongpass"},
            headers=headers,
            timeout=10
        )

        print(f"Error Test Status: {error_response.status_code}")
        print(f"Error Test Response: {error_response.text}")

        if error_response.status_code == 400:
            error_data = error_response.json()
            if 'message' in error_data:
                print("✅ Error handling working correctly")
            else:
                print("❌ Error response missing message field")
        else:
            print(f"❌ Unexpected error status: {error_response.status_code}")

    except Exception as e:
        print(f"❌ Error handling test failed: {e}")

    print("\n🏁 Integration Test Complete")
    print("=" * 60)


if __name__ == "__main__":
    test_complete_flow()
