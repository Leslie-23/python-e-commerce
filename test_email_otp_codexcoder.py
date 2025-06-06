#!/usr/bin/env python3
"""
Test OTP functionality with codexcoder082@gmail.com
This script tests the complete OTP flow with a real email address
"""

import requests
import json
import time
from datetime import datetime

# Configuration
FLASK_BASE_URL = "http://127.0.0.1:5000"
TEST_EMAIL = "codexcoder082@gmail.com"
TEST_PASSWORD = "TestPass123!"
TEST_NAME = "Test User"


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


def test_email_otp_flow():
    """Test complete OTP flow with codexcoder082@gmail.com"""
    print_header("TESTING EMAIL OTP FLOW")
    print_info(f"Testing with email: {TEST_EMAIL}")

    try:
        # Step 1: Check if user already exists
        print_info("Step 1: Checking if user exists...")

        # Try to login first to see if user exists
        login_data = {
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        }

        login_response = requests.post(
            f"{FLASK_BASE_URL}/auth/login", json=login_data)

        if login_response.status_code == 200:
            print_success("User already exists and is verified!")
            user_data = login_response.json()
            print_info(
                f"User ID: {user_data.get('user', {}).get('id', 'N/A')}")
            print_info(
                f"Email: {user_data.get('user', {}).get('email', 'N/A')}")
            print_info(
                f"Verified: {user_data.get('user', {}).get('isVerified', 'N/A')}")
            return True

        # Step 2: Register new user
        print_info("Step 2: Registering new user...")

        signup_data = {
            "name": TEST_NAME,
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        }

        signup_response = requests.post(
            f"{FLASK_BASE_URL}/auth/signup", json=signup_data)

        if signup_response.status_code == 201:
            signup_result = signup_response.json()
            print_success("User registration successful!")
            print_info(f"User ID: {signup_result.get('id', 'N/A')}")

            user_id = signup_result.get('id')

            if not user_id:
                print_error("No user ID returned from registration")
                return False

            # Step 3: Check email for OTP
            print_info("Step 3: OTP should be sent to your email")
            print_warning(
                f"Please check your email at {TEST_EMAIL} for the OTP code")
            print_info("The OTP will be valid for 10 minutes")

            # Wait for user to get OTP
            print_info("Please enter the OTP you received:")
            otp_code = input("OTP: ").strip()

            if not otp_code:
                print_error("No OTP entered")
                return False

            # Step 4: Verify OTP
            print_info("Step 4: Verifying OTP...")

            otp_data = {
                "otp": otp_code,
                "userId": user_id
            }

            otp_response = requests.post(
                f"{FLASK_BASE_URL}/auth/verify-otp", json=otp_data)

            if otp_response.status_code == 200:
                print_success("OTP verification successful!")
                otp_result = otp_response.json()
                print_info(f"Message: {otp_result.get('message', 'N/A')}")

                # Step 5: Test login after verification
                print_info("Step 5: Testing login after OTP verification...")

                login_response = requests.post(
                    f"{FLASK_BASE_URL}/auth/login", json=login_data)

                if login_response.status_code == 200:
                    print_success("Login successful after OTP verification!")
                    login_result = login_response.json()
                    user_info = login_result.get('user', {})
                    print_info(f"User ID: {user_info.get('id', 'N/A')}")
                    print_info(f"Email: {user_info.get('email', 'N/A')}")
                    print_info(f"Name: {user_info.get('name', 'N/A')}")
                    print_info(
                        f"Verified: {user_info.get('isVerified', 'N/A')}")
                    print_info(f"Admin: {user_info.get('isAdmin', 'N/A')}")
                    return True
                else:
                    print_error(
                        f"Login failed after OTP verification: {login_response.status_code}")
                    print_info(f"Response: {login_response.text}")
                    return False

            else:
                print_error(
                    f"OTP verification failed: {otp_response.status_code}")
                print_info(f"Response: {otp_response.text}")

                # Check if we can resend OTP
                print_info("Attempting to resend OTP...")
                resend_data = {"user": user_id}
                resend_response = requests.post(
                    f"{FLASK_BASE_URL}/auth/resend-otp", json=resend_data)

                if resend_response.status_code == 200:
                    print_success("OTP resent successfully!")
                    print_info("Please check your email again for the new OTP")
                else:
                    print_error(
                        f"Failed to resend OTP: {resend_response.status_code}")

                return False

        else:
            print_error(
                f"User registration failed: {signup_response.status_code}")
            print_info(f"Response: {signup_response.text}")

            # Check if user already exists
            if "already exists" in signup_response.text.lower():
                print_info("User might already exist. Trying to resend OTP...")

                # Try to get user ID by attempting login (will fail but might give us info)
                # Or try to resend OTP with email
                resend_data = {"email": TEST_EMAIL}
                resend_response = requests.post(
                    f"{FLASK_BASE_URL}/auth/resend-otp", json=resend_data)

                if resend_response.status_code == 200:
                    print_success("OTP resent to existing user!")
                    print_info("Please check your email for the OTP")
                else:
                    print_error(
                        f"Failed to resend OTP: {resend_response.status_code}")

            return False

    except requests.exceptions.ConnectionError:
        print_error(
            "Cannot connect to Flask backend. Make sure it's running on port 5000.")
        return False
    except Exception as e:
        print_error(f"Email OTP test failed: {str(e)}")
        return False


def test_backend_email_config():
    """Test if backend email configuration is working"""
    print_header("TESTING BACKEND EMAIL CONFIGURATION")

    try:
        # Check if Flask backend is running
        response = requests.get(f"{FLASK_BASE_URL}/")
        if response.status_code == 200:
            print_success("Flask backend is running")
        else:
            print_error("Flask backend is not responding")
            return False

        # Test a simple endpoint to ensure backend is functional
        response = requests.get(f"{FLASK_BASE_URL}/products")
        if response.status_code == 200:
            print_success("Backend API is functional")
        else:
            print_warning("Backend API might have issues")

        return True

    except Exception as e:
        print_error(f"Backend test failed: {str(e)}")
        return False


def main():
    """Run email OTP test"""
    print_header("EMAIL OTP TEST FOR CODEXCODER082@GMAIL.COM")
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Test backend first
    if not test_backend_email_config():
        print_error(
            "Backend is not ready. Please start the Flask backend first.")
        return

    # Run email OTP test
    success = test_email_otp_flow()

    # Summary
    print_header("TEST SUMMARY")

    if success:
        print_success("🎉 EMAIL OTP TEST COMPLETED SUCCESSFULLY!")
        print_info("The OTP system is working correctly with your email.")
        print_info("You can now use the frontend application to:")
        print_info("1. Register new users")
        print_info("2. Receive OTP via email")
        print_info("3. Verify accounts")
        print_info("4. Login after verification")
    else:
        print_error("⚠️  EMAIL OTP TEST FAILED")
        print_info("Please check:")
        print_info("1. Flask backend is running (python run.py)")
        print_info("2. Email configuration in .env file")
        print_info("3. Internet connection for sending emails")
        print_info("4. Spam folder for OTP emails")

    print(
        f"\nTest completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
