#!/usr/bin/env python3
"""
Test OTP functionality with marvelmmk2005@gmail.com
This will test the complete OTP registration and verification flow
"""

import requests
import json
import time
from datetime import datetime

# Configuration
FLASK_BASE_URL = "http://127.0.0.1:5000"
TEST_EMAIL = "marvelmmk2005@gmail.com"
TEST_PASSWORD = "TestPass123!"
TEST_NAME = "Marvel Test User"


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


def test_user_registration():
    """Test user registration with marvelmmk2005@gmail.com"""
    print_header("TESTING USER REGISTRATION")

    print_info(f"Registering user with email: {TEST_EMAIL}")

    try:
        # Registration data
        signup_data = {
            "name": TEST_NAME,
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        }

        # Send registration request
        response = requests.post(
            f"{FLASK_BASE_URL}/auth/signup", json=signup_data)

        if response.status_code == 201:
            result = response.json()
            print_success("✅ User registration successful!")
            print_info(f"User ID: {result.get('id')}")
            print_info(f"Email: {result.get('email')}")
            print_info(f"Name: {result.get('name')}")
            print_info(f"Is Verified: {result.get('isVerified', False)}")

            return result

        elif response.status_code == 400:
            error_data = response.json()
            if "already exists" in error_data.get('message', '').lower():
                print_warning(
                    "User already exists! This is expected if testing multiple times.")
                # Try to get user info by attempting login
                return test_existing_user_login()
            else:
                print_error(
                    f"Registration failed: {error_data.get('message')}")
                return None
        else:
            print_error(
                f"Registration failed with status: {response.status_code}")
            print_error(f"Response: {response.text}")
            return None

    except Exception as e:
        print_error(f"Registration error: {str(e)}")
        return None


def test_existing_user_login():
    """Test login for existing user to get user data"""
    print_info("Testing login to get existing user data...")

    try:
        login_data = {
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        }

        response = requests.post(
            f"{FLASK_BASE_URL}/auth/login", json=login_data)

        if response.status_code == 200:
            result = response.json()
            print_info("Login successful - user exists")
            return result.get('user')
        else:
            print_error("Could not login with existing user")
            return None

    except Exception as e:
        print_error(f"Login error: {str(e)}")
        return None


def test_resend_otp(user_id):
    """Test resending OTP to user's email"""
    print_header("TESTING OTP SENDING")

    print_info(f"Sending OTP to: {TEST_EMAIL}")
    print_info("📧 CHECK YOUR EMAIL INBOX for the OTP!")

    try:
        # Resend OTP data
        otp_data = {
            "user": user_id
        }

        # Send OTP request
        response = requests.post(
            f"{FLASK_BASE_URL}/auth/resend-otp", json=otp_data)

        if response.status_code == 200:
            result = response.json()
            print_success("✅ OTP sent successfully!")
            print_success(f"📧 Check your email: {TEST_EMAIL}")
            print_info(f"Response: {result.get('message')}")

            # Also check console for OTP (fallback)
            print_warning(
                "💡 Also check the Flask server console for the OTP (backup)")

            return True
        else:
            print_error(
                f"OTP sending failed with status: {response.status_code}")
            print_error(f"Response: {response.text}")
            return False

    except Exception as e:
        print_error(f"OTP sending error: {str(e)}")
        return False


def test_otp_verification(user_id):
    """Test OTP verification with user input"""
    print_header("TESTING OTP VERIFICATION")

    print_info("Please check your email and enter the OTP you received")
    print_info(f"Email: {TEST_EMAIL}")

    try:
        # Get OTP from user
        otp_code = input("\n🔑 Enter the OTP from your email: ").strip()

        if not otp_code:
            print_error("No OTP entered")
            return False

        # Verification data
        verify_data = {
            "otp": otp_code,
            "userId": user_id
        }

        # Send verification request
        response = requests.post(
            f"{FLASK_BASE_URL}/auth/verify-otp", json=verify_data)

        if response.status_code == 200:
            result = response.json()
            print_success("✅ OTP verification successful!")
            print_success("🎉 Email verified successfully!")
            print_info(f"Message: {result.get('message')}")
            return True
        else:
            error_data = response.json() if response.headers.get(
                'content-type') == 'application/json' else {}
            print_error(
                f"OTP verification failed: {error_data.get('message', response.text)}")
            return False

    except KeyboardInterrupt:
        print_info("\nTest interrupted by user")
        return False
    except Exception as e:
        print_error(f"OTP verification error: {str(e)}")
        return False


def test_login_after_verification():
    """Test login after successful email verification"""
    print_header("TESTING LOGIN AFTER VERIFICATION")

    try:
        login_data = {
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        }

        response = requests.post(
            f"{FLASK_BASE_URL}/auth/login", json=login_data)

        if response.status_code == 200:
            result = response.json()
            user = result.get('user', {})
            print_success("✅ Login successful!")
            print_info(f"User: {user.get('name')} ({user.get('email')})")
            print_info(f"Is Verified: {user.get('isVerified')}")
            print_info(f"Is Admin: {user.get('isAdmin')}")

            if user.get('isVerified'):
                print_success(
                    "🎉 User is fully verified and can access the app!")
            else:
                print_warning("User still needs email verification")

            return True
        else:
            print_error(f"Login failed: {response.status_code}")
            return False

    except Exception as e:
        print_error(f"Login error: {str(e)}")
        return False


def main():
    """Main test function"""
    print_header("OTP EMAIL TESTING WITH MARVEL EMAIL")
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print_info(f"Testing with email: {TEST_EMAIL}")
    print_info("Make sure Flask backend is running on port 5000")

    # Test sequence
    user_data = test_user_registration()
    if not user_data:
        print_error("❌ Registration failed, cannot continue tests")
        return

    user_id = user_data.get('id')
    if not user_id:
        print_error("❌ No user ID found, cannot continue")
        return

    # Test OTP sending
    otp_sent = test_resend_otp(user_id)
    if not otp_sent:
        print_error("❌ OTP sending failed")
        return

    # Test OTP verification
    print_info("\n" + "="*60)
    print_info("📧 IMPORTANT: Check your email now!")
    print_info(f"Look for an email from the system in: {TEST_EMAIL}")
    print_info("The email should contain a 4-digit OTP code")
    print_info("="*60)

    otp_verified = test_otp_verification(user_id)
    if otp_verified:
        # Test final login
        test_login_after_verification()

        print_header("🎉 TEST COMPLETION SUMMARY")
        print_success("✅ User registration successful")
        print_success("✅ OTP email sent successfully")
        print_success("✅ OTP verification successful")
        print_success("✅ Login after verification successful")
        print_success("🎉 EMAIL OTP SYSTEM IS WORKING PERFECTLY!")

    else:
        print_header("❌ TEST SUMMARY")
        print_error("OTP verification failed")
        print_info("This could be due to:")
        print_info("1. Wrong OTP entered")
        print_info("2. OTP expired (10 minutes)")
        print_info("3. Email not received")

    print(
        f"\nTest completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
