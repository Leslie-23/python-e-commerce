#!/usr/bin/env python3
"""
Test Email OTP Functionality
This script will register a new user and send an actual OTP to the provided email
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
    print(f"\n{'='*50}")
    print(f" {title}")
    print(f"{'='*50}")


def print_success(message):
    print(f"✅ {message}")


def print_error(message):
    print(f"❌ {message}")


def print_info(message):
    print(f"ℹ️  {message}")


def test_email_otp_flow():
    """Test the complete OTP flow with real email"""
    print_header(f"TESTING EMAIL OTP WITH {TEST_EMAIL}")

    # Step 1: Register new user
    print_info("Step 1: Registering new user...")

    # Add timestamp to make email unique if needed
    timestamp = str(int(time.time()))
    # Gmail ignores +text
    unique_email = f"codexcoder082+{timestamp}@gmail.com"

    signup_data = {
        "name": "Test User",
        "email": unique_email,
        "password": TEST_PASSWORD
    }

    try:
        response = requests.post(
            f"{FLASK_BASE_URL}/auth/signup", json=signup_data)

        if response.status_code == 201:
            user_data = response.json()
            user_id = user_data.get('id')
            print_success(f"User registered successfully!")
            print_info(f"User ID: {user_id}")
            print_info(f"Email: {unique_email}")
            print_info(f"Name: {user_data.get('name', 'N/A')}")

            if user_id:
                # Step 2: Check if OTP was sent
                print_info("Step 2: OTP should be sent to your email...")
                print_info(
                    "📧 Check your Gmail inbox and spam folder for the OTP")
                print_info("⏰ OTP expires in 10 minutes")

                # Interactive OTP verification
                print_info("\nStep 3: Enter the OTP you received via email")

                while True:
                    try:
                        otp_input = input(
                            "Enter OTP (or 'q' to quit): ").strip()

                        if otp_input.lower() == 'q':
                            print_info("OTP test cancelled by user")
                            break

                        if len(otp_input) != 6 or not otp_input.isdigit():
                            print_error(
                                "OTP must be 6 digits. Please try again.")
                            continue

                        # Verify OTP
                        otp_data = {
                            "otp": otp_input,
                            "userId": user_id
                        }

                        otp_response = requests.post(
                            f"{FLASK_BASE_URL}/auth/verify-otp", json=otp_data)

                        if otp_response.status_code == 200:
                            verified_user = otp_response.json()
                            print_success("🎉 OTP verification successful!")
                            print_info(
                                f"User is now verified: {verified_user.get('isVerified', False)}")
                            print_info(
                                "You can now login with your credentials")

                            # Test login after verification
                            print_info(
                                "\nStep 4: Testing login after verification...")
                            login_data = {
                                "email": unique_email,
                                "password": TEST_PASSWORD
                            }

                            login_response = requests.post(
                                f"{FLASK_BASE_URL}/auth/login", json=login_data)

                            if login_response.status_code == 200:
                                login_result = login_response.json()
                                print_success(
                                    "Login successful after OTP verification!")
                                print_info(
                                    f"Logged in user: {login_result.get('email', 'N/A')}")
                                print_info(
                                    f"Is verified: {login_result.get('isVerified', False)}")
                                print_info(
                                    f"Is admin: {login_result.get('isAdmin', False)}")
                            else:
                                print_error(
                                    f"Login failed: {login_response.status_code}")
                                if login_response.text:
                                    print_info(f"Error: {login_response.text}")

                            break

                        elif otp_response.status_code == 400:
                            error_msg = otp_response.json().get('message', 'Invalid OTP')
                            print_error(
                                f"OTP verification failed: {error_msg}")

                            if "expired" in error_msg.lower():
                                # Offer to resend OTP
                                resend = input(
                                    "OTP expired. Resend OTP? (y/n): ").strip().lower()
                                if resend == 'y':
                                    resend_data = {"user": user_id}
                                    resend_response = requests.post(
                                        f"{FLASK_BASE_URL}/auth/resend-otp", json=resend_data)

                                    if resend_response.status_code == 200:
                                        print_success(
                                            "New OTP sent! Check your email.")
                                    else:
                                        print_error(
                                            f"Failed to resend OTP: {resend_response.status_code}")
                                        break
                                else:
                                    break
                            else:
                                print_info(
                                    "Please check the OTP and try again.")

                        else:
                            print_error(
                                f"Unexpected error: {otp_response.status_code}")
                            if otp_response.text:
                                print_info(
                                    f"Error details: {otp_response.text}")
                            break

                    except KeyboardInterrupt:
                        print_info("\nTest interrupted by user")
                        break
                    except Exception as e:
                        print_error(f"Error during OTP verification: {str(e)}")
                        break
            else:
                print_error("No user ID returned from signup")

        else:
            print_error(f"User registration failed: {response.status_code}")
            error_data = response.json() if response.content else {}
            error_msg = error_data.get('message', 'Unknown error')
            print_info(f"Error: {error_msg}")

            # If user already exists, offer to test with existing user
            if "already exists" in error_msg.lower():
                print_info(f"\nUser {unique_email} already exists.")
                print_info(
                    "You can try logging in directly or use a different email.")

    except requests.exceptions.ConnectionError:
        print_error(
            "Cannot connect to Flask backend. Make sure it's running on port 5000.")
    except Exception as e:
        print_error(f"Test failed with error: {str(e)}")


def main():
    """Run the email OTP test"""
    print_header("EMAIL OTP TESTING TOOL")
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print_info(f"Testing email: {TEST_EMAIL}")
    print_info("Make sure your Flask backend is running!")

    test_email_otp_flow()

    print(
        f"\nTest completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
