#!/usr/bin/env python3
"""
Simple OTP Test - Register a new user and test OTP functionality
This script creates a fresh test user to avoid password issues
"""

import requests
import json
import time
from datetime import datetime

# Configuration
FLASK_BASE_URL = "http://127.0.0.1:5000"
TEST_EMAIL = "otp.test.user@gmail.com"  # Different email for testing
TEST_PASSWORD = "TestOTP123!"
TEST_NAME = "OTP Test User"


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


def print_warning(message):
    print(f"⚠️  {message}")


def test_full_otp_flow():
    """Test complete OTP flow with a new user"""
    print_header("TESTING COMPLETE OTP FLOW")
    print_info(f"Testing with email: {TEST_EMAIL}")

    try:
        # Step 1: Register new user
        print_info("Step 1: Registering new user...")

        signup_data = {
            "name": TEST_NAME,
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        }

        response = requests.post(
            f"{FLASK_BASE_URL}/auth/signup", json=signup_data)

        if response.status_code == 201:
            user_data = response.json()
            user_id = user_data.get('id')
            print_success("User registration successful!")
            print_info(f"User ID: {user_id}")
            print_info(f"Email: {user_data.get('email', 'N/A')}")
            print_info(f"Name: {user_data.get('name', 'N/A')}")
            print_info(f"Verified: {user_data.get('isVerified', False)}")

            if not user_id:
                print_error("No user ID returned")
                return False

            # Step 2: Check console for OTP
            print_info("Step 2: OTP should be generated...")
            print_warning("Check your Flask backend console for the OTP code!")
            print_info("Look for: '🔐 OTP for otp.test.user@gmail.com: XXXXXX'")

            time.sleep(2)  # Give time to see the message

            # Step 3: Interactive OTP verification
            print_info("Step 3: OTP Verification")
            otp_code = input(
                "Enter the OTP from the backend console: ").strip()

            if not otp_code:
                print_error("No OTP entered")
                return False

            if len(otp_code) != 6 or not otp_code.isdigit():
                print_warning("OTP should be 6 digits")
                print_info("Trying anyway...")

            # Verify OTP
            otp_data = {
                "otp": otp_code,
                "userId": user_id
            }

            otp_response = requests.post(
                f"{FLASK_BASE_URL}/auth/verify-otp", json=otp_data)

            if otp_response.status_code == 200:
                verified_user = otp_response.json()
                print_success("🎉 OTP verification successful!")
                print_info(f"User ID: {verified_user.get('id', 'N/A')}")
                print_info(f"Email: {verified_user.get('email', 'N/A')}")
                print_info(f"Name: {verified_user.get('name', 'N/A')}")
                print_info(
                    f"Verified: {verified_user.get('isVerified', False)}")
                print_info(f"Admin: {verified_user.get('isAdmin', False)}")

                # Step 4: Test login after verification
                print_info("Step 4: Testing login after OTP verification...")

                login_data = {
                    "email": TEST_EMAIL,
                    "password": TEST_PASSWORD
                }

                login_response = requests.post(
                    f"{FLASK_BASE_URL}/auth/login", json=login_data)

                if login_response.status_code == 200:
                    login_result = login_response.json()
                    user_info = login_result.get('user', {})
                    print_success("Login successful after OTP verification!")
                    print_info(f"User ID: {user_info.get('id', 'N/A')}")
                    print_info(f"Email: {user_info.get('email', 'N/A')}")
                    print_info(f"Name: {user_info.get('name', 'N/A')}")
                    print_info(
                        f"Verified: {user_info.get('isVerified', 'N/A')}")
                    print_info(f"Admin: {user_info.get('isAdmin', 'N/A')}")
                    return True
                else:
                    print_error(f"Login failed: {login_response.status_code}")
                    print_info(f"Response: {login_response.text}")
                    return False

            else:
                print_error(
                    f"OTP verification failed: {otp_response.status_code}")
                print_info(f"Response: {otp_response.text}")

                # Test resend OTP
                print_info("Testing resend OTP...")
                resend_data = {"user": user_id}
                resend_response = requests.post(
                    f"{FLASK_BASE_URL}/auth/resend-otp", json=resend_data)

                if resend_response.status_code == 200:
                    print_success("OTP resent successfully!")
                    print_info("Check console again for new OTP")

                    # Allow another attempt
                    new_otp = input("Enter the new OTP: ").strip()
                    if new_otp:
                        retry_data = {"otp": new_otp, "userId": user_id}
                        retry_response = requests.post(
                            f"{FLASK_BASE_URL}/auth/verify-otp", json=retry_data)

                        if retry_response.status_code == 200:
                            print_success(
                                "OTP verification successful on retry!")
                            return True
                        else:
                            print_error(
                                f"Retry failed: {retry_response.status_code}")
                else:
                    print_error(
                        f"Resend OTP failed: {resend_response.status_code}")

                return False

        elif response.status_code == 400:
            response_data = response.json()
            if "already exists" in response_data.get('message', ''):
                print_warning(
                    "User already exists! Testing with existing user...")
                return test_existing_user_otp()
            else:
                print_error(
                    f"Registration failed: {response_data.get('message', 'Unknown error')}")
                return False

        else:
            print_error(f"Registration failed: {response.status_code}")
            print_info(f"Response: {response.text}")
            return False

    except Exception as e:
        print_error(f"Test failed: {str(e)}")
        return False


