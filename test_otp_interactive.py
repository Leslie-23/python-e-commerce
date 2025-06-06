#!/usr/bin/env python3
"""
Focused OTP Test for codexcoder082@gmail.com
"""

import requests
import json
import time

# Configuration
FLASK_BASE_URL = "http://127.0.0.1:5000"
timestamp = str(int(time.time()))
TEST_EMAIL = f"codexcoder082+{timestamp}@gmail.com"
TEST_PASSWORD = "TestPass123!"


def print_step(step, message):
    print(f"\n🔸 Step {step}: {message}")


def main():
    print("="*60)
    print(" TESTING OTP FUNCTIONALITY")
    print("="*60)
    print(f"📧 Test Email: {TEST_EMAIL}")
    print(f"🔑 Password: {TEST_PASSWORD}")

    try:
        # Step 1: Register new user
        print_step(1, "User Registration")
        signup_data = {
            "name": "Code Coder Test",
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        }

        response = requests.post(
            f"{FLASK_BASE_URL}/auth/signup", json=signup_data)

        if response.status_code == 201:
            user_data = response.json()
            print("✅ Registration successful!")
            print(f"   User ID: {user_data.get('id')}")
            print(f"   Name: {user_data.get('name')}")
            print(f"   Email: {user_data.get('email')}")
            print(f"   Verified: {user_data.get('isVerified', False)}")

            user_id = user_data.get('id')

        else:
            print(f"❌ Registration failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return

        # Step 2: Check console for OTP
        print_step(2, "OTP Generation")
        print("✅ Check your Flask backend console now!")
        print(f"   Look for: '🔐 OTP for {TEST_EMAIL}: XXXXXX'")
        print("   The OTP should be a 6-digit code")

        # Wait a moment for user to see the OTP
        input("\n⏳ Press Enter after you've noted the OTP from the console...")

        # Step 3: Get OTP from user
        print_step(3, "OTP Verification")
        actual_otp = input("🔐 Enter the OTP from the console: ").strip()

        if not actual_otp:
            print("❌ No OTP entered, using test OTP")
            actual_otp = "123456"

        # Verify OTP
        otp_data = {
            "otp": actual_otp,
            "userId": user_id
        }

        otp_response = requests.post(
            f"{FLASK_BASE_URL}/auth/verify-otp", json=otp_data)

        if otp_response.status_code == 200:
            verified_user = otp_response.json()
            print("✅ OTP verification successful!")
            print(
                f"   User is now verified: {verified_user.get('isVerified', False)}")
            print(f"   User ID: {verified_user.get('id')}")
            print(f"   Email: {verified_user.get('email')}")

            # Step 4: Test login with verified user
            print_step(4, "Login Test (Post-Verification)")
            login_data = {
                "email": TEST_EMAIL,
                "password": TEST_PASSWORD
            }

            login_response = requests.post(
                f"{FLASK_BASE_URL}/auth/login", json=login_data)

            if login_response.status_code == 200:
                login_user = login_response.json()
                print("✅ Login successful after verification!")
                print(
                    f"   Verified status: {login_user.get('isVerified', False)}")
                print("✅ Complete OTP flow working correctly!")
            else:
                print(f"❌ Login failed: {login_response.status_code}")
                print(f"   Response: {login_response.text}")

        else:
            otp_error = otp_response.json()
            print(f"❌ OTP verification failed: {otp_response.status_code}")
            print(f"   Error: {otp_error.get('message', 'Unknown error')}")

            # Test resend OTP
            print_step("4a", "Testing Resend OTP")
            resend_data = {"user": user_id}
            resend_response = requests.post(
                f"{FLASK_BASE_URL}/auth/resend-otp", json=resend_data)

            if resend_response.status_code == 200:
                print("✅ Resend OTP successful!")
                print("   Check console again for new OTP")

                # Allow another attempt
                new_otp = input("🔐 Enter the NEW OTP from console: ").strip()
                if new_otp:
                    retry_data = {
                        "otp": new_otp,
                        "userId": user_id
                    }

                    retry_response = requests.post(
                        f"{FLASK_BASE_URL}/auth/verify-otp", json=retry_data)

                    if retry_response.status_code == 200:
                        print("✅ OTP verification successful on retry!")
                        retry_user = retry_response.json()
                        print(
                            f"   User verified: {retry_user.get('isVerified', False)}")
                    else:
                        print(f"❌ Retry failed: {retry_response.status_code}")
            else:
                print(f"❌ Resend OTP failed: {resend_response.status_code}")

        print("\n" + "="*60)
        print(" TEST COMPLETE")
        print("="*60)
        print("📋 Summary:")
        print(f"   • Email: {TEST_EMAIL}")
        print(f"   • User ID: {user_id}")
        print("   • OTP functionality tested")
        print("   • Check above for verification results")

    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")


if __name__ == "__main__":
    main()
