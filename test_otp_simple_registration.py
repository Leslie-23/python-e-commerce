#!/usr/bin/env python3
"""
Simple OTP Registration Test
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


def test_registration_and_otp():
    """Test user registration and OTP sending"""
    print_header("TESTING REGISTRATION AND OTP")

    # Test data
    test_email = "marvelmmk2005@gmail.com"
    signup_data = {
        "name": "Marvel Test User",
        "email": test_email,
        "password": "TestPass123!"
    }

    print_info(f"Testing with email: {test_email}")

    try:
        # Step 1: Register user
        print_info("Step 1: Registering user...")
        response = requests.post(
            "http://127.0.0.1:5000/auth/signup", json=signup_data)

        print_info(f"Registration response status: {response.status_code}")
        print_info(f"Registration response: {response.text}")

        if response.status_code == 201:
            result = response.json()
            user_id = result.get('id')
            print_success(f"User registered successfully! User ID: {user_id}")

            # Step 2: Request OTP
            if user_id:
                print_info("Step 2: Requesting OTP...")
                otp_data = {"user": user_id}
                otp_response = requests.post(
                    "http://127.0.0.1:5000/auth/resend-otp", json=otp_data)

                print_info(f"OTP request status: {otp_response.status_code}")
                print_info(f"OTP request response: {otp_response.text}")

                if otp_response.status_code == 200:
                    print_success("OTP request successful!")
                    print_info(
                        "Check your email and Flask backend console for the OTP")

                    # Instructions
                    print_header("WHAT TO CHECK NOW")
                    print_info(
                        "1. Check your Gmail inbox: marvelmmk2005@gmail.com")
                    print_info("2. Check Gmail spam/junk folder")
                    print_info("3. Look at Flask backend console for:")
                    print_info(
                        "   - 'OTP sent to email: marvelmmk2005@gmail.com'")
                    print_info("   - The actual OTP code")
                    print_info("   - Any error messages")

                else:
                    print_error("OTP request failed")
            else:
                print_error("No user ID returned from registration")

        elif response.status_code == 400:
            print_error(
                "User might already exist - this is expected if testing multiple times")
            # Try to get user info
            try:
                error_data = response.json()
                print_info(f"Error details: {error_data}")
            except:
                print_info("Could not parse error response")
        else:
            print_error(
                f"Registration failed with status: {response.status_code}")

    except requests.exceptions.ConnectionError:
        print_error(
            "Cannot connect to Flask backend. Make sure it's running on port 5000")
    except Exception as e:
        print_error(f"Test failed: {str(e)}")


def check_backend_status():
    """Check if backend is running"""
    print_header("CHECKING BACKEND STATUS")

    try:
        response = requests.get("http://127.0.0.1:5000/")
        if response.status_code == 200:
            print_success("Backend is running")
            return True
        else:
            print_error(f"Backend returned status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Backend is not running or not accessible")
        return False


def main():
    """Main test function"""
    print_header("OTP EMAIL SYSTEM TEST")

    # Check backend first
    if check_backend_status():
        test_registration_and_otp()
    else:
        print_error(
            "Backend is not running. Please start the Flask backend first.")


if __name__ == "__main__":
    main()
