#!/usr/bin/env python3
"""
Test OTP with Existing User
"""

import requests
import json


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


def test_login_and_otp():
    """Test login with existing user and request OTP"""
    print_header("TESTING WITH EXISTING USER")

    test_email = "marvelmmk2005@gmail.com"
    login_data = {
        "email": test_email,
        "password": "TestPass123!"
    }

    print_info(f"Testing login with: {test_email}")

    try:
        # Step 1: Try to login
        print_info("Step 1: Attempting login...")
        response = requests.post(
            "http://127.0.0.1:5000/auth/login", json=login_data)

        print_info(f"Login response status: {response.status_code}")
        print_info(f"Login response: {response.text}") if response.status_code == 200:
            result = response.json()
            user_id = result.get('id')
            is_verified = result.get('isVerified')

            print_success(f"Login successful! User ID: {user_id}")
            print_info(f"User verified status: {is_verified}")

            if not is_verified and user_id:
                # Step 2: Request OTP for unverified user
                print_info("Step 2: Requesting OTP for unverified user...")
                otp_data = {"user": user_id}
                otp_response = requests.post(
                    "http://127.0.0.1:5000/auth/resend-otp", json=otp_data)

                print_info(f"OTP request status: {otp_response.status_code}")
                print_info(f"OTP request response: {otp_response.text}")

                if otp_response.status_code == 200:
                    print_success("🎉 OTP request successful!")
                    print_header("CHECK FOR EMAIL NOW")
                    print_info("1. Check Gmail inbox: marvelmmk2005@gmail.com")
                    print_info("2. Check Gmail spam/junk folder")
                    print_info("3. Look at Flask backend console for:")
                    print_info(
                        "   - 'Sending OTP to: marvelmmk2005@gmail.com'")
                    print_info("   - 'OTP: XXXX' (the actual OTP code)")
                    print_info("   - Email sending status messages")
                    print_info(
                        "4. If no email, the OTP should be in backend console")

                    return True
                else:
                    print_error("OTP request failed")

            elif is_verified:
                print_info("User is already verified - no OTP needed")
            else:
                print_error("No user ID found")

        else:
            print_error(f"Login failed with status: {response.status_code}")

    except Exception as e:
        print_error(f"Test failed: {str(e)}")
        return False


def main():
    """Main test function"""
    print_header("EXISTING USER OTP TEST")
    test_login_and_otp()


if __name__ == "__main__":
    main()
