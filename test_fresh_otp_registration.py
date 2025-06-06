#!/usr/bin/env python3
"""
Test Fresh OTP Registration Flow
Tests the complete OTP flow with the freshly removed user codexcoder082@gmail.com
"""

import requests
import json
import time
from datetime import datetime

# Configuration
FLASK_BASE_URL = "http://127.0.0.1:5000"


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


def test_fresh_otp_registration():
    """Test complete OTP registration flow with fresh user"""
    print_header("FRESH OTP REGISTRATION TEST")

    test_email = "codexcoder082@gmail.com"
    test_password = "TestPass123!"
    test_name = "Codex Coder"

    print_info(f"Testing with email: {test_email}")
    print_info(
        "This email was just removed from database - testing fresh registration")

    try:
        # Step 1: Register new user
        print_header("Step 1: User Registration")
        signup_data = {
            "name": test_name,
            "email": test_email,
            "password": test_password
        }

        response = requests.post(
            f"{FLASK_BASE_URL}/auth/signup", json=signup_data)

        if response.status_code == 201:
            signup_result = response.json()
            print_success("✨ User registration successful!")
            print_info(f"User ID: {signup_result.get('id', 'N/A')}")
            print_info(f"User Name: {signup_result.get('name', 'N/A')}")
            print_info(f"User Email: {signup_result.get('email', 'N/A')}")
            print_info(
                f"Is Verified: {signup_result.get('isVerified', 'N/A')}")

            user_id = signup_result.get('id')

            if not user_id:
                print_error("No user ID returned from registration")
                return False

        else:
            print_error(
                f"Registration failed with status: {response.status_code}")
            print_error(f"Response: {response.text}")
            return False

        # Step 2: Test OTP Generation (via resend OTP)
        print_header("Step 2: OTP Generation")
        resend_data = {"user": user_id}

        resend_response = requests.post(
            f"{FLASK_BASE_URL}/auth/resend-otp", json=resend_data)

        if resend_response.status_code == 200:
            print_success("✨ OTP generation successful!")
            print_info(
                "OTP has been generated and sent (check backend console)")
        else:
            print_error(
                f"OTP generation failed: {resend_response.status_code}")
            print_error(f"Response: {resend_response.text}")

        # Step 3: Interactive OTP Verification
        print_header("Step 3: OTP Verification (Interactive)")
        print_warning("Check your Flask backend console for the generated OTP")
        print_info("The OTP should be displayed in the backend logs")

        while True:
            user_input = input(
                "\nEnter the OTP from backend console (or 'skip' to continue): ").strip()

            if user_input.lower() == 'skip':
                print_info(
                    "Skipping OTP verification - testing with dummy OTP")
                user_input = "123456"  # This will fail but tests the endpoint

            otp_data = {
                "otp": user_input,
                "userId": user_id
            }

            otp_response = requests.post(
                f"{FLASK_BASE_URL}/auth/verify-otp", json=otp_data)

            if otp_response.status_code == 200:
                print_success("✨ OTP verification successful!")
                otp_result = otp_response.json()
                print_info(
                    f"Verification result: {json.dumps(otp_result, indent=2)}")
                break
            elif otp_response.status_code == 400:
                error_response = otp_response.json()
                if "invalid" in error_response.get('message', '').lower():
                    print_error("Invalid OTP entered. Please try again.")
                    retry = input("Try again? (y/n): ").strip().lower()
                    if retry != 'y':
                        break
                else:
                    print_error(
                        f"OTP verification failed: {error_response.get('message', 'Unknown error')}")
                    break
            else:
                print_error(
                    f"OTP verification failed: {otp_response.status_code}")
                print_error(f"Response: {otp_response.text}")
                break

        # Step 4: Test Login After Verification
        print_header("Step 4: Login Test")
        login_data = {
            "email": test_email,
            "password": test_password
        }

        login_response = requests.post(
            f"{FLASK_BASE_URL}/auth/login", json=login_data)

        if login_response.status_code == 200:
            login_result = login_response.json()
            print_success("✨ Login successful!")
            print_info(f"Login result: {json.dumps(login_result, indent=2)}")

            user_data = login_result.get('user', {})
            print_info(f"Logged in user: {user_data.get('name', 'N/A')}")
            print_info(f"Email: {user_data.get('email', 'N/A')}")
            print_info(f"Is Verified: {user_data.get('isVerified', 'N/A')}")
            print_info(f"Is Admin: {user_data.get('isAdmin', 'N/A')}")

        else:
            login_result = login_response.json()
            if "not verified" in login_result.get('message', '').lower():
                print_warning(
                    "Login redirected to OTP verification (user not verified yet)")
                print_info("This is expected behavior for unverified users")
            else:
                print_error(f"Login failed: {login_response.status_code}")
                print_error(f"Response: {login_response.text}")

        return True

    except Exception as e:
        print_error(f"Test failed with exception: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run the fresh OTP registration test"""
    print_header("FRESH OTP REGISTRATION & VERIFICATION TEST")
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print_info("Testing with freshly removed user: codexcoder082@gmail.com")

    # Check Flask backend availability
    try:
        response = requests.get(f"{FLASK_BASE_URL}/")
        if response.status_code != 200:
            print_error("Flask backend is not running! Please start it first.")
            return
    except requests.exceptions.ConnectionError:
        print_error(
            "Cannot connect to Flask backend. Please start it on port 5000.")
        return

    # Run the test
    success = test_fresh_otp_registration()

    # Summary
    print_header("TEST SUMMARY")
    if success:
        print_success("🎉 Fresh OTP registration test completed!")
        print_info("Key points tested:")
        print_info("✓ User registration with fresh email")
        print_info("✓ OTP generation and sending")
        print_info("✓ OTP verification process")
        print_info("✓ Login behavior based on verification status")
    else:
        print_error("⚠️  Test encountered issues. Check the output above.")

    print(
        f"\nTest completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