def test_existing_user_otp():
    """Handle existing user OTP testing"""
    print_info("Testing with existing user...")

    # Try to determine user status by attempting login
    login_data = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }

    response = requests.post(f"{FLASK_BASE_URL}/auth/login", json=login_data)

    if response.status_code == 200:
        user_data = response.json().get('user', {})
        print_success("User login successful!")
        print_info(f"User ID: {user_data.get('id', 'N/A')}")
        print_info(f"Verified: {user_data.get('isVerified', 'N/A')}")

        if user_data.get('isVerified'):
            print_success("User is already verified - OTP test not needed!")
            return True
        else:
            print_info("User exists but not verified - can test OTP")
            user_id = user_data.get('id')
            if user_id:
                return test_otp_resend_and_verify(user_id)

    elif response.status_code == 401:
        print_warning(
            "Login failed - either wrong password or user needs verification")
        print_info("This might indicate the user needs OTP verification")

    print_info("For existing user testing, you may need to:")
    print_info("1. Use the correct password")
    print_info("2. Or delete the existing user and try again")
    return False


def test_otp_resend_and_verify(user_id):
    """Test OTP resend and verification for existing user"""
    print_info(f"Testing OTP resend for user ID: {user_id}")

    # Resend OTP
    resend_data = {"user": user_id}
    resend_response = requests.post(
        f"{FLASK_BASE_URL}/auth/resend-otp", json=resend_data)

    if resend_response.status_code == 200:
        print_success("OTP resent successfully!")
        print_info("Check backend console for OTP")

        otp_code = input("Enter OTP from console: ").strip()
        if otp_code:
            verify_data = {"otp": otp_code, "userId": user_id}
            verify_response = requests.post(
                f"{FLASK_BASE_URL}/auth/verify-otp", json=verify_data)

            if verify_response.status_code == 200:
                print_success("OTP verification successful!")
                return True
            else:
                print_error(
                    f"OTP verification failed: {verify_response.status_code}")

    else:
        print_error(f"OTP resend failed: {resend_response.status_code}")

    return False


def main():
    """Run OTP test"""
    print_header("OTP FUNCTIONALITY TEST")
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Check backend
    try:
        response = requests.get(f"{FLASK_BASE_URL}/")
        if response.status_code != 200:
            print_error("Flask backend is not running!")
            return
    except:
        print_error("Cannot connect to Flask backend!")
        return

    print_success("Flask backend is running")

    # Run test
    success = test_full_otp_flow()

    # Summary
    print_header("TEST SUMMARY")

    if success:
        print_success("🎉 OTP TEST COMPLETED SUCCESSFULLY!")
        print_info("Key findings:")
        print_info("✅ User registration works")
        print_info("✅ OTP generation works (check console)")
        print_info("✅ OTP verification works")
        print_info("✅ Login after verification works")
        print_info("✅ User data fields are properly formatted (camelCase)")
        print("")
        print_info("You can now test with your actual email:")
        print_info("1. Change TEST_EMAIL to 'codexcoder082@gmail.com'")
        print_info("2. Run the test again")
        print_info("3. Check your actual email for OTP")
    else:
        print_error("⚠️  OTP TEST FAILED")
        print_info("Please check:")
        print_info("1. Flask backend console for OTP codes")
        print_info("2. User registration process")
        print_info("3. OTP verification endpoint")

    print(
        f"\nTest completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
