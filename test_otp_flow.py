#!/usr/bin/env python3
"""
OTP Functionality Test
Tests the complete OTP verification flow with a specific email
"""

import requests
import json
import time
from datetime import datetime

# Configuration
FLASK_BASE_URL = "http://127.0.0.1:5000"
TEST_EMAIL = "codexcoder082@gmail.com"
TEST_PASSWORD = "TestPass123!"


def print_header(title):
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")


def print_success(message):
    print(f"✅ {message}")


def print_error(message):
    print(f"❌ {message}")


def print_info(message):
    print(f"ℹ️  {message}")


def print_warning(message):
    print(f"⚠️  {message}")


def test_user_signup_and_otp():
    """Test user signup and OTP verification flow"""
    print_header("TESTING OTP FUNCTIONALITY")

    print_info(f"Testing with email: {TEST_EMAIL}")
    print_info(f"Password: {TEST_PASSWORD}")

    try:
        # Step 1: User Registration
        print("\n🔸 Step 1: User Registration")
        signup_data = {
            "name": "Code Coder",
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        }

        response = requests.post(
            f"{FLASK_BASE_URL}/auth/signup", json=signup_data)

        if response.status_code == 201:
            signup_result = response.json()
            print_success("User registration successful!")
            print_info(f"User ID: {signup_result.get('id', 'N/A')}")
            print_info(f"User Name: {signup_result.get('name', 'N/A')}")
            print_info(f"User Email: {signup_result.get('email', 'N/A')}")
            print_info(
                f"Is Verified: {signup_result.get('isVerified', 'N/A')}")

            user_id = signup_result.get('id')

            if not user_id:
                print_error("No user ID returned from signup")
                return False

        elif response.status_code == 400:
            error_data = response.json()
            if "User already exists" in error_data.get('message', ''):
                print_warning(
                    "User already exists - testing with existing user")
                # Try to get user info by attempting login
                return test_existing_user_otp()
            else:
                print_error(
                    f"Signup failed: {error_data.get('message', 'Unknown error')}")
                return False
        else:
            print_error(f"Signup failed with status {response.status_code}")
            print_error(f"Response: {response.text}")
            return False

        # Step 2: Check if OTP was sent (look for console output)
        print("\n🔸 Step 2: OTP Generation")
        print_info("Check the Flask backend console for the OTP code")
        print_info(
            "The OTP should be printed like: '🔐 OTP for codexcoder082@gmail.com: 123456'")

        # Step 3: Prompt for OTP
        print("\n🔸 Step 3: OTP Verification")
        print_warning("Please check your Flask backend console for the OTP")

        # For automated testing, let's try some common test scenarios
        test_otp_scenarios = [
            {"otp": "123456", "description": "Test OTP (123456)"},
            {"otp": "000000", "description": "Invalid OTP (000000)"},
        ]

        for scenario in test_otp_scenarios:
            print(f"\n   Testing {scenario['description']}:")

            otp_data = {
                "otp": scenario["otp"],
                "userId": user_id
            }

            otp_response = requests.post(
                f"{FLASK_BASE_URL}/auth/verify-otp", json=otp_data)

            if otp_response.status_code == 200:
                otp_result = otp_response.json()
                print_success(
                    f"OTP verification successful with {scenario['otp']}!")
                print_info(
                    f"User now verified: {otp_result.get('isVerified', 'N/A')}")
                return True
            elif otp_response.status_code == 400:
                otp_error = otp_response.json()
                print_info(
                    f"OTP {scenario['otp']} failed as expected: {otp_error.get('message', 'Invalid OTP')}")
            else:
                print_error(
                    f"Unexpected OTP response status: {otp_response.status_code}")
                print_error(f"Response: {otp_response.text}")

        # Step 4: Test Resend OTP
        print("\n🔸 Step 4: Testing Resend OTP")
        resend_data = {"user": user_id}
        resend_response = requests.post(
            f"{FLASK_BASE_URL}/auth/resend-otp", json=resend_data)

        if resend_response.status_code == 200:
            print_success("Resend OTP successful!")
            print_info("Check console again for new OTP code")
        else:
            print_error(f"Resend OTP failed: {resend_response.status_code}")
            if resend_response.text:
                print_error(f"Error: {resend_response.text}")

        # Step 5: Manual OTP Input
        print("\n🔸 Step 5: Manual OTP Entry")
        print_info(
            "Now you can manually test with the actual OTP from the console")
        print_info("Copy the OTP from your Flask backend console and run:")
        print_info(f"  Test URL: POST {FLASK_BASE_URL}/auth/verify-otp")
        print_info(
            f"  Payload: {{'otp': 'ACTUAL_OTP', 'userId': '{user_id}'}}")

        return True

    except Exception as e:
        print_error(f"Test failed with error: {str(e)}")
        return False


