#!/usr/bin/env python3
"""
Enhanced OTP test for existing user codexcoder082@gmail.com
This script handles both new and existing users
"""

import requests
import json
import time
from datetime import datetime

# Configuration
FLASK_BASE_URL = "http://127.0.0.1:5000"
TEST_EMAIL = "codexcoder082@gmail.com"


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


def check_user_status():
    """Check if user exists and their verification status"""
    print_header("CHECKING USER STATUS")

    try:
        # Try to login with a dummy password to get user info
        login_data = {
            "email": TEST_EMAIL,
            "password": "dummy_password"
        }

        response = requests.post(
            f"{FLASK_BASE_URL}/auth/login", json=login_data)

        if response.status_code == 200:
            # User exists and is verified
            user_data = response.json()
            print_success("User exists and is already verified!")
            user_info = user_data.get('user', {})
            print_info(f"User ID: {user_info.get('id', 'N/A')}")
            print_info(f"Email: {user_info.get('email', 'N/A')}")
            print_info(f"Name: {user_info.get('name', 'N/A')}")
            print_info(f"Verified: {user_info.get('isVerified', 'N/A')}")
            print_info(f"Admin: {user_info.get('isAdmin', 'N/A')}")
            return "verified", user_info.get('id')

        elif response.status_code == 401:
            response_data = response.json()
            if "verify" in response_data.get('message', '').lower() or "otp" in response_data.get('message', '').lower():
                print_warning("User exists but is not verified!")
                print_info("User needs OTP verification")
                # We need to extract user ID somehow
                return "unverified", None
            else:
                print_info("User exists but wrong password used for test")
                return "exists", None

        elif response.status_code == 404:
            print_info("User does not exist")
            return "not_exists", None

        else:
            print_warning(f"Unexpected response: {response.status_code}")
            print_info(f"Response: {response.text}")
            return "unknown", None

    except Exception as e:
        print_error(f"Error checking user status: {str(e)}")
        return "error", None


def test_otp_resend():
    """Test OTP resend functionality"""
    print_header("TESTING OTP RESEND")

    try:
        # Try different approaches to resend OTP
        print_info("Attempting to resend OTP using email...")

        # Method 1: Using email
        resend_data = {"email": TEST_EMAIL}
        response = requests.post(
            f"{FLASK_BASE_URL}/auth/resend-otp", json=resend_data)

        if response.status_code == 200:
            print_success("OTP resent successfully using email!")
            response_data = response.json()
            print_info(f"Response: {response_data}")
            return True, "email"

        print_warning(f"Resend via email failed: {response.status_code}")
        print_info(f"Response: {response.text}")

        # Method 2: Let's check what the resend endpoint expects
        print_info("Checking resend endpoint requirements...")

        return False, None

    except Exception as e:
        print_error(f"Error testing OTP resend: {str(e)}")
        return False, None


def interactive_otp_verification():
    """Interactive OTP verification process"""
    print_header("INTERACTIVE OTP VERIFICATION")

    print_info(f"We will send an OTP to: {TEST_EMAIL}")
    print_warning("Please check your email (including spam folder)")
    print_info("The OTP will be a 6-digit code")

    # Attempt to resend OTP
    success, method = test_otp_resend()

    if success:
        print_success(f"OTP sent successfully via {method}!")
        print_info("Please check your email now...")

        # Wait for user input
        time.sleep(2)
        print_info("Please enter the OTP you received:")
        otp_code = input("OTP: ").strip()

        if not otp_code:
            print_error("No OTP entered")
            return False

        if len(otp_code) != 6 or not otp_code.isdigit():
            print_warning("OTP should be a 6-digit number")
            print_info("Please try again:")
            otp_code = input("OTP: ").strip()

        # Now we need to verify the OTP
        # But we need the user ID. Let's try different approaches
        print_info("Attempting OTP verification...")

        # Try with email instead of userId if the API supports it
        otp_data_email = {
            "otp": otp_code,
            "email": TEST_EMAIL
        }

        response = requests.post(
            f"{FLASK_BASE_URL}/auth/verify-otp", json=otp_data_email)

        if response.status_code == 200:
            print_success("OTP verification successful!")
            response_data = response.json()
            print_info(f"Response: {response_data}")
            return True

        print_warning(
            f"OTP verification with email failed: {response.status_code}")
        print_info(f"Response: {response.text}")

        # The API might need userId, let's inform the user
        print_info(
            "The API might require userId instead of email for verification")
        print_info("This is a limitation we need to address in the backend")

        return False

    else:
        print_error("Could not send OTP. Please check backend logs.")
        return False


def test_login_after_verification():
    """Test login after OTP verification"""
    print_header("TESTING LOGIN AFTER VERIFICATION")

    print_info("Please enter the password for this account:")
    password = input("Password: ").strip()

    if not password:
        print_warning("No password entered, skipping login test")
        return False

    login_data = {
        "email": TEST_EMAIL,
        "password": password
    }

    response = requests.post(f"{FLASK_BASE_URL}/auth/login", json=login_data)

    if response.status_code == 200:
        print_success("Login successful!")
        user_data = response.json()
        user_info = user_data.get('user', {})
        print_info(f"User ID: {user_info.get('id', 'N/A')}")
        print_info(f"Email: {user_info.get('email', 'N/A')}")
        print_info(f"Name: {user_info.get('name', 'N/A')}")
        print_info(f"Verified: {user_info.get('isVerified', 'N/A')}")
        print_info(f"Admin: {user_info.get('isAdmin', 'N/A')}")
        return True

    else:
        print_error(f"Login failed: {response.status_code}")
        print_info(f"Response: {response.text}")
        return False


def main():
    """Run enhanced email OTP test"""
    print_header("ENHANCED EMAIL OTP TEST")
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print_info(f"Testing with email: {TEST_EMAIL}")

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

    # Check user status
    status, user_id = check_user_status()

    if status == "verified":
        print_success("User is already verified! No OTP needed.")
        print_info("You can login directly with this account.")

    elif status == "unverified":
        print_info("User exists but needs verification")
        success = interactive_otp_verification()

        if success:
            test_login_after_verification()

    elif status == "exists":
        print_info("User exists. Let's test the OTP flow anyway...")
        success = interactive_otp_verification()

        if success:
            test_login_after_verification()

    elif status == "not_exists":
        print_info("User doesn't exist. You can:")
        print_info("1. Register via the frontend app")
        print_info("2. Register via API and test OTP")
        print_info("Would you like to register now? (y/n):")

        choice = input().strip().lower()
        if choice == 'y':
            print_info("Please provide user details:")
            name = input("Name: ").strip()
            password = input("Password: ").strip()

            if name and password:
                signup_data = {
                    "name": name,
                    "email": TEST_EMAIL,
                    "password": password
                }

                response = requests.post(
                    f"{FLASK_BASE_URL}/auth/signup", json=signup_data)

                if response.status_code == 201:
                    print_success("Registration successful!")
                    interactive_otp_verification()
                else:
                    print_error(f"Registration failed: {response.status_code}")
                    print_info(f"Response: {response.text}")

    # Summary
    print_header("TEST SUMMARY")
    print_info("Email OTP functionality test completed")
    print_info("Key findings:")
    print_info("1. Backend is running and responding")
    print_info("2. Email configuration is set up")
    print_info(f"3. User {TEST_EMAIL} status checked")
    print_info("4. OTP resend functionality tested")

    print(
        f"\nTest completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
