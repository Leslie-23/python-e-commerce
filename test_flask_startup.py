#!/usr/bin/env python3
"""
Test Flask startup and basic functionality
"""

import requests
import json
import time


def test_signup_with_otp():
    """Test the complete signup flow with OTP"""

    # Generate unique email with timestamp
    import time
    timestamp = str(int(time.time()))

    # Test data
    test_user = {
        "email": f"testuser{timestamp}@example.com",
        "password": "TestPass123!",
        "firstName": "Test",
        "lastName": "User",
        "phone": "1234567890"
    }

    print(f"🧪 Testing signup with email: {test_user['email']}")

    try:
        # Test signup
        response = requests.post(
            "http://127.0.0.1:5000/auth/signup", json=test_user)

        if response.status_code == 201:
            print("✅ Signup successful!")
            result = response.json()
            user_id = result.get('user', {}).get('id')
            print(f"📝 User ID: {user_id}")

            if user_id:
                # Test OTP verification with a test OTP
                print("🔐 Testing OTP verification...")
                otp_data = {
                    "otp": "123456",  # Test OTP
                    "userId": user_id
                }

                otp_response = requests.post(
                    "http://127.0.0.1:5000/auth/verify-otp", json=otp_data)
                print(
                    f"📱 OTP verification response: {otp_response.status_code}")

                if otp_response.status_code == 400:
                    print("✅ OTP endpoint working (expected 400 for wrong OTP)")
                elif otp_response.status_code == 200:
                    print("✅ OTP verification successful!")
                else:
                    print(f"❌ Unexpected OTP response: {otp_response.text}")

        else:
            print(f"❌ Signup failed: {response.status_code}")
            print(f"Response: {response.text}")

    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Flask backend on port 5000")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

    return True


if __name__ == "__main__":
    print("🚀 Starting Flask Backend Test...")

    # Wait for Flask to start
    print("⏳ Waiting for Flask backend to start...")
    time.sleep(3)

    # Test basic health check
    try:
        response = requests.get("http://127.0.0.1:5000/")
        if response.status_code == 200:
            print("✅ Flask backend is running!")
        else:
            print(f"⚠️  Flask backend returned: {response.status_code}")
    except:
        print("❌ Flask backend not responding")
        exit(1)

    # Test signup with OTP
    test_signup_with_otp()

    print("🏁 Test completed!")