def test_existing_user_otp():
    """Test OTP flow for existing user"""
    print_info("Testing OTP flow for existing user")

    try:
        # Try to trigger OTP resend for existing user
        # We need to get user ID first by attempting login
        login_data = {
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        }

        login_response = requests.post(
            f"{FLASK_BASE_URL}/auth/login", json=login_data)

        if login_response.status_code == 200:
            user_data = login_response.json()
            print_success("User login successful")
            print_info(
                f"User is verified: {user_data.get('isVerified', 'N/A')}")

            if user_data.get('isVerified'):
                print_success("User is already verified - no OTP needed!")
                return True
            else:
                print_info("User exists but not verified - can test OTP flow")
                user_id = user_data.get('id')
                if user_id:
                    # Trigger OTP resend
                    resend_data = {"user": user_id}
                    resend_response = requests.post(
                        f"{FLASK_BASE_URL}/auth/resend-otp", json=resend_data)

                    if resend_response.status_code == 200:
                        print_success("OTP resent! Check console for OTP code")
                        print_info(f"User ID for testing: {user_id}")
                        return True
                    else:
                        print_error(
                            f"Failed to resend OTP: {resend_response.status_code}")
                        return False

        else:
            print_error(f"Login failed: {login_response.status_code}")
            print_error(f"Response: {login_response.text}")
            return False

    except Exception as e:
        print_error(f"Existing user test failed: {str(e)}")
        return False


def test_otp_endpoints():
    """Test OTP-related endpoints"""
    print_header("TESTING OTP ENDPOINTS")

    endpoints_to_test = [
        {"url": "/auth/verify-otp", "method": "POST",
            "description": "OTP Verification"},
        {"url": "/auth/resend-otp", "method": "POST", "description": "Resend OTP"},
    ]

    for endpoint in endpoints_to_test:
        try:
            if endpoint["method"] == "POST":
                # Test with dummy data to check if endpoint exists
                test_data = {"test": "data"}
                response = requests.post(
                    f"{FLASK_BASE_URL}{endpoint['url']}", json=test_data)

                # We expect 400/422 for invalid data, not 404
                if response.status_code in [200, 400, 422]:
                    print_success(
                        f"{endpoint['description']} endpoint is available")
                elif response.status_code == 404:
                    print_error(
                        f"{endpoint['description']} endpoint not found")
                else:
                    print_info(
                        f"{endpoint['description']} endpoint responded with {response.status_code}")

        except Exception as e:
            print_error(f"Failed to test {endpoint['description']}: {str(e)}")


def main():
    """Run OTP functionality tests"""
    print_header("OTP FUNCTIONALITY TEST SUITE")
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Test endpoints first
    test_otp_endpoints()

    # Test the main OTP flow
    success = test_user_signup_and_otp()

    print_header("TEST RESULTS")

    if success:
        print_success("🎉 OTP functionality test completed!")
        print_info("Key points:")
        print_info("1. Check Flask backend console for OTP codes")
        print_info("2. OTP codes are printed for development/testing")
        print_info("3. Use the actual OTP from console for verification")
        print_info("4. OTP verification should update user.isVerified to true")
    else:
        print_error("❌ OTP functionality test had issues")
        print_info("Check the error messages above for details")

    print(
        f"\nTest completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
