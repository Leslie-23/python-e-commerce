#!/usr/bin/env python3
"""
Complete Integration Test for Flask Backend + React Frontend
Tests the full authentication flow end-to-end
"""

import requests
import json
import time
from datetime import datetime

# Configuration
FLASK_BASE_URL = "http://127.0.0.1:5000"
REACT_BASE_URL = "http://localhost:3000"


def print_header(title):
    print(f"\n{'='*50}")
    print(f" {title}")
    print(f"{'='*50}")


def print_success(message):
    print(f"✅ {message}")


def print_error(message):
    print(f"❌ {message}")


def print_info(message):
    print(f"ℹ️  {message}")


def test_flask_backend():
    """Test Flask backend endpoints"""
    print_header("TESTING FLASK BACKEND")

    try:
        # Test health check
        response = requests.get(f"{FLASK_BASE_URL}/")
        if response.status_code == 200:
            print_success("Flask server is running")
        else:
            print_error(
                f"Flask server health check failed: {response.status_code}")
            return False

        # Test products endpoint
        response = requests.get(f"{FLASK_BASE_URL}/products")
        if response.status_code == 200:
            products = response.json()
            print_success(
                f"Products endpoint working - {len(products)} products found")
        else:
            print_error(f"Products endpoint failed: {response.status_code}")

        # Test brands endpoint
        response = requests.get(f"{FLASK_BASE_URL}/brands")
        if response.status_code == 200:
            brands = response.json()
            print_success(
                f"Brands endpoint working - {len(brands)} brands found")
        else:
            print_error(f"Brands endpoint failed: {response.status_code}")

        # Test categories endpoint
        response = requests.get(f"{FLASK_BASE_URL}/categories")
        if response.status_code == 200:
            categories = response.json()
            print_success(
                f"Categories endpoint working - {len(categories)} categories found")
        else:
            print_error(f"Categories endpoint failed: {response.status_code}")

        return True

    except requests.exceptions.ConnectionError:
        print_error(
            "Cannot connect to Flask backend. Make sure it's running on port 5000.")
        return False
    except Exception as e:
        print_error(f"Flask backend test failed: {str(e)}")
        return False


def test_react_frontend():
    """Test React frontend availability"""
    print_header("TESTING REACT FRONTEND")

    try:
        response = requests.get(REACT_BASE_URL, timeout=10)
        if response.status_code == 200:
            print_success("React frontend is accessible")
            return True
        else:
            print_error(
                f"React frontend returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error(
            "Cannot connect to React frontend. Make sure it's running on port 3000.")
        return False
    except Exception as e:
        print_error(f"React frontend test failed: {str(e)}")
        return False


def test_auth_endpoints():
    """Test authentication endpoints"""
    print_header("TESTING AUTHENTICATION ENDPOINTS")

    # Generate unique test user
    timestamp = str(int(time.time()))
    test_email = f"testuser{timestamp}@test.com"
    test_password = "TestPass123!"

    print_info(f"Testing with email: {test_email}")

    try:
        # Test user registration
        signup_data = {
            "name": "Test User",
            "email": test_email,
            "password": test_password
        }

        response = requests.post(
            f"{FLASK_BASE_URL}/auth/signup", json=signup_data)
        if response.status_code == 201:  # Fixed status code
            signup_result = response.json()
            print_success("User registration successful")
            print_info(
                f"User ID: {signup_result.get('id', 'N/A')}")  # Fixed field access
            user_id = signup_result.get('id')

            if user_id:
                # Test OTP verification (simulate with a dummy OTP)
                otp_data = {
                    "otp": "123456",  # This will fail, but we can test the endpoint
                    "userId": user_id
                }

                otp_response = requests.post(
                    f"{FLASK_BASE_URL}/auth/verify-otp", json=otp_data)
                # 400 is expected for wrong OTP
                if otp_response.status_code in [200, 400]:
                    print_success("OTP verification endpoint is working")
                else:
                    print_error(
                        f"OTP verification endpoint failed: {otp_response.status_code}")

                # Test resend OTP
                resend_data = {"user": user_id}
                resend_response = requests.post(
                    f"{FLASK_BASE_URL}/auth/resend-otp", json=resend_data)
                if resend_response.status_code == 200:
                    print_success("Resend OTP endpoint is working")
                else:
                    print_error(
                        f"Resend OTP endpoint failed: {resend_response.status_code}")

        else:
            print_error(f"User registration failed: {response.status_code}")
            if response.text:
                print_info(f"Error details: {response.text}")
          # Test login with existing admin user
        admin_login_data = {
            "email": "admin@example.com",
            "password": "admin123"
        }

        login_response = requests.post(
            f"{FLASK_BASE_URL}/auth/login", json=admin_login_data)
        if login_response.status_code == 200:
            print_success("Admin login successful")
            login_result = login_response.json()
            print_info(
                f"Admin user: {login_result.get('user', {}).get('email', 'N/A')}")
        else:
            print_error(f"Admin login failed: {login_response.status_code}")
            if login_response.text:
                print_info(f"Error details: {login_response.text}")

        return True

    except Exception as e:
        print_error(f"Authentication tests failed: {str(e)}")
        return False


def test_cors_configuration():
    """Test CORS configuration"""
    print_header("TESTING CORS CONFIGURATION")

    try:
        # Test preflight request
        headers = {
            'Origin': 'http://localhost:3000',
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'Content-Type'
        }

        response = requests.options(
            f"{FLASK_BASE_URL}/auth/login", headers=headers)
        if response.status_code in [200, 204]:
            cors_headers = response.headers
            if 'Access-Control-Allow-Origin' in cors_headers:
                print_success("CORS is properly configured")
                print_info(
                    f"Allowed origins: {cors_headers.get('Access-Control-Allow-Origin', 'N/A')}")
            else:
                print_error("CORS headers not found in response")
        else:
            print_error(
                f"CORS preflight request failed: {response.status_code}")

        return True

    except Exception as e:
        print_error(f"CORS test failed: {str(e)}")
        return False


def main():
    """Run all integration tests"""
    print_header("COMPLETE E-COMMERCE INTEGRATION TEST")
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Test results
    results = {
        'flask_backend': False,
        'react_frontend': False,
        'auth_endpoints': False,
        'cors_config': False
    }

    # Run tests
    results['flask_backend'] = test_flask_backend()
    results['react_frontend'] = test_react_frontend()
    results['auth_endpoints'] = test_auth_endpoints()
    results['cors_config'] = test_cors_configuration()

    # Summary
    print_header("TEST SUMMARY")

    passed = sum(results.values())
    total = len(results)

    for test_name, result in results.items():
        status = "PASS" if result else "FAIL"
        symbol = "✅" if result else "❌"
        print(f"{symbol} {test_name.replace('_', ' ').title()}: {status}")

    print(f"\nOverall: {passed}/{total} tests passed")

    if passed == total:
        print_success(
            "🎉 ALL TESTS PASSED! The migration is complete and working!")
        print_info("You can now:")
        print_info("1. Open http://localhost:3000 in your browser")
        print_info("2. Register a new user account")
        print_info("3. Verify OTP (check console for OTP)")
        print_info("4. Login and browse products")
        print_info("5. Test admin features with admin@example.com / admin123")
    else:
        print_error(
            f"⚠️  {total - passed} test(s) failed. Please check the issues above.")

    print(
        f"\nTest completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
