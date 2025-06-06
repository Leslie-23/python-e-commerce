#!/usr/bin/env python3
"""
OTP Verification Test
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


def verify_otp():
    """Verify OTP with user input"""
    print_header("OTP VERIFICATION TEST")

    # Get user info first
    test_email = "marvelmmk2005@gmail.com"
    login_data = {
        "email": test_email,
        "password": "TestPass123!"
    }

    try:
        # Step 1: Login to get user ID
        print_info("Step 1: Getting user information...")
        response = requests.post(
            "http://127.0.0.1:5000/auth/login", json=login_data)

        if response.status_code == 200:
            result = response.json()
            user_id = result.get('id')
            is_verified = result.get('isVerified')

            print_success(f"User ID: {user_id}")
            print_info(f"Current verification status: {is_verified}")

            if not is_verified and user_id:
                # Step 2: Get OTP from user
                print_header("ENTER OTP FROM EMAIL")
                otp_code = input(
                    "Please enter the 4-digit OTP you received: ").strip()

                if len(otp_code) == 4 and otp_code.isdigit():
                    # Step 3: Verify OTP
                    print_info(f"Verifying OTP: {otp_code}")
                    verify_data = {
                        "otp": otp_code,
                        "userId": user_id
                    }

                    verify_response = requests.post(
                        "http://127.0.0.1:5000/auth/verify-otp", json=verify_data)

                    print_info(
                        f"OTP verification status: {verify_response.status_code}")
                    print_info(
                        f"OTP verification response: {verify_response.text}")

                    if verify_response.status_code == 200:
                        print_success("🎉 OTP VERIFICATION SUCCESSFUL!")
                        print_success("Your account is now verified!")

                        # Step 4: Test login again to confirm verification
                        print_info("Testing login with verified account...")
                        final_login = requests.post(
                            "http://127.0.0.1:5000/auth/login", json=login_data)

                        if final_login.status_code == 200:
                            final_result = final_login.json()
                            final_verified = final_result.get('isVerified')
                            print_success(
                                f"Final verification status: {final_verified}")

                            if final_verified:
                                print_header("🎉 COMPLETE SUCCESS!")
                                print_success("✅ Email sending works")
                                print_success("✅ OTP generation works")
                                print_success("✅ OTP verification works")
                                print_success("✅ User account is now verified")
                                print_info(
                                    "You can now login normally without OTP!")
                            else:
                                print_error(
                                    "Account verification status not updated")
                        else:
                            print_error("Final login test failed")
                    else:
                        print_error("OTP verification failed")
                        try:
                            error_data = verify_response.json()
                            print_info(f"Error details: {error_data}")
                        except:
                            pass
                else:
                    print_error("Please enter a valid 4-digit OTP")

            elif is_verified:
                print_success("User is already verified! No OTP needed.")
                print_info("You can login directly without OTP verification.")
            else:
                print_error("Could not get user information")

        else:
            print_error(f"Login failed: {response.status_code}")

    except Exception as e:
        print_error(f"Test failed: {str(e)}")


def main():
    """Main test function"""
    print_header("OTP VERIFICATION INTERACTIVE TEST")
    print_info("This test will help you verify the OTP you received via email")
    verify_otp()


if __name__ == "__main__":
    main()
